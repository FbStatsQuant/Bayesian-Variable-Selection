# W2-VT24G — REPORT: adversarial verification of W1-T24G (restated T24, Theorem B)

Run of 2026-11-02, branch `theory/W2-VT24G`. I acted as an independent referee of
`origin/theory/W1-T24G:theory_campaign/W1-T24G/`. Nothing here has been reviewed. Every PROVED is a candidate.

The repairs are in `PROOF.md`. Working notes are in `NOTES.md`. Scripts (fixed seeds) are in `scripts/`, and
their outputs in `results/`.

**What the numerics were built on.** All numerics come from a new engine:
- `scripts/ref_engine.py` and `scripts/exact_laws.py`, written from METHODOLOGY_v3 and the production C++
  (`Scripts/SMC_BVS/core/cpp/v3_engine.h`, `v3_blocks.h`);
- it does not import any W1 code;
- it was validated by `scripts/validate_engine.py`: elementary laws are π-reversible, and the vectorised round
  agrees with a slow exact-law round to within Monte Carlo noise.

## 1. Headline

1. **Theorem B (restated T24): PROVED (candidate), after one repair.**
   - I checked it line by line against METHODOLOGY_v3 §6.5 and the production round code.
   - There is one GAP, and I fixed it. W1's Lemma F needs a hypothesis that two of its uses do not satisfy:
     Prop. B2's slot step, and Theorem B part (a). The union-bound form, **Lemma F′ (PROVED)**, gives the same
     conclusions without that hypothesis.
   - I found no ERROR in Theorem B, Props. U/B1/B2/D/A, Lemmas O/C/P, or Cors. B-unif/B-M/P1.
   - I also prove a free sharpening, **B1′/B2′ (PROVED)**: at |P| = 1 no deletability premise is needed, and
     c′₂ = 1 − H₁ ≥ 1/(B+3).
2. **CE1: COUNTEREXAMPLE, confirmed independently and strengthened. CE2: COUNTEREXAMPLE, confirmed.**
   - CE1 shows that H24's uniform exit input is far from small at n = 200. Monte Carlo puts the one-round exit
     probability at 0.62–0.98 in S2–S6 on W1's datasets and on fresh seeds.
   - New: an *exact* lower bound, from enumeration and with no Monte Carlo, is ≥ 0.39 in every S2–S6 cell.
   - New: **Lemma E (PROVED)** reduces the asymptotic CE1 to two named limits, which remain PROOF SKETCH.
   - Wording correction: H24 "as written" is satisfiable, trivially, with a_n = 0 and η_n = 1. What fails is
     its *asymptotic* input (L+4)η_n → 0.
3. **T21 route (e′) drop-in: VERIFIED as an implication, with three edits.** The edits are the asymptotic
   paragraph, the hypothesis list, and the eligibility set. Replacement text is in §6.
4. **Errors and gaps found elsewhere in W1.** None of them touches the theorem.
   - **ERROR in the §6 asymptotic sketch.** The equicorrelated-null inflation is 1 + r = 1.3, not 1.86. So NL0(1)
     fails in rate only for p ≫ n^{5/3}, not p ≳ n^{0.58}.
   - **GAP in the evidence.** W1's block packing is not the production packing. The start-law statements (the
     "S5 masked mode", Table T4b, the π₀-draw repair numbers) were therefore computed on a non-production π₀.
     Recomputed with production packing, the qualitative conclusions survive: 100% repair within 12 rounds in
     every cell.
5. **Usefulness: confirmed as asymptotic only, plus a new structural limit.** The bound is trivially ≥ 1
   whenever v(x) > H, and H = 12 at n = 200. With the look-alike budget A inside v, realistic incomplete starts
   can have v > 12. Cor. P1 is still the only non-vacuous finite-n statement, and its "a₁ ≥ 0.14" was shown only
   at B = 4.

## 2. Verdict table

Labels: VERIFIED = checked line by line, or reproduced independently; GAP = a step is missing or wrongly
justified (fixable or not); ERROR = a false statement, with a counterexample.

| W1 claim | Verdict | Evidence / note |
|---|---|---|
| §0 round model: (R1) order independent of state; (R2) each label once | VERIFIED | `v3_engine.h::draw_order` draws a Fisher–Yates permutation of all m labels before any step; `one_round` executes each label once |
| §0 kernels G_j, U, N_i, I (Hastings ratio, cap, empty-candidate rejection) | VERIFIED | `step_gibbs`, `step_uswap`, `step_nswap`, `step_indep` match line for line; my exact laws are π-reversible (`results/validate_engine.json`) |
| (R3), (R4): SR scoring | VERIFIED in the implementation | `step_gibbs` calls `held(P)` (current state) and `eval(flip)` (other configuration, if feasible). SR is still listed as "to be confirmed by Felipe" in 00_COMMON |
| (R5): conditional independence of terminal trajectories | VERIFIED under EX-S | `run_island_s`: no resampling in the L burn-in and Hm measured rounds. One RNG stream is shared sequentially; under EX-S each particle's uniforms are fresh at stopping times, so the trajectories are a product of Markov chains. Note: there are L+5 rounds at φ = 1 after the last resampling (the last bridge stage's round), so H = L+4 is conservative |
| Lemma F (first-failure bound) | GAP, fixable, **fixed** | Its hypothesis "non-failing steps stay in 𝓕" fails in the Prop. B2 slot step and in Theorem B (a), at S₀. Lemma F′ (PROOF.md §1) needs no closure hypothesis and gives exactly the bounds used |
| Lemma O (order facts) | VERIFIED | arrival-time realisation |
| Lemma C (binomial domination), and g_H(k) ≤ k(1−c)^{⌊H/k⌋} | VERIFIED | induction uses only P(J=1 \| past) ≥ c and monotonicity of g; block argument correct; exact check in `results/ce2_check.json` |
| Lemma P (first-change progress, c_poly) | VERIFIED | coupling valid up to the first change; ∫(1−t)^k(1−tQ)dt correct; a negative integrand only weakens the bound |
| Cor. P1 (distance-one scoring, a₁(x)) | VERIFIED (proof); numerics CONFIRMED | a₁ min 0.139–0.439 over the 12 cells, matching W1. Every a₁ ≤ the simulated scoring frequency (`results/p1_repair.json`). **Caveat:** shown only at B = 4. At production B = 14 the order factor drops to about 1/(B+3) = 1/17 unless the non-Gibbs labels are inactive |
| Prop. U (EXIT_d resolution) | VERIFIED as bookkeeping | Every undo is either bad (charged to η) or V-neutral (charged to the slot term h(l)). It does not make η small: that is premise TS/IND/NL0 territory |
| Prop. B1 (phase-1 progress) | VERIFIED | The missing set is constant on {no bad, no progress} because every truth removal is bad and every non-bad truth addition is progress. The added state is in 𝒵(x) and is feasible since s₀ + a ≤ K |
| Prop. B2 (phase-2 progress) | VERIFIED after the Lemma F′ fix | Slot and order bounds checked. Independently, c₂ at a = 1 reproduces W1's T4a values exactly (0.326 … 0.469), and the simulated P(no exit, not scored) ≤ 0.094 is below the bound in all 12 cells (`results/b2_check.json`) |
| c₂ ≥ 1/(B+3) − ε_del | VERIFIED | H_a ≤ (B+2)/(B+3) since \|P\| ≥ 1 |
| **Theorem B** | **VERIFIED** (PROVED, candidate) after the Lemma F′ fix | (a) bad steps ≤ Hη (Lemma F′); (b) J_h adapted with conditional probability ≥ c_*; (c) on {no bad, not scored}, V decreases by ≥ 1 per progress round and stays > 0, so Σ J_h ≤ v−1. Classification and phase transitions checked; V is nonincreasing on non-bad steps across the phase-1 → phase-2 jump (a+1+… → \|P\| ≤ a) |
| Prop. D (drift form) | VERIFIED | z^{−I+vN} ≤ z^{−I} + (z^{vN} − 1); P(I=0) ≤ 1−c_*+η; supermartingale for N; Y_H ≥ z on the bad event |
| Cor. B-unif | VERIFIED | immediate. Uniformity is not even needed for T21 (§6) |
| Cor. B-M (many particles) | VERIFIED; wording GAP | Product bound correct under (R5). "No η → 0 needed" is misleading: a per-particle bound β < 1 needs Hη < 1. So at n = 200 (η₂ ≈ 0.4–0.6) B-M is vacuous unless used with Cor. P1 |
| Prop. A (one-round sweep) | VERIFIED (proof) | ε₂ ≈ 2.6 not rechecked numerically |
| **CE1** (H24 uniform exit fails; 0.62–0.98 in S2–S6) | **CONFIRMED** (COUNTEREXAMPLE at n = 200); wording GAP | W1's data (seed 1): S1 0.16–0.22, S2 0.62–0.78, S3 0.90–0.96, S4 0.89–0.96, S5 0.93–0.97, S6 0.72–0.95. Fresh seeds 2–4: S2–S6 0.67–0.98. Exact lower bound ≥ 0.39 in S2–S6. (L+4)·exit = 7.5–11.8 in S2–S6 (`results/ce1_recheck.json`). Exit grows with n (`results/ce1_scaling.json`). "H24 is false" should read "H24's asymptotic input (L+4)η_n → 0 is false" |
| CE1 asymptotic sketch | PROOF SKETCH, reduced | Lemma E (PROVED) gives exit ≥ o*·[1−Q_T/(B+d+5)]/(B+d+4) for one missing truth. The remaining limits o* → 1 and Q_T → 0 are standard but not written out. The sketch must count every missing truth's Gibbs label in D (done in Lemma E) |
| **CE2** (the brief's (1−c′)^{⌊H/(s₀+d)⌋} is invalid) | **CONFIRMED** | exact rational check: the form fails in 395 of 1050 (v, H, c) cases, including v = 2, H = 12, c = 1/20 (0.88 > 0.74). W1's v(1−c)^{⌊H/v⌋} dominates in all cases |
| §6 table, NL0(a) row: "inflation ≈ 1.86, fails for p ≳ n^{0.58}" | **ERROR** (inside a PROOF SKETCH) | For equicorrelated nulls the max pairwise partial Z² is (1+r)·2 log p, not (1+r)/(1−r)·2 log p. Numerics: median ratio 1.08 → 1.21 for p = 10² → 10⁶ (`results/nl0_inflation.json`). Corrected threshold p ≫ n^{5/3}. The conclusion "NL0 needs a separate hypothesis" stands |
| §6 other rows (truth deletion at supersets, leakage at S₀, ε_del at a = 1, BTP, TS, TL, IND) | plausible; PROOF SKETCH, not upgraded | spot-checked the deletion-odds and leakage-at-S₀ rates; with B2′, ε_del is not needed at a = 1 at all |
| T4a (phase-2 constants, a = 1) | CONFIRMED | c₂ and η₂(1) = 0.37–0.64 reproduced exactly |
| T4b, "S5 masked mode {0,2,13,14}", π₀-draw repair table | GAP (evidence): non-production π₀ | W1 packs blocks in scipy `pre_order` leaf order. Production (`v3_blocks.h`) uses left child = smaller minimum index. The retained clusters agree but the blocks differ, e.g. S5. With the production packing: the S5 π₀ mode misses truth 6 (c = 1) or truths 6 and 15 (c = 0.5); round-1 repair is 0.19–0.25 in S5 (W1: 0.11–0.12); 100% within 12 rounds in all 12 cells (confirmed) |
| Scaling table (`scaling_reps.json`) | not rechecked | — |
| T21 (e′)/(e-M) drop-in (W1 §5) | VERIFIED with three edits | see §6 |

## 3. Statements (refined)

**Lemma F′, Prop. B1′, Prop. B2′, Theorem B′, and Lemma E** are stated in full in PROOF.md §§1–3. All are
PROVED (candidates).

**Theorem B′ (Theorem B, sharpened).** Use W1's setting and hypotheses: EX-A, EX-S, SR, φ = 1, and H terminal
rounds with no resampling. Use W1's families, potential and classification, and replace two constants:
- ε′_del(a) := sup{o_l(W) : W ∈ 𝒮_a°, |P(W)| ≥ 2, l ∈ P(W)}, with ε′_del(1) := 0;
- ε′_add excludes the distance-one state S₀∖{j} from its sup.

Then P_x(S₀ not scored within H rounds) ≤ P(Bin(H, c′_*) < v) + Hη, with c′_* = min(c′₁, c′₂) ≥ c_*. In
particular, for x = S₀ ∪ {l}: P_x(not scored in H rounds) ≤ P(Bin(H, 1−H₁) < 1) + Hη₂(1), where 1 − H₁ ≥ 1/(B+3)
deterministically.

**Corrected NL0 remark (PROOF SKETCH).** For an equicorrelated null family with correlation r, sup-superset
leakage at a = 1 is n^{−1/2} p^{r} up to polylog factors. So NL0(1) fails in rate only if p ≫ n^{1/(2r)}.

## 4. Evidence (my runs; all seeds fixed in the scripts)

**CE1** (`ce1_recheck.py`; 20000 reps per state; worst boundary state found among the 30 best by screening).
Data seed 1 is W1's data; seeds 2–4 are fresh.

| design | exit MC, seed 1 | exit MC, seeds 2–4 | exact lower bound P*_exit | (L+4)·exit |
|---|---|---|---|---|
| S1 | 0.16–0.22 | 0.12–0.37 | 0.07–0.24 | 1.4–4.5 |
| S2 | 0.62–0.78 | 0.67–0.90 | 0.39–0.73 | 7.5–10.8 |
| S3 | 0.90–0.96 | 0.85–0.96 | 0.57–0.73 | 10.2–11.6 |
| S4 | 0.89–0.96 | 0.90–0.98 | 0.57–0.78 | 10.7–11.8 |
| S5 | 0.93–0.97 | 0.82–0.97 | 0.58–0.77 | 9.8–11.7 |
| S6 | 0.72–0.95 | 0.80–0.94 | 0.53–0.73 | 8.7–11.4 |

**CE1 scaling** (`ce1_scaling.py`, c = 0.5, p = 20, B = 4). The exit probability does not decay:

| design | n = 200 | n = 3200 |
|---|---|---|
| S2 | 0.61–0.85 | 0.95–0.97 |
| S3 | 0.85–0.95 | 0.98 |

**Cor. P1** (`p1_and_repair.py`). The minimum of a₁ over the 20 distance-one states is:

| design | min a₁ |
|---|---|
| S1 | 0.375 / 0.439 |
| S2 | 0.162 / 0.175 |
| S3 | 0.158 / 0.184 |
| S4 | 0.184 / 0.183 |
| S5 | 0.158 / 0.165 |
| S6 | 0.139 / 0.184 |

The two values are c = 1 / c = 0.5. The worst state is S₀ minus a truth, except in S1. Every a₁ is below its
simulated frequency.

**Repair from 3000 raw π₀ draws, production packing, H = 12.** All designs reach 1.000 by H.

| design | scored in round 1 | by round 2 |
|---|---|---|
| S1 | 0.84–0.90 | 0.97–0.99 |
| S2 | 0.66–0.73 | 0.92–0.93 |
| S3 | 0.40–0.43 | 0.84 |
| S4 | 0.42–0.44 | 0.82–0.85 |
| S5 | 0.19–0.25 | 0.74–0.75 |
| S6 | 0.44–0.47 | 0.85–0.86 |

**v at π₀ draws.**
- The median of v = |M|+|A|+c is 2 in S1–S2, 5 in S3/S4/S6, and 8 in S5.
- The maximum is 17.
- The fraction with v > H = 12 is 0.10 in S5 at c = 0.5, and ≤ 0.002 elsewhere.

**Prop. B2 at a = 1** (`b2_check.py`):

| quantity | value |
|---|---|
| c₂ (W1's definition) | 0.326–0.469 (identical to W1's T4a) |
| c′₂ | 0.431–0.500 |
| η₂(1) | 0.37–0.64 |
| max over W of the simulated P(no exit, not scored) | 0.040–0.094 (≤ bound in every cell) |

**Engine validation** (`validate_engine.py`).
- Detailed-balance log residual ≤ 1.0·10⁻³. This comes from cancellation in 1 − o; the 508 pairs with
  underflowed odds are excluded, and there are 0 unexplained zero pairs.
- Fast vs slow round: TV distance 0.013/0.046/0.032, against a fast-vs-fast baseline of 0.012/0.038/0.028.

**CE2** (`ce2_check.py`): exact rationals; see the table above.

## 5. What fails, and why (referee routes tried)

- **Trying to break Theorem B through the phase-2 "slot" argument.** Neutral removal followed by re-insertion of
  l before G_l is harmless. A neutral removal after G_l is harmless too. The only defect was Lemma F's closure
  hypothesis, which is now fixed.
- **Trying to break B1 through truth-for-truth swaps.** W1 already classifies every truth removal as bad, so the
  missing set is constant on the event. No break.
- **Trying to break V monotonicity at the phase boundary.** Phase-2 V ≤ a < a+1 ≤ phase-1 V, and a non-bad
  step cannot re-enter phase 1, because that would be a truth removal. No break.
- **Trying to break (R5) through the shared RNG stream.** It holds under EX-S. It would fail only for a non-ideal
  generator, which is outside EX-S.
- **Trying to make Theorem B useful at n = 200.** This fails for two independent reasons:
  1. Hη ≥ 12 × 0.37 > 1, because π(S₀) ≈ 0.72 forces O(1) superset leakage per round. Any union-over-rounds
     bound has this problem.
  2. v > H makes the binomial term trivial. The cause is the one-unit-per-round credit (PROOF.md §5). A
     multi-step-per-round progress argument is OPEN.

## 6. T21 route (e′): checked against PROOF_v3.tex §"Route (e)"

PROOF_v3 uses H24 only in two places:
- eq. (H24), to get P(J | selection past) ≤ Hη and P(B_H | past) ≤ (1−a)^H, hence eq. (repair);
- the asymptotic paragraph.

Every later step uses only eq. (repair), its [0,1] cap, and the measurability of the selected state:
- the availability split P(A^c) + E[1_A min{1,·}];
- the final-run three-way split (eq. finalrepair);
- the pilot forward filtration.

So the drop-in is valid. Below, x is the selected state; it is past-measurable. Theorem B is applied conditional
on the selection past, which is legitimate because future randomness is fresh and the H rounds form a K₁-chain.
This gives P(M_H | past) ≤ β(x) := P(Bin(H, c_*(x)) < v(x)) + Hη(x). **No uniformity over an eligible set is
needed**, because β is a function of the past-measurable state.

**Edits required.**
1. **Statement (e).** Replace "Under H24 and SR, select an eligible particle (state in R_d)" with "Under SR,
   select a particle at a state x ≠ S₀ using only the available past". Replace (1−a_n)^H + Hη_n by β(x) (or
   β′(x) with the B′ constants). Delete H24 from §2 of STATEMENT.md, and from the open-item list in LOCKED, as a
   route-(e) input.
2. **Asymptotic paragraph.** Replace "Ha_n → ∞ and Hη_n → 0" by the following. On availability, with
   probability → 1: H·c_*(x) → ∞ with v(x) bounded, and Hη(x) → 0. Alternatively, through Prop. D: Hη_ex(x) → 0
   and η_in(x) → 0. For H = L+4, the sufficient premises are W1 §4's list (NL0, UDEL, TS, TL(𝒵,A), BTP, IND),
   all PROOF SKETCH or open, with W2's NL0 threshold correction.
3. **Multi-particle form (e-M).** P(M_H | population) ≤ ∏_i min{1, β(x_i)} over the particles at terminal start
   (R5). For a one-round version, use Cor. P1: ∏_{i: x_i △ S₀ = {j_i}} (1 − a₁(x_i)).

**Status of (e′).** VERIFIED as an implication. It is unconditional as a finite inequality (it may be vacuous).
It inherits T21's own CONDITIONAL status for everything else: H03, the exposure condition, and availability.

## 7. Needs escalation

1. **HQ decision: retire H24.** Route (e) should be rewritten with β(x) (§6). Do not cite "H24 is false"; cite
   "H24's asymptotic input is false in correlated designs (CE1, Lemma E)".
2. **Independent check of Lemma F′ and B2′.** These are short and should be quick for a different model family.
3. **The two limits in Lemma E** (look-alike attraction o* → 1, truth retention Q_T → 0) for a concrete block
   design under BM-∞. They need routine Bayes-factor asymptotics, written out.
4. **A non-vacuous finite-n single-particle repair bound.** It needs both a multi-step-per-round credit and
   state-averaged rather than sup rates. This is genuinely OPEN, and is the real obstacle to Thm 3 at n = 200.
5. **Felipe: confirm SR (R3/R4).** The code implements it (`held` + `eval`), but 00_COMMON lists it as "to be
   confirmed".
6. **Engineering note: W1's Python block packing ≠ production.** Any future campaign numerics that use π₀
   should use the `v3_blocks.h` rule (implemented in `scripts/ref_engine.py::complete_linkage_blocks`).

## 8. Outside scope

- **Cor. P1 at production B = 14** (p = 500/1000) is unmeasured. The order factor alone gives about 1/17, so
  "0.86^{N₁}" should not be quoted for production until it is measured.
- **The final bridge stage's round at φ = 1** (after the last resampling) is an extra terminal round. Every
  terminal bound may use H = L + 5 in the final run.
- Theorem B is not the operative mechanism at n = 200. The data (100% repair by 12 rounds, 0.75–1.0 progress
  per round) point to a drift argument with averaged rates. This is relevant to T37/T38 planning, and I did not
  pursue it.

## 9. Confidence cards

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Theorem B / B′ (restated T24, finite inequality) | PROOF.md §2 + W1 §4, with Lemma F′ | 0.95 | done (candidate); needs independent check of F′/B2′ | classification bookkeeping; Lemma F′ | no |
| Prop. U (EXIT_d resolution) | W1 §3 | 0.95 | done | it only relocates the problem into η | no |
| Cor. P1 (distance-one scoring) | W1 §2 | 0.98 (proof); numeric floor at production B unknown | done | value of a₁ at B = 14 | no |
| Cor. B-M / route (e-M) | W1 §4 + (R5) | 0.95 | done | delivery of many near-truth particles (T38), not this lemma | no |
| CE1 (H24's asymptotic input fails) | Lemma E + two limits | 0.93 | 0.8 (routine BF asymptotics) | o* → 1 and Q_T → 0 on one design family | no |
| CE2 | — | 1.0 | done | — | no |
| T21 route (e′) | §6 | 0.93 | done (text edits) | statement edits, and the asymptotic premises list | no |
| Asymptotic premises (W1 §4, with W2 NL0 fix) | W1 §4 | 0.7 | 0.45 | IND in the masked regime; TS/BTP under cancellation; NL0 for dense correlation | no |
| Useful finite-n single-particle repair at n = 200 | — | 0.6 (that some such bound exists) | 0.2 with the current technique | v > H vacuity and O(1) leakage; needs multi-step credit and averaged rates | no (H = L + 5 is free) |
