# API-MASKZPIP — PROOF.md (candidates; not reviewed, not adopted)

Status words follow `theory_campaign/PROTOCOL.md`. "PROVED" = complete proof checked line by line by this run;
it is a candidate. Inputs from other branches are marked (locked) or (candidate).

## 0. Setting and notation

Fixed data, a successful frozen calibration 𝓒 (EX-A, EX-S, CAL, START), one island with N particles, frozen grid
0 = φ_0 < φ_1 < … < φ_T = 1. Notation of O-PW2 §2 (candidate), which re-derives T12(i) (locked):

- γ₀ = unnormalised start law, γ₁ = γ = unnormalised posterior, d := log γ₁ − log γ₀ on Ω (finite), so the bridge is
  γ_φ = γ₀ e^{φd} = γ₀^{1−φ}γ₁^φ, Z̄_φ := Σ_Ω γ_φ, q_φ := γ_φ/Z̄_φ; π₀ = q_0, π = q_1, Z = Z̄_1. q_t := q_{φ_t}.
- Δ_t := φ_t − φ_{t−1}, G_t := e^{Δ_t d}, c_t := Z̄_t/Z̄_{t−1}, g_t := G_t/c_t (so q_{t−1}(g_t) = 1, q_{t−1}g_t = q_t).
- q̂_t := empirical law of the N particles of stage t after the stage-t mutation (q̂_0: N iid π₀ draws).
- W_t := ∏_{k=1}^t q̂_{k−1}(g_k) = Ẑ_t/Z̄_t·Z̄_0/… ; W := W_T = Ẑ_r/Z (Z̄_0 known exactly under EX-A).
- 𝓕_t := σ-field of the island up to q̂_t. h_{s,T} := Q_{s+1}⋯Q_T 1 with Q_t f := g_t·K_t f, K_t the v3 round kernel
  at φ_t; equivalently h_{s,T}(x) = E[∏_{k=s+1}^{T} g_k(X_{k−1})] for the chain X_s = x, X_k ~ K_k(X_{k−1}, ·).
- Inputs used: (O-PW2 Lemma 2, candidate; = T12(i.b) (locked) at intermediate stages) E_𝓒[W_s q̂_s(f)] = q_s(f) for f
  fixed given 𝓒; (O-PW2 Thm A1, candidate) M_s := W_s q̂_s(h_{s,T}) is an (𝓕_s)-martingale, s = −1, …, T−1, M_{T−1} = W.
  Both are the standard Feynman–Kac identities for multinomial resampling + fresh mutation randomness.
- New symbols: S° := argmax π₀ (start mode); for x°, x* ∈ Ω, a(x°,x*) := log π₀(x°)/π₀(x*), Λ(x°,x*) := log π(x*)/π(x°),
  φ* := a/(a+Λ) (the **crossing temperature**: q_φ(x*) = q_φ(x°) iff φ = φ*, when a, Λ > 0); d_max := max_Ω d,
  x_m ∈ argmax_Ω d; for A ⊆ Ω, D_A := d_max − max_{Ω∖A} d; E_s(A) := {q̂_s(A) = 0} ("no particle of stage s in A").
- PIP notation (T23, W2-T26, F-MASKPIP): δ₁ := 1 − π(S₀), u_π := δ₁/π(S₀), ρ̄ (one-round departure probability from S₀ at
  φ = 1), f_{r,0} := q̂_T(Ω∖{S₀}), PIP̂_rj the island's RB PIP over the 4 measured rounds after L burn-in rounds,
  PIP_j := π(j ∈ S). ν̄_r := E_𝓒[q̂_T] (mean end-of-stage-T law). TV(μ,ν) := ½Σ|μ−ν|.
- Top store 𝒯 (O-CERT): the reported set of distinct scored models with exact scores; Z_𝒯 := Σ_𝒯 γ₁;
  PIP^𝒯_j := Σ_{S∈𝒯, S∋j} γ₁(S)/Z_𝒯.

---------------------------------------------------------------------------------------------------------------------

## Part E — the evidence

### Theorem E1 (two-phase sandwich). PROVED (deterministic, any kernel, any grid, any N).

Let 1 ≤ t ≤ T, M, M′ ⊆ Ω, x° ∈ M, x* ∈ M′, η := max_{x∈M}|d(x)−d(x°)|, η′ := max_{x∈M′}|d(x)−d(x*)| (η′ := 0 if t = T).
On F := {supp q̂_k ⊆ M for k = 0,…,t−1; supp q̂_k ⊆ M′ for k = t,…,T−1},

  | log W − Ψ_t | ≤ φ_t η + (1−φ_t) η′,   Ψ_t := log[q_t(x°)/π₀(x°)] + log[π(x*)/q_t(x*)].

Moreover Ψ_t = (1−φ_t)a − φ_tΛ + log π(x*) − log π₀(x°) = (a+Λ)(φ* − φ_t) + log π(x*) − log π₀(x°).

*Proof.* For k ≤ t−1, q̂_k(G_{k+1}) is an average of e^{Δ_{k+1}d(x)} over x ∈ M, hence lies in
[e^{Δ_{k+1}(d(x°)−η)}, e^{Δ_{k+1}(d(x°)+η)}]. For k ≥ t it lies in e^{Δ_{k+1}(d(x*)±η′)}. Since Σ_{k=1}^t Δ_k = φ_t and
Σ_{k=t+1}^T Δ_k = 1−φ_t, Ẑ_r/Z̄_0 = ∏_k q̂_{k−1}(G_k) = exp{φ_t d(x°) + (1−φ_t)d(x*) ± (φ_tη + (1−φ_t)η′)}. On the other
hand q_t(x°)/π₀(x°) = e^{φ_t d(x°)} Z̄_0/Z̄_t and π(x*)/q_t(x*) = e^{(1−φ_t)d(x*)} Z̄_t/Z̄_1, so
e^{Ψ_t} = e^{φ_t d(x°) + (1−φ_t)d(x*)} Z̄_0/Z. Divide: W = Ẑ_r/Z = e^{Ψ_t ± (…)}. For the second form,
log q_t(x) = (1−φ_t) log π₀(x) + φ_t log π(x) − log C_t with the same C_t for every x, so
log q_t(x°) − log q_t(x*) = (1−φ_t)a − φ_tΛ. ∎

**Corollary E1a (late switching = underestimation by the log-odds overshoot).** With x° = S°, x* = S₀ and the
population frozen at S° before stage t and at S₀ from stage t on (η = η′ = 0):
log W = (a+Λ)(φ* − φ_t) + log π(S₀) − log π₀(S°) exactly. If π(S₀), π₀(S°) → 1, the island underestimates Z by
e^{(a+Λ)(φ_t−φ*)} when it switches after the crossing temperature, and overestimates (at most by 1/π₀(S₀)) when it
switches before. PROVED.

**Corollary E1b (island agreement is uninformative).** On F, log W is determined by (x°, x*, t) up to
φ_tη + (1−φ_t)η′. Hence four islands that switch at the same stage report log Ẑ_r within 2(φ_tη + (1−φ_t)η′) of
each other *whatever* the value of log Ẑ − log Z. PROVED. (Explains F-MASKPIP's masked8/G1 row: q05–q95 of
log W_r = (−10.8, −10.8).)

**Corollary E1c (one-sided relaxation).** If supp q̂_k ⊆ M for k < t and q̂_k(x*) ≥ 1 − f_k for k ≥ t, then
log W ≥ Ψ_t − φ_tη + Σ_{k=t}^{T−1} log(1−f_k). *Proof:* q̂_k(G_{k+1}) ≥ (1−f_k)G_{k+1}(x*) for k ≥ t; rest as above. ∎

### Theorem E2 (miss bound: the evidence lost by a blind step). PROVED (any kernel, any grid, any N).

For A ⊆ Ω and 1 ≤ t ≤ T,

  (a) E_𝓒[W·1{E_{t−1}(A)}] ≤ κ_t(A) := q_{t−1}(1_{Ω∖A} h_{t−1,T}) ≤ e^{(1−φ_t)d_max} γ_{φ_t}(Ω∖A)/Z
       ≤ [π₀(Ω∖A)/π₀(x_m)]·e^{−φ_t D_A};
  (b) for η ∈ (0,1): P_𝓒(W > κ_t(A)/η) ≤ η + P_𝓒(E_{t−1}(A)ᶜ); for t = 1, P_𝓒(E_0(A)ᶜ) ≤ N π₀(A);
  (c) (arrival-temperature form) let τ_A := min{s ≥ 0 : q̂_s(A) > 0} and τ′ := min(τ_A, T). Then
       P_𝓒( W > (T/η)·[π₀(Ω∖A)/π₀(x_m)]·e^{−φ_{τ′} D_A} ) ≤ η + N π₀(A).
  For t = T the bound in (a) is exactly π(Ω∖A) (h_{T−1,T} = g_T).

*Proof.* (a) E_{t−1}(A) ∈ 𝓕_{t−1}; by the martingale property E[W 1_E] = E[M_{t−1}1_E] = E[1_E W_{t−1} q̂_{t−1}(h_{t−1,T})].
On E, q̂_{t−1} charges only Ω∖A, so q̂_{t−1}(h) = q̂_{t−1}(1_{Ω∖A}h); dropping 1_E (all terms ≥ 0) and applying
Lemma 2 with f = 1_{Ω∖A}h_{t−1,T} (fixed given 𝓒) gives E[W1_E] ≤ q_{t−1}(1_{Ω∖A}h_{t−1,T}) = κ_t(A). For the bound on
h: in h_{t−1,T}(x) = E[g_t(x)∏_{k=t+1}^T g_k(X_{k−1})], each g_k(y) ≤ e^{Δ_k d_max}/c_k, so
h_{t−1,T}(x) ≤ g_t(x) e^{(1−φ_t)d_max} Z̄_t/Z. Then q_{t−1}(1_{Ω∖A}g_t) = q_t(Ω∖A) = γ_{φ_t}(Ω∖A)/Z̄_t, giving the
middle bound. Finally γ_{φ_t}(Ω∖A) ≤ γ₀(Ω∖A)e^{φ_t max_{Ω∖A}d} and Z ≥ γ₀(x_m)e^{d_max}; the ratio is
[π₀(Ω∖A)/π₀(x_m)] e^{−φ_t D_A}.
(b) Markov on W1_E plus P(Eᶜ); at t = 1, q̂_0 is N iid π₀ draws, so P(q̂_0(A) > 0) ≤ Nπ₀(A).
(c) Apply (a) and Markov at each t ∈ {1,…,T} with level η/T and take the union bound:
P(∃t: E_{t−1}(A) ∧ W > (T/η)κ_t(A)) ≤ η. If 1 ≤ τ_A ≤ T−1, then E_{τ_A−1}(A) holds (no particle of stage τ_A−1 in A),
so t = τ_A = τ′ is admissible; if τ_A ≥ T, then E_{T−1}(A) holds and t = T = τ′ is admissible. In both cases
κ_{τ′}(A) ≤ [π₀(Ω∖A)/π₀(x_m)]e^{−φ_{τ′}D_A} by (a). The remaining event {τ_A = 0} = E_0(A)ᶜ has probability ≤ Nπ₀(A). ∎

*Reading.* Whatever happens later in the bridge, the island evidence carries at most the start-mass-weighted
fraction e^{−φ D_A} of Z, where φ is the temperature at which the population first touches A. Choosing A = "the basin
of S₀" (models agreeing with S₀ where S° disagrees), D_A is the d-gap between the best model of the basin and the best
model outside it. This generalises F-MASKPIP (N-c) (T = 1, W ≤ e^{−D}/π₀(S₀)) to every grid and every kernel, and it
is the rigorous half of Corollary E1a. Note that E W = 1 is not contradicted: the event Eᶜ has probability ≤ Nπ₀(A)
and carries the mean (F-MASKPIP M3).

### Lemma J (a full-space ESS grid cannot jump a crossing). PROVED.

If χ²(q_t‖q_{t−1}) ≤ χ̄ then q_t(A)² ≤ (1+χ̄) q_{t−1}(A) for every A ⊆ Ω.
*Proof.* q_t(A) = q_{t−1}(g_t1_A) ≤ q_{t−1}(g_t²)^{1/2}q_{t−1}(A)^{1/2} (Cauchy–Schwarz) and q_{t−1}(g_t²) = 1+χ². ∎
With the method's threshold (ESS ≥ 0.9 ⇔ χ̄ = 1/9): a single step can raise the mass of a set from ε only to
≤ (10ε/9)^{1/2}; so the blind step of E2 (q_{t−1}(A) ≈ 0, q_t(Ω∖A) ≈ 0) is impossible on the full space and possible
only when the ESS is computed on a set that misses A (T13(iii); the candidate set V of METHODOLOGY §6.7, or a particle
population with no particle in A).

### Proposition E3 (positive side: exact pair refresh gives W → 1). PROVED in the stated idealisation;
### the perturbation to a pair-dominated bridge is a PROOF SKETCH.

(a) (O-PW2 Thm C with λ = 0, candidate) If every round kernel is an exact refresh, K_t(x,·) = q_t, then
E_𝓒(W−1)² = ∏_t(1 + χ²_t/N) − 1, χ²_t := χ²(q_t‖q_{t−1}).
(b) (pair) Let x°, x* differ in exactly one coordinate j and suppose q_t({x°,x*}) = 1 for all t (pure pair). Then the
v3 round is an exact refresh: the Gibbs step on j is a draw from q_t(·|{x°,x*}) = q_t, and every other elementary step
proposes a state of q_t-mass 0, which is never accepted (heat-bath probability 0; MH ratio 0). So (a) applies, and
with a grid satisfying χ²_t ≤ 1/9, E(W−1)² ≤ e^{T/(9N)} − 1.
*Proof of (b).* Immediate from the description of the round (smc_sim.round = METHODOLOGY §6.5) and (a). ∎
(c) PROOF SKETCH (pair-dominated): if q_t({x°,x*}) ≥ 1 − ε_t, couple the island with the pure-pair island; the coupling
fails with probability ≤ N Σ_t (m·ε_t·ḡ-type leakage) and on success W equals the pure-pair W up to factors
∏(1 ± O(ε_t ḡ_t)). This is the "two-state analysis, V11" that METHODOLOGY §6.7 attributes to Fable-T3 (unproved). Not
completed here: the leakage constant needs sup-norm control of h (O-PW2's H_{s,T}), which is the same obstruction O-PW2
reports.

### Theorem E4 (the evidence dichotomy on a pair-dominated masked bridge). PARTLY PROVED.

Let x° = S° and x* = S₀ (or the pair that dominates the bridge), A := the S₀ basin, φ* the crossing temperature.
- **(blind; PROVED by E2(c))** If the population first touches A at stage τ_A, then
  log Ẑ_r − log Z ≤ −φ_{τ_A}D_A + log(T/η) + log(1/π₀(x_m)) w.p. ≥ 1 − η − Nπ₀(A).
  On the frozen path the matching lower bound holds up to the sandwich width (E1, E1c).
- **(resolved; CONJECTURE, PROOF SKETCH E3(c))** If both members of the pair are in the candidate set V, the grid's
  restricted ESS controls the pair's χ²_t (Lemma J on the pair), and the pair is exactly refreshed (E3(b)); then
  log Ẑ_r − log Z = O_P(√(T/N)) + leakage.
So the honest two-sided statement is: **upper tail always O_P(1) (Markov, T31(i)); lower tail O_P(√(T/N)) if the grid
resolves the crossing, and −φ_{τ_A}D_A + O_P(log T + log 1/π₀(x_m)) if it does not.** Which case occurs is decided by
whether any calibration run scored the S₀ basin (V includes the top 20p *scored* models by γ₁, METHODOLOGY §6.7).

**LH consequence (PROOF SKETCH).** On exact-Gram LH (W1-EXP §4; c hubs M omitted by S° = S₀∖M), with A := models
containing a hub: D_A ≥ d(S₀) − max_{hub-free} d = Θ(n) (F-MASKPIP N-c, PROOF SKETCH) and π₀(A) = c p^{−1}n^{−1/2}e^{O_P(1)}.
If the final grid is blind (no calibration run scored a hub-containing model) and its first step is φ₁, then
log Ẑ_r − log Z ≤ −Θ(n)φ₁ + O_P(log n) → −∞ (assuming log 1/π₀(x_m) = O_P(log n), hypothesis XM). But O-BGIBBS BG1/BG3
(candidates) say the pilot scores S₀ at stage 1 w.p. → 1 on LH, so V ∋ S₀ and the method's grid is expected to be in
the *resolved* case on LH c = 1 (pair differs in one coordinate: E3(b) applies to the pair). For c ≥ 2 the pair differs
in c coordinates; exact pair refresh fails and the resolved case is OPEN.

---------------------------------------------------------------------------------------------------------------------

## Part P — the PIPs

### Theorem P1 (RB PIP bias ≤ TV distance of the delivered population). PROVED.

For every j, |E_𝓒[PIP̂_rj] − PIP_j| ≤ TV(ν̄_r P^{L}, π) ≤ TV(ν̄_r, π) ≤ E_𝓒 f_{r,0} + δ₁, where P is the φ = 1 round
kernel. Conditionally: |E[PIP̂_rj | 𝓕_T] − PIP_j| ≤ TV(q̂_T, π) ≤ f_{r,0} + δ₁; in particular on the locked event
{q̂_T = δ_{S₀}}, |E[PIP̂_rj | 𝓕_T] − PIP_j| ≤ δ₁ (no L, no B, no ρ̄).

*Proof.* PIP̂_rj = (4N)^{−1}Σ_{i,h} o_{i,h,j}, where o_{i,h,j} is the heat-bath probability π(j ∈ S | S_{−j}) evaluated at
particle i's state just before its Gibbs step on j in measured round h. Fix i. Given 𝓕_T, particle i's terminal
path is a function Φ(X_{i,T}, U_i) of its end-of-stage-T state and fresh randomness U_i (uniform orders and uniforms;
EX-S; no resampling in the terminal rounds, T12 (R3)) whose law does not depend on i. Let F(x) := E[o_{h,j}(Φ(x, U))]
∈ [0,1]. If X ~ π, then every intermediate state of the path is ~ π (each elementary kernel is π-invariant), so
E_π F = E_π[π(j ∈ S | S_{−j})] = PIP_j. Hence for any start law μ, |μ(F) − PIP_j| = |μ(F) − π(F)| ≤ TV(μ, π) since
0 ≤ F ≤ 1. Average over i and h: E[PIP̂_rj | 𝓕_T] = q̂_T(F̄) with F̄ := ¼Σ_h F_h ∈ [0,1], so
|E[PIP̂_rj|𝓕_T] − PIP_j| ≤ TV(q̂_T, π); taking E_𝓒 and using linearity, |E_𝓒 PIP̂_rj − PIP_j| = |ν̄_r(F̄) − π(F̄)| ≤
TV(ν̄_r, π). The burn-in refinement: F̄ = P^L F̃ for F̃ defined from the start of the first measured round, and
TV(μP^L, π) ≤ TV(μ, π) because πP = π. Finally TV(μ, π) ≤ TV(μ, δ_{S₀}) + TV(δ_{S₀}, π) = μ(Ω∖{S₀}) + δ₁. ∎

### Theorem P2 (two-sided PIP error after delivery, with rate). PROVED (composition of locked T23(ii) and T12 (R3)).

Conditionally on 𝓕_T: E[ max_j |PIP̂_rj − PIP_j| | 𝓕_T ] ≤ f_{r,0} + (L+4)ρ̄ + u_π + δ₁, and
E[max_j|PIP̂_rj − 1{j∈S₀}| | 𝓕_T] ≤ f_{r,0} + (L+4)ρ̄ + u_π.
*Proof.* T23(ii-a,b) (locked, pathwise): max_j|PIP̂_rj − 1{j∈S₀}| ≤ B̄_r + u_π. B_{i,h} = 1 requires X_{i,T} ≠ S₀ or a
departure from S₀ in one of the first L+h ≤ L+4 terminal rounds; given the state at S₀ at the start of a round (and
everything before), a departure has probability ρ̄ (T12 (R3)); union bound: E[B̄_r|𝓕_T] ≤ f_{r,0} + (L+4)ρ̄. Finally
|PIP_j − 1{j∈S₀}| ≤ δ₁. ∎
*Rates.* W2-T26 Lemma 2 (candidate): ρ̄ ≤ (B+3)u_π. Under T03 (locked) δ₁ = O_P(√(log n/n)) and L = O(log n), B ≤ 16:
on the locked event (f_{r,0} = 0) the error is O_P(log n·√(log n/n)), and the conditional bias is ≤ δ₁ = O_P(√(log n/n))
(P1). Locking itself is O-BGIBBS BG3 (candidate; LH with p fixed) or F-MASKPIP DELIV-POP (OPEN in general).

### Proposition P3 (top-store evidence and PIPs: deterministic two-sided bounds). PROVED.

For any reported set 𝒯 of exactly scored models: Z_𝒯/Z = π(𝒯) and |PIP^𝒯_j − PIP_j| ≤ π(Ω∖𝒯) for every j.
If S₀ ∈ 𝒯: 1 − δ₁ ≤ Z_𝒯/Z ≤ 1, |PIP^𝒯_j − PIP_j| ≤ δ₁ and |PIP^𝒯_j − 1{j∈S₀}| ≤ 2δ₁.
*Proof.* Z_𝒯/Z = Σ_𝒯γ₁/Σ_Ωγ₁. Write J := {S ∋ j}, a := π(𝒯∩J), b := π(𝒯), so PIP^𝒯_j = a/b, PIP_j = a + π(J∖𝒯).
Then PIP^𝒯_j − PIP_j = a(1−b)/b − π(J∖𝒯). Both terms lie in [0, 1−b] (a/b ≤ 1), so the difference has absolute value
≤ 1 − b = π(Ω∖𝒯). If S₀ ∈ 𝒯 then π(Ω∖𝒯) ≤ δ₁; add |PIP_j − 1{j∈S₀}| ≤ δ₁. ∎
**Corollary P3′ (PROVED as a composition, CONDITIONAL).** If P(𝒪 ∩ {S₀ ∉ 𝒯}) → 0 (S₀ scored, e.g. O-BGIBBS BG3 on LH,
and the top store keeps the best scored models, so S₀ ∈ 𝒯 once S₀ is scored and is the HPM, T03) and δ₁ → 0 (T03),
then on 𝒪: Z_𝒯/Z → 1 and max_j|PIP^𝒯_j − PIP_j| → 0 in probability, both at rate δ₁ = O_P(√(log n/n)), with no
grid, ESS, mixing or second-moment hypothesis. **This is the only two-sided evidence consistency statement on the
masked family that does not need the bridge to resolve the crossing.**

---------------------------------------------------------------------------------------------------------------------

## Part C — per-fit certificates at finite n (building on O-CERT)

### Proposition C1 (certified upper bound on the evidence ratio). PROVED (deterministic).
Ẑ/Z ≤ Ẑ/Z_𝒯 on every run (Z ≥ Z_𝒯). If Ẑ < Z_𝒯, the run **certifies underestimation** of Z by at least Z_𝒯/Ẑ.
Same for each island: Ẑ_r/Z ≤ Ẑ_r/Z_𝒯.

### Proposition C2 (the per-fit evidence band). PROVED (O-CERT Thm C1 + C1 above).
With probability ≥ 0.95, simultaneously for all models: log Z ≥ max(log Z_𝒯, log Ẑ − log 20). No finite-n upper bound
on Z (equivalently no lower bound on W) follows from the run alone (O-CERT; T31(c,d)); E1b shows that island agreement
cannot supply one.

### Proposition C3 (per-fit PIP gap). PROVED.
For every j: |PIP̂_rj − PIP_j| ≤ |PIP̂_rj − PIP^𝒯_j| + π(Ω∖𝒯). The first term is computable from the output; the second
is not certifiable from above, but w.p. ≥ 0.95 π(Ω∖𝒯) ≥ 1 − Z_𝒯/(0.05Ẑ) (a certified *lower* bound on the missing mass,
O-CERT). On a box R = 2^U certified by O-CERT C4, the region-relative PIPs π(j ∈ S | R) are computable exactly.
*Proof.* Triangle inequality and P3; the lower bound is O-CERT's "posterior mass outside the top store". ∎

### Remark C4 (blind-crossing flag; diagnostic, no theorem).
E2 says the evidence is lost at the first stage where the S₀ basin's particle fraction jumps from 0 to ≈ 1. The run can
record the per-stage fraction of particles in the HPM's basin; a 0 → >½ jump in one stage whose V-restricted ESS was
≥ 0.9 flags a blind crossing (Lemma J: impossible on the full space). The method's rebuild loop (§6.7) is the remedy:
rebuilding V with the newly scored HPM inserts temperatures at the crossing.
