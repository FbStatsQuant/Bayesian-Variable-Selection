# ASSUMPTION_MAP.md — W3-RM2 (Wave 3 protocol item 3; written after the statement lock, before heavy proving)

Target statement: `STATEMENT.md` v1.4, claim ids `W3-RM2:RM2-F`, `W3-RM2:RM2-R` (and the lemma rows of the registry
block in `REPORT.md`). This map was written for v1.2 and reviewed with it (BT1); the rows marked [v1.3] were
updated after HQ's CP1 decision and the Form R row after the CP2 riders [v1.4].
Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3. [SW1-4] The map now describes the proofs as written: "enters at"
refers to the proof files `lemmas/L0`–`L5` (bridges P0–P10 of STATEMENT §4); the status of every claim is in
`REPORT.md` §3. "Observed" always means the numerics of `numerics/RESULTS.md`
(ids B1–B4): observations at n = 400 and 1600 [MP1-3], never proofs; all theorems are asymptotic. No cell asserts necessity for the
conclusion Ŝ⁺ = S₀.

## Proof sketch (the route)
RM-0 (W3-RM, any Q with |Q| ≤ K): start mode in the lattice [S₀, Q] (Sand) + no addition improves F anywhere on the
lattice (NA) + no truth-removing move improves F (TL) ⇒ LS0 deletes one extra per move and ends at S₀; with
π(S₀) > ½ every output run reports S₀. New at |Q| ≤ n^b: Sand by the size ladder and junk exclusion with margin
[β(η, A) − b] log n; TL by the exact two-square identity and the truth-removal width d_n (`lemmas/L2_width.md` §4) [SW1-4]; NA by Gaussian concentration of the lattice
maximum around its mean, the mean being controlled by (W).

## Entry map

| hypothesis | where it enters (bridge / step) | how (bound or mechanism) | property actually used | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:T1-F / A:T1-R (Theorem 1's conditions) | P6 / P10 → [POST]; components ‖μ‖² ≤ Mn, p ≤ n^A → P0–P3 | inherited (SOP:TH09; W2-APP:POST) | P:POST (only "S₀ is the F-maximiser among scored models w.p. → 1" is needed by RM-0(b)) | none (as W3-RM) | none new |
| A:FL-16, A:FL-R (small sets) | P1 / P7 (block tables behave like regressions) | Gram floor on ≤ 16-sets | well-posed block regressions | none (as W3-RM) | none new |
| A:FL-Q (floor on Q ∪ {l}) | P2, P3, P4 ((W-loc) ⇒ (W-ref)), P8 | residual norms ≥ φ₀√(n − 1) on the lattice; truth removal costs ≥ nφ₀²θ²_min | lattice directions defined; atom coefficients ≤ L_n/φ₀ | none; at \|Q\| = n^b it is a floor on sets of polynomial size — for Gaussian rows it is supplied here by the sufficient entrywise bound q√(log n/n) → 0 (in particular b < ½); necessity is not asserted [MP1-1] | none |
| A:V / A:V-R (visibility, "15") | P1 / P7, truth inclusion | truth's add gain ≥ M_n log n beats the prior cost | truths enter the start mode | not necessary on masked designs (W3-RM SHARPNESS §2); B3 observed: a weak truth is missing from the start mode in 32/32 runs and LS0 adds it | boundary-numerics (inherited) |
| A:L-gain (leak level η off Q, τ-form) | P1: ladder (`lemmas/L1_sandF_b.md` (2.2)–(2.3)) and junk exclusion (Step 2(b)) [C1-F4] | Young's inequality between leak and noise; union over p·2^{20} block pairs | outside columns do not enter the start mode | none; converse heuristic only (W3-RM SHARPNESS §3.1). B4 observed: near the frontier (η ≤ 0.2) outside columns enter the start mode and LS0 deletes them; at η = 1, n = 1600, the LS0 probe stops at its move cap before S₀ in 4/6 runs [MP1-3] — an observed finite-n failure of the LS0 probe far outside the condition | artefact-threshold (η_A, and now the coupling b < β(η, A)); boundary-numerics |
| **A:L-size-b** (\|Q\| ≤ n^b, b < β(η, A); b < ½ at η = 0) | P1 junk exclusion only (the ladder and truth inclusion do not use it); P0/P2/P3 need only q log n/n → 0; (W-ref) needs h + b < ½ | deleting an outside column from a start mode of size k̃ gains log(p/k̃) + ½ log n − ½(noise + leak)²; the best of p noise gains is ≈ log p, so the margin is [½ − η/2 − √(2Aη)] log n − log k̃ | start mode ⊆ Q | **heuristic boundary at k̃ ≈ √n** (expected number of pure-noise columns entering a start mode of size k is ≈ k/√n): above it the sandwich in a *deterministic* Q should fail; not proved. B1 observed: an outside column in the start mode in 5/12 runs at b ≥ 0.625, n = 1600 | artefact-threshold (the coupling with η comes from a max bound; a counting form may decouple them); boundary-numerics: conclusion observed at b = 0.625, 0.75 |
| A:L-feas | P1 (ladder end; adding a truth is feasible), lattice ⊆ Ω | k̃ ≤ 2\|Q\| + 32s₀ < K | feasibility | FAC-PK (W3-RM SHARPNESS §3.2) is a failing class with saturated starts | none new |
| **A:BM-W** [v1.3] (nθ²_min ≫ d_n² + log n, d_n = Gaussian width of the truth-removal directions; implied by the v1.2 condition (BM-Q): nθ²_min ≫ \|Q\| + log n) | P2 (TL) | exact identity RSS_A − RSS_T = (θ_i‖(I − P_A)x_i‖ + σZ_{A,i})² − σ²Z²_{T,l}; Gaussian concentration of max over the truth-removal directions; the subtracted term is controlled by (W) | truth removal never improves F on the lattice | none (sufficient; necessity not studied). In v1.2 this was (BM-Q), a single-use union bound over the 2^{\|Q∖S₀\|} lattice sets — replaced on BT1's proposal P1 | none now (was single-use-union-bound); B3 could not isolate it at feasible n (see RESULTS) |
| **A:W** [v1.3] (lattice width gap 𝔴⁰_n → −∞; the v1.2 fixed-fraction form 𝔴_n(δ₀) ≤ 0 is sufficient) | P3 NA-W | Gaussian concentration (1-Lipschitz maximum) + size-dependent score conversion | [NA(Q)]: no addition improves F at any lattice set | [MP1-2] a sufficient negative-gap condition with a positive-gap obstruction (Lemma W-conv: if 𝔴⁰_n → +∞ then P(NA(𝓛)) → 0) and an unresolved bounded-gap regime; no necessity for reporting is proved or refuted. B2 observed, at finite n: the LS0 probe ends at S₀ although NA(𝓛) is violated at a probed lattice set in most runs | boundary-numerics (improvable for the conclusion, not for the route); not derived from (V), (L) |
| A:W-χ, A:W-ref, A:W-loc (sufficient forms) | P4 | one χ² charge / frames + ℓ¹ atoms + ℓ² remainder / local regressions | E max over the lattice ≤ √(2 log p + 2h log n) + o(√log n) | sufficient only; (W-ref)'s ℓ¹ atoms do not cover a leak group sharing a common factor (ℓ¹ norm ≈ 1), where (W) itself may still hold (heuristic: width² ≈ 8 log q) | single-use-union-bound for the frame count (h + b < ½) |
| A:L-gain-R [v1.4: leak ϖ_n = o(√(log n/n)) at every conditioning set of size ≤ 15], A:L-loc-R [v1.4: r_n → 0, no rate], **A:H-size-ρ** (\|H_l\| ≤ n^ρ, 15ρ + b < ½) | P7 SAND-R^b (`lemmas/L4_sandR_b.md`) | leak: the cross term of selection removal equals the difference of the leak covariances at U₀ and at U (product form), and a mean shift of norm o(√log n) in the spherical tail; localisation: only the sample error r_nh_n of that cross term; reference count n^{15ρ} per column in the ladder (needs 15ρ < ½) and in the maximum for junk exclusion (15ρ + b < ½) | selection removal for the X-measurable partition; outside columns do not enter the start mode | none proved. Harvested in v1.4: the rate on r_n — and the reference radius n^ρ, ρ > 1/(4α), it forced in decaying designs — was an artefact of a norm bound [CP2-T6]; the leak constant C_Ln^{−1/2} was an artefact [CP2-P3]. Open: the exact leak scale κ√(log n/n) (O3′) | artefact-threshold (15ρ: reference counting) |
| A:W-R (width on the realised design) / A:D-R-b | P8 (F→R), P9 | conditional on X the lattice events are fixed-design events; (D-R^b) ⇒ (W-R) by NA-R's steps and a probability-≥ ½ event plus lower-tail concentration about the mean [C1-F5] | as A:W | as A:W | as A:W |
| implementation premises, E4 hypotheses | RM-0, E4 | as W3-RM | — | — | — |

## Binding map (where each hypothesis is forced, as far as known now)
* [SC1-4] A:W and P:NA(Q): negative diverging width gaps are sufficient; positive diverging gaps force failure of
  whole-lattice no-addition by Lemma W-conv (`lemmas/L2_width.md` §2); bounded gaps and necessity for reporting are undetermined.
* A:L-size-b ← P:SAND(Q) through junk exclusion: a sufficient budget; forced only heuristically (k̃ ≈ √n).
* A:H-size-ρ ← P:SAND(Q) through the reference count: a sufficient budget.
* A:BM-W ← P:TL(Q) through the truth-removal width [v1.3]: sufficient; not known to be forced.
* A:L-feas, A:V, A:L-gain, A:FL: as in W3-RM (`Theory_work/Wave3/W3-RM/ASSUMPTION_MAP.md`).

## Readings of the boundary-violation numerics (`numerics/RESULTS.md`; LS0 from the start mode, production score/tables)
[MP1-3] 208 runs; completed sizes n = 400 and 1600 (no n = 3200 run finished); p = 2n; classification **nominal**
(population design; the fixed-design hypotheses were not certified on the realised designs); "held" = the validated
LS0 re-implementation, started from the start mode, ends at S₀, certified. The sampler, the posterior input and the
full method's reported model were not tested. Overall 204/208.

| id | assumption | nominally outside it, the LS0 probe… | what failed on the way | flag |
|---|---|---|---|---|
| B1 | A:L-size-b (b < ½) | held in 48/48 runs at b ∈ {0.5, 0.625, 0.75} (start modes up to 241 columns at √n = 40) | sandwich in 3/6, 2/6 runs (b = 0.625, 0.75, n = 1600); a path-level no-addition margin > 0 in 1/6, 1/6, 4/6; up to 4 non-deletion moves per run against a cap slack of 15 | `improvable` (b ≥ ½ observed fine at these n; the protecting margin is the cap slack) |
| B2 | A:W | held in 48/48 | whole-lattice NA truly violated at a probed lattice set in 6/6 runs at b = 0.5, n = 1600 (3/6 at b = 0.375); never along the path | finite-n LS0 success despite observed NA violations: `improvable` as a flag, not a proof that (W) is unnecessary for asymptotic reporting [MP1-2] |
| B3 | A:V at finite n (A:BM-W not isolated) | held in 32/32 | the weak truth is missing from the start mode in 32/32; LS0 adds it | `improvable` (V); no information on the signal floor |
| B4 | A:L-gain (η) and the frontier b < β(η, A) | held in 32/32 at η = 0.05, 0.2; **failed in 4/6 at η = 1, n = 1600** (10/10 at n = 400) | η ≤ 0.2: a few outside columns in the start mode, deleted. η = 1: 505–727 outside columns in the start mode; the failing runs made 19, 24, 35, 73 swaps; LS0 stops at the move cap (slack 15) before S₀ | near the frontier `improvable`; far outside it the LS0 probe fails under the shipped cap — the leak condition is not only a proof device |

Nominal baseline cells (B1 at b ≤ 0.375) [MP1-3]: sandwich, path-level no-addition and deletion-only descent in 32/32 runs.

Conclusion level (identity < target < posterior < reported-model < delivery): **reported-model** (one data event of
probability → 1 on which every admissible output run reports S₀); rate: none claimed; scope: fixed design (F) and
Gaussian rows (R); s₀ fixed; p ≤ n^A, p ≫ n allowed; deterministic Q with |Q| ≤ n^b.

Unharvested conclusions (what the proofs give but the statement does not state):
* [SC1-2] The no-addition rate is now harvested in STATEMENT v1.3 (C3)(a): under (W),
  P(NA(𝓛)ᶜ) ≤ exp(−(𝔴⁰_n)²/8) + P(toolkit event fails) for all sufficiently large n. Under the stronger (W-δ),
  P(𝒵_nᶜ) ≤ n^{−c*}, c* = δ₀²/(32(2A + 2)). Bare (W) supplies no fixed polynomial rate through this bound. For
  [SAND(Q)] the ladder gives O(√log n · n^{−ξ}) plus 1/log n terms from the maxima (the latter can be made
  polynomial); no rate for [POST] or the common reporting event is claimed.
* the archive certificate (`returned` = S₀, `local_certified`, moves = |S̃₀ ∖ S₀| ≤ n^b) — stated in (C1);
* uniformity over the class defined by the constants and rate envelopes (n₀ depends on nothing else);
* [SC1-3] W-conv in v1.3 (C3)(b) gives an improving addition at some feasible lattice set with probability tending
  to one when 𝔴⁰_n → +∞; this is a whole-lattice obstruction, not a path-level or reported-model failure statement.

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
