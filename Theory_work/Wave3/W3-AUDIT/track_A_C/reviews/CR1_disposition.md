# Council C-R1 disposition (lead, 2026-11-16)

Sol 9.3 PASS (C1 ACCEPT, no findings). Opus 8.5 FAIL (C1 REJECT as written, ACCEPT after F1). bind R1: not attempted (Opus FAIL).

| # | seat | tag | finding | disposition |
|---|---|---|---|---|
| F1 | opus | F | (C1-c), PROOF §3 attribute both A-7 terms to P̄_LS0; the `ls0_archive` bytes are excluded by A4's mem_n ≥ P_e + A | ACCEPT: both terms named (STATEMENT v2.1 (C1-c); PROOF v2.2 §3), with DLV-0's own words quoted |
| E1 | opus | E | A-7 scope worded two ways (B1′ vs B3) | ACCEPT: B1′ = tier-0 site; escalation stays B3 (unspecified tier-1 memory estimate includes `ls0_archive`) |
| E2 | opus | E | STATEMENT said escalation can stop on LS0 seconds | ACCEPT: aligned with PROOF §1.1 (cannot newly fire) |
| E3 | opus | E | T9's (H4) not named | ACCEPT: discharged by IDEAL-W, MACH, T2's |C_b| ≤ 16 (STATEMENT (C1-b), PROOF §2) |
| E4 | opus | E | import statuses not recorded | ACCEPT: "Inputs consumed (status as recorded)" section |
| E5 | opus | E | SMC timing context, note for resource owners | ACCEPT as a note in CHECK.md (not C1's claim) |
| E6 | opus | E | `v3_preprocess.R:98-107` → `:99-107` | ACCEPT |

Diff round C-R2: Opus seat only (D91; Sol found no C).
