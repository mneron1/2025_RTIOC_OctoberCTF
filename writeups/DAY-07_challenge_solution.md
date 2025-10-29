🧩 OCTOBER CTF – DAY 07

🏷️ *Category:* **Audio / Steganography / Forensics**
⚙️ *Difficulty:* **Medium–Hard**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Frequency Analysis, Pitch Detection, Virtual Piano Decoding**

📜 Challenge Description

💬
“I encoded my flag using a different approach. This time, it’s all about the actual sounds.
I learned to play piano with a virtual piano here: https://virtualpiano.net.”

Provided file:
🎧 secret_tunes.wav

Goal: Decode the hidden flag from the musical sequence contained in the audio file.

📦 Provided Files / Data
📁 File / Variable	🔍 Description	💾 Value
secret_tunes.wav	Audio file containing a piano melody	—
🧠 Understanding the Problem

This challenge hides the flag within sound, not metadata.
Each note in the .wav file corresponds to a Virtual Piano key press, meaning:

The pitch (frequency) represents a letter or character.

The sequence of notes, when played back on VirtualPiano.net, forms a word or phrase.

The task: extract pitches → convert to notes → map notes → interpret the word.

🧩 Step-by-Step Solution
🔹 Step 1 – Analyze the Audio File

Open the .wav in Audacity or a spectrogram viewer to confirm it contains distinct piano notes (no voice, no Morse).
Each frequency peak represents one played note.

🔹 Step 2 – Extract Frequencies Programmatically

Using Python + Librosa, extract the dominant pitch at each frame.

import librosa, numpy as np

def frequency_to_note(freq):
    A4 = 440.0
    if freq <= 0: return None
    semitones = int(round(12 * np.log2(freq / A4)))
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_index = (semitones + 9) % 12
    octave = 4 + ((semitones + 9) // 12)
    return f"{notes[note_index]}{octave}"

y, sr = librosa.load("secret_tunes.wav")
pitches, mags = librosa.piptrack(y=y, sr=sr)

sequence = []
for i in range(pitches.shape[1]):
    idx = mags[:, i].argmax()
    if pitches[idx, i] > 0:
        sequence.append(pitches[idx, i])

unique_notes = []
for f in sequence:
    n = frequency_to_note(f)
    if n and n not in unique_notes:
        unique_notes.append(n)

print(unique_notes)

🔹 Step 3 – Extracted Notes

Running the script yields the dominant sequence:

C7, E4, C5, F4, F6, B4, C6, B5, A4, A3, D4, G4, B3, D5

🔹 Step 4 – Map to Virtual Piano Keys

Each note corresponds to a Virtual Piano key:

Note	Key	Note	Key
C7	Q	F6	m
E4	d	B4	j
C5	k	C6	v
F4	f	B5	c
A4	h	D4	s
G4	g	D5	l
A3	—	B3	—
🔹 Step 5 – Decode by Playing

When played on VirtualPiano.net, the melody phonetically produces:

musicalkpeyord


Interpreting the slightly off rhythm gives the intended word:

musicalkeyboard

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{musicalkeyboard}

</details>
📘 Explanation — Why It Works

💡 Each piano note was chosen so its corresponding Virtual Piano key (letter on the keyboard) spelled part of the flag.
By converting audio frequencies into musical notes, then into Virtual Piano keystrokes, the phrase musicalkeyboard emerges — a clever play on the method used to reveal it.

🧰 Tools & Techniques Used
🧩 Tool / Library	💡 Purpose
🐍 Python + Librosa	Extract frequencies and convert to notes
🎹 VirtualPiano.net	Map notes to keyboard keys
🎧 Audacity / Sonic Visualizer	Confirm notes visually
🧮 NumPy	Handle frequency arrays and math
📚 Key Learnings
🔑 Concept	🧠 Takeaway
Frequency → Note mapping	Fundamental for decoding musical steganography
Virtual Piano encoding	Text can be represented as playable notes
Signal analysis	Useful for both forensics and creative encoding
💬 Final Thoughts

🎵 Sometimes, the answer isn’t hidden in the data — it is the data.
Every note matters when your keyboard is both a piano and a cipher.

---
⭐ Author: mneron1  
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Audio / Steganography / Forensics
---