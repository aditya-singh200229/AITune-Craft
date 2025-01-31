import random
from midiutil import MIDIFile

# MIDI drum note numbers
DRUM_NOTES = {
    'kick': 36,
    'snare': 38,
    'hihat': 42,
    'ride': 51
}

def get_scale(key='C', scale_type='major', octaves=2, base_octave=4):
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
            octave_notes.append((note, base_octave + octave))
            current_idx = (current_idx + interval) % 12

        scale_notes.extend(octave_notes)

    return scale_notes

def get_chord_progression(scale_type='major'):
    """Get a chord progression based on scale type."""
    if scale_type == 'major':
        return [1, 4, 5, 1]  # I-IV-V-I progression
    else:
        return [1, 6, 4, 5]  # i-vi-iv-v progression

def note_to_midi_number(note, octave):
    """Convert a note name and octave to MIDI note number."""
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
             'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    return 60 + notes[note] + (octave - 4) * 12

def generate_drum_pattern(measures=8):
    """Generate a basic drum pattern."""
    pattern = []
    for _ in range(measures):
        # Basic pattern: kick on 1 and 3, snare on 2 and 4, hihat every beat
        for beat in range(4):
            if beat in [0, 2]:
                pattern.append(('kick', beat * 1.0))
            if beat in [1, 3]:
                pattern.append(('snare', beat * 1.0))
            pattern.append(('hihat', beat * 1.0))
            pattern.append(('hihat', beat * 1.0 + 0.5))  # Add eighth notes
    return pattern

def generate_midi(filename, tempo=120, key='C', scale_type='major', base_octave=4, length=32, 
                 enable_chords=True, enable_drums=True):
    """Generate a MIDI file with melody, chords, and drums."""
    # Create MIDI file with 3 tracks (melody, chords, drums)
    midi = MIDIFile(3)
    time = 0

    # Setup tracks
    for track in range(3):
        midi.addTempo(track, time, tempo)
        # Set different instruments for each track
        midi.addProgramChange(track, 0, 0, 0 if track == 0 else 48 if track == 1 else 0)

    # Get scale notes
    scale = get_scale(key, scale_type, octaves=2, base_octave=base_octave)

    # Track 0: Melody
    prev_note_idx = None
    for i in range(length):
        if prev_note_idx is not None:
            possible_indices = list(range(max(0, prev_note_idx - 3), 
                                       min(len(scale), prev_note_idx + 4)))
            note_idx = random.choice(possible_indices)
        else:
            note_idx = random.randint(0, len(scale) - 1)

        note, octave = scale[note_idx]
        midi_note = note_to_midi_number(note, octave)
        prev_note_idx = note_idx

        duration = random.choice([0.5, 1, 2])
        velocity = random.randint(85, 110)
        midi.addNote(0, 0, midi_note, time, duration, velocity)
        time += duration

    # Track 1: Chords (if enabled)
    if enable_chords:
        time = 0
        progression = get_chord_progression(scale_type)
        chord_duration = 4  # One bar per chord

        for _ in range(length // 4):
            for chord_idx in progression:
                # Build triad from scale degrees
                root_idx = (chord_idx - 1) * 2
                third_idx = root_idx + 2
                fifth_idx = root_idx + 4

                if root_idx < len(scale):
                    root_note, root_oct = scale[root_idx]
                    third_note, third_oct = scale[third_idx % len(scale)]
                    fifth_note, fifth_oct = scale[fifth_idx % len(scale)]

                    # Add chord notes
                    for note, oct in [(root_note, root_oct), (third_note, third_oct), (fifth_note, fifth_oct)]:
                        midi_note = note_to_midi_number(note, oct)
                        midi.addNote(1, 0, midi_note, time, chord_duration, 70)

                time += chord_duration

    # Track 2: Drums (if enabled)
    if enable_drums:
        drum_pattern = generate_drum_pattern(measures=length//4)
        for drum, beat_time in drum_pattern:
            midi.addNote(2, 9, DRUM_NOTES[drum], beat_time, 0.25, 100)

    # Write file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)