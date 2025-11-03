# 🧩 **OCTOBER CTF – DAY 09**

> 🏷️ *Category:* **Cryptography / Password Cracking**
> ⚙️ *Difficulty:* **Medium–Hard**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `NTLM`, `MD4`, `Hash Cracking`, `John the Ripper`, `Hashcat`

---

## 📜 Challenge Description

> 💬
> “We recovered five suspicious hashes from an old Windows SAM file.
> Can you reveal the passwords and build the final flag?”
>
> **Goal:** Crack all NTLM hashes and construct the flag in this format:
>
> `flag{password1_password2_password3_password4_password5}`

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                 |  💾 Value |
| ------------------ | ------------------------------ | --------: |
| `hashes.txt`       | List of 5 NTLM hashes to crack | See below |

```
0ea0e4bb502bd4acaf6997d7c26b54d1  
326f5f6c590b925012b8930758b42148  
1337bdd3c9fa21e8d72849e1618d2535  
9ad1180ec59ccbca760e6de738fb4d70  
6b56ad7d13656b993ded0758f58794f6
```

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The provided hashes are **32-character hexadecimal strings** typical of NTLM format.
> NTLM hashes are **unsalted MD4 digests** of the password encoded in **UTF-16LE**.
>
> Because there’s no salt, identical passwords always produce identical hashes — making them highly vulnerable to dictionary or rainbow table attacks using tools like **John the Ripper** or **Hashcat**.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* Each hash is **32 hex characters long (128 bits)** → consistent with **NTLM**.
* Format: `MD4(UTF-16LE(password))` → unsalted.
* Best approach: use a **wordlist-based** cracking attack.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

We know NTLM hashing logic:
[
\text{hash} = \text{MD4}(\text{UTF-16LE(password)})
]

Since NTLM has no salt, one password list can crack many accounts efficiently.

---

### 🔹 Step 3: Perform the Exploit / Decrypt / Extract

#### 🪓 Option 1 — Using **John the Ripper**

```bash
john --format=NT hashes.txt --wordlist=rockyou.txt
```

#### ⚡ Option 2 — Using **Hashcat**

```bash
hashcat -m 1000 hashes.txt rockyou.txt
```

Where:

* `-m 1000` = NTLM mode
* `rockyou.txt` = common password wordlist (can be found on Kali or GitHub)

#### 🌐 Option 3 — Quick Online Lookup

If no GPU access, try:

* [CrackStation.net](https://crackstation.net)
* [Hashes.com](https://hashes.com/en/decrypt/hash)

These databases often already contain common NTLM hashes.

---

### 🔹 Step 4: Recover the Flag

Once all five hashes are cracked, concatenate their plaintexts in order using underscores (`_`):

```
flag{password1_password2_password3_password4_password5}
```

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{password1_password2_password3_password4_password5}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> NTLM uses a **weak, unsalted hash function (MD4)** over UTF-16LE encoded passwords.
> This design makes it trivial to reverse using dictionary or brute-force attacks.
> Because there’s no randomization (salt), the same password always yields the same hash — allowing rapid lookups through precomputed lists or GPU attacks.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language               | 💡 Purpose                           |
| -------------------------------- | ------------------------------------ |
| 🔐 **John the Ripper**           | CLI password cracking with NT format |
| ⚡ **Hashcat**                    | GPU-accelerated NTLM cracking        |
| 🌐 **CrackStation / Hashes.com** | Online lookup for known hashes       |
| 🧾 **RockYou.txt**               | Common password dictionary           |
| 💻 **MD4 (UTF-16LE)**            | NTLM hash generation scheme          |

---

## 📚 Key Learnings

| 🔑 Concept             | 🧠 Takeaway                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| **NTLM hashes**        | Unsalted MD4 digests — extremely weak by modern standards               |
| **UTF-16LE encoding**  | NTLM encodes passwords before hashing                                   |
| **Dictionary attacks** | Efficient for common passwords; precomputed wordlists make them trivial |
| **Security hygiene**   | Replace legacy NTLM authentication; enforce password complexity         |

---

## 💬 Final Thoughts

> 💻 Even decades-old authentication mechanisms like **NTLM** are still found in modern networks.
>
> This challenge highlights the danger of relying on outdated hashing schemes — **one weak password** or **legacy protocol** can compromise an entire system.
>
> Regular audits and migration away from NTLM remain critical in any secure infrastructure.

---

⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Cryptography / Password Cracking

---
