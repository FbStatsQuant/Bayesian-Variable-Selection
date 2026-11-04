# SR audit: "both Gibbs configurations count as scored" (HQ, 2026-11-02)

**Verdict: SR holds in the deployed engine (code v2.1 core in `Scripts/SMC_BVS/core/cpp/`).** Felipe delegated this confirmation to HQ.

## What SR asserts
Every model that a Gibbs step at coordinate j looks at, namely the current state S and the flipped state S Δ {j}, is a scored model. In particular it reaches the HPM store, the same as any other evaluated model. The proofs that lean on SR are D2 (W1-T38E), Theorem B and its corollaries (W1-T24G), T21 routes (d)/(e′), and T38.

## Evidence (file:line)
1. `v3_engine.h:113–132`, `step_gibbs`:
   - it calls `held(P, ME_GIBBS_HELD)` on the current state;
   - for a feasible flip, it builds `tmpQ = S Δ {j}` and calls `eval(tmpQ, ME_GIBBS_FLIP)` **before** the accept draw. The flipped configuration is therefore evaluated whether or not the move is taken, and the comment at :112 states SR explicitly;
   - an infeasible addition (|S| = K and j ∉ S) is not evaluated. This is consistent with SR's "feasible configurations".
2. `v3_engine.h:87–100`, `eval`: every evaluation with `emit = true` (the default) calls `led->event(...)` with `is_fresh = fresh || !cache`. **No call site passes `emit = false`** (grep over `cpp/`).
3. `v3_ledger.h`, `Ledger::event`: `offer_stores → offer_hpm` runs on fresh evaluations. Cache hits and held states are not re-offered, because they were offered when first evaluated in the same run context:
   - the cache is inserted only inside `eval`, which always emits;
   - an evicted model is re-evaluated as fresh and offered again, which is harmless;
   - the HPM tie rule (`hpm_better`) applies.
4. **Every state a particle can enter is evaluated on entry:**
   - initial draws: `eval(P[i], ME_INIT)` (:289–291);
   - Gibbs flips: `P = tmpQ` after `eval` (:131);
   - uniform and neighbour swaps, and independence moves: `eval` then `P = tmpQ` (:158, :179, :186–191).

   So a `held` current state has always been offered before.
5. **Calibration → final run.** Calibration runs in its own context, `CalState`, with its own cache and ledger (`v3_core.cpp:553–582`). Its scored models and its HPM are passed through `frozen$inherited` (`v3_calib.R:155, 168`) and offered to the final run's stores and HPM with provenance "inherited" (`v3_core.cpp:409–421`). The reported HPM is therefore the best over calibration plus the final run.

## Caveats (stated, not defects)
- **SR covers the *logical* scored set.** "Scored" in the theorems means "offered to the HPM store at least once in the fit". That is what the code does.
- **LS0 must follow the same discipline:** emit its centre S̃₀ through `eval` (a score event) before searching (the W3-VT38E caveat).
- **This is HQ's read of the code, not an independent audit.** W5-LOCKBOOK includes a GUARD/OUT/SR code audit; its verdict supersedes this note if they differ.

## Decision recorded
**LS0: APPROVED by Felipe (2026-11-02), conditional on O-LS0's data check.** O-LS0 must show that on the 2,400 regenerated datasets LS0 changes few or no reported HPMs, never turns a correct report into an incorrect one beyond posterior-mode corrections, and costs a negligible amount of compute.
- Presentation: as part of the method (a final local search from both the best-scored model and the start mode), with T38 + LS0 as the main theorem and the no-LS0 version as a conditional remark.
- Implementation: emit the centre, use the HPM tie rule, label mechanisms; whether to run to certification is decided with O-LS0's data.
