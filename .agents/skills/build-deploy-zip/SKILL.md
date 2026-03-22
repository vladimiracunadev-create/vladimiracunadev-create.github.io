# build-deploy-zip

Genera el ZIP de despliegue del portafolio para subir a AWS u otros ambientes estáticos (S3, Amplify, Netlify, etc.).

## Cuándo usar este skill

- El usuario dice "genera el ZIP", "crea el bundle", "quiero subir a AWS", "actualiza el ambiente", "empaqueta la web"
- Antes de un despliegue manual a cualquier ambiente externo
- Después de regenerar PDFs o cambiar contenido

## REGLA OBLIGATORIA

NUNCA generar el ZIP si hay cambios sin commit. Verificar primero con `git status`. Si hay cambios pendientes, reportar y esperar instrucción del usuario.

---

## Flujo de ejecución

### Paso 1 — Verificar estado del repo

```bash
cd C:/portfolio-pages
git status
```

Si hay cambios sin commit: **DETENER** y reportar. No continuar hasta que el usuario confirme o haga commit.

### Paso 2 — Ejecutar validaciones

```bash
npm test
npm run lint:html
```

Si alguna validación falla: reportar errores y **no generar el ZIP** hasta que el usuario autorice continuar.

### Paso 3 — Generar el ZIP

```bash
cd C:/portfolio-pages
python scripts/build-zip.py
```

El script genera automáticamente: `portfolio-bundle-YYYY-MM-DD.zip` en la raíz.

**Qué incluye el ZIP:**

| Elemento | Incluido |
|---|---|
| `index.html`, `app.js`, `styles.css` | SI |
| `pwa.js`, `service-worker.js` | SI |
| `manifest.webmanifest`, `offline.html` | SI |
| `robots.txt`, `sitemap.xml`, `llm.txt` | SI |
| `api/v1/` (6 JSONs) | SI |
| `assets/` — 30+ PDFs en 6 idiomas | SI |
| `assets/icons/` — iconos PWA | SI |
| `experiencia-3d/` | SI |
| `assets/backups/` | NO — solo dev |
| `assets/no_aplica/` | NO — versiones descartadas |
| `assets/por_solicitud/` | NO — privado |
| `assets/*.docx` | NO — no es web |
| `node_modules/`, `scripts/`, `.git/` | NO |
| `.agents/`, `.claude/`, `docs/` | NO |
| `apps/`, `data/`, `sources/` | NO |

### Paso 4 — Verificar el ZIP

```bash
python -c "
import zipfile
with zipfile.ZipFile('portfolio-bundle-YYYY-MM-DD.zip') as z:
    files = z.namelist()
    pdfs = [f for f in files if f.endswith('.pdf')]
    jsons = [f for f in files if f.endswith('.json')]
    size_mb = sum(z.getinfo(f).file_size for f in files) / 1_048_576
    print(f'Total archivos : {len(files)}')
    print(f'PDFs           : {len(pdfs)} (esperado: 31)')
    print(f'JSONs api/v1   : {len(jsons)} (esperado: 6)')
    print(f'Tamano real    : {size_mb:.1f} MB')
    missing = []
    for req in ['index.html','app.js','styles.css','service-worker.js','manifest.webmanifest']:
        if req not in files:
            missing.append(req)
    if missing:
        print(f'FALTANTES: {missing}')
    else:
        print('Archivos criticos: OK')
"
```

Si hay archivos faltantes críticos o el ZIP pesa 0 MB: **reportar y no continuar**.

### Paso 5 — Reportar al usuario

```text
[ZIP] portfolio-bundle-YYYY-MM-DD.zip
  Archivos : N incluidos
  PDFs     : 31 (6 idiomas x 5 documentos + 1 legacy)
  JSONs    : 6 (api/v1/)
  Tamano   : X.X MB comprimido
  Ruta     : C:/portfolio-pages/portfolio-bundle-YYYY-MM-DD.zip

[Instrucciones de subida]
  AWS S3    : aws s3 sync . s3://tu-bucket/ --delete (desde el ZIP descomprimido)
  Amplify   : subir el ZIP directamente en la consola
  Netlify   : drag & drop del ZIP en netlify.com/drop
  Otro      : descomprimir y copiar contenido a la raiz del servidor web
```

---

## ZIP personalizado (nombre especifico)

Si el usuario quiere un nombre especifico:

```bash
python scripts/build-zip.py --output mi-nombre-v2.zip
```

---

## Errores comunes

| Error | Causa | Solucion |
|---|---|---|
| ZIP pesa 0 KB | Ruta incorrecta o permisos | Verificar que se corre desde C:/portfolio-pages |
| Faltan PDFs | No se generaron antes | Correr `python scripts/generate-all-languages.py` primero |
| ZIP muy grande (+50 MB) | Se incluyeron node_modules | Verificar que el script excluye correctamente |
| `UnicodeEncodeError` | Terminal Windows sin UTF-8 | Ya corregido en el script — emojis eliminados |
