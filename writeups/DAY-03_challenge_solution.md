# 🧩 OCTOBER CTF – DAY 03

🏷️ *Category:* **Steganography / Forensics**
⚙️ *Difficulty:* **Medium**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Unicode, Zero-Width Characters, Morse Code, PowerShell Automation**

## 📜 Challenge Description

💬
Challenge Name: Invisible Ink

Agent Joe received a .txt file that looked completely empty, with a single line reading:

Find the flag ... --- ...


The sequence ... --- ... corresponds to “SOS” in Morse code — a distress signal hinting that hidden information may be embedded in the file.

Goal: Reveal the invisible message and extract the flag.

## 📦 Provided Files / Data
## 📁 File / Variable	🔍 Description	💾 Value
file.txt	Text file appearing empty	—
## 🧠 Understanding the Problem

🕵️‍♂️ The .txt file appears blank, but hints suggest the presence of hidden Unicode characters (zero-width spaces or other invisible code points).
Such characters are often used in steganography, where binary or symbolic data is encoded invisibly within text.

## 🧩 Step-by-Step Solution
### 🔹 Step 1 – Inspecting the File

Running:

cat -Raw file.txt


revealed odd mojibake characters like:

â€‹â€€â€€â€€â€€ â€€â€‹ â€‹â€‹â€‹â€€ ...


These characters correspond to invisible Unicode glyphs:

Unicode	Name	Role
U+200B	Zero-Width Space	Dot (·)
U+2000	En Quad	Dash (–)
### 🔹 Step 2 – Hypothesis

The two invisible characters encode Morse code, using:

U+200B → .
U+2000 → -


Spaces act as separators between symbols and letters.

### 🔹 Step 3 – Decoding Logic

Read the file as UTF-8 to preserve Unicode integrity.

Map invisible characters to . and -.

Normalize spaces into Morse symbol breaks.

Decode Morse to ASCII text.

As fallback, check for binary interpretation if Morse fails.

### 🔹 Step 4 – Implementation (PowerShell)
decode-hidden.ps1
param([string]$Path)

$content = Get-Content -Raw -Encoding UTF8 $Path
$content = $content -replace "`u200B", "." -replace "`u2000", "-"
$morse = $content -replace "\s+", " "
$decoded = ""
$map = @{
    ".-"="A"; "-..."]="B"; "-.-."]="C"; "-.."]="D"; "."="E"; "..-."]="F";
    "--."]="G"; "...."]="H"; ".."]="I"; ".---"]="J"; "-.-"]="K"; ".-.."]="L";
    "--"]="M"; "-."]="N"; "---"]="O"; ".--."]="P"; "--.-"]="Q"; ".-."]="R";
    "..."]="S"; "-"]="T"; "..-"]="U"; "...-"]="V"; ".--"]="W"; "-..-"]="X";
    "-.--"]="Y"; "--.."]="Z";
}

foreach ($symbol in $morse.Trim().Split(" ")) {
    $decoded += $map[$symbol]
}

Write-Output $decoded


Run the script:

.\decode-hidden.ps1 -Path .\file.txt

### 🔹 Step 5 – Result

The decoded output reveals the hidden flag:

<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{1NV1S1BL3_M0R53}

</details>

## 📘 Explanation — Why It Works

💡 Invisible Unicode characters are frequently used in steganography because they don’t appear visually, yet can encode binary or symbolic patterns.
In this case, two characters (Zero-Width Space and En Quad) were cleverly chosen to represent Morse dots and dashes, forming a fully hidden SOS-style message.

## 🧰 Tools & Techniques Used
## 🧩 Tool / Language	💡 Purpose
🪟 PowerShell	Unicode parsing and decoding
🧠 Unicode Inspector	Identify invisible characters
🌐 Online Morse Decoders	Cross-check decoded sequences
🧾 cat -Raw / xxd	Raw character visualization
📚 Key Learnings
🔑 Concept	🧠 Takeaway
Zero-width characters	Can carry data invisibly in plain text
Unicode handling	Essential for forensic text analysis
Morse encoding	Simple yet powerful form of symbolic encoding
PowerShell scripting	Efficient for Unicode and text processing

## 💬 Final Thoughts

✨ This challenge highlights how invisible Unicode can be weaponized for covert communication or CTF tricks.
Always check “empty” files — the real message may be hiding in plain sight.
---
⭐ Author: mneron1  
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Steganography / Forensics
---