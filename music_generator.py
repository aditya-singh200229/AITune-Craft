import random
from midiutil import MIDIFile

def get_scale(key='C', scale_type='major'):
    """Generate a musical scale based on key and type."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = {
        'major': [2, 2, 1, 2, 2, 2, 1],
        'minor': [2, 1, 2, 2, 1, 2, 2]
    }
    
    start_idx = notes.index(key)
    scale = [notes[start_idx]]
    current_idx = start_idx
    
    for interval in intervals[scale_type]:
        current_idx = (current_idx + interval) % 12
        scale.append(notes[current_idx])
        
    return scale

def generate_midi(filename, tempo=120, key='C', scale_type='major', length=16):
    """Generate a MIDI file with basic music theory rules."""
    # Create MIDI file with 1 track
    midi = MIDIFile(1)
    track = 0
    time = 0
    
    # Setup track
    midi.addTempo(track, time, tempo)
    
    # Get scale notes
    scale = get_scale(key, scale_type)
    base_note = 60  # Middle C
    
    # Generate melody
    for i in range(length):
        # Random note from scale
        note_idx = random.randint(0, len(scale) - 1)
        note = base_note + note_idx
        
        # Random duration (quarter or eighth note)
        duration = random.choice([1, 0.5])
        
        # Add note to track
        midi.addNote(track, 0, note, time, duration, 100)
        time += duration
    
    # Write file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
