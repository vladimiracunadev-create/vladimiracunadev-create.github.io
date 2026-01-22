# Caso A — AWS Amplify + GitLab (hosting automático)

## Qué hace
- Conecta el repo de GitLab con **AWS Amplify Hosting**.
- Cada `git push` a tu rama (ej. `main`) despliega automáticamente tu web estática.

## Pasos (sin afectar otros entornos)
1) En AWS, crea una **nueva Amplify App** (no reutilices una existente).
2) Conecta tu repo GitLab y selecciona la rama (ej. `main`).
3) Marca **My app is a monorepo** y pon el path: `caso-a-amplify`.
4) (Recomendado) Para que quede "infra como código" en el repo:
   - Copia `caso-a-amplify/amplify.yml` a la **raíz** del repositorio (quedará como `./amplify.yml`).
   - Haz commit y push.

Amplify usa el `amplify.yml` del repositorio para el buildspec cuando está presente.

Testing local
-------------
- Puedes ejecutar un servidor estático para ver la web localmente: `npx http-server caso-a-amplify -p 8080`.
- Para revisar que el build funciona, reproduce los pasos de `amplify.yml` localmente (por ejemplo, instalar dependencias y ejecutar comandos de build).

Notas y buenas prácticas
------------------------
- No incluyas credenciales en el repositorio. Usa las opciones de variables y secret manager en Amplify cuando sea necesario.
- Mantén `amplify.yml` simple; si necesitas transformaciones (minificación, versiones) define pasos explícitos en el build.
- Revisa la configuración de dominio y certificado en Amplify si vas a usar un dominio personalizado.

Referencias
-----------
- `amplify.yml` (este folder)
- Documentación oficial: https://docs.aws.amazon.com/amplify

Despliegue en Amplify ✅
-----------------------
La app del **Caso A** está desplegada en: https://main.d1uybq9oui7h8c.amplifyapp.com/ (deployed 2026-01-13).

Verificación rápida
-------------------
- Abrir la URL y comprobar que la página carga correctamente.
- Revisar que los assets (CSS, JS, PDFs) se sirvan sin errores.
- Probar en móvil/desktop y navegar por enlaces.
- Para problemas, revisar logs de Amplify Console y el build log.

Siguientes pasos recomendados
-----------------------------
- Configurar un dominio personalizado y certificado en Amplify si aplica.
- Revisar ajustes de cache y headers (Cache-Control) en S3/CloudFront o Amplify.
- Añadir monitorización/alertas (CloudWatch) y pruebas E2E si deseas.

