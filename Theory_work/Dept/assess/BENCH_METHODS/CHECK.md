# BENCH_METHODS: Haiku verification of matrix cells

Two Claude Work Haiku checkers re-opened each paper's full text. They used the local PDF when there was one, and otherwise arXiv, PMC or the publisher. They checked whether each sampled matrix cell is true: does the method really appear in that paper's simulation or real-data **comparison**, as a competitor? Opus adjudicated every MISMATCH by re-reading the paper. The raw rows are in `check/CHECK.tsv` and `check/CHECK2.tsv`; the samples are in `check/SAMPLE.tsv` and `check/SAMPLE2.tsv`.

| Pass | Sample | OK | MISMATCH | UNVERIFIABLE |
|---|---|---|---|---|
| **Check 1** | 42 cells (seeded random). 28 are competitor cells of frequently used methods, 8 are competitor cells of other methods, and 6 test cells we recorded as ABSENT (missed methods). | 39 | 3 | 0 |
| **Check 2** (targeted) | All 30 remaining competitor cells of the low-count Bayesian samplers (ASI, wTGS, HBS, SMC, EMVS, varbvs, SuSiE, SSLASSO, Skinny Gibbs, BAS, BASAD, SSS, PT) | 25 | 4 | 1 |
| **Total** | 72 cells | 64 | 7 | 1 |

## Adjudication (Opus)

| id | Cell | Checker | Opus ruling | Fix applied |
|---|---|---|---|---|
| V01 | Staerk2024 × HBS | MISMATCH: the Hamming-ball sampler is never run | **Confirmed.** The re-read of Sec 5 (p.18) shows the comparators are "local MC3 … with additional swap moves" and "the adaptive weighted tempered Gibbs sampling algorithm of Zanella and Roberts (2019)" via scaleBVS, with BAS giving the exact PIPs. ASI and the locally informed sampler were also wrongly listed; Griffin and Zanella are only cited. | Dropped HBS, ASI and LIT_MH. Added WTGS (C) and BAS (G). |
| V30 | Cui2024 × COJO-ABF | MISMATCH: not in the simulations | **Overruled.** It is run in the real-data comparison ("SuSiE, FINEMAP and COJO-ABF show high RFR"), which counts under our schema. Only the location was wrong. | Location corrected |
| V41 | Liang2022 × WTGS (claimed ABSENT) | MISMATCH: wTGS is run in Sec 5.2 | **Confirmed.** It was missed in extraction. | Added WTGS (C) |
| W03 | Hahn2015 × BAS | MISMATCH: used only to cross-check the HPM and MPM | **Confirmed.** BAS is a reference, not a competitor column. | Reclassified as G |
| W06 | Ročková2018 (SSL) × EMVS | MISMATCH: the paper's own EM variant | **Confirmed.** Table 1 is titled "Two variants of the Spike-and-Slab LASSO procedure". | Reclassified as V |
| W22 | Jankowiak2023 × TGS | MISMATCH: an ablation of its own PG-wTGS | **Confirmed.** | Reclassified as V |
| W30 | Yang2025 × SuSiE | MISMATCH: only its own SuSiE-RSS-based approach is run | **Confirmed.** | Dropped |
| W25 | Truong2023 × WTGS | OK | **Overruled by Opus.** The checker's own evidence quotes "subset wTGS [11]", and the re-read of Sec 3–4 shows the comparator is the subset wTGS of Jankowiak 2023, not wTGS. | Dropped WTGS; added NEW:SUBSET_WTGS (C) |
| W14 | Weissbrod2020 × SuSiE | UNVERIFIABLE: Nature and Europe PMC returned only the abstract and legends | Kept. It comes from the BENCH_DESIGN full-text read; this is flagged in the REPORT caveats. | — |

**Corrections overall.** After adjudication, 7 of the 72 checked cells were wrong (about 10%), and 2 more wrong cells in the same flagged paper were found on re-read. All of them are corrected in `MATRIX.csv`; the corrections are recorded in `rows/OPUSFIX_methods.tsv` and `drops.tsv`.

**Where the errors were.** Every error is in a low-count Bayesian cell, and the typical mistake is a role confusion: a gold standard, ablation or own variant recorded as a competitor. No error was found in the 17 sampled cells of lasso, SCAD, MCP, Gibbs and add-delete-swap, which drive the top of both rankings.

**Effect on the recommendations.** The corrections changed only small counts: wTGS 4→3, ASI 3→2, HBS 3→2, EMVS 6→5 in all roles, SuSiE 3→2. The final set does not change.

**Earlier corrections, before the Haiku checks.**
- Six rows in Martin2017 were dropped. They had been copied from Narisetty–He 2014's tables rather than re-run, as the sweep worker had flagged.
- The Schäfer 2012 thesis was excluded as a duplicate of Schäfer–Chopin 2013.
