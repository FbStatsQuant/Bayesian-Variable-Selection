# W3-MISR-R — council round R3 (HQ-ordered diff round), seat `opus`

Seat: Claude Opus 5.5, fresh agent, effort high. Content reviewed: MANIFEST 43b2366bf27f0e778853274910883be7587f1a43600e079bb8a83f2d53b1d0ab
(`reviews/MANIFEST_R3.txt`).

## Checks done

- `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-MISR-R reviews/MANIFEST_R3.txt` →
  `verify: OK MANIFEST 43b2366b…d0ab`. I also recomputed the sha256 of every manifest row (17 ticket files and 11 EXT
  files); all match.
- `diff MANIFEST_R2.txt MANIFEST_R3.txt`: only the header and the `READER_DELTA.md` row differ (34afe8e6… → 10babe4a…).
  No file was added or removed. **`READER_DELTA.md` is the only file whose hash changed.**
- `R3_diff_since_R2.txt` matches the repository: `git show 8d335893:READER_DELTA.md` has hash 34afe8e6… (R2) and
  `f7dd0389` has hash 10babe4a… (R3). The ± lines of `git diff 8d335893 f7dd0389` are byte-identical to the ± lines of the
  diff file. The diff touches exactly two places: row "remark" (`READER_DELTA.md:17`) and the (A0) bullet of §3
  (`READER_DELTA.md:61-66`).
- Masters read: `STATEMENT.md` §1–§2 (:25-92), §3 (for CorGb-plus's hypotheses), §4–§5 (:110-155). I also read BASE
  `W3-MISR/STATEMENT.md` (GR^c) at :36-43 and (GR^c | 𝓕_n) at :144-149. The rest of `READER_DELTA.md` was read for context
  only. Only F5 and F-R2-1 were read from the R2 reviews.

## (a) Carried findings

| finding | decision | reason |
|---|---|---|
| F5 (opus R2: contrasts not centred, variance not fixed) | **RESOLVED** | `READER_DELTA.md:63` now says "i.i.d. N(0, σ²_𝒞) — centred, with the variance of (A0)". That is (GR^c \| σ(X_𝒞)) (BASE :144-149) with the deterministic σ²_𝒞 that (A3) and CorGb-plus need. A common mean m ≠ 0 and a design-dependent variance are both excluded. |
| F-R2-1 (sol R2: no subtraction of the linear candidate component) | **RESOLVED** | `:65-66` now requires the condition of "the omitted contribution, after subtracting its linear candidate component", with law N(0, σ²_𝒞 − σ²) and "the variance possibly zero". This is (OV^c) (`STATEMENT.md:57-59`) with γ = β^𝒞 − β_𝒞 and τ² = σ²_𝒞 − σ² ≥ 0. Sol's counterexample (Z = bX₁ + ζ) now satisfies both sides of the iff. |

## (b) Does the diff introduce a new C, S or F finding?

**No new C, S or F finding.**

**The changed sentence (`READER_DELTA.md:61-66`) against CorG-min (a)+(c):**
- *The condition.* The coordinates of y^r − α′1 − x_𝒞β^𝒞 in an orthonormal basis of 1^⊥, given the candidates, are
  i.i.d. N(0, σ²_𝒞). This is exactly Uᵀ(y^r − X_𝒞β^𝒞) | X_𝒞 ~ N_N(0, σ²_𝒞 I_N), i.e. (GR^c | σ(X_𝒞)) at
  κ_n = (X_𝒞, β^𝒞, σ²_𝒞). The term α′1 is annihilated by Uᵀ. The law is spherical, so the choice of basis does not
  matter. "Nothing is required of the residual's sample mean" is correct: (GR^c) constrains only Uᵀ(·) (BASE :38-40, random
  intercept allowed).
- *Sufficiency.* CorG-min (a) gives (N) + (OV^c) ⇒ (GR^c | σ(X_𝒞)), which feeds MIS-R (ii). Under (A0) the residual
  condition is itself (GR^c | σ(X_𝒞)), so "a weaker condition that the proof uses" is the (GR^c) hypothesis of the
  master chain. (A0) implies it, as bridge B4.0 records.
- *Equivalence under Gaussian noise.* The sentence says "noise Gaussian with variance σ², independent of all
  predictors". This is (N), and the structural model of the Example (`:43-44`, ε ~ N_n(0, σ²I) independent of the rows)
  fixes the noise as centred. The sentence then says: residual condition ⇔ the omitted contribution minus its linear
  candidate component has, given the candidates, i.i.d. N(0, σ²_𝒞 − σ²) contrast coordinates.
  - ⇐ is (a) with γ := β^𝒞 − β_𝒞 and τ² := σ²_𝒞 − σ². N_N(0, 0) = δ₀ is admitted by §1.
  - ⇒ is (c) with constant v = σ²_𝒞. It gives v ≥ σ² a.s. and (OV^c) with the same γ and τ² = (v − σ²)₊ = σ²_𝒞 − σ².
  - "Possibly zero" is the case τ² = 0, which (OV^c) allows (τ² ≥ 0, with σ²_𝒞 > 0 kept by (A0)).
- *Reading of "its linear candidate component".* The sentence fixes β^𝒞, so the only consistent reading is
  x_𝒞(β^𝒞 − β_𝒞). It is unique up to directions with Uᵀx_𝒞δ = 0, which do not affect the contrasts; compare the
  non-uniqueness remark of CorG-min, `:88-91`. In the Example it is the population regression term
  x_𝒞Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜. So this is faithful. It does not overstate (d), the Cramér converse, which the sentence does not
  invoke.

So the sentence is exactly what CorG-min (a)+(c) give: sufficiency, and under (N) equivalence. It has centred contrasts,
variance σ²_𝒞 for the residual, and σ²_𝒞 − σ² ≥ 0 (possibly 0) for the omitted part after its linear candidate component
is subtracted.

**Row "remark" (`READER_DELTA.md:17`) against CorH-plus (a′), CorH-U (U-a), (RD), (G):**
- "Hellinger and Kullback–Leibler in-sample versions": the sets H^a, K^a (h̄_n, k̄_n of §1). This matches (a′) and (U-a).
- "Around the (A0) law with its mean centred over the sample": the reference is N(μ_i(κ), v) with μ(κ) = Cxβ (BASE
  :33, :187-191). This matches the §2 remark (`:52-54`) and B4.4.
- "For a fixed design whenever the posterior mass of the support tends to one in probability": this is (a′)'s premise
  δ_n → 0 in P_{κ_n}-probability. (OS) and the margin are not assumed.
- "Uniformly over any class on which this convergence is uniform": this is (U-a) with (UP).
- "Random designs by conditioning": this is (RD), with (G) as the Gaussian-row instance used by the theorem (B4.4).

The cell does not repeat the standing class hypotheses (κ_n ∈ 𝒦^F_n: size, energy bound, floor; classes 𝒦^♭_n ⊆
𝒦^F_n(≤s̄, A, M, φ₀) with common constants). I do not count this as an F finding, for two reasons:
- §1 is the plain-words change summary for the manager and HQ. It is not text that ships into the row, and its master
  column points to CorH-plus and CorH-U.
- The governing reader sentence (`:55-57`) states those hypotheses explicitly: "with the energy bound and a floor on
  S₀^𝒞" and "common constants and bounded support size".

The R2 wording of this cell had the same level of compression and was accepted by both seats. The new wording is strictly
more precise: it names the centred reference and replaces "uniform over configurations" with the (UP) qualifier.

**Consistency with unchanged text.** The new §3 sentence agrees with:
- B4.0, which maps (A0) to (N) with q = 0 and (OV) with γ = 0, τ² = 0, a special case of the iff;
- the Example and the linear-plus-noise sentence (E1, E2);
- the §2 remark's "mean centred over the sample".

## (c) Per-claim decisions

| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

STATEMENT and the lemmas have the same hashes as in R2, where both seats accepted them. The diff gives no reason to
reopen them. CorG-min (a), (c) and CorH-plus (a′) / CorH-U (U-a), (RD), (G) were re-read against the changed text above.

## (d) Gates (on MANIFEST_R3)

- **correct: PASS** — the changed sentence and row state only what CorG-min (a)+(c), CorH-plus (a′) and CorH-U (U-a),
  (RD), (G) prove. The iff is checked in both directions, including the zero-variance case.
- **strength: PASS** — the residual condition is (GR^c | σ(X_𝒞)), neither weaker (centred, variance σ²_𝒞) nor
  stronger than the masters' hypothesis. The necessity side carries the subtraction and τ² ≥ 0.
- **faithful: PASS** — the wording matches (OV^c) and (GR^c) term by term, and the row matches its four masters. The
  hypotheses the row compresses are stated in the governing reader sentence `:55-57`.
- **statuses: PASS** — unchanged by the diff. READER_DELTA still says the new masters are not yet checked and that the
  row keeps its current masters until CP3 and HQ adoption (`:5-7`, §5).
- **sweep: PASS** — the manifest verifies, READER_DELTA is the only changed file, the diff file matches git, both changed
  places are checked against their masters, and they are consistent with the unchanged neighbouring text (§2 remark,
  B4.0, B4.4).
- **reader: PASS** — both R2 reader findings (F5, F-R2-1) are resolved. The new sentence is precise and readable, and it
  introduces no new defect.

## (e) Score and verdict

Score 9.6. No C, S or F finding remains: both carried findings are resolved by a sentence that is exactly CorG-min
(a)+(c), and the summary row is faithful to its masters. Nothing in the diff gives a reason to deduct for correctness or
strength. The small deduction reflects that the §1 summary cell relies on the §2 sentence for the class hypotheses.

`COUNCIL-VERDICT round=R3 manifest=43b2366bf27f0e778853274910883be7587f1a43600e079bb8a83f2d53b1d0ab seat=opus score=9.6 gates=PASS`
