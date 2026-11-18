# case3 · gpt-6.1-sol (codex, reasoningEffort high), SCORED run (clean control)

Wrapper: chunks of 120 lines; no other file. Run about 19:23 to 19:26 CT (wall ≈ 3 min). Full reply: T3 child thread "SOL62 A/B case3 · gpt-6.1-sol". Header line correct.

**Verdict line:** `K2-VERDICT: 2 RESOLVED, 0 NOT RESOLVED; 0 FATAL, 0 MAJOR, 0 MINOR, 0 NIT new findings; 2 VERIFIED, 0 NOT-VERIFIED`. This is **identical to the known answer and to the stored 6.1 original.**

**Repairs:**
- **K1-2 (n ≥ 5 → 9):** checked with log 9/9 ≈ 0.244136 < ¼ and the monotonicity of log n / n.
- **K1-3 (support stratification):** Borel argument given.

**Other checks:** change completeness was checked against the whole-file snapshots. DEPS rows are STALE (as anticipated). External sources are marked "not supplied" without raising a finding.

**Score.**
- Known answer: correct (no finding expected; none raised).
- False: 0.
- Nitpick: 0.
- Fidelity: exact.
