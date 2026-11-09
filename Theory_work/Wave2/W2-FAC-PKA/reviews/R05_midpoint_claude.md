# R05 — independent mid-point review (Claude Opus 5.5), W2-FAC-PKA

**VERDICT: CONTINUE**

Scope read: Wave2/Wave1C/Wave1 PROTOCOL.md; STATEMENT.md; SINGLETON_TARGET.md; lemmas/L0_rank.md, L1_saturation.md, L2_singleton_start_swaps.md. Primary-source fidelity checked: `Scripts/SMC_BVS/core/cpp/v3_engine.h:370-430` (local_search), `cpp/v3_score.h:40,61-70` (K=min(p,n/2), log w), `v3_preprocess.R:21-29` (ell=ceil_log2(n+p+1)), `cpp/v3_core.cpp:372-408` (ingest_tables; LS0 cap at :473). No LOG/REPORT/CHECKPOINT, other reviews, GENERAL_ASSUMPTIONS or W2-FAC-PK read. Embedded "VERIFIED" labels were not relied on; every step below was re-derived.

## 1. Step-by-step findings

**L0 (T0).** Correct. Necessity: centred columns lie in 1-perp, rank ≤ n−1 < p if p ≥ n, while the CS Gram is PD. Sufficiency: X = sqrt(n−1) Q R with Q orthonormal in 1-perp. Confirmed numerically (n=40, p=28: |1'X| ≤ 5e-15, Gram error 2e-13; R05_scratch/r05_check.py).

**L1 (T1a).** Correct as stated. Re-derived: c_u = ρθ̄(1−ρ)/(1+(u−1)ρ) and t_u = 1−ρ²u/(1+(u−1)ρ) via Σ_U^{-1}1 = 1/(1−ρ+uρ)·1. The uniform error R̂_U − R_U = O_P(sqrt(log n/n)) over all |U| ≤ 16 follows deterministically from the single max-coordinate event, because the Gram is exact. The transfer Q_U = hR̂_U/v̂ + O(1) is right (the eigenvalue gap gives ≤ h/(n+1)). The determinant increment is log n + O(1), and the prior increment is ≥ −log(2p). Counting: truth-free blocks hold ≥ p−16s0 ≥ K variables, so any |S| < K misses one, and its block intersection has size ≤ 15. No gaps. Minor: the proof only shows ratio > 1 at an O(1)-from-zero margin through δ_min; that suffices because the n/2 factor beats log n.

**L2 (S1/S2 obstruction).** I found no false step. Re-derived:
- z_j = b + dξ_j + fθ_j with b, d, f as stated (Σθ = ½θ + ½s0·1, y'y = h).
- Singleton start: log BF_j is monotone in z_j², and min log BF ≥ b_*n beats the prior cost log(2p), so |start| = K and it holds the top K−s0 null ξ. q = 1/(2c) ∈ (½,1), t < 0, μ = φ(t)/q > 0.
- Sherman–Morrison constants α, β, α′, β′, γ_k. The deletion identity −(1+γ_{k−1})t_j²/α and the swap identity were both checked algebraically, and numerically against direct matrix scores (max error 2.7e-13).
- L_K − L_{K−1} = log((n²+1)/(n+1)) + O(1/n) = log n + O(1/n), so Δ_K = ½ log n + O(1).
- Offset: bα − βfs0 = hs0/(2s) + α·sqrt(h/2)·η/s, giving O((|η|+1)/k). Correct (α − β = 1).
- Family-uniform bound sup|x_T − x_T0| = O(log^{3/2} n / n), with γ_K ≈ 1/(K+1). Correct and avoids adaptivity issues.
- Tail count of ξ ≤ −sqrt(1.5 log n) has mean ≍ n^{1/4}/sqrt(log n), which is ≫ 2L. Chebyshev is fine.
- ψ_T ≤ ‖e‖²/s² + O(1) for T ⊇ S0. In fact the sharper bound Q_T − RSS_T/s² ≤ 1 holds. With ν n d²/α → h/(2s²), M_T ≥ ½ − o(1). Swap gain ≥ M_T·V ≥ (0.75 − o(1)) log n, versus deletion ≤ 0.5 log n + O(1). The margin is ¼ log n, which is genuine.
- Truth-out swap: t_j ≈ f ≍ n, so its gain is negative. Additions are infeasible at K (code: `v3_engine.h:397`, K = min(p, n/2)).
- Induction over the family of ≤ L null-null swaps, with strictness, gives no early termination.
- Size counting in §6 with L0 = ell+s0+2, a = ell+K: centres ≥ s0+2, so neighbours ≥ s0+1. C > 1/log 2 suffices for L ≥ L0 eventually.
- The definition of N_LS0 matches code semantics: moves ≤ cap, then one further scan, and the move-limit "returned" model is a neighbour of the last scanned centre.

**Falsification (my own simulator; exact-CS sufficient statistics; singleton partition; ρ=½, σ=1, c=.75; production cap; `reviews/R05_scratch/r05_check.py`, `r05_out.json`).**
- n=200: L0 is not reached. LS0 finds S0 (finite-n, allowed by the statement).
- n=800 and n=2000, all seeds and s0 ∈ {1,2}: the first L0 moves are null-null swaps, the swap phase lasts 16–45 moves (> L0 = 14–16), the path then deletes nulls until the cap, the minimum centre size is 5–33, and S0 is not found.
- This is consistent with L2 and the stated asymptotic direction.

## 2. Issues (none blocking)

1. **L2 §2, quantile/trimmed-mean limit.** This is a sketch. Write it out (Glivenko–Cantelli for the threshold, plus a uniform-integrability tail) before the sweep.
2. **L2 §1.** The event "max|ξ_j| ≤ 2 sqrt(log n)" should say it covers the truth ξ's too (it does, since the bound is over all p). The phrase "residual variance ≥ 1" in §2 is unused; drop it or use it.
3. **L2 §5.** The stated 1 + 2/(n−1) bound is valid but loose; the sharp bound is 1. Cosmetic.
4. **Scope wording (agree with the files).** For s0=1 the obstruction is LS0-only and moot for the full method (table ingestion, `v3_core.cpp:372,408`). For s0=2 singletons it refutes only "LS0 alone scores S0 under cap ell+|start| uniformly over allowed partitions". It does not refute uniform-partition D_n → 0, production-partition discovery, or full-method consistency. Keep this exact phrasing in any headline.
5. **Status.** L2 is "PROVED (by this seat, unchecked)". The protocol still requires its falsification evidence to be filed and a cross-family line check before downstream use. This review is not that check and does not upgrade any status.

## 3. Precise remaining frontier

- **T1b (production/uniform allocation).** Truth inclusion and null allocation for production (linkage) partitions under exact CS, including tie conventions. L2 covers singletons only.
- **T2-positive or production obstruction.** Discovery for the production partition profile is OPEN. The singleton obstruction does not transfer automatically.
- **T4 cap remedy.** This is the natural next target from this route. Diagnostic only, not evidence of a limit: with cap ell+2|start| (R05_scratch/r05_cap2.py, partial output r05_cap2_partial.txt), S0 was found at n = 400–4000. The path ran null-null swaps (count growing roughly like sqrt(n/log n): 8–59), then pure null deletions down to S0. A proof needs:
  - (a) an upper bound on the swap-phase length, ≤ ell + |start| + 1 − s0 or as required;
  - (b) a deletion-phase lemma: from size K down to s0, the best move is a null deletion or a harmless swap, never a truth-out move, with no addition cycles. This needs residual/deletion bounds that are explicitly not inherited (L4.0(d), L3 E2);
  - (c) a re-charged score/preflight envelope.
- **T3.** Conditional D_n → 0 and reported-model consistency are not started. For s0 ≥ 2 singletons, full SMC/final-search discovery is unaddressed.
- **T5.** p ≥ n population-CS remains an evidence inventory only.

Continue the current route: L0–L2 are sound. The next step is the cap-remedy and deletion-phase analysis (T4/T2-positive in the singleton subclass), then the production-partition profile, keeping the LS0-only scope label.
