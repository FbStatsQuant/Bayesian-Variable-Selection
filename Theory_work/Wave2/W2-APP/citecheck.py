"""Citation-LOCATION check (limited: token presence in cited lines, verbatim statuses in context, and presence of
claim-specific qualifications in the summaries; it does not re-verify mathematics). Citation check for W2-APP (protocol rule 2). Each entry: (citing file, cited path, line range, token that must
occur in the cited lines, whitespace-normalised). Also checks that every file/dir path named in REPORT.md as a ticket
deliverable exists. Writes reviews/CITECHECK.txt. Run: python -I citecheck.py"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIN = "Theory_work/Wave1C/FINAL/sections/"
CITES = [
    ("STATEMENT.md", FIN + "s3_posterior.tex", (5, 15), "theorem}[S-T"),
    ("STATEMENT.md", FIN + "s3_posterior.tex", (6, 15), "SE$_\\lambda(j_0)$"),
    ("STATEMENT.md", FIN + "s5_hpm.tex", (42, 56), "Canonical certificate"),
    ("STATEMENT.md", FIN + "s5_hpm.tex", (62, 74), "(G4-χ)"),
    ("L3_LOC.md", FIN + "s5_hpm.tex", (16, 16), "some maximiser"),
    ("L1_POST.md", "Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md", (57, 60), "diagonal tightness transfer"),
    ("EMPIRICAL.md", "Theory_work/State_of_Project/sections/06_open_and_plan.tex", (279, 279), "Real data"),
    ("L4_families.md", "Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md", (177, 177), "Not covered: S2"),
    ("L4_families.md", "Theory_work/Wave1C/C-GROW/STATEMENT.md", (150, 156), "Frontier"),
    ("L3_LOC.md", "Scripts/SMC_BVS/core/cpp/v3_core.cpp", (473, 473), "o.ls0_ell + (o.ls0_cap_plus_mode ? (long long)m.S.size()"),
    ("L6_ENUM.md", "Scripts/SMC_BVS/core/v3_preprocess.R", (18, 18), "exact-branch decision (M §6.2): sum_{k<=K} C(p,k) <= (5 H0 + 4 N0) p"),
    ("L6_ENUM.md", "Scripts/SMC_BVS/core/v3_fit.R", (120, 125), "mechanism = \"enumeration\""),
    ("L3_LOC.md", "Theory_work/Wave1C/C-GROW/lemmas/L2_NA_TL.md", (38, 38), "c_n := log(n + 1) + 2 log p"),
    ("L5_VN.md", "Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md", (45, 50), "Score differences"),
    ("L4_families.md", FIN + "s3_posterior.tex", (40, 52), "Neighbour rule"),
    ("L2_CT.md (AR1 spectrum)", "Theory_work/Wave1C/C-GROW/lemmas/L5_instances.md", (23, 24), "Spectrum"),
    ("L4_families.md (F3iii)", "Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md", (130, 140), "a0=(theta_min/2)(1-r^2)/(1+r^2)"),
]
STATUSES = [  # verbatim status strings quoted in the ticket, with a source that must contain them
    (FIN + "s3_posterior.tex", "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"),
    (FIN + "s1_setting.tex", "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"),
    (FIN + "s5_hpm.tex", "W1-GEN: \\st{PROVED-CHECKED}"),
    (FIN + "s5_hpm.tex", "C-GROW: \\st{PROVED-CHECKED}"),
    (FIN + "s5_hpm.tex", "W1-PXN: \\st{PROVED-CHECKED}"),
    (FIN + "s3_posterior.tex", "C-MIS: \\st{PROVED-CHECKED}"),
    (FIN + "s5_hpm.tex", r"Lemma SEL and L8 (C1′) each \st{VERIFIED-WITH-AMENDMENTS}"),
]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
out, bad = [], 0
for who, path, (a, b), tok in CITES:
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        out.append(f"MISS-FILE  {who} -> {path}"); bad += 1; continue
    L = open(fp, encoding="utf-8", errors="replace").read().splitlines()
    if b > len(L):
        out.append(f"MISS-LINES {who} -> {path}:{a}-{b} (file has {len(L)})"); bad += 1; continue
    seg = norm(" ".join(L[a - 1:b]))
    ok = norm(tok) in seg
    out.append(f"{'OK   ' if ok else 'MISS '}      {who} -> {path}:{a}-{b} token «{tok}»"); bad += (not ok)
for path, tok in STATUSES:
    s = norm(open(os.path.join(ROOT, path), encoding="utf-8").read())
    ok = norm(tok) in s
    out.append(f"{'OK   ' if ok else 'MISS '}      status «{tok}» in {path}"); bad += (not ok)
CONSIST = [  # claim-specific qualifications that must appear in each summary (R07 #19)
    ("STATEMENT.md", "p − s₀ ≤ (1 − δ₀) log n"), ("lemmas/L4_families.md", "p − s₀ ≤ (1 − δ₀) log n"),
    ("REPORT.md", "post-enlargement bound"), ("REPORT.md", "≤ 1 truth per block"),
    ("lemmas/L4_families.md", "≤1 truth per block"), ("REPORT.md", "min(K, |𝒩_n|)/log n → ∞"),
    ("lemmas/L3_LOC.md", "Zero-mean reduction"), ("REPORT.md", "component port"), ("REPORT.md", "(EXB) holds eventually"), ("lemmas/L4_families.md", "(EXB) holds eventually"),
    ("STATEMENT.md", "(EXB)"), ("numerics/NUMERICS_LOC_VN.md", "SUPERSESSION NOTICE"),
]
for f, tok in CONSIST:
    ok = norm(tok) in norm(open(os.path.join(HERE, f), encoding="utf-8").read())
    out.append(f"{'OK   ' if ok else 'MISS '}      qualification «{tok}» in {f}"); bad += (not ok)
for f in ["STATEMENT.md", "PLAN.md", "LOG.md", "CHECKPOINT.md", "EMPIRICAL.md", "REPORT.md", "lemmas/L1_POST.md",
          "lemmas/L2_CT.md", "lemmas/L3_LOC.md", "lemmas/L4_families.md", "lemmas/L5_VN.md", "lemmas/L6_ENUM.md", "numerics/LEAD_READING.md",
          "numerics/vn_bound_recheck.py", "numerics/vn_bound_recheck_out.txt", "numerics/ct_check_out.txt", "numerics/post_check_out.txt",
          "numerics/n3_merged.csv", "numerics/n2_results.csv", "numerics/n1_results.csv",
          "numerics/NUMERICS_LOC_VN.md", "data_diag/SUMMARY.md", "data_diag/summary_table.csv"]:
    ok = os.path.exists(os.path.join(HERE, f)); out.append(f"{'OK   ' if ok else 'MISS '}      deliverable {f}"); bad += (not ok)
out.append(f"TOTAL MISSES: {bad}")
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
import sys
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(out))
