import librosa

y, sr = librosa.load("secret_tunes.wav")
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Extract dominant pitches
note_sequence = []
for i in range(pitches.shape[1]):
    index = magnitudes[:, i].argmax()
    pitch = pitches[index, i]
    if pitch > 0:
        note_sequence.append(pitch)

print(note_sequence)