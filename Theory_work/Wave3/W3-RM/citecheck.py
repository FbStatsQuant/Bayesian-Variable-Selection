"""Citation check for W3-RM (Wave1C protocol rule 2), v2 (after sweep R08 findings 6, 15).

Scope and limits (read before trusting the result):
* It checks the citations it can EXTRACT: `path:line`, `path:a-b` / `path:a–b`, same-reference lists `path:a-b, c-d`,
  backticked continuations `:a` / `:a-b` later on the same line (they inherit the last full citation on that line), and
  alias citations ALIAS:range in lemmas/L3_SANDR.md (G6, G3, G0, APP, D4, D1, UNI, RM) and START/RUN/ENGINE in
  lemmas/L5_E4.md, lemmas/L0_core.md. A continuation with no full citation before it on its line is reported UNSUPPORTED
  (a failure). References split across lines are not parsed as one path; such references must be written on one line.
* For each extracted range it checks that the resolved file exists and 1 <= a <= b <= number of lines. This is a
  syntactic range check. Whether the cited lines SAY what is claimed is checked only for the TOKENS list below and by the
  human reviewers (sweep R08 sampled 73 ranges).
* Quoted statuses ("PROVED…", "VERIFIED…") are checked for verbatim existence in the cited tickets' files, not for
  attachment to a particular result.

Resolution rule (fixed; file existence is never used to choose):
 1. A path starting with Theory_work/ or Scripts/ is repository-relative.
 2. A path starting with ../ is relative to the directory of the citing file.
 3. Same-line context = the nearest ticket abbreviation (ABBR) before the citation on the same line.
 4. A file name in OWN (this ticket's lemma files) resolves to this ticket's lemmas/.
 5. A bare name, or lemmas/NAME, or cpp/NAME, with NAME in KNOWN (names unambiguous among this ticket's sources) resolves
    by the table — unless the same-line context names a DIFFERENT ticket, which is a CONFLICT (failure).
 6. Any other path with a directory part is taken relative to the same-line context ticket, else to this ticket.
 7. Any other bare name is taken in the same-line context ticket, else (for lemma-like names) the last abbreviation on
    the previous line, else this ticket; lemma-like names go to <ticket>/lemmas/.
Exit code 1 if any check fails. Writes reviews/CITECHECK.txt. Run: py -3.13 -I citecheck.py
"""
import os, re, glob, sys, posixpath
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OWNDIR = "Theory_work/Wave3/W3-RM"
ABBR = {"GROW": "Theory_work/Wave1C/C-GROW", "GEN": "Theory_work/Wave1/W1-GEN", "APP": "Theory_work/Wave2/W2-APP",
        "LOC2": "Theory_work/Wave2/W2-LOC2", "UNI": "Theory_work/Wave2/W2-UNI", "N3": "Theory_work/Wave1/W1-N3",
        "PACK": "Theory_work/Wave1C/C-PACK", "DLV": "Theory_work/Wave1C/C-DLV", "ENG": "Theory_work/Wave1C/C-ENG",
        "FIN": "Theory_work/Wave1C/FINAL/sections", "SoP": "Theory_work/State_of_Project/sections",
        "CORE": "Scripts/SMC_BVS/core"}
ALIAS = {"G6": "Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md", "G3": "Theory_work/Wave1C/C-GROW/lemmas/L3_sandwich.md",
         "G0": "Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md", "D4": "Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md",
         "D1": "Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md", "RM": "Theory_work/Wave3/W3-RM/STATEMENT.md",
         "START": "Scripts/SMC_BVS/core/cpp/v3_start.h", "RUN": "Scripts/SMC_BVS/core/cpp/v3_core.cpp",
         "ENGINE": "Scripts/SMC_BVS/core/cpp/v3_engine.h"}
ALIAS_L3 = {"APP": "Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", "UNI": "Theory_work/Wave2/W2-UNI/lemmas/L2_k0.md"}
OWN = {"L0_core.md", "L1_fixed.md", "L1b_rss.md", "L2_NAF.md", "L3_SANDR.md", "L3b_rate.md", "L4_formR.md", "L5_E4.md",
       "L7_examples.md"}
KNOWN = {"L1_descent.md": "Theory_work/Wave1C/C-GROW/lemmas", "L3_sandwich.md": "Theory_work/Wave1C/C-GROW/lemmas",
         "L2_NA_TL.md": "Theory_work/Wave1C/C-GROW/lemmas", "L0_toolkit.md": "Theory_work/Wave1C/C-GROW/lemmas",
         "L6_random_AR1.md": "Theory_work/Wave1C/C-GROW/lemmas", "L1_lemmaE.md": "Theory_work/Wave1/W1-GEN/lemmas",
         "L7_counterexample.md": "Theory_work/Wave1/W1-GEN/lemmas",
         "L1_toolkit.md": "Theory_work/Wave2/W2-LOC2/lemmas", "L2_NAR.md": "Theory_work/Wave2/W2-LOC2/lemmas",
         "L4_LOCd.md": "Theory_work/Wave2/W2-LOC2/lemmas", "L2_k0.md": "Theory_work/Wave2/W2-UNI/lemmas",
         "L5_VN.md": "Theory_work/Wave2/W2-APP/lemmas", "L3_LOC.md": "Theory_work/Wave2/W2-APP/lemmas",
         "L1_POST.md": "Theory_work/Wave2/W2-APP/lemmas", "TDP_E.md": "Theory_work/Wave1C/C-ENG/lemmas",
         "I1_e4_replacement.md": "Theory_work/Wave1C/C-PACK/lemmas", "L4_delivery.md": "Theory_work/Wave1C/C-DLV/lemmas",
         "v3_core.cpp": "Scripts/SMC_BVS/core/cpp", "v3_start.h": "Scripts/SMC_BVS/core/cpp",
         "v3_engine.h": "Scripts/SMC_BVS/core/cpp", "v3_run.R": "Scripts/SMC_BVS/core", "v3_fit.R": "Scripts/SMC_BVS/core"}
TOPLEVEL = {"STATEMENT.md", "REPORT.md", "SHARPNESS.md", "PLAN.md", "LOG.md", "ASSUMPTION_MAP.md"}
SRC = [os.path.join(HERE, f) for f in ("STATEMENT.md", "SHARPNESS.md", "ASSUMPTION_MAP.md", "REPORT.md")
       if os.path.exists(os.path.join(HERE, f))]
SRC += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
D = r"[-–]"
RNG = r"\d+(?:" + D + r"\d+)?"
PAT = re.compile(r"([A-Za-z0-9_./\-]+\.(?:md|tex|R|py|txt|h|cpp)):(" + RNG + r"(?:,\s*:?" + RNG + r")*)")
APAT = re.compile(r"(?<![A-Za-z0-9_./`])(" + "|".join(list(ALIAS) + ["APP", "UNI"]) + r"):(" + RNG + r"(?:,\s*:?" + RNG + r")*)")
SHORT = re.compile(r"`:(" + RNG + r")`")
ABBR_RE = re.compile(r"(?<![A-Za-z0-9-])(" + "|".join(ABBR) + r")(?![A-Za-z0-9-])")
LEMMA_LIKE = re.compile(r"(L\d|I\d|TDP|C_)")
TOKENS = [
    ("Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md", (42, 57), "reaches S₀ after exactly"),
    ("Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md", (9, 11), "|Q| ≤ K"),
    ("Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md", (57, 61), "no bound on |Q| enters"),
    ("Theory_work/Wave1C/C-GROW/lemmas/L3_sandwich.md", (13, 13), "Lemma L3"),
    ("Theory_work/Wave1C/C-GROW/lemmas/L3_sandwich.md", (88, 93), "η < η_A"),
    ("Theory_work/Wave1C/C-GROW/lemmas/L2_NA_TL.md", (38, 66), "Lemma L2.3"),
    ("Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md", (65, 70), "𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ"),
    ("Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md", (11, 16), "Operational closure"),
    ("Theory_work/Wave1/W1-GEN/lemmas/L7_counterexample.md", (14, 36), "λ_min(Σ) ≥ 1 − a"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (23, 36), "(R3)"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md", (33, 36), "FIXED beta-min"),
    ("Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", (28, 28), "PTV(a₀)"),
    ("Theory_work/Wave2/W2-APP/lemmas/L5_VN.md", (23, 26), "Under (F16) and VNF(κ_n)"),
    ("Theory_work/Wave2/W2-UNI/STATEMENT.md", (103, 110), "Theorem UNI-0"),
    ("Theory_work/Wave2/W2-UNI/lemmas/L2_k0.md", (139, 149), "(R3) variance ratio"),
    ("Theory_work/Wave2/W2-LOC2/STATEMENT.md", (76, 85), "Theorem LOC-BF"),
    ("Theory_work/Wave1C/C-GROW/STATEMENT.md", (119, 126), "any block partition with blocks of size ≤ 16"),
    ("Theory_work/Wave1/W1-GEN/STATEMENT.md", (145, 155), "(C6)"),
    ("Theory_work/Wave2/W2-FAC-PK/REPORT.md", (24, 33), "Theorem NEG"),
    ("Theory_work/Wave2/W2-FAC-PK/REPORT.md", (24, 33), "Theorem PATH"),
    ("Theory_work/Wave1/W1-N3/STATEMENT.md", (113, 126), "always a maximiser of π₀"),
    ("Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md", (3, 3), "PROVED (by this seat, unchecked)"),
    ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (469, 469), "start_mode(st, 1000000, o.ls0_tie_dp)"),
    ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (476, 476), "E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0)"),
    ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (392, 392), "const Start& st = *h->st"),
    ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (404, 404), "ls0_cap"),
    ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (473, 475), "ls0_cap_plus_mode"),
    ("Scripts/SMC_BVS/core/cpp/v3_start.h", (303, 303), "mode_tie_dp(st, dp)"),
    ("Scripts/SMC_BVS/core/cpp/v3_start.h", (261, 261), "no tight path"),
    ("Scripts/SMC_BVS/core/cpp/v3_engine.h", (413, 415), "local_certified = true"),
    ("Scripts/SMC_BVS/core/cpp/v3_engine.h", (89, 100), "led->event"),
    ("Scripts/SMC_BVS/core/v3_run.R", (88, 101), "ell_n_plus_mode"),
]


def resolve(path, line, prev, pos, srcfile):
    """Return (resolved repository-relative path, note) or (None, reason) on a rule failure."""
    if path.startswith(("Theory_work/", "Scripts/")):
        return (path, "rule 1") if ".." not in path.split("/") else (None, "dot-dot in absolute citation")
    srcdir = posixpath.dirname(os.path.relpath(srcfile, ROOT).replace(os.sep, "/"))
    if path.startswith("../"):
        return posixpath.normpath(posixpath.join(srcdir, path)), "rule 2"
    ctx = None
    for mm in ABBR_RE.finditer(line[:pos]):
        ctx = mm
    ctxdir = ABBR[ctx.group(1)] if ctx else None
    d, name = posixpath.dirname(path), posixpath.basename(path)
    if name in OWN and d in ("", "lemmas"):
        return OWNDIR + "/lemmas/" + name, "rule 4"
    if name in KNOWN and d in ("", "lemmas", "cpp"):
        tgt = KNOWN[name]
        if ctxdir is not None and not (tgt == ctxdir or tgt.startswith(ctxdir + "/")):
            return None, f"CONFLICT: same-line context {ctx.group(1)} vs table {tgt}"
        if d and not tgt.endswith("/" + d):
            return None, f"CONFLICT: directory {d}/ vs table {tgt}"
        return tgt + "/" + name, "rule 5"
    if d:
        return (ctxdir or OWNDIR) + "/" + path, "rule 6"
    if ctxdir is None and name not in TOPLEVEL and prev is not None and LEMMA_LIKE.match(name):
        for mm in ABBR_RE.finditer(prev):
            ctxdir = ABBR[mm.group(1)]
    tick = ctxdir or OWNDIR
    if LEMMA_LIKE.match(name) and not tick.endswith("sections"):
        return tick + "/lemmas/" + name, "rule 7"
    return tick + "/" + name, "rule 7"


def ranges(spec):
    out = []
    for part in re.split(r",\s*:?", spec):
        ab = re.split(D, part)
        out.append((int(ab[0]), int(ab[-1])))
    return out


def nlines(rel):
    f = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.isfile(f):
        return None
    with open(f, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


fails, total, lines_out = [], 0, []
# resolver self-tests (R08 finding 6): wrong directory and conflicting ticket must not be accepted
t1 = resolve("wrong-directory/L1_toolkit.md", "see `wrong-directory/L1_toolkit.md:28-32`", None, 5, os.path.join(HERE, "STATEMENT.md"))
t2 = resolve("lemmas/L1_toolkit.md", "GROW `lemmas/L1_toolkit.md:28-32`", None, 6, os.path.join(HERE, "STATEMENT.md"))
t3 = resolve("L1_toolkit.md", "LOC2 `L1_toolkit.md:28-32`", None, 6, os.path.join(HERE, "STATEMENT.md"))
st_ok = (t1[0] is None or nlines(t1[0]) is None) and t2[0] is None and t3[0] == "Theory_work/Wave2/W2-LOC2/lemmas/L1_toolkit.md"
lines_out.append(f"{'SELFTEST-OK  ' if st_ok else 'SELFTEST-FAIL'} wrong-directory -> {t1}; conflicting ticket -> {t2}; correct -> {t3}")
if not st_ok:
    fails.append(lines_out[-1])
for src in SRC:
    rel_src = os.path.relpath(src, HERE).replace(os.sep, "/")
    with open(src, encoding="utf-8") as fh:
        L = fh.read().splitlines()
    prev = None
    for i, line in enumerate(L, 1):
        found, spans = [], []
        for m in PAT.finditer(line):
            res, note = resolve(m.group(1), line, prev, m.start(), src)
            found.append((res, note, m.group(2), m.group(0), m.end()))
            spans.append((m.start(), m.end()))
        if rel_src in ("lemmas/L3_SANDR.md", "lemmas/L5_E4.md", "lemmas/L0_core.md"):
            for m in APAT.finditer(line):
                al = m.group(1)
                if al in ("APP", "UNI") and rel_src != "lemmas/L3_SANDR.md":
                    continue
                found.append((ALIAS.get(al) or ALIAS_L3[al], "alias", m.group(2), m.group(0), m.end()))
                spans.append((m.start(), m.end()))
        for m in SHORT.finditer(line):  # backticked continuation `:a-b`
            if any(a <= m.start() < b for a, b in spans):
                continue
            before = [f for f in found if f[4] <= m.start()]
            if not before:
                total += 1
                lines_out.append(f"UNSUPPORTED {rel_src}:{i}  {m.group(0)}  (continuation without a citation before it on the line)")
                fails.append(lines_out[-1])
                continue
            last = max(before, key=lambda f: f[4])
            found.append((last[0], "continuation of " + last[3], m.group(1), m.group(0), m.end()))
        for res, note, spec, raw, _ in found:
            body = nlines(res) if res else None
            for a, b in ranges(spec):
                total += 1
                ok = body is not None and 1 <= a <= b <= len(body)
                why = "" if ok else ("  [" + note + "]" if res is None else ("  [file not found]" if body is None else "  [range]"))
                lines_out.append(f"{'OK  ' if ok else 'MISS'} {rel_src}:{i}  {raw}  ->  {res}:{a}-{b}  ({note})" + why)
                if not ok:
                    fails.append(lines_out[-1])
        prev = line
tok_fail = []
for rel, (a, b), tok in TOKENS:
    body = nlines(rel)
    ok = body is not None and b <= len(body) and tok in "\n".join(body[a - 1:b])
    lines_out.append(f"{'TOK-OK  ' if ok else 'TOK-FAIL'} {rel}:{a}-{b}  «{tok}»")
    if not ok:
        tok_fail.append(lines_out[-1])
STAT = re.compile(r"\"((?:PROVED|VERIFIED)[^\"]{0,80})\"")
allstat = set()
for src in SRC:
    with open(src, encoding="utf-8") as fh:
        allstat |= set(STAT.findall(fh.read()))
corpus = []
STAT_DIRS = ["Wave1/W1-GEN", "Wave1/W1-N3", "Wave1/W1-PXN", "Wave1C/C-GROW", "Wave1C/C-PACK", "Wave1C/C-DLV", "Wave1C/C-ENG",
             "Wave1C/FINAL/sections", "Wave2/W2-APP", "Wave2/W2-LOC2", "Wave2/W2-UNI", "Wave2/W2-FAC-PK",
             "State_of_Project/sections"]
for d in STAT_DIRS:
    for pat in ("*.md", "*.tex", os.path.join("lemmas", "*.md")):
        for f in glob.glob(os.path.join(ROOT, "Theory_work", d.replace("/", os.sep), pat)):
            with open(f, encoding="utf-8", errors="replace") as fh:
                corpus.append(fh.read())
big = "\n".join(corpus)
stat_fail = [st for st in sorted(allstat) if st not in big]
for st in sorted(allstat):
    lines_out.append(f"{'STAT-FAIL' if st in stat_fail else 'STAT-OK  '} \"{st}\"")
hdr = [f"W3-RM citation check v2: {total} extracted citation ranges, {len(fails)} failures (misses/conflicts/unsupported/selftest); "
       f"{len(TOKENS)} token assertions, {len(tok_fail)} failures; {len(allstat)} quoted statuses, {len(stat_fail)} not found verbatim. "
       f"(Range check + listed tokens only; see the docstring for what is NOT checked.)", ""]
with open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(hdr + lines_out) + "\n")
print(hdr[0])
for x in fails + tok_fail:
    print(x)
for x in stat_fail:
    print("STAT-FAIL", x)
sys.exit(1 if (fails or tok_fail or stat_fail) else 0)
