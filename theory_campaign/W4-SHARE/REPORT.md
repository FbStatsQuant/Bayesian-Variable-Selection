# W4-SHARE — REPORT: delivery to the terminal rounds (route (b2))

Run of 2026-11-02, branch `theory/W4-SHARE`. Proofs are in `PROOF.md`; working notes in `NOTES.md`; scripts and their saved outputs (`*.txt`) in `scripts/`. Every result here is a **candidate**: not reviewed, not adopted.

## 1. Headline

1. **SHARE is replaced by a checkable envelope, and route (b2) delivery is PROVED given it (Theorem D4, Corollary D5).** For any target set W and any space-time potential h_t, the W-count of an island dominates a branching chain whose cumulative mean is P_t = (Ẑ^h_t/Ẑ_t)·∏(1−η_s): the h-subpopulation's evidence relative to the island's. Then P(no W-particle at the end of the bridge) ≤ P(envelope fails) + exp{−Nπ₀(h₀)(1−e^{−c})}, with 1/c ≤ [1 + (T−1)/(e−1)]e^{Γ}/∏(1−η_s). Here Γ = Σ_tΔ_tκ_t is the cumulative fitness (discrepancy) oscillation between the outsiders the particles can occupy and the h-support. Delivery holds whenever **Γ + Σ_sη_s ≤ log(Nπ₀(h₀)/T) − ω(1)**. No LT, no bridge-mass hypothesis and no SHARE are used, and exits only need Ση_s ≲ log N, not Ση_s → 0.
2. **The threshold is sharp and no grid condition can replace it.** Proposition SH (PROVED): with κ ≥ 2 log N + ω(1), extinction has probability → 1 even with zero exits. D5 tolerates κ ≤ log(Nπ₀(W)/T) − ω(1). Proposition G (PROVED): Γ ≤ max κ for **every** grid, because Σ_tΔ_t = 1. An ESS or restricted-ESS (T13) condition on the φ-grid therefore cannot imply SHARE; the grid matters only through T (drift) and through the rounds available for tracking. C1's extinction rates are reproduced by a one-line branching formula (0.066/0.493/0.999 predicted, 0.060/0.465/0.995 simulated). With the method's own grid, C1 still kills A.
3. **In T03's regime the masked case has no posterior-level barrier (Proposition M; deterministic core PROVED, score gain PROOF SKETCH).** Under R, every truth-subset T ⊊ S₀ has a missing truth with δ²_{T,j} ≥ (n−1)λ²_min θ²_min, and under SE this extends to 𝓡_d. So the path to S₀ inside 𝓡_d is downhill for every φ ≥ φ_n → 0. In 500 faithful small-p final-run islands on five start-masked designs with π(S₀) ≥ 0.66, **S₀ was scored during the bridge in 500/500 islands**: as an initial draw or by Gibbs, at stage 1 when the start sits on subsets, and at stages 5–7 (φ ≈ 0.4–0.5, once the start-favoured extras become deletable) when the start sits entirely on 4-extra supersets. It was never scored in the terminal rounds and never missed. Delivery to 𝓡_d and even LT held in every island. Route (b2) is closable there, but it is **not needed**.
4. **Outside that regime route (b2) fails through REPAIR, not through delivery (COUNTEREXAMPLE, finite n, reproducible).** The posterior-barrier design PB has λ_min(R_{S₀}) = 0.004 and π(S₀) = 0.94–0.97, and the start mode {12} ⊂ S₀ has π₀ ≈ 0.98. Delivery to 𝓡₀ succeeded in 200/200 islands, LT failed in the typical island (median log Ẑ/Z = −67), and LS0 cannot score S₀. S₀ was scored only through a rare gate, in 82% (n = 4000) and 51% (n = 16000) of islands. The gate-obstruction bound (Proposition X, PROVED), 0.48 per island, essentially matches the observed rate.
5. **Recommendation.** For the original method, state (b2) as Theorem B2-W4: (TRACK) + (OSC) + confinement + REPAIR on the same W, with N, T ≤ T_e and the 4 islands explicit. Its BVS-level inputs are CONJECTURE (supported numerically). The better no-tweak theorem for the masked regime is **bridge-Gibbs discovery**: a multi-flip extension of D2, for which Proposition M supplies the key input (CONJECTURE). No method change closes posterior-barrier designs: LS0, (b2) and T39 all fail there, so T38 must keep R/SE-type hypotheses.

## 2. Statements

Setting: one final-run island given a successful 𝓒; EX-A, EX-S, CAL. X_t is the population at the end of stage t, and K_t the one-round kernel at φ_t. Potentials h_t: Ω → [0,1] are 𝓒-measurable with h_T ≤ 1_W. Ḡ_t is the population mean weight, Ḡ_t^h = ΣG_t h_{t−1}/Σh_{t−1}, r_t = Ḡ^h_t/Ḡ_t, and P_t = ∏_{s≤t} r_s(1−η_s). Full definitions are in PROOF §0.

- **Theorem D4 (PROVED).** Assume (TRACK): K_t h_t ≥ (1−η_t)h_{t−1} pointwise. Then for any 𝓒-measurable envelope P̲_t, P(n_T(W) = 0 | 𝓒) ≤ P(∃t: P_t < P̲_t | 𝓒) + (1 − π₀(h₀)(1−e^{−θ₀}))^N, with 1/θ₀ ≤ ΣP̲_t^{−1}, and 1/θ₀ ≤ 1/P̲_T + (e−1)^{−1}Σ_{t<T}P̲_t^{−1} if P̲ is non-increasing.
- **Corollary D5 (PROVED).** Assume confinement sets 𝔛_t with event E, and κ_t ≥ sup{d(y): y ∈ 𝔛_{t−1}, h_{t−1}(y) < 1} − inf{d(x): x ∈ 𝔛_{t−1}, h_{t−1}(x) > 0}. Then r_t ≥ 1/(1 + o_{t−1}(e^{Δ_tκ_t} − 1)) ≥ e^{−Δ_tκ_t}, and P(n_T(W) = 0 | 𝓒) ≤ P(E^c | 𝓒) + exp{−Nπ₀(h₀)(1−e^{−c})}, with 1/c ≤ [1 + (T−1)/(e−1)]e^{Γ}/∏_{s≤T}(1−η_s).
- **Proposition G (PROVED).** Γ ≤ max_tκ_t for every grid.
- **Proposition SH (PROVED).** Two states, no moves, T = 1: P(ext) ≤ exp{−Nπ₀(a)e^{−κ}/2} and P(ext) ≥ (1 − N²e^{−κ})(1 − π₀(a)^N). The exact transition is at κ ≈ log(Nπ₀(a)/π₀(o)).
- **Proposition X (PROVED).** If every round at φ_k enters U from U^c with probability ≤ a_k, then P(some particle ever in U) ≤ Nπ₀(U) + NΣ_{k ≤ T+L+4}a_k per island.
- **Proposition M (a) PROVED, (b) PROOF SKETCH.** (a) If λ := λ_min(R_{T∪M}) > 0 and M = S₀∖T ≠ ∅, then max_{j∈M}δ²_{T,j} ≥ (n−1)λ²‖θ*_M‖⁴₂/‖θ*_M‖²₁ ≥ (n−1)λ²θ²_min. (b) Under G, R, SE and BM-∞, w.p. → 1, every T ∈ 𝓡_d missing a truth has an addition whose odds are ≥ 1 for all φ ≥ φ_n := λ_n/(λ_n + g_n) → 0, with λ_n = log(2p) + ½log(n+1).
- **Lemma PD (PROVED).** log γ₀ + d = F − log m(∅). So a C1-type takeover of an occupied W-state x by an outsider y needs F(y) ≥ F(x) + ω: the outsider must be posterior-better than the occupied W-states.
- **Theorem B2-W4 (PROVED given inputs).** Inputs: (TRACK), (OSC), confinement with P(E^c | 𝓒) ≤ ε_E, and REPAIR on W with failure ε_rep (Theorem B of W1-T24G). Then P(S₀ ∉ 𝒮 | 𝓒) ≤ [ε_E + exp{−Nπ₀(h₀)(1−e^{−c})}]⁴ + ε_rep, with 1/c ≤ [1 + (T_e−1)/(e−1)]e^{Γ}/∏(1−η_s). T ≤ T_e comes from T13(ii)(b). Composed with T38(b)-R and T21, this gives liminf P(Uᶜ, Ŝ = S₀) ≥ 1 − limsup P(U) whenever the right side → 0.

## 3. Proofs

All proofs are in `PROOF.md`:
- D4: §1 (stopped exponential supermartingale for Y_t = H_t/P_t; the per-stage step uses only iid-ness after multinomial resampling and convexity of e^{−θy} on [0,1]);
- D5 and Proposition G: §2;
- Proposition SH: §3;
- Proposition X: §4;
- C1 branching analysis: §5 (PROOF SKETCH, numerically confirmed);
- Proposition M: §6;
- Lemma PD: §6b;
- assembly: §7.

The crux of D4 is that P ↦ P(1 − e^{−θ/P}) is monotone and that τ = first envelope failure is predictable, because r_t is computed from X_{t−1}.

## 4. Evidence (fixed seeds; outputs saved next to each script)

| check | script | result |
|---|---|---|
| g increasing, monotone map, θ₀ bounds, D4 vs exact DP for binomial chains, Prop M(a) on random designs | `s0_lemma_checks` | all hold. D4/exact ≤ 0.9990 (200 chains). M(a) min LHS/RHS = 1.00000 (3000 cases; equality when \|M\| = 1) |
| SH, T = 1 | `s1_toys` A | exact transition at log(Nπ₀(a)/π₀(o)), between D5's log(Nπ₀(a)) and SH's 2 log N |
| D5 multi-stage, two states | `s1_toys` B | bound valid in all 10 settings. Loose at T = 1000 because of the drift term (κ = 2: simulated 0.0125 vs bound 0.30) |
| C1, reversible kernel, 200 islands | `s1_toys` C | P(A extinct): 0.060 / 0.465 / 0.995 at N = 10⁴/10⁵/10⁶. Branching prediction 1 − (1 − π₀(o)s)^N, s = 0.150: 0.066 / 0.493 / 0.999 |
| C1 without o | `s1_toys` D | A survives 50/50; log(Ẑ/Z) ≤ −1738 in every island (LT fails, delivery holds) |
| C1 with the method's grid | `s1_toys` E | the method grid has T = 10, with the last step 0.027 → 1. A extinct in 0.26 / 0.92 / 1.00 of islands (cf. P(an o copy is drawn) = 0.37 / 0.99 / 1.00) |
| start-masked BVS designs E1a–E1e (p = 16, n = 400–4000, π(S₀) = 0.66–0.97, π₀(S₀) down to 4·10⁻³²) | `s2_bvs_masked` | 500 islands, N = 2500, method grid (T = 13–32). S₀ first scored: stage 0 (initial draw) in 0.02/0.98/0/0/0.31 of islands (E1a–e), by Gibbs in the rest: stages 1–2 (E1a, b, c, e) and stages 5–7 (E1d, `s2b_stage_hist`). **Never in terminal rounds, never missed.** P(n_T(𝓡_d) = 0) = 0 for d = 0, 1, 2. Realised min_t log P_t ≥ −1.72 (𝓡₀), ≥ −0.01 (𝓡₁, 𝓡₂). min log Ẑ/Z ≥ −0.08 and P(Ẑ/Z < ½) = 0 (LT holds) |
| plug-in D4 bound (P̲ ≡ worst realised envelope) | report §4 computation | per island: 𝓡₁ ≤ 4·10⁻³², 10⁻¹²¹, 0.063, 4·10⁻⁴⁸ (E1a, b, c, e); 𝓡₂ ≤ 7·10⁻¹⁸ in all. Illustrative only: the envelope is estimated, not proved |
| posterior-barrier design PB (λ_min(R_{S₀}) = 0.004) | `s3_bvs_barrier`, `s3b_gate_rate` | π(S₀) = 0.94/0.97. Paths from {12}: −6.3 (single additions), −12.0 to −14.6 (pairs) at *both* endpoints. min_φ q_φ(𝓡₀) = 0.94/0.97. Delivery to 𝓡₀ in 200/200 islands. S₀ scored in 82/100 and 51/100 islands. LS0 stops at {12}. Gate ≈ 5·10⁻⁶ per particle-round; Prop X bound 0.48 vs observed 0.51 |

**Fidelity.** `bvs_core.py` is written from METHODOLOGY_v3 §§4–6: exact scores; complete-linkage blocks with cut and next-fit packing; tables; exact π₀ draws; neighbour graph; the m = p+B+2 random-order round with heat-bath Gibbs (SR scoring), uniform swap, B neighbour swaps with the Hastings factor, and the independence proposal; multinomial resampling every stage; L burn-in plus 4 measured rounds.

**Idealised calibration (declared):**
- the pilot temperatures come from the exact-law ESS rule instead of a particle pilot;
- V is the top-20p models by γ₀ and by γ₁ over all of Ω, as if every model had been scored;
- the calibration's own scoring is not simulated, so "S₀ scored" refers to the final run alone.

Sufficient statistics are drawn from their exact law, so n ≫ p is exact.

## 5. What fails and why

- **SHARE as a per-stage hypothesis (D3).** It is nearly the conclusion (W3-VT38E §5.2), and it compounds over T stages. The natural replacement is a cumulative statement, the envelope on Ẑ^h/Ẑ, not a per-stage share bound. Lemma S-type share bounds decay geometrically over stages (W1), so they cannot be iterated.
- **LT (D1/T15).** It is not necessary: C1 without o and PB both deliver while log Ẑ/Z ≈ −1800 and −67. T15 measures the wrong ratio (population vs truth). Delivery depends on subpopulation vs population.
- **Grid-based conditions** ("π_φ(𝓡_d) rises fast relative to the ESS grid"). Proposition G: cumulative selection is grid-independent. C1 with the method's own grid still loses A. The ESS grid places only O(1) stages across a two-state crossing; the Fisher–Rao length of a two-point crossing is π.
- **Sup-exit control on W = 𝓡_d.** Boundary states have O(1) exit probability (W1-T24G CE1). D4's potentials and its ∏(1−η) form are the fix: occupancy-weighted exits, with Ση up to ≈ log N allowed.
- **Asymptotic BVS instance of (TRACK)/(OSC).** Not completed. The crux is an occupancy-weighted exit potential near the 𝓡_d boundary when a truth with proxies is missing. Proposition M gives the downhill direction; turning it into a uniform K_t h_t ≥ (1−η)h_{t−1} needs TL/NL-type leakage control (00_COMMON TL_avg) and a choice of W that tolerates look-alikes (W1-T24G's completion family).
- **A BVS realisation of C1 with repair valid on the occupied region.** Not found. Lemma PD shows such a design needs W-particles that lag in the posterior, and in BVS that means a posterior-level barrier, which also breaks REPAIR (PB). So the open W1 question ("does a BVS design realise C1?") now has a sharper form: C1-type extinction is possible only where REPAIR on the occupied region already fails (CONJECTURE).

## 6. Needs escalation

1. **Bridge-Gibbs discovery theorem (multi-flip D2), to a stronger prover.** Claim (CONJECTURE): under G, R, SE, BM-∞ and EX-A/EX-S/SR, if π₀(𝓡_d) ≥ b > 0, then S₀ is scored during the bridge w.p. → 1, within O(s₀+d) stages after φ passes the last threshold of a downhill path from the start region. That threshold is φ_n → 0 for missing truths (Proposition M); for deleting start-favoured extras it can be Θ(1), as in E1d (φ ≈ 0.4–0.5). Inputs: Proposition M (b) (odds ≥ 1 for φ ≥ φ_n → 0, while every stage has φ ≥ 1/T_e), D2's share and order arguments, and an exit/disruption bound per round. This would make route (b2) unnecessary in T03's regime and is the most valuable item. The numerics (500/500) support it. The risk is the order-compatibility constant (≥ 1/(s₀+d)! naively; it should be polynomial via W1-T24G's per-round progress argument).
2. **Proposition M (b)** needs a careful gain expansion with explicit remainders (EXP-type) and a union over the relevant (T, j) pairs. It is routine, but it should be checked.
3. **Independent check of D4.** The proof is short, but the predictable-stopping step and the convexity step at θ = ∞ should be read by another model family.

## 7. Outside scope

- The evidence for a regime split matters for T38's text. In T03's regime, masked starts are resolved by Gibbs during the bridge (often in stage 1). The terminal local search and the terminal rounds have nothing to repair, consistent with the n = 200 data (98% of fresh scores from Gibbs; the local search repaired 0 fits). T38(b) should be phrased around bridge-Gibbs discovery (item 6.1), not terminal repair.
- **Posterior-barrier designs are a ceiling for every local method** (Proposition X; PB). With N = max(2500, n, p) and T ≤ 1000, a depth-c posterior barrier is crossed with probability ≍ N(T+L)·(p√n)^{−(c−1)}. That is O(1/p^{c−1}) at fixed p, independent of n, because N grows with n. Any finite-n "masked" illustration in the paper should state λ_min(R_{S₀}) and n·λ²θ²_min against log(2p√n).
- The drift term T/N in D4/D5 is real: multinomial resampling at every stage, regardless of ESS, gives neutral genetic drift. It is harmless along R4 (N ≥ max(n, p) → ∞, T ≤ T_e) but not negligible at N = 2500, T ≈ 1000.

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| D4 (envelope delivery) | PROOF §1 | 0.97 | done (candidate) | predictable stopping; convexity at θ = ∞ | no |
| D5 + G (oscillation; grid independence) | PROOF §2 | 0.97 | done | — | no |
| SH (log N threshold sharp up to factor 2) | PROOF §3 | 0.99 | done | — | no |
| X (gate obstruction) | PROOF §4 | 0.99 | done; numerically tight on PB | — | — |
| M (a) / (b) | PROOF §6 | 0.99 / 0.9 | done / 0.8 | gain expansion with explicit remainders | no |
| PD (start mass × fitness = posterior) | PROOF §6b | 0.99 | done | — | — |
| Theorem B2-W4 (route (b2) assembly) | PROOF §7 | 0.95 given inputs | done given inputs | the inputs (TRACK, OSC) for BVS | no |
| (TRACK)+(OSC) for BVS under G, R, SE, BM-∞, with W = 𝓡_d or the completion family | CONJECTURE | 0.75 | 0.4 | occupancy-weighted exits at 𝓡_d's boundary with proxies; leakage (TL_avg) | no |
| Bridge-Gibbs discovery (multi-flip D2) in T03's regime | CONJECTURE (§6.1) | 0.8 | 0.55 | order-compatibility constant; first-stage temperature vs φ_n | no |
| Route (b2) for posterior-barrier designs | COUNTEREXAMPLE at finite n (PB); fails through REPAIR | 0.95 | — | ceiling for local methods | no change helps (LS0, T39 fail too) |
| SHARE (D3 form) / LT as hypotheses | superseded by D4; LT not necessary | — | — | — | — |

**Minimal change, if HQ wants (b2) without the TRACK/OSC hypotheses.** None among small tweaks closes (b2) itself.
- Selection-free scoring tracks (T39) remove the SHARE problem entirely: their delivery is just start mass b_n, but they are a method change and fail on posterior barriers.
- LS0 (route (b1)) remains the cheapest provable route where its ELIG + TD′ hold.
- For T03's regime the recommendation is no change, with the bridge-Gibbs discovery theorem as the target.
