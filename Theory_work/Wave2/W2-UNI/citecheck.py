"""Citation check for W2-UNI (protocol rule 2). (1) Extracts every `path:line` / `path:a-b` citation from STATEMENT.md,
REPORT.md and lemmas/*.md, resolves the path (repo root, Theory_work/, Theory_work/Wave2/, Theory_work/Wave1C/, this
folder, or a ticket lemmas/ folder named by an abbreviation on the same line), and checks that the file exists and the
line range is inside it. (2) Token checks: claim-specific quoted text must occur in the cited line range. (3) Verbatim
status strings quoted in this ticket must occur in their sources. It does not re-verify mathematics.
Writes reviews/CITECHECK.txt. Run: py -3.13 -I citecheck.py"""
import os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TW = os.path.join(ROOT, "Theory_work")
ABBR = {"APP": "Wave2/W2-APP", "LOC2": "Wave2/W2-LOC2", "FACA": "Wave2/W2-FAC-A", "FACB": "Wave2/W2-FAC-B",
        "GROW": "Wave1C/C-GROW", "GEN": "Wave1/W1-GEN", "FIN": "Wave1C/FINAL/sections", "W2-FAC-A": "Wave2/W2-FAC-A",
        "W2-LOC2": "Wave2/W2-LOC2", "W2-APP": "Wave2/W2-APP", "C-DLV": "Wave1C/C-DLV", "C-GROW": "Wave1C/C-GROW"}
SRC = [os.path.join(HERE, "STATEMENT.md")] + sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
if os.path.exists(os.path.join(HERE, "REPORT.md")):
    SRC.append(os.path.join(HERE, "REPORT.md"))
PAT = re.compile(r"`?([A-Za-z0-9_./\-]+\.(?:md|tex|R|py|txt))(?::(\d+)(?:-(\d+))?)`?")


def nlines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().split("\n")


def resolve(rel, line):
    cands = [os.path.join(ROOT, rel), os.path.join(TW, rel), os.path.join(TW, "Wave2", rel), os.path.join(TW, "Wave1C", rel)]
    for ab, d in ABBR.items():
        if re.search(r"(?<![A-Za-z0-9-])" + re.escape(ab) + r"(?![A-Za-z0-9-])", line):
            cands.append(os.path.join(TW, d, rel))
            cands.append(os.path.join(TW, d, "lemmas", os.path.basename(rel)))
    cands.append(os.path.join(HERE, rel))  # this folder last: an abbreviation on the context lines takes precedence
    found = [c for c in dict.fromkeys(os.path.normpath(x) for x in cands) if os.path.isfile(c)]
    if not found:  # fallback: repository-wide basename search (Theory_work excluding Old_Projects, Scripts)
        base = os.path.basename(rel)
        for top in (TW, os.path.join(ROOT, "Scripts")):
            for dp, dn, fn in os.walk(top):
                if "Old_Projects" in dp or "scratch" in dp:
                    continue
                if base in fn and dp.replace(os.sep, "/").endswith(os.path.dirname(rel)):
                    found.append(os.path.join(dp, base))
    return found


out, miss, n = [], 0, 0
for src in SRC:
    L_src = nlines(src)
    for i, line in enumerate(L_src, 1):
        ctx = " ".join(L_src[max(0, i - 5):i])
        for m in PAT.finditer(line):
            rel, a, b = m.group(1), m.group(2), m.group(3)
            if a is None:
                continue
            n += 1
            a = int(a); b = int(b) if b else a
            hits = resolve(rel, ctx)
            ok = [h for h in hits if b <= len(nlines(h))]
            tag = "OK  " if ok else "MISS"
            if not ok:
                miss += 1
            amb = " AMBIGUOUS:" + ",".join(os.path.relpath(h, ROOT) for h in ok[1:]) if len(ok) > 1 else ""
            out.append(f"{tag} {os.path.basename(src)}:{i} -> {rel}:{a}-{b} [{os.path.relpath(ok[0], ROOT) if ok else (hits or 'not found')}]{amb}")

TOKENS = [  # (file, (a, b), token) — claim-specific quotations
    ("Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", (28, 28), "PTV(a₀)"),
    ("Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md", (62, 64), "PTV gives it directly"),
    ("Theory_work/Wave1C/C-GROW/STATEMENT.md", (146, 146), "satisfy separation for every signal scale"),
    ("Scripts/Data_generators/gen_dev_data.R", (18, 28), "0.3*matrix(1,p,p)+0.4*H+0.3*I"),
    ("Scripts/Data_generators/gen_dev_data.R", (32, 41), "step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)"),
    ("Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md", (65, 77), "S₀"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L3_NA_TL.md", (1, 200), "On E_n, Corollary U gives |Z_{T,l}| ≤ √(2P) + κ̄√(2x_k) + ε_n"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L1_uniform_add.md", (1, 400), "Lemma U(d)."),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L5_random_instances.md", (1, 400), "Lemma κ (block compound symmetry)"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md", (1, 200), "|θ*_j|Var(W_j | W_U) ≥ c_Bθ_lo"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md", (1, 200), "Packing fact."),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L4_assembly.md", (1, 200), "only S₀ ⊆ Q, |Q| ≤ K (no bound on |Q|)"),
]
tok_miss = 0
for f, (a, b), tok in TOKENS:
    L = nlines(os.path.join(ROOT, f))
    ok = tok in "\n".join(L[a - 1:b])
    tok_miss += not ok
    out.append(f"{'OK  ' if ok else 'MISS'} TOKEN {f}:{a}-{b} '{tok[:60]}'")

STATUSES = [
    ("Theory_work/Wave2/W2-FAC-A/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave2/W2-FAC-A/REPORT.md", "for the narrowed, flagged target"),
    ("Theory_work/Wave2/W2-FAC-B/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave2/W2-LOC2/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave2/W2-APP/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave2/W2-APP/lemmas/L1_POST.md", "PROVED (by this seat, unchecked)"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md", "R04 (Sol high): VERIFIED-WITH-AMENDMENTS"),
    ("Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md", "PROVED (by this seat, unchecked)"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L4_assembly.md", "VERIFIED"),
    ("Theory_work/Wave1C/C-GROW/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave1/W1-GEN/REPORT.md", "PROVED-CHECKED"),
    ("Theory_work/Wave2/W2-FAC-A/lemmas/L1_uniform_add.md", "VERIFIED-WITH-AMENDMENTS"),
]
st_miss = 0
for f, s in STATUSES:
    p = os.path.join(ROOT, f)
    ok = os.path.isfile(p) and s in open(p, encoding="utf-8", errors="replace").read()
    st_miss += not ok
    out.append(f"{'OK  ' if ok else 'MISS'} STATUS {f}: '{s}'")

head = [f"W2-UNI CITECHECK: {n} path:line citations, {miss} misses; {len(TOKENS)} token checks, {tok_miss} misses; "
        f"{len(STATUSES)} status strings, {st_miss} misses.",
        "Scope: location/token/status check only; it does not re-verify mathematics."]
with open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(head + out) + "\n")
print("\n".join(head))
print("\n".join(l for l in out if l.startswith("MISS")))
