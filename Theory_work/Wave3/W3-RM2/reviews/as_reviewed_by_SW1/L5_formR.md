# L5 — Form R: bridges (P8), (P9), (P10), Theorem RM2-R (claim (C2)) and the containment of RM-R (claim (C4), second half)

Status: **PROVED (by this seat, unchecked)**; lemma check LC2-B (Codex gpt-6.1-sol high, blind,
`../reviews/LC2B_L5_check_sol.md`): (S2)/(S3), P8, P9, D-loc^b, P10, Theorem RM2-R (conditional on W2-APP:POST@1.0.1),
containment of RM-R VERIFIED; P9a VERIFIED-WITH-AMENDMENTS (2 MINOR proof conventions, applied [LC2B-1], [LC2B-2]); no
FATAL, no MAJOR. Given `L4_sandR_b.md` (Lemma SAND-R^b), `L0_toolkit_b.md`, `L2_width.md`
and the consumed claims with their recorded statuses (§5 below). Ticket W3-RM2; statement: `../STATEMENT.md` v1.4
§3.2, §4. Templates (re-run, not consumed): RM `lemmas/L4_formR.md` (bridges at polylogarithmic size) and LOC2
`lemmas/L2_NAR.md` (Lemma NA-R, polylogarithmic lattice; `Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md`).
One classical fact, as in `L2_width.md`: Gaussian concentration for a 1-Lipschitz f and g ~ N(0, I_n),
P(f(g) − Ef(g) ≤ −t) ≤ e^{−t²/2}, and E|f(g)| < ∞.

## 0. Setting R: standing facts

Setting and notation of `L4_sandR_b.md` §0–§1 (N, C, h_n, W, t_j, X, Y, ε, θ_lo, θ_hi, the event E_W of §1.1 with
P(E_W) → 1). Q = Q_n ⊇ S₀ deterministic, q := |Q| ≤ K, **q ≤ n^b with a fixed b < ½**. 𝓛, 𝔓, 𝔓⁺, u_{T,l}, Z_{T,l},
a⁰_n(k), a_{n,δ}(k), 𝔴⁰_n, 𝔴_n(δ), d_n, λ_n, c_n(k), 𝒵_n: as in `L2_width.md` §0, §4, for the realised X.
(S1) *Energy.* ‖μ‖² ≤ s₀²θ_hi²(n − 1) surely: (F0)'s ‖μ‖² ≤ Mn with M := s₀²θ_hi². θ* is the coefficient vector of
the standardised design, so conditionally on W the model is Setting F with μ = Xθ*, θ*_min ≥ θ_lo.
(S2) *Floors on Q ∪ {l}.* Assume λ_min(Σ_{Q∪{l}}) ≥ c for every l ∈ [p] (part of (FL-R)). On E_W, for n ≥ n₀:
λ_min(R̂_{Q∪{l}}) ≥ c/2 for every l, i.e. **𝒲⁰_n ⊇ E_W**. *Proof.* On E_W, |R̂_{jk} − Σ_{jk}| ≤ 3C_Ah_n for all j, k
(`L4_sandR_b.md` 1.2(iii)), so ‖R̂_S − Σ_S‖_op ≤ (q + 1)·3C_Ah_n ≤ 6C_An^{b−1/2}√(log n) → 0 for S = Q ∪ {l}: here b < ½ is
used. ∎ So (FL-Q) holds with φ₀² := c/2 on E_W, and (F0) holds: q log n/n → 0.
(S3) *Signal floor.* On E_W, λ_n = (n − 1)(c/2)θ*²_min/σ² ≥ (n − 1)cθ_lo²/(2σ²) and, by Lemma d of `L2_width.md`,
d_n² + log n ≤ 2(q + 1) + 4 log(2p) + log n ≤ C(A)(n^b + log n). So (BM-W) holds on E_W with the deterministic rate
λ_n/(d_n² + log n) ≥ c′n^{1−b}/log n → ∞.

## 1. (P8) F → R: no-addition and truth removal under Gaussian rows

**Lemma P8.** Setting R, λ_min(Σ_{Q∪{l}}) ≥ c for all l, q ≤ n^b with b < ½, q ≤ K, and **(W-R)**: there is a
deterministic t_n → ∞ with P(𝒲⁰_n ∩ {𝔴⁰_n ≤ −t_n}) → 1. Then, under the joint law of (W, ε), P(NA(𝓛)) → 1 and
P(TL(𝓛)) → 1.
*Proof.* Let 𝒳_n := E_W ∩ {𝔴⁰_n ≤ −t_n} (W-measurable; P(𝒳_n) → 1 by `L4_sandR_b.md` 1.1 and (W-R)). Condition on
W ∈ 𝒳_n: Setting F with (F0) (M = s₀²θ_hi², the deterministic envelope q log n/n ≤ n^{b−1} log n), (FL-Q) (φ₀² = c/2, (S2)),
and ε ~ N(0, σ²I) independent of W. The lemmas of `L2_width.md` then apply with thresholds n₀ that depend only on
(σ², M, c, A) and on deterministic envelopes:
* Lemma NA-conv: n₀ depends on (σ², M, φ₀, A) and the sequence q log n/n — replace it by its envelope
  n^{b−1} log n (every condition in `L0_toolkit_b.md` §1 and in the proof of NA-conv is monotone in q).
* Lemma NA-W, (1.1): with s_n := −𝔴⁰_n ≥ t_n, as soon as (3/4)t_n√(log(n + 1)) ≥ 4κ_E + 2:
  P(𝒵_nᶜ | W) ≤ exp(−s_n²/8) ≤ exp(−t_n²/8).
* Toolkit event of the lattice family: P(𝓔_nᶜ | W) ≤ 2e^{−n^{1/3}} + n^{−2} + 2/n.
Hence P(NA(𝓛)ᶜ | W) ≤ exp(−t_n²/8) + 2e^{−n^{1/3}} + n^{−2} + 2/n for n ≥ n₀, uniformly on 𝒳_n; integrate:
P(NA(𝓛)ᶜ) ≤ P(𝒳_nᶜ) + exp(−t_n²/8) + o(1) → 0.
* Lemma TL-W: on 𝒳_n, (BM-W) holds with the deterministic rate of (S3), so its n₀ is uniform; TL(𝓛) holds on
  𝓔_n ∩ 𝒵⁺_n ∩ ℬ_n, and P(ℬ_nᶜ | W) ≤ 1/n, P(𝒵⁺_nᶜ | W) ≤ P(𝒵_nᶜ | W) + 2/n ≤ exp(−t_n²/8) + 2/n.
So P(TL(𝓛)ᶜ) ≤ P(𝒳_nᶜ) + exp(−t_n²/8) + o(1) → 0. ∎

## 2. (P9) D → W: the width condition from references and atoms

[LC2B-1] In this section replace W by W − 1m_nᵀ, without changing notation. This leaves CW, X, P_T, every Z_{T,l} and
all population covariance and regression hypotheses unchanged; the latent extension and its functionals are read
on this centred row law (as in the template, `L2_NAR.md:10-11`).

**(D-R^b)** (STATEMENT §3.2) = hypotheses (N1), (R1)–(R3) of LOC2 Lemma NA-R (`L2_NAR.md:22-36`) for (Σ_n, Q), with
its deterministic latent-extension contract (`L2_NAR.md:15-20`), and its size hypothesis (N0) replaced by
**(N0^b)**: p ≤ n^A, S₀ ⊆ Q, q ≤ n^b with b < ½, q ≤ K. Recalled: (N1) λ_min(Σ_{Q∪{l}}) ≥ c for every l; for
(T, l) ∈ 𝔓⁺, e_{T,l} := W_l − W_Tβ_{T,l} is the population regression residual, τ²_{T,l} := Var(W_l | W_T) ≥ c;
(R1) N_n frames of ≤ m₀ deterministic functionals of the (extended) Gaussian row, log N_n ≤ log p + o(log n), and
for each pair a reference r_{T,l} = 𝒲ψ_{T,l} in the span of its frame, ϱ²_{T,l} := Var ψ_{T,l}; (R2) atoms 𝒜_n (functionals of
variance ≤ 1) with e_{T,l} = r_{T,l} − Σ_aλ_{T,l,a}𝒲a, L_n := max‖λ_{T,l}‖₁, L_n² log(|𝒜_n| + 1) = o(log n);
(R3) ϱ²_{T,l} ≤ (1 + η_n)τ²_{T,l}, η_n → 0. The extension is independent of ε.

**Lemma P9a (joint-law bound at polynomial size).** Under (D-R^b) there are a deterministic ς_n → 0 and an event
𝒜_n with P(𝒜_n) → 1 on which every Z_{T,l}, (T, l) ∈ 𝔓⁺, is defined and
  max_{(T,l)∈𝔓⁺} Z²_{T,l} ≤ 2 log p + ς_n log n.                                                            (2.1)
*Proof.* [LC2B-2] If 𝔓⁺ = ∅ (Q = S₀ = [p]), (2.1) is the vacuous bound on its members: take 𝒜_n the sure event and
ς_n = 0. Otherwise: re-run of `L2_NAR.md` Steps 1–5 (`:54-110`); the pair set called 𝔓 there is 𝔓⁺ here. Each step is
re-checked at q ≤ n^b; x, v_n below are O(q + log n) = O(n^b + log n).
*Step 1 (exact identity; no size use beyond q + 1 ≤ N).* A.s. all X_{T∪{l}} have full column rank;
(I − P_T)x_l = t_l⁻¹(I − P_T)Ce_{T,l}; with g := Ce_{T,l}, h := (I − P_T)g: ‖h‖² = ‖g‖² − ‖P_Te_{T,l}‖² and
σZ_{T,l} = (gᵀε − (P_Te_{T,l})ᵀP_Tε)/‖h‖.
*Step 2 (events).* ℓ_𝔓 := log|𝔓⁺| ≤ log p + q log 2; x := ℓ_𝔓 + 2 log n; δ_n := 2√(x/N) + 2x/N → 0 **because q/n → 0**.
E_a: |‖Ce_{T,l}‖²/(τ²_{T,l}N) − 1| ≤ δ_n and ‖Cr_{T,l}‖² ≤ ϱ²_{T,l}N(1 + δ_n) for all pairs (χ²_N, Laurent–Massart, union over
3|𝔓⁺| events: P(E_aᶜ) ≤ 3n^{−2}). E_b: ‖P_Te_{T,l}‖² ≤ τ²_{T,l}v_n, v_n := 4(ℓ_𝔓 + q + 2 log n) (e_{T,l} is independent of W_T with
iid N(0, τ²) entries; given W_T, ‖P_Te‖²/τ² ~ χ²_d, d ≤ q, P(χ²_d > v) ≤ 2^{d/2}e^{−v/4}; P(E_bᶜ) ≤ n^{−2}). E_c:
‖P_Qε‖² ≤ 4σ²(q + log n) (P(E_cᶜ) ≤ 1/n); ‖P_Tε‖ ≤ ‖P_Qε‖ for T ⊆ Q. E_d (frames): ‖P_{𝒮_ι}ε‖² ≤ σ²x′_n for every frame,
x′_n := 2 log N_n + (m₀ + 2) log log n (failure probability O(1/log n)). E_e (atoms): ‖Cε‖² ≤ 2σ²N and
|(C𝒲a)ᵀε| ≤ y_n‖Cε‖ for every atom, y_n² := 2 log(2(|𝒜_n| + 1)) + 2b_n, b_n := √(log n/(1 + L_n²)) → ∞ (failure
probability ≤ e^{−b_n} + e^{−N/8}). None of E_d, E_e involves q. P(E_a ∩ … ∩ E_e) → 1.
*Step 3 (population statistic; no size use).* |gᵀε|/(σ‖g‖) ≤ ζ_n := √((1 + η′_n)x′_n) + L_ny_n√(4/c), with
1 + η′_n := (1 + η_n)(1 + δ_n)/(1 − δ_n) → 1.
*Step 4 (sample vs population — the step that uses the size).* On E_a ∩ E_b: ‖h‖² ≥ τ²(N(1 − δ_n) − v_n) ≥ τ²N/2 for
n ≥ n₀ since v_n = O(n^b + log n) = o(n); ‖g‖/‖h‖ ≤ 1 + ω′_n := (1 − v_n/(N(1 − δ_n)))^{−1/2} → 1; and on E_c
  ‖P_Te‖‖P_Tε‖/(σ‖h‖) ≤ τ√v_n·2√(q + log n)/(τ√(N/2)) = 2√2·√(v_n(q + log n)/N) =: ϵ_n = O((n^b + log n)/√n) → 0,
**which is where b < ½ is needed.** Hence |Z_{T,l}| ≤ (1 + ω′_n)ζ_n + ϵ_n for all pairs.
*Step 5.* x′_n ≤ 2 log p + o(log n) by (R1); L_n²y_n² = o(log n) by (R2) and the choice of b_n (`L2_NAR.md:79-85`,
`:102-105`); so ζ_n² ≤ 2 log p + o(log n), ζ_n² = O(log n), and
((1 + ω′_n)ζ_n + ϵ_n)² = ζ_n² + (2ω′_n + ω′_n²)ζ_n² + 2(1 + ω′_n)ζ_nϵ_n + ϵ_n² ≤ 2 log p + ς_n log n with a deterministic
ς_n → 0 (ς_n collects the o(log n) terms; all are deterministic functions of n). 𝒜_n := E_a ∩ … ∩ E_e. ∎

**Lemma P9 (joint bound ⇒ conditional width).** Under (D-R^b), for every fixed δ₀ ∈ (0, 1 − 2b), with
γ := 1 − 2b − δ₀ > 0 and s̲_n := γ√(log n)/(5√(2A + 1)):
  P(𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ −s̲_n + 2}) → 1.
In particular P(𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ 0}) → 1, and (W-R) holds with t_n := δ₀√(log n)/(2√(2A + 2)) (STATEMENT §1:
𝔴⁰_n ≤ 𝔴_n(δ₀) − δ₀√(log n)/(2√(2A + 2))).
*Proof.* If 𝔓 = ∅, 𝔴_n(δ₀) = −∞. Otherwise let ℬ := {max_{(T,l)∈𝔓}(u_{T,l}ᵀε/σ)² > 2 log p + ς_n log n}; by (2.1) and (S2),
π_n := P(E_Wᶜ ∪ ℬ) → 0 (𝔓 ⊆ 𝔓⁺). The directions u_{T,l} are functions of W, and ε/σ ~ N(0, I_n) is independent of W, so
P(ℬ | W) = P_g(max_𝔓(u_{T,l}ᵀg)² > 2 log p + ς_n log n) with g ~ N(0, I_n) independent of W. Let
𝒲¹_n := E_W ∩ {P(ℬ | W) ≤ √π_n}; by Markov, P(E_W ∖ 𝒲¹_n) ≤ P(ℬ ∩ E_W)/√π_n ≤ √π_n, so P(𝒲¹_n) → 1, and 𝒲¹_n ⊆ 𝒲⁰_n by (S2).
Fix W ∈ 𝒲¹_n, n ≥ n₀ (√π_n ≤ ½). Φ(g) := max_𝔓(|u_{T,l}ᵀg| − a_{n,δ₀}(|T|)) is 1-Lipschitz with E|Φ| < ∞ and
EΦ = 𝔴_n(δ₀). For (T, l) ∈ 𝔓, |T| + 1 ≤ q + 1 ≤ 2n^b, so
a_{n,δ₀}(|T|)² ≥ 2 log p − 2 log(2n^b) + (1 − δ₀) log n = 2 log p + γ log n − 2 log 2. On ℬᶜ therefore
  Φ(g) ≤ √(2 log p + ς_n log n) − √(2 log p + γ log n − 2 log 2) ≤ −[(γ − ς_n) log n − 2 log 2]/(2√((2A + 1) log n)) ≤ −s̲_n
for n ≥ n₀ (both radicands are ≤ (2A + 1) log n; ς_n → 0). So P_g(Φ ≤ −s̲_n) ≥ 1 − √π_n ≥ ½. By concentration,
P_g(Φ ≤ EΦ − 2) ≤ e^{−2} < ½, so the events {Φ ≤ −s̲_n} and {Φ > EΦ − 2} intersect: EΦ − 2 < −s̲_n. ∎
(Only the lower-tail concentration about the mean is used; no median bound is quoted.)

**Lemma D-loc^b ((D-loc^b) ⇒ (D-R^b)).** Assume (N0^b), (N1) and: for every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l}
with |N_l| ≤ ν_n, ν_n = o(log n), and deterministic L_n, η_n with L_n² log(q + 1) = o(log n), η_n → 0, such that for
every (T, l) ∈ 𝔓⁺, with N := T ∩ N_l: ‖β̄_{T,l} − β̄_{N,l}‖₁ ≤ L_n and Var(W_l | W_N) ≤ (1 + η_n)Var(W_l | W_T) (β: population
regression coefficients, zero-padded to Q; β_{∅,l} := 0). Then (R1)–(R3) hold with no latent extension and m₀ = 1.
*Proof* (RM `L4_formR.md`, Lemma D-loc; it does not use the size of Q). Frames: the single functionals
ψ_{N,l} := e_l − Σ_{v∈N}β_{N,l,v}e_v, l ∈ [p], N ⊆ N_l (defined by (N1): N ∪ {l} ⊆ Q ∪ {l}); N_n ≤ p·2^{ν_n}, so
log N_n ≤ log p + o(log n); r_{T,l} := W_l − W_Nβ_{N,l}, ϱ²_{T,l} = Var(W_l | W_N): (R1). Atoms: 𝒜_n := {e_v : v ∈ Q} (variance 1),
λ_{T,l} := β̄_{T,l} − β̄_{N,l}, so r_{T,l} − Σ_vλ_{T,l,v}W_v = W_l − W_Tβ_{T,l} = e_{T,l}, with L_n as given and |𝒜_n| = q: (R2). (R3) is the
variance hypothesis. ∎

## 3. (P10) POST-R

**Lemma P10.** Setting R, (T1-R). Then E[1 − π(S₀)] → 0 under the joint law: [POST].
*Proof.* *p ≥ 2.* (T1-R) is hypothesis LSF of W2-APP:POST@1.0.1 (`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:21-25`;
its setting, `:8-10`, is Setting R with p ≥ max(2, s₀)), whose part (b) (`:30-33`) gives
1 − π(S₀) = O_P(√(log n/n)) under the joint law; since 0 ≤ 1 − π(S₀) ≤ 1, E[1 − π(S₀)] ≤ ε + P(1 − π(S₀) > ε) for every
ε > 0, hence → 0. **Status carried:** W2-APP:POST@1.0.1 is "PROVED (by this seat, unchecked); R02
VERIFIED-WITH-AMENDMENTS, applied" — (C2) is conditional on it.
*p = 1* (if it occurs along a subsequence; self-contained, so no further claim is consumed). Then S₀ = [p] = {1},
K = 1, Ω = {∅, {1}}, w(0) = w(1) = ½. D0 score with ‖y‖² = n − 1: Q_∅ = n − 1; for A = {1}: G_A = n − 1,
H_A = (n + 1)(n − 1) + 1 = n², D_A = n²/n = n, z_A = x₁ᵀy, Q_A = (n − 1) − (x₁ᵀy)²/n = (n − 1)(1 − r̂²(n − 1)/n) with
r̂ := x₁ᵀy/(n − 1) the sample correlation of x₁ and Y. So
F({1}) − F(∅) = −½ log n − ν log[(0.02 + (n − 1)(1 − r̂²(n − 1)/n))/(0.02 + n − 1)] ≥ −½ log n + ν r̂²(n − 1)²/(n(n − 0.98))
(−log(1 − u) ≥ u). Y = x₁θ*₁ + Cε, ‖x₁‖² = n − 1, x₁ᵀε/(n − 1) → 0 and ‖Cε‖²/(n − 1) → σ² in probability (x₁ ⊥ 1 is
independent of ε), so r̂² − θ*₁²/(θ*₁² + σ²) → 0 in probability and θ*₁²/(θ*₁² + σ²) ≥ θ_lo²/(θ_hi² + σ²) > 0. With ν = n/2 + 0.01,
F({1}) − F(∅) → ∞ in probability, π(S₀) = (1 + e^{F(∅)−F({1})})⁻¹ → 1 in probability, and E[1 − π(S₀)] → 0 as above. ∎

## 4. Theorem RM2-R (claim (C2)) and the containment of RM-R

**Theorem RM2-R.** Setting R, the method as coded, any X-measurable partition with blocks ≤ 16, premises and
configuration of STATEMENT §1. Assume (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, and (W-R). Then, under the
joint law of (X, ε): [SAND(Q)], [NA(Q)], [TL(Q)], [POST], hence all conclusions of RM-0 as in (C1).
*Proof.* b < ½ by 15ρ + b < ½. [SAND(Q)]: Lemma SAND-R^b (`L4_sandR_b.md`); its hypotheses are (FL-R) on sets of
size ≤ 16 + s₀, (V-R), and (L-R^b) = (R-Q) + (R-G) + (R-L) + (R-B). [NA(Q)], [TL(Q)]: Lemma P8 ((FL-R) on Q ∪ {l};
(L-size^b), (L-feas) give q ≤ n^b, q ≤ K; (W-R)). [POST]: Lemma P10. [E4]: W3-RM:E4@1.0.0 under its hypotheses (premises
of STATEMENT §1). W3-RM:RM-0@1.0.0 — a statement for any design and any deterministic Q ⊇ S₀ with |Q| ≤ K — applied
under the joint law gives the conclusions: P(Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛)) → 1, on this event LS0 from the coded start
mode makes exactly |S̃₀ ∖ S₀| ≤ |Q ∖ S₀| ≤ n^b deletions and ends at S₀ certified, the shipped cap is not binding; and with
𝒢_n := 𝒦_n ∩ {π(S₀) > ½}, P(𝒢_nᶜ) ≤ 2E[1 − π(S₀)] + P(Sand_n(Q)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0 and every admissible output
run reports Ŝ⁺ = S₀ on 𝒢_n. ∎
With (W-R) supplied by (D-R^b) (Lemma P9, any δ₀ ∈ (0, 1 − 2b)) or by (D-loc^b) (Lemma D-loc^b): the theorem under
population conditions on (Σ_n, θ*, Q) only.

**Containment of RM-R (claim (C4), Gaussian rows).** RM-R's hypotheses (RM `STATEMENT.md:186-190` with §3.2,
`:127-156`): (T1-R), (FL-R), (V-R), (L-R) [|Q| ≤ (log n)^κ, (L-feas), |H_l| ≤ (log n)^κ, the leak bound
|Cov(W_l, W_j | W_{U₀})| ≤ C_Ln^{−1/2} at localised sets, and the localisation bounds with r_n(n log n)^{1/4} → 0], (D-R).
Claim: they imply the hypotheses of RM2-R, with the same Q and H_l.
* Choose any b ∈ (0, ½) and ρ > 0 with 15ρ + b < ½. For n ≥ n₀: |Q| ≤ (log n)^κ ≤ n^b and |H_l| ≤ (log n)^κ ≤ n^ρ.
* (L-R^b): `L4_sandR_b.md` §7 item 1 with ϖ′_n := C_Ln^{−1/2} (ϖ′_n√(n/log n) → 0) and
  r_n(n/log n)^{1/4} ≤ r_n(n log n)^{1/4} → 0; it gives (L-gain-R) with ϖ_n = C_Ln^{−1/2} + 15r_n²/c, and (L-loc-R) holds
  as assumed (r_n → 0).
* (W-R): (D-R) is (D-R^b) (its size hypothesis (N0), |Q| ≤ (log n)^κ, implies (N0^b)), so Lemma P9 gives (W-R).
The conclusions of (C2) are those of RM-0, as for RM-R. Hence RM2-R ⇒ RM-R. ∎

## 5. Consumed claims in this file (registry id@version; statuses verbatim)
W3-RM:RM-0@1.0.0, W3-RM:E4@1.0.0 ("PROVED-CHECKED"): assembly. W2-APP:POST@1.0.1 ("PROVED (by this seat,
unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied"): [POST] for p ≥ 2 — an explicit condition of (C2).
W3-RM:RM-R@1.0.0: its hypotheses only (containment). Not consumed: W3-RM:B9 (the p = 1 endpoint is proved in §3),
W2-LOC2:NA-R and RM's Lemma D-loc (their proofs are re-run in §2 at polynomial size).
