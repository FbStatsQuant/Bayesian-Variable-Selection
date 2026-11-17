# X3 · Re-check of `W3-POST:Lemma-1a'` (design-free size tail) — STATEMENT v1.1 (draft, not locked)

Track A item X3 (`AUDIT.md` §6 "Further open inputs", X3; TRACK_D §3: "lemma (Tier B) — one line check"). Tier B (a
further line check under PROTOCOL_v4 of an existing proof; no new claim). The registry status reads "PROVED (by this
seat, unchecked)", but the lemma file records a check history (R01 VERIFIED-WITH-AMENDMENTS, R02 VERIFIED, council C1
seats re-derived it, council C3 correct:PASS; `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:3-5`); the status label
has not been updated to it (recorder note). **Lean target: no** (analytic: Gaussian slab
integral, inverse-gamma bound, Markov; feasible in principle but not small). Blocks row 1.1, expectation display
(`W3-POST2:C` is "conditional on W3-POST:Prop-LB, [L1a′], …").

## The claim re-checked (verbatim reference, not restated)
`W3-POST:Lemma-1a'@1.0.0`, "PROVED (by this seat, unchecked)" (registry), statement
`Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:9-19`, proof `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:21-42`; summary
in `Theory_work/Wave3/W3-POST/STATEMENT.md:52-58`. In words: under G (Gaussian noise, fixed design), for n ≥ 3 and a standardised design X, if μ = X_Tθ for some T ∈ Ω with
‖μ‖² ≤ nM and ‖θ‖² ≤ nM′, then the normalised size tail Θ^T_{n,m} of the coded posterior obeys
sup_m P(Θ^T_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C′_Λ/log(√L/c♯) for every L > c♯², with
C′_Λ = 1/√2 + 1/2 + (M + M′)/(2σ*²), and π(|S| > m^T_n(ω)) ≤ (1 + 1/n)^{t/2}e^{−ω}Θ^T_{n,m^T_n(ω)} — no eigenvalue condition.

## Inputs (with recorded statuses)
- [P1] `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` (= `main@c4ef0dc`, byte-identical, checked
  2026-11-16; "locked T01/T02"): `lem:slab` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:68-81`), `lem:spec` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:90-111`), `lem:chi` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:139-150`), `thm:T01iii` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:234-240`), `thm:Ta` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:255-264`), `lem:num` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:317-323`), `lem:den` (`Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:324-360`).
- [T03R] `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md` (T02(i♯), "PROVED; SF/XF
  VERIFIED" per `Theory_work/Wave3/W3-POST/STATEMENT.md:43`): R_m, Lemma den′ and the assembly
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md:16-17, 74-97`).

## Re-check result (the item's claim)
**(X3) The proof of Lemma 1a′ is correct as written, given the inputs above.** Each step is verified in PROOF.md. No
correction is needed to the statement; two precisions are recorded (PROOF, end).

## Not claimed
- The inputs [P1], [T03R] themselves (their statuses are as recorded).
- Remarks 1–5 of the lemma file (not part of the claim), in particular the open questions of Remarks 2 and 5.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (second-seat line check of an existing proof) | track A X3 | `AUDIT.md` §6 X3; manager GO 11-16 | `CHECK.md` |
| v1.1 | record of prior checks; summary completed (G, n ≥ 3, second conclusion); citations | EQUAL (description) | LC2 X3 #1, #4, #5 | `reviews/LC2_reply_opus.md` | — |
