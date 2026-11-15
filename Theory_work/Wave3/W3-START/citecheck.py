"""W3-START citation check (mechanical part).

For every backticked `path:line[-line]` in STATEMENT.md, REPORT.md and lemmas/*.md: confirm that the file EXISTS and
the range is IN-RANGE, and print a resolved excerpt (first and last cited line) with a short SHA-256 of the cited
block, so that the claim can be compared by eye. It does NOT check semantics. Backticked paths without a line number
are checked for existence only. Output: reviews/CITECHECK.txt.

Abbreviations of STATEMENT.md (the word just before the backtick selects the base folder):
  CORE = Scripts/SMC_BVS/core/        GROW = Theory_work/Wave1C/C-GROW/     RM  = Theory_work/Wave3/W3-RM/
  SAMP = Theory_work/Wave3/W3-SAMP/   MIS  = Theory_work/Wave1C/C-MIS/      PXN = Theory_work/Wave1/W1-PXN/
  GEN  = Theory_work/Wave1/W1-GEN/
A bare `cpp/...` or `v3_*.R` path is CORE; a bare `lemmas/...`, `numerics/...`, `reviews/...`, `STATEMENT.md`,
`BRIEF.md`, `PLAN.md`, `ASSUMPTION_MAP.md`, `REPORT.md` is this ticket's.
Usage: python citecheck.py [OUTPUT_FILE]
The default output is reviews/CITECHECK.txt in the ticket folder; give another path (for example a file in a
temporary directory) to run the check without writing into the repository.
"""
import re, os, glob, io, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASES = {"CORE": "Scripts/SMC_BVS/core", "GROW": "Theory_work/Wave1C/C-GROW", "RM": "Theory_work/Wave3/W3-RM",
         "SAMP": "Theory_work/Wave3/W3-SAMP", "MIS": "Theory_work/Wave1C/C-MIS", "PXN": "Theory_work/Wave1/W1-PXN",
         "GEN": "Theory_work/Wave1/W1-GEN"}
pat = re.compile(r"(?:(\b[A-Z0-9]{2,5})\s+)?`([A-Za-z0-9_./\-]+\.(?:h|cpp|R|md|tex|py|txt|tsv))(?::(\d+)(?:-(\d+))?)?`")
files = [os.path.join(HERE, f) for f in ("STATEMENT.md", "REPORT.md") if os.path.isfile(os.path.join(HERE, f))]
files += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))


def resolve(abbr, p):
    cands = []
    if abbr in BASES:
        cands.append(os.path.join(ROOT, BASES[abbr], p))
    if p.startswith("cpp/") or p.startswith("v3_"):
        cands.append(os.path.join(ROOT, BASES["CORE"], p))
    cands += [os.path.join(ROOT, p), os.path.join(HERE, p)]
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


out = io.StringIO(); bad = 0; n = 0; nolines = 0
for f in files:
    txt = io.open(f, encoding="utf-8").read(); tag = os.path.relpath(f, HERE).replace("\\", "/")
    for m in pat.finditer(txt):
        abbr, p, a, b = m.group(1), m.group(2), m.group(3), m.group(4)
        # a bare ticket-relative name preceded by an unrelated capitalised word: only the listed abbreviations count
        if abbr not in BASES:
            abbr = None
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
head = "W3-START CITECHECK: %d citations (%d with line ranges, %d path-only); MISSING/OUT-OF-RANGE: %d\n" % (n, n - nolines, nolines, bad)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "reviews", "CITECHECK.txt")
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(head + out.getvalue())
print(head.strip())
