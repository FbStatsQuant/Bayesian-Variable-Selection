# Assumption compliance (owner rule of 2026-11-17) — audit Fable, 2026-11-17, for HQ and the owner

**Rule.** Every assumption of every presented theorem must be (1) in Song–Liang or another Bayesian-variable-selection
paper for linear regression, with a verified citation; or (2a) a mathematical or algorithmic fact that is proved; or
(2b) a condition on the data that is argued to be reasonable and expected in an ordinary situation. Otherwise
**ATTENTION**. I was strict: an assumption that merely implies a Song–Liang condition is not counted as class 1.

**Evidence used.** SL = Song and Liang (2015), main text and supplement (pages as in `TRACK_B.md` v1.4). PREC =
`WRITING/Docs/Writing/from_theory/PRECEDENTS_2026-11-17.md` (all citations verified there). Of its papers only the
Bayesian selection ones qualify for class 1: CSV15, NH14, YWJ15, SBJ, SC11; the Lasso and random-matrix papers (ZH08,
BRT09, MY09, RWY, W09, RZ) do not. Track A ids are registry ids on main (statuses quoted). TB = `TRACK_B.md` dossier;
TC = `track_C/RESULTS.md` (Owls part). "pending" = the proof exists but its check or record is not finished.

## Table

| Theorem (card row) | Assumption | Class | Evidence |
|---|---|---|---|
| All | Gaussian linear model, independent Gaussian errors | 1 | SL model (1), density (2), p. 950 |
| All | exact sparsity, s₀ fixed | 1 | SL (4), p. 950 |
| All but 1.3(a) | p ≤ n^A | 1 | PREC B2: SBJ, NH14, SC11; SL Cor S₁, supp p. 16 (n^{κ log n}) |
| 1.1 Thm 1 | bounded coefficients | 1 | PREC B4b: YWJ15, SC11; SL (3), p. 950 |
| 1.1 Thm 1 | eigenvalue floor on bounded sets | 1 | PREC B5: CSV15, YWJ15; SL Condition 3, p. 955; (22), supp p. 13 |
| 1.1 Thm 1 | no near-collinearity on O(log n) columns | 1 | PREC B6: SBJ, NH14 |
| 1.1 Thm 1 | beta-min at √(log n/n) | 1 | PREC B4a: CSV15, YWJ15 |
| 1.1 Thm 1′ | floor on S₀ and a residual-signal margin | 1, by implication | weaker than the two rows above: `W3-POST2:E3.1`, "PROVED-CHECKED" |
| 1.1 expectation display | input `W3-POST:Prop-LB` | 2a, **pending** | "PROVED (by this seat, unchecked)"; implied by the checked `W3-PSHARP:B` (note on dept/theory; relabel) |
| 1.2 Thm 2 | rows i.i.d. Gaussian | 1 | SL verify their Condition 1 for a zero-mean Gaussian process (p. 953) and (26) for a Gaussian process (supp p. 16); NH14 Lemma 6.1 (sub-Gaussian rows; PREC B7b). Ticket #3 would widen it |
| 1.2 Thm 2 | fixed nonzero coefficients | 1 | PREC B4a, B4b; the natural reading of SL's β* (TB B4) |
| 1.2 Thm 2 | population floor on O(log n) columns | 1 and 2b | same kind as PREC B5; follows from a spectral floor; TC: inside and rising with n in all 19 designs |
| 1.3 Thm 3 | (a) none; (b) orthogonal or Gaussian null columns | not a user assumption | witness designs for a lower bound |
| 2.1 Thm 9 | sub-Gaussian predictors on sparse directions | 1 | PREC B7b: NH14 Lemma 6.1 |
| 2.1 Thm 9 | collinearity floor c/n on O(log n) columns | 1 | PREC B6: SBJ, NH14 |
| 2.1 Thm 9 | bounded standardised signal | 1 | PREC B4b |
| 2.1 Thm 9B | fixed floor on bounded sets; beta-min | 1 | PREC B5, B4a |
| 2.1 Cor 9C | exact arithmetic | 1, convention | implicit in SL's own sampler statements (supp pp. 9–10, 12–13); disclosed |
| 2.1 Cor 9C | **the returned list carries posterior mass ≥ n^{−cM/2}** | **ATTENTION** | a property of the run, neither proved nor a data condition; #5′ (in progress) would supply it on designs inside Thm 6 |
| 2.1 Cor 9C | inputs `W1-N1:B`, `W1-N1:F` | 2a, **pending** | "PROVED under the named premises … council-passed" (old label); line check running |
| 3.1 Thm 6 | Gaussian rows, fixed signals, floor on O(log n) columns | 1 | as row 1.2 |
| 3.1 Thm 6 | **visibility given ≤ 15 columns** | **ATTENTION** | not class 1: SL Condition 5 (p. 958) is only its case with no conditioning and no margin. Not 2b by our own evidence: TC finds it failing at the population level on the riboflavin-like design's clustered placement (on/next to B); Lemma VIS (W3-AUDIT-V:VIS) now proves it with a uniform-in-n margin on the sign-route and generic-position designs, incl. D18's spread placement (≥ 0.1, p ≥ 16352) and D19; TB B8 |
| 3.1 Thm 6 | **leakage set \|Q\| ≤ n^b with locality; local regressions in Q** | **ATTENTION** | not class 1: SL remark (a), p. 958, is not a hypothesis. Not 2b in general: TC finds the leak set covering the whole design for factors, S5 and the riboflavin-like design; inside for independent, block, AR ≤ 0.8 |
| 3.1 Thm 6 | floor on Q ∪ {l} | 2b | follows from a spectral floor; TC row P3: rising with n in all 19 designs |
| 3.1 Thm 6 | the code does what the proof says (guard, blocks ≤ 16, start table, LS0, tie rule) | 2a | `W3-AUDIT-A:GW`, `BLK`, `ENC`, `OPC`, `TDP`: "PROVED-CHECKED; council R2, …"; `W3-RM:E4` "PROVED-CHECKED" |
| 3.1 delivery clause | no-output exits inventoried; machine idealisation IDEAL-W⁺ | 2a | `W3-AUDIT-A:P1S3` "CODE-CHECKED (second seat, code reading); council R2, …"; `W3-AUDIT-AX:REP` "PROVED-CHECKED; council R2, …" (vacuous on inputs R can represent) |
| 3.1 delivery clause | declared time and memory at least the method's envelopes | 2b, with a caveat | reasonable in form; at p = 10⁴ the default 24 h is refused by the search's worst-case charge (`HQ_NOW.md:33`), so the clause should state the requirement |
| 3.2 Thm 7, 3.3 Thm 5 | sample-level visibility; bounded leakage or no leakage | **ATTENTION** | same items as 3.1 and 3.6 |
| 3.5 | calibration frozen; exact start; coded moves; frozen-run identities; guard | 2a | `W3-AUDIT-A:CAL-C`, `START-X`, `KER`, `GW`; `W3-AUDIT-AX:FR`: "PROVED-CHECKED; council R2, …"; `W3-READER:PoolZ` "PROVED-CHECKED; council R3, …" |
| 3.5 | inputs `W1-N1:B`, `W1-N1:F`; exact arithmetic, ideal random numbers | 2a pending; 1, convention | as Cor 9C |
| 3.6 Thm 10 | **no leakage** | **ATTENTION** | no precedent; holds on independent designs only (TB B11); the card already says AR and block designs are not covered |
| 3.6 Thm 10 | visibility | **ATTENTION** | as 3.1 |
| 3.6 Thm 10 | start mass, overlap, non-collapse | 2a under the two rows above | `W3-START2-R:IF-START` "PROVED-CHECKED; council R2, …"; `W3-AUDIT-A:OVL` "PROVED-CHECKED, conditional on W1-N1:B; …" |
| 3.7 Thm 8 | floor on (q_n + s₀)-sets; fixed signal bounds | 1 and 2b | same kinds as PREC B5, B4; no visibility or leakage condition |
| 1.4 Thm 4 (if presented) | **response Gaussian given the candidates, with a linear mean** (e.g. omitted predictors jointly Gaussian with the candidates) | **ATTENTION (minor)** | SL Thm 4 asks second moments only (Condition 4, p. 957); joint Gaussianity of omitted predictors is not an ordinary situation. Inputs `C-MIS:Prop-P` ("R02 VERIFIED; … council PASS") and C-MIS:GDb carry old labels: 2a pending |
| Not yet stated | #2 (Theorem 2 from the omitted-variables master), #3 (sub-Gaussian rows), #5′ (list-based outputs) | to classify when stated | #2 would inherit row 1.4's inputs and Prop-LB; #3 moves row 1.2's row law to PREC B7b; #5′ inherits visibility and leakage from Thm 6 |

## ATTENTION items: options and recommendation

Options: (i) a verified Bayesian-selection precedent; (ii) a sharper ordinary-case argument; (iii) narrow the presented
scope; (iv) demote to the supplement.

1. **Visibility (rows 3.1, 3.2, 3.3, 3.6; #5′).** (i) None found: Song–Liang's Condition 5 is the marginal case only.
   (ii) Possible and cheap in part: a lemma that, for a fixed correlation structure, visibility fails only on a
   measure-zero set of coefficient vectors, plus the proved cases (one truth per correlated group, Markov, aligned
   signs). **Done (D112/track V):** Lemma VIS, uniform-in-n margin; it covers D18's spread placement (certified ≥ 0.1) but not its clustered placement. (iii) State the theorem "for designs in which no true
   predictor is masked by 15 others", with the examples and the two failures named. **Recommendation: (iii) now, (ii) as
   a Tier B lemma (1–2 lead-days).** The honest sentence for the paper: this is a condition of the method's first
   stage, as Condition 5 is of Song–Liang's.
2. **Leakage set with locality and local regressions (rows 3.1, 3.2; #5′).** (i) None. (ii) Only for local or grouped
   correlation; it is false for pervasive factors and for the riboflavin-like design, so it cannot be called ordinary
   without qualification. **Recommendation: (iii)** present core 3 as the theorem for local or grouped correlation, and
   present certified screening (row 3.7, all class 1 or 2b) as the guarantee that needs neither condition. Cost:
   writing only. No demotion: it is the main theorem, and the conditions are stated openly.
3. **No leakage (row 3.6).** **Recommendation: (iv) demote row 3.6 to the supplement or a body remark**, keep row 3.5
   (no design assumption) in the main text, and let #5′ carry the printed-output message when it lands. Cost: none.
4. **Corollary 9C's premise on the list's posterior mass.** **Recommendation: (iii)** present 9C as a conditional remark
   until #5′ is proved; then cite #5′ for the premise on designs inside Theorem 6. Cost: none now.
5. **Row 1.4's conditional Gaussianity (minor).** **Recommendation: (iv)** keep it in the supplement with its leading
   example stated as an example, not as an ordinary situation. Cost: none.
6. **Pending 2a items (not ATTENTION, but not yet "proved true").** `W1-N1:B`, `W1-N1:F` (rows 3.5, 3.6, 4.1, Cor 9C):
   finish the running line check. `W3-POST:Prop-LB` (row 1.1, expectation display): relabel from the existing
   implication note. `C-MIS:Prop-P`, C-MIS:GDb (row 1.4, #2): relabel or one line check. Cost: about 1 lead-day in all.
7. **Delivery clause's allocation (caveat, not ATTENTION).** State the time requirement in the clause, or wait for
   Engineering's change of the preflight charge. Cost: none for Theory.

**Not flagged, and why.** Gaussian rows: Song–Liang's own worked case for their Condition 1 and for (26), so class 1,
although real predictors are rarely Gaussian; ticket #3 is the remedy for row 1.2. Exact arithmetic and ideal random
numbers: conventions that Song–Liang's sampler statements also presuppose. Strong factors: the posterior theorems hold
there (floors, TC), and core 3 does not claim them.
