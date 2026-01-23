(() => {
  const LEVELS = { recruiter: 0, normal: 1, deep: 2 };
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));

  function setView(view){
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

  function initView(){
    setView(localStorage.getItem("portfolio_view") || "normal");
    $$("[data-view-btn]").forEach(btn => btn.addEventListener("click", () => setView(btn.dataset.viewBtn)));
  }

  function initMenu(){
    const btn = $("#btnMenu");
    const nav = $("#nav");
    if(!btn || !nav) return;
    btn.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
    });
    $$("a", nav).forEach(a => a.addEventListener("click", () => {
      nav.classList.remove("is-open");
      btn.setAttribute("aria-expanded","false");
    }));
  }

  async function loadRecentRepos(){
    const box = $("#recentRepos");
    if(!box) return;
    const url = "https://api.github.com/users/vladimiracunadev-create/repos?per_page=100&sort=updated";
    try{
      const res = await fetch(url, { headers: { "Accept":"application/vnd.github+json" } });
      if(!res.ok) throw new Error("HTTP " + res.status);
      const repos = (await res.json())
        .filter(r => !r.fork)
        .sort((a,b) => new Date(b.pushed_at) - new Date(a.pushed_at))
        .slice(0, 8);

      box.innerHTML = repos.map(r => {
        const updated = new Date(r.pushed_at).toLocaleDateString("es-CL",{year:"numeric",month:"short",day:"2-digit"});
        const desc = (r.description || "").replace(/</g,"&lt;").replace(/>/g,"&gt;");
        return `
          <div class="repo">
            <div class="repo__top">
              <a class="repo__name" href="${r.html_url}" target="_blank" rel="noreferrer">${r.name}</a>
              <div class="repo__meta">★ ${r.stargazers_count} · actualizado ${updated}</div>
            </div>
            ${desc ? `<div class="repo__desc">${desc}</div>` : ""}
          </div>`;
      }).join("");
    }catch(e){
      box.innerHTML = `<div class="muted small">No se pudo cargar la lista (API GitHub). Puedes ver repos en GitHub directamente.</div>`;
    }
  }

  function initCopyEmail(){
    const btn = $("#btnCopyEmail");
    if(!btn) return;
    btn.addEventListener("click", async () => {
      const email = "vladimir.acuna.dev@gmail.com";
      try{
        await navigator.clipboard.writeText(email);
        const old = btn.textContent;
        btn.textContent = "Copiado ✔";
        setTimeout(() => btn.textContent = old, 1200);
      }catch{
        prompt("Copia el email:", email);
      }
    });
  }

  function initMeta(){
    const y = $("#year");
    if(y) y.textContent = String(new Date().getFullYear());
  }

  initView();
  initMenu();
  initCopyEmail();
  initMeta();
  loadRecentRepos();
})();
