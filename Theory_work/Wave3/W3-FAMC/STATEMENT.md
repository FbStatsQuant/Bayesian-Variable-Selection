# W3-FAMC — STATEMENT v1.1 (2026-11-17; lead: Claude Opus 5.5, high; design-family corollary for core 3)

Ticket W3-FAMC (owner GO via HQ, 2026-11-17; brief `Theory_work/Dept/briefs/W3-FAMC_LEAD_BRIEF.md` on dept/theory).
Core 3 = card row 3.1 = reader Theorem 6 ([RV] row thm6), used in Theorems 5 and 10. **Assembly only:** no theorem is
changed, no hypothesis of Theorem 6 is weakened, and no new lemma is introduced. The corollary replaces Theorem 6's
visibility (A3), leakage (A4), floors (A5) and local-regression (A6) conditions by primitive conditions for two design
families. Not a Lean target. Asymptotic (n → ∞). This file **asserts no proof status**: proofs go in `lemmas/`, and
statuses go in the checkpoints. v1.1 = v1.0 with the manager's pre-review items: a reader version (§1R), remarks moved
outside the corollary (§1b), citecheck-form pointers, and full verbatim statuses with D126 expansion (§4). HQ read v1.0
(GO for Tier B, 11-17).

**Aliases.** [RV] = `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` (row thm6, `:660-813`); [NOT] =
`Theory_work/Wave3/W3-READER/NOTATION.md`; [VIS] = `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` v1.5;
[RM2] = `Theory_work/Wave3/W3-RM2/STATEMENT.md`; [L6] = `Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md`;
[RM2R] = `Theory_work/Wave3/W3-RM2-R/STATEMENT.md`; [GROW5] = `Theory_work/Wave1C/C-GROW/lemmas/L5_instances.md`;
[TB] = `Theory_work/Wave3/W3-AUDIT/TRACK_B.md`; [RM] = `Theory_work/Wave3/W3-RM/STATEMENT.md`; [CG] =
`Theory_work/Wave1C/C-GROW/STATEMENT.md`. All on main a779c1df (the cited files are unchanged since f0b8246c).

**Symbols.** W ~ N_p(0, Σ_n) is a standardised row; Cov(·, · | W_U) is the partial covariance ([NOT] `:161-164`).
S₀ = supp θ*, s₀ = |S₀|, and ϑ = (θ*_k)_{k∈S₀}. K = min(p, ⌊n/2⌋) ([NOT] `:60`). In this file **ρ is the AR correlation**,
and Theorem 6's locality exponent (called ρ in [RV]) is written **ϱ**.

## 0. Setting (Theorem 6's own, unchanged)

The rows of X^r are i.i.d. N_p(m_n, Σ_n), with Σ_n a positive definite correlation matrix, and
y^r = α1 + Xθ* + ε with deterministic θ*. Theorem 6 (A1): (S1) Gaussian noise, fixed σ*² > 0, independent of the design;
(S2) n → ∞, 2 ≤ p ≤ n^A for a fixed A ≥ 1 (p ≫ n allowed); (S3) the method as coded, under the standing conventions
([RV] `:28-31`). Theorem 6 (A2): s₀ ≥ 1 fixed, and θ_lo ≤ |θ*_j| ≤ θ_hi on S₀ for fixed 0 < θ_lo ≤ θ_hi. The delivery
conventions (S4) ([RV] `:32-50`) are used only for the delivery clause.

## 1R. Reader version (for the H5 card and Writing; the technical version is §1)

**Corollary (block and AR designs).** Suppose the predictors are Gaussian and their correlation is either *block*
(independent groups of bounded size, each well conditioned) or *autoregressive* with any fixed correlation ρ, |ρ| < 1.
Suppose the number of true predictors is fixed, their coefficients are bounded away from zero and infinity, and the
true coefficients cannot cancel each other: one true predictor per group, or true predictors with
aligned signs, or (for AR) true predictors spread apart, or more generally coefficients a fixed distance away from a
closed null set of cancelling configurations. Then, with probability tending to one, every run of the method that
returns a result reports exactly the true model (Theorem 6's conclusion, delivery clause included).

## 1. Corollary FAMC (core 3 on block and AR designs)

Assume the setting of §0, and that (Σ_n, θ*) belongs to one of the two families below for every n ≥ n₀.

**(BLK) Block correlation.** There is a fixed g ≥ 1 and a fixed c > 0, and for each n a deterministic partition of [p]
into groups G₁, …, G_m (any sizes ≤ g, in any column order), such that Σ_n is block-diagonal on this partition
(Σ_{n,lk} = 0 when l and k lie in different groups) and λ_min(Σ_n) ≥ c. The coefficients satisfy one of:
- **(BLK-1) one truth per group:** each group contains at most one element of S₀;
- **(BLK-s) aligned signs within groups:** for every group G with |G ∩ S₀| ≥ 2 there are signs d_l ∈ {−1, +1},
  l ∈ G, such that diag(d)(Σ_{n,GG})⁻¹diag(d) has nonpositive off-diagonal entries, and d_k·sgn θ*_k is the same for all
  k ∈ G ∩ S₀ (for example, equicorrelated groups with correlation in [0, 1) and equal signs inside each group);
- **(BLK-g) generic position:** inf_{n≥n₀} dist(ϑ_n, B) > 0, where B is the bad set of Lemma VIS for this design
  sequence ([VIS] `:27`): a closed union of hyperplanes through 0. When the group matrices take finitely many values
  over n, B is a finite or countable union of hyperplanes, so it is Lebesgue-null and nowhere dense.

**(AR) Autoregressive correlation.** Σ_{n,lk} = ρ^{|l−k|} in the given column order, for a fixed ρ ∈ (−1, 1). This is
"moderate" in the sense of correlation bounded away from ±1; no uniformity in ρ is claimed. The coefficients satisfy one
of:
- **(AR-s) aligned signs:** sgn θ*_k is the same for all k ∈ S₀ when ρ > 0, and sgn θ*_k = σ·(−1)^k for a common σ when
  ρ < 0. There is no condition when ρ = 0.
- **(AR-sep) truths spread apart:** ρ ≠ 0 and, for every j ∈ S₀,
  Σ_{k∈S₀∖{j}} |θ*_k| |ρ|^{|j−k|} ≤ ½ |θ*_j| (1 − ρ²)/(1 + ρ²);
- **(AR-g) generic position:** inf_{n≥n₀} dist(ϑ_n, B) > 0, with B as in (BLK-g). For AR, B is a countable union of
  hyperplanes, so it is null and nowhere dense ([VIS] (VIS-c), (VIS-d)(ii)).

**Then the conclusion of Theorem 6 holds.** Under the joint law of design and noise, there are data events 𝒢_n with
P(𝒢_n) → 1 on which **every** admissible run that produces output reports Ŝ = S₀, whatever its seed and the outcome of
its internal calibration. In particular, P(output and Ŝ ≠ S₀) → 0. If moreover the delivery conventions (S4) hold,
then P(the run produces output) = 1 for every admissible n ≥ 3 and P(Ŝ = S₀) → 1, with the same qualifications as
Theorem 6 ([RV] `:696-697`: the integer limits under IDEAL-W⁺, the bounded domain 𝔇, and the time guard).

## 1b. Remarks (outside the corollary; nothing below is claimed)

(o) **Visibility margins** (from the proof; they are Theorem 6's (A3) constants, not part of the conclusion).
a = θ_lo·c under (BLK-1) and (BLK-s); a = c·δ under (BLK-g), where
δ := inf dist(ϑ_n, B). For AR: a = θ_lo(1 − |ρ|)/(1 + |ρ|) under (AR-s); a = ½θ_lo(1 − ρ²)/(1 + ρ²) under (AR-sep);
a = δ(1 − |ρ|)/(1 + |ρ|) under (AR-g).

(i) **Excluded cases.** Coefficient vectors on B. The example is two adjacent AR truths with θ = (1, −2) at ρ = ½: the
first truth has Cov(W_j, Wᵀθ* | W_U) = 0 for U = ∅ and for every U to its left
(`Theory_work/Dept/writing_answers/AR1_VIS_NOTE_2026-11-17.md` on dept/theory; [TB] B8 `:216`). The same cancellation can
occur with two mixed-sign truths in one group.
(ii) **Group sizes.** The group size g is any fixed number. It is not tied to the method's block cap of 16, which
enters Theorem 6 only through |U| ≤ 15.
(iii) **The paper's designs.** (BLK-1) covers the block designs with one truth per block. (AR-sep) covers the study's
AR(0.5) layouts, whose truths are spread apart ([CG] `:146-147`, C-GROW (C5)(c): "The generator's S2 layouts … satisfy
separation for every signal scale c > 0").
(iv) **Constants degrade as |ρ| → 1.** The floor (1 − |ρ|)/(1 + |ρ|) and the margins tend to 0. Track C reports a
slowly growing finite-n leak set at ρ = 0.95 ([TB] B9 `:256-257`). This is evidence, not a claim.

## 2. Assumption classes (D109) and source of each condition

| condition | role in Theorem 6 | class (D109) | supplied by |
|---|---|---|---|
| Gaussian rows, (S1)–(S3), (A2) | (A1), (A2) | as recorded for row 3.1 (no change) | Theorem 6 itself |
| (BLK) group structure, g fixed, λ_min ≥ c | gives (A4), (A5), (A6) | 2b (grouped predictors; the standard block simulation design) | §3, item B (direct computation) |
| (AR) ρ fixed, \|ρ\| < 1 | gives (A4), (A5), (A6) | 2b (ordered predictors: time, position; standard AR(1) simulation design) | §3, item A ([L6] E2) |
| (BLK-1) | gives (A3) | 2b (one signal per correlated group) | §3, B.V1 |
| (BLK-s), (AR-s) | gives (A3) | 2b (aligned effects) | [VIS] (VIS-a), (VIS-e): class 2a |
| (AR-sep) | gives (A3) | 2b (signals spread apart along the order) | [GROW5] (G3b), C-GROW:C5a: class 2a |
| (BLK-g), (AR-g) | gives (A3) | 2b (coefficients off a closed null set, by a fixed distance) | [VIS] (VIS-b), (VIS-c), (VIS-d): class 2a |

Class-1 candidates for the two families (block and AR designs as theorem conditions in a BVS paper) are not yet verified.
They are listed as 2b until verified (PLAN item P5).

## 3. Proof map (assembly; every step is an existing result or an explicit computation)

The proof verifies the hypotheses of the **master** of Theorem 6, `W3-RM2-R:RM2-R-plus@1.0.1` ([RM2R] `:177-182`; the
hypotheses of RM2-R: (T1-R), (FL-R), (V-R), (L-R^b) with 15ϱ + b < ½, and (W-R)). It does not go through the reader
bridges B6.1–B6.5. The reader's (A3)–(A6) are also shown, for readability.

**B (block).** Q₀ := ∪{G : G ∩ S₀ ≠ ∅}, so |Q₀| ≤ g·s₀. Q := Q₀ if p ≥ 2|Q₀| + 32s₀ + 1, and Q := [p] otherwise (then p is
bounded and K = p eventually). Fix b = ¼ and ϱ = 1/120.
- **B.0 Cross-group zero.** If l and k lie in different groups and l, k ∉ U, then Cov(W_l, W_k | W_U) = 0 for every U
  (Σ_{UU}⁻¹ is block-diagonal on the partition) [TB B9 computation].
- **B.V1 (BLK-1) ⇒ (V-R).** By (VIS-0) and B.0, Cov(W_j, Wᵀθ* | W_U) = θ*_j·Var(W_j | W_U) ≥ θ_lo·c.
  (BLK-s) ⇒ (V-R): by B.0 and block independence, Cov(W_j, Wᵀθ* | W_U) = Cov(W_j, Σ_{k∈G∩S₀} θ*_k W_k | W_{U∩G}) with
  G = G(j), a quantity of the single group W_G ~ N(0, Σ_{n,GG}); apply (VIS-a) to Σ_{n,GG} (positive definite, with
  floor ≥ c) and the signs of (BLK-s): margin ≥ θ_lo·c. (BLK-1) is the case |G ∩ S₀| = 1. (BLK-g) ⇒ (V-R) by (VIS-b),
  with c₁₆ ≥ c.
- **B.L (L-R^b), (A4).** ϖ_n = 0 by B.0. H_l := Q ∪ G(l), |H_l| ≤ g(s₀ + 1) ≤ n^ϱ eventually, r_n = 0 by B.0.
  (L-size^b) holds since |Q| is bounded. (L-feas) holds by the choice of Q.
- **B.F (T1-R), (FL-R), (A5).** From λ_min(Σ_n) ≥ c by interlacing; (T1-R) by its sufficient form ([RM] `:129-133`).
- **B.W (W-R), (A6).** N_l := (G(l) ∩ Q) ∖ {l}, so |N_l| ≤ g − 1. Because Σ_{TT} is block-diagonal,
  β̄_{T,l} = β̄_{T∩N_l,l} exactly; hence L_n = 0 and η_n = 0. This is (D-loc^b), and it gives (W-R) by
  `W3-RM2:D-to-W@1.0.3` [TB B10].

**A (AR).** Σ_n is in [L6] E2's class (polynomial covariance decay on a line) for every α > 2:
- unit diagonal, with spectrum in [(1 − |ρ|)/(1 + |ρ|), (1 + |ρ|)/(1 − |ρ|)] ([GROW5] (P1));
- |ρ|^d ≤ K_dec(1 + d)^{−α} with K_dec := sup_{d≥0} |ρ|^d(1 + d)^α < ∞.

Take α = 3. [L6] E2 then verifies (T1-R), (FL-R), (L-size^b), (L-feas), (L-gain-R), (L-loc-R) and (W-R) through (D-loc^b),
for any b ∈ [1/6, ½) (take b = ¼) and ϱ = (½ − b)/30. Leakage and locality are cross-checked by [GROW5] (P4),
0 ≤ Cov(W_l, W_k | W_U) ≤ |ρ|^{|l−k|} for every U (after the sign flip D). E2 assumes PTV(a₀) = (V-R); it is supplied
by (AR-s) via (VIS-e), (AR-sep) via [GROW5] (G3b), and (AR-g) via (VIS-b) with c₁₆ ≥ (1 − |ρ|)/(1 + |ρ|).

**Conclusion.** RM2-R-plus gives [SAND(Q)], [TL(Q)], [NA(Q)], [POST] and [MODE], and hence the common data event and,
under (D) = (S4), delivery: the reader conclusion via B6.6′ (identity).

## 4. Inputs and their registry status (claims.tsv on main a779c1df; verbatim; expansion rule D126)

D126 (manager, 11-17): each input is replaced by its current conditions, statuses are quoted verbatim from main's
registry, and no condition the proofs use is dropped. Inputs whose status carries no "conditional on" have nothing to
expand.

| input | used for | status (verbatim, claims.tsv) |
|---|---|---|
| `W3-RM2-R:RM2-R-plus@1.0.1` | master of Theorem 6 | "PROVED-CHECKED; council R3, MANIFEST 5d6d3c905e7dbfe5b637150bbd4cb3fb099596b46f72ddd62357d843056e649f (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS" |
| `W3-RM2-R:RM0-plus@1.0.1` | core (b⁺), (c⁺) | "PROVED-CHECKED; council R3, MANIFEST 5d6d3c905e7dbfe5b637150bbd4cb3fb099596b46f72ddd62357d843056e649f (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS" |
| `W3-RM2-R:DLV-0@1.0.1` | delivery under (S4) | "PROVED-CHECKED; council R3, MANIFEST 5d6d3c905e7dbfe5b637150bbd4cb3fb099596b46f72ddd62357d843056e649f (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS" |
| `W3-AUDIT-V:VIS@1.0.0` | (V-R) for (BLK-s), (BLK-g), (AR-s), (AR-g); (VIS-0) for (BLK-1) | "PROVED-CHECKED; council R4, MANIFEST a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248, sol=9.5 PASS, opus=9.5 PASS" |
| `C-GROW:C5a@1.0.0` ([GROW5] (P1)–(P4), (G3b)) | AR spectrum; (V-R) for (AR-sep); leakage cross-check | "PROVED-CHECKED" |
| `W3-RM2:D-to-W@1.0.3` | (D-loc^b) ⇒ (W-R), block side | "PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda)" |
| `W3-RM2:POST-R@1.0.3` | (T1-R) ⇒ [POST] | "PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda)" |
| ↳ expansion: `W2-APP:POST@1.0.7` | condition of POST-R and of Ex-PolyR | "PROVED-CHECKED" |
| `W3-RM2:Ex-PolyR@1.0.3` ([L6] E2) | AR: (T1-R), (FL-R), (L-R^b), (W-R) | "PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on W2-APP:POST, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; input versions W2-APP:POST@1.0.1, W2-LOC2:Lemma-BC@1.0.0, W2-LOC2:Lemma-IR@1.0.0" |
| ↳ expansion: `W2-LOC2:Lemma-BC@1.0.0` | condition of Ex-PolyR | "PROVED (by this seat, unchecked)" |
| ↳ expansion: `W2-LOC2:Lemma-IR@1.0.0` | condition of Ex-PolyR | "PROVED (by this seat, unchecked)" |

**Consequence.** The block half rests only on PROVED-CHECKED inputs (the POST-R condition expands to a PROVED-CHECKED
input). The AR half rests on Ex-PolyR, BC and IR as quoted. **DP1 (HQ, 11-17):** HQ prefers an unconditional AR half.
An independent Opus seat is checking E2 (with BC and IR as far as FAMC consumes them), and its report goes to
`reviews/E2_check_opus_R1.md`. The result decides between an unconditional AR half, the block-only fallback (AR as track-C
evidence), and, only if the check cannot finish within the kill budget, "AR conditional on E2". No RM2 file is edited.

## 5. Not claimed

- Anything for coefficient vectors on B, or approaching it (dist(ϑ_n, B) → 0).
- Groups whose size grows with n; correlation tending to ±1; AR(q) or other Toeplitz designs. These are outside this
  ticket; the second is covered for |Q| polynomial only through E2's class, which is not stated here.
- Theorems 5 and 10 on these families: their (A5) no-leakage condition fails for AR and for block designs with a truth
  that has correlated block-mates ([TB] B11). Only Theorem 6's conclusion is claimed. Its uses in Theorems 5 and 10 are
  unchanged.
- Finite-n statements, and any change to the method.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1.0 | all | NEW-CLAIM (corollary; additive) | W3-FAMC | owner GO via HQ, 11-17 (brief) | — (draft for HQ; no review yet) |
| v1.1 | §1R added; remarks → §1b; pointers; §4 full statuses + D126 expansion | EQUAL (no clause of §1 changed) | manager pre-review items; HQ DP2 (keep every fixed ρ) | manager 11-17 | citecheck |
