# R07 — Council reviewer 1 (Claude Opus 5.5), raw

Package: `Theory_work/Wave1/W1-N3/` (STATEMENT v1.2, PROOF.md, lemmas L1, L2, L3_L4, L5, L6, L7, LFP, numerics/).
Reviewed fresh. I did not read `reviews/` (other than writing this file) or `LOG.md`.

## What I checked independently

* **Code quotations.** I compared every quoted line in L2 (186–197), L3/L4 (198–213) and L5 (214–238) with the frozen
  `CODE/cpp/v3_start.h`, one line at a time, after stripping CR. All match exactly up to a uniform 2-space dedent. Line
  anchors 178 (comment), 183 (`start_mode`, default cap 1000000) and 240 (closing brace) are correct. The other code
  citations also check out: `build_tables`/`build_start` 76–151 (logprof length min(|C_b|,K)+1 at 107/113;
  `codes_by_size` increasing at 109–111; `logr[b][0] = 0` at 95; NaN for |U| > K at 86/92), `comp`/`log_gamma0` 54–69,
  `lex_less` at `v3_util.h:117-119`, `NEG_INF` at `v3_util.h:22`, `v3_score.h:18,40,63-70`, `v3_preprocess.R:106,112`,
  `v3_fit.R:123`, `README.md:15`.
* **Copies.** The v2_2 copy is byte-identical. `Scripts/SMC_BVS/{core,reference/prototype_core}` are identical
  modulo CRLF. This confirms §0.
* **Spec sources.** METHOD_v3.1_FINAL.md:150 (#8 e4 sentence) and :183 (#26) are quoted correctly. `04_theory.tex:84` (e4
  premise) and the M5 card (464–539: N3 "the only OPEN mathematical obligation", escalation criteria) agree with the
  package. `06_open_and_plan.tex:119-127` (FR05) and `02_method.tex:789, 830-838` are cited correctly.
* **Proof steps.** I re-derived L1(iii), L2, the L3 recurrence, L4, all four parts of L5 (A)–(D), the L6 assembly and the
  D_m claim (maximisers, S*, DFS prefix, returned set), L7 (constrained DP, invariant, cost) and L-FP (monotonicity of
  rn, (ii) upper bound and attainment, (iii), (iv) forward induction). I hand-traced both FP examples through the code:
  example 1 gives M[2][2] = 1000 and arg[1][1] = {code 2}, so the output is {0,2}; example 2 gives 2⁵⁴ ⊕ 2 = 2⁵⁴ by
  ties-to-even, so the output is {1}. Arithmetic constants: C(22,11) = 705,432, C(23,11) = 1,352,078, 2²⁰ = 1,048,576
  ≥ 10⁶, and D_20 has p = 44, K = 22, N = 2²¹.
* **Numerics.** I rebuilt the harness from `sm_harness.cpp` against the frozen header with the `build.sh` flags, into
  `reviews/R07_scratch_opus/`. Compiler: MinGW-Builds g++ 16.2.0, i686 target. I re-ran the scripts against the rebuilt
  binary with `python -I -B`. Results:
  * `cex_default_cap.py`: frozen output {0,2,…,38,41,42}, ties = 10⁶, truncated = 1; TDP gives S* = {0,…,38,40,43}.
  * `fp_example.py`: output identical to `out_fp_example.txt`.
  * `cex_family.py`: identical to `out_cex_family.txt`.
  * `lemma_probes.py 11`: identical to `out_lemma_probes_seed11.txt` (1,500 / 2,521 / 1,551 probes, 0 failures).
  * `run_checks.py 7`: byte-identical to `out_run_checks_seed7.txt`.

## Gates

**G1 correctness of every step — PASS.**
I found no wrong step.
* L5(A) includes the final-prefix condition b = J (the example shows why it is needed). The "⇒" backward induction
  correctly splits a chained equality into two equalities.
* In L5(B), the invariant (I), the no-dead-ends argument and the injectivity of leaves are sound.
* L5(C) correctly identifies the child order (popcount(c), c) with the flattening of κ.
* L5(D) handles N = cap correctly.
* In L7, the case i ∉ S* uses min(S Δ S*) = i ∈ S and L1(iii) correctly.
* In L-FP, rounding monotonicity is proved, not assumed. The fold F_J equals `comp` because both sum in increasing block
  order, and the empty block is the identity on both sides (also for ±0).

One misdescription of the code, which does not affect the logic, is listed under issue 2.

**G2 hypotheses used = hypotheses stated — PASS (bookkeeping blemish).**
* Each lemma uses only (H1)–(H4) or (H2-FP).
* The inverse-map clause (blk/pos) is used only in L1(ii) and L-FP, as STATEMENT says.
* (H4) is used only for execution.
* The PROOF.md index does not list (H4) in its hypotheses column (issue 1).

**G3 no hidden assumptions — PASS.**
* NEG_INF semantics are stated in (H2).
* Unread NaN entries are handled (|U| > K is never read; verified at code lines 107–111, 191–192).
* `kbest = −1` cannot occur because L3 finiteness requires K ≤ p.
* (H2-FP) covers finiteness of every `comp` prefix sum.
* The harness forces SSE2 binary64 on an i686 target, where x87 extended precision would otherwise break (H2-FP).
* Integer/`long` widths are in (H4). The production cap of 10⁶ fits a 32-bit `long`.

**G4 status of cited sources; no over-claiming — PASS.**
* External items are labelled at their real status:
  * D9 / the METHOD #26 sketch is "seat-derived, unchecked" / DESIGN-ASSERTED.
  * D0 is used only as a definition.
  * The deviation is stated to be on abstract tables only. The package explicitly says it is not an LH or data
    counterexample and does not discharge e4 for an integrated LS0.
* Lemma status lines cite cross-family checks in `reviews/`, which I was told not to read, so I did not verify those
  labels.
* Version labels drift (issue 1).

**G5 constants and bounds tracked — PASS.**
* Cap semantics are exact: ties = min(N, cap) and truncated = [N ≥ cap], including at N = cap.
* The p ≤ 22 bound is correct, and the claim "exact range of this sufficient condition" is correct.
* D_m sizes (p = 2m+4, K = m+2, N = 2^{m+1}, cap ≤ 2^m) are correct, as is the m = 20 instance.
* The TDP cost O(p·Σ_b(2^{|C_b|} + (K+1)²)) is justified: one O(1) bitmask test per code, and a convolution of at most
  J(K+1)² per evaluation, over p+1 evaluations.
* Optional sharpening: N ≤ C(p, k*) ≤ max_{k≤K} C(p,k), so (c) also holds for p > 22 when K is small (issue 6).

**G6 fidelity to the method as coded — PASS (minor gaps).**
* The abstract instance is exactly what `start_mode` reads: K, logprior, J, blocks, logr, logprof sizes and
  codes_by_size. (e) adds blk/pos.
* The quotations are exact.
* The deviations from the spec are reported clearly:
  * the e4 truncation fallback is not implemented;
  * the conditional is necessary;
  * the floating-point lexicographic failure happens even without truncation, so a truncation-triggered fallback
    cannot repair it.
* Small gaps are listed as issues 2 and 4.

## Overall score: **8.6 / 10**

This is a publication-quality, code-anchored proof of the stated result. The decomposition is clean. The key lemma (L5)
is careful about the final-prefix condition, DFS order and cap semantics. The deviation family is explicit and checked
through the frozen binary. The floating-point clause is honest and proved. The scope statement is calibrated: it does
not claim e4 for the integrated emitted centre. All gates pass. The points below are presentation, bookkeeping and
small fidelity items, not gaps in the mathematics.

## Issues that cost points (location → fix)

1. **Version and hypothesis bookkeeping (−0.4).**
   * `PROOF.md:3` says "Target: STATEMENT.md v1.1 (locked)", but STATEMENT is LOCKED v1.2.
   * `lemmas/L1_reduction.md:5`, `L5_enumeration.md:34` and `L6_assembly_and_deviation.md:6` cite v1.1. L5 also cites
     v1.2 at line 38.
   * The PROOF.md table lists "(H1)–(H3)" for L5 and for (a)–(d), and "(H1) incl. inverse maps, (H2-FP), (H3)" for (e),
     all without (H4). STATEMENT §3 and L-FP state (H4).

   Fix: change every reference to v1.2 and add "(H4) for execution" to the PROOF.md hypotheses column.

2. **L5(B) misdescribes line 234 (−0.2).** L5(B), "Leaves" paragraph: "the reset at line 234 happens only after the loop
   of that level is finished". In the code, `choice[b - 1] = 0;` is inside the j-loop and runs after each j's c-loop. The
   argument does not need the claim: line 233 assigns `choice[b-1] = c` immediately before every recursive call, which
   is enough.

   Fix: "line 234 runs only after the c-loop for a given j, never between the assignment at 233 and the call it
   precedes".

3. **The (d) parenthetical is ambiguous (−0.2).** STATEMENT §3(d): "(the frozen code does so for every cap and instance
   satisfying (H4))". Read literally, this says the frozen code returns a set ≠ S* on every instance.

   Fix, in L6 wording: "(the frozen code returns that set on D_m for every cap ≤ 2^m for which (H4) holds for
   (D_m, cap))".

4. **Fidelity context for start-mode callers and the O-LS0 export (−0.2).**
   * §0 correctly says `start_mode` is the only start-mode routine in the repository.
   * L6 correctly says no production caller exists.
   * Two facts are missing:
     * The reference prototype does call it, with the default cap: `Scripts/SMC_BVS/reference/prototype_core/cpp/v3_core.cpp:272-274, 710`, `v3_setup.R:59`.
     * The only empirical start-mode computations in the study (O-LS0, 2,400 fits) went through `cpp_ls0_start_mode`
       (`NBH/branch_snapshots/O-LS0/REPORT.md:102`). That was a test-only export, not in the repo
       (`CODE/README.md:15`: "Test-only exports are appended … to testing copies"). Whether it wraps `start_mode` with
       cap 10⁶ is unverified. O-LS0 also reports that S̃₀ was unique in all 2,400 fits, so N = 1 there.

   Fix: add one sentence to §0 and to L6 "Note on the specification". It should name both callers, mark the O-LS0
   wrapper as out-of-repo and unverified, and cite the N = 1 evidence. This places the theorem's object relative to
   the only empirical use.

5. **§1 lex-transfer claim broader than its lemma (−0.1).** STATEMENT §1 says lexicographic order on sorted internal
   lists *equals* lexicographic order on sorted original lists, without a size restriction. L1(iv) proves it only for
   equal-size sets. The general statement is also true and trivial: a strictly increasing φ preserves elementwise
   comparisons and the proper-prefix rule.

   Fix: either restrict §1 to equal sizes, which is all that is used, or add the one-line general argument to L1(iv).

6. **Optional sharpening of (c) and the data-realisability remark (−0.1, not a correctness issue).**
   * (c) could also state N ≤ max_{k≤K} C(p,k).
   * The §0 / L6 remark "whether ≥ 10⁶ exact smallest-size ties can arise from data is not decided here" could name
     the known mechanism: under EX-A, exactly duplicated columns give exactly symmetric table ties. Duplicates are kept
     (METHOD #25) and noted as D9 in `NBH/branch_snapshots/MEET-THM/evidence/W1_PC2/VERDICTS.md:41`.
   * The remark could also say what the deviation would additionally need: a within-block tie whose code order differs
     from its lex order (as with {a,d} vs {b,c}), or an allocation tie that crosses block order. Pure singleton-pair
     ties inside blocks put S* first in DFS order, so they cannot cause the deviation.

   This tells HQ precisely what remains open for data tables.

No issue found under G1 that changes a conclusion. No numerics claim failed to reproduce.

Scratch (rebuilt harness, copies of scripts, rerun outputs): `Theory_work/Wave1/W1-N3/reviews/R07_scratch_opus/`.
