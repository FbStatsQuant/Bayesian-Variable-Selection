# Amendment 01 (2026-11-03, HQ, from Felipe): the method must apply for every (n, p)

**Felipe's words (binding, as a ground rule 9):** "Make the final method remains something applicable to all n - sample size - like hyperparameters being fixed small values, or depending on n, or P_n (number of variables at n) etc, like in Song (2015), make sure there is no weird arbitrary choice so the method applies in general for all n and. Cases p << n and n >> p being separate is also available if needed. I think v3 is already grounded but make sure the final methodology is something applicable for whatever n, p as well."

**New agenda item 9: generality in (n, p).** Every seat audits every setting of v3.1 and classifies it as one of:
(a) a modelling convention with a stated reason (e.g. g = n, τ = 1, IG(0.01, 0.01), BB(1, p), cap ⌊n/2⌋);
(b) an explicit function of (n, p) or of X;
(c) a declared resource budget (it changes cost, never the target);
(d) a numerical tolerance;
(e) **arbitrary**, tuned to the study, or one that silently stops scaling. Every (e) must be fixed, or justified and moved to (a)–(d).

v3 already states this principle (METHODOLOGY_v3 Requirements (4): "no bare tuning constants"). The audit must check that it actually holds, including as n, p → ∞ jointly, for p ≪ n, p ≈ n and p ≫ n, and at tiny n. HQ's list of settings to check (not exhaustive; seats should find any others in the spec and the code):

- B = min(⌊√n⌋, ⌊√p⌋, B*), with B* = 16 an "implementation limit" that binds once n, p ≥ 289. Is a constant block size for large n, p acceptable for the method and the theory (W7-PART needs g ≤ B < 2g)?
- N₀ = max(2,500, n, p) and T₀ = max(1,000, ℓ²): the floors 2,500 and 1,000.
- ESS threshold 0.90 (schedule and grid construction), 60 bisection halvings, exploratory floor 1/T_e.
- Stores and caches: top 40p + 1, |V| ≤ 40p + 1, cache 500p; the near-tie window 10⁻⁹ nat.
- R = 4 islands, 4 measured rounds, tier factor 4, at most one escalation, L = max(4, ⌈log₂(n+1)⌉), ℓ = ⌈log₂(n+p+1)⌉.
- Exact-branch rule Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p, and the H₀ definition.
- The neighbour-graph threshold (√(log n / n) scale) and the correlation cut of the clustering.
- **Resource limits:** the status `resource_limit` depends on the job's memory and wall-time allocation. So the same (X, y, seed) can give a different output on different hardware. Is that acceptable under "runnable from X, y and one seed alone", and how does the paper state it?
- Any regime where a separate rule for p ≪ n versus p ≫ n is needed (Felipe allows it, if it is principled).

Also say, per regime, whether the **theory's** scope (e.g. p ≤ n^A, against Song–Liang's p up to e^{Cn^α}) restricts what the method can claim, and whether a method choice is what causes that restriction.

Deliverable: a table "setting → class → reason → behaviour as n, p grow → action", folded into `METHOD_v3.1_FINAL.md`, with every (e) item resolved in `MINUTES.md`.
