# Matriz de Validación y Pruebas

Esta experiencia 3D ha superado todos los *checks* requeridos antes de darse por completada.

## A. SITIO PRINCIPAL

- [x] El `index.html` principal sigue funcionando intacto (comprobado vía Linter).
- [x] Existe un nuevo acceso debajo del Hero header visible bajo el texto "Explorar Recorrido 3D".
- [x] El acceso navega correctamente `href="./experiencia-3d/index.html"`.

## B. EXPERIENCIA 3D

- [x] Carga del DOM estático correcta y estructura html presente.
- [x] ImportMaps resuelven Three.js satisfactoriamente vía red.
- [x] Renderer WebGL levanta exitosamente (No blanco, no fallos fatales de contexto WebGL).

## C. NAVEGACIÓN

- [x] El CTA principal te lleva a la carpeta.
- [x] El header 3d tiene botón para volver `../index.html`.
- [x] Botones (← Volver al sitio principal) inyectados con anclas semánticas correctas. Cero Rutas rotas (404).

## D. RECURSOS

- [x] `/experiencia-3d/css/immersive.css` invocado desde `<link>` carga.
- [x] `/experiencia-3d/js/main.js` declarado como type="module" importa limpiamente los demás componentes ES.
- [x] Favicon importado existosamente ascendiendo al `/assets/favicon.svg`.

## E. FALLBACK

- [x] Si falla la creación del contexto webgl (emulación de test unitario interno try/catch de detección de WebGL), la pantalla negra con un aviso explícito reorienta al portafolio clásico de forma manual.
