# 🧩 **OCTOBER CTF – DAY 06**

> 🏷️ *Category:* **Steganography / Forensics**
> ⚙️ *Difficulty:* **Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Alpha Channel Analysis`, `LSB Steganography`, `Image Forensics`

---

## 📜 Challenge Description

> 💬
> “I've been working on a new method to hide sensitive data in images for secure communications.
> I was very careful to hide my flag this time... Take a look at my test file and see if you can spot anything unusual.”
>
> 🖼️ **Provided file:** `v.0_secretCommunicationTestFile_finalfinal3.png`
>
> **Goal:** Find the hidden flag inside the image.

---

## 📦 Provided Files / Data

| 📁 File / Variable                                | 🔍 Description                                     | 💾 Value |
| ------------------------------------------------- | -------------------------------------------------- | -------: |
| `v.0_secretCommunicationTestFile_finalfinal3.png` | Black PNG image potentially containing hidden data |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The image appears **completely black**, suggesting that data could be hidden through **invisible channels** (like the alpha layer) or **least significant bits (LSB)** of pixel values.
>
> Typical hiding spots in such files include:
>
> * Alpha transparency channel
> * Near-black pixel variations
> * Embedded metadata (text chunks in PNG)
> * Hidden binary payloads appended after the image data

Our task: analyze every layer, extract hidden information, and reveal the flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The image is uniformly black — no visible artifacts.
* PNGs can hold multiple layers and bitplanes, making them ideal for steganography.
* No obvious compression artifacts — indicating possible **pixel-level encoding**.

---

### 🔹 Step 2: Inspect Metadata and Structure

```bash
exiftool v.0_secretCommunicationTestFile_finalfinal3.png
```

🧩 **Result:**
No hidden metadata, comments, or text fields found.
The file’s EXIF and tEXt chunks were clean.

We also verified chunk integrity:

```bash
pngcheck -v v.0_secretCommunicationTestFile_finalfinal3.png
```

🧩 **Result:**
Valid PNG file, no structural anomalies.

---

### 🔹 Step 3: Channel Extraction

To isolate hidden layers, extract each color and alpha channel using **ImageMagick**:

```bash
magick v.0_secretCommunicationTestFile_finalfinal3.png -alpha extract alpha.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel R -separate R.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel G -separate G.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel B -separate B.png
```

Then enhance contrast and brightness to visualize any hidden data:

```bash
magick alpha.png -auto-level alpha_revealed.png
```

🧩 **Result:**
Subtle variations in the **alpha channel** hinted at hidden information not visible in RGB layers.

---

### 🔹 Step 4: Brightness Amplification

To make near-black variations visible:

```bash
magick v.0_secretCommunicationTestFile_finalfinal3.png -evaluate multiply 12 -auto-level revealed.png
```

🧩 **Result:**
Faint patterns appeared, suggesting the presence of LSB-based data encoding.

---

### 🔹 Step 5: Automated LSB Extraction

Use **zsteg** to analyze the PNG bitplanes:

```bash
zsteg -a v.0_secretCommunicationTestFile_finalfinal3.png
```

🧩 **Result:**
`zsteg` successfully extracted readable ASCII text from the alpha channel’s least significant bits — revealing the hidden flag.

---

### 🔹 Step 6: (Optional) Binary Inspection

For completeness, check if data was appended after the image payload:

```bash
binwalk -e v.0_secretCommunicationTestFile_finalfinal3.png
```

🧩 **Result:**
No extra appended data found — confirming that the secret resided entirely within the image pixels.

---

### 🔹 Step 7: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{paint_ftw}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> Steganographic tools like `zsteg` analyze pixel-level binary data to detect patterns in **least significant bits (LSBs)**.
> Even when an image looks pure black, each pixel may contain encoded data in the lower bitplanes.
>
> In this case, the challenge creator likely embedded ASCII text directly into the alpha channel or one of the RGB bit layers — invisible to the naked eye but recoverable via LSB extraction.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language      | 💡 Purpose                             |
| ----------------------- | -------------------------------------- |
| 🧮 **ExifTool**         | Inspect embedded metadata              |
| 🖼️ **ImageMagick**     | Extract and enhance RGB/alpha channels |
| 🧩 **zsteg**            | Decode LSB-based steganography in PNGs |
| 🔍 **Binwalk**          | Detect appended or hidden binary files |
| 🪟 **PowerShell / CLI** | Command-line execution and automation  |

---

## 📚 Key Learnings

| 🔑 Concept             | 🧠 Takeaway                                             |
| ---------------------- | ------------------------------------------------------- |
| **Alpha channels**     | Often used to hide invisible data in PNGs               |
| **zsteg**              | Excellent for automating LSB and bitplane analysis      |
| **Visual enhancement** | Amplifying brightness can reveal hidden content         |
| **Black images**       | “Empty” images can still store rich steganographic data |

---

## 💬 Final Thoughts

> 🖤 Sometimes, the **darkest images hide the brightest secrets**.
> What looks like an empty PNG might hold a complete message — if you’re willing to peel back the layers.
>
> Steganography remains one of the most creative intersections of **art and cryptography**.

---
⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Steganography / Forensics
---