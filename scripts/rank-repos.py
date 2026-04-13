#!/usr/bin/env python3
"""
rank-repos.py — Ranks public GitHub repos by quality and updates pinned profile repos.

Usage:
  python scripts/rank-repos.py              # dry-run: show ranking, no changes
  python scripts/rank-repos.py --apply      # update pinned repos (top 6)
  python scripts/rank-repos.py --force      # re-analyze all repos ignoring cache
  python scripts/rank-repos.py --apply --force  # force-reanalyze + pin

Scoring (100 pts total):
  Documentation   30 pts  (README substance, depth, CHANGELOG, docs/, RECRUITER.md)
  Reproducibility 20 pts  (Dockerfile, docker-compose, GitHub Actions, Makefile)
  Code quality    15 pts  (tests, releases, GitHub issue/PR templates)
  Observability   15 pts  (Prometheus/Grafana, health endpoints, K8s)
  Activity        10 pts  (recency, stars)
  Stack diversity 10 pts  (polyglot languages, 2 pts each up to 5)

Cache:
  Scores are cached in data/repo-scores.json keyed by repo name.
  Only repos whose pushed_at changed since the last run are re-analyzed.
  First run is slow (all repos analyzed). Subsequent runs are fast.

Pinning:
  Top 6 public repos are pinned to the GitHub profile via GraphQL API.
  Requires: gh auth status with repo scope.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

OWNER = "vladimiracunadev-create"

# Repos permanently excluded from ranking + pinning
EXCLUDED = {
    "rootcause-windows-inspector",
    "rootcause-landing",
    "vladimiracunadev-create",          # profile README repo
    "vladimiracunadev-create.github.io",  # portfolio site (pinned separately if desired)
}

CACHE_FILE = Path(__file__).parent.parent / "data" / "repo-scores.json"
TOP_N_PINNED = 6

# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd: str) -> tuple[str, int]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip(), result.returncode


def gh(endpoint: str, extra: str = "") -> tuple[dict | list | None, int]:
    out, code = run(f"gh api {endpoint} {extra}")
    if code != 0 or not out:
        return None, code
    try:
        return json.loads(out), 0
    except json.JSONDecodeError:
        return None, 1



# ── Repo listing ──────────────────────────────────────────────────────────────

def fetch_public_repos() -> list[dict]:
    """Return all public non-excluded repos for OWNER."""
    data, code = gh(
        f"users/{OWNER}/repos",
        "--paginate --jq '[.[] | {name,description,pushedAt:(.pushed_at),stargazerCount:(.stargazers_count),forkCount:(.forks_count),isFork:(.fork),isPrivate:(.private),languages_url}]'"
    )
    if data is None:
        # fallback: use gh repo list JSON
        out, _ = run(
            f"gh repo list {OWNER} --json name,description,pushedAt,stargazerCount,"
            "forkCount,isFork,isPrivate,languages --limit 50"
        )
        if not out:
            print("[ERROR] Could not fetch repo list", file=sys.stderr)
            sys.exit(1)
        all_repos = json.loads(out)
    else:
        all_repos = data

    return [
        r for r in all_repos
        if not r.get("isPrivate", r.get("private", False))
        and r["name"] not in EXCLUDED
    ]


# ── File-tree analysis ────────────────────────────────────────────────────────

def get_file_tree(repo: str) -> set[str]:
    """Return set of lowercase file paths in the repo (recursive)."""
    data, code = gh(f"repos/{OWNER}/{repo}/git/trees/HEAD?recursive=1")
    if data is None or "tree" not in data:
        return set()
    return {item["path"].lower() for item in data["tree"] if item["type"] == "blob"}


def get_readme(repo: str) -> str:
    """Return README content as plain text (decoded from base64)."""
    import base64
    data, code = gh(f"repos/{OWNER}/{repo}/readme")
    if data is None or "content" not in data:
        return ""
    try:
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except Exception:
        return ""


def get_release_count(repo: str) -> int:
    data, _ = gh(f"repos/{OWNER}/{repo}/releases?per_page=5")
    if data is None:
        return 0
    return len(data) if isinstance(data, list) else 0


# ── Scoring ───────────────────────────────────────────────────────────────────

OBS_KEYWORDS = re.compile(
    r"prometheus|grafana|jaeger|zipkin|opentelemetry|otel|elk|loki|datadog",
    re.IGNORECASE,
)
HEALTH_KEYWORDS = re.compile(
    r"/health|/metrics|/readiness|/liveness|healthcheck|health[_\s-]endpoint",
    re.IGNORECASE,
)
K8S_PATTERNS = {"k8s", "kubernetes", "helm", "manifests"}


def has_k8s(files: set[str]) -> bool:
    return any(
        any(kw in f for kw in K8S_PATTERNS)
        for f in files
    ) or any(f.endswith(".yaml") and ("deploy" in f or "manifest" in f or "k8s" in f) for f in files)


def score_repo(repo_meta: dict) -> dict:
    """
    Analyze one repo and return a score breakdown dict.
    Makes 3–5 gh API calls per repo.
    """
    name = repo_meta["name"]
    print(f"  -> Analyzing {name} ...", end=" ", flush=True)

    files = get_file_tree(name)
    readme = get_readme(name)
    releases = get_release_count(name)

    breakdown = {}

    # ── Documentation (30 pts) ──────────────────────────────────────────────
    readme_len = len(readme)
    breakdown["readme_substance"] = 10 if readme_len > 1500 else (5 if readme_len > 500 else 0)

    # depth: has >=3 headings and >=1 code block
    heading_count = len(re.findall(r"^#{1,3} .+", readme, re.MULTILINE))
    code_block_count = readme.count("```")
    breakdown["readme_depth"] = 5 if heading_count >= 3 and code_block_count >= 2 else 0

    breakdown["changelog"] = 3 if any("changelog" in f for f in files) else 0
    breakdown["security_contributing"] = 2 if any(
        f in files for f in ("security.md", "contributing.md")
    ) else 0
    breakdown["docs_dir"] = 5 if any(f.startswith("docs/") for f in files) else 0
    breakdown["recruiter_md"] = 5 if "recruiter.md" in files else 0

    # ── Reproducibility (20 pts) ────────────────────────────────────────────
    breakdown["dockerfile"] = 5 if any("dockerfile" in f for f in files) else 0
    breakdown["docker_compose"] = 5 if any(
        "docker-compose" in f or "compose.yml" in f or "compose.yaml" in f
        for f in files
    ) else 0
    breakdown["github_actions"] = 7 if any(f.startswith(".github/workflows/") for f in files) else 0
    breakdown["makefile"] = 3 if "makefile" in files else 0

    # ── Code quality (15 pts) ───────────────────────────────────────────────
    has_tests = any(
        f.startswith("test") or "/test" in f or "spec" in f or "_test." in f
        for f in files
    )
    breakdown["tests"] = 8 if has_tests else 0
    breakdown["releases"] = min(releases * 2, 4)  # 2 pts per release, max 4
    breakdown["github_templates"] = 3 if any(
        ".github/issue_template" in f or ".github/pull_request_template" in f
        or "issue_templates" in f
        for f in files
    ) else 0

    # ── Observability (15 pts) ──────────────────────────────────────────────
    breakdown["observability"] = 8 if OBS_KEYWORDS.search(readme) else 0
    breakdown["health_endpoints"] = 4 if HEALTH_KEYWORDS.search(readme) else 0
    breakdown["k8s"] = 3 if has_k8s(files) else 0

    # ── Activity (10 pts) ───────────────────────────────────────────────────
    pushed_at_str = repo_meta.get("pushedAt", "")
    if pushed_at_str:
        try:
            pushed_dt = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            days_ago = (datetime.now(timezone.utc) - pushed_dt).days
            if days_ago <= 30:
                breakdown["recency"] = 5
            elif days_ago <= 90:
                breakdown["recency"] = 3
            elif days_ago <= 180:
                breakdown["recency"] = 1
            else:
                breakdown["recency"] = 0
        except ValueError:
            breakdown["recency"] = 0
    else:
        breakdown["recency"] = 0

    stars = repo_meta.get("stargazerCount", repo_meta.get("stargazers_count", 0)) or 0
    breakdown["stars"] = min(stars * 2, 5)  # 2 pts per star, max 5

    # ── Stack diversity (10 pts) ────────────────────────────────────────────
    langs = repo_meta.get("languages", [])
    if isinstance(langs, list):
        lang_count = len(langs)
    else:
        lang_count = 0
    breakdown["polyglot"] = min(lang_count * 2, 10)

    total = sum(breakdown.values())
    print(f"{total} pts")

    return {
        "name": name,
        "total": total,
        "breakdown": breakdown,
        "pushed_at": repo_meta.get("pushedAt", ""),
        "description": repo_meta.get("description", "") or "",
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }


# ── Cache management ──────────────────────────────────────────────────────────

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ── GitHub pinning ────────────────────────────────────────────────────────────

def print_pinning_guide(repo_names: list[str]) -> None:
    """
    GitHub does not expose profile-pinning via its public GraphQL/REST API.
    The `updatePinnedItems` mutation only exists in the internal API.

    Print a clear guide for manual pinning — takes < 30 seconds on the web.
    """
    print("\n" + "-" * 65)
    print("MANUAL PINNING REQUIRED (GitHub API limitation)")
    print("-" * 65)
    print(f"  1. Open: https://github.com/{OWNER}")
    print("  2. Click 'Customize your pins' (top-right of pinned section)")
    print("  3. Select these repos in order:")
    for i, name in enumerate(repo_names, 1):
        print(f"       {i}. {name}")
    print("  4. Save")
    print("-" * 65)


# ── Display ───────────────────────────────────────────────────────────────────

def print_ranking(ranked: list[dict], top_n: int = TOP_N_PINNED) -> None:
    print("\n" + "=" * 65)
    print(f"{'RANK':<5} {'REPO':<38} {'SCORE':>5}")
    print("-" * 65)
    for i, entry in enumerate(ranked, 1):
        pin_marker = " [PIN]" if i <= top_n else ""
        print(f"  {i:<4} {entry['name']:<38} {entry['total']:>3}/100{pin_marker}")
    print("=" * 65)
    print(f"\n[PIN] = will be pinned (top {top_n})")

    print("\nTop repo breakdown:")
    for entry in ranked[:top_n]:
        bd = entry["breakdown"]
        print(
            f"  {entry['name']:35} "
            f"docs={sum(bd.get(k,0) for k in ['readme_substance','readme_depth','changelog','security_contributing','docs_dir','recruiter_md'])}/30 "
            f"repro={sum(bd.get(k,0) for k in ['dockerfile','docker_compose','github_actions','makefile'])}/20 "
            f"qual={sum(bd.get(k,0) for k in ['tests','releases','github_templates'])}/15 "
            f"obs={sum(bd.get(k,0) for k in ['observability','health_endpoints','k8s'])}/15 "
            f"act={sum(bd.get(k,0) for k in ['recency','stars'])}/10 "
            f"poly={bd.get('polyglot',0)}/10"
        )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    apply = "--apply" in sys.argv
    force = "--force" in sys.argv

    print(f"[rank-repos] {'DRY-RUN' if not apply else 'APPLY'} mode  {'| --force' if force else ''}")
    print(f"Owner: {OWNER}  |  Top {TOP_N_PINNED} will be pinned\n")

    # 1. Fetch all public repos
    print("Fetching public repo list ...")
    repos = fetch_public_repos()
    print(f"Found {len(repos)} public repos to rank.\n")

    # 2. Load cache
    cache = load_cache()
    updated_cache = dict(cache)

    # 3. Analyze repos (incremental)
    scores: list[dict] = []
    fresh_count = 0
    cached_count = 0

    for repo_meta in repos:
        name = repo_meta["name"]
        pushed_at = repo_meta.get("pushedAt", "")

        cached = cache.get(name)
        if not force and cached and cached.get("pushed_at") == pushed_at:
            # Use cached score
            scores.append(cached)
            cached_count += 1
            continue

        # Fresh analysis
        fresh_count += 1
        entry = score_repo(repo_meta)
        scores.append(entry)
        updated_cache[name] = entry

    print(f"\nAnalyzed: {fresh_count} fresh, {cached_count} from cache.")

    # 4. Save updated cache
    save_cache(updated_cache)
    print(f"Cache saved -> {CACHE_FILE}")

    # 5. Rank
    ranked = sorted(scores, key=lambda x: x["total"], reverse=True)
    top_repos = [r["name"] for r in ranked[:TOP_N_PINNED]]

    print_ranking(ranked)

    # 6. Print pinning guide
    print_pinning_guide(top_repos)

    if apply:
        print("\n[DONE] Ranking complete. Follow the guide above to pin repos.")
    else:
        print("\nRun with --apply to confirm this ranking and print the pinning guide.")
        print("Run with --force to re-analyze all repos regardless of cache.")


if __name__ == "__main__":
    main()
