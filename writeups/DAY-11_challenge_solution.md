Sure thing 😎 — here’s a more **fun, dynamic, markdown-style writeup** with emojis, headers, and a slightly more casual CTF tone while keeping it 100% accurate technically.

---

# 🕵️‍♂️ CTF — Day 11: *Git Happens*

---

## 💡 The Challenge

A developer at our company accidentally committed sensitive information to a shared Git repository. Realizing their mistake, they quickly delete the file and committed the changes, thinking the sensitive data was gone forever.

Your mission here is to investigate whether any sensitive information can still be recovered from the repository.

Spoiler alert: it’s **not**. 😏
Your mission? Dig into the repo’s history and recover what was “lost.”

---

## 🧭 Step-by-step Hunt

### 🔍 Step 1 — Check the repo’s timeline

Let’s see what went down:

```bash
git log --oneline --graph --decorate --all
```

and then zoom in on deleted files:

```bash
git log --diff-filter=D --summary --all
```

🧾 Boom — we find this smoking gun:

```
commit 56c6dac... (Removed config file - oops!)
 delete mode 100644 config.txt
```

---

### 🪄 Step 2 — Bring back the “deleted” file

Git never truly forgets. The file still lives in the parent commit:

```bash
git show 56c6dac^:config.txt > recovered-config.raw
```

---

### ⚙️ Step 3 — What’s with the weird symbols?!

Open the file — you’ll see gibberish like ` u s e r n a m e ...`.

That’s UTF-16-LE encoding (thanks, Windows 😬). Let’s fix that.

```bash
iconv -f UTF-16LE -t UTF-8 recovered-config.raw > recovered-config.txt
```

Or if you’re a Python enjoyer:

```bash
python3 - <<'PY'
raw = open('recovered-config.raw','rb').read()
print(raw.decode('utf-16-le'))
PY
```

---

### 🗝️ Step 4 — The Reveal

Open the converted file:

```
username: admin_user
password: S3cur3P4ss2024!
```

#### 🔒 Spoiler — reveal the flag
<details> <summary>🎯 Click to reveal the flag</summary>

Flag (revealed):

S3cur3P4ss2024!

</details>

---

## 🧠 Why This Works

Deleting a file in Git doesn’t *erase* it — the data remains in history until it’s explicitly purged.
We simply went back in time to the commit *before* it was deleted and read it out. Easy win. 💪

---

## 🧰 Bonus Tools I Used

* `git log --diff-filter=D` → find deleted files
* `git show <commit>^:<file>` → resurrect the file
* `iconv` → fix encoding weirdness
* `git grep` → look for hidden `flag{}`s (none found)
* `git fsck --lost-found` → check for dangling blobs

---

## 🚨 Lessons Learned

🧩 **1. Git remembers everything.**
Deleting ≠ gone. Once pushed, your secret is part of history.

🕳️ **2. Rotate secrets immediately.**
Even in CTFs — never trust old passwords.

🧹 **3. Clean your history if this happens for real.**
Use:

```bash
git filter-repo --path config.txt --invert-paths
git gc --prune=now --aggressive
```

🧱 **4. Prevent leaks.**
Add a `.gitignore`, secret scanners (like *Gitleaks* or *TruffleHog*), and pre-commit hooks.

---

## 🏁 Final Thoughts

Another “Oops-I-committed-a-secret” challenge — classic dev move.
By simply walking back through the Git history and decoding a UTF-16 file, we grabbed the hidden flag.

✅ **Flag recovered:** `S3cur3P4ss2024!`
💾 **Lesson learned:** Git never forgets. 😅

---

Generated with OpenAI ChatGPT
