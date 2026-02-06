# 🍎 Soporte iOS | Capacitor Engineering

Guía especializada en la resolución de desafíos técnicos dentro de Xcode y el ecosistema de certificados de Apple.

---

## 🛡️ Desafíos de Aprovisionamiento y Firma

### 1. Signing & Capabilities

**Falla**: *"Signing for App requires a development team."*

**Solución**: Es obligatorio registrar un Apple ID en la pestaña *Signing & Capabilities* para permitir el despliegue nativo.

### 2. Identificación de Dispositivos Target

**Falla**: *"Your team has no devices from which to generate a provisioning profile."*

**Solución**:

- Conectar un iPhone real registrado en el Developer Portal.
- O desplegar en un **Simulador** (ideal para validación de UI básica).

---

## 📱 Entorno de Simulación

**Problema**: No aparecen dispositivos virtuales en la lista de Xcode.

**Solución**:

1. Instalar el runtime en **Xcode > Settings > Platforms**.
2. Crear perfiles de dispositivos en **Window > Devices and Simulators**.

---

## 🔄 Flujo de Sincronización Web-Nativo

Para garantizar que la lógica de negocio y estilos CSS de tu portafolio se propaguen correctamente al binario de iPhone:

```bash
./scripts/mobile-ios.sh  # Ejecuta build web + cap sync
```

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
