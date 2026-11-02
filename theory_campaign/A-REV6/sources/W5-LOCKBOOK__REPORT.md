# W5-LOCKBOOK — REPORT: lock the low-risk half

Cloud run W5-LOCKBOOK, branch `theory/W5-LOCKBOOK`, 2026-11-02. **Nothing here is reviewed or adopted.** Every PROVED
is a candidate that I checked line by line; this is a same-family (Claude-on-Claude) referee, not cross-family
review. Files: `AUDIT.md` (implementation lemmas), `PROOF.md` (T32(i) proof; referee notes §R1, §R2),
`STATEMENTS.tex` (paper statements, not compiled), `scripts/`, `results/`, `NOTES.md`.

## 1. Headline

1. **W2-BOOK refereed: no errors in the mathematics; three fixable gaps, one sharpening.** Lemma RO, Prop 2 (a)–(e),
   the ¾-covariance formula, Prop 1 (i′)/(iii′) and Thm 4 (C1′, (a), (d), (e′), (e-M), (d⁺)) check out. Gaps: the
   VAL-FP contract must require the exact run to share the status and 𝓒; the T23(ii-d) output corollary is false on the
   exact branch as written; the (iii′) certificate needs "strict beyond numerical error". Every number of
   `frozen_run_exact.py` and the guard COUNTEREXAMPLE was reproduced to every printed digit by independent code. The
   counterexample also survives the engine's real cost rule, where the bias can even be upward.
2. **W2-T26 refereed: Lemmas 1–3 and Theorem A are CORRECT.** That includes the flagged step, Lemma 3's use of T15 at a
   terminal-round prefix: it is exactly T12(i.b). Theorem B is correct as a conditional composition. Prop C stays a
   PROOF SKETCH; I found no error in its algebra. The p = 18 premise scan reproduces at n = 160, 2560 and 40,960 (66
   rows). One evidence gap: in 5 of the 66 rows W2-T26's block packing is not the production packing. It changes no
   conclusion.
3. **Code audit: GUARD, OUT, SR, STREAM and the scan-before-limit rule are PROVED by code reading** (read, not run).
   Every resource check ends the fit, and none touches an RNG, a setting, the inherited store or the cache. No failure
   mode reports a partial estimate. New caveats:
   - (G1) a stopped fit *does* return an incomplete HPM, so Thm 4 needs the convention 𝒢 ⊆ U;
   - (G2) partial island evidences sit in the `partial_final` archive field;
   - LS0 with `emit_centre = false` would let the cache hide the start mode from the HPM permanently, so
     `emit_centre = true` is mandatory, not cosmetic.
4. **T32(i) is PROVED** as a deterministic count:
   C_eval ≤ Σ_b2^{|C_b|} + Σ_e(1+4ℓ)H_e[1+m(T_e+L+4)] + 4N₁[1+m(T₁+L+4)] + (2ℓ+3)[1+(ℓ+1)M_p] + 2(ℓ+1)(40p+1) + 80p+1.
   The conjectured form follows as a corollary, so **Thm 5(c), polynomially many score evaluations, is now a theorem.**
5. **STATEMENTS.tex** gives Prop 1, Prop 2, Thm 4 (routes (a), (d)/(d⁺), (e′)/(e-M)) and Thm 6 ((P1) with the realised
   T_n), with hypotheses named, the run/output split applied and the n = 200 disclosure sentences.

## 2. Statements

The full paper forms are in `STATEMENTS.tex`. Changes relative to W2-BOOK and W2-T26:
- **Thm 4.** U must contain every stopped fit (G1) and every abort (G3). The cap term in (d⁺) is 1{ℓ < s₀ + d − 1}.
  (e′) eligibility = feasibility s₀ + a(x) ≤ K. (e-M) rests on Lemma STREAM.
- **Prop 2 (f).** VAL-FP(η, ε) is restated: on G_fp, the exact-arithmetic run on the same streams has the same status
  and the same 𝓒, and |log Ẑ^fp − log Ẑ̄| ≤ η.
- **Prop 1 (iv).** "Exactly computed score above S₀'s", or a gap beyond numerical error when used on data.
- **Thm 6.** (P1) is stated with the realised T_n. OUT holds for the estimate fields. The reported MPM is uncapped,
  which is harmless here.
- **T23(ii-d) output corollary.** Restrict to the SMC branch.
- **T32(i).** Theorem and two corollaries in PROOF.md §T32.
- **Implementation lemmas.** The one-line forms with file:line evidence are in AUDIT.md §7.

## 3. Proofs

- T32(i): PROOF.md §T32 (8 steps, every count tied to a code line).
- Lemma STREAM: AUDIT.md §4, a strong-Markov argument for an i.i.d. stream read at stopping times.
- Referee checks: PROOF.md §R1 (W2-BOOK) and §R2 (W2-T26).

### Verdict table: W2-BOOK

| Claim | Verdict | Note |
|---|---|---|
| GUARD as an implementation fact | CONFIRMED and extended | Every stop site read, including calibration (C1–C7, AUDIT §0–1). W2-BOOK read only the final-run sites. Add caveats G1–G4 |
| Lemma RO (1)–(4) | CORRECT | 𝒪 = 𝒢ᶜ ∩ 𝒪̄ verified in code |
| COUNTEREXAMPLE: conditioning on completion | CONFIRMED (reproduced exactly) | Also holds under engine-faithful costs (0.32% stops give E[Ẑ \| 𝒪] = 0.975Z; 3.0% stops give 1.0014Z) |
| Prop 2 (a), (b), (d) | CORRECT | Locked T12(iii) |
| Prop 2 (c), ¾-covariance, uses island independence T12(iv.c) | CORRECT | Reproduced: ¾Cov/Z = 0.130481, relative bias −0.131716, closed form = convolution to 10⁻⁵⁸ |
| Prop 2 (e1)–(e3) output level | CORRECT | Exact branch contributes 0 |
| Prop 2 (f) VAL-FP | GAP (wording), fixable | VAL-FP must include agreement of the exact run's status and 𝓒 |
| Prop 1 (i′) sharpness | CORRECT | ε-prior argument checked |
| Prop 1 (iii′) certificate | CORRECT; amendment | On data: gap beyond numerical error (the engine's bound is heuristic) |
| T06 "outer products" wording fix | CORRECT | Register one-liner needs the fix |
| Thm 4 (C1′) | CORRECT | Needs 𝒢 ⊆ U (G1) |
| Route (a) Q_f = 4N_e(T+L+5) | CORRECT | Counted against `run_island_s` |
| Route (d) | CORRECT | Needs scan completion: IMPL-LS(a) |
| (e′) vs W2-VT24G's three edits | CONSISTENT | Statement and eligibility: W2-BOOK's feasibility-eligibility is the right set. Asymptotic paragraph: W2-BOOK's premise implies VT24G's. Hypothesis list: matches. H ≤ L + 5 matches the code |
| (e-M) | CORRECT given (R5) | (R5) = Lemma STREAM (PROVED under EX-S) |
| (d⁺) T37 wiring | CORRECT as an implication; sharpened | Cap 1{ℓ < s₀ + d − 1} (scan-before-limit) |
| Split edits T11(iii), T14(i), T15, T25(iv), T31, T34 | CORRECT | Statement edits only |
| Split edit T23(ii-d) | GAP (scope), fixable | Fails on the exact branch; restrict to the SMC branch |
| `frozen_run_exact.py` numbers | REPRODUCED (independent code) | All seven values; identities to 10⁻⁶⁰ |
| 541-fit reading | not checked (data) | Interpretation; needs ANALYSIS-H2 |

### Verdict table: W2-T26

| Claim | Verdict | Note |
|---|---|---|
| Lemma 1 (Δ_n exact) | CORRECT | Grid check: \|Δ_grid − Δ\| ≤ 1.1·10⁻¹⁶ in 66/66 rows |
| Lemma 2 (ρ̄ exact, ρ̄ ≤ (B+3)u_π) | CORRECT | Exact product form re-derived |
| **Lemma 3: T15 at a terminal-round prefix (T12(i.b))** | **CORRECT** | Measured-round starts are populations after the stage-T round + L + h − 1 rounds at φ = 1, which is T12(i.b), i.e. T15 𝒯(b). W_r is unchanged after stage T. 𝔄 = {S₀} is fixed. (R3) holds in the code (STREAM) |
| Redundancy of (L+4)ρ* → 0 | CORRECT, and material | At n = 40,960: median (L+4)ρ* = 2.4–3.9 vs ρ̄ + u_π = 0.05–0.07 |
| Theorem A (A-0)(a)–(e) | CORRECT | Constants 3x, 27x, 108x checked |
| (A-i), (A-ii), output form | CORRECT | OUT verified in code (IMPL-OUT); T ≤ T^max verified (IMPL-T) |
| Theorem B (composition) | CORRECT, CONDITIONAL | On T03 and T22(iii)'s premises; EXP′ may now be removable via W1-EXP (not rechecked) |
| Prop C (ORTH) | PROOF SKETCH (kept) | Algebra re-done, no error; constants not written out |
| p = 18 premise scan | REPRODUCED at three sizes | 61/66 partitions identical; 5 rows use non-production packing (scipy leaf order), e.g. fav_iid n = 2560 seed 2: 1 − π₀(S₀) 0.180 (production) vs 0.150. Medians unchanged |

## 4. Evidence

### 4.1 Exact frozen-run law (`scripts/frozen_run_indep.py` → `results/frozen_run_indep.txt`)

This is written from the T12 STATEMENT, with explicit 2×2 Bayes factors and a round tensor
J[x, y, z] = (1/m!)Σ_σ Prefix_σ[x, y]·Suffix_σ[y, z], at 60 digits. Results:
- D = 8.146762406341, π₀({1,2}) = 0.027914117318, c₀ = 0.069471112691, c₁ = 0.998708337452, PIP₁ = 0.990618012243;
- E[P̄₁] − PIP₁ = −0.173974177850; E[ẐP̄₁]/(Z·PIP₁) − 1 = −0.131716;
- E Ẑ = Z and E ẐPIP̂ = Z·PIP to 10⁻⁶⁰.

Guard table under W2-BOOK's cost convention (reproduced) and under the engine-faithful one (new):

| convention | h | P(𝒪) | E[Ẑ \| 𝒪]/Z |
|---|---|---|---|
| both configurations paid (W2-BOOK) | 30 / 32 / 33 | 0.961367 / 0.990674 / 0.997834 | 0.01123 / 0.79784 / 0.97392 |
| flip only (engine, SR) | 16 / 19 | 0.970286 / 0.996830 | 1.00136 / 0.97524 |

### 4.2 p = 18 premise scan (`scripts/premise_indep.py` → `results/premise_indep.csv`, `premise_compare.txt`, `premise_partition_check.txt`)

The data generator is copied verbatim from W2-T26, with the same seeds. Everything else is my own: batched-Cholesky
scores for all 2¹⁸ models, an R13 complete linkage, the engine's neighbour graph, explicit per-label kernels at S₀,
and the ESS grid. Medians:

| design | n | 1−π₀(S₀) | δ₁ | Δ_n | T_ideal | (T+1)Δ_n | (T^max+1)Δ_n | ρ̄ + u_π | (L+4)ρ* |
|---|---|---|---|---|---|---|---|---|---|
| fav_iid | 160 | 0.287 | 0.266 | 0.319 | 2 | 0.98 | 1275 | 0.76 | 12 |
| fav_iid | 2560 | 0.0491 | 0.0750 | 0.0750 | 1 | 0.150 | 300 | 0.196 | 9.1 |
| fav_iid | 40960 | 0.0142 | 0.0171 | 0.0186 | 1 | 0.037 | 74 | 0.046 | 2.4 |
| fav_cor | 160 | 0.257 | 0.243 | 0.278 | 2 | 0.70 | 1114 | 0.67 | 12 |
| fav_cor | 2560 | 0.0687 | 0.0784 | 0.104 | 1 | 0.263 | 415 | 0.206 | 9.5 |
| fav_cor | 40960 | 0.0324 | 0.0273 | 0.0336 | 1 | 0.067 | 134 | 0.069 | 3.9 |
| masked | 160 | 0.623 | 0.244 | 0.653 | 5 | 3.9 | 2613 | 0.63 | 12 |
| masked | 2560 | 1.000 | 0.0954 | 1.000 | 18 | 19 | 4001 | 0.20 | 11.8 |
| masked | 40960 | 1.000 | 0.0228 | 1.000 | 25 | 26 | 4001 | 0.046 | 3.3 |

- Agreement with W2-T26's rows: on the 61 rows with identical partitions, every quantity agrees to relative 10⁻¹⁴.
- On the 5 others, 1 − π₀(S₀) differs by up to 20%, and δ₁ and T_ideal are unchanged.
- W2-T26's qualitative conclusions all reproduce:
  - Δ_n ≈ c·n^{−1/2} in the favourable designs;
  - (P1) holds with the realised T but fails badly with T^max;
  - the frozen P2 quantity stays ≥ 1;
  - in the masked design Δ_n → 1.

### 4.3 T32 counts (`scripts/t32_count.py` → `results/t32_count.txt`)

| n, p | C_eval bound (both tiers) | tier 0 only | conjectured form | local searches | their evaluations |
|---|---|---|---|---|---|
| 200, 500 | 2.68·10¹¹ | 1.62·10¹⁰ | 5.35·10¹¹ (= Sol J9) | 23 | 1.02·10⁷ |
| 200, 1000 | 5.62·10¹¹ | 3.40·10¹⁰ | 1.12·10¹² | 25 | 2.73·10⁷ |

The conjectured form minus the proved bound is positive on a grid up to n = p = 10⁷, as Corollary T32(i-lit) proves.

### 4.4 Stop rates (`scripts/wilson_indep.py`)

6/2,400 = 0.25% [0.11%, 0.54%]; S5 6/400 = 1.5% [0.69%, 3.2%]; S5 at p = 1000 5/200 = 2.5% [1.1%, 5.7%]. This
matches W2-BOOK.

## 5. What fails and why

- **"Every partial output is hidden" is false in the literal sense.** A stopped fit returns an incomplete HPM (G1),
  and the archive carries partial island evidences (G2). The theorems survive only through the conventions 𝒢 ⊆ U and
  "reported = estimate fields". These must be written into the statements, and they now are.
- **The literal T32(i) for logical events (2m per round)** is not obtained by my slack argument, because the held
  events use up most of the factor 2. It is cosmetic and not pursued.
- **T32(i) for wall time** is not attempted: it is not a count.
- **VAL-FP** cannot be measured here (no R/C++ build).

## 6. Needs escalation

1. **Cross-family read of AUDIT §1 item 4** (the list of stop sites) and of IMPL-SR(d) (the "every cache insertion was
   offered" argument). These two facts carry GUARD and the definition of 𝒮̄. A D61 same-seed replay is the empirical
   check.
2. **W1-T24G Theorem B′** is still unreviewed cross-family. (e′) and (e-M) inherit that.
3. **LS0 implementation:** `emit_centre = true` is required (AUDIT §5). Without it the HPM can miss the start mode
   for the rest of the run.
4. **Felipe:** confirm the conventions 𝒢 ⊆ U and "reported = estimate fields", and confirm SR.

## 7. Outside scope

- W2-T26's `bvs_exact.py` repeats the non-production packing that W2-VT24G found in W1-T24G (scipy leaf order instead
  of R13). Any other campaign script that reuses it inherits the issue.
- The reported MPM is uncapped (`v3_run.R:130`), while T07's Bayes rule over Ω is the capped one. This matters only
  when more than K PIPs exceed ½.
- The resource guard is shared between calibration and the final run, so the final-run stop probability depends on
  calibration time (G4). This is relevant to any model of P(𝒢).

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable, reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Implementation lemmas (GUARD, OUT, SR, STREAM, LS) | AUDIT §7 | 0.95 (code reading, not executed) | done; needs a replay and a second reader | completeness of the stop-site list; cache/offer invariant | no (LS0 needs `emit_centre = true`) |
| Prop 1 | STATEMENTS.tex | 0.98 | done | none | no |
| Prop 2 | STATEMENTS.tex with the VAL-FP repair | 0.97 | done | (f) needs a measured VAL-FP | no |
| Thm 4 (C1), (a), (d), (d⁺) | STATEMENTS.tex, 𝒢 ⊆ U | 0.97 | done | conventions; Thm 3 input for (d⁺) | no |
| Thm 4 (e′), (e-M) | STATEMENTS.tex | 0.9 | done as an implication | Theorem B′ review | no |
| Thm 6 | STATEMENTS.tex, realised T_n | 0.95 | done (now refereed once) | (P1) itself: favourable start at rate o(1/T_n) | no |
| T32(i) / Thm 5(c) | PROOF.md §T32 | 0.97 | done | the code-to-count mapping (re-check on any engine change) | no (LS0: +1 + (ℓ+1)M_p) |
