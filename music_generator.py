import random
from midiutil import MIDIFile

def get_scale(key='C', scale_type='major', octaves=2):
    """Generate a musical scale based on key and type across multiple octaves."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = {
        'major': [2, 2, 1, 2, 2, 2, 1],
        'minor': [2, 1, 2, 2, 1, 2, 2]
    }

    # Find starting index for the key
    start_idx = notes.index(key)
    scale_notes = []

    # Generate scale across specified octaves
    for octave in range(octaves):
        current_idx = start_idx
        octave_notes = []

        # Generate one octave of notes
        for interval in intervals[scale_type]:
            note = notes[current_idx]
            octave_notes.append((note, octave))
            current_idx = (current_idx + interval) % 12

        scale_notes.extend(octave_notes)

    return scale_notes

def note_to_midi_number(note, octave, base_octave=4):
    """Convert a note name and octave to MIDI note number."""
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
             'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    return 60 + notes[note] + ((base_octave + octave) - 4) * 12

def generate_midi(filename, tempo=120, key='C', scale_type='major', length=32):
    """Generate a MIDI file with basic music theory rules."""
    # Create MIDI file with 1 track
    midi = MIDIFile(1)
    track = 0
    time = 0

    # Setup track
    midi.addTempo(track, time, tempo)

    # Get scale notes with 2 octaves for more variety
    scale = get_scale(key, scale_type, octaves=2)

    # Keep track of previous note to create more musical movement
    prev_note_idx = None

    # Generate melody with more variation
    for i in range(length):
        # Avoid repeating same note too often
        if prev_note_idx is not None:
            # Prefer moving by steps or small intervals
            possible_indices = list(range(max(0, prev_note_idx - 3), 
                                       min(len(scale), prev_note_idx + 4)))
            note_idx = random.choice(possible_indices)
        else:
            note_idx = random.randint(0, len(scale) - 1)

        note, octave = scale[note_idx]
        midi_note = note_to_midi_number(note, octave)
        prev_note_idx = note_idx

        # More varied durations (eighth, quarter, or half note)
        duration = random.choice([0.5, 1, 2])

        # Vary velocity (volume) for more natural sound
        velocity = random.randint(85, 110)

        # Add note to track
        midi.addNote(track, 0, midi_note, time, duration, velocity)
        time += duration

    # Write file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)