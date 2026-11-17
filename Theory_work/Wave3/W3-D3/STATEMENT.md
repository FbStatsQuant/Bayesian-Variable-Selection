# W3-D3 — STATEMENT v1.0 (2026-11-17; lead: Claude Opus 5.5, high; track D ticket #3, sub-Gaussian rows for Theorem 2)

Ticket W3-D3: Theorem 2 (claims card row 1.2, posterior concentration on a random design) with Gaussian rows replaced by
rows that are sub-Gaussian along sparse directions, as a **coexisting** claim. The proof reuses W3-DIST's
population-to-sample bridge (owner condition D105/D112). Source: W3-AUDIT `TRACK_D.md` §2 candidate #3 (branch
theory/W3-AUDIT). Tier B (no new key lemma). Delta statement (RIDER_RULES §1) over the recorded reader Theorem 2
([RV] row thm2) and its master [W3P] Theorem 1 item 6. This file **asserts no proof status**: proofs in `lemmas/`,
statuses in the checkpoints. Asymptotic (n → ∞) unless marked *deterministic*. No method change.

**Aliases.** [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`; [DIST] = `Theory_work/Wave3/W3-DIST/STATEMENT.md`;
[EB] = `Theory_work/Wave3/W3-DIST/work/E_bridges/`; [RV] = `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`;
[NOT] = `Theory_work/Wave3/W3-READER/NOTATION.md`; [R1] = `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md`;
[POST] = `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`. All on main 029bb748 (unchanged at 968f19d1).

## 0. Setting (delta over [NOT] §1 and [RV] `:28-29`)

* **Data and model.** As [NOT] §1 `:11-19` and [RV] (S1), (S2) `:28-29`: y^r = α*1_n + X^rβ* + ε, ε ~ N_n(0, σ*²I_n)
  independent of X^r, σ*² > 0 fixed; α*, β* deterministic; 2 ≤ p ≤ n^A with A ≥ 1 fixed, where **p is the number of
  predictor columns of X^r** (before the method removes constant columns).
* **Random design (the only change).** The rows of X^r are i.i.d. copies of a random vector x ∈ ℝ^p with mean m_n and
  covariance matrix Σ_n, where Σ_n is a correlation matrix (every predictor has variance 1). No other condition on the
  law of x than (A3), (A4) below. ([NOT] `:22-25` take the rows Gaussian; that is the case K = 1 of (A4).)
* **Posterior and outputs.** π(· | X^r, y^r) is the method's posterior over models, computed on the non-constant columns
  as in [W3P] §0 `:16-29` (model space Ω = {S ⊆ retained columns : |S| ≤ min(p_ret, ⌊n/2⌋)}). S₀ := supp β*, s₀ := |S₀|.
  δ_n := 1 − π(S₀ | X^r, y^r), with π(S₀) := 0 if S₀ ∉ Ω (a true column removed, or s₀ > K); PIP_j := π(j ∈ S) (:= 0 for
  a removed column j); HPM := a measurable selection of argmax π (any tie rule); MPM := {j : PIP_j > ½} ([W3P] `:31-34`).
  r_n := √(log n/n).

## 1. Theorem 2SG — posterior concentration on a random sub-Gaussian design

Registry id `W3-D3:Thm2SG`.

Let the rows of X^r be i.i.d. copies of a random vector x ∈ ℝ^p with mean m_n and covariance matrix Σ_n, Σ_n a
correlation matrix, and assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity and fixed signals.** s₀ ≥ 1 is fixed and b_lo ≤ |β*_j| ≤ b_hi for j ∈ S₀, with fixed
  0 < b_lo ≤ b_hi < ∞.
- **(A3) Population sparse eigenvalue floor.** λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ 5(A + 1)(s₀ + 1) log n, for a
  fixed φ ∈ (0, 1].
- **(A4) Sub-Gaussian predictors on sparse directions.** For a fixed K, every u ∈ ℝ^p with at most
  5(A + 1)(s₀ + 1) log n nonzero entries and every λ ∈ ℝ:
  E exp(λ·uᵀ(x − m_n)) ≤ exp(K²λ²·uᵀΣ_nu/2).

Then, under the joint law of design and noise,
  1 − π(S₀ | y) = O_P(√(log n/n)),   P(HPM = MPM = S₀) → 1,   max_j |PIP_j − 1{j ∈ S₀}| = O_P(√(log n/n)).

## 2. Lemma B3w — the events of [W3P] Theorem 1 item 6 under (A1)–(A4)

Registry id `W3-D3:B3w`. (Copy of `W3-DIST:B3@1.0.1` ([DIST] `:409-414`, proof [EB]`B3.md`) with the window changed
from q_n = min{p, ⌈C_q log n⌉} to w_n below; changed lines marked [R-#] in `lemmas/B3w.md`.)

Assume (A1)–(A4) of §1 and put w_n := min{p, ⌊5(A + 1)(s₀ + 1) log n⌋}, j₀ := ⌈(2A + 1)s₀⌉ + 1, m♯_n as in [W3P] `:36-37`
(computed with p and s₀), and, in the unit-noise model of [EB]`B0.md` (coefficients β*/σ*),
  M_E := 2s₀²b_hi²/σ*²,  φ₀² := φ²/4,  g₀ := φ²/8,  M_n := b_lo²nφ²/(8σ*² log n).
There are 𝓔₁ (event of [EB]`B1.md`) and 𝓔₂(w_n) (event of [EB]`B2core.md` at q = w_n) and n₁ = n₁(s₀, A, K) such that for
every n ≥ n₁, on 𝒜_n := 𝓔₁ ∩ 𝓔₂(w_n): (i) no column of X^r is constant in the sample (p_ret = p), and |supp θ*| = s₀ ≤ K;
(ii) (E; M_E); (iii) (F_λ; φ₀) of [W3P] `:68-70`; (iv) (F_w; g₀) of [W3P] `:71-73`; (v) BM-∞ with the common deterministic
envelope θ*²_min nφ₀²/log n ≥ M_n → ∞; and (vi) P(𝒜_nᶜ) ≤ 4p·e^{−c₁n/K⁴} + e^{−c₂n/K⁴} → 0 (c₁ = 1/576, c₂ = 10⁻⁵).

## 3. Proposition ExSG — a family satisfying (A4)

Registry id `W3-D3:ExSG`. Let x = m + Lξ with m ∈ ℝ^p, L a p × d matrix with LLᵀ = Σ a correlation matrix, and ξ ∈ ℝ^d
with independent coordinates, E ξ_k = 0, Var ξ_k = 1 and E exp(λξ_k) ≤ exp(K²λ²/2) for every k and every λ ∈ ℝ. Then x
has mean m and covariance Σ, and E exp(λuᵀ(x − m)) ≤ exp(K²λ²uᵀΣu/2) for **every** u ∈ ℝ^p and λ ∈ ℝ; so (A4) holds with
this K. In particular K = 1 when every ξ_k is standard Gaussian, Rademacher (±1 with probability ½), or uniform on
[−√3, √3].

## 4. Remarks (not part of the registered spans)

(a) *Gaussian rows.* Rows N_p(m_n, Σ_n) satisfy (A4) with K = 1 (Proposition ExSG with L = Σ_n^{1/2} and Gaussian ξ). So
every design covered by the recorded Theorem 2 ([RV] `:263-270`) is covered by Theorem 2SG. Row 1.2, its master
(`W2-APP:POST`) and their consumers are not changed: Theorem 2SG coexists with them (§7).
(b) *What (A4) asks.* Sub-Gaussianity of each sparse linear combination of the centred predictors at the scale of its
own standard deviation, with one constant K; only combinations of at most 5(A + 1)(s₀ + 1) log n predictors are
constrained, the same sets as in (A3). It fails for a binary predictor with P(x_j = 1) → 0 (for every fixed K).
(c) *Where (A4) is used.* Only to make the sample standard deviations and the sample Gram matrices of small sets of
standardised predictors track their population values (Lemma B3w); the fixed-design posterior theorem ([W3P] Theorem 1)
and the transfer to the joint law of design and noise (its item 6) are unchanged and use the Gaussian noise of (S1).
(d) *Constants.* K ≥ 1 automatically ([EB]`B1.md` (a)). The floor φ² enters the sample floors as φ²/4 and φ²/8; the
constants are proof artefacts.

## 5. Class of the new hypothesis (owner rule D109; stated for HQ's judgement)

(A4) is the only new hypothesis (its constant K is the only new constant); (A1)–(A3) are row 1.2's, verbatim.
**Proposed class 1, between two verified precedents** (same assumption as Theorem 9 (A3), `W3-DIST` reader version,
already classed 1 in `W3-AUDIT/ASSUMPTION_COMPLIANCE.md:31`):
- **Narisetty & He (2014), Lemma 6.1** (Ann. Statist. 42(2) 789–817; arXiv 1405.6545v1, p. 16), quoted verbatim:
  "Lemma 6.1 (MNEV for sub-Gaussian random matrices). Suppose that the rows of X_{n×p_n} are independent isotropic
  sub-Gaussian random vectors in R^{p_n}. Then there exists a ν > 0 such that, with probability greater than
  1 − exp(−w′n), inf_{|k|≤m_n(ν)} φ_min(X_k′X_k/n) > 0." Introduced (p. 16): "We now show that this requirement is
  satisfied with high probability if the design matrix consists of independent sub-Gaussian rows."
  Relation: their rows (independent, isotropic: identity covariance) and ours play the same role (sub-Gaussian rows ⇒ a
  floor on the sample Gram matrix of small sets). Centred isotropic sub-Gaussian rows satisfy (A4) with K a multiple
  of their sub-Gaussian constant; (A4) asks less along sparse directions and allows any correlation matrix Σ_n.
- **Song & Liang (2015), Condition 1** (J. R. Statist. Soc. B 77, p. 953), quoted verbatim: "Condition 1. There are some
  constants M > 0 and δ > 0 such that for any subvector of x, (x_{j1}, …, x_{jr})ᵀ with 1 ≤ j1 < … < jr ≤ P_n, r ≤ r̄_n,
  and |a_i| ≤ δ for i = 1, …, r, we have E exp{(Σ_{i=1}^r a_i x_{ji}/r)²} ≤ exp(M), where the expectation is taken with
  respect to the distribution of the random variables x_{ji}." (Their Theorem 2, p. 953, assumes it; they verify it for
  a zero-mean Gaussian process with unit variances, p. 953.)
  Relation: same family (an exponential-moment bound on averages of a few predictors, under any correlation). (A4)
  implies Condition 1 for standardised predictors, for every r (`W3-AUDIT/TRACK_B.md:184-198`, confirmed in
  `W3-AUDIT/reviews/AUDITCALC_check_opus.md` §4); the converse fails, so (A4) is the stronger of the two.
- **Honest residual.** No verified Bayesian variable-selection paper states sub-Gaussian rows with a *general*
  correlation matrix: NH14 assume identity covariance, and Song–Liang's Condition 1 is weaker. (A4) sits between them.
  (Not a precedent: Rudelson & Zhou, arXiv 1106.1151v1, Def. 1.5/Thm 1.6, give the anisotropic ψ₂ form, but in compressed
  sensing, not Bayesian selection. Checked negative: Yang, Wainwright & Jordan, arXiv 1505.07925v1, random designs Gaussian only.)
  2b support: (A4) holds with K = 1 for Gaussian rows and for the families of Proposition ExSG.

## 6. Inputs (registry id @ version; statuses verbatim from `Theory_work/INFRA/registry/claims.tsv` at main 029bb748)

- `W3-POST:Thm-1@1.0.1` ([W3P] `:61-100`; items 1–4 under item 6) — "PROVED-CHECKED; council C3, MANIFEST
  420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS".
- `W3-DIST:B0@1.0.1`, `W3-DIST:B1@1.0.1`, `W3-DIST:B2core@1.0.1`, `W3-DIST:B2@1.0.1` ([DIST] `:385-408`; proofs
  [EB]`B0.md`, `B1.md`, `B2core.md`, `B2.md`) — each "PROVED-CHECKED; council R2, MANIFEST
  9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r),
  astra=9.3 PASS, opus=9.2 PASS".
- `W3-DIST:B3@1.0.1` ([DIST] `:409-414`; proof [EB]`B3.md`; re-instantiated as Lemma B3w) — "PROVED-CHECKED, conditional on
  W3-POST:Thm-1 (for its last sentence); council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r),
  astra=9.3 PASS, opus=9.2 PASS". (Its last sentence, δ_n → 0, is not used; W3-POST:Thm-1 is consumed directly above.)
- `W3-READER:R1@1.0.2` ([R1] B1.2 `:15-17`, B1.3 `:19-31`) — "PROVED-CHECKED; council R3, MANIFEST
  7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS".
- Definitions only: [W3P] §0 `:16-39`; [NOT] §1–§2; [RV] (S1), (S2) `:28-29`.

## 7. Dependencies and supersession

| new claim | relation | why (one line) |
|---|---|---|
| W3-D3:B3w | consumes W3-DIST:B0, B1, B2core, B2 (part (a)), W3-READER:R1 (B1.2, B1.3) | `B3.md` with the window w_n; set sizes from R1 instead of B2 (d) |
| W3-D3:ExSG | none (self-contained) | product of scalar moment generating functions |
| W3-D3:Thm2SG | consumes W3-D3:B3w, W3-POST:Thm-1 (items 1–4 via item 6), W3-DIST:B0 | B3w gives item 6's events; B0 reduces to unit noise |
| W3-D3:Thm2SG | **coexists** with row 1.2 (`W3-POST:Thm-1` item 6 + `W2-APP:POST`, [RV] row thm2) | its hypotheses contain row 1.2's (K = 1); different bridge; row 1.2 unchanged |

## 8. Tag against the recorded row 1.2 (reader statement [RV] `:263-275`, card `CLAIMS_CARD.md:55`)

**STRONGER** (statement): the conclusions are row 1.2's verbatim; (A1)–(A3) are row 1.2's verbatim; the Gaussian row law
is replaced by (A4) plus "mean m_n, covariance Σ_n a correlation matrix", which every Gaussian row law of row 1.2
satisfies with K = 1 (remark (a)). Nothing is weaker against the reader statement. Against row 1.2's **master**
(`W2-APP:POST`, LSF, [POST] `:20-25`), which lets the floor on the sets of size ≤ k̄_n vanish slowly (ψ_n√n/(log n)^{3/2} → ∞),
Theorem 2SG keeps the reader statement's fixed floor φ² (option o2, a vanishing floor through `W3-DIST:B2`, is OFF by
HQ's decision). Status: every input is PROVED-CHECKED (§6).

## 9. Changelog

| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| 1.0 | all | NEW-CLAIM | first version | ticket (manager GO, 2026-11-17) | statement lock (pending) |
