# 🧩 **Robots**

> 🏷️ *Category:* **Web**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **cybersecurity.ctfd.io**
> 🧠 *Concepts:* `robots.txt`, web discovery, enumeration

---

## 📜 Challenge Description

> 💬
> **Can you confirm that you are a robot? Only robots should be able to find this flag!**
> (Hosted on the CTF platform: `https://cybersecurity.ctfd.io/challenges#robots-134`)

---

## 📦 Provided Files / Data

| 📁 File / Variable     | 🔍 Description             |                                                💾 Value |
| ---------------------- | -------------------------- | ------------------------------------------------------: |
| `/robots.txt`          | Web crawler directives     |                                               see below |
| `robots.txt` (content) | What the site tells robots | `User-agent: *\nDisallow: /admin\nflag{h3110_Mr_R0b07}` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ The challenge hints that *robots* should be able to find the flag — a clear pointer toward the standard web crawler file `/robots.txt`. That file often contains paths site owners don't want crawlers to index (e.g., `/admin`) — and in CTF puzzles it’s frequently abused to hide flags.

Goal: inspect `/robots.txt`, follow whatever it reveals, and extract the flag.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The prompt explicitly references **robots** → check `/robots.txt`.
* `/robots.txt` is public and commonly used in web discovery challenges.

---

### 🔹 Step 2: Fetch `/robots.txt`

You can inspect it in a browser or via CLI:

```bash
# CLI example
curl -sS https://cybersecurity.ctfd.io/robots.txt
```

**Observed content**:

```
User-agent: *
Disallow: /admin
flag{h3110_Mr_R0b07}
```

---

### 🔹 Step 3: Extract the Flag

The flag is present directly in the `robots.txt` file (a common CTF trick). Copy the `flag{...}` string and submit it to the challenge.

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{h3110_Mr_R0b07}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

`robots.txt` is a publicly accessible file intended to instruct web crawlers which paths to avoid. Because it is public and often overlooked, CTF authors hide flags there to test players’ ability to perform simple web enumeration. This challenge simply rewarded checking the obvious location hinted by the prompt.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language | 💡 Purpose                  |
| ------------------ | --------------------------- |
| Browser (any)      | View `/robots.txt` directly |
| `curl` / `wget`    | Quick fetch from CLI        |
| Text editor        | Inspect file content        |

---

## 📚 Key Learnings

| 🔑 Concept           |                                                              🧠 Takeaway |
| -------------------- | -----------------------------------------------------------------------: |
| `robots.txt`         |                     Public file; useful first target for web enumeration |
| Web discovery basics | Always check common files: `robots.txt`, `sitemap.xml`, `.git/`, `/.env` |
| CTF hint-reading     |              Prompts often point to the exact technique or file to check |

---

## 💬 Final Thoughts

> ✨ Simple and elegant web discovery challenge. A good reminder: **check the basics first** — many flags live in plain sight if you think like a crawler. Another flag captured! 🏴‍☠️💪

---
⭐ **Author:** YourTeamName  
🕒 **Date:** October, 2025  
🏆 **CTF Event:** OCTOBER CTF (example)  
📍 **Category:** Web
---
