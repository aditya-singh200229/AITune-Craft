document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const playBtn = document.getElementById('playBtn');
    const stopBtn = document.getElementById('stopBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const progressBar = document.getElementById('progressBar');
    const tempoSlider = document.getElementById('tempo');
    const tempoValue = document.getElementById('tempoValue');

    const synth = new Tone.PolySynth().toDestination();
    let currentMelody = null;
    let isPlaying = false;

    tempoSlider.addEventListener('input', (e) => {
        tempoValue.textContent = `${e.target.value} BPM`;
    });

    const getParams = () => new URLSearchParams({
        key: document.getElementById('key').value,
        scale: document.getElementById('scale').value,
        tempo: document.getElementById('tempo').value,
        genre: document.getElementById('genre').value
    });

    generateBtn.addEventListener('click', async () => {
        try {
            generateBtn.disabled = true;
            playBtn.disabled = true;
            stopBtn.disabled = true;
            downloadBtn.disabled = true;
            progressBar.style.width = '50%';

            const response = await fetch(`/generate?${getParams().toString()}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            // Store the blob for later download
            currentMelody = await response.blob();

            progressBar.style.width = '100%';
            playBtn.disabled = false;
            downloadBtn.disabled = false;
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate music');
        } finally {
            generateBtn.disabled = false;
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 1000);
        }
    });

    playBtn.addEventListener('click', () => {
        if (!isPlaying) {
            const key = document.getElementById('key').value;
            const scale = document.getElementById('scale').value;
            const tempo = parseInt(document.getElementById('tempo').value);

            // Create a simple preview melody based on the selected key and scale
            const baseNote = key + '4';
            const interval = scale === 'major' ? 4 : 3;
            const notes = [
                baseNote,
                Tone.Frequency(baseNote).transpose(interval).toNote(),
                Tone.Frequency(baseNote).transpose(7).toNote(),
                baseNote
            ];

            // Calculate note duration based on tempo
            const noteDuration = 60 / tempo;

            // Play the preview melody
            const now = Tone.now();
            notes.forEach((note, i) => {
                synth.triggerAttackRelease(note, noteDuration, now + i * noteDuration);
            });

            isPlaying = true;
            playBtn.innerHTML = '<i class="bi bi-pause-circle"></i> Pause';
            stopBtn.disabled = false;
        } else {
            synth.releaseAll();
            isPlaying = false;
            playBtn.innerHTML = '<i class="bi bi-play-circle"></i> Play';
        }
    });

    stopBtn.addEventListener('click', () => {
        synth.releaseAll();
        isPlaying = false;
        playBtn.innerHTML = '<i class="bi bi-play-circle"></i> Play';
        stopBtn.disabled = true;
    });

    downloadBtn.addEventListener('click', () => {
        if (currentMelody) {
            const url = window.URL.createObjectURL(currentMelody);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'generated_music.mid';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }
    });
});