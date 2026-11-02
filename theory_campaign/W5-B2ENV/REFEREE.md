# W5-B2ENV — referee report on W4-SHARE (`origin/theory/W4-SHARE`, PROOF.md §§0–7)

W4-SHARE had no verifier. This is a same-family check (it is **not** the cross-family review the protocol asks for).
Verdict words: VERIFIED (every step checked), GAP (a step missing or overstated; repair given), ERROR (a false step).
Numerical spot checks: `scripts/r0_referee_checks.py` (seed 20261102), output `scripts/r0_referee_checks.txt`.

## Verdict table

| item | verdict | notes |
|---|---|---|
| §0 setting, P_t interpretation | VERIFIED | Σ_{s≤t} log Ḡ_s = log(Ẑ_t/(m(∅)Z̄₀)) on {H_s > 0}; P_t = (Ẑ^h_t/Ẑ_t)∏(1−η_s) is a rewriting. |
| **D4** Step 1 (one stage, conditional iid, convexity) | VERIFIED, with a citation GAP | m_t = Σ_j G_t(K_t h_t)(X^j)/Σ_j G_t ≥ (1−η_t)Σ_j G_t h_{t−1}/Σ_j G_t = (1−η_t) r_t H_{t−1}/N (the identity r_t H_{t−1}/N = ΣGh/ΣG is exact). Chord bound e^{−θy} ≤ 1 − y(1−e^{−θ}) on [0,1], including θ = ∞ (1{y=0} ≤ 1−y). **GAP (citation only):** "the N values h_t(X_t^i) are iid given F_{t−1}" is not literally the code (one sequential stream per island, state-dependent consumption). It is true under EX-S by W2-PREM's Lemma S (shift at a stopping time) applied to the blocks (resampling uniforms, then particle rounds in order): the pairs (ancestor, round output) are iid given F_{t−1}. Cite W2-PREM IND-T. |
| D4 Step 2 (normalised count) | VERIFIED | P_t is F_{t−1}-measurable; (1−η_t)r_tH_{t−1} = Y_{t−1}P_t also when H_{t−1} = 0 (then r_t := 1, both sides 0). P ↦ P(1 − e^{−θ/P}) = θ(1−e^{−v})/v, v = θ/P, with (1−e^{−v})/v decreasing: non-decreasing in P (for θ = ∞ it is P). |
| D4 Step 3 (predictable τ, stopped supermartingale) | VERIFIED | {τ > t} = ∩_{s≤t}{P_s ≥ P̲_s} ∈ F_{t−1}. E[M_t∣F_{t−1}] ≤ 1{τ>t}e^{−θ_{t−1}Y_{t−1}} ≤ M_{t−1} (1{τ>t} ≤ 1{τ>t−1}). τ ≥ 1, so M_0 = e^{−θ_0H_0}. With θ_T = ∞, M_T = 1{H_T = 0, τ > T}, and n_T(W) = 0 ⇒ H_T = 0 because h_T ≤ 1_W. |
| D4 Step 4 (start) | VERIFIED | iid π₀ draws, chord bound. |
| D4 Step 5 (θ₀) | VERIFIED | 1/θ_{t−1} = 1/θ_t + g(u_t)/P̲_t with g(u) = 1/(1−e^{−u}) − 1/u = ½ + ½L(u/2) (L = Langevin function, increasing from 0 to 1): g increases from ½ to 1. Monotone case: θ_t ≤ P̲_{t+1} ≤ P̲_t ⇒ u_t ≤ 1 ⇒ g(u_t) ≤ g(1) = 1/(e−1); g(u_T) = g(∞) = 1. Checked numerically (r0 §1). |
| **D5**, bound (2.1) | VERIFIED | r_t = NΣGh/(H(ΣGh + ΣG(1−h))); x ↦ x/(x+c) increasing in x and decreasing in c; ΣGh ≥ e^{Δa}H, ΣG(1−h) ≤ e^{Δb}(N−H) on E. Gives r_t ≥ 1/(1 − o + o e^{Δ(b−a)}) ≥ 1/(1 + o(e^{Δκ} − 1)) since κ ≥ (b−a)⁺. Edge cases (empty sup/inf; H_{t−1} = 0) fine. |
| D5 consequence | VERIFIED | P̲_t := e^{−Γ_t}∏_{s≤t}(1−η_s) is non-increasing and 𝓒-measurable; on E, P_t ≥ P̲_t, so {τ ≤ T} ⊆ Eᶜ; θ₀ ≥ c and 1 − e^{−x} is increasing. Note E only constrains X_0,…,X_{T−1}. |
| D5 Remark 2 (refined form) | VERIFIED | 1/(1+y) ≥ e^{−y}; the random event {o_{s−1} ≤ ε_s} is handled by the stopping time (it is F_{s−1}-measurable). |
| D5 Remark 3 (reading) | VERIFIED | Nπ₀(h₀)(1 − e^{−c}) ≥ Nπ₀(h₀)c/2 for c ≤ 1. |
| **Prop G** (grid independence) | VERIFIED as stated (Γ ≤ max_t κ_t because Σ_tΔ_t = 1); **GAP (wording)** | It is an upper bound, not grid independence of Γ. When κ_t = κ(φ_{t−1}) for a function κ(·), Γ is a left Riemann sum of ∫₀¹κ(φ)dφ and does depend (mildly) on the grid; what is grid-free is the bound max κ. The sentence "the total selection pressure … is fixed by d alone" should read "is bounded by the largest oscillation, whatever the grid". |
| **Prop SH** (i) | VERIFIED | D5 with T = 1, η = 0, 𝔛 = Ω′, Γ = κ; 1 − e^{−x} ≥ x/2 on [0,1]. |
| Prop SH (ii) converse | VERIFIED | Given n₀ < N, ω = n₀/(n₀ + (N−n₀)e^κ) ≤ Ne^{−κ}; (1−ω)^N ≥ 1 − Nω. |
| Prop SH (iii) | exact law VERIFIED; "transition at κ ≈ log(Nπ₀(a)/π₀(o))" is a **heuristic** (GAP: label it as such) | The location follows from Nω ≈ 1 with n₀ ≈ Nπ₀(a); the bracketing log(Nπ₀(a)) ≤ · ≤ 2 log N for π₀(o) ≥ 1/N is correct. r0 §2 evaluates the exact law: for N = 10⁴, π₀(a) = ½ the 50% point is at κ = 9.6 vs log(Nπ₀(a)/π₀(o)) = 9.2 (N = 10³: 7.3 vs 6.9; N = 10⁴, π₀(a) = 0.99: 14.2 vs 13.8). "Sharp up to a factor 2 in log N" holds in this two-state example only. |
| **Prop X** (main inequality) | VERIFIED | Resampling copies states; first entry into U is either an initial draw or an end-of-round entry; union bound. |
| Prop X, "Moreover" clause (scoring S₀ through U) | **GAP (two missing terms)** | (a) a_k bounds *end-of-round* entries, but a proposal of S₀ is made from the *current* state at some step inside a round; a particle can enter U mid-round, score S₀ and leave before the round ends. The clause needs a_k^{visit} := sup_{x∉U} P_x(the round visits U at some step). (b) The independence proposal proposes S′ ~ π₀ from **every** state, so "entering U is necessary to propose S₀" is false for label I: add N·(T+L+4)·π₀(S₀) per island. With (a) and (b) the clause holds. |
| Prop X, "Use" (route (b2) fails w.p. ≥ …) | **GAP** | As a lower bound on the failure of the *method*, the calibration's scoring (pilot and diagnostic islands, same kernel), and the final local search, must also be bounded; as stated it is a statement about the final-run SMC only. Fine as "route (b2) cannot work", not as "the method misses S₀". |
| Prop X numerical sharpness (≈ 0.48 vs 0.51) | VERIFIED (arithmetic) | 2500 · 38 · 5·10⁻⁶ = 0.475. Not re-simulated. |
| §5 C1 mechanism | PROOF SKETCH as labelled; numbers VERIFIED | Poisson(e^{0.08} = 1.083) survival s solves 1 − s = e^{−1.083s}: s = 0.1532; 1 − exp(−Nπ₀(o)s) = 0.50 (N = 10⁵) and 0.9990 (N = 10⁶). The approximations (relative fitness of an o-lineage against an a₁-dominated population; survival decided in the first few stages) are heuristic. |
| **Prop M(a)** | VERIFIED | ‖r‖² = Σ_{j∈M}θ*_j‖x̃_j‖δ_{T,j} ≤ √(n−1)‖θ*_M‖₁max|δ|; ‖r‖² = (n−1)θ*_Mᵀ Schur θ*_M ≥ (n−1)λ‖θ*_M‖² (λ_min of a Schur complement ≥ λ_min of the matrix); ‖θ_M‖₁² ≤ |M|‖θ_M‖₂². Also valid with extras in T. Checked on random instances (r0 §3: 0 violations in 20,000). |
| Prop M(b) | PROOF SKETCH as labelled | The Lemma A crossing argument is correct; the uniform gain bound over the relevant (T, j) needs a uniform full-level BF expansion (W2-PREM Lemma U). Upgraded on LH to PROVED in this run (PROOF.md §3, Proposition M-LH). |
| **Lemma PD** | VERIFIED (identity); consequence VERIFIED given its premises (Nπ₀(y) ≥ 1, d(y) − d(x) ≥ log N + ω) | log γ₀ + d = log ϖ + log BF = F − log m(∅). That a takeover *needs* these two premises is a mean-field heuristic (PROOF SKETCH, as the "Reading" paragraph says). |
| **Theorem B2-W4** | VERIFIED given its inputs | Islands conditionally independent given 𝓒 (streams 10–13); product of the four D5 bounds; smallest-index W-particle measurable; terminal rounds have no reweighting/resampling; REPAIR applies with fresh randomness (rigorously: W2-PREM IND-T). One bookkeeping remark: after stage T's resampling there are **L + 5** rounds at φ = 1 (stage-T round, L burn-in, 4 measured; W2-PREM §1.1), so "REPAIR in L + 4 rounds" from the end-of-stage-T state is the right (and slightly conservative) form. |
| "Where T13 and T15 enter" | VERIFIED as discussion | — |

## Summary
No ERROR. D4, D5 and B2-W4 are correct as stated (D4 should cite IND-T for the conditional iid step). Two GAPs that
matter for later use: Prop X's scoring clause needs the "visit" form of the gate rate and the independence-proposal
term; Prop G is an upper bound, not grid independence. M(b) is upgraded on LH in this run.

## The finding that matters for route (b2) on LH (see PROOF.md §4)
D4/D5 are correct but, on the linked-hub family, the right choice of potential makes them degenerate: with
h_t = 1_𝒩 for the region 𝒩 = {S ⊇ S° with ≤ k neutral extras, any subset of the masked groups}, confinement
(E with 𝔛_t = 𝒩) holds for **every** grid because junk is non-persistent, so κ_t ≡ 0, Γ = 0, and D5 reduces to
Prop X (a union bound on exits). The lattice-indicator potential suggested in the task brief is the wrong choice:
it forces outsiders (proxy states, junk-carrying states) whose discrepancy exceeds the occupied lattice state by
Θ(n) or by O(log n) with a constant > 1, so Γ ≳ log(N/T_e) and the D5 certificate fails at the v3 budgets (§4.6).
