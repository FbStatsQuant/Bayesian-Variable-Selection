# W3-RM2-R — READER_DELTA (draft for CP1; RIDER_RULES §5)

Source of the current reader versions (read only): `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
draft v0.1 (W3-READER CP1, 2026-11-15), §6 "Theorem 6" (Gaussian rows; master RM2-R) and §7 "Theorem 7" (fixed
design; master RM2-F). Nothing here is written in W3-READER's folder; the manager passes this file to HQ.

## 1. What changes, in plain words

* **Theorem 7 (fixed design).** The signal conditions become the standard constant-level ones: each true coefficient
  must exceed a fixed multiple of σ√(log n / n) (not a sequence that is larger by a factor tending to infinity), and
  "visibility" asks each truth to explain at least a fixed multiple of log n units of signal given any 15 other
  columns (not M_n log n with M_n → ∞). With a large leakage set the signal must also beat the size of the set's
  removal directions, now with an explicit constant. Nothing else in the hypotheses changes.
* **Theorems 6 and 7 (conclusion).** The reader versions already say "the run produces output with probability one"
  and "P(Ŝ = S₀) → 1", through two NEW bridges (B6.6, B7.4 to W2-UNI:F-UNI). This ticket's masters state that
  directly: under the standing conventions (exact arithmetic, an idealised machine with unbounded integers — which also lifts two
  fixed size ceilings in the code, see STATEMENT §2 IDEAL-W⁺ — shipped configuration, sufficient allocation) every run
  on every valid non-degenerate input returns output, and P(Ŝ ≠ S₀) ≤ P(S₀ is not the unique best-scoring model) +
  P(the local search from the start mode does not reach S₀). B6.6 and B7.4 are no longer needed.

## 2. New text

**Theorem 7 — assumptions (replace (A1), (A3) and the signal clause of (A5)(b)).** Keep (A2), (A4), (A5)(a) and the
local-regression part of (A5)(b) verbatim. Write C_R := 3(M + σ²), where ‖Xθ*‖² ≤ nM.
- **(A1) Model and posterior conditions.** (S1), (S2), (S3); (A2)–(A5) of Theorem 1; and the beta-min (A6) of
  Theorem 1 (θ*_min ≥ C_β σ√(log n/n) with C_β²φ₀² > c₀(s₀, A), or θ*_min√(n/log n) → ∞).
- **(A3) Visibility.** There is a fixed M_V > (σ√(2A) + √((2A + 1)C_R))² such that δ²_{U,j} ≥ M_V log n for every
  j ∈ S₀ and every U ∌ j with |U| ≤ 15 (large n).
- **(A5)(b), signal clause.** In place of θ*²_min n/(|Q| + log n) → ∞:
  (n − 1)φ₀²θ*²_min/σ² ≥ 32(|Q| + 1) + 64 log(2p) + c log n for a fixed c > max{16, 8(A + 1) + 4(2A + 1)C_R/σ²}.
  (Under (A5)(a) no extra clause: (A1)'s beta-min with C_β²φ₀² large enough suffices — see bridge R7.2.)

**Theorems 6 and 7 — conclusion (one display, unchanged in form).**
$$P(\text{the run produces output})=1\ \text{for every }n,\qquad P(\hat S=S_0)\to1,$$
with the remark: more precisely, for every seed and calibration outcome,
P(Ŝ ≠ S₀) ≤ P(S₀ is not the unique maximiser of the score) + P(the local search from the start mode misses S₀),
and both terms tend to zero. (Remark (i) of Theorem 6 — the search only deletes spurious members, at most n^b moves,
cap never binding — is unchanged.)

**"Why each assumption" lines (Theorem 7; replace (A3), add to (A1)).**
- (A1) beta-min: the order σ√(log n/n) is that of every comparable selection theorem; the constants are proof artefacts.
- (A3): each truth, added alone to any small model that misses it, must explain more than the prior and Occam
  charge for one variable (order log n) plus the largest noise fluctuation among p candidates (order log p); a fixed
  multiple of log n is enough. Not necessary on masked designs (other theorems); the constant is an artefact.
- (A5)(b) signal: removing a truth from a model of the leakage lattice must cost more than the largest noise
  projection on the removal directions (size ≍ |Q| + log n in the worst case; O(log n) on the proxy example).

## 3. Bridges (reader ⇒ master), to be checked with the masters

| # | bridge | mark | detail |
|---|---|---|---|
| R7.1 | (A1) ⇒ (T1-F♭) | identity + B1.1–B1.3 of READER §1 | (A6) of Theorem 1 is BM(c) with c = C_β²φ₀², or BM-∞ (READER B1.4) |
| R7.2 | (A1) (beta-min with C_β²φ₀² ≥ max{c_TL, 8(1 + √(D/2))²} where d_n² ≤ D log n) ⇒ (BM-W⁺) under (A5)(a) | NEW (two lines) | under (A5)(a), |Q| ≤ s₀ + log n, so d_n² ≤ 2(|Q| + 1) + 4 log(2p) ≤ (2 + 4A + o(1)) log n =: D log n; STATEMENT §2 last sentence of (BM-W⁺) |
| R7.3 | (A5)(b) signal clause ⇒ (BM-W⁺) | identity | it is (BM-Q♭) of STATEMENT §2 |
| R7.4 | (A3) = (V♭) | identity | STATEMENT §2 |
| R6/7.5 | conclusions | master | W3-RM2-R:RM2-F-plus, RM2-R-plus with (D) = (S3) (standing conventions of NOTATION §5: "sufficient allocation" must be read as 𝒜_n of STATEMENT §2, re-audited at v3.2) |

R7.2 needs one more look before the final: under (A5)(a), (A1) at BM(c) level gives (BM-W⁺) only if C_β is large
enough relative to c_TL⁰ and D; the reader text should then say "with C_β large enough (explicit in the remark)" — HQ
choice between that and keeping θ*_min√(n/log n) → ∞ as the simple sufficient form in the main text.

## 4. Open for HQ / W3-READER

* Whether the main-text (A3) shows the explicit constant or "a sufficiently large constant M_V (explicit in a
  remark)". Recommendation: the latter, constant in the remark.
* The error split (mode failure + search failure) as a remark or as a second display. Recommendation: remark.
