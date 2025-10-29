# 🧩 Simple Reverse Engineering

> 🏷️ **Category:** Reverse / Pwn / RE (easy)
> ⚙️ **Difficulty:** Easy
> 🕵️ **Author:** RTIOC Cyber Awareness Month CTF
> 🧠 **Concepts:** Python script analysis, ASCII math, trivial obfuscation

---

## 📜 Challenge Description

You are given a small Python script that checks a user-supplied string against a `FLAG` array of integers. Reverse the logic to recover the flag.

**Provided script (original):**

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

The script verifies a user input by:

1. Enforcing the input length equals the `FLAG` array length (19).
2. For each character `inp[i]`, it checks `ord(inp[i]) + 12 == FLAG[i]`.

To get the original flag text we reverse the per-character operation:

```
ord(flag_char) = FLAG[i] - 12
flag_char = chr(FLAG[i] - 12)
```

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Observe flag length

`FLAG` has 19 entries → input must be **19 characters** long.

### 🔹 Step 2: Reverse transformation

For each number in `FLAG`, subtract `12` and convert to a character.

### 🔹 Step 3: Decode with Python (quick)

You can decode directly with a one-liner:

```python
FLAG = [114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]
flag = ''.join(chr(x - 12) for x in FLAG)
print(flag)
```

**Run output:**

```
flag{s1mple_c@es@r}
```

---

### 🔹 Alternative: Modify the original script to reveal the flag

If you want the original script to print the flag instead of requiring input, replace its logic with the decode and print:

```python
FLAG = [114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]
decoded = ''.join(chr(x - 12) for x in FLAG)
print("Decoded flag:", decoded)
```

---

## 🎯 Click to Reveal the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{s1mple_c@es@r}
```

</details>

---

## 📘 Explanation — *Why It Works*

The check `ord(inp[i]) + 12 == FLAG[i]` is a simple Caesar-style byte shift applied to each character. By subtracting `12` from each number in the provided integer list, we reverse the shift and recover the original ASCII characters. This is trivial obfuscation — not real cryptography — intended to test basic reversing/debugging skills.

---

## 🧰 Tools & Techniques Used

| Tool / Language | Purpose                           |
| --------------- | --------------------------------- |
| Python          | Decode `FLAG` array quickly       |
| Manual math     | Reason about `ord()` / `chr()`    |
| Static analysis | Read and reverse the script logic |

---

## 📚 Key Learnings

* Simple obfuscation is often reversible by inspecting the code.
* `ord()` and `chr()` are essential for ASCII transformations.
* Look for trivial arithmetic-based checks when reversing small scripts.

---

## 💬 Final Thoughts

Nice and tidy challenge — a good warm-up that reinforces reading Python logic and reversing small arithmetic transformations. The flag was recovered by a straightforward reversal of a `+12` offset. Short, sweet, and satisfying. 🎉

---

## 🧾 Reusable Footer

```markdown
---
⭐ **Author:** YourTeam  
🕒 **Date:** Oct 2025  
🏆 **CTF Event:** Day 13  
📍 **Category:** Reverse
---
```

---

If you want, I can also:

* Export this markdown to a file for you.
* Produce a short slide or one-pager for team distribution.
* Create a small validator script that checks the flag automatically. Which would you like next?
