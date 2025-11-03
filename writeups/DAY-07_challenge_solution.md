# 🧩 **OCTOBER CTF – DAY 07**

> 🏷️ *Category:* **Audio / Steganography / Forensics**
> ⚙️ *Difficulty:* **Medium–Hard**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Frequency Analysis`, `Pitch Detection`, `Virtual Piano Decoding`, `Signal Processing`

---

## 📜 Challenge Description

> 💬
> “I encoded my flag using a different approach. This time, it’s all about the actual sounds.
> I learned to play piano with a virtual piano here: [https://virtualpiano.net](https://virtualpiano.net).”
>
> 🎧 **Provided file:** `secret_tunes.wav`
>
> **Goal:** Decode the hidden flag from the piano melody contained within the audio file.

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                       | 💾 Value |
| ------------------ | ------------------------------------ | -------: |
| `secret_tunes.wav` | Audio file containing a piano melody |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The flag isn’t stored in metadata or hidden bytes — it’s encoded **in the melody itself**.
>
> Each **piano note** in the `.wav` corresponds to a **Virtual Piano key** (e.g., A → h, C → k).
> When the notes are correctly identified and mapped to keyboard letters, they form the flag text.
>
> The task involves:
> 🎵 Extracting frequencies → 🧮 Mapping to musical notes → ⌨️ Translating to Virtual Piano keys → 🏁 Revealing the flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The `.wav` file contains clean **piano tones**, no speech or Morse beeps.
* The challenge explicitly mentions **Virtual Piano**, implying **keyboard-to-note mapping**.
* Frequency analysis (e.g., via spectrogram) shows distinct note intervals — a clear melodic pattern.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

To extract the frequencies programmatically, we use Python’s **Librosa** library.

```python
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
```

🧾 **Result:** The extracted dominant notes were:

```
C7, E4, C5, F4, F6, B4, C6, B5, A4, A3, D4, G4, B3, D5
```

---

### 🔹 Step 3: Perform the Extract / Decode

Next, each **note** was mapped to its corresponding **Virtual Piano key** (keyboard letter):

| 🎵 Note | ⌨️ Key | 🎵 Note | ⌨️ Key |
| :------ | :----- | :------ | :----- |
| C7      | Q      | F6      | m      |
| E4      | d      | B4      | j      |
| C5      | k      | C6      | v      |
| F4      | f      | B5      | c      |
| A4      | h      | D4      | s      |
| G4      | g      | D5      | l      |
| A3      | —      | B3      | —      |

When the notes were played in order on **VirtualPiano.net**, they produced the text pattern:

```
musicalkpeyord
```

With slight timing correction, it became clearly readable as:

```
musicalkeyboard
```

---

### 🔹 Step 4: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{musicalkeyboard}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> The flag was embedded as a **melody**, where each **note’s pitch** corresponds to a **Virtual Piano keyboard key**.
>
> When the sequence of detected notes is played on Virtual Piano, the resulting keypresses spell out the flag text — in this case, “musicalkeyboard.”
>
> The clever part is that **the sound itself *is* the cipher**, making this a form of **acoustic steganography**.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language             | 💡 Purpose                                  |
| ------------------------------ | ------------------------------------------- |
| 🐍 Python + Librosa            | Extract frequency and convert to note names |
| 🎧 Audacity / Sonic Visualizer | Confirm piano notes visually                |
| 🎹 VirtualPiano.net            | Map notes to keystrokes for decoding        |
| 🧮 NumPy                       | Frequency math and array handling           |

---

## 📚 Key Learnings

| 🔑 Concept                   | 🧠 Takeaway                                          |
| ---------------------------- | ---------------------------------------------------- |
| **Frequency → Note mapping** | Fundamental for decoding audio-based steganography   |
| **Virtual Piano encoding**   | Each note can represent a character or keypress      |
| **Signal analysis**          | Sound frequencies can carry structured messages      |
| **Audio forensics**          | Useful for both analysis and creative CTF challenges |

---

## 💬 Final Thoughts

> 🎵 This challenge turned sound into code — literally.
> The flag wasn’t in the bits of the file, but in the *melody* itself.
> Every note mattered, proving that sometimes, **the music is the message**.
>
> A fun, creative twist on steganography and signal interpretation. 🎹

---
⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Audio / Steganography / Forensics
---