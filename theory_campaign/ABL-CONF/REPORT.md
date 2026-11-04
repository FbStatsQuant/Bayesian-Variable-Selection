# ABL-CONF report: confirmatory start test (block start vs singleton factors vs prior start)

**Status: complete.** 118/118 fits terminal (107 completed, 11 capped at 75 min, 0 failed). Rule pre-registered in 49b3496 (PREREG.md, dry-run included) before any fit ran; applied unchanged by `scripts/finalize.sh` on 2026-11-04 11:35 UTC. Report written by HQ (the launching task had ended).

**Run history and deviations** (`results/final/DEVIATIONS.md`, `killed.log`): launched 2026-11-04 00:54 UTC; all three worker jobs were killed at 01:25 UTC when the launching agent's session ended (T3 stops the agent's systemd scope; `setsid` does not escape it). 4 reference fits had completed; 6 in-progress reference fits were released and re-run; no test fit had started. Relaunched 01:29 UTC as `systemd-run --user` units (launch mechanism only; queue, seeds, cap, reference and rule unchanged). Last fit 11:20 UTC.

## Verdicts (exactly as `results/final/rule_verdict.txt`)

- Guard (reference not favouring arm A, S1): **pass**, |refA − refB| = 0.029 nat vs tolerance 0.287.
- **Claim 1 (cost: at equal accuracy the block start costs less than singleton factors): INCONCLUSIVE.** Per design: S1 r001 = inconclusive; S4 r001 = holds_nondeliv; S5 r001 = holds.
  - S5 (correlated): the block start was cheaper in 10/10 pairs (sign test p = 0.001), median wall 1,116 s vs 1,639 s and evaluations 3.5e8 vs 4.5e8, with accuracy equivalent (median Δ log Ẑ error 0.033 nat, 90% interval [−0.010, 0.056]; PIP difference within ±0.002).
  - S4 (masked): **singleton factors did not deliver within the 75-min cap in 10/10 fits**; the block start delivered in 9/10 (median 1,915 s). This is a delivery result, not an equal-accuracy result.
  - S1 (favourable): no cost advantage for the block start (B cheaper in 8/10 pairs, p = 0.055, not significant); accuracy equivalent. Under the pre-registered overall rule ("licensed iff it holds on every design"), Claim 1 is therefore not licensed.
- **Claim 2 (accuracy: at equal declared budgets the prior start underestimates the evidence and is less accurate): LICENSED.** Holds on all three designs: median log Ẑ error of the prior start −13.4 (S1), −10.8 (S4), −5.7 (S5) nats vs the fixed reference, with every test fit below arm A (10/10, 9/9, 10/10); it escalated to tier 1 in 7, 9 and 8 of 10 fits and cost 2–4× the block start's wall time.

## Reference (reserved arm-A seeds, K = 8 per design)

| design | log Z_ref | se_ref | best-known = S₀ |
|---|---|---|---|
| S4 r001 c100 | −65.671 | 0.036 | FALSE (posterior miss of the truth, as in the study) |
| S5 r001 c100 | −105.402 | 0.024 | TRUE |
| S1 r001 c100 | −69.546 | 0.007 | TRUE |

Full tables: `results/final/REPORT_TABLES.md`, `rule_designs.csv`, `per_fit.csv`, `reference.csv`.

## What the paper may say
- Licensed (pre-registered): "At equal declared budgets, the prior start underestimates the evidence on all three designs tested (by 6–13 nats in median) while the block start does not."
- Per-design pre-registered results (not the overall claim): "On the correlated design S5 the block start reached the same accuracy as singleton factors at about 30% less cost (10/10 paired wins); on the masked design S4 singleton factors did not finish within 75 minutes in any of 10 seeds, while the block start finished in 9 of 10; on the favourable design S1 the two cost the same." The overall cost claim is inconclusive under the pre-registered rule and must not be stated as licensed.
- Descriptive only: all delivered fits returned the best-known model as HPM.
