# O-WSTAB — REPORT: weight stability of the composite start (W0 → W1 → W2 → Theorem W → W′)

Branch `theory/O-WSTAB` (Opus 5.5, laptop run taking over from the stopped server run). Everything here is a
**candidate**: not reviewed, not adopted. Status words follow `theory_campaign/PROTOCOL.md`. Notation: `00_COMMON.md`;
[PF] = `theory_campaign/O-WSTAB/PROOF.md` (WS1–WS8, the earlier part of this run); [FD] = F-DRAFT
(`origin/theory/F-DRAFT`, `CROSSWALK.md`, `NEW_TARGETS.md`). New symbols are defined where introduced.

## 1. Headline

1. **One function governs everything.** For any reference model S° let ℓ(φ) := −log q_φ(S°). It is convex, and
   **log(1 + χ²(q_v‖q_u)) = ℓ(u) + ℓ(2v−u) − 2ℓ(v) exactly** (T13(i) with V = Ω, in second-difference form). In the
   favourable regime every stage's χ² equals ℓ(2v−u) + o_P(1). The ideal ESS-0.9 grid's stage count is pinned between
   ⌈log₂(1+1/g₊)⌉ and ⌈log₂(1+1/g₋)⌉, where g± are read off the sublevel sets of ℓ. (Prop L, Prop G: **PROVED**, deterministic.)
2. **W0** (three norms of π/π₀) **PROVED**. It is self-contained: a Doeblin argument replaces the unseen Liu (1996)
   citation and gives a two-sided rate for the independence move. **W1** **PROVED** ([PF] WS3). **W2** **PROVED** in an
   *exact* finite-n form, κG ≤ LR ≤ κG/(1−y), with no EXP′ needed.
3. **Theorem W under ORTH** (X′X = (n−1)I, any partition, s₀ and θ* fixed, p log p = o(n)), with r := R²_pop:
   if p^r/√n → 0, then p^{r−ε}/√n ≤ χ²(π‖π₀) ≤ p^{r+ε}/√n w.p. → 1, both sides **PROVED**. If
   L_n := r log p − ½ log n − ((1+r)/2) log log p → ∞, then **c·e^{L_n/r} ≤ log(1+χ²) ≤ C·e^{L_n/r}(log p)^{5(1+r)/(2r)}**,
   i.e. log log(1+χ²) = L_n/r + O(log log p): polynomial in n (both sides **PROVED**, the upper one via an integral
   form of the separable bound).
   KL(π‖π₀) and TV(π, π₀) → 0 throughout (**PROVED**). The proof never takes an expectation of a heavy-tailed weight.
4. **COUNTEREXAMPLE to [FD] Theorem W(c)** ("log(1+χ²) = [R² log p − ½ log n]₊ + O_P(log log p)"). On the divergent side,
   multi-extra models dominate: with p = n^A and Ar > ½, log(1+χ²) ≥ n^{A−1/(2r)−o(1)}, not O(log n). Exact large-p
   numerics agree: at n = 10¹⁶, p = n^{0.95}, r = 0.9 the exact lower bound is 8.8·10³ nats, while W(c) predicts 13.
   The *threshold* of W (Ar ≶ ½) is correct, and so are W(a) and, on the convergent side, W(b).
5. **W′ under ORTH**: the ideal ESS-0.9 grid has **T_ideal ∈ {1, 2}** w.p. → 1. T = 1 if 2Ar < 1, T = 2 if 2Ar > 1
   (with p = n^{A+o(1)}). This is the [FD] formula ⌈log₂(1+1/g)⌉ with g → 1/(2Ar) (**PROVED** for the ideal full-space
   grid; the method's V-restricted pilot grid is a separate, stated obligation). General BO with correlated blocks, and
   p ≍ n: **PROOF SKETCH** / **OPEN**.

## 2. Statements

Standing notation. g(z) := −log(1 − z) on [0, 1) (a function; not the design code G). Fit fractions x_S := t_S/Q̄,
Q̄ = 2b₀ + yᵀy ([PF] §0; Lemma 0: log BF(S) = −½ log D_S + ν g(x_S), 0 ≤ x_S < 1). Bridge q_φ ∝ γ₀e^{φd}, φ ∈ ℝ.
For a reference model S° ∈ Ω: **ℓ(φ) = ℓ_{S°}(φ) := −log q_φ(S°)** and **O(φ) := 1/q_φ(S°) − 1 = e^{ℓ(φ)} − 1** (the
off-reference odds). ℓ* := max{ℓ(0), ℓ(1)} = max{−log π₀(S°), −log π(S°)}. c := log(10/9) (the ESS-0.9 threshold:
ρ ≥ 0.9 ⇔ log(1+χ²) ≤ c). Favourable regime: ℓ_{S₀}* → 0 in probability; masked: ℓ_{S₀}(0) → ∞ (00_COMMON, T22, T27).

**Proposition W0 (three faces; deterministic; EX-A). PROVED.** With r(S) := π(S)/π₀(S) = e^{d(S)}/E_{π₀}e^{d} and
M := max_Ω r:
(i) 1 + χ²(π‖π₀) = E_{π₀}e^{2d}/(E_{π₀}e^{d})² = Z̄₀Z̄₂/Z̄₁² = 1/ρ_Ω(0,1) = π(S)²/(π₀(S)q₂(S)) for every S ∈ Ω.
(ii) π(S)²/π₀(S) ≤ 1 + χ²(π‖π₀) ≤ M for every S; KL(π‖π₀) ≤ log(1+χ²(π‖π₀)); TV ≤ √(KL/2).
(iii) (independence move at φ = 1 = Metropolised independence sampler with proposal π₀, T09(ii)) Its kernel K satisfies
K(x, ·) ≥ π(·)/M for every x, so ‖K^t(x,·) − π‖_TV ≤ (1 − 1/M)^t for all x, t. Conversely, for x* ∈ argmax r,
‖K^t(x*,·) − π‖_TV ≥ (1 − 1/M)^t − π(x*). So, from the worst state, the move needs ≍ M steps.
(iv) (iid discovery, T11(iii)) P(S absent from Q iid π₀ draws) = (1 − π₀(S))^Q ≥ 1 − Qπ₀(S), and π(S)/π₀(S) ≤ M.

**Lemma W1 (= [PF] WS3; PROVED).** Under BO, for every S: D_S = ∏_b D_{S_b}, t_S = Σ_b t_{S_b},
d(S) = ν[g(x̄_S) − Σ_b g(x_b(S))] ≥ 0 with x̄_S = Σ_b x_b(S) = x_S, and equality iff at most one block has x_b(S) > 0.
π₀ is π with the shared noise precision replaced by an independent copy per block (mean-field representation
WS3(d)), and with known σ² the same tables give d ≡ 0, π₀ = π.

**Lemma W2 (exact dilution form; PROVED).** Assume BO. Let S° ∈ Ω, l ∉ S° in block b, S° + l ∈ Ω, T := S° ∩ C_b.
Put x̄ := x_{S°} (and x_T the fit fraction of T), y := (t_{T+l} − t_T)/(Q̄ − t_{S°}) ∈ [0, 1), **κ := (x̄ − x_T)/(1 − x_T) ∈ [0, 1)** (the
fraction of block b's table residual that is other blocks' fit: the realised dilution fraction), and
G := log[BF(S°+l)/BF(S°)] + ½ log(D_{T+l}/D_T) = ν g(y) (the posterior's fit gain). Then
 LR := log[π(S°+l)/π(S°)] − log[π₀(S°+l)/π₀(S°)] = d(S°+l) − d(S°) = ν[g(y) − g((1−κ)y)],
 **κ G ≤ LR ≤ κ G/(1 − y)**,
and the table's fit gain is ν g((1−κ)y) = G − LR. *Statistical reading* (ORTH, S° = S₀, l a null in a truth-free block):
T = ∅, κ = x_{S₀} = r + O_P(n^{−1/2}), G = (Z_l²/2)(1 + O_P(n^{−1/2})) and y = O_P(log p/n), uniformly over nulls
(§3.6). So LR_l = r·Z_l²/2·(1 + O_P(n^{−1/2} + log p/n)) uniformly. Under general BO, identifying G with
Z²_{T,l}/2 is EXP′ (W1-EXP Thm 1, candidate).

**Proposition L (ℓ-form of T13; deterministic; PROVED).** For every S° ∈ Ω:
(i) ℓ is real-analytic and convex on ℝ, and ℓ ≥ 0.
(ii) For all real u, v, with w = 2v − u: log(1 + χ²(q_v‖q_u)) = ℓ(u) + ℓ(w) − 2ℓ(v), i.e. ρ_Ω(u, v) = exp{−[ℓ(u) + ℓ(w) − 2ℓ(v)]}.
The same holds for the V-restricted bridge with ℓ_V(φ) := −log q^V_φ(S°), S° ∈ V, and ρ_V (T13(iii)).
(iii) For 0 ≤ u, v ≤ 1: ℓ(u), ℓ(v) ≤ ℓ*, hence ℓ(w) − 2ℓ* ≤ log(1 + χ²(q_v‖q_u)) ≤ ℓ(w) + ℓ*.
(iv) 1 + χ²(π‖π₀) = π(S°)² e^{ℓ(2)}/π₀(S°), and ℓ(2) − 2ℓ* ≤ log(1 + χ²(π‖π₀)) ≤ ℓ(2) + ℓ*.

**Proposition G (ideal-grid sandwich; deterministic; PROVED).** Fix S° with 2ℓ* < c. Let g₋ := sup{g ≥ 0 : ℓ(1+g) ≤ c − ℓ*}
and g₊ := sup{g ≥ 0 : ℓ(1+g) ≤ c + 2ℓ*}, both in (0, ∞]. The *ideal grid* is φ₀ = 0,
φ_t := max{v ∈ (φ_{t−1}, 1] : ρ_Ω(φ_{t−1}, v) ≥ 0.9}, until φ_T = 1. It is well defined, and
 ⌈log₂(1 + 1/g₊)⌉ ≤ T ≤ ⌈log₂(1 + 1/g₋)⌉ (with 1/∞ := 0).
Moreover, along any grid with every interval accepted: 2ℓ(φ_t) ≥ ℓ(φ_{t−1}) − c (the masked-regime halving of [PF] WS7(d)).

**Lemma SEP (separable domination under ORTH; deterministic; PROVED).** Assume ORTH (XᵀX = (n−1)I_p), any partition, any
S₀ ∈ Ω (here only a reference model). Put x_j := x_{{j}}, s := Σ_{j∈S₀} x_j, N := [p] ∖ S₀, ū := Σ_{j∈N} x_j/(1 − s), and
suppose ū < 1. For w ∈ [0, 2] let β(w) := 1/((1−s)(1−ū)) if w ≤ 1 and β(w) := w/((1−s)(1−ū)) − (w − 1) if 1 ≤ w ≤ 2;
c_j(w) := n^{−1/2}e^{β(w)νx_j}, q(w) := p^{−1}Σ_{j∈N} c_j(w). If q(w) < 1 then
 **ℓ_{S₀}(w) ≤ Σ_{j∈S₀} log(1 + 2p√n e^{−νx_j}) − (s₀ + 1) log(1 − q(w)).**

**Lemma SEP′ (integral form; deterministic; PROVED).** Same setting as Lemma SEP, *without* the condition q(w) < 1:
 **ℓ_{S₀}(w) ≤ Σ_{j∈S₀} log(1 + 2p√n e^{−νx_j}) + log[(1/s₀!)∫₀^∞ t^{s₀}e^{−t}∏_{j∈N}(1 + t c_j(w)/p) dt].**
(Lemma SEP follows from it via ∏(1 + ty_j) ≤ e^{tq}.)

**Theorem W (ORTH; two-sided).** Hypotheses **H-ORTH**: G; ORTH; s₀ ≥ 1 fixed and θ*_{S₀} fixed with all entries nonzero, so
**r := R²_pop = ‖θ*‖²/(‖θ*‖² + σ*²) ∈ (0, 1)** is fixed; p → ∞ with p log p = o(n); any partition (it may depend on X)
whose blocks have size ≤ B, with B fixed (or B ≤ 16, the method's cap). Let N₀ be the nulls in truth-free blocks
(|N₀| ≥ p − s₀B), and ρ_n(w) := p^{(w−1)₊r}/√n. Then, with P₀-probability → 1:
(a) **(both ends concentrate)** ℓ(0), ℓ(1) = O_P(√(log p/n)) for S° = S₀. So π₀(S₀) → 1 and π(S₀) → 1 (self-contained;
 consistent with W1-EXP Thm 2/6 and locked T03).
(b) **(uniform upper bound)** There is V_n = O_P(1), not depending on w, with q(w) ≤ V_n ρ_n(w)√(log p) for all w ∈ [0, 2].
 Hence ℓ(w) ≤ o_P(1) − (s₀+1) log(1 − V_nρ_n(w)√log p) whenever V_nρ_n(w)√log p < 1. The o_P(1) is uniform in w and
 equal to O_P(p√n e^{−c₀n}).
(c) **(uniform lower bound)** For all w ∈ [1, 2]: O(w) ≥ ρ_n(w)(log p)^{−(1+(w−1)r)/2}e^{−U_n}, with U_n = O_P(1) not
 depending on w.
(d) **(convergent side)** If p^r/√n → 0, then for every ε ∈ (0, r): p^{r−ε}/√n ≤ χ²(π‖π₀) ≤ p^{r+ε}/√n. So the one-step
 ESS fraction 1/(1+χ²) → 1 at exactly this polynomial rate.
(e) **(divergent side, lower bound)** If L_n := r log p − ½ log n − ((1+r)/2) log log p → ∞, then log(1 + χ²(π‖π₀)) ≥ e^{(L_n − C₁ − 1)/r}
 with the constant C₁ := 1 + log 2 + (1+r) log 4 + ((1+r)/2) log(4π). With p = n^{A+o(1)} and Ar > ½ this is
 n^{A − 1/(2r) − o(1)}, and the ESS fraction is ≤ exp(−n^{A−1/(2r)−o(1)}).
(g) **(divergent side, upper bound)** w.p. → 1, ℓ(2) ≤ (s₀+1) log 2 + o(1) + K_r(1 + o_P(1))·[p^r(log p)^{2(1+r)}/√n]^{1/r}
 with K_r := (r/2)(2π/((1+r) sin(π/(1+r))))^{(1+r)/r}. Together with (e), when L_n → ∞:
 c e^{L_n/r} ≤ log(1+χ²(π‖π₀)) ≤ C e^{L_n/r}(log p)^{5(1+r)/(2r)}.
(f) **(KL and TV)** TV(π, π₀) ≤ ℓ* = O_P(√(log p/n)) and KL(π‖π₀) = O_P((log p)^{3/2}/√n) in all cases, including (e).

**Theorem W′ (ORTH; ideal grid).** Under H-ORTH, with G_n := log n/(2r log p): w.p. → 1, g± (Prop G, S° = S₀) satisfy
|g± − G_n| ≤ δ_n with δ_n = O_P(log log p/log p) whenever G_n + δ_n ≤ 1, and g₋ ≥ 1 when G_n − δ_n ≥ 1. Consequently
T_ideal ∈ {⌈log₂(1 + 1/(G_n + δ_n))⌉, …, ⌈log₂(1 + 1/(G_n − δ_n))⌉} ∩ {1, 2}. In particular, with p = n^{A+o(1)}:
**T_ideal = 1 if 2Ar < 1 and T_ideal = 2 if 2Ar > 1**, and always T_ideal ≤ 2 w.p. → 1 (ORTH forces p ≤ n − 1, so
G_n ≥ 1/(2r) > ½).

**Counterexample W(c).** [FD] Theorem W(c) is false on the divergent side: under H-ORTH with p = n^A and Ar > ½,
log(1+χ²(π‖π₀)) − [r log p − ½ log n]₊ → ∞ polynomially (Theorem W(e)). Also [FD] W(b) ("1+χ² ≤ 1 + p^{R²+ε}/√n + o(1)")
is false there, because log(1+χ²) grows faster than any multiple of log p.

## 3. Proofs

### 3.1 Prop W0
(i) is [PF] WS1(a) with (u, v) = (0, 1) and WS2(c). E_{π₀}e^{d} = Z̄₁/Z̄₀ because π₀e^{d} = γ₀e^{d}/Z̄₀.
(ii) Lower bound: Cauchy–Schwarz on {S}, {S}ᶜ ([PF] WS1(b)). Upper bound: Σπ²/π₀ = Σπ·r ≤ M. KL = E_π log r ≤
log E_π r = log(1+χ²) by Jensen; Pinsker.
(iii) For y ≠ x, K(x, y) = π₀(y) min{1, r(y)/r(x)} ≥ π₀(y) r(y)/M = π(y)/M, because r(x) ≤ M and r(y) ≤ M. For y = x,
K(x, x) ≥ π₀(x)·1 = π(x)/r(x) ≥ π(x)/M. So K = εΠ + (1−ε)R with ε = 1/M, Π(x,·) = π and R a Markov kernel. πK = π gives
πR = π, so for any law μ, μK − π = (1−ε)(μ − π)R, and ‖(μ−π)R‖_TV ≤ ‖μ − π‖_TV ≤ 1; iterate. Converse: from x*,
P(move) = Σ_{y≠x*} π₀(y) min{1, r(y)/M} ≤ Σ_y π₀(y)r(y)/M = 1/M. So K^t(x*, {x*}) ≥ (1−1/M)^t and
‖K^t(x*,·) − π‖_TV ≥ K^t(x*, {x*}) − π(x*).
(iv) Independence of the draws. ∎
(The spectral statement "second eigenvalue 1 − 1/M" of Liu (1996) is **not** used; I have not seen that source.)

### 3.2 Lemma W2
Under BO adding l changes t_{S°} and t_T by the same δQ̄, with δ := (t_{T+l} − t_T)/Q̄ (WS3(a)). By WS3(b),
d = ν[g(x̄) − Σ_c g(x_c)], so d(S°+l) − d(S°) = ν[g(x̄+δ) − g(x̄)] − ν[g(x_T+δ) − g(x_T)]. The identity
g(a+δ) − g(a) = g(δ/(1−a)) gives LR = ν g(δ/(1−x̄)) − ν g(δ/(1−x_T)). Also δ/(1−x̄) = y (because 1 − x̄ = (Q̄ − t_{S°})/Q̄),
and δ/(1−x_T) = (1−κ)y. y < 1 because x_{S°+l} < 1 (Lemma 0). G = ν g(y) follows from Lemma 0 and D_{S°+l}/D_{S°} = D_{T+l}/D_T
(WS3(a)). Bounds: g is convex with g(0) = 0, so g((1−κ)y) ≤ (1−κ)g(y), giving LR ≥ κνg(y). The mean value theorem gives
g(y) − g((1−κ)y) ≤ κy·g′(y) = κy/(1−y) ≤ κg(y)/(1−y) (since g(y) ≥ y). The statistical reading is §3.6 (S2)–(S3) with
T = ∅: κ = x̄ = s. ∎

### 3.3 Prop L
(i) ℓ(φ) = Λ(φ) − φd(S°) + log(Z̄₀/γ₀(S°)) with Λ convex ([PF] Lemma Λ), and ℓ ≥ 0 because q_φ(S°) ≤ 1.
(ii) [PF] WS1(a) at S = S° says 1 + χ²(q_v‖q_u) = q_v(S°)²/(q_u(S°)q_w(S°)); take logs. The restricted bridge q^V is the
same exponential family with γ₀1_V, and T13(iii) (W = V) gives ρ_V = 1/(1 + χ²(q^V_v‖q^V_u)).
(iii) [PF] WS1(e): log q_φ(S°) is concave, so on [0, 1] it is ≥ min of the endpoint values. Then use (ii) with ℓ(v) ≥ 0
and ℓ(u) ≥ 0.
(iv) (ii) at (u, v) = (0, 1) gives log(1+χ²) = ℓ(0) + ℓ(2) − 2ℓ(1). Here 0 ≤ ℓ(0) ≤ ℓ* and 0 ≤ ℓ(1) ≤ ℓ*. ∎

### 3.4 Prop G
*Well-defined, and the accept side.* Let u ∈ [0, 1) and v ∈ (u, 1] with w = 2v − u ≤ 1 + g₋. If w ≤ 1, then
w ≥ v > 0 and ℓ(w) ≤ ℓ* < c − ℓ* (Prop L(iii)). If w ∈ [1, 1 + g₋], convexity gives ℓ(w) ≤ max{ℓ(1), ℓ(1+g₋)} ≤ c − ℓ*,
because the sublevel set is closed and ℓ(1) ≤ ℓ*. Either way log(1+χ²) ≤ ℓ(w) + ℓ(u) ≤ c (Prop L(ii), ℓ(v) ≥ 0), so the
interval is accepted. In particular v̄ := min{1, (u + 1 + g₋)/2} > u is accepted. The accepted set is closed in [v̄, 1]
(ρ_Ω is continuous), so the maximum exists, and φ_t ≥ min{1, (φ_{t−1} + 1 + g₋)/2}. For the gap e_t := 1 − φ_t this
gives e_t ≤ max{0, (e_{t−1} − g₋)/2}. While e_t > 0, e_t + g₋ ≤ (e_{t−1} + g₋)/2, so e_t ≤ (1 + g₋)2^{−t} − g₋, which is
≤ 0 once 2^t ≥ 1 + 1/g₋. Hence T ≤ ⌈log₂(1 + 1/g₋)⌉.
*Reject side.* If g₊ < ∞: ℓ(1) ≤ ℓ* < c + 2ℓ*, and ℓ is convex, so {w ≥ 1 : ℓ(w) ≤ c + 2ℓ*} = [1, 1+g₊]. For
w > 1 + g₊, log(1+χ²) ≥ ℓ(w) − 2ℓ(v) > c (Prop L(iii)), and the interval is rejected. So φ_t ≤ (φ_{t−1} + 1 + g₊)/2,
e_t + g₊ ≥ (e_{t−1} + g₊)/2, e_t ≥ (1 + g₊)2^{−t} − g₊, and e_T = 0 forces 2^T ≥ 1 + 1/g₊.
*Halving.* Acceptance means ℓ(u) + ℓ(w) − 2ℓ(v) ≤ c with ℓ(w) ≥ 0. ∎
*Remark.* The method bisects only 60 times and appends the largest *tested* passing point. That point is within
2^{−60} of the maximum, which perturbs the recursion by 2^{−60} per stage (negligible). The method also uses ρ_V on
pilot temperatures, not ρ_Ω. By Prop L(ii), ρ_V = ρ_Ω exactly when ℓ_V = ℓ up to an affine function on the evaluated
points, which COVER(V) gives up to its ε_C (T13(ii)–(iii)). Closing the gap between the ideal and the method's grid is
**OPEN** (a pilot-sampling statement).

### 3.5 Lemma SEP
Under ORTH, H_S = n²I and G_S + I = nI on S, so D_S = n^{|S|} and t_S = Σ_{j∈S} t_j. So for every U ⊆ [p],
log BF(U) = −(|U|/2) log n + ν g(X_U) with X_U := Σ_{j∈U} x_j < 1 (Lemma 0), and r_b(U) = BF(U). Since
γ_w = ϖ BF^w ∏_b r_b^{1−w},
 log γ_w(S) = log ϖ(S) − (|S|/2) log n + wν g(X_S) + (1−w)ν Σ_b g(X_{S_b}).
Write S = (S₀ ∖ M) ∪ E with M ⊆ S₀, E ⊆ N, m = |M|, e = |E|. Put a := s − X_M, and per block a_b := X_{S₀∩C_b} − X_{M∩C_b},
e_b := X_{E∩C_b}. Facts: (F1) g′ ≥ 1, g′ is increasing, and g(z+h) − g(z) = g(h/(1−z)). (F2) Σ_b[g(X_{S₀∩C_b}) − g(a_b)] ∈
[X_M, g(s) − g(a)]. The left end uses g′ ≥ 1. For the right end, list the blocks as 1, …, J and let M_{>b} := Σ_{c>b} X_{M∩C_c}.
Then X_{S₀∩C_b} ≤ s − M_{>b}, because the other blocks hold at least their own deletions. Convexity moves each
increment over [a_b, X_{S₀∩C_b}] (length X_{M∩C_b}) to the right, onto [s − M_{>b} − X_{M∩C_b}, s − M_{>b}], and these
intervals tile [a, s]. (F3) For 0 ≤ z ≤ s and 0 ≤ h ≤ X_N: h ≤ g(z+h) − g(z) ≤ h/(1−z−h) ≤ h/((1−s)(1−ū)), since
1 − z − h ≥ 1 − s − X_N = (1−s)(1−ū) > 0.
*Exponent.* Δ(S) := log γ_w(S)/γ_w(S₀) = log[ϖ(S)/ϖ(S₀)] + ((m−e)/2) log n + Φ(S), with
Φ = wν[g(a + X_E) − g(s)] + (1−w)ν Σ_b[g(a_b + e_b) − g(X_{S₀∩C_b})].
If w ∈ [1, 2]: write the block part as (w−1)ν{Σ_b[g(X_{S₀∩C_b}) − g(a_b)] − Σ_b[g(a_b+e_b) − g(a_b)]} ≤ (w−1)ν{g(s) − g(a) − X_E}
(F2, F3), and wν[g(a+X_E) − g(s)] = wν[g(a+X_E) − g(a)] − wν[g(s) − g(a)]. So
Φ ≤ wν[g(a+X_E) − g(a)] − ν[g(s) − g(a)] − (w−1)νX_E ≤ β(w)νX_E − νX_M (F3 with z = a, F2).
If w ∈ [0, 1]: by F3 and F2 the block part is ≤ (1−w)ν{X_E/((1−s)(1−ū)) − X_M}, and wν[g(a+X_E) − g(s)] ≤
wν{X_E/((1−s)(1−ū)) − X_M}. So again Φ ≤ β(w)νX_E − νX_M.
*Prior.* ϖ(S)/ϖ(S₀) = w(s₀−m+e)/w(s₀) = [C(2p−1, s₀)/C(2p−1, s₀−m)]·[C(2p−1, s₀−m)/C(2p−1, s₀−m+e)]. The first factor is
∏_{i=1}^m (2p−1−s₀+i)/(s₀−m+i) ≤ (2p)^m. The second is ∏_{i=0}^{e−1}(s₀−m+i+1)/(2p−1−s₀+m−i) ≤ ∏_{i<e}(s₀+i+1)/p =
(s₀+e)!/(s₀! p^e), because e ≤ p − s₀ makes every denominator ≥ 2p − s₀ − e ≥ p.
*Sum.* Since Ω ⊆ 2^{[p]}, 1/q_w(S₀) = Σ_Ω e^{Δ} ≤ Σ_{M⊆S₀} ∏_{j∈M}(2p√n e^{−νx_j}) × Σ_{e≥0} [(s₀+e)!/s₀!] e_e(c/p),
where e_e is the elementary symmetric polynomial. e_e(c/p) ≤ (Σ_j c_j/p)^e/e! = q^e/e!, so the inner sum is
≤ Σ_e C(s₀+e, e)q^e = (1−q)^{−(s₀+1)}, and the outer sum is ∏_{j∈S₀}(1 + 2p√n e^{−νx_j}). ∎
*SEP′.* Keep the inner sum exact. Write (s₀+e)! = ∫₀^∞ t^{s₀+e}e^{−t}dt and interchange (Tonelli):
Σ_e [(s₀+e)!/s₀!]e_e(c/p) = (1/s₀!)∫ t^{s₀}e^{−t}Σ_e t^e e_e(c/p) dt = (1/s₀!)∫ t^{s₀}e^{−t}∏_{j∈N}(1 + tc_j/p) dt. ∎

### 3.6 Theorem W
**(S1) Exact ORTH representation.** Z_j := x_jᵀε/(σ*√(n−1)), j ∈ [p], are iid N(0,1), because the x_j/√(n−1) are
orthonormal. x_jᵀY = (n−1)θ*_j + σ*√(n−1)Z_j (θ*_j = 0 off S₀), and z_j = x_jᵀY/s_y.
(n−1)s_y² = Σ_j (x_jᵀY)²/(n−1) + σ*²χ²_{n−1−p} (an independent residual term), so
s_y²Q̄(1 − s) = 2b₀s_y² + σ*²W_n + Σ_{j∈S₀}(x_jᵀY)²/(n(n−1)) with W_n := Σ_{j∈N}Z_j² + χ²_{n−1−p} ~ χ²_{n−1−s₀}.
**(S2)** Hence, with ζ_n := 2ν(n−1)/[n(W_n + O_P(1))] − 1 = O_P(n^{−1/2}) *not depending on j*: for every null j,
νx_j/(1−s) = (Z_j²/2)(1+ζ_n). Also s = r + O_P(n^{−1/2}) (s_y² = ‖θ*‖² + σ*² + O_P(n^{−1/2}), since ‖μ‖² = (n−1)‖θ*‖²),
ū = (1+ζ_n)χ²_{p−s₀}/(n+0.02) = O_P(p/n), and for j ∈ S₀, νx_j ≥ (n/2)θ*_j²/(‖θ*‖²+σ*²)·(1 − o_P(1)).
**(S3)** max_{j∈N} Z_j² ≤ 2 log m w.p. → 1 (m := |N|; union bound with P(Z² > τ) ≤ √(2/(πτ))e^{−τ/2}). And
max_{j∈N₀} Z_j² = 2 log m₀ − log log m₀ + O_P(1) with m₀ := |N₀| ≥ p/2 (Gumbel limit, as in [PF] WS6(d)).
**(HT) Heavy-tail lemma (no infinite expectations).** E[e^{Z²/2}1{Z² ≤ τ}] = 2∫₀^{√τ}(2π)^{−1/2}dz = √(2τ/π), so by
Markov, Σ_{j∈N} e^{Z_j²/2}1{Z_j² ≤ 2 log m} = O_P(m√log m). On {max_N Z² ≤ 2 log m}, for *every* a ≥ 1 simultaneously,
Σ_N e^{aZ_j²/2} ≤ m^{a−1}Σ_N e^{Z_j²/2} = m^a·O_P(√log m).
**(a), (b).** By (S2), β(w)νx_j = a_n(w)Z_j²/2 with a_n(w) = (1+ζ_n)[w/(1−ū) − (w−1)₊(1−s)]. For w ≤ 1 the bracket is
1/(1−ū), so a_n(w) = 1 + (w−1)₊r + η_n(w) with sup_{w∈[0,2]}|η_n(w)| ≤ C(|ζ_n| + |s − r| + ū) = O_P(n^{−1/2} + p/n). By (HT)
with a = a(w) + |η_n| ≥ 1: q(w) ≤ p^{−1}n^{−1/2}m^{(w−1)₊r + |η_n|}·m·O_P(√log m). Here m^{|η_n|} = exp(O_P((n^{−1/2} + p/n)log p))
= 1 + o_P(1), because p log p = o(n). This proves (b) with one O_P(1) variable V_n for all w. The truth term of SEP is
Σ_{S₀} log(1 + 2p√n e^{−νx_j}) ≤ 2p√n Σ_{S₀}e^{−νx_j} = O_P(p√n e^{−c₀n}) by (S2). At w ∈ {0, 1}, ρ_n = n^{−1/2}, so
ℓ(0), ℓ(1) ≤ O_P(√(log p/n)): this is (a).
**(c).** For l ∈ N₀ (truth-free block, so T = ∅ in its block), the exact single-term ratio is
log[γ_w(S₀+l)/γ_w(S₀)] = log[(s₀+1)/(2p−1−s₀)] − ½ log n + wν g(x_l/(1−s)) − (w−1)ν g(x_l). Using g(z) ≥ z and
g(x_l) ≤ x_l/(1−x_l): ≥ log[(s₀+1)/(2p)] − ½ log n + (Z_l²/2)(1+ζ_n)[w − (w−1)(1−s)/(1−x_l)]. The bracket is
≥ 1 + (w−1)s − 2x_l ≥ a(w) − |η′_n| with η′_n = O_P(n^{−1/2} + log p/n) uniform in w and l (max x_l = O_P(log p/n) by
(S3)). Take l := argmax_{N₀} Z². By (S3), (a(w)/2)Z_l² ≥ a(w) log m₀ − (a(w)/2) log log m₀ − O_P(1), and
|η′_n|Z_l² = o_P(1). With m₀ ≥ p/2, O(w) ≥ max_l[ratio] ≥ ρ_n(w)(log p)^{−a(w)/2}e^{−U_n}. (This is [PF] WS6(d), made uniform in w.)
**(d).** By (b) at w = 2, q(2) ≤ V_n p^r√(log p)/√n = o(1). Then ℓ(2) ≤ O_P(p√n e^{−c₀n}) + 2(s₀+1)q(2) ≤ p^{r+ε/2}/√n w.p. → 1. With ℓ(0) = O_P(√(log p/n)) = o(p^{r+ε/2}/√n):
χ² = π(S₀)²e^{ℓ(2)}/π₀(S₀) − 1 ≤ e^{ℓ(2)+ℓ(0)} − 1 ≤ 2(ℓ(2) + ℓ(0)) ≤ p^{r+ε}/√n.
Lower: χ² ≥ π(S₀)²(1 + O(2)) − 1 ≥ O(2) − 2(1 − π(S₀))(1 + O(2)), with 1 − π(S₀) ≤ ℓ(1) = O_P(√(log p/n)), and by (c)
O(2) ≥ p^r n^{−1/2}(log p)^{−(1+r)/2}e^{−U_n}, which is ≫ √(log p/n). So χ² ≥ O(2)/2 ≥ p^{r−ε}/√n.
**(e).** Let m₀ = |N₀| ≥ p/2, let k ≥ 1 with s₀ + k ≤ K, and let E_k be the k nulls of N₀ with the largest Z². Exactly,
log[γ₂(S₀∪E_k)/γ₂(S₀)] = log[ϖ(S₀∪E_k)/ϖ(S₀)] − (k/2) log n + 2ν g(X_{E}/(1−s)) − ν Σ_b g(X_{E∩C_b})
(truth-free blocks). Use ϖ-ratio = ∏_{i<k}(s₀+i+1)/(2p−1−s₀−i) ≥ k!/(2p)^k, g(z) ≥ z, and Σ_b g(X_{E∩C_b}) ≤ X_E/(1−X_E).
By (S2), νx_j[2/(1−s) − 1/(1−X_E)] = (Z_j²/2)(1+ζ_n)[2 − (1−s)/(1−X_E)] ≥ (Z_j²/2)(1 + r − |η_k|), with
|η_k| ≤ C(|ζ_n| + |s−r| + X_E) and X_E ≤ k·max_N x_j = O_P(k log p/n). Sum over E_k: Σ_{j∈E_k}Z_j² ≥ k Z²_{(k)}.
*Order statistic.* Let τ_k solve m₀P(Z² ≥ τ_k) = 2k. Chernoff gives P(Z²_{(k)} < τ_k) = P(Bin(m₀, 2k/m₀) ≤ k−1) ≤ e^{−k/4}.
Since τ_k ≤ 2 log m₀ and P(Z² ≥ τ) ≥ (2π)^{−1/2}τ^{−1/2}e^{−τ/2} for τ ≥ 2, we get τ_k/2 ≥ log(m₀/(2k)) − ½ log(4π log m₀).
Combining with Stirling, log k! ≥ k log(k/e), on {Z²_{(k)} ≥ τ_k}:
log[γ₂(S₀∪E_k)/γ₂(S₀)] ≥ k[r log p − ½ log n − ((1+r)/2) log log p − r log k − C₁ − C|η_k| log p].
Take k_n := ⌊e^{(L_n − C₁ − 1)/r}⌋ → ∞. Then k_n ≤ p n^{−1/(2r)} ≤ n^{1−1/(2r)} ≤ √n (because r < 1 and p ≤ n), so
|η_{k_n}| log p = O_P(n^{−1/2}log p + k_n log² p/n) = o_P(1), and s₀ + k_n ≤ K. The bracket is ≥ 1 − o_P(1), so
ℓ(2) ≥ log O(2) ≥ k_n(1 − o_P(1)). Finally log(1+χ²) ≥ ℓ(2) − 2ℓ* (Prop L(iv)). ∎
**(g).** Lemma SEP′ at w = 2, with y_j := c_j(2)/p = n^{−1/2}p^{−1}e^{a_nZ_j²/2}, a_n := a_n(2) = 1 + r + η_n (proof of (b)).
*Order statistics.* With τ_i := 2 log(m/i) + 4 log log m, P(∃i: Z²_{(i)} > τ_i) ≤ Σ_i C(m,i)P(Z² > τ_i)^i ≤
Σ_i (e/(log m)²)^i → 0, because P(Z² > τ) ≤ e^{−τ/2} = (i/m)(log m)^{−2}. On this event,
y_{(i)} ≤ ρ″ i^{−a_n} with ρ″ := p^{a_n−1}(log p)^{2a_n}/√n.
*Sum.* x ↦ log(1 + x u^{−a}) is decreasing in u, so Σ_{i≥1} log(1 + ρ″t i^{−a}) ≤ ∫₀^∞ log(1 + ρ″t u^{−a})du = (ρ″t)^{1/a}C_a,
with C_a := ∫₀^∞ log(1 + v^{−a})dv = a∫₀^∞ dv/(1 + v^a) = π/sin(π/a) (integration by parts; a > 1).
*Integral.* −t + C_a(ρ″t)^{1/a} ≤ −t/2 + f*, with f* := max_t[C_a(ρ″t)^{1/a} − t/2] = ((a−1)/2)(2C_a/a)^{a/(a−1)}ρ″^{1/(a−1)}.
So (1/s₀!)∫t^{s₀}e^{−t}∏(1 + ty_j)dt ≤ e^{f*}(1/s₀!)∫t^{s₀}e^{−t/2}dt = 2^{s₀+1}e^{f*}.
*Rates.* a_n − 1 = r + η_n, with η_n log n = o_P(1) (in the divergent regime log p ≍ log n). So
ρ″^{1/(a_n−1)} = p n^{−1/(2r)}(log p)^{2(1+r)/r}(1 + o_P(1)) and C_{a_n} → C_{1+r}, which gives the display.
With e^{L_n/r} = p n^{−1/(2r)}(log p)^{−(1+r)/(2r)}, the ratio of the two bounds is (log p)^{5(1+r)/(2r)}.
Finally log(1+χ²) ≤ ℓ(2) + ℓ* (Prop L(iv)). ∎
**(f).** TV(π, π₀) ≤ max{1 − π₀(S₀), 1 − π(S₀)} ≤ ℓ* ([PF] WS1(d)). For KL, take θ = 1/log p in [PF] WS6(c):
KL(π‖π₀) ≤ ℓ(0) + (π(S₀)/θ)·O(1+θ), and by (b) O(1+θ) ≤ e^{ℓ(1+θ)} − 1 = O_P(p^{r/log p}√(log p)/√n) = O_P(√(log p/n)). ∎

### 3.7 Theorem W′
Apply Prop G with S° = S₀. By Theorem W(a), ℓ* = o_P(1), so 2ℓ* < c w.p. → 1.
*g₋.* If V_nρ_n(1+g)√log p ≤ c/(8(s₀+1)), then by W(b) ℓ(1+g) ≤ o_P(1) + 2(s₀+1)·c/(8(s₀+1)) ≤ c − ℓ*, w.p. → 1. The left
condition reads g ≤ G_n − δ₋ with δ₋ := [log(8(s₀+1)V_n/c) + ½ log log p]/(r log p) = O_P(log log p/log p) (valid while
1 + g ≤ 2). Hence g₋ ≥ min{1, G_n − δ₋}.
*g₊.* By W(c), ℓ(1+g) ≥ log(1 + ρ_n(1+g)(log p)^{−(1+r)/2}e^{−U_n}) > c + 2ℓ* as soon as
gr log p ≥ ½ log n + ((1+r)/2) log log p + U_n + log(1/(e^{c+2ℓ*} − 1)). That is, as soon as g ≥ G_n + δ₊ with
δ₊ = O_P(log log p/log p), if G_n + δ₊ ≤ 1. Convexity (Prop G) then gives g₊ ≤ G_n + δ₊.
*Count.* Prop G gives ⌈log₂(1 + 1/(G_n + δ₊))⌉ ≤ T ≤ ⌈log₂(1 + 1/min{1, G_n − δ₋})⌉. Because p ≤ n − 1, G_n ≥ 1/(2r) > ½,
so for large n, min{1, G_n − δ₋} > 1/3 and T ≤ 2. If 2Ar < 1, then G_n → 1/(2Ar) > 1 and T = 1. If 2Ar > 1, then
G_n + δ₊ → 1/(2Ar) < 1 and T ≥ 2. ∎

## 4. Evidence (scripts under `scripts/`, outputs under `results/`, seed 20261102)

**Exact enumeration, p ≤ 16** (`check_W.py` → `results/check_W.txt`; reuses `wstab_core.py`, which earlier passed
brute-force identity checks in `results/check_identities.txt`):
- Prop L(ii) identity: max |log(1+χ²) − [ℓ(u) + ℓ(w) − 2ℓ(v)]| = 3.6·10⁻¹² over 1400 random (u, v) in 7 ORTH designs;
  the sandwich (iii) held in all 1400.
- Lemma W2 sandwich κG ≤ LR ≤ κG/(1−y): held in all 246 comparisons (BO with *correlated* blocks, n = 150–1600, four
  reference models each).
- Lemma SEP: ℓ(w) − bound ≤ −0.016 in all 147 (design, w ∈ [0, 2]) cases where it applies (it is a valid upper bound).
- Prop G: in the one design with 2ℓ* < c (p = 16, n = 20000), T_ideal = 1 ∈ [1, 1]. In the others ℓ* is too large at
  these small sizes, and the hypothesis fails, as it should.
- Multi-extra lower bound ≤ ℓ(2) in all 7 designs.

**ORTH at astronomical (n, p)** (`orth_large_p.py` → `results/orth_large_p.txt`). This is exact in the sufficient
statistics. The top 20 000 null Z²'s are drawn as order statistics (exponential spacings); for m ≤ 2·10⁵ all nulls are
drawn directly. s₀ = 2, r = 0.9. "LB" is the exact log(1 + max_k γ₂(S₀∪E_k)/γ₂(S₀)), a rigorous lower bound on ℓ(2).
"SEP" is Lemma SEP's upper bound (∞ when q(2) ≥ 1). "FD" is [FD] W(c).

| log₁₀n | A | r log p − ½ log n | FD = W(c) | LB ℓ(2) | k* | SEP ℓ(2) |
|---|---|---|---|---|---|---|
| 10 | 0.40 | −3.22 | 0 | 0.0008 | 1 | 0.0051 |
| 14 | 0.40 | −4.51 | 0 | 0.00024 | 1 | 0.0010 |
| 14 | 0.50 | −1.61 | 0 | 0.0098 | 1 | 0.041 |
| 16 | 0.70 | 4.79 | 4.79 | 21.1 | 9 | ∞ |
| 12 | 0.85 | 7.32 | 7.32 | 29.7 | 26 | ∞ |
| 16 | 0.85 | 9.76 | 9.76 | 270 | 300 | ∞ |
| 12 | 0.95 | 9.81 | 9.81 | 343 | 359 | ∞ |
| 16 | 0.95 | 13.08 | 13.08 | 8 770 | 9 782 | ∞ |

(The full table has 35 rows. LB ≤ SEP in every row where SEP is finite. The log-ratios use g(X_E/(1−s)), not g(s+X_E) − g(s): the difference form loses about 2 nats to cancellation at n = 10¹⁶.) On the convergent side (2Ar < 1), LB ≤ ℓ(2) ≤ SEP, both small and shrinking: Theorem W(d).
On the divergent side the optimal number of extras k* grows polynomially, and LB exceeds W(c) by orders of magnitude:
Theorem W(e) and the counterexample. Single rows fluctuate (e.g. A = 0.5, n = 10¹⁰, 10¹² give LB ≈ 2–3). These are the
O_P(1) Gumbel fluctuations of max Z² near the boundary 2Ar ≈ 1, and the polylog factor (log p)^{−(1+r)/2} delays
divergence at A = 0.7.

**Divergent side, both bounds** (same script, column `SEPint` = Lemma SEP′). Wherever it is finite, SEP′ ≥ LB:

| log₁₀n | A | LB ℓ(2) | SEP′ ℓ(2) | predicted growth p·n^{−1/(2r)} |
|---|---|---|---|---|
| 12 | 0.85 | 29.7 | 245 | n^{0.294} |
| 14 | 0.85 | 74.2 | 614 | (×3.9 per 10² in n) |
| 16 | 0.85 | 270 | 1891 | |

From 10¹² to 10¹⁶ the two bounds grow ×9.1 and ×7.7, against ×15 predicted before polylog corrections. They differ by
a factor of about 7–8, which is the polylog gap. At A = 0.95, SEP′ is ∞, because ū = Σ_N x_j/(1−s) = 0.16–0.63 is not small
at these n: the theorem's p log p = o(n) is not yet in force there.

**W′ at large (n, p)** (`orth_grid.py` → `results/orth_grid.txt`; r = 0.9, s₀ = 2). Using LB(w) ≤ ℓ(w) ≤ SEP(w) on a
grid of w ∈ [1, 2], Prop G gives rigorous bounds g₋ ≥ …, g₊ ≤ … and hence an interval for T_ideal (up to the
conditional-expectation tail in SEP). It is valid when 2ℓ*_ub < c.
- 2Ar < 1 (A = 0.3; A = 0.45 at n = 10⁸, 10¹²): T_ideal = 1 exactly, as predicted.
- 2Ar > 1 (A = 0.65, 0.8, all n): T_ideal = 2 exactly, as predicted. At A = 0.95, n = 10¹², 10¹⁶ the interval is
  [2, 4] and [2, 3], which contains 2.
- **One finite-n deviation:** A = 0.45, n = 10¹⁶ (2Ar = 0.81) gives T_ideal = 2, not 1. Here ρ_n(2) = n^{−0.095} ≈ 0.03,
  and an O_P(1) Gumbel fluctuation of max Z² pushes ℓ(2) above c. This is within the stated error
  δ_n = O_P(log log p/log p) (≈ 0.17 here, against G_n − g₊ ≈ 0.25), so it does not contradict the asymptotic statement.
  It does mean that near 2Ar = 1 the asymptotic count is reached only very slowly.

## 5. What fails and why
- **[FD] W(c) / W(b) on the divergent side** (COUNTEREXAMPLE above). The [FD] skeleton bounds the multi-extra layers by
  a geometric series in q⁽²⁾. That is right when q⁽²⁾ < 1, but when q⁽²⁾ > 1 the series diverges and the true sum is
  max_k k!·e_k(c)/(2p√n)^k ≈ exp(Θ(k*)) with k* ≍ e^{L_n/r}. The single-null extreme value captures only the first layer.
- **Expectation route.** E e^{(1+r)Z²/2} = ∞, so no moment bound on Σ_l c_l exists. (HT) replaces it by truncation at
  2 log m plus a monotonicity trick that is uniform in the exponent a ≥ 1.
- **Uniform perturbation in the cross-block Gram** ([PF] WS4) controls |d − d_σ| only when ε_S = o(1/n). That is too
  strong for designs with sample correlations of order n^{−1/2}. So W3 (the cross-block term) stays at [FD]'s PROOF
  SKETCH level, and Theorem W is stated for ORTH.
- **p ≍ n under ORTH.** Lemma SEP needs ū < 1 and the statistics need ū log p → 0, i.e. p log p = o(n). For p ≍ n,
  large models (|E| comparable to n) need a separate dimension control for the doubled law q₂. This is the analogue
  of T02 for ϖ·BF²/∏r_b, and it is **OPEN**.
- **Expressing W in [FD]'s κ_b = Δ_T/v_T.** That quantity is population-level. The exact finite-n object is the
  realised κ = (x̄ − x_T)/(1 − x_T) of Lemma W2, which matches it to O_P(n^{−1/2}).

## 6. Needs escalation
1. **Lemma SEP and Theorem W(a)–(f)**: an independent line-by-line check. The cruxes are the convex-telescoping step
   (F2) and the uniformity in w of (HT) + (S2), which W′ needs.
2. **Theorem W(e), (g)**: the order-statistic constants of both sides, the Γ-integral form (SEP′), and the
   integral ∫₀^∞ log(1 + v^{−a})dv = π/sin(π/a).
3. **General BO (correlated blocks, B ≤ 16)**: replace per-variable factors by per-block factors
   c_b(U) = n^{−|U|/2}·(table odds)^{β}… and run T22(i)'s aggregation with squared odds ([FD] skeleton step 5). The
   deterministic part looks routine; the statistical part needs EXP′ (candidate). **PROOF SKETCH.**
4. **The method's grid vs the ideal grid** (COVER at the w_t, pilot temperatures): **OPEN** (stated in Prop G remark).

## 7. Outside scope
- In ℓ-language the masked regime is ℓ(0) = −log π₀(S₀) → ∞. Prop L(iv) gives log(1+χ²(π‖π₀)) ≥ ℓ(0) − 2ℓ(1)
  (cf. T27(i)). Prop G's halving gives ≥ log₂(ℓ(0)/c)-type stage counts ([PF] WS7(d)), and transport (moves), not
  reweighting, is what discovers S₀ ([PF] WS7(c)). This connects W to T38(b) delivery, as [FD] says; not pursued.
- The divergent regime's dominant models are S₀ plus k* ≍ e^{L_n/r} extras. These are exactly the states the
  independence move proposes rarely. If one-step importance sampling were ever used as a diagnostic (e.g. the pilot's
  first temperature), its collapse would be driven by these supersets, not by a missing truth. Worth one sentence in
  the paper's §4.4 discussion.

## 8. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| W0 | Prop W0 (i)–(iv), self-contained Doeblin form | 0.99 | done | none | no |
| W1 | Lemma W1 (= WS3) | 0.99 | done | none | no |
| W2 | exact κG ≤ LR ≤ κG/(1−y); ORTH reading | 0.98 | done | none (EXP′ only for general-BO reading) | no |
| Prop L / Prop G | ℓ-form of T13; ideal-grid sandwich | 0.98 | done | none | no |
| Lemma SEP | separable domination under ORTH | 0.95 | done (needs check) | (F2) telescoping | no |
| Theorem W(a)–(d), (f), ORTH, p log p = o(n) | two-sided rate p^{r±ε}/√n on the convergent side; KL, TV → 0 | 0.92 | done (needs check) | (HT) uniformity, (S2) | no |
| Theorem W(e) + counterexample to [FD] W(c) | log(1+χ²) ≥ e^{(L_n−C)/r} | 0.93 | done (needs check) | order statistics; k_n ≤ √n | no |
| W(g) matching upper bound | log(1+χ²) ≤ C e^{L_n/r}(log p)^{5(1+r)/(2r)} | 0.9 | done (needs check) | SEP′ + order statistics | no |
| W′ ORTH | T_ideal ∈ {1,2}; = 1 iff 2Ar < 1 | 0.9 | done (needs check) | uniform-in-w bounds near w = 1 + G_n | no |
| W′ method grid | same count for the V-restricted pilot grid | 0.6 | 0.3 | COVER at w_t; pilot ESS vs ρ_Ω | no |
| Theorem W, general BO + SE-blk | same dichotomy with r replaced by the realised dilution fraction | 0.85 | 0.6 | per-block SEP; EXP′ | no |
| Theorem W, p ≍ n | same threshold | 0.8 | 0.4 | dimension control for q₂ (T02 analogue) | no |

Agent and call counts: this laptop run used no helper agents; all mathematics and scripts are by this O-WSTAB instance.
