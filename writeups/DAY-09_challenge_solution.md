🧩 OCTOBER CTF – DAY 09

🏷️ *Category:* **Cryptography / Password Cracking**
⚙️ *Difficulty:* **Medium–Hard**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **NTLM, MD4, Hash Cracking, John the Ripper, Hashcat**

📜 Challenge Description

💬
“We recovered five suspicious hashes from an old Windows SAM file.
Can you reveal the passwords and build the final flag?”

Goal: Crack all NTLM hashes and construct the flag in this format:

flag{password1_password2_password3_password4_password5}


Given Hashes:

0ea0e4bb502bd4acaf6997d7c26b54d1
326f5f6c590b925012b8930758b42148
1337bdd3c9fa21e8d72849e1618d2535
9ad1180ec59ccbca760e6de738fb4d70
6b56ad7d13656b993ded0758f58794f6

📦 Provided Files / Data
📁 File / Variable	🔍 Description	💾 Value
hashes.txt	List of 5 NTLM hashes	See above
🧠 Understanding the Problem

The hashes are:

32 hex characters long

Identified as NTLM hashes, which are unsalted MD4 digests of the password encoded in UTF-16LE.
Since NTLM is unsalted, common passwords are easily recoverable using dictionary attacks (e.g., rockyou.txt).

🧩 Step-by-Step Solution
🔹 Step 1 – Identify Hash Type

All hashes are 32 characters (128 bits) → matches NTLM format.
NTLM hashes = MD4(UTF-16LE(password)).

🔹 Step 2 – Select Tools

You can use any of the following:

🧰 Tool	💡 Purpose
John the Ripper	Simple CLI cracking (Windows-friendly)
Hashcat	GPU-accelerated, supports hybrid and brute force
CrackStation / Hashes.com	Online quick lookup for common passwords
Cain & Abel (Legacy)	Optional GUI-based Windows tool
🔹 Step 3 – Prepare Your Environment (Windows Example)
📦 Install John the Ripper

Download from Openwall John the Ripper
.

Extract to C:\JohnTheRipper.

Navigate to its run folder:

cd C:\JohnTheRipper\run


Verify:

john --version

🔹 Step 4 – Create a Hash File

Save the five hashes into a file named hashes.txt:

0ea0e4bb502bd4acaf6997d7c26b54d1
326f5f6c590b925012b8930758b42148
1337bdd3c9fa21e8d72849e1618d2535
9ad1180ec59ccbca760e6de738fb4d70
6b56ad7d13656b993ded0758f58794f6

🔹 Step 5 – Run the Crack
🪓 Using John the Ripper
john --format=NT hashes.txt --wordlist=rockyou.txt

⚡ Using Hashcat
hashcat -m 1000 hashes.txt rockyou.txt


-m 1000 → NTLM mode

rockyou.txt → Common wordlist (Linux or GitHub source)

🔹 Step 6 – Verify & Rebuild the Flag

After cracking, combine all recovered plaintexts in order:

flag{password1_password2_password3_password4_password5}


Example (illustrative only):

flag{letmein_admin123_qwerty_password_iloveyou}

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
flag{password1_password2_password3_password4_password5}

</details>
📘 Explanation — Why It Works

💡 NTLM hashes are vulnerable because:

They use the MD4 algorithm (cryptographically weak).

They are unsalted, meaning identical passwords have identical hashes.

Pre-computed rainbow tables and wordlists (like RockYou) can quickly reverse them.

🧰 Tools & Techniques Used
🧩 Tool / Platform	💡 Purpose
🔐 John the Ripper	Password cracking
⚡ Hashcat	GPU-accelerated hash cracking
🌐 CrackStation / Hashes.com	Online lookup for fast verification
🧾 RockYou.txt	Common password wordlist
📚 Key Learnings
🔑 Concept	🧠 Takeaway
NTLM hashes	Unsalted, easily reversible with wordlists
UTF-16LE encoding	Core of NTLM password generation
Dictionary attacks	Fast and effective on weak hashes
Wordlist hygiene	Choose targeted lists for faster results
💬 Final Thoughts

💻 Even decades-old authentication schemes like NTLM still appear in the wild — a perfect reminder that backward compatibility can compromise security.
One weak password can still bring down an entire system.

---
⭐ Author: mneron1
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Cryptography / Password Cracking
---
