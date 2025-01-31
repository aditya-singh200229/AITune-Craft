document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const previewBtn = document.getElementById('previewBtn');
    const progressBar = document.getElementById('progressBar');
    const synth = new Tone.PolySynth().toDestination();

    generateBtn.addEventListener('click', async () => {
        try {
            generateBtn.disabled = true;
            progressBar.style.width = '50%';

            const response = await fetch('/generate', {
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
        // Simple preview melody using Tone.js
        const now = Tone.now();
        const notes = ['C4', 'E4', 'G4', 'B4'];
        notes.forEach((note, i) => {
            synth.triggerAttackRelease(note, '8n', now + i * 0.5);
        });
    });
});
