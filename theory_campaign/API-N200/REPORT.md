# API-N200 — REPORT: a quantitative finite-n theorem that speaks to the study's n = 200

Run API-N200 (Fable 5.1), branch `theory/API-N200`, 2026-11-02. Everything here is a **candidate**: not reviewed, not adopted. Status words follow `theory_campaign/PROTOCOL.md` and are never upgraded. Proofs: `PROOF.md`. Scripts: `scripts/` (run through `owls_run`). Tables: `results/`.

## 1. Headline

1. **Theorem N200 (PROVED, elementary, every n).** For the method as run, with Ŝ the ≻-maximum of the scored set and S† the ≻-maximum of Ω (T21's total order):
   P(U ∪ {Ŝ ≠ S₀}) = P(U) + P(𝒪, Ŝ ≻ S₀) + P(𝒪, S₀ ≻ Ŝ) ≤ P(U) + **Π(X)** + P(𝒪, S₀ ∉ 𝒮), and
   P(U ∪ {Ŝ ≠ S₀}) ≥ P(U) + P(𝒪, S† ≠ S₀) − P(𝒪, S† ∉ 𝒮),
   where **Π(X) := P₀(S† ≠ S₀ | X)** is the posterior-miss probability of the design, free of the algorithm. It implies T21's (C1) term by term (Π(X) ≤ P(π(S₀) ≤ ½) ≤ 2E₀δ₁) and is the first version whose middle term is **not vacuous at n = 200**: 2E₀δ₁ > 1 there (O-CERT: π(S₀) ≤ 0.37 even on correct fits), while Π(X) is 5–75% per cell.
2. **Where rigor stops in Π(X).** PROVED: max_e p_e ≤ P₀(L | X) ≤ P₀(L₂ | X) ≤ Π(X) and P₀(L | X) ≤ Σ_e p_e (one-move event L; Hamming-2 event L₂). P₀(L | X) is computed by exact-score Monte Carlo on the study's own designs (rigorous up to MC error); the closed-form p_e are **PA-exact** (O-SWAP Props 1–3), not rigorous. **An upper bound on Π(X) at finite n is OPEN**: the remainder Π − P₀(L) is measured (≤ 1.1 points per cell by exact-score MC with double drops; ±1 fit per cell by the realised hill-climb; 0.2–1 point at c = 1 in exact p = 12 enumeration) but not bounded. A union bound over Hamming balls provably cannot close it (PROOF.md §3).
3. **The discovery term at n = 200.** The rigorous a-priori bounds (T21 routes) are **vacuous**: Q_f π₀(S₀) ≲ 10⁻⁶ because of σ²-dilution (O-DILUTE). The term is **measured**: S₀ scored in 2,394 of 2,394 completed fits, 0 search misses (S-ELS); exact 95% upper bound 0.125% per fit. It is also **certifiable per fit without S₀** (O-CERT C5, box certificate), a bookkeeping item not yet run over the 2,400 fits.
4. **The n = 200 table (24 cells).** Predicted wrong = observed P(U) + Σ_designs P̂₀(L | X_i) against observed wrong = U + posterior misses: 81.8 vs 81 at c = 1 and 476 vs 490 at c = 0.5; 558 vs 571 over 2,400 fits; RMS z = 1.08 over the 24 cells, max |z| = 2.5 (p = 1000, S5, c = 0.5). The prediction is a **lower bound plus a measured term**, so observed ≥ predicted on average is what the theorem says; the +13 fits of excess over 2,400 is consistent with the measured multi-move remainder (+3.6 from double drops alone) and noise.
5. **What this does and does not give the paper.** It gives an exact finite-n inequality whose three terms are, at n = 200, respectively measured (P(U) = 6/2,400), computed with a rigorous lower bracket (Π(X)), and measured per fit with a rigorous-but-vacuous a-priori bound (discovery). It does **not** give a proved upper bound on the miss rate at n = 200: that needs either a finite-n upper bound on Π(X) (OPEN; the T03 restatement in finite form) or a finite-n discovery bound for the Gibbs route (OPEN, T38(b)).

## 2. Statements

**Setting.** Fixed n, p, standardised X, S₀, θ*, σ*²; G (Gaussian noise); EX-A (exact scores). ≻ = T21's total order (larger F, then smaller size, then lexicographic); S† = max_≻ Ω; on the output event 𝒪, 𝒮 ⊆ Ω is the scored set and Ŝ = max_≻ 𝒮; U = 𝒪ᶜ. Π(X) = P₀(S† ≠ S₀ | X). L = {some one-move neighbour of S₀ beats S₀}, L_d = {some S′ with 1 ≤ |S′ Δ S₀| ≤ d beats S₀}, p_e = P₀(F(S_e) > F(S₀) | X).

**Lemma 1 (deterministic).** On 𝒪: {Ŝ ≻ S₀} ⊆ {S† ≠ S₀}; {S₀ ≻ Ŝ} ⊆ {S₀ ∉ 𝒮}; {S† ∈ 𝒮} ⊆ {Ŝ = S†}; {S† ≠ S₀} ⊆ {π(S₀) ≤ ½}. PROVED.

**Theorem N200.** (i) P(U ∪ {Ŝ ≠ S₀}) = P(U) + P(𝒪, Ŝ ≻ S₀) + P(𝒪, S₀ ≻ Ŝ). (ii) ≤ P(U) + P(𝒪, S† ≠ S₀) + P(𝒪, S₀ ∉ 𝒮) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮). (iii) ≥ P(U) + P(𝒪, S† ≠ S₀) − P(𝒪, S† ∉ 𝒮). (iv) P(𝒪, S† ≠ S₀) ≤ P(π(S₀) ≤ ½) ≤ 2E₀δ₁. Hypotheses: EX-A and the definition of Ŝ; nothing about the sampler. PROVED.

**Proposition 2 (brackets for Π).** max_e p_e ≤ P₀(L | X) ≤ P₀(L₂ | X) ≤ Π(X); P₀(L | X) ≤ Σ_e p_e. PROVED (exact score). The p_e closed forms are O-SWAP's Props 1–3 under PA (PA-exact).

**Discovery (plug-ins, all from locked or candidate results).** P(𝒪, S₀ ∉ 𝒮) ≤ T21 routes (a)–(f) [a priori]; ≤ P(𝒪, box certificate fails for U) + P(𝒪, S₀ ⊄ U) [O-CERT C5, per fit, without S₀]; = 0/2,394 observed [S-ELS].

**Paper wording (candidate), §6 of PROOF.md.** "For every n, p, design and truth, P(no output or Ŝ ≠ S₀) ≤ P(no output) + P₀(S† ≠ S₀ | X) + P(output, S₀ never scored), with a matching lower bound up to P(output, S† never scored). The middle term is the posterior-miss probability of the design; the last is a scoring event, measurable per fit."

## 3. Proofs or sketches

All in `PROOF.md`: Lemma 1 and Theorem N200 (§1–2, complete, one page); Proposition 2 (§3); the failed union-bound route and the convexity "shell" PROOF SKETCH for a finite-n upper bound on the superset part of Π (§3); the vacuity of 2E₀δ₁ at n = 200 (§4); the discovery terms (§5).

## 4. Evidence

### 4.1 The n = 200 table (`results/n200_table.md`, `scripts/assemble_n200.py`)

Inputs: the production counts (`Results/SMC_BVS_v3_production/p*/exact_recovery_long.csv`, SMCBVS hpm primary rows), S-ELS's classification (0 search misses, S₀ scored in every completed fit), and O-SWAP's per-design quantities on the study's own regenerated designs (`data/oswap/*.csv`: exact-score MC of L and of "L or double drop", R = 40 draws per design; realised events on the study y; PA closed forms max_e p_e and Σ_e p_e; T2; Le Cam floor).

Pooled per (p, c), counts per 600 fits (per-cell rows in the results file):

| p | c | obs U | obs posterior misses | **obs wrong** | Σ P̂₀(L\|X) (MC, exact score) | Σ P̂₀(L or dd) | realised one-move on study y | **pred wrong = U + Σ P̂₀(L)** | T2 (approx.) |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 1 | 1 | 40 | **41** | 40.5 | 40.5 | 39 | **41.5** | 43.1 |
| 1000 | 1 | 3 | 37 | **40** | 37.3 | 37.3 | 37 | **40.3** | 39.9 |
| 500 | 0.5 | 0 | 230 | **230** | 228.3 | 230.0 | 226 | **228.3** | 250.6 |
| 1000 | 0.5 | 2 | 258 | **260** | 246.0 | 247.9 | 257 | **248.0** | 270.0 |
| all | | 6 | 565 | **571** | 552.1 | 555.7 | 559 | **558.1** | 603.6 |

Per-cell: RMS z (observed posterior misses vs n_out·mean P̂₀(L|X), SD = design binomial + MC) = 1.08; |z| ≤ 1.5 in 20 of 24 cells; the four larger ones are p500 S4 c0.5 (+2.0), p1000 S5 c0.5 (+2.5), p1000 S5 c1 (+1.8), p500 S2 c0.5 (−1.5). The direction of the largest ones is positive, as the theorem predicts for a lower bound (Π ≥ P₀(L)) plus noise.

Brackets at n = 200 (PA closed forms, per cell): at c = 1 the union bound Σ_e p_e is 6.7–9.6% against MC P₀(L|X) = 5.5–8.4%, so Π(X)'s one-move part is bracketed to within ≈ 1–2 points from above (modulo PA; in one cell, p = 500 S1, the MC estimate 7.4% exceeds the PA union bound 7.2% by 0.2 points, inside the MC standard error of 0.4 points, which is exactly where PA-exactness and MC error meet); the lower bracket max over drops/swaps is ≈ 0 at c = 1 (the adds are the whole story there, each ≈ 1.5·10⁻⁴ per null) and 4.6–24% at c = 0.5. At c = 0.5 the union bound is 1 in S4/S5 (vacuous), and the Le Cam two-point floor (for *any* selector) is 0.4–9.2%.

The discovery term: observed 0 search misses in 2,394 completed fits; exact 95% Clopper–Pearson upper bound 0.125% per fit. The a-priori route-(a) bound is ≥ 1 − 10⁻⁶ (vacuous).

### 4.2 Exact enumeration at p = 12 (`results/small_p_exact.txt`, `scripts/small_p_exact.py`)

n = 40, p = 12 (|Ω| = 4,096, all feasible), s₀ = 3, β = c·(1.4, −1, 1.8), σ = 1, R = 2,000 noise draws per design, one design per kind (iid; equicorrelated 0.3; look-alike blocks r = 0.85), seed fixed. Exact F over all of Ω, so Π(X), P₀(L|X), P₀(L₂|X), the brackets, and the exact π(S₀) are all computed. Findings:

| design | c | Π = P(S† ≠ S₀) | P(L) | P(L₂) | Π − P(L) | Π − P(L₂) | max_e p_e | Σ_e p_e | P(π(S₀) ≤ ½) | 2E₀δ₁ (T21 term) |
|---|---|---|---|---|---|---|---|---|---|---|
| iid | 1 | 0.077 | 0.075 | 0.077 | 0.002 | 0.000 | 0.011 | 0.078 | 0.304 | 0.934 |
| iid | 0.75 | 0.136 | 0.133 | 0.136 | 0.003 | 0.000 | 0.039 | 0.162 | 0.453 | 1.045 |
| iid | 0.5 | 0.509 | 0.490 | 0.505 | 0.019 | 0.004 | 0.381 | 0.875 | 0.823 | 1.459 |
| equi 0.3 | 1 | 0.081 | 0.077 | 0.081 | 0.005 | 0.000 | 0.011 | 0.085 | 0.337 | 0.948 |
| equi 0.3 | 0.75 | 0.196 | 0.184 | 0.196 | 0.012 | 0.001 | 0.104 | 0.248 | 0.547 | 1.130 |
| equi 0.3 | 0.5 | 0.667 | 0.584 | 0.663 | 0.083 | 0.004 | 0.484 | 1 | 0.908 | 1.637 |
| look-alike 0.85 | 1 | 0.217 | 0.206 | 0.208 | 0.011 | 0.009 | 0.077 | 0.269 | 0.627 | 1.203 |
| look-alike 0.85 | 0.75 | 0.429 | 0.398 | 0.401 | 0.032 | 0.029 | 0.139 | 0.582 | 0.872 | 1.480 |
| look-alike 0.85 | 0.5 | 0.789 | 0.762 | 0.768 | 0.028 | 0.021 | 0.381 | 1 | 0.995 | 1.812 |

(c = 0.35 rows are in the results file: Π = 0.89–0.96, P(L) = 0.85–0.95, 2E₀δ₁ = 1.85–1.95.)

So the one-move event carries Π to within 0.2–1 point at c = 1 and within 2–8 points at c = 0.5 in this harder regime (n = 40, s₀/n larger than the study's); the Hamming-2 event carries it to within ≤ 0.4 points except in the look-alike design (2 points, where S† sits 2–7 flips away on a miss). The inclusion L ⊆ {S† ≠ S₀} was asserted on every draw (never violated). The deterministic inclusions of Lemma 1 need no numerical check. **The last two columns are the point of Theorem N200(iv):** at the same (X, c), T21's Markov term 2E₀δ₁ is 0.93–1.95 (vacuous or nearly so) and even the pre-Markov event {π(S₀) ≤ ½} has probability 0.30–1.00, while the exact posterior-miss probability Π = P(S† ≠ S₀) is 0.08–0.79: the truth is the mode far more often than it carries half the mass, and only the former matters for the reported HPM.

### 4.3 Inputs taken from other runs (not re-derived here)

O-SWAP (exact-score MC and PA closed forms on the study's regenerated designs; the realised check matching the observed counts ±1 per cell), S-ELS (ledger classification of the 2,400 fits), O-CERT (π(Ŝ) ≤ 0.37 on correct fits; box certificate), O-DILUTE (π₀(S₀) medians 10^{−11}–10^{−26}; Q_fπ₀(S₀) ≲ 10⁻⁶), T21 STATEMENT (total order, routes). All are candidates; O-VCERT verified O-CERT's arithmetic. I did not regenerate the study data or rerun the engine.

## 5. What fails and why

- **A rigorous finite-n upper bound on Π(X).** Union bounds over Hamming balls fail: the distance-2 superset union bound alone is ≈ 0.07 at p = 500, c = 1, as large as the entire one-add rate, because the two-add events are almost entirely inside the one-add events. The convexity "shell" argument bounds the two-add-only remainder by ≈ 6·10⁻⁴ for orthogonal nulls (PROOF SKETCH) but does not cover correlated nulls, drops or swaps at distance 2, or distance ≥ 3. This is the finite-n face of T03 and is the research item.
- **Using T21's 2E₀δ₁ at n = 200.** It is > 1. The reason is structural (supersets with κ⁺ ≈ 7 nats against 486–986 nulls make π(S₀) < ½ even when S₀ is the mode), not a looseness of Markov.
- **A priori discovery bounds at n = 200.** Route (a) is vacuous by six orders of magnitude (σ²-dilution). Route (d) does not apply to S₀ as a whole. Routes (b), (c), (e) are open at every n. No restatement of the existing routes changes this; a finite-n bound for the Gibbs-flip route (which empirically delivers S₀ in every fit) would be new theory (T38(b), O-BGIBBS-type).
- **Making the PA closed forms rigorous.** Needs an anti-concentration margin for the score gap at 0 (O-SWAP §7.3); not attempted.
- **A lower-bound discovery term P(𝒪, S† ∉ 𝒮).** Not observable at p = 500; left as "consistent with 0" (realised hill-climb matches the counts).

## 6. Needs escalation

1. **Independent check of Lemma 1 / Theorem N200** (elementary; a Lean formalisation next to `T21HPM.lean` is the natural check: `hpm_eq_truth`/`t21_event_subset` already encode the ≤ ½ version; the ≻-version and the lower bound (iii) are two short lemmas).
2. **A finite-n upper bound on Π(X)** of the form P₀(L | X) + r_n(X) with explicit r_n: the shell argument generalised to correlated nulls and to drops/swaps at distance 2, and a tail over distance ≥ 3. Stronger prover.
3. **Tabulating O-CERT's C5 screening event {S₀ ⊆ U(X, y, Ŝ)} over the 2,400 fits** (bookkeeping on the stored fits; gives the per-fit certified version of the discovery term without using S₀ in the certificate).
4. **Per-dataset matching of O-SWAP's realised check with the SMC outputs** (currently counts per cell match ±1; a dataset-by-dataset match would pin the remainder Π − P₀(L) on the study's own y).

## 7. Outside scope

- The sandwich (iii) suggests a cheap *data* estimate of P(𝒪, S† ∉ 𝒮): run O-CERT's box B&B around Ŝ with U = Ŝ ∪ top-k additions on every fit; a refutation (C4(c)) is a search miss relative to an explicit model. This is a post-hoc diagnostic, not a method change.
- The convexity structure of g(x) = −ν log(1 − (n/(n+1))x/(Q̃ + b̃)) (superadditive) is also why multi-add supersets are rare relative to single adds; it may be the right handle for the T02(i) tail sharpening at finite n.
- Nothing here concerns PIPs, Ẑ, or the masked-regime delivery theorem.

## 8. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| T21 (Thm 4), finite-n form | Theorem N200: identity (i), upper bound (ii) with Π(X) = P₀(S† ≠ S₀ \| X) in place of 2E₀δ₁, lower bound (iii), and (iv) showing it implies C1. PROVED. | high | done (elementary; Lean next) | none; it is order bookkeeping | no |
| T03 (Thm 1) at n = 200, finite form | Π(X) is bracketed below by P₀(L \| X) (exact-score MC) and its PA closed forms; the remainder Π − P₀(L) is measured ≤ ~1 point at the study's n but has no proved bound | high that the brackets hold; medium-high that the remainder is ≤ 1–2 points at n = 200 | low–medium for a rigorous upper bound (shell argument + correlated nulls + distance ≥ 3) | union bounds are off by the whole one-add rate; need conditional ("beats while no single move does") events | no |
| Discovery term (T21 routes / T38(b)) at n = 200 | A-priori bounds vacuous (Q_fπ₀(S₀) ≲ 10⁻⁶); measured 0/2,394 (95% UB 0.125%); certifiable per fit by O-CERT C5 | high (as measured) | low for an a-priori bound at n = 200 without new theory (Gibbs route) | σ²-dilution of the start; no finite-n Gibbs-path theorem | no (LS0 would not change it: S₀ is scored anyway) |
| The n = 200 table | observed wrong = 571 vs predicted 558 (U + Σ P̂₀(L)); RMS z 1.08 over 24 cells | high (empirical) | n/a | per-dataset matching (escalation 4) | no |

## 9. Draft paragraph for the paper's n = 200 section (candidate)

> **What the theory says at the study's n = 200.** Theorem 4 holds at every n. In the form used here it reads, for each design, P(no output or Ŝ ≠ S₀) ≤ P(no output) + P₀(S† ≠ S₀ | X) + P(output, S₀ never scored), where S† is the global mode of the posterior, and conversely P(output, Ŝ ≠ S₀) ≥ P(output, S† ≠ S₀) − P(output, S† never scored). The three terms are of different natures. The first is operational: 6 of 2,400 fits stopped at the resource limit. The third is a scoring event: in all 2,394 completed fits S₀ was scored and no reported model was beaten by S₀ (0 search misses; exact 95% upper bound 0.13% per fit); the a-priori bounds of Theorem 4's routes are vacuous at this n because the start mass π₀(S₀) is 10⁻¹¹–10⁻²⁶ (σ²-dilution, Proposition DM), so this term is measured, not proved. The second is the posterior-miss probability of the design: it does not involve the sampler, it is what Theorem 1 drives to zero as n → ∞, and at n = 200 it is bounded below by the probability that a one-move neighbour of S₀ beats S₀, a Gaussian/χ² computation in the residual projections of X (Propositions 1–3 of the supplement). Summed over the study's own 1,200 designs this lower bound predicts 552 posterior misses in 2,394 completed fits against 565 observed (RMS z = 1.08 over the 24 cells), and it predicts the type: supersets at c = 1, same-size swaps and dropped truths at c = 0.5. We do not have a proved upper bound on the posterior-miss probability at finite n; the multi-move remainder is measured to be at most about one point per cell. In short, at n = 200 every observed error is a posterior miss, and the posterior-miss rate is the quantity the finite-n inequality isolates and the one-move theory computes; the asymptotic theorems describe where that quantity goes, not its value at n = 200.

## 10. Files

- `PROOF.md`: statements and proofs.
- `scripts/assemble_n200.py` → `results/n200_table.md`, `results/n200_table.csv` (the 24-cell table).
- `scripts/small_p_exact.py` → `results/small_p_exact.txt` (exact enumeration at p = 12; `results/small_p_exact_v1.txt` is the first run without the δ₁ columns).
- `scripts/run_with_retry.sh`: owls_run wrapper that waits for a slot.
- `data/oswap/`: committed copies of O-SWAP's per-design outputs (`theory/O-SWAP:theory_campaign/O-SWAP/out/`).
- Cost: well under the $25 cap; all compute through `owls_run` (-j 1).
