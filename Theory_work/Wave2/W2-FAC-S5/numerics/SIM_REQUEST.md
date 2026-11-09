# W2-FAC-S5 → W2-SIM request (2026-11-09)

**Question (decides Tier 2 / Lemma KL).** On exact-Gram block compound symmetry (S5: groups of 5, ρ_b = 0.3, ρ_w = 0.7),
along the uncapped LS0 path from the full model, how does the global error e_T scale with p and with the number m of
retained nulls? Theory: KL needs, for every visited T and every one-deletion neighbour T∖j,
(H_q + κ₀|e|)² ≤ (1 − δ)(log n + 2 log((2p − k)/(k + 1))), κ₀ = (1 − ρ_b)^{−1/2}, H_q² = 2 log(2⁵p) + 2 log log n.
The conjecture is: bulk (m ≥ 30) max κ₀|e|/H → 0 as p grows (≈ p^{−c} or (log p/m)^{1/2}), and end-phase (m ≤ 30)
κ₀|e| ≈ H·|I|/(k + (1 − ρ_b)/ρ_b) with imbalance |I| ≤ 1 after a short entry phase.

**What to run.** Scripts (copy as is): Theory_work/Wave2/W2-FAC-S5/numerics/bcs_core.py and s3_cc.py
(usage: `python s3_cc.py p n seed [q rb rw]`; prints one JSON line). Grid: p ∈ {2·10³, 10⁴, 5·10⁴, 2·10⁵} (if feasible),
n ∈ {10¹², 10²⁰} (log-scale only enters through thresholds; e_T itself does not depend on n), seeds 1–50; also
(q, ρ_b, ρ_w) = (3, 0.2, 0.6) at p ∈ {10⁴, 5·10⁴}, 20 seeds. Record the JSON fields cc_max, cc_max_at_m, cc_bulk_m30,
reached_S0 plus (please add, 5 lines of code) the per-run max of κ₀|e|/H over m ≥ 30, over 30 > m ≥ 5 and over m < 5,
where H = √(2 log 2p), and the imbalance #(τ > 0) − #(τ < 0) among retained nulls at m = 30, 10, 5.

**What would change the theory.** (a) If bulk max κ₀|e|/H does NOT decrease with p (stays ≥ 0.03 at p = 2·10⁵), the
conjectured KL mechanism (e_T → 0 relative to H in the bulk) is wrong. (b) If |I| ≥ 2 persists into m ≤ 5 in a positive
fraction of runs, the end-phase imbalance control of FAC-CS does not transfer. (c) Any run with reached_S0 = false at
log p/log n < 1/2 is a candidate counterexample to the path claim (please keep its seed).
Output: Theory_work/Wave2/W2-SIM/results/FAC-S5_CC/ (raw JSONL + a short summary table by p).
