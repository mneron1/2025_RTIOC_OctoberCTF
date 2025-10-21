# OCTOBER CTF - DAY 02
Challenge is :
	A colleague mentioned they saw something out of place while researching animals on Wikipedia.

	They were looking up information about the Australian white ibis and said

	"I swear someone was messing with that page earlier. You might want to check it out.. it looked like someone was trying to hide something"

	https://en.wikipedia.org/wiki/Australian_white_ibis

	Find the secret flag!

## What the script does (at a glance)

**Goal:** find a hidden flag on a Wikipedia page—even if it was only present briefly and later removed.

**Pipeline (in order):**

1) **Fetch the page safely**  
   - Uses a proper **User‑Agent** (with contact info) and polite retries to avoid 403 blocks, as required by Wikimedia. If a direct HTML GET is blocked, it **falls back to the MediaWiki Action API** (`action=parse`) to get the rendered HTML.  
   *Why:* Wikimedia blocks generic scrapers that don’t identify themselves. The API and UA rules are documented policies. [1](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy)[2](https://www.mediawiki.org/wiki/API:Etiquette)[3](https://stackoverflow.com/questions/79618466/specify-contact-info-in-wikipedia-user-agent-policy)

2) **Pull the raw wikitext** (`action=raw`)  
   - This is the exact source editors see, including **hidden comments** like `<!-- ... -->`.  
   *Why:* `action=raw` is the fastest official way to retrieve the page’s wikitext. [3](https://stackoverflow.com/questions/79618466/specify-contact-info-in-wikipedia-user-agent-policy)

3) **Query recent revisions & their content** (`prop=revisions&rvprop=content`)  
   - Grabs the last *N* page versions to catch flags that were added and then removed quickly.  
   *Why:* The Revisions API is the canonical way to access historical content programmatically. [4](https://blog.finxter.com/solved-python-request-error-403-when-web-scraping/)[5](https://evomi.com/blog/conquer-403-forbidden-python-requests-key-tactics)

4) **Scan for “flaggy” things**  
   - Looks for direct flag patterns like `flag{...}`, plus “suspicious” strings (Base64, hex, URL‑encoding) across:
     - Rendered HTML (and **HTML comments**),
     - **Raw wikitext** (and wikitext comments),
     - **Revision contents**.  
   *Why:* Wikipedia allows invisible comments in source (they’re meant for editors), and CTFs often hide data there or in older revisions. 

5) **Try common decodings automatically**  
   - Base64 (and gzip+Base64), hex, URL‑encoding, ROT13, reversed text, single‑byte XOR probe—then recheck for `flag{…}` (or any custom pattern you pass).

6) **(Optional) Scan image File pages**  
   - Lists images used by the article via the API and pulls each **File page’s** wikitext to check for hidden text or encodings.  
   *Why:* More advanced hides sometimes live in file descriptions; the same API methods apply. [3](https://stackoverflow.com/questions/79618466/specify-contact-info-in-wikipedia-user-agent-policy)

7) **(Patch you added)** Print **which revision** contains the flag  
   - After fetching revisions, it now prints **oldid**, timestamp, user, plus direct links:
     - `&oldid=<ID>` (full revision),
     - `&diff=prev&oldid=<ID>` (highlight only the change).

---

## Why this approach works on Wikipedia

- **User‑Agent + Etiquette:** Wikimedia **requires** a descriptive UA with contact info; non‑descriptive defaults like `python-requests/x` may be blocked (triggering your original 403). You complied by adding a UA and using the API if needed. [1](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy)[2](https://www.mediawiki.org/wiki/API:Etiquette)
- **Official content access:** Using `action=raw` and the Action API (`parse`, `revisions`) is the documented, stable way to fetch wikitext, HTML, and history. [3](https://stackoverflow.com/questions/79618466/specify-contact-info-in-wikipedia-user-agent-policy)[4](https://blog.finxter.com/solved-python-request-error-403-when-web-scraping/)
- **Hidden comments & history:** Wikipedia explicitly supports **hidden text** in source (HTML comments) for editorial guidance, which is invisible on the rendered page. Plus, the **View history** preserves every change, so flags can be planted briefly and still be discoverable via revisions. [6](https://www.mediawiki.org/wiki/API:Etiquette/id)

---

## The idea behind this particular challenge

> Clue: “I swear someone was messing with that page earlier.”

That suggests the flag **wouldn’t be in the live page**, but **in a past revision** or hidden comment. Your run confirms exactly that:

- The script found **`flag{lL0v5_1b15}`** in **“Revisions content”**, not in today’s wikitext.  
- That means someone inserted the flag and later removed it—classic CTF behavior to force competitors to check **revision history**, not just current content.

### How you proved it’s real

- The script’s candidates list showed a **direct match** in “Revisions content.”  
- With the revision‑details patch, you can print the **oldid**, the **timestamp/user**, and click a **diff** link to visually confirm the exact insertion. These steps mirror Wikipedia’s **View history** + diffs workflow, just automated. [6](https://www.mediawiki.org/wiki/API:Etiquette/id)

---

## When you’d use the decoders

In many challenges the flag is **encoded** rather than plain `flag{…}`. Common patterns:

- **Base64 / gzip+Base64**: looks like long A–Z/a–z/0–9 with `=` padding—decode, and if the output’s binary, try gunzip.  
- **Hex / URL‑encoding / ROT13 / reversed**: quick transforms that often reveal `flag{…}`.  
- **XOR‑single‑byte**: if the string looks like noise, brute‑force keys `0x01..0xFF` and search the result for the flag pattern.

Your script does all of these automatically and only shows decodes that actually reveal a flag pattern.

---

## How to verify and write up the solve

1) Re‑run with the **revision patch** to print:
   - `oldid`, timestamp, user  
   - `&oldid=<ID>` link (full revision)  
   - `&diff=prev&oldid=<ID>` link (highlights the insertion)
2) Screenshot or cite the **diff view** showing the flag.
3) Submit the exact string:
   ```
   flag{lL0v5_1b15}
   ```

---

## If you had to generalize this method to other pages

- **Start with source & comments** (`action=raw`, HTML comments).  
- **Always check revisions**—especially if a hint says “earlier” or “someone edited it.” Use the **Revisions API** to scale this up or manually use **View history** tools like WikiBlame. [4](https://blog.finxter.com/solved-python-request-error-403-when-web-scraping/)[6](https://www.mediawiki.org/wiki/API:Etiquette/id)
- **Scan linked assets** (File pages, templates) when nothing is found in the main article.  
- **Respect rate limits & etiquette**; identify your client in the UA and keep requests polite. [2](https://www.mediawiki.org/wiki/API:Etiquette)

---

If you want, I can run through adding a **JSON/CSV export** of the revision hits for your CTF write‑up, or tune the regex to catch a custom format like `IOC{…}` specific to your org.

---

Generated with OpenAI ChatGPT
