# R2 — Seat B rebuttal and item 9 (MEET-v31)

Read: SYNTH_R1, R1_A, R1_C, AMEND_01, `evidence/2026-11-03_concurrency_runs.md`, `origin/theory/ABL-START:theory_campaign/ABL-START/REPORT.md` (draft, "results pending": arms A–D, 12 designs × 1 seed, leave-one-arm-out reference, arm A checked bitwise only on a synthetic n = 100, p = 150 design), the spec `Docs/Methodology/METHODOLOGY_v3.md` and every file of `Scripts/SMC_BVS/core/` (R and C++). Small read-only computations in the scratchpad (budgets across (n, p); error-bound scaling; `start_truncated` count on `agg_final/ls0_per_fit.csv`). The saved study fits with per-phase timings are not on this machine (`/home/fb31/ls0_work/study/` does not exist; `ls0_work/full/*.rds` hold only LS0 export records), so D4 rests on the chair's three designs.

## 1. Disputes D1–D8

**D1 (ABL-START decision rule). Compromise; my Round 1 "majority ⇒ change" is withdrawn.** The ablation as designed (12 designs, one seed each, a leave-one-arm-out reference whose own error is of the order of the 4-island spread of log Ẑ_r) cannot deliver an "irrefutable" argument (ground rule 5) for a WORKHORSE change with a 2,400-fit re-run (ground rule 8). It can settle the depth claim and flag an accuracy issue. Rule, declared before results, per design with statistics T_final, rebuilds, calibration seconds, |log Ẑ_X − log Ẑ_ref|, max_j |PIP_X − PIP_ref|, and noise scale σ_r = SD of log Ẑ_r over the arm's 4 islands:
- **Outcome 1 — keep, depth claim allowed:** T_A ≤ min(T_B, T_C) and rebuilds_A ≤ min(rebuilds_B, rebuilds_C) on ≥ 9/12 designs, with A's accuracy not worse than B's and C's by more than σ_r on ≥ 9/12.
- **Outcome 2 — keep, reframe (no depth claim; the start is the theorem-bearing exact merge, S1/S2):** A not worse on accuracy on ≥ 9/12 but Outcome 1's depth condition fails. This is where A and C already are, and where I now join them.
- **Outcome 3 — real issue flagged, method unchanged for paper 1:** B or C beats A on |Δ log Ẑ| or PIP error by more than σ_r on ≥ 9/12 designs including both S4 and both S5 designs. Then v3.1 still ships with the block start, the paper reports the ablation, and a 20-seed paired check on the two worst designs is commissioned (≤ 20 seeds, ground rule 8). A start change goes to v2 unless that check confirms. Arm D enters only as v2 evidence.
- What would move me back to "change": the 20-seed check confirming Outcome 3. What would move me to Outcome 1 against a weak result: nothing; a non-result is Outcome 2.

**D2 (O-CERT card). Concede to A, conditional.** The card is a list of deterministic facts about scored regions plus one probabilistic item, the lower bound on Z. With C's observation (Z_𝒯 ≤ Z deterministically), P(max{Z_𝒯, 0.05Ẑ} > Z) ≤ P(0.05Ẑ > Z) ≤ 0.05, so P(any card item false) ≤ 0.05 by a union over one event (checked here; elementary). Add it POST HOC iff PC1 confirms O-CERT's exact-arithmetic premises, with C's label "numerical implementation of an exact-arithmetic certificate" and the scorer's documented η (`v3_score.h:242–246`) printed beside it.

**D3a (extra local search from the R = 4 centre). HOLD with C.** The point is not HPM monotonicity but the class of (d): with the baseline search path reproduced, the stacked run's scored set contains the R = 4 run's scored set and (d) is ADDITIVE (nested); without it, the stacked run's final search starts from a different centre, greedy paths differ, and (d) is only LAW-PRESERVING. Cost 0.2–0.4 s. What would change my mind: HQ deciding stacked runs make no nested claim; then drop it.

**D3b (flags when R′ > 4). Adopt C's split** (not addressed in my R1): baseline flags on islands 1–4 with the baseline overall best and baseline local search, reported as the bitwise-reproducible v3 flags; expanded flags over all R′ islands reported separately. Reason: E1 compares island bests to the overall best (`v3_run.R:149`); with R′ islands the overall best changes, so one set of flags cannot be both bitwise-baseline and "over all islands".

**D3c (LS0 wording). Concede the merged wording:** "the v3 computation is reproduced bitwise as a prefix (LS0 placed after the final local search, reads no uniforms, API-AUDIT §3); LS0 appends scored models; HPM unchanged on 2,394/2,394; stores nested; near-tie list, `local_certified` and the certificates are recomputed for the returned model." One addition: an LS0 improvement must **not** fire E3 (E3 is the final local search from the HPM centre, RC-1, `v3_run.R:151`); give LS0 its own provenance value and flag `ls0_improved`, so the study's E3 = 0 stays comparable.

**D3d (scope of "scale p", C6). Concede to C for the paper's claims; keep A's conditional.** Depth is stated at the implemented level (islands only: N_e·(T+L+4)·m plus setup, grid, reductions), "free of N, H, R" is the declared v3.2 route with C6's one-line LAW-PRESERVING proof (IND-T on distinct (island, stage, particle) triples). If HQ/Felipe put any p > 2,500 in paper 1, C6 is implemented and law-checked (A's 20-seed two-map check). My Round 1 "demonstrated at one size" is withdrawn as a requirement.

**D3e. Agree:** (h) block tables as the explicit parallel local stage (bitwise, independent sub-model scores); C11 clustering O(p²)–O(p³), neighbour-graph sort per column (`v3_blocks.h:160`), and grid bisection in the large-p roadmap. All ADDITIVE.

**D3f. Agree:** spec sentence "workers are processes (as in the METH-AUDIT harness); threads sharing `Data` need per-worker route counters merged deterministically" (`v3_score.h:20–21, 231–236`). "Bitwise" is stated for process workers, one binary with `Makevars.v3` (`-ffp-contract=off -march=x86-64-v2`), single-thread BLAS.

**D4 (calibration a cost bottleneck). HOLD; chair fact 0.2 is the evidence.** From the log, the wall-clock cap of (a) alone with R = 4 islands is (cal + final)/(cal + final/4):

| design | cal s | serial final s | cap of (a) alone | rebuilds | calibration depth after (b), (1+I_e)·H₀ | final depth N₀ |
|---|---|---|---|---|---|---|
| S1_r001 | 161.6 | 358.2 | 2.1× | 2 | 1,536 | 2,500 |
| S4_r001 | 1,184.5 | 671.8 | 1.4× | 8 | 4,608 | 2,500 |
| S5_r002 | 258.1 | 413.3 | 1.9× | 3 | 2,048 | 2,500 |

On the masked design the calibration's sequential depth exceeds the final run's even after (b), because the I_e rebuilds are serial. So W-cal is on the critical path of any wall-clock sentence, and the paper's parallel claim must count calibration. Rule unchanged (all agree). Closing check: tabulate `timings$calibration` and `timings$final` (`v3_fit.R:124,136`) from the 2,400 saved fits where they are stored.

**D5 (primary PIP). Concede to A and C:** Ẑ-weighted primary now, POST HOC; equal-weight secondary. C is right that MPM-vs-truth is not posterior accuracy; my gate is withdrawn. The rescoring (chair fact 0.5) is reported, not a gate; I ask it to include R_eff = (Σ_r W_r)²/Σ_r W_r² per fit, so the paper can state the finite-R variance consequence where R_eff ≈ 1. The accuracy comparison is the reference-based one on ABL-START's subset.

**D6 (inherent limitations wording).** (i) XᵀX memory: HOLD, not inherent (C7); "every worker needs all of X or G" is inherent to full-coordinate rounds. (ii) "No run can upper-bound Z": concede to C. I checked the bound: D_S ≥ 1 and Q_S ≥ yᵀy/(n+1) are in spec §5, Σϖ = 1, so Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}, i.e. about (n/2)·log(n+1) ≈ 265 nats above m(∅) at n = 200. PROVED, useless, refutes the literal. Wording: "no useful upper bound on Z from the run's record alone". (iii) Markov-only lower bound: concede the wording "assumption-free part is Markov; max{Z_𝒯, 0.05Ẑ} keeps 95% coverage; sharper only under a variance bound". (iv) masked weight variance: both. The mechanism is inherent (Chatterjee–Diaconis one-shot scale, SEP-B); its severity on the production grid is OPEN (V11), a theorem obligation.

**D7 (estimator for general h, joint summaries). Concede in part.** v3.1 should define a measured-round particle-average accumulator for a list fixed from (X, y) before any randomness: model-size distribution, pairwise inclusion on neighbour-graph edges (≤ 2pB pairs), and terminal frequency of the returned HPM. No randomness consumed, nothing else changes: ADDITIVE. Not recoverable for the 2,400 fits; paper 1's empirical joint summaries come from the ≤ 20-seed panel only. C's bound P(|μ̂ − μ| > ε) ≤ 4(M−1)/R + 4M/(Rε²): I re-derived it (E Y_r = 0, E Y_r² ≤ M, W̄ ≥ ½ event, two Chebyshevs, union): PROVED under its hypotheses. The A2 "fails only downward" counterexample is correct (a non-constant non-negative unbiased estimator exceeds its mean with positive probability): theorem-meeting wording item, not a method item.

**D8 (6 resource_limit fits).** Not a method question. I support the re-run as cheap operational evidence (6 fits × 4 cores), labelled as such; it cannot move the delivery theorem (R6).

## 2. Chair facts 0.1–0.5

- **0.1** closes my R1 §5.3 (third design). The useful fact is "sum of island times ≈ serial time": no contention, per-island cost unchanged. It is a 2-core measurement, so my R1 Amdahl numbers are replaced by the table in D4.
- **0.2** supports D4 and refutes "false in cost" on S4; it raises W-cal and C6 to the critical path.
- **0.3** the ablation is clean on the kernel (B, N(j), m fixed; only π₀, its draws and the I step differ, which is intrinsic to a start ablation). One gap: arm A's bitwise check is on a synthetic design; add the same check against one saved study fit (same seed) among the 12, so "arm A = production" is a study-design fact.
- **0.4** → D3f.
- **0.5** → D5; add R_eff per fit.

## 3. Procedural rule (SYNTH_R1 §3)

**Accept, with two amendments.** (a) When a method question is closed because "every plausible answer leaves the decision unchanged", the minutes list the answers considered (the case split must be checkable). (b) An inherent limitation cites the PROVED impossibility or the definition it follows from (file and label); a theorem obligation the paper needs as a claim is proved or the claim is dropped and the exclusion disclosed (C's point; no "exclusion disguised as impossibility").

Sorting my R1 §5 list:
- **(i) method question still open:** 1 (ABL-START; closes by the D1 rule above).
- **(ii) theorem obligations:** 11 (V5 reversibility/self-adjoint row); plus, from this round: rebuild convergence and P(S₀ ∈ V); P(schedule_limit) → 0 (as-coded T_n, Conjecture P); E[W²|𝓒] through a masked crossing (V11); DELIV-POP; Theorem H's measured-round identity for general h; ℓ versus the moves BASIN needs; L versus t_mix (V10).
- **(iii) inherent limitations:** T27(i) masking of any product-of-blocks start (PROVED-LOCKED); a diagnostic from the run's own weights cannot see a never-visited mode (V12, E1c PROVED; CD Thm 2.1); the Θ(p) per-round factor of a single-site Gibbs round (by definition of the kernel); posterior misses at n = 200 (by the fixed target, N200); no finite scored set certifies the global mode without a bound on unscored mass (by definition); every worker needs all of X (by definition of a full-coordinate round); a fixed allocation cannot support unrestricted growing dimension (by definition; spec V13).
- **(iv) engineering/spec, no method content:** 2 (W-cal replay), 3's code check, 4 (LS0 merged, paired), 5 (rescoring, now report-only), 6 (Z_𝒯/PIP^𝒯/C1 script), 7 (spec edits), 8 (evidence files; partly done by 0.1), 9 (`fit$log_Z` NA fix), 10 (calibration tabulation; feeds (ii)).

## 4. Item 9 — generality in (n, p)

Classes: (a) convention with reason, (b) function of (n, p) or X, (c) resource budget, (d) numerical tolerance, (e) arbitrary / study-tuned / silently stops scaling. Study values: n = 200, p ∈ {500, 1000}: K = 100, B = 14, ℓ = 10/11, L = 8, N₀ = 2,500, H₀ = 512, T₀ = 1,000 (all 2,400 fits have B = 14, confirmed in `ls0_per_fit.csv`).

| # | setting | value (ref) | class | reason | behaviour as n, p grow | action |
|---|---|---|---|---|---|---|
| 1 | g = n, τ = 1 | spec §5; `v3_score.h:177–182` | a | unit information; ridge keeps m(S) finite for collinear X_S | p-free; τ matters more as p ≫ n (collinear sub-models) | keep |
| 2 | IG(0.01, 0.01) | spec §5; `v3_score.h:14` | a | proper; pairwise effect ≤ n·b₀\|1/Q₁ − 1/Q₂\| | vanishes relative to the gap as n grows; largest at tiny n | keep |
| 3 | BB(1, p) | spec §5; `v3_score.h:65` | a | depends on p only; project theory is for it | fine | keep |
| 4 | K = min(p, ⌊n/2⌋) | spec §5; `v3_preprocess.R:21` | a/b | Felipe's; T6: non-binding in covered regimes | p ≪ n: K = p; p ≥ n/2: binds; n = 3: K = 1 | keep; MPM may exceed K (reported) |
| 5 | n ≥ 3, drop exactly-constant columns, dup threshold 1 − 10⁻¹⁰ | `v3_preprocess.R:106,111`; `v3_core.cpp:722` | b/d | SD needs n ≥ 2 and K ≥ 1 | fine | keep |
| 6 | B = min(⌊√n⌋, ⌊√p⌋, B*) | spec §3; `v3_preprocess.R:22` | √ terms: a (Felipe's rule; guarantee B ≤ K for all n ≥ 3 and B ≤ p); bind only for n < 289 or p < 289 | small-sample safeguard; asymptotically inactive | keep | |
| 6′ | **B* = 16** | spec §3 "implementation limit", §8.7; `v3_core.cpp:142` B_MAX = 16 | **(c), re-labelled**: table budget 2^{B*} entries per block ⇒ ≤ 2^{B*}·p/B* = 4,096p table scores and 16·2^{B*}·p/B* = 65,536p bytes (`v3_fit.R:28`), linear in p | without B*, B = ⌊√p⌋ gives p·2^{√p}/√p table scores (10³² at p = 10⁴): the √ rule is what stops scaling, B* is what keeps the tables polynomial | constant B for large n, p is correct for the method: the start is a product of ≥ p/16 exact factors; theory with bounded cluster size is unaffected; clusters with g > B are split (W7-PART CE1), inherent to exact block enumeration (cost 2^g) | keep value; replace "implementation limit" by the budget reason; the SIZE hypothesis g_max ≤ B < 2g_min (W7-PART Thm A, blocks = groups) is a **design hypothesis of one theorem**, not a method parameter: with B* = 16 it covers 9 ≤ g ≤ 16; the study's g = 5 (2g ≤ B) is the OPEN partition law PART-pairing / Prop Q (PROOF SKETCH: co-blocking removes the masking), a theorem obligation, not a method defect. Study effect of re-labelling: none (B = 14 < 16) |
| 7 | ℓ = ⌈log₂(n+p+1)⌉ | `v3_preprocess.R:23`; moves cap `v3_engine.h:408`; rebuild cap `v3_calib.R:85` | b/c | grows with log(n+p); each move strictly improves F | the LS0 route needs ℓ ≥ Hamming distance start-mode→S₀ (c ≤ s₀ fixed on LH): eventually true | keep; obligation (ii) |
| 8 | L = max(4, ⌈log₂(n+1)⌉) | `v3_preprocess.R:24` | c | burn-in at φ = 1; V9 heuristic (coordinate ascent in O(1) rounds) | ignores p: a round already touches all p coordinates; gap "L logarithmic vs t_mix possibly polynomial" is spec V10 | keep; obligation (ii) |
| 9 | N₀ = max(2,500, n, p) | spec §3; `v3_preprocess.R:25` | c | Monte Carlo width per island; floor binds for n, p ≤ 2,500 (the study) | linear in max(n, p): per-stage O(p²) scores (T32(i) polynomial); equal-weight bias ∝ 1/N; V7's route Q·π₀(S₀) → ∞ fails under masking with N ∝ p, but the shipped route is LS0 (b1), not V7 | keep; theorems state N_n as a hypothesis; floor is a budget, not a law choice (changes cost and MC error, never the target) |
| 10 | H₀ = ⌈512·N₀/2,500⌉ | `v3_preprocess.R:26` | c | calibration width ≈ 0.2 N₀; T38(b1′) needs H₀ ≍ p | linear in p | keep |
| 11 | T₀ = max(1,000, ℓ²) | `v3_preprocess.R:27` | c + delivery rule | stage ceiling; exceeding ⇒ `schedule_limit` | ideal-grid T* = log₂A₀ + 7.7 with A₀ ≈ c(log p + ½ log n): T* = O(log log p) ≪ ℓ²; as-coded T_n OPEN (Conjecture P) | keep; obligation: P(schedule_limit) → 0 ⇔ T_n ≤ T_e w.h.p. |
| 12 | R = 4 islands | `v3_run.R:87`; `v3_calib.R:12` | c | width; declared before final randomness; R′ = 4k optional | E2's SD is over R values | keep |
| 13 | tier factor 4, one escalation | `v3_preprocess.R:30`; `v3_calib.R:149` | c | ≤ 16× bridge work; decided before final randomness | fine | keep |
| 14 | 4 measured rounds | `v3_run.R:87` | c | RB-PIP averaging | fine | keep |
| 15 | exact branch Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)·p | spec §6.2; `v3_core.cpp:72` | c | enumerate when it costs no more than the SMC's trajectories × p | computed: n ≤ 5 ⇒ exact for **every** p (K ≤ 2, E ≈ p²/2 < 5p²); n = 6, 7: p ≤ 274; n = 10: p ≤ 36; n ≥ 22: p ≤ 17; fixed p: eventually exact (N₀ ≥ n) | keep; spec's "all p ≤ 3,000 at n ≤ 5" → "all p at n ≤ 5" |
| 16 | ESS 0.90 (pilot and grid) | spec §6.6–6.7; `v3_calib.h:31,79` | a | weight CV² ≤ 1/9; dimension-free; Lemma J for any fixed threshold | scale-free | keep |
| 17 | 60 halvings; snap 10⁻¹² | `v3_calib.h:34,42,82,89` | d | φ resolution 2⁻⁶⁰; RC-2 | fine | keep |
| 18 | floor 1/T_e | `v3_calib.h:38` | c | a fully forced pilot has exactly T_e stages | tied to 11 | keep |
| 19 | V = top 20p ∪ top 20p ∪ {∅}, \|V\| ≤ 40p+1 | spec §6.7; `v3_ledger.h:76` | c | O(p) = size of any model's 1-flip neighbourhood; 20 is the multiple | grid cost 60·\|V\|·T_e ∝ p | keep |
| 20 | convergence = grid equality; ≤ ℓ rebuilds | `v3_calib.R:115` | a | lead ruling | obligation (ii) | keep |
| 21 | E1 1 nat, E2 SD > 1 nat, E3, forced steps, grid failure, local_limit | spec §6.9; `v3_calib.R:101–102` | a | factor e in odds / evidence: posterior-scale units, scale-free | fine | keep (law of 𝓒) |
| 22 | top store 40p+1; leader stores 20p | `v3_ledger.h:76` | c | HPM survives eviction; near-ties, Z_𝒯 from the store | linear in p | keep |
| 23 | cache 500p, clear when full | `v3_run.R:89`; `v3_score.h:284` | c | hits return identical bits; no law effect | fine | keep |
| 24 | **near-tie window 10⁻⁹ nat** | spec §6.10; `v3_run.R:138`; `v3_exact.R:10` | **d, silently stops being meaningful** | absolute; informational only (HPM uses exact equality) | η(S) = 64ε[ν(yᵀy/Q)(1+k·cond_H)+…] ≈ 4·10⁻¹⁰ at n = 200, k = 14, cond 10, but 4·10⁻⁹ at n = 2,000 and 4·10⁻⁸ at n = 20,000: the window falls below rounding noise for n ≳ 10³ | **fix:** window = max(10⁻⁹, 2η(Ŝ)); class POST HOC (report only); study effect: lists may lengthen on ill-conditioned fits, no decision changes; proof route: none needed |
| 25 | HPM ties: exact equality, size, lex | spec §6.10 | a | T07 argmax; scale-free | fine | keep |
| 26 | MPM at ½; low-ESS flag 0.5N; 95% bound 0.05Ẑ | `v3_run.R:130,152,122` | a | Hamming rule; flag; Markov | fine | keep |
| 27 | Q recompute when Q < 10⁻⁸·yᵀy; fallback chain; η heuristic | spec §6.13; `v3_score.h:219,227–246` | d | relative tolerances | fine; η is a documented heuristic (C's point) | keep, labelled |
| 28 | r_n = √(2 log p / n), ≥ 1 partner, ≤ B partners | spec §6.4; `v3_blocks.h:154,167` | b | chance-correlation scale of p columns | r_n ≥ 1 when p ≥ e^{n/2} (n = 6: p > 20; n = 20: p > 22,026): graph degenerates to the forced nearest-neighbour graph, well-defined; p ≪ n: r_n → 0, cap B binds | keep; theory note: spec §10's CS scale "√(log n/n)" equals this only under p ≤ n^A; restate as √(log p/n) for p ≫ n^A |
| 29 | clustering: complete linkage, cut by size ≤ B, next-fit | spec §6.3; `v3_blocks.h:131–140` | a | no correlation cut exists: the cut is by size only | cost O(p²)–O(p³) (C11) | keep; HQ's "correlation cut" item is moot |
| 30 | cut_group diagnostic at ρ = r_n | `v3_core.cpp:770` | b | report only | fine | keep |
| 31 | allocation (8 GiB, 24 h defaults); memory preflight formula; wall guard; exact-branch timing (200 scores) | spec §2, §8.6; `v3_fit.R:17–46,49,90`; `v3_runtime.h:15,23` | c | declared input; "operational guard, not a statistical setting" (`v3_fit.R:43`) | estimates on completion are a function of (X, y, s) only (the guard stops; it never alters a value); the completion event 𝒪 depends on allocation and hardware; with a fixed allocation growing (n, p) ends in `resource_limit` (spec V13, by definition) | keep; paper states "(X, y, s, allocation) → status; (X, y, s) → every estimate on 𝒪; P(𝒪 ∩ bad) ≤ α" (C's form) |
| 32 | start-mode tie enumeration cap 10⁶ (LS0 centre) | `v3_start.h:183` | d | DP argmax exact; only the lexicographic choice among exact ties can be truncated; flag returned | 0/2,400 truncated, all 2,400 have 1 tie (`ls0_per_fit.csv`) | spec must state it when LS0 enters production |
| 33 | return_gram p ≤ 2,000; V snapshot p ≤ 25 / 10⁴; W = ⌈p/64⌉; preflight byte constants | `v3_setup.R:9`; `v3_calib.R:19`; `v3_fit.R:20–32` | engineering | no law content | fine | keep |
| 34 | seed s ∈ [1, 2³¹−1], streams 0–13 | `v3_preprocess.R:7`; `v3_run.R:7` | a | fine | fine | keep |

**(e) items:** none that enters the method's law. The one setting that silently stops scaling is informational (row 24) and is fixed POST HOC with no effect on any study decision. Three spec wordings change (rows 6′, 15, 28). Requirement (4) of the spec holds as code.

**Explicit answers.**
- **B* = 16 vs W7-PART's g ≤ B < 2g:** see row 6′. A constant block size is right for the method and necessary for polynomial tables; W7-PART's inequality is a hypothesis of the partition theorem for one design family, and the study's 2g ≤ B case is a theorem obligation (PART-pairing OPEN, Prop Q sketch), not a reason to change B.
- **Floors 2,500 and 1,000:** budgets (c); they bind exactly at the study, so any change is WORKHORSE for no method reason; the theorems carry N_n, T_n as hypotheses.
- **ESS 0.90:** convention (a), scale-free.
- **40p+1, 500p:** budgets (c), linear in p, with the 1-flip-neighbourhood reason.
- **R = 4, tier 4:** budgets (c), declared before final randomness.
- **Exact-branch rule:** (c), computed boundaries above.
- **Neighbour threshold, clustering cut:** (b) and (a); no correlation cut exists.
- **`resource_limit` vs "runnable from X, y and one seed":** compatible as stated in row 31; the dependence is confined to the completion event.
- **Separate p ≪ n / p ≫ n rules:** not needed; every setting is a function of (n, p), and the only regime-sensitive ones (K, exact branch, the √ terms of B) switch automatically.

**Theory scope per regime, and whether a method choice causes it.**
- **p fixed or p ≪ n:** the method is eventually exact (row 15), so V2–V4 are theorems about the output; no restriction.
- **p ≈ n, exact-Gram LH (p ≤ n − 1):** the home of T38(b1-LH)/(b2-LH), C1; restriction g ≤ B < 2g is a theorem hypothesis (row 6′).
- **p ≫ n, p ≤ n^A:** T01–T03 selection consistency, T38(b1-LH-iid) (XF GAP in parts), T32(i) polynomial cost. The restriction to p ≤ n^A comes from the target's theory (BB(1, p), g = n; THM-INV §3b: "we have p ≤ n^A only"), i.e. from Felipe's fixed model and the proof technique, not from the sampler. Song–Liang's p ≤ e^{Cn^α} is a property of their prior and conditions. No method choice causes it, and no method choice could lift it; the budgets are polynomial in p for any p (cost linear in p is unavoidable, reading X is np).
- **tiny n:** n ≤ 5 exact for every p; n = 6–21 exact up to the computed p, SMC above it with B = 2–4; well-defined everywhere; the asymptotic theory says nothing, the exact branch needs none.
- **n, p → ∞ jointly:** every budget grows polynomially (N₀, H₀ linear; L, ℓ logarithmic; B constant; T₀ eventually ℓ²); the two by-definition limits are the fixed allocation (row 31) and the Θ(p) round.

## 5. Final list

**Settled (my vote):** block start kept (Outcome 1 or 2 of D1 unless Outcome 3 fires, which still keeps it for paper 1); HPM only, LS0 in the core after the final local search with its own flag; (a)–(h) as classified, process workers, nested stacking with the baseline centre search, baseline/expanded flags split; calibration unchanged with the contract and the depth table of D4 in the paper; Ẑ-weighted PIP primary (POST HOC), equal-weight secondary, R_eff reported; flags kept as triggers and labelled heuristics, plus C1/Z_𝒯 and the O-CERT card (conditional on PC1); general-h accumulator for a fixed list (ADDITIVE); every item-9 setting classified (a)–(d) with the three spec wordings and the near-tie fix; inherent limitations worded as in D6 and §3(iii).

**Still open, with the single check that closes each:**
1. D1: ABL-START results read against the rule above (plus arm A bitwise on one study design).
2. D2: PC1's verdict on O-CERT's premises.
3. D4 wording: calibration vs final seconds tabulated from the 2,400 saved fits (`timings$calibration`, `timings$final`).
4. (b)'s class: W-cal replay on the three designs; fail ⇒ LAW-PRESERVING and the wall-clock claim is capped at the D4 table.
5. D3c: merged-core LS0 replay on the three designs (HPM, stores, flags identical to the export; E3 unchanged).
6. D3d: HQ/Felipe decision on whether paper 1 shows p > 2,500 (if yes, C6 implemented and law-checked).

Nothing above re-runs the study (ground rule 8).
