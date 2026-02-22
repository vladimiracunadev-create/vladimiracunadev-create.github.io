const $ = (s, e = document) => e.querySelector(s);
const $$ = (s, e = document) => Array.from(e.querySelectorAll(s));
const LEVELS = { recruiter: 0, normal: 1, deep: 2 };

function setView(view) {
  document.body.dataset.view = view;
  localStorage.setItem("portfolio_view", view);
  $$("[data-view-btn]").forEach(btn => {
    const on = btn.dataset.viewBtn === view;
    btn.classList.toggle("is-active", on);
    btn.setAttribute("aria-selected", String(on));
  });
  const current = LEVELS[view] ?? 1;
  $$("[data-min-level]").forEach(el => {
    const min = Number(el.getAttribute("data-min-level") || "0");
    el.dataset.hidden = String(current < min);
  });
}

function setTheme(theme) {
  document.body.dataset.theme = theme;
  localStorage.setItem("portfolio_theme", theme);
  const icon = $("#themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "🌙" : "☀️";
}

function toggleTheme() {
  const cur = document.body.dataset.theme || "dark";
  setTheme(cur === "dark" ? "light" : "dark");
}

function setLang(lang) {
  document.body.dataset.lang = lang;
  localStorage.setItem("portfolio_lang", lang);
  const sel = $("#selectLang");
  if (sel) sel.value = lang;
}

function handleLangChange(e) {
  setLang(e.target.value);
}

function initSettings() {
  setView(localStorage.getItem("portfolio_view") || "normal");
  setTheme(localStorage.getItem("portfolio_theme") || "dark");
  setLang(localStorage.getItem("portfolio_lang") || "es");

  $$("[data-view-btn]").forEach(btn => btn.addEventListener("click", () => setView(btn.dataset.viewBtn)));
  $("#btnTheme")?.addEventListener("click", toggleTheme);
  $("#selectLang")?.addEventListener("change", handleLangChange);
}

function initMenu() {
  const btn = $("#btnMenu");
  const nav = $("#nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    btn.setAttribute("aria-expanded", String(open));
  });
  $$("a", nav).forEach(a => a.addEventListener("click", () => {
    nav.classList.remove("is-open");
    btn.setAttribute("aria-expanded", "false");
  }));
}

async function loadRecentRepos() {
  const box = $("#recentRepos");
  if (!box) return;
  const url = "https://api.github.com/users/vladimiracunadev-create/repos?per_page=12&sort=updated";
  try {
    const res = await fetch(url, { headers: { "Accept": "application/vnd.github+json" } });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const repos = (await res.json())
      .filter(r => !r.fork)
      .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at))
      .slice(0, 8);

    box.innerHTML = repos.map(r => {
      const updated = new Date(r.pushed_at).toLocaleDateString("es-CL", { year: "numeric", month: "short", day: "2-digit" });
      const desc = (r.description || "").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return `
          <div class="repo">
            <div class="repo__top">
              <a class="repo__name" href="${r.html_url}" target="_blank" rel="noreferrer">${r.name}</a>
              <div class="repo__meta">★ ${r.stargazers_count} · actualizado ${updated}</div>
            </div>
            ${desc ? `<div class="repo__desc">${desc}</div>` : ""}
          </div>`;
    }).join("");
  } catch (e) {
    box.innerHTML = `<div class="muted small">No se pudo cargar la lista (API GitHub). Puedes ver repos en GitHub directamente.</div>`;
  }
}

function initCopyEmail() {
  const btn = $("#btnCopyEmail");
  if (!btn) return;
  btn.addEventListener("click", async () => {
    const email = "vladimir.acuna.dev@gmail.com";
    try {
      await navigator.clipboard.writeText(email);
      const old = btn.textContent;
      btn.textContent = "Copiado ✔";
      setTimeout(() => btn.textContent = old, 1200);
    } catch {
      prompt("Copia el email:", email);
    }
  });
}

function initAppDownloads() {
  const actions = $("#smartDownloadActions");
  const notice = $("#platformNotice");
  if (!actions || !notice) return;

  const ua = navigator.userAgent;
  const isAndroid = /Android/i.test(ua);
  const isIOS = /iPhone|iPad|iPod/i.test(ua);
  const isMac = /Macintosh/i.test(ua) && !isIOS;
  const isWindows = /Windows/i.test(ua);

  // Configuración de URLs de Release
  const REPO_URL = "https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/releases/latest/download";
  const APK_URL = `${REPO_URL}/app-debug.apk`;

  let html = "";
  if (isAndroid) {
    notice.textContent = "Plataforma detectada: Android";
    html = `<a class="btn primary" href="${APK_URL}">Descargar APK</a>`;
  } else if (isIOS || isMac) {
    notice.textContent = `Plataforma: ${isIOS ? "iOS" : "macOS"}`;
    html = `<button class="btn primary" data-pwa-trigger>Instalar como App (PWA)</button>`;
  } else if (isWindows) {
    notice.textContent = "Plataforma detectada: Windows";
    html = `<button class="btn primary" data-pwa-trigger>Instalar PWA (Desktop)</button>
              <a class="btn" href="${APK_URL}">Descargar APK (Emulador)</a>`;
  } else {
    notice.textContent = "Plataforma no identificada";
    html = `<a class="btn primary" href="${APK_URL}">Descargar APK</a>
              <button class="btn" data-pwa-trigger>Instalar PWA</button>`;
  }

  actions.innerHTML = html;
}

function initPwaTriggers() {
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-pwa-trigger]")) {
      window.dispatchEvent(new Event("pwa-prompt"));
    }
  });
}

function initMeta() {
  const y = $("#year");
  if (y) y.textContent = String(new Date().getFullYear());
}

initSettings();
initMenu();
initCopyEmail();
initMeta();
initAppDownloads();
initPwaTriggers();
loadRecentRepos();
