"""Citation check for W3-MISR-R (PROTOCOL_v4 §3.6) -- adapted from Theory_work/Wave3/W3-MISR/citecheck.py.

SELECTED checks, not full coverage; it does not check mathematics.
(1) Range checks: in STATEMENT.md, TARGET.md, READER_DELTA.md, REPORT.md, lemmas/*.md, every citation of the forms
    "[ALIAS] `:a-b`", "[ALIAS] line(s) a-b", "[ALIAS] a-b", "BASE `file:a-b`", "`file:a-b`" (file = a known path or
    basename) and bare "`:a-b`" (resolved to the last file named earlier on the same line; default: BASE STATEMENT.md
    in this ticket's STATEMENT.md and TARGET.md, else the file named in the lemma header) must point to an existing
    file with 1 <= a <= b <= number of lines.
(2) Token checks: the hand-written TOKENS list (a token that must occur in the cited range).
(3) Status checks: the STATUS quotations occur verbatim in their source.
Writes reviews/CITECHECK.txt. Run from anywhere: python3 Theory_work/Wave3/W3-MISR-R/citecheck.py
"""
import glob
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
B = "Theory_work/Wave3/W3-MISR/"
P2 = "Theory_work/Wave3/W3-POST2/"
ALIAS = {
    "W3P": "Theory_work/Wave3/W3-POST/STATEMENT.md",
    "POST2": P2 + "STATEMENT.md",
    "A": P2 + "lemmas/A_occam.md", "D": P2 + "lemmas/D_hellinger.md",
    "MIS1": "Theory_work/Wave1C/C-MIS/STATEMENT.md",
    "L2": "Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md",
}
FILES = {  # basename or relative path -> repo path
    "G_corollaries.md": B + "lemmas/G_corollaries.md", "lemmas/G_corollaries.md": B + "lemmas/G_corollaries.md",
    "M_misr.md": B + "lemmas/M_misr.md", "lemmas/M_misr.md": B + "lemmas/M_misr.md",
    "R_reduction.md": B + "lemmas/R_reduction.md", "lemmas/R_reduction.md": B + "lemmas/R_reduction.md",
    "D_hellinger.md": P2 + "lemmas/D_hellinger.md", "A_occam.md": P2 + "lemmas/A_occam.md",
    "L1_reduction.md": "Theory_work/Wave1C/C-MIS/lemmas/L1_reduction.md",
    "TRIAGE.md": "Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md",
    "ASSUMPTION_MAP.md": B + "ASSUMPTION_MAP.md",
    "Theory_work/Wave3/W3-POST/STATEMENT.md": ALIAS["W3P"],
    "Theory_work/Wave3/W3-POST2/STATEMENT.md": ALIAS["POST2"],
    "Theory_work/Wave1C/C-MIS/STATEMENT.md": ALIAS["MIS1"],
    "W3-POST2/STATEMENT.md": ALIAS["POST2"],
}
TOKENS = [  # (repo path, a, b, token)
    (B + "STATEMENT.md", 36, 37, "GR^c"), (B + "STATEMENT.md", 60, 62, "𝒦⁰_n"), (B + "STATEMENT.md", 90, 93, "(b) Reduction"),
    (B + "STATEMENT.md", 110, 113, "𝒦^λ_n"), (B + "STATEMENT.md", 147, 147, "(GR^c | 𝓕_n)"), (B + "STATEMENT.md", 157, 160, "Tight constants"),
    (B + "STATEMENT.md", 162, 170, "Corollary G"), (B + "STATEMENT.md", 171, 174, "(b) (2 ≤ p_𝒞 ≤ n^A"), (B + "STATEMENT.md", 176, 197, "Corollary H"),
    (B + "STATEMENT.md", 181, 183, "C_H"), (B + "STATEMENT.md", 187, 191, "reference law"), (B + "STATEMENT.md", 63, 63, "c₀(s, A)"),
    (B + "lemmas/G_corollaries.md", 26, 34, "Gaussian"), (B + "lemmas/G_corollaries.md", 36, 65, "Corollary G(b)"),
    (B + "lemmas/G_corollaries.md", 67, 93, "Corollary H"), (B + "lemmas/G_corollaries.md", 79, 82, "Hellinger"),
    (B + "lemmas/M_misr.md", 143, 149, "freezing"), (B + "lemmas/M_misr.md", 133, 138, "Borel"),
    (B + "lemmas/R_reduction.md", 26, 26, "(R1)"), (B + "lemmas/R_reduction.md", 37, 37, "(R3)"), (B + "lemmas/R_reduction.md", 59, 72, "Proof of (b)"),
    (ALIAS["POST2"], 35, 35, "(OS; C_OS)"), (ALIAS["POST2"], 46, 47, "(F_w; g₀) ⇒"), (ALIAS["POST2"], 101, 103, "θ = s_yβ"),
    (ALIAS["POST2"], 107, 111, "D(a)"), (ALIAS["POST2"], 112, 116, "D(b)"), (ALIAS["POST2"], 113, 113, "C_H depending only on (s₀, A, σ*²)"),
    (ALIAS["POST2"], 115, 115, "C_H′ := 1 + C_H/(4σ*²)"),
    (P2 + "lemmas/D_hellinger.md", 8, 11, "θ̂_S := nH_S⁻¹X_{c,S}ᵀy_c"), (P2 + "lemmas/D_hellinger.md", 12, 12, "H²(N(a, v), N(b, w))"),
    (P2 + "lemmas/D_hellinger.md", 72, 72, "C_H := 4(m_n^{fit}/log n) + 1"),
    (P2 + "lemmas/A_occam.md", 14, 15, "Lemma A0"),
    (ALIAS["W3P"], 18, 22, "X = CX^rD_x⁻¹"), (ALIAS["W3P"], 63, 64, "Regime R1"),
    ("Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md", 88, 90, "W := UᵀX^r_𝒞"), ("Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md", 91, 93, "SDs"),
    ("Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md", 94, 100, "Sparse eigenvalues"), ("Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md", 105, 105, "Total failure probability"),
    ("Theory_work/Wave1C/C-MIS/STATEMENT.md", 17, 24, "What SL prove"),
    ("Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md", 40, 42, "W3-MISR:Cor-G(a)"),
]
STATUS = [(P2 + "lemmas/D_hellinger.md", "PROVED (by this seat, unchecked)"),
          (P2 + "lemmas/A_occam.md", "PROVED (by this seat, unchecked)")]
REG = "Theory_work/INFRA/registry/claims.tsv"
REG_STATUS = ["W3-MISR:R'", "W3-MISR:MIS(i)", "W3-MISR:MIS(ii)", "W3-MISR:Cor-G(b)", "W3-MISR:Cor-H",
              "SOP:TH09", "SOP:TH128", "C-MIS:Prop-P", "C-MIS:GD(b)"]

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


names = sorted(FILES, key=len, reverse=True)
pat = re.compile(
    r"(?:\[(?P<al>" + "|".join(map(re.escape, ALIAS)) + r")\]\s*(?:\(|`)?\s*(?:lines?\s+)?(?P<a1>\d+)(?:-(?P<b1>\d+))?)"
    r"|(?:\[(?P<al2>" + "|".join(map(re.escape, ALIAS)) + r")\]\s*`:(?P<a2>\d+)(?:-(?P<b2>\d+))?`)"
    r"|(?:`(?P<f>" + "|".join(map(re.escape, names)) + r"|STATEMENT\.md):(?P<a3>\d+)(?:-(?P<b3>\d+))?)"
    r"|(?:`:(?P<a4>\d+)(?:-(?P<b4>\d+))?`)")
pat_file = re.compile(r"(" + "|".join(map(re.escape, names)) + r"|STATEMENT\.md|\[(?:" + "|".join(ALIAS) + r")\])")
docs = [os.path.join(HERE, f) for f in ["STATEMENT.md", "TARGET.md", "READER_DELTA.md", "REPORT.md"]]
docs += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
for f in docs:
    if not os.path.isfile(f):
        continue
    name = os.path.relpath(f, HERE)
    default = B + "STATEMENT.md"
    for ln, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        for m in pat.finditer(line):
            if m.group("al"):
                rel, a, b = ALIAS[m.group("al")], m.group("a1"), m.group("b1")
            elif m.group("al2"):
                rel, a, b = ALIAS[m.group("al2")], m.group("a2"), m.group("b2")
            elif m.group("f"):
                fn = m.group("f")
                if fn == "STATEMENT.md":
                    pre = line[:m.start()]
                    rel = ALIAS["POST2"] if "[POST2]" in pre[-40:] else (ALIAS["W3P"] if "[W3P]" in pre[-40:] else default)
                else:
                    rel = FILES[fn]
                a, b = m.group("a3"), m.group("b3")
            else:
                prev = [x for x in pat_file.finditer(line[:m.start()])]
                if prev:
                    t = prev[-1].group(1)
                    rel = ALIAS[t[1:-1]] if t.startswith("[") else (FILES.get(t) or default)
                else:
                    rel = default
                a, b = m.group("a4"), m.group("b4")
            a = int(a)
            b = int(b) if b else a
            L = lines(rel)
            check(L is not None and 1 <= a <= b <= len(L), f"{name}:{ln}: {m.group(0)!r} -> {rel}:{a}-{b} out of range or missing")
for rel, a, b, tok in TOKENS:
    L = lines(rel)
    check(L is not None and tok in "\n".join(L[a - 1:b]), f"token {tok!r} not in {rel}:{a}-{b}")
for rel, s in STATUS:
    L = lines(rel)
    check(L is not None and s in "\n".join(L), f"status {s!r} not in {rel}")
try:
    reg = subprocess.run(["git", "-C", ROOT, "show", "origin/main:" + REG], capture_output=True, text=True, check=True).stdout
    st = {r.split("\t")[0]: r.split("\t")[11] for r in reg.split("\n")[1:] if r.count("\t") > 11}
    stmt = open(os.path.join(HERE, "STATEMENT.md"), encoding="utf-8").read()
    for cid in REG_STATUS:
        check(cid in st and st[cid] in stmt.replace("\n  ", " "), f"registry status of {cid} not quoted verbatim in STATEMENT.md §7")
except Exception as e:  # noqa: BLE001
    check(False, f"registry read failed: {e}")
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
report = [f"W3-MISR-R citecheck: {nchk} checks, {fails} failures"] + out
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(report) + "\n")
print("\n".join(report))
