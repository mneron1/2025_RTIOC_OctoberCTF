#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Braille ASCII → Text (and Unicode braille) Decoder
--------------------------------------------------
- Decodes North American Braille ASCII (aka SimBraille) into readable text.
- Handles number sign '#' (A–J -> 1–0) and capitalization via ',' and ',,'.
- Can optionally render Unicode braille cells (⠁⠃⠉ …) for visualization.
- Optional leetspeak transform on the decoded plaintext.

Usage examples:
  1) Decode from a file to plain text:
     python braille_ascii_decoder.py -i message.txt

  2) Decode from stdin:
     echo ",H,ELLO #ABJ" | python braille_ascii_decoder.py

  3) Show as Unicode braille instead of decoding to text:
     python braille_ascii_decoder.py -i message.txt --render

  4) Decode to text and apply leetspeak:
     python braille_ascii_decoder.py -i message.txt --leet
"""

import sys
import argparse

# --- Optional: mapping for leetspeak post-processing ---
LEET_MAP = {
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7'
}

def apply_leet(s: str) -> str:
    return ''.join(LEET_MAP.get(ch, ch) for ch in s)

# --- Unicode braille rendering support (optional) ---
# Order of ASCII characters for the 64 six-dot braille cells (space 0x20 .. '_' 0x5F)
# arranged by increasing dot pattern; this is a standard reference ordering
# commonly used by embossers and simulators.
# (This lets us map an ASCII BRAILLE char -> Unicode cell: U+2800 + index)
ASCII_BRF_ORDER = (
    " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
).strip()

# Build a dict for ASCII->Unicode braille cell mapping
BRF_TO_UNICODE = {
    ch: chr(0x2800 + idx) for idx, ch in enumerate(ASCII_BRF_ORDER)
}

def ascii_to_unicode_braille(s: str) -> str:
    """Render Braille ASCII to Unicode braille cells (visualization)."""
    out = []
    for ch in s:
        if ch in BRF_TO_UNICODE:
            out.append(BRF_TO_UNICODE[ch])
        else:
            # For characters outside 0x20..0x5F, keep as-is (newline, etc.)
            out.append(ch)
    return ''.join(out)

# --- Core decoder: Braille ASCII -> “plain text” ---
# Strategy:
# - Letters A–Z represent letters (lowercase by default in print). We output lower or upper
#   depending on capitalization state.
# - '#' enters numeric mode: A..J (or a..j) map to 1..0 until a space or a non A..J letter.
# - ',' (dot-6) capital sign for next letter; ',,' (double cap) capitalizes the next whole word.
# - Punctuation and other symbols are passed through unchanged.
#
# This is intentionally simple and robust for typical CTF flags.

def decode_braille_ascii_to_text(s: str) -> str:
    out = []
    numeric_mode = False
    caps_next = False
    caps_word = False

    i = 0
    n = len(s)
    while i < n:
        ch = s[i]

        # Newline / whitespace resets modes appropriately
        if ch.isspace():
            out.append(ch)
            numeric_mode = False
            caps_next = False
            caps_word = False
            i += 1
            continue

        # Number sign: enter numeric mode
        if ch == '#':
            numeric_mode = True
            i += 1
            continue

        # Capitalization sign(s): ',' -> next letter caps; ',,' -> next word caps
        if ch == ',':
            # Lookahead for double-cap
            if i + 1 < n and s[i + 1] == ',':
                caps_word = True
                i += 2
            else:
                caps_next = True
                i += 1
            # Do not emit anything for the capital sign itself
            continue

        # Letters
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            letter = ch

            # Numeric mode: A..J -> 1..0
            if numeric_mode:
                upper = letter.upper()
                idx = ord(upper) - ord('A')
                if 0 <= idx <= 9:
                    out.append("1234567890"[idx])
                    i += 1
                    # Stay numeric until space or a non-digit letter shows up
                    continue
                else:
                    # Non A..J letter ends numeric mode; fall through as letter
                    numeric_mode = False

            # Apply capitalization (comma indicators)
            if caps_next or caps_word:
                letter = letter.upper()
                # Single caps_next applies to just this letter
                if caps_next:
                    caps_next = False
            else:
                letter = letter.lower()

            out.append(letter)
            i += 1
            continue

        # Everything else (punctuation, symbols): pass through; end numeric mode
        out.append(ch)
        numeric_mode = False
        caps_next = False
        i += 1

    return ''.join(out)

# --- CLI wiring ---

def main():
    ap = argparse.ArgumentParser(
        description="Decode Braille ASCII (SimBraille) to text, or render as Unicode braille."
    )
    ap.add_argument("-i", "--input", type=str, default="-",
                    help="Input file (default: stdin).")
    ap.add_argument("--render", action="store_true",
                    help="Render as Unicode braille cells (⠁⠃⠉ …) instead of decoding to text.")
    ap.add_argument("--leet", action="store_true",
                    help="Apply basic leetspeak to decoded plaintext (A4 E3 I1 O0 S5 T7).")
    args = ap.parse_args()

    # Read input
    if args.input == "-" or args.input is None:
        data = sys.stdin.read()
    else:
        with open(args.input, "r", encoding="utf-8", errors="replace") as f:
            data = f.read()

    if args.render:
        rendered = ascii_to_unicode_braille(data)
        sys.stdout.write(rendered)
        return

    decoded = decode_braille_ascii_to_text(data)
    if args.leet:
        decoded = apply_leet(decoded)

    sys.stdout.write(decoded)

if __name__ == "__main__":
    main()