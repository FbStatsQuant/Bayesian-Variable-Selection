# SHARP3 request — better-gate API Fable sharpness batch for uncovered five-pillar rows (W3-READER leg 2, 2026-11-16)

For the Theory Department manager → HQ (HQ builds and submits; HQ's credits; Fable via the Console key). Format: as
`Theory_work/Wave3/API_AUDIT/audit_batch.py` mode `sharp2` (system prompt `SYSTEM_SHARP`, one ticket's working files
per request), but **one claim per request**: the earlier multi-claim requests for these two tickets hit
`max_tokens` twice (sharp1 f20/f21; sharp1b f20 partial, f21 no text; `API_AUDIT/sharp1b/TRIAGE.md:83-91`).

## Coverage survey (scope of `BRIEF_LEG2_GATES.md`)
| Card row | Master(s) | Existing blind sharpness verdict | Covered? |
|---|---|---|---|
| 1.1 | W3-POST:Thm-1 (= SOP:TH09 content) | sharp1 f15 IMPROVABLE-EASY | yes |
| 1.2 | W2-APP:POST | sharp1 f06 IMPROVABLE-EASY | yes |
| 1.3 | W3-PSHARP:A, B | sharp2 f02: A IMPROVABLE-EASY, B SHARP | yes |
| 1.4 (MISR, moved from 3.4) | W3-MISR:Cor-G(b) | sharp2 f01 IMPROVABLE-EASY | yes |
| 3.1 | W3-RM2:RM2-R; W3-RM:RM-0; W2-UNI:F-UNI | sharp2 f03; sharp1b f19; sharp1 f14 (all IMPROVABLE-EASY) | yes |
| 3.2 | W3-RM2:RM2-F | sharp2 f03 IMPROVABLE-EASY | yes |
| 3.3 | W3-START2:START-R; W3-START:FLOOR | sharp2 f09 IMPROVABLE-EASY; sharp2 f04 SHARP | yes |
| 3.5 | W1-N1:Thm-N1 | sharp1 f01 IMPROVABLE-EASY | yes |
| 3.6 | W3-SAMP:C, TR, LT♯, D | sharp1 f20 truncated; sharp1b f20 partial (D reviewed, LT♯ started; two items "to be confirmed by the re-run") | **no** |
| 3.7 | W3-SCR:A1 | sharp1 f21 truncated; sharp1b f21 no text | **no** |

## Request list (5 requests, one claim each)
| req | claim id@version | statement file:lines | ticket files to attach (as `sharp2`) | note for HQ |
|---|---|---|---|---|
| g00 | `W3-SAMP:C@1.1.1` | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:149-163` | `Theory_work/Wave3/W3-SAMP/` STATEMENT, REPORT, ASSUMPTION_MAP, `lemmas/C_theorem.md`, `lemmas/MR_identities.md`, `lemmas/ST_stay.md` | consistency of printed Ẑ, PIP, MPM (row 3.6 master) |
| g01 | `W3-SAMP:TR@2.1.1` | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:165-177` | same + `lemmas/TR_theorem.md` | — |
| g02 | `W3-SAMP:LT#@2.0.1` | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:126-140` | same + `lemmas/LT_theorem.md` | confirm/deny sharp1b f20 item "NC_r for every r ≤ 4 more than needed" |
| g03 | `W3-SAMP:D@2.1.1` | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:97-105` | same + `lemmas/D_theorem.md`, `lemmas/PC_completed.md` | confirm/deny sharp1b f20 item "P-MAP localisable to 𝒜" |
| g04 | `W3-SCR:A1@1.0.0` | `Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163` (with its parent `W3-SCR:SCR-A@1.0.0`, :79-85, as context) | `Theory_work/Wave3/W3-SCR/` STATEMENT, REPORT, ASSUMPTION_MAP, CODE_CHECK, `lemmas/L3_screening.md`, `lemmas/L4_bridges.md`, `lemmas/L6_sharp.md` | row 3.7 master |

Equivalent spec for `audit_batch.py`: a mode `sharp3` with
`SHARP3_IDS = ["W3-SAMP:C", "W3-SAMP:TR", "W3-SAMP:LT#", "W3-SAMP:D", "W3-SCR:A1"]`, one claim per request, attached
files as above, `max_tokens` 24000 as for `sharp`. Estimated size: 5 requests × (~60–90k input tokens, ≤ 24k output) —
within the ~$15–25 HQ quoted.

## What W3-READER does with the results
Triage in `API_AUDIT/sharp3/TRIAGE.md` style (A adopted / B ticket / C declined / D remark), recorded in
`GATES.md` rows 3.6 and 3.7 and in `gates_staged.tsv` (better, better-proposals). If declined or delayed past Thu
11-19 18:00 CT, rows 3.6 and 3.7 carry `better: PENDING (SHARP3)` in the staged file; nothing else is blocked.
