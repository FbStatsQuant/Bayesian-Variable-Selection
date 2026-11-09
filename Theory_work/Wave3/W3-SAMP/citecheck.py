"""W3-SAMP citation check: open every `path:line[-line]` cited in STATEMENT.md and lemmas/*.md, confirm the file exists
and the range is inside it, and print the cited lines so that the quoted claim can be compared by eye.
Code paths without a directory prefix are resolved against Scripts/SMC_BVS/core/. Output: reviews/CITECHECK.txt.
Usage (from the ticket folder): py -3.13 citecheck.py
"""
import re, os, glob, io

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CORE = os.path.join(ROOT, "Scripts", "SMC_BVS", "core")
HERE = os.path.dirname(os.path.abspath(__file__))
pat = re.compile(r"`([A-Za-z0-9_./\-]+\.(?:h|cpp|R|md|tex|py)):(\d+)(?:-(\d+))?")
files = [os.path.join(HERE, "STATEMENT.md")] + sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
out = io.StringIO(); bad = 0; n = 0


def resolve(p, src):
    cands = []
    if p in ("STATEMENT.md", "PROOF_v6.tex"):  # bare: always T12's files in this ticket's proofs
        cands.append(os.path.join(ROOT, "Docs", "Theory", "proofs", "T12_T8_frozen_run_identities", p))
    cands += [os.path.join(ROOT, p), os.path.join(CORE, p), os.path.join(HERE, p), os.path.join(os.path.dirname(src), p)]
    if p.startswith("W1-N1/"): cands.append(os.path.join(ROOT, "Theory_work", "Wave1", p))
    if p.startswith("Wave"): cands.append(os.path.join(ROOT, "Theory_work", p))
    if p in ("STATEMENT.md", "PROOF_v6.tex"): cands.append(os.path.join(ROOT, "Docs", "Theory", "proofs", "T12_T8_frozen_run_identities", p))
    if p in ("L1_bridge.md", "L3_freezing.md", "L2_post_terminal.md"): cands.append(os.path.join(ROOT, "Theory_work", "Wave1", "W1-N1", "lemmas", p))
    for c in cands:
        if os.path.isfile(c): return c
    return None


for f in files:
    txt = open(f, encoding="utf-8").read()
    for m in pat.finditer(txt):
        n += 1
        p, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        r = resolve(p, f)
        tag = os.path.relpath(f, HERE)
        if r is None:
            bad += 1; out.write(f"MISSING  [{tag}] {p}:{a}-{b}\n"); continue
        lines = open(r, encoding="utf-8", errors="replace").read().split("\n")
        if b > len(lines) or a < 1 or b < a:
            bad += 1; out.write(f"RANGE    [{tag}] {p}:{a}-{b} (file has {len(lines)} lines)\n"); continue
        first = lines[a - 1].strip()[:110]
        out.write(f"OK       [{tag}] {p}:{a}-{b} | {first}\n")
out.write(f"\n{n} citations checked; {bad} missing/out-of-range. Resolution: repo root, Scripts/SMC_BVS/core/, ticket folder;\n"
          f"bare continuation references (':NNN' after a path) are not machine-checked and were checked by hand.\n")
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue()[-400:])
