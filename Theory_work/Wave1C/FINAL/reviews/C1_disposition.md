# Final council round 1 — disposition (writer, 2026-11-08 ~23:55 CST)

Round 1: Sol 7.4 (G1, G6 FAIL), Opus 8.5 (all PASS) → not passed. Replies verbatim: `C1_council_sol.md`, `C1_council_opus.md`.
All findings of both seats ACCEPTED and applied (reviewers' replacement texts used, adapted to the chapter's macros). No objection.
Additional HQ inputs incorporated: (a) A2 + A3 (Proposition F on the GROW class); (b) C-ENG report (branch
`origin/w1c/ls0-merge`, head 8a27652; read with read-only `git show`, as HQ authorised). Locations are files in `sections/`
(line numbers after this revision may shift; the anchor text is given).

## Sol seat
| # | sev | finding | change made | location |
|---|---|---|---|---|
| S1 | MAJOR | N1 / Cor. E omit the fixed-data probability convention | inserted Sol's paragraph (data fixed; expectations over streams only; condition on (X,y) if embedded in the joint law) with citation to W1-N1 STATEMENT:62-66 | s4_sampler.tex §4.1, first paragraph |
| S2 | MAJOR | Theorem F: TAIL discharge lost its cutoffs; R^𝒞, N, U, μ_c, X_{c,𝒞}, κ undefined | contrast coordinates and R^𝒞 (full-mean energy) defined; TAIL removal rewritten: (a) m_n = m♯_n = K; (b) fixed κ ∈ (0,1), Lemma T's m^T_n (exact formula from C-MIS L4:158-162), m_n = min(K, max(m♯_n, m^T_n)) with SE_w at that cutoff | s3_posterior.tex Theorem F |
| S3 | MAJOR | GEN (C4) dropped the favourable random-design branch | (C4) replaced by Sol's text (resp. (H0),(H2) with S* = S₀ ⇒ (C3-fav)); cites GEN STATEMENT:115-120 | s5_hpm.tex Theorem GEN (C4) |
| S4 | MAJOR | Theorem D needs Corollary R's allocation, not a "valid" one | new "Allocation" paragraph before Theorem D (Corollary R inequalities, cap ℓ_n; A1 envelopes for the GROW cap); Theorem D now says "under the setting and allocation above"; D′ likewise | s6_delivery.tex §6 setting, Thm D, Cor D′ |
| S5 | MINOR | BM(c), empty-max convention, f in Lemma UM, e4′ coded-routine conditions | BM(c) inequality and c₀ (TH09 card); empty-max = 0 in SL0; f(S) defined in Lemma UM; e4′ coded-routine clause (H1, H4, cap ≥ 1, H3–H4) | s3_posterior.tex Thm S-T, Lemma SL0; s5_hpm.tex Lemma UM, e4′ |

## Opus seat
| # | sev | finding | change made | location |
|---|---|---|---|---|
| O1 | MAJOR | Theorem D / Cor. D′ / CONFIG are cap-ℓ_n results; §7 over-transferred D′ | §6 setting: "with LS0 move cap ℓ_n (C-DLV's CONFIG; …)", OP-LS0 (cap ℓ_n), cite L4_delivery:6-9; §1 CONFIG now "production core plus LS0 with cap ℓ_n and the e4 fallback, …"; §7 transfer list: only the pathwise part of D′ transfers; D′'s delivery form and Thm D(i) hold for the larger cap only under A1's W_G, M_G | s6_delivery.tex setting; s1_setting.tex §1.3; s7_impl.tex "What survives", 4th bullet |
| O2 | MINOR | "one-line" fallback contradicts A1 / Remark (2) | "total tier-1 calibration fallback" in §6 intro and §2 plain reading; plain reading now names its classes (LH, LH-iid, GEN, GROW; not C-MIS) | s6_delivery.tex intro; s2_map.tex plain box |
| O3 | MINOR | P(no output)=0 relative to two code-reading audits | Remark (3): exclusion relative to P1 inventory and Lemma S.3, both AUDITED (code reading) on the serial shipped call graph; LS0/worker/fallback paths by premises (A1:33) | s6_delivery.tex Remark (3) |
| O4a | MINOR | caps below ℓ_n | MR1 (C-GROW) table cell: "all results simultaneously only for caps ≥ max(ℓ_n, \|S̃₀\|)"; sentence after the transfer list (GEN needs a ≥ 2^{v̄}−2, PXN (T) a ≥ c) | s7_impl.tex table; after "What survives" |
| O4b | MINOR | GROW needs "some maximiser", not covered by e4′'s unique-maximiser clause | §1 e4 parenthesis replaced by Opus's text; §5.2 e4′ paragraph and §7 table say GROW needs some maximiser also under ties, which the coded routine (W1-N3(a)) and TDP satisfy | s1_setting.tex §1.3; s5_hpm.tex §5.2; s7_impl.tex table |
| O5 | MINOR | Thm S row status attached C-DLV status to corrected Prop F | status cell split: C-DLV form (cap ℓ_n) PROVED-CHECKED…; corrected form (cap a_n) A1 HOLDS-WITH-AMENDMENTS, not councilled; GROW extension PROVED (A2), checked by A3, not council-passed | s2_map.tex Thm S row |
| O6 | MINOR | Thm 4 row confused Condition 4 with the conclusion | replaced by Opus's text (Condition 4 = finite second moments; conclusion (18)) | s2_map.tex Thm 4 row |
| O7 | MINOR | two MR1s unlabelled | "MR1 (C-PACK)" / "MR1 (C-GROW)" everywhere (s5 GROW setting, (C4), (C5)(a),(c), coverage table; s7 throughout; s8 memory item); defining sentence in §1.3 and §7 intro | s1, s5, s7, s8 |
| O8 | MINOR | (L1) "only" wording; certificate card | (L1) reworded per Opus; "the certificate card's store-based quantities" added to the metadata bullet | s7_impl.tex (L1), "Flags and metadata" |
| O9 | MINOR | e4 definition dropped the tie rule | e4 now "the prescribed smallest-size, lexicographically smallest start-mode maximiser (DP invariant N3 OPEN)" | s1_setting.tex §1.3 |
| O10 | NIT | SL0(vi) sharpness conditions | "When 1 ≤ s₀ ≤ K and s₀ < p" | s3_posterior.tex Lemma SL0 |
| O11 | NIT | undefined S†_𝒞, N, μ_c, X_{c,𝒞}, s*, ‖x_i‖ | S†_𝒞 = exact-posterior HPM; contrast quantities defined (with S2); s* := \|S*\|; map Thm 1 row "\|x_i\| ≤ 1 (a uniform bound on each predictor)" | s3_posterior.tex; s5_hpm.tex (C1); s2_map.tex |
| O12 | NIT | ξ_q row should quote SL's form | "π(t ⊂ ξ_q) →_p 1 if all true predictors are identifiable (read: P*(t ⊆ ξ_q) → 1)" | s2_map.tex ξ_q row |
| O13 | NIT | PXN (C) stronger conclusion | added "P(𝒪∩{Ŝ⁺=S₀}) − (1−P(U_n)) → 0, … → 1−u whenever P(U_n) → u" | s5_hpm.tex Theorem PXN (C) |
| O14 | NIT | unsourced "merged/adopted" wording; date | all replaced by sourced C-ENG facts (REPORT on branch, lines cited): implemented behind switches, default new, ls0 = FALSE reproduces v3 48/48, LS0 after the final local search on completed SMC runs, reviews APPROVE, 0/2,400 study fits schedule_limit, branch not merged; date set to 2026-11-08 (commit timestamps CST), version "draft v2" | s1 §1.2; s6 intro, Remark (5); s7 §7 intro + table; s8 item 10; preamble |

## New inputs
| input | change | location |
|---|---|---|
| A2 + A3 (Prop F on GROW class) | new Proposition F-GROW (prop:FG) with A2's statement, proof outline and all five A3 amendments (score-count replacement in L4:38 / L1:25,43; S5 fixed-p scope and random-row S5/(C6) exclusion; p_raw wording; enumerated inherited statuses; L4_assembly citation 26-28 / 28-29); status "PROVED (A2), checked by A3, not council-passed"; replaces old remark (4); map, scope list, provenance and coverage table updated | s6_delivery.tex §6.3, Remark (4); s2_map.tex; s8_scope.tex; s9_prov.tex; s5_hpm.tex coverage table |
| C-ENG report | §7 rewritten with sourced facts (BR/ citations checked by `git show` in citecheck.py); Lemma CAP premises (L1)–(L3) verified on branch code: final islands → final local search + guard → (if completed) start mode, cap = ℓ_n + \|S̃₀\|, LS0, guard (`v3_core.cpp:443-481`, cap :469-476); `local_search` cap test unchanged (`v3_engine.h:379-414`); noted that the branch preflight formula does not count the MR1 (C-GROW) LS0 term (REPORT:62-64) | s7_impl.tex; s6 Remark (5); s8 item 10 |

Checks after revision: `citecheck.py` (now also resolves `BR/` = branch files via read-only `git show`) → CITECHECK.txt;
LuaLaTeX build clean. Not re-reviewed by a fresh fidelity reviewer (round 2 council will read it).
