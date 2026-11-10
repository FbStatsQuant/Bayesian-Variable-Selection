"""Citation check for W3-POST (protocol rule 2) — SELECTED checks, not full coverage [C1A-F9].

What it does, exactly:
(1) Range checks: extracts citations of the explicit form path:a-b / path:a (also comma lists) and the alias form
    "[T03R|P1|P3|POST|SL|UNI] line(s) a-b" from STATEMENT.md, ASSUMPTION_MAP.md, REPORT.md and lemmas/*.md; requires
    the file to exist and 1 <= a <= b <= number of lines. Other citation syntaxes (e.g. section names, label names,
    "[T03R] E2(ii)") are NOT extracted.
(2) Content checks: only the hand-written TOKENS list (claim-specific tokens that must occur in the cited range).
(3) Status checks: only the three hard-coded STATUS quotations (verbatim occurrence in the source file).
It does not check literature accuracy, reviewer-verdict summaries or mathematics; semantic audit is manual (excerpts in
reviews/CITECHECK_excerpts.md). Writes reviews/CITECHECK.txt. Run: py -3.13 -I citecheck.py
"""
import os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = r"C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave3/W3-POST"
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TW = os.path.join(ROOT, "Theory_work")
ARC = "Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/"
ALIAS = {
    "T03R": ARC + "W1-T03R/PROOF.md",
    "P1": ARC + "main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex",
    "P3": ARC + "main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex",
    "POST": "Theory_work/Wave2/W2-APP/lemmas/L1_POST.md",
    "SL": "Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md",
    "UNI": "Theory_work/Wave2/W2-UNI/STATEMENT.md",
}
SRC = [os.path.join(HERE, f) for f in ("STATEMENT.md", "ASSUMPTION_MAP.md", "REPORT.md") if os.path.exists(os.path.join(HERE, f))]
SRC += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
RNG = r"(\d+)(?:\s*[-–]\s*(\d+))?"
P_EXPL = re.compile(r"`?([A-Za-z0-9_@./\-]+\.(?:md|tex|R|py|txt|h|cpp)):" + RNG + r"((?:,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
P_ALIAS = re.compile(r"\[(T03R|P1|P3|POST|SL|UNI)\][^\[\n]{0,40}?\blines?\s+" + RNG + r"((?:,\s*\d+(?:\s*[-–]\s*\d+)?)*)")

TOKENS = [  # (alias-or-path, a, b, token)
    ("T03R", 79, 85, "Theorem T02(i♯)"), ("T03R", 149, 149, "SE$_w(m^\\sharp_n;g_0)$"),
    ("T03R", 162, 168, "BM-∞"), ("T03R", 103, 121, "Proposition D"), ("T03R", 50, 54, "\\omega\\ge0"),
    ("T03R", 15, 17, "R_m"), ("T03R", 44, 47, "m^\\sharp_n(\\omega)"), ("T03R", 89, 91, "Lemma den′"),
    ("T03R", 93, 97, "Proof of T02(i♯)"), ("T03R", 77, 77, "c^\\sharp"), ("T03R", 134, 134, "SE$_w(m^\\sharp_n;\\varphi_0^2)$"),
    ("POST", 23, 33, "Hypothesis LSF"), ("POST", 12, 18, "Raw-scale convention"),
    ("SL", 20, 63, "Lemma SL0"), ("UNI", 87, 91, "Theorem UNI-P"),
    ("Theory_work/State_of_Project/sections/04_theory.tex", 771, 771, "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"),
    ("Theory_work/State_of_Project/sections/04_theory.tex", 771, 771, "T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED"),
    ("Theory_work/State_of_Project/sections/04_theory.tex", 780, 788, "BM\\((c)\\)"),
    ("Theory_work/State_of_Project/sections/04_theory.tex", 816, 816, "CJ18"),
    ("Theory_work/Wave2/SR/BLIND_fable.md", 92, 93, "Lemma A (design-free size reduction)"),
    ("Scripts/SMC_BVS/core/cpp/v3_score.h", 40, 71, "D.nu = D.a0 + n / 2.0"),
    ("Scripts/SMC_BVS/core/cpp/v3_score.h", 40, 71, "-M_LN2 - lchoose_d(2.0 * p - 1.0, k)"),
    ("Scripts/SMC_BVS/core/cpp/v3_score.h", 196, 224, "double Q = D->yty - D->n * quad"),
    ("Scripts/SMC_BVS/core/v3_preprocess.R", 111, 127, "kept"),
    ("ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md", 9, 14, "w(k) = ½/C(2p−1, k)"),
]
STATUS = [  # (quoted status, source)
    ("T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", "Theory_work/State_of_Project/sections/04_theory.tex"),
    ("T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED", "Theory_work/State_of_Project/sections/04_theory.tex"),
    ("PROVED (by this seat, unchecked)", "Theory_work/Wave2/W2-APP/lemmas/L1_POST.md"),
]


def resolve(path):
    path = path.strip("`")
    if path in ALIAS:
        path = ALIAS[path]
    if path.startswith("ARC/"):
        path = ARC + path[4:]
    for base in (ROOT, TW, HERE):
        f = os.path.join(base, path)
        if os.path.isfile(f):
            return f
    return None


def lines_of(f):
    with open(f, encoding="utf-8", errors="replace") as h:
        return h.read().split("\n")


def ranges(a, b, rest):
    out = [(int(a), int(b or a))]
    for m in re.finditer(r"(\d+)(?:\s*[-–]\s*(\d+))?", rest or ""):
        out.append((int(m.group(1)), int(m.group(2) or m.group(1))))
    return out


report, excerpts, fails, n = [], ["# CITECHECK excerpts (W3-POST)\n"], 0, 0
for src in SRC:
    for ln, text in enumerate(lines_of(src), 1):
        cites = [(m.group(1), ranges(m.group(2), m.group(3), m.group(4))) for m in P_EXPL.finditer(text)]
        cites += [(m.group(1), ranges(m.group(2), m.group(3), m.group(4))) for m in P_ALIAS.finditer(text)]
        for path, rr in cites:
            f = resolve(path)
            for a, b in rr:
                n += 1
                tag = f"{os.path.relpath(src, HERE)}:{ln} -> {path}:{a}-{b}"
                if f is None:
                    fails += 1; report.append("MISS (no file)  " + tag); continue
                L = lines_of(f)
                if not (1 <= a <= b <= len(L)):
                    fails += 1; report.append(f"FAIL (range; file has {len(L)} lines)  " + tag); continue
                report.append("ok  " + tag)
                excerpts.append(f"\n## {tag}\n```\n" + "\n".join(x[:220] for x in L[a - 1:min(b, a + 11)]) + "\n```")
for path, a, b, tok in TOKENS:
    f = resolve(path); n += 1
    seg = "\n".join(lines_of(f)[a - 1:b]) if f else ""
    if tok in seg:
        report.append(f"ok  TOKEN {path}:{a}-{b} contains {tok!r}")
    else:
        fails += 1; report.append(f"FAIL TOKEN {path}:{a}-{b} lacks {tok!r}")
for st, path in STATUS:
    f = resolve(path); n += 1
    if f and st in open(f, encoding="utf-8").read():
        report.append(f"ok  STATUS {st!r} in {path}")
    else:
        fails += 1; report.append(f"FAIL STATUS {st!r} not in {path}")
report.insert(0, f"W3-POST citecheck: {n} checks, {fails} failures")
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "C3_scratch_opus", "CITECHECK_c3.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
open(os.path.join(HERE, "reviews", "C3_scratch_opus", "CITECHECK_excerpts_c3.md"), "w", encoding="utf-8").write("\n".join(excerpts) + "\n")
print(report[0]); print("\n".join(r for r in report if not r.startswith("ok")))
