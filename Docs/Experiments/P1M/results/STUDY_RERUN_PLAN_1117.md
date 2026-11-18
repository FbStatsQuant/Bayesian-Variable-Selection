# Frozen-method re-run of the 2,400-fit study + post-hoc list PIP + real data (Engineering plan, 2026-11-17; no runs)

## 1. Subset (paired with the 2026-10-28 study on the SAME datasets)
- High p (the study the paper reports for selection): all 24 cells = p ∈ {500, 1000} × c ∈ {1, 0.5} × S1–S6, first 25 of the
  100 datasets per cell = **600 fits**, core v3 at the theory pin, LS0 on, default cap ℓ_n + |S̃₀|, hours = 24.
  Paired read-out vs v2.2.1: HPM agreement, exact recovery, PIP_eq and list-PIP differences, LS0 moves.
- Low p: all 24 cells (p ∈ {20, 30}) × 25 = **600 fits**. v3 has an exact branch (v3_fit.R:30, :106); if it takes p ≤ 30, the
  re-run must force the SMC branch to repeat the SMC-vs-exact check (owner/Theory choice). Cost small either way (≤ 50).
- Settings: the LS0 worst-case preflight charge stays ON (it is the method). Scaled from Writing's 563 h at n = 200, p = 10⁴ by
  (p + p²/4): ≈ 1.4 h at p = 500, ≈ 5.6 h at p = 1000 → below hours = 24, so no refusals expected; LS0 seconds recorded.

## 2. Cost (billed = CPUs × elapsed, the LEDGER unit)
- v2.2.1 basis (PROD-H, ops/PRODH_COMPLETION_20261102.md:32): 1,813 billed for 2,400 → 0.38 (p500) / 1.13 (p1000) per fit.
- 600 high-p fits at v2.2.1 cost ≈ 450. v3 multiplier UNMEASURED at n = 200, p ≥ 500: W3-P6 saw tier-1 escalation (≈ ×4) above
  p > n/2 and unfinished > 6 h fits on its cs ρ = .5 design. Bracket ≈ 450–1,800 (+ low p ≤ 50).
- First step: a 24-fit probe (one per high-p cell, seed = dataset 1), cap 60 core-h, gives the multiplier → final size.
- Budget: margin under 28.3k with D + 20 replicates ≈ 1.8k → fits if the multiplier ≤ ≈ 3.5; otherwise 15/cell or HQ choice.
  Without D, margin ≈ 3.7k → fits.

## 3. Schedule (no date moves)
- Single-node v3 array jobs, 2 at a time, backfilled 11-22 – 11-30 (after the overlap rung, alongside precision/10⁴ science and
  the 10⁵ rung); finished before the 1M block (≈ 12-01), never alongside a 1M fit. Runner = the 2026-10-28 runner with the core
  swapped to the pin (Sonnet). The list-PIP field is post-hoc (§4), so the re-run need not wait for it.

## 4. Post-hoc list PIP
- v4: fit.bin carries the merged top store (models + F; INTERFACES §5.1) and merge already computes PIP_T from it
  (merge.h:359-364). A post-hoc tool calling the same function on fit.bin gives the in-code bits. Covers the 1M pilot (rep 1)
  and T5 → no re-runs, if (a) the spec's "returned list" = the merged top store and (b) the fit.bin files are kept (check offload).
- v3: `top_store` is in the fit object (v3_run.R:210) → same, for saved fit objects.

## 5. Real data
- Not in the experiment plan. Natural choice: riboflavin (Bühlmann, Kalisch & Meier 2014; R package hdi; n = 71, p = 4,088),
  standard in the BVS literature. Cost: engine v4 ≈ one 10⁴-scale fit (≤ 35 core-h, n and p smaller); core v3 needs hours or
  ls0_cap set (worst-case LS0 charge ≈ 94 h by the scaling above at n = 200; less at n = 71). + competitors, small.
