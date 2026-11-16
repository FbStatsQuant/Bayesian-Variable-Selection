# Council R2 (diff round) disposition (MANIFEST 227720d3d5b3ef95adbc1e91f7835058d7858986ef4b173a4044f65ad49879ea)

Seats (new threads, NORMAL): Sol `R2_council_sol.md` — 4/4 ACCEPT, 8.6, gates=FAIL; Opus `R2_council_opus.md` — 4/4 ACCEPT,
9.2, gates=FAIL. All R1 C/S/F findings RESOLVED (Sol F1–F3; Opus F1–F4). Both seats raise one new F finding on the **same
sentence**, introduced by the R1 fix: `READER_DELTA.md:61-65` ((A0) "why" line).

| finding | seat | tag | disposition (proposed; not applied — MANIFEST_R2 kept intact for HQ) |
|---|---|---|---|
| contrast condition must be centred and carry the (A0) variance | Opus F5 | F | ACCEPT |
| necessity must be stated for the omitted part **minus its linear candidate component**, centred, variance possibly zero | Sol F-R2-1 | F (S) | ACCEPT |
| §1 summary table (`READER_DELTA.md:17`) still has the old selection/uniformity wording | Opus (residual, not raised) | E | ACCEPT with the fix |
| STATEMENT §9 lacks A:MISR-POP-SNR and the (G)-only tagging | Opus (observation) | E | ERRATA at the editorial batch |

**Proposed replacement for `READER_DELTA.md:61-65`** (both seats' fixes combined):
"(A0) is a convenient sufficient form. The proof uses only a weaker condition: given the candidates, the coordinates of
the residual vector y^r − α′1 − x_𝒞β^𝒞 in an orthonormal basis of the vectors orthogonal to the constant vector are
i.i.d. N(0, σ²_𝒞) — centred, with the variance of (A0); nothing is required of the residual's sample mean. When the noise
is Gaussian with variance σ² and independent of all predictors, this holds if and only if the omitted contribution, after
subtracting its linear candidate component, has (given the candidates) such coordinates i.i.d. N(0, σ²_𝒞 − σ²), the
variance possibly zero." (= CorG-min (a) + (c), STATEMENT `:56-59`, `:63-74`.)
`manifest.py bind` on R2: REFUSED (both verdicts gates=FAIL). Cap (v4 §5.8): R1 + one diff round used → HQ decides.
