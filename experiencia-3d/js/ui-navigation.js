// ----------------------------------------------------------------------------------
// LÓGICA DE INTERFAZ HTML & WEB AUDIO SINTÉTICO
// Coordina botones, paneles laterales, tipografía escalonada y progresos.
// ----------------------------------------------------------------------------------

// Sintetizar un zumbido profundo tipo Sci-Fi (Bajo consumo, 0 dependencias)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playWooshSound() {
    if (audioCtx.state === 'suspended') { audioCtx.resume(); }

    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    // Rampa de frecuencia tipo swoosh hacia abajo
    osc.type = 'sine';
    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.8);

    // Fade-in cortísimo, y decaimiento largo
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.15, audioCtx.currentTime + 0.1); // Volumen bajo no invasivo
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1.2);

    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + 1.5);
}

export function handleUI(onStepChangeCallback) {
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const stepLabel = document.getElementById('current-step');
    const panels = document.querySelectorAll('.panel');
    const progressBar = document.getElementById('nav-progress-bar'); // Novedad

    const totalSteps = panels.length;
    let currentStep = 0;

    function updateView() {
        // 1. Sonido envolvente UI puro JS al cambiar de slide
        if (audioCtx) {
            playWooshSound();
        }

        // 2. Botones de estado
        btnPrev.disabled = currentStep === 0;
        btnNext.disabled = currentStep === totalSteps - 1;

        // 3. Indicador númerico inferior
        stepLabel.innerText = currentStep + 1;

        // 4. Barra de progreso lineal superior (Cinemática)
        if (progressBar) {
            // Porcentaje a base 100 de 24 pasos (0 es 0%, 23 es 100%)
            const percentage = (currentStep / (totalSteps - 1)) * 100;
            progressBar.style.width = percentage + '%';
        }

        // 5. Paneles Info con Typo Reveal rearmado 
        panels.forEach((panel, index) => {
            if (index === currentStep) {
                panel.classList.add('active');
                // Gatillar nuevamente la animación de reflow para Typo interna (Hack inofensivo)
                panel.classList.remove('animate-text');
                void panel.offsetWidth;
                panel.classList.add('animate-text');
            } else {
                panel.classList.remove('active', 'animate-text');
            }
        });

        // 6. Callback de la cámara LERP
        if (typeof onStepChangeCallback === 'function') {
            onStepChangeCallback(currentStep);
        }
    }

    // Bindings
    btnNext.addEventListener('click', () => {
        if (currentStep < totalSteps - 1) { currentStep++; updateView(); }
    });

    btnPrev.addEventListener('click', () => {
        if (currentStep > 0) { currentStep--; updateView(); }
    });

    // Setup Inicial progress e inicio en 0
    if (progressBar) progressBar.style.width = '0%';
}
