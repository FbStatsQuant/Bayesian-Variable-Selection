# W2-BOOK — REPORT: bookkeeping restatements (P5) for T12 + T31(i), the run/output split, T07, T21

Run of 2026-11-02, branch `theory/W2-BOOK`. **Nothing here has been reviewed.** Every PROVED is a candidate (checked
line by line by me, not adopted). Proofs are in `PROOF.md`, working notes in `NOTES.md`, scripts in `scripts/`,
outputs in `results/`. A LaTeX fragment of the paper statements is in `STATEMENTS.tex`.

## 1. Headline

1. **Run/output split: PROVED (Lemma RO), and needed.** The deployed engine's `resource_limit` is not only a
   preflight. A wall-clock guard runs after every final bridge stage and again after the final local search, so the
   output-available event depends on the final-run path. The 6/2,400 PROD-H stops were this guard, all in S5.
   All locked final-run results hold for the **potential uninterrupted run R̄**. They reach the reported output
   through one checkable implementation hypothesis, GUARD (the stop-only coupling, confirmed by reading the code).
   Never by conditioning: **COUNTEREXAMPLE** (exact, stylised cost). A guard that stops 0.22% of runs makes
   E[Ẑ | output] = 0.974·Z.
2. **Prop 2 (T12 + T31(i)), restated: PROVED** as a corollary of the locked T12/T31(i) plus Lemma RO.
   - Islandwise E[Ẑ_r PIP̂_rj | 𝓒] = Z·PIP_j, and the pooled island product ¼Σ_rẐ_rPIP̂_rj is unbiased.
   - New exact formula: E[Ẑ·P̄_j | 𝓒] − Z·PIP_j = −¾·Cov(PIP̂_1j, Ẑ₁ | 𝓒). In the locked instance this is
     < −0.1275·Z, so pooled × pooled is provably not an identity.
   - Output-level Markov bound: P(a bound is reported and 0.05·Ẑ > Z) ≤ 0.05, with no completion assumption.
   - A floating-point contract VAL-FP(η, ε) gives level 0.05·e^η + ε.
   - The secondary PIP is removed. Exact edits are listed against `COLLECTED_PROOFS_v2.tex`.
3. **The same split for T11(iii), T14(i), T15, T23(ii), T25(iv), T31, T34:** one-line statement changes. No proof
   changes, except a new clause (Lemma RO) for the conjecture T34.
4. **Prop 1 (T07 + T06(i)), paper-ready: PROVED** (the locked parts plus two new short clauses).
   - The ceiling is sharp: some size-only prior recovers S₀ ⇔ S*_{s₀} = S₀.
   - Every strict same-size posterior miss in the study is a certificate that **no** size-only prior recovers S₀ on
     those data.
   - Wording fix: the T06 condition is equal outer products X_SX_Sᵀ, not equal projections.
5. **Thm 4 (T21) with routes (a), (d), (e′): PROVED as an implication.** (e′) uses W1-T24G's Theorem B, which is
   PROVED-candidate and unreviewed, in place of the false H24. A multi-particle form (e-M) is included.
   T37 would enter as a strengthening of route **(d)** (scans), not (e). Its eligibility term is T38's crux.
   Reading of the data: the "local search repaired 0" finding is consistent with T37 and uninformative about it.

## 2. Statements (paper-ready)

Common hypotheses: EX-A, EX-S, CAL (with 𝓒 as below), START (T09(i)) where π₀ draws are used, SR for scoring
routes.

**New code GUARD** (stop-only coupling). On the event 𝒢 := {status = resource_limit} the run stops. On 𝒢^c the
status and every reported output equal those of the potential uninterrupted run R̄, which is the same algorithm with
preflight and time guard removed. No assumption is made on the law of 𝒢 given R̄.

**New code VAL-FP(η, ε).** There is an event G_fp with P(𝒪_E ∖ G_fp) ≤ ε, on which
|log Ẑ^fp − log Ẑ̄| ≤ η, where Ẑ̄ is the exact-arithmetic value on the same streams.

### Lemma RO (run/output split). PROVED.
Under GUARD, let 𝒪 be an output-available event and 𝒪̄ ∈ σ(R̄) its potential counterpart, so that 𝒪 = 𝒢^c ∩ 𝒪̄.
Let g be a reported output and ḡ its R̄-version. Then:
1. 1_𝒪 g = 1_𝒪 ḡ.
2. P(𝒪, g ∈ A) ≤ P(𝒪̄, ḡ ∈ A).
3. P(𝒪^c ∪ {g ∉ A}) ≤ P(𝒢) + P(𝒪̄^c) + P(𝒪̄, ḡ ∉ A).
4. E[1_𝒪 g] ≤ E[1_{𝒪̄} ḡ] for g ≥ 0.

Identities in expectation do **not** transfer to P(· | 𝒪) (COUNTEREXAMPLE, PROOF.md §0.3). The only conditional
statement allowed is P(g ∈ A | 𝒪) ≤ P(𝒪̄, ḡ ∈ A)/P(𝒪).

### Proposition 2 (restated T12 + T31(i)). PROVED (candidate; corollary of locked T12, T31(i) and Lemma RO).
**Frozen object.** 𝓒 = (tier, grid 0 = φ₀ < … < φ_T = 1, T, N_e, L, 4 measured rounds, 4 islands, ℓ, inherited
calibration score leaders, every other setting the final run reads). 𝓒 is a function of the data and streams 0–9,
and escalation is decided before stream 10 is read. The allocation, the clock and the guard are not part of 𝓒.

**Notation.** Ẑ_r and PIP̂_rj are island r's evidence and Rao–Blackwellised PIP in R̄. P̄_j = ¼Σ_r PIP̂_rj is the
reported (primary) PIP. Ẑ = ¼Σ_rẐ_r.

**Claims.** On the success event 𝒜, for every r and j:
- (a) **Islandwise.** E[Ẑ_r | 𝓒] = Z and E[Ẑ_r·PIP̂_rj | 𝓒] = Z·PIP_j.
- (b) **Pooled.** E[Ẑ | 𝓒] = Z and E[¼Σ_rẐ_r PIP̂_rj | 𝓒] = Z·PIP_j.
- (c) **Not claimed, and false in general.** Pooled × pooled:
  E[Ẑ·P̄_j | 𝓒] = Z·PIP_j − ¾·Cov(PIP̂_1j, Ẑ₁ | 𝓒).
  The normalised P̄_j is not unbiased: E[P̄_j | 𝓒] − PIP_j = −Cov(PIP̂_1j, Ẑ₁ | 𝓒)/Z. Both biases are non-zero in an
  explicit component instance: < −0.17 for P̄₁, and < −0.1275·Z for Ẑ·P̄₁.
- (d) **Markov and Jensen.** P(Z ≥ 0.05·Ẑ | 𝓒) ≥ 0.95 (also islandwise), and E[log Ẑ | 𝓒] ≤ log Z.
- (e) **Output level** (under GUARD). P(the bound is reported and 0.05·Ẑ > Z) ≤ 0.05·P(𝒜), and
  E[Ẑ·1{evidence reported}] ≤ Z·P(𝒜). Given completion, only P(0.05·Ẑ > Z | reported) ≤ 0.05·P(𝒜)/P(reported) is
  claimed. No unbiasedness given completion is claimed.
- (f) **Floating point** (under GUARD and VAL-FP(η, ε)). P(the bound is reported and 0.05·Ẑ^fp > Z)
  ≤ 0.05·e^η + ε. The factor e^η is unavoidable (T12(iv.f)). η and ε must be measured by replay; NUM does not supply
  them.

*Paper sentence.* "For the run that would be produced without the resource guard, the island evidences are unbiased
and Ẑ_r·PIP̂_rj is unbiased for Z·PIP_j. The reported PIP is not unbiased. A reported 95% lower bound exceeds Z with
probability at most 5%, whether or not the run completes; we never condition on completion."

### Run/output split for the supplement lemmas (statement changes only; proofs unchanged)
- **T11(iii):** "potential final run R̄" replaces "a launched final run executes all rounds". Output form:
  P(output, S* ∉ final draws | 𝓒) ≤ (1 − π₀(S*))^{Q_f}.
- **T14(i), T15, T25(iv):** read on R̄. Output forms carry 1{output} inside the expectation:
  E[1_𝒪|Ẑ_r/Z − 1|] ≤ …, E[1_𝒪 f_T(A^c)] ≤ …, E[1_𝒪(W_T − 1)²] ≤ B_T.
- **T23(ii):** pathwise on R̄.
  P(no PIP output or MPM̂ ≠ S₀) ≤ P(𝒢) + P(𝒜^c) + 2E[1_𝒜 𝓑_n].
- **T31:** E31-B1–B3 (PROOF.md §1.1).
- **T34** (CONJECTURE; new clause (v) = Lemma RO, PROVED). "Statuses split into potential (exact, completed,
  schedule_limit) and operational (resource_limit). Every output guarantee pays P(resource_limit) additively."

### Proposition 1 (T07 + T06(i)). PROVED (locked T07(i)–(iii) and T06(i)(a); (i′) and (iii′) new, PROVED).
Let π be the target posterior. Let S*_k be the ≺-least maximiser of the marginal likelihood m among models of size k.
1. **Bayes rules.** Under 0–1 loss on supports, the posterior risk of a is 1 − π(a). The HPM S† = argmax π is a
   Bayes rule for exact recovery. Under Hamming loss, the MPM {j : PIP_j > ½} is a Bayes rule, unique iff no
   PIP_j = ½. With the size cap K, keep the min(K, N₊) largest PIPs above ½.
2. **Estimated PIPs.** For any estimate p̂, the plug-in Hamming rule â has excess posterior risk at most
   2Σ_{j ∈ â Δ a_opt}|p̂_j − PIP_j| ≤ 2‖p̂ − PIP‖₁.
3. **Size-prior ceiling (sharp).** For s₀ ≤ K: some positive size-only prior has global HPM S₀ if and only if
   S*_{s₀} = S₀. So a within-size ranking error, that is an S ≠ S₀ with |S| = s₀ and m(S) ≥ m(S₀) (ties by ≺), is
   exactly the error that no re-tuning of the size prior can fix. This covers every truncated BB(a, b), including the
   dropped BB(1,1) arm. Errors between different sizes are fixable for those data by some (data-dependent) size prior
   iff S*_{s₀} = S₀.
4. **Certificate.** If a scored model S′ with |S′| = s₀ has F(S′) > F(S₀), then no positive size-only prior has global
   HPM S₀ on these data.
5. **(T06(i))** Two supports have equal posterior score for every response iff X_SX_Sᵀ = X_{S′}X_{S′}ᵀ. They then have
   equal size, and nothing in the data or in a size-only prior separates them.

*Tie to the data* (preliminary ANALYSIS-H2 working tables, THEORY_PRIORITIES §5).
- Every completed wrong HPM is a posterior miss (F(S₀) ≤ F(HPM)).
- At c = 0.5 these are mostly same-size swaps and subsets.
- By (4), each strict same-size swap is certified: on those data **no** size-only prior recovers S₀. That part of the
  c = 0.5 error is a ceiling of the target (look-alike swaps), not of the prior or the sampler.
- Subset misses are different-size errors, and the ceiling does not cover them.
- *HQ to fill from ANALYSIS-H2:* the count of strict same-size posterior misses out of the posterior misses at
  c = 0.5, by scenario. The data do not say whether the remaining (subset) misses satisfy S*_{s₀} = S₀; the scored set
  certifies only one direction.

### Theorem 4 (restated T21). PROVED (candidate) as an implication; (e′) conditional on W1-T24G Theorem B (unreviewed).
Under EX-A, EX-S, CAL, SR and GUARD, with U ⊇ {resource_limit} the no-output event, Ū its potential-run part, 𝒮̄ the
scored set of R̄ and δ₁ = 1 − π(S₀):

  **(C1)** P(no output or Ŝ ≠ S₀) ≤ P(U) + 2E₀δ₁ + P(Ū^c, S₀ ∉ 𝒮̄),   P(U) ≤ P(resource_limit) + P(Ū).

The discovery term is at most each of the following:
- **(a) iid final draws.** P(𝒜^c, S₀ ∉ 𝒮_cal) + E[1_𝒜 1{S₀ ∉ 𝒮_cal}(1 − π₀(S₀))^{Q_f}], with Q_f = 4N_e(T+L+5).
- **(d) tables and scans.** P(neither S₀ ⊆ some block C_b, nor any local search of R̄ centred at a flip-or-swap
  neighbour of S₀).
- **(e′) Gibbs-path repair.** Take a boundary after the last resampling, followed by H ≤ L + 5 rounds at φ = 1, and a
  past-measurable selected state X_sel on an availability event A_F ⊆ 𝒜. The bound is
  P(𝒜^c, S₀ ∉ 𝒮_cal) + P(𝒜, no eligible particle) + E[1_{A_F} min{1, β_H(X_sel)}],
  where β_H(x) = P(Bin(H, c_*(x)) < v(x)) + H·η(x) (Theorem B; exact data functions).
  **(e-M):** replace min{1, β_H(X_sel)} by ∏_{eligible i} min{1, β_H(X_i)}.

If T37 closes, it enters as **(d⁺)**: P₀(TD*^c) + P(TD*, no local-search centre in 𝓡_d) + 1{ℓ < s₀ + d}. The middle
term is T38's eligibility crux, and LS0 controls it by the start-side event {S̃₀ ∈ 𝓡_d}.

Report P(resource_limit) empirically: 6/2,400 = 0.25%, Wilson 95% [0.11%, 0.54%]. Not homogeneous: S5 is 6/400 =
1.5% [0.69%, 3.2%], and S5 at p = 1000 is 5/200 = 2.5% [1.1%, 5.7%].

## 3. Proofs

All in `PROOF.md`:
- §0: Lemma RO and the COUNTEREXAMPLE.
- §1: Prop 2, with the edit table E12-B1–B8 and E31-B1–B3 against `COLLECTED_PROOFS_v2.tex`.
- §2: split table.
- §3: Prop 1 (i′) and (iii′).
- §4: Thm 4 and the edit table E21-B1–B8 against `T21_T14H_HPM_composition/PROOF_v3.tex`, plus the T37 wiring.

Each new proof is short. The new mathematics is:
- Lemma RO (set inclusions);
- the ¾-covariance formula (expansion plus locked island independence);
- the sharpness of T07(i) (an explicit ε-prior);
- the certificate corollary;
- the (e′) substitution (the locked (e) proof uses H24 only through one conditional inequality, and Theorem B
  supplies it pointwise at the selected state).

## 4. Evidence

- `scripts/frozen_run_exact.py` (exact law propagation, mpmath 50 digits; `results/frozen_run_exact.log`). It is an
  independent re-implementation from the STATEMENT; the T12 helper scripts are not in the repo.
  - It reproduces the locked T12(iv.b) values: D = 8.14676240634, π₀({1,2}) = 0.0279141173179,
    c₀ = 0.0694711126908, c₁ = 0.998708337452, PIP₁ = 0.990618012243, E[P̄₁] − PIP₁ = −0.173974177850.
  - Identities: E Ẑ = Z and E[Ẑ·PIP̂₁] = Z·PIP₁ to 10⁻⁵⁰.
  - Pooled island product unbiased to 10⁻⁴⁹.
  - Pooled × pooled relative bias −0.13172, equal to the ¾ closed form to 10⁻⁴⁹.
  - Guard counterexample, table in PROOF.md §0.3:

    | stopped share | E[Ẑ \| output]/Z |
    |---|---|
    | 0.22% | 0.974 |
    | 0.93% | 0.798 |
    | 3.9% | 0.011 |

- `scripts/wilson.py` (`results/wilson.log`): stop-rate intervals above.
- Code reading (no execution; R is not available), confirming GUARD's basis and H ≤ L + 5:
  - `v3_runtime.h` (guard reads only the steady clock);
  - `v3_engine.h` ~l.335 (check after each bridge stage; burn-in and measured loops have no resampling and no check);
  - `v3_core.cpp` `cpp_final_run` (sequential islands on streams 10–13; final check after the local search).

## 5. What fails and why

- **Treating resource_limit as a σ(𝓒) launch event** (T12(iv.d)) fails. The in-run guard fires during and after the
  final run, so T12(iv.d) does not cover it. Fixed by R̄ and Lemma RO, with no conditioning.
- **"E[Ẑ | completed] = Z"** fails: COUNTEREXAMPLE above. The cause is structural. Unbiasedness is carried by rare
  high-weight paths, and those are the expensive ones. The direction of the bias is design dependent, and typically
  downward when d > 0 on large models.
- **"Pooled Ẑ × primary PIP is unbiased"** fails. The exact bias is −¾·Cov. The correct pooled identity is the island
  product average (which is also Ẑ × the dropped secondary PIP; the paper need not mention that).
- **NUM-only floating-point validity** fails (locked T12(iv.f)). Replaced by VAL-FP, which must be measured; I could
  not measure it here (no R/C++ build).
- **Uniform-over-𝓡_d (e) via H24** fails (W1-T24G CE1). Replaced by the pointwise Theorem B bound at the selected
  state.
- **T37 as route (e)** is a category error: the local search is a scan route, so T37 belongs with (d).
- **Data-dependence in T07 sharpness.** The recovering size prior depends on the data. No claim that one fixed prior
  repairs all different-size misses.

## 6. Needs escalation

1. **GUARD is an implementation fact, not a theorem.** It needs an independent check:
   - a code reviewer confirms that no guard path touches an RNG or a setting (including the inherited-store and cache
     paths);
   - the D61 same-seed reproduction spot-check confirms bitwise-identical outputs on completed fits.
2. **W1-T24G Theorem B and Cor. B-M are unreviewed.** (e′) and (e-M) inherit their status. A cross-family check of
   Theorem B is on the critical path for Thm 4.
3. **VAL-FP** needs a replay study on a sample of PROD-H fits (exact or long-double replay of the final islands):
   report η and the decision-disagreement rate ε. HQ/OPS, not theory.
4. **The 541-fit interpretation** (PROOF.md §4.3) must be confirmed by the ANALYSIS-H2 owners. It holds only if those
   fits refer to the final local search.
5. **Labels:** adopt (e′) = Theorem B and (d⁺) = T37, or rename. FABLE_REVIEW's "(e′ = T37)" conflicts.
6. **Wording in THEORY_PRIORITIES and one-pagers:** T06(i) is "outer products X_SX_Sᵀ agree", not "projections".

## 7. Outside scope

- **The stopped fits are in the hardest cell** (S5, p = 1000: 2.5%). In the c = 0.5 stops, both audit-only supports
  were wrong (BRIEFING). Recovery rates computed "among completed fits" would be selected toward easy fits.
  BRIEFING already counts stops as misses, which is the correct convention. Any "exact among successful" column
  (MASTER notes it as secondary) should carry this caveat.
- **T26 (evidence/PIP consistency)** must also use 1_𝒪 inside, never "given completion". Not pursued.
- **Possible reading of the 541 fits** as posterior-miss fits (above): if confirmed, the empirical case against T37 at
  n = 200 is weaker than THEORY_PRIORITIES §5 suggests, though so is the case for it.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Lemma RO + GUARD | §2 | 0.97 (lemma: 0.99; GUARD as an implementation fact: 0.95) | done (lemma); GUARD needs a code check | that no guard path alters RNG or settings | no |
| Prop 2 (T12 + T31(i)) | §2, (a)–(f) | 0.97 | done (corollary of locked results) | the ¾-covariance step uses locked island independence (iv.c); (e) uses GUARD | no (secondary PIP already removed, D2) |
| Run/output split for T11(iii), T14(i), T15, T23(ii), T25(iv), T31 | statement edits only | 0.97 | done | none beyond GUARD | no |
| T34 restated (v) | Lemma RO | 0.97 | done for (v); the rest of T34 stays CONJECTURE | useful P(𝒢) bounds need allocation sequences (V13) | no |
| Prop 1 (T07 + T06(i)) | §2 | 0.98 | done | none (finite, deterministic) | no |
| Thm 4 (T21) with (a), (d), (e′), (e-M) | §2 | 0.90 for (C1)/(a)/(d) as stated (0.97 given GUARD); 0.85 for (e′)/(e-M), inheriting Theorem B | done as an implication; Theorem B review outstanding | Theorem B's correctness; (R5) conditional independence | no |
| (e′) useful at n = 200 | — | 0.2 single-particle; (e-M) with Cor. P1 at distance one is the non-vacuous case | 0.3 | O(1) superset leakage (W1-T24G) | no |
| T37 → (d⁺) wiring | §2 | 0.95 as an implication | done; T37 itself OPEN | eligibility E_LS (T38); TD* fails on posterior-miss data | LS0 tweak optional |
