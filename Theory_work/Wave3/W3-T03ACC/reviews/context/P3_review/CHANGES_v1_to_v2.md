# Changes from PROOF_v1 to PROOF_v2 (all exposition; no mathematical step changed)

Findings of both round-1 reviewers were all exposition level. v2 applies them as follows.
1. Notation: the contrast response vector is renamed y_c (was w); w(·) is now only the prior weight. θ_n (Lemma 11) renamed υ_n; the random sum U_n renamed Υ_n. A notation sentence is added at the end of §1 conventions.
2. §1 Plan: typo fixed ("one size at a time").
3. §1 conventions: added why n_0 can be taken uniform in the design sequence (δ_n, ε_n, q_n depend on the design only through m_n and are monotone in it; replace m_n by C_m log n), and that under BM-∞ one extra sequence-dependent threshold enters in Step 1.
4. Lemma 7(a): the Laurent–Massart attribution is removed; the bounds are proved in full.
5. §7 opening: scope stated (n ≥ n_0 in (i), (iv), Steps 0–1; the deterministic parts of (ii) and (iii) hold for every n); added the fact that a bound for n ≥ n_0, or a lim_L limsup_n bound, gives tightness over all n.
6. §7 (ii): stated that the PIP bound holds for every data set and every n with s_0 ≤ K, and trivially when s_0 > K.
7. §7 (iii): "bounded convergence" replaced by the direct bound E[1−π(S_0)] ≤ ε + P(1−π(S_0) > ε).
