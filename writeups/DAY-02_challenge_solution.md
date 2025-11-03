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

| 📁 File / Variable | 🔍 Description       | 💾 Value                                              |
| ------------------ | -------------------- | ----------------------------------------------------- |
| —                  | Target Wikipedia URL | `https://en.wikipedia.org/wiki/Australian_white_ibis` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The flag was **briefly added** to a Wikipedia article and then removed.
> That means it’s no longer visible on the live page.
>
> The task is to inspect **Wikipedia’s revision history** or the **raw page source** to locate a hidden or deleted comment that includes a flag pattern (`flag{}`).
>
> This kind of forensic OSINT challenge typically involves the **MediaWiki Revisions API** and careful inspection of revision diffs.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* A Wikipedia link suggests a **public data investigation** (OSINT).
* The phrase *“someone was trying to hide something”* points to hidden data — likely in:

  * HTML comments (`<!-- -->`)
  * Old or reverted page revisions
  * Transient diffs visible only in edit history

---

### 🔹 Step 2: Access the Page Safely

To avoid rate-limiting, use a proper **User-Agent** header when scraping or querying:

```python
headers = {"User-Agent": "CTFStudent/1.0 (contact@example.com)"}
```

If the standard HTML request is blocked or sanitized, use the **MediaWiki API**:

```
https://en.wikipedia.org/w/api.php?action=parse&page=Australian_white_ibis&prop=text&format=json
```

This returns structured JSON containing the rendered HTML.

---

### 🔹 Step 3: Retrieve the Raw Wikitext

You can access the unrendered source via:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&action=raw
```

This exposes any hidden `<!-- comments -->` or other raw wiki markup.

---

### 🔹 Step 4: Enumerate Revisions with the API

List all recent edits and their metadata:

```
https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Australian_white_ibis&rvprop=ids|timestamp|user|comment|content&rvlimit=50&format=json
```

Each revision includes an `oldid` parameter viewable at:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&oldid=<oldid>
```

---

### 🔹 Step 5: Search for Suspicious Patterns

Scan each revision for a flag-like string.

Example quick check in Python:

```python
import re, requests
url = "https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&action=raw"
data = requests.get(url).text
print(re.findall(r"flag\{.*?\}", data, re.IGNORECASE))
```

If nothing is found in the current version, loop through older `oldid` values to find deleted content.

---

### 🔹 Step 6: Compare Revision Diffs

Use the built-in Wikipedia diff viewer to spot hidden edits:

```
https://en.wikipedia.org/w/index.php?title=Australian_white_ibis&diff=prev&oldid=<revision_id>
```

🧩 **Result:**
A previous edit contained a hidden comment like:

```html
<!-- flag{lL0v5_1b15} -->
```

---

### 🔹 Step 7: Confirm and Extract the Flag

The flag appeared inside a revision’s HTML comment, later removed in the next edit.
Once found, copy it directly from the raw source or diff view.

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

> Every Wikipedia page retains a **complete edit history** — including text removed in later revisions.
>
> The challenge exploited this transparency: by hiding a flag in a transient comment, the flag vanished from the live page but remained visible in archived diffs and API data.
>
> Using the **MediaWiki Revisions API** or direct `oldid` links, we could retrieve and search these historical snapshots to recover it.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language             | 💡 Purpose                                      |
| ------------------------------ | ----------------------------------------------- |
| 🐍 Python (`requests`, `re`)   | Automate API queries and pattern matching       |
| 🌐 MediaWiki API               | Enumerate page revisions and fetch raw wikitext |
| 🔍 Revision Diff Viewer        | Visually locate added / removed lines           |
| 🧮 CyberChef / Base64 decoders | Decode if the flag were obfuscated              |

---

## 📚 Key Learnings

| 🔑 Concept               | 🧠 Takeaway                                         |
| ------------------------ | --------------------------------------------------- |
| **Wikipedia API**        | Allows full access to revision metadata and content |
| **Hidden HTML Comments** | Common trick to conceal flags or messages           |
| **Revision Diffs**       | Show exactly when and how secret data was inserted  |
| **OSINT Persistence**    | Public data often remains archived indefinitely     |

---

## 💬 Final Thoughts

> 🦩 A light-hearted yet powerful reminder that **nothing truly disappears online**.
> Wikipedia’s transparency makes it a goldmine for digital forensics and OSINT exercises.
>
> Great warm-up on revision analysis and hidden-data discovery — the *ibis* certainly left a trail! 🕵️‍♀️

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** October CTF Series  
📍 **Category:** Forensics / OSINT  
---
