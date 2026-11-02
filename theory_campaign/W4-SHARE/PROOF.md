# W4-SHARE — PROOF.md (delivery to the terminal rounds, route (b2))

Notation of `Docs/Theory/theorems/00_COMMON.md`, W1-T38E `PROOF.md` and W1-T24G. Every result is a **candidate**: not reviewed, not adopted. Status words: PROVED, PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN.

## 0. Setting and new notation

One island of the final run, conditional on a successful calibration 𝓒 (grid 0 = φ₀ < … < φ_T = 1, Δ_t = φ_t − φ_{t−1}, N = N_e). Standing assumptions EX-A, EX-S, CAL (00_COMMON §3).

- X_t = (X_t¹,…,X_t^N): particle states at the **end of stage t** (after the stage-t resampling and move round); X_0 are the iid π₀ initial draws. F_t := σ(𝓒, data, X_0,…,X_t).
- Stage t: weights G_t(x) = e^{Δ_t d(x)} evaluated at X_{t−1}; multinomial resampling (ancestors iid with probabilities ∝ G_t(X_{t−1}^i)); then one round K_t := K_{φ_t} per particle, with fresh randomness, independently across particles (M §§6.5, 6.6, 6.8; engine `run_island_s`, `resample`, `population_round`).
- K_t also denotes the **one-round Markov kernel** on Ω (the random order averaged out): (K_t h)(x) = E_x[h(state after one round at φ_t)].
- W ⊆ Ω: the delivery target (𝓒-measurable). n_t(W) := #{i : X_t^i ∈ W}.
- **Potentials.** h_0,…,h_T : Ω → [0,1], 𝓒-measurable, with h_T ≤ 1_W. H_t := Σ_i h_t(X_t^i). π₀(h) := Σ_S π₀(S)h(S).
- **Population and h-subpopulation fitness at stage t** (computed from X_{t−1}, hence F_{t−1}-measurable):
  Ḡ_t := N⁻¹Σ_i G_t(X_{t−1}^i), Ḡ_t^h := Σ_i G_t(X_{t−1}^i)h_{t−1}(X_{t−1}^i) / H_{t−1} (if H_{t−1} > 0),
  r_t := Ḡ_t^h/Ḡ_t if H_{t−1} > 0, and r_t := 1 if H_{t−1} = 0.
- **Envelope process.** P_0 := 1, P_t := ∏_{s=1}^t r_s(1 − η_s), with η_s from (TRACK) below.

**Interpretation of P_t.** On {H_s > 0 for all s < t}, Σ_{s≤t} log Ḡ_s = log(Ẑ_t/(m(∅)Z̄₀)), where Ẑ_t is the island's evidence product through stage t (M §6.12). Define the **h-subpopulation evidence** Ẑ_t^h := m(∅)Z̄₀∏_{s≤t}Ḡ_s^h. Then
  P_t = (Ẑ_t^h / Ẑ_t) · ∏_{s≤t}(1 − η_s).
So P_t measures how far the h-weighted subpopulation's own evidence product has fallen behind the whole island's. Compare D1/T15, which needs Ẑ_r/Z itself not to be small.

---

## 1. Theorem D4 (space-time potential delivery bound) — PROVED

**Hypothesis (TRACK).** There are η_1,…,η_T ∈ [0,1) with
  (K_t h_t)(x) ≥ (1 − η_t) h_{t−1}(x)  for every x ∈ Ω and t = 1,…,T.

**Statement.** Let P̲_1,…,P̲_T > 0 be 𝓒-measurable numbers and τ := min{t ≤ T : P_t < P̲_t} (τ = ∞ if there is none). Define θ_T := +∞ and θ_{t−1} := P̲_t(1 − e^{−θ_t/P̲_t}) for t = T,…,1. Then

  P(n_T(W) = 0 | 𝓒) ≤ P(τ ≤ T | 𝓒) + (1 − π₀(h_0)(1 − e^{−θ_0}))^N
                   ≤ P(τ ≤ T | 𝓒) + exp{−N π₀(h_0)(1 − e^{−θ_0})},

with 1/θ_0 ≤ Σ_{t=1}^T 1/P̲_t, and, if t ↦ P̲_t is non-increasing, 1/θ_0 ≤ 1/P̲_T + (e−1)⁻¹ Σ_{t=1}^{T−1} 1/P̲_t ((e−1)⁻¹ ≈ 0.582).

**Proof.**
*Step 1 (one stage).* Fix t and condition on F_{t−1}. The ancestors of the N stage-t particles are iid with law ∝ G_t(X_{t−1}^i), and each resampled particle then makes one round with fresh randomness, independently. Hence the N values h_t(X_t^i) are iid given F_{t−1}, with mean
  m_t := Σ_j G_t(X_{t−1}^j)(K_t h_t)(X_{t−1}^j) / Σ_j G_t(X_{t−1}^j) ≥ (1 − η_t) Σ_j G_t h_{t−1}(X_{t−1}^j)/Σ_j G_t(X_{t−1}^j) = (1 − η_t) r_t H_{t−1}/N =: μ_t,
by (TRACK) (if H_{t−1} = 0, μ_t = 0 and the inequality is trivial). For y ∈ [0,1] and θ ∈ (0, ∞], convexity gives e^{−θy} ≤ 1 − y(1 − e^{−θ}) (for θ = ∞ read e^{−∞·y} = 1{y = 0} ≤ 1 − y). Therefore
  E[e^{−θ h_t(X_t^i)} | F_{t−1}] ≤ 1 − m_t(1 − e^{−θ}) ≤ 1 − μ_t(1 − e^{−θ}),
and by conditional independence
  E[e^{−θ H_t} | F_{t−1}] ≤ (1 − μ_t(1 − e^{−θ}))^N ≤ exp{−(1 − η_t) r_t H_{t−1}(1 − e^{−θ})}.   (1.1)

*Step 2 (normalised count).* Put Y_t := H_t/P_t. P_t > 0 (G > 0, η < 1), and P_t is F_{t−1}-measurable. Since (1 − η_t) r_t H_{t−1} = Y_{t−1}P_{t−1}(1 − η_t)r_t = Y_{t−1}P_t, (1.1) with θ replaced by θ/P_t gives
  E[e^{−θ Y_t} | F_{t−1}] ≤ exp{−Y_{t−1}·P_t(1 − e^{−θ/P_t})}.   (1.2)
The map P ↦ P(1 − e^{−θ/P}) is non-decreasing on (0, ∞) (it equals θ(1 − e^{−v})/v with v = θ/P, and (1 − e^{−v})/v is decreasing in v; for θ = ∞ it equals P). So on {P_t ≥ P̲_t},
  E[e^{−θ_t Y_t} | F_{t−1}] ≤ exp{−Y_{t−1}P̲_t(1 − e^{−θ_t/P̲_t})} = e^{−θ_{t−1}Y_{t−1}}.   (1.3)

*Step 3 (stopped supermartingale).* τ is predictable: {τ > t} = {P_s ≥ P̲_s, s ≤ t} ∈ F_{t−1}. Let M_t := e^{−θ_t Y_t}1{τ > t}. Then E[M_t | F_{t−1}] = 1{τ > t}E[e^{−θ_tY_t} | F_{t−1}] ≤ 1{τ > t}e^{−θ_{t−1}Y_{t−1}} ≤ M_{t−1}. Hence E M_T ≤ E M_0 ≤ E e^{−θ_0 H_0}.
On {n_T(W) = 0} every particle lies outside W, so H_T = 0 (h_T ≤ 1_W) and M_T = 1{τ > T}. Thus P(n_T(W) = 0, τ > T | 𝓒) ≤ E[e^{−θ_0H_0} | 𝓒].

*Step 4 (start).* H_0 is a sum of N iid terms h_0(X_0^i), X_0^i ~ π₀. By the convexity bound, E e^{−θ_0 h_0(X)} ≤ 1 − π₀(h_0)(1 − e^{−θ_0}). So E e^{−θ_0H_0} ≤ (1 − π₀(h_0)(1 − e^{−θ_0}))^N ≤ exp{−Nπ₀(h_0)(1 − e^{−θ_0})}. Adding P(τ ≤ T | 𝓒) proves the first display.

*Step 5 (θ_0).* With u_t := θ_t/P̲_t, 1/θ_{t−1} = 1/θ_t + g(u_t)/P̲_t where g(u) := 1/(1 − e^{−u}) − 1/u. g is increasing on (0, ∞) from ½ to 1 (g(∞) = 1 covers t = T, where 1/θ_T = 0). Hence 1/θ_0 ≤ Σ_t 1/P̲_t. If P̲ is non-increasing, then for t ≤ T − 1, θ_t = P̲_{t+1}(1 − e^{−u_{t+1}}) ≤ P̲_{t+1} ≤ P̲_t, so u_t ≤ 1 and g(u_t) ≤ g(1) = 1/(e−1). ∎

(Checks: `scripts/s0_lemma_checks.py` verifies g's monotonicity and the bound on θ_0 numerically; `s1_toys.py` checks D4 against simulation.)

**Remarks.**
1. *Indicator potentials.* With h_t = 1_{R_t}, R_t ⊆ Ω, (TRACK) reads: from every x ∈ R_{t−1}, one round at φ_t ends in R_t with probability ≥ 1 − η_t. With R_t ≡ W it is D3's EXIT-end. A moving R_t (for instance from the start-reference region to the S₀ region) expresses **within-W tracking of the mode switch**: the kernel must carry the occupied region along as the bridge moves. A non-indicator h expresses *occupancy-weighted* exits (a particle near the boundary of W counts less), which removes the worst-case boundary states that make sup-exit bounds useless (W1-T24G, CE1).
2. *Comparison with D3.* D3 needs Σ_t(ζ_t + η_t) → 0. D4 needs neither SHARE nor Σ_t η_t → 0: the exits enter only through ∏(1 − η_t) inside the exponent, so Σ_t η_t may be as large as log(Nπ₀(h_0)/T) − ω(1). SHARE is replaced by the envelope event {τ > T}.
3. *What D4 does not use.* No evidence lower tail (LT), no bridge-mass statement, no ESS statement about the realised population. Its only random hypothesis is the envelope on P_t = (Ẑ^h_t/Ẑ_t)∏(1−η), a *relative* (subpopulation vs population) evidence statement.

---

## 2. Corollary D5 (fitness oscillation) — PROVED

**Hypotheses.** (TRACK) as in D4. Sets 𝔛_0,…,𝔛_{T−1} ⊆ Ω (𝓒-measurable) and the event E := {X_{t−1}^i ∈ 𝔛_{t−1} for all i and all t = 1,…,T} (confinement). Numbers κ_t ≥ 0 with
  κ_t ≥ sup{d(y) : y ∈ 𝔛_{t−1}, h_{t−1}(y) < 1} − inf{d(x) : x ∈ 𝔛_{t−1}, h_{t−1}(x) > 0}
(empty sup = −∞, empty inf = +∞). Put Γ_t := Σ_{s≤t}Δ_sκ_s and Γ := Γ_T ≤ max_t κ_t.

**Statement.** On E, for every t, with o_{t−1} := N⁻¹Σ_i(1 − h_{t−1}(X_{t−1}^i)),
  r_t ≥ 1/(1 + o_{t−1}(e^{Δ_tκ_t} − 1)) ≥ e^{−Δ_tκ_t}.   (2.1)
Consequently
  P(n_T(W) = 0 | 𝓒) ≤ P(E^c | 𝓒) + exp{−Nπ₀(h_0)(1 − e^{−c})},
  1/c = e^{Γ}/∏_{s≤T}(1−η_s) + (e−1)⁻¹ Σ_{t=1}^{T−1} e^{Γ_t}/∏_{s≤t}(1−η_s) ≤ [1 + (T−1)/(e−1)] e^{Γ}/∏_{s≤T}(1−η_s).

**Proof.** Fix t, assume E and H_{t−1} > 0 (else r_t = 1). Let a := inf over states with h_{t−1} > 0 of d and b := sup over states with h_{t−1} < 1 of d, both within 𝔛_{t−1}. Write G = G_t(X_{t−1}^i), h = h_{t−1}(X_{t−1}^i). Then ΣGh ≥ e^{Δ_t a}Σh and ΣG(1−h) ≤ e^{Δ_t b}Σ(1−h), so
  r_t = NΣGh/(Σh·(ΣGh + ΣG(1−h))) ≥ N/(Σh + e^{Δ_t(b−a)}Σ(1−h)) = 1/(1 − o + o e^{Δ_t(b−a)}),
which gives (2.1) because κ_t ≥ (b − a)⁺ and 1 + o(e^{x} − 1) ≤ e^{x} for o ∈ [0,1], x ≥ 0. Put P̲_t := e^{−Γ_t}∏_{s≤t}(1−η_s), non-increasing and 𝓒-measurable. On E, P_t ≥ P̲_t for all t, so {τ ≤ T} ⊆ E^c, and D4 with its monotone form of θ_0 gives the claim. ∎

**Remarks.**
1. *Grid independence (Proposition G, PROVED).* Γ = Σ_tΔ_tκ_t ≤ max κ for **every** grid, because Σ_tΔ_t = 1. The total selection pressure that an outsider class can exert against W over the whole bridge is fixed by d alone. The grid enters D5 only through T (drift) and through (TRACK) (how many rounds the kernel gets in each φ-window). In particular no condition on the φ-grid alone (ESS-driven or restricted-ESS-driven, T13) can imply SHARE: see §4 and the C1 runs with the method's own grid.
2. *The refined form.* (2.1) also gives P̲_t := exp{−Σ_{s≤t} ε_s(e^{Δ_sκ_s} − 1)}∏(1−η_s) on the event {o_{s−1} ≤ ε_s for all s} ∩ E. Then the loss is ≈ Σ ε_sΔ_sκ_s: an outsider class that is fitter by κ costs only its own (h-weighted) population fraction times κ. This is the form needed when κ is large but the outsiders are rare.
3. *Reading.* Delivery to W is guaranteed (up to P(E^c)) as soon as
  Nπ₀(h_0) ≫ T·e^{Γ}/∏(1 − η_s),
i.e. **Γ + Σ_s η_s ≤ log(Nπ₀(h_0)/T) − ω(1)**. The threshold is logarithmic in N; §3 shows it is sharp up to a factor 2 in log N.

---

## 3. Proposition SH (sharpness of the log N threshold) — PROVED

**Setting.** Two states, Ω′ = {a, o}, W = {a}, no moves (K_t = identity), one stage (T = 1, Δ_1 = 1), κ := d(o) − d(a) > 0, π₀(a) = 1 − π₀(o) ∈ (0,1). Here (TRACK) holds with h ≡ 1_W, η = 0, 𝔛 = Ω′, Γ = κ.

**Statement.**
(i) (D5) P(n_1(W) = 0) ≤ exp{−Nπ₀(a)(1 − e^{−e^{−κ}})} ≤ exp{−Nπ₀(a)e^{−κ}/2} (for κ ≥ 0). It tends to 0 whenever κ ≤ log(Nπ₀(a)) − ω(1).
(ii) (converse) P(n_1(W) = 0) ≥ (1 − N²e^{−κ})·(1 − π₀(a)^N). It tends to 1 whenever κ ≥ 2 log N + ω(1) (and π₀(a)^N → 0).
(iii) Exactly, P(n_1(W) = 0) = E[(1 − n_0/(n_0 + (N − n_0)e^{κ}))^N], n_0 ~ Bin(N, π₀(a)); the transition happens at κ ≈ log(Nπ₀(a)/π₀(o)), which lies between log(Nπ₀(a)) and 2 log N when π₀(o) ≥ 1/N.

**Proof.** (i) is D5 with T = 1 (1/c = e^{κ}), and 1 − e^{−x} ≥ x/2 for x ∈ [0,1]. (ii) Given n_0 < N, ω = n_0/(n_0 + (N − n_0)e^{κ}) ≤ N e^{−κ}, and (1 − ω)^N ≥ 1 − Nω ≥ 1 − N²e^{−κ}. Multiply by P(n_0 < N) = 1 − π₀(a)^N. (iii) is the exact one-stage law. ∎

So no bound of D5's form can tolerate oscillation κ ≥ 2 log N + ω(1); D5 tolerates κ ≤ log(Nπ₀(W)/T) − ω(1). The gap is the outsider's own start mass (log 1/π₀(o) ≤ log N) and the drift (log T). Multi-stage sharpness, with an outsider lineage that must first survive demographic noise, is in §5 (C1 analysis).

---

## 4. Proposition X (gate obstruction) — PROVED

**Statement.** Let U ⊆ Ω be 𝓒-measurable and let a_t ≥ sup_{x ∉ U} P_x(one round at φ_t ends in U), with a_{T+1} = … = a_{T+L+4} ≥ the same bound at φ = 1. Then, for one island,
  P(some particle is in U at the end of some stage or terminal round | 𝓒) ≤ Nπ₀(U) + N Σ_{k=1}^{T+L+4} a_k.
For the four final islands the bound is multiplied by 4. Moreover the probability that S₀ is scored by a move whose proposal lies in U is bounded by the same quantity whenever entering U is necessary to propose S₀ (for example U ∋ S₀ and U ⊇ every Gibbs or swap neighbour of S₀ that cannot be reached otherwise).

**Proof.** Resampling only copies existing states, so a particle can be in U at some time only if an initial draw is in U or some round starts outside U and ends in U. The expected number of initial draws in U is Nπ₀(U). In round k, at most N particles start outside U, and each enters U with conditional probability ≤ a_k (fresh randomness). A union bound over the first entry gives the claim. ∎

**Numerical sharpness (s3).** In the posterior-barrier design PB(n = 16000) the measured gate rate from the occupied state {12} at φ = 1 is ≈ 5·10⁻⁶ per particle-round (6 entries in 1.2·10⁶ particle-rounds; `s3`/diagnostic), so the bound is ≈ 2500 × 38 × 5·10⁻⁶ ≈ 0.48 per island; the observed frequency of islands in which S₀ was scored is 0.51 (100 islands). The union bound is essentially attained.

**Use.** Lemma A (W1-T38E) bounds a_k by endpoint odds for Gibbs gates. If U = the set of repairable states and U is separated from the start region by a posterior-level barrier (every path needs ≥ 2 individually unfavourable flips at every φ), then a_k ≤ (odds of the first unfavourable step) × (number of gate labels), and route (b2) fails with probability ≥ 1 − Nπ₀(U) − N(T+L+4)·max_k a_k. This is the obstruction for **posterior-level masking**. §6 shows that it cannot occur among truth-subsets under R (and among 𝓡_d under SE) — so it is an obstruction outside T03's regime only.

---

## 5. The C1 mechanism quantified — PROOF SKETCH (numerically confirmed)

In C1 (W1-T38E §5.3, reversible kernel of W3-VT38E), A = {a₁, m, a₂}, o isolated, d(o) − d(a₁) = 80, π₀(o) = e^{−10}/Z̄₀ ≈ 4.54·10⁻⁵, uniform grid of T = 1000 stages (Δ = 10⁻³). Until φ ≈ 0.9 the A-particles sit at a₁ (the move a₁ → m costs 120(1 − φ) nats). An o-lineage therefore has per-stage mean offspring ≈ e^{80Δ} = e^{0.08} relative to the A-dominated population: a supercritical branching process with Poisson(≈1.083) offspring, whose survival probability s solves 1 − s = e^{−1.083 s}, s ≈ 0.153. The initial number of o copies is ≈ Poisson(Nπ₀(o)). Once an o-lineage survives the first few stages its relative growth is e^{80φ} ≫ N long before a₂ becomes reachable, so A dies. Prediction:
  P(A extinct) ≈ 1 − exp{−Nπ₀(o)s} = 0.50 (N = 10⁵), 0.9990 (N = 10⁶).
Observed (W1: 0.480, 0.995; W3 reversible: 0.560, 1.000; this run: `s1_toys.out`). In D5's terms: with h = 1_{a₁} on φ ≤ 0.9, Γ ≈ 80·0.9 = 72 ≫ log N, and D5 correctly gives nothing; with o removed, D5 gives delivery (trivially, W = Ω′) while LT still fails in every island (Ẑ/Z ≈ e^{−1800}): **LT is not necessary for delivery; the envelope is.**

---

## 6. Proposition M (no posterior-level barrier near the truth) — deterministic core PROVED; score gain PROOF SKETCH

**(a) Deterministic core (PROVED).** Let θ* be supported on S₀, μ = Xθ*, T ⊆ [p] with T ⊉ S₀, M := S₀ ∖ T ≠ ∅, and suppose λ := λ_min(R_{T∪M}) > 0. For j ∈ M let u_{T,j} be the unit residual of x_j on X_T and δ_{T,j} = u_{T,j}ᵀμ (00_COMMON §2). Then
  max_{j∈M} δ_{T,j}² ≥ (n−1) λ² ‖θ*_M‖₂⁴/‖θ*_M‖₁² ≥ (n−1) λ² min_{j∈S₀}θ*_j².

*Proof.* Let P_T be the projection on col(X_T) and x̃_j = (I − P_T)x_j. Since θ* is supported on S₀ = (S₀ ∩ T) ∪ M and P_T kills col(X_T), r := (I − P_T)μ = Σ_{j∈M}θ*_j x̃_j. Then ‖r‖² = Σ_{j∈M}θ*_j x̃_jᵀr = Σ_jθ*_j‖x̃_j‖δ_{T,j}, because x̃_jᵀr = x_jᵀ(I − P_T)μ = ‖x̃_j‖δ_{T,j}. With ‖x̃_j‖ ≤ ‖x_j‖ = √(n−1): ‖r‖² ≤ √(n−1)‖θ*_M‖₁ max_j|δ_{T,j}|. On the other hand ‖r‖² = (n−1)θ*_Mᵀ(R_{MM} − R_{MT}R_{TT}⁻¹R_{TM})θ*_M ≥ (n−1)λ‖θ*_M‖₂², because the Schur complement of a positive definite matrix has λ_min ≥ λ_min of the matrix (if R_{TT} is singular use the pseudo-inverse; the bound holds for the generalised Schur complement whenever λ > 0, which forces R_{TT} ≻ 0). Combine and use ‖θ*_M‖₁² ≤ |M|‖θ*_M‖₂² and ‖θ*_M‖₂² ≥ |M|min θ*_j². ∎

So: under R (λ_min(R_{S₀}) ≥ φ₀²) every truth-subset T ⊊ S₀ has a missing truth with δ² ≥ (n−1)φ₀⁴θ²_min; under SE the same holds for every T ∈ 𝓡_d with |T ∪ M| ≤ m_n + s₀ (extras and look-alikes included).

**(b) Score gain (PROOF SKETCH).** Using the gain expansion of 00_COMMON (EXP / E_{T,l} quantities: log[BF(T+j)/BF(T)] = −½log(n+1) + (δ_{T,j} + σ*Z_{T,j})²/(2v_T) + R_n), (a) and BM-∞ give, w.p. → 1 (a finite union over the ≤ 2^{s₀}·poly(n) relevant (T, j) pairs, with v_T ≤ σ*² + ‖μ‖²/(n−1) bounded under R):
  min_{T} max_{j∈M(T)} [F(T+j) − F(T)] ≥ c M_n log n − (A + ½)log n − O(√log n) → ∞.
Combined with the start-side bound log κ₀(T, j) ≥ −log(2p) − ½log(n+1) =: −λ_n (W1-T38E E1 applied to a table), Lemma A's identity gives, for φ ≥ φ_n := λ_n/(λ_n + g_n) with g_n the gain above, γ_φ(T+j)/γ_φ(T) ≥ 1 for that j. **Thus under T03's hypotheses the within-𝓡_d path to S₀ is downhill for all φ ≥ φ_n → 0**: there is no posterior-level barrier, Proposition X cannot bite, and the only remaining obstruction to delivery is outsider competition (D5's Γ) plus exits.

---

## 6b. Lemma PD (start mass × fitness = posterior) — PROVED; consequence for C1-type takeover

**Identity.** For every S ∈ Ω, log γ₀(S) + d(S) = log ϖ(S) + Σ_b log r_b(S∩C_b) + log BF(S) − Σ_b log r_b(S∩C_b) = log ϖ(S) + log BF(S) = F(S) − log m(∅) (00_COMMON §2). Hence for an outsider y and an occupied W-state x,
  [log π₀(y) − log π₀(x)] + [d(y) − d(x)] = F(y) − F(x).

**Consequence (PROVED, elementary).** In the pure-selection two-class picture of §3/§5, the outsider y's expected share relative to x after the whole bridge is (π₀(y)/π₀(x))e^{d(y)−d(x)} = e^{F(y)−F(x)}. A C1-type takeover needs an initial copy, Nπ₀(y) ≥ 1, **and** an advantage d(y) − d(x) ≥ log N + ω. Then F(y) − F(x) = log(π₀(y)/π₀(x)) + d(y) − d(x) ≥ −log(Nπ₀(x)) + log N + ω = log(1/π₀(x)) + ω ≥ ω. In words: **the outsider must beat the occupied W-states in the posterior itself, by at least ω nats**. If the W-particles track the posterior upward (reach states with F ≥ F(y) − δ for every reachable outsider y), no outsider can take over in mean field and only the drift/fluctuation terms of D4 remain.

**Reading for BVS (PROOF SKETCH).** A start-visible outsider extra (marginally correlated with y) is over-counted by its table relative to its joint contribution, so its d-increment is ≤ 0; a synergistic (suppressor-type) extra has d-increment ≈ its gain + ½log n but start factor ≈ 1/(2p√n). So an outsider with Nπ₀(y) ≳ 1 can carry at most ≈ log N/log(2p√n) ≈ 1 invisible synergistic extra (N = max(2500, n, p)). C1's structure in BVS therefore needs W-particles that lag *in the posterior* (they cannot reach better W-states, i.e. a posterior-level barrier, §4/§6) together with an outsider class that is posterior-better than the lagging states. Under T03's hypotheses Proposition M removes the lag, and the right repair set W contains such outsiders anyway (terminal repair from S° ∪ {l} adds the missing truths downhill and deletes l). A BVS design realising C1 with REPAIR still valid on the occupied region was not found and is not expected (CONJECTURE).

---

## 7. Assembly with the actual run (T13, islands, repair) — PROVED given the inputs

**Theorem B2-W4.** Assume EX-A, EX-S, CAL, SR, a successful 𝓒, and for the frozen grid:
- (TRACK) and (OSC): potentials h_t with h_T ≤ 1_W, exits η_t, confinement sets 𝔛_t with P(E^c | 𝓒) ≤ ε_E, oscillations κ_t, Γ = Σ_tΔ_tκ_t;
- (REPAIR on W) sup_{x∈W} P_x(S₀ not scored in L + 4 rounds at φ = 1) ≤ ε_rep (Theorem B of W1-T24G, uniform form B-unif).
Then, with T ≤ T_e (T13(ii)(b): a successful construction has at most T_e intervals) and R = 4 islands,
  P(S₀ ∉ 𝒮 | 𝓒) ≤ [ε_E + exp{−Nπ₀(h_0)(1 − e^{−c})}]^4 + ε_rep,  1/c ≤ [1 + (T_e − 1)/(e−1)] e^{Γ}/∏_{s≤T}(1 − η_s).
*Proof.* Islands are conditionally independent given 𝓒 (fresh streams 10–13, EX-S), so the probability that no island has a W-particle at the end of stage T is the product of the four D5 bounds. On the complement, take the smallest-index W-particle of the first such island (measurable); its terminal rounds carry no reweighting or resampling (engine `run_island_s`), so REPAIR applies with fresh randomness (W1-T38E §7 step (5)). Monotonicity of D5's bound in T gives the T_e form. ∎

Plugging into T38(b)-R route (b2) and T21: liminf P(Uᶜ, Ŝ = S₀) ≥ 1 − limsup P(U) whenever the right side above → 0 in P₀-probability. The (b2) inputs are now **(TRACK), (OSC) with Γ + Σ_sη_s ≤ log(Nπ₀(h_0)/T_e) − ω(1), confinement, and REPAIR on the same W**: no SHARE, no LT.

**Where T13 and T15 enter, and where they cannot.**
- T13(ii)(b) supplies T ≤ T_e and acceptance of every interval; T ≤ T_e is the only grid property D5 needs.
- T13's χ² bounds concern the restricted laws q_φ(· | V), not realised particles. By Proposition G no grid property can control Γ. T13 helps only in a local-equilibrium refinement of r_t (if the h-subpopulation were distributed as q_{t−1}(· | R), its weight dispersion would be ≤ 1/9 + O(ε_C)); this refinement is not needed above and is not claimed.
- T15 converts an islandwise lower tail of Ẑ_r/Z into occupancy (D1). LT fails in the masked, late-crossing case even when delivery succeeds (C1 without o; §5). D4/D5 replace T15's lower tail of Ẑ_r/Z by an envelope on Ẑ^h_t/Ẑ_t, the subpopulation's evidence relative to the island's, which is the quantity that actually decides survival.
