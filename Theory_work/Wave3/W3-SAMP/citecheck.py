"""W3-SAMP citation check (mechanical part; revised after SW1 #23).

For every backticked `path:line[-line]` in STATEMENT.md and lemmas/*.md: confirm the file EXISTS and the range is
IN-RANGE, and print a resolved excerpt (first and last cited line) with a short SHA-256 of the cited block, so that the
claim can be compared by eye. It does NOT check semantics. Output: reviews/CITECHECK.txt.
Usage (from the ticket folder): py -3.13 citecheck.py
"""
import re, os, glob, io, hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CORE = os.path.join(ROOT, "Scripts", "SMC_BVS", "core")
HERE = os.path.dirname(os.path.abspath(__file__))
T12 = os.path.join(ROOT, "Docs", "Theory", "proofs", "T12_T8_frozen_run_identities")
N1L = os.path.join(ROOT, "Theory_work", "Wave1", "W1-N1", "lemmas")
pat = re.compile(r"`([A-Za-z0-9_./\-]+\.(?:h|cpp|R|md|tex|py)):(\d+)(?:-(\d+))?")
files = [os.path.join(HERE, "STATEMENT.md")] + sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))


def resolve(p, src):
    cands = []
    if p in ("STATEMENT.md", "PROOF_v6.tex"):  # bare: always T12's files in this ticket's proofs
        cands.append(os.path.join(T12, p))
    cands += [os.path.join(ROOT, p), os.path.join(CORE, p), os.path.join(HERE, p), os.path.join(os.path.dirname(src), p)]
    if p.startswith("W1-N1/"): cands.append(os.path.join(ROOT, "Theory_work", "Wave1", p))
    if p.startswith("Wave"): cands.append(os.path.join(ROOT, "Theory_work", p))
    if p in ("L1_bridge.md", "L3_freezing.md", "L2_post_terminal.md"): cands.append(os.path.join(N1L, p))
    for c in cands:
        if os.path.isfile(c): return c
    return None


out = io.StringIO(); bad = 0; n = 0
for f in files:
    txt = open(f, encoding="utf-8").read()
    for m in pat.finditer(txt):
        n += 1
        p, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        r = resolve(p, f); tag = os.path.relpath(f, HERE)
        if r is None:
            bad += 1; out.write(f"MISSING          [{tag}] {p}:{a}-{b}\n"); continue
        lines = open(r, encoding="utf-8", errors="replace").read().split("\n")
        if b > len(lines) or a < 1 or b < a:
            bad += 1; out.write(f"OUT-OF-RANGE     [{tag}] {p}:{a}-{b} (file has {len(lines)} lines)\n"); continue
        blk = "\n".join(lines[a - 1:b]); hsh = hashlib.sha256(blk.encode()).hexdigest()[:10]
        first = lines[a - 1].strip()[:100]; last = lines[b - 1].strip()[:70]
        out.write(f"EXISTS/IN-RANGE  [{tag}] {p}:{a}-{b} sha={hsh} | {first}" + (f"  ...  {last}" if b > a else "") + "\n")
out.write(
    f"\n{n} backticked citations: {n - bad} EXISTS/IN-RANGE, {bad} missing/out-of-range. Resolution order: bare\n"
    "STATEMENT.md / PROOF_v6.tex -> T12; repo root; Scripts/SMC_BVS/core/; ticket folder.\n"
    "NOT machine-checked (disclosed, SW1 #23): bare continuation references (':NNN' after a path), comma-separated line\n"
    "lists, paths broken across lines, unnumbered file references. These, and the SEMANTIC match of every excerpt to its\n"
    "claim, were checked by hand by the lead (2026-11-09, after SW1) and spot-checked independently by SL1, LC1, LC2, SW1.\n")
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue()[-700:])
