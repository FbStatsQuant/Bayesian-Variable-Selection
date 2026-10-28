# Claude audit of the OpenAI work: summary (HQ, 2026-10-23 ~02:00Z)

Seven independent Claude audits. Nothing found is critical; everything listed below is kept.

| Audit | Model | Verdict | Key points |
|---|---|---|---|
| A-CODE | Opus | sound with fixes; deployable | Every v2 change from the prototype is justified and correct. Regression 32/32 rerun. Public v3_fit is bit-identical to the verified prototype at production budgets (3 cases). Minor items F1–F5 (below). |
| B-VERIFY | Opus | sound with fixes | The oracles are correct, independent and log-backed. **F1 (major):** most of the orchestration was checked by source review only. Mitigated by A-CODE's bit-identity with the verified prototype; a tiny-p SMC-versus-exact check is now required. G1 wording corrected; R-6 relabelled as a waiver. |
| C-OPS | Sonnet | sound with fixes | 120/120 datasets and 240 units recomputed exactly, with all input hashes matching the manifest. Pilot facts confirmed. The NOTS N0 failures were all infrastructure (no lmod init on compute nodes, no /usr/bin/time, a self-built GNU time that fails). The runner has never run a real fit. |
| D-ANALYSIS | Sonnet | sound with fixes | Byte-identical reuse of the benchmark scoring. All 6,272 published table values recomputed independently, 0 mismatches. Join, R-1 and MCSE are correct; the suite passes 241/241. **F1 (major):** the validator demands a heuristic-bound label that A v2 only writes on certificates. **F2:** the scorer has never run on real v2 output with truth. |
| INVENTORY | Haiku | sound | v2 archive, snapshot and Owls copy are identical. 12 stale root-ledger rows (working-tree paths) need updating. |
| Proofs T22(iii) + T27(i) | Opus (CW) | correct | Optional wording fixes only. Suggests that Lemma EXP′ may be provable. |
| Proofs T21 + T25(iv) | Opus (CW) | correct | Wording fixes E1, E3, E5. H10 may follow from wave-1 T22 Lemma 2. |

## Decisions

1. **A v2 (frozen) is the method code for deployment.** The core is unchanged. Allowed changes are limited to the study layer and runner: A-CODE F1 (locale-independent source hash), F3 (an R out-of-memory error is recorded as failed) and F5 (the in-run `--hours` is aligned with the external unit limit). These become a v2.1 study-layer freeze with an independent review. The F2 label is cosmetic (exact branch only) and may be fixed in the same pass.
2. **The heuristic-bound label (D F1).** The label is required only when a global certificate bound is reported, which happens only on the exact branch. D's validator must accept its absence when `global_certified` is FALSE. Part I wording ("with every certificate") supports this.
3. **NOTS readiness, required before any production array:**
   - the build plus the 32-seed regression;
   - B's battery;
   - a tiny-p SMC-versus-exact check: choose (n, p) such that v3's branch rule selects SMC while external enumeration is still feasible (for example p = 18–20, n ≈ 30), over several seeds, comparing log Ẑ and PIPs with B's exact enumeration;
   - the two dev smokes;
   - ONE real fit end to end through the production runner and transfer.
4. **Runner fixes:**
   - no GNU-time dependency; use R/proc VmHWM plus `sacct`;
   - explicit module initialisation;
   - unit limits re-derived from the NOTS smoke timings;
   - resource kills classified as infrastructure (rerun with the same seed), not permanent failures;
   - fix the status-line check.
5. **Scope:** the full 2,400 units: 1,200 benchmark datasets (S1–S6 × p ∈ {500, 1000} × r = 1..100) × c100 and c050, on exactly the benchmark inputs and seeds.
