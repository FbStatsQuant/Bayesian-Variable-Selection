<!-- Filed by the chair: verbatim final message of PC2 (Opus 5.5, Claude Work), session ~/.claude/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/f9e42a05-8721-4d5a-83bf-0007029cda9b.jsonl. The checker's progressive working file is kept as VERDICTS_working_file.md. -->

# MEET-THM · Check wave 1 · Proof checker 2 · Seat C (R1_C.md) statement sanity

Checker: PC2 (Claude Opus 5.5; cross-family to Seat C = gpt-6-astra). Date 2026-11-04.

Scope:
- Every card of R1_C §D (D1–D13), §E (D14, priority) and §F (D15-TV, D15-KL, D15-CI).
- The R0_E statements those cards adopt (E:T05, T07, T08, T10–T14, T17, T19, T28, T01–T04), checked as Seat C uses them.
- The shared "explicit LH family" and the §E exhibit are checked once and cited.

**Never upgrade.** TRUE-AS-WRITTEN means no counterexample was found by the search stated; it is not a proof. Every Seat C status stays as the seat wrote it (new assemblies: PROOF SKETCH, unchecked). Where PC2 wrote out a derivation (Appendix A, D14), this is a route check, not a filed proof check.

**Scripts.** Python 3, numpy 2.0.2, scipy 1.13.1; fixed seeds; each under 1 minute; run locally. All are in `scripts/`:
- `bvs_common.py`: the actual target (M §5), the coded partition (M §6.3) and D14's D_*.
- `d14_bound.py`, `d14_hillclimb.py`, `d14_family.py`.
- `smc_coded.py`: a forced-dispatch v3.1 final-run replica, with the coded pilot and grid rules copied from `Scripts/SMC_BVS/core/cpp/v3_calib.h`.
- `d15_minor.py`, `misc_checks.py`, `d9_tiedp.py`, `d10_partition.py`, `lh_family.py`.

To reproduce, run `cd scripts && python3 <name>.py`; use `smc_coded.py mask` for the masked design.

## 0. Summary

| Verdict class | Count (56 claim clauses; status-only rows excluded) |
|---|---|
| TRUE-AS-WRITTEN | 54 |
| COUNTEREXAMPLE | 0 |
| NEEDS-HYPOTHESIS | 0 |
| AMBIGUOUS | 2 |
| DESIGN-VERIFIED | 53 |
| DESIGN-ASSERTED | 2 |
| DESIGN-FAILS | 0 |
| NONE-GIVEN | 0 (1 negative clause, D12, has non-vacuity n/a) |
| PLAUSIBLE | 53 |
| GAP | 3 |
| IMPLAUSIBLE | 0 |

Every non-clean verdict, one line each:
- **AMBIGUOUS — D7 coded-grid count:** "bisection resolution *at least* h/2" must read "at most h/2" (fine enough). Under that reading P + ⌈2/h⌉ + 1 holds, with 0 violations on the coded `build_grid` replica. The coded 60 halvings meet it whenever D_V ≲ 3.7·10¹⁷.
- **AMBIGUOUS — D14 §E "within/between separation gives the actual groups as blocks":** true only once B ≥ 9, i.e. p ≥ 81 and n ≥ 9⁶ = 531,441. Before that, B ∈ {4, 6} splits the groups, E then contains the 1/4 within-group correlations, and the δ-rates fail. The reading "for all large n" is true.
- **DESIGN-ASSERTED — D9:** "identical standardized columns produce symmetric table ties" gives a *start-mode* tie only if a duplicated column is in the start mode. This is easy to arrange (put the signal on the duplicated column), but the card does not say so.
- **DESIGN-ASSERTED — D5 region certification:** no design is shown where valid subtree envelopes cover a declared region within budget.
- **GAP — D5 region certificate route:** the branch-cover invariant and validated (outward-rounded) envelopes, N16, are not supplied. The card itself flags both.
- **GAP — D6 updated full count:** the integrated execution DAG is not audited (LS0, baseline-retaining search, rebuild factor). The card flags this.
- **GAP — D4 LS0 consistency route:** the mathematics covers v3 + LS0 and the potential run. Integrated LS0, emitted-centre fidelity (N2(c)) and GUARD-W (N2(e), also D12's premise) are unaudited. The card states this; it is an implementation gap, not a statement error.

Priority findings for the chair (§E, D14):
1. **The deterministic bound osc d ≤ D_* is true as written.**
   - No counterexample in 124 valid exact-enumeration cases at p ≤ 10, with coded and arbitrary partitions and correlated data.
   - The worst ratio osc/D_* over all valid cases was 0.499; a hill-climb reached only 0.45.
   - PC2 wrote out a four-step derivation (Appendix A) and found no gap. Status stays PROOF SKETCH.
2. **Its moment corollaries hold on the coded grid.**
   - Coded-grid replica: 1,600 islands, with both a good and a deliberately poor V.
   - On every path, each island's W lay in [e^{−osc}, e^{osc}]; E W = 1 within MC error; E W² ≤ e^{osc} ≤ e^{D_*}.
   - So "M₂ ≤ e^{D_*} on every successful coded grid" is true regardless of grid quality.
3. **The §E exhibit satisfies every hypothesis eventually, but it covers only vanishing correlation, and the bound is far from tight.**
   - At n = 10⁵ to 10⁸ (10 seeds), D_* has median 1.03–1.08, with a < 1, δ_A < 1, δ_H < 1 and r < 1.
   - The cross-block correlation 1/(np) = O(n^{−4/3}) is far below the sampling-noise scale.
   - The design is SMC-dispatched with blocks = groups only from n ≈ 5·10⁵.
   - The bound stays O(1) up to ε ≈ n^{−1/2}/p. At any fixed ε it diverges: at ε = 0.01, D_* ≈ 10² at n = 10⁵ and ≈ 6·10⁴ at n = 2·10⁷.
   - The true osc d also grows (≈ √n·ε at fixed p; `d14_bound.py` E-analog rows), so this is intrinsic, not slack.
   - On realistic correlated designs at n = 400, D_* = 54–203 nats against a true osc d of 2.7–5.2.
   - **The chair should record that the §5.3 theorem covers vanishing cross-block correlation, ε = O(n^{−1/2}/p), with signal energy O(√n). It is not a fixed-correlation result.**
4. **D1 and D15 finite-R bounds are vacuous at the shipped default R′ = 4.**
   - For every ε < 1 the bound is ≥ M₂/ε² ≥ 1.
   - They are informative only under stacking: R′ ≫ 4M₂/ε² for D1, R′ ≫ 4d₀M₂/ε² for D15.
   - §E's "budget consequence" (R = 4⌈(n+p)⁶/4⌉) is a v3.1 *stacking* configuration with R′ growing polynomially; ground rule 5 applies (declare the rate).

Flags (a)–(d), totals:
- **(a)** No Seat C clause relies on an index-§4 known-false claim:
  - D2 excludes DIL-DM(i).
  - D4 excludes C3-PGD and general LH locking.
  - D5 avoids the OCERT-C1 clauses.
  - D14 avoids the OPW2 perfect-refresh guess.
  - D13 avoids the STG-Wp/W″ O(1) claim.
- **(b)** No status word is stronger than the registry's. Three registry qualifiers are omitted:
  - D2/D4 cite Thm5-LH without its registry flag "SF VERIFIED (W3-VEXP); XF none" (SAME-FAMILY-ONLY).
  - D5 writes MZ-P3 "PROVED" without the registry's "(P3 top store, deterministic); P3′ conditional on T03 + discovery" and its AUTHOR-ONLY flag.
  - D11 writes "T01 reduction: PROVED-LOCKED"; the registry has "PROVED-LOCKED (wave 3; external review queued)", SAME-FAMILY-ONLY.
- **(c)** No hypothesis is a condition on the study. SR, GUARD-W and OP-LS0 are implementation premises and are explicitly named.
- **(d)** Variant scope:
  - D13 is about the ideal grid (labelled).
  - D3 is about start-only/one-shot comparison variants (labelled).
  - D4 is v3 + LS0 mathematics; integrated LS0 is unaudited (labelled).
  - D1, D15-TV and D15-CI are vacuous at R′ = 4 (not labelled; see item 4).
  - D14's budget consequence requires stacking. It is labelled "not a recommended allocation", but ground rule 5 applies.

Novelty note (not a verdict): registry row `OWS-WS4`, "perturbation in the standardised cross-block Gram" (PROVED, author-only, H-ORTH scope per index §1 S4), is the nearest prior project result to D14's route. D14's NEW-COMP claim should cite it and say how it differs.

## Shared objects (checked once)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| Shared · LH family | λ_min(Σ) ≥ 0.4; centred realisation p ≤ n−1; eventually B = 16, 9 ≤ B < 18; complete linkage recovers groups; masked hubs zero marginal covariance | TRUE-AS-WRITTEN: λ_min = 0.4212; cov(x_b, y) = 0 exactly; strict separation 0.6 < 0.8 | DESIGN-VERIFIED (eventually): B = 9 at n = 10⁶, 16 at 2·10⁷; at n = 46,656 (p = 36, B = 6) groups are split | PLAUSIBLE | none; "eventually at least 36" is fine, but blocks = groups needs n ≥ 9⁶ | `lh_family.py`; LH-LAT m₀ = 0.0325 > 0 |
| Shared · §E family | groups of 9 at 1/4, cross ε_n = 1/(np), two n^{−1/4} signals; λ_min ≥ 3/4 − 1/n | TRUE: λ_min = 0.75 (the cross part acts on group-constant vectors only) | DESIGN-VERIFIED eventually: exact branch at n = 10⁴ (p = 18); blocks = groups from n ≈ 5.3·10⁵ | PLAUSIBLE | correlation O(n^{−4/3}); see summary item 3 | `d14_family.py` |

## Cluster 2 — Theorem H (D1)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D1 · general-h identity (N1) | E[W_r H_r(h) \| 𝒞] = π(h) for prescribed bounded measured-endpoint records | TRUE-AS-WRITTEN: coded-grid replica (400 islands × 2 designs × 2 V); size = 2 and pair{0,3} indicators within 0.1–2.0 se | DESIGN-VERIFIED (own p = 9 correlated and masked designs, forced SMC dispatch) | PLAUSIBLE (T12 marked-endpoint extension; N1 is PROOF SKETCH) | none | `smc_coded.py` (both designs) |
| D1 · RB marginal records | same identity for primary marginal RB PIP records at pre-Gibbs positions | TRUE: max \|E[W·PIP_rb] − PIP\|/se = 1.08–1.56 over 9 coordinates | DESIGN-VERIFIED | PLAUSIBLE (FMP-M1 PROVED, XF VERIFIED; status verbatim ✓) | none | `smc_coded.py` |
| D1 · finite-R ratio bound (PC1c3) | P(\|μ̂ − π(h)\| > ε \| 𝒞) ≤ min{1, 4(M₂−1)/R + 4M₂/(Rε²)} | TRUE: re-derived (denominator event B̄ ≥ ½, Chebyshev, \|H − π(h)\| ≤ 1) | DESIGN-VERIFIED only for R > 4M₂/ε²; at R′ = 4 the bound is ≥ 1 for every ε < 1 | PLAUSIBLE (PC1c3 PROVED, N1 premise ✓) | (d) vacuous at default R′ = 4; needs stacking | derivation; `smc_coded.py` prints bound = 1.000 at R = 4 |
| D1 · class union + truth anchor | union bound over a predeclared class; \|π(h) − h(S₀)\| ≤ 1 − π(S₀) for 0 ≤ h ≤ 1 | TRUE (elementary) | DESIGN-VERIFIED | PLAUSIBLE | none | Σ_{S≠S₀} π(S)\|h(S) − h(S₀)\| ≤ 1 − π(S₀) |
| D1 · MPM margin transfer (K62, E:T28) | uniform PIP error below min_j \|PIP_j − ½\| transfers the MPM decision | TRUE (elementary) | DESIGN-VERIFIED | PLAUSIBLE | none | threshold argument |
| D1 · IC3 | §E family gives M₂ = O_P(1) | TRUE conditional on D14 (PROOF SKETCH) | DESIGN-VERIFIED (D_* ≈ 1.03–1.08) | PLAUSIBLE | depends on unchecked D14 | `d14_family.py` |

## Cluster 3 — Output events, Z𝒯, certificate card (D5, D12)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D5 · envelope | m(S) ≤ U_m gives U = Z_𝒯 + U_m[1 − Σ_𝒯 ϖ] ≥ Z | TRUE: 40 designs × 5 random stores, 0 failures (U_m = N17 envelope) | DESIGN-VERIFIED (incl. duplicate columns) | PLAUSIBLE (N17 PROVED ✓) | none | `misc_checks.py` D5U, D11env |
| D5 · TV certificate | TV(π, π(·\|𝒯)) = 1 − Z_𝒯/Z ≤ 1 − Z_𝒯/U | TRUE (identity holds to 1e−9) | DESIGN-VERIFIED | PLAUSIBLE | none | `misc_checks.py` D5TV |
| D5 · underestimation / LCB | Ẑ < Z_𝒯 certifies Ẑ < Z; max{Z_𝒯, αẐ} is a joint-output lower bound at level 1 − α | TRUE (Z_𝒯 ≤ Z pointwise; Markov; the output form needs GUARD-W) | DESIGN-VERIFIED (item-1 certified 10/12 record) | PLAUSIBLE (N6 CORRECT WITH AMENDMENT ✓) | none | event containment |
| D5 · region certification | needs valid subtree envelopes covering the region; budget exhaustion unresolved | TRUE (definitional) | DESIGN-ASSERTED | GAP: branch-cover invariant and N16 validated envelopes not supplied (card says so) | (b) MZ-P3 qualifier and AUTHOR-ONLY flag omitted | card text; IDX MZ-P3 row |
| D12 · joint failure bound | potential-run P(B \| 𝒞) ≤ α gives P(𝒪 ∩ B \| 𝒞) ≤ α under stop-only coupling/GUARD-W | TRUE (event containment) | DESIGN-VERIFIED (any input) | PLAUSIBLE; the GUARD-W audit is an implementation gap | none | LemmaRO PROVED, XF VERIFIED* ✓ |
| D12 · no conditional claim | nothing follows for P(B \| 𝒪, 𝒞) | TRUE (CEX-guard COUNTEREXAMPLE, XF VERIFIED* ✓) | n/a (negative statement) | PLAUSIBLE | none | IDX §4.A CEX-guard |

## Cluster 4 — Weight stability §5.3 (D14, §E) · PRIORITY

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D14 · deterministic bound | if a, δ_A, δ_H, r < 1 then osc d ≤ D_* = νa²/[2(1−a)] + 2b_X, any partition | TRUE-AS-WRITTEN: 255 cases (124 valid), 0 violations; max osc/D_* = 0.499; hill-climb (8 seeds × 400 steps, p = 4–6) max 0.446 | DESIGN-VERIFIED (§E family; own correlated designs) | PLAUSIBLE: route written out in Appendix A, no gap; key lemmas are restriction monotonicity of z′H⁻¹z and of relative norms | none | `d14_bound.py`, `d14_hillclimb.py` |
| D14 · one-shot / increment χ² | E_{π₀}[(π/π₀)²] ≤ e^{D_*}; χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1 | TRUE: 0 failures (all valid cases; u ∈ {0, …, 0.9}; Δ ∈ {.05, .1, .3}) | DESIGN-VERIFIED | PLAUSIBLE (E e^{2Δd}/(E e^{Δd})² ≤ e^{Δ osc d}) | none | `d14_bound.py` |
| D14 · actual-grid moment | on every successful coded grid M₂ ≤ e^{D_*}; actual kernels retained | TRUE: W ∈ [e^{−osc}, e^{osc}] on every path in 1,600 islands (coded pilot + `build_grid` replica, good and poor V); E W = 0.998–1.004; E W² ≤ 1.02 | DESIGN-VERIFIED (forced dispatch: the exact branch would fire at p = 9) | PLAUSIBLE: product of stage averages lies in [e^{Δ_t d_min}, e^{Δ_t d_max}], Σ Δ_t = 1, then EW = 1 (T12/N9) | none; independent of pooling and LS0 | `smc_coded.py` |
| D14 · §E rates | a = O_P(n^{−1/2}); δ = O(1/n); νa² = O_P(1); Kδ = o(1); νr = o_P(1); D_* = O_P(1) | TRUE: medians a = 2.0e−2 → 2.0e−4; νa² ≈ 2.06–2.13; Kδ ≤ 6e−4; νr ≤ 1.7e−3; D_* ≈ 1.03–1.08 (n = 10⁴…10⁸) | DESIGN-VERIFIED (eventually; SMC from n ≈ 10⁵, blocks = groups from ≈ 5.3·10⁵) | PLAUSIBLE | cross corr 1/(np) = O(n^{−4/3}); at fixed ε, D_* → ∞ (true osc d also grows) | `d14_family.py` |
| D14 · groups = blocks (§E) | within/between separation gives the actual groups as blocks | AMBIGUOUS: true for n ≥ 9⁶ (B ≥ 9); false for 5,832 ≤ n < 531,441 (B ≤ 8 splits groups) | DESIGN-VERIFIED for large n | PLAUSIBLE (PART-ThmA) | add "for n ≥ 9⁶" | `d14_family.py` (blocks=groups column) |
| D14 · grid gap disappears | Ẑ/Z ≤ e^{D_*} on every path, regardless of grid quality or mixing | TRUE (0 violations on any path, poor-V grid included) | DESIGN-VERIFIED | PLAUSIBLE | none | `smc_coded.py` V = poor |
| D14 · budget consequence | for ≤ (n+p)² predeclared summaries, R = 4⌈(n+p)⁶/4⌉ gives simultaneous o_P(1) error on the family | TRUE given N1, PC1c3 and D14 (union bound ~ (n+p)^{−4}M₂/ε²) | DESIGN-VERIFIED | PLAUSIBLE | (d) needs stacking R′ growing polynomially in n + p; ground rule 5 rate must be declared | derivation |
| D14 · statuses | new extension PROOF SKETCH; O-WSTAB keeps H-ORTH/ideal-grid statuses | consistent with IDX §1 S4 (no stronger word) | — | — | novelty: cite OWS-WS4 | IDX S4 rows |

## Cluster 5 — The start (D2)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D2 · exact factorisation | π₀(S) = A(\|S\|) Π_b q_b(S_b), A(k) = ϖ(k) Π B_b / Z̄₀, every feasible S | TRUE: 40 designs, all feasible S, error < 1e−8 | DESIGN-VERIFIED | PLAUSIBLE (DIL-E PROVED, XF VERIFIED ✓) | none | `misc_checks.py` D2 |
| D2 · LH masking law | π₀(S₀) = p^{−2} n^{−1} e^{O_P(1)} while π(S₀) → 1 | TRUE as cited: W1-EXP Thm 5(b) with c = 2, and 5(d) | DESIGN-VERIFIED (\|ψ\| = 0.2 < ρ = 0.4; g ≤ B < 2g eventually; exact Gram; fixed β) | PLAUSIBLE (T27(i) PROVED-LOCKED, CONDITIONAL ✓; Thm3/4-EXP) | (b) Thm5-LH's "SF VERIFIED; XF none" (SAME-FAMILY-ONLY) not stated; DIL-DM correctly excluded | IDX S1 rows; `lh_family.py` |

## Clusters 6–7 — Reported HPM, LS0, Theorem A, composition (D4)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D4 · LS0 consistency on LH | under G, A, SR, GUARD-W, OP-LS0, emitted start-mode centre, complete scans, ℓ ≥ 1: P(𝒪, Ŝ⁺ ≠ S₀) → 0 | TRUE as cited (T38-b1-LH PROVED, SF/XF VERIFIED* ✓) | DESIGN-VERIFIED: premises of W4-T38FULL (b1-LH) hold; LH-LAT m₀ = 0.0325 > 0; ℓ = ⌈log₂(n+p+1)⌉ ≥ 1 | GAP: integrated LS0, N2(c,e), tie-DP (stated) | (d) v3 + LS0 mathematics; avoids C3-PGD and general LH locking ✓ | `lh_family.py`; W4-T38FULL REPORT L40–51 |
| D4 · LS-score | capped tie-aware TD′ progress gives the max{Φ(S°) − 1, 0} scoring bound | TRUE as cited (LS-score PROVED, XF VERIFIED* ✓) | DESIGN-VERIFIED (Φ(S°) = c = 2) | PLAUSIBLE | none | IDX R3/R5 rows |

## Cluster 8 — SEP + Lemma KL (D3)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D3 · miss probability | Q iid start draws miss S₀ with probability (1 − a_n)^Q | TRUE (independence) | DESIGN-VERIFIED (LH) | PLAUSIBLE (SEP-A PROVED, XF VERIFIED ✓) | none | elementary |
| D3 · χ² bound | 1 + χ²(π‖π₀) ≥ π(S₀)²/a_n | TRUE: every S₀ in 40 designs | DESIGN-VERIFIED | PLAUSIBLE | none | `misc_checks.py` D3chi |
| D3 · KL bound | KL(π‖π₀) ≥ π(S₀) log(1/a_n) − log 2 | TRUE (binary coarsening + entropy ≤ log 2); 0 failures | DESIGN-VERIFIED | PLAUSIBLE (KL PROOF SKETCH ✓ verbatim) | none | `misc_checks.py` D3KL |
| D3 · IS variance | unnormalised evidence relative variance = χ²(π‖π₀)/Q | TRUE (iid IS identity) | DESIGN-VERIFIED | PLAUSIBLE (SEP-B PROVED, XF VERIFIED ✓) | (d) comparison variant, labelled | elementary |

## Cluster 9 — Stage laws, restricted-ESS geometry (D7, D13)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D7 · missing-mass identity (E:T14) | ρ_full(u,v) = ρ_V(u,v) a_u a_w / a_v², w = 2v − u | TRUE: 300 synthetic families; log-identity holds to 1e−8 | DESIGN-VERIFIED | PLAUSIBLE (three-normaliser cancellation) | none | `misc_checks.py` D7id |
| D7 · transfer | a_u, a_w ≥ 1 − η and ρ_V ≥ 0.9 give ρ_full ≥ 0.9(1−η)² | TRUE (a_v ≤ 1); 0 failures | DESIGN-VERIFIED | PLAUSIBLE | none | D7transfer |
| D7 · increment h (E:T13) | every increment ≤ h = 2√log(10/9)/D_V passes | TRUE (Popoviciu: F″ ≤ D_V²/4); 0 failures | DESIGN-VERIFIED (§E: D_V ≤ D_* = O_P(1)) | PLAUSIBLE | none | D7h |
| D7 · coded count | P pilot targets and bisection resolution "at least" h/2 give ≤ P + ⌈2/h⌉ + 1 insertions, absent ceiling/snap failure | AMBIGUOUS: true with resolution ≤ h/2 (0 violations on the coded `build_grid` replica, incl. snap and validation) | DESIGN-VERIFIED | PLAUSIBLE (monotone ρ_V; each bisection step ≥ h/2) | P itself uncontrolled (Conjecture P OPEN) | D7count; `v3_calib.h` L68–100 |
| D7 · statuses | STG-L0/L1/G PROVED, no checks; T26BUD-G PROVED, deterministic | verbatim ✓ | — | — | none | IDX D2 rows |
| D13 · ideal crossing | ideal two-state bridge, initial log odds −A, exact maximal ESS-0.9 grid: log₂A + O(1) stages | TRUE: stages − log₂A ∈ [5.7, 6.7] for A = 10…10¹² | DESIGN-VERIFIED (comparison object) | PLAUSIBLE (odds halve per stage) | (d) ideal grid, labelled; STG-M PROVED, XF VERIFIED* ✓ | `misc_checks.py` D13 |

## Cluster 12 — Target consistency (D8)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D8 · T03♯ restatement | R1, G, R, SE_λ(j₀), SE_w(m♯; g₀), BM give 1 − π(S₀) = O_P(√(log n/n)); exact HPM/MPM consistent | TRUE as cited: matches W6-FIXREV2 §1.1–1.2 verbatim, incl. j₀ and fixed g₀ | DESIGN-VERIFIED (LH: λ_min ≥ 0.4 gives SE_λ and SE_w with g₀ = 0.4(n−1); ‖μ‖² ≤ Mn; fixed β gives BM-∞; p ≤ n^{1/3}) | PLAUSIBLE (PROVED, SF/XF VERIFIED ✓) | none | FIX L16–56; `lh_family.py` |
| D8 · no beta-min | only T03♯(iv)'s large-signal inclusion clause | TRUE as cited | DESIGN-VERIFIED | PLAUSIBLE | none | FIX (iv) |

## Cluster 13 — Work, depth (D6)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D6 · final run | work RN(T+L+4)m step slots; island depth N(T+L+4)m, times waves when workers < R | TRUE as counting (M §6.8; AMENDMENT #19) | DESIGN-VERIFIED (any input) | GAP: integrated DAG audit (stated) | none | METHOD v3 §6.8; amendment #19 |
| D6 · calibration and LS | (1+4I_e)H_e work, (1+I_e)H_e 4-worker depth, I_e ≤ ℓ; LS ≤ (ℓ+1)[p + k*(p−k*)] | TRUE (amendments #18, #42) | DESIGN-VERIFIED | PLAUSIBLE | statuses verbatim ✓ (MA-PropD, T32(i), Cost-T38) | AMENDMENT_HQ_01 §2 |

## Cluster 16 — Approximation error §5.4 (D15-TV, D15-KL, D15-CI)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D15-TV · round minorisation (E:T10) | full production round minorises q_φ by 1/M_φ, no 1/m factor | TRUE: exact kernels, all 40,320 orders, φ ∈ {0.3, 1}; min K(x,y)/q(y) equals 1/M_φ exactly | DESIGN-VERIFIED (p = 4, n = 20, actual graph) | PLAUSIBLE (independence step in every order; invariant steps before and after) | none | `d15_minor.py` |
| D15-TV · law TV | terminal-particle marginal TV after L rounds ≤ (1 − 1/M₁)^L | TRUE: holds for every L = 1…8 | DESIGN-VERIFIED | PLAUSIBLE | none | `d15_minor.py` |
| D15-TV · realised cell TV | P(TV > ε \| 𝒞) ≤ min{1, 4(M₂−1)/R + 4d₀M₂/(Rε²)} | TRUE: re-derived with 2d₀M₂/(Rε²), since Σ_c(η_c − π_c)² ≤ 2; the card's 4 is conservative | DESIGN-VERIFIED only for R ≫ 4d₀M₂/ε²; vacuous at R′ = 4 | PLAUSIBLE (N1 for cell indicators is a premise) | (d) needs stacking | derivation; `smc_coded.py` |
| D15-TV · IC3 | §E family: M₁ ≤ e^{D_*} = O_P(1); L → ∞ gives law convergence | TRUE (M₁ = e^{d_max}/E_{π₀}e^d ≤ e^{osc d}) | DESIGN-VERIFIED | PLAUSIBLE | none | `d14_family.py` |
| D15-KL · mixture KL | λ_L = (1−q^L)π + q^Lν_L; KL(π‖λ_L) ≤ −log(1 − q^L); KL(λ_L‖π) ≤ q^L log(1/π_min) | TRUE: residual kernel ≥ 0 (min 9.4e−4); bounds hold for L = 1…8 and 200 random mixtures | DESIGN-VERIFIED | PLAUSIBLE | none | `d15_minor.py`; `misc_checks.py` D15KLmix |
| D15-KL · forward empirical | KL(π̂‖π) ≤ χ²(π̂‖π) ≤ 4TV²/π_min | TRUE: 0 failures | DESIGN-VERIFIED | PLAUSIBLE | none | D15KLemp |
| D15-KL · reverse obstruction | a positive-mass state missing from the records makes KL(π‖π̂) = ∞; surely so if \|Ω\| > 4NR | TRUE (by definition) | DESIGN-VERIFIED: even with 4NR = 480,000 ≫ \|Ω\| = 512, 346–407 states are never recorded | PLAUSIBLE | none | `smc_coded.py` |
| D15-CI · set content | if P(TV > ε) ≤ δ, an output-selected C with π̂(C) ≥ 1 − α has P(𝒪, π(C) < 1 − α − ε) ≤ δ under GUARD-W | TRUE (simultaneous over all sets of the cell σ-field) | DESIGN-VERIFIED | PLAUSIBLE | none | elementary |
| D15-CI · size intervals | the size partition d₀ = K + 1, via the size accumulator, gives the same statement | TRUE (only for unions of size cells) | DESIGN-VERIFIED for R ≫ (K+1)M₂/ε²; vacuous at R′ = 4 | PLAUSIBLE | (d) stacking; not frequentist coverage (card says so) | derivation |

## Cluster 17 — Tie DP (D9)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D9 · greedy tie DP | take the smallest maximising size, then include the smallest index whenever an optimal consistent completion exists; this gives the lexicographically smallest start maximiser | TRUE: 400 random integer-table instances (heavy ties, interleaved block indices), 0 mismatches vs brute force | DESIGN-ASSERTED (a tie needs a duplicated column in the start mode); n = 40, p = 20 dispatch verified (2²⁰ > 251,200) | PLAUSIBLE (prefix-feasibility max-plus). E:T07's union-order lemma also checked true: for equal sizes, lex order goes to the owner of min(AΔA′) | N3 OPEN ✓ verbatim | `d9_tiedp.py` |

## Cluster 19 — Blocks, graph (D10)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D10 · separation (E:T05) | with strict separation and sizes ≤ B, groups never split; if all groups > B/2, blocks = groups | TRUE: 300 instances (shuffled indices), 0 failures | DESIGN-VERIFIED eventually (LH and §E: B ≥ 9 for n ≥ 9⁶) | PLAUSIBLE (PART-ThmA PROVED, XF VERIFIED* ✓) | PART-CE2 respected | `d10_partition.py` (1) |
| D10 · counting | ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉; Σ 2^{\|C_b\|} ≤ p2^B/B | TRUE: 300 random matrices, 0 failures | DESIGN-VERIFIED | PLAUSIBLE (adjacent next-fit sums > B; 2^x/x nondecreasing) | none | `d10_partition.py` (2) |
| D10 · graph (E:T08) | ≤ pB edges; no isolated vertex for p > 1 | TRUE: 300 inputs, 0 failures | DESIGN-VERIFIED | PLAUSIBLE | none | `d10_partition.py` (3) |

## Cluster 20 — Target lemmas (D11)

| card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence |
|---|---|---|---|---|---|---|
| D11 · propriety and envelopes (E:T02) | for n ≥ 3: proper target; Q_S ≥ Y/(n+1); 1 ≤ det H/det(G+I) ≤ (n+1)^{\|S\|}; Z ≤ C_n(2b₀ + Y/(n+1))^{−ν} | TRUE: 40 designs, all S, 0 failures (incl. duplicate columns) | DESIGN-VERIFIED | PLAUSIBLE (N17 PROVED ✓) | none | `misc_checks.py` D11, D11env |
| D11 · invariance (E:T01) | target probabilities are affine-invariant and permutation-equivariant | TRUE (sign conjugation of G and H; relabelling) | DESIGN-VERIFIED | PLAUSIBLE | (b) T01: registry "PROVED-LOCKED (wave 3; external review queued)", SAME-FAMILY-ONLY | IDX R1 T01-T03 row |
| D11 · contrast regression | IG shape a₀ + ½, rate b₀s_y² | TRUE (matches M §5: IG(0.51, 0.01 s_y²)) | DESIGN-VERIFIED | PLAUSIBLE | none | METHODOLOGY_v3 §5 |
| D11 · exact branch (E:T04) | enumeration is exact; every fixed-p sequence eventually dispatches (N₀ ≥ n) | TRUE | DESIGN-VERIFIED | PLAUSIBLE | none | M §6.2 |
| D11 · IG perturbation | the exact pairwise coefficient is 2νb₀ (not nb₀) | TRUE: \|log(1+x₁) − log(1+x₂)\| ≤ \|x₁ − x₂\| with x = 2b₀/Q | DESIGN-VERIFIED | PLAUSIBLE | none | derivation |

## Appendix A — PC2's derivation of D14's deterministic bound (route check, not a filed proof)

Notation as in the card: G_D is the block-diagonal part of G, E = G − G_D, and ν = a₀ + n/2. For a feasible S, the D-quantities (A_{D,S}, H_{D,S}, Q_{D,S}) are the ones built from G_{D,S}.

1. **Exact split.** d(S) = d_D(S) + [f(S) − f_D(S)] + [g(S) − g_D(S)], where f = −½[log det H_S − log det A_S] and g = −ν log(2b₀ + Q_S). The split is exact because the table terms Σ_b log r_b(S_b) see only the diagonal blocks.
2. **Orthogonal part.** Let t_b = n z_b′H_b^{−1}z_b/(2b₀ + Y) and x = Σ_b t_b.
   - Then d_D(S) = ν[Σ_b log(1 − t_b) − log(1 − x)], which lies in [0, νx²/(2(1−x))].
   - The principal-submatrix inequality z_S′(H_D)_{SS}^{−1}z_S ≤ z′H_D^{−1}z gives x ≤ a.
   - Hence osc d_D ≤ νa²/[2(1−a)].
3. **Determinant part.**
   - For every v supported on S: \|v′Ev\|/v′A_Dv ≤ δ_A and \|(n+1)v′Ev\|/v′H_Dv ≤ δ_H.
   - So the eigenvalues of I + M lie in [1 − δ, 1 + δ].
   - Hence \|f − f_D\| ≤ (K/2)[−log(1−δ_A) − log(1−δ_H)].
4. **Residual part.** Write t and t_D for the full and block-diagonal quadratic gains.
   - Using w′(I+M)^{−1}w − w′w = −w′(I+M)^{−1}Mw, we get \|t − t_D\| ≤ [δ_H/(1−δ_H)] t_D.
   - With t_D ≤ a, this gives (2b₀ + Q_S)/(2b₀ + Q_{D,S}) ∈ [1 − r, 1 + r], so \|g − g_D\| ≤ −ν log(1 − r).
   - Steps 3 and 4 together give \|d − d_D\| ≤ b_X, so osc d ≤ osc d_D + 2b_X ≤ D_*.

Corollaries:
- E_{π₀}[(π/π₀)²] = E e^{2d}/(E e^d)² ≤ e^{osc d}.
- On a successful grid, each stage average lies in [e^{Δ_t d_min}, e^{Δ_t d_max}], and Σ Δ_t = 1 because the coded grid ends exactly at 1 (`v3_calib.h` snap rule). Hence W ∈ [e^{−osc d}, e^{osc d}] on every path.
- By T12/N9 unbiasedness (E W = 1), E W² ≤ e^{osc d} E W = e^{osc d}.

No step uses the grid's quality, the kernel's mixing or the pooling rule. The numerics suggest the bound is loose by about 2× (max observed osc/D_* = 0.499), likely from the factor 2 on b_X and the step-2 bound.