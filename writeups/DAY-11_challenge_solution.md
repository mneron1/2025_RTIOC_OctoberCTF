# 🧩 **OCTOBER CTF – DAY 11**

> 🏷️ *Category:* **Forensics / Git / Incident Response**
> ⚙️ *Difficulty:* **Easy**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Git history`, `deleted file recovery`, `UTF-16LE encoding`, `incident response`

---

## 📜 Challenge Description

> 💬
> A developer accidentally committed a sensitive configuration file to a shared Git repository, then deleted it and committed the deletion.
>
> The challenge is to determine whether the sensitive information can still be recovered from the repository history.
>
> **Goal:** Recover any secret data left in the repository’s history.

---

## 📦 Provided Files / Data

| 📁 File / Variable | 🔍 Description                               |                                         💾 Value |
| ------------------ | -------------------------------------------- | -----------------------------------------------: |
| `repo.zip`         | Repository archive / Git repo                | Contains a deleted config file in commit history |
| `config.txt`       | Deleted configuration file (to be recovered) |                                                — |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> Deleting a file in Git only removes it from the **current commit**, not from the **repository history**.
>
> The goal is to **find the commit where the file existed**, extract that version, and decode it.
>
> The challenge also mentions encoding — the deleted file is encoded in **UTF-16LE**, so viewing it as UTF-8 will produce gibberish. We’ll need to convert it to the correct text encoding to reveal the secret data.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The repository likely contains a deleted file in its history.
* The CTF description hints at **Git forensics** — recovering a deleted blob.
* Mention of “sensitive data” and “UTF-16LE” points to an **encoded text file**.

---

### 🔹 Step 2: Reconstruct or Analyze the Key Data

We start by investigating commit history for deleted files:

```bash
git log --oneline --graph --decorate --all
git log --diff-filter=D --summary --all
```

Look for commits with messages like:

```
Removed config file - oops!
```

Once identified, note its commit hash (e.g., `56c6dac`).

Then, extract the deleted file from the **parent commit**:

```bash
git show 56c6dac^:config.txt > recovered-config.raw
```

This command outputs the deleted file as it existed before the deletion.

---

### 🔹 Step 3: Perform the Extract / Decode

The recovered file appears garbled when opened directly — that’s because it’s encoded in **UTF-16LE** (common for Windows text files).

To fix the encoding:

#### 🧩 Option 1 — Use `iconv`:

```bash
iconv -f UTF-16LE -t UTF-8 recovered-config.raw > recovered-config.txt
```

#### 🧩 Option 2 — Use Python:

```python
raw = open('recovered-config.raw', 'rb').read()
print(raw.decode('utf-16-le'))
```

🧾 **Result:**
You now have a readable configuration file.

---

### 🔹 Step 4: Recover the Flag

Open the converted file (`recovered-config.txt`) — you’ll see something like:

```
username: admin_user
password: S3cur3P4ss2024!
```

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
flag{S3cur3P4ss2024!}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> Git stores all versions of every file as *blobs* inside its object database.
>
> When a file is deleted, Git simply updates the latest tree to exclude it — but previous commits (and their blobs) still contain the old file.
>
> By checking the parent commit of the deletion and extracting the blob, you can fully recover the file as it existed before deletion.
>
> The additional twist in this challenge was the **UTF-16LE encoding**, requiring proper decoding to reveal the readable plaintext.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Command                      | 💡 Purpose                                                        |
| -------------------------------------- | ----------------------------------------------------------------- |
| `git log --diff-filter=D`              | Identify deleted files across history                             |
| `git show <commit>^:<path>`            | Extract deleted file from previous commit                         |
| `iconv` / `Python decode('utf-16-le')` | Fix encoding to readable UTF-8 text                               |
| `git fsck --lost-found`                | (Optional) Locate dangling blobs if commit references are missing |

---

## 📚 Key Learnings

| 🔑 Concept             | 🧠 Takeaway                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| **Git history**        | Deleting a file doesn’t remove it from history — it can be recovered unless the repo is cleaned. |
| **Encoding awareness** | Binary or encoded files must be interpreted correctly (UTF-16LE → UTF-8).                        |
| **Incident response**  | If secrets are leaked via commits, rotate credentials and clean history with `git filter-repo`.  |

---

## 💬 Final Thoughts

> 🔐 A classic “oops — I pushed a secret” scenario!
>
> This challenge reinforces how Git retains full project history — and how easy it is to recover sensitive data unless the history is rewritten.
>
> In real-world cases: **recover, rotate, then scrub**. Implement secret-scanning tools (e.g., TruffleHog, Gitleaks) in your CI/CD to prevent future incidents. 🧑‍💻

---
⭐ **Author:** mneron1  
🕒 **Date:** October 2025  
🏆 **CTF Event:** October CTF Series  
📍 **Category:** Forensics / Git / Incident Response
---