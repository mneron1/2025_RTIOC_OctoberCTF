🧩 OCTOBER CTF – DAY 11

🏷️ *Category:* **Forensics / Git / Incident Response**
⚙️ *Difficulty:* **Easy**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Git history, resurrecting deleted files, file encoding (UTF-16LE)**

📜 Challenge Description

💬
A developer accidentally committed a sensitive configuration file to a shared Git repository, then deleted it and committed the deletion. The challenge: determine whether the sensitive info can still be recovered from the repository history.

Goal: Recover any secret data left in the repo history.

📦 Provided Files / Data
📁 File / Variable	🔍 Description
Repository archive / Git repo	Contains a deleted config file referenced in commit history. 

DAY-11_challenge_solution

🧠 Understanding the Problem

Deleting a file in Git removes it from the current tree but does not erase it from history. If the repo contains the commit where the file existed, you can show or extract that version. The catch in this challenge: the recovered file contains Windows-style UTF-16LE encoding (producing visible gibberish if viewed as UTF-8), so the recovered bytes must be reinterpreted to reveal meaningful text.

🧩 Step-by-Step Solution
🔹 Step 1 — Inspect repo history for deleted files

Find commits that deleted files and locate the relevant commit:

git log --oneline --graph --decorate --all
git log --diff-filter=D --summary --all


Look for a commit message like Removed config file - oops! and note its commit hash (example: 56c6dac).

🔹 Step 2 — Extract the file from the parent commit

Recover the file as it existed before deletion:

git show 56c6dac^:config.txt > recovered-config.raw


This writes the file’s raw blob to recovered-config.raw.

🔹 Step 3 — Detect and fix encoding

Opening recovered-config.raw directly may display odd spaced characters (e.g., u s e r n a m e ...). That’s a sign of UTF-16LE encoding. Convert to UTF-8:

Using iconv:

iconv -f UTF-16LE -t UTF-8 recovered-config.raw > recovered-config.txt


Or with Python:

python3 - <<'PY'
raw = open('recovered-config.raw','rb').read()
print(raw.decode('utf-16-le'))
PY

🔹 Step 4 — Read the recovered file

Open recovered-config.txt with your text editor. The file contents reveal credentials (example):

username: admin_user
password: S3cur3P4ss2024!

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
S3cur3P4ss2024!

</details>
📘 Explanation — Why It Works

Git stores the full project history as objects — commits point to trees and blobs. Deleting a file only updates the current tree; the old blob still exists in history until garbage-collected or explicitly removed.

Many Windows-generated config files are encoded in UTF-16LE. If you view those bytes as UTF-8, the output looks like spaced or garbled characters. Converting with the correct encoding recovers the original, human-readable text.

The approach is purely forensic: locate the commit → extract the file blob → convert encoding → read secret.

🧰 Tools & Commands Used
🧩 Tool / Command	💡 Purpose
git log --diff-filter=D	Find deleted files across history
git show <commit>^:<path>	Extract file as it was in parent commit
iconv or Python decode('utf-16-le')	Fix UTF-16LE → UTF-8 encoding
git fsck --lost-found	(Optional) locate dangling blobs
📚 Key Learnings
🔑 Concept	🧠 Takeaway
Git history	Deleting a file doesn't remove it from history
Encoding matters	Correctly interpreting file bytes (UTF-16LE vs UTF-8) is essential
Incident response	If secrets are committed, rotate them and clean history (filter-repo)
💬 Final Thoughts

🔐 This was a classic “oops — I pushed a secret” exercise: the secret wasn’t lost, it was just moved back in time. In real environments, recover, rotate, and then scrub history if necessary (with tools like git filter-repo) — and add secret scanning to CI to prevent recurrence.

---
⭐ Author: mneron1  
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Forensics / Git / IR
---