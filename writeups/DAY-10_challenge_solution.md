# 🧩 **OCTOBER CTF – DAY 10**

> 🏷️ *Category:* **Reverse Engineering / Web / JavaScript**
> ⚙️ *Difficulty:* **Hard**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `XOR Encoding`, `JS-to-Python Translation`, `Raw Byte Extraction`, `Encoding Quirks`

---

## 📜 Challenge Description

> 💬
> “There’s something unusual hidden in the code of a small website I built.
> See if you can decode my secret message!”
>
> **Goal:** Locate and decode the hidden flag embedded inside the provided website archive (`index.html`).

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                                                    | 💾 Value |
| ------------------ | ----------------------------------------------------------------- | -------: |
| `index.html`       | Contains a custom XOR-encoded JavaScript function and hidden data |        — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The challenge hides an encoded string and a passphrase in a JavaScript comment. The encoder uses a **custom XOR cipher** implemented in JS that behaves slightly differently than a typical XOR loop because of JavaScript’s handling of empty substrings.
>
> To recover the flag, we need to:
>
> 1. Extract the encoded string exactly as stored (byte-for-byte).
> 2. Recreate the XOR logic accurately in Python.
> 3. Decode and clean the output.

Hidden comment inside `index.html`:

```javascript
// super secret txt = `SlTgNcZnFoYelZg"]eYlZ BoGlQ"}`
// super secret pass = 0b101
```

At first glance, the text contains **escaped control characters** (`\x1b`, `\x1d`, `\x1c`), and the pass `0b101` could represent **binary 5** or simply **the character `'5'`**.
The challenge: reproduce JavaScript’s XOR quirk exactly.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* Suspicious JS comments → likely custom encoding
* XOR cipher mentioned explicitly
* Control bytes → need **byte-accurate extraction**
* `pass = 0b101` → may hint at XOR key `5`

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

From the original JavaScript encoder (simplified):

```javascript
for (j = z = 0; z < txt.length; z++) {
    buf += String.fromCharCode(ord[txt.substr(z, 1)] ^ ord[pass.substr(j, 1)]);
    j = (j < pass.length) ? j + 1 : 0;
}
```

⚙️ Observation:
When `pass.length == 1`, `pass.substr(j, 1)` sometimes returns an empty string, which coerces to `0`.
👉 **Only every other character** ends up XORed — a subtle JS behavior that must be replicated in Python.

---

### 🔹 Step 3: Perform the Extract / Decode

To avoid corruption when copying, extract the raw bytes directly from the HTML file:

```python
# extract_secret.py
import re
b = open("index.html", "rb").read()
m = re.search(b'super secret txt\\s*=\\s*`([\\s\\S]*?)`', b)
block_bytes = m.group(1)
print(block_bytes)
```

**Output (escaped form):**

```
SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}
```

🧮 Raw hex bytes:

```
53 6c 54 67 4e 63 5a 6e 46 6f 59 65 1b 6c 5a 67 1d 22 5d 65 59 6c 5a 20 42 6f 47 6c 51 22 1c 7d
```

Now, replicate the JS behavior in Python:

```python
def cheat_decode_final(encoded: str, key_char: str) -> str:
    key = ord(key_char)
    chars = []
    for i, ch in enumerate(encoded):
        if i % 2 == 0:  # XOR only even indices
            chars.append(chr(ord(ch) ^ key))
        else:
            chars.append(ch)
    return ''.join(chars)

def cleaned(s: str) -> str:
    return ''.join(c for c in s if 32 <= ord(c) < 127)

encoded = r"SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}"
encoded = encoded.encode("utf-8").decode("unicode_escape")
decoded = cheat_decode_final(encoded, "5")
print(cleaned(decoded))
```

---

### 🔹 Step 4: Recover the Flag

Running the Python decoder yields:

```
flag{console.log("hello world")}
```

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{console.log("hello world")}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> The XOR cipher in JavaScript used `substr()` with an edge case: when the substring index exceeds the string length, JS returns an empty string (`''`), interpreted as `0`.
>
> This resulted in **only half of the characters** being XORed.
> By reproducing that pattern in Python (XOR only at even indices) and using the ASCII `'5'` as the key, the hidden message is perfectly restored.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Library                 | 💡 Purpose                                    |
| --------------------------------- | --------------------------------------------- |
| 🐍 Python 3                       | Decode the XOR string and replicate JS quirks |
| 🔎 Regex                          | Extract backtick-enclosed encoded data        |
| 🧮 XOR Logic                      | Recreate even-index XOR pattern               |
| 🧾 Hex Viewer (`xxd`, VSCode Hex) | Verify control bytes                          |
| 🌐 JavaScript Source Analysis     | Identify XOR behavior in original code        |

---

## 📚 Key Learnings

| 🔑 Concept                | 🧠 Takeaway                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| **JS vs Python behavior** | Even subtle string handling differences (e.g., `substr` returning `''`) can alter encryption logic |
| **Raw byte accuracy**     | Copying from rendered HTML can corrupt control characters — extract bytes directly                 |
| **XOR debugging**         | Check both numeric (`0b101` → 5) and ASCII interpretations                                         |
| **Index alignment**       | Misaligned XOR operations often produce half-readable output — a clue in itself                    |

---

## 💬 Final Thoughts

> ⚙️ This challenge was a masterclass in **cross-language reverse engineering** — understanding how JavaScript handles strings differently from Python was the key to solving it.
>
> Faithful emulation of quirks like empty substrings made the difference between gibberish and the correct flag.
>
> A single off-by-one substring behavior — and the secret stays hidden. 🕵️‍♂️💡

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** October CTF Series
📍 **Category:** Reverse Engineering / Web / JavaScript
---