# MEET-THM · Check wave 2 · Proof checker 2 · Seat C (R2_C.md; R0_E as Seat C uses it)

Checker: PC2 (Claude Opus 5.5; cross-family to Seat C = gpt-6-astra). Date 2026-11-04. Brief: `CHECK_W2_BRIEF.md`, with {PC} = 2.

**Never upgrade.** TRUE-AS-WRITTEN means no counterexample was found by the search stated. It is not a proof. Seat C's statuses stand as written: every new assembly is **PROOF SKETCH, unchecked**. Where PC2 wrote out a derivation, it is a route check, not a filed proof check. Results that already have a filed cross-family check are cited, not re-checked: W1 = `W1_PC2/VERDICTS.md`; CHK = `CHK_INHERITED/REPORT.md`.

**R0_E.** R2_C makes no new or changed use of any Advisor E statement. Its cards C8, C10, C11, C12 and C15 descend from E:T05/T07/T08/T10/T13/T14/T01–T04. Those statements were checked in W1 and are cited, not re-run.

**Scripts.** Python 3, numpy/scipy, fixed seeds (≤ 10 per configuration), each run under 1 minute, all local. They are in `W2_PC2/scripts/`, and `bvs_common.py` and `smc_coded.py` are copied unchanged from W1. To reproduce, run `cd scripts && python3 <name>.py`.
- `w_family.py`: the W exhibit with the method's own partition actually computed. This is complete linkage on 1 − |r|, the coded top-down size cut at B and next-fit packing (`v3_blocks.h`), with B = min(isqrt n, isqrt p, 16) (`v3_preprocess.R:22`). The script reports the matrix-domain quantities, D_*, and the §R5 proxy and its bounds. It runs three ε regimes.
- `r3_clauses.py`: the §R3 clauses (a) and (b) and the continuity sandwich, checked by exact enumeration on 160 designs, 104 of them inside the matrix domain.
- `c8_pilot.py`: the coded pilot (`v3_calib.h` replica), tested on 600 adversarial runs, followed by the coded `build_grid`.
- `necessity.py`: the fixed-ε range obstruction, at n = 9⁶ to 10¹³.
- `c10_seat_script.py`: Seat C's quoted script, verbatim. `c10_tie.py` builds the C10 exhibit as actual data.
- `jhat_mc.py`: Ĵ on W1's coded-grid replica, 300 islands.

## 0. Summary

| Verdict class | Count (29 claim rows. Repair-only, definition-compliance and negative rows are counted separately below.) |
|---|---|
| TRUE-AS-WRITTEN | 29 |
| COUNTEREXAMPLE | 0 |
| NEEDS-HYPOTHESIS | 0 |
| AMBIGUOUS | 0 |
| DESIGN-VERIFIED | 29 |
| DESIGN-ASSERTED | 0 |
| DESIGN-FAILS | 0 |
| PLAUSIBLE | 27 |
| GAP | 2 (both carried from W1, self-flagged implementation audits) |
| IMPLAUSIBLE | 0 |
| Repairs: REPAIRED | 22 |
| Repairs: REPAIRED DIFFERENTLY | 1 (K73 region certification withdrawn; this covers both W1 D5 DESIGN-ASSERTED and D5 GAP) |
| Repairs: NOT REPAIRED | 2 (audit obligations, not statement errors) |
| Run-card definition compliance (HQ Q4) | 2 of 2 compliant, with one note (a read-only record accumulator is needed) |

Every non-clean verdict, one line each:
- **NOT REPAIRED: C3 (K69) LS0/GUARD-W/emitted-centre audits (W1 D4 GAP).** The integrated audits remain open. The card states this and keeps "mathematical specification theorem" as its fallback. This is not a statement defect.
- **NOT REPAIRED: C7 (K87/K88) integrated execution-DAG audit (W1 D6 GAP).** It remains open. The card states this and stops simplification at unaudited components.
- **GAP: C3 route.** Same item as the first line, carried over from W1.
- **GAP: C7 route.** Same item as the second line, carried over from W1.
- There is no COUNTEREXAMPLE, NEEDS-HYPOTHESIS, DESIGN-FAILS or IMPLAUSIBLE verdict.

Priority findings for the chair (§R3, the §5.3 package):
1. **Parts (a) and (b) are TRUE-AS-WRITTEN at the clause level, beyond W1's osc-d check.**
   - On 104 matrix-domain designs, `r3_clauses.py` found 0 violations of each of: 0 ≤ d_σ ≤ C_σ; |d_X| ≤ b_X; KL(π‖π₀), KL(π₀‖π), J ≤ D_*; the J identity; the χ² increment bound; and the continuity sandwich e^{±4vb_X}.
   - The largest observed ratios were d_σ/C_σ = 0.75, |d_X|/b_X = 0.43 and J/D_* = 0.065. The J bound is valid but loose.
2. **The stage-count envelope T ≤ 2⌈D_*/c_ρ⌉ + 2 holds against the actual coded pilot.**
   - `c8_pilot.py` ran 600 adversarial runs. No non-final step advanced less than h/2; the worst step was ≈ h, consistent with a step ≥ h − 2⁻⁶⁰. P ≤ ⌈2/h⌉ + 1 and T ≤ 2⌈D_*/c_ρ⌉ + 2 held throughout.
   - PC2's route: the empirical ESS is monotone in Δ, because the empirical log-MGF is convex. Popoviciu's bound makes every Δ ≤ h pass, and the bisection invariant does the rest. **PLAUSIBLE.**
   - HQ's "stage count continuous in ε" is met only through this continuous *envelope*. The integer count can jump, and the seat says so. Whether that reading meets HQ's condition is the chair's call.
3. **The IC3 exhibit W is DESIGN-VERIFIED with the method's own partition, now actually computed** (W1 checked it analytically).
   - Blocks = groups for every n ≥ 9⁶ tested (B = 9 → 16).
   - At n = 9⁶ − 1 (p = 72, B = 8) the groups split, and D_* ≈ 1.27·10³.
   - ε_n = 1/(np) > 0, and the matrix domain held on 10/10 seeds at each n. D_* had median 1.08 (n = 9⁶) falling to 1.04 (n = 10⁸).
   - **Caveat for HQ (a)/(b):** on W the cross-block term is negligible (b_X ≈ 5·10⁻⁴ to 3·10⁻⁵), and D_* is essentially the σ²-coupling term C_σ ≈ 1.05.
   - A stronger exhibit, also verified, sits at the edge of the useful regime: ε = n^{−1/2}/p. There b_X ≈ 0.35 (visible, not negligible) and D_* ≈ 1.73–1.90, with blocks = groups and the domain holding on 10/10 seeds. The chair may want both cited.
4. **ε-scale confirmed.**
   - D_* = O(1) requires p²ε = O(1) and √n·p·ε = O(1). With p ≍ n^{1/3}, the binding condition is ε ≲ n^{−1/2}/p.
   - At fixed ε = 0.01, D_* grows from 534 to 6.45·10⁴ (n = 9⁶ to 2·10⁷), and the domain fails at n = 10⁸ (δ = 1.5).
5. **The necessity route is TRUE as a prediction.**
   - At fixed ε ∈ {0.01, 0.05, 0.2}, d(S₀)/(−ε(1+ε)√n) → 1.0000 by n = 10¹³, with |d − pred| ≤ 0.33·n^{1/4}. This matches the seat's O_P(n^{1/4}) score-error claim.
   - It is a range obstruction for the displayed D_* route only, not a weight-variance necessity. The seat says so.
6. **Part (c) uses the CHK amendments verbatim in substance**: the bounded-block TV scope; initial versus later presence; the log π₀(V) side condition; and the singleton endpoint. CHK §6 says the refutation survives, so HQ's condition (c) is met.

Other notes:
- **§R4 is a valid masked statement.** It is non-vacuous on LH (masked hubs; π₀(S₀) ≍ p⁻²n⁻¹ → 0 while π(S₀) → 1). It assembles C3, C4 and C9 and is TRUE as an assembly, under the named implementation premises SR, GUARD-W and OP-LS0.
- **§R5 definitions comply with HQ Q4.**
  - The inputs exist in the run: the particle field `d` at initialisation and after each measured round (`v3_engine.h:286–360`), Ẑ_r, X and the blocks.
  - Neither definition reads a random number or feeds back into the run.
  - The per-particle values are not currently retained, so a read-only accumulator is needed, as the seat states.
  - Ĵ is unbiased in its components on the replica: E[W·B] = 0.1031 ± 0.0006 against E_π d = 0.1035; E[A] = 0.0284 ± 0.0006 against 0.0288; Ĵ₃₀₀ = 0.07471 against J = 0.07468.
- **C16's Ĵ tail bound is vacuous at the default R′ = 4, and the card does not say so.** In `jhat_mc.py` the bound equals 1 at R′ = 4 and at R′ = 50. Flag (d), minor; the declared stacking rate repairs it asymptotically.
- **R′_n = 4⌈(n+p)⁶/4⌉ is explicit, and the theorem holds with it.** But (n+p)^{4+δ} already suffices for ≤ (n+p)² summaries at ε = 1/(n+p). At n = 9⁶ the declared rate means about 2·10³⁴ islands: mathematically non-vacuous, computationally meaningless. Not a verdict issue.

Flags (a)–(d), totals:
- **(a)** None. The §4 known-false list was checked against the new clauses:
  - STG-cexW2 concerns masked crossings. C claims an O_P(1) count only on the unmasked W, and disclaims a masked law.
  - CEX-W2frac: C's x_b is the v3 score fraction (H_S = (n+1)G_S + I), not the RSS partial R².
  - CEX-NMremainder is respected: the necessity route keeps the √n-scale term and the n^{1/4} fluctuation.
  - OPW2-cex: perfect refresh is disclaimed.
  - DIL-DM(i) is excluded.
  - PART-CE2 is handled by B < 2g_min.
- **(b)** No status word is stronger than the registry's. All three qualifiers W1 found omitted are restored. Minor omissions remain:
  - T26BUD-G's own AUTHOR-ONLY flag (C8);
  - "SF none" on DIL-E (C5);
  - the registry ⚑ CONFLICT markers on T32(i) (C7) and T38-b1-LH (C3). The latter conflict concerns the iid sub-claim, which C excludes.
- **(c)** No study condition is used as a hypothesis.
  - SR, GUARD-W and OP-LS0 are named implementation premises. Successful calibration enters as conditioning on 𝒞.
  - The matrix-domain inequalities are data/design inequalities, shown to hold with probability → 1 on W.
- **(d)** Variant labelling:
  - R′_n is labelled as the v3.1 optional-stacking configuration (METHOD_v3.1 #7). LS0 is v3.1 (#8), and its integration is unaudited (labelled).
  - C14 is the ideal grid (labelled).
  - Unlabelled: C16's bound is vacuous at R′ = 4.

## 1. §R3 — the §5.3 package (C2: K102/K10/K11/K53), deepest look

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| C2(a) · split | Under A and matrix domain: d = d_σ + d_X, 0 ≤ d_σ ≤ C_σ = νa²/[2(1−a)], \|d_X\| ≤ b_X; d_σ survives E = 0 | TRUE-AS-WRITTEN: 104 domain designs (coded and arbitrary partitions, correlated), all feasible S: 0 violations; max d_σ/C_σ = 0.75, \|d_X\|/b_X = 0.43 | DESIGN-VERIFIED: W, own partition; C_σ ≈ 1.05, b_X ≈ 10⁻⁴ (ε = 1/(np)), 0.35 (ε = n^{−1/2}/p) | PLAUSIBLE: d_σ = d_D (block-diagonal discrepancy); Σx_b ≤ a by principal-submatrix inequality; W1 App. A steps 2–4 | W1 D14 (osc only) refined to clause level | none | `r3_clauses.py`, `w_family.py` |
| C2(a) · divergences | osc d ≤ D_*; KL(π‖π₀), KL(π₀‖π), Jeffreys J all ≤ D_* | TRUE-AS-WRITTEN: J = KL+KL identity to 1e−7; 0 violations; max J/D_* = 0.065 (loose but valid) | DESIGN-VERIFIED (W: D_* = 1.04–1.19) | PLAUSIBLE: each KL ≤ J = E_πd − E_π₀d ≤ osc d | — | none | `r3_clauses.py`; W1 cluster 4 row 1 |
| C2(b) · increments | χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1 | TRUE-AS-WRITTEN: 0 violations (6 u × 5 Δ per design); W1 likewise | DESIGN-VERIFIED | PLAUSIBLE (E e^{2Δd}/(E e^{Δd})² ≤ e^{Δ osc d}) | — | none | `r3_clauses.py`; W1 cluster 4 |
| C2(b) · weights | Every successful coded grid: e^{−D_*} ≤ W_r ≤ e^{D_*}, M₂ ≤ e^{D_*} | TRUE as cited: W1 found W in [e^{−osc}, e^{osc}] on 1,600 coded-grid islands, good and poor V | DESIGN-VERIFIED (W: M₂ ≤ e^{1.2}) | PLAUSIBLE (Σ Δ_t = 1 by snap; E W = 1 by N9/T12) | — | none | W1 cluster 4 rows 3, 6 (not re-run) |
| C2(b) · stage count | Under C8: T ≤ 2⌈D_*/c_ρ⌉ + 2 ≤ 4 + 2D_*/c_ρ, a continuous envelope; integer count may jump; checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1 | TRUE-AS-WRITTEN: coded pilot, 600 adversarial runs (T_e ∈ {2, 10, 1000}, D ∈ [10⁻³, 200]): 0 steps < h/2, 0 P > ⌈2/h⌉+1, 0 T > 2⌈D/c_ρ⌉+2 | DESIGN-VERIFIED: W gives T = O_P(1) | PLAUSIBLE (see C8 row, §5) | — | HQ "stage count continuous in ε" met via the envelope only (chair's call) | `c8_pilot.py`; `v3_calib.h:30–47` |
| C2(b) · continuity | b_X → 0 as E → 0 (fixed partition); e^{−4vb_X} ≤ [1+χ²(q_v‖q_u)]/[1+χ²(q^σ_v‖q^σ_u)] ≤ e^{4vb_X} | TRUE-AS-WRITTEN: 0 violations (10 (u,v) pairs × 104 designs) | DESIGN-VERIFIED (W: e^{4b_X} ≈ 1 + 4·10⁻⁴) | PLAUSIBLE: 1+χ² = Z_{2v−u}Z_u/Z_v², and Z_t/Z^σ_t ∈ e^{±\|t\|b_X} | HQ (b) continuity condition met | none | `r3_clauses.py` |
| C2(c) · one-shot refutation | Amended WS6(d)/WS7: zero cross-block dependence does not bound one-shot weight variance; masked start gives divergence/support obstruction | TRUE as cited: CHK §§1, 2, 6 VERIFIED WITH AMENDMENT; the seat's four amendments match CHK's wording (bounded-block TV; initial vs later presence; log π₀(V) condition; singleton endpoint) | DESIGN-VERIFIED: CHK §6 orthogonal p = n−1 example (χ² ≳ n^{3/10}/(log n)^{9/10}, TV → 0) | PLAUSIBLE | HQ (c): check passed (CHK §6) | statuses verbatim (AUTHOR-ONLY; CHK verdicts listed separately) ✓ | CHK §§1, 2, 6 (not re-checked) |
| C2 · ε-scale | Bounded within-block inverse eigenvalues, p ≍ n^{1/3}, energy O(√n): δ = O(pε), a = O_P(n^{−1/2}); useful regime ε ≲ n^{−1/2}/p | TRUE-AS-WRITTEN: PC2's own computation needs Kδ ≈ p²ε and νr ≈ √n·pε to be O(1); the binding one is n^{−1/2}/p. Numerically: D_* ≈ 1.75 at ε = n^{−1/2}/p; 534 → 6.45·10⁴ at ε = .01 | DESIGN-VERIFIED (three ε regimes) | PLAUSIBLE | W1 summary item 3 ("not a fixed-correlation result"): REPAIRED (stated scope) | none | `w_family.py` |
| C2 · IC3 W | within 1/4, cross 1/(np), two n^{−1/4} signals, σ² = 1, n ≥ 9⁶: own blocks = groups; domain w.p. → 1; D_* = O_P(1) | TRUE-AS-WRITTEN: own partition computed, blocks = groups for n ∈ {9⁶, 10⁶, 2·10⁷, 10⁸}; fails at 9⁶ − 1 (B = 8); domain 10/10 seeds per n | DESIGN-VERIFIED; ε > 0 ✓ (vanishing: ε_n ≈ 2·10⁻⁸ at 9⁶) | PLAUSIBLE | W1 D14 AMBIGUOUS (n ≥ 9⁶): REPAIRED | cross term negligible on W; suggest also citing ε = n^{−1/2}/p (verified) | `w_family.py` |
| C2 · variance transfer | First-stage iid comparison transfers 1 + N·Var(Ẑ/Z) = 1 + χ², not Var; no perfect-refresh product for later stages | TRUE-AS-WRITTEN (iid identity) | DESIGN-VERIFIED (any input) | PLAUSIBLE | repair pattern of SYNTH §3 cluster 4 (A.C9(c)) respected | OPW2-cex avoided ✓ | derivation |
| C2 · necessity route | At fixed 0 < ε < 1/4 on W′: d(S₀) = −ε(1+ε)√n + o_P(√n), d(∅) = 0; range obstruction only | TRUE-AS-WRITTEN (as a prediction): ratio 0.928 → 1.0000 (n = 9⁶ → 10¹³); \|d − pred\| ≤ 0.33·n^{1/4} | DESIGN-VERIFIED: Σ positive definite for ε < 1/4; strict separation 0.75 < 1 − ε keeps own blocks = groups | PLAUSIBLE (explicit 2×2 inverse; Gaussian score errors O_P(n^{1/4})) | — | proposed route, not a list theorem (seat says so) | `necessity.py` |
| C2 · not supplied | No necessity at 1/(p√n); no inference from range to weight variance | n/a (negative scope statement); consistent with CHK §4 and §6 | n/a | n/a | — | none | — |
| C2 · statuses | New assembly PROOF SKETCH; OWS rows PROVED, AUTHOR-ONLY, SF/XF none; CHK verdicts separate | verbatim ✓ (IDX L404–413) | — | — | W1 novelty note (cite OWS-WS4): REPAIRED (§R6 agenda 10, internal predecessor) | none | IDX |

**HQ Q1 conditions.** Constants: explicit (C_σ, b_X, D_*) ✓. σ²-coupling term: explicit, and it survives E = 0 ✓. Stage count: a continuous envelope only ✓*. Continuity in ε: ✓. Correlated family with ε > 0: W, verified ✓, with a vanishing ε (see summary item 3). Part (c) uses the CHK amendments ✓.

## 2. Main-list cards (§R6 item 11: C1–C7, with their §R2 statements)

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| C1 (K46…) · unchanged clauses | E[W_rH_r(h)\|𝒞] = π(h); RB records; ratio bound; union; truth anchor; MPM margin | as W1 (TRUE) | as W1 | as W1 | — | — | W1 cluster 2 (not re-checked) |
| C1 · repair: vacuous at R′ = 4 | label default-4 bounds vacuous | — | — | — | REPAIRED (Repairs row; D11 row). The statement text itself carries no label | — | R2_C L71, L25 |
| C1 · repair: stacking rate | explicit W stacking rate | — | — | — | REPAIRED: R′_n = 4⌈s⁶/4⌉ (§R6) | (d) labelled as optional stacking ✓ | R2_C L322 |
| C1 · IC3 | W: M₂ ≤ e^{D_*} = O_P(1) | TRUE-AS-WRITTEN | DESIGN-VERIFIED (D_* ≤ 1.19, 40 runs) | PLAUSIBLE | — | none | `w_family.py`; W1 cluster 4 |
| C2 | see §1 | | | | | | |
| C3 (K69…) · output form + SIZE | Under G on LH, A, SR, GUARD-W, OP-LS0, ℓ ≥ 1: P(𝒪, Ŝ⁺ ≠ S₀) → 0 | TRUE as cited (T38-b1-LH PROVED; SF/XF VERIFIED*) | DESIGN-VERIFIED: LH, n ≥ 9⁶ gives g = 9 ≤ B ≤ 16 < 18 (SIZE) | GAP: integrated LS0, emitted centre, GUARD-W (self-flagged) | PC1/PC2 cl. 6 SIZE: REPAIRED; output-event form: REPAIRED; audits: NOT REPAIRED (open obligation) | (c) SR/GUARD-W/OP-LS0 are implementation premises (named); (b) ⚑ CONFLICT marker not carried (iid sub-claim, excluded) | W1 D4; IDX L438, L553 |
| C3 · scoring vs certification | TD′: truth scored with ℓ ≥ max{Φ(S°)−1, 0} plus completed scans; certified return needs ℓ ≥ τ(S°) plus final scan | TRUE-AS-WRITTEN: each move lowers integer Φ ≥ 1, so after Φ−1 moves truth is a neighbour; certification needs arrival (τ ≤ Φ moves) and a no-improvement scan | DESIGN-VERIFIED (LH: Φ(S°) = c = 2; ℓ = ⌈log₂(n+p+1)⌉ ≥ 1) | PLAUSIBLE | PC1 cl. 6 (D.M5(a) pattern): REPAIRED | none | derivation; W1 D4 LS-score row |
| C4 (K43…) · unchanged clauses | envelope U ≥ Z; TV = 1 − Z_𝒯/Z ≤ 1 − Z_𝒯/U; Markov joint LCB; Ẑ < Z_𝒯 ⇒ Ẑ < Z | as W1 (TRUE) | as W1 | as W1 | — | — | W1 cluster 3 |
| C4 · retention | Under SR, scored S₀ with π(S₀) > ½ survives top-c; TV ≤ 1 − π(S₀); store MPM = S₀ | TRUE-AS-WRITTEN: S₀ is the unique score maximiser; store PIP_j ≥ π(S₀)/π(𝒯) > ½ for j ∈ S₀, < ½ otherwise | DESIGN-VERIFIED (LH: π(S₀) → 1, W1 D8) | PLAUSIBLE | — | consistent with METHOD_v3.1 #9 (𝒯_new = top_c(𝒯_old ∪ 𝒮_added)) | derivation |
| C4 · repairs | withdraw operational K73; restore MZ-P3 qualifiers | — | — | — | K73: REPAIRED DIFFERENTLY (withdrawn, so W1 D5 DESIGN-ASSERTED and GAP are moot); MZ-P3: REPAIRED (verbatim IDX L201 + AUTHOR-ONLY) | none | IDX L201 |
| C5 (K18…) · statement | Exact factorisation; on LH, π₀(S₀) = p⁻²n⁻¹e^{O_P(1)}, π(S₀) → 1 | as W1 (TRUE) | as W1 | as W1 | Thm5-LH SAME-FAMILY-ONLY: REPAIRED; n ≥ 9⁶: REPAIRED (via LH definition) | (b) minor: DIL-E "SF none" omitted (not stronger) | W1 cluster 5; IDX L325, L328 |
| C6 (K106…) · Q* scale | On LH, Q_n* = p²n: Q/Q* → 0 / ∞ gives miss probability → 1 / 0 | TRUE-AS-WRITTEN: (1−a)^Q = exp(−(Q/Q*)e^{O_P(1)}(1+o(1))), in probability | DESIGN-VERIFIED (LH) | PLAUSIBLE | none owed (W1 clean) | (d) iid start-only comparison, labelled ✓ | derivation; W1 cluster 8 |
| C7 (K87/K88) · calibration | Calibration work Σ N_i(T_i+L_i+4)m over executed trajectories, each with its own grid; m = p + B + 2 | TRUE-AS-WRITTEN (counting; m = p Gibbs + uniform swap + B neighbour swaps + independence) | DESIGN-VERIFIED (any input) | GAP: integrated DAG unaudited (self-flagged) | PC1 cl. 13 distinct grids: REPAIRED; PC2 cl. 13 DAG audit: NOT REPAIRED (open; card stops at unaudited parts) | (b) minor: T32(i) ⚑ CONFLICT marker not carried | W1 D6; IDX L237 |

## 3. §R4 — masked-regime accuracy statement

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| §R4 · named guarantee (K43/K45, C4 via C3) | Under G on LH, A, SR, GUARD-W, OP-LS0: P(𝒪, TV(π, π^𝒯) > ε) → 0; hence sup over [0,1]-functionals, store PIPs and joint inclusions | TRUE-AS-WRITTEN (assembly): P(𝒪, TV > ε) ≤ P(𝒪, Ŝ⁺ ≠ S₀) + P(π(S₀) ≤ max(½, 1−ε)) → 0, by C3, then C4 retention, then C9 | DESIGN-VERIFIED **on a masked family**: LH hubs have zero marginal covariance; π₀(S₀) ≍ p⁻²n⁻¹ → 0, π(S₀) → 1; LH-LAT m₀ = 0.0325 | PLAUSIBLE (filed ingredients; assembly PROOF SKETCH) | HQ Q3 requirement: met | (c) implementation premises named; no delivery claim (stated) | W1 Shared LH, clusters 5–6, D8 |
| §R4 · finite-run companion | TV = 1 − Z_𝒯/Z ≤ 1 − Z_𝒯/U and Ẑ < Z_𝒯 ⇒ Ẑ < Z without discovery | TRUE (W1) | DESIGN-VERIFIED (W1) | PLAUSIBLE | — | none | W1 cluster 3 |

## 4. §R5 — run-card definitions (HQ Q4) and C16

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| §R5 · Ĵ definition | Ĵ = Σ Ẑ_rB_r/Σ Ẑ_r − R′⁻¹ Σ A_r; A_r over initial iid particles, B_r over four measured populations | COMPLIANT: inputs exist (`P[i].d` at init and after each measured round, `v3_engine.h:286–360`; Ẑ_r; final islands start from iid draw_start, `v3_core.cpp:437`); no RNG; no feedback | — | — | HQ Q4: met | needs a read-only accumulator (seat states this); label given ✓ | code read |
| C16 · Ĵ theorem | J = E_πd − E_π₀d; P(\|Ĵ − J\| > ε \| 𝒞) ≤ min{1, 4(M₂−1)/R′ + 16D²M₂/(R′ε²) + D²/(R′Nε²)}; a.s. under stacking | TRUE-AS-WRITTEN: PC2 derivation (C1 applied to (d−d_min)/D at ε/(2D); Popoviciu Var ≤ D²/4; union). MC: E[WB] 0.1031 ± .0006 vs 0.1035; Ĵ₃₀₀ = 0.07471 vs J 0.07468 | DESIGN-VERIFIED on W (D ≤ D_* = O_P(1), M₂ = O_P(1)); the bound is 1 at R′ = 4 and at R′ = 50 | PLAUSIBLE | — | (d) minor: vacuous at default R′ = 4, not labelled on C16 | `jhat_mc.py`; `r3_clauses.py` (J identity) |
| §R5 · proxy definition | ε̂_X = max cross-block \|X_j′X_k\|/(n−1), standardized X, final partition; empty max = 0 | COMPLIANT: X and blocks only; deterministic; no feedback; label ✓ | — | — | HQ Q4: met | none | definition |
| C16 · proxy theorem | κ > 0 ⇒ δ_A ≤ (n−1)(p−1)ε̂/[1+(n−1)κ], δ_H ≤ (n²−1)(p−1)ε̂/[1+(n²−1)κ] | TRUE-AS-WRITTEN: row-sum norm ≤ (n−1)(p−1)ε̂, λ_min(A_D) = 1+(n−1)κ, λ_min(H_D) = 1+(n²−1)κ; bounds ≥ δ in all 150 W runs | DESIGN-VERIFIED (W: κ = .75, bound 2.5·10⁻⁶ vs δ 5.6·10⁻⁷ at 9⁶) | PLAUSIBLE | — | sufficient only: loses ≈ p/3 vs true δ at fixed ε | `w_family.py` |

## 5. Supplement cards whose statement changed in Round 2

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| C8 · resolution | bisection resolution at most h_V/2; T ≤ P + ⌈2/h_V⌉ + 1 | TRUE (W1 under this reading) | DESIGN-VERIFIED | PLAUSIBLE | W1 D7 AMBIGUOUS: REPAIRED | (b) minor: T26BUD-G's own AUTHOR-ONLY omitted | W1 cluster 9 |
| C8 · pilot extension | Global range D_*, 2⁻⁶⁰ ≤ h/2: each non-final pilot step ≥ h/2; P ≤ ⌈2/h⌉+1; T ≤ 2⌈D_*/c_ρ⌉+2; D_* = 0 ⇒ P = T = 1 | TRUE-AS-WRITTEN: 600 adversarial coded-pilot runs (two-point extremes, uniform, skewed; floor active and inactive), 0 violations; worst (h/2)/step = 0.496 | DESIGN-VERIFIED (W) | PLAUSIBLE: ESS(Δ) is monotone (convex log-MGF); every Δ ≤ h passes (Popoviciu); bisection keeps lo passing, so step ≥ h − 2⁻⁶⁰; the floor only adds | — | does not touch Conjecture P (stated) | `c8_pilot.py`; `v3_calib.h:30–47` |
| C10 · IC3 exhibit | n = 40, p = 20, columns 1 = 2, others orthogonal; corr²(y, x₁) = ½; two singleton duplicates are tied global start modes; SMC dispatch | TRUE-AS-WRITTEN: seat script reproduced exactly (7.858020937 / 4.91339373; 251,200). Actual data: own partition (B = 4) keeps {1,2} together; top scores {1} = {2} = 7.858020937 > {1,2} 4.913 > 3.069 | DESIGN-VERIFIED (2²⁰ > 251,200) | PLAUSIBLE (prefix-feasibility DP, W1 d9) | W1 D9 DESIGN-ASSERTED: REPAIRED | N3 OPEN kept ✓ | `c10_seat_script.py`, `c10_tie.py` |
| C11 · equality | strict separation + sizes ≤ B preserve groups; plus B < 2g_min ⇒ blocks = groups; counts/graph unchanged | TRUE-AS-WRITTEN: the coded top-down cut never splits a ≤ B subtree; next-fit cannot pack two groups; W/LH equality exactly from n = 9⁶ | DESIGN-VERIFIED | PLAUSIBLE | n ≥ 9⁶: REPAIRED; SIZE: REPAIRED | PART-CE2 respected ✓ | `w_family.py`; W1 cluster 19 |
| C12 · repairs | target equivariance only; T01 "PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY"; IC3 = C10 design | statement otherwise as W1 (TRUE) | DESIGN-VERIFIED (C10 design: rank-deficient, correlated) | PLAUSIBLE | W1 flag (b) T01: REPAIRED; equivariance wording: REPAIRED | none | IDX L469 |
| C15-TV · repairs | marginal law vs realized empirical law; default-4 bound labelled vacuous | as W1 (TRUE) | as W1 | as W1 | W1 cluster 16 / §0 item 4: REPAIRED | none | W1 cluster 16 |
| C15-CI · new form | \|π(C) − (1−α)\| ≤ TV(π̂_cell, π_cell) + \|π̂(C) − (1−α)\| for unions of cells; joint-output tail via C15-TV | TRUE-AS-WRITTEN (triangle inequality; set mass within cell TV) | DESIGN-VERIFIED (W, size cells d₀ = K+1, stacking) | PLAUSIBLE | HQ Q2 absolute-content reading: REPAIRED (not frequentist coverage) | none | derivation |
| C9, C13, C14, C15-KL | unchanged in substance (qualifiers only) | as W1 | as W1 | as W1 | C9 statistical-scope repairs: REPAIRED (stated) | none | W1 clusters 3, 9, 12, 16 |

## 6. Growth rates (§R6 item 7)

| card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence |
|---|---|---|---|---|---|---|---|
| C1/H · R′_n = 4⌈s⁶/4⌉, s = n + p | ≤ s² summaries, ε_n = 1/s: union bound O_P(s⁻²); truncation at 1 needs no uniform M₂ moment | TRUE-AS-WRITTEN: s²[4(M₂−1)/R′ + 4M₂s²/R′] = O_P(s⁻²); dominated convergence on min{1, ·} | DESIGN-VERIFIED (W: M₂ ≤ e^{D_*}) | PLAUSIBLE | SYNTH D11: REPAIRED (explicit (n,p) function; M₂ bound derived from the design) | s^{4+δ} suffices; s⁶ is about 2·10³⁴ islands at n = 9⁶ (practicality note) | derivation |
| C15 terminal · L = max{4, ⌈log₂(n+1)⌉} | On W, M₁ ≤ e^{D_*} = O_P(1), so q^L → 0 in probability | TRUE-AS-WRITTEN (q = 1 − 1/M₁ bounded away from 1 in probability; L → ∞) | DESIGN-VERIFIED | PLAUSIBLE | — | forward-KL rate disclaimed ✓ | derivation |
| C3/C4 · ℓ = ⌈log₂(n+p+1)⌉ | existing ℓ ≥ c − 1 = 1 on LH; default R′ = 4 suffices | TRUE-AS-WRITTEN (ℓ ≥ 1 for all n; "eventually" unnecessary) | DESIGN-VERIFIED | PLAUSIBLE | — | no delivery rate claimed ✓ | derivation |
| C16 · same R′_n | Ĵ − J → 0 in probability on W | TRUE-AS-WRITTEN (16D²M₂/(R′_nε²) → 0) | DESIGN-VERIFIED | PLAUSIBLE | — | none | derivation |

Every rate is an explicit function of (n, p) (ground rule 5/6). The only random quantity in the conclusions, D_*, is computed from the design and data. It enters as a derived O_P(1) bound on W, not as a hypothesis.
