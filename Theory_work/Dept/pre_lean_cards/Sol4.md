# Sol-4 Fable card: track V R4 (Lemma VIS) + dossier B8; FAMC checked for knock-on

Sol 6.2: `W3-AUDIT-V:VIS@1.0.0` ACCEPT; DOSSIER-B8 OVERREACH; R4 8.5 gates=FAIL, bound to manifest 1e298254. Snapshot: `origin/theory/PRE-LEAN` 6850c3a5.

**Verdict:** Sol is right on both dossier points, judged strictly. They are wording overclaims in `TRACK_B.md` B8 only. **Lemma VIS and Cor-FAMC are not affected.**

## Rulings

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **S4-1** B8 line 216: "Holds when no truth is cancelled by ≤ 15 others: … AR and banded with the truths spread apart" | AGREE | Wording overclaim, twice over (see below) | **No.** `TRACK_B.md` has no registry span. Lemma VIS's span (`V1_VIS/STATEMENT.md:29-59`) already excludes this case in its "Not claimed" list. | Replacement A below |
| **S4-2** B8 lines 219-220: clustered D18 called one of "two concrete failures at the population level" | AGREE | Wording overclaim: only the upper bound 6.9 × 10⁻⁹ on the margin is established; the exact value is nonzero for the U found, and whether the minimum is 0 is not determined (`D18_VERDICT.md`: "neither δ > 0 nor δ = 0 can be certified") | No | Replacement B below |
| **S4-3** registry status cell names digest a125ce4d, council cell names 1e298254 | AGREE | Status bookkeeping. I checked: a125ce4d is `MANIFEST_VR4r`, 1e298254 is `MANIFEST_VR4r3`; the status cell is one re-freeze behind | Registry status cell only, not a claim span | Recorder: re-point the status cell to 1e298254 "(= R4 re-frozen CORRECTION-ONLY as VR4r3)". The sol=9.5 there is the carried V-R1 score; Sol's read of the final text is this 8.5. |

### S4-1: the two overclaims in line 216

1. **"No truth is cancelled" is not enough for a margin uniform in n.** Coefficients can avoid exact cancellation at every n while approaching a limit hyperplane, so the margin tends to 0. Lemma VIS says this itself (last "Not claimed" bullet) and requires δ = inf dist(ϑ_n, B) > 0.
2. **"Spread apart" is not a sufficient condition for mixed-sign AR truths.** Sol's example is correct: gap 31, ρ = 2^{−1/31}, θ = (1, −2) gives Cov(W_{k₁}, Wᵀθ*) = 1 + ρ³¹·(−2) = 0 at U = ∅. What is proved is the quantitative bound (AR-sep) of Cor-FAMC. "Banded" has no spread result at all: Lemma VIS puts banded designs under generic position, (VIS-d)(ii).

### Replacement A (`TRACK_B.md:216`, up to the comma before "(W2-APP family map")

Old: "Holds when no truth is cancelled by ≤ 15 others: bounded blocks with one truth each, AR and banded with the truths spread apart (study gaps 31–37, ≈ p/5; adjacent mixed-sign AR truths can cancel: ρ = 0.5, θ = (1, −2) lies on B, Lemma VIS),"

New: "Holds with a margin uniform in n under the sufficient conditions of Lemma VIS: bounded blocks with one truth each; aligned signs (VIS-a); or coefficients a fixed distance from the closed bad set B (VIS-b; this covers banded designs in generic position). For AR(ρ) with mixed signs, spread alone is not enough: the proved condition is the separation bound (AR-sep) of Cor-FAMC, Σ_{k≠j}|θ*_k||ρ|^{|j−k|} ≤ ½|θ*_j|(1 − ρ²)/(1 + ρ²), which the study's AR(0.5) layouts satisfy (gaps 31–37, ≈ p/5; 0.5³¹ < 10⁻⁹). Mixed-sign AR truths that violate it can cancel: adjacent truths with ρ = 0.5, θ = (1, −2), and truths at gap 31 with ρ = 2^{−1/31}, θ = (1, −2), lie on B (Lemma VIS),"

The cancellation example stays on line 216, so the pointer at `W3-FAMC/STATEMENT.md:93` remains valid.

### Replacement B (`TRACK_B.md:219-220`)

Old: "Track C gives two concrete failures at the population level: a pervasive factor with **mixed-sign** truths (its D14, D15: a set of ≤ 15 columns cancels the truth's covariance with the signal) and the **clustered** placement of the riboflavin-like design (D18; effectively on the bad set B, not certifiably on it: a 15-column U gives |Cov| ≤ 6.9 × 10⁻⁹, exact recomputation)."

New: "Track C gives one concrete failure at the population level, a pervasive factor with **mixed-sign** truths (its D14, D15: a set of ≤ 15 columns cancels the truth's covariance with the signal), and one near-cancellation, the **clustered** placement of the riboflavin-like design (D18: a 15-column U gives |Cov| ≤ 6.9 × 10⁻⁹ by exact recomputation, so any margin is at most that; whether it is exactly 0 is not determined)."

Line 233 ("outside in practice … no usable margin certifiable") is accurate and stays.

## Is Lemma VIS or Cor-FAMC affected?

- **Lemma VIS: no.** Sol ACCEPTs the claim. (VIS-b) carries δ > 0 explicitly, and the statement's "Not claimed" list covers both of Sol's scenarios.
- **Cor-FAMC: no.** Its AR conditions are (AR-s) aligned signs, (AR-sep) the quantitative bound, and (AR-g) δ > 0. Sol's example violates all three: mixed signs with ρ > 0; left side of (AR-sep) is 1 against a right side of about 0.011; and it lies on B. The corollary never uses "spread apart" unquantified. It cites B8 line 216 only in §1b, for the cancellation example, under "nothing below is claimed".
- **Card row 3.1F** says the study's AR(0.5) layouts satisfy the conditions; that is FAMC §1b(iii) with C-GROW (C5)(c), specific to ρ = 0.5. No change.
- **One residue, not for action:** `V1_VIS/PROOF.md:109-110` says the clustered placement is "effectively on B … like D14, D15". "Effectively" hedges it and Sol accepted the file; I would leave it unless that file is reopened.

## Process consequences of editing B8

`TRACK_B.md` is an EXT input of both `MANIFEST_VR4r3` (track V) and `W3-FAMC/reviews/MANIFEST_R5r2`. The edit therefore needs a CORRECTION-ONLY re-freeze of track V and a CITATION-ONLY re-freeze of FAMC; no claim text changes in either.
