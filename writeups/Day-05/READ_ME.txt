=========================================================================================================
October CTF - Day 05
=========================================================================================================

A junior analyst accidently leaked some information about his really private address used for development.
The leak was reported to be obvious to anyone looking at the txid.

Can you find the flag?

tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0

Note: This address belongs in the testnet

=========================================================================================================

Resolve

## 🕵️‍♂️ CTF Write-Up: **Private Address Leak via Bitcoin Testnet Transaction**

### 📌 Challenge Summary

> _"A junior analyst accidentally leaked some information about his really private address used for development. The leak was reported to be obvious to anyone looking at the txid."_  
>  
> **Given:**  
> Bitcoin Testnet address: `tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0`  
>  
> **Objective:**  
> Find the hidden flag by analyzing the transaction(s) associated with the address.

---

### 🧭 Step-by-Step Solution

#### 1. **Understanding the Context**
The challenge hints that the leak is visible to “anyone looking at the txid,” suggesting that the transaction itself contains the flag—possibly in the metadata or OP_RETURN field.

#### 2. **Locating the Address on a Testnet Explorer**
We used a Bitcoin testnet block explorer such as:
- [Mempool.space Testnet](https://mempool.space/testnet) -> https://mempool.space/testnet/address/tb1qc3kuvwdp97t6ytg9sch5w70ste4wuduk2gkwr0
- [Blockchair Testnet Explorer](https://blockchair.com/bitcoin/testnet)
- [BitRef Testnet](https://bitref.com/)

By pasting the address into the search bar, we retrieved its transaction history.

#### 3. **Inspecting the Transaction**
The address had a single transaction. Upon opening it, we examined:
- **Transaction ID (txid)**
- **Outputs**, especially any with `OP_RETURN` scripts

#### 4. **Finding the Flag**
Right next to the OP_RETURN output, the explorer displayed a **hex-encoded message**. In many CTFs, flags are embedded in this field because it allows arbitrary data to be stored on-chain.

In this case, the flag was **clearly visible** in the explorer interface—no decoding required. It was presented in the format:

```
FLAG{...}
```

This confirmed the challenge’s hint: the leak was “obvious” to anyone inspecting the transaction.

---

### 🧠 Key Concepts

- **Bitcoin Testnet**: A sandbox version of Bitcoin used for development and testing.
- **OP_RETURN**: A script opcode used to embed up to 80 bytes of arbitrary data in a transaction.
- **txid (Transaction ID)**: A unique identifier for a transaction, often used to trace and verify blockchain activity.

---

### ✅ Final Flag

> `FLAG{...}`  
> *(Exact flag redacted for write-up purposes)*

---

### 🛠️ Tools Used

- Bitcoin Testnet Explorers
- Hex decoding (optional)
- Basic blockchain analysis

---

### 📚 Lessons Learned

- Always inspect OP_RETURN fields in blockchain CTFs—they’re a common hiding spot.
- Testnet explorers are invaluable for tracing transactions and metadata.
- txid analysis can reveal more than just hashes—it can expose embedded data.

---
