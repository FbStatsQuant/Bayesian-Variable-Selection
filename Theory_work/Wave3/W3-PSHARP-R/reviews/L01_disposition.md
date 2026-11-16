# L01 disposition — statement lock (Sol gpt-6.1-sol, high; NORMAL mode; fresh, blind first read)

Review: `reviews/L01_statement_lock_sol.md` (verbatim). Brief: `reviews/BRIEF_L01_sol.md`. Verdict: LOCK-WITH-AMENDMENTS;
FATAL 0, MAJOR 1, MINOR 3, NIT 0. No counterexample to any claim; every claim item derived analytically by the reviewer.

| finding | decision | change (STATEMENT v1.1 / PLAN v1.1) |
|---|---|---|
| F1 MAJOR — §0 row R1 "r_n exact in expectation for every p" is false over the class (huge p under (W-sph-E) gives E δ_n ≫ r_n); summary only | ACCEPT | R1 row now: "the √(log n) expectation obstruction includes bounded p; r_n is exact in expectation where the quoted expectation upper bound applies". Same narrowing in READER_DELTA v0.2 §3 remark. §4.1 unchanged (reviewer: supported). |
| F2 MINOR — PLAN Lemma T: E Y equals the sum over P(G_j), not N·min | ACCEPT | PLAN §2.1 corrected; c > 0, T > 0 stated. |
| F3 MINOR — rank condition of (W-sph-E) removable in A2-E via PARENT B1 | ACCEPT (adopted strengthening, pre-lock) | §3.3 drops the rank condition; §6 adds `W3-PSHARP:B`@1.0.0 (B1) as consumed; PLAN §2.5 records the step. |
| F4 MINOR — expectation consequence of A2C is free | ACCEPT (adopted, pre-lock) | §3.4 adds limsup E π(S₀) ≤ e^{−λ}, liminf E δ_n ≥ 1 − e^{−λ}; §5 bullet reworded. |
| remarks (not findings): meaning of "same o(·) sequences"; empty sub-block case in A2-E; fixed J₀ in A2C | ACCEPT | §3.1 wording (common deterministic sequences); PLAN §2.5, §2.6 notes. |

Statement locked as v1.1. All changes made before the lock; changelog rows record them (tags confirmed in substance by
the review's own analysis; no post-lock statement-change check is owed).
