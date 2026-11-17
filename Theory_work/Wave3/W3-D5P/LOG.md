# W3-D5P — LOG (track D ticket #5′, store-restricted output consistency; lead Opus 5.5 high)

Times from `date` (local).

- 2026-11-17 12:46 CST Start. Worktree /home/fb31/BVS-wt/W3-D5P, branch theory/W3-D5P @ 029bb748 (core unchanged since 72785fe; `git diff 4676af6 029bb748 -- Scripts/SMC_BVS/core` empty). Brief = manager's launch message (D105/D106; kill 3 d).
- 12:40–13:20 CST Read: SPEC_LIST_PIP (W3-AUDIT 523dda23), TRACK_D §5a + table row 5′, W3-DIST STATEMENT §2 (DIST-C, :289-318; links at :297-303), CLAIMS_CARD rows 3.1/3.5/3.6, READER_VERSIONS Thm 2/6/9C, W3-RM2-R STATEMENT (RM0-plus, RM2-R-plus, DLV-0), W3-RM STATEMENT §1/§4, C-DLV L4_delivery:60-77, W3-SAMP CC2, W2-APP L1_POST, PROTOCOL_v4, RIDER_RULES (dept/theory), registry rows.
- 13:20 CST Code read at the pin (v3_run.R, v3_fit.R, v3_exact.R, cpp/v3_core.cpp cpp_final_run + cpp_enumerate + store_to_list, cpp/v3_ledger.h TopStore/Ledger, cpp/v3_engine.h eval/local_search, cpp/v3_score.h ScoreCache, cpp/v3_start.h build_tables). Finding: every HPM offer on a completed final run goes through Ledger::offer_stores, which offers the same (F, S) to `top`; TopStore never evicts its first element (cap 40p+1 ≥ 41). Corollary route viable: no new key lemma. "Result 3" = row 3.1 / Theorem 6 (Writing OUTLINE).
