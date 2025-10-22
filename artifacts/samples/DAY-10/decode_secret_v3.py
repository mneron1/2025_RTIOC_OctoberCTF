#!/usr/bin/env python3

def cheat_decode_final(encoded: str, key_char: str) -> str:
    """
    XOR every even index (0, 2, 4, ...) with ord(key_char).
    This matches JS xorEncode() when pass="5".
    """
    key = ord(key_char)
    chars = []
    for i, ch in enumerate(encoded):
        if i % 2 == 0:  # XOR even indices
            chars.append(chr(ord(ch) ^ key))
        else:
            chars.append(ch)
    return ''.join(chars)

def cleaned(s: str) -> str:
    return ''.join(c for c in s if 32 <= ord(c) < 127)

def main():
    # The original raw string from index.html (with control bytes)
    encoded = r"SlTgNcZnFoYe\x1blZg\x1d\"]eYlZ BoGlQ\"\x1c}"
    # Convert escaped hex codes to real control characters
    encoded = encoded.encode("utf-8").decode("unicode_escape")

    decoded = cheat_decode_final(encoded, "5")  # literal '5', not 5
    print(cleaned(decoded))

if __name__ == "__main__":
    main()
