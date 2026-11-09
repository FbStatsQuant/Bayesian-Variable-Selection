# R05a — disposition of the pre-pause exhaustive sweep (Codex gpt-6.1-sol, xhigh)

Reviewer reply verbatim: `reviews/R05a_sweep_sol.md` (written 2026-11-09 11:07 CST as `R05_sweep_sol.md`, just before the
pause; renamed R05a on resumption so that the fresh Astra sweep requested on resumption is R05b; content unchanged).
The reviewer ran at xhigh before the binding effort cap of 2026-11-09; it is kept as an extra layer, not as the protocol
sweep (the protocol sweep is R05b, gpt-6-astra high). Counts: FATAL 0, MAJOR 1, MINOR 14, NIT 3. All 18 fixed (2026-11-09,
~15:00 CST, resuming lead). Change markers [R05a-#] in the files.

| # | Class | Disposition |
|---|---|---|
| 1 | MAJOR | FIXED. FAC-L containment restricted to its fixed-positive-beta-min subclass; BM-∞ relaxation listed as a separate imported result: STATEMENT (iii) Containment + §5 FAC-L row; L4_k1 Remark (1); C_corollaries row 8; REPORT. Verified the premise: FACA STATEMENT §3 (H0)/BM-∞ admits vanishing signals (`W2-FAC-A/STATEMENT.md:86-95`). No UNI-1 change. |
| 2 | MINOR | FIXED. STATEMENT (i′) now opens with setting (R), fixed s₀, (A3) coefficient bounds without PTV, method premises; "not an (E)-design theorem". C-i/C-ii split kept. |
| 3 | MINOR | FIXED. REPORT §6: λ_max ≤ C is part of LOC_M; replaced the "no condition on λ_max" sentence with the reviewer's text. |
| 4 | MINOR | FIXED. REPORT §6: exclusivity claim replaced by the SHARP/FAC-B wording (necessity and exclusivity not established). |
| 5 | MINOR | FIXED. STATEMENT (iii): LS0 move count stated on Sand ∩ NA ∩ TL for the uninterrupted deterministic search; delivered run / enumeration distinguished (FACA wording). L4_k1's theorem already carried the event. |
| 6 | MINOR | FIXED. REPORT flag 1 and synopsis: "merged cap suffices uniformly; admitted subclasses can require order-p deletion paths"; "every start maximiser contains S₀ …". No full-start theorem asserted. |
| 7 | MINOR | FIXED. C_corollaries row 9: signal scale c_sig introduced (θ* = c_sig × unit-scale pattern, gen_dev_data.R:37); τ₀ = c_sig²·7/2080, c_sig²·2023/32500; c keeps its spectral meaning. |
| 8 | MINOR | FIXED. Diagonal-Ψ formula in absolute values: q_j = |λ_j|/√(1 − λ_j²), κ′ = max q_j, c_𝒢 = min q_j², κ = max q / min q. Reviewer's example (−0.4, −0.7) gives 2.2459 with the new formula. |
| 9 | MINOR | FIXED. L6 mapping rule replaced by the reviewer's two-direction rule. |
| 10 | MINOR | FIXED. citecheck.py rewritten (v2): one explicit resolution per citation by a fixed rule (no alternatives accepted; a rule-selected missing file is a MISS), hyphen/en-dash ranges and shorthand continuations expanded, 1 ≤ a ≤ b ≤ length, automatic content assertions for every self-citation of STATEMENT.md (missing assertion = FAIL), expanded claim-specific tokens (S1/S3/S4/S5/S6, truth layout, FACA τ₀, FACA BM-∞); every other citation is labelled existence/range-only, and its content is audited manually from `reviews/CITECHECK_excerpts.md` → `reviews/CITECHECK_AUDIT.md`. The hand-appended resolution note is gone. Two mis-resolving citations made explicit (L2 §10 LOC2 L7; L2 §12 `W2-UNI/STATEMENT.md`). |
| 11 | MINOR | FIXED. All self-citations of STATEMENT updated to v1.1.2 lines (L1: R1 :143-151, LOC_M :50-53, R3(b) :158-161, setting :22-23; L2: UNI-0 :103-110, R2 :152-154, unit diagonal :103, …) and each is now content-asserted by citecheck v2 (so later drift fails the check). |
| 12 | MINOR | FIXED. S5 → `gen_dev_data.R:28`; combined definitions → `:18-29` with per-scenario lines (S1 :24, S3 :26, S4 :27, S6 :29); truth layout :32-42; tokens for each in citecheck. |
| 13 | MINOR | FIXED. n1_metric.py docstring now describes the fitted slopes as exploratory and points to n2 for the analytic CT_M ratio check (code and output unchanged). |
| 14 | MINOR | FIXED. Exact κ values restricted to N3b's four exhaustive p = 10 designs, distinguishing non-block A–C from block-diagonal D; N3's sampled ratios labelled exploratory, no theorem exponent inferred (C_corollaries, L4_k1 Remark (2), REPORT §6). |
| 15 | MINOR | FIXED. (b) OBS-k: new `numerics/n5_obsk.py` → `n5_obsk_out.txt` (k ∈ {2,3}, m ∈ {1,2,k,k+1,5}, p ≤ 3200; 0 chain violations; ratio → 0 for m ≥ k; R01-7 example), recorded in the L6 header. (a) R2 interface: new `numerics/n4_r2_pseudo.py` → `n4_r2_pseudo_out.txt` on zero-distance/small-positive-distance designs (method port of LOC2 d1_diag), recorded in the L2 header (see LOG for the result). |
| 16 | NIT | FIXED. 27 162 → 27 324 (L3 header). |
| 17 | NIT | FIXED. OBS-k proof uses L_* := max(1, L). |
| 18 | NIT | FIXED. REPORT review trail: "1 MAJOR, 2 MINOR, 1 NIT, applied". |

STATEMENT v1.1.1 → v1.1.2 (items 1, 2, 5: scope/qualification wording only; no hypothesis or conclusion of UNI-0/UNI-1 changed).
