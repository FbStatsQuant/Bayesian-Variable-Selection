# W5-VMASK plan (independent referee of W3-PXN and W4-T38FULL masked-regime claims)

1. Paper verification, in task order: PXN Lemma B, Lemma Tr, P3 (+ W1-EXP L1.1/1.2/1.4 generality), P1, P3–P8,
   T38FULL LS-score, Lemma M, Theorem b1, LH-LAT. Verdict per step: VERIFIED / GAP / ERROR.
2. Margin consistency (PXN P6 c2 vs T38FULL m0 vs brute-force population minimum) on a parameter grid.
3. Independent numerics (own scorer, own partition port, own generator via unit Cholesky):
   LH-iid table (A, B; n = 200, 400, 800), LH exact-Gram LS0 (G = 12, g = 9), Lemma B KS tests,
   (L)-failure rate, adversarial designs (|psi| near rho; strongly correlated null group).
4. Method faithfulness: local_search and start_mode vs the modelled LS0.
5. REPORT.md, REPAIRS.md, confidence card.
