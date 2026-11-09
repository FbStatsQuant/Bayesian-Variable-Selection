r"""Citation check for W2-FAC-PK: every cited path(:line) and every verbatim-quoted status is opened and the quoted text
searched (within the line range when one is cited).  Output: reviews/CITECHECK.txt."""
import os, io
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
C = [  # (path relative to repo root, (lo, hi) or None, expected substring, where cited)
 ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (473, 473), "ls0_cap_plus_mode ? (long long)m.S.size()", "METHOD_REQUIREMENTS Implementation"),
 ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (479, 479), "move_cap_rule", "METHOD_REQUIREMENTS Implementation"),
 ("Scripts/SMC_BVS/core/v3_fit.R", (44, 44), "ls0_scans <- b$ell + K + 1", "METHOD_REQUIREMENTS Implementation"),
 ("Scripts/SMC_BVS/core/v3_fit.R", (45, 45), "ls0_archive = (2 * ls0_scans + 4) * (12 * K + 256) + 96 * ls0_scans + 4 * (8 * W + 4 * K + 96) + 4096", "L4 archive formula"),
 ("Scripts/SMC_BVS/core/v3_fit.R", (62, 62), "v3.1 LS0 worst case", "METHOD_REQUIREMENTS labels"),
 ("Theory_work/Wave1C/FINAL/sections/s6_delivery.tex", (33, 44), r"W_G:=\bar{W}+C\,K\,q(p)", "L4 allocation (s6:33-44)"),
 ("Theory_work/Wave1C/FINAL/sections/s6_delivery.tex", (33, 44), r"(\ell_n+K+1)q(p)(\tau U_K+\tau_0)/100", "L4 P_LS0 (s6:33-44)"),
 ("Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md", (7, 25), "", "L4 (A4:7-25) — file and range exist"),
 ("Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md", None, "OK-WITH-FIXES", "L4 status A4"),
 ("Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md", None, "HOLDS-WITH-AMENDMENTS", "L4 status A1"),
 ("Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md", None, "EXTENDS", "L4 A2 verdict"),
 ("Theory_work/Wave1C/FINAL/sections/s6_delivery.tex", None, "PROVED (A2), checked by A3", "L4/STATEMENT status A2"),
 ("Theory_work/Wave2/W2-FAC-B/STATEMENT.md", None, "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))", "status T38-(0)"),
 ("Theory_work/Wave2/W2-FAC-B/STATEMENT.md", None, "T03♯ \"PROVED; SF VERIFIED (W2-VT03R);", "status T03# (source wraps the line before XF VERIFIED (A-REV2))"),
 ("Theory_work/Wave2/W2-FAC-B/STATEMENT.md", None, "[OP] \"PROVED (by this seat, unchecked)\" inside Theorem GEN \"PROVED-CHECKED\"", "status [OP]"),
("Theory_work/Wave1C/FINAL/sections/s7_impl.tex", None, r"Status: \st{PROVED (by this seat)}", "status Lemma CAP"),
 ("Theory_work/Wave1C/FINAL/sections/s7_impl.tex", None, r"if the move count has reached \texttt{ell}", "loop rule (L3)"),
 ("Theory_work/Wave1C/FINAL/sections/s7_impl.tex", None, "What does not transfer verbatim", "L4.4 cite"),
 ("Theory_work/Wave1C/FINAL/sections/s7_impl.tex", None, "What survives under MR1", "METHOD_REQUIREMENTS Transfer"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L1_cs_reduction.md", None, "## L1.3 Every neighbour of T in closed form", "L0.3"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L1_cs_reduction.md", None, "## L1.5 Size-only terms and the effective multiplier", "L0.5"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L2_start.md", None, "## L2.3 Single-flip improvements", "L1(a)"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L4_path.md", None, "**(d) The multiplier**", "L3 (M2)"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L4_path.md", None, "Thus (E1, E2) if Σ_{j∈T}ξ_j² + kL_n² ≤ n/log n then M_T ≤ ½(1 + C_ρ/log n)", "L3 (M2) small-energy refinement"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L4_path.md", None, "**(e) Truth moves (TL).**", "L3(a)"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L5_assembly.md", None, "## L5.1 (H0) holds on the class", "L4.1"),
 ("Theory_work/Wave2/W2-FAC-B/lemmas/L5_assembly.md", None, "## L5.4 Delivery ((C4))", "L4 (iii)"),
 ("Theory_work/Wave2/W2-FAC-B/reviews/R03_L1L2L3_check_sol.md", None, "", "STATEMENT §6 FACB R03 file exists"),
 ("Theory_work/Wave2/W2-FAC-B/reviews/R04_L4_check_sol.md", None, "", "STATEMENT §6 FACB R04 file exists"),
 ("Theory_work/Wave2/W2-FAC-B/reviews/R05_L5_check_sol.md", None, "", "STATEMENT §6 FACB R05 file exists"),
 ("Theory_work/Wave1/W1-GEN/STATEMENT.md", None, "[OP]", "[OP] source"),
 ("Theory_work/State_of_Project/sections/02_method.tex", None, "LS0: local search from the start mode", "LS0 definition"),
 ("Theory_work/Wave2/W2-FAC-PK/numerics/full_method/NF_summary.md", None, "est_seconds 527,480", "P6 / METHOD_REQUIREMENTS finding"),
 ("Scripts/SMC_BVS/core/v3_run.R", (101, 101), 'ro$ls0_cap <- if (identical(getOption("v3.ls0_cap", "ell_n_plus_mode"), "ell_n")) "ell_n" else "ell_n_plus_mode"', "MR plumbing"),
 ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (394, 394), "bool ls0, ls0_tie_dp, ls0_cap_plus_mode", "MR plumbing"),
 ("Scripts/SMC_BVS/core/cpp/v3_core.cpp", (404, 404), "o.ls0_cap_plus_mode =", "MR plumbing"),
 ("Scripts/SMC_BVS/core/v3_fit.R", (114, 115), "ls0_worst_case = ls0_wc", "MR plumbing preflight call"),
 ("Scripts/SMC_BVS/core/v3_fit.R", (145, 145), "ls0_worst_case = ls0_wc", "MR plumbing escalation preflight"),
]
out = io.StringIO(); miss = 0
for path, rng, sub, where in C:
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        out.write(f"MISS (no file)  {path}  [{where}]\n"); miss += 1; continue
    lines = open(fp, encoding="utf-8", errors="replace").read().split("\n")
    seg = lines[rng[0] - 1: rng[1]] if rng else lines
    ok = (sub in "\n".join(seg)) if sub else (len(seg) > 0 and (rng is None or len(lines) >= rng[1]))
    out.write(("OK    " if ok else "MISS  ") + f"{path}{':%d-%d' % rng if rng else ''}  '{sub[:60]}'  [{where}]\n")
    miss += (not ok)
out.write(f"\n{len(C)} citations checked, {miss} misses\n")
open(os.path.join(os.path.dirname(__file__), "CITECHECK_rerun.txt"), "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue())
