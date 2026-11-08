# W1-N3 — REPORT to Theory HQ (ticket FR05 / OB03, the e4 tie-DP invariant N3)

> **Flag (statement vs card).** The card asks that "the DP returns the prescribed smallest-size, lexicographically
> smallest start-mode maximiser". The DP **as coded** (`start_mode`, frozen v2.2.1 `cpp/v3_start.h:178-240`) does so
> **only when the number N of smallest-size maximisers is ≤ cap (10⁶)**: when there are more ties than the cap it can
> return a different maximiser, and the spec's truncation fallback ("deterministic tie-aware DP", METHOD #8/e4) has **no
> code**. The locked target is therefore the precise true version plus a counterexample (abstract tables) and a proved
> reference fallback. **Premise e4 for an integrated LS0 centre is not discharged**: LS0 and the fallback are not in
> production code, and the deviation is not shown on data or LH (it is not a counterexample to T38-b1-LH).

## 1. RESULT
**PROVED-CHECKED** — for the locked target `STATEMENT.md` v1.3 (Theorem N3-code (a)–(e) + supplementary (f)); N3 as an
unconditional property of the frozen code is **false** (counterexample, clause (d)); e4 for integrated LS0 stays OPEN.

## 2. Statement as proved
`STATEMENT.md` v1.3 (locked; v1.1 at lock, v1.2/v1.3 wording and hypothesis-precision fixes only). In short, for any
ordered block partition (block order unrelated to index order), cap K, real tables λ, ρ:
- (a) `res.lg0` = max π₀-objective and `res.S` is always a smallest-size maximiser of π₀, truncated or not;
- (b) the enumeration visits exactly the ≺_DFS-first min(N, cap) smallest-size maximisers; `ties` = min(N, cap),
  `truncated` = [N ≥ cap] (true also at N = cap);
- (c) **N ≤ cap ⇒ `res.S` = S\*** (the prescribed choice); in particular `truncated == false` ⇒ correct; with cap 10⁶ always
  when max_{k≤K} C(p,k) ≤ 10⁶ (e.g. p ≤ 22);
- (d) N > cap ⇒ `res.S` = lex-min of the DFS-first cap maximisers, which can differ from S\*; explicit family D_m for every
  cap; for cap 10⁶: p = 44, K = 22, code returns {0,2,…,38,41,42}, S\* = {0,2,…,38,40,43};
- (e) binary64 (round-to-nearest-even, finite intermediates): value, membership and smallest size hold for the code's
  own evaluation `log_gamma0`, but the lex choice can fail **even without truncation** (two explicit examples) — so a
  truncation-triggered fallback cannot by itself give the prescribed choice in native doubles;
- (f) reference algorithm TDP (greedy inclusion + constrained max-plus feasibility DP) returns S\* for every instance in
  exact arithmetic without enumerating ties, O(p · Σ_b (2^{|C_b|} + (K+1)²)) operations.
Hypotheses: (H1) encoding of `Start` (+ inverse maps for (e)), (H2) EX-A for `start_mode`'s arithmetic, (H2-FP) for (e),
(H3) cap ≥ 1, (H4) C++ execution limits (added after the sweep).
Change vs card and reason: see the flag above (the code deviates from the spec; the true version is conditional).

## 3. Status per clause (evidence)
| clause | status | proof | checks |
|---|---|---|---|
| reduction, lex transport (L1) | PROVED; XF-checked | `lemmas/L1_reduction.md` | R02 GAP → fixed → R03 CORRECT (Sol) |
| block maxima (L2) | PROVED; XF-checked | `lemmas/L2_block_maxima.md` | R02 CORRECT (Sol) |
| DP table, size selection (L3, L4) | PROVED; XF-checked | `lemmas/L3_L4_dp_and_size.md` | R02 CORRECT-WITH-MINOR-FIXES (Sol) |
| enumeration, key lemma (L5) | PROVED; XF-checked | `lemmas/L5_enumeration.md` | R02 WRONG in (A) wording → fixed → R03 CORRECT (Sol) |
| (a)–(d), deviation family (L6) | PROVED; XF-checked | `lemmas/L6_assembly_and_deviation.md` | R05 CORRECT (Sol) |
| (e) floating point (L-FP) | PROVED; XF-checked | `lemmas/LFP_floating_point.md` | R05 CORRECT-WITH-MINOR-FIXES (Sol) |
| (f) TDP (L7) | PROVED; XF-checked (reference algorithm, not in code) | `lemmas/L7_tie_aware_dp.md` | R05 CORRECT (Sol) |
| whole package | council passed round 1 | `PROOF.md` | R07: Sol 9.3, Opus 8.6, all 6 gates PASS |
Numerical companion (`numerics/README.md`), all through the frozen header compiled with SSE2/no-FMA: exhaustive p ≤ 3
(19,950 instances per seed) + constructed ties, allocation/cross-size/within-block code≠lex ties, K binding, cap edges
N−1/N/N+1, random p ≤ 12 — **35,551 / 35,585 integer-table instances (seeds 20261108 / 7), 0 failures of (a)–(d), (f)**;
DATA mode with the coded scorer and real prior (n ∈ {2,3,4,6,10,20}, duplicated columns), 400/seed, 0 mismatches;
FP stress 3,000/seed, 0 failures of (e); lemma probes 5,572, 0 failures; D_m m = 0..12 50/50; p = 44 default-cap
counterexample confirmed; n = 2 (ENG10): routine 36/36 correct (S\* = {0} at p = 1, ∅ for p ≥ 2), and the public
preprocessing rejects n = 2 (`invalid_input`, "n < 3"). Side observation: at n = 2 the mathematically equal singleton
tables differ in the last bit in 10/36 runs (scorer rounding) — relevant to e3's "p-fold exact tie" sentence for the
exact branch, not to `start_mode`.

## 4. Review trail
- Statement lock R01 (Sol): LOCK-AFTER-FIXES; 5 fixes applied; locked v1.1.
- Lemma checks: R02 batch 1 (L1 GAP, L2 CORRECT, L3/L4 minor, L5 WRONG in (A) — missing final-prefix condition, valid
  counterexample to the lemma's wording, not to the code); R03 re-check L1, L5: both CORRECT, no fixes (attempt 2 each).
  R05 batch 2: L6 CORRECT, L-FP minor (monotone-rounding wording), L7 CORRECT. Falsification for every lemma in `numerics/`.
- Mid-point R04 (fresh Sol, statement + lemmas only): **CONTINUE**; 3 points applied.
- Exhaustive sweep R06 (Sol): 12 flaws — 0 critical, 0 major, 8 minor, 4 nit — all fixed (STATEMENT v1.2, (H4) added).
- Council R07 round 1: **Sol 9.3, Opus 8.6, all gates PASS** → passed; their minor points then applied (v1.3, wording).
- Models used: Codex gpt-6.1-sol (all cross-family reviews), Claude Opus 5.5 (council seat). No Astra, no Fable, no
  helper subagents.

## 5. Open items and recommended next step
1. **e4 for the integrated LS0 centre remains OPEN** (needs LS0 in the production core, N2(c)/ENG02 replay).
2. **Engineering (ENG10):** implement the e4 fallback. Recommended: replace the post-truncation branch by TDP (L7), or
   simply run TDP always (cost O(p·Σ_b(2^{|C_b|}+(K+1)²)), small). Caveat (L-FP): in native doubles neither the current
   enumeration nor a truncation-triggered fallback guarantees the rounded lexicographic choice; if the lex rule must hold
   in floating point, the implementation needs its own rounded-feasibility argument (TDP with Φ evaluated by the same
   fold as `log_gamma0` is the natural candidate, not proved here). Under EX-A everything above holds.
3. For M5 (b1-LH): what LS-score needs from the centre should be checked — (a) already gives "a smallest-size maximiser
   of π₀" unconditionally; if LS-score only needs the centre to be *a* start-mode maximiser (or the maximiser is a.s.
   unique on LH, as the O-LS0 runs observed in 2,400/2,400 fits), the lex tie rule and the truncation issue are moot
   for (b1-LH). Recommended: one short HQ check of the LS-score proof for which property of the centre it uses; and,
   optionally, a lemma that exact ties of γ₀ have probability 0 under G with full-column-rank X (not attempted here).
4. Whether ≥ 10⁶ exact smallest-size ties can arise from data (duplicated columns are the known mechanism) is undecided.

## 6. Files produced (all in `Theory_work/Wave1/W1-N3/`)
`STATEMENT.md`, `PLAN.md`, `PROOF.md`, `LOG.md`, `REPORT.md`;
`lemmas/`: `L1_reduction.md`, `L2_block_maxima.md`, `L3_L4_dp_and_size.md`, `L5_enumeration.md`,
`L6_assembly_and_deviation.md`, `LFP_floating_point.md`, `L7_tie_aware_dp.md`;
`numerics/`: `README.md`, `sm_harness.cpp`, `build.sh`, `sm_harness.exe`, `n3lib.py`, `tdp.py`, `run_checks.py`,
`lemma_probes.py`, `check_union_order.py`, `cex_default_cap.py`, `cex_family.py`, `fp_example.py`, `eng10_n2.py`,
`eng10_preprocess_n2.R`, `out_*.txt`;
`reviews/`: R01–R07 raw replies + dispositions (`R01_statement_lock*`, `R02_batch1_check*`, `R03_recheck_L1_L5*`,
`R04_midpoint*`, `R05_batch2_check*`, `R06_sweep*`, `R07_council1_*`), reviewer scratch folders `R03_scratch/`,
`R05_scratch/`, `R07_scratch_sol/`, `R07_scratch_opus/`.
