Here’s a **detailed Markdown write-up** you can use for documentation:

---

# 🔐 CTF Challenge Day 9 – NTLM Hash Cracking

## **Challenge Description**
We are given five NTLM hashes extracted from an old Windows Security Account Manager (SAM) file. The goal is to recover the plaintext passwords and construct the flag in the format:

```
flag{hash1_hash2_hash3_hash4_hash5}
```

### **Hashes Provided**
```
0ea0e4bb502bd4acaf6997d7c26b54d1
326f5f6c590b925012b8930758b42148
1337bdd3c9fa21e8d72849e1618d2535
9ad1180ec59ccbca760e6de738fb4d70
6b56ad7d13656b993ded0758f58794f6
```

---

## **Step 1: Identify the Hash Type**
- Each hash is **32 hexadecimal characters**.
- The challenge name is **NTLM**, which strongly suggests these are **NTLM hashes**.
- NTLM hashes are unsalted and based on the MD4 algorithm applied to the UTF-16LE password.

---

## **Step 2: Tools for Cracking NTLM Hashes**
### ✅ **Windows-Compatible Tools**
- **[John the Ripper](https://www.openwall.com/john/)**
- **Hashcat**
- **Cain & Abel** (legacy)
- **Online NTLM hash databases**:
  - [CrackStation](https://crackstation.net)
  - [Hashes.com](https://hashes.com/en/decrypt/hash)

---

## **Step 3: Install John the Ripper on Windows**
1. Download the latest **Windows binaries** from [Openwall](https://www.openwall.com/john/).
2. Extract the ZIP to a folder, e.g., `C:\JohnTheRipper`.
3. Open **Command Prompt** and navigate to the `run` directory:
   ```cmd
   cd C:\JohnTheRipper\run
   ```
4. Verify installation:
   ```cmd
   john --version
   ```

---

## **Step 4: Prepare the Hash File**
Create a text file named `hashes.txt` with the five hashes, one per line:
```
0ea0e4bb502bd4acaf6997d7c26b54d1
326f5f6c590b925012b8930758b42148
1337bdd3c9fa21e8d72849e1618d2535
9ad1180ec59ccbca760e6de738fb4d70
6b56ad7d13656b993ded0758f58794f6
```

---

## **Step 5: Crack the Hashes**
### **Using John the Ripper**
```cmd
john --format=NT hashes.txt --wordlist=rockyou.txt
```

### **Using Hashcat**
```cmd
hashcat -m 1000 hashes.txt rockyou.txt
```
- `-m 1000` → NTLM mode
- `rockyou.txt` → common password wordlist

---

## **Step 6: Build the Flag**
Once all hashes are cracked, concatenate the plaintext passwords in the given order:
```
flag{password1_password2_password3_password4_password5}
```

---

## **Notes**
- NTLM hashes are case-sensitive and based on the original password in **UTF-16LE**.
- If the password is not in your wordlist, consider **brute force** or **hybrid attacks**.

---

### ✅ **Next Steps**
- Do you want me to **also include an example cracking session output** (with fake passwords for illustration)?
- Or **prepare a section on optimizing Hashcat performance for NTLM**?

Would you like me to **add a section on common pitfalls and troubleshooting** for NTLM cracking?