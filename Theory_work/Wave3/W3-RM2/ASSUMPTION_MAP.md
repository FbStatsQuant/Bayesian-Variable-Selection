# ASSUMPTION_MAP.md — W3-RM2 (Wave 3 protocol item 3; written after the statement lock, before heavy proving)

Target statement: `STATEMENT.md` v1.2 LOCKED, claim ids `W3-RM2:RM2-F`, `W3-RM2:RM2-R` (and the lemma rows of its §7).
Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3. **Nothing is proved yet**: "enters at" refers to the planned proof
(PLAN §3; bridges P0–P10 of STATEMENT §4). "Observed" always means the numerics of `numerics/RESULTS.md`
(ids B1–B4): observations at n ≤ 3200, never proofs; all theorems are asymptotic. No cell asserts necessity for the
conclusion Ŝ⁺ = S₀.

## Proof sketch (the route)
RM-0 (W3-RM, any Q with |Q| ≤ K): start mode in the lattice [S₀, Q] (Sand) + no addition improves F anywhere on the
lattice (NA) + no truth-removing move improves F (TL) ⇒ LS0 deletes one extra per move and ends at S₀; with
π(S₀) > ½ every output run reports S₀. New at |Q| ≤ n^b: Sand by the size ladder and junk exclusion with margin
[β(η, A) − b] log n; TL by the toolkit at lattice cardinality 2^{|Q∖S₀|}; NA by Gaussian concentration of the lattice
maximum around its mean, the mean being controlled by (W).

## Entry map

| hypothesis | where it enters (bridge / step) | how (bound or mechanism) | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:T1-F / A:T1-R (Theorem 1's conditions) | P6 / P10 → [POST]; components ‖μ‖² ≤ Mn, p ≤ n^A → P0–P3 | inherited (SOP:TH09; W2-APP:POST) | P:POST (only "S₀ is the F-maximiser among scored models w.p. → 1" is needed by RM-0(b)) | none (as W3-RM) | none new |
| A:FL-16, A:FL-R (small sets) | P1 / P7 (block tables behave like regressions) | Gram floor on ≤ 16-sets | well-posed block regressions | none (as W3-RM) | none new |
| A:FL-Q (floor on Q ∪ {l}) | P2, P3, P4 ((W-loc) ⇒ (W-ref)), P8 | residual norms ≥ φ₀√(n − 1) on the lattice; truth removal costs ≥ nφ₀²θ²_min | lattice directions defined; atom coefficients ≤ L_n/φ₀ | none; at \|Q\| = n^b it is a floor on sets of polynomial size — holds for Gaussian rows iff b < ½-type (q√(log n/n) → 0 in P8) | none |
| A:V / A:V-R (visibility, "15") | P1 / P7, truth inclusion | truth's add gain ≥ M_n log n beats the prior cost | truths enter the start mode | not necessary on masked designs (W3-RM SHARPNESS §2); B3 observed: a weak truth is missing from the start mode in 32/32 runs and LS0 adds it | boundary-numerics (inherited) |
| A:L-gain (leak level η off Q, τ-form) | P1: ladder (3.3) and junk exclusion | Young's inequality between leak and noise; union over p·2^{20} block pairs | outside columns do not enter the start mode | none; converse heuristic only (W3-RM SHARPNESS §3.1). B4 observed: near the frontier (η ≤ 0.2) outside columns enter the start mode and LS0 deletes them; at η = 1, n = 1600, LS0 stops at its move cap before S₀ in 3/5 runs — an observed failure far outside the condition | artefact-threshold (η_A, and now the coupling b < β(η, A)); boundary-numerics |
| **A:L-size-b** (\|Q\| ≤ n^b, b < β(η, A); b < ½ at η = 0) | P1 junk exclusion only (the ladder and truth inclusion do not use it); P0/P2/P3 need only q log n/n → 0; (W-ref) needs h + b < ½ | deleting an outside column from a start mode of size k̃ gains log(p/k̃) + ½ log n − ½(noise + leak)²; the best of p noise gains is ≈ log p, so the margin is [½ − η/2 − √(2Aη)] log n − log k̃ | start mode ⊆ Q | **heuristic boundary at k̃ ≈ √n** (expected number of pure-noise columns entering a start mode of size k is ≈ k/√n): above it the sandwich in a *deterministic* Q should fail; not proved. B1 observed: an outside column in the start mode in 5/12 runs at b ≥ 0.625, n = 1600 | artefact-threshold (the coupling with η comes from a max bound; a counting form may decouple them); boundary-numerics: conclusion observed at b = 0.625, 0.75 |
| A:L-feas | P1 (ladder end; adding a truth is feasible), lattice ⊆ Ω | k̃ ≤ 2\|Q\| + 32s₀ < K | feasibility | FAC-PK (W3-RM SHARPNESS §3.2) is a failing class with saturated starts | none new |
| **A:BM-Q** (nθ²_min ≫ \|Q\| + log n) | P2 (TL) | toolkit union over the 2^{\|Q∖S₀\|} lattice sets: t_n + h_n² = O(\|Q\| + log n) must be ≪ the truth's removal cost | truth removal never improves F on the lattice | none. Looks WEAKENABLE: the union is over directions u_{T∖i,i}, and a width condition on them (as (W) does for additions) would replace \|Q\| by the width; under BM-∞ only | **single-use-union-bound**; B3 could not isolate it at feasible n (see RESULTS) |
| **A:W** (lattice width, 𝔴_n(δ₀) ≤ 0) | P3 NA-W | Gaussian concentration (1-Lipschitz maximum) + size-dependent score conversion | [NA(Q)]: no addition improves F at any lattice set | **NECESSARY-FOR-ROUTE up to the slack δ** (planned Lemma W-conv: if 𝔴⁺_n(δ₁) ≥ 0 then P(NA(𝓛)) → 0). Not necessary for the conclusion: B2 observed — NA(𝓛) truly violated at a probed lattice set in most runs, LS0 still ends at S₀ | boundary-numerics (improvable for the conclusion, not for the route); not derived from (V), (L) |
| A:W-χ, A:W-ref, A:W-loc (sufficient forms) | P4 | one χ² charge / frames + ℓ¹ atoms + ℓ² remainder / local regressions | E max over the lattice ≤ √(2 log p + 2h log n) + o(√log n) | sufficient only; (W-ref)'s ℓ¹ atoms do not cover a leak group sharing a common factor (ℓ¹ norm ≈ 1), where (W) itself may still hold (heuristic: width² ≈ 8 log q) | single-use-union-bound for the frame count (h + b < ½) |
| A:L-gain-R, A:L-loc-R, **A:H-size-ρ** (\|H_l\| ≤ n^ρ, 15ρ + b < ½) | P7 SAND-R^b | reference count n^{15ρ} per column in the ladder (needs 15ρ < ½) and in the maximum for junk exclusion (15ρ + b < ½) | selection removal for the X-measurable partition | none; reproduces W2-LOC2's cutoff α > 17/2 | **artefact-threshold** (15 = block cap − 1 times a counting bound); localisation removal open (W3-RM SHARPNESS §3.3) |
| A:W-R (width on the realised design) / A:D-R-b | P8 (F→R), P9 | conditional on X the lattice events are fixed-design events; (D-R^b) ⇒ (W-R) by NA-R's steps and a median–mean bound | as A:W | as A:W | as A:W |
| implementation premises, E4 hypotheses | RM-0, E4 | as W3-RM | — | — | — |

## Binding map (where each hypothesis is forced, as far as known now)
* A:W ← P:NA(Q), by W-conv (target): forced for the whole-lattice event, not for reporting.
* A:L-size-b ← P:SAND(Q) through junk exclusion: a sufficient budget; forced only heuristically (k̃ ≈ √n).
* A:H-size-ρ ← P:SAND(Q) through the reference count: a sufficient budget.
* A:BM-Q ← P:TL(Q) through the toolkit union: a sufficient budget.
* A:L-feas, A:V, A:L-gain, A:FL: as in W3-RM (`Theory_work/Wave3/W3-RM/ASSUMPTION_MAP.md`).

## Readings of the boundary-violation numerics (`numerics/RESULTS.md`; LS0 from the start mode, production score/tables)
207 runs (n = 400, 1600; p = 2n; nominal classification); "held" = LS0 from the start mode ends at S₀, certified.
Overall 204/207.

| id | assumption | outside it, the conclusion… | what failed on the way | flag |
|---|---|---|---|---|
| B1 | A:L-size-b (b < ½) | held in 48/48 runs at b ∈ {0.5, 0.625, 0.75} (start modes up to 241 columns at √n = 40) | sandwich in 3/6, 2/6 runs (b = 0.625, 0.75, n = 1600); a path-level no-addition margin > 0 in 1/6, 1/6, 4/6; up to 4 non-deletion moves per run against a cap slack of 15 | `improvable` (b ≥ ½ observed fine at these n; the protecting margin is the cap slack) |
| B2 | A:W | held in 48/48 | whole-lattice NA truly violated at a probed lattice set in 6/6 runs at b = 0.5, n = 1600 (3/6 at b = 0.375); never along the path | `improvable` for the conclusion; forced for the route |
| B3 | A:V at finite n (A:BM-Q not isolated) | held in 32/32 | the weak truth is missing from the start mode in 32/32; LS0 adds it | `improvable` (V); no information on BM-Q |
| B4 | A:L-gain (η) and the frontier b < β(η, A) | held in 32/32 at η = 0.05, 0.2; **failed in 3/5 at η = 1, n = 1600** (10/10 at n = 400) | η ≤ 0.2: a few outside columns in the start mode, deleted. η = 1: ~600 outside columns in the start mode, 19–35 swaps, LS0 stops at the move cap (slack 15) before S₀ | near the frontier `improvable`; far outside it the conclusion fails under the shipped cap — the leak condition is not only a proof device |

Inside every assumption (B1 at b ≤ 0.375): sandwich, path-level no-addition and deletion-only descent in 32/32 runs.

Conclusion level (identity < target < posterior < reported-model < delivery): **reported-model** (one data event of
probability → 1 on which every admissible output run reports S₀); rate: none claimed; scope: fixed design (F) and
Gaussian rows (R); s₀ fixed; p ≤ n^A, p ≫ n allowed; deterministic Q with |Q| ≤ n^b.

Unharvested conclusions (what the planned proofs give but the statement does not state):
* a polynomial failure rate for [NA(Q)]: under (W), P(max over 𝔓 of [Z² − c_n(|T|)] > 0) ≤ n^{−c(δ₀, A)} with
  c ≈ δ₀²/(8(2A + 2)) (Gaussian concentration with a gap of order δ₀√log n); for [SAND(Q)] the ladder gives
  O(√log n · n^{−ξ}) plus 1/log n terms from the maxima (the latter can be made polynomial); no rate for [POST];
* the archive certificate (`returned` = S₀, `local_certified`, moves = |S̃₀ ∖ S₀| ≤ n^b) — stated in (C1);
* uniformity over the class defined by the constants and rate envelopes (n₀ depends on nothing else);
* W-conv gives more than stated: when 𝔴⁺_n(δ₁) ≥ 0 an improving *addition at a lattice set* exists w.p. → 1.

Boundary-violation numerics: done in this leg (B1–B4); to be added to `ci/falsification.tsv` with `kind=boundary` at
CP3 together with a width probe for the examples.

Closest literature result and how ours compares (from memory; to be checked against the papers at the `lit:` gate):
* Song & Liang (2015, split-and-merge Bayesian variable selection): posterior consistency for p up to
  exponential in a power of n under sparse-eigenvalue and beta-min conditions — a statement about the posterior,
  with no search algorithm and no leakage structure. Our [POST] input is of that type (Theorem 1); the present
  theorem is about the *coded method's reported model*, which they do not address. No dominance either way.
* Yang, Wainwright & Jordan (2016, computational complexity of high-dimensional Bayesian variable selection): rapid
  mixing of an add/delete/swap Metropolis–Hastings chain under a restricted-eigenvalue condition, a beta-min
  condition and a **"sparse projection condition"** — a bound on the expected maximum over sparse sets S and columns
  k ∉ S of the Gaussian projection on (I − P_S)x_k, absorbed by choosing the prior's size-penalty exponent large
  enough. (W) is the same kind of object: a Gaussian-width bound on residual directions; here it is restricted to
  the lattice [S₀, Q], carries the exact constant of the shipped prior (level 2 log(p/(k + 1)) + log n; the prior is
  not tunable — no method change), and comes with a converse. Their result controls the whole path of the chain
  under a width condition over *all* sparse sets with a tunable prior; ours controls a deterministic greedy search
  under a width condition over the leak lattice only with the fixed prior. Incomparable; their condition is the
  natural literature anchor for (W) and for the path-level follow-up.
* Zhou, Yang, Vats, Roberts & Rosenthal (2022, dimension-free mixing / informed MH) and the greedy/forward-backward
  selection literature (An, Huang, Wainwright, Zhang-type results) give path-level guarantees under restricted
  eigenvalue and irrepresentable-type conditions; none treats a polynomial set of visible nulls around the truths
  with the BB(1, p) size prior. Relevant for the path-level ticket rather than for this statement.
