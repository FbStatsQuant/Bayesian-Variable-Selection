# R06 disposition — L6_poly (D3) checks
R06a (Claude Opus 5.5 high, cross-family to the Codex author; reply verbatim R06a_L6_check_opus.md): VERIFIED-WITH-AMENDMENTS.
R06b (fresh Codex gpt-6.1-sol xhigh; reply verbatim R06b_L6_check_sol.md): VERIFIED-WITH-AMENDMENTS.
| # | Sev | Item | Disposition |
|---|---|---|---|
| R06b-1 | MINOR | (P13) τ may fall below (P10)'s range t ≥ (log n)/2 | APPLIED: max(2λ, ½) < τ < 1 − 2b (nonempty since b < ¼). Cutoff unchanged. |
| R06a-1 | MINOR | IR cites L2_CT:19; Schur/Neumann steps (a),(b) unstated | APPLIED: cite L2_CT.md:22–28 algebra; (a), (b) written. |
| R06a-2 | MINOR | D description inconsistent; any fixed D > 0 works | APPLIED. |
| R06a-3 | MINOR | rate audit note on τ > ½ | APPLIED; overlong line re-wrapped. |
| R06a-4 | NIT | symbol overloads | NOT APPLIED (renaming risks new errors); overloads flagged in the status header. |
| R06a-5 | NIT | spell out (P8) expansion | Recorded in the reply (z_U − z₀ = [−a′R⁻¹b + z₀(1 − Δ)]/Δ); not needed for correctness. |
| R06a-6 | NIT | weak prover numerics | Noted; R06a's stronger check (reviews/R06a_scratch/check.py, p = 600, adversarial |U| = 15) found no counterexample. |
Both checks: no FATAL/MAJOR; α₀ = 17/2 confirmed as the infimum for this argument (not a necessity statement).
