# Seguridad y Caching

Guía de mejores prácticas para el despliegue del portafolio estático en entornos de producción.

## 🛡 Security Headers (Checklist)

Para obtener calificación **A+** en auditorías de seguridad:

* **Content-Security-Policy (CSP)**: Control de recursos permitidos.
* **Strict-Transport-Security (HSTS)**: Forzar HTTPS.
* **X-Content-Type-Options**: `nosniff`.
* **X-Frame-Options**: `DENY`.
* **Referrer-Policy**: `strict-origin-when-cross-origin`.

## ⚡ Estrategia de Cache (Performance)

### Archivos HTML (`index.html`)

* **Cache-Control**: `no-cache` o `max-age=0, must-revalidate`.
* *Razón*: Asegura entrega inmediata de actualizaciones.

### Assets (CSS, JS)

* Si no tienen hash: `public, max-age=86400, must-revalidate` (1 día).
* Si tienen hash: `public, max-age=31536000, immutable`.

### Binarios Pesados (PDFs, Imágenes)

* **Cache-Control**: `public, max-age=31536000, immutable`.

---
**Vladimir Acuña** - Senior Software Engineer
