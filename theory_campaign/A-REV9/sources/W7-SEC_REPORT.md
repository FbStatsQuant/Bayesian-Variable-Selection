# W7-SEC — REPORT: the cheap secondary lemmas (T05, T33, T32(i))

Cloud run W7-SEC, branch `theory/W7-SEC`, 2026-11-02. **Nothing here is reviewed or adopted.** Every PROVED is a
candidate I checked line by line (same-family check only). Files: `PROOF_T05.md`, `PROOF_T33.md`, `NOTES.md`,
`scripts/` (all seeded), `results/`.

## 1. Headline

1. **T05: PROVED in full, with explicit finite-n bounds for the half the remark needs.** Under ORTH an exact
   representation makes every score a function of n independent N(±√λ_j, 1) statistics and one χ² (Lemma T05-R).
   Results:
   - a finite-n failure bound for the global HPM (Thm T05-U) and its reported-HPM version (Cor T05-Ŝ);
   - the threshold limit P(S† = S₀) → Φ(c)^{s₀} (T05(ii));
   - an explicit bound for the known-size selector (Prop T05-O), and the gap (T05(iii)).

   **Wording correction:** the gap is an additive [√(1+2a) − √(2a)]√log n on the *amplitude* scale (√λ). On the
   b_n or energy scale it is a constant factor (1+2a)/(2a), not a multiplicative √log n.
2. **T33: PROVED (candidate) as a deterministic floating-point bound for the production scorer** (Thm T33-S), in terms
   of λ_min(H_S), κ(H_S), κ(A_S) and y′y/Q_S. It rests on two new exact facts:
   - Q_S ≥ y′y/(n+1) (Lemma T33-Q), so the cancellation in Q costs at most a factor n + 1;
   - I ≼ H_S, A_S (Lemma T33-M).

   Consequences:
   - **numerical_failure is impossible at n = 200 for every p and y** (Cor T33-NF; a priori up to n ≈ 1,286 when
     K = n/2);
   - HPM decisions and ties on a common scored set are stable within 2η (Prop T33-H);
   - on path agreement, |log Ẑ^fp − log Ẑ^ex| ≤ η_Z ≈ 10⁻¹⁰–10⁻⁶ (Prop T33-Z, combined with W2-BOOK's VAL-FP).
3. **T33: the a-priori VAL-FP ε is vacuous at the study's budgets.** The union bound over 10⁸–10¹¹ final-run decisions
   is ≥ 10⁻³ even with measured per-score errors and ≫ 1 with rigorous ones. ε must be measured by replay, as W2-BOOK
   said. A path-free argument is OPEN.
4. **COUNTEREXAMPLE: the engine's `error_bound()` (`v3_score.h:242`) is not a bound** at large n. Actual error / η_eng
   reaches 1.17 at n = 10⁵ and 6.2 at n = 4·10⁶ when y is highly correlated with the model. It held with about 25×
   room at n ≤ 4,000. The R9 "global_certified" flag on the exact branch inherits this.
5. **T32(i): W5-LOCKBOOK's PROVED is confirmed.** I re-read the code independently, and an independent recount
   reproduces all of W5's numbers to the last digit. One harmless slip in W5's corollary proof. One floating-point
   addendum (the pilot can take T_e + 1 stages without EX-A), which changes the bound by about 10⁻⁵ relative.

## 2. Statements

### T05 (hypotheses: G; ORTH-design XᵀX = (n−1)I_p, p ≤ n − 1; 1 ≤ s₀ < p, s₀ ≤ K; λ_j := (n−1)θ*_j²/σ*²;
τ_n := log n + 2 log((2p−s₀)/s₀); d := n − 1 − s₀; M := p − s₀; ν′ := (n−1)(n+0.02)/n). Full text: `PROOF_T05.md`.

- **Lemma T05-R (exact representation). PROVED.** With T_j := √(n−1)θ*_j/σ* + ξ_j (ξ iid N(0,1)) and R′ ~ χ²_{n−1−p}
  independent:
  - Q_S = (n−1)V_S/V_tot, where V_S := R′ + Σ_{j∉S}T_j² + n⁻¹Σ_{j∈S}T_j²;
  - D_S = n^{|S|};
  - F(S) = κ + log ϖ(|S|) − (|S|/2) log n − ν log(c_n + V_S).

  The s_y standardisation cancels exactly. Hence S† is the top-k set by T_j² at the best k (Cor T05-R1). This proves
  T05(i).
- **Thm T05-U (finite-n failure). PROVED.** For every δ ∈ (0,1), with t_δ := √((1−δ)dτ_n/ν′):
  P₀(S† = S₀) ≤ e^{−dδ²/4} + ∏_{j∈S₀}[Φ(√λ_j − t_δ) + Φ̄(√λ_j + t_δ)].
- **Cor T05-U∞. PROVED.**
  - If √τ_n − √λ_{j₀} → ∞ for some j₀ ∈ S₀, then P₀(S† = S₀) → 0.
  - With equal magnitudes and √λ_n − √τ_n → c ∈ [−∞, ∞), limsup P₀(S† = S₀) ≤ Φ(c)^{s₀}.
- **Cor T05-Ŝ (reported HPM, SMC branch). PROVED, given the code reading of `local_search`.**
  P(Ŝ = S₀ reported) ≤ bound(U) + P(the final local search ends with local_limit). On the exact branch, Ŝ = S†.
- **Thm T05-L. PROVED (limit).** Assume equal magnitudes, b_n²/σ*² bounded and √λ_n − √τ_n → c ∈ (−∞, ∞]. Then
  liminf P₀(S† = S₀) ≥ Φ(c)^{s₀}. Together with U∞ this proves **T05(ii)** for every c ∈ [−∞, ∞]. The explicit n₀
  implied by my constants is log n ≈ 227, which is useless; numerically the limit is accurate at n = 10³.
- **Prop T05-O. PROVED.** For every x > 0, P₀(Ŝ_or ≠ S₀) ≤ e^{−x} + Σ_{j∈S₀}Φ(√(2 log M + 2x) − √λ_j).
- **Thm T05-G (= T05(iii)). PROVED.** Equal magnitudes, √λ_n − √(2 log M_n) → ∞ and √τ_n − √λ_n → ∞ give
  P(Ŝ_or = S₀) → 1 and P(S† = S₀) → 0. Such sequences exist whenever n → ∞, since τ_n − 2 log M_n ≥ log n − 2 log s₀.
  At p = n^a the amplitude gap is [√(1+2a) − √(2a)]√log n + o(1).
- **Paper sentence (proposed).** "Under an orthogonal design with p = n^a, the HPM of the g-prior/BB(1,p) posterior
  recovers S₀ with probability → Φ(c)^{s₀} when the standardised signal √λ = √τ_n + c, τ_n ≈ (1+2a) log n. The
  known-size oracle needs only λ ≳ 2a log n. The posterior therefore loses an additive [√(1+2a) − √(2a)]√log n in
  standardised amplitude, i.e. a factor (1+2a)/(2a) in signal energy. For example, at n = 10⁹, p = √n, λ = 0.7τ_n the
  oracle succeeds in 74% of replicates and the HPM in 2%."

### T33 (hypotheses FP, NOUF, LIB(c_L), SMALL; stored doubles are the data; cited lemmas H1–H4 from Higham 2002).
Full text: `PROOF_T33.md`.

- **Lemma T33-M (= T33(i), generalised). PROVED.** I ≼ H_S ≼ (1 + (n+1)tr G_S)I and I ≼ A_S ≼ (1 + tr G_S)I, also with
  duplicate columns.
- **Lemma T33-Q (new). PROVED.** Q_S ≥ y′y − (n/(n+1))‖P_Sy‖² ≥ y′y/(n+1).
- **Thm T33-S. PROVED.** Assume ε_H, ε_A, ε_Q ≤ ½ and θ_Q ≤ ½ (explicit in k, n, g_S, λ_H, y′y/Q_S). Then:
  - the Cholesky route succeeds;
  - |l̂dH − log det H_S| ≤ η_H;
  - |Q̂_S − Q_S| ≤ y′y·r_Q;
  - |log m̂(S) − log m(S)| ≤ η_m(S) and |F̂(S) − F(S)| ≤ η_F(S), with every constant explicit.

  First order:
  |Δlog m| ≲ ½k²(n+k)u(κ_H + κ_A) + ν(y′y/Q_S)[k(n+3k)uκ_H + nu(1 + 2√(nkg_S/λ_H))] + u(2|log C_n| + 2 log D_S + νL_S) + η_C.
- **Cor T33-NF. PROVED.** At sizes where the a-priori hypotheses hold, every score returns on route chol and the Q
  fallback is never used, so **numerical_failure cannot occur**. This covers n = 200 for any p, and n ≤ 1,286 with
  K = n/2.
- **Prop T33-H. PROVED.** Let η̄′ := max_𝒮(η_F − η_C); the common log Ĉ_n error cancels. Then:
  - the computed HPM over a common scored set lies in {S : F(S) ≥ F(S*) − 2η̄′}, and equals S* if the gap exceeds 2η̄′;
  - exact ties are decided by rounding unless the computed scores are bitwise equal;
  - with T03's margin, η = o(log n) holds with a lot of room.
- **Prop T33-Z. PROVED.** The exact comparator is the exact final run on the fp-computed 𝓒 (T12 applies because 𝓒 is
  streams-0–9 measurable, so calibration agreement is not needed).
  - (Z1) On the path-agreement event G_fp, |log Ẑ_r^fp − log Ẑ_r^ex| ≤ η_Z (explicit).
  - (Z2) P(G_fp^c | 𝓒) ≤ an explicit union bound (vacuous at the study's budgets).
  - (Z3) VAL-FP(η_Z, ε), hence P(𝒪_E ∩ {αẐ^fp > Z}) ≤ αe^{η_Z}P(𝒜) + ε.
- **COUNTEREXAMPLE (engine heuristic).** η_eng of `v3_score.h:241–246` is exceeded 6.2× at n = 4·10⁶
  (`results/t33_engine_bound_stress.txt`).

### T32(i)
- **W5-LOCKBOOK Theorem T32(i) (T32-a) and Corollaries T32(i-lit), T32(c): PROVED (by W5); independently re-checked
  here, no error in the count.**
- **Addendum (fp pilot). PROVED.** Without EX-A the pilot has ≤ T_e + 1 stages, and ≤ T_e unless its last step is a
  non-forced bisection value within 2T_e u of 1 (or T_e > 4,503). The fp-safe bound adds Σ_e H_e·m. At n = 200,
  p = 500 that is +1,320,960 on 2.676·10¹¹. Corollary T32(i-lit) survives (grid minimum of the difference 1.09·10⁹ > 0).

## 3. Proofs

- **T05:** `PROOF_T05.md` §§1–4. The crux is the exact representation (Lemma T05-R): Q_S = (n−1)V_S/V_tot removes the
  random s_y. The failure half is then three lines: F(S₀) − F(S₀∖j) ≤ ½[ν′T_j²/Ξ − τ], with Ξ ~ χ²_d independent of
  the signal statistics. The success half needs uniform control of supersets: order statistics of null χ²₁, plus a
  bottom-sum (trimmed-sum) bound via Hoeffding on min(ζ, median).
- **T33:** `PROOF_T33.md` §§1–4. Steps:
  1. Gram and z rounding;
  2. forming H̃;
  3. Cholesky success via Demmel's criterion;
  4. backward error ‖E_H‖ ≤ ε_H;
  5. log-det perturbation ≤ kρ/(1−ρ);
  6. the quadratic form, via the forward-solve backward error and Lemma T33-Q;
  7. the log Q term;
  8. assembly rounding.
- **T32(i):** W5's `PROOF.md` §T32 steps 1–8, each re-read against the code (`NOTES.md` §1).
  - Step 2(a) addendum: §3.3 below.
  - Slip in W5's Corollary T32(i-lit) proof: "(1 + 4ℓ)H₀m(T₀+L+4) ≥ 5ℓ·512·p·1000" uses 1 + 4ℓ ≥ 5ℓ, false for ℓ ≥ 2.
    With 4ℓ the lower bound is 2.05·10⁶ℓp ≥ 245ℓp, so the conclusion stands.

### 3.3 The fp pilot addendum (proof)
`pilot_next_phi` (`v3_calib.h:30–46`): a non-forced step has fl(lo − φ) ≥ fl(1/T_e), hence lo − φ ≥ 1/T_e − 2u/T_e. A
forced step gives fl(φ + fl(1/T_e)) ≥ φ + 1/T_e − 2u, then a snap to 1 above 1 − 10⁻¹². So, until it reaches 1,
φ_k ≥ k(1/T_e − 2u).
- After T_e steps, φ ≥ 1 − 2T_e u > 1 − 1/T_e, because 2T_e²u < 1.
- From any φ > 1 − 1/T_e the next step ends at exactly 1: either the ESS test at 1 passes, or the bisection gap is
  < 1/T_e, so the step is forced to min(1, ·) = 1 (or snapped).
- Hence T_pilot ≤ T_e + 1. If T_e ≤ 4,503, a forced last step is snapped, so T_e + 1 needs a non-forced step landing in
  [1 − 2T_e u, 1).
- Diagnostic and final grids keep T ≤ T_e in fp: the integer check at `v3_calib.h:94`. ∎

## 4. Evidence

### 4.1 T05
- `results/t05_representation_check.txt` (brute-force enumeration with real standardised data; n ∈ {13, 25, 40, 60},
  p ≤ 12, including p = n − 1):
  - |log D_S − k log n| ≤ 2·10⁻¹⁴;
  - relative |Q_S − (n−1)V_S/V_tot| ≤ 5·10⁻¹⁵;
  - the HPM equals the top-k set at the best k in 70/70 data sets;
  - the inequality F(S₀) − F(S₀∖j) ≤ ½[ν′T_j²/Ξ − τ] held in every instance.
- `results/t05_mc.txt` (MC via Lemma T05-R, 4,000 replicates per row, s.e. ≤ 0.008), p = ⌈√n⌉, s₀ = 2:

  | n | c = −1: P(S†=S₀) / Φ(c)² / U | c = 0 | c = 1 | oracle at c = 0 |
  |---|---|---|---|---|
  | 10³ | 0.029 / 0.025 / 0.061 | 0.238 / 0.250 / 0.375 | 0.704 / 0.708 / 0.815 | 0.81 |
  | 10⁵ | 0.028 / 0.025 / 0.029 | 0.242 / 0.250 / 0.267 | 0.716 / 0.708 / 0.725 | 0.88 |
  | 10⁷ | 0.023 / 0.025 / 0.026 | 0.253 / 0.250 / 0.252 | 0.706 / 0.708 / 0.710 | 0.94 |
  | 10⁹ | 0.025 / 0.025 / 0.025 | 0.253 / 0.250 / 0.250 | 0.697 / 0.708 / 0.708 | 0.96 |

  The n = 10⁷, c = 0 row was rechecked with 10⁵ replicates: 0.2473 ± 0.0014 ≤ U = 0.2523
  (`results/t05_mc_check_U.txt`).
- Gap, a = ½, λ = 0.7τ_n: the oracle succeeds 0.61 → 0.74 and the HPM 0.080 → 0.020 as n goes 10³ → 10⁹. The
  amplitude gap is only 0.61 → 1.05 there: the √log n growth is real but slow.
- `results/t05_constants.txt`: β₀ = 0.0513; the crude n₀ of Part L is log n ≈ 227.

### 4.2 T33
- `results/t33_fp_check.txt`: the production scorer (compiled from the unmodified `v3_score.h` with the production
  flags) against a 60-digit reference with an exact integer Gram, on the stored doubles. Designs: iid (n = 200),
  near-collinear pairs (ρ ≈ 1 − 10⁻¹⁴), exact duplicates, y almost in the span (y′y/Q = 100 = n), and n = 4,000.

  | design | max \|Δlog m\| | max \|Δlog m\| / η_m (rigorous) | / η_eng (heuristic) | route / Q-recompute |
  |---|---|---|---|---|
  | D1 iid n=200 | 1.3·10⁻¹³ | 7.6·10⁻³ | 5.9·10⁻³ | chol only / 0 |
  | D2 near-collinear | 1.0·10⁻¹¹ | 7.3·10⁻³ | 6.3·10⁻³ | chol only / 0 |
  | D3 duplicates | 4.9·10⁻¹³ | 9.3·10⁻⁶ | 1.3·10⁻⁵ | chol only / 0 |
  | D4 y′y/Q = n | 7.3·10⁻¹³ | 8.4·10⁻³ | 3.9·10⁻³ | chol only / 0 |
  | D5 n = 4000 | 1.3·10⁻¹⁰ | 2.6·10⁻³ | 4.2·10⁻² | chol only / 0 |

  The constants have errors |log Ĉ_n − log C_n| ≤ 1.8·10⁻¹² and |log ϖ̂ − log ϖ| ≤ 1.1·10⁻¹³. Lemma T33-Q held in
  every case (min (n+1)Q/y′y = 1.0099).
- `results/t33_engine_bound_stress.txt`: n ∈ {10⁴, 10⁵, 10⁶, 4·10⁶}, y = x₁ + noise. The ratio to η_eng reaches
  1.17 (n = 10⁵), 3.5 (n = 10⁶) and 6.2 (n = 4·10⁶). The rigorous bound holds wherever its hypotheses hold
  (n ≤ 10⁵ here); beyond that it is ∞.
- `results/t33_valfp_budget.txt`:
  - worst-case a-priori quantities at n = 200, K = 100: ε_H = 1.4·10⁻⁷, (n+1)r_Q = 4.6·10⁻⁵, universal
    η_Q = 4.6·10⁻³;
  - largest n for Cor T33-NF: 1,286 (K = n/2), 4,575 (K = 10), 8,149 (K = 1);
  - η_Z and the ε union bound at the study's budgets: §1 item 3.

### 4.3 T32(i)
- `results/t32_recount.txt`: my code, written from my own code reading, gives (T32-a) = 267,610,872,968 at
  (200, 500), tier 0 only 16,189,996,622, and conjectured 535,236,539,242. It also gives 562,428,743,935 at
  (200, 1000) and 563,899,741,650 at (800, 1000). All match W5's `t32_count.txt` exactly.

## 5. What fails and why

- **Explicit n₀ for T05's success half.** My constants give log n ≳ 227. The loss is in the superset regime
  m = |S∖S₀| ≥ 0.008d, where I bound the residual by a trimmed sum ≥ 0.05d and the added null by a crude quantile. A
  DKW-type uniform control of null order statistics should bring n₀ to O(10²); the MC suggests that is the truth. Not
  pursued, because the remark only needs the failure half and the oracle, which have clean finite-n bounds.
- **"Loses a √log n factor"** is false as a multiplicative statement at p = n^a, a > 0. It is true additively in
  amplitude, and multiplicatively only when log p = o(log n).
- **A data-free fp bound is weak.** The worst case (κ_H = kn² and y′y/Q = n + 1 at once) allows 4.6·10⁻³ nats at
  n = 200, K = 100, and is vacuous at n = 1000, K = 500. The a-posteriori form, which uses the model's λ_min(H_S) and
  Q_S, is ~10²× above the observed errors. That is the usual price of worst-case (n·u) dot-product bounds.
- **A-priori VAL-FP.** The union bound over path decisions cannot certify path agreement at 10⁸–10¹¹ decisions. The
  path-free route (perturbed Feynman–Kac) stalls: the MH self-loop probability 1 − α is not multiplicatively stable
  under score perturbations when α ≈ 1, and fp kernels are not invariant for any target. OPEN.
- **Preprocessing error** (raw → stored doubles) is not bounded. It does not matter for fp-vs-exact comparisons on the
  same stored data, which is all VAL-FP needs.

## 6. Needs escalation

1. **The cited backward-error results (H1–H3).** In particular, the exact form of Demmel's success criterion
   (Higham 2002, Thm 10.7: λ_min(D⁻¹AD⁻¹) > kγ_{k+1}/(1 − γ_{k+1})). I used it from memory. A reader with the book
   should confirm the statement and its constant; if the constant differs, only the factor in Cor T33-NF moves.
2. **LIB.** The accuracy of `log` and `lgamma` in the deployment libm (glibc on NOTS). The measured constant errors
   (≤ 1.8·10⁻¹²) are for this container's glibc.
3. **The engine heuristic COUNTEREXAMPLE.** It needs a decision on the implementation (Felipe/OPS). Options:
   - add a √n- or n-scaled dot-product term to `error_bound`;
   - or accumulate `data_init`'s dot products in long double or with compensated summation;
   - and use η_F − η_C (Thm T33-S) for R9 certificates.

   This does not affect the n = 200 study (about 25× room), but it does affect exact-branch certificates at large n.
4. **Cor T05-Ŝ** rests on my reading of `local_search` (`v3_engine.h:378–418`): a certified final centre is the
   reported HPM, and its flips have been scanned. A second reader should check it.
5. **ε of VAL-FP** must be measured by replay (HQ/OPS). This is unchanged from W2-BOOK, now with the explicit η_Z and
   the reason why theory cannot supply ε.

## 7. Outside scope

- **`error_bound` feeds R9's `global_certified`** (`v3_exact.R`) on the exact branch. With large n and small p (the
  exact branch's typical regime), a certificate can be issued with an η that underestimates the true error by up to
  6×. A wrong certificate needs a near-tie within ~10⁻³ nats, so it is rare but possible.
- **T34 statuses.** Cor T33-NF turns "numerical_failure has unknown probability" into "numerical_failure is impossible
  for n ≲ 1,300 (K = n/2), including n = 200". T34's statement can use this.
- **T05's remark does not describe the study design.** ORTH needs p ≤ n − 1; the study has p ∈ {500, 1000} > n = 200.
  It is a mechanism remark only.
- **The scorer's non-negative Q fallback (`q_nonneg`) is dead code** for n + 1 < 10⁷ under the hypotheses of
  Cor T33-NF (Lemma T33-Q). That is harmless, but the method text could say so.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| T05(i) | Lemma T05-R (exact representation, D_S, Q_S, log-odds) | 0.99 | done | none | no |
| T05(ii) | Thm T05-U (finite n) + Thm T05-L (limit) ⇒ P(S† = S₀) → Φ(c)^{s₀} | 0.97 | done (limit); a useful explicit n₀ needs DKW work, ~1 day | uniform superset control | no |
| T05(iii) + remark | Thm T05-G + Prop T05-O; corrected wording (additive in amplitude, factor (1+2a)/(2a) in energy) | 0.98 | done | none | no |
| T05 for the reported Ŝ | Cor T05-Ŝ: P(Ŝ = S₀) ≤ (U) + P(final local_limit) | 0.93 | done, given the code reading | `local_search` invariant | no |
| T33(i) | Lemma T33-M (+ Lemma T33-Q) | 0.99 | done | none | no |
| T33 fp bound | Thm T33-S (explicit η_m(S), η_F(S)); Cor T33-NF | 0.9 | done modulo the citations H1–H3 and LIB | Demmel's criterion; libm accuracy | no |
| T33(ii) | Prop T33-H (2η̄′ margin, ties need bitwise equality) | 0.98 | done | none | no |
| T33 + VAL-FP | Prop T33-Z: η_Z explicit and tiny; ε a priori vacuous, so measure it | 0.95 (η part); ε: n/a | η: done. ε: OPEN as theory; cheap by replay | path agreement over 10⁸–10¹¹ decisions | no (a replay study, not a method change) |
| Engine `error_bound` | COUNTEREXAMPLE at n ≥ 10⁵ | — | — | dot-product rounding × νy′y/Q | **implementation fix recommended** (not a statistical method change) |
| T32(i) | W5's (T32-a) + corollaries; fp addendum (pilot T_e + 1) | 0.97 | done (verified twice) | code-to-count mapping; recheck on any engine change | no |
