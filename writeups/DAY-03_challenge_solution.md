# CTF Challenge Day 03
CTF Write-up: Invisible Ink
Challenge
Agent Joe received a .txt file that looked empty, with the message:
Find the flag ... --- ...

The hint ... --- ... is Morse code for SOS, suggesting hidden data. Opening the file showed no visible text, but something was clearly hidden.

## Investigation

Used cat -Raw file.txt and saw strange characters like:
â€‹â€€â€€â€€â€€ â€€â€‹ â€‹â€‹â€‹â€€ ...

These are mojibake representations of Unicode invisible characters:

U+200B → Zero-Width Space
U+2000 → En Quad

The file contained zero-width steganography.

## Solution Steps

Hypothesis: Two distinct invisible characters likely encode Morse code (dots and dashes).
Mapping:

U+200B → . (dot)
U+2000 → - (dash)

### Decoding:
Normalize spaces as separators.
Translate Morse to text using a standard Morse dictionary.


### Implementation:

Wrote a PowerShell script (decode-hidden.ps1) to:
1. Read file as UTF-8.
2. Detect invisible characters.
3. Decode Morse and binary (as fallback).

Execution:
.\decode-hidden.ps1 -Path .\file.txt

Decoded Flag
flag{1NV1S1BL3_M0R53}


## Key Learnings

Invisible characters (zero-width spaces, quads) are common in steganography.
UTF-8 decoding avoids mojibake issues.
Challenge hints often point to encoding type (SOS → Morse).
PowerShell can handle Unicode and decoding tasks effectively.

---

Generated with OpenAI ChatGPT

