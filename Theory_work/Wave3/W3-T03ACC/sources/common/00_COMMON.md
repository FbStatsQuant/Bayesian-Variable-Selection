# 00_COMMON.md — shared definitions for every theorem file in this folder

Status of everything in this folder: **conjectured, not proven.** Methodology: SMC-BVS v3.0 of 2026-10-19, `C:\Users\felip\OneDrive\Documents\Local_to_global_Bayesian\01_Methodology_and_Theory\Methodology\SMC_BVS_v3_20261019\METHODOLOGY_v3.md`, SHA-256 `93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c`. The exact algorithm (blocks, tables, composite start, bridge, pilot, candidate grid, final run, local search, statuses) is written out in `..\THEORY_BRIEF.md` §2; the method file is authoritative. Each theorem file `T<k>_<name>.md` names the definitions and inventory codes it uses; give proof.md the theorem file, this file, THEORY_BRIEF.md and the method file (all by path).

Felipe's fixed decisions (no theorem changes them): the target (standardised X, y; β_S ~ N(0, nσ²(G_S+I)⁻¹); σ² ~ IG(0.01, 0.01); BB(1, p) capped at K = min(p, ⌊n/2⌋)); the HPM over all scored models with exact-equality ties; B = min(⌊√n⌋, ⌊√p⌋, 16); neighbour threshold ρ_n = √(2 log p/n); no secondary prior arm; the budgets of METHODOLOGY §3.

## 1. Data, target, decision objects

- Raw data (X^r, y^r), n ≥ 3, no constant column, non-constant y^r. C = I − 11ᵀ/n; D_x = diag of retained raw column sample SDs. Standardised X = CX^rD_x⁻¹, y = Cy^r/s_y with s_y² = ‖Cy^r‖²/(n−1); so ‖x_j‖² = ‖y‖² = n − 1. Contrast coordinates: U ∈ ℝ^{n×(n−1)}, UᵀU = I, UUᵀ = C; y_c = Uᵀy^r, X_c = UᵀX.
- State space Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). G_S = X_SᵀX_S = (n−1)R_S; z_S = X_Sᵀy; H_S = (n+1)G_S + I; D_S = det H_S/det(G_S+I); Q_S = yᵀy − n z_SᵀH_S⁻¹z_S; ν = 0.01 + n/2; a₀ = b₀ = 0.01.
- m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}; w(k) = ½/C(2p−1, k); W_K = Σ_{k≤K} C(p,k)w(k); ϖ(S) = w(|S|)/W_K.
- F(S) = log[ϖ(S)m(S)]; Z = Σ_Ω ϖ(S)m(S); π(S) = e^{F(S)}/Z; BF(S) = m(S)/m(∅).
- Global HPM S† = argmax_Ω F (ties: smallest size, then lexicographic). Reported HPM Ŝ = the same rule over 𝒮, the set of all models ever scored (calibration, final run, rejected proposals, local scans); 𝒮_cal ⊆ 𝒮 is the calibration's scored set. PIP_j = π(j ∈ S); MPM = {j : PIP_j > ½}.
- Statistical model: y^r = α*1 + X^rβ* + ε; μ = CX^rβ* = Xθ*, θ* = D_xβ*; S₀ = supp β*, s₀ = |S₀|. Contrast-scale parameters θ = s_yβ, v = s_y²σ². P₀ is over ε; "joint probability" adds the algorithm's randomness. r_n := √(log n/n). m_n(ω) := ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ω)/log 2⌉, m_n := m_n(½ log n).

## 2. Sampler objects

- Blocks C₁, …, C_J (deterministic in X: complete linkage, top-down cut, next-fit packing), |C_b| ≤ B = min(⌊√n⌋, ⌊√p⌋, 16). Tables r_b(A) = BF(A) for A ⊆ C_b (full response).
- γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b); π₀ = γ₀/Z̄₀ (Z̄₀ by exact convolution of block size profiles with the capped size prior; backward sampler gives exact iid π₀ draws). Start mode S̃₀ := argmax π₀.
- Discrepancy d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b). Bridge γ_φ = γ₀e^{φd}, q_φ = γ_φ/Z̄_φ (defined for real φ; production φ ∈ [0,1]); q₀ = π₀, q₁ = π, Z = m(∅)Z̄₁.
- Round K_φ: m = p + B + 2 labelled steps in a uniformly random order: p Gibbs flips (o_j(S, φ) = pre-draw inclusion probability of j at S; a_j(S,φ) = γ_φ(S+j)/γ_φ(S)), one uniform swap, B neighbour swaps (symmetric-union neighbour graph N(·) at threshold ρ_n), one independence proposal from π₀. Elementary kernels K_e; reflected kernels K_e^W(x,A) = K_e(x, A∩W) + K_e(x, W^c)1_A(x).
- Calibration 𝓒 := (grid 0 = φ₀ < … < φ_T = 1, T, L, N_e, tier e, candidate set V, every V-independent setting), measurable w.r.t. streams 0–9; final streams 10–13 are fresh; escalation is decided before final randomness. Δ_t = φ_t − φ_{t−1}; w_t = 2φ_t − φ_{t−1}; 𝓔_grid = {φ₀,…,φ_T, w₁,…,w_T}. Restricted ESS ρ_V(u,v) = Z̄_v(V)²/(Z̄_u(V)Z̄_{2v−u}(V)).
- Final run: 4 fresh islands × N_e iid π₀ draws; frozen grid; multinomial resampling after every reweighting; one round per stage; L burn-in rounds and 4 measured rounds at φ = 1; local search (≤ ℓ moves, scans score every feasible flip and swap of the centre). Outputs: Ẑ_r (island evidence), Ẑ = ¼Σ_rẐ_r, bound 0.05Ẑ; PIP̂_{rj} = Rao–Blackwell average of the pre-draw Gibbs conditionals over the 4 measured rounds; primary PIP̂_j (equal weight), secondary (Ẑ_r-weighted); MPM̂; Ŝ; statuses {exact, completed, schedule_limit, numerical_failure, resource_limit, y_constant, no_predictors, invalid_input}; flags (E1–E3, low_empirical_ESS, local_certified, global_certified, …).
- Budgets: N₀ = max(2500, n, p); H₀ = ⌈512N₀/2500⌉; ℓ = ⌈log₂(n+p+1)⌉; T₀ = max(1000, ℓ²); (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), e ∈ {0,1}; L = max(4, ⌈log₂(n+1)⌉). Q_f := 4N_e(T + L + 5) iid π₀ draws scored in the final run (initialisation + independence proposals); 4N_e(L+6) ≤ Q_f ≤ 4N_e(T_e + L + 5).
- Exact branch: Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)p; it precedes block/Gram construction and scores every feasible model.
- Stage notation: q_t = q_{φ_t}, G_t = e^{Δ_t d}, Z_t = m(∅)Z̄_{φ_t}; q̂_t = empirical population after stage-t resampling and mutation; Ẑ_{r,t} = island r's evidence product through stage t. Reflected normalisation on W: q_t^W = q_t(·|W), g_t^W = G_t/[Z̄_{φ_t}(W)/Z̄_{φ_{t−1}}(W)], 𝒬^W_{s,t} = ∏_{j=s+1}^t (g_j^W K_j^W); comparator mean with the original start normaliser Z·r_W, r_W = q₁(W)/q₀(W).
- Leakage quantities: u_{T,l} = unit residual of x_l on X_T; δ_{T,l} = u_{T,l}ᵀμ; Δ_T = ‖(I−P_T)μ‖²/(n−1); v_T = σ*² + Δ_T; h_n = √(2(A+ε) log n); E_{T,l} = min{δ²_{T,l}/(2Δ_T), δ²_{T,l}/(2v_T) + |δ_{T,l}|σ*h_n/v_T} (E_{T,l} = 0 when δ_{T,l} = 0).
- Truth stability: δ₁ = 1 − π(S₀); u_π = δ₁/π(S₀); ρ_* = min{1, (B+3)u_π}.
- Regimes: R1: n → ∞, s₀ fixed, p ≤ n^A. R2: p fixed (SMC statements are component results; the exact branch eventually applies). R3: data and 𝓒 fixed, N or the island count varies (idealised). R4: actual budgets along R1. Fixed-data identities condition on a successful frozen 𝓒, never on passing later diagnostics.

## 3. Assumption inventory (codes used by the theorem files)

| Code | Condition | Status |
|---|---|---|
| G | Fixed design; ε ~ N_n(0, σ*²I), σ*² > 0 fixed; intercept removed by contrasts. | Standard/project (paper_draft §2); external precedent UNVERIFIED |
| R | s₀ fixed; p ≤ n^A, A ≥ 1; ‖μ‖²/n ≤ M; λ_min(R_{S₀}) ≥ φ₀² > 0; eventually s₀ ≤ K. | Project bundle (paper_draft T6); truth-dependent |
| SE | λ_min(R_T) ≥ φ₀² for every nonempty T with |T| ≤ min(p, m_n + s₀). | Project (proofs T7_T8 §1, T9_C9 §9); strong; not checkable exhaustively |
| BM-C | min_{j∈S₀} θ*_j² ≥ M_*σ*² log n/(nφ₀²), M_* = 2L_*+1, L_* = max{4C_*, 32[s₀(A+1)+2]}, C_* = 2s₀ + 3[Aj_* + s₀ + log(j_*+1) + 1], j_* = ⌈(2A+1)s₀⌉ + 1. | New candidate fixed constant (J1 audit of the project proof; provisional); the proving run may replace M_* |
| BM-∞ | Same inequality with M_n → ∞ in place of M_*. | Project sufficient condition (v2's BM) |
| DX | min retained raw column SD ≥ d₋ > 0. | New; observable |
| GL | R_{S₀} → Γ₀ ≻ 0 with consistent support ordering. | Project limit form; generic BvM precedent UNVERIFIED |
| ORTH | G = (n−1)I_p (so p ≤ n−1); for A4: fixed 1 ≤ s₀ < p, equal magnitudes b_n on S₀, b_n²/σ*² bounded. | Project benchmark (P4/Pb1); observable |
| COH | c_n = max_{i≠j}|r_ij|, c_n log(p∨n) → 0, s₀c_nθ_max/θ_min → 0. | New; optional |
| DUP | Exact signed duplicate columns; or two Gaussian truths with ‖μ₁−μ₂‖/σ* → 0. | New alternative regimes |
| NIS | No distinct feasible S ≠ S′ with X_SX_Sᵀ = X_{S′}X_{S′}ᵀ (equal sizes then follow from traces). | New; decidable from X |
| VIS | For U_b* = S₀∩C_b ⊄ T ⊆ C_b: ‖(P_{T∪U_b*} − P_T)μ‖² ≥ M_n^V v_T log n, M_n^V → ∞. | New actual-block visibility; not implied by SE/BM |
| NL_avg(κ) | (p−s₀)⁻¹Σ_{l∉S₀} max_{U*_{b(l)}⊆T⊆C_{b(l)}∖l} e^{E_{T,l}} ≤ n^{½−κ}, fixed κ > 0. | New; Gaussian-design prevalence UNVERIFIED |
| NL_η / TL | Sufficient cases: δ²_{T,l} ≤ ησ*² log n with η < (√(2A+1) − √(2A))², over the block comparisons (NL_η) or a target-state family (TL). | New explicit threshold |
| TL_avg(κ; 𝓡) | For every T ∈ 𝓡, the average of e^{E_{T,l}} over l ∉ S₀∪T is ≤ n^{½−κ}. | New; uniform before selection |
| EXP | Uniform actual-block expansion: log[r_b(T+l)/r_b(T)] ≤ −½ log(n+1) + (δ_{T,l} + σ*Z_{T,l})²/(2v_T) + R_n, Z_{T,l} = u_{T,l}ᵀε/σ*; R_n = O_P(1) (strict rate) or o_P(log n) (exponent rate); plus a uniform lower gain bound c·gain/v_T − CB log n for visibility. | New explicit proof obligation (J5) |
| AGG | For feasible S°, s = |S°|, U_b* = S°∩C_b: a_bj = Σ_{U⊇U_b*, |U∖U_b*|=j} r_b(U)/r_b(U_b*); D_b = max_{j≥1}(j!a_bj)^{1/j}; q = (p−s)⁻¹Σ_bD_b; e = 2p max_{b,U: a=|U_b*∖U|>0}[r_b(U)/r_b(U∪U_b*)]^{1/a}. Hypothesis q < 1. Conventions: empty maxima are 0; q = 0 if s = p; e = 0 if s = 0. | New deterministic table condition |
| BO | X_{C_b}ᵀX_{C_b′} = 0 for b ≠ b′. | New benchmark; observable |
| ONE | S̃₀ and S₀ differ by one flip, or by a same-block proxy swap with |r_{ij′}| > ρ_n. 𝔓 = {S̃₀, S₀}. | Project case definition |
| LK_d | 𝓡_d = {U∪P : U ⊆ S₀, P ⊆ S₀^c, |P| ≤ d}, fixed d, s₀+d ≤ K; Λ = max_{T∈𝓡_d}Σ_{l∉S₀∪T} o_l(T,1); (L+4)2^{s₀+d}Λ → 0. | New, truth-dependent |
| EXIT_d | ξ = max over starts in 𝓡_d of the one-round probability that the first exit from 𝓡_d is caused by a non-Gibbs label; (L+4)ξ → 0. | New; does not bound internal non-Gibbs changes |
| GAIN_d | Uniform best missing-true addition gain g⁺ → ∞ and uniform best extra-deletion gain g⁻ → ∞ from proper supersets, over 𝓡_d. | New; multi-extra deletion not derived |
| BASIN(𝓡, r₀, a, η, ρ, δ) | Given 𝓒: 𝓡 ∋ S₀; inf_{x∈𝓡}K₁^{r₀}(x, S₀) ≥ a; one-round basin first exit ≤ η; truth prefix-departure ≤ ρ; expected stage-T outside fraction ≤ δ. | New abstract conditions |
| BOCC(d) | With probability → 1 all specified pilot/final elementary states have size ≤ d. | New; insufficient alone |
| EX-A | Exact scores, convolutions, probabilities, comparisons. | Declared idealisation |
| EX-S | Independent ideal uniform streams with the method's stream separation. | Declared idealisation |
| CAL | 𝓒 uses streams 0–9 only; streams 10–13 fresh; escalation before final randomness. | Method construction (M §§6.8–6.9) |
| SR | Each Gibbs update evaluates both feasible configurations (incl. the current one); both count as scored. | Scoring reading of M §§6.5, 6.10 (to be confirmed by Felipe) |
| COVER(W, ε_C) | q_ψ(W) ≥ 1 − ε_C at every ψ ∈ 𝓔_grid. | New full-space coverage |
| HIT | A specified scoring route succeeds with probability → 1 (e.g. Q_fπ₀(S₀) → ∞, table inclusion, scanned one-neighbour centre). | New conditional route |
| PX | On no prior discovery, ≥ ω_n k(p−k) uniform-swap executions at S̃₀ occur with probability → 1, ω_n → ∞. | New occupancy condition |
| CPL-E | Common-randomness coupling with the reflected particle system through all populations/ancestors used by the last weight evaluation, failure h_E; sufficient bound: initial mismatch + Σ_e E[1{τ>e⁻}K_e(X_{e⁻}, W^c)]. | New particle-system obligation |
| CPL-H / RB | HPM transfer: couple all scored proposals and scans. PIP transfer: couple recorded rewards or bound the reward discrepancy. | New output-specific obligations |
| MISS-E | Data-measurable 𝓜, ∅ ∉ 𝓜; calibration scores avoid 𝓜; CPL-E for W = 𝓜^c with h_E → 0. | New conditional loss hypothesis |
| MISS-H | Calibration avoidance plus avoidance of every subsequent scoring opportunity, failure h_H → 0; RB condition for PIP conclusions. | New |
| RET / OCC | RET: return visits from neighbours of 𝔓. OCC: expected outside fractions ≤ Cq_t or specified weighted slacks. | New first-moment conditions; not variance premises |
| BW2 | ∫q^W_{t−1}(dx)[g_t^W(x)]²K_t^W(x,dy)K_t^W(x,dz) ≤ C_t q_t^W(dy)q_t^W(dz). | New two-lineage domination |
| BW_W | sup_{s<t}sup_x 𝒬^W_{s,t}1(x)/inf_x 𝒬^W_{s,t}1(x) ≤ C₀. | New future-weight control |
| WS | Working set W; terminal initial law λ ≤ wπ(·|W); reflected terminal round has absolute gap g > 0; sup_{s<t,x}𝒬^W_{s,t}1(x)/q_s^W(𝒬^W_{s,t}1) ≤ a_n. | New |
| PW2 | With W_t = Ẑ_t/Z_t: E[W²_{t−1}{(q̂_{t−1}g_t)² − 1}] ≤ (a_t/N)EW²_{t−1} + ν_t with controlled slack. | New research obligation |
| OP-a / OP-s | Preflight passes under the allocation; / schedule failure probability → 0 when final outputs are needed. | New operational conditions |
| NUM | Simultaneous error bound η for all compared log scores at fixed n. | New validation contract |
| NDR | No limiting finite bisection comparison equals the ESS threshold; no limiting pilot increment equals the floor. | New nondegeneracy |
| STIFF | Two-state restricted law, high-discrepancy mass a, gap D: ρ(a, D(b−u)2^{−60}) < 0.9, ρ(a,x) = [a+(1−a)e^{−x}]²/[a+(1−a)e^{−2x}]. | Corrected mass-qualified obstruction |
| UB | Externally justified upper bound U ≥ Z. | Optional external input |

Retired as hypotheses: MASS; AGG-stat (a conclusion); ζ-EXIT; OP's numerics clause; V≤, OT-lb, NA (optional research ideas only). Regimes are not declared universally disjoint; exact duplicates conflict with SE and NIS; ORTH excludes p > n.
