# Corrección de portafolio y CV — 2026-09-25

## Alcance

Corrección posterior a la sincronización integral del 25 de septiembre de
2026. Se reemplazó la agrupación ambigua de proyectos en los CV, se incorporó
la tarjeta de presentación a la web y se añadió una referencia horaria visible
de vigencia.

## Cambios realizados

- Los 61 proyectos destacados de los CV se distribuyen en cinco familias
  explícitas: 18 productos, 15 laboratorios de ingeniería, 7 proyectos de IA
  aplicada, 17 currículos técnicos y 4 iniciativas científico-educativas.
- Ya no existe una ruta de salida `Otros`: una clave sin categoría provoca un
  error de generación y exige una decisión explícita antes de publicar.
- Los 12 archivos `cv-ats*.pdf` y `cv-reclutador*.pdf` se regeneraron en los
  seis idiomas con fecha, hora y zona `America/Santiago`.
- La web muestra una opción `Tarjeta` en el menú y una sección accesible con
  `assets/icons/1.png` (frente) y `assets/icons/2.png` (reverso), texto
  multilingüe y descargas directas.
- La web muestra la vigencia `2026-09-25, 16:27 (America/Santiago)` y el agente
  de sincronización actualizará automáticamente esa referencia en ejecuciones
  posteriores.
- El service worker usa la caché `vladi-portfolio-v15-business-card` e incluye
  ambas imágenes en el app shell.

## Respaldo

Antes de regenerar se copiaron los 12 CV originales, sin sobrescribir respaldos
anteriores, a `assets/backups/2026-09-25/classification-card-fix/`.

## Verificación

- Cobertura de categorías: 61 de 61 proyectos; cero claves sin clasificar.
- Extracción de texto: fecha y zona presentes; etiquetas `Otros`, `Other`,
  `Outros`, `Altri`, `Autres` y `其他` ausentes como grupos de proyectos.
- Paginación final: CV de reclutador en 4 páginas y CV ATS en 2 páginas para
  cada idioma.
- Revisión visual de español y chino, incluidos encabezados, clasificación,
  saltos de página y línea horaria.
- Revisión funcional local de `#tarjeta`: opción de menú, imágenes, textos y
  botones de descarga visibles.
