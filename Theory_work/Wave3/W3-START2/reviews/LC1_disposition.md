# LC1 disposition (lead) — line checks of the four proof files

Manifest ffeba7a53ceaa916e6b69a7a86597991ecb314673d74fe9e3d2557919d76d7af (STATEMENT v1.4.1, `lemmas/P1`–`P4`, `numerics/`,
`citecheck.py`). Two blind seats, Codex gpt-6.1-sol, reasoningEffort high.

| round | files | verdict | findings | review file |
|---|---|---|---|---|
| LC1-A | `lemmas/P1_LEADING.md`, `lemmas/P3_NEC.md` | VERIFIED, VERIFIED | none (0 CRITICAL, 0 MAJOR, 0 MINOR) | `reviews/LC1_A_line_check.md` |
| LC1-B | `lemmas/P2_OVL.md`, `lemmas/P4_BR.md` | VERIFIED, VERIFIED | none (0 CRITICAL, 0 MAJOR, 0 MINOR) | `reviews/LC1_B_line_check.md` |

Disposition: nothing to apply. The proof files and the statement are unchanged after the round. The kill budget (one
repair per changed step) was not used; no P-item is dropped.

What the seats did beyond reading (their own checks, recorded in their files): LC1-B enumerated Lemma P2.1(a), (b) on
100,404 cases (all set partitions for p ≤ 5), tested the exponent bookkeeping of P2.2 on 30,000 cases and the two
fixed-n splits of P4 on 10,000 synthetic indices, with no violation; LC1-A re-derived every constant of Lemma LEAK-0
and Proposition P1.4 and every formula of Example P3.3. Both recorded as not checked: an independent re-proof of the
accepted base results, and Monte Carlo certification of asymptotic probabilities.

Next: `REPORT.md` is added (new content, read by the council); council round R1 (Sol + Opus 5.5) on one frozen
manifest that contains the unchanged statement and proof files.
