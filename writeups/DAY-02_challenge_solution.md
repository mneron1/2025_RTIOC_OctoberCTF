# 🧩 **OCTOBER CTF – DAY 02**

> 🏷️ *Category:* **Forensics / OSINT**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Wikipedia Revisions API`, `Hidden Comments`, `Web Scraping Etiquette`

---

## 📜 Challenge Description

> 💬
> A colleague mentioned they saw something strange while researching animals on Wikipedia.
>
> They were looking up information about the *Australian white ibis* and said:
>
> “I swear someone was messing with that page earlier. You might want to check it out… it looked like someone was trying to hide something.”
>
> 🔗 [https://en.wikipedia.org/wiki/Australian_white_ibis](https://en.wikipedia.org/wiki/Australian_white_ibis)
>
> **Goal:** Find the secret flag!

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description       |                                              💾 Value |
| ------------------ | -------------------- | ----------------------------------------------------: |
| —                  | Target Wikipedia URL | `https://en.wikipedia.org/wiki/Australian_white_ibis` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The flag was **briefly added** to a Wikipedia article, then removed — meaning it no longer appears on the live page.
>
> We must explore **Wikipedia’s revision history** or **raw wikitext** to find deleted or commented-out text that matches the `flag{}` pattern.

This kind of forensic OSINT task involves examining how pages change over time, especially through the **MediaWiki Revisions API**.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The challenge involves a public Wikipedia page → indicates an **OSINT / API investigation**.
* The phrase *“looked like someone was trying to hide something”* hints at hidden data in:

  * HTML comments (`<!-- -->`)
  * Past revisions of the article
  * Temporary edits or diffs

---

### 🔹 Step 2: Access the Page Safely

Use a proper **User-Agent** when fetching the content programmatically to avoid `403 Forbidden` responses:

```python
headers = {"User-Agent": "CTFStudent/1.0 (contact@example.com)"}
```

If direct access fails, use the **MediaWiki Action API** endpoint:

```
https://en.wikipedia.org/w/api.php?action=parse&page=Australian_white_ibis&prop=text&format=json
```

---

### 🔹 Step 3: Pull the Raw Wikitext

Request the page source with:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&action=raw
```

This gives the **unrendered text**, including hidden `<!-- comments -->` or deleted notes.

---

### 🔹 Step 4: Explore Revisions via API

Use the Wikipedia API to list and retrieve old page versions:

```
https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Australian_white_ibis&rvprop=ids|timestamp|user|comment|content&rvlimit=50&format=json
```

Each **revision** contains an `oldid`, which can be viewed at:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&oldid=<oldid>
```

---

### 🔹 Step 5: Search for Flag Patterns

For each revision’s text, search for:

* `flag{`
* `FLAG{`
* `base64`, `urlencoded`, or `rot13` variants

Example quick scan in Python:

```python
import re, requests

url = "https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&action=raw"
content = requests.get(url).text
print(re.findall(r"flag\{.*?\}", content, re.IGNORECASE))
```

---

### 🔹 Step 6: Compare Old vs New Revisions

By comparing diffs:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&diff=prev&oldid=<revision_id>
```

you can visually confirm when a line containing a flag was added and removed.

🧩 **Result:**
A specific revision contained a hidden comment like:

```html
<!-- flag{lL0v5_1b15} -->
```

---

### 🔹 Step 7: Confirm and Retrieve the Flag

The flag was located inside a revision comment, briefly added and later removed.

---

### 🔹 Step 8: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{lL0v5_1b15}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> Wikipedia keeps a **full revision history** of every article, even for deleted or reverted edits.
> Searching through old revisions or hidden HTML comments often reveals transient data like test edits, vandalism, or — in CTFs — hidden flags.
>
> Using the **MediaWiki Revisions API**, you can systematically fetch and scan previous versions for the hidden content.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language                 | 💡 Purpose                              |
| ---------------------------------- | --------------------------------------- |
| 🐍 **Python (requests + regex)**   | Query and scan MediaWiki data           |
| 🌐 **MediaWiki API**               | Retrieve page revisions and raw content |
| 🧮 **CyberChef / Base64 decoders** | Decode any obfuscated strings           |
| 🔎 **Revision diffs**              | Visually confirm hidden insertions      |

---

## 📚 Key Learnings

| 🔑 Concept            | 🧠 Takeaway                                     |
| --------------------- | ----------------------------------------------- |
| **Wikipedia API**     | Enables structured access to full edit history  |
| **Hidden comments**   | Great place to hide CTF clues or flags          |
| **Revision diffs**    | Quick way to identify added/removed secret data |
| **OSINT methodology** | Sometimes “deleted” just means “archived”       |

---

## 💬 Final Thoughts

> 🦩 This challenge is a perfect reminder that **public data is never truly gone**.
> Even when content is edited out, revision logs preserve everything.
>
> A solid lesson in **open-source forensics** — and a fun hunt through the trails left by an Australian ibis! 🕵️‍♀️

---
⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Forensics / OSINT
---