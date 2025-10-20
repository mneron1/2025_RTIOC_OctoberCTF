The script quickly :

- Opens the image, reports mode/size/format  
- Extracts **R/G/B/Alpha** channels and **bit-planes**  
- Generates **enhanced** variants (autocontrast, equalize, brightness multipliers, invert)  
- Parses **PNG text chunks** (`tEXt`, `zTXt`, `iTXt`) and decompresses where applicable  
- Scans for **appended data** (ZIP/PDF/GZIP/RAR/7z) and extracts ZIPs automatically  
- Runs **LSB ASCII** extraction (both byte bit-order variants)  
- Dumps **strings** from the whole file and searches for `flag{...}` patterns  
- Saves everything into an output folder

Works best on **Python 3.9+** with **Pillow** (and optionally **NumPy** for performance).

---

## ✅ Prerequisites (Windows, no WSL)

1. **Install Python** (3.9+):  
   <https://www.python.org/downloads/>  
   Check “Add Python to PATH” during install.

2. **Install dependencies** (Pillow required; NumPy optional but recommended):
   ```powershell
   pip install pillow numpy
   ```
   > If you’d rather avoid NumPy, the script will fall back to a slower pure-Python path automatically.

---

## ▶️ Usage

Save the script below as `stego_image_analyzer.py`, then run:

```powershell
python stego_image_analyzer.py "v.0_secretCommunicationTestFile_finalfinal3.png"
```

Optional arguments:
```powershell
python stego_image_analyzer.py <input_image> --out out_dir --max-bytes 20000000 --no-numpy
```

- `--out` : output directory (default: `out_<basename>`)
- `--max-bytes` : safety cap for file size reads
- `--no-numpy` : force pure-Python (slower)

---

## 📦 What You’ll Get in the Output Folder

- `strings/strings.txt` — all printable strings from the file (auto-flag search)
- `png_chunks/png_text_chunks.txt` — text from `tEXt`/`zTXt`/`iTXt` (if PNG)
- `channels/` — R, G, B, A channels (and autocontrast versions)
- `enhanced/` — autocontrast, equalize, invert+autocontrast, brightness-boost variants
- `bitplanes/` — all bit-planes 0–7 per channel
- `lsb/` — raw LSB-extracted byte streams + printable views; auto flag search
- `extracted/` — any appended blobs (and ZIP contents if detected)

---

## 🔎 Tips

- If you know the challenge tends to hide in alpha or LSBs, check:
  - `channels/A_autocontrast.png`
  - `bitplanes/*_bit0.png` to `*_bit2.png`
  - `lsb/LSB_*_bit0_msb.txt` (and `_lsb.txt`)
- The script prints any hits matching `flag{...}` in the console and collects them in the relevant outputs.

---

If you want, I can also **bundle this as a ready-to-run `.zip`** with a sample folder structure and a **PowerShell helper** (`run.ps1`) so you can drag-and-drop files for analysis.