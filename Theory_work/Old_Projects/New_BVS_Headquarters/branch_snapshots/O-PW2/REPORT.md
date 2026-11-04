# O-PW2 — a PW2-free variance bound for the island evidence ratio

Run: O-PW2 (Opus 5.5), branch `theory/O-PW2`, 2026-11-02. All proofs here are **candidates**: not reviewed, not adopted.

## 1. Headline

1. **PROVED (candidate). Theorem A, exact variance identity.** For the actual v3 stage structure, for any q_t-invariant round kernels:
   - N·Var_c(W_T) = Σ_{s<T} (1−1/N)^{T−1−s} (E_c[W_s² μ_s(h²_{s,T})] − 1);
   - equivalently, N·Var_c(W_T) = Σ_{s<T} E_c[W_s² Var_{μ_s}(h_{s,T})].

   Here h_{s,T} is the future-weight function and μ_s is the conditional child law. No mixing assumption is used.
2. **PROVED (candidate). Theorem B, two-sided non-asymptotic bound.** |N·Var_c(W_T) − Σ_s (1−1/N)^{T−1−s} σ²_{s,T}| ≤ Σ_{s≥1} H²_{s,T} √(V_s(1+V_s)). This gives an explicit closed recursion U_T ≥ Var_c(W_T). The leading term is the asymptotic variance σ²_T/N; the error is O(N^{−3/2}).
   - It delivers T25(iv)'s **conclusion** directly, including the /4 for pooling, with PW2 removed as a hypothesis.
   - It also gives PW2 itself with explicit a_t and ν_t (Corollary B2).
3. **PROVED (candidate). Theorem C, constants from stage primitives.**
   - σ²_{s,T} obeys an L² recursion in four stage constants: χ²_t (T13-certified), δ²_t, ḡ_t = max g_t, and the L² mixing defect λ_t (T09(iv) gives λ_t ≤ 1−ε_t).
   - H_{s,T} obeys a sup-norm recursion in ε_t (T09(iv)) and ḡ_t.
   - With exact refresh (λ = 0) it reduces to Π(1+χ²_t/N) − 1.
4. **Not vacuous at the study's N and T only conditionally.** It needs an L² mixing condition, λ_t(1 + ḡ_tλ_t) ≤ κ < 1, and sup-norm control of h_{s,T} (BW_W on Ω). Neither is implied by the locked T09 constant, which is exponentially small (T09(v)). With only locked inputs, Theorem C grows geometrically in T: **vacuous at study scale.**
5. **Evidence (exact enumeration, p ≤ 10).** Theorem A holds to machine precision, and Theorems B and C hold in every case and at every N. The minimal PW2 constants a_t* can be several times χ²_t. So **PW2 with a_t = χ²_t (the "perfect-mixing" guess) is false**, a numerical COUNTEREXAMPLE: p=6 Gibbs-only kernel, a_4* = 0.90 against χ²_4 = 0.111. The constants of `helpers/OPTIONAL_PW2.md` (B)–(C) make T25(iv)'s B_T vacuous (≈ 1–223, vs truth ≤ 0.1) in every case.

## 2. Setting and notation

Everything is as in `Docs/Theory/proofs/T25iv_T19_crossing_evidence/STATEMENT.md`: fixed data, a successful frozen calibration c, one island, and N = N_e. The definitions of q_t, G_t, c_t, g_t = G_t/c_t (so q_{t−1}(g_t) = 1), Ẑ_t, W_t = Ẑ_t/Z_t and W_0 = 1 are all from there. K_t is the v3 round kernel at φ_t: a uniformly random order, q_t-invariant and q_t-reversible (T09(iii)). EX-A, EX-S, CAL.

New symbols (all deterministic given c):
- 𝓕_t: the σ-field of the island's randomness up to and including q̂_t (after the stage-t mutation), t ≥ 0.
- λ_{t−1} := G_t q̂_{t−1} / q̂_{t−1}(G_t), the weighted parent law. μ_t := λ_{t−1}K_t for t ≥ 1, and μ_0 := q_0. **Fact F**: given 𝓕_{t−1}, the N particles of q̂_t are iid μ_t. Multinomial ancestors are iid λ_{t−1} and mutations are independent (EX-S). At t = 0 the particles are iid q_0 (T09(i)).
- Q_t f(x) := g_t(x)(K_t f)(x).
- h_{s,T} := Q_{s+1}⋯Q_T 1 for 0 ≤ s ≤ T, with h_{T,T} = 1, so h_{T−1,T} = g_T and h > 0.
- σ²_{s,T} := Var_{q_s}(h_{s,T}). H_{s,T} := max_Ω h_{s,T}. σ²_T := Σ_{s=0}^{T−1} σ²_{s,T}.
- V_t := Var_c(W_t), v_t := E_c W_t² = 1 + V_t.
- Stage constants:
  - χ²_t := q_{t−1}(g_t²) − 1 = χ²(q_t‖q_{t−1});
  - δ²_t := q_t((g_t − 1)²) = q_{t−1}(g_t³) − 1 − 2χ²_t ≤ ḡ_t χ²_t;
  - ḡ_t := max_Ω g_t;
  - λ_t := ‖K_t − Π_t‖_{L²(q_t)→L²(q_t)}, where Π_t f = q_t(f);
  - ε_t := ε_{φ_t} of T09(iv), so K_t(x,·) ≥ ε_t q_t(·).

**Lemma 1.** q_{t−1}(Q_t f) = q_t(f). Hence q_s(h_{s,T}) = 1 for every s ≤ T.

*Proof.* q_{t−1}(g_t ·) = q_t(·) as measures, because q_{t−1}G_t/c_t = γ_{φ_t}/Z̄_{φ_t}. Then q_t K_t = q_t. Induct downward from h_{T,T} = 1. ∎

**Lemma 2.** For t ≥ 1, W_t = W_{t−1} q̂_{t−1}(g_t), and W_t μ_t(f) = W_{t−1} q̂_{t−1}(Q_t f) = E[W_t q̂_t(f) | 𝓕_{t−1}]. Also E_c[W_t q̂_t(f)] = E_c[W_t μ_t(f)] = q_t(f).

*Proof.*
- Ẑ_t/Z_t = (Ẑ_{t−1}/Z_{t−1}) · q̂_{t−1}(G_t)/c_t.
- μ_t f = q̂_{t−1}(g_t K_t f)/q̂_{t−1}(g_t); multiply by W_t.
- The conditional expectation follows from Fact F, since W_t is 𝓕_{t−1}-measurable.
- Iterate down to E[q̂_0(f')] = q_0(f') and apply Lemma 1. (This is the product-form unbiasedness of T12(i.a), re-derived here.) ∎

## 3. Statements and proofs

### Theorem A (exact identities). PROVED (candidate).

Set Γ_s(f) := W_s q̂_s(f), M_s := Γ_s(h_{s,T}) for 0 ≤ s ≤ T−1, and M_{−1} := 1. Then:

(A1) (M_s)_{s=−1}^{T−1} is an (𝓕_s)-martingale with M_{T−1} = W_T. Moreover W_s μ_s(h_{s,T}) = M_{s−1}.

(A2) Var_c(W_T) = (1/N) Σ_{s=0}^{T−1} E_c[W_s² Var_{μ_s}(h_{s,T})].

(A3) Var_c(W_T) = (1/N) Σ_{s=0}^{T−1} (1−1/N)^{T−1−s} (e_s − 1), where e_s := E_c[W_s² μ_s(h²_{s,T})] and e_0 = q_0(h²_{0,T}).

(A4) PW2's left side is exactly a variance increment: E_c[W²_{t−1}{(q̂_{t−1}g_t)² − 1}] = V_t − V_{t−1}.

*Proof.*
- **M_{T−1} = W_T.** Γ_{T−1}(h_{T−1,T}) = W_{T−1} q̂_{T−1}(g_T) = W_T by Lemma 2.
- **Martingale.** For s ≥ 1, Lemma 2 and Q_s h_{s,T} = h_{s−1,T} give E[M_s | 𝓕_{s−1}] = W_s μ_s(h_{s,T}) = Γ_{s−1}(h_{s−1,T}) = M_{s−1}. For s = 0, E M_0 = q_0(h_{0,T}) = 1 = M_{−1} (Lemma 1).
- **Increments.** D_s := M_s − M_{s−1} = W_s(q̂_s(h_{s,T}) − μ_s(h_{s,T})). Everything is bounded (finite Ω), so the D_s are orthogonal and E W_T = 1. Hence Var W_T = Σ_s E D_s².
- **(A2).** By Fact F, E[D_s² | 𝓕_{s−1}] = W_s² Var_{μ_s}(h_{s,T})/N.
- **(A3).** E[W_s²(μ_s h_{s,T})²] = E M²_{s−1} =: m_{s−1}, by (A1). So E D_s² = (e_s − m_{s−1})/N and m_s = m_{s−1} + E D_s². Hence m_s − 1 = (1−1/N)(m_{s−1} − 1) + (e_s − 1)/N with m_{−1} = 1. Unroll this, and use Var W_T = m_{T−1} − 1.
- **(A4).** E[W²_{t−1}(q̂_{t−1}g_t)²] = E W_t² by Lemma 2, and E W²_{t−1} = 1 + V_{t−1}. ∎

(A4) shows that PW2 is precisely a hypothesis on the growth v_t ≤ (1+a_t/N)v_{t−1} + ν_t. Theorem A computes that growth instead of assuming it.

### Theorem B (two-sided non-asymptotic bound). PROVED (candidate).

(B1) For every T ≥ 1:

  |N·V_T − Σ_{s=0}^{T−1} (1−1/N)^{T−1−s} σ²_{s,T}| ≤ Σ_{s=1}^{T−1} (1−1/N)^{T−1−s} H²_{s,T} √(V_s(1+V_s)).

There is no s = 0 error term; in particular V_1 = χ²_1/N exactly.

(B2) Define U_0 := 0 and, recursively,

  U_t := (1/N) Σ_{s=0}^{t−1} (1−1/N)^{t−1−s} [σ²_{s,t} + 1{s≥1} H²_{s,t} √(U_s(1+U_s))].

Then V_t ≤ U_t for every t ≤ T. Under the four final islands (T12(iv.c): independent given c), Var_c(Ẑ/Z) ≤ U_T/4.

(B3) Closed form. Put x := max_{t≤T} σ²_t/N and y := max_{t≤T} (1/N) Σ_{s=1}^{t−1} H²_{s,t}. If 2y²(1+2x) ≤ x, then for every t ≤ T:
- V_t ≤ U_t ≤ 2x, and
- V_T ≤ σ²_T/N + y√(2x(1+2x)) = σ²_T/N + O(N^{−3/2}).

*Proof.*
- **(B1).** For s ≥ 1:
  - e_s = E[W_s μ_s(h²)] + E[W_s(W_s − 1)μ_s(h²)].
  - The first term equals q_s(h²_{s,T}) = 1 + σ²_{s,T} by Lemma 2.
  - The second has absolute value at most H²_{s,T} E[W_s|W_s − 1|] ≤ H²_{s,T} √(V_s v_s), by Cauchy–Schwarz and E W_s = 1.
  - For s = 0, e_0 − 1 = σ²_{0,T} exactly.
  - Insert these into (A3).
- **(B2).** By induction on t: the right side of (B1)'s upper bound is nondecreasing in each V_s, s < t, and V_s ≤ U_s.
- **Pooling.** W_pool is the mean of four iid copies.
- **(B3).** By induction, U_t ≤ x + y·max_{s<t} √(U_s(1+U_s)) ≤ x + y√(2x(1+2x)) ≤ 2x; the last step is the hypothesis. ∎

**Corollary B2 (PW2 itself, explicit).**

- Write η_t := Σ_{s=1}^{t−1} H²_{s,t} √(U_s(1+U_s)) and S_t := Σ_s (1−1/N)^{t−1−s} σ²_{s,t}.
- By (B1) and (A4), N(V_t − V_{t−1}) ≤ S_t − S_{t−1} + η_t + η_{t−1}.
- So PW2 holds with a_t := (S_t − S_{t−1})_+ and ν_t := (η_t + η_{t−1})/N. This uses v_{t−1} ≥ 1.
- The slack ν_t = O(N^{−3/2}), and a_t → (σ²_t − σ²_{t−1})_+ as N → ∞.
- So PW2 is **true with O(1) rate constants** in the finite-state v3 setting. The rate constant is the increment of the asymptotic variance, **not** χ²_t.
- T25(iv) fed with these constants is weaker than (B2) used directly; we recommend (B2).

### Theorem C (primitive constants: T13's χ², T09's ε, an L² mixing defect). PROVED (candidate).

(C1) σ²_{T−1,T} = χ²_T. For 1 ≤ t ≤ T−1:

  σ²_{t−1,T} ≤ χ²_t + 2δ_tλ_t σ_{t,T} + ḡ_tλ_t² σ²_{t,T} ≤ χ²_t + λ_tδ²_t + λ_t(1 + ḡ_tλ_t) σ²_{t,T}.

Here σ_{t,T} := (σ²_{t,T})^{1/2}.

(C2) H_{T,T} = 1, and H_{t−1,T} ≤ ḡ_t(ε_t + (1−ε_t)H_{t,T}).

(C3) Suppose for all t: χ²_t + λ_tδ²_t ≤ c̄ and κ_t := λ_t(1 + ḡ_tλ_t) ≤ κ < 1. Then σ²_{s,T} ≤ c̄/(1−κ) and σ²_T ≤ Tc̄/(1−κ). If also ḡ_t(1−ε_t) ≤ θ < 1, then H_{s,T} ≤ ḡ*/(1−θ), where ḡ* := max_t ḡ_t.

(C4) Exact refresh (K_t = Π_t, so λ_t = 0 and ε_t = 1): h_{s,T} = g_{s+1}, σ²_{s,T} = χ²_{s+1}, and Theorem A gives exactly V_T = Π_t(1+χ²_t/N) − 1.

T13(ii)(b) and (iii): under COVER(V, ε_C), 1 + χ²_t ≤ 10/(9(1−ε_C)²); with ε_C = 0 this is χ²_t ≤ 1/9.

*Proof.*
- **Setup.** Write h_{t,T} = 1 + f with q_t f = 0 (Lemma 1), so ‖f‖²_{q_t} = σ²_{t,T}. Then h_{t−1,T} = g_t(1 + K_t f).
- **Expansion.** Using q_{t−1}(g_t ·) = q_t(·):

  1 + σ²_{t−1,T} = q_{t−1}(g_t²) + 2q_t(g_t K_t f) + q_t(g_t (K_t f)²).

- **Cross term.** q_t(K_t f) = 0, so q_t(g_t K_t f) = q_t((g_t − 1)K_t f) ≤ δ_t‖K_t f‖ ≤ δ_tλ_tσ_{t,T}.
- **Last term.** It is at most ḡ_tλ_t²σ²_{t,T}. Then 2δλσ ≤ λ(δ² + σ²) gives (C1).
- **(C2).** T09(iv) gives K_t(x,·) = ε_t q_t + (1−ε_t)R_t(x,·) with R_t stochastic. So K_t h ≤ ε_t q_t(h) + (1−ε_t) max h, and q_t(h_{t,T}) = 1.
- **(C3).** Induct downward with the fixed points of the two affine recursions.
- **(C4).** Since K_t h = q_t(h) = 1, h_{s,T} = g_{s+1}. Then e_s = v_s(1+χ²_{s+1}), because μ_s = q_s is deterministic. So (A3) becomes V_{t} = (1+χ²_t/N)v_{t−1} − 1, by the same unrolling. ∎

**Remark (where the sup norms enter).** Both ḡ_t in (C1) and H_{s,T} in (B) come from one source: the particle law μ_s is not q_s. The term q_t(g_t u²) equals (1+χ²_t)·q_{w_t}(u²), where w_t = 2φ_t − φ_{t−1} is T13's evaluation point. So ḡ_t in (C1) can be replaced by (1+χ²_t)·λ^{(w)}_t²/λ_t², where λ^{(w)}_t := ‖K_t − Π_t‖_{L²(q_t)→L²(q_{w_t})}. That is a two-temperature mixing constant on the T13 grid.

## 4. Is it non-vacuous at the study's N and T?

**Budgets.** N = N_e ≥ 2500 and T ≤ T_e = 4^e·max(1000, ℓ²). For any n + p < 2³¹, ℓ² ≤ 961, so T_e/N_e ≤ 1000/2500 = 0.4.

**Under the L² mixing condition.** Suppose (C3) holds with c̄ = 1/9 + λδ² and κ ≤ 1/2. Then the leading term is σ²_T/N ≤ 0.4·2c̄ ≈ 0.09 per island at the very worst T/N, and pooling gives ≤ 0.02. That is a relative SD of about 0.15 for Ẑ/Z. Realised grids (T ≪ T_e) give much less.

**The correction term.** It is negligible once N ≳ 2T²H⁴/σ² (B3), so this needs H_{s,T} = O(1). That is exactly the full-space version of the inventory's **BW_W** (sup h/inf h ≤ C₀). Since q_s(h) = 1, BW_W gives H_{s,T} ≤ C₀.

**What fails with locked inputs only.**
- T09 gives λ_t ≤ 1−ε_t, and ε_t is exponentially small in n for realistic data (T09(v)). Then κ_t ≈ 1 + ḡ_t > 1: the recursion (C1) grows like Π ḡ_t, and (C2) likewise.
- **Verdict: with only locked T09/T13 inputs, the bound is valid but vacuous at study scale.** It becomes informative under an L²-mixing premise, λ_t(1+ḡ_tλ_t) ≤ κ < 1 (or the two-temperature variant), plus BW_W.
- T09(v) proves the true gap can be ≥ 1/40 even when ε_t is exponentially small. So this premise is not hopeless, but it is not established. ḡ_t is also not controlled by any ESS statement.
- **(b) realised-grid ESS route.** T13 controls only χ²_t. Theorem C shows that χ²_t alone cannot control σ²_T (see the numbers in §5: σ²_T can be 20× Σχ²_t). So a condition stated **only** via the realised grid's ESS cannot give a bound. It must be paired with a mixing constant.

## 5. Evidence: exact enumeration (p ≤ 10)

Script: `scripts/pw2_exact.py <p> <corr> <kernel> [seed] [ess_thr]`, seed 20261102. Results are in `results/*.json` and `results/log_*.txt`.

**Data and setup.**
- Data: n = 60; AR(corr) Gaussian design; three true effects. Score m(S), BB(1,p) prior and B are exactly as in 00_COMMON.
- Blocks: contiguous groups of size ≤ B. This replaces complete linkage, and it does not matter for the theorems.
- Grid: greedy largest step with ρ_Ω ≥ thr, 60 bisections (§6.7 rule with V = Ω).

**Kernels.**
- `full`: the v3 round. For p = 6 it is the exact uniform average over all 10! orders (subset DP). For p ≥ 8 it is the average over R random orders and their reverses; this is still q-reversible, so all theorems apply.
- `gibbs1`: one uniformly chosen Gibbs flip (a weak kernel).
- `indep`: the independence step alone.

**What was computed exactly.**
- v_t for all t via the two-particle recursion E[W_t² q̂_t^{⊗2}F | 𝓕_{t−1}] = W²_{t−1} q̂^{⊗2}_{t−1}(M_t F), where M_t F(x,y) = g_t(x)g_t(y)[(1−1/N)(K_t⊗K_t F)(x,y) + N⁻¹(K_t diag F)(y)]. This is a direct consequence of Fact F and Lemma 2.
- e_s, h_{s,T}, all stage constants, and the bounds.
- An independent Monte Carlo run of the particle system (N = 20) checks v_T.

| case (p, corr, kernel, thr) | T | Σχ²_t | σ²_T | N·V_T at N=2500 | N·U_T (Thm B) | N·(Thm C) | N·refresh | T25(iv)+OPTIONAL B_T | max_t a_t* (χ² at that t) | MC Var (N=20) vs exact |
|---|---|---|---|---|---|---|---|---|---|---|
| 6, .6, full, .9 | 3 | 0.225 | 0.278 | 0.278 | 0.374 | 0.441 | 0.225 | 10.9 (vacuous) | 0.145 (0.111) | 0.01396±0.00009 vs 0.01399 |
| 6, .9, gibbs1, .9 | 5 | 0.518 | 2.771 | 2.771 | 2.937 | 6.22 | 0.518 | 5.90 (vacuous) | **0.896 (0.111)** | 0.1357±0.0006 vs 0.1360 |
| 8, .95, gibbs1, .9 | 8 | 0.837 | 17.31 | 17.31 | 20.06 | 59.9 | 0.837 | 222.9 (vacuous) | **4.13 (≤0.111)** | 0.849±0.016 vs 0.865 |
| 8, .9, full, .5 | 2 | 1.152 | 1.184 | 1.184 | 1.253 | 1.547 | 1.152 | 1.00 | 1.0 (1.0) | 0.0602±0.0006 vs 0.0596 |
| 8, .9, indep, .9 | 5 | 0.449 | 1.080 | 1.080 | 1.317 | 2.118 | 0.449 | 7.83 (vacuous) | **0.416 (0.111)** | 0.0534±0.0006 vs 0.0539 |
| 10, .9, full, .9 | 3 | 0.315 | 0.323 | 0.323 | 0.428 | 0.621 | 0.315 | 18.8 (vacuous) | 0.113 (0.111) | 0.0161±0.0004 vs 0.0162 |

"OPTIONAL" uses the kernel's sharp minorisation β = min_{x,y} K(x,y)/q(y); this is 0 for `gibbs1`, so ε_t = ḡ_t − 1 there. The Thm C column uses the same sharp β in (C2): T09's ε_t is valid only for kernels that contain the independence step. "B_T vacuous" means B_T ≫ the truth (and ≥ 1 per island). For each case, all of the following held: (A3) to 1e−9 relative accuracy, U_t ≥ V_t at every t ≤ T, and Thm C ≥ V_T, at every N ∈ {10, 30, 100, 300, 1000, 2500}.

**Findings.**
- (A3) matches the pair recursion to all printed digits (`identity_rhs` = `VarW_T`) in every case and at every N ∈ {10, …, 2500}.
- U_t ≥ V_t held at every t, in every case and at every N (`allB_ok`).
- At N = 2500, Theorem B is within 6–35% of the truth (16% for the hardest Gibbs-only case), and Theorem C within a factor of 3.5.
- The exact-refresh formula Π(1+χ²/N) − 1 can **under**-estimate the truth by 5.4× (p=6) and **20.7×** (p=8, corr .95, Gibbs-only kernel). So χ²-only reasoning (T13 alone) is not a bound.
- Minimal PW2 constants a_t* = N(v_t − v_{t−1})/v_{t−1} are O(1) and stable in N, as Corollary B2 predicts, but up to ~40× χ²_t (p=8 Gibbs-only: a* = 4.13).
- In the logs, T09's ε_t ∈ [0.03, 0.6] at these tiny p. So the T09-based H recursion is still informative there, which it will not be at study scale.

## 6. What fails and why

- **The one-step, parent-uniform route** (OPTIONAL_PW2 (A)–(C)) requires sup_x K_{t−1}g_t(x) ≤ 1 + O(1/N). This is false for any fixed imperfect kernel, so a_t ∝ N and B_T is vacuous (1–223 in all cases above). The martingale route avoids this: the bias terms (μ_{t−1}g_t)² − 1 need not be O(1/N) individually; they cancel through the future-weight functions h_{s,T}.
- **PW2 with a_t = χ²_t** (the natural "T13-only" constant): COUNTEREXAMPLE by exact computation (table, rows 2, 3 and 5; `results/pw2_p6_rho0.9_gibbs1_thr0.9.json`, `results/pw2_p8_rho0.9_indep_thr0.9.json`).
- **Removing the sup norm H_{s,T} from Theorem B** by iterating Cauchy–Schwarz (J(f) ≤ q(f) + √V·√J(f²)) only raises the power of V. A sup norm of h always remains at the last level. I did not find a pure-L² non-asymptotic bound.

## 7. Needs escalation

1. An independent check of Theorem A (A3) and Theorem B's Cauchy–Schwarz step. Both are short; the numerics confirm A to machine precision.
2. Corollary B2: the a_t uses S_t − S_{t−1} with the (1−1/N) weights. Check that the sign handling is right when σ²_t < σ²_{t−1}.
3. Whether an L² mixing premise (λ_t, or the two-temperature λ^{(w)}_t) can be **certified per fit**, for example by a spectral-gap estimate on the restricted candidate set V, as the next step for O-CERT and T26.

## 8. Outside scope

- The pair recursion of §5 computes E_c[(Ẑ/Z)²] exactly whenever |Ω| is enumerable. On the exact branch this is moot, but it gives a reference oracle for any O-CERT certificate test at p ≤ 12.
- Theorem A's W_s μ_s(h_{s,T}) = M_{s−1} identity also gives an unbiased-type handle for **lower** bounds on Var (two-sided evidence control). It may matter for T26.

## 9. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| Thm A (exact identity) | (A1)–(A4) | high | done (candidate) | Fact F + martingale telescoping | no |
| Thm B (two-sided bound, replaces PW2 in T25(iv)) | (B1)–(B3), pooled /4 | high | done (candidate) | Cauchy–Schwarz on E[W(W−1)μ(h²)] | no |
| Cor B2 (PW2 with explicit a_t = Δσ²-type, ν_t = O(N^{−3/2})) | §3 | high | done modulo item 7.2 | (A4) + (B1) | no |
| Thm C (primitive constants) | (C1)–(C4) | high | done (candidate) | L² expansion with q_{t−1}(g·) = q_t | no |
| Non-vacuous at study N, T | needs λ_t(1+ḡ_tλ_t) ≤ κ < 1 and BW_W on Ω | medium (true in good-mixing fits) | low–medium (needs a certified gap and a sup-weight bound) | mixing certification; ḡ_t not ESS-controlled | possibly a per-fit spectral diagnostic |
| PW2 with a_t = χ²_t | — | **false** (COUNTEREXAMPLE) | — | — | — |
