# CLC1 disposition (lead, 2026-11-16)

| # | tag | finding | disposition | where |
|---|---|---|---|---|
| 1 | C | SMC LS0 worst-case preflight exit (`v3_fit.R:43-47, 61-66, 117`; escalation via `pf_fun`) not covered by any row (B1 memory-only, B2 exact) | **ACCEPT** (verified in code; trigger added by ef33f91c after INVENTORY v2). Amendment A-7 (row B1′); (C1-a) now "holds after A-7". The "no correctness break" sentence is kept, now with its reason: DLV-0's own (E2) names this exit ("on the SMC branch with the C-GROW cap also the LS0 archive and LS0 time") and excludes it by 𝒜_n's FIN A4 term P̄_LS0 (W3-RM2-R `lemmas/Q5_dlv0.md` lines 59-64, e78a1055); DLV-0 does not take it from P1. Lemma R's exact-branch-only scope recorded. | STATEMENT v2 (C1-a), (C1-c), A-7; PROOF v2 §1.1, §3 |
| 2 | S | configuration under-stated | ACCEPT: all five options named unset | STATEMENT v2 Code of record; PROOF §2 X7/X8 |
| 3 | E | `v3_calib.R:67` is C3, not a guard route | ACCEPT | PROOF §1.1 |
| 4 | E | NULL guard citation | ACCEPT (`cpp/v3_runtime.h:29-31`, `cpp/v3_core.cpp:778-779`) | PROOF §1.3 |
| 5 | E | `cpp_exact_count`, SMC timing path missing in §1.3; (vi′) both branches | ACCEPT | PROOF §1.3, §2 (vi′) |

Correctness event on row 3.1? **No**: the defect is in the registered inventory text (P1 as written misses one trigger at
the pin); DLV-0, the row's delivery lemma, walks and excludes this exit itself. Manager told at once (LOG).
