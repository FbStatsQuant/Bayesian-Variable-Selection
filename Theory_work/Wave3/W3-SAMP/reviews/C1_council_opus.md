# W3-SAMP · Council C1 — Claude seat (Opus 5.5, effort high)

Reviewer brief: break the result. Read: STATEMENT.md (v3), all eight lemma files, ASSUMPTION_MAP.md, numerics/README.md
(and the scripts and RESULTS it indexes), reviews/CITECHECK.txt, citecheck.py; PROGRAM.md item 4, PROTOCOL.md; imports T12
(STATEMENT, STATUS), W1-N1 (STATEMENT, REPORT, L1_bridge, L2_post_terminal, L3_freezing), W3-POST STATEMENT. I did not read
LOG.md, REPORT.md, CHECKPOINT.md or any reviews/*.md.

## What I checked independently

**Code of record.** `git diff --stat 4676af6 HEAD -- Scripts/SMC_BVS/core` is empty and the folder is clean. I diffed main against
the v2.2.1 core myself: `v3_engine.h` differs only by the plain-PIP lines and the `phase` argument of `local_search`; `v3_ledger.h`
differs only by `PH_LS0` and the registry hook; `v3_score.h`, `v3_util.h`, `v3_blocks.h` and `v3_calib.h` are identical;
`v3_start.h` first differs at v2.2.1 line 181, after `draw_pi0`; `v3_runtime.h` differs only in `local_event`. The CC header is
accurate. I re-read every code fact the proofs use against the source:
- `run_island_s` resamples at every bridge stage and never at φ = 1. So the burn-in and measured particles follow separate
  Markov chains, which TR's per-particle argument and MR-b's s = L + q − 1 indexing need.
- The incremental weight is computed on the population after the previous round, before resampling (`:317-327`). This is
  C Step 4's recursion (1).
- `logZ` is initialised to log m(∅) + log Z̄₀ (`:299`).
- `step_gibbs` adds o_j at the current state before the Gibbs uniform, and o_j = 0 when j ∉ S and |S| = K (`:116-129`).
- Each round contains exactly one `I` label (`:211`), and `step_indep` scores the proposal (emit = true) before its accept
  uniform. Every accepted state passes through `eval`.
- `RngSource::u` ignores the purpose string and reads a single stream.
- `draw_pi0` reads at most 1 + 2J uniforms.
- The cache is local to `cpp_final_run`. The only `emit = false` call is the final local search's centre, which is `led.hpmS`.
  Tables and inherited models go through `offer_stores` directly.
- `hpm_better` is a strict total order. `logprior[k] = log w(k) − log W_K`, so Σ_Ω e^F = Z, as LT-f's observable condition needs.
- The reported fields: `pip_primary = rowMeans`, `mpm` uses the strict `> 0.5`, `log_Z` is the log-sum-exp minus log R, and `out$hpm`
  is the ledger's running best. On a run that is not completed, the estimates are NA.
- The budgets: N₀ = max(2500, n, p), N_e = 4^e N₀, L = max(4, ⌈log₂(n+1)⌉), T_e = 4^e max(1000, ℓ²), B ≤ 16.
- Calibration status "ok" includes the C-DLV B tier-1 fallback grid, which is either a construction or the pilot schedule, so
  T ≤ T_e still holds.

Citecheck reports 83/83 in range. The SHA-256 prefixes in numerics/README match the files.

**Proofs, step by step:**
- **ST.** ST-a: the stationarity equation at S₀ gives π(S₀)K(S₀,Ω∖S₀) = Σ_{S≠S₀}π(S)K(S,S₀) ≤ π(Ω∖S₀). ST-b: the exit
  probabilities are exact, and the targets S₀⊕j are distinct, so the sum over j is ≤ o₁. ST-c: a first-exit decomposition
  given σ, and each label occurs once, so λ₀ ≤ o₁ + (B+2)o₁. All three are correct.
- **MR.** MR-a, MR-b and MR-c are T12 (i.a), (i.b) and (i.c) at fixed c. The κ(σ) = σ⁻¹(ℓ) − 1 prefix is T12's own example. The RB
  identity holds: π(o_j(·,1)) = π(j ∈ S), checked by pairing S⁻ with S⁺ (cap configurations have π-mass 0). The bound Ẑ_t/Z_t ≤
  e^{max d − min d} is correct. The freezing is applied to a jointly measurable bounded g. Correct, and correctly localised.
- **LT♯.**
  - Step 1: the good/bad pair split does not depend on j. That is what removes the union over coordinates, and inequality (1)
    holds pathwise.
  - Step 2(a) is MR-b at s = L + q − 1.
  - Step 2(b) uses R3 conditioning on H_q (the order is uniform and independent of H_q).
  - Step 2′: W is H_q-measurable because evidence is not updated after T. Then E[WΛ_q] ≤ λ₀E[W A_{r,q−1}] = λ₀(1 − δ). The minimum
    with E W = 1 gives g.
  - Step 3: the inclusion {B̄ + Λ̄ ≥ 2ε} ⊆ {B̄ ≥ ε} ∪ {Λ̄ ≥ ε} holds. The constants check: 8 = 1/ε, 152 = 19·8, 57 = 19·3,
    21 = 1 + 1 + 19.
  - The MPM inclusion covers the tie at ½.
  - LT-e, LT-e′: the truncation and bounded convergence are correct. In LT-e′ the 𝓒-measurable threshold is valid for a
    conditional Markov step.
- **C.**
  - Step 1 (Hölder) holds, with ω(φ) = Σ(γ₀(S)/γ₀(s))^{1−φ}(γ₁(S)/γ₁(s))^φ.
  - Step 2 holds.
  - Step 3 (stopped sum): the pointwise bound min(U,u) ≤ Y holds, and so does the bound on W_t when V_{t−1} ≤ u. Only
    deterministic-index identities are used. Correct.
  - Step 4 is the key new argument. I re-derived it line by line:
    - The recursion V_t = V_{t−1}q̂_{t−1}(e^{Δ_t a}) holds.
    - The rescaled MR-a gives E[V_{t−1}q̂_{t−1}(f)] = Σπ₀e^{φ_{t−1}a}f.
    - Jensen gives (1 − mean)⁺ ≤ mean (1 − ·)⁺, and the sum telescopes to b₋.
    - c = π₀(s)/π(s) and W = V_T/c.
    - The positive part is subadditive, so E|W − 1| ≤ 2(b₋ + (c − 1)⁺)/c = 2max(b₋,b₊)/c.
    - The bounds b₋ ≤ δ₀ and b₊ ≤ c·δ hold, and δ₀/c = (1 − δ)o₀.
    The argument is correct for every grid and N_e ≥ 1. At T = N_e = 1 it reduces to E|w(X) − 1| for X ~ π₀, which confirms the
    bound is attainable in form. The bias bound and E E_r ≤ g + β/2 follow from E(1 − W) = 0, and E(W − 1)⁺ = E(1 − W)⁺.
- **TR.** TR-a: K_I(x,y) = min{π₀(y), π(y)/w(x)} ≥ π(y)/M, and K_I(x,x) ≥ π₀(x) ≥ π(x)/M. K_post is π-invariant, so
  K_pre K_I K_post ≥ M⁻¹π. The Doeblin contraction is standard. TR-b: R3 makes the particles evolve as separate per-particle
  chains under K₁ after the bridge (verified in the code: no resampling at φ = 1), so E[ψ(X′)|𝓗] = K₁^Lψ ≤ π(ψ) + e_L. Taking
  the expectation of min{1,·} only ever loses. Correct.
- **D.** τ_k is a stopping time because control flow and uniform counts depend only on values already read. The strong Markov
  property of an iid sequence, together with START, makes each draw π₀ and independent of 𝓕_{τ_k}, which contains the earlier
  draws. The count D_r = N_e(1 + T + L + 4) is deterministic given c. The deterministic step {S† ≠ S₀} ⊆ {δ ≥ ½} holds. The
  production corollary D_r ≥ N₀(L + 6) ≥ max(n,p)·log₂(n+1) is correct.
- **PC.** On a completed run no island returned early (the only early return is at `:335-338`, and a partial island sets
  `resource_limit`). Nothing resets the status. The ledger is never reset.

**Own falsification run** (independent simulator, my scratch dir; not the package's `samp_sim.py`). Exact kernels on Ω with
p = 4, K ∈ {2, 3}: Gibbs, the uniform swap, and the π₀-independence MH at φ_t. Multinomial resampling at every stage, random
orders, RB recorded before the Gibbs draw. 10 random targets, 3 of them adversarial (a state of tiny π₀ with a(S) = +5, so
b₊ > 0), × (T, N, L) ∈ {(1,1,0), (3,2,1), (16,1,2), (64,3,4)}, with 20 000 islands each. I tested E|W−1| ≤ β, E[W E_r] ≤ g,
E E_r ≤ g + β/2, E E_r ≤ min(1, g + e_L) and E min(U,1) ≤ 4(T+1)δ̄. There were **0 violations in 40 cells**. E W was 1 to Monte
Carlo accuracy. The T-free bound came close to equality at T = N = 1 (0.073 against β = 0.076), and E|W−1| fell with T at fixed β.

## Gates

**G1 — correctness of every step: PASS.** I found no wrong step. The key arguments are correct as written:
- LT's pathwise all-coordinate decomposition and its unweighted leave bound;
- C Step 4's telescoping, which I consider the strongest new result here;
- C-ii's stopped sum;
- TR's minorization, Doeblin bound and per-particle chain;
- D's stopping-time argument;
- the MR extension to stage, prefix and pre-step states.

Two small presentation slips (issues 3 and 6) do not affect any stated claim.

**G2 — hypotheses used = hypotheses stated: PASS** (one non-blocking omission, issue 2). Each theorem uses the premises it lists:
- LT, C and TR use the N1 premises, plus P-CONC/NC_r, δ̄, and P-OVL∞ respectively, in the asymptotic parts.
- D-ii alone uses IND-T.
- MR's h class is restored, with the counterexample remark.
- The production corollaries are labelled, separately from the component claims.

**G3 — no hidden assumptions: PASS.** The proofs make the following explicit, and every one matches the code:
- the localisation to 𝒜 and to completed runs;
- the potential/completed split (PC);
- the order being independent of the state;
- no resampling at φ = 1;
- emission before acceptance;
- the bound B ≤ 16.

The one implicit step is that the conditional bounds are integrated under the joint data/algorithm law. This needs the
ideal final streams to be independent of the data (issue 7). That idealisation is standard and inherited, but it should be one
explicit sentence. Issue 1 is a scope gap in PC's wording, not a hidden assumption about the method.

**G4 — imports have adequate status and say what is claimed: PASS.** I checked each import at its cited lines:
- T12 (i.a), (i.b), (i.c), (ii) and (R3) say what is used. T12's status ("proved … not adopted") is quoted verbatim.
- W1-N1 Lemma B (record convention including orders and within-round paths, `L1_bridge.md:14-20`; (B-b) stopping times
  `:77-88`) and L3 (localisation, boundedness) say what is used. W1-N1's status is PROVED-CHECKED.
- START and KERNEL's inherited status is quoted.
- W3-POST Theorem 1(1) is quoted exactly. P-CONC is consumed as an interface property, as PROTOCOL rule 5 requires.

The internal status lines are stale (issue 4). That is bookkeeping, not adequacy.

**G5 — constants and rates tracked: PASS.** The explicit constants 19, 21, 22, 44, 57, 152, 4(T+1) and β are all re-derived
and correct. The O_P(r_n) transfer in C-v is valid: E min(1, 2X/M) ≤ P(X > K) + 2K/M with X tight. The T-free claim is real: β
depends on the data only. TR's e_L ≤ e^{−L/M} holds. D's exponent is exact.

**G6 — fidelity to the method as coded: PASS.** I verified each coded object against the source:
- pip_primary is the equal-weight mean of the RB island PIPs, recorded before the draw with the cap convention.
- MPM uses the strict > ½.
- Reported HPM: the hpm_better-maximum of every offered model, including rejected proposals, tables, inherited models, the
  final local search and LS0. PC(iii) correctly says it is not a function of the island records.
- log Z: log-sum-exp minus log 4.
- The RB recording position is pre-step, so MR-c (not MR-b) is the right identity.
- Draws: N_e(1 + T + L + 4) per island, all emitted.
- Ledger: idempotent re-offers, and cache hits imply an earlier offer.
- On a run that is not completed, no estimates are returned.

The exact-enumeration branch is correctly excluded: its status is "exact", not "completed".

## Overall score: **8.8 / 10** (all six gates PASS)

This is a careful, honest and largely sharp package. It delivers PROGRAM item 4 (a)–(d):
- (a) unbiasedness, through the MR extension;
- (b) the corrected LT, which now covers pip_primary (RB recorded mid-round) and the MPM, with no factor p, and labels NC_r
  honestly as a premise about the particle system;
- (c) the concentrated bridge, now with a T-free evidence bound that improves on both sources;
- (d) draw discovery with the code check on rejected proposals.

TR offers a premise that involves no particle statistic, in place of NC_r. The statements are design-agnostic and use interface
properties. Every listed issue is non-blocking. I deducted for a scope gap in PC that the D/LT/C/TR HPM transfers rely on, one
premise omission in D, and some stale bookkeeping.

## Issues

1. **NON-BLOCKING — Lemma PC's scope is narrower than its downstream use.** `STATEMENT.md:87-89`,
   `lemmas/PC_completed.md:120-129`. PC(i) states record equality for "Ẑ_r, all populations, the RB accumulator". Four results
   transfer the potential event {S₀ ∉ 𝓜_r} to completed runs:
   - D-iii (`D_theorem.md:180-185`);
   - LT-e HPM (`LT_theorem.md:72-73`);
   - C-v HPM;
   - TR-d HPM.

   That transfer needs the set of models **evaluated** by island r, including rejected π₀ draws and swap proposals, to coincide
   with the potential run's set. The statistical record of Lemma B excludes rejected proposals. D §1 builds an augmented record,
   but PC never cites it. The same argument works: on a completed run the island ran uninterrupted, and the sequence of
   `eval` arguments is a function of (c, stream) under EX-A. **Fix:** in PC(i), add "and the sequence of models passed to
   `eval` by island r (in particular its D_r π₀ draws), i.e. 𝓜_r" and cite D §1's augmented record.
2. **NON-BLOCKING — D's premise list omits KERNEL**, though the proof cites W1-N1 Lemma B (B-b), which is stated "under EX-A,
   START and KERNEL". See `STATEMENT.md:94` and `D_theorem.md:146-149`. The part used, that control flow and uniform counts are
   decided by values already read, does not need KERNEL. **Fix:** either add KERNEL to D's premises, or say explicitly that
   only the control-flow clause of (B-b) is used and that this clause is a code fact independent of KERNEL.
3. **NON-BLOCKING — TR-b proof slip.** `lemmas/TR_theorem.md:49-50` (and `:16`). With ψ(x) := K₁^q(x, Ω∖S₀), the
   burn-in step as written gives δ + e_L, not the claimed δ + e_{L+q}. The statement claims only e_L (`STATEMENT.md:163`), so no
   claim is affected. **Fix:** apply TR-a to K₁^{L+q} directly, (K₁^{L+q}1_{Ω∖S₀})(X^{(T)}) ≤ δ + e_{L+q}, or drop e_{L+q}.
4. **NON-BLOCKING — stale status and version lines.** `lemmas/PC_completed.md:3`, `MR_identities.md:3` and `ST_stay.md:3` say
   "Statement: STATEMENT.md v2" and "PROVED (by this seat, unchecked)". The statement is v3, and the lemmas have since been
   through lemma checks and a sweep. `LT_theorem.md`, `C_theorem.md`, `D_theorem.md` and `TR_theorem.md` also say
   "unchecked". **Fix:** update every status line to the post-council label before the registry entry. PROTOCOL wants statuses
   verbatim, and these are what downstream tickets will quote.
5. **NON-BLOCKING — 𝒜 should be identified with the coded success condition.** `STATEMENT.md:37-39` and `D_theorem.md:180`.
   The inclusion {completed} ⊆ 𝒜 rests on 𝒜 = {`cal$status == "ok"`}, which **includes** the C-DLV B tier-1 fallback grid
   (`v3_calib.R:141-143, 162-167`). CC6 already handles the fallback for the T ceiling. **Fix:** add one sentence to §0 defining
   𝒜 as the event that `v3_calibrate` returns status "ok", fallback included. Cite `v3_fit.R:154-162` for "no final run
   otherwise".
6. **NON-BLOCKING — wording in the asymptotic clauses.** `STATEMENT.md:132` ("— for any frozen parameters") sits in a
   joint-law statement where the frozen parameters are the random 𝓒. **Fix:** say "with no condition on 𝓒 (grid, N_e, L)".
   Similarly, `LT_theorem.md:67` bounds by P(o₁ > ε/3) where the set inclusion is in κ₀; correct as an upper bound, but
   should say "{κ₀ > ε/3} ⊆ {o₁ > ε/3}".
7. **NON-BLOCKING — the joint-law integration step should state its idealisation.** `STATEMENT.md:33-35`. Integrating a
   fixed-data conditional bound as E[min(1, ρ)] under the joint data/algorithm law uses one fact: given (data, 𝓒), the final
   streams have the ideal iid law (H-U + SI), whatever the data. In code the streams are a deterministic function of the
   user's seed. This is inherited and standard. **Fix:** add one sentence to §0 saying that H-U/SI are assumed under the joint
   law, i.e. the ideal streams are independent of the data.
8. **NON-BLOCKING — the constant 19 should be tied to the coded B.** `STATEMENT.md:120` and `lemmas/ST_stay.md:122-123`.
   λ₀ ≤ (B + 3)o₁ is the general bound, and 19 uses B ≤ 16 from production preprocessing (`v3_preprocess.R:22`). The
   component claims are for "any frozen parameters", and B is a setup quantity, not a frozen one, so this is fine for the
   method. A harness that builds a setup with another B would change the constant. **Fix:** state the constants as (B + 3) in
   the component claims, with "≤ 19 for the coded B" in parentheses.
9. **NON-BLOCKING (presentation) — an optional sharpness note on TR's example.** `lemmas/TR_theorem.md:66-69`. The remark
   argues "not nested" from one direction only: π₀(S₀) → 1 does not imply M = o(L). The converse is immediate (π₀(S₀) = ½ fixed,
   π(S) ≤ π₀(S) off S₀ and π(S₀) → 1 give M ≤ 2 while π₀(S₀) does not tend to 1), but it is not written down. **Fix:** add the one-line converse.

No BLOCKING issues.
