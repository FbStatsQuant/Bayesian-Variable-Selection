# WSL1 brief — statement lock + line check of track-A_W items W1 (ISL) and W2 (FRZ) (Codex gpt-6.1-sol, high)

The gate read (PROTOCOL_v4 §2, Tier B, NORMAL: Sol lock + Sol line check in one read; key lemma). **Blind first read:**
read only the files below and the code. Do not open any LOG, CHECKPOINT, INDEX, CHECK or `reviews/` file. Read only;
write no files; change no git state; start no subagents.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT` (branch `theory/W3-AUDIT`).
- Items: `Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/{STATEMENT,PROOF}.md` (v1.1), `.../track_A_W/W2_FRZ/{STATEMENT,PROOF}.md` (v1.1).
- Steps they re-check: `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md` (Lemma B: (B-0), control-flow clause of (B-b), (B-d)),
  `Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md` (Lemma F), `Theory_work/Wave1/W1-N1/STATEMENT.md` §2, T12's freezing lemma
  `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:155-166`.
- Consumers: `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md` §1, `Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md`,
  `Theory_work/Wave3/W3-SAMP/STATEMENT.md` §0–§2.
- Inputs (to see what is assumed; review only where the items lean on them): `Theory_work/Wave3/W3-AUDIT/track_A/{T1_GW,T4_ENC,T5_CAL,T6_START,T7_KER}/STATEMENT.md`,
  `Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/{STATEMENT,PROOF}.md` (FR), `Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/STATEMENT.md`.
- Code of record `Scripts/SMC_BVS/core/` (pin 4676af6; confirm with `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`).
  Read the code yourself; do not trust the line quotes.

Context: three edges into the registry are NOT-COVERED by the existing at-pin checks: `W3-SAMP:D` → `W1-N1:B` (island
control flow, stopping times, (B-0)/(B-d)); `W3-SAMP:MR` → `W1-N1:B` ((B-d) MEAS); `W3-SAMP:MR` → `W1-N1:F` (the freezing
step at general calibration value c, incl. MR's extension to stage/prefix records). W1 and W2 are meant to discharge them
at the code of record so that those conditions can be removed from W3-SAMP and its consumers (rows 3.6 and others).

**Part 1 — statement lock.** Right target (do W1, W2 give D and MR exactly what they take from `W1-N1:B` and `W1-N1:F`?),
faithful to the code and the sources, every hypothesis explicit (H-U, EX-A, potential run, (𝒜°, 𝓒°) reading, executed
N_e/L), no clause stronger than proved. Verdict per item: LOCK / LOCK WITH CHANGES (list) / DO NOT LOCK.
**Part 2 — line check.** Every step against the code; try to break it: a source other than (c, data, uniforms) that
influences an island transition or weight; a uniform read outside the island's `vs->u`; a read count not decided by the
past; a wrong bound; a measurability gap; SI at the pin (stream 9 + r read outside island r, or 𝓒° depending on it); A₀,
E₀ = {𝓒° ∈ A₀}; O_r = Φ(𝓒°, U_r); the monotone-class proof; the evidence bounds; each consumer's integrand being of the
stated form. Verdict per item: VERIFIED / VERIFIED WITH AMENDMENTS / NOT VERIFIED.
If a consumer's use is not supported at the pin, say so first and tag it **C**.

**Reply format** (plain markdown, as your final message): Part 1 verdicts; Part 2 verdicts; numbered findings tagged **C**,
**S**, **F** or **E** with file:line, what fails, and the fix. Last line:
`WSL1-VERDICT: W1 lock=<…>, check=<…>; W2 lock=<…>, check=<…>`.
