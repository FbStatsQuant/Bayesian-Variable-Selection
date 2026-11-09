# C-DLV — method requirements and findings (for HQ → C-ENG)

## A. Not-yet-shipped components (LS0, e4 tie fallback): requirements adopted
One implementation choice is adopted (TDP-IMPL, item 2); otherwise only what the spec already says is used:
1. LS0 runs the §6.10 local-search rules with a move cap ℓ_n that is a polynomially bounded function of (n, p)
   (spec: ℓ = ⌈log₂(n+p+1)⌉); a capped LS0 returns output with `local_limit` (not a stop).
2. LS0 and the tie-aware start-mode DP (e4) run under the same stop-only runtime guard (GUARD-W) and read no uniforms.
   **Adopted requirement (TDP-IMPL, flagged):** the e4 truncation fallback is implemented as W1-N3's reference
   algorithm TDP (greedy inclusion + constrained max-plus feasibility DP; Theory_work/Wave1/W1-N3/lemmas/
   L7_tie_aware_dp.md, "PROVED; XF-checked"), or any algorithm returning the same maximiser within its bounds:
   O(p·Σ_b(2^{|C_b|} + (K+1)²)) operations (W1-N3 L7:20), implemented with O(Σ_b 2^{|C_b|} + J(K+1)) storage (the (block, size) DP table plus the block tables;
   this storage bound is a requirement on the implementation — L7 states only the operation bound). The delivery resource bound (L1)
   depends on this cost guarantee; e4's correctness requirement alone does not supply it (R02 #3, R05 #1).
3. Their memory (one centre + scan, the DP tables O(J·(K+1)·2^B)) is counted in the preflight/allocation (L1 R.5).
None of LS0/e4 can affect `schedule_limit` (they run after calibration).

## B. FINDING on a shipped component (calibration) — reported, not made (Wave1C protocol)
F1 (lemmas/L4_delivery.md, Proposition F): `schedule_limit` is the only no-output path that is not excluded by the
declared polynomial allocation and the idealisation premises. If, when a tier-1 grid construction fails, calibration
froze a valid fallback grid — the tier-1 pilot schedule (always ≤ T₁ strictly increasing stages from 0 to 1), or the
last successful construction of that tier when one exists — instead of returning `schedule_limit`, then P(no output) = 0
under the premises, and the reported-HPM consistency results of W1-GEN / W1-PXN would hold with P(Ŝ⁺ = S₀) → 1, without
the delivery caveat. The change affects the calibration law only on the event where the shipped code returns no
estimates; final-run validity holds conditionally on any frozen 𝒞 (calibration contract). Classification under
METH-AUDIT (ADDITIVE / LAW-PRESERVING / …) is HQ's call.

## C. Idealisation findings (no method change proposed)
- Fixed word size: the checked-overflow status `unsupported_size` (spec e7) fires for every fixed machine word at
  large enough (n, p); the theorem is stated under IDEAL-W (unbounded words), like EX-A for arithmetic.
- Fixed bisection depth (60 halvings, kept literally under EX-A): `non_progress` needs a d-range on V above
  2√c₀·2⁶⁰ ≈ 7.48·10¹⁷, which the crude bound of L4 Remark D.1 excludes for n ≤ 2.277·10⁸; beyond that the bound no
  longer excludes it. No failure is claimed — attainability on the classes is open (R06 #4).
