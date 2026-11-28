# PRE-LEAN PASS, Sol-4: PACKET for the Sol final-text confirmation (track V R4)

Target: **`W3-AUDIT-V:VIS` (Lemma VIS, visibility with a margin uniform in n), final text after council rounds V-R2, V-R3 and V-R4**, which were Opus-only (diff-only, D91, Codex level 1); plus the post-freeze CORRECTION-ONLY re-wording of the dossier `TRACK_B.md` B8 that **no council seat reviewed**. Sol saw only V-R1 (9.5 PASS, on MANIFEST c271cfac…). Lean target: yes (finite-dimensional: Schur complements, Stieltjes matrices, closed sets of hyperplanes).
**FAMC note (not part of this call):** `W3-FAMC:Cor-FAMC` already had Sol 6.2 reviews on all five rounds, including R5 (10.0 PASS on MANIFEST 3305c329…); the two later re-freezes (R5r, R5r2) changed only `W3-READER/READER_VERSIONS.md`; `manifest.py verify` of `W3-FAMC/reviews/MANIFEST_R5r2.txt` is OK. So FAMC is not re-read here.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). Paths repo-relative.

## Registry cell (verbatim, `Theory_work/INFRA/registry/claims.tsv:550`)
| id | version | status (verbatim) |
|---|---|---|
| `W3-AUDIT-V:VIS` | 1.0.0 | PROVED-CHECKED; council R4, MANIFEST a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248, sol=9.5 PASS, opus=9.5 PASS |
Registry council cell (the recorded manifest): `R4; MANIFEST 1e298254e4993eeae52dd9acbefea491ccf4884147b15210389dbb6677d29ef6; sol=9.5 PASS(reviews/VR4r3_record_sol.md); opus=9.5 PASS(reviews/VR4r3_record_opus.md)`. Claim span `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md:29-59`, premises :8-27. `manifest.py verify` of `reviews/MANIFEST_VR4r3.txt`: OK.
**Bind your verdict line to `1e298254e4993eeae52dd9acbefea491ccf4884147b15210389dbb6677d29ef6`.** The `VR4r_record_*` and `VR4r3_record_*` files are HQ carriers of earlier verdicts, not reviews of the final text; do not rely on them. `ingest.py convert` is not applicable (already registered).

## Spans (read these; long files in chunks of 120 lines), `Theory_work/Wave3/W3-AUDIT/track_V/`
Final text (the thing to confirm):
1. `V1_VIS/STATEMENT.md:1-88` (v1.5: (VIS-0), (VIS-a), (VIS-b), notation, bad set B, scope note), `V1_VIS/PROOF.md:1-118`, `V1_VIS/CHECK.md:1-18`.
What changed since Sol's V-R1 read (the part Sol never saw): `reviews/DIFF_VR1_to_VR2.patch:1-117`, `reviews/DIFF_VR2_to_VR3.patch:1-104`, `reviews/DIFF_VR3_to_VR4.patch:1-53`, and the three Opus rounds `reviews/VR2_council_opus.md:1-145`, `reviews/VR3_council_opus.md:1-122`, `reviews/VR4_council_opus.md:1-81`; Sol's own V-R1 read for reference: `reviews/VR1_council_sol.md:1-58`, `reviews/VR1_disposition.md:1-14`, `reviews/VR3_post_disposition.md:1-8`.
The dossier lines no seat reviewed: `Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233` (B8; the VR4r re-wording of lines 220 and 233-234, and the VR4r3 change of line 216, "AR and banded with the truths spread apart (study gaps 31–37, ≈ p/5; adjacent mixed-sign AR truths can cancel: ρ = 0.5, θ = (1, −2) lies on B, Lemma VIS)"), with `V1_VIS/PROOF.md:96-112` and `reviews/D18/D18_VERDICT.md` (the design evidence it must match).
Only as needed to judge a point in context: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:581-582, 672-673, 1292` (the three (A4)/(A3) conditions VIS discharges), `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:63-69`.

## The question
1. **Claim:** is Lemma VIS, as stated in STATEMENT v1.5 and proved in PROOF, correct (each of (VIS-0), (VIS-a), (VIS-b): hypotheses, the uniform constant, the topology step for the closed bad set, and the sign route via Stieltjes / M-matrix structure)? Does the uniform-in-n margin claim follow exactly as stated, including the quantifier "for n ≥ n₀" and the dependence of n₀ and the constant on (c₁₆, s₀, θ_lo, θ_hi)? ACCEPT or REJECT.
2. **Sol's V-R1 findings:** were they fixed? State FIXED / NOT-FIXED per finding, one line each.
3. **Opus-only diffs and dossier:** did V-R2/V-R3/V-R4 or the B8 re-wording introduce a wrong step, a scope widening, or a statement of the dossier that claims more than Lemma VIS proves? In particular for TRACK_B.md B8: which designs are said to be inside (spread-out AR, banded, block) must be exactly those the lemma covers; the cancellation example ρ = 0.5, θ = (1, −2) on the bad set B must be consistent with PROOF.
Role: final-text confirmation. Findings only, important points only. Do NOT rewrite, restate what holds, or report nitpicks. Report only a genuine wrong claim, a step that does not follow, an unstated hypothesis, an overreaching dossier sentence, or a status misquote.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `CLAIM W3-AUDIT-V:VIS@1.0.0: ACCEPT | REJECT`; the V-R1 finding lines (FIXED / NOT-FIXED); `DOSSIER-B8: CONSISTENT | OVERREACH`; numbered points (id S4-1, ...; class FLAW / UNSTATED-HYPOTHESIS / STATUS-MISQUOTE / OVERREACH / OBSERVATION; file:line; what and why; minimal fix; severity blocking / local / cosmetic); then, on a line of its own and exactly once (score 0.0-10.0; gates=PASS only if CLAIM is ACCEPT, all V-R1 findings FIXED and DOSSIER-B8 is CONSISTENT):
`COUNCIL-VERDICT round=R4 manifest=1e298254e4993eeae52dd9acbefea491ccf4884147b15210389dbb6677d29ef6 seat=sol score=<x.y> gates=<PASS|FAIL>`
Finish with `COUNT: <n>`.
