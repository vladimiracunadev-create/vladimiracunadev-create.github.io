// Registro del Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js')
            .then(reg => console.log('PWA: Service Worker registrado', reg.scope))
            .catch(err => console.log('PWA: Error en registro de SW', err));
    });
}

// Lógica de Instalación
let deferredPrompt;
const installBtn = document.getElementById('pwaInstall');

// Capturamos el evento de instalación
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevenir que el navegador muestre el prompt automáticamente
    e.preventDefault();
    // Guardamos el evento
    deferredPrompt = e;
    // Registramos que el evento fue capturado
    console.log('PWA: Evento installation capturado y listo.');

    // Si el botón existe, lo mostramos
    if (installBtn) {
        installBtn.classList.remove('is-hidden');
    }
});

// Listener para la acción de instalar
if (installBtn) {
    installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) {
            console.warn('PWA: No hay evento de instalación guardado.');
            return;
        }

        // Mostramos el prompt del sistema
        deferredPrompt.prompt();

        // Esperamos la elección del usuario
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`PWA: El usuario eligió: ${outcome}`);

        // Limpiamos el recurso
        deferredPrompt = null;

        // Ocultamos el botón de nuevo
        installBtn.classList.add('is-hidden');
    });
}

// Evento de confirmación de instalación
window.addEventListener('appinstalled', () => {
    console.log('PWA: Aplicación instalada correctamente.');
    if (installBtn) installBtn.classList.add('is-hidden');
});

// Listener para disparar el prompt desde otros componentes
window.addEventListener('pwa-prompt', () => {
    if (installBtn) installBtn.click();
});
