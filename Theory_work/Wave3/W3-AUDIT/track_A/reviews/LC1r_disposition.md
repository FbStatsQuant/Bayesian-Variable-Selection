# LC1r disposition (lead, 2026-11-16 ~16:53 CST) — reply `LC1r_reply_opus.md`

All 12 findings accepted. T1 → STATEMENT/PROOF v3; T2 → STATEMENT/PROOF v3.

| # | tag | action |
|---|---|---|
| 1 | C | (GW-iv): 𝒜 = 𝒜° ∩ G with G := {no check evaluated before `v3_calibrate` returns fires, (C1) included}; both inclusions proved in Step 4. |
| 2 | S/C | Fields defined at leaf level; 𝒱_op seeded by clock/environment readings and check-body internal values only; a check's Boolean and what is computed from it are statistical. (GW-i) restated: statistical fields are computed from the input, earlier statistical fields and Booleans; Step 1 closes with this; (GW-iii) speaks of statistical fields. |
| 3 | F | (GW-iv) now states 𝒜° ∈ σ(𝓒°) and that W3-SAMP's "𝒜 ∈ σ(𝓒)" holds for the potential pair; CAL for 𝓒° is assigned to T5 (CAL-C), not claimed here. |
| 4 | S | Input now (X, y, seed, allocation, options); allocation reaches statistical state only at `fit$allocation` (Step 4). Changelog WEAKER/STRONGER row added. |
| 5 | C (minor) | Step 5: the `NumericalFailure` exit and its status added. |
| 6 | E | (GW-i) and Step 1: the bridge check reads only `ev`, copied into the guard record. |
| 7 | E | `v3_calib.R:50, 94` and `Sys.getenv` at `v3.R:17, 29` added. |
| 8 | E | Step 2: the no-error-path argument written out (`fail`, `cpp_cal_export`, `v3_stage_table`, incomplete branch); TLF Output contract cited for the upper-bound direction. |
| 9 | F | T2 setting R premise: i.i.d. rows with atomless coordinate marginals ((Σ_n)_jj = 1); proof line added. |
| 10 | E | T2 binary64 sentence for (BLK-c) added. |
| 11 | E | T2 downstream list: `cut_group` added (not used by rows 3.1, 3.6). |
| 12 | E | Changelog retags: (GW-i) termination and (BLK-c) setting-R clause → STRONGER. |

Next: LC1r2, a new Opus agent, on the v3 changes only.
