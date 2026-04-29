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
  updateLocalizedPdfLinks(lang);
}

function resolveLocalizedPdfHref(link, lang) {
  const fallback = link.dataset.pdfEs || link.getAttribute("href") || "#";
  const key = "pdf" + lang.charAt(0).toUpperCase() + lang.slice(1);
  return link.dataset[key] || fallback;
}

function updateLocalizedPdfLinks(lang) {
  $$("[data-pdf-link]").forEach(link => {
    link.setAttribute("href", resolveLocalizedPdfHref(link, lang));
  });
}

function handleLangChange(e) {
  setLang(e.target.value);
}

function detectLang() {
  const saved = localStorage.getItem("portfolio_lang");
  if (saved) return saved;
  const supported = ["es", "en", "pt", "it", "fr", "zh"];
  const browser = (navigator.language || navigator.languages?.[0] || "es")
    .toLowerCase().slice(0, 2);
  return supported.includes(browser) ? browser : "es";
}

function initSettings() {
  setView(localStorage.getItem("portfolio_view") || "normal");
  setTheme(localStorage.getItem("portfolio_theme") || "dark");
  setLang(detectLang());

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
  const ghUrl = "https://api.github.com/users/vladimiracunadev-create/repos?per_page=12&sort=updated";
  const glUrl = "https://gitlab.com/api/v4/groups/vladimir.acuna.dev-group/projects?per_page=12&order_by=last_activity_at&sort=desc";
  try {
    const [ghRes, glRes] = await Promise.all([
      fetch(ghUrl, { headers: { "Accept": "application/vnd.github+json" } }),
      fetch(glUrl, { headers: { "Accept": "application/json" } })
    ]);

    let repos = [];

    if (ghRes.ok) {
      const ghData = await ghRes.json();
      repos.push(...ghData.map(r => ({
        name: r.name,
        url: r.html_url,
        desc: (r.description || "").replace(/</g, "&lt;").replace(/>/g, "&gt;"),
        stars: r.stargazers_count,
        forks: r.forks_count,
        pushed: r.pushed_at,
        isFork: r.fork,
        source: "GH"
      })));
    }

    if (glRes.ok) {
      const glData = await glRes.json();
      repos.push(...glData.map(r => ({
        name: r.name,
        url: r.web_url,
        desc: (r.description || "").replace(/</g, "&lt;").replace(/>/g, "&gt;"),
        stars: r.star_count,
        forks: r.forks_count,
        pushed: r.last_activity_at,
        isFork: !!r.forked_from_project,
        source: "GL"
      })));
    }

    repos = repos.sort((a, b) => new Date(b.pushed) - new Date(a.pushed)).slice(0, 12);
    if (!repos.length) throw new Error("empty");

    box.innerHTML = repos.map(r => {
      const updated = new Date(r.pushed).toLocaleDateString("es-CL", { year: "numeric", month: "short", day: "2-digit" });
      const forkBadge = r.isFork ? ' · <span title="Fork">⑂ fork</span>' : "";
      const sourceBadge = `<span class="pill mini" title="${r.source === "GL" ? "GitLab" : "GitHub"}" style="font-size:.65rem;padding:.1rem .35rem;vertical-align:middle">${r.source}</span>`;
      return `
          <div class="repo">
            <div class="repo__top">
              <a class="repo__name" href="${r.url}" target="_blank" rel="noreferrer">${r.name}</a> ${sourceBadge}
              <div class="repo__meta">★ ${r.stars} · ⑂ ${r.forks} · ${updated}${forkBadge}</div>
            </div>
            ${r.desc ? `<div class="repo__desc">${r.desc}</div>` : ""}
          </div>`;
    }).join("");
  } catch (e) {
    box.innerHTML = `<div class="muted small">No se pudo cargar la lista. Ver repos en <a href="https://github.com/vladimiracunadev-create" target="_blank" rel="noreferrer">GitHub</a> y <a href="https://gitlab.com/vladimir.acuna.dev-group" target="_blank" rel="noreferrer">GitLab</a>.</div>`;
  }
}

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor(diff / 3600000);
  const mins = Math.floor(diff / 60000);
  if (days > 30) return new Date(dateStr).toLocaleDateString("es-CL", { month: "short", day: "2-digit", year: "numeric" });
  if (days > 0) return `hace ${days}d`;
  if (hours > 0) return `hace ${hours}h`;
  return `hace ${mins}m`;
}

async function loadRecentActivity() {
  const box = $("#recentActivity");
  if (!box) return;
  const ghUrl = "https://api.github.com/users/vladimiracunadev-create/events?per_page=50";
  const glUrl = "https://gitlab.com/api/v4/groups/vladimir.acuna.dev-group/merge_requests?state=merged&per_page=10&order_by=updated_at&sort=desc";
  try {
    const [ghRes, glRes] = await Promise.all([
      fetch(ghUrl, { headers: { "Accept": "application/vnd.github+json" } }),
      fetch(glUrl)
    ]);

    let totalCommits = 0, totalPRs = 0, totalReleases = 0;
    const activeRepos = new Set();
    const highlights = [];

    if (ghRes.ok) {
      const events = await ghRes.json();
      for (const e of events) {
        const repo = e.repo.name.replace("vladimiracunadev-create/", "");
        activeRepos.add(repo);
        if (e.type === "PushEvent") {
          totalCommits += e.payload.commits?.length || 1;
        } else if (e.type === "PullRequestEvent" && e.payload.pull_request?.merged) {
          totalPRs++;
          highlights.push({ icon: "🔀", label: `PR → ${repo}`,
            detail: e.payload.pull_request.title?.slice(0, 90) || "",
            date: e.created_at, source: "GH", url: e.payload.pull_request.html_url });
        } else if (e.type === "ReleaseEvent") {
          totalReleases++;
          highlights.push({ icon: "🚀", label: `release ${e.payload.release.tag_name} → ${repo}`,
            detail: e.payload.release.name?.slice(0, 90) || "",
            date: e.created_at, source: "GH", url: e.payload.release.html_url });
        } else if (e.type === "CreateEvent" && e.payload.ref_type === "tag") {
          highlights.push({ icon: "🏷", label: `tag ${e.payload.ref} → ${repo}`,
            detail: "", date: e.created_at, source: "GH", url: `https://github.com/${e.repo.name}` });
        }
      }
    }

    if (glRes.ok) {
      const mrs = await glRes.json();
      totalPRs += mrs.length;
      for (const mr of mrs) {
        const project = mr.web_url.split("/")[4] || "gitlab";
        activeRepos.add(project);
        highlights.push({ icon: "🔀", label: `MR → ${project}`,
          detail: mr.title?.slice(0, 90) || "",
          date: mr.merged_at || mr.updated_at, source: "GL", url: mr.web_url });
      }
    }

    if (!totalCommits && !highlights.length) throw new Error("empty");

    const stats = [
      totalCommits  ? `⬆ ${totalCommits} commits`  : null,
      totalPRs      ? `🔀 ${totalPRs} PRs / MRs`   : null,
      totalReleases ? `🚀 ${totalReleases} releases` : null,
      activeRepos.size ? `📦 ${activeRepos.size} repos` : null,
    ].filter(Boolean).map(s => `<span class="pill">${s}</span>`).join(" ");

    const top = highlights
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 6)
      .map(item => {
        const ago = timeAgo(item.date);
        const safeDet = item.detail.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        const src = `<span class="pill mini" style="font-size:.65rem;padding:.1rem .35rem;vertical-align:middle">${item.source}</span>`;
        return `
          <div class="repo">
            <div class="repo__top">
              <a class="repo__name" href="${item.url}" target="_blank" rel="noreferrer">${item.icon} ${item.label}</a> ${src}
              <div class="repo__meta">${ago}</div>
            </div>
            ${safeDet ? `<div class="repo__desc">${safeDet}</div>` : ""}
          </div>`;
      }).join("");

    box.innerHTML = `<div class="chips" style="margin-bottom:.75rem">${stats}</div>${top}`;
  } catch (e) {
    box.innerHTML = `<div class="muted small">No se pudo cargar la actividad.</div>`;
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
loadRecentActivity();
