# Carrier: W3-START2-R:MIS status text, re-point 12bb52cd -> R2r2 (recorder only; S4-3 style; not edited here)

Requested by the manager 11-18 after the pre-Lean batch landed (main 97f9c8c3), for the MEAS-D / NA_DROP landing set. The batch moved `W3-START2-R:MIS` to version 1.0.1 (the `STATEMENT.md:189` citation sits inside its span 189-198) and re-froze it CORRECTION-ONLY as R2r2.

**What the registry row says now** (`Theory_work/INFRA/registry/claims.tsv`, row `W3-START2-R:MIS`, main 97f9c8c3):
- `status` = "PROVED-CHECKED; council R2, MANIFEST 12bb52cd32c6870e14de43b0918827bc0ca9364d1ff04d6f16122b8a2a951ff5 (= R2 90886d06 re-frozen CITATION-ONLY as R2r), sol=9.0 PASS, opus=9.3 PASS" (`status_source` = `Theory_work/Wave3/W3-START2-R/CHECKPOINT_4.md:30`, which holds the same text),
- `council` = "R2; MANIFEST cc4f2e12722fea028e79dea543f6f694eed7f819eeebea45d203f272f1d80d87; sol=9.0 PASS(reviews/R2r2_record_sol.md); opus=9.3 PASS(reviews/R2r2_record_opus.md)". `reviews/MANIFEST_R2r2.txt` first line: `MANIFEST cc4f2e12722fea028e79dea543f6f694eed7f819eeebea45d203f272f1d80d87` (checked).

**Mismatch:** the status cell cites the R2r digest 12bb52cd while the council cell cites R2r2 cc4f2e12 (same pattern as Sol4-S4-3 for `W3-AUDIT-V:VIS`).

**Carrier (recorder):** re-point the status cell's digest to cc4f2e12722fea028e79dea543f6f694eed7f819eeebea45d203f272f1d80d87 and its parenthesis to "(= R2 90886d06 re-frozen CITATION-ONLY as R2r 12bb52cd and CORRECTION-ONLY as R2r2 cc4f2e12)", keeping "sol=9.0 PASS, opus=9.3 PASS" (the carried R2 scores, as for VIS). Mirror it at the status source so that "each status starts verbatim on its status_source" holds: `W3-START2-R/CHECKPOINT_4.md:30` (as for VIS, whose status source is `track_V/CHECKPOINT_4.md:6`). No claim text, span or score changes; no new review; tag: recorder-only registry bookkeeping, n/a (no text change). The sol/opus scores stay the R2 ones; nothing here is a read of the final text.
