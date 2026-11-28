# PSMC-S0 — CHECKPOINT_1 (Part 1: T-N, T-CAL preliminary, D-7) — final; ticket ends here (Part 2 cancelled)

**Scope (owner via HQ, 2026-11-15):** the theory stays about the method as coded at p = 10⁴. Engineering may change the
algorithm for 1M if it documents each change and validates the variant against the theorem-covered method on an overlap
rung. This checkpoint is therefore advice to Engineering, not a list of theorem premises. Part 2 (T-PART) is cancelled.
Nothing here blocks OD-1, OD-2(c) or the D-7 drop. HOLDS.md: no holds. Review: Sol FR1 fidelity read (NORMAL mode): FAIL on citations, wording and inventory completeness; all 9 findings
accepted and fixed (`reviews/FR1_disposition.md`); FR1 confirmed the D-7 verdict and the any-N / any-frozen-𝓒 proofs.
Files: `AUDIT_N.md`, `AUDIT_CAL.md`, `reviews/FR1_*`.

## Plain words for HQ and Engineering (≤ 10 lines)
1. Leader stores (D-7): SAFE TO DROP from final islands and output, as long as calibration still feeds its leader
   stores into V and into the inherited models the final run is offered (`v3_core.cpp:707-708, :732-733 → :418-428`).
2. OD-1's text "equals v3.1 for p ≤ 2,500" is true only when n ≤ 2,500 too (N₀ = max(2500, n, p)).
3. Fixed N = 2,500: the theorems are proved for any number of particles, so a fixed-N run at the overlap rung is still
   inside them; what changes is precision (σ̂ of log Ẑ_r) and the draw-only discovery rate. Under fixed N, exact
   enumeration eventually covers only fixed p ≤ 17.
4. Bounded calibration: no theorem reads E2, the tier or grid convergence; keep the tier-1 fallback grid (delivery).
   If a failed tier-0 rebuild freezes instead of escalating, install that grid, or the run exits with no output (D2).
5. Questions: under OD-2(c), is a tier-1 island 4 × 2,500 or 2,500 (and H 512 or 2,048)? Fix I_max ≤ ℓ (true at 3).
   Does a failed tier-0 rebuild escalate (as coded) or freeze the last successful grid?

## Verdicts (Part 1)
| item | verdict | file |
|---|---|---|
| RM-0, RM2, LT♯, C, TR, N1, finite D: any N, any frozen 𝓒 | confirmed | AUDIT_N §2, AUDIT_CAL §2 |
| TH01(e)(f), TH06 | N-free | AUDIT_N rows 1, 2, 4 |
| TH01(i) | N-free; needs R′_n → ∞ (not R′ = 16) | row 3 |
| TH08 | formulas in N_e; v3.1 budgets written in | row 5 |
| W3-SAMP D production corollary; W2-APP ENUM (ii) | weaker under fixed N (sufficient conditions) | rows 6, 7 |
| C-DLV Prop F (delivery) under OD-2(c) | holds with the fallback + A1 amended allocation; Thm D (ii) is unpatched-law only | AUDIT_CAL rows 1–4, 15 |
| D-7 final-run leader stores | **SAFE TO DROP** (condition above) | AUDIT_CAL §3 |

## Engineering-facing notes (document / validate on the overlap rung)
- **Fixed N.** Document N, H per tier (incl. escalation) in the manifest. Validate at the overlap rung (p = 10⁴, where
  v3.1 uses N₀ = 10⁴): old-law vs fixed-N on the same data — HPM, PIP agreement, σ̂(log Ẑ_r), R_eff, and the first
  scoring time of S₀ (draw discovery is the mechanism that weakens).
- **Calibration.** Document I_max (≤ ℓ), the escalation rule, the tier-1 (N, H), and the meaning of `escalated` (now "a
  construction failed"); a tier-0 freeze must install the grid (no D2 exit). Validate with the three-arm test (coded / I_max / pilot only): grid length T, σ̂, HPM, PIPs; record every
  trigger as now. Keep the C-DLV tier-1 fallback.
- **Partition.** Document τ_n, ≥ vs >, cut and packing order. Validate (gate T11 + A3): blocks equal to the exact
  dendrogram below 1 − τ_n; π₀(S₀), the start mode S̃₀ and the LS0 path compared with exact linkage on the same data.
- **Streams.** Document the address map and generator. Validate the law, not bits (T4): distributional checks of
  log Ẑ_r, PIPs and HPM against v3.1 over many seeds at the overlap rung.
- **Merge / R′ = 16.** Document the pooled outputs (PIP_eq, PIP_Z, PIP_𝒯, union stores) and which is primary.
  Validate: at R′ = 4 with v3.1's N the merge reproduces serial output (T9); report R_eff and island agreement.
- **Leader stores.** Drop from final islands; keep the inherited set = calibration top ∪ lead0 ∪ lead1, and check in
  T2 that the final top store and HPM are unchanged by the drop.
