# Disposition of D1_codex_fidelity.md (Sol, NOT-FAITHFUL: 1C 4S 1F 1E). Manager, 2026-11-16.

All 7 were confirmed in the code and fixed.

| id | sev | fix |
|---|---|---|
| D1-C01 | C | The default memory is 8 GiB (8·2³⁰ bytes; `v3_fit.R:28,47,60`), fixed in §1.2 and in Table 1. Appendix D item corrected: METHODOLOGY_v3 is right about the unit; it omits only the 24 h default. |
| D1-S01 | S | "The best model found so far" during the calibration now includes the block-table models, which are recorded before the pilot (`v3_core.cpp:603-613`, `ingest_tables`). |
| D1-S02 | S | The Markov bound is scoped: it applies to the potential estimate on calibration success, under the companion's (C3); it gives P(completes and Ẑ > 20Z) ≤ 0.05; it is not coverage conditional on completion. |
| D1-S03 | S | Near ties are taken from the store of the 40p+1 best, with the truncation flag (`v3_run.R:170-173`). |
| D1-S04 | S | An invalid allocation and the two integer-limit violations end with an error and return nothing (`v3_fit.R:91-94`; `v3_run.R:95-97`; `v3_core.cpp:473-474`). Table rows now say "ends with an error". |
| D1-F01 | F | Appendix A caches row: the 10⁶ engine keeps a per-island store of the 40p+1 best; it drops the score cache and the two stores of 20p. |
| D1-E01 | E | Start-mode enumeration: "fewer than 10⁶" maximisers (the fallback fires at count ≥ 10⁶; `v3_start.h:288-290`). |

D2 does not state the memory unit; no change there.
