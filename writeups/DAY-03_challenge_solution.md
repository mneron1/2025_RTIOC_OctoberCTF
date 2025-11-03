# 🧩 **OCTOBER CTF – DAY 03**

> 🏷️ *Category:* **Steganography / Forensics**
> ⚙️ *Difficulty:* **Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Zero-width Unicode`, `Morse code`, `Unicode parsing`, `PowerShell / text processing`

---

## 📜 Challenge Description

> 💬
> **Challenge Name:** Invisible Ink
>
> Agent Joe received a `.txt` file that looked completely empty, with a single visible line reading:
>
> `Find the flag ... --- ...`
>
> The sequence `... --- ...` is Morse for “SOS”, hinting that there may be hidden (invisible) data embedded in the file.
> **Goal:** Reveal the invisible message and extract the flag.

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description               | 💾 Value |
| ------------------ | ---------------------------- | -------: |
| `file.txt`         | Text file that appears empty |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The file appears visually empty but the visible hint (`... --- ...`) strongly suggests **Morse code** is used.
> A common stego technique is to use **zero-width / invisible Unicode characters** to hide data inside otherwise normal text files.
> Our task is to detect which invisible code points are present, map them to Morse symbols (dot / dash), decode Morse to ASCII, and extract the flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The file shows almost nothing when opened in a normal editor — typical sign of zero-width characters.
* The hint `... --- ...` (SOS) implies the hidden content is Morse, so invisible glyphs likely encode `.` and `-`.

---

### 🔹 Step 2: Identify the Invisible Characters

Use raw viewing or a hex/Unicode inspector to reveal invisible characters. Examples:

```bash
# show raw bytes / characters (Linux)
xxd file.txt
# or view raw text with visible escapes
cat -v file.txt
```

Typical findings (example mapping discovered in this challenge):

* `U+200B` ZERO WIDTH SPACE — used as **dot** `.`
* `U+2000` EN QUAD (or a similar visible-space code) — used as **dash** `-`
* Regular spaces or other separators used to separate Morse letters/words

(Exact codepoints may differ per challenge; always inspect the file to confirm.)

---

### 🔹 Step 3: Reconstruction / Analysis Strategy

If forensic:

> Use `xxd`, `hexdump`, `cat -v`, or a Unicode inspector to list codepoints.
> Map each invisible codepoint to a Morse symbol, normalize consecutive separators, then decode Morse into text.

If automation:

> Implement a short script (PowerShell or Python) that:
>
> 1. Reads file as UTF-8 (preserve zero-width characters).
> 2. Replaces the chosen Unicode points with `.` or `-`.
> 3. Normalizes whitespace into spaces between Morse letters.
> 4. Uses a Morse mapping table to convert to ASCII.

---

### 🔹 Step 4: Implementation (PowerShell example)

```powershell
# decode-hidden.ps1
param([string]$Path)

# Read file preserving Unicode characters
$content = Get-Content -Raw -Encoding UTF8 $Path

# Map the zero-width / invisible code points to dots and dashes
# (adjust the escape sequences if a different codepoint was used)
$content = $content -replace "`u200B", "."    # ZERO WIDTH SPACE -> dot
$content = $content -replace "`u2000", "-"    # EN QUAD (example)   -> dash

# Normalize whitespace so single spaces separate Morse letters
$morse = ($content -replace "\s+", " ").Trim()

# Morse mapping
$map = @{
    ".-"   = "A"; "-..." = "B"; "-.-." = "C"; "-.."  = "D"; "."    = "E";
    "..-." = "F"; "--."  = "G"; "...." = "H"; ".."   = "I"; ".---" = "J";
    "-.-"  = "K"; ".-.." = "L"; "--"   = "M"; "-."   = "N"; "---"  = "O";
    ".--." = "P"; "--.-" = "Q"; ".-."  = "R"; "..."  = "S"; "-"    = "T";
    "..-"  = "U"; "...-" = "V"; ".--"  = "W"; "-..-" = "X"; "-.--" = "Y";
    "--.." = "Z";
    ".----"="1"; "..---"="2"; "...--"="3"; "....-"="4"; "....."="5";
    "-...."="6"; "--..."="7"; "---.."="8"; "----."="9"; "-----"="0";
}

$decoded = ""
foreach ($symbol in $morse.Split(" ")) {
    if ($symbol -eq "") { $decoded += " " ; continue }
    if ($map.ContainsKey($symbol)) {
        $decoded += $map[$symbol]
    } else {
        $decoded += "?"  # unknown symbol (for debugging)
    }
}

Write-Output $decoded
```

Run it:

```powershell
.\decode-hidden.ps1 -Path .\file.txt
```

---

### 🔹 Step 5: Result

Running the script (after confirming codepoints and mapping) produced the decoded plaintext which contains the flag.

---

### 🔹 Step 6: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{1NV1S1BL3_M0R53}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 Invisible Unicode characters are visually non-rendering but still occupy codepoints inside the text stream. By mapping those codepoints to symbolic values (dot/dash) and treating whitespace as separators, we convert an otherwise empty file into a Morse transmission. Decoding that Morse yields the hidden message (the flag).

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language        | 💡 Purpose                                               |
| ------------------------- | -------------------------------------------------------- |
| PowerShell                | Read UTF-8, replace Unicode codepoints, and decode Morse |
| `xxd` / `hexdump` / `cat` | Inspect raw bytes / show invisible chars                 |
| Unicode inspector         | Identify exact codepoints used                           |
| Online Morse decoder      | Quick cross-check of decoded sequences                   |

---

## 📚 Key Learnings

| 🔑 Concept            | 🧠 Takeaway                                      |
| --------------------- | ------------------------------------------------ |
| Zero-width characters | Can carry covert data inside text files          |
| Unicode handling      | Always read files with correct encoding (UTF-8)  |
| Simple encodings work | Morse remains useful as a compact covert channel |
| Scripting automation  | Short scripts quickly reveal hidden payloads     |

---

## 💬 Final Thoughts

> ✨ This challenge is a neat demonstration of how **“empty” does not mean empty**. Zero-width characters are stealthy and effective for hiding short messages.
> When you encounter files that seem blank, always inspect raw bytes and Unicode codepoints — the message may literally be invisible. Great medium-difficulty stego puzzle! 🕵️‍♂️🔍

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** October CTF Series  
📍 **Category:** Steganography / Forensics  
