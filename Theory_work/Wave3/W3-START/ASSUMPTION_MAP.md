# ASSUMPTION_MAP.md — W3-START (Wave 3 protocol item 3; written after the statement lock, before heavy proving)

Target statement: `STATEMENT.md` v1.2 (LOCKED), claim ids `W3-START:AGG`, `W3-START:FLOOR`, `W3-START:START-F`,
`W3-START:START-R`, `W3-START:NEC`, `W3-START:OVL`, `W3-START:MIS`. Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3.
Numerics: `numerics/RESULTS.md` (production core, 1018 runs; observations, not proofs). Sections (a)–(i) below refer to it.

## 1. Assumption entry map

| hypothesis | where it enters (lemma / step) | how (bound or mechanism) | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:START-E, part ‖μ‖² ≤ Mn | (B-TK): toolkit constants C_R, c_E, κ_E | bounds ‖Y‖² ≤ C_Rn, so the O(1) remainder of the table expansion is uniform | [TK] | none; numerics (f) (θ ∝ n^{1/4}): o₀√n unchanged, T₁/pred ≈ 1 | boundary-numerics → **improvable** (route artefact of the toolkit) |
| A:START-E, part p ≤ n^A | truncation z_n; visibility threshold 1 + 2A; counting of the block family | union bounds over ≤ 2²¹p Gaussians; the prior price log p of one variable | [TK], [VIS], [LEAK] | (N2), (N3); numerics (a), (c): both transitions sit at 1 + 2A_n ≈ 3.2 | none (the dependence on A is sharp in the thresholds) |
| A:START-E, part s₀ fixed | (C1) constants; (B-V1) union over ≤ s₀ truth blocks | (s₀ + 1), 16s₀, c_s enter explicitly | — | numerics (g): o₀√n/(s₀ + 1) ≈ 1.4–1.9 for s₀ ≤ 4; for s₀ = 16, 32 the mass is lost at n ≤ 800 because visibility fails (τ² grows with ‖θ‖²), not because of the s₀-bookkeeping | unharvested-conclusion (bounds explicit in s₀; a growing-s₀ statement must carry the τ²-normalised visibility) |
| A:START-E, part p > s₀ | (T0), (T1)(c) | T₁ > 0, f_n(s₀) > 0 | — | SL1 counterexamples (saturated models; p = s₀) | none: NECESSARY for the stated conclusions |
| A:START-FL (FL-16) | (B-TK): Gram floor of the block family | log-determinant and Q ≈ RSS expansions (GEN L1.3 (E1), (E2)) | [TK] | none; numerics (e) (every second null a near-twin, λ_min ≈ 1/n): o₀√n ≈ 7 as in the baseline | boundary-numerics → **improvable** among nulls; single-use (toolkit) |
| A:START-V, form (V-c) | (B-V1): e_n → (AGG-d) → Ξ | each truth-deletion step ≤ n^{½−c_V/2+o(1)}; price 2p per deleted truth | [VIS(κ)] | (N3): level 1 + 2A necessary at truth-only sets; numerics (a) | **improvable**: quantifies over every 15-set; fails with close correlates while Ξ is small (numerics (b): min level 0.3–1.6 < 3.2, e_n ≈ 10⁴, Ξ ≤ 2·10⁻³, π₀(S₀) = 0.91–0.96). Superseded in generality by (V-m) |
| A:START-V, form (V-m) | (B-V2): each term of Ξ | two nested RSS comparisons through W = U ∪ D | [VIS(κ)] | (AGG-b): o₀ ≥ c_sΞ, so [VIS] itself is necessary; (N3) for D = {j}, N = ∅ | margin constants c_m, ε₀ are route constants; the form is close to the table functional it controls |
| A:START-AL | (B-L): truncated expectation of each table step | Markov on E[step·1_event] = e^{O(1)}n^{−1/2}J_n | [LEAK(Q)] | (AGG-b): o₀ ≥ T₁ (the leading functional is exact); (N2); numerics (d): when all nulls leak the transition is where the functional puts it (η ≈ Δ/τ² = 2/3; T₁/pred ≈ 1), far above η_A ≈ 0.09 | **improvable for isolated leakers** (numerics (c)): the uniform truncation z_n makes 𝔏 overshoot a single leaking null by 10–10³, so (AL) at Q = S₀ rejects c ∈ (≈1.3, 3.2) where the conclusion holds; remedy: put isolated leakers in Q with the individual threshold 1 + 2A. The max over all 15-sets U in 𝔏_n(Q) is used only at second order |
| Gaussian noise (model G) | Lemma J; toolkit χ² and Gaussian tails | exact Gaussian integral | [LEAK] | none | route (sub-Gaussian noise not attempted) |
| A:START-R-FL, A:START-R-V | (B-R) | sample floors and sample visibility from population ones, uniformly over ≤ p¹⁶ sets | (FL-16), (V-c) w.p. → 1 | as for the fixed-design forms | none |
| A:START-R-L, (L-gain-R) | (B-R): centring d of √n × sample partial correlation | E[e^{g²/2}; |g| ≤ h] with g ~ N(d, 1), d = O(C_L) | 𝔏_n(Q) ≤ e^{C√log n} | numerics (h): C_L = 1 converges; C_L = 2, 4 have U > 1 up to n = 1600 (U decreasing); just outside (ρ² = η log n/n) the behaviour is graded in η | **artefact-threshold**: C_L n^{−1/2} is not a threshold; a version with population leakage level η and an explicit exponent is the natural statement; the constant C_R decides the onset |
| A:START-R-L, (L-loc-R) | (B-R): the partition is X-measurable, so the conditioning set is selected | second-order perturbation √n·r_n² of δ_{U,l} | reduces max over p¹⁵ sets to polylog many | none (inherited form of W3-RM) | route |
| A:BLOCK-LE-16 | (C0) counting (2¹⁶ subsets; ≤ 15 partners) | constants only | — | true of the code | none |
| EX-A | everywhere | exact π₀ | — | idealisation | none |

## 2. Binding map (where each hypothesis is forced)
* visibility ← forced by (AGG-b) lower bound o₀ ≥ c_sΞ (deterministic) and by (C2)(ii)/(N3) at level 1 + 2A.
* averaged leakage ← forced by (AGG-b) lower bound o₀ ≥ T₁ (deterministic) and by (C2)(i)/(N2).
* the exponent ½ ← forced by (T0) for every design.
* (FL-16), ‖μ‖² ≤ Mn, Gaussian noise, (L-loc-R) ← forced only by the proof route (toolkit, Lemma J, localisation).

Conclusion level: target (start distribution; an input of the sampler theorems, not a posterior or reported-model
claim). Rate: n^{−1/2}𝔏⁰_n with 𝔏⁰_n between 1 and √log n when nothing leaks; n^{−1/2} is optimal (T0). Scope: p ≤ n^A
(p ≫ n included), fixed s₀, fixed design (partition-free conditions) or Gaussian rows; any X-measurable partition with
blocks ≤ 16.

Unharvested conclusions: (i) growing s₀ (table identities explicit in s₀); (ii) the first-order form identifies the
limit object T₁ — a distributional limit of √n·o₀ in specific designs is not stated; (iii) the same floor argument
gives 1 − π(S) ≥ c n^{−1/2} for the **posterior** of every unsaturated model (compare W3-POST:Prop-LB).

Closest literature and how ours compares (recorded comparisons: SoP card TH03, `04_theory.tex:345, 350`): Song–Liang
(2015) Theorem 4 / Corollary 2 give screening consistency of the posterior on a fixed-size candidate subset under
misspecification — no rate and no statement about an aggregate block-product start; Papaspiliopoulos–Rossell (2017)
compute block-diagonal posteriors exactly (orthogonal blocks) — the start here is that object for non-orthogonal
blocks, and the rate, the leakage functional and the floor are not in either. The `lit:` gate is a headline gate
(LIFECYCLE §4.2) and stays PENDING until CP3.
