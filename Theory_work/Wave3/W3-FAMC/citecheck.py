"""Citation check for W3-FAMC (copied from W3-D3/citecheck.py; aliases, tokens and registry list adapted) (PROTOCOL_v4 §3.6). Does not check mathematics.

(1) Range checks in STATEMENT.md, lemmas/A_assembly.md, TARGET.md, REPORT.md: every "[ALIAS] ... `:a-b`" (alias = the last
    [ALIAS] earlier on the same line) or "`path:a-b`" must point to an existing file with 1 <= a <= b <= #lines.
    A bare "`:a-b`" with no alias earlier on its line is UNRESOLVED (a failure).
(2) Token checks: TOKENS (a token that must occur in the cited range).
(3) Status checks: every registry status quoted in STATEMENT §4 occurs verbatim in claims.tsv for that id@version.
Writes reviews/CITECHECK.txt. Run: python3 Theory_work/Wave3/W3-FAMC/citecheck.py
"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W = "Theory_work/Wave3/"
T = "W3-FAMC/"
ALIAS = {
    "RV": W + "W3-READER/READER_VERSIONS.md", "NOT": W + "W3-READER/NOTATION.md",
    "VIS": W + "W3-AUDIT/track_V/V1_VIS/STATEMENT.md", "RM2R": W + "W3-RM2-R/STATEMENT.md",
    "RM2": W + "W3-RM2/STATEMENT.md", "L6": W + "W3-RM2/lemmas/L6_examples.md",
    "GROW5": "Theory_work/Wave1C/C-GROW/lemmas/L5_instances.md", "TB": W + "W3-AUDIT/TRACK_B.md",
    "RM": W + "W3-RM/STATEMENT.md", "CG": "Theory_work/Wave1C/C-GROW/STATEMENT.md",
}
LOCAL = {"STATEMENT.md", "TARGET.md", "REPORT.md", "PLAN.md", "lemmas/A_assembly.md"}
FILES = ["STATEMENT.md", "lemmas/A_assembly.md", "TARGET.md", "REPORT.md"]
EB = W + "W3-READER/"
A = ALIAS
TOKENS = [
    (A["RV"], 660, 660, "## 6. Theorem 6"), (A["RV"], 28, 31, "(S3)"), (A["RV"], 32, 32, "(S4)"),
    (A["RV"], 696, 697, "IDEAL-W⁺"), (A["RV"], 697, 697, "time guard"), (A["NOT"], 60, 60, "K:=\\min(p,\\lfloor n/2\\rfloor)"),
    (A["NOT"], 161, 164, "Cov"), (A["VIS"], 27, 27, "**bad set** B"), (A["VIS"], 30, 31, "(VIS-0)"),
    (A["VIS"], 31, 31, "≥ c₁₆"), (A["VIS"], 32, 35, "(VIS-a)"), (A["VIS"], 36, 40, "(VIS-b)"), (A["VIS"], 46, 51, "finitely many local patterns"),
    (A["VIS"], 52, 53, "stationary designs"), (A["VIS"], 54, 58, "(VIS-e)"), (A["VIS"], 22, 22, "Γ^U_{jk}"),
    (A["RM2R"], 177, 182, "Theorem RM2-R-plus"), (A["RM2"], 134, 134, "(L-feas)"), (A["RM2"], 172, 172, "### 3.2"),
    (A["RM2"], 201, 202, "(D-loc^b)"), (A["RM"], 129, 133, "Sufficient: λ_min(Σ_n) ≥ c."), (A["RM"], 135, 136, "PTV(a₀)"),
    (A["RM"], 154, 156, "(D-loc)"), (A["L6"], 35, 38, "K_dec (1+d(j,k))^(-alpha)"), (A["L6"], 97, 103, "r=floor(sqrt(log n))"),
    (A["L6"], 164, 164, "## E2."), (A["L6"], 170, 174, "PTV(a0)"), (A["L6"], 174, 174, "No truth-separation"),
    (A["L6"], 211, 248, "Thus all hypotheses of RM2-R are verified"), (A["GROW5"], 18, 20, "Reduction to ρ > 0"),
    (A["GROW5"], 23, 25, "(P1) Spectrum"), (A["GROW5"], 31, 42, "(P4) Conditional covariance"), (A["GROW5"], 43, 46, "(P5)"),
    (A["GROW5"], 58, 61, "(G3b) TV"), (A["TB"], 216, 216, "θ = (1, −2)"), (A["TB"], 256, 257, "AR(0.95)"),
    (A["CG"], 146, 147, "S2 layouts"),
]
REG = "Theory_work/INFRA/registry/claims.tsv"
REG_QUOTES = ["W3-RM2-R:RM2-R-plus", "W3-RM2-R:RM0-plus", "W3-RM2-R:DLV-0", "W3-AUDIT-V:VIS", "C-GROW:C5a",
              "W3-RM2:D-to-W", "W3-RM2:POST-R", "W2-APP:POST", "W3-RM2:Ex-PolyR", "W2-LOC2:Lemma-BC", "W2-LOC2:Lemma-IR"]

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
        return W + T + path
    if path.startswith("lemmas/") or path.startswith("numerics/"):
        return W + T + path
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
    for ln, text in enumerate(lines(W + T + f) or [], 1):
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
st = "\n".join(lines(W + T + "STATEMENT.md"))
st_flat = re.sub(r"\s*\n\s*", " ", st)
for cid in REG_QUOTES:
    n += 1
    r = reg.get(cid)
    ver = r["version"] if r else "?"
    ok = r is not None and f"`{cid}@{ver}`" in st and r["status"] in st_flat
    fails += not ok
    out.append(f"{'OK  ' if ok else 'FAIL'} status {cid}@{ver} quoted verbatim in STATEMENT §4")
summary = f"W3-FAMC citecheck: {n} checks, {fails} failures"
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out + [summary]) + "\n")
print("\n".join(l for l in out if not l.startswith("OK")))
print(summary)
