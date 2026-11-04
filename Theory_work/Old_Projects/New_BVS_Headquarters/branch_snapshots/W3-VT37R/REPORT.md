# W3-VT37R: adversarial verification of W1-T37R. REPORT

Referee of `origin/theory/W1-T37R` at commit d492f22. I read BRIEF.md, PROOF.md, REPORT.md, scripts/ and results/.
- W1's REPORT.md is an unfinished draft: it contains the headline and nothing else (§§2–8 are missing).
- W1's `results/exp1_p20_pm0.json`, `exp1_p20_pm1.json` and `exp1_p25_pm1.json` are **0-byte files**. Exp 1, the small exact
  experiment, left no output, so nothing W1 says rests on it.

All my code is independent of W1's: `scripts/vt_core.py` uses slogdet and solve where W1 used Cholesky, and it implements the
local search line by line from `v3_engine.h`. I cross-checked it against a dense-inverse formula and against W1's scorer, and
the scores agree to the last bit. Repairs are in `REPAIRS.md`. All statuses are candidates, pending cross-family review.

## 1. Headline

- **Theorem A (A1–A4), Lemma 2, Lemma 3, Prop 1 and the Lemma 0 inclusions: VERIFIED** line by line, and exhaustively on 720
  small designs with 0 violations. The refined T37(i), with TD′_P / TD′_∞ and the lattice version, stands.
- **ERROR, with COUNTEREXAMPLE (CEX-1), in A5(a):** literal TD(d,0) strict does **not** imply TD′_P, because it has no
  positivity clause. As a consequence **the original T37(i) is false even at d = 0**, not merely vacuous for d ≥ 1. Repair R1
  adds POS and is PROVED.
- **ERROR, with COUNTEREXAMPLE (CEX-2), in Lemma 0(b)'s "in particular on every posterior miss".** The remark "0/541 is
  forced by monotonicity" is therefore unproven: at production scale, 233 of the 234 non-repaired sampled centres had
  F(S₀) > F(S_c). Repair R2 is PROVED; the data question stays OPEN.
- **Theorems B and C:** B's inclusions and union bound are VERIFIED, and its headline overstates the gain (R6). C1 and C2 are
  sketches with real errors: a miscomputed containment, and a false noise-variance inequality (COUNTEREXAMPLE). Both are
  repaired at PROOF SKETCH level (R4, R5). **C3 (SE + BM-∞ ⇏ PGD): COUNTEREXAMPLE confirmed**, and strengthened: TD′_∞ holds
  on all of R_{2,1} while TD′_P fails.
- The "TD′_P is the weakest condition among ≤Φ-move statements" prose is false (COUNTEREXAMPLE in 23 of 360 designs, R3).

## 2. Verdict table

| # | Claim (W1) | Verdict | Evidence |
|---|---|---|---|
| 1 | Prop 1: literal TD(d,m) unsatisfiable for d ≥ 1; P₀(TD(d,0)) = 0 | **VERIFIED** | §3.1; EXH: literal TD(2,0) strict held in 0/720 designs |
| 1b | Swap identity (SW) | **VERIFIED** | telescoping |
| 2 | Lemma 0(a) strict monotonicity of the path | **VERIFIED** | engine `best.F > C.F` (v3_engine.h:403) |
| 2b | Lemma 0(b) delivery only on E_LS | **VERIFIED** | §3.2 |
| 2c | Lemma 0(b) "in particular on every posterior miss" | **ERROR** | CEX-2; PROD: 233/234 |
| 2d | Remark (ii): "0/541 repair count is forced by monotonicity" | **GAP** (fixable only with data) | R2: needs F(S₀) − F(S_c) at the final centre per fit |
| 2e | Lemma 0(c): certified at S₀ ⇒ Ŝ = S₀ up to ties, no π(S₀) > ½ needed | **VERIFIED** | final LS is the last scoring event (v3_core.cpp:447); fit-level certification requires hpm == returned (v3_run.R:146) |
| 3 | Lemma 2(a) lattice closure; 2(b) NA_d ∧ TL_d ⇒ (L) and extra deletion | **VERIFIED** | EXH: 193 designs with NA∧TL, 0 violations |
| 4 | Lemma 3 (best truth addition under SE) | **VERIFIED** | §3.3 |
| 5 | Theorem A(A1) characterisation of TD′_∞, length ≤ r_𝓡 | **VERIFIED** | EXH: iff and length checked on 720 × 632 states |
| 6 | Theorem A(A2) progress path, τ = m + e − σ ≥ max(m,e) | **VERIFIED** | EXH: 160 TD′_P designs, every centre |
| 7 | Theorem A(A3) production search, ℓ ≥ a + d; lattice version | **VERIFIED** (but "needs ℓ ≥ a+d" should be "ℓ ≥ a+d suffices"; the exact need is ℓ ≥ τ(S_c)) | EXH: 200,700 lattice-certified centres, all certified at S₀ |
| 8 | Theorem A(A4) necessity, PD | **VERIFIED** | definitions |
| 9 | A5(a) literal TD(d,0) strict ⇒ TD′_P(R_d) | **ERROR** | CEX-1; repaired R1 |
| 10 | A5(b) TD′_P ⇒ TD′_∞, converse fails | **VERIFIED** | EXP3-R: TD′_∞(R_{2,1}) in 198/200 draws at n = 3000, TD′_P in 0/200 |
| 11 | "Weakest" prose: TD′_P necessary and sufficient among ≤Φ-move statements | **ERROR** | PHIR: 23/360 designs |
| 12 | Theorem B (B1), (B2), counting | **VERIFIED** | §3.4 |
| 12b | Headline "2^{Φ(S_c)} states, no 2^{s₀}" | **GAP** (presentation) | R6: only for a data-independent centre; otherwise C(s₀, ≤a)p^d |
| 13 | C1: TL_d w.p. → 1 | **PROOF SKETCH, plausible** | §3.5 |
| 13b | C1: NA_d under LD, containment "c(1 − o(1/log p))" | **GAP, fixable** (miscomputed; the conclusion survives and LD can be weakened) | R4 |
| 13c | C1: exceptional nulls | **GAP** (W1 admits it); fixable under the strengthened LD* | R4 |
| 14 | C2: noise sd ≤ Cσ√(n(\|ΔΔ′\| + \|ΔΔ″\|)) ≤ Cσ√(nR⁺) | **ERROR** in the inequality; C2 **PROOF SKETCH after repair** | C2N: ratios 201 and 1,896; repaired bound ratio ≤ 0.963 |
| 15 | C3: SE + BM-∞ ⇏ PGD (combination look-alike) | **COUNTEREXAMPLE, VERIFIED** | EXP3-R; exact population computation |
| 16 | C4 | CONJECTURE (not assessed beyond EXP3-R, which is consistent with it) | |

## 3. Line-by-line notes on the verified steps

**3.1 Prop 1.** Take S = S₀ − j + l. It lies in R_d (d ≥ 1) and has size s₀ < K, so "add j" and "swap l→j" are both feasible.
- TD(1) at S names the only missing truth j and requires F(S₀+l) − F(S) ≥ m + F(S₀) − F(S).
- TD(3) at S₀, applied to "add l", requires F(S₀+l) − F(S₀) ≤ −m.
- Together these force m = 0 and equality.

The null-set claim needs x_l ∉ span X_{S₀}, which W1 states. The function y ↦ F(S₀+l) − F(S₀) is real-analytic on {Cy^r ≠ 0}.
It is non-constant, because a y orthogonal to col X_{S₀+l} and a y with a component along the residual of x_l give different
values. Its zero set is therefore null. All correct. Prop 1 is close to trivial, but it is right.

**3.2 Lemma 0.** (a) and (c) match the engine: strict improvement only; every scanned model goes to the ledger; the final
local search starts from `led.hpmS` and is the last scoring event. In (b) the inclusion is correct. The "in particular"
confuses a post-search quantity with a pre-search one (CEX-2).

**3.3 Lemma 3.** Every step checks:
- (I−P_S)μ = Σ_{j∈M}θ_j r_j.
- Hölder with ‖r_j‖ ≤ √(n−1).
- The Schur-complement eigenvalue bound needs SE on S ∪ S₀ (size ≤ s₀ + d ≤ m_n + s₀).
- Cauchy–Schwarz, then the Gram–Schmidt update.

**3.4 Theorem B.** On {S_c ∈ 𝒞} ∩ NA_d ∩ TL_d ∩ ⋂_{S∈Lat(𝒞), m≥1} D_S:
- (L) holds, and D_S holds on the superset states (Lemma 2(b) gives strictness). So A3's lattice version applies.
- The union over the data-independent Lat(𝒞) is legitimate.
- (B2) is a plain inclusion.
- The counts hold: Σ_{e≤d}C(N,e) ≤ (N+1)^d, and per state p + s(p−s) ≤ (K+1)p.
- The TL non-centrality for a swap truth k→null l needs SE on S₀ ∪ P′ ∪ {l}, of size s₀ + d + 1; that is fine.

**3.5 C1 (TL).** Removing truth k loses ≥ c nφ₀²θ_k² in signal, against O(√(nθ_k² log p)) noise and an O(log n + log p)
penalty. Under BM-∞ the signal term dominates, uniformly over polynomially many events. This is a plausible PROOF SKETCH;
the log-linearisation for non-small gaps is owed, but is standard.

## 4. Evidence (all reproducible; seeds fixed in each script)

**4.1 CEX-1** (`cex1_literalTD_d0_no_positivity.py` → `results/cex1.txt`). Literal TD(0,0) strict holds (0 failing clauses).
TD′_P fails only at ∅, where M(∅) = None.
- Gains at ∅: add x₁ −2.30, add x₂ −5.37, best null −5.44.
- F(S₀) − F(∅) = +20.99.
- Enumeration of 2¹² models gives the global HPM S₀, with π(S₀) = 0.86.
- The production local search from ∅ returns ∅, `certified = True`.
- λ_min(R_{S₀}) = 0.05.

**4.2 CEX-2** (`cex2_lemma0b_posterior_miss_with_ELS.py`).
- F(S_c) − F(S₀) = −2.29, so E_LS holds.
- The search goes S_c = {x₁, x₃} → {x₁, x₂, x₃} and stops, certified.
- F(S₀ + x₃) − F(S₀) = +7.21, so the fit is a posterior miss.

**4.3 EXP3-R** (`exp3_recheck.py` → `results/exp3_recheck.txt`). Population values: λ_min(R₁₂₃) = 0.15; R⁺(∅) = 0.090 and
R⁰(∅) = 0.130, so PGD fails exactly. Over 200 draws per n:

| n | first move "add x₃" | TD′_P(R_{2,1}) | TD′_∞(R_{2,1}) (all 4 × 7 = 28 states) |
|---|---|---|---|
| 200 | 139 | 36 | 40 |
| 1000 | 195 | 5 | 166 |
| 3000 | 200 | 0 | 198 |

W1 tested only the path from ∅. TD′_∞ on the whole region is now confirmed, so A5(b)'s "converse fails" holds.

**4.4 PROD, the production-scale rerun** (`prod_scale.py`, `summ_prod.py` → `results/prod_scale_summary.md`).
- Setup: n = 200, p = 500, s₀ = 14, S1–S6, c ∈ {1, 0.5}, 4 datasets per cell, own seeds, ℓ = 10.
- 18 sampled centres per dataset in R_{2,2}: look-alike or uniform extras.

Results:
- S₀ was a strict flip/swap local max in 35/48 datasets.
- **Centres reached S₀: 630/630 when S₀ is a local max, 0/234 when it is not.** No `local_limit`; at most 5 moves.
  Among the reached paths, 626/630 were all-progress.
- **E_LS held at 863/864 sampled centres.** 233 of the 234 non-repaired centres ended at a model with F ≥ F(S₀).
- At the 105 states S₀ − A with |A| ≤ 2, the greedy move was progress in a fraction 0.28–1.00 by cell, lowest at S5 with
  c = 0.5. Literal TD(1) held in exactly the same fraction, and literal TD(1) was never non-improving at production scale.

This agrees with W1's exp2 (1.000 reached given S₀ a local max, 0.99 all-progress). It also shows the mechanism of
non-repair: S₀ is not a local max, and the search runs past it. The sampled centres are not the SMC's actual centres, which
are the running HPM and score higher. So this does not settle the 0/541 question. It does show that "forced by monotonicity"
cannot be assumed.

**4.5 EXH, the exhaustive Theorem A check** (`exhaust_theoremA.py` → `results/exhaust_theoremA.txt`).
- Designs: p = 15, s₀ = 3, S1–S6, n ∈ {40, 80}, c ∈ {0.25, 0.5, 1}, 20 replicates each: 720 datasets, all 632 states of R₂.
- Checked: A1 iff, A1 length, A2 lattice/Φ/τ, A3 (ℓ = a + d, plus "all scored F ≤ F(S₀)"), A3 lattice version per centre,
  A5(b), Lemma 2(b). **0 violations.**
- Literal TD(2,0) strict: 0/720.
- TD′_P(R₂): 160; TD′_∞(R₂): 328 (168 have TD′_∞ without TD′_P).
- NA∧TL: 193.
- By cell, TD′_P(R₂) holds in 0/120 at (n = 40, c = 0.25) and up to 85/120 at (n = 80, c = 1).

**4.6 PHIR** (`phi_reach_vs_TDP.py`). Over 360 designs: PHI-REACH and TD′_P in 67, PHI-REACH alone in 23, TD′_P alone in 0.
Example paths are in `results/phi_reach_vs_TDP.txt`.

**4.7 C2N** (`c2_noise_bound.py`). Inequality (I), general pair: ratio 201 (orthogonal example). (II): ratio up to 1,896.
Repaired union bound: ≤ 0.963. Repaired C2 bound: ratio ≤ 7.7 at λ_min = 0.04, which is consistent with the constant 2a²/φ₀⁴.

## 5. Method faithfulness (W1's modelling vs. the spec and engine)

| Item | Spec / engine | W1 | Verdict |
|---|---|---|---|
| Centre | `led.hpmS`, the running HPM (v3_core.cpp:447, 610, 657) | the global best of 𝒮_pre | faithful |
| Scan | all feasible flips (adds only if \|S\| < K), all swaps, centre frozen (v3_engine.h:389–402) | N(S) | faithful |
| Best move | max F, exact ties broken by plain lexicographic order | the same | faithful. W1's exp2 uses argmax-first instead, which is immaterial because ties have measure zero |
| Move rule | strict improvement only (R14) | the same | faithful |
| Cap | ≤ ℓ moves, then one more scan; local_limit returns that best neighbour | the same; A3 uses only the certified branch | faithful |
| Scored models | every scanned model updates the HPM | used in Lemma 0(c) | faithful |
| Fit-level `local_certified` | also requires hpm == returned (v3_run.R:146) | "up to exact ties" | faithful |
| Several local searches (pilot, ≤ ℓ diagnostic iterations, final) | M §6.1 | treats the final one | acceptable. Lemma 0 holds for each search; only the final one fixes Ŝ |
| ESS / resampling / streams | irrelevant to the deterministic local search; they enter only through S_c | P(S_c ∉ 𝒞) term in B | faithful |
| Score F | M §5 | td_core matches bit for bit | faithful |
| Data generator | gen_dev_data.R | numpy port with the same covariance, truth and pre-scaling; different RNG | faithful in distribution, not the benchmark datasets |

## 6. What fails and why (routes tried)

- I tried to prove W1's "weakest" claim by a shortcut argument: any non-progress move is dominated by a direct swap. It fails
  for paths of length ≥ 3, and PHIR then produced counterexamples.
- I tried to bound ‖(P_{S′} − P_{S″})μ‖² by Δ-differences relative to S. It fails for non-nested pairs. The union-model bound
  (R5) is the correct tool.

## 7. Needs escalation

1. **Data extraction (decisive for T37's role).** For each of the 541 fits, compute F(S₀) − F(S_c) at the final local-search
   centre, and record whether the final local search improved the HPM. Without these numbers, "repair impossible by
   monotonicity" is not established.
2. **C2 after repair, and C1 with LD*.** The remaining owed step is the uniform linearisation of ν log(2b₀ + Q) with the
   ridge term; this is T01 material. A stronger prover should write it out once and reuse it for T02, T03 and T37.
3. **PGD.** No verification of when PGD holds in S1–S6. EXP3-R shows that it can fail under SE + BM-∞.

## 8. Outside scope

- At production scale the repair works exactly when S₀ is a local max (630/630 against 0/234). The binding issue at n = 200
  is therefore the statistical half: S₀ being beaten by a neighbour (T02/T03/T07), not the search. This supports §5 of
  THEORY_PRIORITIES.
- The Gibbs route (T24) is not assessed here.

## 9. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| T37(i) | W1 Theorem A with TD′_P / TD′_∞ / lattice condition (M(S) ≠ ⊥ built in); A5 with POS (R1) | high (VERIFIED) | high (done; Lean-ready) | none | no |
| original T37(i) | as filed | false (CEX-1 at d = 0; vacuous for d ≥ 1) | n/a | positivity | no |
| T37(ii) | W1 Theorem B, with the R6 headline | high | high for the inclusions; medium for explicit single-event tails | single 2- to 4-dim events with the ridge | no |
| T37(iii) | C2 under PGD(η) + SE + BM-∞, NA via LD* (R4, R5) | medium-high | medium | uniform linearisation of log Q; LD* and PGD are strong and unverified on S1–S6 | no |
| C3 | SE + BM-∞ ⇏ PGD | high (VERIFIED) | done | none | no |
| Lemma 0 data remark | "0/541 forced" | OPEN (cannot be judged without data) | trivial once the ledger numbers exist | F(S₀) vs F(S_c) per fit | no |
