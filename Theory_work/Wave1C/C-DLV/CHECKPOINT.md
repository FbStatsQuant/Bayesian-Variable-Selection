# C-DLV — CHECKPOINT (written 22:30 CST, ahead of the 01:30 deadline; updated if anything changes)

## Proved and checked so far (each lemma: own proof file + cross-family check + falsification numerics)
- **Statement lock** R01 (Codex): REJECT (1 FATAL = the conditional plan does not prove the ticket target) → v2:
  target (T) kept, NOT claimed; claims split into proved reductions / conditional criteria / finding / open item.
- **Inventory** of every no-output exit of `v3_fit` (INVENTORY.md v2, 30+ sites, path:line), cross-checked by R01/R02.
- **Lemma R** (L1): all loops capped; explicit polynomial envelopes for operations, words, bytes, preflight bytes and
  exact-branch preflight seconds; under MACH and a declared allocation mem = C(n+p)², time = C[(n+p)p(n³+pn)log³(n+p)
  + (n+p)²p log³(n+p) + p²n² + p³], no resource path fires. R02: GAP → fixed (cache probing, tie-DP via W1-N3 TDP, a
  dropped term, memory reconciliation).
- **Lemma S** (L2): input/degenerate paths null on the classes; exact arithmetic ⇒ scorer never fails (PD + Q ≥ yᵀy/(n+1)
  + exact q_nonneg identity); internal errors unreachable on the call graph. R02: survives, S.3 extended.
- **Theorem D** (L4): no output ⟺ `schedule_limit` (up to a null set) ⟺ escalation to tier 1 and a failed tier-1 grid
  construction; failure = (α) interval count > T_e, (β) non_progress (needs d-range > 7.5·10¹⁷; impossible for
  n ≤ 2.277·10⁸), (γ) post-snap validation. **Corollary D′**: P(Ŝ⁺ = S₀ on 𝒪) ≥ 1 − o(1) − P(schedule_limit), by a
  pathwise argument with no CAL premise. **Proposition F (finding)**: freezing the tier-1 pilot schedule on failure
  makes P(no output) = 0, hence P(Ŝ⁺ = S₀) → 1 on LH / LH-iid / GEN for the patched method. R04: V-W-A, applied.
- **Grid lemmas** (L3, L5): exact identity ρ_V(u,v) = q_u(M)q_{2v−u}(M)/q_v(M)²; pilot ≤ T_e stages; dominance ⇒ no
  insertion; two-model family ⇒ ≤ 22 + O(log(1+|x₀|)) insertions (+⌈log_{4/3}((1+η)/η)⌉ if the remainder is controlled
  only on [0,1+η]). R03 (xhigh): core lemmas verified; one corollary ERROR (wrong bound, real counterexample) fixed.
- **Numerics**: production core, 80 fits on masked/favourable LH-type designs up to (1600,135): 80/80 completed, no
  escalation, max 17 grid intervals vs T_e = 1000 (numerics/SUMMARY_dlv.md); exact-enumeration N1; falsification
  N2/N2b 0 violations.

## Left
Mid-point R05 (running) → sweep → council; N3 (two-model hypothesis on the realised V of production fits), N4 (stress
designs). REPORT by 04:30.

## Honest estimate
The ticket target (T) — P(no output) → 0 on LH, LH-iid, GEN for the SHIPPED calibration — will **not** close by the
deadline: what remains is (O) a probability bound for the realised calibration candidate sets (two-model structure)
and for the tier-1 pilot stage count (the CJ06 / Conjecture P question; particle-system dynamics). Expected RESULT:
**PARTIAL** — delivery reduced exactly to `schedule_limit`, every other path excluded under a declared polynomial
allocation, (T) proved for the method with a one-line calibration fallback (finding for HQ), and (O) stated precisely.

## Update 23:03
Council PASSED in round 2 (Codex 9.0, Opus 8.9, all gates PASS). REPORT.md is final; RESULT = PARTIAL (target (T) not
proved; reduction package PROVED-CHECKED; fallback finding F1; (O) stated exactly).
