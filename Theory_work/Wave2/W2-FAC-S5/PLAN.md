# W2-FAC-S5 — PLAN

1. Numerics first (done 08:41–09:25): bcs_core.py (exact closed form, validated vs FACB fac_core.scan: bcs_selftest_out.txt),
   S1 path grid (27 runs), S2 re-add invariants. Next: S3 = CC_n margin along Π (incl. one-deletion sets T∖j),
   S4 = start-mode falsification for BCS with N₀ ≠ ∅ (FACB bvs_core start_mode on exact-Gram S5).
2. Lemmas (one file each): L1 exact two-level reduction (closed form; τ = group part + κ·e; |τ| ≤ |A| + κ₀|e|; gain
   formulas with M_T = ½(1+o); size terms); L2 start mode (BCS partial covariances via inverse-M-matrix; FACB L2 pattern);
   L3 event E_n (H_q union bound over (null, mate-set) pairs; χ² bounds; truth-signal bounds); L4 path lemma (C2-R);
   L5 assembly (C3-R), (C4-R) — FACB L5 pattern with D_n ≤ P(CCᶜ) + o(1).
3. Tier 2: Lemma KL (P(CC_n) → 1). Parallel prover: Codex gpt-6.1-sol xhigh with a self-contained brief
   (reviews/KL_BRIEF.md) while the lead writes Tier 1. Accept only with a cross-family check; else PARTIAL with KL as the
   obstruction.
4. Reviews: R01 statement lock (Sol high); lemma checks (L1–L3 Sol high; L4 Sol xhigh; L5 Sol high); mid-point (fresh Sol
   xhigh); exhaustive sweep (Sol xhigh); council (Sol xhigh + Opus high); citecheck.
