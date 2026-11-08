# W1-N1 · PLAN (v2, 2026-11-08; changes after statement lock SL1 marked [SL1])

## Route

The charter route ("finite-state resample–move recursion; the state before each measured record is Zπ-weighted because
the prefix of a uniformly random order is state-independent", `THEOREM_LIST_FINAL.md:119`) is already carried out, for a
fixed frozen parameter c, by the locked T12 proof (status PROVED-LOCKED on the card):
- T12 (i.a): E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f) at every bridge stage t (resample–move recursion, Lemmas bridge/res/round/prefix);
- T12 (i.b): after stage T, for any fixed finite sequence of rounds at φ = 1, E_c[Ẑ q̂(f)] = Zπ(f) for the population after
  any of them (`Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:131`); its proof says it "covers the L′ rounds
  and the M measured rounds of I(c)";
- T12 freezing lemma (`PROOF_v6.tex:157-168`): conditioning on 𝓒.

The measured endpoints are *full-round* endpoints (state after `population_round` returns), so N1 needs the κ ≡ m case only
(T12 (i.b)), not the within-round prefix (i.c) that the RB record needs. What is missing for N1 and is done here:

1. **Lemma B (code bridge).** The coded island `run_island_s` on stream 9 + r with the frozen 𝓒 realises T12's frozen run
   I(c) with N = N_e, M = 4, L′ = L, flag unset, and the endpoints S_{rqi} are T12's populations after measured round q.
   In particular T12's randomness model (R1)–(R3) holds for the coded single-stream sequential execution under H-U
   (stopping-time / strong Markov argument for an iid uniform sequence; N9 rows 1–5 for kernels and order; resampling
   sampler `v3_engine.h:235-260`). Also: grid endpoints (0 and exactly 1), Ẑ_r formula, no round at stage 0.
2. **Lemma P (post-terminal identity, fixed c).** T12 (i.b) restated for the four measured populations, with a
   self-contained proof (the 5-line induction) so the reviewer can check it without the T12 packet.
3. **Lemma F (conditioning on 𝓒 with 𝓒-measurable h).** Freezing lemma applied to g(c, u) = Ẑ(Φ(c,u))·H(Φ(c,u); h_c)·1_𝒜(c),
   bounded because Ẑ ∈ [Z₀e^{min d}, Z₀e^{max d}] and h is bounded on finite Ω; for r > 4 uses the per-island IND-T premise.
4. **Theorem N1** = 1 + 2 + 3 + linearity over q.
5. **Corollary E** (M1(e)): |h(S) − h(S₀)| ≤ 1{S ≠ S₀} for h ∈ [0,1] ⇒ |H_r(h) − h(S₀)| ≤ H_r(1{S ≠ S₀}); apply N1.
6. **Remarks / sharpness.** (a) adaptive h breaks it (explicit small counterexample, numerically); (b) measuring before the
   final reweighting or with a non-invariant kernel breaks it (negative controls); (c) conditioning on completion need not preserve it
   (CEX-guard, cited); conditioning on a favourable final diagnostic breaks it (T12 (iv.e), cited).

Files: `lemmas/L1_bridge.md`, `lemmas/L2_post_terminal.md`, `lemmas/L3_freezing.md`, `lemmas/N1_theorem.md`,
`lemmas/E_corollary.md`, `lemmas/R_remarks.md`.

## Numerical companion (`numerics/`) [SL1 item 4]

- **NX (exact, floating-point enumeration).** `numerics/cpp/n1_harness.exe export` (C++, compiled against the production
  headers `CODE/cpp/*.h`, unmodified; SHA-256 in `numerics/production_headers.sha256`) builds 10 seeded designs (p from 4
  to 8, n from 6 to 30; iid, equicorrelated, AR(1), two-block and exact-duplicate-column designs): production Data, blocks,
  tables, start sampler, neighbour graph; production scores for every S ∈ Ω; the production π₀-sampler law (product of
  its categorical interval widths); a production adaptive pilot (stream 0) and production `build_grid` on V = top-20p by
  lg0 ∪ top-20p by lg1 ∪ {∅} ranked over Ω (replica of the coded V, which ranks scored models); and the kernel matrix of
  each production elementary step (scripted uniforms by purpose, categorical choices at interval midpoints, acceptance
  thresholds by bisection on the production accept test, to one ulp). `numerics/n1_exact.py` forms the round kernel
  exactly (multiset DP over all orders) and propagates the **evidence-weighted** population measure
  μ_t(x) = E[Ẑ_t/Z ; population = x] (N = 1: vector; N = 2: ordered-pair matrix, mixture-of-products recursion for
  multinomial resampling), then L burn-in and 4 measured rounds, recording E[W η_q(h)] **separately for each q**. h list:
  **every basis indicator 1{S = s}, s ∈ Ω** (so N1-q is checked coordinatewise), joint inclusions on two graph edges and
  on the true pair, a marginal, 1{S ≠ S₀}, |S|/K, normalised d, and a seeded random h ∈ [0,1]^Ω. Grids: production,
  {0,1}, {0,½,1}. Tolerance: |residual| ≤ 1e-10 (floating-point enumeration, not certified real arithmetic).
  Corollary E: its equality part E[W H(1{S≠S₀})] = δ₁ is checked exactly; the inequality E[W|H(h) − h(S₀)|] ≤ δ₁ needs the
  joint law over 4 rounds and is checked by Monte Carlo (NMC).
- **NMC (production engine).** `n1_harness.exe mc` runs the production `run_island` (header copy with two read-only hook
  lines, `numerics/cpp/instr.diff`) on independent streams, production grid; the hook is validated against the production
  `pip_plain` output for marginal indicators. Budget: the 10 design seeds (≤ 20, PROTOCOL), N ∈ {2, 8}, 2·10⁵ (N = 2) and
  5·10⁴ (N = 8) island replicates per design. Rule: |z| ≤ 4 for every h (with ~20 h × 20 runs, a |z| > 4 is a flag).
- **Negative controls (chosen to be non-degenerate; discrepancy reported per design, must exceed 1e-6 exactly or 6 SE):**
  NC1 burn-in + measured rounds run with the φ = ½ round kernel (not π-invariant whenever d is non-constant on Ω);
  NC2 bridge stopped at φ_{T−1} (no final reweighting), then the same L + 4 rounds **at φ = 1** (detects a target error
  only partly attenuated by the invariant rounds); NC3 adaptive h = indicator of the island's most frequent endpoint
  (chosen after the run). Designs with constant d are reported as degenerate for NC1/NC2.

## Lean [SL1 item 3: objection recorded]

The charter item "the Lean file to the registrar" (T12Core `unbiased_of_step` with `hstep`) is not attempted: the HQ
ticket says Lean is "optional and out of scope unless trivial", and no Lean toolchain is installed here. Left as an open
item for the registrar (REPORT §5).

## Review pipeline (PROTOCOL.md)

Statement lock (Codex gpt-6.1-sol) → per-lemma falsification + XF check → mid-point independent review after Lemma B +
Theorem N1 → exhaustive sweep → council (gpt-6.1-sol high + Claude Opus 5.5 high).
