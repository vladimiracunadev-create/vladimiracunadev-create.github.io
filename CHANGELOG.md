# Changelog

## 2026-03-11

- Fixed HTML lint coverage so the validation step targets real site files.
- Improved `scripts/build.js` to use local CLI binaries, making CSS and JS minification work in Windows environments where `npx` via PowerShell can fail.
- Expanded the build output to include `llm.txt`, `api/v1/` and `experiencia-3d/` so `dist/` matches the public site more closely.
- Corrected the API manual to distinguish SEO generation from versioned JSON data maintenance.
