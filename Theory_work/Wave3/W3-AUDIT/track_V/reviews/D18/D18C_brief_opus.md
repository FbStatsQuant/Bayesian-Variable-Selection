# D18C brief — independent check of the D18 visibility verdict (Claude Opus 5.5, high; fresh agent)

Write no files except your reply; change no git state; start no subagents. Read:
- the verdict `/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_V/reviews/D18/D18_VERDICT.md`;
- the design code `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/nots_pkg/scripts/c_designs.py` (classes `Design`,
  `LowRank`, function `_real`) and the data `/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/nots_pkg/data/riboflavin_L.csv`;
- the lemma `/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` ((VIS-0), (VIS-b), (VIS-d)).
Do NOT read `d18.py` or `d18_output.txt` until you have done steps 1–3 yourself.

1. **Structure.** From the code, confirm or refute: (a) every local matrix of D18 is a principal submatrix of
   Σ₀ = L Lᵀ + 0.1 I (with zeros across copies), so D18 has finitely many local patterns; (b) λ_min(Σ₀) = 0.1; (c) the
   placements (spread: 0, p/4, p/2, 3p/4 with θ = (1.4, −1, 1.8, −1.2); clustered: rows 0, 214, 660, 295 for p > 4088 with
   θ = (1.4, 1, 1.8, 1.2)); (d) for p ≥ 16352 the four spread truths lie in four different copies, and then
   Cov(W_j, Wᵀθ | W_U) = θ_j Var(W_j | W_U) ≥ |θ_j|·0.1 for every U — the claimed certified margin a ≥ 0.1.
2. **Reproduce independently** (your own code, R or Python; `python3` has numpy in the user site, `Rscript` exists):
   for the clustered placement, search for a set U (|U| ≤ 15) making |Cov(W_j, Wᵀθ | W_U)| small for some truth j
   (any method: greedy as in track C's `c_proxies.py:visibility_path`, or your own); report the smallest value found and
   whether it is a floating-point artefact (recompute at the found U in higher or exact precision). Also compute the
   spread placement at p = 16000 (truths at 0, 4000, 8000, 12000).
3. **Judge the verdict's claims:** spread covered with a ≥ 0.1 for p ≥ 16352; clustered not certifiable (margin ≤ ~2e-7);
   the reconciliation with track C's numbers (`/home/fb31/SMC_Theory_Department/helpers/W3-AUDIT-C/collect_all/summary.csv`,
   rows `18,RIBO,…,P4pop`).
4. Then read `d18.py` and say whether it computes what the verdict says.

Reply: per step CONFIRMED / REFUTED with numbers; any error tagged C (wrong verdict), S (overstated), E (editorial).
Last line: `D18C-VERDICT: spread=<CONFIRMED|REFUTED>; clustered=<CONFIRMED|REFUTED>; reconcile=<CONFIRMED|REFUTED>`.
