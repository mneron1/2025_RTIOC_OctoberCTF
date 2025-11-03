# 🧩 **OCTOBER CTF – DAY 01**

> 🏷️ *Category:* **Forensics / Encoding**
> ⚙️ *Difficulty:* **Easy–Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Braille ASCII`, `File Extension Analysis`, `Leetspeak Decoding`

---

## 📜 Challenge Description

> 💬
> “While cleaning up old files, I found a file I made a long time ago called `message.txt`.
>
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

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The text file doesn’t render properly, suggesting **file type confusion** — it may not actually be plain text.
>
> Once fixed, the file supposedly reveals a **Braille ASCII sequence**, which can then be **translated into readable text**.
>
> The final flag will include **leetspeak substitutions** (`a → 4`, `i → 1`, `e → 3`, etc.).

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* Opening `message.txt` in a text editor produced unreadable binary symbols.
* The gibberish resembled **binary image headers** (e.g., `‰PNG`), hinting that this was **actually an image file mislabeled as `.txt`**.
* Hypothesis: The file extension is incorrect.

---

### 🔹 Step 2: Test File Type Hypothesis

Check the real file type:

```bash
file message.txt
```

🧩 **Result:**

```
message.txt: PNG image data
```

So the file was indeed a **.png image disguised as text**.

Rename it:

```bash
mv message.txt message.png
```

Then open it with any image viewer.

---

### 🔹 Step 3: Examine the Image Content

🧩 Upon opening `message.png`, the image displayed **a sequence of Braille dots** arranged to form a readable pattern.

Each symbol corresponded to **Braille ASCII** — a 6-dot representation of letters and numbers.

---

### 🔹 Step 4: Decode the Braille ASCII

Use the Braille ASCII conversion table from [Wikipedia’s Braille ASCII article](https://en.wikipedia.org/wiki/Braille_ASCII) to map each Braille symbol to its equivalent Latin letter.

You can do this manually or by using an online Braille translator.

---

### 🔹 Step 5: Translate Leetspeak

Once the Braille was decoded into normal text, the result included **numbers replacing certain letters** according to *leetspeak* conventions:

| Letter | Leet Equivalent |
| ------ | --------------- |
| A      | 4               |
| E      | 3               |
| I      | 1               |
| O      | 0               |
| S      | 5               |
| T      | 7               |

Use this mapping to interpret the final message correctly.

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

> The `.txt` file wasn’t a text file at all — it was a **PNG image** misnamed to disguise its true format.
> Once renamed and viewed correctly, it contained **Braille ASCII**, a compact way of representing Braille using printable characters.
> Translating from Braille ASCII revealed the hidden flag, which was stylized using **leetspeak**.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language     | 💡 Purpose                            |
| ---------------------- | ------------------------------------- |
| 🧮 `file` command      | Identify true file type               |
| 🖼️ Image viewer       | Display the hidden PNG image          |
| 🔡 Braille ASCII table | Decode Braille patterns               |
| 🔠 Leetspeak reference | Interpret number–letter substitutions |

---

## 📚 Key Learnings

| 🔑 Concept              | 🧠 Takeaway                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| File extension spoofing | File extensions can mislead you; always check the magic bytes                |
| Braille ASCII           | Converts Braille dots into standard ASCII characters                         |
| Leetspeak               | A playful encoding often used in CTFs for obfuscation                        |
| Layered encoding        | Challenges may combine multiple encoding steps (e.g., Braille → Leet → Flag) |

---

## 💬 Final Thoughts

> 🔍 This challenge was a fun reminder that **not everything is what it seems** — even a `.txt` file might hide an image.
> By following forensic instincts and checking the file structure, we uncovered a clever double-layered encoding.
>
> A simple yet elegant warm-up for the October CTF series. 🎯💪

---
⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Forensics / Encoding
---