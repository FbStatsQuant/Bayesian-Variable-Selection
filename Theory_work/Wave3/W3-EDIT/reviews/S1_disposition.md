# S1 disposition (lead, 2026-11-15 21:48 CST)

Sol S1 (`S1_editorial_check_sol.md`): `EDITORIAL-CHECK verdict=FAIL rows=29 changes_math=0 incorrect=1`.
28 rows EDITORIAL; I4-S1 INCORRECT (incomplete). No hunk changes mathematics; no orphan edits, no missing edits.

| finding | tag | decision | action |
|---|---|---|---|
| S1: `W3-MISR/ASSUMPTION_MAP.md:17` still ends "— **weakenable, not removable**" after the row was qualified | S | ACCEPT | Sol's exact text applied: "— **numerical evidence compatible with weakening; non-removability suggested, not proved**". Ledger I4-S1 extended. |
| E1: ledger I1-M45 note "[fp_example.py sets no cap]" is wrong (fp_example.py:10,22 pass 10**6 = default, n3lib.py:21) | E | ACCEPT | Ledger note corrected; the lemma text was already correct. |

Repair re-check: one line (ASSUMPTION_MAP.md:17), sent to a fresh Sol agent (S1b), diff only, per v4 §5.5 (same model, fresh thread, diff since S1).
