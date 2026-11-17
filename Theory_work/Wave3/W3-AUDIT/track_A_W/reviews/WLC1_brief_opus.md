# WLC1 brief — blind line check of track-A_W items W1 (ISL) and W2 (FRZ) (Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
CHECKPOINT, INDEX, CHECK or `reviews/` file. Write no files; change no git state; start no subagents. Your job is to
**break** these lemmas.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- The items: `Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/{STATEMENT,PROOF}.md`, `.../track_A_W/W2_FRZ/{STATEMENT,PROOF}.md`.
- The steps they re-check (written for an older core): `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md` (Lemma B: (B-0), the
  control-flow clause of (B-b), (B-d)), `Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md` (Lemma F), `Theory_work/Wave1/W1-N1/STATEMENT.md` §2,
  T12's freezing lemma `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:155-166`.
- The consumers: `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md` (§1), `Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md`,
  `Theory_work/Wave3/W3-SAMP/STATEMENT.md` (§0–§2).
- Inputs they cite (read to see what is assumed; do not review): `Theory_work/Wave3/W3-AUDIT/track_A/{T1_GW,T5_CAL,T6_START,T7_KER,T4_ENC}/STATEMENT.md`,
  `Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/{STATEMENT,PROOF}.md` (FR), `Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/STATEMENT.md`.
- The code of record `Scripts/SMC_BVS/core/` (pin 4676af6; `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`
  confirms). Read the code yourself; do not trust the line quotes.

Check, per item:
1. **Correctness.** W1: a source other than (c, data, uniforms read) that influences an island transition, weight or
   log Ẑ (cache, ledger, clock, guard, shared engine members, other islands, the calibration streams); a uniform read
   outside `vs->u`; an operation whose read count is not decided by the past; a wrong bound; a measurability gap (cells,
   branches, EX-A); a record coordinate the consumers use that is not a measurable function of the record. W2: the
   monotone-class proof; SI at the pin (any stream ≥ 10 read before or outside island r; any dependence of 𝓒° on stream
   9 + r); A₀ ∈ 𝓔 and E₀ = {𝓒° ∈ A₀}; O_r = Φ(𝓒°, U_r) (settings, stream, earlier islands); the evidence bounds.
2. **Strength.** No clause claims more than is proved; every hypothesis used is stated (H-U, EX-A, potential run, the
   reading with (𝒜°, 𝓒°)).
3. **Faithfulness.** Each item discharges exactly what the consumers take from `W1-N1:B` ((B-0), (B-b) control flow,
   (B-d)) and `W1-N1:F` (freezing at general c, incl. MR's extension and D's freezing step).
If a step fails for real (a consumer's use is not supported at the pin), say so first and tag it **C**.

Reply (plain markdown, as your final message): per item a verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` /
`NOT VERIFIED`, then numbered findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix.
Last line: `WLC1-VERDICT: W1=<…>; W2=<…>`.
