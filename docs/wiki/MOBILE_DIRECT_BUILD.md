# 🚀 Mobile Direct Build | Flujo Android Studio Directo

Este documento detalla el camino de alta eficiencia para transformar el núcleo web del portafolio en una aplicación Android directamente desde Windows, optimizando tiempos de compilación y evitando problemas de permisos comunes.

---

## 💎 Propuesta de Valor

A diferencia del flujo estándar que requiere múltiples pasos manuales en el IDE, este sistema automatiza la sincronización y construcción mediante un único orquestador de PowerShell.

- **KISS Compliance**: Sin pasos redundantes.
- **Sandboxed Build**: Configura `GRADLE_USER_HOME` localmente para evitar conflictos de sistema.
- **Reproducibilidad Local-First**: Funciona en cualquier entorno Windows con Android Studio.

---

## 🛠️ Ejecución del Script

Desde la raíz del repositorio, ejecuta:

```powershell
./scripts/mobile-android-build.ps1
```

### Parámetros Avanzados

| Parámetro | Efecto |
| :--- | :--- |
| `-SkipWebSync` | Omite la sincronización de la carpeta `/www` |
| `-SkipGradle` | Solo sincroniza Capacitor (abre el proyecto sin build) |
| `-OpenAndroidStudio` | Inicia el IDE automáticamente tras la sincronización |
| `-ForceNpmInstall` | Fuerza el refresco de dependencias en `apps/mobile` |

---

## 📂 Salida del Artefacto (APK)

Tras un proceso exitoso, el APK de depuración se localiza en:

`apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`

---

## 🤖 Skill de IA Recomendado

Usa el skill [`portfolio-mobile-direct-build`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-mobile-direct-build/SKILL.md) cuando quieras que un agente orqueste todo este flujo de forma autónoma.

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
