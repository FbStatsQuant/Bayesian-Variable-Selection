# SL1+LC2 (Sol gate read) disposition (lead, 2026-11-16 18:00 CST) — reply `SL1LC2_reply_sol.md`

Verdict: T1 LOCK WITH CHANGES / VERIFIED WITH AMENDMENTS; T2 LOCK WITH CHANGES / VERIFIED WITH AMENDMENTS. No C finding,
so (manager 11-16) no further Claude re-read. All three required changes applied; T1 → v5, T2 → v5; T5 PROOF Step 2
aligned with T1's new definition. The changed rows go to the council batch (statement-change checks in the Sol seat).

| # | tag | action |
|---|---|---|
| 1 | S (T1) | The allocation argument and every copy (`fit$allocation`, the normalised local, `cpp_runtime_new`'s `hours` and `elapsed_before`) are internal values; (GW-i), (GW-iv): statistical state is a function of (X, y, seed, options); PROOF Step 4 rewritten; T5 PROOF Step 2 aligned. |
| 2 | F (T2) | C_b(X) := {j + 1 : j ∈ make_blocks(D(X), B)_b}; `st.blocks` = internal representation, reported blocks via `to_orig`; the shift added at the end of the (BLK-b) proof. |
| 3 | S (T2) | Binary64 remark qualified by successful execution with every integer size, index and allocation size representable (e.g. `2 * p - 1` at `cpp/v3_blocks.h:49`). |

Also before the council freeze (manager question 11-16): T10 PROOF v2.1 gives the exact R-representability bound for
X7/X8 (n, p ≤ 2³¹ − 1 from `dim`/`int`; `le` ≤ 32; `cap_ll` ≤ 32 + 2³⁰ − 1 < INT_MAX).
