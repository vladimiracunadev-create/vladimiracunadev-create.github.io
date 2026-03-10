import * as THREE from 'three';

// ----------------------------------------------------------------------------------
// CONFIGURADOR DE LA CÁMARA Y NAVEGACIÓN GUIADA (24 Estaciones con Parallax)
// ----------------------------------------------------------------------------------

const numStations = 24;
const zOffset = -25;
const waypoints = [];

for (let i = 0; i < numStations; i++) {
    const stationZ = i * zOffset;
    if (i === 0) {
        waypoints.push({ position: new THREE.Vector3(0, 6, 12), lookAt: new THREE.Vector3(0, 4, 0) });
    } else if (i === numStations - 1) {
        waypoints.push({ position: new THREE.Vector3(0, 4, stationZ + 10), lookAt: new THREE.Vector3(0, 5, stationZ - 10) });
    } else {
        waypoints.push({ position: new THREE.Vector3(0, 4, stationZ + 10), lookAt: new THREE.Vector3(-6, 3, stationZ) });
    }
}

// Variables de puntero global para el parallax
export const mouseState = { x: 0, y: 0 };

export function setupCamera(width, height) {
    const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 200);

    // Posición inicial
    camera.position.copy(waypoints[0].position);
    camera.lookAt(waypoints[0].lookAt);

    camera._targetPosition = waypoints[0].position.clone();
    camera._targetLookAt = waypoints[0].lookAt.clone();
    camera._currentLookAt = waypoints[0].lookAt.clone();

    // Loop interno inyectado
    camera.updatePosition = function (time) {
        // Interpolar base LERP
        this.position.lerp(this._targetPosition, 0.05);
        this._currentLookAt.lerp(this._targetLookAt, 0.05);

        // Clona el LookAt matriz para no ensuciar la real con el parallax del ratón
        const finalLookAt = this._currentLookAt.clone();

        // 1. Efecto cinemático (respiración) persistente
        let breathingOffsetY = 0;
        let breathingOffsetX = 0;
        if (time) {
            breathingOffsetY = Math.sin(time * 0.001) * 0.05;
            breathingOffsetX = Math.cos(time * 0.0008) * 0.02;
            this.position.y += breathingOffsetY;
            this.position.x += breathingOffsetX;
        }

        // 2. Parallax de Cursor (Mirar hacia donde el usuario apunta suavemente)
        // Multiplicador bajo (por ej. max 3 unidades en el espacio 3D a lo ancho)
        finalLookAt.x += (mouseState.x * 2.5); // Ratón -1 a 1 ajusta LookAt
        finalLookAt.y += (mouseState.y * 1.5);

        this.lookAt(finalLookAt);
    };

    return camera;
}

export function moveCameraToStep(camera, stepIndex) {
    const safeStep = Math.max(0, Math.min(stepIndex, waypoints.length - 1));
    const wp = waypoints[safeStep];

    camera._targetPosition.copy(wp.position);
    camera._targetLookAt.copy(wp.lookAt);
}
