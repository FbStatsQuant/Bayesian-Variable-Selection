# R02 disposition ("better theorem" review, Codex gpt-6-astra high)

Reviewer reply verbatim: `reviews/R02_better_theorem_astra.md`. PROTOCOL item 3: the outcome is recorded here and in
REPORT; HQ decides on strengthening. The lead adopted, as post-lock extensions (STATEMENT v1.2), only the proposals
that (i) strictly weaken a hypothesis so that the locked v1.1 statement remains a special case, (ii) the reviewer
marked LOW risk / ADOPT NOW, and (iii) could be proved and cross-checked inside this ticket. Everything else is a
recommendation to HQ.

| R02 item | proposal | reviewer | disposition |
|---|---|---|---|
| P1 | entropy budget: log\|𝒰_n\| ≤ log p + h log n, fixed h < ½, in (N-D); ν_n/log n < 1/(2 log 2) in (N-loc); same for (R1) of NA-R | LOW, ADOPT NOW | **adopted for Form F** (`lemmas/L2_NAF.md`, one line of Step 3). **Not adopted for (D-R)/(R1)**: it would re-open LOC2's Lemma NA-R (a checked, council-passed proof of another ticket); recommended to HQ |
| P2 | RSS-normalised leakage δ² ≤ ητ²_U log n in Form F | LOW, ADOPT NOW | **adopted**: `lemmas/L1b_rss.md` (Lemma τ, Lemma B2τ). Reviewer's caveat kept: this does not unify F and R |
| P3a | localisation rate r_n = o((n log n)^{−1/4}) instead of n^{−2} | LOW, ADOPT NOW | **adopted**: `lemmas/L3b_rate.md` (the prover's L3 §8 independently proved the case C√(log n/n)) |
| P3b | standardised leak budget n·aᵀG⁻¹a/v ≤ η log n (leaks of order √(log n/n)) | MEDIUM, SEPARATE TICKET | not adopted; recommended |
| P4 | joint block visibility (JV_b) in the block-relative variant | LOW, ADOPT NOW (block-relative) | **not adopted in this ticket**, recommended. Reason: the comparison S̃ vs S̃ ∪ M adds \|M\| ≥ 2 elements and needs k̃ + \|M\| ≤ K; (L-feas) gives only k̃ ≤ 2\|Q\| + 32s₀ < K, i.e. room for one element, so (L-feas) would have to be strengthened to K ≥ 2\|Q\| + 33s₀ (harmless, but a change of a locked hypothesis). The reviewer's own caveat: no gain in the partition-free form |
| P5 | polynomial \|Q\| ≤ n^b, b < ¼ (and b < ½ − η/2 − √(2Aη) in F), design-agnostic | MEDIUM, SEPARATE TICKET, high priority | not adopted; **recommended to HQ as the most valuable follow-up** |
| P6 | dropping (N)/(D-R) | HIGH, open | not adopted; recorded as open in SHARPNESS.md together with the reviewer's analysis (the weak-extra inequality min_e D_e ≤ ‖(P_Q − P_{S₀})ε‖²/(φ₀²\|E\|) controls deletions but not swaps; path sets are ε-dependent) |
| P7 | archive-level certification corollary (returned = S₀, local_certified, moves, scans) | LOW, ADOPT NOW | **adopted** as a corollary of RM-0(a) (`lemmas/L0_core.md`) |

No counterexample to any locked assumption was produced by R02 ("I do not have a counterexample satisfying all those
hypotheses in the small-Q regime").
