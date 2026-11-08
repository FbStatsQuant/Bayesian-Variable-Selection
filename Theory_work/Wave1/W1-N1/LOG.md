# W1-N1 · LOG

- 2026-11-08 · Read PROTOCOL.md, agent brief, FR04 card, TH01 card, M1 charter, N9 REPORT/PROOF §2–5, method section
  (02_method.tex), production engine `CODE/cpp/v3_engine.h` (full), `v3_calib.h:25-98`, `v3_core.cpp:460-485`, T12
  STATEMENT and PROOF_v6 (lemmas, (i.b), freezing).
- 2026-11-08 · Finding: the locked T12 already proves, for fixed c, the post-terminal identity (i.b) for "any fixed
  finite sequence of rounds at φ = 1" (PROOF_v6.tex:131), which covers the measured-round populations. N1 therefore
  reduces to (1) a code bridge (coded island = T12's I(c), with endpoints = populations after measured rounds),
  (2) conditioning on 𝓒 for 𝓒-measurable h, (3) linearity over q. The within-round prefix identity (i.c) is not needed
  for endpoint (full-round) records.
- 2026-11-08 · Finding: Corollary E holds with δ₁ (not only 2δ₁) for the plain average; consistent with TH412 (a).
- 2026-11-08 · Toolchain: Python 3.13 + numpy 2.3; Rtools45 g++ (64-bit); R lacks Rcpp (not installed; not installing).
  Production headers are Rcpp-free → a standalone C++ harness can drive the production Engine.
- 2026-11-08 · STATEMENT v1 and PLAN v1 written; sending to statement-lock review.
- 2026-11-08 · Numerics built: `numerics/cpp/n1_harness.cpp` compiles against the unmodified production headers (Rcpp
  stubs only for `runtime_ptr` and `NA_REAL`, both unused); instrumented engine copy differs by 2 read-only hook lines
  (`numerics/cpp/instr.diff`). Exact (`n1_exact.py`) and MC (`n1_mc.py`) drivers tested on design 7: exact residual ≤ 1.1e-15;
  NC1/NC2 fail at ~1e-2; MC adaptive-h control 0.482 vs 0.421 (se 0.0012).
- 2026-11-08 · SL1 statement-lock review (Codex gpt-6.1-sol high): LOCK WITH CHANGES. Items 1, 2, 4–7 accepted and applied
  (STATEMENT v2, PLAN v2); item 3 (Lean) objection recorded (HQ: Lean out of scope unless trivial; no toolchain).
  Disposition `reviews/SL1_disposition.md`. **STATEMENT v2 LOCKED.**
- 2026-11-08 · Proof files v1 written: `lemmas/L1_bridge.md` (Lemma B, code bridge), `L2_post_terminal.md` (Lemma P = T12 (i.b),
  re-derived), `L3_freezing.md` (Lemma F), `N1_theorem.md`, `E_corollary.md` (bound δ₁ ≤ 2δ₁). Citations re-verified by grep.
- 2026-11-08 · Exact companion restructured (vector DP for |Ω| > 130; N = 2 only for |Ω| ≤ 130); added basis indicators, per-q
  residuals, L = 0 stress cases. Full runs (exact, 10 designs; MC on production engine, N ∈ {2, 8}) launched.
- 2026-11-08 · LC1 lemma check sent to Codex gpt-6.1-sol (high), fresh task.
- 2026-11-08 · Numerics complete (10 designs). Exact: worst N1 residual 9.3e-15 (all h, all basis indicators, every q, N = 1
  everywhere, N = 2 for |Ω| ≤ 130, 3 grids + L = 0 stress); controls NC1/NC2 3.2e-3 … 7.7e-1. MC (production engine, N = 2:
  2e5 islands, N = 8: 5e4 islands per design): max |z| 3.48, max z_E 2.79, hook = pip_plain exactly; NC3 adaptive h biased
  on 18/20 runs. `numerics/RESULTS.md`.
- 2026-11-08 · LC1 (Codex Sol high): L1 GAP (record scope), others verified (with amendments); no counterexample. All 6
  issues accepted and fixed (L1 v2, L2 v2, L3 v2, N1 v2, E v2; RESULTS.md). `reviews/LC1_disposition.md`.
  Added `lemmas/R_remarks.md`. Next: independent mid-point review (STATEMENT + proof files only).
- 2026-11-08 · MP1 independent mid-point review (Codex Sol high, statement + proof files only): **CONTINUE**, no blocking
  issues; one wording note applied (EX-S within-stream vs SI cross-stream, post-lock exposition note). `reviews/MP1_disposition.md`.
- 2026-11-08 · SW1 exhaustive sweep sent (Codex Sol high, fresh).
- 2026-11-08 · SW1 exhaustive sweep (Codex Sol high): 0 CRITICAL, 5 MAJOR, 11 MINOR; "N1 and Corollary E are established as
  conditional mathematical statements under the locked statement's named idealised premises"; all MAJOR items concern the
  numerical package. All 16 accepted (`reviews/SW1_disposition.md`): harness v2 (black-box Gibbs bisection, π₀ scripts
  validated on production draw_pi0, bisection to adjacent doubles, kind-4 design fixed), exact row sums via transposed DP,
  NC3 N1-centred, pilot-derived grid naming, durable archive + manifest + BUILD.md, assertions. Full numerics rerun (v2) launched.
- 2026-11-08 · Numerics v2 complete (first background job hit its 30-min limit during MC; MC resumed and finished).
  RESULTS.md v2 regenerated from `numerics/json/` with assertions: worst N1 residual 9.3e-15; controls 3.2e-3 … 7.7e-1;
  max |z| 3.48; max z_E 2.79; hook diff 0; π₀ scripts 0 failures; Gibbs bisection = RB o_j exactly; brackets ≤ 1.1e-16;
  NC3 N1-centred resolved on 18/20. Lemma numeric paragraphs updated. Next: council round 1.
- 2026-11-08 · Council round 1: Codex gpt-6.1-sol high 9.3/10, Claude Opus 5.5 high 8.9/10; G1–G6 PASS for both; no
  blocking issues → **council PASSED (round 1)**. Non-blocking items applied (exposition only): `reviews/C1_disposition.md`.
  Final status string written into lemma headers. REPORT.md written.
