# C1 · Check of the audits C-DLV:P1-Inventory and C-DLV:L2-S3 at the pin — STATEMENT v1 (draft, not locked)

Track A_C item C1 (manager, 11-16: the last unchecked inputs on row 3.1). Tier B (PROTOCOL_v4 §2, §2A NORMAL;
second-seat code reading of two registered "AUDITED (code reading)" claims). **Lean target: no** (code facts).
Blocks row 3.1, delivery: `W3-RM2-R` Lemma DLV-0 consumes "Lemma S.3 and the P1 inventory (AUDITED, code reading)"
for the core as pinned (W3-RM2-R STATEMENT.md lines 144-162, on branch theory/W3-RM2-R at commit e78a1055, not on this
branch).

## Claims under check (registered text; not edited here)
- **`C-DLV:P1-Inventory`** (registry: `Theory_work/Wave1C/C-DLV/STATEMENT.md:52-53`, "AUDITED (code reading)"): "every
  exit of `v3_fit` without estimates is one of the listed sites", the list being `Theory_work/Wave1C/C-DLV/INVENTORY.md:15-93`
  (v2, rows A1–A7, B1–B3, C1–C5, D1–D5, E1–E5, X1–X6, G1–G4, and the erratum rows X7–X8 with A:IDEAL-W⁺, 2026-11-16).
- **`C-DLV:L2-S3`** (registry: `Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md:37-67`, "AUDITED (code reading)"): D2
  is unreachable, and the internal error sites (X2) reachable from `v3_fit` are each excluded by the invariant listed,
  (i)–(vii); with the erratum (viii)–(ix) (`Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md:72`), which names X7–X8 as
  reachable stops excluded by A:IDEAL-W⁺ or 𝔇, not by an invariant.
- Both were written against a core in which LS0 was specified, not shipped (`Theory_work/Wave1C/C-DLV/INVENTORY.md:6-7, 71-77`);
  their line numbers predate the pin.

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core; `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`).
Shipped `v3_fit` (`v3_fit.R:73-174`) with default options (`ls0 = TRUE`, `grid_fallback = TRUE`).

## Reading
"Exit without estimates" = INVENTORY's 𝒰 (`Theory_work/Wave1C/C-DLV/INVENTORY.md:8-10`): `v3_fit` returns with
`estimates_available = FALSE`, or the process ends without a fit object. A row "covers" a site when the site is an
instance of the row's trigger; X2 is a class row ("internal-invariant `stop()` / `runtime_error` on the `v3_fit` call
graph", its instances listed with "incl."). Valid declared inputs: seed an integer in [1, 2³¹ − 1], allocation a list
of two finite positive numbers. Premises as in C-DLV: EX-A, IDEAL-W, MACH; for X7–X8, A:IDEAL-W⁺ or 𝔇.

## Lemma C1 (the two audits hold at the pin, with amendments)
- **(C1-a) P1 holds at the pin.** Every site of the shipped `v3_fit` call graph at which `v3_fit` returns with
  `estimates_available = FALSE`, or which ends `v3_fit` by an error, is covered by a row of the INVENTORY (with the
  erratum): the row → pin-line map is the table of T10 (`track_A/T10_P1S3/PROOF.md` §1), re-verified in PROOF §1 here,
  plus the call-graph nodes added in PROOF §1 (`cpp_dup_components`, `cpp_cut_group`, `cpp_runtime_new`,
  `cpp_runtime_report`, `cpp_numerical_routes`, `v3_peak_memory_kb`). The sites new since the audit fall under
  existing rows: the `start_mode` exceptions (`cpp/v3_start.h:261, 272`; T10's X9), `get_holder`'s stop
  (`cpp/v3_core.cpp:18`) and the implicit Rcpp/R errors (T10's X2-imp) are X2-class sites; the coded LS0 guard stop
  (`cpp/v3_core.cpp:480`, T10's X10) is row E5 ("LS0 stop", class (a)/(b) under MACH).
- **(C1-b) S.3 holds at the pin.** D2 (`v3_calib.R:170`) is unreachable, by S.3's argument at re-located lines; each
  invariant (i)–(vii) holds at the pin (re-located; for (i) the cited reason must be the code (T2 BLK), not the
  specification); and the X2-class sites new since the audit (`start_mode` exceptions, `get_holder`, implicit errors)
  are unreachable on valid internal state (T10 §2, under T4 ENC and T9 TDP-e for `start_mode`). The erratum's
  (viii)–(ix) (= X7–X8) are reachable only beyond R's dimension limit: for every input R can represent
  (n, p ≤ 2³¹ − 1) both predicates are false (T10 v2.2 §2; `track_A_X/T14_REP`).
- **(C1-c) Consequence for DLV-0.** On valid declared inputs, under EX-A, IDEAL-W, MACH and (for X7–X8) A:IDEAL-W⁺ or
  𝔇: every exit without estimates of the shipped `v3_fit` at the pin is a site in A1–A5, A7, B1–B3, C1–C5, D1, D2,
  E1–E5, X1–X8, and D2 and the X2 class are unreachable; so the two audits supply, at the pin, the premise DLV-0 takes
  from them. No correctness break on row 3.1.

## Amendments found (to the recorded audit text; none changes a conclusion)
- A-1 (all rows): line numbers predate the pin; the pin lines are PROOF §1 / T10 §1.
- A-2 (X2 list; S.3): the instance list misses the `start_mode` exceptions, `get_holder`'s stop and the implicit-error
  class; each is unreachable (PROOF §2).
- A-3 (E5/G2): the LS0 stop is coded at the pin (`cpp/v3_core.cpp:480`), no longer spec-only.
- A-4 (D1, Summary `Theory_work/Wave1C/C-DLV/INVENTORY.md:80-81`): with the tier-1 fallback (`v3_calib.R:122-125, 163-170`) D1 is unreachable
  on the shipped path under EX-A (T10 §3; `C-DLV:Prop-F`); "the main random path" describes the pre-fallback core.
- A-5 (S.3 (i)): its reason cites the specification (`Theory_work/State_of_Project/sections/02_method.tex:189-192`); at the pin the reason is the code
  (T2 BLK-a/BLK-b).
- A-6 (A6, A3): `degenerate_n` is not coded; n < 3 is rejected by A3 (`v3_preprocess.R:99-107`).

## Not claimed
- Probability or resource bounds for the reachable (a)/(b)/(c) rows (`C-DLV:L1-R`, `:Cor-R`, `:Thm-D`, `:Prop-F`).
- Sites off the `v3_fit` call graph (inspection helpers).
- Binary64 (C-DLV and DLV-0 are under EX-A).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (verdict on two registered audits at the pin) | track A_C C1 | manager 11-16 | `CHECK.md` |
