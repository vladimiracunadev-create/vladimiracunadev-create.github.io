const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DIST = 'dist';
const ASSETS = 'assets';

// Clean dist
if (fs.existsSync(DIST)) {
    fs.rmSync(DIST, { recursive: true, force: true });
}
fs.mkdirSync(DIST);

console.log('🧹 Cleaned dist/');

// Copy Assets
if (fs.existsSync(ASSETS)) {
    fs.cpSync(ASSETS, path.join(DIST, ASSETS), { recursive: true });
    console.log('📂 Assets copied');
}

// Copy SEO files if they exist
['sitemap.xml', 'robots.txt'].forEach(file => {
    if (fs.existsSync(file)) {
        fs.copyFileSync(file, path.join(DIST, file));
        console.log(`📄 Copied ${file}`);
    }
});

// Minify CSS
try {
    console.log('🎨 Minifying CSS...');
    // Requires clean-css-cli
    execSync(`npx cleancss -o ${DIST}/styles.css styles.css`);
} catch (e) {
    console.log('⚠️ CSS Minification failed, copying raw.');
    fs.copyFileSync('styles.css', path.join(DIST, 'styles.css'));
}

// Minify JS
try {
    console.log('📜 Minifying JS...');
    // Requires terser
    execSync(`npx terser app.js -o ${DIST}/app.js --compress --mangle`);
} catch (e) {
    console.log('⚠️ JS Minification failed, copying raw.');
    fs.copyFileSync('app.js', path.join(DIST, 'app.js'));
}

// Minify HTML (Simple regex based or copy)
// For a robust solution we'd use html-minifier, but let's keep it simple "vanilla" or just copy for now
// to avoid heavy dependencies if requested. Let's just copy for vanilla approach strictly or use a simple replacement.
console.log('<html> Processing HTML...');
let html = fs.readFileSync('index.html', 'utf8');
// Simple comment removal (careful with this)
html = html.replace(/<!--[\s\S]*?-->/g, '');
fs.writeFileSync(path.join(DIST, 'index.html'), html);

console.log('✅ Build complete in dist/');
