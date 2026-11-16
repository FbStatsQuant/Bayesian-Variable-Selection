# W3-MISR-R — council R2 (diff round), seat `opus`

Manifest reviewed: `MANIFEST 227720d3d5b3ef95adbc1e91f7835058d7858986ef4b173a4044f65ad49879ea` (`reviews/MANIFEST_R2.txt`).

**Manifest check.** I recomputed the sha256 of every entry in MANIFEST_R2: all 17 ticket files and all 11 EXT files match.
Diffing MANIFEST_R1 against MANIFEST_R2 shows that only `DEPS.tsv`, `ERRATA.md`, `READER_DELTA.md`, `REPORT.md` and
`deps_hand.py` changed. This agrees with `reviews/R2_diff_since_R1.txt`.

**What I read.**
- My R1 review.
- The diff.
- `STATEMENT.md` §§1–5, §7 and §9 (unchanged), as the masters of the changed text.
- BASE `W3-MISR/STATEMENT.md:108-123` (MIS(i)).

**Tool runs (nothing written).**
- `deps_hand.py`, run in memory with its write redirected: its output is byte-identical to `DEPS.tsv`.
- The same run with the S:notation checked_sha perturbed: STALE now propagates transitively to every dependent row,
  including the depth-2 rows L:G2_corr and L:H2_uniform.
- `citecheck.py`, run with its final write disabled: 152 checks, 0 failures, identical to `reviews/CITECHECK.txt`.
- The working tree was clean before and after.

## (a) R1 findings

| R1 finding | verdict / action | reason |
|---|---|---|
| F1 (A0 "necessary") | **RESOLVED** | `READER_DELTA.md:61-65` now calls (A0) "a convenient sufficient form". It says the proof uses only the contrast condition, and that under Gaussian noise independent of the predictors this condition holds iff the omitted part has the same property. That is CorG-min (a)+(c) (`STATEMENT.md:63-74`). The Cauchy-intercept counterexample is now consistent with the text. (The new wording has its own defect on the mean of the contrasts, F5 below.) |
| F2 (uncentred reference) | **RESOLVED** | `READER_DELTA.md:52-53` now reads "around this law, with its mean centred over the sample (the fitted mean carries no intercept)". Centring α′ + x_iᵀβ^𝒞 gives (Cxβ^𝒞)_i = μ_i(κ) of `STATEMENT.md:33-34`. B4.4 records "the reference is centred". |
| F3 (selection premise; uniformity) | **RESOLVED** | Part (i): `:55` now reads "posterior mass of S₀^𝒞 tends to one in probability", which is A:SEL-P / CorH-plus (a′) (`STATEMENT.md:114`). Part (ii): `:56-57` now reads "uniformly over any class … with common constants and bounded support size on which this convergence is uniform", which is (U-a) with (UP) (`STATEMENT.md:139-142`). B4.4 maps each sentence to its premise. *Residual (unchanged text, not raised):* the §1 change-summary table (`READER_DELTA.md:17`) still says "selects the support with probability → 1; uniform over configurations". This is the summary for HQ, not the reader statement, but the lead should align it with `:55-57` so the old wording is not copied forward. |
| F4 (registry assumption lists) | **RESOLVED** | CorGb-plus (`REPORT.md:54`) now lists A:MISR-OVC, whose text (`:46`) contains (N), and the new A:MISR-POP-SNR. Its text matches `STATEMENT.md:102-103` (energy bound ≤ M₀σ²_𝒞; liminf ρ^{BM} > 16c₀/c_R). CorH-U (`:70-71`) adds the five §3 ids, marked "through clause (G) only", and its premises add `STATEMENT.md:94-108`. |
| E1 | deferred (ERRATA E2) | |
| E2 | deferred (ERRATA E3) | |
| E3 | partly applied, rest deferred | Applied: CorG-min premises +`:184-185`; CorH-plus depends_on +CorG-min; CorH-U premises +§3; `REPORT.md:15` rewritten. Deferred: the "pointer only" note (ERRATA E6). |
| E4 | applied | `uses` entries completed (S:CorH-U, L:G1_min, L:G2_corr). DOWNSTREAM is now marked by iteration to a fixed point (verified above). |
| E5 | applied | Σ_𝒞𝒞 is assumed invertible, with Moore–Penrose for the singular case; the noise rows are iid and independent of the candidates; B4.1 says "for all large n". |
| E6 | applied | B4.4 maps the uniform-in-v sentence to W3-MISR:MIS(i)@1.0.0, BASE `:110-114`. I checked that `:114` says the constants are free of v. |
| E7 | deferred (ERRATA E4) | |
| E8 | deferred (ERRATA E5) | |

## (b) Does the diff break anything?

**F5 (F, new, introduced by the diff) — `READER_DELTA.md:61-64`: the "weaker condition" does not centre the contrasts
and does not fix their variance.**

*The text.* "The proof uses only a weaker condition: given the candidates, the coordinates of the residual vector
y^r − α′1 − x_𝒞β^𝒞 in an orthonormal basis of the vectors orthogonal to the constant vector are i.i.d. Gaussian with a
common variance".

*What the master needs.* The proof needs (GR^c | σ(X_𝒞)) at κ_n with deterministic (β^𝒞, σ²_𝒞): Uᵀ(residual) | X_𝒞 ~ N_N(0, σ²_𝒞 I_N). The
reader condition is strictly weaker in two ways:
- Taken literally, "i.i.d. Gaussian" in a fixed basis U allows a common mean m ≠ 0.
- Read conditionally on the candidates, the "common variance" may depend on the design. CorGb-plus, through (A3), needs a
  deterministic σ²_𝒞.

*Failure.* Take residual contrasts i.i.d. N(m, σ²_𝒞) with m ≠ 0 constant. The response then carries the omitted direction
w := mU1_N ∈ 1^⊥, with ‖w‖² = m²(n − 1). This is a fixed predictor outside the candidate span. Its squared correlation
with a standardised Gaussian candidate column is of order m²·χ²₁. Over p = n^A columns, the largest such term is of order
m² log n. For m²/σ²_𝒞 above a constant, this is the same order as the beta-min threshold. So the conclusion
E[1 − π(S₀^𝒞)] = O(√(log n/n)) is not given by any master under the stated condition.

*Context.* The R1 fix I proposed for F1 ("Gaussian contrasts of the residual given the candidates") had the same
looseness. The lead's more explicit "i.i.d. … with a common variance" makes it visible.

*Fix (one phrase).* "… are i.i.d. N(0, σ²_𝒞) (centred, with the variance of (A0))". The iff sentence at `:64-65` then
holds as CorG-min (c), with τ² = σ²_𝒞 − σ² ≥ 0 and centred omitted contrasts.

**No other new C/S/F.**
- REPORT edits: the status lines are untouched. The new premises and depends_on entries are correct, and A:MISR-POP-SNR
  matches its statement lines.
- The ERRATA rows are editorial queue entries only.
- DEPS / `deps_hand.py`: the output is correct and terminates (rows move only OK → DOWNSTREAM).
- The new READER_DELTA Example text agrees with (E1)/(E2).
- B4.4's new mappings are correct.
- *Observation (no finding raised, per brief):* `STATEMENT.md` §9 (`:199-204`) does not list the new id A:MISR-POP-SNR.
  It still tags A:GAUSS-CAND-ROWS and A:CORR-FLOOR "CorGb-plus (only)", although REPORT now also attaches them to CorH-U
  (G). REPORT defines the new id in place with its line range. Align §9 at the editorial batch.

## (c) Per-claim decisions

| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

STATEMENT and the lemmas are unchanged (same hashes as R1). My R1 line-by-line acceptance stands. F5 is in a derived
reader text, not in any claim or proof.

## (d) Gates on manifest R2

- `correct`: **PASS** — no proof text changed; the R1 verification of all four proofs stands.
- `strength`: **PASS** — no claim states more than its proof gives (STATEMENT unchanged).
- `faithful`: **FAIL** — F1–F4 are resolved, but the new reader sentence `READER_DELTA.md:61-64` states a sufficient
  condition weaker than any master's hypothesis (F5).
- `statuses`: **PASS** — the REPORT status lines are unchanged and verbatim. The conditional lists are complete.
- `sweep`: **FAIL** — the diff sweep is done (manifest, tools, masters, bridges), but it found a blocking F finding (F5).
- `reader`: **FAIL** — READER_DELTA's (A0) explanation claims beyond CorG-min (c) and CorGb-plus (F5).

## (e) Score and verdict

Score 9.2. All four R1 blocking findings are resolved, and the DEPS tool defect is fixed. One new F finding (F5) remains.
It is a one-phrase wording fix ("centred, with the variance of (A0)") and needs no new mathematics.

COUNCIL-VERDICT round=R2 manifest=227720d3d5b3ef95adbc1e91f7835058d7858986ef4b173a4044f65ad49879ea seat=opus score=9.2 gates=FAIL
