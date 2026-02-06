# Seguridad y Caching

Este documento describe las cabeceras recomendadas para desplegar este portafolio estático en producción (AWS CloudFront, Vercel, Netlify, o Apache/Nginx).

## Recomendación de Security Headers (Checklist)

Para obtener calificación A+ en validadores de seguridad:

- [ ] **Content-Security-Policy (CSP)**:

  ```http
  default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; object-src 'none';
  ```

- [ ] **Strict-Transport-Security (HSTS)**:

  ```http
  max-age=63072000; includeSubDomains; preload
  ```

- [ ] **X-Content-Type-Options**:

  ```http
  nosniff
  ```

- [ ] **X-Frame-Options**:

  ```http
  DENY
  ```

- [ ] **Referrer-Policy**:

  ```http
  strict-origin-when-cross-origin
  ```

- [ ] **Permissions-Policy**:

  ```http
  camera=(), microphone=(), geolocation=()
  ```

## Estrategia de Cache (Performance)

Como este sitio es estático:

### Archivos HTML (`index.html`)

- **Cache-Control**: `no-cache` (o `max-age=0, must-revalidate`)
- *Razón*: Asegura que los usuarios siempre vean la última versión del contenido al recargar.

### Assets con Hash (si se implementa versionado) o Inmutables

- Como actualmente **no usamos hash** en los nombres de archivo (`styles.css`, `app.js`), **NO** usar cache agresivo.
- **Recomendado para estáticos simples**:

  ```http
  Cache-Control: public, max-age=86400, must-revalidate
  ```

  *(Cache de 1 día, pero validar si cambió).*

### Assets pesados (PDFs, Imágenes)

- **Cache-Control**: `public, max-age=31536000, immutable`
- *Nota*: Solo si estás seguro que los nombres de archivo cambiarán si el contenido cambia (ej. `cv-2026.pdf`). Si usas nombres fijos (`cv-completo.pdf`), usa la estrategia de 1 día.

---

[← Volver al README](../README.md) | **Vladimir Acuña** - Senior Software Engineer
