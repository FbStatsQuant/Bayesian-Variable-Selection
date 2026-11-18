# A4 post-check (Opus): fidelity of the editorial diff (checked snapshot to current)

Scope: `.rc_tmp/a4_postcheck_diff.patch`, checked against the A4_R2 disposition, D1 (`smc_bvs_method.tex`), card v1.13, and TRACK_B / WRITING_DELTA v1.4. Only non-OK hunks are listed.

| id | file:line | issue | source | fix |
|---|---|---|---|---|
| P1 | s3_method.tex:183-185 | CHANGED-CLAIM. "The calibration starts at tier $i=0$, with $N_0$ particles per island, and moves at most once to tier $i=1$ ($4N_0$ particles)". The calibration's own islands (the pilot and the diagnostics) have $\Nc_i=4^i\Nc_0$ particles ($\approx2{,}048$ at tier 0), not $N_0$. $N_i=4^iN_0$ is the final-run size that the tier fixes. | D1 §m-calibration ("At tier $i$ these islands have $\Nc_i:=4^i\Nc_0$ particles"); Algorithm 1, steps 2 and 4 | "...starts at tier $i=0$ and moves at most once to tier $i=1$, which multiplies by four both its own islands' particles ($\Nc_0$) and the final run's ($N_0$), when..." |
| P2 | s3_method.tex:202-203 | CHANGED-CLAIM (scope broadened). "whatever a stopped run returns is flagged incomplete, and the results do not cover stopped runs". In D1, a run with a constant response or no retained predictor stops and returns the empty model, which is not marked incomplete; §3 Stage 1 says so too. Only later stops return a best-so-far model marked incomplete. The old text ("anything else it returns", meaning a time-guard stop) matched card rows 3.5 and 3.6. | D1 "Runs without estimates" (lines 586-591); card v1.13 rows 3.5 and 3.6 [GUARD-W] | "whatever else a run stopped after the calibration has started returns is flagged incomplete, and the results do not cover it" |
| P3 | s5_assumptions.tex:70 | LOST (minor). In the "In words" cell of the Signal size row of Table 3, "nonzero (fixed in Thms post-random, reported, outputs; ...)" became "nonzero (beta-min in Thm post-fixed)". The condition that the signals are fixed in Theorems 1, 3 and 4 is dropped. | TRACK_B v1.4 B4 ("fixed nonzero or beta-min") | restore "fixed nonzero in Thms \ref{thm:post-random}, \ref{thm:reported}, \ref{thm:outputs}; beta-min in Thm \ref{thm:post-fixed}" |
| P4 | s4_results.tex:464-465 | CHANGED-CLAIM (provenance). Result 5(c): the measurements are now called "single-draw measurements from our simulation experiments". They are Engineering measurements (D-17), not the simulation studies, which §1 says are reported separately. | card v1.13 line 159-163 (moderate-$n$ observation, "Engineering measurement, row D-17") | "single-draw measurements from our engineering runs" |
| P5 | s4_results.tex:365 | CHANGED-CLAIM (minor, plausible). The Prop. unbiased status box changed "at the code of record" to "against the released code". This asserts that the code has been released, and it no longer names the pinned version that was checked. The status itself is unchanged. | card v1.13 row 3.5 (checks at pinned code lines) | "against the code described in Section~\ref{sec:method}" (or "the code version of record") |

Checked and OK. These cover the seven focus items.
- Status boxes: the R3, Thm 3.2 and R5 (a)/(b) statuses are unchanged; only the wording changed.
- Table 3: the uniform one-word cells are exactly GL, SP (with Thm 1 caveat), V, the leakage set, local regressions and NL, matching WRITING_DELTA v1.4. Every "By ..." pointer resolves to a §5.3 head that keeps the conditional sentence.
- Scope lines: R2 ("every design") and R5 match the TRACK_B reading. §5.4 lost no condition: the numerical-check finding for visibility now sits at s5:187, and the $p\gg\sqrt n$ reason at s5:198.
- Result 4: "In words" keeps the indicator, the event intersection and completion. "Why it matters" keeps "on the event that the calibration succeeds". The "no claim how likely" text is kept in Remark (i) and §6.
- §3 definitions: the ESS fraction on candidate models, the trigger, $N_i$, the 𝓔_cal time-guard sentence and the resource-limit estimate agree with D1, apart from P1 and P2.
- Abstract: "attained on two families of designs" agrees with R5(b), the asmlist and card row 1.3, and is weaker than before.
- Result 5: the moved text is identical. Only the scope line was added and status (c) was reworded (P4).

Not a claim change: the notation table in appendices.tex:16 and :155 still uses $C_b$ and $h_b$, while §3 now uses $C_k$ and $h_k$.

POSTCHECK: ISSUES (5)
