🧩 OCTOBER CTF – DAY 10

🏷️ *Category:* **Reverse Engineering / Web / JavaScript**
⚙️ *Difficulty:* **Hard**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **XOR Encoding, JS-to-Python Translation, Raw Byte Extraction**

📜 Challenge Description

💬
“There’s something unusual hidden in the code of a small website I built.
See if you can decode my secret message!”

Goal: Locate and decode the hidden flag embedded inside the provided website archive (index.html).

📦 Provided Files / Data
📁 File	🔍 Description
index.html	Contains a custom XOR-encoded JavaScript function and hidden data
🧠 Understanding the Problem

Inside the site’s source, a suspicious comment stood out:

//super secret txt = `SlTgNcZnFoYelZg"]eYlZ BoGlQ"}`
//super secret pass = 0b101


The xorEncode(txt, pass) function used JavaScript’s String.fromCharCode to XOR each character of txt with the corresponding byte from pass.
However, the txt contained control characters (\x1b, \x1d, \x1c) and pass = 0b101 hinted at either binary 5 or the character '5' (ASCII 53).

This meant a custom XOR cipher was hiding the flag, but with a subtle JavaScript behavior that needed to be replicated precisely.

🧩 Step-by-Step Solution
🔹 Step 1 – Identify the XOR Logic

From the HTML:

for (j = z = 0; z < txt.length; z++) {
    buf += String.fromCharCode(ord[txt.substr(z, 1)] ^ ord[pass.substr(j, 1)]);
    j = (j < pass.length) ? j + 1 : 0;
}


🧩 Observation:
When pass has length 1, the substring call sometimes returns an empty string ('' → 0 in mapping).
As a result, only every other character is XORed, producing the alternating pattern that must be emulated in the decoder.

🔹 Step 2 – Extract the Raw Bytes

Copying directly from the HTML introduced escaped control characters.
To avoid corruption, a byte-level extraction was performed:

# extract_secret.py
import re
b = open("index.html", "rb").read()
m = re.search(b'super secret txt\\s*=\\s*`([\\s\\S]*?)`', b)
block_bytes = m.group(1)
print(block_bytes)


Output (escaped form):

SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}


Raw hex bytes:

53 6c 54 67 4e 63 5a 6e 46 6f 59 65 1b 6c 5a 67 1d 22 5d 65 59 6c 5a 20 42 6f 47 6c 51 22 1c 7d

🔹 Step 3 – Decode Logic in Python

To replicate the JS function accurately:

XOR only even indices.

Treat the pass as the character '5'.

Ignore non-printable ASCII when displaying results.

def cheat_decode_final(encoded: str, key_char: str) -> str:
    key = ord(key_char)
    chars = []
    for i, ch in enumerate(encoded):
        if i % 2 == 0:  # XOR even indices only
            chars.append(chr(ord(ch) ^ key))
        else:
            chars.append(ch)
    return ''.join(chars)

encoded = r"SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}"
encoded = encoded.encode("utf-8").decode("unicode_escape")
decoded = cheat_decode_final(encoded, "5")
print(''.join(c for c in decoded if 32 <= ord(c) < 127))

🔹 Step 4 – Output

Running the above script produced the decoded flag:

flag{console.log("hello world")}

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{console.log("hello world")}

</details>
📘 Explanation — Why It Works

💡 The JavaScript encoder used XOR with subtle index handling:

pass.substr(j,1) returned '' (0) every other cycle.

This effectively XORed only half of the characters.

Using '5' (ASCII 53) as the XOR key restored the original readable text.

Faithfully reproducing this logic in Python, rather than doing a simple XOR loop, was essential to revealing the flag.

🧰 Tools & Techniques Used
🧩 Tool / Library	💡 Purpose
🐍 Python 3	Byte-level decoding and XOR reconstruction
🔎 Regex extraction	Locate backtick-enclosed encoded blob
🧮 XOR logic replication	Mimic JS’s substring quirk
🧾 Hex viewers (xxd, VSCode Hex)	Verify raw control bytes
📚 Key Learnings
🔑 Concept	🧠 Takeaway
JS-to-Python behavior mismatch	Even minor differences (like empty substrings) matter
Raw extraction	Copying from HTML can corrupt non-printables
XOR analysis	Check both numeric and character interpretations of keys
Debugging tip	When output looks “half-right,” consider index misalignment
💬 Final Thoughts

⚙️ This challenge was a perfect reminder that faithful reproduction of language quirks can make or break reverse-engineering efforts.
A single substring behavior change — and the entire flag stays hidden.

---
⭐ Author: mneron1
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Reverse Engineering / Web / JavaScript
---