const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://vladimiracunadev-create.github.io';
const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_DIR = ROOT_DIR;
const TODAY = new Date().toISOString().split('T')[0];

// Keep sitemap generation explicit: only public pages that should be indexed.
const PUBLIC_HTML_FILES = [
    { file: 'index.html', path: '', priority: '1.0' },
    { file: path.join('experiencia-3d', 'index.html'), path: 'experiencia-3d/', priority: '0.7' }
];

let sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`;

PUBLIC_HTML_FILES.forEach(entry => {
    const absoluteFile = path.join(ROOT_DIR, entry.file);
    if (!fs.existsSync(absoluteFile)) {
        return;
    }

    sitemapContent += `
  <url>
    <loc>${BASE_URL}/${entry.path}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${entry.priority}</priority>
  </url>`;
});

sitemapContent += `
</urlset>`;

fs.writeFileSync(path.join(OUTPUT_DIR, 'sitemap.xml'), sitemapContent);
console.log('✅ sitemap.xml generated');

const robotsContent = `User-agent: *
Allow: /
Sitemap: ${BASE_URL}/sitemap.xml

# LLM / AI assistants context file
# See: https://llmstxt.org/
LLM: ${BASE_URL}/llm.txt
`;

fs.writeFileSync(path.join(OUTPUT_DIR, 'robots.txt'), robotsContent);
console.log('✅ robots.txt generated');
