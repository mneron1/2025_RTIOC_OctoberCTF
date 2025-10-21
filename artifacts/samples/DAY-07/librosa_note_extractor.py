import librosa
import numpy as np

# Frequency-to-note mapping using scientific pitch notation
def frequency_to_note(freq):
    A4_freq = 440.0
    if freq <= 0:
        return None
    semitones_from_A4 = int(round(12 * np.log2(freq / A4_freq)))
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_index = (semitones_from_A4 + 9) % 12
    octave = 4 + ((semitones_from_A4 + 9) // 12)
    return f"{note_names[note_index]}{octave}"

# Load the audio file
y, sr = librosa.load("secret_tunes.wav")

# Extract pitches and magnitudes
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Extract dominant pitches
note_sequence = []
for i in range(pitches.shape[1]):
    index = magnitudes[:, i].argmax()
    pitch = pitches[index, i]
    if pitch > 0:
        note_sequence.append(pitch)

# Convert frequencies to note names
note_names = []
for freq in note_sequence:
    note = frequency_to_note(freq)
    if note:
        note_names.append(note)

# Remove duplicates while preserving order
unique_notes = []
seen = set()
for n