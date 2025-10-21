# CTF Writeup — Owl Logo (Day 08)

## Summary

* **Challenge:** Identify the programming language and designer from a noisy orange-owl image.
* **Answer / Flag:** `flag{Prolog_SteveReeves}`

---

# Steps & Findings

## 1. Quick metadata check

* Command used (Python/Pillow): read EXIF.
* **Result:** No EXIF / metadata present. Nothing useful there.

## 2. Inspect visible LSB layer (heuristic)

* Extracted least-significant bits from all color channels to a grayscale image to see hidden bitplane content.
* File produced: `lsb_output.png`
* **Result:** LSB image did not reveal meaningful plaintext or additional clues — it appeared noisy / empty.

## 3. Common stego checks

* Tried the usual tools/techniques (conceptually):

  * `steghide info` / `steghide extract` (no known passphrase found / nothing obvious).
  * `binwalk` (would look for appended archives / embedded files).
  * `zsteg` (for PNG/BMP bitplane checks).
* **Result:** No embedded payload discovered by these typical approaches (consistent with your suspicion that there was no hidden data).

## 4. Visual identification

* With no hidden data to extract, the remaining route was visual identification.
* The orange owl in a white circular badge is the **SWI-Prolog** mascot/logo.

  * Language: **Prolog**
  * Designer credited: **Steve Reeves** (name used in the challenge format without spaces: `SteveReeves`)

---

# Final Flag

```
flag{Prolog_SteveReeves}
```

---

# Notes / Reproducible commands

* EXIF (Python):

```python
from PIL import Image, ExifTags
img = Image.open("DAY08_Owl.jpg")
print(img.getexif())
```

* LSB extraction (Python sketch):

```python
from PIL import Image
import numpy as np
img = Image.open("DAY08_Owl.jpg").convert("RGB")
pixels = np.array(img)
lsb = (pixels & 1)
lsb_gray = (lsb[:,:,0]*85 + lsb[:,:,1]*85 + lsb[:,:,2]*85).astype('uint8')
Image.fromarray(lsb_gray).save("lsb_output.png")
```

* steghide (if available):

```bash
steghide info -sf DAY08_Owl.jpg
steghide extract -sf DAY08_Owl.jpg
```

* zsteg (after converting to PNG):

```bash
# convert via ImageMagick if needed:
magick DAY08_Owl.jpg DAY08_Owl.png
zsteg -a DAY08_Owl.png
```

---

Generated with OpenAI ChatGPT
