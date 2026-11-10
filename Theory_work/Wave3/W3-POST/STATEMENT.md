# W3-POST — STATEMENT (v1.4, 2026-11-09; lead: Claude Opus 5.5, claudeAgent, high; v1.1 = R01 amendments [R01-#], v1.2 = R02 [R02-F#], v1.3 = council C1 [C1A-F#, C1B-F#], v1.4 = council C2/C3 [C2A-, C2B-, C3A-, C3B-#]; council-passed C3)

Ticket: PROGRAM item 1 (`Theory_work/Wave3/PROGRAM.md`) — consolidated posterior-concentration theorem (Theorem 1),
the size-tail lemma on its own (Lemma 1a), an independent adversarial re-check of the proof chain, and the sharpness
gate. This file states; it proves nothing new except Lemma 1a′ (`lemmas/L1a_size_tail.md`) and Proposition LB
(`lemmas/LB_rate_lower_bound.md`) [C3B-N1]. Statuses are verbatim.

Aliases. `ARC/` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/`;
**[P1]** = `ARC/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` (locked T01/T02);
**[P3]** = `ARC/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (locked T03);
**[T03R]** = `ARC/W1-T03R/PROOF.md` (T02(i♯), T02(ii♯), T03♯ — the restated theorem; proof by diff against [P1], [P3]);
**[POST]** = `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` (random design); **[SL]** =
`Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md` (SL0, SL1, SL1′); **[UNI]** = `Theory_work/Wave2/W2-UNI/STATEMENT.md`
(UNI-P, §3(i)).

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

## 1. Lemma 1a (size tail; no eigenvalue condition on X)

**Lemma 1a (= T02(i♯), [T03R] lines 79-85; status "T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED",
`Theory_work/State_of_Project/sections/04_theory.tex:771`).** Assume p ≥ 2 [C1B-F3], G, ‖μ‖² ≤ nM, λ_min(X_{S₀}ᵀX_{S₀}/(n−1)) ≥ φ₀²
and s₀ ≤ K. For every integer m define Θ♯_{n,m} ≥ 0 by π(|S| > m) = R_m (n + 1)^{s₀/2}√n · Θ♯_{n,m} (Θ♯ := 0 if R_m = 0).
Then for every L > c♯² (c♯ a constant depending on (σ*², M) only):
  sup_m P(Θ♯_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C_Λ / log(√L / c♯),
with C_Λ = 1/√2 + 1/2 + 1{s₀ ≥ 1}(1 + 1/(2φ₀²))(M + σ*²)/(2σ*²). Hence for every deterministic ω_n,
π(|S| > m♯_n(ω_n)) ≤ (1 + 1/n)^{s₀/2}e^{−ω_n}Θ♯ = O_P(e^{−ω_n}). Non-asymptotic; uses neither p ≤ n^A nor any condition
on models other than S₀.

**Lemma 1a′ (design-free form; NEW in this ticket — `lemmas/L1a_size_tail.md`, status there).** Replace the eigenvalue
condition on S₀ by a coefficient bound: suppose there are T ∈ Ω and θ ∈ ℝ^T with X_Tθ = μ, ‖μ‖² ≤ nM and ‖θ‖² ≤ nM′.
Then the conclusion of Lemma 1a holds with s₀ replaced by t := |T| in R_m, m♯_n and the normalisation, and with
C_Λ replaced by C′_Λ := 1/√2 + 1/2 + (M + M′)/(2σ*²). In particular, with T = S₀ and |θ*_j| ≤ θ_hi:
**models above m♯_n carry posterior mass O_P(n^{−1/2}) for every standardised design X with ‖Xθ*‖² ≤ nM** — no
eigenvalue condition; automatic for fixed s₀ (M = s₀²θ_hi², since |x_jᵀx_k| ≤ n − 1) — uniformly over such X for fixed
(σ*², M, M′), and for any s₀ ≤ K (s₀ may grow as long as (E) holds, which for growing s₀ is a real condition) [R02-F1]. (Compare BLIND_fable Lemma A,
`Theory_work/Wave2/SR/BLIND_fable.md:92-93`.)

## 2. Theorem 1 (posterior concentration; consolidated, design-agnostic)

**Regime R1.** Triangular array, n → ∞; s₀ ≥ 1 fixed; 2 ≤ p = p_n ≤ n^A ([T03R] line 9 assumes p ≥ 2) [C1B-F3] for a fixed A ≥ 1 (p ≫ n allowed); s₀ ≤ K
eventually; σ*² > 0 fixed; G.

**Hypotheses on (X, θ*)** (fixed design; fixed constants 0 < φ₀ ≤ 1, 0 < g₀ < ∞, 0 ≤ M < ∞ [R01-4]; j₀ := ⌈(2A + 1)s₀⌉ + 1):
- **(E) energy**: ‖μ‖² ≤ nM.
- **(F_λ) anchored floor, bounded size** = SE_λ(j₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}/(n−1)) ≥ φ₀² for every J ⊆ [p]∖S₀ with
  |J| ≤ j₀ (J = ∅ included: this contains R's condition on S₀). *By interlacing it implies* λ_min(R_S) ≥ φ₀² for
  **every** S with |S| ≤ j₀ (S ⊆ S₀ ∪ S), so it excludes e.g. duplicated null columns [R02-F2].
- **(F_w) anchored unnormalised floor, logarithmic size** = SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every
  J ⊆ [p]∖S₀ with |J| ≤ m♯_n (m♯_n = O(log n) under R1). By interlacing it implies λ_min(G_S) ≥ g₀ for every S with
  |S| ≤ m♯_n: no exact linear dependence among ≤ m♯_n columns [R02-F2].
- **(BM) beta-min**, either BM-∞: θ*²_min nφ₀²/(σ*² log n) → ∞; or BM(c): θ*²_min ≥ cσ*² log n/(nφ₀²) with a fixed
  c > c₀(s₀, A) := max{4C_*, 32[s₀(A + 1) + 2]} (C_* the [P3] proof constant; a proof artefact, not sharp).

(Source: [T03R] §6 lines 162-168; card `Theory_work/State_of_Project/sections/04_theory.tex:780-788`; status "T03♯:
PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", `Theory_work/State_of_Project/sections/04_theory.tex:771`.)

**Theorem 1.** In R1 under G, (E), (F_λ), (F_w):
1. **(Rate)** Under (BM): δ_n = 1 − π(S₀) = O_P(r_n).
2. **(Exact HPM, MPM, thresholded models)** Under (BM): P(HPM = S₀) ≥ P(δ_n < ½) → 1 and P(HPM ≠ S₀) ≤ 2Eδ_n → 0;
   P(MPM = S₀) → 1; P(ξ_{q_n} = S₀) → 1 for every deterministic q_n ∈ (0, 1) with r_n = o(min(q_n, 1 − q_n)).
3. **(PIPs)** For every data set, max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n; under (BM) this is O_P(r_n) (sensitivity and
   specificity uniformly in j), and E max_j |PIP_j − 1{j ∈ S₀}| → 0 (no expectation rate claimed).
4. **(Size, functionals)** Under (BM): π(|S| = s₀) = 1 − O_P(r_n); sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = O_P(r_n).
5. **(Without beta-min)** (a) *No strict-superset mass* [R02-F3]: π(S ⊋ S₀) = O_P(r_n) (needs only, in R1, G, (E),
   λ_min(R_{S₀}) ≥ φ₀², (F_w) [R02-F9]; swaps S₀∖{j} ∪ {k} are not controlled; = T02(ii♯), [T03R] line 149). (b) *Strong-signal recovery*: for fixed c > c₀ and
   J_n(c) := {j ∈ S₀ : θ*²_j ≥ cσ*² log n/(nφ₀²)}, π(S ⊉ J_n(c)) = O_P(r_n), hence max_{j∈J_n(c)}(1 − PIP_j) = O_P(r_n)
   (vacuous if J_n(c) = ∅). (c) *Size tail*: Lemma 1a / 1a′. **COUNTEREXAMPLE (numerical, E5; leading-order analytic sketch, unchecked)** [C1B-F4] to specificity
   max_{j∉S₀} PIP_j → 0 without
   beta-min, even under (E), (F_λ), (F_w) with fixed floors — a null proxy of several weak truths takes the posterior
   (`ASSUMPTION_MAP.md`, item POST-BM′: numerics E5 with a leading-order computation for E5's own design; R03 §5A's
   p = 3 construction is the same mechanism with a margin too small to see at n ≤ 10⁶, per C1 seat B).
6. **(Random design, interface form)** [C1A-F7] Let (X, θ*) be random with ε independent of (X, θ*), and suppose there
   are (X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which |supp θ*| = s₀ [C2B-N2] and (E), (F_λ), (F_w) hold with common constants
   (M, φ₀, g₀) and (BM) holds with a common c > c₀ or a common deterministic envelope M_n → ∞. Then 1–4 hold under the
   joint law of (X, θ*, ε); if only (E), (F_λ), (F_w) hold on 𝒜_n, 5(a) and 5(b) hold under the joint law. (Proof:
   apply the fixed-design statements along every deterministic sequence in 𝒜_n; the diagonal tightness transfer of
   [POST] step (5) gives uniformity; add P(𝒜_nᶜ) → 0.)
7. **(Rate lower bound — the rate is sharp up to √log n)** For every data set and every design, if 1 ≤ s₀ < p and
   s₀ + 1 ≤ K, then 1 − π(S₀) ≥ 1/(1 + √(n+1)) (Proposition LB, `lemmas/LB_rate_lower_bound.md`, "PROVED (by this seat,
   unchecked)"; falsification `numerics/lb_check.py` → `lb_check_out.txt`: min over 34 920 cases of
   (1 − π(S₀))(1 + √(n+1)) = 1.013). Whether the extra √(log n) is attained for p = n^A is a conjecture [C1A-F1, C1B-F2].

**Corollary 1R (a sufficient bridge for item 6; Gaussian rows — an example, not part of Theorem 1).** Let the raw rows
be iid N(m, Σ_n), Σ_n a unit-diagonal correlation matrix, ε independent of the design, and **LSF** (fixed 0 < φ ≤ 1):
(i) λ_min(Σ_{n,S}) ≥ φ² for |S| ≤ min(p, s₀ + j₀); (ii) λ_min(Σ_{n,S}) ≥ ψ_n for |S| ≤ k̄_n := min(p, s₀ + max(j₀, m̄_n)),
m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ = O(log n), with ψ_n√n/(log n)^{3/2} → ∞.
(a) With fixed 0 < b_lo ≤ |β_j| ≤ b_hi < ∞ on S₀ and the raw-design event of [POST] lines 12-18 (or fixed standardised
0 < θ_lo ≤ |θ*_j| ≤ θ_hi < ∞) [R01-4], the events of item 6 exist with φ₀² = φ²/2, g₀ = 1, M = s₀²θ_hi² + 1 and the
envelope θ_lo²nφ₀²/(σ*² log n) → ∞ (raw case: θ_lo = b_lo/2, θ_hi = 2b_hi) [C3B-N5]; hence 1–4 hold under the joint law ([POST] Lemma POST(a)-(b), lines 23-33;
status "PROVED (by this seat, unchecked)", W2-APP review R02 VERIFIED-WITH-AMENDMENTS; restated as UNI-P, [UNI]
lines 87-91). (b) Without the lower bound (keep only |θ*_j| ≤ θ_hi or |β_j| ≤ b_hi) the events still carry (E), (F_λ),
(F_w) ([POST] steps (2)–(4) do not use θ_lo), so 5(a) and 5(b) hold with J_n(c) defined by φ₀² := φ²/2 [R02-F4] — a
lead's extension of [POST](b)'s wording, checked by R02 (`reviews/R02_recheck_opus.md`, F4) and both C1 council seats.
Under the raw-scale convention θ* = D_xβ* is design-measurable, so J_n(c) is a random (design-measurable) set; the
diagonal transfer of [POST] step (5) applies along every deterministic sequence in 𝒜_n, J_n(c) included [C1B-N5].

**Proof route.** 1, 5(b): T03♯ ([T03R] §6, by diff against [P3], with T02(i♯) as Step 0 and T02(ii♯) for supersets).
2–4: SL0/SL1 ([SL] lines 20-63), deterministic consequences of δ_n. 7: Proposition LB (prior ratio, [P3] `lem:det`,
[P1] `lem:spec`(d)). 5(a): T02(ii♯) ([T03R] §5). 6: diagonal transfer ([POST] step (5)).
Corollary 1R: [POST] steps (1)–(5): sample entrywise event, Weyl transfer of the floors, diagonal tightness transfer.

**Interface property (protocol rule 5).** The eigenvalue assumptions on X enter through one bridge: the *anchored
floor property* AF(φ₀, g₀) := (F_λ) ∧ (F_w) (with (E)). Corollary 1R ([POST]) is one bridge LSF ⇒ AF w.p. → 1; Theorem 1 consumes AF.
(Beta-min and J_n(c) also involve (X, θ*) through φ₀; Lemma 1a′ needs no part of AF [R02-F11].)
