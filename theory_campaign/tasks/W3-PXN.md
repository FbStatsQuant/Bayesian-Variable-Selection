# W3-PXN: A p ≫ n family carrying all of T38(b)'s premises jointly

The study design is n = 200 with p ∈ {500, 1000}, so p ≫ n. The joint-premise families found so far are below p:
- W1-T38E: CF(c), with p = n^{3/4};
- W1-EXP: the exact-Gram linked-hub family LH, with p ≤ n − 1.

Their p ≫ n versions are CONJECTURE (W1-EXP §4.3 has an iid-Gaussian PROOF SKETCH). Read `theory_campaign/W1-T38E/` and `theory_campaign/W1-EXP/` on branches `theory/W1-T38E` and `theory/W1-EXP`.

**Goal:** prove that one design family with p_n ≥ n^{1+ε}, ideally an iid-Gaussian design close to the study's correlated scenarios, satisfies jointly, on the actual X-dependent block partition:
- G, R, SE-blk (or the anchored SE of W1-T03R);
- BM-∞;
- T27-type masking: π₀(S₀) → 0 at the CL(L) rate;
- near-truth start mass π₀(𝓡_d) ≥ b_n;
- eligibility of the start mode S̃₀ for LS0, or the D2 one-flip-neighbour condition;
- the repair input TD′ (W1-T37R Theorem A);
- π(S₀) → 1.

Prove what you can. State exactly which premise fails or stays open, and why. Check the predictions numerically with exact or very accurate computation, using p up to a few hundred if exact enumeration isn't feasible: the start sampler is block-wise, so π₀ is computable by convolution. Also say whether the study's own n = 200 masking (median π₀(S₀) ~ 1e-12 in S1/S3/S4/S6) is consistent with the "weak-signal masking" explanation W1-EXP proposes.

**Deliverable:** `theory_campaign/W3-PXN/REPORT.md` with statements, proofs, numerics and the confidence card.
