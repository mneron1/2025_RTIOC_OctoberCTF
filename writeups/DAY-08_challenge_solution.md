🧩 OCTOBER CTF – DAY 08

🏷️ *Category:* **Forensics / Image Recognition**
⚙️ *Difficulty:* **Easy–Medium**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Visual OSINT, Image Metadata, LSB Analysis**

📜 Challenge Description

💬
“I found this orange owl logo — looks familiar, but the details are fuzzy.
It might be hiding something, or maybe the answer is in plain sight…”

🖼️ Provided file: DAY08_Owl.jpg

Goal: Identify the programming language and the designer associated with the owl logo.

Flag format:

flag{language_designerName}

📦 Provided Files / Data
📁 File / Variable	🔍 Description	💾 Value
DAY08_Owl.jpg	Noisy image of an orange owl inside a white circle	—
🧠 Understanding the Problem

The challenge likely tests recognition skills and steganography basics:

If the image contains hidden data, stego tools (e.g., zsteg, steghide) would reveal it.

If not, it could simply require identifying a known logo or symbol visually.

Given the name “Owl” and color scheme, the orange bird imagery suggested a language mascot rather than a hidden binary payload.

🧩 Step-by-Step Solution
🔹 Step 1 – Metadata Inspection

Checked for hidden EXIF or metadata entries:

from PIL import Image
img = Image.open("DAY08_Owl.jpg")
print(img.getexif())


🧩 Result: No EXIF or custom tags found. The file contained no embedded metadata.

🔹 Step 2 – LSB (Least Significant Bit) Extraction

Tested for steganographic content within pixel bitplanes:

from PIL import Image
import numpy as np
img = Image.open("DAY08_Owl.jpg").convert("RGB")
pixels = np.array(img)
lsb = (pixels & 1)
gray = (lsb[:,:,0]*85 + lsb[:,:,1]*85 + lsb[:,:,2]*85).astype('uint8')
Image.fromarray(gray).save("lsb_output.png")


🧩 Result: No discernible shapes or text; image appeared uniform — likely no hidden LSB message.

🔹 Step 3 – Run Stego Tools

Tested using standard stego utilities:

steghide info -sf DAY08_Owl.jpg
zsteg -a DAY08_Owl.png
binwalk -e DAY08_Owl.jpg


🧩 Result: No appended data, hidden payloads, or bitplane encodings detected.

🔹 Step 4 – Visual Identification

With no hidden data, the focus shifted to the image itself:

The orange owl inside a white circle is the official SWI-Prolog mascot.

Designer attribution (via official sources): Steve Reeves.

Hence, following the required format:

flag{Prolog_SteveReeves}

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{Prolog_SteveReeves}

</details>
📘 Explanation — Why It Works

💡 Not all forensics challenges involve technical steganography.
Sometimes, “recognition” itself is the test — here, the Prolog owl logo serves as a direct clue.
While stego checks confirmed no embedded content, visually identifying the mascot provided the answer.

🧰 Tools & Techniques Used
🧩 Tool / Platform	💡 Purpose
🐍 Python (Pillow / NumPy)	Image metadata & LSB inspection
🧮 zsteg / steghide	Automated stego scanning
🔍 binwalk	Detect appended binary data
👀 Manual OSINT	Visual recognition of known logo
📚 Key Learnings
🔑 Concept	🧠 Takeaway
Not every image hides data	Some challenges test recognition or research ability
Stego triage	Always check metadata, LSB, and visual clues systematically
OSINT meets CTF	Identifying real-world symbols can solve puzzles faster
💬 Final Thoughts

🦉 Sometimes, the most effective “decoder” is your own memory.
Not every secret hides in bits and bytes — some hide in plain sight.

---
⭐ Author: mneron1  
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Forensics / Image Recognition
---