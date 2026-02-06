# 🔒 Seguridad y Caching | Producción Ready

Protocolos y estándares aplicados para garantizar un despliegue seguro, resiliente y de alto rendimiento.

---

## 🛡️ Checklist de Seguridad (Zero Trust)

Implementar estas cabeceras es crítico para mitigar ataques XSS, Clickjacking y de inyección de recursos.

- [x] **CSP (Content-Security-Policy)**: Control estricto de orígenes permitidos.
- [x] **HSTS (Strict-Transport-Security)**: Garantiza navegación solo vía TLS.
- [x] **X-Content-Type-Options**: Previene el sniffing de MIME types.

---

## ⚡ Estrategias de Caché y Rendimiento

La gestión de caché es vital para una experiencia de usuario instantánea en visitas recurrentes.

### Archivos Dinámicos (`index.html`)

- **Política**: `no-cache` o `max-age=0, must-revalidate`.
- **Razón**: Permite actualizaciones inmediatas sin requerir limpieza manual del navegador.

### Recursos Estáticos (CSS, JS)

- **Agnósticos**: `public, max-age=86400, must-revalidate` (1 día).
- **Inmutables**: `public, max-age=31536000, immutable` (Solo bajo versionado por hash).

---

## 📊 Métricas de Impacto

Un despliegue correcto de estas políticas garantiza un puntaje de **100/100** en la categoría "Best Practices" de Lighthouse.

---

[🏠 Volver al Home](Home.md) | **Vladimir Acuña** - Senior Software Engineer
