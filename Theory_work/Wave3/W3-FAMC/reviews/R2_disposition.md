# W3-FAMC — R2 disposition (lead, Claude Opus 5.5 high; 2026-11-17)

Input: `reviews/R2_diff_sol.md` (gpt-6.2-sol, codex, high; round=R2; 4bb2b603 → 82fb5122; PASS WITH CHANGES). R1: 9
RESOLVED, 2 PARTIAL (S1 → N1, N2; S3 → N3, N4). Each point was triaged against the acceptance filter: **5/5 ACCEPT**, no
false positive. All the fixes are confined to the reader version §1R, the class table §2 and the §4 wording. §1 and the
proof are unchanged.

| id | sev | triage | why genuine | fix (STATEMENT v1.3) |
|---|---|---|---|---|
| N1 | MAJOR | ACCEPT | §1R's group-sign wording omitted the link between the flips and the coefficient signs: θ = (1, −2) at correlation ½ satisfies the wording and cancels | §1R: one flip system, partial correlations ≥ 0, *and* a common flipped coefficient sign, as (BLK-s); AR parity and ρ = 0 spelled out |
| N2 | MINOR | ACCEPT | "every run" lost "admissible", n ≥ 3 and Theorem 6's qualifications | §1R delivery sentence restored |
| N3 | MINOR | ACCEPT | the floor was listed under (A1)–(A2) with one class; the compliance file classes the two floors 1 and 2b | two (A5) rows; in FAMC both are implied by the design |
| N4 | MINOR | ACCEPT | (S1)'s class-1 source is line 18, not line 20 | separate (S1) and (S2) rows |
| N5 | MINOR | ACCEPT | "in the FAMC manifest" was premature before the freeze | evidence = checked-in report; manifest inclusion pending the freeze |

No further Sol round is owed under Tier B (one line check plus one diff round). The v1.3 fixes are wording only and are
listed for the council's diff check.
