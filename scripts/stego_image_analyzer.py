#!/usr/bin/env python3
# stego_image_analyzer.py
# Windows-friendly, no WSL required.
# Python 3.9+; requires Pillow. NumPy optional.

import argparse
import os
import sys
import re
import zlib
import struct
from pathlib import Path

# Optional NumPy
USE_NUMPY = True
try:
    import numpy as np
except Exception:
    USE_NUMPY = False

from PIL import Image, ImageOps, ImageChops

FLAG_REGEXPS = [
    re.compile(rb"flag\{[^}\r\n]{1,200}\}", re.IGNORECASE),
    # Add your CTF’s variations here if needed (e.g., CTF{...}, picoCTF{...}, etc.)
]

# --------- Utils ---------

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def printable_bytes(b: bytes) -> str:
    return "".join(chr(c) if 32 <= c <= 126 else "." for c in b)

def save_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8", errors="replace")

def save_bytes(path: Path, data: bytes):
    path.write_bytes(data)

def human(n):
    for unit in ["B","KB","MB","GB"]:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"

def info(msg):
    print(f"[i] {msg}")

def warn(msg):
    print(f"[!] {msg}")

# --------- File read & quick scan ---------

def read_file_bytes(fn: Path, max_bytes: int) -> bytes:
    sz = fn.stat().st_size
    if sz > max_bytes:
        raise RuntimeError(f"File too large ({human(sz)}). Increase --max-bytes if intentional.")
    return fn.read_bytes()

def scan_signatures(data: bytes):
    # common magic signatures
    sigs = {
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"\xFF\xD8\xFF": "JPEG",
        b"PK\x03\x04": "ZIP",
        b"%PDF": "PDF",
        b"\x1F\x8B\x08": "GZIP",
        b"\x52\x61\x72\x21\x1A\x07\x00": "RAR",
        b"7z\xBC\xAF\x27\x1C": "7-Zip",
        b"BZh": "BZIP2",
        b"ID3": "MP3/ID3"
    }
    hits = []
    for sig, name in sigs.items():
        idx = data.find(sig)
        while idx != -1:
            hits.append((name, sig, idx))
            idx = data.find(sig, idx+1)
    hits.sort(key=lambda t: t[2])
    return hits

def extract_zip_to_dir(zip_bytes: bytes, outdir: Path):
    import io, zipfile
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            zf.extractall(outdir)
        return True, None
    except Exception as e:
        return False, str(e)

# --------- PNG chunk parsing ---------

def parse_png_chunks(data: bytes):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return []

    chunks = []
    pos = 8
    end = len(data)
    while pos + 8 <= end:
        try:
            length = struct.unpack(">I", data[pos:pos+4])[0]
            ctype = data[pos+4:pos+8]
            cdata = data[pos+8:pos+8+length]
            # crc = data[pos+8+length:pos+12+length]
            chunks.append((ctype, cdata, pos, 12+length))
            pos += 12 + length
            if ctype == b"IEND":
                break
        except Exception:
            break
    return chunks

def decode_png_text_chunks(chunks):
    out = []
    for ctype, cdata, _, _ in chunks:
        if ctype == b"tEXt":
            # "keyword\0text"
            try:
                out.append(("tEXt", cdata.decode("latin-1", errors="replace")))
            except Exception:
                out.append(("tEXt", repr(cdata[:64])+("..." if len(cdata)>64 else "")))
        elif ctype == b"zTXt":
            # "keyword\0compression_method(=0) + compressed_text"
            try:
                nul = cdata.index(b"\x00")
                keyword = cdata[:nul].decode("latin-1", errors="replace")
                comp_m = cdata[nul+1]
                comp_data = cdata[nul+2:]
                if comp_m == 0:
                    text = zlib.decompress(comp_data).decode("utf-8", errors="replace")
                    out.append(("zTXt", f"{keyword}: {text}"))
                else:
                    out.append(("zTXt", f"{keyword}: (unknown compression {comp_m}, {len(comp_data)} bytes)"))
            except Exception as e:
                out.append(("zTXt", f"(error decoding) {e}"))
        elif ctype == b"iTXt":
            # iTXt structure: keyword\0 compress_flag(1) \0 compress_method(1) \0 langtag\0 translated_keyword\0 text
            try:
                # Safe but simple parser
                parts = cdata.split(b"\x00", 5)
                if len(parts) >= 6:
                    keyword = parts[0].decode("utf-8", errors="replace")
                    comp_flag = parts[1][0] if parts[1] else 0
                    comp_method = parts[2][0] if parts[2] else 0
                    # parts[3] langtag, parts[4] translated_keyword (ignored here)
                    text_raw = parts[5]
                    if comp_flag == 1:
                        text = zlib.decompress(text_raw).decode("utf-8", errors="replace")
                    else:
                        text = text_raw.decode("utf-8", errors="replace")
                    out.append(("iTXt", f"{keyword}: {text}"))
                else:
                    out.append(("iTXt", "(malformed)"))
            except Exception as e:
                out.append(("iTXt", f"(error decoding) {e}"))
    return out

# --------- Image processing helpers ---------

def save_image(img: Image.Image, path: Path):
    # always save as PNG to avoid recompression artifacts
    img.save(path)

def enhance_variants(img: Image.Image, outdir: Path):
    ensure_dir(outdir)
    save_image(img.convert("RGB"), outdir / "00_original.png")

    # Autocontrast
    try:
        ac = ImageOps.autocontrast(img.convert("RGB"))
        save_image(ac, outdir / "10_autocontrast.png")
    except Exception:
        pass

    # Equalize
    try:
        eq = ImageOps.equalize(img.convert("RGB"))
        save_image(eq, outdir / "11_equalize.png")
    except Exception:
        pass

    # Invert + autocontrast
    try:
        inv = ImageOps.invert(img.convert("RGB"))
        inv_ac = ImageOps.autocontrast(inv)
        save_image(inv_ac, outdir / "12_invert_autocontrast.png")
    except Exception:
        pass
    # Brightness multipliers
    for mult in [2,4,6,8,12,16,24]:
        try:
            def f(p): 
                v = int(p * mult)
                return 255 if v > 255 else v
            bright = img.convert("RGB").point(f)
            bright = ImageOps.autocontrast(bright)
            save_image(bright, outdir / f"20_bright_x{mult}.png")
        except Exception:
            pass

def dump_channels(img: Image.Image, outdir: Path):
    ensure_dir(outdir)
    bands = img.getbands()
    rgb = img.convert("RGB")
    for i, name in enumerate(("R","G","B")):
        ch = rgb.getchannel(i)
        save_image(ch, outdir / f"{name}.png")
        save_image(ImageOps.autocontrast(ch), outdir / f"{name}_autocontrast.png")
    if "A" in bands:
        a = img.getchannel("A")
        save_image(a, outdir / "A.png")
        save_image(ImageOps.autocontrast(a), outdir / "A_autocontrast.png")

def bitplanes_numpy(img: Image.Image, outdir: Path):
    ensure_dir(outdir)
    arr = np.array(img.convert("RGBA" if "A" in img.getbands() else "RGB"))
    bands = img.convert("RGBA" if "A" in img.getbands() else "RGB").getbands()
    for ch_i, ch_name in enumerate(bands):
        ch = arr[:,:,ch_i]
        for b in range(8):
            plane = ((ch >> b) & 1) * 255
            Image.fromarray(plane.astype("uint8")).save(outdir / f"{ch_name}_bit{b}.png")

def bitplanes_pure(img: Image.Image, outdir: Path):
    ensure_dir(outdir)
    src = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    bands = src.getbands()
    w, h = src.size
    for ch_i, ch_name in enumerate(bands):
        ch = src.getchannel(ch_i)
        for b in range(8):
            plane = Image.new("L", (w,h))
            px_in = ch.load()
            px_out = plane.load()
            for y in range(h):
                for x in range(w):
                    px_out[x,y] = 255 if ((px_in[x,y] >> b) & 1) else 0
            plane.save(outdir / f"{ch_name}_bit{b}.png")

def lsb_ascii_extraction(img: Image.Image, outdir: Path, max_chars=2000000):
    """
    Extract LSB streams from each channel and bit plane. 
    Build bytes with both MSB-first and LSB-first per byte ordering.
    Save raw and printable previews; search for flag-like patterns.
    """
    ensure_dir(outdir)
    bands_img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    bands = bands_img.getbands()
    w, h = bands_img.size

    def channel_bits(ch_img):
        # emit bits row-major
        if USE_NUMPY:
            arr = np.array(ch_img, dtype=np.uint8)
            bits = (arr & 1).flatten().astype(np.uint8)
            return bits
        else:
            bits = []
            px = ch_img.load()
            for y in range(h):
                for x in range(w):
                    bits.append(px[x,y] & 1)
            return bits

    found = []
    for ch in bands:
        ch_img = bands_img.getchannel(ch)
        for bit in range(4):  # try lower 4 planes
            # derive plane image first
            if USE_NUMPY:
                arr = np.array(ch_img, dtype=np.uint8)
                plane = (arr >> bit) & 1
                bits = plane.flatten().astype(np.uint8)
            else:
                bits = []
                px = ch_img.load()
                for y in range(h):
                    for x in range(w):
                        bits.append((px[x,y] >> bit) & 1)

            # Build bytes MSB-first and LSB-first
            for order in ("msb", "lsb"):
                by = bytearray()
                cur = 0
                cnt = 0
                for b in bits:
                    if order == "msb":
                        cur = (cur << 1) | (b & 1)
                    else:  # lsb
                        cur |= (b & 1) << cnt
                    cnt += 1
                    if cnt == 8:
                        by.append(cur)
                        cur = 0
                        cnt = 0
                        if len(by) >= max_chars:
                            break
                if by:
                    out_bin = outdir / f"LSB_{ch}_bit{bit}_{order}.bin"
                    out_txt = outdir / f"LSB_{ch}_bit{bit}_{order}.txt"
                    save_bytes(out_bin, bytes(by))
                    preview = printable_bytes(bytes(by))
                    save_text(out_txt, preview)

                    for rx in FLAG_REGEXPS:
                        for m in rx.finditer(bytes(by)):
                            found.append((f"{ch}/bit{bit}/{order}", m.group(0).decode("utf-8", "replace")))
    return found
def dump_strings(data: bytes, outpath: Path, minlen=4):
    s = []
    cur = []
    for b in data:
        if 32 <= b <= 126 or b in (9,10,13):
            cur.append(chr(b))
        else:
            if len(cur) >= minlen:
                s.append("".join(cur))
            cur = []
    if len(cur) >= minlen:
        s.append("".join(cur))
    save_text(outpath, "\n".join(s))
    # search flags
    found = []
    for rx in FLAG_REGEXPS:
        for m in rx.finditer(data):
            found.append(m.group(0).decode("utf-8", "replace"))
    return found

# --------- Main pipeline ---------

def analyze(input_path: Path, outdir: Path, max_bytes: int, force_no_numpy: bool):
    global USE_NUMPY
    if force_no_numpy:
        USE_NUMPY = False

    ensure_dir(outdir)
    info(f"Output dir: {outdir}")

    # Read file
    data = read_file_bytes(input_path, max_bytes)
    info(f"Read {human(len(data))} from {input_path.name}")

    # File signature scan
    sig_hits = scan_signatures(data)
    if sig_hits:
        info("Signatures found (name, offset):")
        for name, _, off in sig_hits:
            print(f"   - {name:6s} @ {off}")

    # Strings dump
    strings_dir = outdir / "strings"
    ensure_dir(strings_dir)
    found_in_strings = dump_strings(data, strings_dir / "strings.txt")
    if found_in_strings:
        info("Possible flags in raw strings:")
        for f in found_in_strings:
            print("   ", f)

    # Try to open as image
    try:
        img = Image.open(input_path)
        info(f"Image opened: format={img.format}, mode={img.mode}, size={img.size}")
    except Exception as e:
        warn(f"Failed to open as image: {e}")
        img = None

    # PNG chunk parsing
    png_texts = []
    png_chunks = []
    iend_offset = None
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        png_chunks = parse_png_chunks(data)
        text_chunks = decode_png_text_chunks(png_chunks)
        if text_chunks:
            png_texts = text_chunks
            txt_dir = outdir / "png_chunks"
            ensure_dir(txt_dir)
            lines = []
            for kind, content in text_chunks:
                lines.append(f"[{kind}] {content}")
            save_text(txt_dir / "png_text_chunks.txt", "\n".join(lines))
            info(f"Extracted {len(text_chunks)} PNG text-like chunk(s).")
            # Flag search inside decoded text
            for _, content in text_chunks:
                for rx in FLAG_REGEXPS:
                    for m in rx.finditer(content.encode("utf-8", "ignore")):
                        print("   [PNG chunk] Found:", m.group(0).decode("utf-8", "replace"))
        # find IEND end
        for ctype, cdata, pos, span in png_chunks:
            if ctype == b"IEND":
                iend_offset = pos + span

    # Appended data after IEND (for PNG) or after end of recognizable structure
    extracted_any = False
    extract_dir = outdir / "extracted"
    if iend_offset and iend_offset < len(data):
        tail = data[iend_offset:]
        if tail.strip(b"\x00"):
            ensure_dir(extract_dir)
            save_bytes(extract_dir / "after_iend.bin", tail)
            info(f"Saved appended data after IEND: {human(len(tail))}")
            extracted_any = True
            # Try ZIP autodetect/extract
            idx_zip = tail.find(b"PK\x03\x04")
            if idx_zip != -1:
                ok, err = extract_zip_to_dir(tail[idx_zip:], extract_dir / "zip_after_iend")
                if ok:
                    info("Extracted ZIP found after IEND.")
                else:
                    warn(f"ZIP extraction failed: {err}")

    # If not PNG, try generic signature-based slicing (first non-leading signature)
    if not extracted_any and sig_hits:
        # ignore the first signature if it starts at 0 (likely the main format)
        for name, sig, off in sig_hits:
            if off > 0:
                ensure_dir(extract_dir)
                save_bytes(extract_dir / f"embedded_{name}_{off}.bin", data[off:])
                info(f"Saved embedded {name} from offset {off} ({human(len(data)-off)})")
                if name == "ZIP":
                    ok, err = extract_zip_to_dir(data[off:], extract_dir / f"zip_{off}")
                    if ok:
                        info(f"Extracted ZIP from offset {off}.")
                break

    # If image loaded: dump channels, enhancements, bitplanes, LSB ASCII
    if img is not None:
        chan_dir = outdir / "channels"
        dump_channels(img, chan_dir)

        enh_dir = outdir / "enhanced"
        enhance_variants(img, enh_dir)

        bp_dir = outdir / "bitplanes"
        if USE_NUMPY:
            bitplanes_numpy(img, bp_dir)
        else:
            bitplanes_pure(img, bp_dir)

        lsb_dir = outdir / "lsb"
        lsb_found = lsb_ascii_extraction(img, lsb_dir)
        if lsb_found:
            info("Possible flags via LSB streams:")
            for src, val in lsb_found:
                print(f"   [{src}] {val}")

    # Final summary
    info("Analysis complete.")
    if found_in_strings:
        info(f"Strings pass found {len(found_in_strings)} candidate flag(s).")
    if png_texts:
        info(f"PNG chunk parsing found {len(png_texts)} text-like chunk(s).")
    if img is None and not found_in_strings and not png_texts and not extracted_any:
        warn("No obvious leads. Try manual inspection or different assumptions.")

def main():
    ap = argparse.ArgumentParser(description="CTF Image Stego Analyzer (Windows-friendly, no WSL)")
    ap.add_argument("input", help="Path to the input image file")
    ap.add_argument("--out", help="Output directory (default: out_<basename>)")
    ap.add_argument("--max-bytes", type=int, default=20_000_000, help="Safety cap for file size (bytes)")
    ap.add_argument("--no-numpy", action="store_true", help="Force pure-Python paths (slower)")
    args = ap.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"Input not found: {input_path}")
        sys.exit(1)

    outdir = Path(args.out) if args.out else input_path.parent / f"out_{input_path.stem}"
    analyze(input_path, outdir, args.max_bytes, args.no_numpy)

if __name__ == "__main__":
    main()