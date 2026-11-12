"""W3-START2 citation check (mechanical part). Adapted from Theory_work/Wave3/W3-START/citecheck.py.

For every backticked `path:line[-line]` in STATEMENT.md, REPORT.md and lemmas/*.md: confirm that the file EXISTS and
the range is IN-RANGE, and print a resolved excerpt (first and last cited line) with a short SHA-256 of the cited
block, so that the claim can be compared by eye. It does NOT check semantics. Backticked paths without a line number
are checked for existence only. Output: reviews/CITECHECK.txt.

Conventions of this ticket (the word just before the backtick selects the base folder):
  BASE = Theory_work/Wave3/W3-START/   (the frozen base ticket; every citation of a base file carries this word)
  CORE = Scripts/SMC_BVS/core/   RM = Theory_work/Wave3/W3-RM/   SAMP = Theory_work/Wave3/W3-SAMP/
  PXN  = Theory_work/Wave1/W1-PXN/
A path without such a word is this ticket's (or repo-relative). A short citation `:a[-b]` (no path) continues the
file cited last before it in the same document; it is resolved to that file and checked in the same way.
Usage: python citecheck.py [OUTPUT_FILE]
"""
import re, os, glob, io, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASES = {"BASE": "Theory_work/Wave3/W3-START", "CORE": "Scripts/SMC_BVS/core", "RM": "Theory_work/Wave3/W3-RM",
         "SAMP": "Theory_work/Wave3/W3-SAMP", "PXN": "Theory_work/Wave1/W1-PXN"}
pat = re.compile(r"(?:(\b[A-Z0-9]{2,5})\s+)?`([A-Za-z0-9_./\-]+\.(?:h|cpp|R|md|tex|py|txt|tsv))(?::(\d+)(?:-(\d+))?)?`")
short = re.compile(r"`:(\d+)(?:-(\d+))?`")
both = re.compile(pat.pattern + r"|" + short.pattern)
files = [os.path.join(HERE, f) for f in ("STATEMENT.md", "REPORT.md") if os.path.isfile(os.path.join(HERE, f))]
files += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))


def resolve(abbr, p):
    if abbr in BASES:                                   # a named base resolves in that base only
        cands = [os.path.join(ROOT, BASES[abbr], p)]
    else:
        cands = [os.path.join(HERE, p), os.path.join(ROOT, p)]
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


out = io.StringIO(); bad = 0; n = 0; nolines = 0
for f in files:
    txt = io.open(f, encoding="utf-8").read(); tag = os.path.relpath(f, HERE).replace("\\", "/")
    prev = None
    for m in both.finditer(txt):
        abbr, p, a, b = m.group(1), m.group(2), m.group(3), m.group(4)
        if p is None:                                   # short citation `:a-b`: continue the file cited last
            n += 1
            if prev is None:
                bad += 1; out.write("MISSING          [%s] :%s (no file cited before it)\n" % (tag, m.group(5))); continue
            abbr, p, a, b = prev[0], prev[1], m.group(5), m.group(6); n -= 1
        # a bare ticket-relative name preceded by an unrelated capitalised word: only the listed abbreviations count
        if abbr not in BASES:
            abbr = None
        prev = (abbr, p)
        r = resolve(abbr, p); n += 1
        cite = (abbr + " " if abbr else "") + p + ((":" + a + ("-" + b if b else "")) if a else "")
        if r is None:
            bad += 1; out.write("MISSING          [%s] %s\n" % (tag, cite)); continue
        rel = os.path.relpath(r, ROOT).replace("\\", "/")
        if a is None:
            nolines += 1; out.write("EXISTS           [%s] %s -> %s\n" % (tag, cite, rel)); continue
        lines = io.open(r, encoding="utf-8", errors="replace").read().split("\n")
        a_i, b_i = int(a), int(b or a)
        if a_i < 1 or b_i > len(lines) or b_i < a_i:
            bad += 1; out.write("OUT-OF-RANGE     [%s] %s -> %s (%d lines)\n" % (tag, cite, rel, len(lines))); continue
        block = "\n".join(lines[a_i - 1:b_i]); h = hashlib.sha256(block.encode("utf-8")).hexdigest()[:12]
        first = lines[a_i - 1].strip()[:90]; last = lines[b_i - 1].strip()[:90]
        out.write("OK %s [%s] %s -> %s\n      first: %s\n      last:  %s\n" % (h, tag, cite, rel, first, last))
head = "W3-START2 CITECHECK: %d citations (%d with line ranges, %d path-only); MISSING/OUT-OF-RANGE: %d\n" % (n, n - nolines, nolines, bad)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "reviews", "CITECHECK.txt")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(head + out.getvalue())
print(head.strip())
