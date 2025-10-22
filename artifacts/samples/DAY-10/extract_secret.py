#!/usr/bin/env python3
import sys, re

def extract_from_file(path):
    b = open(path, 'rb').read()             # read raw bytes
    # Search for the comment block in bytes
    m = re.search(b'super secret txt\\s*=\\s*`([\\s\\S]*?)`', b, flags=re.IGNORECASE)
    if not m:
        print("Couldn't find the backtick block in file.")
        return None
    block_bytes = m.group(1)                # bytes exactly as in file (no decoding)
    return block_bytes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_secret.py path/to/index.html")
        sys.exit(1)
    path = sys.argv[1]
    bs = extract_from_file(path)
    if bs is None:
        sys.exit(1)
    # Show python repr (escaped) and hex bytes
    # decode with latin-1 so bytes map 1:1 to characters
    s = bs.decode('latin-1')
    print("repr:", repr(s))
    print("escaped (useable):", s.encode('unicode_escape').decode('ascii'))
    print("hex:", ' '.join(f"{b:02x}" for b in bs))
