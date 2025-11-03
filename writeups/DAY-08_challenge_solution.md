# 🧩 **OCTOBER CTF – DAY 08**

> 🏷️ *Category:* **Forensics / Image Recognition**
> ⚙️ *Difficulty:* **Easy–Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Visual OSINT`, `Image Metadata`, `Steganography`, `LSB Analysis`

---

## 📜 Challenge Description

> 💬
> “I found this orange owl logo — looks familiar, but the details are fuzzy.
> It might be hiding something, or maybe the answer is in plain sight…”
>
> 🖼️ **Provided file:** `DAY08_Owl.jpg`
>
> **Goal:** Identify the **programming language** and the **designer** associated with the owl logo.
>
> **Flag format:**
> `flag{language_designerName}`

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                                     | 💾 Value |
| ------------------ | -------------------------------------------------- | -------: |
| `DAY08_Owl.jpg`    | Noisy image of an orange owl inside a white circle |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The challenge could either hide data inside the image (**steganography**) or test the player’s ability to visually recognize a logo (**OSINT / recognition**).
>
> The prompt’s phrasing — “looks familiar” — suggested that this was less about hidden bytes and more about identifying a known mascot or symbol.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The owl image looked **clean**, not typical of images with steganographic payloads.
* Its design (flat orange bird in a white circle) looked **like a logo** — possibly of a programming language or software project.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

To rule out any hidden data, we first checked **metadata and bit-level structure**.

#### 🧾 Metadata inspection

```python
from PIL import Image
img = Image.open("DAY08_Owl.jpg")
print(img.getexif())
```

🧩 **Result:** No EXIF tags or embedded data were found — clean image header.

#### 🧮 LSB (Least Significant Bit) analysis

```python
from PIL import Image
import numpy as np

img = Image.open("DAY08_Owl.jpg").convert("RGB")
pixels = np.array(img)
lsb = (pixels & 1)
gray = (lsb[:,:,0]*85 + lsb[:,:,1]*85 + lsb[:,:,2]*85).astype('uint8')
Image.fromarray(gray).save("lsb_output.png")
```

🧩 **Result:** The LSB visualization produced uniform noise — no message or pattern.

---

### 🔹 Step 3: Perform the Extract / Decrypt / Analyze

After confirming no stego data, standard forensic tools were also tested:

```bash
steghide info -sf DAY08_Owl.jpg
zsteg -a DAY08_Owl.jpg
binwalk -e DAY08_Owl.jpg
```

🧩 **Result:**
No appended files, no ZIP signatures, and no bitplane text — confirming no hidden payload.

---

### 🔹 Step 4: Recover the Flag

With no technical leads, attention shifted to **visual recognition**.

* The orange owl inside a circular white background matches the **official SWI-Prolog mascot**.
* According to official references, the logo was designed by **Steve Reeves**.

✅ **Flag format:**
`flag{Prolog_SteveReeves}`

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{Prolog_SteveReeves}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> Not all forensic challenges involve deep steganography — some test **pattern recognition** and **research ability**.
> In this case, all technical stego checks returned negative, meaning the real solution was simply recognizing a **well-known logo**.
> The orange owl logo belongs to **SWI-Prolog**, and its designer is **Steve Reeves**.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language         | 💡 Purpose                               |
| -------------------------- | ---------------------------------------- |
| 🐍 Python (Pillow / NumPy) | Image metadata and LSB plane extraction  |
| 🧮 zsteg / steghide        | Steganography inspection                 |
| 🔍 binwalk                 | Check for embedded or appended data      |
| 👀 Manual OSINT            | Logo recognition and visual verification |

---

## 📚 Key Learnings

| 🔑 Concept             | 🧠 Takeaway                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| **Stego triage**       | Always start with metadata and LSB analysis before assuming complexity |
| **Visual recognition** | Many “forensic” images hide the answer in plain sight                  |
| **OSINT & research**   | Image identification skills are as valuable as data extraction         |

---

## 💬 Final Thoughts

> 🦉 This challenge reminded us that sometimes the hardest part isn’t decryption — it’s **seeing what’s already there**.
> Not every mystery hides in bits and bytes; some hide right before your eyes.
> Observation is your strongest forensic tool. 👁️‍🗨️

---

⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Forensics / Image Recognition
---