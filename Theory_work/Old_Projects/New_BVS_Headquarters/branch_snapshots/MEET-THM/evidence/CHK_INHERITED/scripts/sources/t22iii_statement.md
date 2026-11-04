# T22(iii): statistical concentration of the composite start

Scope: part (iii) only. This is a restatement for the wave-2 proof run; it does not edit or adopt the source theorem. All scores and probabilities below are exact mathematical objects. Probability P₀ is over the data noise, not the sampler.

## Approved Decision Point 2 change

Felipe mandated EXP → EXP′ (Decision Point 2, D1, 2026-10-22), together with NL_η on the leakage family. This change is already approved by Felipe. The separate Astra statement checker checks fidelity of this restatement only. The old uniform quadratic score assumption is replaced by the uniform logarithmic partial-R² expansion below. Its quadratic specialization on the leakage family and its lower bound for visibility will be proved, not added as hypotheses. D7/NL design constructions, cut groups, part (v), endpoint propagation and algorithm-output guarantees are outside this run.

Restatement-check status: APPROVED by the separate Astra xhigh checker, 2026-10-22, with no corrections; archived in review/statement_check/REPLY.md. No other substantive statement change is proposed.

## 1. Data and exact start law

Consider n → ∞, n ≥ 3, along fixed raw designs Xʳ with p = p_n ≥ 1 nonconstant columns. Let C = I − 11ᵀ/n, let D_x contain their sample standard deviations, and put X = CXʳD_x⁻¹. Thus the centered columns x_j satisfy ‖x_j‖² = n−1. Data satisfy yʳ = α*1 + Xʳβ* + ε, ε ∼ N_n(0, σ²I), with fixed σ² > 0. Write Y = Cyʳ = μ + Cε, μ = CXʳβ* = Xθ*, θ* = D_xβ*, S₀ = supp β*, s₀ = |S₀|. Put s_y² = ‖Y‖²/(n−1), y = Y/s_y (defined almost surely). Here σ denotes the true raw-scale noise standard deviation.

Set K = min(p, ⌊n/2⌋), Ω = {S ⊆ [p]: |S| ≤ K}, B = min(⌊√n⌋, ⌊√p⌋, 16). The blocks C₁,…,C_J are the method's partition, determined by X alone: complete linkage for distance 1−|r_jl| with lexicographic merge ties; top-down splitting of nodes larger than B; next-fit packing of whole retained clusters in dendrogram leaf order. Thus every block has size at most B. Statements about the start are component statements if the production method takes its exact-enumeration branch.

For each S, put G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I, D_S = det(H_S)/det(G_S+I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν = 0.01+n/2. Define

    m(S) = c_n D_S^(−1/2)(0.02+Q_S)^(−ν),
    c_n = (0.02)^0.01 Γ(ν)/(π^(n/2) Γ(0.01)),
    r_b(U) = m(U)/m(∅),  U ⊆ C_b,
    w(k) = 1/[2 binom(2p−1,k)],  W_K = Σ_{k=0}^K binom(p,k)w(k),
    γ₀(S) = [w(|S|)/W_K] ∏_b r_b(S∩C_b),
    π₀(S) = γ₀(S)/Σ_{V∈Ω}γ₀(V),  S∈Ω.

Let P_T be the orthogonal projection onto span(X_T), P_∅ = 0, and U_b* = S₀∩C_b. For every within-block addition (b,T,l), T ⊆ C_b∖{l}, define

    u_{T,l} = (I−P_T)x_l / ‖(I−P_T)x_l‖,
    δ_{T,l} = u_{T,l}ᵀμ,  Z_{T,l} = u_{T,l}ᵀε/σ,
    Δ_T = ‖(I−P_T)μ‖²/(n−1),  v_T = σ²+Δ_T,
    RSS_T = ‖(C−P_T)Y‖²,
    x_{T,l} = (RSS_T−RSS_{T∪{l}})/RSS_T
            = (δ_{T,l}+σ Z_{T,l})²/RSS_T.

The partial R² x is unchanged by response standardization. Under the eigenvalue condition below these residual directions exist, and eventually 0 ≤ x < 1 almost surely. Only sufficiently large n matters for the asymptotic claims. The leakage family is

    L_n = {(b,T,l): l∈C_b∖S₀, U_b* ⊆ T ⊆ C_b∖{l}}.

## 2. Hypotheses

**G and R.** The Gaussian fixed-design model above holds; s₀ is fixed; p ≤ n^A for a fixed A ≥ 1; ‖μ‖²/n ≤ M for a fixed M < ∞; λ_min(X_{S₀}ᵀX_{S₀}/(n−1)) ≥ φ₀² > 0 when S₀ is nonempty; and eventually s₀ ≤ K.

**Within-block SE.** For every nonempty T ⊆ C_b and every b, λ_min(X_TᵀX_T/(n−1)) ≥ φ₀², with a fixed positive φ₀. This is the within-block restriction of SE in the source theorem.

**VIS.** There is a deterministic M_n^V → ∞ such that for every b and T ⊆ C_b with U_b* ⊄ T,

    ‖(P_{T∪U_b*}−P_T)μ‖² ≥ M_n^V v_T log n.

**NL_η.** For a fixed 0 ≤ η < (√(2A+1)−√(2A))², every (b,T,l) ∈ L_n satisfies δ_{T,l}² ≤ ησ² log n. If L_n is empty this condition is vacuous.

**EXP′.** For every within-block addition (b,T,l), including the additions of true variables used in a completion, there are remainders R_{n,b,T,l} such that

    log[r_b(T∪{l})/r_b(T)]
      = −(1/2)log(n+1) − ν log(1−x_{T,l}) + R_{n,b,T,l},
    ρ_n := max_{b,T,l}|R_{n,b,T,l}| = O_{P₀}(1).

This is the uniform actual-block EXP′ assumption mandated by Decision Point 2. There is also an explicitly weaker variant, replacing only ρ_n = O_{P₀}(1) by ρ_n = o_{P₀}(log n); its conclusion has the exponent form stated below. The logarithmic expansion is assumed, not inferred from profiling evidence.

**Rate parameter (NL_avg(κ)).** Fix ε₀ > 0 and h_n = √(2(A+ε₀)log n). For a leakage comparison put

    E_{T,l} = min{δ_{T,l}²/(2Δ_T),
                   δ_{T,l}²/(2v_T)+|δ_{T,l}|σh_n/v_T},

with E_{T,l}=0 if δ_{T,l}=0 (if Δ_T=0 then δ_{T,l}=0). The asserted rate holds for every fixed κ>0 for which, eventually, when p>s₀,

    (p−s₀)⁻¹ Σ_{l∉S₀} max_{U*_{b(l)}⊆T⊆C_{b(l)}∖{l}} exp(E_{T,l})
       ≤ n^(1/2−κ).                                      [NL_avg(κ)]

For p=s₀ use no average condition. In particular NL_η supplies this condition for any ε₀>0 and κ>0 satisfying

    κ ≤ 1/2 − η/2 − √(2η(A+ε₀)).

The strict threshold on η guarantees such positive choices. Equivalently, when η>0, every 0<κ<1/2−η/2−√(2Aη) is supplied by a sufficiently small fixed ε₀>0. Exact zero leakage (η=0) permits κ=1/2. NL_avg is the source theorem's rate condition, with NL_η additionally ensuring the small-partial-R² regime for EXP′.

## 3. Aggregation quantities, with reference S₀

For j≥0, a_bj = Σ_{U_b*⊆U⊆C_b, |U∖U_b*|=j} r_b(U)/r_b(U_b*); define D_b^agg = max_{1≤j≤|C_b∖U_b*|}(j!a_bj)^(1/j), with empty maximum zero. For p>s₀ define

    q_n = (p−s₀)⁻¹ Σ_b D_b^agg,
    u_n = (p−s₀)⁻¹ Σ_{l∉S₀} max_{U*_{b(l)}⊆T⊆C_{b(l)}∖{l}}
                                      r_{b(l)}(T∪{l})/r_{b(l)}(T).

Set q_n=u_n=0 when p=s₀. Define

    e_n = 2p max_{b,U⊆C_b: a=|U_b*∖U|>0}
                         [r_b(U)/r_b(U∪U_b*)]^(1/a),

with empty maximum zero, in particular e_n=0 if s₀=0.

## 4. Precise conclusion: part (iii)

Under Sections 1–2 with the strict EXP′ remainder and any fixed κ satisfying the rate condition:

1. q_n ≤ u_n = O_{P₀}(2^B √(log n) n^(−κ)).
2. For every fixed m>0, e_n = o_{P₀}(n^(−m)).
3. 1−π₀(S₀) = O_{P₀}(2^B √(log n) n^(−κ)+e_n); in particular π₀(S₀) → 1 in P₀-probability.

The random-scale O_{P₀} in item 3 means the ratio to the positive displayed scale is bounded in probability. It also follows that 1−π₀(S₀)=O_{P₀}(2^B√(log n)n^(−κ)).

Under the weaker EXP′ variant, item 1 becomes: for some ξ_n=o_{P₀}(1),

    q_n ≤ u_n ≤ 2^B√(log n)n^(−κ+ξ_n)

on events of probability tending to one. Item 2 is unchanged, and item 3 becomes, for some ζ_n=o_{P₀}(1),

    1−π₀(S₀) ≤ 2^B√(log n)n^(−κ+ζ_n)+s₀e_n

on events of probability tending to one; concentration still follows. Exact zero leakage permits κ=1/2 in both variants.

## 5. Previously proved input and provenance

The only previously proved theorem needed is T22(i), from wave 1: for these positive tables and feasible reference S₀, q_n≤u_n, and on {u_n<1},

    1−π₀(S₀) ≤ (s₀+1)u_n/(1−u_n)+s₀e_n.

It is proved, not adopted, in `proofs/T22_T16_start_aggregation/` and in `proofs/COLLECTED/COLLECTED_PROOFS_v2.tex`, the T22 chapter. Parts (ii) and (iv) are also already proved but are not used here. No unproved v3 conjecture is invoked as a theorem.

Sources read: `theorems/T22_T16_start_aggregation.md` (part (iii)); `theorems/00_COMMON.md` (definitions and G/R/SE/VIS/NL/EXP inventory); `THEORY_BRIEF.md` (especially §2); `RULINGS.md`; `THEOREM_MAP.md`; authoritative `Methodology/SMC_BVS_v3_20261019/METHODOLOGY_v3.md` (§§4–6.3); and `MASTER_Methodology_and_Plan/deployment_20261022_v3/source_snapshots/DP2_DECISIONS.md` (D1 and campaign consequences), a local copy of the Decision Point 2 file named in the brief. The approved Decision Point 2 change supersedes old EXP wording only; the method itself is unedited.
