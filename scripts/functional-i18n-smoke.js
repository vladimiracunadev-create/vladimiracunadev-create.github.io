#!/usr/bin/env node
"use strict";

const fs = require("fs");
const http = require("http");
const net = require("net");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const contract = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "portfolio-i18n.json"), "utf8"));
const failures = [];
let assertions = 0;

function check(condition, message) {
  assertions += 1;
  if (!condition) failures.push(message);
}

function browserExecutable() {
  const candidates = process.platform === "win32"
    ? [
        path.join(process.env["PROGRAMFILES(X86)"] || "", "Google/Chrome/Application/chrome.exe"),
        path.join(process.env.PROGRAMFILES || "", "Google/Chrome/Application/chrome.exe"),
        path.join(process.env["PROGRAMFILES(X86)"] || "", "Microsoft/Edge/Application/msedge.exe"),
        path.join(process.env.PROGRAMFILES || "", "Microsoft/Edge/Application/msedge.exe"),
      ]
    : process.platform === "darwin"
      ? ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
      : ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser"];
  const executable = candidates.find(candidate => candidate && fs.existsSync(candidate));
  if (!executable) throw new Error("Chrome or Edge was not found for functional i18n testing");
  return executable;
}

function contentType(file) {
  return ({
    ".css": "text/css; charset=utf-8", ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".webmanifest": "application/manifest+json",
  })[path.extname(file).toLowerCase()] || "application/octet-stream";
}

function startStaticServer() {
  const server = http.createServer((request, response) => {
    const url = new URL(request.url, "http://127.0.0.1");
    let relative = decodeURIComponent(url.pathname).replace(/^\/+/, "");
    if (!relative || relative.endsWith("/")) relative += "index.html";
    const file = path.resolve(ROOT, relative);
    if (!file.startsWith(`${ROOT}${path.sep}`) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Not found");
      return;
    }
    response.writeHead(200, { "Content-Type": contentType(file), "Cache-Control": "no-store" });
    fs.createReadStream(file).pipe(response);
  });
  return new Promise(resolve => server.listen(0, "127.0.0.1", () => resolve(server)));
}

function freePort() {
  return new Promise(resolve => {
    const probe = net.createServer();
    probe.listen(0, "127.0.0.1", () => {
      const port = probe.address().port;
      probe.close(() => resolve(port));
    });
  });
}

async function waitForJson(url, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
    } catch {}
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

async function connectCdp(webSocketUrl) {
  const socket = new WebSocket(webSocketUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });
  let id = 0;
  const pending = new Map();
  socket.addEventListener("message", event => {
    const message = JSON.parse(String(event.data));
    if (!message.id || !pending.has(message.id)) return;
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolve(message.result);
  });
  return {
    close: () => socket.close(),
    send(method, params = {}) {
      const messageId = ++id;
      return new Promise((resolve, reject) => {
        pending.set(messageId, { resolve, reject });
        socket.send(JSON.stringify({ id: messageId, method, params }));
      });
    },
  };
}

async function main() {
  const server = await startStaticServer();
  const sitePort = server.address().port;
  const debugPort = await freePort();
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "portfolio-i18n-"));
  const browser = spawn(browserExecutable(), [
    "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
    "--disable-extensions", `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    "about:blank",
  ], { stdio: "ignore", windowsHide: true });

  try {
    await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const created = await fetch(`http://127.0.0.1:${debugPort}/json/new?about:blank`, { method: "PUT" }).then(response => response.json());
    const cdp = await connectCdp(created.webSocketDebuggerUrl);
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");

    const evaluate = async expression => {
      const result = await cdp.send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
      if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || "Browser evaluation failed");
      return result.result.value;
    };
    const waitFor = async (expression, timeoutMs = 10000) => {
      const deadline = Date.now() + timeoutMs;
      while (Date.now() < deadline) {
        if (await evaluate(expression)) return;
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      throw new Error(`Browser condition timed out: ${expression}`);
    };
    const navigate = async url => {
      await cdp.send("Page.navigate", { url });
      await waitFor(`document.readyState === "complete"`);
    };

    const base = `http://127.0.0.1:${sitePort}`;
    await navigate(`${base}/i18n/ar/`);
    await waitFor(`location.search === "?lang=ar" && document.documentElement.lang === "ar"`);
    await waitFor(`!("serviceWorker" in navigator) || navigator.serviceWorker.controller !== null`);
    await new Promise(resolve => setTimeout(resolve, 300));
    await waitFor(`document.readyState === "complete" && location.search === "?lang=ar"`);
    let state = await evaluate(`({
      url: location.href, lang: document.documentElement.lang, dir: document.documentElement.dir,
      contentLang: document.documentElement.dataset.contentLang, locale: document.body.dataset.locale,
      selected: document.querySelector("#selectLang").value,
      views: document.querySelectorAll("[data-view-btn]").length,
      sections: document.querySelectorAll("main section").length,
      storedLang: localStorage.getItem("portfolio_lang"),
      firstPdf: document.querySelector("[data-pdf-link]").getAttribute("href")
    })`);
    check(state.url.endsWith("/?lang=ar"), "Arabic route did not enter the canonical SPA URL");
    check(state.lang === "ar" && state.dir === "rtl", "Arabic html.lang/dir mismatch");
    check(state.contentLang === "ar" && state.locale === "ar", "Arabic localized content state mismatch");
    check(state.selected === "ar" && state.storedLang === "ar", "Arabic selection was not persisted");
    check(state.views === 4 && state.sections >= 16, "Arabic route lost views or canonical sections");
    check(/-arabic\.pdf$/.test(state.firstPdf), "Arabic PDF routing did not select the localized artifact");

    await evaluate(`document.querySelector('[data-view-btn="freelance"]').click(); document.querySelector('#btnTheme').click(); true`);
    await cdp.send("Page.reload", { ignoreCache: true });
    await waitFor(`document.readyState === "complete" && document.body.dataset.view === "freelance"`);
    state = await evaluate(`({theme:document.body.dataset.theme,view:document.body.dataset.view,lang:document.documentElement.lang})`);
    check(state.theme === "light" && state.view === "freelance" && state.lang === "ar", "Theme, view or language did not survive reload");

    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: 390, height: 844, screenWidth: 390, screenHeight: 844,
      deviceScaleFactor: 1, mobile: false,
    });
    await new Promise(resolve => setTimeout(resolve, 150));
    state = await evaluate(`({
      width: innerWidth,
      clientWidth: document.documentElement.clientWidth,
      visualWidth: visualViewport.width,
      screenWidth: screen.width,
      mobileMedia: matchMedia('(max-width:1023.98px)').matches,
      drawer: getComputedStyle(document.querySelector('#btnMenu')).display,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      offenders: Array.from(document.querySelectorAll('body *')).map(el=>({
        tag:el.tagName,id:el.id,className:typeof el.className==='string'?el.className:'',
        parent:typeof el.parentElement?.className==='string'?el.parentElement.className:'',
        text:(el.textContent||'').trim().slice(0,80),
        right:Math.round(el.getBoundingClientRect().right),width:Math.round(el.getBoundingClientRect().width)
      })).filter(item=>item.right>document.documentElement.clientWidth+1).sort((a,b)=>b.right-a.right).slice(0,8),
      leftOffenders: Array.from(document.querySelectorAll('body *')).map(el=>({
        tag:el.tagName,id:el.id,className:typeof el.className==='string'?el.className:'',
        parent:typeof el.parentElement?.className==='string'?el.parentElement.className:'',
        text:(el.textContent||'').trim().slice(0,80),
        left:Math.round(el.getBoundingClientRect().left),width:Math.round(el.getBoundingClientRect().width)
      })).filter(item=>item.left < -1).sort((a,b)=>a.left-b.left).slice(0,8)
    })`);
    console.log(`Mobile observation: ${JSON.stringify({
      width: state.width, clientWidth: state.clientWidth, visualWidth: state.visualWidth,
      screenWidth: state.screenWidth, mobileMedia: state.mobileMedia,
      drawer: state.drawer, overflow: state.overflow,
    })}`);
    if (state.overflow > 1) {
      console.log(`Overflow diagnostics: ${JSON.stringify({ right: state.offenders, left: state.leftOffenders })}`);
    }
    check(state.clientWidth >= 360 && state.clientWidth <= 390 && state.mobileMedia && state.drawer !== "none", `Mobile viewport/drawer mismatch (clientWidth=${state.clientWidth}, media=${state.mobileMedia}, display=${state.drawer})`);
    check(state.overflow <= 1, `Mobile layout has horizontal page overflow (${state.overflow}px)`);

    await evaluate(`(()=>{const select=document.querySelector('#selectLang'); select.value='fa'; select.dispatchEvent(new Event('change',{bubbles:true})); return true;})()`);
    await waitFor(`document.documentElement.lang === "fa" && location.search === "?lang=fa"`);
    state = await evaluate(`({dir:document.documentElement.dir,pdf:document.querySelector('[data-pdf-link]').getAttribute('href'),theme:document.body.dataset.theme,view:document.body.dataset.view})`);
    check(state.dir === "rtl" && /-persian\.pdf$/.test(state.pdf), "Persian RTL or PDF routing failed");
    check(state.theme === "light" && state.view === "freelance", "Language switch reset theme or view on mobile");

    await cdp.send("Network.enable");
    await cdp.send("Network.emulateNetworkConditions", {
      offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0,
      connectionType: "none",
    });
    await cdp.send("Page.reload", { ignoreCache: false });
    await waitFor(`document.readyState === "complete" && document.querySelectorAll("main section").length >= 16`);
    state = await evaluate(`({lang:document.documentElement.lang,dir:document.documentElement.dir,view:document.body.dataset.view,theme:document.body.dataset.theme})`);
    check(state.lang === "fa" && state.dir === "rtl", "Offline PWA reload did not preserve Persian locale and RTL");
    check(state.view === "freelance" && state.theme === "light", "Offline PWA reload did not preserve view and theme");
    await cdp.send("Network.emulateNetworkConditions", {
      offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1,
      connectionType: "wifi",
    });

    const localeStates = await evaluate(`(()=>{
      const select=document.querySelector('#selectLang');
      return ${JSON.stringify(contract.locales)}.map(locale=>{
        select.value=locale.code;
        select.dispatchEvent(new Event('change',{bubbles:true}));
        return {
          code:locale.code,
          expectedDir:locale.direction,
          suffix:locale.suffix,
          lang:document.documentElement.lang,
          dir:document.documentElement.dir,
          selected:select.value,
          stored:localStorage.getItem('portfolio_lang'),
          contentLang:document.documentElement.dataset.contentLang,
          locale:document.body.dataset.locale,
          query:new URLSearchParams(location.search).get('lang'),
          pdf:document.querySelector('[data-pdf-link]').getAttribute('href'),
          skip:document.querySelector('a.skip').textContent.trim()
        };
      });
    })()`);
    const spanishSkip = localeStates.find(item => item.code === "es")?.skip;
    for (const localeState of localeStates) {
      check(
        localeState.lang === localeState.code &&
        localeState.dir === localeState.expectedDir &&
        localeState.selected === localeState.code &&
        localeState.stored === localeState.code &&
        localeState.locale === localeState.code &&
        localeState.query === localeState.code &&
        localeState.contentLang === localeState.code &&
        (localeState.code === "es" || localeState.skip !== spanishSkip) &&
        localeState.pdf.endsWith(`${localeState.suffix}.pdf`),
        `${localeState.code}: selector, persistence, fallback, direction or PDF mismatch`
      );
    }
    state = await evaluate(`({theme:document.body.dataset.theme,view:document.body.dataset.view})`);
    check(state.theme === "light" && state.view === "freelance", "Full locale cycle reset theme or view");

    await navigate(`${base}/i18n/zh-TW/`);
    await waitFor(`location.search === "?lang=zh-TW" && document.documentElement.lang === "zh-TW"`);
    state = await evaluate(`({dir:document.documentElement.dir,selected:document.querySelector('#selectLang').value,pdf:document.querySelector('[data-pdf-link]').getAttribute('href')})`);
    check(state.dir === "ltr" && state.selected === "zh-TW", "Traditional Chinese route state mismatch");
    check(/-traditional-chinese\.pdf$/.test(state.pdf), "Traditional Chinese PDF routing failed");

    await navigate(`${base}/?lang=unsupported`);
    await waitFor(`location.search === "?lang=es" && document.documentElement.lang === "es"`);
    state = await evaluate(`({selected:document.querySelector('#selectLang').value,content:document.documentElement.dataset.contentLang})`);
    check(state.selected === "es" && state.content === "es", "Unsupported locale did not fall back to Spanish");

    cdp.close();
  } finally {
    browser.kill();
    server.close();
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
  }

  if (failures.length) {
    console.error(`Functional i18n smoke failed: ${failures.length}/${assertions} assertions`);
    failures.forEach(failure => console.error(`  ✗ ${failure}`));
    process.exit(1);
  }
  console.log(`Functional i18n smoke passed: ${assertions} assertions (routes, persistence, mobile and RTL).`);
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});
