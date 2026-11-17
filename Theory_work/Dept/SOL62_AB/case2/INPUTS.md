# Case 2 — INPUTS (excerpts, byte-for-byte from git; nothing added inside the markers)

| path | commit | lines | chars | sha256[:12] of excerpt |
|---|---|---|---|---|
| `Theory_work/Wave3/W3-D2/STATEMENT.md` | `934a2b43` | whole | 10331 | cc970d0deeef |
| `Theory_work/Wave3/W3-D2/PROOF.md` | `934a2b43` | whole | 6652 | 2f44f199dd59 |
| `Theory_work/Wave3/W3-D2/TARGET.md` | `934a2b43` | whole | 2734 | 75be493d2979 |
| `Theory_work/Wave3/W3-D2/numerics/N1_floor_and_e2e.py` | `934a2b43` | whole | 6387 | b051fee4c2de |
| `Theory_work/Wave3/W3-D2/numerics/N1_out.txt` | `934a2b43` | whole | 2450 | f449dd2dabc7 |
| `Theory_work/Wave3/W3-MISR-R/STATEMENT.md` | `a14ce83b` | 88-108 | 1824 | 2cc37d1e0a13 |
| `Theory_work/Wave3/W3-POST/STATEMENT.md` | `e2680987` | 16-40 | 2247 | be6e613f13b7 |

Built by `build_inputs.py`; the text between the markers below is the excerpt.

<<<FILE Theory_work/Wave3/W3-D2/STATEMENT.md @934a2b43 (whole file) >>>
# W3-D2 — STATEMENT v1.3 (2026-11-17; lead: Claude Opus 5.5, high; track D ticket #2, "check X"; v1.1 = statement-lock amendments [L1-1], [L1-2], locked by `reviews/L1_statement_lock_sol.md` (LOCK-WITH-AMENDMENTS; `reviews/L1_disposition.md`); v1.2 = §7 caveats written out and §0 gloss (EQUAL); v1.3 = K2 wording amendments [K2-F1], [K2-F2], [K2-E6] (EQUAL))

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
correlation matrix; (S1) ε ~ N_n(0, σ*²I_n) independent of the design, σ*² > 0 fixed; (S2) 2 ≤ p ≤ n^A, A ≥ 1 fixed;
s₀ ≥ 1 fixed and b_lo ≤ |β_j| ≤ b_hi for j ∈ S₀ with fixed 0 < b_lo ≤ b_hi < ∞; λ_min(Σ_{n,S}) ≥ φ² for every S with
|S| ≤ 5(A + 1)(s₀ + 1) log n, fixed φ ∈ (0, 1]. Then (A1)–(A3) of Theorem 2X hold with c := φ², M₀ := s₀²b_hi²/σ*², and
ρ_n ≥ n b_lo²/(σ*² log n). Hence the four bounds of Theorem 2X's display hold, and with them the three conclusions of the recorded
Theorem 2 ([RV] `:271-275`): δ_n = O_P(r_n), P(HPM = MPM = S₀) → 1, max_j |PIP_j − 1{j ∈ S₀}| = O_P(r_n).
The same holds with the floor asked only on |S| ≤ 3(A + 1)(s₀ + 1) log n.

## 3. Deterministic facts used (inside the proof of Theorem 2X; not separate claims)

For every data set: max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; {HPM ≠ S₀} ⊆ {δ_n ≥ ½}; {MPM ≠ S₀} ⊆ {δ_n ≥ ½}.
(As [MISR] MIS-R (i) consequence 1, `:118-119`, "for every data set".)

## 4. Remarks (not part of the registered spans)

(a) *Relation to Theorem 4.* Theorem 2X is Theorem 4 ([RV] row thm4, `:449-466`) with no omitted predictors: in
(A0) of Theorem 4 take 𝒞 = [p], β^𝒞 = β, σ²_𝒞 = σ², α′ = α. Its floor size 3(A + 1)(s₀ + 1) log n is that of Theorem 4.
(b) *What is not carried over [L1-2].* The master of the recorded Theorem 2 (`W2-APP:POST`, LSF,
`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:20-25`) keeps a fixed positive floor on sets of size ≤ min(p, s₀ + j₀) (LSF (i)),
but lets the floor ψ_n on the larger range |S| ≤ k̄_n vanish, provided ψ_n√n/(log n)^{3/2} → ∞ (LSF (ii)). Theorem 2X
instead needs a fixed positive floor on its whole range |T| ≤ k_n (imposed through the convenient upper bound
3(A + 1)(s₀ + 1) log n). Neither master dominates the other on the floor hypotheses alone.
(c) *Floor size.* The proof uses the floor only on sets of size ≤ k_n; 3(A + 1)(s₀ + 1) log n is a convenient upper
bound ([R1] B4.1), with room (numerics N1 (i): k_n is at most 0.40 of it on the grid). Constants are proof artefacts.

## 5. Inputs (registry id @ version, ACTIVE on main 4d65550a; statuses verbatim)

- `W3-MISR-R:CorGb-plus@1.0.1` ([MISR-R] `:94-108`) — "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E,
  W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS".
- `W3-READER:R1@1.0.2` ([R1] `:43-46`, B4.1; uses B1.3 `:19-31`) — "PROVED-CHECKED; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS".
- Definitions only: [W3P] §0 `:16-39` (target, outputs, m♯_n); [MISR-R] §2 `:48-70` ((N), (OV), N_k(m, 0) := δ_m at `:31`).
- Conditions carried from CorGb-plus (for the recorder; statuses on main): `W3-POST2:C@1.0.6` "PROVED-CHECKED, conditional on
  W3-POST:Prop-LB, W2-APP:POST"; `W3-POST:Prop-LB@1.0.0` "PROVED (by this seat, unchecked)".

## 6. Dependencies and supersession

| new claim | relation | why (one line) |
|---|---|---|
| W3-D2:Thm2X | consumes W3-MISR-R:CorGb-plus, W3-READER:R1 (B4.1) | Theorem 2X's setting is CorGb-plus's with no omitted columns; (A2) covers |T| ≤ k_n by B4.1 |
| W3-D2:Cor2X | implies the reader statement of row 1.2 (Theorem 2, [RV] `:263-275`) | recorded hypotheses ⇒ (A1)–(A3); expectation bounds ⇒ the O_P and w.p. → 1 conclusions (Markov) |
| W3-D2:Cor2X | coexists with W3-POST:Thm-1 item 6 + W2-APP:POST (row 1.2's masters) | different masters; the old one keeps the vanishing-floor remark and its clean status |

## 7. Tag against the recorded row 1.2 (reader statement [RV] `:263-275`, card `CLAIMS_CARD.md:55`)

**STRONGER** (statement, against the constant-floor reader statement [RV] `:263-275`): every hypothesis is implied by the
recorded one (Corollary 2X); the floor is asked on sets of size 3(A + 1)(s₀ + 1) log n instead of 5(A + 1)(s₀ + 1) log n;
Σ need not be a correlation matrix; the fixed absolute signal bounds b_lo ≤ |β_j| ≤ b_hi and the fixed σ*² are replaced by
the relative conditions (A3) (energy and beta-min measured against σ², which may vary with n) [L1-2]; and the conclusions
are in expectation (rate for E δ_n, the PIP error and the HPM/MPM error probabilities) instead of O_P / w.p. → 1.
Two things are not stronger and must travel with the tag [L1-2, CP1]:
- **Caveat (a) — status.** Theorem 2X and Corollary 2X rest on `W3-MISR-R:CorGb-plus@1.0.1`, whose status is conditional
  on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb and C-MIS:Prop-P; through W3-POST2:C this includes
  `W3-POST:Prop-LB`, which is "PROVED (by this seat, unchecked)" (§5). Row 1.2 as recorded is "clean"; the new form is not.
- **Caveat (b) — floor on the large sets [K2-F2].** Against the old **master** (W2-APP:POST with LSF), which allows the
  floor on the sets of size ≤ k̄_n to vanish slowly, Theorem 2X needs a fixed floor on all its sets. Its master CorGb-plus
  (fixed floor on |T| ≤ k_n) and the old master are incomparable on the floor hypotheses (remark (b)); Theorem 2X's own
  (A2) is stronger than LSF on the floor (k̄_n ≤ 3(A + 1)(s₀ + 1) log n for every n ≥ 3, compared on R = Σ_n) [K3-E1]. The gain "smaller sets" is
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
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-D2/PROOF.md @934a2b43 (whole file) >>>
# W3-D2 — PROOF of Theorem 2X and Corollary 2X (v1.2, 2026-11-17; v1.1 = K1 amendments [K1-1]–[K1-4], `reviews/K1_disposition.md`; v1.2 = K2 editorial [K2-E1], [K2-E2] and line 3 rewritten to carry the full conditional status verbatim [K3-E2])

Status: **PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P** (conditions carried from `W3-MISR-R:CorGb-plus@1.0.1`, STATEMENT §5).
Statement: `STATEMENT.md` v1.3 (v1.1 locked; v1.2–v1.3 EQUAL) §§0–3 [K2-E2]; clause (E) is the explicit form of §1. Aliases as there. Every step is either a citation (file:line, id@version) or
elementary; no new estimate.

## P0. Deterministic facts (STATEMENT §3)

Fix a data set with y^r non-constant; write π for π(· | X^r, y^r) and δ := 1 − π(S₀) (δ = 1 if S₀ ∉ Ω).
1. *PIP error.* For j ∈ S₀: 1 − PIP_j = π(S ∌ j) ≤ π(S ≠ S₀) = δ. For j ∉ S₀: PIP_j = π(S ∋ j) ≤ π(S ≠ S₀) = δ.
   So max_j |PIP_j − 1{j ∈ S₀}| ≤ δ.
2. *HPM.* If HPM = T ≠ S₀, then π(T) ≥ π(S₀) = 1 − δ (T maximises π) and π(T) ≤ π(S ≠ S₀) = δ; so δ ≥ ½.
3. *MPM.* MPM = {j : PIP_j > ½}. If MPM ≠ S₀, either some j ∈ S₀ has PIP_j ≤ ½, so δ ≥ 1 − PIP_j ≥ ½ by 1, or some
   j ∉ S₀ has PIP_j > ½, so δ ≥ PIP_j > ½ by 1. Either way δ ≥ ½.
(Item 1 is [MISR] MIS-R (i) consequence 1, `:118-119`, "for every data set".) Under the model of STATEMENT §0, y^r is
non-constant almost surely (σ² > 0, n ≥ 2), so P0 holds almost surely.

## P1. Theorem 2X is an instance of CorGb-plus

Map STATEMENT §0 to the setting of [MISR-R] §3 (`:96-100`) with candidate set 𝒞 := [p] and **no omitted columns**:
- q := 0, X^r_𝓜 the n × 0 matrix, β_𝓜 ∈ ℝ⁰, so X^r_𝓜β_𝓜 = 0 ∈ ℝⁿ; X^r_𝒞 := X^r, β_𝒞 := β, m_𝒞 := m, Σ_𝒞𝒞 := Σ;
  α as in §0 (deterministic; [MISR-R] §2 allows any real random variable, `:51-54`).
- **(N)** ([MISR-R] `:56`): ε ~ N_n(0, σ²I_n), σ² a deterministic (n-dependent) parameter (§0 `:19`, `:21`), independent of
  (X^r_𝒞, X^r_𝓜) = (X^r, empty) — this is §0 [K1-3].
- **(OV)** ([MISR-R] `:67-68`) with the deterministic choices a := 0, γ := 0, τ² := 0: conditionally on X^r,
  X^r_𝓜β_𝓜 = 0 has law δ₀ = N_n(0·1 + X^r·0, 0·I_n) (N_k(m, 0) := δ_m, [MISR-R] `:31`). So (OV) holds; a, γ, τ² are
  deterministic as [MISR-R] `:97-98` requires.
- Then β^𝒞 = β_𝒞 + γ = β, σ²_𝒞 = σ² + τ² = σ² > 0, supp β^𝒞 = S₀, s = s₀, and
  π_𝒞(· | X^r_𝒞, y^r) = π(· | X^r, y^r): both are the coded target of [W3P] §0 computed from the same (X^r, y^r)
  ([MISR] §0 `:21-22`: "π_𝒞(· | x, y^r) is the coded target of [W3P] §0 (lines 16-29) computed from (x, y^r)").
  So CorGb-plus's δ_n = 1 − π_𝒞(supp β^𝒞 | X^r_𝒞, y^r) is STATEMENT's δ_n, and its HPM is STATEMENT's HPM.
- Rows: i.i.d. N_p(m, Σ) with Σ_jj > 0 ([MISR-R] `:96`) — §0. "Everything may depend on n" ([MISR-R] `:99`) — §0.

Hypotheses of CorGb-plus ([MISR-R] `:100-104`), with c_R := c:
- 2 ≤ p ≤ n^A: (A1). s := |supp β^𝒞| = s₀ ≥ 1 fixed: (A1) and the fixed s₀ of STATEMENT §1.
- *Floor.* CorGb-plus asks λ_min(R_TT) ≥ c_R for every T ⊆ 𝒞 with |T| ≤ k_n := s + max(j₀, m♯_n). For n ≥ max(3, 2s₀)
  we have s₀ ≤ K = min(p, ⌊n/2⌋) (p ≥ s₀ because S₀ ⊆ [p]), so `W3-READER:R1@1.0.2` B4.1 ([R1] `:43-45`, valid for
  s ≤ K, n ≥ 3, A ≥ 1, s ≥ 1 and p ≤ n^A ((A1); used in B1.3, [R1] `:25`), with p = |𝒞| [K1-2]) gives k_n ≤ 3(A + 1)(s₀ + 1) log n. Every non-empty T with |T| ≤ k_n is
  therefore covered by (A2). (Empty T does not arise: CorGb-plus's proof uses non-empty T only, `lemmas/G2_corr.md`
  step 2; if the floor is read for T = ∅ it is vacuous.)
- *Energy.* β^𝒞ᵀΣ_𝒞𝒞β^𝒞 = βᵀΣβ ≤ M₀σ² = M₀σ²_𝒞: (A3).
- *Beta-min.* ρ_n^{BM} = n·min_{j∈S₀} Σ_jjβ_j²/(σ² log n) = ρ_n → ∞ by (A3); this is the "→ ∞" branch named at
  [MISR-R] `:104` ("in particular if ρ_n^{BM} → ∞"), which satisfies liminf ρ_n^{BM} > 16c₀(s, A)/c_R.

Conclusion of CorGb-plus ([MISR-R] `:104-107`): there are n* and C such that for every n ≥ n*,
  E δ_n ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1} = b_n,  P(HPM ≠ S₀) ≤ 2C r_n + (2 + 2k_n)n^{−2} + n^{−1} ≤ 2b_n.
C is the constant of MIS-R (i) on 𝒦^λ_n(s, A, 2M₀ + 1, (c_R/8)^{1/2}, C_OS, c′), C_OS = C_OS(s, A) from the bridge
(F_w; 1) ⇒ (OS) and c′ = c₀(s, A) + 1 on the → ∞ branch (`lemmas/G2_corr.md`, [R-3]): it depends only on (s₀, A, M₀, c).
n* depends on the sequence. (Take n* ≥ max(3, 2s₀) as well, for the floor step above.) This is legitimate [K1-1]:
CorGb-plus's floor and energy hypotheses are used only at the current n ≥ n* (and beta-min only through a liminf; k_n is
undefined for s > K) [K2-E1], and its bounds at n concern the n-th law only (its proof checks class membership n by n, `lemmas/G2_corr.md` steps 1–5); so they hold here
for every n ≥ max(n*_master, 3, 2s₀).

## P2. The remaining displays of Theorem 2X

By P0.1, E max_j |PIP_j − 1{j ∈ S₀}| ≤ E δ_n ≤ b_n. By P0.3 and Markov, P(MPM ≠ S₀) ≤ P(δ_n ≥ ½) ≤ 2E δ_n ≤ 2b_n
(P0.2 gives the same bound for the HPM, consistent with P1). Finally k_n ≤ 3(A + 1)(s₀ + 1) log n (P1), so
(2 + 2k_n)n^{−2} = O(log n/n²) and n^{−1} = o(r_n); hence b_n = O(r_n). ∎ (Theorem 2X)

## P3. Corollary 2X

Assume the recorded hypotheses (STATEMENT §2). Then the §0 setting holds with m := m_n, Σ := Σ_n (Σ_jj = 1 > 0),
σ² := σ*² > 0, α := α*, β := β* (parameters of the model of `Theory_work/Wave3/W3-READER/NOTATION.md:15-20`, read as
non-random as in the recorded fixed-signal setting; α* may even be random, [MISR-R] `:52-53`) [K1-3].
- (A1): (S2) and s₀ ≥ 1.
- (A2) with c := φ²: R = Σ_n (unit diagonal), and every T with 1 ≤ |T| ≤ 3(A + 1)(s₀ + 1) log n also has
  |T| ≤ 5(A + 1)(s₀ + 1) log n, where the recorded floor gives λ_min(Σ_{n,T}) ≥ φ². (If the recorded floor is asked only on
  |S| ≤ 3(A + 1)(s₀ + 1) log n, this is (A2) directly.)
- (A3), energy: βᵀΣ_nβ = β_{S₀}ᵀ(Σ_n)_{S₀S₀}β_{S₀} ≤ λ_max((Σ_n)_{S₀S₀})‖β_{S₀}‖² ≤ tr((Σ_n)_{S₀S₀})·s₀b_hi² = s₀²b_hi²
  (a positive semidefinite matrix has λ_max ≤ trace; the trace of an s₀ × s₀ correlation block is s₀). So
  βᵀΣ_nβ ≤ M₀σ*² with M₀ := s₀²b_hi²/σ*², fixed.
- (A3), beta-min: ρ_n = n·min_{j∈S₀}β_j²/(σ*² log n) ≥ n b_lo²/(σ*² log n) → ∞.
So Theorem 2X applies. Its displays give the recorded conclusions: δ_n ≥ 0 and E δ_n = O(r_n) give δ_n = O_P(r_n)
(Markov: P(δ_n > L r_n) ≤ E δ_n/(L r_n)); P(HPM ≠ S₀) + P(MPM ≠ S₀) = O(r_n) → 0 gives P(HPM = MPM = S₀) → 1; the PIP
error is ≥ 0 with expectation O(r_n), hence O_P(r_n). ∎ (Corollary 2X)

## P4. What the proof does not use

No upper eigenvalue bound on Σ; no condition on m; α only deterministic (and even that is not used, [MISR-R] `:52-53`) [K1-3]; no fixed σ², Σ or β (only the fixed constants A, s₀, c, M₀ and
ρ_n → ∞); no Gaussianity beyond the rows and the noise (both used only through CorGb-plus).
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-D2/TARGET.md @934a2b43 (whole file) >>>
# W3-D2 — TARGET (one page; 2026-11-17)

## Assumption map (Theorem 2X; reader form)
| hypothesis | where it enters | how | necessity reading |
|---|---|---|---|
| Gaussian rows N_p(m, Σ), Σ_jj > 0 | CorGb-plus proof steps 1–3 (`W3-MISR-R/lemmas/G2_corr.md`) | sample SDs, sparse eigenvalues, energy χ² | not known to be necessary (sub-Gaussian rows: audit candidate #3) |
| Gaussian noise ⫫ design, σ² > 0 | (N) → (GR^c | σ(X)) | exact contrast law | as Theorem 1 (open) |
| (A1) p ≤ n^A, s₀ fixed | size cutoff m♯_n, union bounds | as Theorem 1 | as Theorem 1 (`W3-PSHARP:B` for s₀) |
| (A2) floor on R, \|T\| ≤ 3(A+1)(s₀+1) log n | CorGb-plus floor on \|T\| ≤ k_n | (F₀), (F_λ), (F_w) ⇒ (OS) | floor on S₀-anchored small sets needed (row 1.1 why-lines); size 3(…) is an upper bound for k_n (N1 (i): ≤ 0.40 of it) |
| (A3) βᵀΣβ ≤ M₀σ² | energy (E^σ) | posterior of the variance on scale | some control necessary (row 1.1 counterexample) |
| (A3) ρ_n → ∞ | (BM^σ) | beta-min branch | order √(log n/n) believed necessary (numerics); a fixed liminf level suffices (CorGb-plus) |

## Parity (each main clause)
| clause | (a) PROGRAM goals | (b) closest published (Song–Liang 2015, Thm 2/3) | (c) best registered (row 1.2 masters) |
|---|---|---|---|
| E δ_n = O(r_n) | matches (p ≫ n, method as coded) | beats: they give screening in probability, no expectation rate | beats: row 1.2 is O_P |
| P(HPM/MPM ≠ S₀) = O(r_n) | matches | beats (exact selection with a rate) | beats (row 1.2: → 0, no rate) |
| floor size | matches | short in kind: they need no sparse floor of this form but assume Condition 1 (stronger moment form) — as row 1.2 | beats: 3(A+1)(s₀+1) log n vs 5(A+1)(s₀+1) log n |
| scope (Σ, β, σ² vary with n) | matches | beats (theirs fixed-order) | beats (row 1.2 fixes σ², bounded β) |
| vanishing floor allowed | — | — | **incomparable** [L1-2]: W2-APP:POST keeps a fixed floor on \|S\| ≤ min(p, s₀ + j₀) and allows ψ_n → 0 (ψ_n√n/(log n)^{3/2} → ∞) on \|S\| ≤ k̄_n; Theorem 2X needs a fixed c on \|T\| ≤ k_n (CorGb-plus's transfer uses one fixed floor); keep the old master as coexisting |
| status | — | — | **short**: conditional (CorGb-plus's conditions; W3-POST2:C ← W3-POST:Prop-LB unchecked) vs "clean" |

## Boundary numerics
`numerics/N1_floor_and_e2e.py` → `N1_out.txt`: (i) exact k_n vs 3(…) and 5(…) log n on 150 grid cases: max ratio 0.394;
(ii) end-to-end exact enumeration (p = 6) with Σ_n, σ_n² varying with n and Σ not a correlation matrix (outside the recorded
Theorem 2, inside Theorem 2X): E δ_n / r_n = 2.14, 1.58, 1.12, 1.15, 1.08, 1.07 at n = 50…1600; P(HPM ≠ S₀) = 0 at n = 1600.
A floor-size boundary cannot be simulated at small p (3(A+1)(s₀+1) log n > p); the floor's size is a proof device.
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-D2/numerics/N1_floor_and_e2e.py @934a2b43 (whole file) >>>
#!/usr/bin/env python3
"""N1 (W3-D2): (i) floor-size arithmetic of Lemma D2-B1; (ii) one end-to-end exact check of Theorem 2X.

(i) For the coded size cutoff m#_n of [W3P] Theory_work/Wave3/W3-POST/STATEMENT.md:33-39
    q_k = C(p, k) w(k), w(k) = 1/2 / C(2p - 1, k)  (0 <= k <= K = min(p, floor(n/2))),
    R_m = sum_{k = max(m+1, 0)}^{K} q_k / w(s0),
    m#_n = min{m >= s0 : R_m <= n^{-(s0+1)/2} e^{-omega}},  omega = (1/2) log n,
    j0 = ceil((2A + 1) s0) + 1,  k_n = s0 + max(j0, m#_n)   (W3-MISR-R STATEMENT.md:96-100),
computed exactly in log space, and compared with 3(A+1)(s0+1) log n (Theorem 2X, (A2)) and with the recorded
row-1.2 size 5(A+1)(s0+1) log n. Worst case over the grid uses p = floor(n^A) (largest allowed p).

(ii) Exact enumeration of the coded target pi of [W3P] :16-29 (p = 6) under random Gaussian designs with
quantities that vary with n (allowed by Theorem 2X, outside the recorded Theorem 2):
    rows iid N_6(m, Sigma_n), Sigma_n = D (rho_n J + (1 - rho_n) I) D, D = diag(1, 2, 0.5, 3, 1, 1),
    rho_n = 0.5 - 1/log n, m = (5, -3, 0, 1, 0, 2);
    beta = (1, -0.7, 0, 0, 0, 0) / D (so Sigma_jj beta_j^2 = (1, 0.49)), alpha = 4;
    sigma_n^2 = (log n)^{1/2}   (grows; energy and beta-min relative to sigma_n^2 still hold).
Outputs per n: E delta_n, P(HPM != S0), P(MPM != S0), E max_j |PIP_j - 1{j in S0}|, and E delta_n / r_n.
"""
import itertools
import math
import sys

import numpy as np


def log_comb(a, b):
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)


def logsumexp(v):
    m = max(v)
    return m + math.log(sum(math.exp(x - m) for x in v))


def m_sharp(n, p, s0):
    K = min(p, n // 2)
    if s0 > K:
        return None
    logw_s0 = math.log(0.5) - log_comb(2 * p - 1, s0)
    logq = [log_comb(p, k) + math.log(0.5) - log_comb(2 * p - 1, k) for k in range(K + 1)]
    thr = -((s0 + 1) / 2) * math.log(n) - 0.5 * math.log(n)
    # tail sums from the top: T[m] = log sum_{k=m+1}^{K} q_k
    tail = [-math.inf] * (K + 2)
    for k in range(K, -1, -1):
        a, b = tail[k + 1], logq[k]
        tail[k] = b if a == -math.inf else max(a, b) + math.log1p(math.exp(-abs(a - b)))
    for m in range(s0, K + 1):
        lr = (tail[m + 1] if m + 1 <= K else -math.inf) - logw_s0
        if lr <= thr:
            return m
    return K


def part_i():
    print("# (i) k_n = s0 + max(j0, m#_n) against 3(A+1)(s0+1) log n and 5(A+1)(s0+1) log n")
    print("# grid: A in {1, 1.5, 2, 3, 5}, s0 in {1, 2, 3, 5, 10}, n in {3, 10, 100, 400, 1e3, 1e4, 1e5}; p = floor(n^A) capped at 1e15")
    worst = 0.0
    rows = []
    for A in [1, 1.5, 2, 3, 5]:
        for s0 in [1, 2, 3, 5, 10]:
            for n in [3, 10, 100, 400, 1000, 10_000, 100_000]:
                if 2 * s0 > n:
                    continue
                p = int(min(math.floor(n ** A), 10 ** 15))
                if p < max(2, s0):
                    continue
                ms = m_sharp(n, p, s0)
                j0 = math.ceil((2 * A + 1) * s0) + 1
                kn = s0 + max(j0, ms)
                b3 = 3 * (A + 1) * (s0 + 1) * math.log(n)
                b5 = 5 * (A + 1) * (s0 + 1) * math.log(n)
                worst = max(worst, kn / b3)
                rows.append((A, s0, n, p, ms, j0, kn, b3, b5))
    for A, s0, n, p, ms, j0, kn, b3, b5 in rows:
        if n in (100, 400, 10_000) and s0 in (1, 5) and A in (1, 2):
            print(f"A={A:<4} s0={s0:<3} n={n:<7} p={p:<12} m#={ms:<5} j0={j0:<4} k_n={kn:<5} "
                  f"3(A+1)(s0+1)log n={b3:8.1f}  5(A+1)(s0+1)log n={b5:8.1f}")
    print(f"# max over the grid of k_n / [3(A+1)(s0+1) log n] = {worst:.4f} ({len(rows)} cases); must be <= 1")


def posterior(x, yr, models, P):
    n = x.shape[0]
    xc = x - x.mean(axis=0)
    sd = np.sqrt((xc ** 2).sum(axis=0) / (n - 1))
    X = xc / sd
    yc = yr - yr.mean()
    y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
    K = min(P, n // 2)
    nu = 0.01 + n / 2
    b0 = 0.01
    G = X.T @ X
    zf = X.T @ y
    yty = y @ y
    lp = {}
    for S in models:
        k = len(S)
        if k > K:
            continue
        logw = math.log(0.5) - log_comb(2 * P - 1, k)
        if k == 0:
            logD, Q = 0.0, yty
        else:
            idx = list(S)
            GS = G[np.ix_(idx, idx)]
            H = (n + 1) * GS + np.eye(k)
            logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(k))[1]
            z = zf[idx]
            Q = yty - n * z @ np.linalg.solve(H, z)
        lp[S] = logw - 0.5 * logD - nu * math.log(2 * b0 + Q)
    L = logsumexp(list(lp.values()))
    return {S: math.exp(v - L) for S, v in lp.items()}


def part_ii(R):
    P = 6
    models = [S for k in range(P + 1) for S in itertools.combinations(range(P), k)]
    D = np.array([1.0, 2.0, 0.5, 3.0, 1.0, 1.0])
    mvec = np.array([5.0, -3.0, 0.0, 1.0, 0.0, 2.0])
    beta = np.array([1.0, -0.7, 0, 0, 0, 0]) / D
    S0 = (0, 1)
    rng = np.random.default_rng(20261117)
    print(f"\n# (ii) end-to-end exact enumeration, p = 6, R = {R} replications per n, seed 20261117")
    print("n      rho_n   sigma2_n  E_delta   P(HPM!=S0)  P(MPM!=S0)  E_maxPIPerr  r_n     E_delta/r_n")
    for n in [50, 100, 200, 400, 800, 1600]:
        rho = 0.5 - 1 / math.log(n)
        Sig = np.diag(D) @ (rho * np.ones((P, P)) + (1 - rho) * np.eye(P)) @ np.diag(D)
        Lc = np.linalg.cholesky(Sig)
        s2 = math.sqrt(math.log(n))
        dl = hm = mm = pe = 0.0
        for _ in range(R):
            x = mvec + rng.standard_normal((n, P)) @ Lc.T
            yr = 4.0 + x @ beta + math.sqrt(s2) * rng.standard_normal(n)
            post = posterior(x, yr, models, P)
            d = 1 - post.get(S0, 0.0)
            pip = np.zeros(P)
            for S, v in post.items():
                for j in S:
                    pip[j] += v
            truth = np.array([1.0 if j in S0 else 0.0 for j in range(P)])
            mpm = tuple(j for j in range(P) if pip[j] > 0.5)
            hpm = max(post, key=post.get)
            dl += d
            hm += hpm != S0
            mm += mpm != S0
            pe += np.abs(pip - truth).max()
        rn = math.sqrt(math.log(n) / n)
        print(f"{n:<6} {rho:6.3f}  {s2:7.3f}   {dl / R:8.5f}  {hm / R:8.4f}    {mm / R:8.4f}    {pe / R:8.5f}     "
              f"{rn:.4f}  {dl / R / rn:7.3f}")


if __name__ == "__main__":
    part_i()
    part_ii(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-D2/numerics/N1_out.txt @934a2b43 (whole file) >>>
# (i) k_n = s0 + max(j0, m#_n) against 3(A+1)(s0+1) log n and 5(A+1)(s0+1) log n
# grid: A in {1, 1.5, 2, 3, 5}, s0 in {1, 2, 3, 5, 10}, n in {3, 10, 100, 400, 1e3, 1e4, 1e5}; p = floor(n^A) capped at 1e15
A=1    s0=1   n=100     p=100          m#=17    j0=4    k_n=18    3(A+1)(s0+1)log n=    55.3  5(A+1)(s0+1)log n=    92.1
A=1    s0=1   n=400     p=400          m#=23    j0=4    k_n=24    3(A+1)(s0+1)log n=    71.9  5(A+1)(s0+1)log n=   119.8
A=1    s0=1   n=10000   p=10000        m#=35    j0=4    k_n=36    3(A+1)(s0+1)log n=   110.5  5(A+1)(s0+1)log n=   184.2
A=1    s0=5   n=100     p=100          m#=45    j0=16   k_n=50    3(A+1)(s0+1)log n=   165.8  5(A+1)(s0+1)log n=   276.3
A=1    s0=5   n=400     p=400          m#=68    j0=16   k_n=73    3(A+1)(s0+1)log n=   215.7  5(A+1)(s0+1)log n=   359.5
A=1    s0=5   n=10000   p=10000        m#=111   j0=16   k_n=116   3(A+1)(s0+1)log n=   331.6  5(A+1)(s0+1)log n=   552.6
A=2    s0=1   n=100     p=10000        m#=25    j0=6    k_n=26    3(A+1)(s0+1)log n=    82.9  5(A+1)(s0+1)log n=   138.2
A=2    s0=1   n=400     p=160000       m#=32    j0=6    k_n=33    3(A+1)(s0+1)log n=   107.8  5(A+1)(s0+1)log n=   179.7
A=2    s0=1   n=10000   p=100000000    m#=48    j0=6    k_n=49    3(A+1)(s0+1)log n=   165.8  5(A+1)(s0+1)log n=   276.3
A=2    s0=5   n=100     p=10000        m#=50    j0=26   k_n=55    3(A+1)(s0+1)log n=   248.7  5(A+1)(s0+1)log n=   414.5
A=2    s0=5   n=400     p=160000       m#=115   j0=26   k_n=120   3(A+1)(s0+1)log n=   323.5  5(A+1)(s0+1)log n=   539.2
A=2    s0=5   n=10000   p=100000000    m#=178   j0=26   k_n=183   3(A+1)(s0+1)log n=   497.4  5(A+1)(s0+1)log n=   828.9
# max over the grid of k_n / [3(A+1)(s0+1) log n] = 0.3942 (150 cases); must be <= 1

# (ii) end-to-end exact enumeration, p = 6, R = 300 replications per n, seed 20261117
n      rho_n   sigma2_n  E_delta   P(HPM!=S0)  P(MPM!=S0)  E_maxPIPerr  r_n     E_delta/r_n
50      0.244    1.978    0.59913    0.4333      0.4300     0.45422     0.2797    2.142
100     0.283    2.146    0.33842    0.1333      0.1300     0.22216     0.2146    1.577
200     0.311    2.302    0.18290    0.0167      0.0167     0.10153     0.1628    1.124
400     0.333    2.448    0.14093    0.0100      0.0067     0.07848     0.1224    1.152
800     0.350    2.585    0.09842    0.0067      0.0067     0.05426     0.0914    1.077
1600    0.364    2.716    0.07275    0.0000      0.0000     0.04031     0.0679    1.071
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-MISR-R/STATEMENT.md @a14ce83b lines 88-108 >>>
  v = σ² + τ²(x).
**Remark (what β^𝒞 is; no claim).** Under (OV^c), the mean of the regular conditional law of UᵀX^r_𝓜β_𝓜 given
X^r_𝒞 = x is Uᵀxγ(x) (no integrability of UᵀX^r_𝓜β_𝓜 itself is assumed or needed) [L1-3]: β^𝒞 is the candidate
coefficient of the conditional mean of the response contrasts given the candidates. As in BASE `:41-42`, β^𝒞 need
not be unique when UᵀX^r_𝒞 has deficient column rank; statements are about the chosen γ.

## 3. Corollary G(b)⁺ (W3-MISR-R:CorGb-plus) — replaces BASE Cor-G(b), `:171-174`

Setting: rows x^r_{𝒞,i}, i ≤ n, iid N_p(m_𝒞, Σ_𝒞𝒞) with Σ_jj > 0 (j ∈ 𝒞; Σ_𝒞𝒞 ≻ 0 is not assumed beyond the floor
below); (N) and (OV) of §2 with **deterministic**
a, γ, τ² (e.g. (E1) with Σ_𝒞𝒞 ≻ 0, or (E2) with Gaussian candidate rows); β^𝒞 := β_𝒞 + γ, σ²_𝒞 := σ² + τ² > 0.
Everything (m_𝒞, Σ_𝒞𝒞, β, γ, σ², τ², p) may depend on n. R := D_Σ^{−1/2}Σ_𝒞𝒞D_Σ^{−1/2}, D_Σ := diag(Σ_𝒞𝒞), is the
correlation matrix of a candidate row. Assume: 2 ≤ p ≤ n^A; s := |supp β^𝒞| ≥ 1 fixed; with k_n := s + max(j₀, m♯_n)
(m♯_n of BASE `:34` with p = |𝒞|),
  λ_min(R_TT) ≥ c_R > 0 for every T ⊆ 𝒞 with |T| ≤ k_n;  β^𝒞ᵀΣ_𝒞𝒞β^𝒞 ≤ M₀σ²_𝒞;
  ρ_n^{BM} := n·min_{j∈supp β^𝒞} Σ_jj(β^𝒞_j)²/(σ²_𝒞 log n) satisfies liminf_n ρ_n^{BM} > 16c₀(s, A)/c_R
(c₀ of BASE `:63`; in particular if ρ_n^{BM} → ∞, BASE's condition). Then there are n* and C such that for every n ≥ n*, with δ_n := 1 − π_𝒞(supp β^𝒞 | X^r_𝒞, y^r):
  E δ_n ≤ C r_n + (2 + 2k_n)n^{−2} + n^{−1},  P(HPM ≠ supp β^𝒞) ≤ 2C r_n + (2 + 2k_n)n^{−2} + n^{−1};
so both are O(r_n). (C is the constant of BASE MIS-R (i) on 𝒦^λ_n for (s, A, 2M₀ + 1, φ₀ = (c_R/8)^{1/2}, C_OS, c), with
C_OS of the bridge (F_w; 1) ⇒ (OS) and c > c₀(s, A) fixed by the beta-min branch; n* depends on the sequence.)
With m_𝒞 = 0 and jointly Gaussian rows, supp β^𝒞 is SL's s̃ (BASE `:174`).
<<<END FILE>>>

<<<FILE Theory_work/Wave3/W3-POST/STATEMENT.md @e2680987 lines 16-40 >>>
## 0. The target π (the method as coded)

Data (X^r, y^r), n ≥ 3, with non-constant y^r (s_y > 0; a.s. under G) [R01-4]. p = number of **retained** (non-constant)
raw columns (the code drops constant columns before K and the prior are formed, `Scripts/SMC_BVS/core/v3_preprocess.R:111-127`);
X = CX^rD_x⁻¹ = standardised design of the retained columns (centred, ‖x_j‖² = n − 1), y = Cy^r/s_y with
s_y² = ‖Cy^r‖²/(n − 1). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S, H_S = (n + 1)G_S + I,
D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S (z_S = X_Sᵀy), ν = 0.01 + n/2;
m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν}, a₀ = b₀ = 0.01; prior ϖ(S) = w(|S|)/W_K, w(k) = ½/C(2p − 1, k) (capped BB(1, p));
π(S) ∝ ϖ(S)m(S) on Ω. (Definitions: `ARC/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md:9-14`; code:
`Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224` — K = min(p, n/2), ν = a₀ + n/2, H = (n+1)G + I, A = G + I,
log w(k) = −log 2 − log C(2p−1, k).) Equivalently π is the exact posterior under the **working** likelihood
y | S, β_S, σ² ~ N_n(X_Sβ_S, σ²I) with β_S | S, σ² ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01) on the standardised
scale (the standardised y does not have this law under the truth; the proofs treat it as a working model, [P1]
lines 155-221) [R01-4]. π is the real-arithmetic target of the code; floating-point fidelity is not part of this file.

Truth: y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I) (**G**), μ := CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp θ*, s₀ = |S₀|,
r_n := √(log n/n). Exact posterior outputs: δ_n := 1 − π(S₀) (π(S₀) := 0 if s₀ > K); PIP_j := π(j ∈ S);
HPM := argmax_Ω π (any tie rule); MPM := {j : PIP_j > ½}; ξ_q := {j : PIP_j > q}. These are properties of π, not of the
sampler.

Size cutoff (data-free — a fixed function of (n, p, s₀), not computable from data since s₀ is unknown [R02-F6]): q_k := C(p, k)w(k) for 0 ≤ k ≤ K (q_k := 0 otherwise [C2A-F4]), R_m := Σ_{k=max(m+1,0)}^{K} q_k / w(s₀), and
m♯_n(ω) := min{m ∈ ℤ : m ≥ s₀, R_m ≤ n^{−(s₀+1)/2}e^{−ω}} (defined for s₀ ≤ K, real ω), m♯_n := m♯_n(½ log n)
([T03R] §1, lines 15-17, 44-47). For s₀ ≤ K: s₀ ≤ m♯_n(ω) ≤ K; and for s₀ ≥ 1, ω ≥ 0 [R01-1]:
m♯_n(ω) ≤ min{K, s₀ + ⌈(log C(p, s₀) + ((s₀+1)/2) log n + ω)/log 2⌉} ([T03R] E2(ii), lines 50-54).

<<<END FILE>>>
