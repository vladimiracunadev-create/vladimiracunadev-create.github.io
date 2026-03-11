# 🛠️ Guía de Construcción Detallada | Mobile Artifacts

Profundización técnica en los procesos de compilación, firma y resolución de conflictos de entorno para Android e iOS.

## 🤖 Android Deep-Dive

### Estrategias de Resiliencia (Troubleshooting)

#### 1. Flujo de Construcción Directa

```powershell
# Sincronización básica
./scripts/mobile-android.ps1

# Flujo Directo de Construcción (Recomendado)
./scripts/mobile-android-build.ps1
```

> [!NOTE]
> **Flujo Validado**: El sistema de construcción directa desde Windows ha sido validado con éxito, generando un APK funcional de ~4.32 MB. Para detalles técnicos de orquestación y parámetros, consulta la [Guía de Construcción Directa](MOBILE_DIRECT_BUILD).

#### 2. Sincronización de Gradle

Si el menú de construcción está inactivo:
- **Sync**: `File` > `Sync Project with Gradle Files` en Android Studio.
- **Target**: Asegura abrir el directorio `/android` y no la raíz.

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
