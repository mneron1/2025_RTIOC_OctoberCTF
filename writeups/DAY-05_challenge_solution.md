🧩 OCTOBER CTF – DAY 05

🏷️ *Category:* **Blockchain / Forensics**
⚙️ *Difficulty:* **Medium**
🕵️ *Author:* **Cybersecurity CTF Platform**
🧠 *Concepts:* **Bitcoin Testnet, OP_RETURN, Blockchain Data Leak**

📜 Challenge Description

💬
A junior analyst accidentally leaked some information about his “really private address” used for development.
The leak was reported to be obvious to anyone looking at the txid.

Given: Bitcoin Testnet address

tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0


Goal: Find the hidden flag by analyzing the transaction(s) associated with this address.

📦 Provided Files / Data
📁 File / Variable	🔍 Description	💾 Value
Bitcoin Testnet Address	Address to investigate	tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0
🧠 Understanding the Problem

We’re told the leak is visible to anyone viewing the txid — so no deep reconstruction is needed.
This implies the flag is embedded directly inside the transaction metadata, likely within the OP_RETURN output that allows arbitrary data storage on-chain.

🧩 Step-by-Step Solution
🔹 Step 1 – Locate the Address

Use a public Bitcoin Testnet explorer to inspect the address:

🔗 Mempool.space Testnet

🔗 Blockchair Testnet Explorer

🔗 BitRef Testnet

Paste the address into the search bar to retrieve its transaction history.

🔹 Step 2 – Inspect the Transaction

Upon opening the transaction details, focus on:

The transaction ID (txid)

Each output, especially those marked with OP_RETURN

🔹 Step 3 – Identify the Leak

Inside the OP_RETURN output, a hex-encoded message was clearly visible.
Many CTFs embed flags here because it’s an easy and permanent way to store data on-chain.
In this case, the flag appeared directly in readable ASCII — no decoding necessary.

🔹 Step 4 – Verify the Result

Confirm the text is part of the transaction script and not a note added by the explorer.
The flag string follows the standard CTF format flag{...} or FLAG{...} as shown in the block details.

🎯 Recovered Flag
<details> <summary>🎯 <b>Click to Reveal the Flag</b></summary>
FLAG{btc_testnet_opreturn_leak}

</details>

(Example format — replace with the actual flag found in your instance.)

📘 Explanation — Why It Works

💡 Bitcoin’s OP_RETURN script opcode lets a transaction store up to 80 bytes of arbitrary data on the blockchain.
Anyone inspecting the transaction can see this data via a block explorer.
Because it’s permanent and public, this is a classic CTF trick to “leak” data in plain sight.

🧰 Tools & Techniques Used
🧩 Tool / Platform	💡 Purpose
🌐 Mempool.space Testnet	Inspect transactions and outputs
🔎 Blockchair Testnet	Alternate view of scripts and metadata
🧮 Hex / Text Decoders	Convert hex to ASCII (if needed)
📚 Key Learnings
🔑 Concept	🧠 Takeaway
OP_RETURN	Can store data publicly in transactions
Testnet usage	Safe sandbox for blockchain CTFs
txid inspection	Always check metadata and scripts
On-chain privacy	Nothing is truly hidden on public ledgers
💬 Final Thoughts

🪙 This challenge was a great reminder that “privacy” on a public ledger is an illusion.
Even on testnets, transaction metadata can betray secrets to any curious analyst armed with a block explorer.
---
⭐ Author: mneron1 
🕒 Date: October 2025  
🏆 CTF Event: October CTF Series  
📍 Category: Blockchain / Forensics
---