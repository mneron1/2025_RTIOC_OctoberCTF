# 🧩 **OCTOBER CTF - DAY 12**

> 🏷️ *Category:* **Crypto**
> ⚙️ *Difficulty:* **Easy / Introductory**
> 🕵️ *Author:* **RTIOC Cyber Awareness Month Challenge**
> 🧠 *Concepts:* `RSA`, `modular inverse`, `Euler’s totient`, `modular exponentiation`, `Chinese Remainder Theorem (CRT)`

---

## 📜 Challenge Description

> 💬
> We are given an RSA modulus `N`, its two prime factors `p` and `q`, the public exponent `e`, and a ciphertext `c`.
>
> The goal is to **recover the plaintext flag** by reconstructing the RSA private key and decrypting the ciphertext.

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description              |                                                                                                                                                     💾 Value |
| ------------------ | --------------------------- | -----------------------------------------------------------------------------------------------------------------------------------------------------------: |
| `N`                | RSA modulus                 | `3843320600049685784489912804979627239090690900770120939549645532352660177607125376287296048082264304090084905042982899278667480441629635344651258767358679` |
| `p`                | Prime factor #1             |                                                                              `61466741848947734604326747104129487556395996097776212069675986601934660255783` |
| `q`                | Prime factor #2             |                                                                              `62526831330909084217232291749586253220920640490081383658843155720941305474513` |
| `e`                | Public exponent             |                                                                                                                                                      `65537` |
| `c`                | Ciphertext (encrypted flag) |  `476651893614742798560907369844073362193050056210659969134933172506446413367009602233331842585206003521478657411290317244308366109218480605103136284255176` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> This is a **textbook RSA decryption challenge**.
>
> Given `p` and `q`, we can compute:
>
> * Euler’s totient function `ϕ(N) = (p - 1) * (q - 1)`
> * The private exponent `d = e⁻¹ mod ϕ(N)`
>
> Once we have `d`, we can decrypt the ciphertext using modular exponentiation:
> [
> m = c^d \mod N
> ]
>
> Finally, the decrypted integer can be converted from hex → bytes → UTF-8 to reveal the plaintext flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* Standard RSA data provided (`N`, `p`, `q`, `e`, `c`)
* Obvious path: compute `ϕ(N)`, find private key `d`, then decrypt.
* Since both primes are known, this is a **fully solvable** RSA system.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

We compute the totient and private exponent:

[
ϕ(N) = (p - 1)(q - 1)
]

[
d = e^{-1} \bmod ϕ(N)
]

In Python:

```python
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
```

---

### 🔹 Step 3: Perform the Decrypt / Extract

```python
m = pow(c, d, N)  # modular exponentiation
```

Convert to bytes:

```python
m_hex = hex(m)[2:]
if len(m_hex) % 2:
    m_hex = "0" + m_hex
plaintext = bytes.fromhex(m_hex).decode()
print(plaintext)
```

🧾 **Result:**
We obtain a readable string — the flag.

---

### 🔹 Step 4: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{crypto_is_fun_when_you_break_it}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> RSA encryption is based on modular exponentiation using a public exponent `e` and modulus `N`.
> Decryption reverses this process using the private exponent `d`, derived from the modular inverse of `e` modulo `ϕ(N)`.
>
> Once `p` and `q` are known, RSA is no longer secure — because the entire private key can be reconstructed.

Mathematically:
[
m = c^d \mod N
]
[
d = e^{-1} \mod (p-1)(q-1)
]

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language      | 💡 Purpose                               |
| ----------------------- | ---------------------------------------- |
| 🐍 Python               | Compute `ϕ(N)`, `d`, and decrypt message |
| 🧮 Modular arithmetic   | Reconstruct private key                  |
| 🧾 Hex → UTF-8 decoding | Convert integer to readable text         |

---

## 📚 Key Learnings

| 🔑 Concept        |                                               🧠 Takeaway |
| ----------------- | --------------------------------------------------------: |
| RSA factorization |   If `p` and `q` are exposed, encryption breaks instantly |
| Modular inverse   | The core of RSA private key recovery (`d = e⁻¹ mod ϕ(N)`) |
| Big integer math  | Python handles huge numbers natively — perfect for crypto |
| CRT optimization  |        Used in real systems to make decryption ~4x faster |

---

## 💬 Final Thoughts

> ✨ This challenge perfectly illustrates the **fragility of RSA** when prime secrecy is lost.
> Once you know `p` and `q`, the rest is just arithmetic.
>
> Great introductory exercise for understanding **RSA internals**, modular arithmetic, and practical key reconstruction. 🧮🔐

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** RTIOC Cyber Awareness Month Challenge  
📍 **Category:** Crypto
---