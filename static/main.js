(() => {

    'use strict';

    const video = document.querySelector('#video');
    const canvas = document.querySelector('#canvas');
    var ctx = null;
    const emojis = {
        anger: '&#128544',
        fear: '&#128552',
        happiness: '&#128512',
        sadness: '&#128543',
        surprise: '&#128562',
        neutral: '&#128528'
    };

    navigator.getUserMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;

    const constraints = { video: true, audio: false };

    navigator.getUserMedia(constraints,
        (stream) => processVideo(stream),
        (error) => console.log(error)
    );

    const processVideo = (stream) => {
        video.srcObject = stream;
        canvas.width = 1080;
        canvas.height = 720;
        ctx = canvas.getContext('2d');
        video.play();
        setInterval(getEmotions, 250);
    }

    const getEmotions = async () => {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const base64 = canvas.toDataURL('image/jpeg', 90);
        const results = await fetch('/emotions/get_emotions', {
            method: 'POST',
            body: base64
        });
        const emotions = await results.json();
        const mainEmotion = document.querySelector('#main-emotion');
        const hightlighted = document.querySelector(`#${emotions['main_emotion']}`);
        const anger = document.querySelector('#anger');
        const fear = document.querySelector('#fear');
        const happiness = document.querySelector('#happiness');
        const sadness = document.querySelector('#sadness');
        const surprise = document.querySelector('#surprise');
        const neutral = document.querySelector('#neutral');

        mainEmotion.innerHTML = emojis[emotions['main_emotion']] || "Acérquese a la cámara";
        anger.innerHTML = 'Angry: ' + (emotions['probabilities']['anger'] || '0');
        fear.innerHTML = 'Fear: ' + (emotions['probabilities']['fear'] || '0');
        happiness.innerHTML = 'Happy ' + (emotions['probabilities']['happiness'] || '0');
        sadness.innerHTML = 'Sad: ' + (emotions['probabilities']['sadness'] || '0');
        surprise.innerHTML = 'Surprised: ' + (emotions['probabilities']['surprise'] || '0');
        neutral.innerHTML = 'Neutral: ' + (emotions['probabilities']['neutral'] || '0');

        const elements = [anger, fear, happiness, sadness, surprise, neutral];
        elements.forEach(e => e.style.color = 'blue');

        hightlighted.style.color = 'red';
    }

})();