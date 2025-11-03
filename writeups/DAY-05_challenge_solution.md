# 🧩 **OCTOBER CTF – DAY 05**

> 🏷️ *Category:* **Blockchain / Forensics**
> ⚙️ *Difficulty:* **Medium**
> 🕵️ *Author:* **Cybersecurity CTF Platform**
> 🧠 *Concepts:* `Bitcoin Testnet`, `OP_RETURN`, `Blockchain Data Leak`

---

## 📜 Challenge Description

> 💬
> A junior analyst accidentally leaked information about his *“really private address”* used for development.
> The leak was said to be **obvious to anyone looking at the txid**.
>
> **Given:**
> Bitcoin Testnet address → `tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0`
>
> **Goal:**
> Find the hidden flag by analyzing the transaction(s) associated with this address.

---

## 📦 Provided Files / Data

| 📁 File / Variable        | 🔍 Description         |                                     💾 Value |
| ------------------------- | ---------------------- | -------------------------------------------: |
| `Bitcoin Testnet Address` | Address to investigate | `tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0` |

---

## 🧠 Understanding the Problem

🕵️‍♂️ Before jumping in, let's understand what we’re dealing with:

> The challenge explicitly mentions that the leak is *“visible to anyone looking at the txid.”*
> This implies no cryptographic reconstruction is required — the flag is most likely embedded within an **`OP_RETURN` output** in a Bitcoin transaction.
>
> The **OP_RETURN** opcode allows arbitrary data to be written directly to the blockchain, often in **hex** or **ASCII** format — a favorite trick in blockchain-related CTFs.

---

## 🧩 Step-by-Step Solution

### 🔹 Step 1: Initial Observation

🧩 *“What does this look like?”*

* The address begins with **tb1q**, identifying it as a **Bitcoin Testnet Bech32 address**.
* The challenge hints at the *txid*, meaning we should inspect **transaction metadata** rather than balances.
* Common data leak vectors on the blockchain:

  * OP_RETURN outputs
  * Unusual text in the scriptPubKey
  * Hex-encoded ASCII in transaction metadata

---

### 🔹 Step 2: Locate the Address and Transactions

Visit a public **Bitcoin Testnet explorer**:

* 🌐 [Mempool.space Testnet](https://mempool.space/testnet)
* 🌐 [Blockchair Testnet](https://blockchair.com/bitcoin/testnet)
* 🌐 [BitRef Testnet](https://testnet.blockexplorer.com/)

Paste the given address to view its **transaction history** and inspect the associated **txids**.

---

### 🔹 Step 3: Inspect Transaction Outputs

In the transaction details, look at the **Outputs** section:

* Identify any `OP_RETURN` outputs.
* These typically appear with a script format like:

  ```
  OP_RETURN 0x<hex data>
  ```
* Check if the data is **readable ASCII** or **hex-encoded text**.

🧩 **Result:**
The OP_RETURN field contained plain-text data resembling a flag — no decoding required.

---

### 🔹 Step 4: Decode (if needed)

If the message appears in **hex format**, convert it to text using:

```bash
echo "<hex_value>" | xxd -r -p
```

Or with Python:

```python
bytes.fromhex("<hex_value>").decode()
```

In this challenge, the flag was **directly visible** within the OP_RETURN output, confirming the leak.

---

### 🔹 Step 5: Recover the Flag

<details>
<summary>🎯 <b>Click to Reveal the Flag</b></summary>

```
FLAG{btc_testnet_opreturn_leak}
```

</details>

---

## 📘 Explanation — *Why It Works*

💡 **In short:**

> The **OP_RETURN** opcode in Bitcoin scripts allows storing arbitrary data (up to 80 bytes) in a transaction output.
>
> Because blockchain data is **immutable and public**, anything written to OP_RETURN is **visible forever** to anyone inspecting the transaction.
>
> This is why leaking data on-chain — even on **testnet** — is considered a major privacy flaw.

---

## 🧰 Tools & Techniques Used

| 🧩 Tool / Platform             | 💡 Purpose                                       |
| ------------------------------ | ------------------------------------------------ |
| 🌐 **Mempool.space (Testnet)** | Inspect Bitcoin Testnet transactions and outputs |
| 🔎 **Blockchair Testnet**      | Alternative blockchain explorer                  |
| 🧮 **Hex/ASCII converters**    | Decode OP_RETURN payloads                        |
| 🧠 **Blockchain OSINT**        | Manual inspection of public ledger data          |

---

## 📚 Key Learnings

| 🔑 Concept                  | 🧠 Takeaway                                                 |
| --------------------------- | ----------------------------------------------------------- |
| **OP_RETURN**               | Allows arbitrary data embedding in Bitcoin transactions     |
| **Testnet vs Mainnet**      | Testnet is a safe sandbox for experiments, but still public |
| **Transaction forensics**   | Always review scripts for human-readable leaks              |
| **Blockchain transparency** | Once written, data on-chain is permanent and public         |

---

## 💬 Final Thoughts

> 🪙 This challenge highlights how **“privacy” on public ledgers is often an illusion**.
> Even developers experimenting on testnets can unintentionally expose sensitive data.
>
> Whether it’s a flag or a private key, **anything on-chain stays there forever** — visible to anyone who knows where to look. 🔍

---
⭐ **Author:** mneron1
🕒 **Date:** October 2025
🏆 **CTF Event:** October CTF Series
📍 **Category:** Blockchain / Forensics
---