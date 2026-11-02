# O-BGIBBS — REPORT: bridge-Gibbs discovery (T38(b) without LS0)

Run of 2026-11-02, branch `theory/O-BGIBBS`. Notation: `Docs/Theory/theorems/00_COMMON.md`, W1-T38E (Lemma A, D2), W4-SHARE (Prop. M, Lemma PD), W1-EXP §4 (LH family). Every result is a **candidate**: not reviewed, not adopted.

## 1. Headline

1. **Multi-flip round lemma (Lemma R, PROVED, deterministic).** From a state x, one round at any φ scores a target z = x Δ Λ with probability ≥ P(O)·(1 − Dep_φ)₊·α_φ^{|Λ|−1}. Here O is an event on the round order, Dep_φ sums the change probabilities of the labels that are not in Λ, and α_φ is the smallest forward-move probability along the chain. D2's one-round step is the case |Λ| = 1.
2. **First-stage discovery theorem (Theorem BG1, PROVED given the round-lemma constants).** In the **pilot's first stage**, P(z ∉ 𝒮_cal | data) ≤ Hπ₀(𝒜) + e^{−Hπ₀(x°)/8} + 1/K + exp{−Hβ/(1 + 2Kρ_𝒩)} for every K > 0. The theorem uses no ESS share (Lemma S), no NB, no SHARE/LT, no envelope and no survival: everything happens in **one** round, so extinction never enters. Selection is controlled uniformly in φ by an endpoint ratio. By Lemma PD this ratio is ρ_𝒩 = [π₀(𝒩) + π₀(x°)π(𝒩)/π(x°)]/π₀(x°). The pilot floor φ₁ ≥ min(1, 1/T_e) (code fact) puts stage 1 above the downhill threshold φ_n → 0 of Proposition M.
3. **On the LH exact-Gram family, every premise of BG1 holds for every fixed c ≥ 1 (Proposition LH: the structure is PROVED; the score estimates are PROOF SKETCH).** Hence P(S₀ ∉ 𝒮) → 0 and, by T38(0), **P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for the original method, without LS0**. This covers c ≥ 2, where D2 does not apply. D2's b > 1/10 and NB hypotheses are not needed even for c = 1.
4. **Obstruction (precise; not a counterexample to the theorem).** BG1 requires stage 1 to be above the crossing temperature. On LH this means n/(T_e log(p√n)) → ∞. That holds asymptotically, because T_e = O(log² n), but needs roughly n ≳ 10⁴ with T₀ = 1000. Below that, discovery must happen at later stages, and the delivery/extinction question of route (b2) returns (§5). The final run's frozen grid has no floor, so the theorem is stated for the **pilot**. 𝒮_cal ⊆ 𝒮 by SR/CAL (SR_AUDIT item 5).

## 2. Statements

**Setting (all results).** EX-A (exact iid π₀ draws), EX-S (fresh uniforms; each particle's round order is a uniform permutation of the m = p + B + 2 labels, independent of everything else), SR (both Gibbs configurations are scored; every entered state and every swap or independence proposal is scored: SR_AUDIT items 1, 4). The pilot (M §6.6, `v3_calib.h:pilot_next_phi`, `v3_engine.h:run_island_s`) works as follows:
- it draws H = H_e particles iid from π₀;
- it sets φ₁ = pilot_next_phi(d(X_{1:H}), 0, H, T_e);
- it resamples multinomially with weights e^{φ₁ d(X_i)} and runs one round at φ₁.

**Code fact F (PROVED from code).** φ₁ ≥ min(1, 1/T_e). The rule returns 1, or the bisection point lo when lo ≥ 1/T_e, or otherwise min(1, 1/T_e).

### Lemma R (multi-flip round lemma) — PROVED

Fix x, z ∈ Ω with z ∈ Ω feasible, and let Λ := x Δ z (labels to add, z∖x, and to delete, x∖z).
- The chain set is 𝒞 := {x Δ A : A ⊆ Λ}; all of its states are feasible.
- O is an event that depends only on the permutation σ of the round. On O, the Λ labels run in an order in which every **forward** step (Gibbs on λ ∈ Λ∖A at x Δ A) is one of the steps counted in α_φ below.
- For a label l ∉ Λ, let 𝒞_l(σ) ⊆ 𝒞∖{z} be the chain states at which l can execute on the ideal path, before the last Λ label.
- Let ε_l(φ) := sup_{y ∈ 𝒞_l} P(the step of label l at y and φ changes the state) and Dep_φ := sup_{σ∈O} Σ_{l∉Λ} ε_l(φ) (taken over labels executed before the last Λ label).
- Let α_φ := the minimum over the forward steps (y, λ) used on O of κ_φ(y,λ)/(1 + κ_φ(y,λ)), where κ_φ(y,λ) = γ_φ(y⊕λ)/γ_φ(y). This is exactly the Gibbs forward-move probability, for an addition and for a deletion alike.

Then for every φ ∈ [0,1]:  P_x(the round at φ scores z) ≥ P(O)·(1 − Dep_φ)₊·α_φ^{|Λ|−1}.

Gibbs labels admit the uniform bound ε_l ≤ max_{y∈𝒞_l} max{κ₀(y,l), κ₁(y,l)} (Lemma A).

### Theorem BG1 (pilot first-stage bridge-Gibbs discovery) — PROVED

Data fixed. Let x°, z ∈ Ω and let 𝔅 ⊆ Ω with x° ∈ 𝔅 (the *basin*). Suppose:
- **(B)** for every y ∈ 𝔅 and every φ ∈ [φ_lo, 1], with φ_lo ≤ min(1, 1/T_e), a single round at φ from y scores z with probability ≥ β > 0 (for example via Lemma R);
- **(O)** Ω∖(𝔅 ∪ {z}) = 𝒜 ⊔ 𝒩, and ρ_𝒩 := Σ_{y∈𝒩} π₀(y)[1 + e^{d(y) − d(x°)}]/π₀(x°).

Then for every K > 0,

  P(z ∉ 𝒮_cal) ≤ H·π₀(𝒜) + exp{−Hπ₀(x°)/8} + 1/K + exp{−Hβ/(1 + 2Kρ_𝒩)}.

By Lemma PD (log γ₀ + d = F − log m(∅)), ρ_𝒩 = π₀(𝒩)/π₀(x°) + π(𝒩)/π(x°). This is a **two-endpoint** quantity: start mass of the light outsiders against x°, plus posterior mass of the light outsiders against x°.

**Corollary BG1-∞ (PROVED given the premises).** Along R1/R4, suppose:
- π₀(x°) ≥ b > 0;
- H·π₀(𝒜) → 0 and ρ_𝒩 = O_P(1), both in P₀-probability;
- β ≥ β₀ > 0 w.p. → 1.

Then P(z ∉ 𝒮) → 0. Here H = H₀ ≥ 0.2·max(2500, n, p) → ∞; take K = K_n → ∞ with K_n = o(H).

### Proposition LH (premises on the linked-hub family, exact Gram) — structure PROVED, score estimates PROOF SKETCH

**The family.** LH exact Gram (W1-EXP §4.1–4.2, T38 (b1-LH)):
- X′X = (n−1)Σ_LH and p ≤ n − 1;
- c ≥ 1 linked pairs (a_i, b_i, ψ_i) with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i});
- g ≤ B_n < 2g;
- fixed nonzero coefficients and fixed σ*² > 0.

**Objects.** M = {b_1,…,b_c} are the masked hubs, x° = S° = S₀∖M and z = S₀. The *masked content* of a state is y ∩ ⋃_i C_{b_i}. The basin is 𝔅 = 𝔅_M ∪ 𝔅_P:
- 𝔅_M := {S° ∪ A : A ⊊ M};
- 𝔅_P := {S° ∪ {k} : k ∈ ⋃_i C_{b_i}∖M} (a masked *proxy*).

The outsiders split as follows:
- 𝒩 := {y ≠ S° : y has no masked content};
- 𝒜 := the remaining states other than z: masked content together with any other deviation from S°, or ≥ 2 masked members not of the form S° ∪ A.

**Conclusions.** W.p. → 1:
- (i) π₀(S°) → 1 [W1-EXP Thm 5(a), PROVED, VERIFIED];
- (ii) H·π₀(𝒜) = O_P(max(n,p)/(pn) + max(n,p)/(p²n)) → 0;
- (iii) ρ_𝒩 = O_P(2^B n^{−1/2}) → 0;
- (iv) the constants of (B) satisfy β ≥ min{g^{−c}, [(c+1)·C(c+1+c(g−1)+B, c+1)]^{−1}}·(1 − o_P(1)), uniformly in φ ∈ [1/T_e, 1], provided n/(T_e·log(p√n)) → ∞. That holds under R1 because T_e = 4^e·max(1000, ⌈log₂(n+p+1)⌉²).

Therefore **P(S₀ ∉ 𝒮) → 0 on LH exact Gram for every fixed c ≥ 1**, for the original method. With T38(0) and (P) on LH [W1-EXP Thm 5(d)]: P(𝒪 ∩ {Ŝ ≠ S₀}) → 0, and liminf P(𝒪 ∩ {Ŝ = S₀}) ≥ 1 − limsup P(U).

## 3. Proofs

### 3.1 Lemma R

Condition on σ ∈ O. Walk through the labels in order up to the last Λ label λ*. Call the run **on track** at a time point if the current state is x Δ A, where A is the set of Λ labels already executed. On track, the state before λ* is in 𝒞∖{z}, because x Δ A = z iff A = Λ.
- A non-Λ label l executed on track runs at some y ∈ 𝒞_l(σ). By definition it changes the state with probability ≤ ε_l(φ), using its own fresh uniform (EX-S).
- A Λ label λ ≠ λ* executed on track moves forward with probability ≥ α_φ (heat-bath Gibbs: addition o = κ/(1+κ); deletion 1 − o = 1/(1 + γ_φ(y)/γ_φ(y−λ)) = κ/(1+κ) with κ = γ_φ(y−λ)/γ_φ(y)).
- Each label executes exactly once per round.

By the chain rule over the executed labels, P(on track just before λ* | σ) ≥ ∏_l(1 − ε_l)·α_φ^{|Λ|−1} ≥ (1 − Σ_l ε_l)₊·α_φ^{|Λ|−1}. The second inequality uses ∏(1−u_i) ≥ 1 − Σu_i for u_i ∈ [0,1], with ε_l truncated at 1.

At λ*, the state is y = z ⊕ λ*. Gibbs evaluates y ⊕ λ* = z, which is feasible since z ∈ Ω, before the accept draw (SR, `v3_engine.h:113–132`). So z is scored. Finally, integrate over σ ∈ O. The event O depends on the order only, and the order is independent of the uniforms. ∎

Labels executed after λ* (non-Gibbs labels, protected proxies) are irrelevant, because scoring happens at the evaluation. This is where SR replaces survival: **one evaluation suffices.**

### 3.2 Theorem BG1

Define three events.
- E₁ := {no initial draw lies in 𝒜}. By a union bound, P(E₁ᶜ) ≤ Hπ₀(𝒜).
- E₂ := {n° ≥ Hπ₀(x°)/2}, where n° := #{i : X_i = x°} ~ Bin(H, π₀(x°)). The Chernoff lower tail gives P(E₂ᶜ) ≤ e^{−Hπ₀(x°)/8}.
- E₃ := {W ≤ K·E W}, with W := Σ_{i: X_i∈𝒩}[1 + e^{d(X_i) − d(x°)}] and E W = Hπ₀(x°)ρ_𝒩. Markov's inequality gives P(E₃ᶜ) ≤ 1/K.

**Uniformity in φ.** For every φ ∈ [0,1] and every Δ ∈ ℝ, e^{φΔ} ≤ 1 + e^{Δ}. Normalise the weights by e^{φd(x°)}:
- each x°-draw has weight 1;
- 𝔅-draws have positive weight;
- on E₁, the remaining draws lie in 𝒩 ∪ {z}, and draws of z are already scored, so assume there are none;
- the 𝒩-draws have total weight ≤ W.

The resampling probability of 𝔅 is ω(φ) = Σ_𝔅 w/(Σ_𝔅 w + Σ_𝒩 w). Since t ↦ t/(t + c) is increasing and Σ_𝔅 w ≥ n°, ω(φ) ≥ n°/(n° + W) for **every** φ. On E₂ ∩ E₃ this gives ω(φ) ≥ 1/(1 + 2Kρ_𝒩) =: ω̲.

This holds in particular at the data-dependent φ₁. φ₁ is a function of the draws. Given the draws, the resampled particles are iid from the weighted empirical law, so the number of 𝔅 particles is Bin(H, ω(φ₁)).

By Fact F, φ₁ ∈ [min(1, 1/T_e), 1] ⊆ [φ_lo, 1]. Given the resampled population, the rounds use independent uniforms and orders (EX-S), and each 𝔅 particle scores z with probability ≥ β by (B). Hence P(z unscored | draws) ≤ E[(1 − βω(φ₁))^H] ≤ exp{−Hβω̲} on E₁ ∩ E₂ ∩ E₃. Add the excluded events. ∎

**Lemma PD form of ρ_𝒩.** π₀(y)e^{d(y)−d(x°)} = π₀(x°)·e^{F(y)−F(x°)} = π₀(x°)π(y)/π(x°). Sum over 𝒩.

**Corollary.** Take K = K_n → ∞ with K_nρ_𝒩 = o(H) in probability. The first, second and fourth terms → 0 when H → ∞, π₀(x°) ≥ b and β ≥ β₀. 𝒮_cal ⊆ 𝒮 by definition (𝒮 includes calibration; SR_AUDIT item 5 for the HPM). ∎

### 3.3 Proposition LH

Exact Gram: within-sample correlations equal Σ_LH. Write μ = Σ_i β_i(x_{a_i} − ψ_i x_{b_i}) + Σ_vis β_h x_{j_h}.

**(P1) Projection algebra (PROVED).** x_{b_i} − ψ_i x_{a_i} is orthogonal to every column outside C_{b_i}. For k ∈ C_{a_i}, Cov(x_k, x_{b_i}) = ψρ_a = ψ·Cov(x_k, x_{a_i}); other groups are independent. Hence:
- (a) for any column set T with no masked content, P_Tμ = P_Tμ₁, where μ₁ := Σ_iβ_i(1−ψ_i²)x_{a_i} + Σ_visβ_hx_{j_h} is supported on S°, and r := μ − μ₁ = −Σ_iψ_iβ_i(x_{b_i} − ψ_ix_{a_i}) ⟂ col(T), with ‖r‖²/(n−1) = Σ_iψ_i²β_i²(1−ψ_i²) =: c_r > 0;
- (b) C_{b_i} is orthogonal to μ (W1-EXP Lemma 4.1(b));
- (c) given a_i, b_i ∈ T, every k ∈ C_{a_i} ∪ C_{b_i} has zero partial covariance with μ;
- (d) given a_i ∈ T and b_i ∉ T, every k ∈ C_{a_i}∖{a_i} has zero partial covariance with μ: Cov(x_k − ρx_a, x_b − ψx_a) = ψρ − ψρ − ρ(ψ − ψ) = 0;
- (e) given T ⊇ {a_i} (with or without one proxy k ∈ C_{b_i}) and b_i ∉ T, the partial covariance of x_{b_i} with μ is a fixed nonzero multiple of β_iψ_i√(1−ψ_i²). If k ∈ T, the factor (1 − ρ_{b_i}²·(·)) stays bounded away from 0, because ρ_{b_i} < 1 and λ_min(Σ) ≥ (1−ψ₊)(1−ρ₊).

**(i)** This is W1-EXP Theorem 5(a).

**(ii) (PROOF SKETCH).**
- γ₀ = ϖ(|S|)∏_b r_b(S ∩ C_b). Since C_{b_i} ⟂ μ, the table r_{b_i}(E) for E ≠ ∅ is a pure-noise Bayes factor with the full response, of order (n+1)^{−|E|/2}e^{O_P(1)}. The exponent (1−A)Z²/2, where A is the total R² of y, has finite exponential moments, and the number of E is ≤ 2^g.
- The size-prior factor per added variable is (k+1)/(2p−1−k) = O(s₀/p) for bounded sizes.
- So π₀(≥ 1 masked member) = O_P(c2^g/(p√n)) and π₀(≥ 2 masked members) = O_P((2^g/(p√n))²).
- Conditionally on the masked content, the non-masked part has the same table structure, up to bounded size-prior factors. So it deviates from S° with probability O_P(2^Bn^{−1/2}) (the proof of (i)).
- Multiply by H ≤ 0.21·max(2500, n, p)·4^e.
- *To be written in full:* the size-prior coupling is bounded crudely (the ratio ϖ(k+j)/ϖ(k) ≤ (K/(2p−K))^j up to constants).

**(iii) (PROOF SKETCH).** The first term is π₀(𝒩)/π₀(S°) = (1 − π₀(S°) − π₀(masked))/π₀(S°) → 0 by (i) and (ii).

For the second term, by (P1a) every y ∈ 𝒩 ∪ {S°} has y′P_y y = (μ₁+ε)′P_y(μ₁+ε), and ‖y‖² = ‖μ₁+ε‖² + C with C := ‖r‖² + 2r′ε, the **same** C for every such y. So F restricted to 𝒩 ∪ {S°} equals the score of a *well-specified* problem with these features:
- design: the non-masked columns (SE by W1-EXP Lemma 4.1(a));
- truth S°, with fixed nonzero coefficients β_i(1−ψ_i²) and β_h;
- noise ε;
- every residual sum Q_y shifted by the common constant C ≥ (1−o_P(1))(n−1)c_r.

The two kinds of comparison then go as follows.
- **Additions of null-like columns** (P1a,d). The overfitting factor is (n+1)^{−1/2}(1 − x)^{−ν} with x = (u′ε)²/(Q_y + …). Because Q_y ≥ C + χ²_{n−|y|−1}σ*², this is ≤ (n+1)^{−1/2}exp{a·Z²/2} with a ≤ σ*²/(c_r + (1−η)σ*²) < 1 w.p. → 1. So **no truncation is needed**: E e^{aZ²/2} = (1−a)^{−1/2}.
- **Deletions or swaps of S° members** lose Θ(n) nats (fixed coefficients, SE).

The T03 argument (locked T03; SE, BM-∞) for this problem then gives π(𝒩)/π(S°) = O_P(n^{−1/2}·2^{O(1)}) → 0. The common shift C only weakens the overfitting gains.

*To be checked:* T03's proof is written for y = μ + ε with μ in the column span. Here the reduction requires its RSS bookkeeping to carry the common additive constant C. The direction is favourable, but this step is a reduction, not a re-proof.

**(iv) (PROOF SKETCH; Lemma R applied).**

*Chains from y ∈ 𝔅_M.* Λ = M∖A, with additions only.
- O := {in every masked group, the hub's label precedes the labels of the other members of C_{b_j}}, so P(O) = g^{−c}.
- Forward steps add b_j at a state y′ ⊇ S° with no masked proxy. Then log κ₀(y′, b_j) = log ϖ-ratio + log BF_noise ≥ −λ_n − O_P(1), with λ_n := log(2p) + ½log(n+1), and log κ₁(y′, b_j) ≥ c₂n w.p. → 1 by (P1e).
- By log-linearity, for φ ≥ 1/T_e: log κ_φ ≥ c₂n/T_e − λ_n − O_P(1) → +∞, so α_φ → 1 uniformly.

The labels that are not in Λ, and their change probabilities ε_l, fall into these classes:
- *Null-like Gibbs labels* (null groups; non-hub members of visible groups and of C_{a_i} by (P1c,d); non-hub members of C_{b_j} only after b_j is present, by O and (P1c)). max(κ₀, κ₁) is ϖ-ratio × noise BF. On every chain state except S₀ itself the residual keeps ≥ one missing-hub component, so a < 1 and Σ_l = O_P(n^{−1/2}).
- *Deletion of S° members.* Both endpoints are e^{−Θ(n)}: the a_i are visible in their blocks with coefficient β_i(1−ψ_i²) ≠ 0. Hub labels are in Λ and execute only once, so an added hub is never re-deleted in the same round.
- *Uniform and neighbour swaps.* The MH acceptance is ≤ min(1, ρ₀^{1−φ}ρ₁^{φ}). Swapping out an S° member costs e^{−Θ(n)} at both endpoints. Swapping out an added b_j costs ρ₀ = e^{O_P(log p)} and ρ₁ = e^{−Θ(n)}, so the actual-φ ratio is ≤ e^{O_P(log p) − Θ(n)/T_e} → 0.
- *Independence proposal.* At S° it moves only if the proposal is ≠ S°: probability ≤ 1 − π₀(S°) → 0. At y′ ⊋ S°, d(y′) − d(S°) ≥ c₂n − O(log n), so accepting a typical proposal costs e^{−φ(…)} → 0, and fitter proposals have π₀ = O_P((p√n)^{−1}).

So Dep_φ → 0 uniformly in φ ∈ [1/T_e, 1], and β ≥ g^{−c}(1 − o_P(1)).

*Chains from S° ∪ {k} ∈ 𝔅_P (k ∈ C_{b_i}∖{b_i}).* Λ = M ∪ {k}, with k deleted last.
- O_k := {the c hubs and k precede every other masked-group member and all B+1 swap labels, and k is last among them}, so P(O_k) = [(c+1)·C(c+1+c(g−1)+B, c+1)]^{−1}.
- The swap labels must be protected here. Between b_i's addition and k's deletion, the useless proxy k could be swapped for a null with probability Θ(1/|y|).
- Forward steps: the hub additions use (P1e) with a proxy present, so α → 1 as above. The deletion of k at y ∋ b_i, k: by (P1c), keep-odds ≤ max(κ₀, κ₁) = O_P(p^{−1}n^{−1/2}), so the deletion probability → 1.
- The remaining Dep terms are as in the 𝔅_M case.

So β ≥ P(O_k)(1 − o_P(1)). ∎ (sketch)

## 4. Evidence

`scripts/bg1_first_stage.py`, which uses the engine `scripts/bvs_core.py`. The engine is copied verbatim from theory/W4-SHARE: a faithful small-p re-implementation, exact scores, SR, every proposal recorded. Seed 20261102. The script runs the setup below and prints its output to `scripts/bg1_first_stage.txt`.
- Design: LH exact Gram, p = 16, g = B = 4, ρ = 0.7, ψ = 0.5, β = 1, σ = 1, c = 2.
- For each replicate (40 per n, fresh noise): H iid π₀ draws, the engine's pilot rule φ₁, multinomial resampling, ONE round at φ₁. S₀ counts as scored if it appears among the evaluated or proposed states of that round.

RESULTS: see §4.1 (filled in when the Owls job completes).

## 5. What fails and why (and the precise obstruction)

- **The obstruction is temperature, not survival.** BG1 needs stage 1 to sit above the crossing threshold of the chain, φ_hub := inf{φ : every forward hub step has odds ≥ some ω_n}. On LH, φ_hub ≈ λ_n/(λ_n + c₂n). Stage 1 is ≥ 1/T_e only by the floor, so the asymptotic condition is n ≫ T_e·log(p√n). At T₀ = 1000 that means n ≳ 10⁴–10⁵, depending on c₂ = ψ²β²(1−ψ²)/(2(σ² + c_r)). The pilot's ESS rule often gives φ₁ ≫ 1/T_e, which helps, but that is data-dependent. When φ₁ < φ_hub, multi-flip discovery must happen at a later stage. Then the particles at S° must survive selection by fitter outsiders until φ ≥ φ_hub, and that is exactly the D4/D5 envelope problem (W4-SHARE) or the C1 extinction mechanism. This run gives no BVS counterexample to later-stage discovery. W4-SHARE's 500/500 numerical record suggests none exists in T03's regime.
- **The final run's first stage.** The same proof works for the final run with H → N_e, and there φ₁^f is 𝓒-measurable and independent of the draws, so the proof is even simpler. But the candidate grid (M §6.7) has **no floor**. Since V contains S₀-type models, the restricted ESS is designed to insert temperatures below the crossing (ρ_V(0, b) ≥ 0.9 forces b ≲ φ_hub/2 when S₀ ∈ V). So the final run's stage 1 is typically *below* φ_hub. Discovery in the final run is then a multi-stage delivery problem, which this run does not solve. The pilot statement avoids it.
- **The ESS share route (D2-style).** It does not iterate (W4-SHARE §5), and it needs NB, which fails whenever a masked proxy is drawn: d-spread Θ(n) ≫ T_e. BG1 sidesteps both. A drawn masked proxy is a *basin* state, so letting it take over the resampling is harmless.
- **Uniform swap with a useless proxy present.** This is a real Θ(1/|y|) disruption. It is handled only by protecting the swap labels in O_k, which costs a combinatorial constant (§3.3(iv)).

## 6. Needs escalation

1. **Proposition LH (ii)–(iv): the score estimates.** In particular:
   - the reduction of (iii) to T03 with a common RSS shift C;
   - the uniform null-leakage bound at the chain states adjacent to S₀ (a = 1 there, so truncation is needed; W1-EXP §4.3(iv)-type argument);
   - the size-prior coupling in (ii).

   All are routine but unchecked. A stronger prover should write them with explicit constants.
2. **Independent check of Lemma R and BG1.** The proofs are short. The points to check are the uniform-in-φ normalisation step (e^{φΔ} ≤ 1 + e^{Δ}, which lets the data-dependent φ₁ through) and the conditional iid structure of multinomial resampling given the draws.
3. **Code check.** Fact F (`pilot_next_phi` floor) and "pilot scored models enter 𝒮 / the HPM store" (SR_AUDIT item 5 says the calibration context is inherited).

## 7. Outside scope

- **LH-iid (p ≫ n, W3-PXN):** the same argument should go through on the event "blocks = groups". There, (P1)'s exact orthogonality becomes O_P(√(log p/n)) approximate orthogonality, and the common-shift structure of (iii) holds only approximately. Status: CONJECTURE.
- **Finite-n reading:** at n = 200, T_e = 1000 ≫ n, so the theorem says nothing about the study. In the masked designs of W4-SHARE (n = 400–4000), discovery happened at stages 1–7 (s2b), consistent with "stage 1 when φ₁ ≥ φ_hub, later otherwise".

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| Lemma R | §2 | 0.97 | done (candidate) | the on-track chain rule with order-only O | no |
| Theorem BG1 | §2 | 0.95 | done (candidate) | uniform-in-φ selection bound; iid resampling given draws | no |
| Prop. LH (i) | W1-EXP Thm 5(a) | 0.97 | done | — | no |
| Prop. LH (ii)–(iv) | §2 | 0.85 | 0.75 | T03 reduction with a common RSS shift; null leakage next to S₀ | no |
| T38(b) without LS0 on LH exact Gram, every fixed c ≥ 1 | BG1 + LH + T38(0) | 0.85 | 0.7 | as above; asymptotic only (n ≫ T_e log n) | **no** |
| Final-run (no-floor) discovery, or a finite-n version | OPEN | 0.75 | 0.3 | delivery to φ ≥ φ_hub (W4-SHARE D4/D5) | no |
