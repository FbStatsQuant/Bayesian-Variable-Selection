# W2-UNI — PLAN

## Route
1. **Statement lock** (R01, Codex gpt-6.1-sol high): STATEMENT.md + this plan.
2. **R1 metric toolkit** (lemmas/L1_metric.md): CT_M, CD_M, RB_M, TAIL_M as a constant-replacement delta of LOC2
   L3_CTd (packing fact (2m+3)^d → growth bound C₀(m+2)^{d₀}, shells m ≥ 0 so separation is not needed); new LOCL.
   Numerics n1_metric.py: random geometric graphs / irregular 2-D sites / block pseudometric, exponential kernels and
   GMRF precisions; check CT_M entry bounds and LOCL ‖Δβ‖₁ ≤ ε(r) on sampled and greedy T.
3. **R2 k = 0** (lemmas/L2_k0.md): delta of LOC2 L4 Part A step by step (A.1–A.6) with the growth function; assembly via
   PLR (LOC2 L5). Every use of "packing" listed and replaced.
4. **R3 k = 1 key lemma U-LOC** (lemmas/L3_ULOC.md): (a) exact decomposition for general Ψ (FACA U(a) never needs
   block-diagonality except to localise P_{𝓚_T}ζ_l and λ̃; both become T-global objects); (b) idiosyncratic bound via
   references (l, T ∩ B(l, r_n)), r_n := ⌈(log log n)²⌉, plus LOCL atoms with vanishing ℓ¹ norm; (c) factor term via
   F_T := λ_TᵀΨ_TT⁻¹ζ_T/√s_T ~ N(0,1) and a union over sets stratified by h_𝒢(T) (no Cauchy–Schwarz); (d) FACA U(d)
   coupling. Numerics n3_uloc.py: identity check for non-block Ψ (AR(1)+factor, 2-D exponential + factor), envelope
   check on random and adversarial (greedy max-|Z|) sets.
5. **k = 1 assembly** (lemmas/L4_k1.md): FACA L2 (sandwich Q = [p], design-agnostic given Gram floor + TV), L3 (NA/TL with
   the new envelope; α₀ calculation unchanged), L4 (assembly), L5.1 (random design; TV from PTV with 𝔅_n = all sets of
   size ≤ 16). Check exactly which FACA steps used block-diagonality.
6. **R4 delivery** (lemmas/L5_delivery.md): abstract Proposition F-UNI from F-FAC/F-LOC2 Step 1–3.
7. **R5 OBS-k + absorption plan** (lemmas/L6_frontier.md).
8. **Corollary table** (lemmas/C_corollaries.md): each family result with the exact assumption check.
9. Lemma checks (Sol high; xhigh for L3), CHECKPOINT after lock and after L3, mid-point (fresh Sol xhigh), sweep
   (Sol xhigh), CITECHECK, council (Sol xhigh + Opus high).

## Risks
* R2: a hidden 1-D/Euclidean step in the APP/GROW sandwich chain (selection removal / spherical tail) — mitigated by a
  line-by-line delta and the reviewer.
* R3: (b) needs ϵ-free population bounds only (Gram-only reduction), so the lattice size enters only through unions
  over references (p·2^{|B|}) and over factor strata — check the reviewer agrees no 2^p union is hidden.
* Exponent for block-structured Ψ depends on 𝒢 (κ_𝒢); singleton 𝒢 gives a smaller exponent for S5 (≈ 0.07), FACA's
  groups give 1/6.
* Mildness of (A2-1): loadings bounded away from 0 is a strong-factor assumption; zero loadings left open.

## Parallel tickets (absorption)
S5/S5F, X/XA, K2, PK/PKA: HQ forwards results; each will be mapped to the general hypothesis it discharges in
L6_frontier.md. W2-SIM: experiments only if needed for falsification at sizes beyond local compute.
