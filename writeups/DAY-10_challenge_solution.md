# Day 10 — Hidden Encoding (CTF) — Write-up

## Summary

Hidden inside a shipped website was a custom JavaScript XOR encoder and a backtick-quoted blob containing non-printable control bytes. By extracting the exact raw bytes and faithfully reproducing the JavaScript behavior (including a 1-character pass quirk), we recovered the flag:

```
flag{console.log("hello world")}
```

---

## Goal

Find the hidden flag left in the code of a provided website archive.

---

## Key Observations

* The `index.html` contained a function named `xorEncode(txt, pass)` that built a mapping for characters `1..255` and XORed `txt` with `pass`.
* Immediately below the function, two commented lines appeared:

  ```js
  //super secret txt = `SlTgNcZnFoYelZg"]eYlZ BoGlQ"}`
  //super secret pass = 0b101
  ```
* The `txt` contained **non-printable control bytes** (escape, group separator, file separator): `\x1b`, `\x1d`, `\x1c`.
* `pass = 0b101` hints at binary `5`, but the JS code used `ord[pass.substr(...)]` — meaning the character `'5'` might be used (ASCII 53) depending on interpretation.

---

## Deep-dive: The JS subtlety

The core loop in the JS encoder is:

```js
for (j = z = 0; z < txt.length; z++) {
    buf += String.fromCharCode(ord[txt.substr(z, 1)] ^ ord[pass.substr(j, 1)]);
    j = (j < pass.length) ? j + 1 : 0;
}
```

With a **1-character pass**, `pass.substr(j,1)` becomes `''` on the iteration when `j == pass.length` (treated as `undefined` → 0 in the mapping). The net effect is **only every other character is XORed** (XOR, skip, XOR, skip, ...). Reproducing that behavior precisely is essential.

---

## Extraction (how we got the raw bytes)

Copy/pasting from rendered HTML can hide control characters. We used a byte-level extractor to pull the backtick block exactly as stored in the file.

**Extractor (core idea)**:

* Read `index.html` as raw bytes.
* Regex-search for the backtick-enclosed `super secret txt` comment.
* Output the bytes as escaped text and hex for inspection.

Example snippet used (saved as `extract_secret.py` — run `python3 extract_secret.py index.html`):

```python
# (excerpt)
b = open(path, 'rb').read()
m = re.search(b'super secret txt\\s*=\\s*`([\\s\\S]*?)`', b, flags=re.IGNORECASE)
block_bytes = m.group(1)
# Now block_bytes contains exact bytes including \x1b \x1d \x1c
```

Escaped output:

```
SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}
```

Hex bytes:

```
53 6c 54 67 4e 63 5a 6e 46 6f 59 65 1b 6c 5a 67 1d 22 5d 65 59 6c 5a 20 42 6f 47 6c 51 22 1c 7d
```

---

## Decoding approach

Two crucial points:

1. Use the **literal raw characters** (including control bytes) — do not use a copy where quotes/escapes were inserted.
2. The JS behavior XORs **every other character** when `pass` has length 1. The pass should be used as the character `'5'` (ASCII 53) rather than the numeric 5.

We implemented a compact Python decoder that:

* converts `\xNN` escapes into real control bytes if needed,
* XORs the correct set of positions using `ord('5') == 53`,
* strips non-printables for a clean printed result.

Final decoder (essence, saved as `decode_secret_v3.py`):

```python
def cheat_decode_final(encoded: str, key_char: str) -> str:
    key = ord(key_char)
    chars = []
    for i, ch in enumerate(encoded):
        if i % 2 == 0:          # XOR even indices 0,2,4,...
            chars.append(chr(ord(ch) ^ key))
        else:
            chars.append(ch)
    return ''.join(chars)

# supply raw escaped string then decode escapes to real control bytes:
encoded = r"SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}"
encoded = encoded.encode("utf-8").decode("unicode_escape")
print(''.join(c for c in cheat_decode_final(encoded, "5") if 32 <= ord(c) < 127))
```

Running that yielded:

```
flag{console.log("hello world")}
```

---

## Tools used

* Python 3 — small helper scripts (`extract_secret.py`, `decode_secret_v3.py`)
* `xxd` / hex-viewer (recommended to inspect raw bytes in the HTML if needed)
* A text editor that can show/handle raw bytes (e.g., VSCode with hex preview, Notepad++ hex plugin) — for verification.

---

## Timeline (how we progressed)

1. Inspect `index.html` and find suspicious `xorEncode` function and commented `super secret txt` / `super secret pass`.
2. Try naive decoding attempts in Python — encountered unreadable output (control characters shown as escapes and slight corruption).
3. Recognize non-printable bytes; write a byte-level extractor to get the exact raw sequence from the file.
4. Analyze the JS loop carefully and reason about the `j` update with a 1-byte pass — conclude only every other character is XORed.
5. Try both key interpretations (`0b101` → 5, and `'5'` → ASCII 53); find that `'5'` plus XORing the correct half yields readable output.
6. Implement final decoder and verify the flag.

---

## Final Notes / Lessons Learned

* Small differences in how languages treat strings and substrings (empty substrings, control bytes, Unicode vs. bytes) can cause large headaches when porting code.
* When an encoded blob "almost" decodes to a human-readable string, the remaining garbage often hints at alignment or missing bytes — use that to guide targeted changes rather than blind brute force.
* Always extract data at the raw byte level when control characters are suspected.

---

Writeup generated with OpenAI ChatGPT
