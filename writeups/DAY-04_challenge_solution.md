# 🧩 **Tunes**

> 🏷️ *Category:* **OSINT / Web**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **Cyber Security CTF (CTFd instance)**
> 🧠 *Concepts:* VirtualPiano notation, OSINT, pattern recognition

---

## 📜 Challenge Description

> 💬
> Who composed this song?
> Decode the message below to identify the composer. The pattern might be more musical than you think.
>
> > [5a] [$y] 3
>
> flag format: flag{firstName_lastName}

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description        | 💾 Value      |
| ------------------ | --------------------- | ------------- |
| `challenge text`   | challenge description | —             |
| `pattern`          | clue to decode        | `[5a] [$y] 3` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ The challenge asks for the **composer** of a song whose title is *encoded* by the short token `[5a] [$y] 3`. The description hints the string “might be more musical than you think,” so the best approach is OSINT: treat the token as a literal pattern or notation and search for where that exact pattern appears online (rather than attempting heavy crypto/music-theory decoding).

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The clue uses square-bracket groups and single characters — it looks like a **music/keyboard pattern** (many online piano/tutor sites use bracketed groups to show simultaneous keys).
* The simplest path is to **search the exact string** `"[5a] [$y] 3"` (including brackets/spacing) — this is an OSINT problem, not a deep cipher.

---

### 🔹 Step 2: Search / Recon (OSINT)

* Open Google and search the exact quoted string:

  ```
  "[5a] [$y] 3"
  ```
* One of the top hits is a **Virtual Piano** page (virtualpiano.net) showing keyboard bindings / a playable sheet where that exact key sequence appears.
* VirtualPiano and similar sites use a mapping of computer keys→piano notes; the bracketed groups are chords/keys to press together. The pattern therefore **is literal VirtualPiano notation** for a short phrase in a song.

---

### 🔹 Step 3: Identify the Song (listen / verify)

* Open the VirtualPiano page result and play the sequence (or paste the pattern into the site’s player if supported) to hear the short riff.
* The snippet matches the intro/theme of **“Circle of Life”** from *The Lion King*.
* Confirm by searching the VirtualPiano sheet or YouTube for the corresponding sequence → it maps to that song.

🧾 **Result:** The song is **“Circle of Life”**.

---

### 🔹 Step 4: Recover the Flag (composer)

* Who **composed** the song (music)? For *Circle of Life* (the pop/film single version), the music is credited to **Elton John** (lyrics by Tim Rice). The challenge asks for the composer, so submit Elton John.

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{Elton_John}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> This challenge was not a cryptographic puzzle or musical-theory exercise — it was an **OSINT recognition** task. The clue used **VirtualPiano-style notation**; searching the exact string pointed directly to an online piano sheet where that sequence is used. Once you hear/verify the short phrase, identifying the title and composer is straightforward.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language  | 💡 Purpose                                |
| ------------------- | ----------------------------------------- |
| 🔎 Google / Search  | Locate exact-match instances of the token |
| 🌐 Browser DevTools | Inspect challenge JSON / confirm no files |
| 🎹 VirtualPiano.net | Play/verify the key sequence              |
| 📝 Note-taking      | Record the song title & composer          |

---

## 📚 Key Learnings

| 🔑 Concept     | 🧠 Takeaway                                               |
| -------------- | --------------------------------------------------------- |
| OSINT search   | Exact-quoted search for short tokens is powerful          |
| Literal clues  | Puzzle text often intends a literal (not cryptic) read    |
| Validate audio | When a musical site appears, play the sequence to confirm |

---

## 💬 Final Thoughts

> ✨ This was a good reminder: **start simple**. Before applying complicated cryptanalysis or overthinking musical encodings, try an exact string search — the answer was literally hosted online in the same notation. Quick OSINT + a short listen = flag. Nice and tidy!

---
⭐ **Solver:** Mathieu Néron (or your team name)  
🕒 **Date:** Nov 2025  
🏆 **CTF Event:** Cyber Security CTF (ctfd instance)  
📍 **Category:** OSINT / Web
---