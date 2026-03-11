const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const DIST = 'dist';
const FILES_TO_COPY = [
    'sitemap.xml',
    'robots.txt',
    'llm.txt',
    'manifest.webmanifest',
    'service-worker.js',
    'pwa.js',
    'offline.html'
];
const DIRS_TO_COPY = [
    'assets',
    path.join('api', 'v1'),
    'experiencia-3d'
];

function copyIfExists(src, dest) {
    if (!fs.existsSync(src)) {
        return false;
    }

    const stats = fs.statSync(src);
    if (stats.isDirectory()) {
        fs.cpSync(src, dest, { recursive: true });
    } else {
        fs.copyFileSync(src, dest);
    }

    return true;
}

function getLocalBin(name) {
    return path.join(
        'node_modules',
        '.bin',
        process.platform === 'win32' ? `${name}.cmd` : name
    );
}

function runLocalBin(name, args) {
    const bin = getLocalBin(name);
    if (!fs.existsSync(bin)) {
        throw new Error(`Missing local binary: ${bin}`);
    }

    if (process.platform === 'win32') {
        execFileSync(process.env.ComSpec || 'cmd.exe', ['/d', '/c', bin, ...args], { stdio: 'inherit' });
        return;
    }

    execFileSync(bin, args, { stdio: 'inherit' });
}

if (fs.existsSync(DIST)) {
    fs.rmSync(DIST, { recursive: true, force: true });
}
fs.mkdirSync(DIST);

console.log('Cleaned dist/');

DIRS_TO_COPY.forEach(dir => {
    if (copyIfExists(dir, path.join(DIST, dir))) {
        console.log(`Copied ${dir}/`);
    }
});

FILES_TO_COPY.forEach(file => {
    if (copyIfExists(file, path.join(DIST, file))) {
        console.log(`Copied ${file}`);
    }
});

try {
    console.log('Minifying CSS...');
    runLocalBin('cleancss', ['-o', path.join(DIST, 'styles.css'), 'styles.css']);
} catch (error) {
    console.warn(`CSS minification failed, copying raw. ${error.message}`);
    fs.copyFileSync('styles.css', path.join(DIST, 'styles.css'));
}

try {
    console.log('Minifying JS...');
    runLocalBin('terser', ['app.js', '-o', path.join(DIST, 'app.js'), '--compress', '--mangle']);
} catch (error) {
    console.warn(`JS minification failed, copying raw. ${error.message}`);
    fs.copyFileSync('app.js', path.join(DIST, 'app.js'));
}

console.log('<html> Processing HTML...');
let html = fs.readFileSync('index.html', 'utf8');
html = html.replace(/<!--[\s\S]*?-->/g, '');
fs.writeFileSync(path.join(DIST, 'index.html'), html);

console.log('Build complete in dist/');
