#!/usr/bin/env node
/**
 * Portfolio Integrity Validator
 * Strict automated checks for every change.
 * Run: npm test
 *
 * Categories:
 *   1. CSP & Security — no inline styles/scripts
 *   2. PDF Integrity — all referenced PDFs exist, correct targets
 *   3. Bilingual Consistency — all 6 languages present where expected
 *   4. View System — data-min-level attributes valid
 *   5. JSON API — all endpoints valid JSON
 *   6. PWA — manifest, service worker, offline page
 *   7. SEO — sitemap, robots, llm.txt
 *   8. Links — external links have rel="noopener"
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const LANGS = ["es", "en", "pt", "it", "fr", "zh"];
const VIEWS = ["0", "1", "2"];

let errors = [];
let warnings = [];
let passed = 0;

function ok(msg) {
  passed++;
}

function fail(msg) {
  errors.push(msg);
}

function warn(msg) {
  warnings.push(msg);
}

function fileExists(relPath) {
  return fs.existsSync(path.join(ROOT, relPath));
}

function readFile(relPath) {
  const full = path.join(ROOT, relPath);
  if (!fs.existsSync(full)) return null;
  return fs.readFileSync(full, "utf-8");
}

// ═══════════════════════════════════════════════════
// 1. CSP & SECURITY
// ═══════════════════════════════════════════════════

function checkCSP() {
  const html = readFile("index.html");
  if (!html) return fail("index.html not found");

  // No inline styles
  const inlineStyles = html.match(/ style="/g);
  if (inlineStyles) {
    fail(`CSP: Found ${inlineStyles.length} inline style(s) in index.html — use CSS classes instead`);
    // Find line numbers
    const lines = html.split("\n");
    lines.forEach((line, i) => {
      if (/ style="/.test(line)) {
        fail(`  -> Line ${i + 1}: ${line.trim().substring(0, 100)}`);
      }
    });
  } else {
    ok("CSP: No inline styles");
  }

  // No inline scripts (except structured data)
  const scriptTags = html.match(/<script(?![^>]*src=)[^>]*>/g);
  if (scriptTags) {
    const nonJson = scriptTags.filter(s => !s.includes('type="application/ld+json"'));
    if (nonJson.length > 0) {
      warn(`CSP: Found ${nonJson.length} inline script tag(s) — consider externalizing`);
    } else {
      ok("CSP: No inline scripts (structured data excluded)");
    }
  } else {
    ok("CSP: No inline scripts");
  }

  // CSP meta tag exists
  if (html.includes("Content-Security-Policy")) {
    ok("CSP: Policy meta tag present");
  } else {
    fail("CSP: No Content-Security-Policy meta tag found");
  }
}

// ═══════════════════════════════════════════════════
// 2. PDF INTEGRITY
// ═══════════════════════════════════════════════════

function checkPDFs() {
  const html = readFile("index.html");
  if (!html) return;

  // Extract all PDF hrefs
  const pdfHrefs = new Set();
  const hrefPattern = /href="(assets\/[^"]*\.pdf)"/g;
  let match;
  while ((match = hrefPattern.exec(html)) !== null) {
    pdfHrefs.add(match[1]);
  }

  // Extract data-pdf-es and data-pdf-en
  const dataPdfEs = /data-pdf-es="([^"]+)"/g;
  const dataPdfEn = /data-pdf-en="([^"]+)"/g;
  while ((match = dataPdfEs.exec(html)) !== null) pdfHrefs.add(match[1]);
  while ((match = dataPdfEn.exec(html)) !== null) pdfHrefs.add(match[1]);

  // Check each PDF exists
  for (const pdfPath of pdfHrefs) {
    if (fileExists(pdfPath)) {
      const stat = fs.statSync(path.join(ROOT, pdfPath));
      if (stat.size < 1000) {
        warn(`PDF: ${pdfPath} is very small (${stat.size} bytes) — may be corrupt`);
      } else {
        ok(`PDF: ${pdfPath} exists (${(stat.size / 1024).toFixed(1)} KB)`);
      }
    } else {
      fail(`PDF: Referenced file missing: ${pdfPath}`);
    }
  }

  // Check all PDF links have target="_blank"
  const pdfLinks = html.match(/<a[^>]*href="assets\/[^"]*\.pdf"[^>]*>/g) || [];
  for (const link of pdfLinks) {
    if (!link.includes('target="_blank"')) {
      fail(`PDF: Link missing target="_blank": ${link.substring(0, 120)}`);
    }
    if (!link.includes('rel="noopener"')) {
      warn(`PDF: Link missing rel="noopener": ${link.substring(0, 120)}`);
    }
  }

  if (pdfLinks.length > 0 && pdfLinks.every(l => l.includes('target="_blank"'))) {
    ok(`PDF: All ${pdfLinks.length} PDF links open in new tab`);
  }

  // Check bilingual PDF pairs
  const pdfPairs = html.match(/data-pdf-es="([^"]+)"\s+data-pdf-en="([^"]+)"/g) || [];
  const pdfPairsAlt = html.match(/data-pdf-en="([^"]+)"\s+.*?data-pdf-es="([^"]+)"/g) || [];
  if (pdfPairs.length > 0 || pdfPairsAlt.length > 0) {
    ok(`PDF: ${pdfPairs.length + pdfPairsAlt.length} bilingual PDF pair(s) declared`);
  }
}

// ═══════════════════════════════════════════════════
// 3. BILINGUAL CONSISTENCY
// ═══════════════════════════════════════════════════

function checkBilingual() {
  const html = readFile("index.html");
  if (!html) return;

  // Count elements per language
  const counts = {};
  for (const lang of LANGS) {
    const pattern = new RegExp(`data-${lang}[\\s>]`, "g");
    const matches = html.match(pattern);
    counts[lang] = matches ? matches.length : 0;
  }

  // ES should be the baseline
  const esCount = counts["es"];
  if (esCount === 0) return fail("Bilingual: No data-es elements found");

  ok(`Bilingual: ES baseline = ${esCount} elements`);

  // EN must match ES exactly (primary pair). Others are secondary — warn if >5% gap, fail if >20%.
  for (const lang of LANGS) {
    if (lang === "es") continue;
    const diff = esCount - counts[lang];
    const pct = ((diff / esCount) * 100).toFixed(1);
    const isPrimary = lang === "en";

    if (diff === 0) {
      ok(`Bilingual: ${lang.toUpperCase()} = ${counts[lang]} (matches ES)`);
    } else if (isPrimary && Math.abs(diff) > 3) {
      fail(`Bilingual: EN = ${counts[lang]} (ES has ${esCount}, diff=${diff} — primary pair must match)`);
    } else if (isPrimary) {
      warn(`Bilingual: EN = ${counts[lang]} (ES has ${esCount}, diff=${diff})`);
    } else if (Math.abs(diff) / esCount > 0.20) {
      fail(`Bilingual: ${lang.toUpperCase()} = ${counts[lang]} (ES has ${esCount}, diff=${diff}, ${pct}% gap — exceeds 20% threshold)`);
    } else if (Math.abs(diff) / esCount > 0.05) {
      warn(`Bilingual: ${lang.toUpperCase()} = ${counts[lang]} (ES has ${esCount}, diff=${diff}, ${pct}% gap)`);
    } else {
      ok(`Bilingual: ${lang.toUpperCase()} = ${counts[lang]} (ES has ${esCount}, diff=${diff})`);
    }
  }
}

// ═══════════════════════════════════════════════════
// 4. VIEW SYSTEM
// ═══════════════════════════════════════════════════

function checkViews() {
  const html = readFile("index.html");
  if (!html) return;

  const viewPattern = /data-min-level="(\d+)"/g;
  let match;
  let viewCount = 0;
  const invalidViews = [];

  while ((match = viewPattern.exec(html)) !== null) {
    viewCount++;
    if (!VIEWS.includes(match[1])) {
      invalidViews.push(match[1]);
    }
  }

  if (viewCount > 0) {
    ok(`Views: ${viewCount} elements with data-min-level`);
  }
  if (invalidViews.length > 0) {
    fail(`Views: Invalid data-min-level values: ${invalidViews.join(", ")} (must be 0, 1, or 2)`);
  } else {
    ok("Views: All data-min-level values valid (0-2)");
  }

  // Check view buttons exist (uses data-view-btn attribute)
  if (html.includes('data-view-btn="recruiter"') && html.includes('data-view-btn="normal"') && html.includes('data-view-btn="deep"')) {
    ok("Views: All 3 view buttons present");
  } else {
    fail("Views: Missing one or more view buttons (recruiter/normal/deep)");
  }
}

// ═══════════════════════════════════════════════════
// 5. JSON API
// ═══════════════════════════════════════════════════

function checkAPI() {
  const apiFiles = [
    "api/v1/profile.json",
    "api/v1/experience.json",
    "api/v1/projects.json",
    "api/v1/skills.json",
    "api/v1/artifacts.json",
    "api/v1/meta.json",
  ];

  for (const file of apiFiles) {
    const content = readFile(file);
    if (!content) {
      fail(`API: Missing ${file}`);
      continue;
    }
    try {
      JSON.parse(content);
      ok(`API: ${file} is valid JSON`);
    } catch (e) {
      fail(`API: ${file} is invalid JSON — ${e.message}`);
    }
  }

  // Check data/resume.json
  const resume = readFile("data/resume.json");
  if (resume) {
    try {
      JSON.parse(resume);
      ok("API: data/resume.json is valid JSON");
    } catch (e) {
      fail(`API: data/resume.json is invalid JSON — ${e.message}`);
    }
  }
}

// ═══════════════════════════════════════════════════
// 6. PWA
// ═══════════════════════════════════════════════════

function checkPWA() {
  // Manifest
  if (fileExists("manifest.webmanifest")) {
    const manifest = readFile("manifest.webmanifest");
    try {
      const m = JSON.parse(manifest);
      if (m.name && m.short_name && m.start_url && m.display) {
        ok("PWA: manifest.webmanifest valid with required fields");
      } else {
        fail("PWA: manifest.webmanifest missing required fields (name, short_name, start_url, display)");
      }
    } catch (e) {
      fail(`PWA: manifest.webmanifest is invalid JSON — ${e.message}`);
    }
  } else {
    fail("PWA: manifest.webmanifest not found");
  }

  // Service worker
  if (fileExists("service-worker.js")) {
    ok("PWA: service-worker.js exists");
  } else {
    fail("PWA: service-worker.js not found");
  }

  // PWA registration
  if (fileExists("pwa.js")) {
    ok("PWA: pwa.js exists");
  } else {
    fail("PWA: pwa.js not found");
  }

  // Offline page
  if (fileExists("offline.html")) {
    ok("PWA: offline.html exists");
  } else {
    fail("PWA: offline.html not found");
  }
}

// ═══════════════════════════════════════════════════
// 7. SEO
// ═══════════════════════════════════════════════════

function checkSEO() {
  // Required files
  const seoFiles = ["robots.txt", "sitemap.xml", "llm.txt"];
  for (const file of seoFiles) {
    if (fileExists(file)) {
      ok(`SEO: ${file} exists`);
    } else {
      fail(`SEO: ${file} not found`);
    }
  }

  // robots.txt references sitemap
  const robots = readFile("robots.txt");
  if (robots && robots.includes("sitemap.xml")) {
    ok("SEO: robots.txt references sitemap.xml");
  } else if (robots) {
    warn("SEO: robots.txt does not reference sitemap.xml");
  }

  // sitemap.xml is valid XML-ish
  const sitemap = readFile("sitemap.xml");
  if (sitemap) {
    if (sitemap.includes("<urlset") && sitemap.includes("<loc>")) {
      ok("SEO: sitemap.xml has valid structure");
    } else {
      fail("SEO: sitemap.xml missing <urlset> or <loc> elements");
    }
  }

  // index.html has essential meta tags
  const html = readFile("index.html");
  if (html) {
    const metaChecks = [
      ["og:title", /property="og:title"/],
      ["og:description", /property="og:description"/],
      ["description", /name="description"/],
      ["viewport", /name="viewport"/],
      ["canonical or og:url", /property="og:url"|rel="canonical"/],
    ];
    for (const [name, pattern] of metaChecks) {
      if (pattern.test(html)) {
        ok(`SEO: meta ${name} present`);
      } else {
        warn(`SEO: meta ${name} not found`);
      }
    }
  }
}

// ═══════════════════════════════════════════════════
// 8. LINKS & SECURITY
// ═══════════════════════════════════════════════════

function checkLinks() {
  const html = readFile("index.html");
  if (!html) return;

  // External links should have rel="noopener"
  const extLinks = html.match(/<a[^>]*href="https?:\/\/[^"]*"[^>]*>/g) || [];
  let missingNoopener = 0;
  for (const link of extLinks) {
    if (link.includes('target="_blank"') && !link.includes("noopener")) {
      missingNoopener++;
    }
  }

  if (missingNoopener > 0) {
    warn(`Links: ${missingNoopener} external link(s) with target="_blank" missing rel="noopener"`);
  } else {
    ok(`Links: All ${extLinks.length} external links properly secured`);
  }
}

// ═══════════════════════════════════════════════════
// 9. FILE STRUCTURE
// ═══════════════════════════════════════════════════

function checkStructure() {
  const requiredFiles = [
    "index.html",
    "styles.css",
    "app.js",
    "pwa.js",
    "service-worker.js",
    "manifest.webmanifest",
    "offline.html",
    "package.json",
  ];

  for (const file of requiredFiles) {
    if (fileExists(file)) {
      ok(`Structure: ${file} exists`);
    } else {
      fail(`Structure: Required file missing: ${file}`);
    }
  }
}

// ═══════════════════════════════════════════════════
// 10. CURLY QUOTES & ENCODING
// ═══════════════════════════════════════════════════

function checkEncoding() {
  const html = readFile("index.html");
  if (!html) return;

  // Check for curly/smart quotes in attributes
  const curlyDoubleLeft = html.match(/\u201c/g);
  const curlyDoubleRight = html.match(/\u201d/g);
  const curlySingleLeft = html.match(/\u2018/g);
  const curlySingleRight = html.match(/\u2019/g);

  // Curly quotes inside HTML attributes are problematic
  const attrCurly = html.match(/=["\u201c\u201d][^>\n]*[\u201c\u201d\u2018\u2019]/g);
  if (attrCurly) {
    fail(`Encoding: Found ${attrCurly.length} curly/smart quote(s) in HTML attributes — use straight quotes`);
  } else {
    ok("Encoding: No curly quotes in attributes");
  }

  // Check for BOM
  if (html.charCodeAt(0) === 0xFEFF) {
    warn("Encoding: index.html has BOM — consider removing");
  } else {
    ok("Encoding: No BOM detected");
  }
}

// ═══════════════════════════════════════════════════
// RUNNER
// ═══════════════════════════════════════════════════

console.log("Portfolio Integrity Validator");
console.log("=".repeat(50));
console.log();

checkStructure();
checkCSP();
checkEncoding();
checkPDFs();
checkBilingual();
checkViews();
checkAPI();
checkPWA();
checkSEO();
checkLinks();

// ── Report ──
console.log();
console.log("=".repeat(50));
console.log(`  PASSED:   ${passed}`);
console.log(`  WARNINGS: ${warnings.length}`);
console.log(`  ERRORS:   ${errors.length}`);
console.log("=".repeat(50));

if (warnings.length > 0) {
  console.log("\nWARNINGS:");
  warnings.forEach(w => console.log(`  ⚠  ${w}`));
}

if (errors.length > 0) {
  console.log("\nERRORS:");
  errors.forEach(e => console.log(`  ✗  ${e}`));
  console.log();
  process.exit(1);
} else {
  console.log("\n  All checks passed.\n");
  process.exit(0);
}
