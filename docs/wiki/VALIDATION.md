# 📊 Guía de Validación Local | Calidad de Software

Asegurando que cada línea de código cumpla con los estándares de excelencia técnica mediante auditorías automatizadas.

---

## 🛠️ Herramental de Calidad

Utilizamos **Lighthouse CI (LHCI)** como gatekeeper de calidad antes de cualquier promoción a producción.

### Comandos de Inspección

```bash
npm run build      # Genera el artefacto web optimizado
npm run lhci       # Ejecuta la batería de pruebas de Lighthouse
```

---

## 🔍 Ejes de Evaluación

1. **Performance**: Optimización de imágnes y carga diferida.
2. **Accesibilidad**: Navegación por teclado y etiquetas semánticas.
3. **SEO**: Preparación para indexación orgánica.

---

## 🔒 Content Security Policy (CSP)

El portafolio opera bajo una **CSP de denegación por defecto**:

- **Self-Only**: Solo servimos lo que nosotros mismos generamos.
- **Strict Scripts**: Bloqueo de inyecciones externas maliciosas.

Para una exploración profunda de los headers, consulta la [Guía de Seguridad](SECURITY_HEADERS).

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
