# Auditoria de codigo generado por IA — decisiones de implementacion

Documento de la linea profesional incorporada el **2026-08-27**:
*Auditoria, verificacion y recuperacion de software generado por IA*
(`AI Code Assurance & Remediation`).

Pagina publica: <https://vladimiracunadev-create.github.io/servicios/auditoria-codigo-ia/>

---

## 1. Que se agrego

Una pagina de servicio propia, con ruta semantica `/servicios/auditoria-codigo-ia/`, y sus
puntos de entrada desde la portada. La pagina cubre las diez secciones pedidas:

1. Hero (`#inicio`)
2. La brecha de verificacion (`#brecha`)
3. Riesgos del codigo generado por IA (`#riesgos`)
4. Servicios (`#servicios`) — 4 servicios comerciales
5. Especialidades (`#especialidades`) — las 8 capacidades, presentadas como complementarias
6. Tipos de proyectos que reviso (`#proyectos`)
7. Metodologia (`#metodologia`) — 7 etapas
8. Entregables (`#entregables`)
9. Modalidades de contratacion (`#modalidades`)
10. Preguntas frecuentes (`#faq`) y llamada a la accion con formulario (`#contacto`)

---

## 2. Decisiones y por que

### 2.1 Pagina estatica, sin dependencias nuevas

El sitio es HTML/CSS/JS plano servido por GitHub Pages. La pagina nueva **no agrega ninguna
dependencia**: reutiliza `styles.css` y `app.js` del raiz. Los unicos ficheros propios son su
`index.html` y `audit-form.js`.

### 2.2 Seis idiomas, no solo espanol

La regla 4 de `CLAUDE.md` prohibe romper el sistema de 6 idiomas. La pagina usa el mismo
mecanismo pasivo por CSS (`data-es` / `data-en` / `data-pt` / `data-it` / `data-fr` / `data-zh`)
y el mismo `<select id="selectLang">`, asi que el idioma elegido en la portada se conserva al
entrar (`localStorage.portfolio_lang`). El espanol sigue siendo el idioma por defecto.

### 2.3 Sin selector de vistas

La pagina no usa `data-min-level`: es una oferta comercial que debe verse completa siempre.
Por eso su barra superior solo lleva idioma y tema, mas el enlace de vuelta al portafolio.
El resumen que vive en la portada (`#auditoria-ia`) tampoco lleva `data-min-level`, de modo
que aparece en las cuatro vistas (Reclutador, Normal, Profundo, Freelance).

### 2.4 Formulario por `mailto:`, no por servicio externo

No hay backend. Un servicio de formularios de terceros obligaria a abrir `connect-src` en la
CSP y a enviar los datos del visitante a un proveedor externo. En su lugar `audit-form.js`
valida en cliente y compone un `mailto:` con los campos, que el propio cliente de correo de la
persona envia. **Nada sale hacia terceros.**

Campos pedidos: nombre, correo, empresa (opcional), URL del repositorio (opcional),
tecnologias, estado actual, tipo de revision, nivel de confidencialidad, problema principal
y mensaje. Los tres campos de opcion son grupos de radios dentro de `<fieldset>`/`<legend>`,
no `<select>`: un `<option>` no admite los seis `<span data-XX>` que necesita el sistema de
idiomas.

**El formulario no pide contrasenas, tokens, claves privadas ni credenciales**, y la pagina lo
advierte de forma visible antes del primer campo.

### 2.5 Estados visibles

- **Foco:** `outline` de 2px en inputs, textareas, radios y `summary` de la FAQ.
- **Error:** `aria-invalid` en el control, borde rojo, asterisco en la etiqueta y mensaje en
  `#auditError` con `role="alert"`. El foco viaja al primer control invalido.
- **Carga:** `#auditSubmit[data-busy="true"]` mientras se compone el mensaje.
- **Exito:** `#auditOk`, con la alternativa de escribir directo al correo si el cliente no abrio.

### 2.6 Lo que **no** se afirma

Por las restricciones del encargo, la pagina no incluye: certificaciones de auditoria, nombres
de clientes, testimonios, logotipos, premios, estadisticas, precios ni garantia de deteccion del
100 % de vulnerabilidades. La FAQ lo dice de forma explicita: lo que se entrega es **cobertura
declarada** (que se reviso, con que metodo, que se encontro y que quedo fuera del alcance).

---

## 3. SEO

- `<title>`, `<meta name="description">`, `rel="canonical"`, Open Graph y Twitter Cards
  (el sitio ya usaba ambos).
- Datos estructurados JSON-LD en un `@graph` con `Person`, `ProfessionalService` (con
  `hasOfferCatalog` de los 4 servicios), `BreadcrumbList` y `FAQPage`. Las preguntas del
  `FAQPage` son las mismas que se ven en pantalla.
- Encabezados jerarquicos: un solo `h1` visible, `h2` por seccion, `h3` dentro de las tarjetas.
- La URL entra en `sitemap.xml` con prioridad `0.9` y en `scripts/generate-seo.js`, que es
  quien lo regenera en CI.
- `llm.txt` la lista en su indice y describe la linea profesional en `About`.

No hay relleno artificial de palabras clave: los terminos objetivo aparecen en el texto porque
describen el servicio.

---

## 4. Ficheros tocados

| Fichero | Cambio |
|---|---|
| `servicios/auditoria-codigo-ia/index.html` | **Nuevo.** La pagina completa, en 6 idiomas. |
| `servicios/auditoria-codigo-ia/audit-form.js` | **Nuevo.** Validacion y composicion del `mailto:`. |
| `index.html` | `og:image` + `twitter:image`. Enlace en la navegacion lateral, CTA en el hero, seccion `#auditoria-ia` antes de `#productos`, tarjeta en `#servicios` y enlace en el footer. Ademas: los controles de vista/idioma/tema se movieron del pie del sidebar al tope del contenido. |
| `styles.css` | `.content-controls` (barra de controles) y el bloque de estilos de la pagina de servicio. Se retiraron las reglas `.sidebar__controls` y `.sidebar .views/.settings`, que quedaron sin elemento al que aplicarse. |
| `sitemap.xml` | URL nueva. |
| `scripts/generate-seo.js` | La pagina entra en `PUBLIC_HTML_FILES`. |
| `llm.txt` | Indice y descripcion de la linea profesional. |
| `service-worker.js` | La pagina y su JS entran al app shell; `CACHE_NAME` a `v14`. |
| `api/v1/meta.json` | Bloque `site_pages`. |
| `api/v1/profile.json` | Bloque `service_lines` con la nueva linea, sus 4 servicios y sus 8 especialidades. |
| `scripts/build.js` | `servicios/` entra en `DIRS_TO_COPY`. |
| `scripts/build-zip.py` | `servicios/` entra en `DIRS_INCLUDE`. |
| `package.json` | `lint:html` cubre `servicios/**/*.html`. |
| `scripts/generate-og-image.py` | **Nuevo.** Genera las tarjetas Open Graph 1200x630. |
| `assets/og/*.png` | **Nuevo.** Las dos tarjetas generadas. |
| `docs/AI_CODE_ASSURANCE.md` | Este documento. |
| `CHANGELOG.md` | Entrada de la sesion. |

Ningun contenido existente se elimino.

---

## 5. Verificacion ejecutada

| Comprobacion | Resultado |
|---|---|
| `node scripts/validate.js` (57 checks de integridad) | 57 pasados, 0 errores, 1 aviso preexistente |
| `html-validate` sobre `index.html` + `servicios/**/*.html` | limpio |
| `markdownlint-cli2` | limpio |
| `node scripts/build.js` | `dist/servicios/auditoria-codigo-ia/` presente |
| Navegador: consola de la pagina nueva | sin errores |
| Navegador: cambio de idioma (es → fr) | los 6 bloques conmutan |
| Navegador: tema claro/oscuro | tokens conmutan en ambas paginas |
| Navegador: envio con campos vacios | 7 campos marcados, `#auditError` visible |
| Navegador: envio completo (iframe en sandbox, sin abrir correo real) | `#auditOk` visible, sin campos invalidos |
| Navegador: 375 px y 1280 px | sin scroll horizontal |
| DOM: ids duplicados, `alt`, etiquetas de formulario, orden de encabezados | sin hallazgos |

Lighthouse CI no pudo ejecutarse localmente: en Windows aborta al limpiar el perfil temporal de
Chrome (`EPERM`), que es el motivo por el que `pnpm lhci` ya venia con `|| echo` en
`package.json`. En CI (Ubuntu) si corre.

---

## 6. Pendientes reales

- ~~Anos de trayectoria.~~ **Resuelto el 2026-08-27**: la cifra de trayectoria es **16+** en todo
  el sitio. Se cambiaron el hero, la meta description, `og:description`, la seccion `#roles`, el
  bullet de modernizacion de legacy, la pagina de servicio, el `README.md` y el `summary` de
  `api/v1/profile.json`. **Se conservan a proposito** los dos "14+" que estan entre parentesis y
  acotan un subconjunto — `llm.txt` (`16+ years of experience (14+ years in
  educational/psychometric web platforms)`) y el mismo `summary` de `profile.json` — porque son
  la permanencia en Fundacion CEIS Maristas (2011-2025), que es lo que declaran los CV en PDF
  (`14 years of core experience at Fundacion CEIS Maristas`). Cambiarlos a 16 volveria falsa esa
  cifra. Los generadores de PDF **no se tocaron**: `generate-portfolio.py` ya declaraba `16+
  years` de trayectoria, y sus "14 years" son la permanencia en CEIS.
- ~~Imagen Open Graph.~~ **Resuelto el 2026-08-27**: `scripts/generate-og-image.py` produce
  `assets/og/og-home.png` y `assets/og/og-auditoria-codigo-ia.png` (1200x630, con la paleta de
  `:root`), y ambas paginas declaran `og:image`, `og:image:type/width/height/alt` y
  `twitter:image` con URL absoluta.
- **Comprobacion de enlaces en CI.** El `rel="canonical"` apunta a una URL que solo existe una
  vez publicada. La primera ejecucion de Lychee tras el push puede reportarla como rota
  mientras GitHub Pages termina de desplegar. El job no rompe la build (`lycheeverse/lychee-action`
  v1 no falla por defecto), pero conviene saberlo.
- **Marketplace de perfiles.** Las especialidades quedaron como datos estructurados reutilizables
  (`service_lines.specialities` en `api/v1/profile.json` y `hasOfferCatalog` en el JSON-LD), pero
  el directorio o marketplace **no se anuncia** en la pagina, por indicacion expresa.
