"""Citation check for W3-SCR (anti-hallucination rule: no claim without a file).
(1) Extracts every `path:line` / `path:a-b` citation (also comma-continued ranges `a-b, c-d` after a path) from
    STATEMENT.md, CODE_CHECK.md, ASSUMPTION_MAP.md, REPORT.md and lemmas/*.md.
(2) Resolves the path by a fixed rule: explicit `Theory_work/...` or `Scripts/...` from the repo root; `cpp/...`,
    `v3_*.R` relative to Scripts/SMC_BVS/core/; `tests/...` relative to Scripts/SMC_BVS/; `numerics/...`, `reviews/...`,
    `lemmas/...` relative to this ticket. No basename search. A missing file or a range outside the file is a FAIL.
(3) Content assertions (TOKENS): for the code facts CC1-CC6 the cited range must contain the given token.
Writes reviews/CITECHECK.txt. Run: py -3.13 -I citecheck.py"""
import os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CORE = os.path.join(ROOT, "Scripts", "SMC_BVS", "core")
SRC = [os.path.join(HERE, f) for f in ("STATEMENT.md", "CODE_CHECK.md", "ASSUMPTION_MAP.md", "REPORT.md") if os.path.exists(os.path.join(HERE, f))]
SRC += sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
PAT = re.compile(r"([A-Za-z0-9_./\-]+\.(?:md|tex|R|py|txt|h|cpp)):(\d+(?:[-–]\d+)?(?:,\s*\d+(?:[-–]\d+)?)*)")
TOKENS = [  # (path suffix, line inside range, token that must occur in the cited range)
    ("cpp/v3_engine.h", 397, "continue"), ("cpp/v3_engine.h", 408, "best.F > C.F"), ("cpp/v3_engine.h", 410, "move_limit"),
    ("cpp/v3_engine.h", 414, "local_certified = true"), ("cpp/v3_engine.h", 391, "eval(q, ME_LOCAL)"), ("cpp/v3_engine.h", 407, "scan_complete"),
    ("cpp/v3_core.cpp", 456, "local_search(led.hpmS"), ("cpp/v3_core.cpp", 476, "PH_LS0"), ("cpp/v3_core.cpp", 352, "scanned_centres"),
    ("v3_run.R", 146, "local_certified <- FALSE"), ("v3_run.R", 179, "identical(as.integer(out$hpm)"), ("v3_run.R", 194, "cert_final || cert_ls0"),
    ("v3_run.R", 197, "final_local_limit || out$ls0_local_limit"), ("v3_exact.R", 15, 'status == "exact"'), ("v3_fit.R", 76, "local_certified = FALSE"),
    ("cpp/v3_score.h", 223, "D->nu * std::log(arg)"), ("cpp/v3_score.h", 65, "lchoose_d(2.0 * p - 1.0, k)"), ("cpp/v3_ledger.h", 85, "hpm_better"),
    ("cpp/v3_ledger.h", 112, "offer_stores"), ("v3_preprocess.R", 66, "length(x) - 1"),
]


def resolve(path):
    if path.startswith(("Theory_work/", "Scripts/")): return os.path.join(ROOT, path)
    if path.startswith("cpp/") or re.match(r"v3_[a-z]+\.R$", path): return os.path.join(CORE, path)
    if path.startswith("tests/"): return os.path.join(ROOT, "Scripts", "SMC_BVS", path)
    if path.startswith(("numerics/", "reviews/", "lemmas/")): return os.path.join(HERE, path)
    if re.match(r"v3_[a-z]+\.(h|cpp)$", path): return os.path.join(CORE, "cpp", path)
    return os.path.join(HERE, path)


out = []; nfail = 0; ncite = 0; cited = {}
for src in SRC:
    for ln, line in enumerate(open(src, encoding="utf-8"), 1):
        for m in PAT.finditer(line):
            path, ranges = m.group(1), m.group(2)
            full = resolve(path)
            for rg in re.split(r",\s*", ranges):
                ncite += 1
                a, b = (re.split(r"[-–]", rg) + [None])[:2]; a = int(a); b = int(b) if b else a
                tag = f"{os.path.relpath(src, HERE)}:{ln}  {path}:{rg}"
                if not os.path.exists(full):
                    out.append(f"FAIL (missing file) {tag} -> {os.path.relpath(full, ROOT)}"); nfail += 1; continue
                lines = open(full, encoding="utf-8", errors="replace").read().split("\n")
                if not (1 <= a <= b <= len(lines)):
                    out.append(f"FAIL (range) {tag} (file has {len(lines)} lines)"); nfail += 1; continue
                cited.setdefault(os.path.relpath(full, ROOT).replace("\\", "/"), []).append((a, b))
                out.append(f"ok   {tag} -> {os.path.relpath(full, ROOT)}")
ntok = 0
for suffix, at, token in TOKENS:
    key = [k for k in cited if k.endswith(suffix)]
    hit = [(k, a, b) for k in key for a, b in cited[k] if a <= at <= b]
    if not hit:
        out.append(f"FAIL (token: no citation covers {suffix}:{at})"); nfail += 1; continue
    k, a, b = hit[0]; lines = open(os.path.join(ROOT, k), encoding="utf-8", errors="replace").read().split("\n")
    if token in lines[at - 1]:
        ntok += 1; out.append(f"ok   token '{token}' at {suffix}:{at}")
    else:
        out.append(f"FAIL (token '{token}' not on {suffix}:{at}: {lines[at - 1].strip()[:80]})"); nfail += 1
out.append(f"\nSUMMARY: {ncite} citations in {len(SRC)} files, {ntok}/{len(TOKENS)} content tokens verified, {nfail} failures")
os.makedirs(os.path.join(HERE, "reviews"), exist_ok=True)
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(out[-1]); [print(o) for o in out if o.startswith("FAIL")]
