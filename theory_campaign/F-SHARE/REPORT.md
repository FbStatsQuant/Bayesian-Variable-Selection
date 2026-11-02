# F-SHARE — REPORT: the delivery theorem for route (b2) in the masked regime

Run of 2026-11-02 (Fable 5.1, Felipe's laptop; two Opus 5.5 helpers for the exact checks and the simulation), branch `theory/F-SHARE`. Proofs in `PROOF.md`; scripts and their saved outputs in `scripts/` and `results/`. Every result is a **candidate**: not reviewed, not adopted. Status words follow `theory_campaign/PROTOCOL.md` and are never upgraded.

## 1. Headline

1. **The right delivery theorem is a closure theorem, not an envelope theorem (Theorem F1, PROVED).** If the near-truth class is the *superset class* W(S°) = {x : S° ⊆ x} of the start reference S°, and if deleting a member of S° is unfavourable at **both** endpoints (start table and posterior), uniformly over supersets — hypothesis KEEP(W, η) with η = e^{−Θ(n)} — then with probability ≥ 1 − N[π₀(Ω∖W) + (T + L + 4)η] **no particle of the final run ever leaves W**. Delivery to W is then automatic, with the whole population eligible at the terminal boundary; the realised D4 envelope is deterministic (P_t = ∏(1 − η_s)); and the C1 extinction mechanism cannot start (Corollary F3, PROVED). KEEP is a single-state, single-round, two-endpoint condition: block-table ratios and score differences, no SHARE, no LT, no particle-system quantity.
2. **On the linked-hub family (LH, exact Gram, p ≤ (1 − c₀)n) the superset class is closed, so route (b2)'s delivery step is closed there for the method as it is (Theorem F2: structure PROVED, Gaussian estimates PROOF SKETCH).** The unit structure of LH (Lemma 3.1) makes every residual statistic a function of the state's intersection with one unit, so the supremum over the 2^{p−s} supersets is a maximum over ≤ s·2^{2g} Gaussians, and the keep margins are Θ(n) uniformly. Two checkable population conditions enter: PK (proxy keep: a truth is kept at every proxy configuration) and DOM (every truth in S° is worth more than every missing hub, so the truth-for-hub swap is unfavourable); both are checked exactly at p = 16, 20 (§4), DOM failing marginally in one LH20 replicate at n = 1600. Masked hubs are added *inside* W after the crossing temperature φ_hub = O(log(p√n)/n) → 0 (Prop. M of W4-SHARE in this family).
3. **What remains is repair on W, not delivery (§4 of PROOF, PROOF SKETCH).** Extras are fast variables (re-drawn at their own Gibbs label every round, odds ≤ (2p√n)^{−ε_n}); hubs are slow (uphill before φ_hub, downhill after). S₀ is scored at the first stage with φ_t ≥ 2φ_hub by any extra-free particle, and in the terminal rounds otherwise. The one non-routine input is the extras bookkeeping across resampling (CONJECTURE 4.3). The numerics (§4) show S₀ scored in every island during the bridge, never in the terminal rounds, with no particle ever outside W.
4. **Counterexamples and the no-go side.** C1 (W1-T38E) needs an outsider class that is drawn at the start (Nπ₀(o) ≳ 1) and fitter by ≥ log N; both are excluded by KEEP's two endpoints, and Proposition SH shows the second is the sharp threshold. The posterior-barrier design PB (W4-SHARE) has a closed class too; there delivery holds and repair fails, so Theorem F1 locates (b2)'s failure outside T03's regime exactly where W4 found it. **No method change is needed on LH**; LS0 and T39 are compared in §7: on LH all three deliver, and only the closed-class route needs no tweak.
5. **The genuinely open case is the random design (LH-iid, p ≫ n).** Lemma 3.1 holds only approximately, the class must be cut at bounded extras, and the leak through the (d+1)-st extra is O_P(n^{−1/2}polylog) per round, so N(T+L+4)η ↛ 0 and F1 does not apply; the reversible-leak version F1′ (D4 with a discounted leak potential) is the tool (CONJECTURE F2-iid, §2). The sharp question is uniform null leakage over the bounded-extras supersets a particle can visit.

## 2. Statements

Setting: one final-run island given a successful 𝓒; EX-A, EX-S, CAL, SR; T ≤ T_e stages, then L + 5 rounds at φ = 1; S° a data-measurable reference; W(S°) := {x ∈ Ω : S° ⊆ x}; K_φ the one-round kernel.

- **KEEP(W, η).** W 𝓒-measurable and sup_{x∈W} K_φ(x, Ω∖W) ≤ η for every φ ∈ {φ₁, …, φ_T, 1}.
- **Theorem F1 (PROVED).** Under EX-A, EX-S, CAL and KEEP(W, η): P(some particle is ever outside W | 𝓒) ≤ Nπ₀(Ω∖W) + N(T + L + 4)η per island. On the complement every particle is in W at every stage, at 𝔉_T and through the terminal rounds (DELIV(W) with the whole population eligible).
- **Lemma 1.2 (PROVED).** For W = W(S°), K_φ(x, Ω∖W) ≤ Σ_{j∈S°}max{κ₀, κ₁}(x, j) + (B+1)Σ_{j∈S°}max{ρ₀, ρ₁}(x, j) + π₀(Ω∖W), with κ_e the endpoint deletion odds and ρ_e the endpoint swap-out odds (maximised over the added label).
- **Corollary F3 (PROVED).** Under KEEP with Nπ₀(Ω∖W) + N(T+L+4)η → 0, the W-count is N at every stage w.p. → 1, the D4 envelope for h = 1_W equals ∏(1 − η_s) deterministically, and no outsider lineage exists: the C1 mechanism cannot start.
- **Lemma 3.1 (PROVED, LH exact Gram).** The unit residual u_{x,j} depends on x only through x ∩ unit(j) and is orthogonal to every column of another unit. **Lemma 3.2 (PROVED).** For x ∈ W(S°), b ∈ M∖x: δ_{x,b} = θ_b‖(I − P_x)x_b‖, δ²_{x,b} ≥ θ_b²(n−1)λ_min(Σ_LH).
- **PK(d*)** (population proxy-keep, §3.1 of PROOF): finitely many inequalities in (ρ, ψ, g); checked exactly for (0.7, 0.5, 4) at every proxy configuration (§4); CONJECTURE in general for |ψ| < ρ < 1.
- **Lemma 3.3 (PROVED given W1-EXP Thm 1 and PK).** Start keep odds κ₀(x, j) ≤ 2p e^{−c₁n} uniformly over x ∈ W(S°), j ∈ S°; swap-out odds ρ₀ ≤ 2p e^{−c_Kc₁n}.
- **DOM.** min_{x∈W(S°), j∈S°}[F(x) − F(x−j)] ≥ max_{x∈W(S°), b′∈M∖x}[F(x+b′) − F(x)] + c₄n: every truth in S° outweighs every missing hub. Void for c = 1.
- **Lemma 3.4 (PROOF SKETCH).** Posterior keep margins F(x) − F(x − j) ≥ c₂n and swap margins F(x) − F(x − j + l) ≥ c₂n uniformly over x ∈ W(S°), |x| ≤ K, j ∈ S°, l ∉ x; for l a missing hub of another pair the swap margin is DOM.
- **Theorem F2 (PROOF SKETCH; structure PROVED).** LH exact Gram, p ≤ (1 − c₀)n, PK(g−1), DOM: with W = W(S°), (a) π₀(Ω∖W), π(Ω∖W) ≤ Cpe^{−cn}; (b) KEEP(W, η) with η ≤ Cp²e^{−cn}; (c) P(some particle of some island is ever outside W) ≤ C′NT_ep²e^{−cn} → 0; (d) DELIV(W) with every particle eligible.
- **§4 (PROOF SKETCH).** Crossing temperature φ_hub = O(log(p√n)/n); extras deleted w.p. ≥ 1 − (2p√n)^{−ε_n/3} per label and added at expected rate (2p√n)^{−2/3+o(1)} per round (finite Z-families + truncated moment); S₀ scored at the first stage with φ_t ≥ 2φ_hub or in the terminal rounds; CONJECTURE 4.3 (extras count across resampling) is the only non-routine step.
- **Theorem F1′ (CONJECTURE, routine from D4).** Reversible leaks: a class whose exits land in a less-fit set 𝓛 from which the kernel returns w.p. ≥ 1 − η′, with Tη + Tη′ → 0, is delivered (h = 1_W + ρ1_𝓛 in D4).
- **CONJECTURE F2-iid.** On LH-iid (W3-PXN) with blocks = groups, W_d(S°) := W(S°) ∩ {≤ d extras} satisfies the hypotheses of F1′ with 𝓛 = states with d + 1 extras, η = O_P(n^{−1/2}polylog), hence DELIV(W_d) → 1, for every fixed d ≥ 1; the crux is the uniformity of the null leakage over the ≤ p^d·2^c states of W_d (W3-PXN Lemma B gives the per-state Beta laws).

## 3. Proofs

`PROOF.md`: §1 F1 and Lemma 1.2; §2 F3; §3 the LH family (Lemmas 3.1–3.4, PK, Theorem F2, Remark 3.6 on why the enlarged class fails); §4 extras, crossing, scoring (sketch); §5 failure modes (PB, leaky classes, the random-design obstruction).

The crux of F1 is trivial (resampling copies states); the content is in the choice of W: a class closed under the kernel at the e^{−cn} level, which the *superset* class is whenever truths are kept at both endpoints, because additions never leave it. The crux of F2 is Lemma 3.1 (finite Gaussian families), which is exact-Gram-specific.

## 4. Evidence

(All scripts in `scripts/`, outputs in `results/`; engine `bvs_core.py` copied verbatim from W4-SHARE: exact scores, v3 blocks and tables, exact π₀, full random-order round with heat-bath Gibbs (SR), uniform and neighbour swaps with Hastings factors, independence proposal, multinomial resampling, the method's idealised grid. Design `lh_design.py`: LH16 (p = 16, c = 1) and LH20 (p = 20, c = 2), ρ = 0.7, ψ = 0.5, β = 1, σ = 1, g = B = 4, blocks = groups.)

### 4.1 Exact checks of the closure hypotheses (`f1_exact_lh.py`, helper H1; `results/f1_exact_lh.txt`, `f1_run.log`)

All 2^{p−s} supersets x ∈ W(S°) enumerated (16,384 at p = 16; 131,072 at p = 20), exact scores, 20 (LH16) / 5 (LH20) noise replicates per n, n ∈ {400, 1600, 6400, 25600}. "median \| worst" over replicates.

| quantity | LH16 n=400 | n=1600 | n=6400 | n=25600 | LH20 n=400 | n=1600 | n=6400 | n=25600 |
|---|---|---|---|---|---|---|---|---|
| posterior keep margin min_{x∈W, j∈S°}[F(x)−F(x−j)]/n | 0.059 \| 0.049 | 0.084 \| 0.080 | 0.087 \| 0.083 | 0.085 \| 0.084 | 0.068 | 0.063 | 0.066 | 0.071 |
| start keep margin min[log γ₀(x)−log γ₀(x−j)]/n | 0.025 \| 0.021 | 0.045 \| 0.044 | 0.048 \| 0.046 | 0.048 \| 0.047 | 0.029 | 0.029 | 0.032 | 0.034 |
| argmin state | S° + all 3 a-proxies (the worst PK configuration) | same | same | same | same | S°+{9,10,11} | same | same |
| hub gain min_{x,b}[F(x+b)−F(x)]/n | 0.016 \| 0.014 | 0.035 \| 0.032 | 0.039 \| 0.037 | 0.042 \| 0.041 | 0.012 | 0.021 | 0.030 | 0.034 |
| #(x,b) with hub gain ≤ 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| start hub odds max g₀ (ref −log 2p − ½log(n+1)) | −2.9 (−6.5) | −3.6 (−7.2) | −4.3 (−7.8) | −4.9 (−8.5) | −2.9 (−6.7) | −3.4 (−7.4) | −4.2 (−8.1) | −5.1 (−8.8) |
| max crossing temperature φ* over (x,b) | 0.42 \| 0.44 | 0.083 \| 0.088 | 0.023 \| 0.024 | 0.0060 \| 0.0061 | 0.47 | 0.13 | 0.029 | 0.0075 |
| φ* at x = S° | 0.17 | 0.042 | 0.012 | 0.0032 | 0.22 | 0.061 | 0.015 | 0.0039 |
| log₁₀ π₀(Ω∖W) | −7.0 \| −6.3 | −38.0 \| −37.8 | −142 \| −135 | −540 \| −536 | −7.8 | −26.4 | −97.5 | −391 |
| log₁₀ π(Ω∖W) | −23 \| −20 | −111 \| −107 | −429 \| −408 | −1668 \| −1663 | −24 | −94 | −383 | −1618 |
| log₁₀ max_{x∈W} η(x) (one-round Gibbs exit bound, Lemma 1.2) | −4.4 \| −3.7 | −31 \| −31 | −134 \| −127 | −531 \| −527 | −5.0 | −20 | −90 | −382 |
| min_φ q_φ(W) | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| π₀(W₀), π(W₀) (basin S°∪A, no extras) | 0.92, 0.81 | 0.96, 0.93 | 0.98, 0.94 | 0.99, 0.97 | 0.89, 0.72 | 0.95, 0.90 | 0.97, 0.91 | 0.99, 0.97 |
| non-proxy extras: max_{x,l}[F(x+l)−F(x)] | −0.70 \| 3.2 | −1.7 \| 0.13 | −2.5 \| 1.8 | −2.7 \| −0.65 | — | — | — | — |
| non-proxy extras: max d-advantage d(x+l)−d(x) | 1.4 \| 4.0 | 1.3 \| 2.8 | 1.2 \| 4.0 | 1.7 \| 3.0 | — | — | — | — |
| non-proxy extras: log max_x Σ_l e^{F(x+l)−F(x)} | −0.36 \| 3.2 | −1.2 \| 0.85 | −2.0 \| 1.8 | −2.2 \| −0.59 | — | — | — | — |

Reading.
- **KEEP holds with Θ(n) margins at both endpoints, uniformly over all supersets**, and the worst state is the one PK(g−1) is about (all proxies of a_i present): m₁/n ≈ 0.085 (LH16), 0.07 (LH20); m₀/n ≈ 0.045, 0.03. The one-round exit bound is 10^{−31} at n = 1600 and 10^{−134} at n = 6400, so N(T_e + L + 4)η is negligible from n = 1600 on; π₀(Ω∖W) and π(Ω∖W) are e^{−Θ(n)}. This is Theorem F2(a)(b) at p = 16, 20.
- **Hub crossing.** The hub gain is Θ(n) at *every* superset (no (x, b) with gain ≤ 0), the start-side odds are −log(2p√n) + O(1) (the +3.5 offset is the size-prior term at |x| > s), and max_x φ*(x, b) falls like log n/n: 0.44 → 0.088 → 0.024 → 0.0061 (LH16). φ_hub at S° is 0.17, 0.042, 0.012, 0.0032.
- **Extras.** The proxies of a *missing* hub (k ∈ C_{b_i}) are posterior-favourable by Θ(n) (a₁ ≈ 0.037n in the full table); these are the basin states 𝔅_P of O-BGIBBS, not extras, and they become null-like once the hub is present. Non-proxy (null-like) extras have posterior addition odds ≤ e^{−0.7}…e^{−2.7} in the median replicate, a bounded d-advantage ≤ 4 nats (the predicted (α₁−α₀)Z²/2 ≤ log(2p√n)), and total addition odds Σ_l e^{F(x+l)−F(x)} ≤ e^{−2.2} at n = 25600, decreasing slowly, as (2p√n)^{−ε_n}·polylog predicts. In 1–2 of 20 replicates at n ≤ 6400 some null has a posterior-favourable addition at some superset (worst a₁ = 3.2, 1.8): the heavy-tail event P(max_l Z_l² > 2 log(2p√n)) ≈ 1/(2√n√(π log(2p√n))), which vanishes slowly. This is the quantitative content of PROOF §4.2.

**Swap margins (`f1b_swap_margins.py`, F-SHARE; `results/f1b_swap_margins.txt`).** Max over x ∈ W(S°), j ∈ S°, l ∉ x of the swap log-odds F(x − j + l) − F(x) (posterior) and the start analogue, split by the added label: a member of unit(j) (proxies, partner), a column of another unit, or a missing hub of another pair (the DOM case). "median | worst" over 10 (LH16) / 4 (LH20) replicates.

| | LH16 n=400 | n=1600 | n=6400 | LH20 n=1600 | n=6400 |
|---|---|---|---|---|---|
| l ∈ unit(j), posterior / start | −24 \| −15 / −19 \| −13 | −97 \| −65 / −78 \| −60 | −374 \| −342 / −296 \| −280 | −62 \| −55 / −51 \| −47 | −346 \| −339 / −230 \| −228 |
| l in another unit (non-hub), posterior / start | −32 \| −24 / −18 \| −13 | −137 \| −108 / −78 \| −61 | −533 \| −499 / −296 \| −280 | −62 \| −51 / −50 \| −47 | −306 \| −302 / −230 \| −227 |
| l = missing hub of another pair (DOM), posterior / start | −29 \| −13 / −39 \| −32 | −112 \| −82 / −158 \| −139 | −506 \| −415 / −650 \| −604 | **−2.4 \| +4.7** / −51 \| −47 | −64 \| −52 / −230 \| −228 |
| F(x − j + b′) − F(x + b′), max | — | — | — | −114 \| −107 | −539 \| −534 |

Reading. Every swap out of W(S°) is Θ(n)-unfavourable at both endpoints, **except** the truth-for-hub swap j → b′ in LH20 at n = 1600, where in one replicate it is posterior-favourable by 4.7 nats at one superset (all a-proxies present); at n = 6400 it is unfavourable by ≥ 52 nats. This is the DOM condition of PROOF §3.2(iv): on LH16 (c = 1, no other pair) it is void. The enlarged class W⁺ of the first draft is **not** closed (from x − j_h + b′ the proxies of the missing j_h are favourable by +175 nats): the correct treatment of a DOM failure is the reversible-leak theorem F1′, and the landing state is always posterior-worse than x + b′ ∈ W(S°) by ≥ 107 nats (last row).

### 4.2 Final-run simulation (`f2_sim_lh.py`, helper H2; `results/f2_sim_lh.txt`, `f2_sim_lh.json`, `f2_qH_check.txt`)

Faithful final-run islands (engine as above), N = 1000, the method's idealised grid (T = 14–18 stages, L = 9–13), 20 islands per n for LH16 (5 datasets × 4 islands) and 8 for LH20 (2 datasets). Set counts are taken after each stage's round and after the terminal rounds. W = W(S°), W₀ = {S° ∪ A : A ⊆ M}, W₂ = W ∩ {≤ 2 extras}, H = {x ⊇ S₀}.

| config, n | π₀(S₀) | π(S₀) | islands with a particle outside W | max stage-fraction outside W₂ | S₀ first scored (stage, mechanism) | crossing stage t* (grid[t*] ≥ φ*) | stage with n_t(H) ≥ 99 % | n_T(H) = N at end of bridge | min_t log P_t (h = 1_W / 1_{W₀}) | log Ẑ/Z (median) |
|---|---|---|---|---|---|---|---|---|---|---|
| LH16, 400 | 4.9·10⁻³ | 0.62–0.86 | 0/20 | 0.009 | 0, initial draw (20/20) | 8–9 (φ* = 0.13–0.15) | 13–15 | 20/20 | 0.000 / −0.37 | −0.006 |
| LH16, 1600 | 2.5·10⁻³ | 0.91–0.94 | 0/20 | 0.002 | 0 (16 islands), 1 Gibbs (4) | 9 (φ* = 0.040–0.045) | 15 | 20/20 | 0.000 / −0.10 | 0.002 |
| LH16, 6400 | 1.4·10⁻³ | 0.95–0.97 | 0/20 | 0.001 | 0 (15), 1 Gibbs (5) | 8–9 (φ* = 0.011–0.013) | 14–15 | 20/20 | 0.000 / −0.06 | 0.007 |
| LH20, 1600 | 1.3·10⁻⁵ | 0.88 | 0/8 | 0.002 | 1, Gibbs (8/8), φ₁ = 0.0135 < φ* | 12 (φ* = 0.060) | 18 | 8/8 | 0.000 / −0.13 | −0.015 |
| LH20, 6400 | 2.6·10⁻⁶ | 0.93 | 0/8 | 0.001 | 1, Gibbs (8/8), φ₁ = 0.004 < φ* | 12 (φ* = 0.014) | 17 | 8/8 | 0.000 / −0.10 | −0.015 |

Reading.
- **Closure holds in every island**: no particle outside W at any snapshot (76 islands, 14–18 stages each). The realised D4 envelope for h = 1_W is exactly 0 (log P_t = 0), as Corollary F3 says.
- **Extras.** The fraction of particles with ≥ 3 extras never exceeds 0.9 %. The basin fraction n_t(W₀)/N (0.6–0.97) equals the *exact* q_{φ_t}(W₀) at every stage (`f2_qH_check.txt`: simulated vs exact agree to ±0.01 at all 16 stages for n = 400, 1600, 6400), and so does the hub-complete fraction through the crossing (n = 400, stages 0–14: exact 0.006, 0.03, 0.08, 0.17, 0.30, 0.45, 0.61, 0.77, 0.91, 1.00 vs simulated 0.003, 0.03, 0.09, 0.17, 0.30, 0.46, 0.61, 0.78, 0.91, 1.00). **Inside the closed class the population sits at the local equilibrium q_φ(· | W) at every stage**: the ESS grid places 8–12 stages across the crossing and one Gibbs flip per round suffices to follow it. This is the fast/slow picture of PROOF §4 realised; it is also why LT (log Ẑ/Z within ±0.1) holds here, although Theorem F1 does not need it.
- **Scoring.** LH16 at these (n, N) is not strongly masked (Nπ₀(S₀) = 1.4–5), so S₀ is mostly an initial draw. LH20 is masked (π₀(S₀) = 10⁻⁵–10⁻⁶, Nπ₀(S₀) ≤ 0.013) and S₀ is scored **at stage 1 by a Gibbs flip in 8/8 islands at both n**, at φ₁ = 0.004–0.0135, *below* the crossing temperature φ* = 0.014–0.060: with SR, scoring S₀ from S° needs only one accepted uphill flip (odds e^{g₀+φ₁(g₁−g₀)} ≈ e^{−3.9}) followed by the *evaluation* of the second hub's flip (Lemma R with |Λ| = 2), and N = 1000 particles make that certain. The hub-complete class then takes over between the crossing stage t* = 12 and t* + 5, and n_T(H) = N in 76/76 islands at the end of the bridge. S₀ was never first scored in the terminal rounds and never missed; delivery to W₀ ∪ H at the terminal boundary: 76/76.

## 5. What fails and why

- **D4/D5 as the primary tool.** On a closed class the envelope is deterministic and D5's oscillation κ is irrelevant; on a non-closed class with *fitter* leaks D5 is sharp (SH) and the leaks are C1. The envelope is the right tool only for *reversible* leaks (F1′), i.e. exits to less-fit states that return. The three cases (closed / reversible leak / fitter leak) are the classification; W4-SHARE's (TRACK)+(OSC) is the middle one with the oscillation measured against the leak set only.
- **W = 𝓡_d (bounded extras) as the class.** It leaks through the (d+1)-st extra at rate n^{−1/2}polylog per round; N T_e n^{−1/2} → ∞. That is why W1/W4's sup-exit bounds on 𝓡_d were useless. The superset class fixes it in the exact Gram; in random designs the cut is forced (Remark 3.5) and F1′ is needed.
- **Uniform keep margins over all supersets in general designs.** They need the truth's partial signal to survive conditioning on any set of extras; with p close to n the ridge residual Q_x can be small (Q_x ≥ RSS_{[p]} ≈ σ²(n − p)), which is why Theorem F2 assumes p ≤ (1 − c₀)n. For p ≥ n only bounded-extras classes make sense.
- **Enlarging the class to absorb the DOM leak does not work.** W⁺ = W ∪ {x − j + b′} is not closed (the proxies of the missing j become Θ(n)-favourable: +175 nats, `f1b`); the leak must be treated as reversible (F1′), not closed. This was found by the exact check after the first draft of the proof.
- **PK in general.** For (ρ, ψ, g) with ρ close to 1 and many proxies present, the swap a_i → proxy can become posterior-favourable at states that miss b_i (PROOF §3.1 computation); such states have start mass (2p√n)^{−(g−1)} and are never visited, but a sup-over-W statement must exclude them by hand (cut W at d* proxies and treat the rest as a reversible leak).
- **Extras across resampling (CONJECTURE 4.3).** The re-weighting multiplies an extra-carrying particle by up to (2p√n)^{Δ_t(1−ε_n)} per extra; the Gibbs round re-equilibrates each null at its label, but the B + 1 swap labels and the independence proposal can re-insert extras after their label. The finite-constant bookkeeping is not written.

## 6. Needs escalation

1. **Lemma 3.4 with explicit remainders** (ridge Schur-complement step, the finite union of Lemma 3.1, the DOM case): routine, should be written by a stronger prover and checked cross-family.
2. **CONJECTURE 4.3 and §4.4** (extras across resampling; one-round scoring constant c₀ via Lemma R of O-BGIBBS): this is REP(W(S°)) on LH. Either W1-T24G's Theorem B is instantiated on W(S°) with bounded extras (the certificates are the proxies), or §4.4 is completed.
3. **PK(g − 1) as a theorem** for |ψ| < ρ < 1 (a finite population computation; the one-proxy cases are done).
4. **Theorem F1′ (reversible leaks) as a theorem**, for the DOM-failure case and for random designs: D4 with the two-level potential; routine but unwritten.
5. **CONJECTURE F2-iid** (random design): the uniform null-leakage bound over W_d. This is the only thing standing between the present result and a p ≫ n delivery theorem; W3-PXN's exact Beta laws are the input.
6. **Independent check of the reading of C1** (Corollary F3): that KEEP's two-endpoint form is exactly what C1 violates (π₀(o) > 0 with Nπ₀(o) ≳ 1), and that no BVS design can realise C1 inside a closed superset class (Lemma PD argument, PROOF §5.3).

## 7. Outside scope

- **Minimal method change, compared with LS0 and T39.** On LH none is needed for delivery: F2 delivers every particle. LS0 (deterministic search from S̃₀ = S°) delivers eligibility for free but needs TD′; T39 (scoring tracks) delivers through start mass b_n and fails on posterior barriers like (b2). The closed-class route is the only one that uses the bridge, and it is the one consistent with the n = 200 data (98 % of fresh scores from Gibbs, local search repaired 0 fits).
- **Paper text.** T38(b2) should read: DELIV(W(S°)) by Theorem F2 (every particle eligible) + REP(W(S°)). The hypothesis list is: LH exact Gram (or any family with two-endpoint keep margins, i.e. VIS-lin(S°) on the start side and a uniform posterior keep margin), PK, DOM, p ≤ (1 − c₀)n. Without DOM, use F1′ (reversible leaks). The ESS grid plays no role (consistent with W4's Proposition G).
- **The n = 200 study.** W3-PXN showed the study's masking is dilution, not LH-type cancellation; nothing here speaks to n = 200 (the constants in §4.2 need n > 4^g).
- **O-BGIBBS overlap.** BG1 proves pilot first-stage discovery when φ₁ ≥ φ_hub; F2 + §4 is the multi-stage complement: when φ₁ < φ_hub the particles wait in W(S°) (closed) until the grid passes φ_hub, then score S₀. Together they cover the final run on LH with no floor on the grid.

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Theorem F1 (closed-class delivery) | PROOF §1 | 0.99 | done (candidate) | — | no |
| Corollary F3 (no C1 under KEEP) | PROOF §2 | 0.98 | done | — | no |
| Lemmas 3.1–3.2 (unit structure) | PROOF §3.1 | 0.99 | done | — | — |
| PK(g−1) for (0.7, 0.5, 4) | exact check | 0.98 | done numerically; general CONJECTURE 0.8 | ρ → 1 with many proxies | — |
| Lemma 3.3 (start keep, via EXP′) | PROOF §3.2 | 0.95 | 0.9 | VIS-lin at all block configs | no |
| Lemma 3.4 (posterior keep, uniform over supersets) | PROOF §3.2 | 0.9 | 0.8 | ridge remainders; DOM case | no |
| DOM for LH with equal β, ψ = 0.5, ρ = 0.7 | exact check | 0.9 (fails marginally at LH20 n = 1600 in 1/4 replicates) | — | the a-proxy-rich supersets | — |
| Theorem F2 (LH exact Gram, DELIV(W(S°)) with all particles, under PK + DOM) | PROOF §3.3 | 0.9 | 0.75 | Lemma 3.4 | **no** |
| §4 scoring on W(S°) (REP) | PROOF §4 | 0.85 | 0.5 | extras across resampling (Conj. 4.3) | no |
| T38(b2) on LH exact Gram, no tweak, every fixed c | F2 + §4 + T38(0) | 0.85 | 0.5 | as above | **no** |
| F1′ (reversible leaks) | PROOF §5.2 | 0.9 | 0.85 | D4 with a two-level potential | no |
| F2-iid (p ≫ n) | §2 | 0.75 | 0.4 | uniform null leakage over W_d | no |
| Route (b2) outside T03's regime | fails through REPAIR (W4 PB) | 0.95 | — | ceiling for local methods | none helps |
