# Post-BT1 addendum (not seen by any reviewer; kept outside the frozen manifest so that MANIFEST_BT1 still verifies)

These files were produced after the better-theorem round was frozen. They move into `numerics/` at the next freeze.
Observations only, never proofs.

1. **The 78th run of the n = 1600 layer** (cell B4, η = 1, seed 1) finished after the freeze:
   start mode 743 columns (727 outside Q), 73 swaps, LS0 stopped at the move cap (756 moves) at a model of 60
   columns — not S₀. With it the cell reads: conclusion in **2 of 6** runs (RESULTS.md, frozen at 5 runs, says 2/5),
   and the overall count is **204 of 208**. All six rows: `B4_eta1_n1600_all6_rows.csv`. The four failing runs made
   19, 24, 35, 73 swaps; the two successes 6 and 12; the cap slack is ℓ_n + s₀ = 15.
2. **Identity used by proposal P1 of BT1** (the reviewer's suggested refutation test): for T ⊇ S₀, i ∈ S₀, l ∉ T and
   A = (T ∖ {i}) ∪ {l}: RSS_A − RSS_T = (θ_i‖(I − P_A)x_i‖ + σZ_{A,i})² − σ²Z²_{T,l}; for A = T ∖ {i} the last term is
   absent. `check_identity.R` → `check_identity_out.txt`: 400 comparisons with correlated columns and signed
   coefficients, maximum relative error 1.2e-14.
3. **The n = 3200 layer** (B1 only, 3 seeds per cell) was started at 18:09 and **stopped before any run finished**
   (more than 7 minutes per run with three workers; free memory down to 6 GB). Not run.
