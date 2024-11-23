document.addEventListener("DOMContentLoaded", () => {
    const audioElement = document.getElementById('background-music');
    const muteButton = document.getElementById('mute-button');
    const volumeControl = document.getElementById('volume-control');

    // Устанавливаем начальную громкость на 50%
    audioElement.volume = 0.5;

    // Кнопка мута
    muteButton.addEventListener("click", () => {
        if (audioElement.muted) {
            audioElement.muted = false;
            muteButton.innerText = "Mute";
        } else {
            audioElement.muted = true;
            muteButton.innerText = "Unmute";
        }
    });

    // Регулятор громкости
    volumeControl.addEventListener("input", () => {
        audioElement.volume = volumeControl.value;
    });

    // Таймер до следующего комплимента
    function countdown() {
        const now = new Date();
        const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
        const diff = tomorrow - now;

        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        document.getElementById("countdown").innerText =
            `${hours} ч ${minutes} мин ${seconds} сек`;

        if (diff > 0) setTimeout(countdown, 1000);
    }

    // Анимация конверта
    const envelope = document.querySelector(".envelope");
    const compliment = document.querySelector(".compliment");

    // Проверяем, был ли конверт уже открыт
    const envelopeOpened = localStorage.getItem("envelopeOpened") === "true";

    if (envelopeOpened) {
        envelope.classList.add("opened");
        compliment.style.display = "block";
    }

    if (envelope) {
        envelope.addEventListener("click", () => {
            envelope.classList.add("opened");
            localStorage.setItem("envelopeOpened", "true"); // Сохраняем состояние
            setTimeout(() => {
                compliment.style.display = "block";
            }, 500);
        });
    }

    // Запускаем таймер обратного отсчета
    countdown();
});
