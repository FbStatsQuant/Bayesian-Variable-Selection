# Do the two lifted ceilings of IDEAL-W⁺ ever bind in practice? (post-freeze note for HQ; no runs, existing records only)

**Answer: no, and it is settled by arithmetic on the run sizes; logs are needed only as a confirmation.**
1. `v3_run.R:96` rejects the LS0 base cap `le > 1e6`. In the shipped configuration le = ℓ_n = ⌈log₂(n + p + 1)⌉, so it can
   reject only when n + p + 1 > 2^{10⁶}. W3-P6 runs its fits with the documented testing option `v3.ls0_ell = ℓ_n + K`
   (arm `wide`, `W3-P6/DESIGN.md:25`), so there le ≤ ℓ_n + ⌊n/2⌋, which exceeds 10⁶ only for n ≳ 2·10⁶; P6's designs have
   n ≤ 200, p ≤ 2,500 (`W3-P6/DESIGN.md:58-73`).
2. `cpp/v3_core.cpp:474` rejects an LS0 cap above INT_MAX = 2³¹ − 1; the cap is ≤ le + |S̃₀| ≤ le + ⌊n/2⌋, so it can reject
   only for n ≳ 4·10⁹ (P6 arm `wide`: also n ≳ 2·10⁹).
3. The 2,400-fit study: FIN `s7_impl.tex:12` records only that none of its fits had status `schedule_limit`; I have not
   established here whether those fits ran code containing the two checks (they were added by C-ENG, 0638af9 / bf093a8).
   Either way they cannot bind unless a fit had n + p + 1 > 2^{10⁶} or n ≳ 4·10⁹, i.e. never at any feasible size — the
   study's (n, p) range from its fit logs confirms this in one look. W3-SCR's numerics are at n ≈ 100 (`W3-SCR/numerics/`).
**Confirming log fields (if HQ wants them):** in each fit object, `status` together with `message` (the two checks stop
with "option v3.ls0_ell must be a whole number in [0, 1e6]" and "LS0 move cap out of range"), `settings$ls0_ell`, and
`n`, `p`. A grep of the stored fit logs/RDS for those two messages would close it; not run here (no runs post-freeze).
