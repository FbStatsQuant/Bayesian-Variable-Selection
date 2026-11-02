# W1-T37R — REPORT (T37 truth dominance and greedy repair, restated)

Everything here is a candidate pending cross-family review. Long proofs are in `PROOF.md`, scripts in `scripts/`,
raw outputs and summaries in `results/`. Notation follows 00_COMMON.md. Additional notation: m(S) = |S₀∖S|
(missing truths), e(S) = |S∖S₀| (extras), Φ = m + e = |S Δ S₀|, R_{a,d} = {S ∈ R_d : m(S) ≤ a}. Moves split
into progress 𝒫 (add a truth, delete an extra, swap extra→truth; ΔΦ < 0), neutral 𝒩 (truth→truth or
null→null swap) and regressive ℛ (add a null, delete a truth, swap truth→null). M(S) is the production best-move
map, with ⊥ meaning there is no strict improvement.

## 1. Headline

* **PROVED (Prop 1).** Literal TD(d, m) **cannot hold for any d ≥ 1**, on any design and (up to a null set) any y.
  Take S = S₀ − j + l. There TD(1) requires F(S₀+l) − F(S₀) ≥ m, while TD(3) requires F(S₀+l) − F(S₀) ≤ −m. Decision
  D18 is therefore an internal contradiction, not a "generic failure". T37(iii) as written is false for every d ≥ 1,
  and T37(i) holds only vacuously.
* **PROVED (Lemma 0).** The search only moves to strictly better models and starts from the best model scored so
  far. So it can make Ŝ = S₀ only when S₀ is still unscored **and** F(S₀) > F(Ŝ_pre). On a posterior miss it cannot,
  whatever the move cap. The preliminary "0 repairs out of 541 centres in R₂∖S₀" is forced by this and says nothing
  about truth dominance. After a certified repair, Ŝ = S₀ automatically; the condition π(S₀) > ½ is not needed.
* **PROVED (Theorem A, the refined T37(i)).** TD′_∞(𝓡) is necessary and sufficient for the search to repair from
  every centre in 𝓡. TD′_∞ means: S₀ is a local max, no other state of 𝓡 is a local max, and greedy moves stay in 𝓡.
  TD′_P(R_{a,d}) (every greedy move is a progress move) is necessary and sufficient if, in addition, the number of
  moves must stay ≤ Φ ≤ a + d. **The cap only has to satisfy ℓ ≥ a + d, not ℓ ≥ s₀ + d.**
* **PROVED / PROOF SKETCH (Theorems B, C).** The finite-n bound now runs over the lattice of the centre (2^{Φ(S_c)}
  states), or over R_{a,d} (about s₀^a p^d states), with no 2^{s₀} factor. The asymptotic version needs two new
  named hypotheses: PGD (population greedy dominance) and LD (local dependence of nulls). **COUNTEREXAMPLE:**
  SE + BM-∞ do not imply PGD (a null that looks like a combination of two missing truths).
* **Evidence at n = 200** (72 regenerated datasets with p = 500, s₀ = 14). Whenever S₀ is a flip/swap local max,
  **all 1160/1160 sampled centres in R_{2,2} were repaired and certified in ≤ 3 moves**, and 99% of the paths used
  only progress moves. Every failure comes from S₀ **not** being a local max: a posterior miss, which no local
  search can fix. So the repair route works at n = 200 exactly where it is not needed.

## 2. Refined statements (full; named hypotheses)

Standing assumptions: EX-A; X and S₀ fixed; s₀ ≥ 1. 𝓡 is any finite family of feasible models containing S₀.

**Lemma 0 (monotonicity obstruction; PROVED).**
(a) F strictly increases along the search path.
(b) The search can make S₀ a centre, or make Ŝ = S₀, only on E_LS = {S₀ ∉ 𝒮_pre, F(S₀) > max_{𝒮_pre} F}.
(c) If the search stops at S₀ with local_certified, every model it scored has F ≤ F(S₀), so Ŝ = S₀ up to exact
ties.

**Prop 1 (PROVED).** Assume s₀ ≥ 1, d ≥ 1, s₀ + 1 ≤ K and p > s₀. Then TD(d, m) implies m = 0 and F(S₀+l) =
F(S₀) for every null l. Under G, P₀(TD(d, 0)) = 0.
Swap identity (SW): F(S − i + j) − F(S) = g(S, j) + h(S + j, i). So "swap i→j" beats "add j" exactly when i can be
deleted once j is in.

**Conditions.**
* TD′_∞(𝓡): (L) M(S₀) = ⊥; (N) for every S ∈ 𝓡∖S₀, M(S) ≠ ⊥ and M(S) ∈ 𝓡.
* TD′_P(𝓡): (L), and M(S) ∈ 𝒫(S) for every S ∈ 𝓡∖S₀.
* D_S (one-state progress event): the best progress neighbour of S strictly beats S and every non-progress neighbour.
* Lat(S) for S = U ∪ P (U ⊆ S₀, P ⊆ S₀ᶜ): Lat(S) = {U′ ∪ P′ : U ⊆ U′ ⊆ S₀, P′ ⊆ P}.
* NA_d: for every P′ ⊆ S₀ᶜ with |P′| ≤ d and every null l ∉ S₀ ∪ P′, F(S₀ ∪ P′ + l) < F(S₀ ∪ P′).
* TL_d: from every S₀ ∪ P′ with |P′| ≤ d, every move that removes a truth has negative gain.
* PGD(η) on R_{a,d}: for every S with m(S) ≥ 1, R⁰(S) ≤ (1−η)R⁺(S). Here R⁺ and R⁰ are the best reductions of
  Δ_S = ‖(I−P_S)μ‖²/(n−1) achievable by a progress move and by a non-progress move, respectively.
* LD(d): for every P′ with |P′| ≤ d, all but at most B′|P′| nulls l have ρ²(l, P′ | S₀) ≤ κ_n, where ρ² is the
  squared partial correlation and κ_n log p → 0. COH implies LD.

**Theorem A (refined T37(i); PROVED).**
(A1) TD′_∞(𝓡) holds if and only if the uncapped greedy path from every S ∈ 𝓡 stays in 𝓡 and ends at S₀. The path
from S has at most #{S′ ∈ 𝓡 : F(S′) > F(S)} moves.
(A2) Under TD′_P(R_{a,d}), the path from S stays in Lat(S) and reaches S₀ in τ(S) moves, where τ(S) = m + e −
#(extra→truth swaps) and max(m, e) ≤ τ(S) ≤ Φ(S).
(A3) Suppose TD′_P(R_{a,d}) holds and ℓ ≥ a + d. Then from every centre S_c ∈ R_{a,d} the production search
returns S₀ with local_certified and without local_limit, and Ŝ = S₀. The same conclusion holds for one given
centre under the weaker lattice condition (L) ∧ ⋂_{S ∈ Lat(S_c)∖S₀} D_S.
(A4) Each conclusion implies posterior dominance on the states it starts from.
(A5) Literal strict TD(d, 0) ⇒ TD′_P(R_d) ⇒ TD′_∞(R_d). The first premise is impossible for d ≥ 1. The reverse of
the second implication fails (Exp 3).

**Lemma 2 (PROVED).** Progress moves keep Lat(S) and R_{a,d} closed. On NA_d ∩ TL_d, S₀ is a local max, and at
every S₀ ∪ P with 1 ≤ |P| ≤ d the best move is deletion of an extra.
**Lemma 3 (PROVED).** If S ⊉ S₀ and SE holds on S ∪ S₀, then max_{j ∈ S₀∖S} δ²_{S,j} ≥ (n−1)φ₀⁴‖θ*_{S₀∖S}‖²/m(S).

**Theorem B (refined T37(ii); PROVED for the inclusions and the union bound, PROOF SKETCH for the form of each
single event).** Assume G. Let 𝒞 ⊆ R_{a,d} be any class of centres chosen without looking at the data, with ℓ ≥
max_𝒞 Φ. Then

  P(the search fails) ≤ P(S_c ∉ 𝒞) + P₀(NA_dᶜ) + P₀(TL_dᶜ) + Σ_{S ∈ Lat(𝒞), m(S) ≥ 1} P₀(D_Sᶜ),

and P₀(D_Sᶜ) ≤ Σ over the ≤ (K+1)p non-progress neighbours S″ of P₀(F(π(S)) ≤ F(S″)), plus P₀(F(π(S)) ≤ F(S)),
for any fixed progress move π(S). For a single centre the state count is 2^{Φ(S_c)}; with 𝒞 = R_{a,d} it is at most
(2s₀)^a (p+1)^d. Each comparison is an event in a Gaussian vector of dimension ≤ 4, conditional on an independent
residual χ², and the ridge contributes O(1/n).

**Theorem C (refined T37(iii)).** Regime R1 with G, R, SE and BM-∞; a and d fixed.
(C1) PROOF SKETCH: TL_d holds with probability → 1. Under LD(d), NA_d holds with probability → 1. Without LD, the
plain union bound needs p^d = o(√(n log n)).
(C2) PROOF SKETCH: under PGD(η), TD′_P(R_{a,d}) holds with probability → 1. Hence repair from every centre in
R_{a,d}, certified, for all n large enough that ℓ_n ≥ a + d.
(C3) COUNTEREXAMPLE: SE + BM-∞ ⇏ PGD (Exp 3).
(C4) CONJECTURE: without PGD, TD′_∞ still holds on an enlarged region R_{a, d+d₁}.

These statements replace GAIN_d, LK_d and EXIT_d **only for the local-search route, and only on E_LS**.

## 3. Proofs and sketches

All proofs are in `PROOF.md`. In brief:
* Prop 1: two-line contradiction at S₀ − j + l. Probability-0 statement: the zero set of a non-constant
  real-analytic function of y.
* Lemma 0: strict monotonicity of the best-improvement rule. Every scanned model has F ≤ F(next centre).
* Theorem A: induction along the path, plus finiteness under strictly increasing F. For (A2), Φ is a potential that
  each progress move lowers by 1 or 2.
* Lemma 2: from (SW) and NA at P − l, h(S, l) = −g(S − l, l) > 0, and a null→null swap is worse than the matching
  deletion.
* Lemma 3: a Schur-complement bound plus Cauchy–Schwarz.
* Theorem B: deterministic inclusion of events, then a union bound over a family fixed in advance. This is valid
  even though S_c depends on ε.
* Theorem C: linearise ν log Q_T around (n−1)v_T and bound the noise uniformly. The noise in a comparison has
  standard deviation ≲ σ√(nR⁺), while the population margin is ≳ ηnφ₀⁴θ²_min ≫ log n under BM-∞. NA via the
  perturbation (I − P_T)x_l = (I − P_{S₀})x_l − P_Ṽ(…). The gaps are listed in §6.

## 4. Evidence (fixed seeds; Python reimplementation; R not used)

The scorer was checked against a direct dense marginal-likelihood computation, agreeing to 1e-14
(`scripts/td_core.py`). Data are regenerated with numpy, so they are **not** the benchmark's R streams. Covariances
and the truth pattern are verbatim ports of `gen_dev_data.R`.

**Exp 2: production scale** (`exp2_prod_scale.py`, `results/exp2_summary.md`). n = 200, p = 500, s₀ = 14,
ℓ = 10; S1–S6 × c ∈ {1, 0.5} × 6 replicates = 72 datasets.
* S₀ is a flip/swap local max in 35/36 datasets at c = 1 (the exception is S2, beaten by adding a noise null) and in
  23/36 at c = 0.5. The c = 0.5 failures are weak-truth deletions and truth→look-alike swaps, concentrated in S4–S6:
  0.50, 0.33 and 0.50 of datasets are local maxima there.
* When S₀ is not a local max, greedy from S₀ reaches S* with F(S*) − F(S₀) between 0.2 and 4.8 nats (median 1.3).
  These are certified posterior misses: S₀ is not the HPM of Ω.
* 20 centres per dataset (a ∈ {1,2} missing truths; e ∈ {0,1,2} extras, either look-alikes from a missing truth's
  group or uniform). **In the 58 datasets where S₀ is a local max, 1160/1160 centres were repaired and certified,
  using 1–3 moves (≤ ℓ = 10).** 99.0% of the paths were all-progress; the exceptions are truth→truth swaps. Moves on the
  successful paths were: 1156 extra→truth swaps, 584 truth additions, 236 extra deletions, 11 truth→truth swaps and
  1 null→null swap (1988 in total). In the other 14 datasets, 0/280 centres were repaired, which
  Lemma 0 forces.
* At the 105 d = 0 states with m ≤ 2, the greedy move is "add a truth" in 3732/3780 cases at c = 1. At c = 0.5 it
  is "add a truth" in only 2472/3780 cases; truth→truth swaps take 1239. **This is why literal TD(0) fails.**

**Exp 1: small exact enumeration of R₂** (`exp1_small_exact.py`, `results/exp1_p20_summary.md`). n = 200, p = 20,
s₀ = 4, S1–S6 × c ∈ {1, 0.5, 0.25} × 50 replicates. It was run twice: with the true size prior, and with the size
prior penalty-matched to p = 500 ("pm500", labelled).
* Literal TD(1, 0): **0/1800**, confirming Prop 1.
* Literal TD(0, 0) fails at d = 0 states mainly through truth→truth swaps (1491 and 2149 states summed over
  datasets) and weak-truth deletions (118 and 807).
* Among datasets with PD and S₀ a local max (about 620–670 of 900 per run):
  * TD′_∞(R_{s₀,2}): 0.92 / 0.94 (true prior / pm500);
  * TD′_P(R_{s₀,2}): 0.71 / 0.71;
  * TD′_P(R_{1,1}): 1.00 / 1.00;
  * TD′_P(R_{2,2}): 0.78 / 0.83; TD′_∞(R_{2,2}): 0.97 / 0.98;
  * uncapped path-wise repair from **every** state of R_{s₀,2} is almost exactly equivalent to "S₀ is a local max"
    (the "path" column);
  * at most 6 moves were ever needed, while ℓ = 7 at p = 20 and 10 at p = 500.
* The worst state-wise violations are noise-driven:
  * the missing truth's projection is cancelled by noise (for example δ = 5.13 with noise −3.27), so deleting a
    weak truth wins by up to 14.5 nats;
  * at c = 0.25 a truth→null swap brings in a look-alike (δ_l ≈ −3.7 versus a missing truth with δ ≈ −3.6).
  Consistent with T37's "Why", these are look-alike leakage at the level of the missing truth's projection.
* At c = 0.25, S₀ is a local max in only 2–48% of datasets: the posterior misses dominate.

**Exp 3: COUNTEREXAMPLE to PGD under SE** (`exp3_combination_lookalike.py`, `results/exp3_combination.txt`).
Design: truths x₁ ⊥ x₂, null x₃ = 0.85(x₁+x₂)/√2 + √(1−0.85²)z, so φ₀² = 0.15. At n = 3000 the first greedy move from
∅ is "add x₃" in 200/200 draws. The uncapped path still reaches S₀ in 3 moves, against Φ = 2. TD′_P fails and
TD′_∞ holds.

## 5. What fails and why

1. **Literal TD, d ≥ 1.** It is self-contradictory (Prop 1). The progress swap extra→truth is exactly the move that
   literal TD forbids, and it is the main repair move in practice (1156 of the 1988 moves on successful Exp-2 paths).
2. **Literal TD at d = 0, and TD′_P on large regions.** A missing truth inflates the residual variance, which
   masks weak truths. At S, deleting a weak truth k (or swapping k for the missing truth j) wins when the t-statistic
   of k given S + j − k is below √(2·pen), where pen = ½log(n+1) + log((2p−k)/(k+1)), so √(2·pen) ≈ 3.7 at n = 200,
   p = 500. Such moves are neutral or regressive, so TD′_P fails, but the path usually recovers (TD′_∞ and the
   path-wise condition hold).
3. **Requiring the condition on all of R_d (2^{s₀} states).** This is the wrong object. The masked-regime centres
   have small Φ, and the condition is needed only on Lat(S_c). Restricting to R_{a,d} removes the 2^{s₀} factor and
   the cap problem.
4. **Asymptotics.** SE + BM-∞ alone do not give progress, because of combination look-alikes (C3). NA_d with d ≥ 2
   needs LD: pairs of correlated nulls fitting noise. The plain union bound grows like p^d/√n.
5. **At n = 200 the binding constraint is posterior dominance, not search.** S₀ fails to be a local max in 13/36
   regenerated c = 0.5 datasets at p = 500 (S4–S6 worst), and 0.2–4.8 nats separate it from a better model. In those
   fits no repair theorem can deliver S₀ (Lemma 0). Where S₀ is a local max, repair succeeded every time in our
   sample. **So T37 is an asymptotic statement plus a finite-n "works whenever the posterior allows" observation; it
   cannot explain the masked-regime successes, which (by Lemma 0 and the 98% Gibbs share) were scored before the
   search.**
6. **Move cap.** ℓ = 10 < s₀ + d = 15 is a non-issue once the region is R_{a,d} with a + d ≤ 10. The observed moves
   were ≤ 3 at p = 500 and ≤ 6 at p = 20. T37(i)'s "exactly |S Δ S₀| moves" is wrong in general: swaps give
   τ = Φ − #swaps.

## 6. Needs escalation

* Theorem C(C1), NA_d under LD: the claim that the exceptional events depend only on correlated neighbours needs the
  perturbation bound written out for the non-neighbour part. Independent check wanted.
* Theorem C(C2): a uniform linearisation of ν log(2b₀ + Q_T) that includes the ridge term H = (n+1)G + I (T01
  material). The noise bound sd ≲ σ√(nR⁺) for comparisons between neighbours also needs checking.
* Theorem B: the claim that each single event is a ≤ 4-dimensional non-central event conditional on an independent
  χ² is exact only without the ridge. State the O(1/n) correction.
* Conjecture C4: bound the number of regressive null additions on population greedy paths.
* Independent recheck of Exp 2 on the actual benchmark datasets (R streams). This needs R.

## 7. Outside scope (brief)

* **The Gibbs route is the right repair statement for this method (my view; T24 belongs to another run).** Under
  SR, every Gibbs update scores both configurations. So a particle at S = S₀ − j scores S₀ in the very first sweep
  that reaches j, deterministically. From S = S₀ − j + l, S₀ is scored as soon as j has been accepted (its
  conditional odds are e^{g} with g ≫ 1) and the l update comes after that in some sweep. The probability is about ½
  per round and → 1 over L + 4 rounds. Scoring needs no F-monotonicity, so the Gibbs route works on E_LS and on
  its complement alike. What it needs for Ŝ = S₀ is only posterior dominance over the scored set. The local search
  adds only swaps, and Gibbs reproduces a swap with two flips. Suggested restatement: "T24: from any particle in
  Lat-type neighbourhoods of S₀ with Φ ≤ 2, S₀ is scored within one or two rounds w.p. ≥ 1 − ε". T37 then becomes a
  backup that matters only on E_LS.
* Lemma 0(c) shows that T21's π(S₀) > ½ premise is unnecessary for the local-search delivery of Ŝ = S₀.
* The posterior misses at c = 0.5 in S4–S6 (strong within-group correlation) contradict the "correlated-design
  advantage" margin story of T37's Why, at least at n = 200.

## 8. Confidence cards

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change needed? |
|---|---|---|---|---|---|
| Prop 1 (literal TD) | unsatisfiable for d ≥ 1 | 0.99 | done (PROVED) | none | no |
| Lemma 0 | monotone obstruction; Ŝ = S₀ after certification | 0.98 | done (PROVED) | reading "centre = led.hpmS" (confirmed in v3_core.cpp) | no |
| T37(i) → Theorem A | TD′_∞ iff; TD′_P with ≤ Φ moves, ℓ ≥ a + d | 0.97 | done (PROVED) | none | no |
| T37(ii) → Theorem B | lattice/R_{a,d} union bound | 0.95 | 0.9 (event description) | ridge correction | no |
| T37(iii) → Theorem C (C1–C2) | TD′_P(R_{a,d}) w.p. → 1 under PGD + LD | 0.8 | 0.6 | NA_d without COH; uniform linearisation | no |
| C4 | TD′_∞ without PGD | 0.6 | 0.3 | bounded number of regressive steps | no |
| "T37 explains the n = 200 masked-regime successes" | — | 0.1 | — | Lemma 0: the search cannot act on posterior misses, and successes were scored earlier | rely on Gibbs (T24) |
