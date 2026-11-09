# R05 disposition (independent mid-point, fresh Codex gpt-6.1-sol xhigh; verdict CONTINUE; reply verbatim in R05_midpoint_sol.md)
| # | Sev | Item | Disposition |
|---|---|---|---|
| 1 | MINOR | (A) allows any fixed κ but asserts t_n + h_n² = O((log n)^κ); false for κ < 1 | APPLIED (editorial correction to the locked statement, logged): κ ≥ 1 WLOG in (A) and (D2) (a polylog envelope with κ < 1 is also an envelope with κ = 1). L1_toolkit already assumes κ ≥ 1; L2_NAR states κ ≥ 1 WLOG. |
Verdict CONTINUE; no FATAL/MAJOR; (D3) explicitly not covered by this review (separate checks R06a/R06b).
