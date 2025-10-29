🧩 OCTOBER CTF – DAY 06

🏷️ *Category:* **Steganography / Forensics**
⚙️ *Difficulty:* **Medium**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Alpha Channel Analysis, LSB Steganography, Image Forensics**

📜 Challenge Description

💬
"I've been working on a new method to hide sensitive data in images for secure communications.
I was very careful to hide my flag this time... Take a look at my test file and see if you can spot anything unusual."

File provided:
v.0_secretCommunicationTestFile_finalfinal3.png

Goal: Find the hidden flag inside the image.

📦 Provided Files / Data
📁 File / Variable	🔍 Description	💾 Value
v.0_secretCommunicationTestFile_finalfinal3.png	Black PNG file used to hide data	—
🧠 Understanding the Problem

The image appears entirely black, suggesting that visible data was replaced or hidden using:

Invisible color channels (Alpha)

Subtle near-black variations

LSB (Least Significant Bit) encoding

PNG metadata or appended binary data

The goal is to reveal any hidden content — visually or through steganographic analysis.

🧩 Step-by-Step Solution
🔹 Step 1 – Inspect Metadata
exiftool v.0_secretCommunicationTestFile_finalfinal3.png


Look for Comment, Description, or Software fields that might contain hints.

🧩 Result: No visible metadata leaks.

🔹 Step 2 – Check PNG Chunks and Embedded Strings
strings v.0_secretCommunicationTestFile_finalfinal3.png | findstr flag
pngcheck -v v.0_secretCommunicationTestFile_finalfinal3.png


🧩 Result: No readable flag found in textual chunks.

🔹 Step 3 – Extract Channels

Use ImageMagick to separate each color channel:

magick v.0_secretCommunicationTestFile_finalfinal3.png -alpha extract alpha.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel R -separate R.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel G -separate G.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel B -separate B.png


Then enhance the alpha channel for visibility:

magick alpha.png -auto-level alpha_revealed.png


🧩 Result: Subtle data may become visible in the alpha-revealed output.

🔹 Step 4 – Brighten the Image

Enhance brightness and contrast to expose faint patterns:

magick v.0_secretCommunicationTestFile_finalfinal3.png -evaluate multiply 12 -auto-level revealed.png


🧩 Result: Hidden contours may appear faintly, confirming steganographic manipulation.

🔹 Step 5 – Analyze with zsteg

Run automated analysis for LSB and text-based payloads:

zsteg -a v.0_secretCommunicationTestFile_finalfinal3.png


🧩 Result: zsteg successfully extracts the embedded flag from the image’s pixel data.

🔹 Step 6 – (Optional) Check for Appended Data
binwalk -e v.0_secretCommunicationTestFile_finalfinal3.png


🧩 Result: No appended data found — confirming the flag is embedded in the image data itself.

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{paint_ftw}

</details>
📘 Explanation — Why It Works

💡 Steganographic tools such as zsteg analyze the least significant bits (LSBs) of image pixel data.
Even when the picture looks perfectly black, those bits can hold structured binary data — like ASCII characters forming a flag.
The challenge author likely encoded the flag in the alpha channel or bit planes of the PNG file.

🧰 Tools & Techniques Used
🧩 Tool / Platform	💡 Purpose
🪟 PowerShell	Native CLI for running commands on Windows
🧮 ExifTool	Inspect image metadata
🖼️ ImageMagick	Extract and enhance color/alpha channels
🧩 zsteg	Steganography analysis (LSB and text extraction)
🧰 Binwalk	Detect hidden or appended binary data
📚 Key Learnings
🔑 Concept	🧠 Takeaway
Black images	Often hide content in alpha or LSB channels
zsteg	Detects invisible pixel-level encodings
Channel separation	Quick way to visually inspect hidden content
PNG metadata	Should always be inspected in stego challenges
💬 Final Thoughts

🖤 Sometimes, the most invisible things hold the clearest secrets.
Even a solid-black image can contain a message if you look through the right channel.
---
⭐ Author: mneron1  
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Steganography / Forensics
---