# W3-D3 — K1 line check (Opus 5.5, high; fresh, blind) — 2026-11-17

Scope: `STATEMENT.md` v1.1 §§0–3 (spans §§1–3), `lemmas/B3w.md`, `lemmas/ASSEMBLY.md`, `reviews/STATEMENT_v1.0_to_v1.1.diff`,
and the consumed sources named in `reviews/K1_brief.md` (W3-POST STATEMENT :16-100; [EB] B0, B1, B2core, B2, B3; [R1] B1.2,
B1.3; [RV] :26-30, :257-290, :1095-1100; [NOT] §§1–2; W3-DIST STATEMENT (RD) :17-20 for B0 (e)'s scope). I did not read
LOG.md, CHECKPOINT files or other reviews. I did not change git state. My scratch directory `.rc_tmp/` has been deleted.

## Verdicts

- `lemmas/B3w.md` — **VERIFIED-WITH-AMENDMENTS** (K1-1, K1-2, K1-4, K1-5, K1-6; none changes a constant or a conclusion).
- `lemmas/ASSEMBLY.md` — **VERIFIED-WITH-AMENDMENTS** (K1-1; ExSG (a), (b) and the in-place Hoeffding proof VERIFIED as written).
- `STATEMENT.md` v1.1 (claimed spans §§1–3) — **VERIFIED-WITH-AMENDMENTS** (K1-1 wording of (c), K1-3, K1-11; changelog K1-7, K1-8).

Numerical side check (my own script, deleted). First, the window: for A ∈ {1, 1.5, 2, 3, 5}, s₀ ∈ {1, 2, 3, 5, 8},
n ∈ [3, 10⁵] and p ∈ [2, min(n^A, 10⁵)], I computed m♯_n exactly from [W3P] :36-37 (log-domain). Over 859 cases there were
no violations of min(p, s₀ + j₀) ≤ w_n, min(p, s₀ + m♯_n) ≤ w_n or s₀ + m♯_n ≤ 3(A + 1)(s₀ + 1) log n, and the largest
(s₀ + m♯_n)/W̄_n was 0.219. Second, on λ ∈ [−30, 30]: cosh λ ≤ e^{λ²/2}, sinh(√3λ)/(√3λ) ≤ e^{λ²/2}, and the Hoeffding bound
held on every two-point mean-zero law on [a, a + 2K] for K ∈ {½, 1, 2}. Third, the §5 converse example: for ε = 10⁻⁴, at
λ = log(1/ε) the MGF along z₁ − z₂ is 5001 while the (A4) bound with L = 3 is 1.16.

## Findings

**K1-1 (C, minor; fix is a choice of θ⁰ plus one sentence).** `B3w.md:104-106` (also `STATEMENT.md:72-75`) completes the
truth by "θ⁰ ∈ ℝ^p with |supp θ⁰| = s₀ (any choice)". W3-POST item 6 applied to (X°, θ°) gives its conclusions for the
random true set supp θ°, not for S₀ = supp β*. In 𝒜′_n, (F_λ) and (F_w) are likewise anchored at supp θ°. Yet
`ASSEMBLY.md:39-41` states "P(HPM° = S₀) → 1 … max_j |PIP°_j − 1{j ∈ S₀}| ≤ δ°_n" with δ°_n = 1 − π°(S₀). With an arbitrary
θ⁰, supp θ⁰ ≠ S₀ is possible off {p_ret = p}. The conclusion survives: on {p_ret = p} every ŝ_j > 0, so
supp θ° = supp θ̃* = S₀, and Step 4 adds P(p_ret ≠ p) anyway. The text does not say this, though.
*Fix:* in B3w Step 6 and STATEMENT §2 (c), take θ⁰ with **supp θ⁰ = S₀**, which is allowed because β* is deterministic and
|S₀| = s₀ ≤ p. Then add to ASSEMBLY Step 3: "supp θ° = S₀ on every outcome (on {p_ret = p} because all ŝ_j > 0; off it by
the choice of θ⁰), so item 6's outputs refer to S₀; in 𝒜′_n, (F_λ) and (F_w) are anchored at supp θ° = S₀."

**K1-2 (F).** `B3w.md:45-51` says "Statements used verbatim", but the quotations of B1 (a) ("P(𝓔₁ᶜ) ≤ 4p·exp(−c₁n/L⁴)") and
of B2-core ("If q′·log(ep/q′) ≤ c₂n/L⁴ …, then P(𝓔₂(q)) ≥ 1 − exp(−c₂n/L⁴)") replace the source's K by L. The sources
(`B1.md:13`, `B2core.md:15`) read K⁴, and in the same quotation (SG₁) keeps K. *Fix:* restore K⁴ inside the quotation marks
and add after them "(read with K := L, [L1-1])".

**K1-3 (S, wording).** `STATEMENT.md:76`: "… 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p}, and so on the events 𝒜′_n the hypotheses of [W3P]
Theorem 1 item 6 hold …". Item 6's hypotheses include P(𝒜′_n) → 1, which comes from (b), not from the two preceding
facts. They also include R1 (s₀ ≤ K eventually, 2 ≤ p ≤ n^A, G) and the independence of ε. "And so" therefore presents an
inference that is not made there. B3w (c) (`B3w.md:37-40`) states the claim correctly. *Fix:* replace it with "Moreover
(with (b): P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) the hypotheses of [W3P] Theorem 1 item 6 hold for (X°, θ°, ε/σ*) in regime R1 with the
events 𝒜′_n, …".

**K1-4 (E).** `B3w.md:65-66`: "The left side is an integer, so it is ≤ ⌊W̄_n⌋". The nearest left side is (2A + 2)s₀ + 2,
which is not an integer when A is not. The intended integer is |S₀ ∪ J|. *Fix:* "|S₀ ∪ J| is an integer ≤ W̄_n, so
|S₀ ∪ J| ≤ ⌊W̄_n⌋ = q_n".

**K1-5 (E).** `B3w.md:3`: "Target: `STATEMENT.md` §2 (v1.0)". The file proves the v1.1 statement, since it carries [L1-1] and
[L1-2] and part (c). *Fix:* "(v1.1)". `ASSEMBLY.md:23` "Fix n" should read "Fix n ≥ 3", because B0 assumes n ≥ 3. This is
harmless, since n ≥ n₁ ≥ 3 wherever it is used.

**K1-6 (E).** `B3w.md:110-112`: the measurability argument says each condition is a finite collection of inequalities
between continuous functions. That is not accurate for |supp θ°| = s₀, for θ°_min, or for (F_λ) and (F_w), which are
anchored at the random support. Each is a finite union over T ⊆ [p] of {supp θ° = T} ∩ {Borel conditions for T}, so the
conclusion stands. *Fix:* "Borel (a finite union over supports T of Borel conditions)". After K1-1 the support is fixed
and the issue goes away.

**K1-7 (E, changelog completeness).** These diff changes have no changelog row:
- §2 v1.1 adds n₁ ≥ max(3, 2s₀), writes 𝓔₂(q_n) for 𝓔₂(w_n) (the same event, `B3w.md:22-23`), and computes m♯_n "with
  p_ret" instead of "with p" (equal on 𝒜_n). It also replaces "θ*" by θ̃* and splits (vi) into (b).
- §4 (a) adds non-Gaussian examples, §4 (b) adds the rare-jump failure, and §4 (d) adds "with L > 0".
- §6 and §7 change "items 1–4" to "items 1–3" (a narrower consumed scope, correct: only 1–3 are used) and add the Hoeffding
  input and the "adapts W3-DIST:B3" relation.
- §8 adds text ("admits non-Gaussian laws", "SL1 (a)–(e)", "its three conclusions").

*Fix:* add one row: "§2 bookkeeping (n₁ ≥ max(3, 2s₀), q_n for w_n, p_ret in m♯_n, θ̃*); §4 (a), (b), (d); §6; §7; §8 |
EQUAL (equal events and objects on 𝒜_n / outside spans; consumed scope narrowed to items 1–3) | L1, Q2 | — |".

**K1-8 (S, tagging).** In changelog row 2 (`STATEMENT.md:179`), part (c) of B3w is a **new conclusion** of the companion
claim W3-D3:B3w. It is the existence of (X°, θ°)-measurable events 𝒜′_n ⊇ 𝒜_n on which item 6's hypotheses hold. v1.0's B3w
stated only (i)–(vi) on 𝒜_n; the v1.0 heading implied (c), but the heading is not a clause, and v1.1 moves it out of the
span. The same file tags the analogous addition, ExSG (b), STRONGER on the companion claim. *Fix:* tag row 2 as
"**STRONGER** on the companion claim B3w (added conclusion (c), proved in B3w Step 6); EQUAL for Theorem 2SG".

**K1-9 (E, §5 outside spans; observation only).** The converse example (z₁ = R, z₂ = RB, P(B = −1) = ε → 0) is correct as
worded: Condition 1 holds because |z_j| = 1, and (A4) fails along z₁ − z₂ for every fixed L. But Corr(z₁, z₂) = 1 − 2ε → 1,
so the example also violates (A3). If §5 is ever read as saying that (A4) is strictly stronger than Condition 1 *among
designs that satisfy (A3)*, this example does not show it. Under (A3) with bounded coordinates, (A4) holds on directions
of bounded size, so such an example would need directions of logarithmic size or unbounded coordinates. *Fix:* none
required; optionally add "(the example also has Corr(z₁, z₂) → 1)".

**K1-10 (E).** §1 (A3) (`STATEMENT.md:49-50`) drops the recorded parenthetical "(for instance, λ_min(Σ_n) ≥ φ²)" of [RV]
row thm2, while §5 and §8 call (A1)–(A3) "verbatim". This is harmless because the parenthetical is an example, not a
condition. *Fix:* restore it, or write "verbatim up to the parenthetical example".

**K1-11 (E, span hygiene).** `STATEMENT.md:78`, "(𝒜_n itself need not be (X, θ̃*)-measurable; it is used only for its
probability.)", is commentary inside a registered span. It is true, because 𝓔₁ involves the sample scales of null columns,
which standardisation discards. *Fix:* move it to §4 or label it as a remark.

**K1-12 (E, §5 2b sentence).** The sentence is true for (A4) (ExSG (a), (b)) under the reading that ξ_k has mean 0 and
variance 1 and lies in [−K, K], so the interval has length 2K and L = K, with K fixed in n, and under the §4 (e)
normalisation that makes BBᵀ unit-diagonal. "Qualify" means "satisfy (A4)": Theorem 2SG also needs (A3). *Fix (optional):*
"qualify for (A4)".

## Per-step table

| file | step | verdict | note |
|---|---|---|---|
| B3w | Statement (a)–(c) | VERIFIED-WITH-AMENDMENTS | K1-1 (θ⁰ support), K1-2 (quotations); the statement proves slightly more than STATEMENT §2 (p_ret = p ≥ 2, φ₀ ≤ ½, the 5n^A form of (b)) |
| B3w | Step 0 (window) | VERIFIED (K1-4 wording) | (1): s₀ + j₀ ≤ (2A + 2)s₀ + 2 ([R1] B1.2) ≤ 5.493(A + 1)(s₀ + 1) ≤ W̄_n for n ≥ 3; integer, so ≤ q_n; ≤ p trivially. (2): [R1] B1.3 used within its hypotheses (n ≥ 3, A ≥ 1, s₀ ≥ 1, s₀ ≤ K_cap, p_ret ≤ p ≤ n^A); 3(A + 1) ≤ 5(A + 1). W̄_n ≥ 21.9 ≥ s₀ ∨ 1 |
| B3w | Step 1 (B1, B2-core hypotheses) | VERIFIED | z = x − m_n has E z = 0, Var z_j = Σ_jj = 1, Γ = Σ_n; (A4) at e_j is (SG₁) with K := L; (A4) restricted to ≤ q_n entries is (SG_{q_n}); q′ = w_n ≥ 1; log(ep/w_n) ≤ 1 + A log n; w_n log(ep/w_n) ≤ W̄_n(1 + A log n) ≤ c₂n/L⁴ for n ≥ n₁; n₁ is finite and depends on (s₀, A, L) only |
| B3w | Step 2 ((a)(i), (ii)) | VERIFIED | B1 (b): p_ret = p; ŝ_j > 0 ⇒ supp θ̃* = S₀; K_cap ≥ s₀ for n ≥ 2s₀; B1 (c) with b̄ = b_hi/σ*, sd = 1 ⇒ ‖μ̃‖² ≤ n·2s₀²b_hi²/σ*² = nM_E; μ̃ = Xθ̃* |
| B3w | Step 3 ((a)(iii)) | VERIFIED | G_T = nΛ_TΣ̂^z_TΛ_T (B2 :45-48, Λ_T = diag(1/ŝ_j)); B2-core "in particular" on ũ (≤ q_n entries); (A3) on T, |T| ≤ W̄_n; ŝ_j² ≤ 2 ⇒ ≥ (nφ²/4)‖u‖²; φ₀² = φ²/4, φ₀ ∈ (0, ½] |
| B3w | Step 4 ((a)(iv)) | VERIFIED | B2 hypotheses: p ≥ 2, Var ∈ (0, ∞), (SG_{q_n}), (A4_{q_n}) with c_ψ = φ² (φ² ≥ φ²/n); B2 (a) ⇒ φ²/4 ≥ φ²/8 = g₀; sizes from Step 0 (2) on 𝒜_n. (Lossy but valid: Step 3's argument gives nφ²/4.) |
| B3w | Step 5 ((a)(v)) | VERIFIED | θ̃*_j = ŝ_jβ*_j/σ* (B0 (f)); ŝ_j² ≥ ½ ⇒ θ̃*_j² ≥ b_lo²/(2σ*²); ×nφ²/(4 log n) = M_n = b_lo²nφ²/(8σ*² log n) → ∞; σ*² = 1 in item 6's (BM) |
| B3w | Step 6 / (c) | VERIFIED-WITH-AMENDMENTS | K1-1, K1-6. The completion is admissible (X⁰ has centred, non-constant columns of norm² n − 1 and is its own standardisation); (X°, θ°) is Borel in the raw design ({p_ret = p} is open and X, θ̃* are continuous on it), hence independent of ε; m♯_n(n, p, s₀) is deterministic; 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p}; R1 holds for the completed pair (K = min(p, ⌊n/2⌋) ≥ s₀, 2 ≤ p ≤ n^A, ε/σ* ~ N(0, I)) |
| B3w | (b) | VERIFIED | B1 (a) for n ≥ 3 plus B2-core under Step 1's size condition; c₂ ≤ c₁, p ≤ n^A ⇒ ≤ 5n^A e^{−c₂n/L⁴} → 0 |
| ASSEMBLY | Step 1 (scale) | VERIFIED (K1-5: n ≥ 3) | B0 (a) needs a non-constant y^r and p_ret ≥ 1; B0 (e) applies because (RD) allows an arbitrary row law ν_x; the outputs are functions of the model posterior and of S₀ = supp β̃* |
| ASSEMBLY | Step 2 (events) | VERIFIED | P(p_ret ≠ p) ≤ P(𝒜_nᶜ) because 𝒜_n ⊆ 𝓔₁ ⊆ {p_ret = p} |
| ASSEMBLY | Step 3 (item 6, dimension) | VERIFIED-WITH-AMENDMENTS | K1-1. Y° = X°θ° + Cε/σ* is C of the response of the fixed design X^r := X° (CX° = X°, D = I, θ* = θ°), so it is a legitimate W3-POST fixed-design instance; on {p_ret = p}, Y° = Cỹ (CX^rβ̃* = Xθ̃*); the posterior depends on (X, Cy^r) only; the conventions are not invoked on {p_ret = p} (S₀ ∈ Ω since K_cap ≥ s₀) |
| ASSEMBLY | Step 4 (conclusions) | VERIFIED (given K1-1) | (1) and (3) by adding P(p_ret ≠ p); (2) by the union bound; (3) uses item 3's every-data-set bound; transfer to the original data by Step 1 (pathwise equality) |
| ASSEMBLY | Constants | VERIFIED | M_E depends on (s₀, b_hi, σ*²); φ₀ and g₀ on φ; M_n on (b_lo, φ, σ*², n); n₁ on (s₀, A, L) |
| ASSEMBLY | ExSG (a) | VERIFIED | mean, covariance BBᵀ = Σ; the product over the finitely many independent coordinates; ‖Bᵀu‖² = uᵀΣu; "(A4)" needs m = m_n, Σ = Σ_n and L fixed in n (implicit, see interpretive list) |
| ASSEMBLY | ExSG (b), Gaussian / Rademacher / uniform | VERIFIED | cosh: (2k)! ≥ 2^k k!; sinh(√3λ)/(√3λ) = Σ3^kλ^{2k}/(2k + 1)!, with (2k + 1)!/(2^k k!) = (2k + 1)!! ≥ 3^k; each law has mean 0 and variance 1 |
| ASSEMBLY | ExSG (b), Hoeffding (in place) | VERIFIED | the chord bound; the a = 0 or b = 0 degenerate cases; θ = −a/(b − a) ∈ (0, 1); e^{−θh}(1 − θ + θe^h); ψ(0) = ψ′(0) = 0, ψ″ = ρ(1 − ρ) ≤ ¼; Lagrange ⇒ ψ(h) ≤ h²/8; b − a = 2K ⇒ exp(K²λ²/2) |

## Statement vs proof (task 2)

- Theorem 2SG (§1) is exactly what ASSEMBLY proves: the three conclusions under the joint law, with the hypotheses (A1)–(A4)
  plus the §0 setting. No unstated hypothesis is used. The proof uses s₀ ≥ 1 fixed, 2 ≤ p ≤ n^A, Σ_n a correlation
  matrix (Var x_j = 1), ε ~ N(0, σ*²I) independent of X^r, α* and β* deterministic, and φ, L, b_lo, b_hi fixed. All are
  stated in §0 and §1. The triangular-array law of x may depend on n; the only uniformity used is the fixed L and φ, which
  are stated.
- Lemma B3w: STATEMENT §2 (a)–(c) ⊆ `B3w.md` (a)–(c). The quantifiers match ("there is n₁ = n₁(s₀, A, L) ≥ max(3, 2s₀) such
  that for every n ≥ n₁"), and so do the constants M_E, φ₀², g₀ and M_n in units after B0. (a) holds on 𝒜_n, whose
  probability bound is (b); (c) then holds as worded, with K1-1 and K1-3.
- ExSG: §3 (a) and (b) are exactly what is proved.

## Statement-change table (task 3, v1.0 → v1.1)

| row (`STATEMENT.md:178-183`) | tag claimed | verdict | reason |
|---|---|---|---|
| 1.1 symbols L, K_cap | EQUAL | **CONFIRMED** | For Theorem 2SG the renaming is pure. "Fixed K" → "fixed L > 0" is EQUAL: K = 0 is infeasible because Var(z) = 1, and only L² enters. For B3w, v1.0 "(i) … s₀ ≤ K" read literally under the collision (K = sub-Gaussian constant) was a different, false clause. EQUAL holds against the *intended* v1.0 clause, and the row should say so ("corrects a notational defect") |
| 1.1 §2 interface / completed pair / part (c) | EQUAL | **CONTESTED** for B3w → STRONGER (added conclusion (c)), K1-8; **CONFIRMED** EQUAL for Theorem 2SG (its text is unchanged; (c) is how the proof already had to go, B3 A-2) |
| 1.1 §0 conventions | EQUAL | **CONFIRMED** | π(S₀) := 0 and PIP_j := 0 were already in v1.0. The p_ret = 0 convention only defines the outputs on {p_ret = 0} ⊆ {p_ret ≠ p}, whose probability → 0, so no O_P or "→ 1" conclusion is affected |
| 1.1 §4 (e), §5 centring, §2 heading/provenance | EQUAL (outside spans / editorial) | **CONFIRMED** | the heading and provenance are not clauses |
| 1.1 ExSG B, part (b) | STRONGER on ExSG; Theorem 2SG unchanged | **CONFIRMED** | (b) adds bounded features with L = K. v1.0's "K = 1 when every ξ_k is Gaussian, Rademacher, uniform" is retained and slightly generalised (the coordinates may be mixed). Theorem 2SG does not consume ExSG, so it is EQUAL there |
| 1.1 §5 HQ wording, NH14 note | EQUAL (outside spans) | **CONFIRMED** | — |
| (missing) | — | add a row | K1-7 (§2 bookkeeping, §4 (a)/(b)/(d), §6, §7, §8) |

Of special interest:
- The symbol change, interface part (c) and conventions are all EQUAL for Theorem 2SG: **confirmed**.
- ExSG (b) is STRONGER on the companion claim: **confirmed**, and its proof is verified.

## Interpretive sentences inside the spans (task 4)

| `STATEMENT.md` line | sentence | verdict |
|---|---|---|
| :74 | "(X°, θ°) is a Borel function of the raw design, hence independent of ε." | **checked** (ε ⫫ X^r by (S1); B3w Step 6) |
| :76 | "… 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p}, and so on the events 𝒜′_n the hypotheses of [W3P] Theorem 1 item 6 hold …" | **reword** (K1-3): the conclusion is true and proved, but it follows from (b) and the R1 check, not from the preceding clause |
| :78 | "(𝒜_n itself need not be (X, θ̃*)-measurable; it is used only for its probability.)" | **move out** (commentary; true), K1-11 |
| :85 | "In particular (A4) holds with this L." | **checked**, assuming the rows are copies of x with m = m_n, Σ = Σ_n and L fixed in n (suggest writing "(with m = m_n, Σ = Σ_n)") |

There are no hence/so/in particular sentences in §1.

## STATEMENT §5 relations (task 5, outside the spans)

| relation | verdict |
|---|---|
| NH14 isotropic sub-Gaussian rows as the case Σ = I, for centred rows, with L a fixed multiple of their sub-Gaussian constant | **True.** Centred isotropic rows have Σ = I, a correlation matrix. A ψ₂ bound K on every direction gives E exp(λ⟨X, u⟩) ≤ exp(Cλ²K²‖u‖²) for mean-zero rows, which is (A4) with L² = 2CK² (absolute C), provided K is fixed in n. The containment is strict: (A4) at Σ = I constrains sparse directions only. "Contains … as the special case" should be read as containment, not identity |
| (A4) ⇒ Song–Liang Condition 1 for z = x − m_n | **True.** (A4) at u = e_j gives E e^{λz_j} ≤ e^{L²λ²/2}. By Jensen, exp((Σa_iz_{j_i}/r)²) ≤ r⁻¹Σexp(δ²z_{j_i}²), and E exp(tz²) ≤ (1 − 2tL²)^{−1/2} for t < 1/(2L²). With δ² ≤ 1/(4L²) this gives M = ½ log 2, for every r |
| the converse fails (z₁ = R, z₂ = RB, rare sign flip) | **True as worded** (Condition 1 holds since |z_j| = 1; along z₁ − z₂, at λ = log(1/ε), the MGF ≈ 1/(2ε) → ∞ while the bound → 1). See the K1-9 observation (the example also violates (A3)) |
| the 2b sentence | **True for (A4)** via ExSG (a), (b) (an interval of K sd either side ⇒ length 2K ⇒ L = K; Rademacher K = 1; uniform K = √3, and L = 1 by (b) directly). "Light-tailed … ordinary situation" is non-mathematical. See K1-12. The statement that HQ's first wording is false is correct: a standardised binary with P(x_j = 1) → 0 has MGF ≥ πe^{λa}, a ≈ π^{−1/2}, and λ = 2 log(1/π)/a gives ≥ 1/π → ∞ while the (A4) bound → 1 |
