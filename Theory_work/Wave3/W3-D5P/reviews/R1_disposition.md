# Council R1 — disposition (lead), 2026-11-17

R1 on MANIFEST 952d9840…: Sol 7.5 gates=FAIL (LIST-K ACCEPT, LIST-CODE ACCEPT, LIST-R REJECT on 3 F in derived texts);
Opus 8.4 gates=FAIL (all ACCEPT, LIST-R subject to one minor C). No finding against LIST-K or LIST-CODE; no C against the
mathematics. Every C/S/F finding is ACCEPTED and repaired; every E is applied. Diff round R2 (Opus-only, manager's
instruction) on the diff since R1's manifest; the R2 seat also confirms the Sol findings.

| finding | tag | decision | repair (marker) |
|---|---|---|---|
| R1-sol-1 exact-branch fields described as list-renormalised in READER_DELTA/CARD | F | ACCEPT | READER_DELTA Corollary 6L and CARD Options A/B split the branches: sampler = list-renormalised; exact enumeration = exact PIPs/MPM [R1-sol-1] |
| R1-sol-2 evidence error not named / "within ε_n" for log_Z_list | F | ACCEPT | relative error 1 − ε_n ≤ Z^list/Z ≤ 1 and log error 0 ≤ log Z − log_Z_list ≤ −log(1 − ε_n) named explicitly; rate stated for the log error; Option B rewritten clause by clause |
| R1-sol-3 = R1-opus-2 NA qualification dropped (REPORT REGISTRY LIST-R, CARD, READER_DELTA) | F | ACCEPT | "when not NA" / "where printed" restored throughout; "where returned" for the exact store. The Opus alternative (prove never NA) is STRONGER → TARGET §4 row, proposed to HQ at CP3 |
| R1-opus-1 pin → post-commit transfer step unwritten | C (minor) | ACCEPT | L3 new step (0.5); Step 1 and Step 3 point to it; remark on IMPL-LIST's two uses corrected |
| R1-opus-3 AR/BLK qualifier dropped (CARD "why it matters", READER_DELTA remark) | F | ACCEPT | "AR and block designs that satisfy Theorem 6's conditions" in both |
| R1-opus-4 REGISTRY LIST-K scope "any score" | F | ACCEPT | "any real-valued F on Ω (as (C1))" |
| R1-opus-5 (C2) gloss omits `ls0_ell` = ℓ_n | E | applied | STATEMENT changelog v1.1.2 (EQUAL; the seat confirms the tag) |
| R1-opus-6 stale headers | E | applied | REPORT, L1–L3, TARGET headers |
| R1-opus-7 LIST-CODE REGISTRY premises/assumptions | E | applied | premises add :49-57; A:OP's content listed (EX-A, EX-S, SR, GUARD-W, OP-LS0; registry row A:OP) |
| R1-opus-8 READER "A completed run" | E | applied | "A run that produces output" |
| R1-opus-9 TARGET "beats 3.6 in scope (AR/BLK)" | E | applied | "(AR/BLK designs inside Theorem 6)" |
| R1-opus-10 DEPS checked_sha convention | E | applied | checked_sha = the hash council R1 read; checked_by names every checker and the tree it read |
| Opus note (∅ ∈ 𝓜^run needs logm_tab[b][0] finite) | — | no change | ∅ has size 0 ≤ K, so it is scored (`cpp/v3_start.h:91-93`) and finite under EX-A; nonemptiness is not used by any claim |
