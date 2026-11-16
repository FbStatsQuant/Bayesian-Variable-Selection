#!/usr/bin/env python3
"""Item 7: extract every file:line / file:line-line pin in STATEMENT.md and check that the file exists and the lines exist.
Pin forms handled: `path/file.ext:142`, `path:43-56, 78` (extra list items), and BARE pins `:159-162` (they inherit the last full file pin
earlier in the text; this is how STATEMENT §2 writes them).  A relative path is tried (i) from the repo root, (ii) from the directory of the
last full pin (STATEMENT §2 writes `cpp/v3_core.cpp` for Scripts/SMC_BVS/core/cpp/v3_core.cpp).  Working-tree files are checked; commit scope
(4676af6 / fe9a1d7) is NOT checked (no git command is run).
usage: python3 -B citecheck.py > out/citecheck_out.txt        DRAFT (by this seat, unchecked)"""
import re, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
STATEMENT = os.path.abspath(os.path.join(HERE, "..", "..", "STATEMENT.md"))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))   # repo root
FILE = r"[A-Za-z0-9_][A-Za-z0-9_./\-]*\.[A-Za-z0-9]{1,5}"
RANGE = r"\d+(?:-\d+)?"
PIN = re.compile(rf"(?P<file>{FILE}):(?P<ranges>{RANGE}(?:\s*,\s*{RANGE})*)|(?<![A-Za-z0-9_./\-])(?P<bare>:{RANGE}(?:\s*,\s*{RANGE})*)")
lines = open(STATEMENT, encoding="utf-8").read().split("\n")
rows = []; last = None; lastdir = None
for ln, text in enumerate(lines, 1):
    for m in PIN.finditer(text):
        if m.group("file"):
            f, rg = m.group("file"), m.group("ranges"); last = f; inh = ""
        else:
            if last is None: continue
            f, rg = last, m.group("bare")[1:]; inh = " (inherits file)"
        for part in re.split(r"\s*,\s*", rg):
            a, b = (part.split("-") + [None])[:2]
            a = int(a); b = int(b) if b else a
            rows.append((ln, f, a, b, inh, m.group(0)))
def resolve(f, ctxdir):
    cands = [os.path.join(ROOT, f)]
    if ctxdir: cands.append(os.path.join(ROOT, ctxdir, f))
    for c in cands:
        if os.path.isfile(c): return c
    return None
cache = {}; out = []; miss = 0; ctxdir = None
print(f"STATEMENT: {os.path.relpath(STATEMENT, ROOT)}   repo root: {ROOT}\n")
print("| STATEMENT line | pin as written | resolved file | file lines | cited lines | status | text of first cited line |")
print("|---|---|---|---|---|---|---|")
for (ln, f, a, b, inh, raw) in rows:
    path = resolve(f, ctxdir)
    if path is None:
        status, nl, txt = "MISS (file not found)", "-", ""
        rel = f
    else:
        rel = os.path.relpath(path, ROOT)
        if "/" in f and os.path.dirname(f) and (f == rel): ctxdir = os.path.dirname(rel)    # full path from root => context for later relative pins
        if path not in cache: cache[path] = open(path, encoding="utf-8", errors="replace").read().split("\n")
        L = cache[path]
        if L and L[-1] == "": L = L[:-1]
        nl = len(L)
        if a >= 1 and b <= nl and a <= b: status, txt = "OK", L[a - 1].strip()[:70].replace("|", "/")
        else: status, txt = "MISS (line out of range)", ""
    if status.startswith("MISS"): miss += 1
    print(f"| {ln} | `{raw}`{inh} -> {f}:{a}" + (f"-{b}" if b != a else "") + f" | {rel} | {nl} | {a}-{b} | {status} | {txt} |")
print(f"\nTotal pins (each range/list item counted once): {len(rows)};  OK: {len(rows)-miss};  MISS: {miss}")

# ---- semantic spot check (identifiers named next to the pins in STATEMENT §2 appear on the cited lines) ----
sem = [("Scripts/SMC_BVS/core/v3_run.R", 142, "hpm"), ("Scripts/SMC_BVS/core/v3_run.R", 160, "pip_r"), ("Scripts/SMC_BVS/core/v3_run.R", 162, "pip_primary"),
       ("Scripts/SMC_BVS/core/v3_run.R", 163, "mpm"), ("Scripts/SMC_BVS/core/v3_run.R", 154, "log_Z"), ("Scripts/SMC_BVS/core/v3_run.R", 210, "top_store"),
       ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", 358, "store_to_list"), ("Scripts/SMC_BVS/core/cpp/v3_ledger.h", 43, "TopStore"),
       ("Scripts/SMC_BVS/core/cpp/v3_ledger.h", 78, "40 * p + 1"), ("Scripts/SMC_BVS/core/cpp/v3_ledger.h", 49, "offer")]
print("\nSemantic spot check (identifier named in STATEMENT occurs on the cited line):")
bad = 0
for f, l, key in sem:
    L = open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read().split("\n")
    ok = key in L[l - 1]; bad += (not ok)
    print(f"  {f}:{l}  contains `{key}`: {ok}")
print(f"  semantic mismatches: {bad}")
