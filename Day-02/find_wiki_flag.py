#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_wiki_flag.py

Hunt for hidden CTF flags on a Wikipedia page:
 - Fixes 403 by sending a descriptive UA and using API fallbacks
 - Scans rendered HTML (including HTML comments)
 - Scans raw wikitext (action=raw) for hidden <!-- ... -->, encodings, etc.
 - Scans the last N revisions via the MediaWiki Action API
 - Optionally scans File pages for images used by the page
 - Tries common decoders (base64, gzip+base64, hex, url, rot13, reverse, xor-1byte)

Usage:
  python find_wiki_flag.py "https://en.wikipedia.org/wiki/Australian_white_ibis" --limit 100 --images
  python find_wiki_flag.py <url> --extra-pattern "IOC\\{[^}]+\\}"
"""

import argparse
import base64
import binascii
import gzip
import os
import re
import sys
import json
from urllib.parse import unquote, urlparse, parse_qs, quote_plus

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup, Comment

# ---------------------- Config & Patterns ----------------------

# Default patterns; add more via --extra-pattern argument
FLAG_PATTERNS = [
    r'flag\{[^}]+\}',
    r'ctf\{[^}]+\}',
    r'flg\{[^}]+\}',
]

# Encoded-looking tokens (heuristics)
B64_RE = re.compile(r'\b(?:[A-Za-z0-9+/]{20,}={0,2})\b')
HEX_RE = re.compile(r'\b(?:[0-9A-Fa-f]{16,})\b')
URL_RE = re.compile(r'(?:%[0-9A-Fa-f]{2}){4,}')

# Contact info for Wikimedia UA policy (URL or email). Prefer URL.
CONTACT = os.getenv("WIKI_CONTACT", "https://github.com/your-org/ctf-tools")

# Build a Wikimedia-friendly User-Agent (see policy)
# https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
USER_AGENT = f"IOC-CTF-Finder/1.2 ({CONTACT}) requests/{requests.__version__}"

# ---------------------- HTTP Session w/ Retries ----------------------

def make_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    })
    retry = Retry(
        total=4,
        backoff_factor=0.6,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET"])
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

SESSION = make_session()

# ---------------------- Utilities ----------------------

def title_from_url(url: str) -> str:
    u = urlparse(url)
    if u.path.startswith('/wiki/'):
        return u.path.split('/wiki/', 1)[1]
    qs = parse_qs(u.query)
    if 'title' in qs:
        return qs['title'][0]
    return u.path.strip('/').replace(' ', '_')

def report(section, items):
    if not items:
        return
    print(f'\n===== {section} =====')
    for it in items:
        # prevent newlines from making output too long
        if isinstance(it, str) and len(it) > 1200:
            print(it[:1200] + '… [truncated]')
        else:
            print(it)

# ---------------------- Fetchers ----------------------

def get_html(url: str) -> str:
    """
    Fetch rendered HTML. If a direct GET hits 403, fallback to the API:
    action=parse, which returns rendered HTML.
    """
    r = SESSION.get(url, timeout=20)
    if r.status_code == 403:
        title = title_from_url(url)
        api = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "parse",
            "format": "json",
            "formatversion": "2",
            "page": title,
            "prop": "text",
            "maxlag": "2",
        }
        rp = SESSION.get(api, params=params, timeout=25)
        rp.raise_for_status()
        data = rp.json()
        html = data.get("parse", {}).get("text", "")
        if not html:
            r.raise_for_status()
        return html
    r.raise_for_status()
    return r.text

def get_raw_wikitext(title: str) -> str:
    """
    Fetch raw wikitext via action=raw (official, documented method).
    """
    raw_url = f"https://en.wikipedia.org/w/index.php?title={quote_plus(title)}&action=raw"
    r = SESSION.get(raw_url, timeout=20)
    r.raise_for_status()
    return r.text

def get_revisions(title: str, limit: int = 50):
    """
    Fetch recent revisions (with content) via the MediaWiki Action API.
    Now returns 'revid' too, so we can print direct links to the hit.
    """
    api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvslots": "main",
        # ⬇️ Added 'ids' so we get the revision ID (revid)
        "rvprop": "ids|timestamp|user|comment|content",
        "rvlimit": str(limit),
        "format": "json",
        "formatversion": "2",
        "maxlag": "2",
    }
    r = SESSION.get(api, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    pages = data.get('query', {}).get('pages', [])
    if not pages:
        return []
    revs = pages[0].get('revisions', []) or []
    results = []
    for rev in revs:
        content = ""
        try:
            content = rev['slots']['main']['content']
        except Exception:
            pass
        results.append({
            # ⬇️ Keep these…
            "timestamp": rev.get("timestamp"),
            "user": rev.get("user"),
            "comment": rev.get("comment"),
            "content": content or "",
            # ⬇️ …and add this
            "revid": rev.get("revid"),
        })
    return results

def get_images(title: str, max_pages: int = 500):
    """
    List image (File:...) titles used by the page (enwiki).
    We'll then fetch each File page's wikitext via action=raw.
    """
    api = "https://en.wikipedia.org/w/api.php"
    images = []
    cont = {}
    while True:
        params = {
            "action": "query",
            "prop": "images",
            "titles": title,
            "imlimit": "max",
            "format": "json",
            "formatversion": "2",
            **cont
        }
        r = SESSION.get(api, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            break
        page = pages[0]
        ims = page.get("images", []) or []
        for im in ims:
            t = im.get("title")
            if t and t not in images:
                images.append(t)
                if len(images) >= max_pages:
                    return images
        cont = data.get("continue", {})
        if not cont:
            break
    return images

def get_file_wikitext(file_title: str) -> str:
    """
    Fetch File page wikitext (might redirect to Commons; still worth scanning).
    """
    raw_url = f"https://en.wikipedia.org/w/index.php?title={quote_plus(file_title)}&action=raw"
    r = SESSION.get(raw_url, timeout=20)
    if r.status_code == 404:
        return ""
    r.raise_for_status()
    return r.text

# ---------------------- Extractors & Decoders ----------------------

def scan_html_comments(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    return [str(c) for c in comments]

def find_candidates(text: str, flag_regex: re.Pattern):
    found = set()
    for m in flag_regex.finditer(text):
        found.add(m.group(0))
    for m in B64_RE.finditer(text):
        found.add(m.group(0))
    for m in HEX_RE.finditer(text):
        found.add(m.group(0))
    for m in URL_RE.finditer(text):
        found.add(m.group(0))
    return list(found)

def try_decode_all(s: str):
    """
    Try multiple decoders; return list of (decoder_name, decoded_text).
    """
    out = []
    def add(name, val):
        if val and isinstance(val, str) and val.strip():
            out.append((name, val))

    # URL decode
    if '%' in s or URL_RE.search(s):
        try:
            add('urldecode', unquote(s))
        except Exception:
            pass

    # Base64 (and gzip+base64)
    if re.fullmatch(r'[A-Za-z0-9+/=]+', s) or B64_RE.search(s):
        # Try with padding adjustments
        for pad in ['', '=', '==']:
            t = s + (pad if len(s) % 4 else '')
            try:
                b = base64.b64decode(t, validate=False)
                try:
                    add('base64', b.decode('utf-8', errors='ignore'))
                except Exception:
                    pass
                try:
                    gz = gzip.decompress(b).decode('utf-8', errors='ignore')
                    add('gzip+base64', gz)
                except Exception:
                    pass
            except Exception:
                pass

    # Hex
    if HEX_RE.search(s):
        try:
            b = binascii.unhexlify(re.sub(r'\s+', '', s))
            add('hex', b.decode('utf-8', errors='ignore'))
        except Exception:
            pass

    # ROT13
    def rot13(t):
        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        b = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        return t.translate(str.maketrans(a, b))
    add('rot13', rot13(s))

    # Reverse
    add('reverse', s[::-1])

    # Single-byte XOR heuristic (looks for 'flag{' or 'ctf{')
    try:
        bs = s.encode('latin-1', errors='ignore')
        for key in range(1, 256):
            dec = bytes([b ^ key for b in bs]).decode('utf-8', errors='ignore')
            low = dec.lower()
            if 'flag{' in low or 'ctf{' in low:
                add(f'xor-0x{key:02x}', dec)
    except Exception:
        pass

    return out

def show_revision_hits(title: str, revisions: list, flag_regex: re.Pattern):
    """
    Scan revisions one-by-one for the flag. When found, print:
      • revid, timestamp, user
      • direct 'oldid' link to the full revision
      • 'diff=prev' link to highlight what changed
      • a short context snippet around the first match
    """
    hits = 0
    for rev in revisions:
        txt = rev.get("content", "") or ""
        m = flag_regex.search(txt)
        if not m:
            continue

        hits += 1
        start = max(0, m.start() - 60)
        end = min(len(txt), m.end() + 60)
        snippet = (txt[start:end]).replace("\n", " ")
        revid = rev.get("revid")
        ts = rev.get("timestamp")
        user = rev.get("user") or "(unknown)"

        # Direct links
        oldid_url = f"https://en.wikipedia.org/w/index.php?title={quote_plus(title)}&oldid={revid}"
        diff_prev_url = f"https://en.wikipedia.org/w/index.php?title={quote_plus(title)}&diff=prev&oldid={revid}"

        print("\n===== FLAG FOUND IN REVISION =====")
        print(f"oldid:     {revid}")
        print(f"timestamp: {ts}")
        print(f"user:      {user}")
        print(f"revision:  {oldid_url}")
        print(f"diff prev: {diff_prev_url}")
        print(f"snippet:   …{snippet}…")

    if hits == 0:
        print("\n[info] No individual revision contained a direct flag match using the current patterns.")

# ---------------------- Main Flow ----------------------

def main():
    ap = argparse.ArgumentParser(description="Find hidden flags in a Wikipedia page.")
    ap.add_argument("url", help="Wikipedia page URL")
    ap.add_argument("--limit", type=int, default=50, help="Revisions to scan (default: 50)")
    ap.add_argument("--images", action="store_true", help="Also scan File pages for images used by the page")
    ap.add_argument("--extra-pattern", action="append", default=[], help="Add custom regex for flags (e.g., IOC\\{[^}]+\\})")
    args = ap.parse_args()

    # Compile flag regex
    pats = FLAG_PATTERNS + args.extra_pattern
    flag_regex = re.compile("|".join(pats), re.IGNORECASE)

    # Resolve title
    title = title_from_url(args.url)
    print(f"[+] Title: {title}")
    print("[+] Fetching HTML…")
    html = get_html(args.url)

    print("[+] Extracting HTML comments…")
    html_comments = scan_html_comments(html)
    report("HTML comments", html_comments[:10])  # only preview

    print("[+] Fetching raw wikitext…")
    wikitext = get_raw_wikitext(title)
    report("Raw wikitext (first 400 chars)", [wikitext[:400] + ('…' if len(wikitext) > 400 else '')])

    wt_comments = re.findall(r'<!--(.*?)-->', wikitext, flags=re.DOTALL)
    report("Wikitext comments", wt_comments)

    print(f"[+] Fetching last {args.limit} revisions via API…")
    revisions = get_revisions(title, args.limit)
    print(f"[+] Got {len(revisions)} revisions")
    # Print exactly which revision(s) contain a flag
    show_revision_hits(title, revisions, flag_regex)

    any_hits = False
    datasets = [
        ('HTML comments', '\n'.join(html_comments)),
        ('Raw wikitext', wikitext),
        ('Wikitext comments', '\n'.join(wt_comments)),
        ('Revisions content', '\n'.join([r.get('content','') for r in revisions])),
    ]

    # Optional: image File pages
    file_pages = []
    if args.images:
        print("[+] Listing images used by the page…")
        file_titles = get_images(title)
        print(f"[+] Found {len(file_titles)} File pages; fetching wikitext for each…")
        for ft in file_titles:
            try:
                wt = get_file_wikitext(ft)
                if wt:
                    file_pages.append((ft, wt))
            except Exception as e:
                print(f"[warn] Failed to fetch {ft}: {e}")
        datasets.append(('Image File pages (wikitext)', '\n'.join([wt for _, wt in file_pages])))

    # Search + decode
    FLAG_REGEX = flag_regex
    for label, text in datasets:
        cands = find_candidates(text, FLAG_REGEX)
        if cands:
            any_hits = True
            print(f'\n### Candidates in {label} ({len(cands)})')
            printed = set()
            for c in sorted(set(cands)):
                if c in printed:
                    continue
                printed.add(c)
                print(f'- {c}')
                for name, decoded in try_decode_all(c):
                    # Show decodes that actually reveal a flag pattern
                    if FLAG_REGEX.search(decoded):
                        print(f'    -> [{name}] {decoded}')

    if not any_hits:
        print("\n[!] No obvious candidates found.")
        print("    Tips:")
        print("      • Increase --limit (e.g., --limit 200) to scan more revisions;")
        print("      • Add --images to scan image File pages;")
        print("      • Add custom formats with --extra-pattern 'IOC\\{[^}]+' ;")
        print("      • Manually check View History for brief edits around the CTF window.")

if __name__ == '__main__':
    try:
        main()
    except requests.HTTPError as e:
        print(f"[HTTPError] {e}")
        sys.exit(2)
    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)