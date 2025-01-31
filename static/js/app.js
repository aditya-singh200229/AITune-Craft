document.addEventListener('DOMContentLoaded', () => {
    const generateMidiBtn = document.getElementById('generateMidiBtn');
    const generateMp3Btn = document.getElementById('generateMp3Btn');
    const previewBtn = document.getElementById('previewBtn');
    const progressBar = document.getElementById('progressBar');
    const tempoSlider = document.getElementById('tempo');
    const tempoValue = document.getElementById('tempoValue');
    const synth = new Tone.PolySynth().toDestination();

    tempoSlider.addEventListener('input', (e) => {
        tempoValue.textContent = `${e.target.value} BPM`;
    });

    const getParams = () => new URLSearchParams({
        key: document.getElementById('key').value,
        scale: document.getElementById('scale').value,
        tempo: document.getElementById('tempo').value,
        genre: document.getElementById('genre').value
    });

    const handleDownload = async (endpoint, format) => {
        try {
            generateMidiBtn.disabled = true;
            generateMp3Btn.disabled = true;
            progressBar.style.width = '50%';

            const response = await fetch(`/${endpoint}?${getParams().toString()}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`Generation failed`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `generated_music.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            progressBar.style.width = '100%';
        } catch (error) {
            console.error('Error:', error);
            alert(`Failed to generate ${format.toUpperCase()} file`);
        } finally {
            generateMidiBtn.disabled = false;
            generateMp3Btn.disabled = false;
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 1000);
        }
    };

    generateMidiBtn.addEventListener('click', () => handleDownload('generate', 'mid'));
    generateMp3Btn.addEventListener('click', () => handleDownload('generate-mp3', 'mp3'));

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