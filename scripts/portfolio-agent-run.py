#!/usr/bin/env python3
"""
portfolio-agent-run.py
======================
Agente autonomo de sincronizacion de portfolio profesional.

Invocado por PortfolioAgentService.php desde Portal Bienestar.
Usa archivos en --run-dir para comunicarse con el portal:
  - run_config.json : configuracion del agente escrita por PHP antes de lanzar
  - agent.log       : log cronologico (PHP hace polling)
  - status.json     : estado actual (paso, progreso, waiting)
  - approve_STEP    : creado por PHP cuando el usuario aprueba
  - cancel_STEP     : creado por PHP cuando el usuario cancela

Uso:
  python portfolio-agent-run.py --run-dir /ruta/run --portfolio-dir /ruta/portfolio

Configuracion (leida de run_config.json, con fallback a env vars):
  github_owner         : usuario/org en GitHub
  github_profile_repo  : repo del profile README
  gitlab_group         : grupo en GitLab
  gitlab_readme_repo   : repo del group README en GitLab
  github_token         : token GitHub (opcional si gh auth esta configurado)
  gitlab_token         : token GitLab (requerido para operaciones GitLab)
  auto_approve         : dict de pasos auto-aprobados {wait_proceed: bool, ...}
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import argparse
import base64
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ============================================================
# CONSTANTES (defaults, sobreescritos por run_config.json)
# ============================================================

GITHUB_OWNER        = "vladimiracunadev-create"
GITLAB_GROUP        = "vladimir.acuna.dev-group"
PORTFOLIO_WEB_REPO  = "vladimiracunadev-create.github.io"
GITHUB_PROFILE_REPO = GITHUB_OWNER
GITLAB_README_REPO  = GITLAB_GROUP

APPROVAL_TIMEOUT       = 300
APPROVAL_POLL_INTERVAL = 2

AGENT_VERSION = "1.0.0"


def load_run_config(run_dir: Path) -> dict:
    """
    Carga run_config.json escrito por PHP.
    Retorna el config o un dict vacio si no existe.
    """
    config_file = run_dir / "run_config.json"
    if config_file.exists():
        try:
            return json.loads(config_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


# ============================================================
# CLASE PRINCIPAL DEL AGENTE
# ============================================================

class PortfolioAgent:

    def __init__(self, run_dir: Path, portfolio_dir: Path, config: dict):
        self.run_dir       = run_dir
        self.portfolio_dir = portfolio_dir
        self.log_file      = run_dir / "agent.log"
        self.status_file   = run_dir / "status.json"
        self.snapshot_file = portfolio_dir / "data" / "portfolio-snapshot.json"
        self.api_dir       = portfolio_dir / "api" / "v1"
        self.scripts_dir   = portfolio_dir / "scripts"
        self.config        = config

        # Sobreescribir constantes globales con valores del config
        global GITHUB_OWNER, GITLAB_GROUP, PORTFOLIO_WEB_REPO, GITHUB_PROFILE_REPO, GITLAB_README_REPO
        if config.get("github_owner"):
            GITHUB_OWNER        = config["github_owner"]
            GITHUB_PROFILE_REPO = config.get("github_profile_repo", config["github_owner"])
        if config.get("gitlab_group"):
            GITLAB_GROUP       = config["gitlab_group"]
            GITLAB_README_REPO = config.get("gitlab_readme_repo", config["gitlab_group"])

        # Credenciales: config tiene prioridad sobre env vars
        self.github_token = config.get("github_token") or os.environ.get("GITHUB_TOKEN", "")
        self.gitlab_token = config.get("gitlab_token") or os.environ.get("GITLAB_TOKEN", "")

        # Auto-aprobacion de pasos
        self.auto_approve: dict = config.get("auto_approve", {})

        # Estado de ejecucion
        self.github_repos: dict = {}
        self.gitlab_repos: dict = {}
        self.snapshot:     dict = {}
        self.deltas:       dict = {}
        self.is_first_run: bool = False

    # ──────────────────────────────────────────
    # UTILIDADES DE LOGGING Y ESTADO
    # ──────────────────────────────────────────

    def log(self, msg: str, level: str = "INFO") -> None:
        ts   = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}"
        print(line, flush=True)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def set_status(self, status: str, step: str = None, pct: int = None, **extra) -> None:
        current = {}
        if self.status_file.exists():
            try:
                current = json.loads(self.status_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        current["status"]    = status
        current["updatedAt"] = datetime.now(timezone.utc).isoformat()
        if step is not None:
            current["currentStep"] = step
        if pct is not None:
            current["pct"] = pct
        current.update(extra)

        self.status_file.write_text(
            json.dumps(current, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # ──────────────────────────────────────────
    # SISTEMA DE APROBACION
    # ──────────────────────────────────────────

    def wait_approval(self, step_id: str, description: str) -> bool:
        """
        Pausa el agente y espera aprobacion del usuario.
        Si el paso esta en auto_approve, continua directamente sin esperar.
        Retorna True si aprobado, False si cancelado o timeout.
        """
        # Verificar auto-aprobacion configurada por el usuario
        if self.auto_approve.get(step_id, False):
            self.log(f"AUTO-APROBADO (configuracion): {description}", "INFO")
            return True

        approve_file = self.run_dir / f"approve_{step_id}"
        cancel_file  = self.run_dir / f"cancel_{step_id}"

        self.set_status("waiting", step_id, waitingFor=step_id, waitDescription=description)
        self.log(f"ESPERANDO APROBACION: {description}")
        self.log("Aprueba o cancela desde el portal web.", "INFO")

        start = time.time()
        while time.time() - start < APPROVAL_TIMEOUT:
            if approve_file.exists():
                self.log(f"Aprobado por el usuario: {description}", "INFO")
                return True
            if cancel_file.exists():
                self.log(f"Cancelado por el usuario: {description}", "WARN")
                return False
            time.sleep(APPROVAL_POLL_INTERVAL)

        self.log(f"Timeout ({APPROVAL_TIMEOUT}s) esperando aprobacion.", "WARN")
        return False

    # ──────────────────────────────────────────
    # EJECUCION DE COMANDOS
    # ──────────────────────────────────────────

    def run_gh(self, args: list, timeout: int = 60) -> tuple:
        """Ejecuta gh CLI y retorna (returncode, stdout)."""
        try:
            result = subprocess.run(
                ["gh"] + args,
                capture_output=True, text=True,
                timeout=timeout,
                cwd=str(self.portfolio_dir),
                encoding="utf-8", errors="replace"
            )
            return result.returncode, result.stdout.strip()
        except FileNotFoundError:
            return 1, "gh CLI no encontrado. Instala GitHub CLI: https://cli.github.com"
        except subprocess.TimeoutExpired:
            return 1, f"Timeout ({timeout}s) ejecutando: gh {' '.join(args)}"
        except Exception as e:
            return 1, str(e)

    def run_git(self, args: list, cwd: Path = None) -> tuple:
        """Ejecuta git y retorna (returncode, output)."""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True, text=True,
                timeout=120,
                cwd=str(cwd or self.portfolio_dir),
                encoding="utf-8", errors="replace"
            )
            return result.returncode, (result.stdout + result.stderr).strip()
        except Exception as e:
            return 1, str(e)

    def run_python_script(self, script: Path, timeout: int = 600) -> tuple:
        """Ejecuta un script Python del portfolio y retorna (success, output)."""
        if not script.exists():
            return False, f"Script no encontrado: {script}"
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True,
                timeout=timeout,
                cwd=str(self.portfolio_dir),
                encoding="utf-8", errors="replace"
            )
            output = (result.stdout + result.stderr)[:2000]
            return result.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, f"Timeout ({timeout}s) generando PDFs"
        except Exception as e:
            return False, str(e)

    def gitlab_get(self, endpoint: str) -> tuple:
        """GET a la API de GitLab. Retorna (status_code, data)."""
        return self._gitlab_request("GET", endpoint, data=None)

    def gitlab_put(self, endpoint: str, data: dict) -> tuple:
        """PUT a la API de GitLab. Retorna (status_code, data)."""
        return self._gitlab_request("PUT", endpoint, data=data)

    def _gitlab_request(self, method: str, endpoint: str, data) -> tuple:
        url = f"https://gitlab.com/api/v4/{endpoint}"
        headers = {
            "PRIVATE-TOKEN": self.gitlab_token,
            "Content-Type":  "application/json",
        }
        body = json.dumps(data).encode() if data else None
        try:
            req  = Request(url, data=body, headers=headers, method=method)
            resp = urlopen(req, timeout=30)
            resp_body = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(resp_body)
            except Exception:
                return resp.status, resp_body
        except HTTPError as e:
            return e.code, {"error": str(e)}
        except URLError as e:
            return 0, {"error": str(e)}
        except Exception as e:
            return 0, {"error": str(e)}

    # ──────────────────────────────────────────
    # UTILIDADES
    # ──────────────────────────────────────────

    @staticmethod
    def md5(content: str) -> str:
        return hashlib.md5(content.encode("utf-8", errors="replace")).hexdigest()

    def load_json(self, path: Path, default=None):
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return default if default is not None else {}

    def save_json(self, path: Path, data) -> None:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # ──────────────────────────────────────────
    # PASOS DEL AGENTE
    # ──────────────────────────────────────────

    def step_init(self) -> None:
        """PASO 1 — Carga snapshot existente o detecta primera ejecucion."""
        self.log("=" * 55)
        self.log("PASO 1: Inicializando agente Portfolio Sync v" + AGENT_VERSION)
        self.log("=" * 55)

        if self.snapshot_file.exists():
            self.snapshot = self.load_json(self.snapshot_file)
            last_updated  = self.snapshot.get("last_updated", "desconocido")
            gh_count      = len(self.snapshot.get("github_repos", {}))
            gl_count      = len(self.snapshot.get("gitlab_repos", {}))
            self.is_first_run = False
            self.log(f"Snapshot cargado. Ultimo update: {last_updated}")
            self.log(f"Repos en snapshot: {gh_count} GitHub, {gl_count} GitLab")
        else:
            self.snapshot     = {"github_repos": {}, "gitlab_repos": {}, "last_updated": None}
            self.is_first_run = True
            self.log("Primera ejecucion detectada — se realizara bootstrap completo.", "WARN")

        self.log(f"Portfolio dir: {self.portfolio_dir}")
        self.log(f"Run dir:       {self.run_dir}")

    def step_fetch_github(self) -> None:
        """PASO 2 — Lee todos los repos publicos de GitHub y sus READMEs."""
        self.log("=" * 55)
        self.log("PASO 2: Leyendo repositorios GitHub")
        self.log("=" * 55)

        rc, output = self.run_gh([
            "repo", "list", GITHUB_OWNER,
            "--json", "name,description,pushedAt,url,repositoryTopics,primaryLanguage,stargazerCount,isPrivate",
            "--limit", "100"
        ])

        if rc != 0:
            self.log(f"Error listando repos GitHub: {output}", "ERROR")
            self.log("Continuando con repos vacios.", "WARN")
            return

        try:
            repos_raw = json.loads(output) if output else []
        except json.JSONDecodeError:
            self.log(f"Error parseando JSON de GitHub: {output[:200]}", "ERROR")
            return

        self.log(f"Repos encontrados: {len(repos_raw)}")

        for repo in repos_raw:
            if repo.get("isPrivate"):
                continue

            name = repo["name"]

            # Omitir repos destino (no son fuente de experiencia)
            if name in (PORTFOLIO_WEB_REPO,):
                self.log(f"  [omitido] {name} (repo destino)")
                continue

            self.log(f"  Leyendo README de: {name}")
            readme_content = self._fetch_github_readme(name)

            language = ""
            if repo.get("primaryLanguage") and isinstance(repo["primaryLanguage"], dict):
                language = repo["primaryLanguage"].get("name", "")

            self.github_repos[name] = {
                "description":   repo.get("description") or "",
                "pushed_at":     repo.get("pushedAt") or "",
                "url":           repo.get("url") or "",
                "topics":        [t["name"] for t in repo.get("repositoryTopics", []) if isinstance(t, dict)],
                "language":      language,
                "stars":         repo.get("stargazerCount", 0),
                "readme_hash":   self.md5(readme_content),
                "readme_snippet": readme_content[:600],
            }

        self.log(f"GitHub: {len(self.github_repos)} repos publicos procesados")

    def _fetch_github_readme(self, repo_name: str) -> str:
        """Obtiene el contenido del README de un repo GitHub via gh CLI."""
        rc, b64 = self.run_gh(["api", f"repos/{GITHUB_OWNER}/{repo_name}/readme", "--jq", ".content"])
        if rc != 0:
            return ""
        try:
            clean = b64.replace("\\n", "").replace("\n", "")
            return base64.b64decode(clean).decode("utf-8", errors="replace")
        except Exception:
            return b64[:500]

    def step_fetch_gitlab(self) -> None:
        """PASO 3 — Lee repos del grupo GitLab."""
        self.log("=" * 55)
        self.log("PASO 3: Leyendo repositorios GitLab")
        self.log("=" * 55)

        if not self.gitlab_token:
            self.log("GITLAB_TOKEN no configurado — se intentara con repos publicos.", "WARN")

        code, projects = self.gitlab_get(
            f"groups/{GITLAB_GROUP}/projects?per_page=50&visibility=public&order_by=last_activity_at"
        )

        if code != 200:
            self.log(f"Error leyendo grupo GitLab (HTTP {code}): {str(projects)[:200]}", "ERROR")
            self.log("Continuando sin datos de GitLab.", "WARN")
            return

        if not isinstance(projects, list):
            self.log("Respuesta GitLab no es lista.", "ERROR")
            return

        self.log(f"Repos encontrados en GitLab: {len(projects)}")

        for repo in projects:
            name       = repo.get("path", "")
            project_id = repo.get("id")

            if not name or not project_id:
                continue

            # Omitir el repo README del grupo (es destino, no fuente)
            if name == GITLAB_README_REPO:
                self.log(f"  [omitido] {name} (repo destino)")
                continue

            self.log(f"  Leyendo README de: {name}")

            # Intentar obtener README
            readme_content = ""
            rc2, readme_data = self.gitlab_get(
                f"projects/{project_id}/repository/files/README.md/raw?ref=main"
            )
            if rc2 == 200 and isinstance(readme_data, str):
                readme_content = readme_data
            elif rc2 == 404:
                rc3, _ = self.gitlab_get(
                    f"projects/{project_id}/repository/files/README.md/raw?ref=master"
                )
                if rc3 == 200 and isinstance(_, str):
                    readme_content = _

            self.gitlab_repos[name] = {
                "description":    repo.get("description") or "",
                "pushed_at":      repo.get("last_activity_at") or "",
                "url":            repo.get("web_url") or "",
                "topics":         repo.get("topics", []),
                "language":       "",
                "readme_hash":    self.md5(readme_content),
                "readme_snippet": readme_content[:600],
                "project_id":     project_id,
            }

        self.log(f"GitLab: {len(self.gitlab_repos)} repos procesados")

    def step_detect_deltas(self) -> None:
        """PASO 4 — Compara repos actuales vs snapshot para detectar cambios."""
        self.log("=" * 55)
        self.log("PASO 4: Detectando cambios vs snapshot")
        self.log("=" * 55)

        snap_gh = self.snapshot.get("github_repos", {})
        snap_gl = self.snapshot.get("gitlab_repos", {})

        new_repos, updated_repos, unchanged = [], [], []

        # GitHub
        for name, current in self.github_repos.items():
            if name == GITHUB_PROFILE_REPO:
                continue  # lo manejamos por separado
            if name not in snap_gh:
                new_repos.append(f"github:{name}")
                self.log(f"  NUEVO (GitHub): {name}")
            elif (current["pushed_at"] != snap_gh[name].get("pushed_at") or
                  current["readme_hash"] != snap_gh[name].get("readme_hash")):
                updated_repos.append(f"github:{name}")
                self.log(f"  ACTUALIZADO (GitHub): {name} — pushed_at cambio o README distinto")
            else:
                unchanged.append(f"github:{name}")

        # GitLab
        for name, current in self.gitlab_repos.items():
            if name not in snap_gl:
                new_repos.append(f"gitlab:{name}")
                self.log(f"  NUEVO (GitLab): {name}")
            elif (current["pushed_at"] != snap_gl[name].get("pushed_at") or
                  current["readme_hash"] != snap_gl[name].get("readme_hash")):
                updated_repos.append(f"gitlab:{name}")
                self.log(f"  ACTUALIZADO (GitLab): {name}")
            else:
                unchanged.append(f"gitlab:{name}")

        # Detectar cambio en README del perfil GitHub
        github_profile_changed = False
        if GITHUB_PROFILE_REPO in self.github_repos:
            current_hash = self.github_repos[GITHUB_PROFILE_REPO]["readme_hash"]
            saved_hash   = snap_gh.get(GITHUB_PROFILE_REPO, {}).get("readme_hash", "")
            github_profile_changed = current_hash != saved_hash
            if github_profile_changed:
                self.log(f"  Cambio detectado en README del perfil GitHub")

        # Detectar cambio en README del grupo GitLab
        gitlab_group_changed = False
        # Lo inferimos de si hay repos nuevos/actualizados en GitLab
        gitlab_group_changed = any("gitlab:" in r for r in new_repos + updated_repos)

        total = len(new_repos) + len(updated_repos)
        self.log(f"Resumen: {len(new_repos)} nuevos, {len(updated_repos)} actualizados, {len(unchanged)} sin cambios")

        self.deltas = {
            "new":                    new_repos,
            "updated":                updated_repos,
            "unchanged":              unchanged,
            "total":                  total,
            "github_profile_changed": github_profile_changed,
            "gitlab_group_changed":   gitlab_group_changed,
        }

        # Actualizar status con resumen de cambios
        self.set_status("running", "detect_deltas",
                        deltasSummary=f"{len(new_repos)} nuevos, {len(updated_repos)} actualizados")

    def step_update_jsons(self) -> None:
        """PASO 6 — Actualiza los JSONs del portfolio de forma aditiva (nunca destruye)."""
        self.log("=" * 55)
        self.log("PASO 6: Actualizando JSONs del portfolio (aditivo)")
        self.log("=" * 55)

        changed_names = set()
        for ref in self.deltas.get("new", []) + self.deltas.get("updated", []):
            changed_names.add(ref.split(":", 1)[1])

        if not changed_names:
            self.log("Sin repos con cambios — nada que actualizar en JSONs.")
            return

        # Cargar projects.json actual
        projects_file = self.api_dir / "projects.json"
        projects      = self.load_json(projects_file, {})
        updated_count = 0

        for repo_name in changed_names:
            repo = self.github_repos.get(repo_name) or self.gitlab_repos.get(repo_name)
            if not repo:
                continue

            if repo_name in projects:
                # Update aditivo: solo sobreescribir si el nuevo valor es mejor
                existing = projects[repo_name]
                if repo.get("description"):
                    existing["description"] = repo["description"]
                if repo.get("pushed_at"):
                    existing["last_pushed"] = repo["pushed_at"]
                if repo.get("topics"):
                    existing["topics"] = repo["topics"]
                if repo.get("stars", 0) > 0:
                    existing["stars"] = repo["stars"]
                self.log(f"  Actualizado: {repo_name}")
            else:
                # Nuevo repo: crear entrada completa
                projects[repo_name] = {
                    "name":        repo_name,
                    "description": repo.get("description", ""),
                    "url":         repo.get("url", ""),
                    "topics":      repo.get("topics", []),
                    "language":    repo.get("language", ""),
                    "stars":       repo.get("stars", 0),
                    "last_pushed": repo.get("pushed_at", ""),
                    "status":      "active",
                    "readme_snippet": repo.get("readme_snippet", "")[:300],
                }
                self.log(f"  Nuevo repo agregado: {repo_name}")

            updated_count += 1

        if updated_count > 0:
            # Backup antes de modificar
            backup = self.api_dir / "projects.json.bak"
            if projects_file.exists():
                backup.write_bytes(projects_file.read_bytes())
            self.save_json(projects_file, projects)
            self.log(f"  projects.json guardado ({updated_count} repos actualizados, backup en .bak)")
        else:
            self.log("  Sin cambios efectivos en projects.json")

        # Actualizar meta.json con timestamp
        meta_file = self.api_dir / "meta.json"
        meta      = self.load_json(meta_file, {})
        meta["last_agent_sync"] = datetime.now(timezone.utc).isoformat()
        meta["agent_version"]   = AGENT_VERSION
        self.save_json(meta_file, meta)
        self.log("  meta.json actualizado")

    def step_update_seo(self) -> None:
        """PASO 7 — Actualiza sitemap.xml, robots.txt y llm.txt."""
        self.log("=" * 55)
        self.log("PASO 7: Actualizando archivos SEO")
        self.log("=" * 55)

        today = datetime.now().strftime("%Y-%m-%d")

        # sitemap.xml — actualizar <lastmod>
        sitemap = self.portfolio_dir / "sitemap.xml"
        if sitemap.exists():
            content     = sitemap.read_text(encoding="utf-8")
            new_content = re.sub(
                r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
                f"<lastmod>{today}</lastmod>",
                content
            )
            if new_content != content:
                sitemap.write_text(new_content, encoding="utf-8")
                self.log(f"  sitemap.xml: fecha actualizada a {today}")
            else:
                self.log("  sitemap.xml: ya estaba actualizado")
        else:
            self.log("  sitemap.xml no encontrado", "WARN")

        # llm.txt — actualizar fecha
        llm = self.portfolio_dir / "llm.txt"
        if llm.exists():
            content     = llm.read_text(encoding="utf-8")
            new_content = re.sub(
                r"(Actualizado|Updated|Last[\s\-]updated):\s*\d{4}-\d{2}-\d{2}",
                lambda m: m.group(0).split(":")[0] + f": {today}",
                content,
                flags=re.IGNORECASE
            )
            if new_content != content:
                llm.write_text(new_content, encoding="utf-8")
                self.log(f"  llm.txt: fecha actualizada a {today}")
            else:
                self.log("  llm.txt: sin cambios de fecha requeridos")
        else:
            self.log("  llm.txt no encontrado", "WARN")

        # robots.txt — verificar que este correcto (no modificamos, solo validamos)
        robots = self.portfolio_dir / "robots.txt"
        if robots.exists():
            self.log("  robots.txt: OK (sin cambios)")
        else:
            self.log("  robots.txt no encontrado", "WARN")

    def step_regen_pdfs(self) -> bool:
        """PASO 9 — Regenera todos los PDFs via el script existente."""
        self.log("=" * 55)
        self.log("PASO 9: Regenerando PDFs (30 archivos, 6 idiomas)")
        self.log("=" * 55)

        # Backup del directorio assets antes de regenerar
        assets_dir = self.portfolio_dir / "assets"
        backup_dir = self.portfolio_dir / "assets" / "backups"
        if assets_dir.exists() and backup_dir.exists():
            self.log("  Directorio de backups detectado — los scripts existentes haran backup automatico")

        # Intentar con generate-all-languages.py (genera 12 CVs)
        script_all = self.scripts_dir / "generate-all-languages.py"
        if script_all.exists():
            self.log("  Ejecutando generate-all-languages.py...")
            ok, output = self.run_python_script(script_all, timeout=600)
            if ok:
                self.log("  generate-all-languages.py completado exitosamente")
            else:
                self.log(f"  Error en generate-all-languages.py: {output[:400]}", "ERROR")
            # Mostrar primeras lineas del output
            for line in output.split("\n")[:8]:
                if line.strip():
                    self.log(f"    {line.strip()}")
        else:
            self.log(f"  Script no encontrado: {script_all}", "WARN")

        # Intentar con generate-portfolio.py (genera portafolios)
        script_portfolio = self.scripts_dir / "generate-portfolio.py"
        if script_portfolio.exists():
            self.log("  Ejecutando generate-portfolio.py...")
            ok, output = self.run_python_script(script_portfolio, timeout=600)
            if ok:
                self.log("  generate-portfolio.py completado exitosamente")
            else:
                self.log(f"  Error en generate-portfolio.py: {output[:400]}", "ERROR")
        else:
            self.log(f"  Script no encontrado: {script_portfolio}", "WARN")

        # Contar PDFs generados
        if assets_dir.exists():
            pdfs = list(assets_dir.glob("*.pdf"))
            self.log(f"  PDFs en /assets: {len(pdfs)} archivos")

        return True

    def step_push_portfolio(self) -> bool:
        """PASO 11 — Commit y push del portfolio web al repositorio."""
        self.log("=" * 55)
        self.log("PASO 11: Commit y push portfolio web")
        self.log("=" * 55)

        changed = self.deltas.get("new", []) + self.deltas.get("updated", [])
        today   = datetime.now().strftime("%Y-%m-%d")
        msg     = f"agent: sync portfolio — {len(changed)} repos [{today}]"

        # git add -A
        rc, out = self.run_git(["add", "-A"])
        if rc != 0:
            self.log(f"  Error en git add: {out}", "ERROR")
            return False
        self.log("  git add -A: OK")

        # git status --short para ver que se va a commitear
        rc, staged = self.run_git(["diff", "--cached", "--name-only"])
        if staged:
            self.log(f"  Archivos staged: {staged[:300]}")
        else:
            self.log("  Nada que commitear — working tree limpio")
            return True

        # git commit
        rc, out = self.run_git(["commit", "-m", msg])
        if rc != 0 and "nothing to commit" not in out:
            self.log(f"  Error en git commit: {out}", "ERROR")
            return False
        self.log(f"  git commit: {msg[:80]}")

        # git push
        rc, out = self.run_git(["push", "origin", "main"])
        if rc != 0:
            self.log(f"  Error en git push: {out}", "ERROR")
            return False
        self.log("  git push origin main: OK")

        return True

    def step_push_github_profile(self) -> bool:
        """PASO 13 — Actualiza el README del perfil de GitHub."""
        self.log("=" * 55)
        self.log("PASO 13: Actualizando README perfil GitHub")
        self.log("=" * 55)

        today = datetime.now().strftime("%Y-%m-%d")

        # Leer README actual via gh API
        rc, b64_content = self.run_gh([
            "api", f"repos/{GITHUB_OWNER}/{GITHUB_PROFILE_REPO}/contents/README.md",
            "--jq", ".content"
        ])
        if rc != 0:
            self.log(f"  No se pudo leer README del perfil: {b64_content}", "ERROR")
            return False

        # Decodificar
        try:
            clean = b64_content.replace("\\n", "").replace("\n", "")
            current_readme = base64.b64decode(clean).decode("utf-8", errors="replace")
        except Exception as e:
            self.log(f"  Error decodificando README: {e}", "ERROR")
            return False

        # Actualizar fecha — buscar patrones comunes
        new_readme = current_readme
        patterns = [
            (r"\*\*Actualizado:\*\*\s*\d{4}-\d{2}-\d{2}", f"**Actualizado:** {today}"),
            (r"\*\*Updated:\*\*\s*\d{4}-\d{2}-\d{2}",     f"**Updated:** {today}"),
            (r"<!-- LAST_UPDATE -->[^<]*<!-- /LAST_UPDATE -->",
             f"<!-- LAST_UPDATE -->{today}<!-- /LAST_UPDATE -->"),
            (r"!\[Last update\]\([^)]*\d{4}-\d{2}-\d{2}[^)]*\)",
             f"![Last update](https://img.shields.io/badge/sync-{today.replace('-', '--')}-blue)"),
        ]
        for pattern, replacement in patterns:
            new_readme = re.sub(pattern, replacement, new_readme)

        if new_readme == current_readme:
            self.log("  README del perfil ya esta actualizado — sin cambios necesarios")
            return True

        # Obtener SHA del archivo (necesario para la API PUT)
        rc_sha, sha_out = self.run_gh([
            "api", f"repos/{GITHUB_OWNER}/{GITHUB_PROFILE_REPO}/contents/README.md",
            "--jq", ".sha"
        ])
        if rc_sha != 0:
            self.log(f"  Error obteniendo SHA del README: {sha_out}", "ERROR")
            return False
        sha = sha_out.strip().strip('"')

        # Encodear nuevo contenido
        new_b64 = base64.b64encode(new_readme.encode("utf-8")).decode("ascii")

        # Escribir payload a archivo temporal (evita problemas de quoting en Windows)
        # NOTA: Tecnica documentada en memory/feedback_sync_portfolio_rules.md
        payload_file = self.run_dir / "gh_payload_profile.json"
        payload = {
            "message": f"agent: sync profile README [{today}]",
            "content": new_b64,
            "sha":     sha,
        }
        payload_file.write_text(json.dumps(payload), encoding="utf-8")

        # PUT via gh api con --input (evita shell quoting issues en Windows)
        rc_put, out_put = self.run_gh([
            "api", "--method", "PUT",
            f"repos/{GITHUB_OWNER}/{GITHUB_PROFILE_REPO}/contents/README.md",
            "--input", str(payload_file)
        ])

        if rc_put == 0:
            self.log("  README perfil GitHub actualizado exitosamente")
            return True
        else:
            self.log(f"  Error actualizando README (rc={rc_put}): {out_put[:400]}", "ERROR")
            return False

    def step_push_gitlab(self) -> bool:
        """PASO 15 — Actualiza el README del grupo de GitLab."""
        self.log("=" * 55)
        self.log("PASO 15: Actualizando README grupo GitLab")
        self.log("=" * 55)

        if not self.gitlab_token:
            self.log("  GITLAB_TOKEN no configurado — omitiendo.", "WARN")
            return True

        today = datetime.now().strftime("%Y-%m-%d")

        # Buscar el proyecto README del grupo
        code, projects = self.gitlab_get(
            f"groups/{GITLAB_GROUP}/projects?search={GITLAB_README_REPO}&per_page=10"
        )
        if code != 200 or not isinstance(projects, list) or not projects:
            self.log(f"  No se encontro proyecto GitLab '{GITLAB_README_REPO}' (HTTP {code})", "ERROR")
            return False

        # Buscar el que coincide exactamente
        project = next((p for p in projects if p.get("path") == GITLAB_README_REPO), projects[0])
        project_id = project["id"]
        self.log(f"  Proyecto GitLab encontrado: {project.get('name_with_namespace')} (id={project_id})")

        # Leer README actual
        code2, readme_data = self.gitlab_get(
            f"projects/{project_id}/repository/files/README.md/raw?ref=main"
        )
        if code2 != 200:
            # Intentar con master
            code2, readme_data = self.gitlab_get(
                f"projects/{project_id}/repository/files/README.md/raw?ref=master"
            )
        if code2 != 200:
            self.log(f"  No se pudo leer README GitLab (HTTP {code2})", "ERROR")
            return False

        current_readme = readme_data if isinstance(readme_data, str) else json.dumps(readme_data)

        # Actualizar fecha
        new_readme = re.sub(
            r"\*\*Actualizado:\*\*\s*\d{4}-\d{2}-\d{2}",
            f"**Actualizado:** {today}",
            current_readme
        )
        new_readme = re.sub(
            r"<!-- LAST_UPDATE -->[^<]*<!-- /LAST_UPDATE -->",
            f"<!-- LAST_UPDATE -->{today}<!-- /LAST_UPDATE -->",
            new_readme
        )

        if new_readme == current_readme:
            self.log("  README GitLab ya estaba actualizado — sin cambios")
            return True

        # Determinar branch
        branch = "main"

        # PUT via API
        code3, result = self.gitlab_put(
            f"projects/{project_id}/repository/files/README.md",
            {
                "branch":         branch,
                "content":        new_readme,
                "commit_message": f"agent: sync group README [{today}]",
                "encoding":       "text",
            }
        )

        if code3 in (200, 201):
            self.log("  README grupo GitLab actualizado exitosamente")
            return True
        else:
            self.log(f"  Error actualizando README GitLab (HTTP {code3}): {str(result)[:300]}", "ERROR")
            return False

    # ──────────────────────────────────────────
    # SNAPSHOT
    # ──────────────────────────────────────────

    def save_snapshot(self) -> None:
        """Guarda el snapshot actualizado en data/portfolio-snapshot.json."""
        snapshot = {
            "last_updated":  datetime.now(timezone.utc).isoformat(),
            "agent_version": AGENT_VERSION,
            "github_repos":  self.github_repos,
            "gitlab_repos":  self.gitlab_repos,
        }
        self.snapshot_file.parent.mkdir(parents=True, exist_ok=True)
        self.save_json(self.snapshot_file, snapshot)
        self.log("Snapshot actualizado guardado en data/portfolio-snapshot.json")

    # ──────────────────────────────────────────
    # ORQUESTADOR PRINCIPAL
    # ──────────────────────────────────────────

    def run(self) -> None:
        """Ejecuta el flujo completo del agente, paso a paso."""
        self.log(f"=== PORTFOLIO AGENT v{AGENT_VERSION} INICIADO ===")

        try:
            # ── PASO 1: Init ─────────────────────────────────
            self.set_status("running", "init", pct=5)
            self.step_init()

            # ── PASO 2: GitHub ───────────────────────────────
            self.set_status("running", "fetch_github", pct=15)
            self.step_fetch_github()

            # ── PASO 3: GitLab ───────────────────────────────
            self.set_status("running", "fetch_gitlab", pct=25)
            self.step_fetch_gitlab()

            # ── PASO 4: Detectar deltas ──────────────────────
            self.set_status("running", "detect_deltas", pct=35)
            self.step_detect_deltas()

            # Si no hay cambios y no es primera vez, terminamos sin actualizar
            if self.deltas["total"] == 0 and not self.is_first_run:
                self.log("Sin cambios detectados. Portfolio ya esta actualizado.", "WARN")
                self.save_snapshot()
                self.set_status("done", "done", pct=100,
                                summary="Sin cambios detectados. Portfolio ya estaba actualizado.")
                return

            # ── PASO 5: Aprobacion — proceder ───────────────
            self.set_status("running", "wait_proceed", pct=38)
            n_new = len(self.deltas["new"])
            n_upd = len(self.deltas["updated"])
            summary_text = f"{n_new} nuevos, {n_upd} actualizados"

            self.log(f"Cambios detectados: {summary_text}")
            for r in self.deltas["new"]:
                self.log(f"  + {r}")
            for r in self.deltas["updated"]:
                self.log(f"  ~ {r}")

            if not self.wait_approval("wait_proceed", f"Proceder con actualizacion ({summary_text})"):
                self.set_status("cancelled", "wait_proceed", pct=38, summary="Cancelado por el usuario.")
                return

            # ── PASO 6: Actualizar JSONs ─────────────────────
            self.set_status("running", "update_jsons", pct=45)
            self.step_update_jsons()

            # ── PASO 7: Actualizar SEO ───────────────────────
            self.set_status("running", "update_seo", pct=52)
            self.step_update_seo()

            # ── PASO 8: Aprobacion — PDFs ────────────────────
            self.set_status("running", "wait_pdfs", pct=55)
            if self.wait_approval("wait_pdfs", "Regenerar 30 PDFs en 6 idiomas (puede tardar 3-5 min)"):
                # ── PASO 9: Regenerar PDFs ───────────────────
                self.set_status("running", "regen_pdfs", pct=60)
                self.step_regen_pdfs()
            else:
                self.log("Regeneracion de PDFs omitida por el usuario.", "WARN")
                # Marcar pasos de PDF como skipped en status
                self.set_status("running", "regen_pdfs", pct=68)

            # ── PASO 10: Aprobacion — push portfolio ─────────
            self.set_status("running", "wait_push_portfolio", pct=72)
            if self.wait_approval("wait_push_portfolio", "Publicar todos los cambios en el portfolio web (git push)"):
                # ── PASO 11: Push portfolio ───────────────────
                self.set_status("running", "push_portfolio", pct=78)
                self.step_push_portfolio()
            else:
                self.log("Push del portfolio omitido.", "WARN")

            # ── PASO 12: Aprobacion — README GitHub ──────────
            if self.deltas.get("github_profile_changed") or self.deltas["total"] > 0:
                self.set_status("running", "wait_push_github", pct=83)
                if self.wait_approval("wait_push_github", "Actualizar README del perfil de GitHub"):
                    # ── PASO 13: Push GitHub profile ─────────
                    self.set_status("running", "push_github", pct=88)
                    self.step_push_github_profile()
                else:
                    self.log("README perfil GitHub omitido.", "WARN")
            else:
                self.log("README perfil GitHub: sin cambios relevantes — saltando.")

            # ── PASO 14: Aprobacion — README GitLab ──────────
            if self.deltas.get("gitlab_group_changed") or self.deltas["total"] > 0:
                self.set_status("running", "wait_push_gitlab", pct=91)
                if self.wait_approval("wait_push_gitlab", "Actualizar README del grupo de GitLab"):
                    # ── PASO 15: Push GitLab ──────────────────
                    self.set_status("running", "push_gitlab", pct=95)
                    self.step_push_gitlab()
                else:
                    self.log("README GitLab omitido.", "WARN")
            else:
                self.log("README GitLab: sin cambios relevantes — saltando.")

            # ── GUARDAR SNAPSHOT ─────────────────────────────
            self.save_snapshot()

            # ── DONE ─────────────────────────────────────────
            final_summary = f"Completado: {self.deltas['total']} cambios procesados."
            self.set_status("done", "done", pct=100, summary=final_summary)
            self.log("=" * 55)
            self.log("=== PORTFOLIO AGENT COMPLETADO EXITOSAMENTE ===")
            self.log("=" * 55)

        except KeyboardInterrupt:
            self.log("Agente interrumpido manualmente.", "WARN")
            self.set_status("cancelled", summary="Interrumpido manualmente.")

        except Exception as e:
            self.log(f"ERROR INESPERADO: {e}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            self.set_status("error", pct=None, error=str(e))


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Portfolio Agent — sincronizacion autonoma de portfolio profesional"
    )
    parser.add_argument("--run-dir",       required=True, help="Directorio del run actual")
    parser.add_argument("--portfolio-dir", required=True, help="Directorio raiz del portfolio")
    args = parser.parse_args()

    run_dir       = Path(args.run_dir)
    portfolio_dir = Path(args.portfolio_dir)

    if not run_dir.exists():
        print(f"ERROR: --run-dir no existe: {run_dir}", file=sys.stderr)
        sys.exit(1)

    if not portfolio_dir.exists():
        print(f"ERROR: --portfolio-dir no existe: {portfolio_dir}", file=sys.stderr)
        sys.exit(1)

    # Cargar configuracion escrita por PHP antes de lanzar el proceso
    config = load_run_config(run_dir)

    agent = PortfolioAgent(run_dir, portfolio_dir, config)
    agent.run()


if __name__ == "__main__":
    main()
