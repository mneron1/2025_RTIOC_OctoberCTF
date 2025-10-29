# 🧩 **RSA Decryption — Pre-filled CTF Writeup**

> 🏷️ **Category:** Crypto
> ⚙️ **Difficulty:** Easy / Introductory
> 🕵️ **Source:** RTIOC Cyber Awareness month challenge
> 🧠 **Concepts:** RSA, modular inverse, Euler’s totient, modular exponentiation, CRT

---

## 📜 Challenge Description

> We are given an RSA modulus `N`, the two prime factors `p` and `q`, the public exponent `e`, and a ciphertext `c`.
> Task: Recover the plaintext flag.

---

## 📦 Provided Data

| Variable | Value                                                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `N`      | `3843320600049685784489912804979627239090690900770120939549645532352660177607125376287296048082264304090084905042982899278667480441629635344651258767358679` |
| `p`      | `61466741848947734604326747104129487556395996097776212069675986601934660255783`                                                                              |
| `q`      | `62526831330909084217232291749586253220920640490081383658843155720941305474513`                                                                              |
| `e`      | `65537`                                                                                                                                                      |
| `c`      | `476651893614742798560907369844073362193050056210659969134933172506446413367009602233331842585206003521478657411290317244308366109218480605103136284255176`  |

---

## 🚀 Step-by-Step Solution

### 1️⃣ Verify inputs

Confirm the primes multiply to the modulus:

```text
check: p * q == N  -> True
```

If that fails, inputs are inconsistent — stop and re-check.

---

### 2️⃣ Compute Euler’s totient ϕ(N)

Because `N = p * q` and `p, q` are primes:

[
\varphi(N) = (p-1) \times (q-1)
]

This number is required to compute the modular inverse of `e`.

---

### 3️⃣ Compute the private exponent `d`

Find `d` such that:

[
d \equiv e^{-1} \pmod{\varphi(N)}
]

This is the modular inverse of `e` modulo `ϕ(N)`. In Python:

```python
d = pow(e, -1, phi)
```

This `d` is the private key exponent.

---

### 4️⃣ Decrypt the ciphertext

Compute:

[
m \equiv c^d \pmod{N}
]

This returns an integer `m` representing the plaintext bytes. Convert it to hex/bytes and decode UTF-8.

---

### 5️⃣ Final plaintext / flag

<details>
<summary>🎯 Click to reveal the flag</summary>

```
flag{crypto_is_fun_when_you_break_it}
```

</details>

---

## ⚙️ Full Working Script (copy/paste)

```python
# Pre-filled script used for this challenge
N = 3843320600049685784489912804979627239090690900770120939549645532352660177607125376287296048082264304090084905042982899278667480441629635344651258767358679
p = 61466741848947734604326747104129487556395996097776212069675986601934660255783
q = 62526831330909084217232291749586253220920640490081383658843155720941305474513
e = 65537
c = 476651893614742798560907369844073362193050056210659969134933172506446413367009602233331842585206003521478657411290317244308366109218480605103136284255176

# 1) sanity check
assert p * q == N

# 2) phi(N)
phi = (p - 1) * (q - 1)

# 3) private exponent
d = pow(e, -1, phi)

# 4) decrypt
m = pow(c, d, N)

# 5) convert to bytes and decode
m_hex = hex(m)[2:]
if len(m_hex) % 2 == 1:
    m_hex = "0" + m_hex
plaintext = bytes.fromhex(m_hex).decode('utf-8')
print(plaintext)
```

---

## 🔎 Optional: Faster Decryption (CRT)

For performance (not necessary here), one can use the Chinese Remainder Theorem:

```python
# Precomputed values
dP = d % (p - 1)
dQ = d % (q - 1)
qInv = pow(q, -1, p)

# Local decryptions
m1 = pow(c % p, dP, p)
m2 = pow(c % q, dQ, q)

# Recombine
h = (qInv * (m1 - m2)) % p
m_crt = m2 + h * q
# m_crt should equal m computed earlier
```

CRT reduces exponent sizes and speeds up modular exponentiation ~4x.

---

## 🧠 Key Learnings

* 🔐 **RSA security relies on p & q being secret.** If `p` and `q` are known, anyone can compute `d` and decrypt.
* 🧮 **Modular inverse** (`d = e⁻¹ mod ϕ(N)`) is the critical step for retrieving the private key.
* ⚠️ **Don’t encrypt raw text with RSA in real systems.** Use proper padding (OAEP) and hybrid encryption (RSA + symmetric cipher).
* ⚡ **CRT** is commonly used in real-world implementations to speed decryption.

---

## 🧰 Tools & References

* Python (built-in big integers and `pow` with three args)
* Optional: OpenSSL, CyberChef for quick conversions
* References: standard RSA cryptography concepts (Euler’s theorem, modular inverse, CRT)

---

## 💬 Final Thoughts

This challenge is a classic: once `p` and `q` are exposed, RSA is trivial to invert. It’s a great exercise to reinforce the mathematical underpinnings of RSA (ϕ, modular inverse, modular exponentiation) and to practice turning integer results into human-readable data.

---

### 🧾 Footer (ready to paste into GitHub/CTFd)

```markdown
---
⭐ **Author:** mneron1  
🕒 **Date:** 2025-10-27  
🏆 **CTF Event:** RTIOC Cyber Awareness month challenge  
📍 **Category:** Crypto
---
```

---

Want me to export this as a polished Markdown file ready to drop into a repo (with a nice header image and README-style badges)?
