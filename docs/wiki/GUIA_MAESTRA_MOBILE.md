# 🚀 Guía Maestra Mobile | Ecosistema Multiplataforma

Esta guía proporciona la visión estratégica y los requisitos técnicos para operar el portafolio como una aplicación nativa de alto rendimiento.

---

## 📱 Hardware y Entorno de Ingeniería

El desarrollo móvil exige un entorno optimizado para garantizar tiempos de compilación mínimos y estabilidad en emuladores.

### Perfil de Hardware Recomendado

- **CPU**: Apple M2/M3 o Intel i7/i9 (mínimo 8 núcleos).
- **RAM**: 16GB (32GB recomendado para flujos de trabajo paralelos).
- **Almacenamiento**: NVMe SSD con 20GB+ dedicados a SDKs y Runtimes.

---

## ⚡ Puesta en Marcha (Fast-Track)

### 1. Preparación del Workspace

```bash
git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
cd vladimiracunadev-create.github.io
npm install
```

### 2. Capa de Abstracción Móvil

Utilizamos **Capacitor** para exponer APIs nativas al núcleo Vanilla JS.

```bash
cd apps/mobile
npm install
```

---

## 🤖 Android (Universal)

### Pipeline de Construcción (APK)

1. **Sync Core**: Prepara los assets web.

    ```bash
    ./scripts/mobile-android.ps1        # (Sincronización)
    ./scripts/mobile-android-build.ps1  # (Construcción Directa 🚀)
    ```

2. **Studio Integration**: Abre `apps/mobile/android` en **Android Studio**.

3. **Artifact Generation**: `Build` > `Build APK(s)`.

---

## 🍎 iOS (Apple Ecosystem)

### Pipeline de Construcción (IPA)

1. **Sync Core**:

    ```bash
    ./scripts/mobile-ios.sh
    ```

2. **Xcode Integration**:

    ```bash
    npx cap open ios
    ```

3. **Archiving**: Selecciona `Any iOS Device` > `Product` > `Archive`.

---

## 📦 Reglas de Ingeniería de Versiones

- **Higiene del Repo**: Prohibido subir binarios (.apk/.ipa).
- **GitHub Releases**: Utilizar el sistema de assets de GitHub para distribución.
- **Trazabilidad**: Cada release debe documentar cambios técnicos y correcciones.

---

[🏠 Volver al Home](Home.md) | **Vladimir Acuña** - Senior Software Engineer
