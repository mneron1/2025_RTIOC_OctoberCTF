# 🧩 **OCTOBER CTF – DAY 01**

> 🏷️ *Category:* **Forensics / Encoding**
> ⚙️ *Difficulty:* **Easy – Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Braille ASCII`, `File Type Analysis`, `Leetspeak Decoding`

---

## 📜 Challenge Description

> 💬
> “While cleaning up old files, I found a file I made a long time ago called `message.txt`.
> When I try to open the file, it doesn’t display properly — something’s not right with it.
>
> Can you help me read the file properly and decode the message inside?
>
> **Note:** Braille ASCII was used to encode the message, and the flag contains *leetspeak* ([Wikipedia link](https://simple.wikipedia.org/wiki/Leet)).
> For example, the name *David* would become *D4v1d*.”

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                              | 💾 Value |
| ------------------ | ------------------------------------------- | -------: |
| `message.txt`      | File that appears corrupted or misformatted |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's analyze what’s happening:

> The provided file doesn’t render properly — suggesting **it might not actually be plain text**.
> Once its real type is identified, we’ll likely find **Braille ASCII** inside, which must then be decoded.
> The decoded text will include **leetspeak substitutions** (e.g., `a→4`, `e→3`, `i→1`), which form the final flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* Opening `message.txt` in a standard text editor produced unreadable symbols.
* The gibberish resembled **binary file headers** — notably, `‰PNG`, which hints at a **PNG image**.
* Hypothesis: the file extension was renamed incorrectly.

---

### 🔹 Step 2: Verify the Actual File Type

Check the file’s magic bytes using the `file` command:

```bash
file message.txt
```

🧾 **Output:**

```
message.txt: PNG image data
```

✅ The file is **a PNG image** disguised as a `.txt`.

Rename it back to its proper format:

```bash
mv message.txt message.png
```

Now open it using any image viewer.

---

### 🔹 Step 3: Analyze the Image Content

Upon opening `message.png`, we can see a **pattern of Braille dots**.
Each pattern represents a character in **Braille ASCII** — a textual encoding of Braille cells using printable characters.

---

### 🔹 Step 4: Decode the Braille ASCII

Use a Braille ASCII chart (see [Wikipedia: Braille ASCII](https://en.wikipedia.org/wiki/Braille_ASCII)) or an online converter.

Example of manual decoding:

```
⠋⠇⠁⠛{⠑⠭⠁⠍⠏⠇⠑}
↓
flag{example}
```

This translation yields readable text with **numbers replacing letters** according to leetspeak.

---

### 🔹 Step 5: Translate from Leetspeak

Apply the leetspeak substitutions:

| Letter | Leet Equivalent |
| :----: | :-------------: |
|    A   |        4        |
|    E   |        3        |
|    I   |        1        |
|    O   |        0        |
|    S   |        5        |
|    T   |        7        |

Decoding the message accordingly reveals the final flag.

---

### 🔹 Step 6: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{example_1n_l337_bra1ll3}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> The `.txt` file was a **disguised image** — by renaming it properly, we uncovered a PNG containing **Braille ASCII** text.
> Translating Braille ASCII gave us a readable message written in **leetspeak**, which then formed the final flag.

This challenge emphasizes **file type verification** and **layered decoding** — classic steps in forensics-style puzzles.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Technique    | 💡 Purpose                                |
| ---------------------- | ----------------------------------------- |
| 🧮 `file` command      | Identify true file type using magic bytes |
| 🖼️ Image viewer       | Display hidden PNG image                  |
| 🔡 Braille ASCII table | Decode Braille characters                 |
| 🔠 Leetspeak mapping   | Convert obfuscated text to readable flag  |

---

## 📚 Key Learnings

| 🔑 Concept              | 🧠 Takeaway                                                   |
| ----------------------- | ------------------------------------------------------------- |
| File extension spoofing | File names can mislead; inspect headers, not extensions       |
| Braille ASCII           | Represents Braille with printable ASCII characters            |
| Leetspeak               | A CTF-favorite obfuscation using numeric substitutions        |
| Multi-layer encoding    | Combining encodings hides meaning deeper than one layer alone |

---

## 💬 Final Thoughts

> 🧩 This was a clever warm-up — a “fake” text file that turned out to be an image hiding a Braille code.
> A gentle reminder that **surface appearances can be deceiving** — always check what a file *really is*!
> Perfect start to the October CTF series. 🕵️‍♂️🎯

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** October CTF Series  
📍 **Category:** Forensics / Encoding  
---