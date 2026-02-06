const fs = require('fs');
const path = require('path');

const MAX_SIZE_MB = 5;
const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
const DIR = path.resolve(__dirname, '..', 'assets'); // Adjust if assets are elsewhere

function checkPdfs(dir) {
    if (!fs.existsSync(dir)) return;

    const files = fs.readdirSync(dir);
    let hasError = false;

    files.forEach(file => {
        const filePath = path.join(dir, file);
        if (path.extname(file).toLowerCase() === '.pdf') {
            const stats = fs.statSync(filePath);
            const sizeMb = (stats.size / (1024 * 1024)).toFixed(2);

            if (stats.size > MAX_SIZE_BYTES) {
                console.error(`❌ PDF TOO LARGE: ${file} (${sizeMb} MB) > ${MAX_SIZE_MB} MB`);
                hasError = true;
            } else {
                console.log(`✅ PDF OK: ${file} (${sizeMb} MB)`);
            }
        }
    });

    if (hasError) {
        console.error('Some PDFs are too large. Please compress them (e.g. using ilovepdf.com).');
        process.exit(1);
    }
}

console.log('⚖️ Checking PDF sizes...');
checkPdfs(DIR);
