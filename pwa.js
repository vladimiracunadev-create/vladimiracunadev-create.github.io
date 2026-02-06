if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js')
            .then(reg => console.log('SW registrado', reg.scope))
            .catch(err => console.log('Error registro SW', err));
    });
}

// Lógica para el botón de instalación (Promoted Installation)
let deferredPrompt;
const installBtn = document.getElementById('pwaInstall');

window.addEventListener('beforeinstallprompt', (e) => {
    // Evita que Chrome 67 y anteriores muestren el prompt automáticamente
    e.preventDefault();
    // Guarda el evento para poder dispararlo más tarde
    deferredPrompt = e;
    // Muestra el botón de instalación en la UI
    if (installBtn) {
        installBtn.style.display = 'inline-block';
    }
});

if (installBtn) {
    installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        // Muestra el prompt de instalación
        deferredPrompt.prompt();
        // Espera a la respuesta del usuario
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`Usuario eligió la instalación: ${outcome}`);
        // Ya no necesitamos el prompt guardado
        deferredPrompt = null;
        // Ocultamos el botón de nuevo
        installBtn.style.display = 'none';
    });
}

window.addEventListener('appinstalled', () => {
    console.log('PWA instalada con éxito');
    if (installBtn) installBtn.style.display = 'none';
});
