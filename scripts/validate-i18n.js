#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const read = relative => fs.readFileSync(path.join(ROOT, relative), "utf8");
const exists = relative => fs.existsSync(path.join(ROOT, relative));
const contract = JSON.parse(read("data/portfolio-i18n.json"));
const localeIndex = JSON.parse(read("api/v1/i18n/index.json"));
const artifacts = JSON.parse(read("api/v1/artifacts.json"));
const app = read("app.js");
const rootHtml = read("index.html");
const serviceWorker = read("service-worker.js");
const buildScript = read("scripts/build.js");
const syncPowerShell = read("scripts/sync-web.ps1");
const syncShell = read("scripts/sync-web.sh");
const capacitorConfig = read("apps/mobile/capacitor.config.ts");
const failures = [];
let checks = 0;

function check(condition, message) {
  checks += 1;
  if (!condition) failures.push(message);
}

const codes = contract.locales.map(locale => locale.code);
check(codes.length === 22, `Canonical contract must contain 22 locales; found ${codes.length}`);
check(new Set(codes).size === codes.length, "Canonical locale codes must be unique");
check(contract.default_locale === "es" && contract.fallback_locale === "es", "Default and fallback locale must be es");
check(JSON.stringify(contract.views) === JSON.stringify(["recruiter", "normal", "deep", "freelance"]), "Canonical views must include recruiter, normal, deep and freelance");
check(!contract.content_source.includes("profile-readme"), "Profile README cannot be the portfolio content source");

for (const section of contract.sections) {
  const present = section.selector === "section.hero"
    ? /<section class="hero">/.test(rootHtml)
    : rootHtml.includes(`id="${section.id}"`);
  check(present, `Canonical section missing from index.html: ${section.id}`);
}

for (const view of contract.views) {
  check(rootHtml.includes(`data-view-btn="${view}"`), `Missing ${view} view control in index.html`);
}

for (const requiredRuntime of [
  "portfolio_lang", "portfolio_theme", "portfolio_view", "document.documentElement.lang",
  "document.documentElement.dir", "data-i18n-fallback", "PDF_SUFFIXES",
]) {
  check(app.includes(requiredRuntime), `app.js is missing i18n runtime contract: ${requiredRuntime}`);
}

check(serviceWorker.includes("LOCALE_ROUTES"), "Service worker must cache locale route entries");
check(serviceWorker.includes("./data/portfolio-i18n.json"), "Service worker must cache the canonical i18n contract");
check(localeIndex.languages.length === codes.length, "API locale index count differs from canonical contract");
check(/webDir:\s*['"]www['"]/.test(capacitorConfig), "Capacitor must package the synchronized www directory");
for (const requiredMobileAsset of ["i18n", "api", "data/portfolio-i18n.json"]) {
  check(syncPowerShell.includes(requiredMobileAsset), `PowerShell mobile sync is missing ${requiredMobileAsset}`);
  check(syncShell.includes(requiredMobileAsset), `Shell mobile sync is missing ${requiredMobileAsset}`);
}
check(buildScript.includes("portfolio-i18n.json"), "Web build must include the canonical i18n contract");
check(syncPowerShell.includes("service-worker.js") && syncShell.includes("service-worker.js"), "Mobile sync scripts must copy the PWA service worker");
check(syncPowerShell.includes("backups") && syncShell.includes("backups"), "Mobile sync scripts must explicitly exclude backups");

for (const locale of contract.locales) {
  const code = locale.code;
  const pagePath = `i18n/${code}/index.html`;
  const docPath = `docs/i18n/${code}/README.md`;
  const apiPath = `api/v1/i18n/${code}.json`;
  check(exists(pagePath), `Missing locale route: ${pagePath}`);
  check(exists(docPath), `Missing localized Markdown: ${docPath}`);
  check(exists(apiPath), `Missing localized API: ${apiPath}`);
  if (!exists(pagePath) || !exists(docPath) || !exists(apiPath)) continue;

  const page = read(pagePath);
  const doc = read(docPath);
  const api = JSON.parse(read(apiPath));
  const indexed = localeIndex.languages.find(item => item.code === code);

  check(page.includes(`<html lang="${code}" dir="${locale.direction}">`), `${code}: route lang/dir mismatch`);
  check(page.includes(`?lang=${code}`), `${code}: route does not preserve requested locale`);
  check(page.includes('src="../localized.js"'), `${code}: route controller missing`);
  check(!/Source synchronized from the public GitHub profile/i.test(page), `${code}: route still uses profile README copy`);
  check(doc.includes("Generated from canonical portfolio content: index.html"), `${code}: Markdown source marker missing`);
  check(doc.includes(`locale:${code}; fallback:es`), `${code}: Markdown fallback marker missing`);
  check(!/Synced from the public GitHub profile/i.test(doc), `${code}: Markdown still claims profile README as source`);
  check(api.meta.language === code, `${code}: API language mismatch`);
  check(api.meta.direction === locale.direction, `${code}: API direction mismatch`);
  check(api.meta.fallback_language === "es", `${code}: API fallback mismatch`);
  check(api.meta.source.endsWith("/index.html"), `${code}: API source must be canonical portfolio`);
  check(JSON.stringify(api.views) === JSON.stringify(contract.views), `${code}: API views differ from canonical contract`);
  check(JSON.stringify(api.sections.map(section => section.id)) === JSON.stringify(contract.sections.map(section => section.id)), `${code}: API section order differs from canonical contract`);
  check(indexed && indexed.direction === locale.direction, `${code}: locale index direction mismatch`);

  for (const section of contract.sections) {
    check(doc.includes(`portfolio-section:${section.id}`), `${code}: Markdown section missing: ${section.id}`);
  }

  for (const artifact of artifacts.artifacts) {
    const variant = artifact.variants && artifact.variants[code];
    check(Boolean(variant), `${code}: missing ${artifact.id} artifact variant`);
    if (variant) check(exists(variant.file), `${code}: missing artifact file ${variant.file}`);
  }
}

for (const rtl of ["ar", "fa"]) {
  check(contract.locales.find(locale => locale.code === rtl)?.direction === "rtl", `${rtl}: canonical direction must be rtl`);
}

if (failures.length) {
  console.error(`i18n equivalence failed: ${failures.length}/${checks} checks`);
  failures.forEach(failure => console.error(`  ✗ ${failure}`));
  process.exit(1);
}

console.log(`i18n equivalence passed: ${checks} checks across ${codes.length} locales.`);
