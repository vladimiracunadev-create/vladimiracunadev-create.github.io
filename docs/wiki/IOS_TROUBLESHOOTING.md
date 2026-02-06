# Solución de Problemas - iOS (Capacitor)

Detalles sobre la resolución de errores comunes al configurar el entorno de Apple.

## 1. Error de "Signing & Capabilities"

**Problema:** *"Signing for App requires a development team."*

**Solución:** Selecciona un Apple ID válido en la pestaña *Signing & Capabilities* en Xcode.

## 2. Error de "No Devices"

**Problema:** *"Your team has no devices from which to generate a provisioning profile."*

**Solución:**

* Conecta un iPhone físico.
* O selecciona un **Simulador** como destino.

## 3. Simuladores Faltantes

**Problema:** No aparecen simuladores en la lista.

**Solución:**

* Instala el runtime en **Xcode > Settings > Platforms > iOS**.
* Crea simuladores en **Window > Devices and Simulators**.

## 4. Sincronización de Archivos Web

Para asegurar que la app refleje los últimos cambios del portafolio:

1. Usa el script `./scripts/mobile-ios.sh`.
2. O manualmente:

   ```bash
   ./scripts/sync-web.sh
   npx cap sync ios
   ```

---
**Vladimir Acuña** - Senior Software Engineer
