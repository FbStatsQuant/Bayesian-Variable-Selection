# NA_DROP — prepared statement change v1.2 (drop the "log_Z_list not NA" qualifier); to apply at the IMPL-LIST code-read

Prepared 2026-11-17 on the manager's instruction (before the `method-v3.1-listpip` tag). **Not applied**: the frozen tree
(R3 manifest 35a027be) is untouched. Applies on top of `reviews/R3r_correction.patch` (REPORT.md hunk) with
`git apply --verbose`; expected post-apply sha256: `NA_DROP_expected_sha256.txt`. Drafts: `STATEMENT_v1.2_draft.md`,
`L3_listR_v1.2_draft.md`.

**(a) The two spec readings vs LIST-CODE (i)–(v).** (1) Exact branch: `pip_list` = enumeration PIPs and
`log_Z_list`/`list_size`/`list_full` from `fit$exact$top`: consistent — LIST-CODE (iv) is exactly about `fit$exact$top`
(distinct models of Ω, values F, contains the HPM-order maximum); STATEMENT §1 already took `pip_list := pip_primary`
and `log_Z_list := logZ_{𝒯^ex}` "when returned", and (1) removes the "else NA" case. (2) All scores −Inf → fields NA,
`pip_list_flag = "nonfinite_score"`: consistent — under EX-A every returned value is a finite F(S) (LIST-CODE (iii),
(iv); Lemma S.2), so the row never fires on an output run. Neither reading touches a LIST-CODE clause (LIST-CODE is about
the pinned core's existing fields).

**(b) Is `log_Z_list` provably never NA?** Yes, on **every** output run (not only on the data event or the delivery
event), under EX-A and IMPL-LIST with reading (1): SPEC §4's NA rows are (i) empty list — impossible, the list contains the
HPM-order maximum of a nonempty offered set (LIST-CODE A4, (iii), (iv)); (ii) nonfinite scores — impossible under EX-A
(Lemma S.2, yᵀy > 0 on every output run); (iii) the exact-branch "store not returned" row — removed by reading (1); the
duplicate row is an error, excluded by L3 (0.5). Under (D) every run outputs, so in particular never NA on the delivery
event (HQ's condition).

**The change (v1.2).** STATEMENT §1: exact-branch row read as "from `fit$exact$top`" (also inside IMPL-LIST) [NA-1];
new (C3)(o) "every output run prints `pip_list`, `mpm_list` and a finite `log_Z_list`" [NA-2]; the qualifiers "when
`log_Z_list` is not NA" / "when returned" removed from (C3)(i), B₃, the rate display and (iii). L3: new Step 0′ proving
(o); NA mentions removed. Derived texts (REPORT registry block, CARD, READER_DELTA) follow. Tag: **STRONGER** (new clause
(o); evidence clauses on every output run); the IMPL-LIST edit is EQUAL (SPEC's own row in the reading HQ confirmed;
verified at the code-read). Check: one Opus statement-change check (`NA_check_opus.md`), as HQ ordered.
