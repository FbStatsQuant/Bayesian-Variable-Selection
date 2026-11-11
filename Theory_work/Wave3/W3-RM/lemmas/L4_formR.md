# L4 — Form R: bridges (B8a), (B8b), (B9) and Theorem RM-R (claim (C2))

Status: **PROVED (by this seat, unchecked)**, given `L3_SANDR.md` (Lemma SAND-R; parallel prover) and the cited inputs
with their recorded statuses. Setting R and notation: `../STATEMENT.md` §1, §3.2. Sources: LOC2 `lemmas/L1_toolkit.md`
(L0′, L1.2), `L2_NAR.md` (Lemma NA-R), `L5_assembly.md` (Theorem PLR) — each "PROVED (by this seat, unchecked)" with
checks R02/R03/R04 "VERIFIED-WITH-AMENDMENTS", inside W2-LOC2 "PROVED-CHECKED"; APP `lemmas/L1_POST.md` (b)
("PROVED (by this seat, unchecked)", R02 "VERIFIED-WITH-AMENDMENTS", inside W2-APP "PROVED-CHECKED").

## Standing facts in Setting R
(S1) Energy: μ = X_{S₀}θ* and ‖x_k‖² = n − 1, so ‖μ‖² ≤ (Σ_{k∈S₀}|θ*_k|‖x_k‖)² ≤ s₀²θ_hi²(n − 1): the bound ‖μ‖² ≤ Mn
holds surely with M := s₀²θ_hi². (S2) Fixed beta-min: θ*_min ≥ θ_lo > 0. (S3) Sample floors: on the entrywise event
A_X of LOC2 `L1_toolkit.md:45-50` (probability → 1), λ_min(R̂_S) ≥ c/2 for every S with |S| ≤ (log n)^{κ′} and
λ_min(Σ_{n,S}) ≥ c; by (FL-R) this covers S = Q ∪ {l} (|Q ∪ {l}| ≤ (log n)^κ + 1) and every S with |S| ≤ 16 + s₀.

## (B8a) NA-R, and (D-loc) ⇒ (D-R)

**Lemma B8a.** Setting R, deterministic Q ⊇ S₀ with |Q| ≤ (log n)^κ and |Q| ≤ K_n, λ_min(Σ_{n,Q∪{l}}) ≥ c for all l,
and (D-R) (= (R1)–(R3) with the latent-extension contract). Then P(NA(𝓛)) → 1.
*Proof.* (N0), (N1) of LOC2 `L2_NAR.md:23-26` are the listed conditions; Lemma NA-R (`L2_NAR.md:38-41`) gives
P(max_𝔓 Z²_{T,l} ≤ c_n) → 1 and, with the score reduction (L2.2 of the fixed-design source) on the L0′ event of the
lattice family (LOC2 `L1_toolkit.md:37-42`, applied conditionally on X ∈ A_X with the floor of (S3) and the energy bound
(S1), then integrated, LOC2 `L1_toolkit.md:54-56`),
P(NA(𝓛)) → 1. ∎

**Lemma D-loc.** Assume (N0), (N1) and: for every l ∈ [p] a deterministic N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
ν_n = o(log n), and deterministic L_n, η_n with L_n² log(|Q| + 1) = o(log n), η_n → 0, such that for every
(T, l) ∈ 𝔓, with N := T ∩ N_l:
  ‖β̄_{T,l} − β̄_{N,l}‖₁ ≤ L_n  and  Var(W_l | W_N) ≤ (1 + η_n)Var(W_l | W_T)
(β̄ = regression coefficient vector zero-padded to Q; β_{∅,l} = 0). Then (R1)–(R3) hold with no latent extension
(p′ = 0), m₀ = 1.
*Proof.* (The construction of UNI `lemmas/L2_k0.md:139-149` with the ball B_l replaced by N_l.) Frames: for l ∈ [p]
and N ⊆ N_l the single functional ψ_{N,l} := e_l − Σ_{v∈N}β_{N,l,v}e_v (deterministic; λ_min(Σ_{N∪{l}}) ≥ c by (N1)
since N ∪ {l} ⊆ Q ∪ {l}). Number of frames N_n ≤ p·2^{ν_n}, so log N_n ≤ log p + o(log n): (R1) with
ι(T, l) := (l, T ∩ N_l), r_{T,l} = 𝒲ψ_{N,l} = W_l − W_Nβ_{N,l}, ϱ²_{T,l} = Var(W_l | W_N). Atoms: 𝒜_n := {e_v : v ∈ Q},
Var e_v = Σ_vv = 1 (unit diagonal), |𝒜_n| = |Q|; λ_{T,l} := β̄_{T,l} − β̄_{N,l}, supported on T ⊆ Q, so
r_{T,l} − Σ_{v∈Q}λ_{T,l,v}W_v = W_l − W_Tβ_{T,l} = e_{T,l}; L_n as given: (R2). (R3) is the variance hypothesis
(τ²_{T,l} = Var(W_l | W_T)). ∎

## (B8b) TL-R

**Lemma B8b.** Setting R (fixed θ_lo > 0), deterministic Q ⊇ S₀ with |Q| ≤ (log n)^κ, |Q| ≤ K_n, and
λ_min(Σ_{n,Q∪{l}}) ≥ c for all l. Then P(TL(𝓛)) → 1. ((D-R) is not used.)
*Proof.* LOC2 `L1_toolkit.md:33-36`: GROW L2.1 holds on the L0′ event 𝓔_n of the lattice family under the Gram floor
and a fixed beta-min; conditionally on X ∈ A_X the floor is c/2 on Q ∪ {l} ((S3)) and the energy bound is (S1), the
conditional failure probability of 𝓔_n is o(1) uniformly, and one integrates over X (as UNI `lemmas/L2_k0.md:154-155`,
APP `lemmas/L3_LOC.md:158-160`). ∎

## (B9) POST-R
(T1-R) is the LSF hypothesis of APP `lemmas/L1_POST.md` (b); with fixed s₀, p ≤ n^A and the signal bounds of
Setting R it gives 1 − π(S₀) = O_P(√(log n/n)) under the joint law, hence E[1 − π(S₀)] → 0: [POST].
[R07-1] *The case p = 1* (APP `L1_POST.md:9-10` treats p ≥ 2; if p = 1 on a subsequence, argue directly along it).
Then S₀ = [p] = {1}, Ω = {∅, {1}} (K = 1 for n ≥ 2) and w(1)/w(0) = 1/(2p − 1) = 1. With the D0 score (response
scaled to yᵀy = n − 1): Q_∅ = n − 1, and for A = {1}: G_A = n − 1, H_A = n², z_A = x₁ᵀy, Q_A = (n − 1)(1 − r̂²(n − 1)/n),
r̂ := x₁ᵀy/(n − 1) the sample correlation of x₁ and Y. Hence
  F({1}) − F(∅) = −½ log n − ν log[(0.02 + (n − 1)(1 − r̂²(n − 1)/n))/(0.02 + n − 1)].
Y = x₁θ*₁ + Cε with ‖x₁‖² = n − 1, x₁ᵀε/(n − 1) → 0 and ‖Cε‖²/(n − 1) → σ² in probability, so
r̂² → θ*₁²/(θ*₁² + σ²) ≥ θ_lo²/(θ_hi² + σ²) > 0 in probability, and F({1}) − F(∅) ≥ (n/2)·c′ − ½ log n → ∞ with probability
→ 1 (c′ > 0 fixed). So π(S₀) = 1/(1 + e^{F(∅) − F({1})}) → 1 in probability and E[1 − π(S₀)] → 0.

## Theorem RM-R (claim (C2))

Setting R, the method as coded, any X-measurable partition with blocks ≤ 16, premises and configuration of
STATEMENT §1. Assume (T1-R), (FL-R), (V-R), (L-R), (D-R).

*Proof.* [SAND(Q)]: Lemma SAND-R (`L3_SANDR.md`) in the form SAND-R′ of `L3b_rate.md` (localisation rate r_n of
STATEMENT v1.2), from (FL-R), (V-R), (L-R). [NA(Q)]: Lemma B8a ((L-size), (L-feas)
give |Q| ≤ (log n)^κ, |Q| ≤ K_n; the floor on Q ∪ {l} is in (FL-R)). [TL(Q)]: Lemma B8b. [POST]: (B9). Theorem RM-0
(`L0_core.md`) — a statement about any design and deterministic Q with |Q| ≤ K_n — gives all conclusions under the
joint law of (X, ε). ∎

**Relation to Theorem PLR** (LOC2 `STATEMENT.md` (C); UNI `STATEMENT.md` (i′)). PLR assumes P(Sand_n(Q)) → 1 — a
statement about the algorithm's start mode — together with (R1)–(R3). RM-R replaces that hypothesis by the population
conditions (V-R), (L-R) on (Σ_n, θ*) (Lemma SAND-R), replaces e4 by Lemma E4, and states the conclusion for all run
parameters simultaneously. `implies`: PLR's hypotheses with Sand_n supplied by SAND-R ⇐ RM-R's hypotheses;
UNI-0 and LOC-BF are instances (`L7_examples.md`).
