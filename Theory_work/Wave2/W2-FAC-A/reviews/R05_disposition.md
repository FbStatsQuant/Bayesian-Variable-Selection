# R05 disposition (fresh Codex gpt-6.1-sol xhigh mid-point: CONTINUE)
1. MAJOR — S5 certificate not exact: fixed. New Lemma TVF (closed form of the population partial signal for one factor
   + block-diagonal Ψ, proved in L5.3) and numerics/tv_cert_exact.py (exact Fraction arithmetic; closed form
   cross-checked against direct linear algebra, 3.8e-15). Exact minima: 2023/32500 (s₀ = 4) and 7/2080 (both s₀ = 14
   layouts) at unit scale; exhaustiveness and invariance under adding null groups argued in L5.3.
2. MINOR — L3 "p + 1 ≤ K" and probability line: already fixed after R03 (identical finding).
3. MINOR — g₀ minimisation over infeasible (V, u) for bounded p: restricted to u ≤ min(15, |V| + p − s₀) in L5.2 (I)(a).
