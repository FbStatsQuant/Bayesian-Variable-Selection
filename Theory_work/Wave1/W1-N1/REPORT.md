# W1-N1 · REPORT to Theory HQ (FR04 / OB01 · Lemma N1 = clause M1(b) of TH01)

**Changes against the card (flagged):** none narrowing. The proved statement is *stronger* than the card in three places, all
locked before proof work: (i) any jointly measurable h with a fixed bound (|h| ≤ B_h), not only 0 ≤ h ≤ 1; (ii) the identity
holds for each measured round q separately, not only for the 4-round average; (iii) Corollary E has constant **δ₁**, so the
card's 2δ₁ follows. One charter item was not done: **Lean** (objection recorded: the ticket says Lean is out of scope unless
trivial, and no Lean toolchain is installed here).

## 1. RESULT

**PROVED-CHECKED.** N1 and Corollary E are proved under the named premises. The proof was cross-family checked (Codex Sol)
and passed the council in round 1 (Codex 9.3, Opus 8.9; all gates passing).

## 2. The statement as proved

File: `STATEMENT.md` (v2, locked; two exposition notes added after the lock, no change of claim).

> **Premises.** The data are fixed; EX-A (exact arithmetic); H-U (ideal iid uniforms within stream 9 + r); START
> (`draw_pi0` exact, Z̄₀ exact); KERNEL (the coded steps and order realise the T12 kernels: N9); CAL (𝓒 frozen on streams 0–9);
> SI (stream 9 + r is independent of streams 0–9); MEAS; the potential (uninterrupted) run; worker equivalence for v3.1's
> concurrent workers.
>
> **Claim.** For every r, every q ∈ {1,…,4} and every jointly measurable h(S; 𝓒) with a fixed bound, fixed before
> stream 10, a.s. on 𝒜 ∩ {r ≤ R′} (localised form):
> E[Ẑ_r · (1/N_e)Σ_i h(S_{rqi}) | 𝓒] = Z·π(h), and hence E[Ẑ_r H_r(h) | 𝓒] = Z·π(h).
> Here S_{rqi} is particle i's state right after the q-th measured `population_round(P, 1.0)` returns
> (`v3_engine.h:357-360`). H_r(h) = (4N_e)⁻¹ Σ_{q,i} h(S_{rqi}) is the v3.1 accumulator (`METHOD_v3.1_FINAL.md:159`); for
> h = 1{j ∈ S} it equals the coded `pip_plain[j]` exactly (`:360, 371`).
>
> **Corollary E (M1(e)).** For h ∈ [0,1]: E[W_r|H_r(h) − h(S₀)| | 𝓒] ≤ E[W_r H_r(1{S≠S₀}) | 𝓒] = δ₁ ≤ 2δ₁, with W_r = Ẑ_r/Z
> and δ₁ = 1 − π(S₀). The bound is attained by h = 1{S ≠ S₀}.

**Route.** The charter's route works, and is shorter than expected. The measured endpoints are full-round endpoints, so only
the κ ≡ m case of the terminal-round identity is needed; the within-round prefix identity is not. N1 is assembled from four
pieces:
- the locked T12 clause (i.b), "post-terminal rounds" (Lemma P);
- a code bridge (Lemma B): the coded single-stream, sequential execution satisfies T12's randomness model (R1)–(R3), with
  the measured populations and Ẑ identified line by line;
- conditioning on 𝓒 with a 𝓒-dependent bounded h (Lemma F, via T12's freezing lemma and a uniform bound on Ẑ);
- linearity over q.

## 3. Status per clause, with evidence

| Clause | Status (this ticket) | Evidence |
|---|---|---|
| M1(b) = N1 (OB01) | **PROVED under the named premises — cross-family checked, council-passed (round 1)**. It inherits START/KERNEL (N9: "PROVED (candidate), code-checked"; CHK_INHERITED "VERIFIED WITH AMENDMENT") and T12 ("PROVED-LOCKED"). | `lemmas/N1_theorem.md`, `L1_bridge.md`, `L2_post_terminal.md`, `L3_freezing.md`; reviews LC1, MP1, SW1, C1 |
| M1(e) Corollary E | **PROVED under the same premises**, constant δ₁ (implies the card's 2δ₁); same checks | `lemmas/E_corollary.md`; C1 (both seats) |
| PC1c3 premise "E[W_r ĥ_r] = π(h)" used by M1(f), (g), (i) | **Discharged islandwise** (given 𝓒, on 𝒜 ∩ {r ≤ R′}) for every bounded declared h. Those clauses keep their own statuses and remaining premises (IND-T extension for R′ > 4, GUARD-W, stacking, T03♯). | `lemmas/R_remarks.md` §5 |
| Numerical companion | The N1 identity holds on 10 designs to floating-point precision; all controls are detected; the production engine agrees within Monte Carlo error. | `numerics/RESULTS.md` |

**Numerical companion** (p ≤ 8, 10 design seeds, coded production headers with SHA-256 verified):
- **Exact enumeration** on kernels extracted from the production step functions (scripted uniforms, bisection to adjacent
  doubles; π₀ scripts validated on production `draw_pi0` with 0 failures). Tested on 3 grids (pilot-derived, {0,1},
  {0,½,1}) plus L = 0 stress cases, N = 1 on all designs and N = 2 where #Ω ≤ 130. Every basis indicator, every q, and the
  h list (joint inclusions, 1{S≠S₀}, |S|/K, normalised d, a random non-indicator h) were checked.
  - Worst N1 residual: **9.3e-15** (tolerance 1e-10).
  - The unweighted average is biased by up to 0.16 in the same cases, so the identity is not trivially satisfied.
  - Negative controls NC1 (non-invariant terminal kernel) and NC2 (no final reweighting) are detected on every design, with
    discrepancies from 3.2e-3 to 7.7e-1.
- **Production engine Monte Carlo** (`run_island` with a 2-line read-only hook; N = 2 with 2·10⁵ islands and N = 8 with
  5·10⁴ islands per design):
  - max |z| = 3.48 over 160 tests (rule |z| ≤ 4);
  - Corollary E: max z_E = 2.79;
  - the hook reproduces `pip_plain` exactly;
  - NC3 (h chosen after the run) breaks the identity, resolved on 18 of 20 runs.

## 4. Review trail

- **Statement lock SL1** (Codex Sol, high): LOCK WITH CHANGES. Items 1, 2, 4–7 applied; item 3 (Lean) is an objection.
  STATEMENT v2 locked. `reviews/SL1_*`.
- **Lemma check LC1** (Codex Sol, high): L1 GAP (scope of the record); L2, L3 and E verified with amendments; N1 verified;
  no counterexample. All 6 issues fixed (statistical-record convention, localisation, RESULTS.md). `reviews/LC1_*`.
  Numerical falsification of each lemma: `numerics/RESULTS.md` §1–§5.
- **Mid-point MP1** (fresh Codex Sol, statement and proof files only): **CONTINUE**, no blocking issues; one wording note
  applied. `reviews/MP1_*`.
- **Exhaustive sweep SW1** (Codex Sol, high): **0 CRITICAL, 5 MAJOR, 11 MINOR.** All accepted and fixed; the 5 MAJOR items
  were all in the numerical package, and the whole companion was regenerated as v2. The reviewer's verdict: "N1 and
  Corollary E are established." `reviews/SW1_*`.
- **Council round 1:** Codex gpt-6.1-sol (high) **9.3/10** and Claude Opus 5.5 (high) **8.9/10**; G1–G6 PASS for both; no
  blocking issues; **passed**. Their non-blocking exposition items were applied afterwards. `reviews/C1_*`.
- Models used: Codex gpt-6.1-sol only, for cross-family work (6 calls); Claude Opus 5.5, once, as the council seat. No Astra
  or Fable calls.

## 5. Open items and recommended next step

1. **Lean (FR04 "Done when").** Not supplied. HQ should either waive it or open a registrar task: T12Core `unbiased_of_step`
   with `hstep` for multinomial resampling plus an invariant kernel, followed by the post-terminal step. The ticket is
   **not** Lean-certified.
2. **Inherited premises are not discharged here:**
   - N9 START/KERNEL remain PROVED (candidate).
   - EX-A and H-U are idealisations (2⁻⁵³ grid, floating point).
   - The GUARD-W audit (delivered record = potential record) is open.
   - The IND-T extension (streams 10..9+R′ independent of each other) is needed by the pooled clauses for R′ > 4.
   - Worker equivalence for v3.1 concurrency is open.
   - The general-h accumulator is spec-only in the frozen core; only the marginal plain PIP is coded.
3. **Card update (HQ / registrar):**
   - TH01.b: "N1: PROOF SKETCH" → the status of §3 above.
   - TH01.e: carry the constant as "δ₁ (hence the printed 2δ₁)".
   - The "PC1c3 … 'E[W_r ĥ_r] = π(h) is still a premise'" note → "premise discharged islandwise by W1-N1".
   - Keep the scope sentence: p ≤ 8 inputs take the exact branch in the full method, so the numerical companion tests the
     SMC component only.
4. **Recommended next step:** binding goal §13.1 no longer needs the marginal-PIP fallback. Next, re-run the checks of
   M1(f), (g) and (i) with N1 as a proved input, and put the IND-T extension audit (R′ > 4) on the path to clause (i).

## 6. Files produced (all under `Theory_work/Wave1/W1-N1/`)

- `STATEMENT.md` (v2, locked), `PLAN.md` (v2), `LOG.md`, `REPORT.md`.
- `lemmas/`: `L1_bridge.md` (Lemma B, code bridge), `L2_post_terminal.md` (Lemma P = T12 (i.b), re-derived),
  `L3_freezing.md` (Lemma F), `N1_theorem.md`, `E_corollary.md`, `R_remarks.md`.
- `numerics/`:
  - harness: `cpp/n1_harness.cpp`, `cpp/n1_harness_v2.exe`, `cpp/instr/v3_engine.h`, `cpp/instr.diff`,
    `cpp/production_headers.sha256`;
  - drivers: `n1_exact.py`, `n1_mc.py`, `make_results.py`;
  - `BUILD.md`, `RESULTS.md`, `json/d0…d9/` (archived outputs), `json/MANIFEST.sha256`, `exact_summary.txt`,
    `mc_summary.txt`.
- `reviews/`: `SL1_statement_lock_codex.md` + `SL1_disposition.md`; `LC1_lemma_check_codex.md` + `LC1_disposition.md`;
  `MP1_midpoint_codex.md` + `MP1_disposition.md`; `SW1_sweep_codex.md` + `SW1_disposition.md`; `C1_council_codex.md`,
  `C1_council_opus.md`, `C1_disposition.md`.
- Nothing outside the folder was modified, and no git state was changed. The large kernel binaries and raw Monte Carlo
  files are in the session scratchpad only; their hashes are in the manifest.
