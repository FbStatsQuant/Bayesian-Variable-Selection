"""Citation check for W3-D2 (PROTOCOL_v4 §3.6). Pattern of W3-MISR-R/citecheck.py; simplified. Does not check mathematics.

(1) Range checks in STATEMENT.md, PROOF.md, REPORT.md, TARGET.md, READER_DELTA.md, API_CARD.md: every
    "[ALIAS] ... `:a-b`" / "[ALIAS] `:a`" (alias resolved from the last [ALIAS] earlier on the same line),
    "`path:a-b`" (path = a repo path, or a ticket-local file) must point to an existing file with 1 <= a <= b <= #lines.
    A bare "`:a-b`" with no alias earlier on its line is reported as UNRESOLVED (counted as a failure).
(2) Token checks: TOKENS (a token that must occur in the cited range).
(3) Status checks: every registry status quoted in STATEMENT §5 occurs verbatim in claims.tsv for that id@version.
Writes reviews/CITECHECK.txt. Run: python3 Theory_work/Wave3/W3-D2/citecheck.py
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
    "W3P": W + "W3-POST/STATEMENT.md", "MISR": W + "W3-MISR/STATEMENT.md", "MISR-R": W + "W3-MISR-R/STATEMENT.md",
    "RV": W + "W3-READER/READER_VERSIONS.md", "R1": W + "W3-READER/lemmas/R1_set_sizes.md",
}
LOCAL = {"STATEMENT.md", "PROOF.md", "TARGET.md", "REPORT.md", "READER_DELTA.md", "PLAN.md"}
FILES = ["STATEMENT.md", "PROOF.md", "REPORT.md", "TARGET.md", "READER_DELTA.md", "API_CARD.md"]
TOKENS = [
    (ALIAS["MISR-R"], 94, 108, "CorGb-plus"), (ALIAS["MISR-R"], 31, 31, "N_k(m, 0) := δ_m"), (ALIAS["MISR-R"], 56, 56, "(N)"),
    (ALIAS["MISR-R"], 67, 68, "(OV)"), (ALIAS["MISR-R"], 96, 96, "Σ_jj > 0"), (ALIAS["MISR-R"], 99, 99, "may depend on n"),
    (ALIAS["MISR-R"], 104, 104, "ρ_n^{BM} → ∞"), (ALIAS["MISR-R"], 105, 105, "E δ_n ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1}"),
    (ALIAS["MISR-R"], 52, 52, "q = q_n ≥ 0"), (ALIAS["MISR"], 20, 22, "coded target of [W3P] §0"),
    (ALIAS["MISR"], 118, 119, "for every data set"), (ALIAS["W3P"], 33, 33, "MPM := {j : PIP_j > ½}"),
    (ALIAS["W3P"], 33, 33, "HPM := argmax_Ω π (any tie rule)"), (ALIAS["W3P"], 37, 37, "m♯_n(ω) := min"),
    (ALIAS["R1"], 43, 45, "B4.1"), (ALIAS["R1"], 44, 44, "s\\le K"), (ALIAS["RV"], 263, 263, "**Theorem 2.**"),
    (ALIAS["RV"], 269, 269, "5(A+1)(s_0+1)\\log n"), (ALIAS["RV"], 271, 271, "three conclusions"),
    (ALIAS["RV"], 28, 28, "(S1)"), (ALIAS["RV"], 29, 29, "(S2)"), (ALIAS["RV"], 449, 449, "**Theorem 4**"),
    (W + "W3-READER/NOTATION.md", 15, 20, "\\alpha^*\\mathbf 1_n+X^{\\mathrm r}\\beta^*+\\varepsilon"),
    (W + "W3-READER/CLAIMS_CARD.md", 55, 55, "| 1.2 (Thm 2) |"),
    ("Theory_work/Wave2/W2-APP/lemmas/L1_POST.md", 20, 25, "ψ_n"),
    (W + "W3-MISR-R/lemmas/G2_corr.md", 29, 34, "non-empty T"),
]
REG = "Theory_work/INFRA/registry/claims.tsv"
REG_QUOTES = ["W3-MISR-R:CorGb-plus", "W3-READER:R1", "W3-POST2:C", "W3-POST:Prop-LB"]

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
        return W + "W3-D2/" + path
    if path.startswith("Theory_work/"):
        return path
    for pre in (W, "Theory_work/", W + "W3-READER/"):
        if lines(pre + path) is not None:
            return pre + path
    return path


out, fails, n = [], 0, 0
rng = re.compile(r"`([^`\s]*?):(\d+)(?:-(\d+))?`")
alias_rx = re.compile(r"\[(" + "|".join(re.escape(a) for a in ALIAS) + r")\]")
for f in FILES:
    for ln, text in enumerate(lines(W + "W3-D2/" + f) or [], 1):
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
st = "\n".join(lines(W + "W3-D2/STATEMENT.md"))
st_flat = re.sub(r"\s*\n\s*", " ", st)
for cid in REG_QUOTES:
    n += 1
    r = reg.get(cid)
    ver = r["version"] if r else "?"
    ok = r is not None and f"`{cid}@{ver}`" in st and r["status"] in st_flat
    fails += not ok
    out.append(f"{'OK  ' if ok else 'FAIL'} status {cid}@{ver} quoted verbatim in STATEMENT §5")
summary = f"W3-D2 citecheck: {n} checks, {fails} failures"
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out + [summary]) + "\n")
print("\n".join(l for l in out if not l.startswith("OK")))
print(summary)
