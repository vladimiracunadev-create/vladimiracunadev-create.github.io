import * as THREE from 'three';
import { setupScene } from './scene.js';
import { setupCamera, moveCameraToStep, mouseState } from './camera-path.js';
import { handleUI } from './ui-navigation.js';

let scene, camera, renderer;
let isWebGLSupported = true;

// 1. Detección temprana de WebGL (Fallback)
function detectWebGL() {
    try {
        const canvas = document.createElement('canvas');
        return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
        return false;
    }
}

// 2. Setup Principal
function init() {
    if (!detectWebGL()) {
        isWebGLSupported = false;
        document.getElementById('webgl-error').classList.remove('hidden');
        return;
    }

    const container = document.getElementById('canvas-container');

    // Renderer optimizado visualmente
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    scene = new THREE.Scene();
    scene.background = new THREE.Color('#020617'); // fondo súper deep dark

    // Niebla densa para esconder el fin del horizonte (muro)
    scene.fog = new THREE.FogExp2('#020617', 0.045);

    camera = setupCamera(window.innerWidth, window.innerHeight);
    setupScene(scene);

    // Eventos de entorno
    window.addEventListener('resize', onWindowResize);
    document.addEventListener('mousemove', onMouseMove, false);

    // Ocultar preloader y mostrar UI
    document.getElementById('fallback').classList.add('hidden');
    document.getElementById('ui-layer').classList.remove('hidden');

    // Iniciar eventos UI (Pasos/Navegación + Sonido sintético)
    handleUI((step) => {
        moveCameraToStep(camera, step);
    });

    // Arrancar Loop
    animate();
}

// Interacción del ratón normalizada (-1 a 1) para el parallax
function onMouseMove(event) {
    mouseState.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouseState.y = -(event.clientY / window.innerHeight) * 2 + 1;
}

// 3. Loop de Animación
function animate() {
    if (!isWebGLSupported) return;
    requestAnimationFrame(animate);

    // Lógica de cámara interpolada (Parallax y Breathing effect)
    if (camera.updatePosition) {
        camera.updatePosition(performance.now());
    }

    renderer.render(scene, camera);
}

// 4. Utilidad de Resize
function onWindowResize() {
    if (!camera || !renderer) return;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('DOMContentLoaded', init);
