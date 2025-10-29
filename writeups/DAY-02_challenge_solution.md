# 🧩 **OCTOBER CTF – DAY 02**

> 🏷️ *Category:* **Forensics / OSINT**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* **Wikipedia Revisions API, Hidden Comments, Web Scraping Etiquette**

---

## 📜 Challenge Description

> 💬
> A colleague mentioned they saw something out of place while researching animals on Wikipedia.
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

| 📁 File / Variable | 🔍 Description              | 💾 Value                                              |
| ------------------ | --------------------------- | ----------------------------------------------------- |
| —                  | Target URL (Wikipedia page) | `https://en.wikipedia.org/wiki/Australian_white_ibis` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ We need to locate a hidden flag that once existed on a Wikipedia article but is **no longer visible on the live version**.
This implies exploring **past revisions**, **HTML comments**, or **raw wikitext** where the flag could have been planted and later removed.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1 – Fetch the Page Properly

Use a polite User-Agent (with contact info) to avoid 403 blocks, or fallback to the MediaWiki `action=parse` API endpoint to fetch rendered HTML.

> Wikimedia blocks unidentified scrapers, so identifying the client is essential.

---

### 🔹 Step 2 – Pull Raw Wikitext

Request the page via `action=raw` to obtain its source (including hidden comments `<!-- … -->`).

---

### 🔹 Step 3 – Query Recent Revisions

Use the API endpoint:

```
?action=query&prop=revisions&rvprop=content&titles=Australian_white_ibis
```

to retrieve the most recent *N* page versions and compare them for inserted or removed flags.

---

### 🔹 Step 4 – Scan for Flag Patterns

Search each revision’s content for:

* `flag{...}` patterns
* Encoded variants (Base64, hex, URL-encoded strings, etc.)
* Hidden HTML comments

---

### 🔹 Step 5 – Attempt Decoding (if needed)

Run automatic decoders (Base64, hex, URL, ROT13, XOR, reversed text) and search decoded results for flag syntax.

---

### 🔹 Step 6 – Locate the Exact Revision

Once a match appears, print its:

* `oldid` value
* Timestamp and user
* Direct revision URL `?oldid=<ID>`
* Diff URL `?diff=prev&oldid=<ID>`

---

### 🔹 Step 7 – Confirm the Finding

The revision diff visibly shows the flag being inserted then removed — a classic CTF indicator of a temporary hide.

---

## 🎯 Recovered Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{lL0v5_1b15}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 Wikipedia keeps **every revision** of an article accessible through the MediaWiki API.
Even if someone removes content immediately after posting it, the data remains in the revision history.
By programmatically searching through these revisions and hidden comments, we can uncover transient flags.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Language            | 💡 Purpose                             |
| ----------------------------- | -------------------------------------- |
| 🐍 Python (requests + regex)  | API queries and flag scanning          |
| 🌐 MediaWiki API              | Retrieve HTML, wikitext, and revisions |
| 🧮 CyberChef / Base64 decoder | Optional manual decoding check         |

---

## 📚 Key Learnings

| 🔑 Concept               | 🧠 Takeaway                                           |
| ------------------------ | ----------------------------------------------------- |
| Wikipedia API usage      | Provides official access to page history and wikitext |
| Hidden HTML comments     | Common place for CTF flags                            |
| Revision diff inspection | Lets you find content added and removed quickly       |

---

## 💬 Final Thoughts

> 🦩 This challenge reminds us that “deleted” does not mean “gone.”
> Exploring revision history is a powerful OSINT technique in CTFs and incident response alike.
> The ibis may have flown away — but the flag was still in its footprints 🕵️‍♀️💪

---
⭐ Author: mneron1
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Forensics / OSINT
---
