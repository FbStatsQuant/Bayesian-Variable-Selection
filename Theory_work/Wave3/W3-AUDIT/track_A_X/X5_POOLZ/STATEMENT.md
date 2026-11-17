# X5 · Re-check of `W3-READER:PoolZ` (pooled evidence unbiased) — STATEMENT v1.2 (draft, not locked)

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
- **(X5-a) VERIFIED WITH AMENDMENTS.** What is verified is PoolZ for the uninterrupted pair: the identities hold for
  (𝒜°, 𝓒°, Ẑ°), with MEAS-J and the joint independence below for the joint-law form; equality for the actual 𝒜 holds
  only under the additional clock-independence premise of (X5-b). The original PoolZ wording is not verified without
  these qualifications. The argument: N1's identity for r = 1, …, 4 on 𝒜° (R′ = 4 there) and linearity of
  conditional expectation give E[Ẑ°/Z | 𝓒°] = 1 a.s. on 𝒜°, with Z a constant for fixed data. The joint-law form
  E[1_𝒜Ẑ] = E[1_𝒜Z] (an equality in [0, ∞]; both sides nonnegative, no integrability needed) additionally uses
  **MEAS-J** — the island record is jointly measurable in (data, c, u), not only in (c, u) for fixed data as W1-N1's
  MEAS gives — and that the final streams are independent of (data, streams 0–9) **jointly**; PoolZ's proof uses both
  without stating them. MEAS-J holds by the bounded-computation argument of T5 (CAL-b) with the data as a further Borel
  input (PROOF, step 4).
- **(X5-b) Precision (F, reading — same as T5's flag).** N1's conditioning "given 𝓒 on 𝒜" needs 𝓒 to satisfy CAL
  (a function of the data and streams 0–9). For the actual record 𝒜 ∈ σ(𝓒) holds (the status is a statistical field),
  but CAL fails: the actual 𝓒 depends on the clock through the guard's Booleans. Only 𝓒° satisfies CAL (T5 CAL-b), and
  𝒜 ∈ σ(𝓒°) holds for 𝒜°, not for 𝒜 = 𝒜° ∩ G (T1 GW-iv). So PoolZ is proved with 𝒜° in place of 𝒜, for the uninterrupted record (its Remark (iii)
  already says the identity is about the potential record). For the actual 𝒜 the unconditional form
  E[1_𝒜Ẑ°] = E[1_𝒜Z] needs, in addition, that the final streams be independent of (data, streams 0–9, G) jointly —
  a statement about the clock that no premise supplies (T1, Not claimed). Recommended wording:
  "almost surely on 𝒜°" / "on the event that calibration succeeds in the uninterrupted run".
- **(X5-c) Registry row (for the recorder; no edit made).** `W3-READER:PoolZ` is absent from this worktree's
  `claims.tsv` (A_inventory drift D5). Proposed fields: kind claim; file Theory_work/Wave3/W3-READER/STATEMENT.md,
  lines 12-37; depends_on `W1-N1:Thm-N1@1.0.0@stmt`; premises EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT (the N1
  premises) plus, for the joint-law form, MEAS-J and "final streams ⫫ (data, streams 0–9) jointly"; status after the gate per PROTOCOL_v4; note "reads with 𝒜° (X5-b)".

## Not claimed
- Anything about the normalised PIPs or about Ẑ on interrupted runs.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (second-seat line check of an existing proof) | track A X5 | `AUDIT.md` §6 X5; manager GO 11-16 | `CHECK.md` |
| v1.1 | joint-law form: MEAS-J and joint independence named; (X5-b): failing premise is CAL; clock condition stated jointly | STRONGER as to stated premises / EQUAL in conclusion | LC2 X5 #1, #3, #4 | `reviews/LC2_reply_opus.md` | — |
| v1.2 | verification label: VERIFIED WITH AMENDMENTS, scope (𝒜°, 𝓒°, Ẑ°) stated in (X5-a) | WEAKER (label made exact; no new argument) | Sol X-read #1 | `reviews/LC3_reply_sol.md` | — |
