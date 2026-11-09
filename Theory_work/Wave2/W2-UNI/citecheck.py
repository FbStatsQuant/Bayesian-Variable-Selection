"""Citation check for W2-UNI (protocol rule 2), v2.1 (after sweeps R05a item 10 and R05b items 9-10).

What it does, exactly:
(1) Extracts every `path:line`, `path:a-b` and `path:a–b` (hyphen or en dash) citation from STATEMENT.md, REPORT.md and
    lemmas/*.md, including shorthand continuations `:a–b` / `:a` that follow a citation on the same line (they inherit
    the preceding path).
(2) Resolves each citation to ONE explicit path by a fixed rule; file existence is never used to choose (R05b-9):
    an explicit prefix (`W2-UNI/…`, `W2-FAC-A/…`, `C-GROW/…`, `Theory_work/…`, `Scripts/…`, `Wave2/…`) wins; otherwise
    the nearest ticket abbreviation (APP, LOC2, FACA, FACB, GROW, GEN, FIN, C-DLV, …) preceding the citation on the same
    source line, or, if the same line has none, the last abbreviation on the previous source line (not for bare top-level
    files STATEMENT.md/REPORT.md/…, which then mean this ticket); otherwise this ticket.
    Bare lemma names (L<digit>…, C_…) map to <ticket>/lemmas/, other paths to <ticket>/. The rule-selected path is printed
    for every citation ("via …"); if it does not exist the citation is a MISS (no fallback, no basename search).
(3) Requires 1 <= a <= b <= (number of lines of the resolved file).
(4) Content: every citation of this ticket's own STATEMENT.md must have a content assertion (a token that must occur in
    the cited range) in SELF_ASSERT; a self-citation without an assertion is a FAIL. Additional claim-specific token
    checks for external sources are in TOKENS. All other external citations are checked for existence and range only;
    their content is audited manually from the excerpt file reviews/CITECHECK_excerpts.md (one entry per citation),
    with the audit recorded in reviews/CITECHECK_AUDIT.md.
(5) Every quoted status in the ticket is extracted automatically and must occur verbatim (word-bounded) in the
    attributed source ticket; its attachment to the specific cited result is checked in the manual audit.
It does not re-verify mathematics. Writes reviews/CITECHECK.txt and reviews/CITECHECK_excerpts.md.
Run: py -3.13 -I citecheck.py"""
import os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TW = os.path.join(ROOT, "Theory_work")
ABBR = {"APP": "Wave2/W2-APP", "LOC2": "Wave2/W2-LOC2", "FACA": "Wave2/W2-FAC-A", "FACB": "Wave2/W2-FAC-B",
        "GROW": "Wave1C/C-GROW", "GEN": "Wave1/W1-GEN", "FIN": "Wave1C/FINAL/sections", "W2-FAC-A": "Wave2/W2-FAC-A",
        "W2-FAC-B": "Wave2/W2-FAC-B", "W2-LOC2": "Wave2/W2-LOC2", "W2-APP": "Wave2/W2-APP", "C-DLV": "Wave1C/C-DLV",
        "C-GROW": "Wave1C/C-GROW", "C-PACK": "Wave1C/C-PACK", "W2-FAC-XA": "Wave2/W2-FAC-XA"}
TICKET_PREFIX = {"W2-UNI": "Wave2/W2-UNI", **{k: v for k, v in ABBR.items() if k.startswith(("W2-", "C-"))}}
SRC = [os.path.join(HERE, "STATEMENT.md")] + sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
if os.path.exists(os.path.join(HERE, "REPORT.md")):
    SRC.append(os.path.join(HERE, "REPORT.md"))
DASH = r"[-–]"
PAT = re.compile(r"([A-Za-z0-9_./\-]+\.(?:md|tex|R|py|txt))((?::\d+(?:" + DASH + r"\d+)?)(?:,\s*:\d+(?:" + DASH + r"\d+)?)*)")
SHORT = re.compile(r"(?<![A-Za-z0-9_.\-])`?:(\d+)(?:" + DASH + r"(\d+))?`?")
ABBR_RE = re.compile(r"(?<![A-Za-z0-9-])(" + "|".join(sorted(map(re.escape, ABBR), key=len, reverse=True)) + r")(?![A-Za-z0-9-])")

# Content assertions for self-citations of STATEMENT.md: (a, b) -> token required in the cited range.
SELF_ASSERT = {
    (143, 151): "R1 Metric toolkit", (50, 53): "Definition (metric locality, LOC_M)",
    (158, 161): "for U = T ∩ B(l, r_n)", (22, 23): "WLOG by scale invariance", (103, 110): "Theorem UNI-0",
    (152, 154): "R2 k = 0 engine inputs", (22, 25): "random design", (22, 26): "Y = Xθ* + Cε", (74, 75): "fixed beta-min θ_lo > 0", (74, 76): "PTV(a₀)", (26, 34): "Method and premises",
    (45, 45): "(Sufficient: λ_min(Σ_n) ≥ c.)", (103, 103): "unit diagonal", (28, 32): "implementation premises",
    (56, 57): "distance 0 within / p between blocks",
}
TOKENS = [  # (file, (a, b), token) — claim-specific quotations in external sources
    ("Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", (28, 28), "PTV(a₀)"),
    ("Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", (62, 64), "PTV gives it directly"),
    ("Theory_work/Wave1C/C-GROW/STATEMENT.md", (146, 146), "satisfy separation for every signal scale"),
    ("Scripts/Data_generators/gen_dev_data.R", (24, 24), "    I,"),
    ("Scripts/Data_generators/gen_dev_data.R", (26, 26), "0.7*H+0.3*I"),
    ("Scripts/Data_generators/gen_dev_data.R", (27, 27), "0.85*H+0.15*I"),
    ("Scripts/Data_generators/gen_dev_data.R", (28, 28), "0.3*matrix(1,p,p)+0.4*H+0.3*I"),
    ("Scripts/Data_generators/gen_dev_data.R", (29, 29), "rho <- 0.4+0.1*((group-1L)%%6L)"),
    ("Scripts/Data_generators/gen_dev_data.R", (32, 42), "step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)"),
    ("Scripts/Data_generators/gen_dev_data.R", (37, 37), "pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)"),
    ("Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md", (65, 77), "S₀"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L3_NA_TL.md", (1, 10**6), "On E_n, Corollary U gives |Z_{T,l}| ≤ √(2P) + κ̄√(2x_k) + ε_n"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L1_uniform_add.md", (1, 10**6), "Lemma U(d)."),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md", (1, 10**6), "Lemma κ (block compound symmetry)"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md", (144, 146), "c²·2023/32500"),
    ("Theory_work/Wave2/W2-FAC-A/STATEMENT.md", (86, 95), "BM-∞"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md", (1, 10**6), "|θ*_j|Var(W_j | W_U) ≥ c_Bθ_lo"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md", (1, 10**6), "Packing fact."),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L4_assembly.md", (1, 10**6), "only S₀ ⊆ Q, |Q| ≤ K (no bound on |Q|)"),
]


def lines_of(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().split("\n")


def ticket_file(tdir, rel):
    """bare lemma names (L<digit>…, C_…) live in <ticket>/lemmas/; any other bare name or relative path is under <ticket>/"""
    if "/" not in rel and re.match(r"(L[0-9]|C_)", rel):
        return os.path.join(tdir, "lemmas", rel)
    return os.path.join(tdir, rel)


def resolve(rel, same_line_before, prev_line):
    """ONE explicit path, existence NOT used to choose (a rule-selected missing file is a MISS):
    (a) explicit prefix (W2-UNI/…, W2-FAC-A/…, C-GROW/…, Theory_work/…, Scripts/…, Wave*/…);
    (b) else the nearest ticket abbreviation preceding the citation on the same source line; if the same line has none,
        the last abbreviation on the previous source line; the path is then ticket_file(<ticket>, rel);
    (c) else this ticket: ticket_file(W2-UNI, rel)."""
    first = rel.split("/")[0]
    if first in TICKET_PREFIX:
        return os.path.normpath(os.path.join(TW, TICKET_PREFIX[first], "/".join(rel.split("/")[1:]))), first
    if first in ("Theory_work", "Scripts"):
        return os.path.normpath(os.path.join(ROOT, rel)), "explicit"
    if first in ("Wave1", "Wave1C", "Wave2", "State_of_Project"):
        return os.path.normpath(os.path.join(TW, rel)), "explicit"
    top_level = "/" not in rel and rel in ("STATEMENT.md", "REPORT.md", "PLAN.md", "LOG.md", "CHECKPOINT.md")
    # [C1-A1] the previous-line rule is not applied to bare top-level ticket files: a bare STATEMENT.md/REPORT.md with no
    # same-line abbreviation means this ticket, so a mis-attribution surfaces as a self-citation content failure.
    ab = ABBR_RE.findall(same_line_before) or ([] if top_level else ABBR_RE.findall(prev_line))
    if ab:
        return os.path.normpath(ticket_file(os.path.join(TW, ABBR[ab[-1]]), rel)), ab[-1]
    return os.path.normpath(ticket_file(HERE, rel)), "W2-UNI"


out, exc = [], ["# CITECHECK excerpts (one entry per citation; for the manual content audit)\n"]
n = miss = self_fail = 0
cache = {}
for src in SRC:
    L_src = lines_of(src)
    for i, line in enumerate(L_src, 1):
        spans = []
        for m in PAT.finditer(line):
            rel = m.group(1)
            for sm in SHORT.finditer(m.group(2)):
                spans.append((rel, int(sm.group(1)), int(sm.group(2) or sm.group(1)), m.start()))
        # shorthand continuations `:a–b` after a citation elsewhere on the line (not inside a PAT match)
        covered = [(m.start(), m.end()) for m in PAT.finditer(line)]
        for sm in SHORT.finditer(line):
            if any(a <= sm.start() < b for a, b in covered):
                continue
            prev = [m for m in PAT.finditer(line[:sm.start()])]
            if prev:
                spans.append((prev[-1].group(1), int(sm.group(1)), int(sm.group(2) or sm.group(1)), prev[-1].start()))
        for rel, a, b, pos in spans:
            n += 1
            path, via = resolve(rel, line[:pos], L_src[i - 2] if i > 1 else "")
            ok_file = os.path.isfile(path)
            if ok_file and path not in cache:
                cache[path] = lines_of(path)
            N = len(cache[path]) if ok_file else 0
            ok_range = ok_file and 1 <= a <= b <= N
            relp = os.path.relpath(path, ROOT).replace(os.sep, "/")
            tag = "OK  " if ok_range else "MISS"
            note = "range"
            if ok_range and os.path.normpath(path) == os.path.normpath(os.path.join(HERE, "STATEMENT.md")):
                tok = SELF_ASSERT.get((a, b))
                if tok is None or tok not in "\n".join(cache[path][a - 1:b]):
                    tag, note = "FAIL", f"self-citation content assertion {'missing' if tok is None else 'not found'}"
                    self_fail += 1
                else:
                    note = f"content '{tok}'"
            if not ok_range:
                miss += 1
            out.append(f"{tag} {os.path.basename(src)}:{i} -> {relp}:{a}-{b} [via {via}; {note}]")
            if ok_range:
                txt = " ".join(x.strip() for x in cache[path][a - 1:min(b, a + 5)])[:400]
                exc.append(f"* **{os.path.basename(src)}:{i}** → `{relp}:{a}-{b}`\n  - context: {line.strip()[:300]}\n"
                           f"  - cited: {txt}\n")

tok_miss = 0
for f, (a, b), tok in TOKENS:
    L = lines_of(os.path.join(ROOT, f))
    ok = tok in "\n".join(L[a - 1:b])
    tok_miss += not ok
    out.append(f"{'OK  ' if ok else 'MISS'} TOKEN {f}:{a}-{b} '{tok[:60]}'")
# (5) every quoted status in the ticket: extracted automatically (quotes "…" containing a status keyword, across line
# breaks), attributed to a source ticket (nearest abbreviation/ticket name in the 300 characters before the quote; if none,
# the set of cited tickets), and required to occur VERBATIM (whitespace-normalised, Markdown ** removed) in that ticket's
# .md/.tex files, with a word boundary after it (so "VERIFIED" does not match "VERIFIED-WITH-AMENDMENTS"). This checks
# existence of the exact status string in the attributed source; that it is attached to the specific cited result is
# part of the manual audit (every occurrence is listed in CITECHECK_excerpts.md).
KW = re.compile(r"PROVED|VERIFIED|AUDITED|OPEN|CHECKED|REFUTED|STUCK|PARTIAL")
NAMES = {**ABBR, "W1-GEN": "Wave1/W1-GEN", "FAC-A": "Wave2/W2-FAC-A", "FAC-B": "Wave2/W2-FAC-B"}
NAME_RE = re.compile(r"(?<![A-Za-z0-9-])(" + "|".join(sorted(map(re.escape, NAMES), key=len, reverse=True)) + r")(?![A-Za-z0-9-])")
CITED = sorted(set(NAMES.values()))
corpus = {}


def ticket_text(d):
    if d not in corpus:
        parts = []
        for dp, dn, fn in os.walk(os.path.join(TW, d)):
            if "scratch" in dp.lower():
                continue
            for f in fn:
                if f.endswith((".md", ".tex")):
                    parts.append(open(os.path.join(dp, f), encoding="utf-8", errors="replace").read())
        corpus[d] = re.sub(r"\s+", " ", "\n".join(parts).replace("**", ""))
    return corpus[d]


def norm(x):
    return re.sub(r"\s+", " ", x.replace("**", "")).strip()


st_n = st_miss = 0
exc.append("\n# Quoted status occurrences (for the manual audit: is the status attached to the cited result?)\n")
for src in SRC:
    raw = open(src, encoding="utf-8").read()
    for m in re.finditer(r'"([^"]{3,220})"', raw):
        q = norm(m.group(1))
        if not KW.search(q) or "\n\n" in m.group(1):
            continue
        st_n += 1
        line_no = raw.count("\n", 0, m.start()) + 1
        before = raw[max(0, m.start() - 300):m.start()]
        nm = NAME_RE.findall(before)
        dirs = [NAMES[nm[-1]]] if nm else CITED
        pat = re.compile(re.escape(q) + r"(?![A-Za-z0-9*-])")
        hit = [d for d in dirs if pat.search(ticket_text(d))]
        ok = bool(hit)
        st_miss += not ok
        where = (nm[-1] if nm else "cited-ticket set")
        out.append(f"{'OK  ' if ok else 'MISS'} STATUS {os.path.basename(src)}:{line_no} \"{q[:80]}\" [attributed: {where}; found in: {','.join(hit) or '-'}]")
        exc.append(f"* STATUS **{os.path.basename(src)}:{line_no}** \"{q}\" → {where}; context: {norm(raw[max(0, m.start() - 160):m.end() + 40])}\n")

head = [f"W2-UNI CITECHECK v2: {n} path:line citations (incl. shorthand continuations), {miss} existence/range misses, "
        f"{self_fail} self-citation content failures; {len(TOKENS)} token checks, {tok_miss} misses; "
        f"{st_n} quoted status occurrences (automatic extraction), {st_miss} misses.",
        "Scope: one explicit resolution per citation (no alternatives accepted); range 1<=a<=b<=lines; content asserted "
        "automatically for every self-citation of STATEMENT.md and for the TOKENS list; all other citations: existence/"
        "range here, content audited manually from reviews/CITECHECK_excerpts.md (see reviews/CITECHECK_AUDIT.md). "
        "Does not re-verify mathematics."]
with open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(head + out) + "\n")
with open(os.path.join(HERE, "reviews", "CITECHECK_excerpts.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(exc))
print("\n".join(head))
for o in out:
    if not o.startswith("OK"):
        print(o)
