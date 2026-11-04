# T20 (T15): Local-search semantics and conditional repair

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** deterministic component validity and statistical consistency. Clauses (i)–(ii): **core**; (iii) ORTH repair: **secondary**; (iv) COH extension: **optional**. v2's SE-only "every best move is a true move" clause is withdrawn.

## Definitions used
The local search: from a centre S_c, each scan scores every feasible flip and swap of the centre; best-improvement moves, at most ℓ moves, then one extra scan; `local_certified` flag; running all-scored HPM Ŝ; E_n := {S₀ is the strict global maximiser of F} (00_COMMON §§1–2; THEORY_BRIEF §2).

## Assumptions
EX-A and execution of the relevant scans for (i)–(ii); G, R, SE and BM-C (through T03) for the statistical reading; ORTH and BM-∞ for (iii); COH and BM-∞ for (iv).

## Precise statement
(i) [certificate] `local_certified` certifies exactly that the returned model was itself scanned as a centre and had no strictly improving feasible flip or swap within the cap; equal-score neighbours are allowed; weak local maximality only. All scanned candidates, including rejected ones, enter the running HPM comparison; a model first discovered by the final extra scan can be the reported HPM without a certificate.
(ii) [one neighbour] On E_n, every completed scan from a feasible flip-or-swap neighbour of S₀ scores S₀; if a move remains the search moves to S₀; if the subsequent scan executes it certifies S₀. Under T03, P₀(E_n) → 1, and a sufficient global margin is min_{S≠S₀}{F(S₀) − F(S)} ≥ log[π(S₀)/(1−π(S₀))] ≥ ½ log n − ½ log log n − O_{P₀}(1).
(iii) [ORTH repair] Under G, R, ORTH, BM-∞: with probability → 1, simultaneously for every feasible starting centre with |S_c Δ S₀| ≤ ℓ, each selected best improvement reduces |S Δ S₀| (by 1 for a true addition or noise deletion, by 2 for a true-for-noise swap); the search reaches S₀ within |S_c Δ S₀| moves and the extra scan certifies it. Equal magnitudes are unnecessary.
(iv) [COH extension] The same conclusion under G, R, COH, BM-∞, with the obligation of proving monotonicity of the selected best move uniformly over the centres with the integrated-variance score.
(v) [scope] Posterior concentration does not imply the entry condition of (iii), nor bound an arbitrary centre's size by m_n; the move limit can bind; a later search repeats an earlier ascent only if its centre and comparisons are unchanged. Under SE alone a signal-bearing proxy can win the first improvement from ∅ (correlation matrix [[1,0,.65],[0,1,.65],[.65,.65,1]], S₀ = {1,2}: eigenvalue floor 0.081 > 0, proxy population fit gain 1.69 vs 1 per true singleton).

## Dependencies
Builds on: T03, T05, T11. Used by: T21, T24, T31.

## Numerical evidence (provisional)
provisional evidence (Sol check J3): on the design above with θ = (1,1,0), best-improvement paths from ∅ at n = 64, 512, 2048 select the proxy first and recover S₀ afterwards; at n = 128 the path stops at a certified wrong local maximum although S₀ is globally best; one-neighbour scoring/certification semantics confirmed; a truth first hit on the final scan is scored but not certified. Files: judge/sol1/J3_LOCAL_SEARCH.md.

## Proof-route hint (optional)
(i)–(ii): frozen-centre scan rule and the all-scored ledger (T11). (iii): the gain statistics G_l do not depend on the centre under ORTH; one no-lucky event {max_l G_l < x_k for all k ≤ s₀+ℓ} of probability → 1 separates true-coordinate gains from noise gains in the exact integrated odds. (iv): control residualised gains uniformly over admissible centres (deviation ≤ 4c_n|T| log p/φ₀²(1+o(1)) from ORTH). Hardest step: best-move ordering after integrating variance. *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
