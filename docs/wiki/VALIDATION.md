# Guía de Validación Local

Asegurando la calidad, accesibilidad y performance del proyecto mediante herramientas automatizadas.

## 🛠 Herramientas

El proyecto utiliza **Lighthouse CI (LHCI)** para auditorías automáticas.

### Comandos de Ejecución

```bash
npm run build
npm run lhci
```

## 📊 ¿Qué se evalúa?

1. **Performance**: Velocidad de carga y optimización de recursos.
2. **Accesibilidad**: Facilidad de uso para todos los usuarios.
3. **Best Practices**: Estándares web modernos y seguridad.
4. **SEO**: Visibilidad en motores de búsqueda.

## 🔒 Política de Seguridad (CSP)

El portafolio implementa una **CSP estricta** para mitigar ataques XSS y de inyección:

* **default-src 'self'**: Solo recursos del mismo origen por defecto.
* **script-src**: Solo scripts locales y de confianza.
* **img-src**: Permitir imágenes externas solo mediante HTTPS.

Para más detalles sobre la implementación técnica, consulta la [Guía de Seguridad](SECURITY_HEADERS).

---
**Vladimir Acuña** - Senior Software Engineer
