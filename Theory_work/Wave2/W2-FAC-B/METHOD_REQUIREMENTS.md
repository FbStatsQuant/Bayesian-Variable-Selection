# W2-FAC-B — METHOD_REQUIREMENTS

**No new method requirement for the proved class.** Theorem FAC-CS is proved for the method as merged on main
(v3.1, 4676af6): LS0 from the start mode with the merged cap a_n = ℓ_n + |S̃₀| (MR1 (C-GROW)), tie-aware start DP,
tier-1 calibration fallback. On this class MR1 is **used essentially**: the LS0 path has exactly m₀ = p − s₀ − |N₀|
moves, so with the legacy cap ℓ_n the deterministic LS0 scored set misses S₀ whenever m₀ ≥ ℓ_n + 2 (STATEMENT (C2);
L5.2). This is a statement about the LS0 route, not about the full fit.

**Finding (not a requirement; for HQ's information).** For p > n/2 (outside the proved class), in the diagnostic data set N2 the start
mode is size-saturated at K = ⌊n/2⌋ (not claimed in general: p − |N₀| < K is possible) and the LS0 path begins with null–null swaps (noise fitting at |T| ≈ n/2, where the
residual dimension halves). In the single diagnostic data set N2 (exact Gram, one factor ρ = 0.5, n = 600, p = 500) the
uncapped path needs 315 moves and the MR1 cap is 311, so LS0 misses S₀: its last scanned centre has 4 extras and the returned improving neighbour 3 (numerics/N2_summary.md). A cap that also
allows a swap phase (e.g. ℓ_n + 2|S̃₀|, or ℓ_n + |S̃₀| + K) is a *possible* response; it is **not** shown to suffice
(the number of swaps is not bounded by any proof here) and is not proposed for adoption.
