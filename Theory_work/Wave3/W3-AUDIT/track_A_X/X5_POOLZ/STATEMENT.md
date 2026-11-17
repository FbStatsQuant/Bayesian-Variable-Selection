# X5 · Re-check of `W3-READER:PoolZ` (pooled evidence unbiased) — STATEMENT v1 (draft, not locked)

Track A item X5 (`AUDIT.md` §6 "Further open inputs", X5; TRACK_D §3: "lemma (Tier B) — two-line proof; line check and
registry row"). Tier B (second-seat line check; no new claim). **Lean target: yes** (linearity of conditional
expectation on top of N1; trivial once N1 is formalised). Blocks row 3.5.

## The claim re-checked (verbatim reference; the file is not on this branch)
`W3-READER:PoolZ`, "PROVED (by this seat, unchecked)", in the W3-READER worktree, branch `theory/W3-READER`, file
Theory_work/Wave3/W3-READER/STATEMENT.md lines 12–37 (last changed at commit 68443dcc; sha256 prefix 29696a79d4f0, read
2026-11-16). In words: on the SMC branch, under the N1 premises, with the reported evidence Ẑ = ¼Σ_{r=1}^4 Ẑ_r, almost
surely on 𝒜, E[Ẑ | 𝓒] = Z; hence E[1_𝒜Ẑ] = E[1_𝒜Z] under the joint law with the H-U/SI idealisation.

## Inputs
- `W1-N1:Thm-N1@1.0.0` "PROVED-CHECKED" (`Theory_work/Wave1/W1-N1/STATEMENT.md:98-104`; its "in particular" clause
  E[W_r | 𝓒] = 1, `Theory_work/Wave1/W1-N1/STATEMENT.md:104`).
- Code: `log_Z = v3_log_sum_exp(logZr) - log(R)` (`Scripts/SMC_BVS/core/v3_run.R:150-154`), `islands = 4L`
  (`Scripts/SMC_BVS/core/v3_run.R:91`); island evidence as in `Theory_work/Wave3/W3-SAMP/STATEMENT.md:52-53`.
- T1 (GW-iv) and T5 (CAL-b, CAL-d) of this track (the success event; see the precision below).

## Re-check result
- **(X5-a) VERIFIED.** The proof is correct: N1's identity for r = 1, …, 4 on 𝒜 (R′ = 4 there) and linearity of
  conditional expectation give E[Ẑ/Z | 𝓒] = 1 a.s. on 𝒜, with Z a constant for fixed data; integrating over (data, 𝓒)
  under H-U/SI gives E[1_𝒜Ẑ] = E[1_𝒜Z].
- **(X5-b) Precision (F, reading — same as T5's flag).** The conditioning "given 𝓒 on 𝒜" needs 𝒜 ∈ σ(𝓒). That holds
  for the uninterrupted pair (𝒜°, 𝓒°) (T5 CAL-b), not for the actual 𝒜, which also depends on the clock through the
  guard (T1 GW-iv: 𝒜 = 𝒜° ∩ G). So PoolZ is proved with 𝒜° in place of 𝒜, for the uninterrupted record (its Remark (iii)
  already says the identity is about the potential record). For the actual 𝒜 the unconditional form
  E[1_𝒜Ẑ°] = E[1_𝒜Z] needs, in addition, that the calibration-time clock (through G) be independent of the final
  streams given 𝓒° — a statement about the clock that no premise supplies (T1, Not claimed). Recommended wording:
  "almost surely on 𝒜°" / "on the event that calibration succeeds in the uninterrupted run".
- **(X5-c) Registry row (for the recorder; no edit made).** `W3-READER:PoolZ` is absent from this worktree's
  `claims.tsv` (A_inventory drift D5). Proposed fields: kind claim; file Theory_work/Wave3/W3-READER/STATEMENT.md,
  lines 12-37; depends_on `W1-N1:Thm-N1@1.0.0@stmt`; premises EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT (the N1
  premises); status after the gate per PROTOCOL_v4; note "reads with 𝒜° (X5-b)".

## Not claimed
- Anything about the normalised PIPs or about Ẑ on interrupted runs.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (second-seat line check of an existing proof) | track A X5 | `AUDIT.md` §6 X5; manager GO 11-16 | `CHECK.md` |
