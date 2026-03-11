# 🛠️ Guía de Construcción Detallada | Mobile Artifacts

Profundización técnica en los procesos de compilación, firma y resolución de conflictos de entorno para Android e iOS.

---

## 📋 Requisitos de Software de Grado Industrial

- **Node.js**: v18+ (LTS recomendado).
- **Android Studio**: Ladybug con SDK 34 (Android 14) o superior.
- **Xcode**: v15+ (Bridge nativo para iOS).
- **Capacitor CLI**: Gestionado para consistencia de APIs.

---

## 🤖 Android Deep-Dive

### Estrategias de Resiliencia (Troubleshooting)

#### 1. Políticas de Seguridad (Windows)

En caso de `PSSecurityException`:

```powershell
# Sincronización básica
./scripts/mobile-android.ps1

# Flujo Directo de Construcción (Recomendado)
./scripts/mobile-android-build.ps1
```

> 📖 Consulta la [Guía de Construcción Directa](MOBILE_DIRECT_BUILD) para detalles de configuración.

#### 2. Sincronización de Gradle

Si el menú de construcción está inactivo:

- **Sync**: `File` > `Sync Project with Gradle Files`.
- **Target**: Asegura abrir el directorio `/android` y no la raíz.

---

## 🍎 iOS Deep-Dive

### Soporte Crítico

Para detalles sobre firmas de Apple y perfiles de aprovisionamiento, consulta la [Guía de Soporte iOS](IOS_TROUBLESHOOTING.md).

---

## 📜 Estándares de Sincronización

- **Zero Trash Policy**: El repositorio debe estar libre de rastro de IDEs (.idea/vscode).
- **Permisos Unix**: Mantener `gradlew` con permisos correctos incluso en entornos Windows.

---

[🏠 Volver al Home](Home.md) | **Vladimir Acuña** - Senior Software Engineer
