# W3-D2 — STATEMENT v1.5 (2026-11-17; lead: Claude Opus 5.5, high; track D ticket #2, "check X"; v1.1 = statement-lock amendments [L1-1], [L1-2], locked by `reviews/L1_statement_lock_sol.md` (LOCK-WITH-AMENDMENTS; `reviews/L1_disposition.md`); v1.2 = §7 caveats written out and §0 gloss (EQUAL); v1.3 = K2 wording amendments [K2-F1], [K2-F2], [K2-E6] (EQUAL); v1.4 = council R1 editorial (EQUAL); v1.5 = post-CP3 form fix in §2: α*, β* non-random stated (EQUAL, form only))

Ticket W3-D2: Theorem 2 (claims card row 1.2, posterior concentration on a random Gaussian design) derived from the
omitted-variables master `W3-MISR-R:CorGb-plus@1.0.1`, so that its eigenvalue floor is asked on smaller sets. Source:
W3-AUDIT `TRACK_D.md` §2 candidate #2 (branch theory/W3-AUDIT) and the check X sketch
(`W3-MISR-R/reviews/post_cp3/CHECK_X_sketch.md`, branch of worktree W3-MISR-R; unchecked). Tier B (no new key lemma), NORMAL mode.
This file **asserts no proof status**: proofs in `lemmas/`, statuses in the checkpoints. Asymptotic (n → ∞) unless
marked *deterministic*. No method change.

**Aliases.** [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`; [MISR] = `Theory_work/Wave3/W3-MISR/STATEMENT.md`;
[MISR-R] = `Theory_work/Wave3/W3-MISR-R/STATEMENT.md`; [RV] = `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`;
[R1] = `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md`. All on main 4d65550a.

## 0. Setting and notation (at each n ≥ 3)

* **Data.** Raw design X^r (n × p) and raw response y^r ∈ ℝⁿ. The rows of X^r are i.i.d. N_p(m, Σ) with Σ_jj > 0 for
  every j (so every column is non-constant almost surely and p is the number of retained columns). R := D_Σ^{−1/2} Σ D_Σ^{−1/2},
  D_Σ := diag(Σ), is the correlation matrix of a row.
* **Model.** y^r = α1 + X^rβ + ε with ε ~ N_n(0, σ²I_n) independent of X^r, σ² > 0, and α ∈ ℝ, β ∈ ℝ^p deterministic.
  S₀ := supp β, s₀ := |S₀|.
* **Everything may depend on n:** m, Σ, α, β, σ² and p (no condition beyond (A1)–(A3)).
* **Posterior and outputs.** π(· | X^r, y^r) is the method's posterior over models S ⊆ [p] with |S| ≤ K := min(p, ⌊n/2⌋):
  the exact posterior of the coded prior (X the standardised design, response standardised; coefficients
  N(0, nv(X_SᵀX_S + I)⁻¹) given (S, v), with IG(0.01, 0.01) on the working variance v; capped beta-binomial size prior),
  computed from (X^r, y^r) as defined in [W3P] §0 `:16-29` [L1-1, K2-F1].
  δ_n := 1 − π(S₀ | X^r, y^r) (π(S₀) := 0 if s₀ > K); PIP_j := π(j ∈ S); HPM := a measurable selection of
  argmax π (any tie rule); MPM := {j : PIP_j > ½} ([W3P] `:31-34`). r_n := √(log n/n).

## 1. Theorem 2X — posterior concentration on a random Gaussian design

Registry id `W3-D2:Thm2X`: the reader statement below together with the technical clause (E) [L1-1].

Assume, with constants A ≥ 1, s₀ ∈ ℕ, c > 0, M₀ < ∞ fixed (not depending on n):
- **(A1) Dimension and sparsity.** 2 ≤ p ≤ n^A and s₀ ≥ 1.
- **(A2) Sparse eigenvalue floor on the correlation matrix.** λ_min(R_TT) ≥ c for every T ⊆ [p] with
  1 ≤ |T| ≤ 3(A + 1)(s₀ + 1) log n.
- **(A3) Signal relative to the noise.** βᵀΣβ ≤ M₀σ², and ρ_n := n·min_{j∈S₀} Σ_jjβ_j² / (σ² log n) → ∞.

Then, under the joint law of (X^r, ε):
$$
E\,\delta_n=O(r_n),\qquad P(\mathrm{HPM}\neq S_0)=O(r_n),\qquad P(\mathrm{MPM}\neq S_0)=O(r_n),\qquad
E\max_{j\in[p]}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|=O(r_n).
$$
**(E) Explicit form (technical clause; not part of the reader statement) [L1-1].** There are C (depending only on (s₀, A, M₀, c)) and n* (depending on the sequence) such that for every
n ≥ n*, with k_n := s₀ + max(j₀, m♯_n) (j₀ := ⌈(2A + 1)s₀⌉ + 1; m♯_n of [W3P] `:36-39`) and
b_n := C r_n + (2 + 2k_n)n^{−2} + n^{−1}:
  E δ_n ≤ b_n,  E max_j |PIP_j − 1{j ∈ S₀}| ≤ b_n,  P(HPM ≠ S₀) ≤ 2b_n,  P(MPM ≠ S₀) ≤ 2b_n,
and k_n = O(log n), so b_n = O(r_n).

## 2. Corollary 2X (W3-D2:Cor2X) — the recorded Theorem 2 hypotheses give Theorem 2X

Let the recorded hypotheses of Theorem 2 hold ([RV] `:263-270`, row thm2 at FRZ-B): rows i.i.d. N_p(m_n, Σ_n) with Σ_n a
correlation matrix; (S1) ε ~ N_n(0, σ*²I_n) independent of the design, σ*² > 0 fixed, α*, β* non-random; (S2) 2 ≤ p ≤ n^A, A ≥ 1 fixed;
s₀ ≥ 1 fixed and b_lo ≤ |β_j| ≤ b_hi for j ∈ S₀ with fixed 0 < b_lo ≤ b_hi < ∞; λ_min(Σ_{n,S}) ≥ φ² for every S with
|S| ≤ 5(A + 1)(s₀ + 1) log n, fixed φ ∈ (0, 1]. Then (A1)–(A3) of Theorem 2X hold with c := φ², M₀ := s₀²b_hi²/σ*², and
ρ_n ≥ n b_lo²/(σ*² log n). Hence the four bounds of Theorem 2X's display hold, and with them the three conclusions of the recorded
Theorem 2 ([RV] `:271-275`): δ_n = O_P(r_n), P(HPM = MPM = S₀) → 1, max_j |PIP_j − 1{j ∈ S₀}| = O_P(r_n).
The same holds with the floor asked only on |S| ≤ 3(A + 1)(s₀ + 1) log n.

## 3. Deterministic facts used (inside the proof of Theorem 2X; not separate claims)

For every data set: max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; {HPM ≠ S₀} ⊆ {δ_n ≥ ½}; {MPM ≠ S₀} ⊆ {δ_n ≥ ½}.
(The PIP inequality is [MISR] MIS-R (i) consequence 1, `:118-119`, "for every data set"; the HPM/MPM inclusions are proved
in PROOF P0 [R1-opus-E3].)

## 4. Remarks (not part of the registered spans)

(a) *Relation to Theorem 4.* Theorem 2X is Theorem 4 ([RV] row thm4, `:449-466`) with no omitted predictors, plus the
deterministic PIP/MPM consequences of §3 [R1-opus-E7]: in
(A0) of Theorem 4 take 𝒞 = [p], β^𝒞 = β, σ²_𝒞 = σ², α′ = α. Its floor size 3(A + 1)(s₀ + 1) log n is that of Theorem 4.
(b) *What is not carried over [L1-2].* The master of the recorded Theorem 2 (`W2-APP:POST`, LSF,
`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:20-25`) keeps a fixed positive floor on sets of size ≤ min(p, s₀ + j₀) (LSF (i)),
but lets the floor ψ_n on the larger range |S| ≤ k̄_n vanish, provided ψ_n√n/(log n)^{3/2} → ∞ (LSF (ii)). Theorem 2X
instead needs a fixed positive floor on its whole range |T| ≤ k_n (imposed through the convenient upper bound
3(A + 1)(s₀ + 1) log n). Neither master dominates the other on the floor hypotheses alone.
(c) *Floor size.* The proof uses the floor only on sets of size ≤ k_n; 3(A + 1)(s₀ + 1) log n is a convenient upper
bound ([R1] B4.1), with room (numerics N1 (i): k_n is at most 0.40 of it on the grid). Constants are proof artefacts.

## 5. Inputs (registry id @ version, ACTIVE on main 4d65550a; statuses verbatim; the four that changed since are requoted at the recording, task D2; caveat (a) follows them)

- `W3-MISR-R:CorGb-plus@1.0.3` ([MISR-R] `:94-108`) — "PROVED-CHECKED, conditional on W2-APP:POST,
  C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS".
- `W3-READER:R1@1.0.4` ([R1] `:43-46`, B4.1; uses B1.3 `:19-31`) — "PROVED-CHECKED; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS".
- Definitions only: [W3P] §0 `:16-39` (target, outputs, m♯_n); [MISR-R] §2 `:48-70` ((N), (OV), N_k(m, 0) := δ_m at `:31`).
- Rows named in CorGb-plus's former condition list (for the recorder; statuses on main at the recording; its status above is the HQ 11-23 refresh): `W3-POST2:C@1.0.7` "PROVED-CHECKED, conditional on
  W2-APP:POST"; `W3-POST:Prop-LB@1.0.1` "PROVED-CHECKED; council C3, MANIFEST 420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS".

## 6. Dependencies and supersession

| new claim | relation | why (one line) |
|---|---|---|
| W3-D2:Thm2X | consumes W3-MISR-R:CorGb-plus, W3-READER:R1 (B4.1) | Theorem 2X's setting is CorGb-plus's with no omitted columns; (A2) covers |T| ≤ k_n by B4.1 |
| W3-D2:Cor2X | implies the reader statement of row 1.2 (Theorem 2, [RV] `:263-275`) | recorded hypotheses ⇒ (A1)–(A3); expectation bounds ⇒ the O_P and w.p. → 1 conclusions (Markov) |
| W3-D2:Cor2X | coexists with W3-POST:Thm-1 item 6 + W2-APP:POST (row 1.2's masters) | different masters; the old one keeps the vanishing-floor remark and its clean status |

## 7. Tag against the recorded row 1.2 (reader statement [RV] `:263-275`, card `CLAIMS_CARD.md:55`)

**STRONGER** (statement, against the constant-floor reader statement [RV] `:263-275`): every hypothesis is implied by the
recorded one (Corollary 2X); the floor is asked on sets of size 3(A + 1)(s₀ + 1) log n instead of 5(A + 1)(s₀ + 1) log n;
Σ is not normalised (the floor and the signal are stated on the correlation scale; a cosmetic gain, since the recorded
model takes Σ_n a correlation matrix without loss of generality, `NOTATION.md:21-23`) [R1-opus-E2]; the fixed absolute signal bounds b_lo ≤ |β_j| ≤ b_hi and the fixed σ*² are replaced by
the relative conditions (A3) (energy and beta-min measured against σ², which may vary with n) [L1-2]; and the conclusions
are in expectation (rate for E δ_n, the PIP error and the HPM/MPM error probabilities) instead of O_P / w.p. → 1.
Two things are not stronger and must travel with the tag [L1-2, CP1]:
- **Caveat (a) — status.** Theorem 2X and Corollary 2X rest on `W3-MISR-R:CorGb-plus@1.0.3`, whose status is conditional
  on W2-APP:POST, C-MIS:GDb and C-MIS:Prop-P (§5; @1.0.1 listed W3-POST2:C, :E, :A1, :A0 and, through W3-POST2:C, the
  then-unchecked `W3-POST:Prop-LB`). Row 1.2 as recorded is "clean"; the new form is not.
- **Caveat (b) — floor on the large sets [K2-F2].** Against the old **master** (W2-APP:POST with LSF), which allows the
  floor on the sets of size ≤ k̄_n to vanish slowly, Theorem 2X needs a fixed floor on all its sets. Its master CorGb-plus
  (fixed floor on |T| ≤ k_n) and the old master are incomparable on the floor hypotheses (remark (b)); Theorem 2X's own
  (A2) is stronger than LSF on the floor (k̄_n ≤ 3(A + 1)(s₀ + 1) log n for every n ≥ 3, compared on R = Σ_n; proof in PROOF P5) [K3-E1, R1-opus-E1]. The gain "smaller sets" is
  measured against the reader statement's 5(A + 1)(s₀ + 1) log n. STRONGER holds against the constant-floor reader
  statement only.

## 8. Changelog

| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| 1.0 | all | NEW-CLAIM | first version | ticket | `reviews/L1_statement_lock_sol.md` (LOCK-WITH-AMENDMENTS) |
| 1.1 | §0 posterior line; §1 title, clause (E) moved out of the reader statement; §2 "bounds" | EQUAL | presentation [L1-1] | L1-1 | lock amendments (lead applies; the lock reviewer specified the fix) |
| 1.1 | §4 remark (b), §7 tag wording | EQUAL | faithfulness of the comparison with the old master [L1-2] | L1-2 | as above |
| 1.2 | §7 caveats (a), (b) written out (outside the registered spans) | EQUAL | manager's CP1 answer | CP1 | none needed (EQUAL, outside spans) |
| 1.2 | §0 posterior line: coefficient prior written as coded (ridge form, not "g-prior"); citation on one line | EQUAL | wording of the verbal gloss; the definition is the [W3P] pointer | lead (citecheck) | `reviews/K2_recheck_opus.md` (K1 read v1.1) [K2-E6] |
| 1.3 | §0 gloss (working variance v, standardised X); §7 caveat (b) subject corrected | EQUAL | wording [K2-F1], [K2-F2] (outside the claim spans) | K2 | `reviews/K3_recheck_opus.md` [K3-E3] |
| 1.4 | §3 attribution sentence (inside the §3 span; content unchanged); §4(a), §7 wording; pointer to PROOF P5 | EQUAL | council R1 editorial [R1-opus-E1, E2, E3, E7] | `reviews/R1_council_opus.md` | diff round D1 |
| 1.5 | §2 (Cor2X span): "α*, β* non-random" stated in the quoted recorded hypotheses | EQUAL (form only) | HQ API audit auditD2 s1-5, s2-4 (MINOR): the corollary used it as a reading of the recorded model (PROOF P3) | `Theory_work/Wave3/API_AUDIT/auditD2_results/` (main) | `reviews/F1_formcheck_opus.md` |
