# Integración con Portafolio Base

El portafolio tiene su propio build y CI.
La **Experiencia 3D** no rompe ni la estructura lógica y DOM base, simplemente es un enlace URL clásico (`<a href="./experiencia-3d/index.html">`).

## ¿Afecta Lighthouse?

No afecta al Lighthouse Score de `index.html` puesto que la carga de dependencias gráficas (`three.js`), CSS complementarias y evaluación de JS ocurre solo si el usuario navega explícitamente hacia `/experiencia-3d/index.html`.

## Archivos de Origen que se conectan

La referencia más crítica que conecta la experiencia 3D al portafolio raíz es:
`../index.html` o `../assets/` contenidos en `<a href="../index.html">` o `<link rel="icon" href="../assets/...`

Las urls estáticas se mantienen dentro de la carpeta actual con el sufijo relacional (`./`), logrando que en Github Pages en entornos `user.github.io/repo/experiencia-3d/` todo resuelva normalmente tanto ascendiendo un nivel (../) como explorando de forma contigua (./).
