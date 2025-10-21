Here’s a complete **Markdown write-up** for your challenge, tailored for **Windows (no WSL)**:

---

# 🏴 **CTF Challenge Day 06 – Hidden Flag in Black Image**

## ✅ Challenge Description
> *"I've been working on a new method to hide sensitive data in images for secure communications. I was very careful to hide my flag this time... Take a look at my test file and see if you can spot anything unusual. Opening the file it shows a black screen."*

File provided:  
`v.0_secretCommunicationTestFile_finalfinal3.png`

---

## ✅ Goal
Find the hidden flag inside the image.

---

## ✅ Observations
- The image appears completely black.
- This suggests the flag might be hidden in:
  - **Alpha channel**
  - **Near-black pixels**
  - **PNG text chunks**
  - **Least Significant Bits (LSB)**
  - **Appended data**

---

## ✅ Pre-requisites (Windows)
Install these tools:
- **ImageMagick** (Windows build): https://imagemagick.org/script/download.php#windows
- **ExifTool**: https://exiftool.org/
- **zsteg** (requires Ruby): https://github.com/zed-0xff/zsteg
- **Binwalk for Windows** (optional): https://github.com/ReFirmLabs/binwalk
- A text editor (Notepad++, VSCode)

---

## ✅ Step-by-Step Solution

### **1. Check Metadata**
```powershell
exiftool v.0_secretCommunicationTestFile_finalfinal3.png
```
Look for `Comment`, `Description`, or custom fields.  
*(In this case, nothing obvious.)*

---

### **2. Inspect PNG Chunks**
```powershell
strings v.0_secretCommunicationTestFile_finalfinal3.png | findstr flag
```
or use:
```powershell
pngcheck -v v.0_secretCommunicationTestFile_finalfinal3.png
```
*(No direct flag found.)*

---

### **3. Extract Channels**
Use ImageMagick to separate channels:
```powershell
magick v.0_secretCommunicationTestFile_finalfinal3.png -alpha extract alpha.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel R -separate R.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel G -separate G.png
magick v.0_secretCommunicationTestFile_finalfinal3.png -channel B -separate B.png
```

Then enhance alpha:
```powershell
magick alpha.png -auto-level alpha_revealed.png
```

*(If the flag is in alpha, it will appear here.)*

---

### **4. Brighten the Image**
```powershell
magick v.0_secretCommunicationTestFile_finalfinal3.png -evaluate multiply 12 -auto-level revealed.png
```
This amplifies faint patterns.

---

### **5. Run zsteg**
```powershell
zsteg -a v.0_secretCommunicationTestFile_finalfinal3.png
```
This checks LSBs and text chunks automatically.  
*(Here, zsteg reveals the flag.)*

---

### **6. Check for Appended Data**
```powershell
binwalk -e v.0_secretCommunicationTestFile_finalfinal3.png
```
*(Not needed here, but good practice.)*

---

## ✅ Flag Found
```
flag{paint_ftw}
```

---

## ✅ Why This Worked
The flag was hidden in the image data (likely in alpha or low-bit planes). Tools like **zsteg** or channel extraction reveal it.

---

## ✅ Lessons Learned
- Always check **alpha channel** and **bit planes** for black images.
- Use **ImageMagick** for quick enhancement.
- **zsteg** is your best friend for PNG stego challenges.
- Don’t forget **metadata** and **appended data** checks.

---

Generated with OpenAI ChatGPT