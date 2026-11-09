# R01 — Statement-lock review of W2-FAC-PKA (STATEMENT v1 + PLAN)

Reviewer: Claude Opus 5.5 (high), fresh, cross-family relative to the lead. Brief: break the proposed scope.
Read: Wave2/Wave1C/Wave1 PROTOCOL.md; W2-FAC-PKA STATEMENT.md, PLAN.md (and the 3-line METHOD_REQUIREMENTS.md);
W2-FAC-B STATEMENT.md, lemmas/L1–L5, REPORT.md, numerics/fac_core.py, cs_core.py (and n2_saturated.py and
bvs_core.py signatures to see how the start and partition are computed); W2-APP lemmas/L5_VN.md; SoP
`02_method.tex:180-211` (partition, tables, start); `Scripts/SMC_BVS/core/v3_preprocess.R:19-31` (K, B, ℓ),
`cpp/v3_core.cpp:402-479` (LS0 cap), `v3_fit.R:43-47` (LS0 preflight); FINAL `s3_posterior.tex:9-10` (m♯_n, SE_w).
Not read: PKA LOG.md, anything from W2-FAC-PK.

## Verdict: **LOCK-WITH-CHANGES**

The scope split is right in spirit and several traps are already avoided: the exact-Gram rank frontier
p ≤ n − 1 is correctly identified; the statement explicitly says the rank obstruction is neither a counterexample
nor a settlement of K < p < n; LS0 failure is not equated with method failure; the finite-cap diagnostic (N2) is
not treated as an asymptotic failure; ℓ + 2|S̃₀| is labelled a conjecture; and the method is the merged core
(cap ℓ_n + |S̃₀| is what `v3_core.cpp:473` computes; K = min(p, ⌊n/2⌋) and B = min(⌊√n⌋, ⌊√p⌋, 16) as in
`v3_preprocess.R:21-23`). But the file is not yet a lockable *statement*: it imports FAC-B §§1–2 wholesale although
several of its items are false or meaningless for p > K, it has no explicit target claims or success criteria, it
overstates what the rank obstruction forces, and it misses two structural facts about the saturated start (truth
exclusion on open parameter sets; noise-driven, sign-biased selection) that change what can be imported from FAC-B.
Twelve required fixes (S1–S9 statement, P1–P3 plan); none is fatal to the programme.

## Required changes to STATEMENT.md

**S1. State target claims, not only questions.** A council cannot apply "hypotheses used = hypotheses stated" to
Q0–Q4. Write each as a claim with its alternative outcome, e.g.:
* T0 (rank frontier): exact CS Gram with ρ ∈ (0, 1) is realizable by a centred, standardized design with
  nonconstant raw columns iff p ≤ n − 1 (centred columns lie in 1^⊥; any PD correlation matrix of order ≤ n − 1 is
  realizable).
* T1 (start): characterization of S̃₀ (see S4–S5), including |S̃₀|, truth inclusion and the law of the retained nulls.
* T2 (LS0): either P(LS0 with cap a_n = ℓ_n + |S̃₀| scores S₀) → 1, or an **asymptotic LS0-route counterexample**,
  defined as a specified deterministic sequence (n, p_n, partition, S₀, ϑ) in the class with
  liminf P(LS0 with cap a_n does not score S₀) > 0. State the deterministic criterion used: LS0 with cap a scores S₀
  iff its uncapped path reaches S₀ in d ≤ a + 1 moves (prefix property, FAC-B STATEMENT §1); from a size-K start
  containing S₀ the MR1 cap tolerates at most ℓ_n + s₀ + 1 non-deletion moves.
* T3 (consequences): conditional on T2-positive, D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and delivery, each with its premises;
  conditional on T2-negative, only "the [OP] route gives no bound"; explicitly **not claimed**: D_n ↛ 0, failure of
  the full method.
* T4 (frontier, evidence only): Q4 deliverable (see S8).

**S2. Replace, do not import, the FAC-B items that depend on p ≤ n/2.** "Use FAC-B STATEMENT sections 1–2"
imports (P) p ≤ ⌊n/2⌋ and K = p, the sentence "(C1)–(C3) hold, at indices with K = p, for every deterministic
partition", the N₀/S* = [p] ∖ N₀ machinery whose meaning is that the start is "everything but N₀", and the (H0)
check, which cites p ≤ n/2. Write out: G, D0, method and premises (imported verbatim, with file:line); **(P′)
⌊n/2⌋ < p_n ≤ n − 1, K = ⌊n/2⌋ < p**; (CS); (θ); and the new genericity hypotheses (S4). Say explicitly that FAC-B
L3's E2 (r ≥ (n − 1 − p)(1 − n^{−1/3}) with N ≥ n/2 − 1) and L4.0(d) (M_T ≤ (1 + 1/n)n/(2r) ≤ 1 + n^{−1/4}) use
p ≤ n/2 and are not inherited; at p = n − 1, r ≡ 0.

**S3. Fix the p-regime and the boundary layers.** State whether the target is every sequence in (P′) or
p_n/n → c ∈ (1/2, 1) (recommended primary target, with c fixed), and treat separately: (a) p − K small (whether
the start saturates depends on p − K versus the number of zero-increment nulls N₀, |N₀| ≤ 15; saturation must be
proved, not presupposed — Q1 currently says "the saturated start"), (b) n − 1 − p = o(n) (the residual χ² term
degenerates; any bound on M_T must come from RSS_T with |T| ≤ K, not from r).

**S4. Truth inclusion and the genericity condition under saturation.** In FAC-B every element with a nonzero
population increment enters because the size cost is O(log n); with |S̃₀| = K < p the start solves an order-n
*allocation* problem across blocks, so inclusion depends on magnitudes, not on (FS)'s nonvanishing. Reviewer
scratch (population heuristic only, not a checked result: blocks of 16, J = 40, K = 0.625p, value of a block
subset = −log(1 − R²_pop(U)), exact knapsack over block size profiles, s₀ = 2, ϑ = (1, t), σ = 1): for
ρ ∈ {0.3, 0.5, 0.8} the weaker truth is **excluded** from the population-optimal start for t ∈ {−0.15, −0.1, −0.05}
(different blocks) and t = ±0.05 (same block) — open intervals of ϑ, all satisfying (FS). Truth blocks also receive
fills (5, 6, 15) different from null blocks (9–10). Required: (a) a population allocation hypothesis, e.g. (FS-K):
the population size-profile problem has a unique optimum up to permutations of identical null blocks, with a fixed
gap; (b) either a truth-priority hypothesis guaranteeing S₀ ⊆ S̃₀, or the path analysis must include truth-in swaps
(their gain is plausibly order n, so they may come first — but each costs one move of MR1's ℓ_n + s₀ + 1 slack).
(FS) alone must not be presented as the genericity condition.

**S5. The saturated start is noise-selected and sign-biased; FAC-B L3/L4 cannot be imported as black boxes.**
Identical null blocks and exchangeable nulls inside a block are population ties; they are broken at order √n by
t_{U,l} ∝ n c(U, l) + √n(g_l − γ_uΣ_U g), with c ∝ θ̄ for nulls. So the retained nulls are (conjecturally) the top
part of each block by sign(θ̄)·ξ, the start centre x_{S̃₀} is shifted by Θ(1), and the excluded nulls are
the ones far from it — exactly the swap incentive seen in N2 (19 swaps first). FAC-B's sign-symmetric events
(L3 E5–E7: conditional Rademacher signs of the top set) and the bulk centre bound (L4.3 B3) are therefore false
for the retained set; uniqueness of the start maximiser w.p. → 1 must also be re-proved (not inherited from L2).
T1 must deliver the conditional law of (retained set, ξ) on which T2 rests.

**S6. Partition.** Under exact CS all |r̂_{jl}| equal ρ, so the production complete-linkage dendrogram is decided
by tie rules (in floating point, by rounding), and next-fit packing leaves unequal blocks (SoP `02_method.tex:187-199`).
Unlike FAC-B's p ≤ n/2 case, the saturated start depends on the block-size profile and on truth placement (S4).
"Actual method partition" is therefore not a usable hypothesis. Claims must be uniform over every deterministic
partition into blocks of size ≤ B (with B ≤ K for delivery), or be parametrized by an explicit profile.

**S7. The rank-obstruction sentence overclaims.** "A separate population-CS iid-row design is necessary to make
p/n grow without bound" is false as stated. What is forced is: no positive-definite exact CS Gram for p ≥ n; every
design with p ≥ n has a singular Gram, and FAC-B L1's exact reduction (g ~ N(0, Σ), r ~ χ²_{n−1−p}) is lost.
Fixed deterministic designs with p ≥ n exist (e.g. Gram (n − 1)[ρ11ᵀ + (1 − ρ)W], W a unit-diagonal PSD Gram of
rank ≤ n − 2 such as a tight frame). Rephrase: iid-row population CS is a *chosen* (study-like) model for p ≥ n,
not a necessary one; and p/n fixed > 1 and p/n → ∞ (p ≤ n^A) are distinct cases.

**S8. Q2's SMC branch and Q4 need defined deliverables.** "Separately analyze discovery by SMC plus final search"
has no target: the only discovery inclusion available is [OP] (D_n ≤ P(LS0 misses S₀)); no lemma bounds the SMC
scored set or the final ℓ_n-capped search from the reported HPM. Either drop it from the theorem scope (record as
frontier with numerics at feasible n), or name a concrete inclusion to be proved. For Q4 (iid rows, p ≥ n), state
that the deliverable is evidence plus an exact list of missing proof inputs, no theorem, and that feasible n is far
below the onsets FAC-B observed (N3: failures up to n = 10⁴; N4: misses at n = 10⁵), so numerics there cannot
indicate asymptotic behaviour. In that list, separate genuinely missing inputs (exact reduction; X-measurable
partition; start/path analysis) from inputs that are probably standard: (H0) needs SE_w only up to
m♯_n = O(log n) (FINAL `s3_posterior.tex:9-10`), a sparse-eigenvalue fact for iid Gaussian rows with p ≤ n^A.

**S9. (H0) and costs for the exact-Gram part.** Record that (H0) remains automatic for exact CS with p ≤ n − 1
(λ_min(X_AᵀX_A) ≥ (n − 1)(1 − ρ) for every A; A = 1), with this justification rather than FAC-B L5.1's "p ≤ n/2".
For Q3, state the cost in production terms: at |T| = K each scan has ≈ K(p − K) swaps, and a cap ℓ + 2|S̃₀| ≈ n
changes the worst-case LS0 charge in `v3_fit.R:44` (ls0_scans = ell + K + 1) and Proposition F's envelopes; the
required path bound is d ≤ ℓ_n + 2|S̃₀| + 1.

## Required changes to PLAN.md

**P1. Numerics tooling is not reusable as stated.** `cs_core.ls0_path_cs` starts from [p], which is infeasible
when p > K, and assumes the full start; `fac_core.scan` is dense, O(k³) per scan, and `bvs_core.start_mode` scores
all 2^B subsets per block with the dense scorer. At the n where FAC-B saw asymptotic behaviour (≥ 10⁵–10⁷) with
p ≈ cn, neither is feasible. Plan a new closed-form CS module: block tables via (u, A_U, B_U) (2^16 subsets per block
is ≈ 4·10⁸ evaluations at p = 10⁵, feasible vectorized; p = 10⁶ is not), the size-capped start DP, and a path with
no additions at |T| = K and swap extremes. Self-test it against `fac_core`/`bvs_core` at small n, use the partition
convention of S6, and state the n-range in advance.

**P2. Protocol details.** CHECKPOINT at the key lemma *or after ~3 hours, whichever is first* (Wave-2 protocol);
name the key lemma in advance (T1 or the T2 path bound); include the Wave-1 stop rules (3 failed attempts → STUCK;
a counterexample to the locked target → stop and report); run source modules with `python -B` /
PYTHONDONTWRITEBYTECODE=1 (`W2-FAC-B/numerics/__pycache__` already exists and must not be rewritten).

**P3. Grid and falsification.** Include p/n near 1/2 and near 1 (S3); falsify T1 by comparing the population
allocation prediction (S4) and the sign-biased selection (S5) with the exact capped DP over ≤ 20 seeds; for T2,
record the move-type decomposition (deletions, null swaps, truth-in swaps) against MR1's slack ℓ_n + s₀ + 1.

## Not required (noted)

The method-fidelity paragraph is accurate against the code. "Scores of all neighbours, including the final scan
after a moves, count for discovery" matches CAP's prefix property. METHOD_REQUIREMENTS.md correctly makes no
requirement.
