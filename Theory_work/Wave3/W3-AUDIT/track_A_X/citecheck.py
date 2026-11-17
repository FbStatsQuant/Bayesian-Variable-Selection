"""W3-AUDIT track A citation check (mechanical; adapted from W3-SAMP/citecheck.py).

For every backticked citation `path:L[-M][, L[-M]]...` in <item>/STATEMENT.md and <item>/PROOF.md, and every backticked
bare continuation `:L[-M][, ...]` (resolved against the most recent cited path in the same file), confirm that the file
EXISTS and each range is IN-RANGE, and print the first cited line and a short SHA-256 of the block. Semantics are NOT
checked (that is the line checker's job). Output: <item>/CITECHECK.txt.
Usage: python3 citecheck.py T1_GW [T2_BLK ...]
"""
import re, os, sys, io, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CORE = os.path.join(ROOT, "Scripts", "SMC_BVS", "core")
RNG = r"\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*"
full = re.compile(r"`([A-Za-z0-9_./\-]+\.(?:h|cpp|R|md|tex|py|tsv)):(" + RNG + r")")
bare = re.compile(r"`:(" + RNG + r")`")


def resolve(p, item):
    for c in (os.path.join(ROOT, p), os.path.join(CORE, p), os.path.join(ROOT, "Theory_work", p),
              os.path.join(item, p)):
        if os.path.isfile(c):
            return c
    return None


def ranges(s):
    for part in s.split(","):
        part = part.strip()
        a, _, b = part.partition("-")
        yield int(a), int(b or a)


def check(item):
    idir = os.path.join(HERE, item)
    out = io.StringIO(); n = bad = 0
    for fn in ("STATEMENT.md", "PROOF.md"):
        f = os.path.join(idir, fn)
        if not os.path.isfile(f):
            continue
        txt = open(f, encoding="utf-8").read()
        last = None
        events = sorted([(m.start(), "full", m) for m in full.finditer(txt)] +
                        [(m.start(), "bare", m) for m in bare.finditer(txt)], key=lambda x: x[0])
        for _, kind, m in events:
            if kind == "full":
                p, rs = m.group(1), m.group(2); last = p
            else:
                if last is None:
                    continue
                p, rs = last, m.group(1)
            r = resolve(p, idir)
            for a, b in ranges(rs):
                n += 1
                tag = f"{fn}{'(cont)' if kind == 'bare' else ''}"
                if r is None:
                    bad += 1; out.write(f"MISSING       [{tag}] {p}:{a}-{b}\n"); continue
                lines = open(r, encoding="utf-8", errors="replace").read().split("\n")
                if b > len(lines) or a < 1 or b < a:
                    bad += 1; out.write(f"OUT-OF-RANGE  [{tag}] {p}:{a}-{b} (file has {len(lines)} lines)\n"); continue
                blk = "\n".join(lines[a - 1:b]); h = hashlib.sha256(blk.encode()).hexdigest()[:10]
                out.write(f"OK            [{tag}] {p}:{a}-{b} sha={h} | {lines[a - 1].strip()[:110]}\n")
    out.write(f"\n{n} citations: {n - bad} OK, {bad} missing/out-of-range. Resolution: repo root, Scripts/SMC_BVS/core/, "
              "Theory_work/, item folder. Bare `:L` resolves to the last full path cited before it in the same file.\n"
              "Not machine-checked: unbackticked references and the semantic match of each excerpt.\n")
    open(os.path.join(idir, "CITECHECK.txt"), "w", encoding="utf-8").write(out.getvalue())
    return n, bad


if __name__ == "__main__":
    for it in sys.argv[1:]:
        n, bad = check(it)
        print(f"{it}: {n} citations, {bad} bad")
