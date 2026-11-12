# ASSUMPTION_MAP.md — W3-START (Wave 3 protocol item 3)

Target statement: `STATEMENT.md` v1.3.4. Claim ids `W3-START:<id>` as listed in `REPORT.md` §3. Rules:
`Theory_work/INFRA/LIFECYCLE.md` §4.3. This map describes the final statement; it replaces the map written before the
proofs. Numerics: `numerics/RESULTS.md` (production core, 1018 runs; sections (a)–(i) below refer to it) and
`numerics/lemmas/RESULTS_LEMMAS.md`; they are observations, not proofs.

## 1. Assumption entry map

| hypothesis | where it enters (lemma / step) | how (bound or mechanism) | property actually used | necessity evidence | signal |
|---|---|---|---|---|---|
| A:START-E, part ‖μ‖² ≤ Mn | Lemma TK, (TK-b) only (`lemmas/L2_TK.md`) | ‖Y‖² ≤ C_Rn, hence RSS^y_U ≥ c_En, which keeps the remainder of the score expansion bounded | [TK] | none. Numerics (f) (θ ∝ n^{1/4}): the conclusion is unchanged in that direction | route assumption; not removable outright with this toolkit (the scorer's fixed 0.02 and the ridge term are O(1) only relative to a residual of order n) |
| A:START-E, part p ≤ n^A (any fixed A > 0) | sizes of t_n, q_n, z_n; the prior price log p of one variable | union bounds over ≤ 2^{24}pn events; thresholds 1 + 2A | [TK], [VIS], [LEAK] | (C2)(i), (C2)(ii): both one-column thresholds sit at 1 + 2A; numerics (a), (c) | none: the dependence on A is sharp in the thresholds |
| A:START-E, part s₀ fixed | constants of (AGG), of L5.2, of the event 𝓧 | (s₀ + 1), 16s₀, c_s, s₀·3^{16} enter explicitly | — | numerics (g): for s₀ ≤ 4 the odds scale as (s₀ + 1) | unharvested: the table identities are explicit in s₀ (open item O3) |
| A:START-E, part p > s₀ | (T0), (T1)(b), (c), (B-R), (T3)(b) | T₁ > 0, s₀ < K | — | at p = s₀ there is no null column and the ratio o₀/T₁ is undefined | NECESSARY for the stated conclusions |
| A:START-GF (GF-16) | Lemma TK: (E1), (E2) and the rank of block sets | D_U/(n + 1)^{\|U\|} ∈ [(g_*/(g_* + 1))^{\|U\|}, 1]; 0 ≤ Q_U − RSS^y_U ≤ 1 + 1/g_* | [TK] | none. Numerics (e) (near-twin nulls) are inside the hypothesis | route assumption; dropping the floor altogether needs a rank-sensitive aggregation (open item O2) |
| A:START-V, form (V-c) | (B-V1), `lemmas/L4_VIS.md` L4.2: e_n, then (AGG-d) | each truth-addition step gains at least c_V log n; price log(2p) + ½ log n per truth | [VIS(κ)], κ < (c_V − 1 − 2A)/2 | (C2)(ii): level 1 + 2A necessary on the actual partition; (N3) partition-free | WEAKENABLE: it asks the single-truth gain given every 15-set; example F-2 satisfies (V-m) and not (V-c) |
| A:START-V, form (V-m) | (B-V2), `lemmas/L4_VIS.md` L4.1: each term of Ξ | two nested RSS comparisons through W = U ∪ D, with τ²_U on the left and τ²_W on the right | [VIS(κ)], κ < c_m/2 | (AGG-b): when s₀ + 16 ≤ K, π₀(S₀) → 1 forces Ξ → 0 in probability; this does not by itself force the polynomial-rate interface [VIS(κ)]. (C2)(ii) treats D = {j}, N = ∅. | the margin constants c_m, ε₀ are route constants; the form is close to the table functional it controls |
| A:START-AL | (B-L), `lemmas/L3_LEAK.md` L3.3, L3.4 | small gains from (J0); step bound; truncated expectation and Markov | [LEAK(Q)] | **T₁ → 0 is necessary** (o₀ ≥ T₁). The functional itself is **sufficient for this route**: the bridge is an upper bound by Markov's inequality, not a converse; the necessity of the truncated expectation and of the maximum over all conditioning sets is not established | the level per column (tail budget) removes the overshoot for a bounded number of leaking columns (F4), up to the level 1 + 2A̲ of (C2)(i) |
| Gaussian noise | Lemma TK tails; Lemma J | exact Gaussian integrals | [TK], [LEAK] | none | route |
| A:START-R-FL (FL-R16) | `lemmas/L9_BR.md` L9.1 (c2)–(c4), L9.5 | population floor on sets of size ≤ 16 + s₀; sample floors by the pairwise covariance event | (GF-16), Schur bounds, τ_e² ≥ c_Σ | as for the fixed-design floor | none |
| A:START-R-V (V-R) | `lemmas/L9_BR.md` L9.2 | sample visibility at every fixed level from the population conditional covariance | (V-c) | as for (V-c) | none |
| A:START-R-L, (L-gain-R) | `lemmas/L9_BR.md` L9.5 | a bounded mean shift d̄ of a standard Gaussian at the critical exponential moment | 𝔏_n(Q) ≤ exp(C√log n) w.p. → 1; tightness if C_L = 0 | numerics (h): no cliff at the scale C_Ln^{−1/2}; graded in the leakage level | ARTEFACT-threshold: a population leakage level with an explicit exponent is the natural statement (open item O1) |
| A:START-R-L, (L-loc-R) | `lemmas/L9_BR.md` L9.4 | columns outside H_l change √n × partial correlation by o(1/√log n) | reduces all 15-sets to ≤ (1 + (log n)^{κ_Q})^{15} reference sets per column | none | route |
| A:BLOCK-LE-16 | (AGG) counting (2^{16} subsets; ≤ 15 partners) | constants only | — | true of the coded partition | none |
| A:EX-A | everywhere | exact π₀ | — | idealisation | none |

## 2. Binding map (where each hypothesis is forced)

* **Visibility** ← Ξ → 0 in probability is necessary for concentration when s₀ + 16 ≤ K, by o₀ ≥ c_sΞ; the one-truth
  failure threshold is given by (C2)(ii) on the actual partition and (N3) partition-free.
* **T₁ → 0** ← forced by the deterministic lower bound o₀ ≥ T₁ of (AGG-b). The averaged leakage condition (AL) is a
  sufficient condition for it on this proof route; the necessity of its particular functional is not established.
* **Leak level 1 + 2A for one column** ← forced on the actual partition by (C2)(i). The partition-free form (N2) has an
  empty premise for s₀ ≤ 15 (it includes V = S₀, where every null gain is zero) and has content only for s₀ ≥ 16.
* **Exponent ½** ← forced by (T0) for every design with a null column.
* **(GF-16), ‖μ‖² ≤ Mn, Gaussian noise, (L-loc-R)** ← forced only by the proof route (Lemma TK, Lemma J, localisation).

## 3. Level, rate, scope

Conclusion level: target (the start distribution: an input of the sampler theorems, not a posterior or
reported-model claim). Rate: n^{−1/2} × leakage functional; with zero null gains (δ_{U,l} = 0 for all nulls) the leading
functional is at most (1 + 15/p)·√(2/π)z_n = O(√log n); n^{−1/2} is optimal by (T0). The target "no leakage" of the statement
is Q = S₀, and (AL) at Q = S₀ also allows functionals much larger than √log n. Scope: p ≤ n^A with any fixed A > 0
(p ≫ n included), fixed s₀; fixed design under partition-free conditions, any design law through the transfer, or
Gaussian rows; any partition that is a function of X with blocks of size ≤ 16.

Unharvested conclusions: (i) growing s₀ (the table identities are explicit in s₀); (ii) the first-order form
identifies the limit object T₁ — a distributional limit of √n·o₀ in specific designs is not stated; (iii) the same
floor argument gives 1 − π(S) ≥ c·n^{−1/2} for the **posterior** of every unsaturated model (compare W3-POST:Prop-LB);
(iv) (AGG-a) holds in the stronger form 1 − 1/F (`lemmas/L1_AGG_FLOOR.md` L1.2).

## 4. Numerics and what they do and do not show

* The production scripts of `numerics/` compute block-relative functionals; they do not verify the partition-free
  (AL). For Gaussian rows (AL) is delivered by bridge (B-R), not by a computation.
* The design `leakall` with η = 0 (satellites at correlation 0.9 with truths of fixed strength) is outside
  partition-free (AL) at Q = S₀; its good behaviour is block-relative (the satellites sit in the truths' blocks).
* Boundary numerics by assumption: (a) visibility threshold; (b) (V-c) against Ξ; (c) one leaking null; (d) all nulls
  leaking; (e) near-twin nulls; (f) energy; (g) s₀; (h) Gaussian rows with a population leak; (i) lattice form.
* Lemma falsification: `numerics/lemmas/RESULTS_LEMMAS.md`.

## 5. Closest literature

Recorded comparisons (SoP card TH03, `04_theory.tex:345, 350`): Song–Liang (2015) Theorem 4 / Corollary 2 give
screening consistency of the posterior on a fixed-size candidate subset under misspecification — no rate and no
statement about an aggregate block-product start; Papaspiliopoulos–Rossell (2017) compute block-diagonal posteriors
exactly (orthogonal blocks) — the start here is that object for non-orthogonal blocks, and the rate, the leakage
functional and the floor are not in either. The `lit:` gate is a headline gate (LIFECYCLE §4.2) and is open.

## 6. Open items named in the statement

O1: Gaussian rows with a population leakage level and an explicit exponent. O2: no Gram floor at all. O3: growing s₀.
