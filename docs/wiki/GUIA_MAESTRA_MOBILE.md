# 🚀 Guía Maestra Mobile | Ecosistema Multiplataforma

Esta guía proporciona la visión estratégica y los requisitos técnicos para operar el portafolio como una aplicación nativa.

## 🤖 Android (Universal)

### Pipeline de Construcción (APK)

Dispones de tres caminos según tu necesidad:

1. **Sync + Build Directo (Recomendado)**: Sincroniza y genera el APK en un solo paso.

   ```powershell
   ./scripts/mobile-android-build.ps1
   ```

2. **Solo Sincronización**: Útil si vas a trabajar dentro de Android Studio.

   ```powershell
   ./scripts/mobile-android.ps1
   ```

3. **Manual**: Sincroniza Capacitor sin tocar el código web.

   ```powershell
   cd apps/mobile
   npx cap sync android
   ```

> 📖 Para detalles técnicos del flujo directo (parámetros y entorno), consulta la [Guía de Construcción Directa](MOBILE_DIRECT_BUILD).

## 📦 Reglas de Ingeniería de Versiones

- **Higiene del Repo**: Prohibido subir binarios (.apk/.ipa).
- **GitHub Releases**: Utilizar el sistema de assets de GitHub para distribución.
- **Trazabilidad**: Cada release debe documentar cambios técnicos y correcciones.

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
