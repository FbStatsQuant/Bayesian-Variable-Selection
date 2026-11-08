# R02 — batch-1 lemma check (L1–L5): disposition

Reviewer: Codex gpt-6.1-sol (high), fresh `delegate_task`, files only. Reply verbatim: `reviews/R02_batch1_check_raw.md`.
Verdicts: L1 GAP; L2 CORRECT; L3, L4 CORRECT-WITH-MINOR-FIXES; L5 WRONG in (A) as stated, (B)–(D) "repairably proved".
All 53 quoted code lines match the source; reviewer reran the numerics (0 failures) and confirmed the L5(A)
counterexample on the frozen harness (the counterexample is to the lemma's wording, not to the code's behaviour).

| # | finding | disposition |
|---|---|---|
| 1 | L5(A) first form omits the final-prefix (b = J) condition; converse invalid; counterexample p = 2 | ACCEPTED. (A) restated as the all-prefix form b = 0..J plus per-block optimality; counterexample recorded in the lemma; "⇐" uses b = J explicitly; "⇒" unchanged (reviewer: correct). Attempt 2 of L5. |
| 2 | L1(ii) used the inverse-map clause that (H1) states for (e) only | ACCEPTED. The `comp` identity is now stated conditional on that clause; the lemma notes L2–L6 never use `comp`. No change to the locked (H1). Attempt 2 of L1. |
| 3 | L1(i) identified arbitrary λ, ρ with the BB prior / scorer | ACCEPTED. Abstract argument with γ₀ := exp f, Z̄₀ := Σ exp f; D0 identification labelled as method specialisation. |
| 4 | "recovers the visiting order" overclaim (L5 falsification, `lemma_probes.py`) | ACCEPTED. Wording narrowed in both files to output/count/flag checks; (C) rests on the proof. |
| 5 | L3 probe covers only feasible prefix sizes; instance counts/coverage wording | ACCEPTED. L3 text and probe docstring corrected; counts given per family type (integer-table 35,551/35,585; DATA 400; fp_stress 3,000 is (e)-only). L1 DATA evidence wording corrected. |
| 6 | L5(B): state why every nonterminal call has a child | ACCEPTED. "No dead ends" paragraph added. |

Re-check of L1 and L5 (attempt 2): new `delegate_task` → `reviews/R03_recheck_L1_L5_raw.md`.
