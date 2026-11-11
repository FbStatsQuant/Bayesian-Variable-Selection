"""Citation check for W3-POST2 (protocol rule 2) — SELECTED checks, not full coverage.

What it does, exactly:
(1) Range checks: citations of the explicit form path:a-b / path:a (comma lists too) and the alias form
    "[T03R|P1|P3|W3P|L1a′|LB|SL|POST] line(s) a-b" in STATEMENT.md, ASSUMPTION_MAP.md, REPORT.md, lemmas/*.md: the file
    must exist and 1 <= a <= b <= number of lines.
(2) Label checks: every backticked LaTeX label `lem:x`, `thm:x`, `prop:x`, `cor:x`, `eq:x` (and the forms eq. (`eq:x`))
    must exist as \\label{...} in [P1] or [P3].
(3) Content checks: the hand-written TOKENS list (claim-specific tokens that must occur in the cited range).
(4) Status checks: the hard-coded STATUS quotations must occur verbatim in their source.
It does not check mathematics, literature accuracy or reviewer summaries (manual). Writes reviews/CITECHECK.txt.
Run: py -3.13 -I citecheck.py
"""
import os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ARC = "Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/"
ALIAS = {
    "T03R": ARC + "W1-T03R/PROOF.md",
    "P1": ARC + "main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex",
    "P3": ARC + "main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex",
    "W3P": "Theory_work/Wave3/W3-POST/STATEMENT.md",
    "L1a′": "Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md",
    "LB": "Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md",
    "POST": "Theory_work/Wave2/W2-APP/lemmas/L1_POST.md",
    "SL": "Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md",
    "PROOF.md": ARC + "W1-T03R/PROOF.md",
    "PROOF_v2.tex": ARC + "main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex",
    "PROOF_v3.tex": ARC + "main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex",
}
SRC = [os.path.join(HERE, f) for f in ("STATEMENT.md", "ASSUMPTION_MAP.md", "REPORT.md") if os.path.exists(os.path.join(HERE, f))]
SRC += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
RNG = r"(\d+)(?:\s*[-–]\s*(\d+))?"
P_EXPL = re.compile(r"`?([A-Za-z0-9_@./\-]+\.(?:md|tex|R|py|txt|h|cpp)):" + RNG + r"((?:,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
P_ALIAS = re.compile(r"\[(T03R|P1|P3|W3P|L1a′|LB|POST|SL)\][^\[\n]{0,40}?\blines?\s+" + RNG + r"((?:,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
P_LABEL = re.compile(r"`((?:lem|thm|prop|cor|eq):[A-Za-z0-9]+)`")

TOKENS = [  # (alias-or-path, a, b, token)
    ("T03R", 77, 77, "c^\\sharp"), ("T03R", 79, 85, "Theorem T02(i♯)"), ("T03R", 89, 91, "Lemma den′"),
    ("T03R", 93, 97, "Proof of T02(i♯)"), ("T03R", 139, 139, "(B1)"), ("T03R", 143, 143, "(B1) SE$_w$"),
    ("T03R", 140, 140, "(B2)"), ("T03R", 141, 141, "(B3)"), ("T03R", 149, 149, "SE$_w(m^\\sharp_n;g_0)$"),
    ("T03R", 174, 174, "(C2)"), ("T03R", 176, 176, "(C3)"), ("T03R", 178, 181, "(C4)"), ("T03R", 183, 185, "(C5)"),
    ("T03R", 187, 190, "(C6)"), ("T03R", 194, 197, "(C8)"), ("T03R", 199, 199, "(C9)"), ("T03R", 201, 201, "(C10)"),
    ("T03R", 213, 215, "Where the normalised constant"), ("T03R", 215, 215, "CONJECTURE"),
    ("P3", 177, 177, "(G2)"), ("P3", 179, 179, "(G4)"), ("P3", 190, 190, "C_Ak\\log n"), ("P3", 194, 194, "(G4)"),
    ("P3", 158, 158, "e^{\\chi^2_d/2}"), ("P3", 317, 317, "\\max\\emptyset:=0"), ("P3", 227, 227, "\\Xi_j"),
    ("P3", 114, 114, "\\eta_n\\|P_Tu\\|^2"), ("P3", 146, 151, "signal left by an underfitting model"),
    ("P1", 337, 338, "Bound on $Q^c_{S_0}$"), ("P1", 95, 95, "If $k\\ge1$ and $\\lambda_{\\min}(G)\\ge g>0$"),
    ("P1", 94, 94, "Q\\ge\\|(I-P_{\\mathsf{A}})Y\\|^2"), ("P1", 178, 178, "v\\mid S,y\\sim\\IG(\\nu,b_0\\sy^2+Q^c_S/2)"),
    ("Theory_work/Wave3/W3-POST/STATEMENT.md", 81, 86, "(Rate)"),
    ("Theory_work/Wave3/W3-POST2/numerics/post2_checks_out.txt", 1, 400, "N1 anchored dependence, kappa=0.5"),
    ("Theory_work/Wave3/W3-POST2/numerics/post2_checks_out.txt", 1, 400, "N7 D(b) no BM"),
]
STATUS = [  # (quoted status, source)
    ("PROVED (by this seat, unchecked)", "Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md"),
    ("PROVED (by this seat, unchecked)", "Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md"),
]


def resolve(path):
    path = path.strip("`")
    path = ALIAS.get(path, path)
    if path.startswith("ARC/"):
        path = ARC + path[4:]
    for base in (ROOT, os.path.join(ROOT, "Theory_work"), HERE, os.path.join(HERE, "lemmas")):
        f = os.path.normpath(os.path.join(base, path))
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


labels = set()
for k in ("P1", "P3"):
    labels |= set(re.findall(r"\\label\{([^}]+)\}", "\n".join(lines_of(resolve(k)))))
report, fails, n = [], 0, 0
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
        for m in P_LABEL.finditer(text):
            n += 1
            tag = f"{os.path.relpath(src, HERE)}:{ln} label {m.group(1)}"
            if m.group(1) in labels:
                report.append("ok  " + tag)
            else:
                fails += 1; report.append("FAIL (no such \\label in P1/P3)  " + tag)
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
report.insert(0, f"W3-POST2 citecheck: {n} checks, {fails} failures")
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")
print(report[0]); print("\n".join(r for r in report if not r.startswith("ok")))
