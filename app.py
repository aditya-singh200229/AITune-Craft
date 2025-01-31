import os
import logging
import subprocess
from flask import Flask, render_template, jsonify, send_file, request
from music_generator import generate_midi
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "music_generator_secret"

@app.route('/')
def index():
    return render_template('index.html')

def generate_music_file(filename, params):
    """Generate a MIDI file with the given parameters."""
    key = params.get('key', 'C')
    scale = params.get('scale', 'major')
    tempo = int(params.get('tempo', 120))

    logging.debug(f"Generating MIDI with key={key}, scale={scale}, tempo={tempo}")

    generate_midi(
        filename,
        tempo=tempo,
        key=key,
        scale_type=scale,
        length=16
    )

@app.route('/generate', methods=['POST'])
def generate():
    try:
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as temp_file:
            generate_music_file(temp_file.name, request.args)
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name='generated_music.mid',
                mimetype='audio/midi'
            )
    except Exception as e:
        logging.error(f"Error generating MIDI: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-mp3', methods=['POST'])
def generate_mp3():
    try:
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as midi_file:
            generate_music_file(midi_file.name, request.args)

            # Convert MIDI to WAV using FluidSynth
            mp3_path = midi_file.name.replace('.mid', '.mp3')
            logging.debug(f"Converting {midi_file.name} to {mp3_path}")

            subprocess.run([
                'fluidsynth',
                '-ni',
                '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                midi_file.name,
                '-F',
                mp3_path,
                '-r',
                '44100'
            ], check=True)

            return send_file(
                mp3_path,
                as_attachment=True,
                download_name='generated_music.mp3',
                mimetype='audio/mpeg'
            )
    except Exception as e:
        logging.error(f"Error generating MP3: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)