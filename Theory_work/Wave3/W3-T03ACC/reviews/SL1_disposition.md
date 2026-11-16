# SL1 disposition (lead, 2026-11-16) — review `reviews/SL1_statement_lock_sol.md` on MANIFEST 161f3f56…

Verdict LOCK WITH CHANGES. All required changes and all optional suggestions accepted and applied → STATEMENT v1.1 LOCKED
(sha256 a2e399a8d30873713a950f5c16de58614901dbf6f8ad9d6e40285f8556ae6bef). Changelog rows: STATEMENT §6.

| item | class | disposition | where applied |
|---|---|---|---|
| Req. 1: restore "A fixed"; expose A ≥ 1 as a source discrepancy; same-A check in the line checks | CRITICAL, F | ACCEPTED, applied in the required words | STATEMENT §0, R1, §4 item 3; PLAN §2; LC-A N4, LC-B N5, LC-C N6 |
| Req. 2: close the [P1] dependency list (`prop:closed`, `thm:T01i`, `thm:T01ii`, `lem:spec`(a)–(e)) and LC-A coverage | MAJOR, E | ACCEPTED | STATEMENT §5; PLAN LC-A; BRIEF_LC_A |
| Req. 3: m♯_n ≤ K only for n with s₀ ≤ K | MINOR, E | ACCEPTED, required words | STATEMENT §2 |
| Opt. 1: PLAN section labels; `lem:signal` proof is a shared dependency | — | ACCEPTED | PLAN §2 |
| Opt. 2: scaling letter d in clause 5 | — | ACCEPTED | STATEMENT §3 clause 5 |
| Opt. 3: pointer to the record's mandatory scope paragraph | — | ACCEPTED | STATEMENT §3 "What the theorem is about" |
| SL1 check 2 ruling on p = 1: no p ≥ 2 hypothesis needed | — | ADOPTED; LC-C records the specialization | STATEMENT §4 item 4; LC-C N7 |

Consequence for the manager's CP1 instruction: neither A ≥ 1 nor p ≥ 2 is added, so no clause is WEAKER than the record at
v1.1. If a line check finds a step that needs A ≥ 1, that becomes a WEAKER changelog row and is named in CP3.
No separate statement-change check: v1.1 applies the lock reviewer's own required text, and every row is EQUAL vs the record.
