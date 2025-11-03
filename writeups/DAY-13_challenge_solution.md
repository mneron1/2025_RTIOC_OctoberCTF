# 🧩 **Simple Reverse Engineering**

> 🏷️ *Category:* **Reverse / Pwn / RE (easy)**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Python script analysis`, `ASCII math`, `trivial obfuscation`, `Caesar-style shift`

---

## 📜 Challenge Description

> 💬
> You are given a small Python script that checks a user-supplied string against a `FLAG` array of integers. Reverse the logic to recover the flag.

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                           |                                                                                       💾 Value |
| ------------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------: |
| `script.py`        | Original challenge script (input check)  |                                                                                      See below |
| `FLAG`             | Array used by the script to verify input | `[114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]` |

**`script.py` (original):**

```python
inp = input("Flag: ")

FLAG = [114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]

if len(inp) != len(FLAG):
    print("Wrong!")
    quit()

for i in range(len(FLAG)):
    if ord(inp[i])+12 != FLAG[i]:
        print("Wrong!")
        quit()
    
print("Success!")
```

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The script enforces a fixed input length (19) and checks each character using `ord(inp[i]) + 12 == FLAG[i]`. The check is a per-character arithmetic transform (a Caesar-like shift on bytes). To recover the original flag we invert that operation: subtract `12` from each number in `FLAG` and convert to characters.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The script requires input length equal to `len(FLAG)` → 19 characters.
* Each `FLAG[i]` is compared to `ord(inp[i]) + 12` → a simple additive obfuscation.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

Reverse the arithmetic:

[
\text{ord(flag_char)} = \text{FLAG}[i] - 12
]
[
\text{flag_char} = \text{chr}(\text{FLAG}[i] - 12)
]

---

### 🔹 Step 3: Perform the Extract / Decode

```python
FLAG = [114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]
decoded = ''.join(chr(x - 12) for x in FLAG)
print(decoded)
```

🧾 **Result (run output):**

```
flag{s1mple_c@es@r}
```

---

### 🔹 Step 4: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{s1mple_c@es@r}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

The script used a trivial per-character offset (`+12`) to obfuscate the flag. This is essentially a Caesar-style shift at the byte level. By subtracting `12` from each integer in the `FLAG` array and converting to ASCII characters, we recover the original plaintext flag. This is lightweight obfuscation intended for easy reverse-engineering practice rather than cryptographic security.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language | 💡 Purpose                              |
| ------------------ | --------------------------------------- |
| Python             | Quick decode and verification script    |
| Manual analysis    | Identify `ord()` / `chr()` + arithmetic |
| Text editor        | Inspect the provided script             |

---

## 📚 Key Learnings

| 🔑 Concept              |                                                        🧠 Takeaway |
| ----------------------- | -----------------------------------------------------------------: |
| Code inspection         | Reading code often reveals the whole attack surface or hidden data |
| `ord()` / `chr()` usage |                          Useful for byte/character transformations |
| Simple obfuscation      |           Easy to reverse — don't confuse with secure cryptography |

---

## 💬 Final Thoughts

Nice and tidy challenge — a perfect warm-up for reversing and reading small scripts. It reinforces the habit of reading the check logic first: many CTFs hide flags behind trivial arithmetic or string operations. Quick, educational, and satisfying to solve. 🎉

---
⭐ **Author:** mneron1  
🕒 **Date:** October, 2025  
🏆 **CTF Event:** Cybersecurity CTF Platform  
📍 **Category:** Reverse / Pwn / RE (easy)
---
