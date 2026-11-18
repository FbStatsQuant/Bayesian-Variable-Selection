# Helper B brief — W3-START2-R boundary numerics (Sonnet 5.5, effort high, Claude Third) — saved before launch

You run observational numerics for ticket W3-START2-R. Repository root `/home/fb31/BVS-wt/W3-START2-R` (git worktree).
**Write only inside** `Theory_work/Wave3/W3-START2-R/numerics/`. Change no git state, start no agents.

## Machine rules (binding)
- Temp: `export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261116-W3-START2-R-numerics; mkdir -p "$TMPDIR"`;
  remove that folder when done. Never write to /tmp or elsewhere in /home/fb31.
- Every R job under `nice -n 10`, at most 16 cores in total, ramp up gradually (start with 4); no bursts; no NOTS.
- Large outputs (raw arrays, per-run files) go in `numerics/out/` and must not enter git: create
  `numerics/.gitignore` containing `out/`. Keep only scripts, a small summary CSV (< 200 KB) and `RESULTS.md` tracked.

## Tools
Copy (do not edit) what you need from `Theory_work/Wave3/W3-START/numerics/start_common.R` into
`numerics/r_common.R`. It sources the production core via `W3START_CORE`; set it to
`/home/fb31/BVS-wt/W3-START2-R/Scripts/SMC_BVS/core` (read-only; compile with Rcpp as `v3.R` does; if compilation
fails, report it and stop). π₀(S₀) is read from the coded start (`cpp_start_logmass`), as in the parent scripts.
Context: `Theory_work/Wave3/W3-START2-R/STATEMENT.md` v1.5 (D3, F4, (T3⁺⁺)(b)(iii), EX F-2, G-1) and `TARGET.md` §3.

## Runs (TARGET.md §3; observations only — never call them proofs)
1. **(V-cp) small p.** Orthogonal frame as BASE `lemmas/L11_EXAMPLES.md` L11.0 (p ≤ n − 1), s₀ = 1, null columns
   orthogonal to everything; truth signal set so that δ²_{∅,1}/τ²_∅ = c·log n + 2 log p, c ∈ {0.6, 0.9, 1.1, 1.5};
   p ∈ {⌈n^{0.3}⌉, ⌈n^{0.9}⌉} (≥ 17), n ∈ {200, 800, 3200}; 10 seeds. Report median π₀(S₀) and o₀ per cell.
   (Note: with one truth the deletion move is what visibility controls; compare with c computed at the v1.4 level
   (1 + 2A) log n, A = log p/log n.)
2. **F-2 at A = 0.9** (BASE L11.3 design, ρ² = 0.4, θ*₁² = 2(1 + 2A)σ² log n/(n − 1), p = min(⌊n^A⌋, n − 1)),
   n ∈ {200, 800, 3200}: o₀/T₁ (T₁ from the block tables as in the parent scripts), 10 seeds.
3. **G-1 rate.** Gaussian rows Σ = I, s₀ = 2, θ* = (1, 1)·(fixed), σ = 1, p = 2n, n ∈ {200, 400, 800, 1600, 3200}:
   o₀·√(n/log n), 10 seeds (6 at 3200 if slow).
4. **(L-gain-0) boundary.** As 3, but one null column with population correlation ρ_n = C₀/√(n log n) (C₀ = 2) with
   truth 1, versus ρ_n = C_L/√n (C_L = 2): o₀·√(n/log n) vs n.
Budget ≈ 1.5 h wall clock; if a cell is slow, cut seeds or the largest n and say so.

## Output
`numerics/RESULTS.md`: setup, one table per run (medians, IQR), and one plain sentence per run on what is observed;
no claim beyond observation. Final message ≤ 10 lines: what ran, headline observations, anything that failed.
