# Council XR1 disposition (lead, 2026-11-16) — X1, X3, X5, T14; MANIFEST 0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c

- Sol (`XR1_council_sol.md`): 9.4 PASS; X1, X3, X5, T14 ACCEPT; 2 E.
- Opus (`XR1_council_opus.md`): 8.5 FAIL; X1, X3, X5 ACCEPT; T14 REJECT on F1 (F; claim true): T14's proof bounded
  |start mode| through T9 (TDP-a, b), which assume EX-A/(H2-FP), while T14 claims to use only R's dim limit and the
  options. 8 E findings.
- `bind` XR1: refused (Opus gates=FAIL). Diff round XR2 follows.

Repairs (T14 only; X1, X3, X5 kept byte-identical):
| finding | action |
|---|---|
| Opus F1 | T14 PROOF v1 Step 3: structural bound |m.S| ≤ max(k̂, 0) ≤ K from the integer structure of `start_mode` (k̂ scanned over 0..K; leaves of `rec` have size k̂; `mode_tie_dp` keeps feasibility to the end, so IN is a path set of size k̂), valid in any arithmetic; T9 no longer cited; closing sentence corrected. |
| Opus E7, E8 | T14 STATEMENT v1: ℓ_n ∈ [3, 32]; changelog added. |

Editorial batch (not applied; X items accepted by both seats): Sol E1 (X5 STATEMENT:26 joint-law identity with ° marks),
Sol E2 / Opus E3 (X3 summary: "any p ≥ 2"), Opus E1 (X1: ledger attribution), E2 (X1: off-path change list wording),
E4 (X5: SOURCE_PoolZ copy cut mid-sentence in Remark (iii) — copy lines 12–38), E5 (X5 vs T5 CAL-d wording: "CAL, in
the sense of T5 CAL-b (a function of data and streams 0–9 for every input), fails for the actual record off G"), E6
(X5: MEAS-J argued by analogy; "only under" phrasing).
