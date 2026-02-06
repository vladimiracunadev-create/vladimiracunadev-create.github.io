const fs = require('fs');
const path = require('path');

// Configuration
const BASE_URL = 'https://vladimiracunadev-create.github.io'; // Adjust if custom domain exists
const ROOT_DIR = path.resolve(__dirname, '..');
const OUTPUT_DIR = ROOT_DIR;

// Find HTML files
function getHtmlFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            if (file !== 'node_modules' && file !== '.git' && file !== 'assets') {
                getHtmlFiles(filePath, fileList);
            }
        } else {
            if (path.extname(file) === '.html') {
                fileList.push(filePath);
            }
        }
    });
    return fileList;
}

const htmlFiles = getHtmlFiles(ROOT_DIR);
const today = new Date().toISOString().split('T')[0];

let sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`;

htmlFiles.forEach(file => {
    let relativePath = path.relative(ROOT_DIR, file).replace(/\\/g, '/');
    if (relativePath === 'index.html') relativePath = ''; // Root

    // Skip 404 pages if any
    if (relativePath.includes('404')) return;

    sitemapContent += `
  <url>
    <loc>${BASE_URL}/${relativePath}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>${relativePath === '' ? '1.0' : '0.8'}</priority>
  </url>`;
});

sitemapContent += `
</urlset>`;

fs.writeFileSync(path.join(OUTPUT_DIR, 'sitemap.xml'), sitemapContent);
console.log('✅ sitemap.xml generated');

// Robots.txt
const robotsContent = `User-agent: *
Allow: /
Sitemap: ${BASE_URL}/sitemap.xml
`;

fs.writeFileSync(path.join(OUTPUT_DIR, 'robots.txt'), robotsContent);
console.log('✅ robots.txt generated');
