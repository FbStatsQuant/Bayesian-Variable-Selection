# V-R4 diff check — seat `opus` (Claude Opus 5.5, high) — V1 Lemma VIS v1.4 → v1.5 (scope-text correction)

**Frozen content.** `MANIFEST_VR4.txt` first line `MANIFEST 8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0`;
`manifest.py verify` → `verify: OK` (run 2026-11-17 from `/home/fb31/BVS-wt/W3-AUDIT`). No git state changed; this is the
only file written.

**Read (as allowed).** `V1_VIS/{STATEMENT,PROOF,CHECK}.md`; `reviews/DIFF_VR3_to_VR4.patch`; `reviews/VR3_post_disposition.md`;
`reviews/D18/{D18_VERDICT.md, D18C_reply_opus.md, d18.py, d18_output.txt}`; `c_designs.py` (`Design.spread/clustered`,
`LowRank`, `_real`, the `DESIGNS` table); `TRACK_B.md:209-233`; `track_C/RESULTS.md`.

**Own checks.**
- `_real` (`c_designs.py:239-252`): p ≤ p₀ is a sorted random row subset of the fixed Σ₀ = L₀L₀ᵀ + 0.1 I (`LowRank`, diagonal set
  to exactly 1 in `sigma_rows`); p > p₀ is the tiling j ↦ row j mod p₀ of copy ⌊j/p₀⌋ with Σ_jk = 0 across copies. D18 and D19
  use the same function (`DESIGNS` 18, 19). So every labelled local matrix Σ_{n,V} (|V| ≤ 15 + s₀) is a labelled principal
  submatrix of Σ₀ with zero cross-copy blocks: finitely many over all n. The floor needed by (VIS-d): λ_min(LLᵀ + 0.1I) ≥ 0.1
  for any L, and the diagonal reset moves it by at most the row-norm tolerance (`assert ... atol=1e-6`; for D18 measured
  4.8e-14), so c_m ≥ 0.1 − 10⁻⁶ > 0 for both D18 and D19. (VIS-d)(i) applies. ✓
- Spread threshold: positions k·⌊p/4⌋, copy ⌊k⌊p/4⌋/4088⌋. p = 16351 → copies (0, 0, 1, 2); p = 16352 → (0, 1, 2, 3);
  p = 20000 → (0, 1, 2, 3). For ⌊p/4⌋ ≥ 4088 consecutive positions differ by ≥ 4088, so the copies are distinct; "four
  different tiles for p ≥ 16352" is exact (and sharp). ✓
- Block-diagonal Σ and Σ_UU across copies ⇒ Γ^U_{jk} = 0 for truths in different copies ⇒ γ(U, j) = Var(W_j|W_U)·e_{i(j)}:
  every direction is a coordinate vector, B = coordinate hyperplanes, dist(ϑ, B) = min_k|θ_k| = 1.0 (θ = (1.4, −1.0, 1.8,
  −1.2)), c̲ ≥ 0.1 − 5e-14, a ≥ 0.1·min_k|θ_k|. ✓
- Clustered: D18C's U (15 columns) gives Cov(W_0, Wᵀθ*|W_U) = −6.896e-9, Var 0.529, recomputed in exact rationals two ways
  (agreement ~9 digits, nonzero). |⟨ν, ϑ⟩| = |Cov|/|γ| ≤ |Cov|/Var = 1.30e-8 = the verdict's dist(ϑ, B) bound. ✓
- (VIS-b), (VIS-c) premises re-read: (VIS-b) needs only c̲ > 0, δ > 0 (no countability) ⇒ "(VIS-b) still applies whenever
  δ > 0" is correct. ∪_n 𝒩_n is a countable union of finite sets ⇒ "every design sequence has countably many local patterns
  (finitely many at each n)" is correct. For s₀ = 2, an arc of directions in 𝒩 makes B a double cone with interior ⇒ "B may
  then have interior" is correct.

## Findings
| id | grade | location | finding | suggested fix |
|---|---|---|---|---|
| E-1 | E | STATEMENT "Not claimed" bullet 2 | "fall under (VIS-d)(i)" gives only finiteness of 𝒩 (so (VIS-c) applies and dist(ϑ, B) is a finite minimum); it does not say the D18 placements are visible. A reader of the STATEMENT alone may read "D18 covered" as "D18 inside", while D18's clustered placement is numerically on B (margin ≤ 6.9e-9) and its spread placement is ≈ 0 for p < 16352. The PROOF remark and bullet 1 together are correct; the STATEMENT is not wrong. | Append e.g. "(whether ϑ ∉ B is a separate question: D18's clustered placement is numerically on B, see the PROOF remark)". |
| E-2 | E | STATEMENT "Not claimed" bullet 2 | "only their closure can be uncountable … when the closure 𝒩 is uncountable": "their" refers to the local patterns ℒ, and the example (entries dense in an interval) is an uncountable ℒ̄; the excluded case is an uncountable 𝒩 (closure of the *directions*). An uncountable ℒ̄ need not give an uncountable 𝒩. No false statement ("may"), but the two closures are conflated in one sentence. | "only the closure of the patterns (and hence possibly 𝒩) can be uncountable". |
| E-3 | E | PROOF remark, D18 clustered | "effectively on B …, like D14, D15": D14's and D15's *clustered* placements are visible (track C: D14 2.9 → 100, D15 → 51; D14 clustered is listed as a (VIS-a) instance in the same remark); the analogy is to their *spread* placements (population value 0). Also the clustered computation is for p > 4088 (fixed rows 0, 214, 660, 295 of copy 0); the spread sentence carries its p-range, the clustered one does not. | "like the spread placements of D14, D15"; add "(p > 4088)". |
| E-4 | E | PROOF remark "(up to 5 × 10⁻¹⁴)" (and D18_VERDICT, not in the diff) | The 5e-14 is a Weyl bound from max|diag − 1| = 4.8e-14 and the exact λ_min(LLᵀ + 0.1I) = 0.1 (rank 70); it is correct. D18_VERDICT attributes it to "D18C E-1", which reports the numerical λ_min = 0.09999999999976 (0.1 − 2.4e-13, eigensolver roundoff). Attribution only; immaterial to a ≥ 0.1. | Optionally state the Weyl basis in D18_VERDICT. |

No C, S or F finding.

## Diff-hunk verdicts
| hunk | content | verdict |
|---|---|---|
| PROOF @@1 | header v1.4 → v1.5 | OK |
| PROOF @@102 | D18, D19 moved into the "(VIS-b) cases" list as one-fixed-matrix designs with finitely many local patterns ((VIS-d)(i)); D18 finite computation: spread four tiles for p ≥ 16352, coordinate directions, a ≥ 0.1·min|θ| (up to 5e-14); clustered effectively on B, 15-column U, |Cov| ≤ 6.9e-9, exact recomputation | **OK** — faithful to D18_VERDICT / D18C / d18_output and to `_real`; every number checked (above). Nothing stronger than the computation: the spread claim is a proof (block-diagonal argument), the clustered claim is stated as an upper bound ("effectively", "|Cov| ≤"), not as δ = 0. E-3, E-4 editorial. |
| STATEMENT @@1 | header v1.4 → v1.5 | OK |
| STATEMENT @@67 | "Not claimed" bullet: false D18 exclusion replaced by: uncountable closure 𝒩 is what escapes (VIS-c); countably many patterns always; B may have interior; (VIS-b) still applies when δ > 0; D18, D19 under (VIS-d)(i) | **OK** — correct; removes the refuted claim; D18 and D19 now treated identically (same `_real` recipe). E-1, E-2 editorial. |
| STATEMENT @@82 | changelog row v1.5 | OK — no clause changed; tag "STRONGER (scope)" is the right direction (a design moved from "no claim" into (VIS-d)(i)); trigger and check columns resolve. |

## Task answers
1. **New bullet correct: yes.** Each component verified: countably many patterns (finite at each n); only an uncountable
   closure 𝒩 escapes (VIS-c) and then B may have interior; (VIS-b) needs no countability; D18, D19 are sub-panels/tilings
   of one fixed matrix ⇒ finitely many labelled local patterns with c_m ≥ 0.1 − 10⁻⁶ ⇒ (VIS-d)(i). The refuted "uncountable
   local patterns" claim is gone, and the D18/D19 inconsistency is removed (both now in (VIS-d)(i) in the STATEMENT and in
   the same PROOF list).
2. **Proof remark faithful: yes.** p ≥ 16352 exact and sharp; coordinate directions and a ≥ 0.1·min_k|θ_k| follow from
   block-diagonality; 5e-14 is a valid Weyl bound; |Cov| ≤ 6.9e-9 at a 15-column U with exact rational recomputation is
   D18C's value (−6.896e-9), carried by D18_VERDICT. No claim exceeds the computation (no δ = 0 claim; "effectively").
3. **Other hunks: no error.** Headers and changelog consistent; CHECK.md already records v1.5 and "V-R4 pending".

## Gates (on the changed content)
| gate | reading used here | result |
|---|---|---|
| G1 | mathematical correctness of changed statements | PASS |
| G2 | proof/remark faithful to the cited computation | PASS |
| G3 | scope ("Not claimed") consistent with clauses and with the designs | PASS (E-1, E-2 editorial) |
| G4 | citations, paths, numbers resolve | PASS (E-4 attribution, outside the diff) |
| G5 | versioning / changelog tag | PASS |
| G6 | no claim stronger than the evidence | PASS (E-3 wording) |

(The brief names G1–G6 without defining them in the files I was allowed to read; the readings above are mine.)

## Claims
| claim | verdict |
|---|---|
| V1 | ACCEPT |

**Score 9.5 / 10** — minimal, correct fix of the refuted scope text; D18 remark faithful and checked number by number; four
editorial items, none blocking.

COUNCIL-VERDICT round=R4 manifest=8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0 seat=opus score=9.5 gates=PASS
