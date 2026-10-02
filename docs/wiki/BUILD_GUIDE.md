# 🛠️ Guía de Construcción Detallada | Mobile Artifacts

Profundización técnica en los procesos de compilación, firma y resolución de conflictos de entorno para Android e iOS.

**Verificada:** 2026-10-01.

## 📄 Paquete documental

Los seis generadores Python producen 42 PDFs públicos: 7 familias por 6 idiomas. Antes de ejecutar, respalda `assets/*.pdf`; después valida con `node scripts/check-pdf.js`, `pdfinfo` y renderizado visual de páginas representativas. La codificación documental se controla con `python scripts/mojibake_probe.py .`. `generate-institutional-context-note.py` conserva la nota fuente en español y regenera sus cinco traducciones.

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
