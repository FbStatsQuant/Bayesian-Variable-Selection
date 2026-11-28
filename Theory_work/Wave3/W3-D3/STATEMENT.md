# W3-D3 — STATEMENT v1.4 (2026-11-17; lead: Claude Opus 5.5, high; track D ticket #3, sub-Gaussian rows for Theorem 2)

Ticket W3-D3: Theorem 2 (claims card row 1.2, posterior concentration on a random design) with Gaussian rows replaced by
rows that are sub-Gaussian along sparse directions, as a **coexisting** claim. The proof reuses W3-DIST's
population-to-sample bridge (owner condition D105/D112). Source: W3-AUDIT `TRACK_D.md` §2 candidate #3 (branch
theory/W3-AUDIT). Tier B (no new key lemma). Delta statement (RIDER_RULES §1) over the recorded reader Theorem 2
([RV] row thm2) and its master [W3P] Theorem 1 item 6. This file **asserts no proof status**: proofs in `lemmas/`,
statuses in the checkpoints. Asymptotic (n → ∞) unless marked *deterministic*. No method change.
v1.4 = v1.3 with H5 card 17 (class-1 anchor Narisetty–He only; §5, outside the claim spans). v1.3 = v1.2 with the council R1 dispositions (`reviews/R1_disposition.md`). v1.2 = v1.1 with the line-check amendments [K1-1]…[K1-12] (`reviews/K1_linecheck_opus.md`;
`reviews/K1_disposition.md`). v1.1 = v1.0 with the statement-lock amendments [L1-1]…[L1-6] (`reviews/L1_statement_lock_sol.md`, LOCK-WITH-AMENDMENTS;
`reviews/L1_disposition.md`) and the HQ anchoring wording with the lead's queued edits Q1, Q2
(`reviews/PENDING_LEAD_EDITS.md`).

**Aliases.** [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`; [DIST] = `Theory_work/Wave3/W3-DIST/STATEMENT.md`;
[EB] = `Theory_work/Wave3/W3-DIST/work/E_bridges/`; [RV] = `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`;
[NOT] = `Theory_work/Wave3/W3-READER/NOTATION.md`; [R1] = `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md`;
[POST] = `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`. All on main 029bb748 (unchanged at 968f19d1).

**Symbols [L1-1].** L is the sub-Gaussian constant of (A4) (the symbol of the reader version of Theorem 9, [RV] `:1097-1099`);
K_cap := min(p_ret, ⌊n/2⌋) is the cap on the model size of the method. (In the quoted files [EB]`B1.md`, `B2core.md` the
sub-Gaussian constant is called K; in [W3P] the cap is called K.)

## 0. Setting (delta over [NOT] §1 and [RV] `:28-29`)

* **Data and model.** As [NOT] §1 `:11-19` and [RV] (S1), (S2) `:28-29`: y^r = α*1_n + X^rβ* + ε, ε ~ N_n(0, σ*²I_n)
  independent of X^r, σ*² > 0 fixed; α*, β* deterministic; 2 ≤ p ≤ n^A with A ≥ 1 fixed, where **p is the number of
  predictor columns of X^r** (before the method removes constant columns; [NOT] writes p for the retained number, here
  p_ret ≤ p). Columns keep their original labels: S₀ := supp β* ⊆ [p], s₀ := |S₀|.
* **Random design (the only change).** The rows of X^r are i.i.d. copies of a random vector x ∈ ℝ^p with mean m_n and
  covariance matrix Σ_n, where Σ_n is a correlation matrix (every predictor has variance 1), as in the recorded reader
  Theorem 2. No other condition on the law of x than (A3), (A4) below. ([NOT] `:22-25` take the rows Gaussian; that is the
  case L = 1 of (A4).)
* **Posterior and outputs.** π(· | X^r, y^r) is the method's posterior over models, computed on the p_ret non-constant
  columns as in [W3P] §0 `:16-29` (model space Ω = {S ⊆ retained columns : |S| ≤ K_cap}). δ_n := 1 − π(S₀ | X^r, y^r);
  PIP_j := π(j ∈ S); HPM := a measurable selection of argmax π (any tie rule); MPM := {j : PIP_j > ½} ([W3P] `:31-34`).
  *Conventions off the event where no column is removed (these do not describe the code, which may reject such input)
  [L1-3]:* π(S₀) := 0 if S₀ ∉ Ω (a true column removed, or s₀ > K_cap); PIP_j := 0 for a removed column j; if p_ret = 0,
  π := point mass at ∅ and HPM = MPM := ∅. (The response is non-constant with probability one under (S1).)
  r_n := √(log n/n).

## 1. Theorem 2SG — posterior concentration on a random sub-Gaussian design

Registry id `W3-D3:Thm2SG`.

Let the rows of X^r be i.i.d. copies of a random vector x ∈ ℝ^p with mean m_n and covariance matrix Σ_n, Σ_n a
correlation matrix, and assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity and fixed signals.** s₀ ≥ 1 is fixed and b_lo ≤ |β*_j| ≤ b_hi for j ∈ S₀, with fixed
  0 < b_lo ≤ b_hi < ∞.
- **(A3) Population sparse eigenvalue floor.** λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ 5(A + 1)(s₀ + 1) log n, for a
  fixed φ ∈ (0, 1] (for instance, λ_min(Σ_n) ≥ φ²).
- **(A4) Sub-Gaussian predictors on sparse directions.** For a fixed L > 0, every u ∈ ℝ^p with at most
  5(A + 1)(s₀ + 1) log n nonzero entries and every λ ∈ ℝ:
  E exp(λ·uᵀ(x − m_n)) ≤ exp(L²λ²·uᵀΣ_nu/2).

Then, under the joint law of design and noise,
  1 − π(S₀ | y) = O_P(√(log n/n)),   P(HPM = MPM = S₀) → 1,   max_j |PIP_j − 1{j ∈ S₀}| = O_P(√(log n/n)).

## 2. Lemma B3w — bridge events for [W3P] Theorem 1 item 6 under (A1)–(A4)

Registry id `W3-D3:B3w`.

Assume (A1)–(A4) of §1 and put W̄_n := 5(A + 1)(s₀ + 1) log n, q_n := ⌊W̄_n⌋, j₀ := ⌈(2A + 1)s₀⌉ + 1, m♯_n as in
[W3P] `:36-37` (computed with p_ret and s₀), and, for the unit-noise model of [EB]`B0.md` (coefficients β̃* := β*/σ*,
standardised coefficients θ̃* := D_xβ̃*),
  M_E := 2s₀²b_hi²/σ*²,  φ₀² := φ²/4,  g₀ := φ²/8,  M_n := b_lo²nφ²/(8σ*² log n).
Let 𝓔₁ be the event of [EB]`B1.md` and 𝓔₂(q_n) the event of [EB]`B2core.md` at q = q_n, both events of the raw design,
and 𝒜_n := 𝓔₁ ∩ 𝓔₂(q_n). There is n₁ = n₁(s₀, A, L) ≥ max(3, 2s₀) such that for every n ≥ n₁:
(a) on 𝒜_n: no column of X^r is constant in the sample (p_ret = p), |supp θ̃*| = s₀ ≤ K_cap, and
    (ii) (E; M_E): ‖Xθ̃*‖² ≤ nM_E; (iii) (F_λ; φ₀) of [W3P] `:68-70`; (iv) (F_w; g₀) of [W3P] `:71-73`;
    (v) θ̃*²_min nφ₀²/log n ≥ M_n, and M_n → ∞;
(b) P(𝒜_nᶜ) ≤ 4p·e^{−c₁n/L⁴} + e^{−c₂n/L⁴} → 0, with c₁ = 1/576, c₂ = 10⁻⁵;
(c) [L1-2] **interface.** Let (X°, θ°) be the *completed pair*: (X°, θ°) := (X, θ̃*) on {p_ret = p}, and, outside it, a fixed
    deterministic centred standardised n × p matrix with a fixed truth θ⁰ with supp θ⁰ = S₀ [K1-1]. Then supp θ° = S₀ on every
    outcome, and (X°, θ°) is a Borel function of the raw design, hence independent of ε. Let 𝒜′_n be the set of outcomes on
    which (X°, θ°) satisfies ‖X°θ°‖² ≤ nM_E, (F_λ; φ₀), (F_w; g₀) (with m♯_n computed from (n, p, s₀)) and
    θ°²_min nφ₀²/log n ≥ M_n. Then 𝒜′_n is (X°, θ°)-measurable and 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p}. Moreover (with (b):
    P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) the hypotheses of [W3P] Theorem 1 item 6 hold for (X°, θ°, ε/σ*) in regime R1 with the events
    𝒜′_n, the common constants (M_E, φ₀, g₀) and the common envelope M_n [K1-3]. (For n < n₁ put 𝒜′_n := ∅; item 6
    needs only P(𝒜′_n) → 1 [R1-opus-E5].)

## 3. Proposition ExSG — families satisfying (A4)

Registry id `W3-D3:ExSG`. Let x = m + Bξ with m ∈ ℝ^p, B a p × d matrix with BBᵀ = Σ a correlation matrix, and ξ ∈ ℝ^d
with independent coordinates, E ξ_k = 0 and Var ξ_k = 1.
(a) If E exp(λξ_k) ≤ exp(L²λ²/2) for every k and every λ ∈ ℝ, then x has mean m and covariance Σ, and
    E exp(λuᵀ(x − m)) ≤ exp(L²λ²uᵀΣu/2) for **every** u ∈ ℝ^p and λ ∈ ℝ. In particular (A4) holds with this L.
(b) The scalar hypothesis of (a) holds with L = 1 when ξ_k is standard Gaussian, Rademacher (±1 with probability ½) or
    uniform on [−√3, √3]; and it holds with L = K whenever every ξ_k takes its values in an interval of length 2K, with
    the same K > 0 for all k [R1-opus-E4].

## 4. Remarks (not part of the registered spans)

(a) *Gaussian rows.* Rows N_p(m_n, Σ_n) satisfy (A4) with L = 1 (Proposition ExSG with B = Σ_n^{1/2} and Gaussian ξ). So
every design covered by the recorded Theorem 2 ([RV] `:263-270`) is covered by Theorem 2SG. Non-Gaussian examples that
satisfy (A3) as well: Σ_n = I with independent Rademacher or uniform coordinates (φ = 1, L = 1). Row 1.2, its master
(`W2-APP:POST`) and their consumers are not changed: Theorem 2SG coexists with them (§7).
(b) *What (A4) asks.* Sub-Gaussianity of each sparse linear combination of the centred predictors at the scale of its
own standard deviation, with one constant L; only combinations of at most 5(A + 1)(s₀ + 1) log n predictors are
constrained, the same sets as in (A3). It fails for a binary predictor with P(x_j = 1) → 0, and along a sparse direction
of bounded predictors whose difference is a rare jump (§5, example from the statement lock).
(c) *Where (A4) is used.* Only to make the sample standard deviations and the sample Gram matrices of small sets of
standardised predictors track their population values (Lemma B3w); the fixed-design posterior theorem ([W3P] Theorem 1)
and the transfer to the joint law of design and noise (its item 6) are unchanged and use the Gaussian noise of (S1).
(d) *Constants.* L ≥ 1 automatically ([EB]`B1.md` (a), with L > 0). The floor φ² enters the sample floors as φ²/4 and φ²/8;
the constants are proof artefacts.
(e) *Unit variances [L1-4].* The correlation-matrix assumption is the recorded one and is used as stated. Read as a
normalisation of a design with arbitrary positive variances, it replaces β* by D_σβ* (D_σ = diag(sd(x_j))): the bounds of
(A2) then apply to |sd(x_j)β*_j|, not to the raw slopes. No other generalisation is claimed.
(f) *Measurability of 𝒜_n [K1-11].* 𝒜_n itself need not be (X, θ̃*)-measurable (𝓔₁ involves the sample scales of null
columns, which standardisation discards); it is used only for its probability, through 𝒜′_n ⊇ 𝒜_n.

## 5. Class of the new hypothesis (owner rule D109; HQ ruling of 2026-11-17: class 1, stated precisely, with a 2b backup; anchor Narisetty–He only, H5 card 17)

(A4) is the only new hypothesis (L the only new constant); (A1)–(A3) are row 1.2's, verbatim (including the parenthetical example of (A3), restored in v1.2 [K1-10]).
**Class 1 (HQ wording, with the lead's precision in brackets [Q1]; the anchor is Narisetty–He only [H5-17]).**
"Sub-Gaussian rows on sparse directions with arbitrary correlation. This contains Narisetty & He's (2014, Lemma 6.1)
isotropic sub-Gaussian rows as the special case Σ = I [for centred rows, with L a fixed multiple of their sub-Gaussian
constant]." Separate factual remark, not an anchor: it also implies Song–Liang's Condition 1 for centred rows
[z = x − m_n, unit marginal variances here — L1-5].
- **Narisetty & He (2014), Lemma 6.1** (Ann. Statist. 42(2) 789–817; cited from arXiv 1405.6545v1, pp. 16–17; journal
  version not checked), verbatim: "Lemma 6.1 (MNEV for sub-Gaussian random matrices). Suppose that the rows of X_{n×p_n}
  are independent isotropic sub-Gaussian random vectors in R^{p_n}. Then there exists a ν > 0 such that, with
  probability greater than 1 − exp(−w′n), inf_{|k|≤m_n(ν)} φ_min(X_k′X_k/n) > 0." Introduced (p. 16): "We now show that this
  requirement is satisfied with high probability if the design matrix consists of independent sub-Gaussian rows."
  Same role as (A4): sub-Gaussian rows ⇒ a floor on the sample Gram matrix of small sets.
- **Song & Liang (2015), Condition 1** (factual comparison, not a class-1 anchor [H5-17]; J. R. Statist. Soc. B 77, p. 953), verbatim: "Condition 1. There are some
  constants M > 0 and δ > 0 such that for any subvector of x, (x_{j1}, …, x_{jr})ᵀ with 1 ≤ j1 < … < jr ≤ P_n, r ≤ r̄_n,
  and |a_i| ≤ δ for i = 1, …, r, we have E exp{(Σ_{i=1}^r a_i x_{ji}/r)²} ≤ exp(M), where the expectation is taken with
  respect to the distribution of the random variables x_{ji}." (Assumed in their Theorem 2, p. 953; verified there for a
  zero-mean Gaussian process with unit variances.) For z = x − m_n, (A4) applied to single coordinates implies Condition 1
  for every r (W3-AUDIT TRACK_B.md lines 184–198 and reviews/AUDITCALC_check_opus.md §4, branch theory/W3-AUDIT; also derived in
  `reviews/L1_statement_lock_sol.md`); the converse fails (bounded coordinates z₁ = R, z₂ = RB with a rare sign flip B:
  Condition 1 holds, (A4) fails along z₁ − z₂ — `reviews/L1_statement_lock_sol.md`; the example also has
  Corr(z₁, z₂) → 1, so it violates (A3) as well [K1-9]).
- **Residual (a report of the lead's search, not a non-existence claim) [L1].** No verified Bayesian variable-selection paper
  found states sub-Gaussian rows with a general correlation matrix; (A4) sits between NH14 (identity covariance) and
  Song–Liang's weaker Condition 1. Not a precedent: Rudelson & Zhou, arXiv 1106.1151v1, Def. 1.5/Thm 1.6 (anisotropic ψ₂
  form; compressed sensing). Checked negative: Yang, Wainwright & Jordan, arXiv 1505.07925v1 (Gaussian random rows only).
- **2b backup [Q2].** "Light-tailed, correlated features are the ordinary situation: Gaussian predictors qualify, and so
  do correlated mixtures x = m + Bξ of independent features each confined to an interval of K standard deviations on
  either side of its mean (for instance Rademacher features, K = 1; uniform features, K = √3)." (Proposition ExSG (a), (b); "qualify" means "satisfy
  (A4)"; Theorem 2SG also needs (A3) [K1-12].) HQ's first
  wording "(any bounded or Gaussian-like predictors qualify)" is not used: it is false for (A4) (remark (b)).

## 6. Inputs (registry id @ version; statuses verbatim from `Theory_work/INFRA/registry/claims.tsv` at main 029bb748; version pins requoted at the recording, task D3)

- `W3-POST:Thm-1@1.0.2` ([W3P] `:61-100`; items 1–3 under item 6) — "PROVED-CHECKED; council C3, MANIFEST
  420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS".
- `W3-DIST:B0@1.0.3`, `W3-DIST:B1@1.0.3`, `W3-DIST:B2core@1.0.3`, `W3-DIST:B2@1.0.3` ([DIST] `:385-408`; proofs
  [EB]`B0.md`, `B1.md`, `B2core.md`, `B2.md`) — each "PROVED-CHECKED; council R2, MANIFEST
  9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r),
  astra=9.3 PASS, opus=9.2 PASS".
- `W3-DIST:B3@1.0.3` ([DIST] `:409-414`; proof [EB]`B3.md`, the template of Lemma B3w) — "PROVED-CHECKED, conditional on
  W3-POST:Thm-1 (for its last sentence); council R2, MANIFEST
  9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r),
  astra=9.3 PASS, opus=9.2 PASS". (Its last sentence, δ_n → 0, is not used; W3-POST:Thm-1 is consumed directly above.)
- `W3-READER:R1@1.0.5` ([R1] B1.2 `:15-17`, B1.3 `:19-31`) — "PROVED-CHECKED; council R3, MANIFEST
  7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS".
- External, standard: Hoeffding's lemma (W. Hoeffding, J. Amer. Statist. Assoc. 58 (1963) 13–30, eq. (4.16)) for ExSG (b).
- Definitions only: [W3P] §0 `:16-39`; [NOT] §1–§2; [RV] (S1), (S2) `:28-29`.

## 7. Dependencies and supersession

| new claim | relation | why (one line) |
|---|---|---|
| W3-D3:B3w | consumes W3-DIST:B0, B1, B2core, B2 (part (a)), W3-READER:R1 (B1.2, B1.3); adapts W3-DIST:B3 | B3's argument on the window of (A3), (A4); set sizes from R1 |
| W3-D3:ExSG | Hoeffding's lemma (part (b)) | product of scalar moment generating functions |
| W3-D3:Thm2SG | consumes W3-D3:B3w, W3-POST:Thm-1 (items 1–3 via item 6), W3-DIST:B0 | B3w (c) gives item 6's events; B0 reduces to unit noise |
| W3-D3:Thm2SG | **coexists** with row 1.2 (`W3-POST:Thm-1` item 6 + `W2-APP:POST`, [RV] row thm2) | its hypotheses contain row 1.2's (L = 1); different bridge; row 1.2 unchanged |

## 8. Tag against the recorded row 1.2 (reader statement [RV] `:263-275`, card `CLAIMS_CARD.md:55`)

**STRONGER** (statement): the conclusions are row 1.2's verbatim; (A1)–(A3) are row 1.2's verbatim; the Gaussian row law
is replaced by (A4) plus "mean m_n, covariance Σ_n a correlation matrix", which every Gaussian row law of row 1.2
satisfies with L = 1, and which admits non-Gaussian laws (remark (a)). Nothing is weaker against the reader statement.
Against row 1.2's **master** (`W2-APP:POST`, LSF, [POST] `:20-25`), which lets the floor on the sets of size ≤ k̄_n vanish
slowly (ψ_n√n/(log n)^{3/2} → ∞) and carries further posterior-summary conclusions (SL1 (a)–(e)), Theorem 2SG keeps the
reader statement's fixed floor φ² and its three conclusions (option o2, a vanishing floor through `W3-DIST:B2`, is OFF by
HQ's decision). Status: every input is PROVED-CHECKED (§6).

## 9. Changelog

| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| 1.0 | all | NEW-CLAIM | first version | ticket (manager GO, 2026-11-17) | `reviews/L1_statement_lock_sol.md` (LOCK-WITH-AMENDMENTS) |
| 1.1 | symbols: L for the sub-Gaussian constant, K_cap for the cap (§0, §1 (A4), §2, §3) | EQUAL | B3w(i) "s₀ ≤ K" was false under the collision [L1-1] | L1-1 | lock amendment (fix specified by the lock reviewer) |
| 1.1 | §2: raw bridge events vs (X°, θ°)-measurable interface events; completed pair; part (c) | **STRONGER on the companion claim B3w** (added conclusion (c), proved in B3w Step 6); EQUAL for Theorem 2SG (the interface its proof uses, made explicit; B3 Step 6 / A-2) [K1-8] | [L1-2] | L1-2 | `reviews/K1_linecheck_opus.md`: tag corrected per K1-8 |
| 1.1 | §0: conventions when columns are removed (π(S₀) := 0, PIP_j := 0, p_ret = 0) | EQUAL (conventions off an event of probability → 0) | [L1-3] | L1-3 | as above |
| 1.1 | §4 (e) unit variances; §5 centring qualifier; §2 heading and provenance moved out of the span | EQUAL (outside spans / editorial) | [L1-4], [L1-5], [L1-6] | L1-4..6 | as above |
| 1.1 | §3 ExSG: B for the mixing matrix; **part (b) bounded features, L = K (Hoeffding)** | **STRONGER** on the companion claim ExSG (an added conclusion; Theorem 2SG unchanged) | support for HQ's 2b sentence [Q2] | HQ ruling via manager | `reviews/K1_linecheck_opus.md`: CONFIRMED (STRONGER on ExSG) [R1-opus-E1] |
| 1.1 | §5 HQ class-1 and 2b wording; NH14 "journal version not checked" | EQUAL (outside spans) | HQ ruling [Q1], [Q2] | HQ ruling | — |
| 1.1 | §2 bookkeeping (n₁ ≥ max(3, 2s₀), 𝓔₂(q_n) for 𝓔₂(w_n), p_ret in m♯_n, θ̃*); §4 (a), (b), (d); §6; §7; §8 [K1-7] | EQUAL (equal events and objects on 𝒜_n / outside spans; consumed scope narrowed to items 1–3) | L1, Q2 | K1-7 | `reviews/K1_linecheck_opus.md` |
| 1.2 | §2 (c): θ⁰ with supp θ⁰ = S₀ (supp θ° = S₀ on every outcome); "and so" replaced by the explicit appeal to (b) and R1; the measurability remark moved to §4 (f) | EQUAL for Theorem 2SG (the v1.1 conclusion with an arbitrary θ⁰ was stated for supp θ°; the proof's intended object is S₀, and the two agree on {p_ret = p}); on the companion claim B3w (c) the completion is specialised (supp θ⁰ = S₀ instead of any support of size s₀): **WEAKER in form, EQUAL in use** (ASSEMBLY needs one completion; the broader v1.1 completion is no longer claimed); 𝒜′_n drops '|supp θ°| = s₀', now automatic [K2-4] | [K1-1], [K1-3], [K1-11] | K1, K2 | `reviews/K2_recheck_opus.md` (tag per K2-4); `reviews/K3_recheck_opus.md`: CONFIRMED |
| 1.2 | §1 (A3): the recorded parenthetical "(for instance, λ_min(Σ_n) ≥ φ²)" restored | EQUAL (an example, not a condition) | [K1-10] | K1 | `reviews/K2_recheck_opus.md`: CONFIRMED |
| 1.2 | §5, §6 (outside spans): off-main paths written as plain text; B3 status quoted in full; Condition-1 example note; "qualify" glossed | EQUAL (outside spans) | [K1-9], [K1-12], citecheck | K1, lead | — |
| 1.3 | §3 ExSG (b): "every ξ_k … with the same K > 0 for all k" | EQUAL (the reading (a) needs; a common constant was implicit) | [R1-opus-E4] | council R1 | diff round R2 |
| 1.3 | §2 (c): "for n < n₁ put 𝒜′_n := ∅" | EQUAL (completes a definition; item 6 needs only P(𝒜′_n) → 1) | [R1-opus-E5] | council R1 | diff round R2 |
| 1.3 | §9 check cell of the ExSG (b) row | EQUAL (bookkeeping) | [R1-opus-E1] | council R1 | — |
| 1.4 | §5 class-1 wording: anchor Narisetty–He only; the Song–Liang implication kept as a separate factual remark (for centred rows); Song–Liang bullet labelled "not a class-1 anchor" | EQUAL (outside the claim spans; no mathematical relation changed) | H5 card 17 (consultant AGREE, binding) | manager | form check F2 |
