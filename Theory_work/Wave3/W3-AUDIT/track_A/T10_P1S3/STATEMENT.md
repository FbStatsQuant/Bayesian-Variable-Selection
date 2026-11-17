# T10 · Re-audit P1/S.3 (every no-output exit of the shipped fit is inventoried) — STATEMENT v2 (draft, not locked)

Track A item T10 (`AUDIT.md` §6; CHECKPOINT_1 annex order 10). Tier B (second-seat code reading of two audits whose
status is "AUDITED (code reading)"). **Lean target: no.** Blocks row 3.1, delivery clause only (`W2-UNI:F-UNI`:
"P1/S.3 keep 'AUDITED (code reading)'", `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:12-13`).

## Sources
- `C-DLV:P1-Inventory` "AUDITED (code reading)": "every exit of `v3_fit` without estimates is one of the listed sites"
  (`Theory_work/Wave1C/C-DLV/STATEMENT.md:52-53`); the list `Theory_work/Wave1C/C-DLV/INVENTORY.md:15-93` (v2, with the
  2026-11-16 erratum X7–X8).
- `C-DLV:L2-S3` "AUDITED (code reading)": D2 unreachable and the X2 invariants (i)–(vii) (+ (viii)–(ix) by erratum)
  (`Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md:37-72`).
- Both were written against a pre-LS0 core (their line numbers do not match the pin; LS0 is listed as spec-only,
  `Theory_work/Wave1C/C-DLV/INVENTORY.md:71-77`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); shipped `v3_fit`, default options (`ls0 = TRUE`,
`grid_fallback = TRUE`).

## Claim (re-audit)
On valid declared inputs (seed an integer in [1, 2³¹ − 1], allocation a list of two finite positive numbers):
- **(P1′)** Every return of `v3_fit` with `estimates_available = FALSE`, and every error ending `v3_fit` without a fit
  object, is one of the INVENTORY rows A1–A5, A7, B1–B3, C1–C5, D1, E1–E5, X1–X8, or one of two sites new at the pin,
  X9–X10 below. Rows D2, X2 and X9 are unreachable, and so is D1 under EX-A (below); X10 is a reachable resource
  path. The row → pin-line map is the table in PROOF.md.
  - **X9** `start_mode` exceptions (`cpp/v3_start.h:261, 272`), reached through LS0 (`cpp/v3_core.cpp:469`).
  - **X10** the LS0 guard stop (`cpp/v3_core.cpp:480`) — INVENTORY's spec row E5/G2, now coded; a `resource_limit` exit
    (class (b) as E1–E3, and stop-only by T1 GW).
- **(S.3′)** D2 is unreachable at the pin; the invariants (i)–(vii) of S.3 hold at the pin (re-located lines in
  PROOF.md); `get_holder`'s stop and the class of implicit Rcpp/R errors on the call graph (X2-imp) are unreachable; X7, X8 are reachable only under
  IDEAL-W's unbounded reading of (n, p), are then excluded by A:IDEAL-W⁺ or 𝔇 (erratum), and cannot fire for inputs R can
  represent (PROOF §2); X9 is unreachable (cap = 10⁶ ≥ 2 at the only call; the root check passes by T9 TDP-e, under
  T4 ENC).
- **(D1)** INVENTORY calls D1 (`schedule_limit`) "the main random path". At the pin, with `grid_fallback = TRUE`, it is
  reached only if the tier-1 tier has no grid **and** its recorded fallback grid fails `v3_check_grid`
  (`v3_calib.R:163-170`). The recorded fallback is either the tier's last successful construction or its pilot schedule
  (`v3_calib.R:122-125`); under EX-A both start at exactly 0, increase strictly and end at exactly 1 (PROOF), so
  **D1 is unreachable on the shipped path under EX-A** — consistent with `C-DLV:Prop-F` ("PROVED-CHECKED for the patched
  calibration law", `Theory_work/Wave1C/C-DLV/REPORT.md:70`; `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:79-93`). It
  also holds in binary64 (the progress check and the exact end at 1 are coded). The INVENTORY summary ("D1 … is the only random no-output path") describes the pre-fallback core.

## Not claimed
- That any (a)/(b)-class path has small probability (that is `C-DLV:L1-R`, `:Thm-D`, outside this item).
- Paths off the `v3_fit` call graph (inspection helpers `cpp_start`, `cpp_start_draw`, `v3_gram`, …).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (second-seat re-audit at the pin; adds X9, X10) | track A T10 | `AUDIT.md` §6 T10 | `CHECK.md` |
| v2 | (S.3′) get_holder, X2-imp, X7/X8 for R inputs; (D1) binary64 | STRONGER (more sites covered) / EQUAL (citations) | LC2 #13–#19 | `reviews/LC2_reply_opus.md` | pending (gate) |
| v2.1 | X2-imp stated as a class, more instances | STRONGER (scope of the audit made explicit) | LC4 S2, E3 | `reviews/LC4_reply_opus.md` | pending (gate) |
| v2.2 | X7/X8: exact R-representability bound (n, p ≤ 2³¹ − 1 via `dim`/`int`); A:IDEAL-W⁺ reduces to IDEAL-W on R-representable inputs | STRONGER (made exact) | manager question 11-16 | — | pending (council batch) |
