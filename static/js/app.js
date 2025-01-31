document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const previewBtn = document.getElementById('previewBtn');
    const progressBar = document.getElementById('progressBar');
    const tempoSlider = document.getElementById('tempo');
    const tempoValue = document.getElementById('tempoValue');
    const synth = new Tone.PolySynth().toDestination();

    tempoSlider.addEventListener('input', (e) => {
        tempoValue.textContent = `${e.target.value} BPM`;
    });

    generateBtn.addEventListener('click', async () => {
        try {
            generateBtn.disabled = true;
            progressBar.style.width = '50%';

            const params = new URLSearchParams({
                key: document.getElementById('key').value,
                scale: document.getElementById('scale').value,
                tempo: document.getElementById('tempo').value,
                genre: document.getElementById('genre').value
            });

            const response = await fetch(`/generate?${params.toString()}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Generation failed');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'generated_music.mid';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            progressBar.style.width = '100%';
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

    previewBtn.addEventListener('click', () => {
        const key = document.getElementById('key').value;
        const scale = document.getElementById('scale').value;
        const notes = scale === 'major' 
            ? [`${key}4`, `${key}4`, `${key}5`, `${key}4`]
            : [`${key}4`, `${key}4`, `${key}4`, `${key}3`];

        const now = Tone.now();
        notes.forEach((note, i) => {
            synth.triggerAttackRelease(note, '8n', now + i * 0.5);
        });
    });
});