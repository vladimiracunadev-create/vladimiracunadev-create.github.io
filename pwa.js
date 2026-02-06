// pwa.js - Registro del Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js')
            .then((reg) => {
                console.log('SW registrado con éxito:', reg.scope);
            })
            .catch((err) => {
                console.error('Error al registrar el SW:', err);
            });
    });
}
