# Council W-R1 disposition (lead, 2026-11-17)

Sol 9.4 PASS (W1, W2 ACCEPT; 1 E). Opus 8.1 FAIL (W1, W2 REJECT as written; 2 F, 7 E; "every proof step and every code
line I checked was right"). bind R1: not attempted (Opus FAIL).

| # | seat | tag | finding | disposition |
|---|---|---|---|---|
| F1 | opus | F | error/exception exits on the potential path not excluded (W2 prelude: `v3_check_seed`, inherited-model stop and scorer; islands: NumericalFailure, \|S\| > K, `nth_nonmember`; W1 assumes termination) | ACCEPT: W1 (ISL-0) normal termination + PROOF Step 2 paragraph; W2 PROOF (FRZ-b)(iii) "No error exit" paragraph (also the X7 validator `v3_run.R:95-97` via T14 REP, found by the lead while repairing); execution premise IDEAL-W/MACH stated |
| F2 | opus | F | locators: MR Step 2 `:51-58`, Step 3 `:60-62`, Steps 2–4 `:51-67`; L1 (B-0) `:62-75`, (B-d) `:119-125`; L3 proof `:25-39` | ACCEPT (also (B-b) control flow `:77-86`) |
| E1 | sol | E | MR locators | = F2 |
| E1 | opus | E | ledger citation | ACCEPT (`cpp/v3_ledger.h:104-113`) |
| E2 | opus | E | dangling changelog reference | ACCEPT (→ `reviews/WLC1_disposition.md`) |
| E3 | opus | E | import statuses | ACCEPT ("Inputs reused (status as recorded)" in both) |
| E4 | opus | E | value space of 𝓒° (⊥), tier ∈ {0, 1} | ACCEPT (W1, W2 settings) |
| E5 | opus | E | data integration not in "Not claimed" | ACCEPT (W2) — also a note for the recording package |
| E6 | opus | E | C1 PROOF reference | ACCEPT (argument via `v3_frozen`'s own check) |
| E7 | opus | E | finiteness of d | ACCEPT (valid-input hypothesis) |
Diff round W-R2: Opus seat only (D91; Sol found no C). Items: W1 STATEMENT/PROOF v1.2, W2 STATEMENT/PROOF v1.2.
