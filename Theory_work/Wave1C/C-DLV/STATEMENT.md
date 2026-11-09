# C-DLV — STATEMENT (v2.2: v2 locked after R01 ~21:58; v2.1 sweep/council-1 edits 22:40–22:58; v2.2 council-2 minors 23:03)

Changes v1 → v2 (R01 dispositions in reviews/R01_disposition.md): the ticket target (T) is kept verbatim as the goal
and is NOT claimed; claims are split into proved reductions (P), conditional criteria (C) and findings (F); the Ψ_n
route is demoted to a remark (numerics N1 do not support it at the tested configurations; no asymptotic
impossibility is claimed); grid snapping, `validation_failed` and
`non_progress` are carried explicitly; resource envelopes are separated by unit; inventory completed (interrupts,
allocation exceptions, dependency failures); Lemma R is stated for valid inputs with p_raw.

## 0. Objects
- **Method** 𝔐 = v3.1 + LS0 as specified (SoP/02_method.tex: statuses :57-63, calibration :303-350, final islands
  :352-385, GUARD-W :403-406, LS0 :490-501, output convention :583-590), R′ = 4k declared (k fixed), LS0 cap ℓ_n = ℓ.
  Code facts: production core `Scripts/SMC_BVS/core/` on the `v3_fit` call graph (calibration rules `cpp/v3_calib.h`
  byte-identical to the study's v2.2.1).
- **No-output event** 𝒰_n = 𝒪_nᶜ: `v3_fit` returns with `estimates_available = FALSE`, or ends without returning a fit
  object. INVENTORY.md v2 lists every path (each a code site whose firing ends the fit without estimates).
- **Classes**: LH (exact Gram), LH-iid (W1-PXN), W1-GEN class (Theorem GEN), fixed s₀, p ≤ n^A.
- Grid objects (L3): for a candidate set V, ℓ_S(t) = log γ₀(S) + t d(S), q_t^V ∝ e^{ℓ_S(t)} on V,
  ρ_V(u,v) = exp{2F_V(v) − F_V(u) − F_V(2v−u)}; c₀ = log(10/9).

## 1. Premises
From the cards: EX-A, EX-S, SR, OP-LS0, e4, GUARD-W, IND-T (R′ > 4; not used by this ticket's proofs). **CAL is not assumed** (calibration success is
part of the question). New, flagged, class (d):
- **IDEAL-W**: an abstract unbounded-word/address machine: integer, index, stream-id and allocation arithmetic never
  overflow (the RNG's intentional modular arithmetic is kept), so `unsupported_size` (spec e7) never fires.
- **EX-A as a cost model**: unit-cost exact real arithmetic, including exp and log (used by ρ_V, log-sum-exp and the
  pilot ESS); no bit complexity is charged.
- **MACH(τ, τ₀, β, β₀)**: wall time ≤ τ·(operation count) + τ₀; peak bytes ≤ β·(words held) + β₀; every heap, stack
  and worker allocation succeeds whenever the live bytes stay within the declared memory (R06 #3: this is an
  operational premise, not a consequence of counting words); the build, its lock/cache and runtime dependencies
  (Rcpp, digest) succeed; no user/external interruption, no worker crash.
- **CONFIG** (the computational configuration covered, R06 #1–#2): the production core plus LS0 (cap ℓ) and the e4
  fallback (TDP-IMPL); the general-h accumulator with the default list 𝓗 only (size indicators, neighbour-edge pairs
  ≤ 2pB, and d; O(1) evaluation each; user-declared functions are NOT covered — council C1 Codex #1); certificate
  computations with declared envelopes Cert(n,p) operations and Cert_M(n,p) words, both polynomial and carried
  explicitly in the allocation (no claim that they are dominated by the core terms); serial execution or a fixed number w of concurrent workers/scorers
  (memory envelope multiplied by w).
- **TDP-IMPL** (method requirement for a not-yet-shipped component; METHOD_REQUIREMENTS A.2): the e4 tie-aware
  fallback is implemented as W1-N3's reference algorithm TDP (Theory_work/Wave1/W1-N3/lemmas/L7_tie_aware_dp.md), with
  O(p·Σ_b(2^{|C_b|} + (K+1)²)) operations (W1-N3 L7:20), implemented with O(Σ_b 2^{|C_b|} + J(K+1)) storage (the
  (block, size) DP table plus the block tables; a requirement on the implementation, since L7 states no storage bound). e4 itself only fixes WHICH maximiser is
  emitted; TDP-IMPL fixes HOW (its cost). Used by P2, P4 (Theorem D), C2 and F1.
- **Valid declared inputs**: integer seed in [1, 2³¹−1]; allocation a list with named finite positive scalar fields
  `mem_gb` and `hours` (the core silently substitutes 8 GiB / 24 h for missing names, `v3_fit.R:19, :66-71`).
- **Declared allocation** 𝒜_n: `allocation$mem_gb` ≥ mem_n/2³⁰ and `allocation$hours` ≥ time_n/3600, with (mem_n,
  time_n) the polynomial envelopes of Corollary R (explicit polynomial shapes; implementation-dependent constants).

## 2. Target (T) — the ticket's theorem, kept as the goal, NOT claimed
On LH, LH-iid and the W1-GEN class, for 𝔐 under 𝒜_n: P(𝒰_n) → 0, hence P(Ŝ⁺ = S₀) → 1.

## 3. Claims
**(P1) Inventory** (INVENTORY.md v2) — AUDITED (code reading; R01, R02, R05, R06, council): every exit of `v3_fit`
without estimates is one of the listed sites.
**(P2) Lemma R** (L1; uses TDP-IMPL): for valid inputs (n ≥ 3, raw dimension p_raw), every seed and uniform realisation, the
operation count, words held, preflight bytes and exact-branch preflight seconds are bounded by polynomials (explicit shapes, implementation-dependent constants; within CONFIG) in
(n, p_raw); hence under MACH and 𝒜_n no resource path fires.
**(P3) Lemma S** (L2): under model G on the classes (n ≥ 3), the input/degenerate paths have probability 0 and p_raw = p
a.s.; under EX-A no scorer call fails; the remaining internal error sites are unreachable on the `v3_fit` call graph (this last part AUDITED by code reading, L2 S.3).
**(P4) Theorem D** (L4; uses P2, hence TDP-IMPL, and holds relative to the audits P1 and L2 S.3): 𝒰_n ⊆ 𝒮ℒ_n ∪ (null set), 𝒮ℒ_n = {escalation to tier 1 and some tier-1 grid construction
fails}, and a construction fails iff (α) its interval count exceeds T_e, or (β) `non_progress`, or (γ) a point snapped
to 1 fails validation. P(𝒰_n) → 0 ⟺ P(𝒮ℒ_n) → 0.
**(P5) Grid lemmas** (L3, L5): exact identity ρ_V(u,v) = q_u(M)q_{2v−u}(M)/q_v(M)² (any M ∈ V); pilot schedules have
≤ T_e strictly increasing stages ending at 1; success criteria: (a) dominance (one M with q_t^V(M) ≥ √0.9 at t = 0
and t = 2) or sup_{[0,2]} Var < c₀ ⇒ the construction succeeds with ≤ (pilot count) intervals; (b) two-model family with
ε-remainder on [0, 2] ⇒ N_b ≤ N̄_b = 22 + ⌈log_{4/3} max{1, (−x₀ − λ_θ)/(2s_θ)}⌉ (ε = 0.01, exact constants in L5)
bisection-limited trials; with the remainder only on [0, 1+η] add ⌈log_{4/3}((1+η)/η)⌉ (Lemma 5.2′); no
`non_progress` if D ≤ s_θ2⁶⁰; post-snap validation (γ) not excluded.
**(C1) Conditional delivery**: P(𝒰_n) ≤ P(E_n ∩ ∪_{tier-1 constructions} {(α) ∨ (β) ∨ (γ)}), E_n = {some tier-0 trigger
fires}; in particular P(𝒰_n) → 0 on any design sequence where, w.p. → 1, either no tier-0 trigger fires, or every
tier-1 candidate set satisfies (P5)(a), or satisfies (P5)(b) with pilot count ≤ T₁ − N̄ (N̄ the applicable bound),
D ≤ s_θ2⁶⁰ and no (γ). Measured status (Opus C1 #2): no design sequence is known to satisfy the (P5) hypotheses; at the
tested sizes, since (P5)(a) forces N_b = 0 (Prop 3.5(a)), (P5)(a) fails in every construction with N_b > 0 (220/236
in the 80-fit runs, 146/146 in N4; the other 16 were not tested for dominance) and (P5)(b) fails with the selected pair (other pairs not
searched); in all 134 production fits no tier-0 trigger fired, so tier 1 was never reached.
**(C2) Joint consistency with the delivery term**: P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − o(1) − P(𝒮ℒ_n) on the classes, from W1-GEN
(C1)+(C2) and T03♯ (GEN class, incl. LH exact Gram) and W1-PXN (T), (P) (LH-iid), under their hypotheses (L4 D′).
**(F1) Finding** (shipped component): freezing the tier-1 pilot schedule when a tier-1 construction fails makes
P(𝒰_n) = 0 under the premises, hence (T) for the patched method.
**(O) Open obstruction (exact form, Opus C1 #1)**: P(𝒮ℒ_n) → 0 on the classes, i.e. P(E_n ∩ F¹_n) → 0 with
F¹_n = {some tier-1 construction fails through (α), (β) or (γ)}. Two sufficient routes: (O-a) P(E_n) → 0 — no tier-0
trigger (E1–E3, forced pilot steps, grid failure/unconvergence, local_limit) w.p. → 1; (O-b) P(E_n ∩ F¹_n) → 0 via
(α)–(γ) for the realised tier-1 candidate sets and pilot schedule — to be proved jointly with (or conditionally on) the
triggering event, not for an unconditioned tier-1 run (E_n includes forced pilot steps, and fully forced pilots attain
k = T_e exactly, N2b). The pilot stage count is the CJ06 / Conjecture P question.
