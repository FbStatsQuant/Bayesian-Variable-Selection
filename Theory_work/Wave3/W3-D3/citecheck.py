"""Citation check for W3-D3 (copied from W3-D2/citecheck.py, aliases/tokens adapted) (PROTOCOL_v4 §3.6). Pattern of W3-MISR-R/citecheck.py; simplified. Does not check mathematics.

(1) Range checks in STATEMENT.md, PROOF.md, REPORT.md, TARGET.md, READER_DELTA.md, API_CARD.md: every
    "[ALIAS] ... `:a-b`" / "[ALIAS] `:a`" (alias resolved from the last [ALIAS] earlier on the same line),
    "`path:a-b`" (path = a repo path, or a ticket-local file) must point to an existing file with 1 <= a <= b <= #lines.
    A bare "`:a-b`" with no alias earlier on its line is reported as UNRESOLVED (counted as a failure).
(2) Token checks: TOKENS (a token that must occur in the cited range).
(3) Status checks: every registry status quoted in STATEMENT §5 occurs verbatim in claims.tsv for that id@version.
Writes reviews/CITECHECK.txt. Run: python3 Theory_work/Wave3/W3-D3/citecheck.py
"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W = "Theory_work/Wave3/"
ALIAS = {
    "W3P": W + "W3-POST/STATEMENT.md", "DIST": W + "W3-DIST/STATEMENT.md", "RV": W + "W3-READER/READER_VERSIONS.md",
    "NOT": W + "W3-READER/NOTATION.md", "R1": W + "W3-READER/lemmas/R1_set_sizes.md",
    "POST": "Theory_work/Wave2/W2-APP/lemmas/L1_POST.md",
}
LOCAL = {"STATEMENT.md", "TARGET.md", "REPORT.md", "READER_DELTA.md", "PLAN.md", "lemmas/B3w.md", "lemmas/ASSEMBLY.md"}
FILES = ["STATEMENT.md", "lemmas/B3w.md", "lemmas/ASSEMBLY.md", "REPORT.md", "TARGET.md", "READER_DELTA.md", "API_CARD.md"]
EB = W + "W3-DIST/work/E_bridges/"
TOKENS = [
    (ALIAS["W3P"], 61, 61, "## 2. Theorem 1"), (ALIAS["W3P"], 63, 64, "Regime R1"), (ALIAS["W3P"], 68, 70, "(F_λ) anchored floor"),
    (ALIAS["W3P"], 71, 73, "(F_w) anchored unnormalised floor"), (ALIAS["W3P"], 95, 100, "(Random design, interface form)"),
    (ALIAS["W3P"], 36, 37, "m♯_n(ω) := min"), (ALIAS["W3P"], 31, 34, "MPM := {j : PIP_j > ½}"),
    (ALIAS["DIST"], 385, 390, "B0 (scale; pathwise)"), (ALIAS["DIST"], 391, 395, "B1 ((A3) for single coordinates"),
    (ALIAS["DIST"], 396, 399, "B2-core"), (ALIAS["DIST"], 400, 408, "B2 ((A3), (A4) ⇒ (ND))"), (ALIAS["DIST"], 409, 414, "B3 (for Theorem B)"),
    (ALIAS["R1"], 15, 17, "s+j_0\\le(2A+2)s+2"), (ALIAS["R1"], 19, 31, "s+m^\\sharp_n\\le3(A+1)(s+1)\\log n"),
    (ALIAS["RV"], 263, 263, "**Theorem 2.**"), (ALIAS["RV"], 28, 28, "(S1)"), (ALIAS["RV"], 29, 29, "(S2)"),
    (ALIAS["RV"], 1097, 1099, "Sub-Gaussian predictors on sparse directions"), (ALIAS["NOT"], 11, 19, "Gaussian linear model"),
    (ALIAS["NOT"], 22, 25, "correlation matrix"), (ALIAS["POST"], 20, 25, "ψ_n"),
    (W + "W3-READER/CLAIMS_CARD.md", 55, 55, "| 1.2 (Thm 2) |"),
    (EB + "B1.md", 1, 30, "c₁ = 1/576"), (EB + "B2core.md", 1, 20, "c₂ = 10⁻⁵"), (EB + "B2.md", 45, 55, "G_T = Λ_TZ_TᵀCZ_TΛ_T = n·Λ_TΣ̂^z_TΛ_T"),
    (EB + "B3.md", 95, 104, "A-2 (Step 6"), (EB + "B0.md", 1, 40, "the model posteriors coincide"),
]
REG = "Theory_work/INFRA/registry/claims.tsv"
REG_QUOTES = ["W3-POST:Thm-1", "W3-DIST:B0", "W3-DIST:B1", "W3-DIST:B2core", "W3-DIST:B2", "W3-DIST:B3", "W3-READER:R1"]

cache = {}


def lines(rel):
    if rel not in cache:
        p = os.path.join(ROOT, rel)
        cache[rel] = open(p, encoding="utf-8").read().split("\n") if os.path.isfile(p) else None
    return cache[rel]


def nlines(rel):
    L = lines(rel)
    return None if L is None else (len(L) - 1 if L and L[-1] == "" else len(L))


def resolve(path):
    if path in LOCAL:
        return W + "W3-D3/" + path
    if path.startswith("lemmas/") or path.startswith("numerics/"):
        return W + "W3-D3/" + path
    if path.startswith("Theory_work/"):
        return path
    for pre in (W, "Theory_work/", W + "W3-READER/", EB):
        if lines(pre + path) is not None:
            return pre + path
    return path


out, fails, n = [], 0, 0
rng = re.compile(r"`([^`\s]*?):(\d+)(?:-(\d+))?`")
alias_rx = re.compile(r"\[(" + "|".join(re.escape(a) for a in ALIAS) + r")\]")
for f in FILES:
    for ln, text in enumerate(lines(W + "W3-D3/" + f) or [], 1):
        for m in rng.finditer(text):
            path, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            if path == "":
                als = [x for x in alias_rx.finditer(text) if x.start() < m.start()]
                if not als:
                    fails += 1; n += 1
                    out.append(f"UNRESOLVED {f}:{ln} `:{a}-{b}`")
                    continue
                rel = ALIAS[als[-1].group(1)]
            else:
                rel = resolve(path)
            n += 1
            N = nlines(rel)
            ok = N is not None and 1 <= a <= b <= N
            if not ok:
                fails += 1
            out.append(f"{'OK  ' if ok else 'FAIL'} {f}:{ln} -> {rel}:{a}-{b} (lines {N})")
for rel, a, b, tok in TOKENS:
    n += 1
    L = lines(rel)
    ok = L is not None and tok in "\n".join(L[a - 1:b])
    fails += not ok
    out.append(f"{'OK  ' if ok else 'FAIL'} token {tok!r} in {rel}:{a}-{b}")
reg = {r["id"]: r for r in csv.DictReader(open(os.path.join(ROOT, REG), encoding="utf-8"), delimiter="\t")}
st = "\n".join(lines(W + "W3-D3/STATEMENT.md"))
st_flat = re.sub(r"\s*\n\s*", " ", st)
for cid in REG_QUOTES:
    n += 1
    r = reg.get(cid)
    ver = r["version"] if r else "?"
    ok = r is not None and f"`{cid}@{ver}`" in st and r["status"] in st_flat
    fails += not ok
    out.append(f"{'OK  ' if ok else 'FAIL'} status {cid}@{ver} quoted verbatim in STATEMENT §6")
summary = f"W3-D3 citecheck: {n} checks, {fails} failures"
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out + [summary]) + "\n")
print("\n".join(l for l in out if not l.startswith("OK")))
print(summary)
