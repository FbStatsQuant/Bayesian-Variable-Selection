# VERIFY — ADVISOR_BRIEFING claims → sources

Paths are relative to the repo root. Every line below was re-opened after drafting. A token check
(scratchpad script; exact string match on the cited line) confirmed every number. Line citations that
had drifted were corrected in the .tex comments. **Nothing is marked [unverified] in the PDF.**

Status mapping (never upgraded): PROVED-CHECKED → "proved, checked"; council passed but HQ label not yet
applied → "proved, sign-off pending"; "PROVED (candidate)" / "by this seat, unchecked" → "proved, unchecked";
OPEN → "open".

Path note: the brief named `Scripts/Campaigns/2026-10-28_New_Campaign/analysis/` for HEADLINE_H.md. That
folder holds only `scripts/` and `tests/`. The headline files are under `Results/2026-10-28_New_Campaign/`.

## §1 Method
| Claim | Source |
|---|---|
| g = n ridge prior, IG(0.01,0.01), BB(1,p) capped at K = min(p,⌊n/2⌋), score F | Theory_work/State_of_Project/sections/02_method.tex:78-102, :132 |
| blocks (complete linkage, size ≤ B ≤ 16), tables, exact π₀, exact Z̄₀, iid draws | 02_method.tex:185-203, :149, :205 |
| bridge γ_φ = γ₀e^{φd}, d(S) | 02_method.tex:200-201 |
| pilot ESS ≥ 0.90, restricted-ESS grid, rebuild, escalation | 02_method.tex:304-327 (0.90 at :309) |
| R = 4 islands in the study; move round; multinomial resampling every stage | 02_method.tex:155, :264-281, :306 |
| Ẑ_r formula | 02_method.tex:422 |
| Ẑ = mean of Ẑ_r; RB PIPs pooled; MPM; HPM = max of the ledger | Theory_work/Wave3/W3-SAMP/REPORT.md:43-53 |
| meaning of `local_certified` | Theory_work/Wave3/W3-SCR/REPORT.md:13-18 |

## §2 Empirics (high-p study; R = Results/2026-10-28_New_Campaign/H2_20261102)
| Claim | Source |
|---|---|
| n=200, p∈{500,1000}, S1–S6, 100/cell, 14 true variables, exact-recovery rule, failures = misses | R/HEADLINE_H.md:3 |
| design descriptions; β pattern (|β| ∈ [0.8,1.8]); c ∈ {1, 0.5} | Theory_work/State_of_Project/sections/03_empirics.tex:38-45, :50-52, :29 |
| 2,394 completed + 6 resource_limit; counted as misses | R/HEADLINE_H.md:140, :144 |
| c=1 counts: HPM 559/560, MPM 559/561, SuSiE 585/582, SSL 569/582, horseshoe 574/575, MCP 377/235, ABESS 365/323, lasso 111/89, EN 61/50, aLasso 493/512 | R/HEADLINE_H.md:44,45,47,49,50,51,53,55,56,57 |
| c=0.5 counts: HPM 370/340, MPM 338/321, SuSiE 220/205, SSL 303/255, horseshoe 185/136, MCP 240/192, ABESS 256/214, lasso 24/15, EN 14/10, aLasso 253/197 | R/HEADLINE_H.md:63,64,66,68,69,70,72,74,75,76 |
| MCP/ABESS primary = EBIC(γ=1) at c=1, EBIC with K=37 at c=0.5 (pre-registered) | R/HEADLINE_H.md:30 |
| shares 93.2 / 93.3 / 61.7 / 56.7 % | R/HEADLINE_H.md:116-119 |
| c=0.5: first or tied-first in 11/12 cells; +67 / +85 over SSL | R/HEADLINE_H.md:132 |
| c=1: 4th of 9; ~93% vs 95–97%; misses add variables; beats lasso family, MCP, ABESS (EBIC k≤37) in all 24 cells | R/HEADLINE_H.md:133-136 |
| 565 completed misses, each with a scored competitor above S₀; min gap 0.0049 nats; 0 detected search misses | R/EVIDENCE_H.md:136-147 (gap :143, "Shown" :147) |
| low-p: SMC HPM = exact HPM 2,400/2,400 and 12,000/12,000 | Docs/HQ/STATUS.md:29 |
| low-p: design, 2,400 cases, enumeration; log-Ẑ bias −0.0002, RMSE 0.012; RB PIP error 0.0005 | Results/2026-10-28_New_Campaign/L_20261102/HEADLINE_L.md:3,7,9 |
| median runtime 565/607 s (p=500), 1,550/1,616 s (p=1000) | R/tables/ev_cost.csv:2-5 |
| 906 core-hours total | Scripts/Campaigns/2026-10-28_New_Campaign/ops/PRODH_COMPLETION_20261102.md:32 |
| runtime ×2^1.4 when p doubles | R/EVIDENCE_H.md:115 |

Correction to the brief: "14 signal settings". The source has 14 true variables (|S₀| = 14). The settings are
6 designs × 2 scales × 2 values of p.

## §3 Theory
| Claim | Status in PDF | Source (statement; status) |
|---|---|---|
| r_n, δ_n | — | Theory_work/Wave3/W3-POST/STATEMENT.md:32 |
| SL theorems/conditions, p up to exp(Cn^α) | — | Papers/Core_bibliography/32_*.pdf pp. 952–958 (Thm 1 p.952, Thm 2 p.953, Cor 1 p.954, Thm 3 p.956, Thm 4 p.957, Cond 5 p.958); Theory_work/Wave1C/FINAL/sections/s2_map.tex:12-24 |
| Thm P1 hypotheses and conclusions; BM(c) | proved, checked | W3-POST/REPORT.md:52-71; STATEMENT.md:74; Theory_work/Wave3/HQ_DECISIONS.md:6 |
| random-design interface; factors allowed (UNI-P) | — | W3-POST/REPORT.md:70-79; Theory_work/Wave2/W2-UNI/REPORT.md:29-30, :40 |
| design-free size tail O_P(n^{-1/2}) | proved, checked | W3-POST/REPORT.md:46-50; HQ_DECISIONS.md:6-7 |
| rate lower bound 1/(1+√(n+1)) | proved, checked | W3-POST/REPORT.md:23-24, :72-74; HQ_DECISIONS.md:6-7 |
| strengthenings (ID^M + Occam sum; E δ_n ≤ C r_n; Hellinger O(log n/n)) | proved, sign-off pending | Theory_work/Wave3/W3-POST2/REPORT.md:46-55, :82-92, :94-101, :103-111; status :6-20; Theory_work/Pause_2026-11/RESUME_PLAN.md:18, :72-79 |
| specificity counterexample | counterexample, numerical; sketch unchecked | W3-POST/REPORT.md:69, :158-162 |
| SL comparison (rates, sensitivity only, condition (10)) | — | W3-POST/REPORT.md:171-176; s2_map.tex:12-17 |
| Thm M1 (misspecification) | proved, checked | Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:36-54 (status :52); s2_map.tex:21-22 |
| exact π₀ sampler | proved, unchecked; matched to code | W3-SAMP/REPORT.md:106; s4_sampler.tex:7 |
| start sandwich S₀ ⊆ S̃ ⊆ Q | proved, checked | Theory_work/Wave1C/FINAL/sections/s5_hpm.tex:69 (status :73) |
| start-mass rate | open | Theory_work/Wave3/PROGRAM.md:16; RESUME_PLAN.md:142-146 |
| Thm C1 certified screening (threshold, A1, SCR-C, SCR-N) | proved, checked | Theory_work/Wave3/W3-SCR/REPORT.md:20-47, status :7-9, :56-66; STATEMENT.md:58-59 |
| Thm C2 reported model (FL, V, L, N; examples) | proved, sign-off pending | Theory_work/Wave3/W3-RM/REPORT.md:25-31, :44-65; STATEMENT.md:90-106, :39; RESUME_PLAN.md:16, :51-60 |
| dropping (N) | open | W3-RM/REPORT.md:4-8 |
| SL Theorem S not obtained; Cond 5 analogy | — | s2_map.tex:4, :18, :23; W3-POST/REPORT.md:110 |
| Thm S1 unbiasedness | proved, checked | s4_sampler.tex:10-15 (status :21) |
| Thm S2–S4 (draw discovery, concentrated bridge, terminal repair); δ̄ | proved, sign-off pending | W3-SAMP/REPORT.md:54-57, :79-87, :88-94; STATEMENT.md:26-27; status :17, :96-102; RESUME_PLAN.md:17, :63-70 |
| NC_r necessity | open | W3-SAMP/REPORT.md:102 |
| GEN (C6), older cap | proved, checked | s5_hpm.tex:54; PROGRAM.md:28 |
| NEG (exact-Gram CS, p/K > 16/15) | proved, checked | Theory_work/Wave2/W2-FAC-PK/REPORT.md:29-30, :9, :17-21 |
| SHARP (log p/log n > 1/6) | proved, checked | Theory_work/Wave2/W2-FAC-A/REPORT.md:44-46, :20 |
| OBS-k | proved, checked (inside a checked package) | W2-UNI/REPORT.md:20-22; Theory_work/Wave2/SR/CRITIQUE_fable.md:104, :166 |

## §4 Next steps
| Claim | Source |
|---|---|
| strong-factor experiment: p > K, p/n up to 10; n=50 batch 298/320; n=75–150 not run; no verdict | Theory_work/Pause_2026-11/RESUME_PLAN.md:81-94, :123-137 |
| recovery vs "screening + limits" decision | Theory_work/Wave3/PROGRAM.md:32-35 |
| rerun ≈ 910 core-h; islands bit-identical, HPM score can only rise | Theory_work/Pause_2026-11/RERUN_SPEC.md:24, :242 |
| remaining proofs (start-mass rate, polynomial leakage, path-level (N)) | RESUME_PLAN.md:142-153 |
| scaling programme, evidence-weighted merging, degeneracy open, long-term line | owner's brief for this document (plans, not results; no numbers quoted) |
