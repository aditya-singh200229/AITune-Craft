import os
import logging
from flask import Flask, render_template, jsonify, send_file
from music_generator import generate_midi
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "music_generator_secret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Generate MIDI file in temporary directory
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as temp_file:
            generate_midi(temp_file.name)
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name='generated_music.mid',
                mimetype='audio/midi'
            )
    except Exception as e:
        logging.error(f"Error generating MIDI: {str(e)}")
        return jsonify({'error': str(e)}), 500
