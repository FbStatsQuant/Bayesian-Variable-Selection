"""Citation check for W3-MISR (protocol rule 2) -- SELECTED checks, not full coverage.

(1) Range checks: every citation "[ALIAS] line(s) a-b" / "[ALIAS] a-b" in table cells, and every "`file:a-b`" /
    "path:a-b" for the code files and the files named in ALIAS, in STATEMENT.md, ASSUMPTION_MAP.md, lemmas/*.md,
    REPORT.md: the file exists and 1 <= a <= b <= number of lines.
(2) Token checks: the hand-written TOKENS list (a token that must occur in the cited range).
(3) Status checks: the STATUS quotations occur verbatim in their source.
It does not check mathematics. Writes reviews/CITECHECK.txt.  Run: py -3.13 -I Theory_work/Wave3/W3-MISR/citecheck.py
"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ARC = "Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/"
P2 = "Theory_work/Wave3/W3-POST2/"
ALIAS = {
    "W3P": "Theory_work/Wave3/W3-POST/STATEMENT.md",
    "POST2": P2 + "STATEMENT.md",
    "A": P2 + "lemmas/A_occam.md", "C": P2 + "lemmas/C_expectation.md",
    "D": P2 + "lemmas/D_hellinger.md", "E": P2 + "lemmas/E_visibility.md",
    "MIS1": "Theory_work/Wave1C/C-MIS/STATEMENT.md",
    "L2": "Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md",
    "L4": "Theory_work/Wave1C/C-MIS/lemmas/L4_theoremF.md",
    "T03R": ARC + "W1-T03R/PROOF.md",
    "P3": ARC + "main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex",
}
CODE = {n: "Scripts/SMC_BVS/core/" + n for n in ["v3_preprocess.R", "v3_fit.R", "v3_setup.R"]}
CODE["cpp/v3_score.h"] = "Scripts/SMC_BVS/core/cpp/v3_score.h"
CODE["L1_reduction.md"] = "Theory_work/Wave1C/C-MIS/lemmas/L1_reduction.md"
CODE["L5_frontier.md"] = "Theory_work/Wave1C/C-MIS/lemmas/L5_frontier.md"
CODE["HQ_DECISIONS.md"] = "Theory_work/Wave3/HQ_DECISIONS.md"

TOKENS = [  # (alias or repo path, a, b, token)
    ("W3P", 18, 29, "m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}"), ("W3P", 20, 21, "y = Cy^r/s_y"), ("W3P", 31, 31, "S₀ = supp θ*"),
    ("W3P", 36, 39, "m♯_n"), ("W3P", 63, 64, "Regime R1"), ("W3P", 67, 67, "(E) energy"), ("W3P", 68, 70, "(F_λ)"),
    ("W3P", 74, 75, "c₀(s₀, A)"), ("W3P", 84, 84, "max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n"),
    ("POST2", 25, 25, "(F₀)"), ("POST2", 29, 36, "(OS; C_OS)"), ("POST2", 40, 41, "(ID^M; c)"), ("POST2", 42, 42, "(ID^M_j; c)"),
    ("POST2", 44, 44, "B_T(ϑ)"), ("POST2", 46, 47, "(OS; C_OS(c_D, s₀, A))"), ("POST2", 70, 70, "G′"),
    ("POST2", 85, 89, "E δ_n ≤ C r_n"), ("POST2", 101, 103, "(θ = s_yβ, v = s_y²σ²)"), ("POST2", 105, 105, "H²(P, Q)"),
    ("POST2", 107, 111, "D(a)"), ("POST2", 112, 116, "D(b)"), ("POST2", 130, 130, "c₁ :="),
    ("C", 9, 15, "depending only"), ("C", 31, 42, "Lemma C2"), ("C", 44, 55, "E T₀"),
    ("A", 14, 15, "Lemma A0"), ("A", 46, 53, "(G3′)"), ("A", 64, 66, "(C5′)"), ("A", 67, 67, "E Υ′^{>j₁}_n ≤ 𝒪_n^{>j₁}"),
    ("A", 85, 86, "5(a)"), ("E", 26, 27, "Lemma E1"), ("E", 61, 65, "Underfits"), ("E", 67, 68, "(5b′)"), ("E", 76, 77, "lem:signal"),
    ("D", 12, 12, "H²(N(a, v), N(b, w))"),
    ("MIS1", 54, 58, "(GR)"), ("MIS1", 62, 62, "with σ_𝒞²"), ("MIS1", 83, 85, "τ_n² ≡ τ² fixed"), ("MIS1", 101, 105, "Lemma Z"),
    ("MIS1", 126, 126, "(EP)"), ("MIS1", 132, 133, "BM-∞"), ("MIS1", 140, 140, "(TL)"),
    ("L2", 40, 44, "Gaussian conditioning"), ("L2", 91, 93, "SDs"), ("L2", 94, 100, "Sparse eigenvalues"), ("L2", 101, 102, "Energy"),
    ("L2", 103, 103, "BM"), ("L2", 105, 105, "Total failure probability"), ("L2", 74, 74, "counterexample"),
    ("T03R", 187, 189, "(C6)"), ("T03R", 194, 197, "(C8)"), ("P3", 39, 41, "\\ell(S)"), ("P3", 227, 229, "\\Xi_j"), ("P3", 201, 201, "\\rho_n"),
    ("Scripts/SMC_BVS/core/v3_preprocess.R", 37, 68, "v3_standardise <- function"), ("Scripts/SMC_BVS/core/v3_preprocess.R", 123, 127, "y = sy$z"),
    ("Scripts/SMC_BVS/core/v3_preprocess.R", 126, 127, "s_y = sy$max * sy$sd"), ("Scripts/SMC_BVS/core/v3_fit.R", 97, 97, "v3_preprocess(X, y"),
    ("Scripts/SMC_BVS/core/v3_fit.R", 118, 118, "v3_context(pre$X, pre$y"), ("Scripts/SMC_BVS/core/v3_setup.R", 7, 13, "cpp_context"),
    ("Scripts/SMC_BVS/core/cpp/v3_score.h", 14, 14, "b0 = 0.01"), ("Scripts/SMC_BVS/core/cpp/v3_score.h", 55, 60, "D.yty"),
    ("Scripts/SMC_BVS/core/cpp/v3_score.h", 217, 223, "D->nu * std::log(arg)"),
    ("Theory_work/Wave3/HQ_DECISIONS.md", 48, 49, "PROVED-CHECKED labels for W3-POST2 claims A–E restored"),
]
STATUS = [("Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md", "PROVED (by this seat, unchecked)"),
          ("Theory_work/Wave3/W3-POST2/lemmas/E_visibility.md", "PROVED (by this seat, unchecked)"),
          ("Theory_work/Wave3/W3-POST2/lemmas/A_occam.md", "PROVED (by this seat, unchecked)"),
          ("Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md", "PROVED (by this seat, unchecked)"),
          ("Theory_work/State_of_Project/sections/04_theory.tex", "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)")]

cache = {}
def lines(rel):
    if rel not in cache:
        p = os.path.join(ROOT, rel)
        cache[rel] = open(p, encoding="utf-8").read().split("\n") if os.path.isfile(p) else None
    return cache[rel]

out, fails, nchk = [], 0, 0
def check(ok, msg):
    global fails, nchk
    nchk += 1
    if not ok:
        fails += 1
        out.append("FAIL " + msg)

files = [os.path.join(HERE, f) for f in ["STATEMENT.md", "ASSUMPTION_MAP.md", "REPORT.md"]] + sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
pat_alias = re.compile(r"\[(" + "|".join(map(re.escape, ALIAS)) + r")\]\s*\(?(?:lines?\s+)?(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)")
pat_code = re.compile(r"(" + "|".join(map(re.escape, CODE)) + r"):(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)")
pat_rel = re.compile(r"`:(\d+)(?:-(\d+))?`")
for f in files:
    if not os.path.isfile(f):
        continue
    txt = open(f, encoding="utf-8").read()
    name = os.path.relpath(f, HERE)
    for pat, table in ((pat_alias, ALIAS), (pat_code, CODE)):
        for m in pat.finditer(txt):
            rel = table[m.group(1)]
            L = lines(rel)
            spans = [(m.group(2), m.group(3))] + re.findall(r"(\d+)(?:-(\d+))?", m.group(4) or "")
            for a, b in spans:
                a = int(a); b = int(b) if b else a
                check(L is not None and 1 <= a <= b <= len(L), f"{name}: {m.group(0)!r} -> {rel}:{a}-{b} out of range or missing")
for key, a, b, tok in TOKENS:
    rel = ALIAS.get(key, key)
    L = lines(rel)
    check(L is not None and tok in "\n".join(L[a - 1:b]), f"token {tok!r} not in {rel}:{a}-{b}")
for rel, s in STATUS:
    L = lines(rel)
    check(L is not None and s in "\n".join(L), f"status {s!r} not in {rel}")
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
report = [f"W3-MISR citecheck: {nchk} checks, {fails} failures"] + out
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(report) + "\n")
print("\n".join(report))
