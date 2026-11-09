"""Citation-LOCATION check for W2-LOC2 (protocol rule 2). Limited: checks that each cited path exists, that cited
line ranges contain a claim-specific token, that verbatim statuses quoted in the ticket occur in their sources, that
claim-specific qualifications are present in the summaries, and that deliverables exist. It does not re-verify
mathematics. Writes reviews/CITECHECK.txt. Run: python -I citecheck.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TW = "Theory_work/"
FIN = TW + "Wave1C/FINAL/sections/"
GROW = TW + "Wave1C/C-GROW/lemmas/"
APP = TW + "Wave2/W2-APP/lemmas/"
CITES = [  # (citing file, cited path, (a, b), token in cited lines)
    ("L7_delivery.md", FIN + "s6_delivery.tex", (54, 54), "Add to Proposition F's classes"),
    ("L7_delivery.md", TW + "Wave1C/C-DLV/lemmas/L4_delivery.md", (65, 77), "S₀"),
    ("L2_NAR.md / L1_toolkit.md (c_n)", GROW + "L2_NA_TL.md", (38, 38), "c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2"),
    ("L2_NAR.md (u, Z def)", GROW + "L2_NA_TL.md", (21, 21), "Z_{T,l} := u_{T,l}ᵀε/σ"),
    ("L1_toolkit.md (t_n)", TW + "Wave1/W1-GEN/lemmas/L1_lemmaE.md", (21, 23), "t_n := 4(D + 2) log n"),
    ("L1_toolkit.md (GROW L0 t_n)", GROW + "L0_toolkit.md", (17, 17), "t_n := 4(D + 2 + C_J) log n"),
    ("L5_assembly.md (descent)", GROW + "L1_descent.md", (47, 47), "scores S₀ whenever ℓ ≥ |C ∖ S₀| − 1"),
    ("L4_LOCd.md (L6.5 ladder)", GROW + "L6_random_AR1.md", (353, 353), "K<=n/2"),
    ("L4_LOCd.md (L6.3 H_l)", GROW + "L6_random_AR1.md", (174, 174), "R_n=ceil(2 log n/log(1/r))"),
    ("L4_LOCd.md (APP L3.6 window)", APP + "L3_LOC.md", (109, 109), "r_n := ⌈log log n/t₂⌉"),
    ("L4_LOCd.md (APP LOC-B)", APP + "L3_LOC.md", (175, 175), "(B-χ) s₀(g_n − 1) ≤ (1 − δ₀) log n"),
    ("L3_CTd.md (APP CD)", APP + "L2_CT.md", (41, 41), "Lemma CD (conditional decay)"),
    ("STATEMENT.md (K_n)", TW + "State_of_Project/sections/02_method.tex", (618, 618), "Cap K = min(p, ⌊n/2⌋)"),
    ("STATEMENT.md (VN V2)", APP + "L5_VN.md", (1, 109), "(V2)"),
    ("L7_delivery.md (F-FAC)", TW + "Wave2/W2-FAC-A/lemmas/L7_delivery.md", (22, 22), "Proposition F-FAC"),
    ("L6_poly.md -> L2 Step 2", "Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (62, 62), "Step 2 (events)"),
    ("L6_poly.md -> L2 E_c", "Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (72, 72), "E_c"),
    ("L6_poly.md -> L2 E_e", "Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (79, 79), "adaptive threshold"),
    ("L6_poly.md -> L2 Step 3", "Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (88, 88), "Step 3 (population statistic)"),
    ("L6_poly.md -> L2 Step 4", "Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md", (96, 96), "Step 4 (sample vs population)"),
    ("L6_poly.md -> L3 RB", "Theory_work/Wave2/W2-LOC2/lemmas/L3_CTd.md", (73, 73), "Block inversion gives β_A(l)_v = −Ψ_vl/Ψ_ll"),
    ("L6_poly.md -> L4 atoms", "Theory_work/Wave2/W2-LOC2/lemmas/L4_LOCd.md", (51, 51), "(R2) Atoms"),
    ("L6_poly.md -> L5 path", "Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md", (26, 26), "(b) *Path.*"),
    ("L6_poly.md -> L5 posterior", "Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md", (30, 30), "(c) *Posterior (C-ii).*"),
    ("L6_poly.md -> L5 inputs", "Theory_work/Wave2/W2-LOC2/lemmas/L5_assembly.md", (7, 7), "Inputs (statuses verbatim)"),
    ("L6_poly.md IR -> APP CT algebra", APP + "L2_CT.md", (22, 28), "Schur test"),
    ("L6_poly.md -> GROW L6 ladder", GROW + "L6_random_AR1.md", (329, 329), "Fix ANY maximizer"),
]
STATUSES = [  # verbatim status strings quoted in the ticket, with a source that must contain them
    (FIN + "s3_posterior.tex", "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"),
    (FIN + "s1_setting.tex", "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"),
    (FIN + "s5_hpm.tex", "C-GROW: \\st{PROVED-CHECKED}"),
    (FIN + "s5_hpm.tex", "W1-GEN: \\st{PROVED-CHECKED}"),
    (GROW + "L0_toolkit.md", "lemma check R03 (Codex Sol high, reviews/R03_L0L1L2_check_sol.md): VERIFIED"),
    (GROW + "L2_NA_TL.md", "VERIFIED-WITH-AMENDMENTS (2), applied"),
    (GROW + "L4_assembly.md", "VERIFIED-WITH-AMENDMENTS (1)"),
    (TW + "Wave1/W1-GEN/lemmas/L1_lemmaE.md", "VERIFIED-WITH-AMENDMENTS"),
    (TW + "Wave2/W2-FAC-A/lemmas/L7_delivery.md", "R04 (Sol high): VERIFIED-WITH-AMENDMENTS"),
    (TW + "Wave2/W2-FAC-A/REPORT.md", "PROVED-CHECKED"),
    (TW + "Wave2/W2-APP/REPORT.md", "PROVED-CHECKED"),
    (APP + "L1_POST.md", "PROVED (by this seat, unchecked)"),
]
CONSIST = [  # claim-specific qualifications that must appear
    ("STATEMENT.md", "LOCKED"), ("STATEMENT.md", "NOT locked"), ("STATEMENT.md", "K_n := min(p, ⌊n/2⌋)"),
    ("STATEMENT.md", "min_{k∈S₀}"), ("STATEMENT.md", "INCLUDES sequences"), ("STATEMENT.md", "(C-ii)"),
    ("lemmas/L2_NAR.md", "b_n := √(log n/(1 + L_n²))"), ("lemmas/L3_CTd.md", "H := [p] ∖ U"),
    ("lemmas/L4_LOCd.md", "|θ*_j|Var(W_j | W_U) ≥ c_Bθ_lo"), ("lemmas/L5_assembly.md", "(C-ii)"),
    ("numerics/D1_SUMMARY.md", "observations only"),
    ("REPORT.md", "component port"), ("REPORT.md", "α > 17/2"), ("REPORT.md", "observations only"), ("lemmas/L6_poly.md", "max(2lambda, 1/2) < tau"), ("REPORT.md", "≤ one truth per group"), ("REPORT.md", "increasing-domain"),
]
DELIV = ["STATEMENT.md", "PLAN.md", "LOG.md", "CHECKPOINT.md", "REPORT.md", "lemmas/L1_toolkit.md", "lemmas/L2_NAR.md",
         "lemmas/L3_CTd.md", "lemmas/L4_LOCd.md", "lemmas/L5_assembly.md", "lemmas/L6_poly.md", "lemmas/L7_delivery.md", "numerics/poly_check.py", "numerics/poly_out.txt",
         "numerics/d1_diag.py", "numerics/d1_results.csv", "numerics/d1_out.txt", "numerics/D1_SUMMARY.md",
         "numerics/n4_nar_check.py", "numerics/n4_out.txt"]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
out, bad = [], 0
for who, path, (a, b), tok in CITES:
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        out.append(f"MISS-FILE  {who} -> {path}"); bad += 1; continue
    L = open(fp, encoding="utf-8", errors="replace").read().splitlines()
    if b > len(L):
        out.append(f"MISS-LINES {who} -> {path}:{a}-{b} (file has {len(L)})"); bad += 1; continue
    ok = norm(tok) in norm(" ".join(L[a - 1:b]))
    out.append(f"{'OK   ' if ok else 'MISS '}      {who} -> {path}:{a}-{b} token «{tok}»"); bad += (not ok)
for path, tok in STATUSES:
    fp = os.path.join(ROOT, path)
    ok = os.path.exists(fp) and norm(tok) in norm(open(fp, encoding="utf-8", errors="replace").read())
    out.append(f"{'OK   ' if ok else 'MISS '}      status «{tok}» in {path}"); bad += (not ok)
for f, tok in CONSIST:
    fp = os.path.join(HERE, f)
    ok = os.path.exists(fp) and norm(tok) in norm(open(fp, encoding="utf-8").read())
    out.append(f"{'OK   ' if ok else 'MISS '}      qualification «{tok}» in {f}"); bad += (not ok)
for f in DELIV:
    ok = os.path.exists(os.path.join(HERE, f)); out.append(f"{'OK   ' if ok else 'MISS '}      deliverable {f}"); bad += (not ok)
out.append(f"TOTAL MISSES: {bad}")
open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(out))
