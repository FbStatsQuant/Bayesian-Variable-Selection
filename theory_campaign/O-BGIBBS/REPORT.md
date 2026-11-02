# O-BGIBBS — REPORT: bridge-Gibbs discovery (T38(b) without LS0)

Run of 2026-11-02, branch `theory/O-BGIBBS`. The first draft (Lemma R, BG1, Prop LH) came from the server instance. It was continued on the laptop, which added BG1′, BG2, LH-rate, BG3, LH-lock and all numerics in §4. Notation: `Docs/Theory/theorems/00_COMMON.md`, W1-T38E (Lemma A, D2), W4-SHARE (Prop. M, Lemma PD), W1-EXP §4 (LH family). Every result is a **candidate**: not reviewed, not adopted.

## 1. Headline

1. **Main result: the final run alone discovers S₀ on the masked family LH, for every fixed c, with no LS0, no pilot, no temperature condition and no survival hypothesis (Theorem BG3, PROVED; Proposition LH-lock, PROOF SKETCH for p fixed).**
   - The start set 𝒰 = {y ⊇ S°} is *locked*: leaving it costs e^{−Θ(n)} at both endpoints γ₀ and γ₁, at every φ. So no particle ever leaves it.
   - The L + 4 terminal rounds at φ = 1 have **no resampling**, and from every y ∈ 𝒰 they are downhill to S₀.
   - The bound is P(S₀ ∉ 𝒮) ≤ Nπ₀(𝒰ᶜ) + N(T + L + 4)m·e^{−c₃n} + e^{−N(L+4)β₁} + o(1).
   - With T38(0): **P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for the original method, without LS0.** This answers W4-T38FULL item 6 on LH with p fixed.
   - The deterministic premises (lock and downhill gaps C1–C3) are verified by exhaustive enumeration for both simulated designs (c = 2 and c = 3).
   - Simulated islands: no particle ever left 𝒰 (min_t N_𝒰/N = 1 in 19/19 islands); the minimum q₁ over the 28 tested states per island is 0.019–0.15; the implied miss bound in the terminal rounds is ≤ 10⁻³²⁰.
2. **Discovery is a hazard, not a survival event (Theorem BG2, PROVED).** P(S₀ never scored by round t₁) ≤ P(Λ_{t₁} < Λ) + e^{−Λ}, where Λ_t = Σ_{s≤t} m_sβ_s is the cumulative scoring hazard of predictable good sets. One scoring event suffices (SR), and what happens after it is irrelevant. *Time-to-score* is the time for Λ to diverge; *time-to-extinction* is the time for m to reach 0. On LH, extinction of 𝒰 takes ≳ e^{c₃n}/N rounds, while scoring takes O(1) rounds at φ = 1, and usually already happens at stage 1.
3. **Bridge-stage discovery, quantified (Lemma R, Theorem BG1 / Corollary BG1′, PROVED; Proposition LH-rate, PROOF SKETCH).**
   - One round at φ from the start mode scores S₀ with probability ≍ P_c·min(1, e^{φc₂n−λ_n})^{c−1}, with λ_n = log(2p√(n+1)).
   - Stage-1 discovery holds w.p. → 1 in the pilot (via its floor φ ≥ 1/T_e, for every c, when n ≫ T_e log n), and in both the pilot and the final run at **any** temperature for c = 1, and for c = 2 with p fixed (p = o(√n): CONJECTURE).
   - Simulated: c = 2 was scored in pilot round 1 in **160/160** replicates (n = 400–25600), and in the final run's stage 1 in every replicate where it was not an initial draw (31/31; 5 were initial draws). For c = 3, the stage-1 hazard is Θ(1) and S₀ was scored at stage 1–2.
4. **Obstructions (precise).**
   - (L2) fails on posterior-barrier designs (W4-SHARE PB: COUNTEREXAMPLE at finite n, to every local kernel).
   - (L1) would fail if a start-mode member were not supported by its own block table (not the case on LH).
   - For p → ∞ (LH-iid), the uniformity of the gaps over supersets and the order constant are open (CONJECTURE).
   - Bridge-stage discovery for c ≥ 3 needs a survival input (W4-SHARE D4/D5). BG3 makes it unnecessary on LH.

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

### Theorem BG2 (cumulative scoring hazard: time-to-score against time-to-extinction) — PROVED

Data (and, for the final run, 𝓒) fixed. Consider one island, pilot or final, with stages t = 1, …, T followed by the terminal rounds t = T+1, …, T+L+4 at φ = 1. Let 𝓕_t⁻ be the σ-field of everything up to and including the resampling of stage t, before the stage-t round. For the terminal rounds, 𝓕_t⁻ is everything before round t; they have no resampling. Let Y_t = (Y_t^1, …, Y_t^N) be the population entering the round of stage t.
- Fix z ∈ Ω.
- For each t, let G_t ⊆ Ω and β_t ∈ [0,1] be 𝓕_t⁻-measurable, such that P(the stage-t round of a particle started at y scores z | 𝓕_t⁻) ≥ β_t for every y ∈ G_t.
- Let m_t := #{i : Y_t^i ∈ G_t}, and let **Λ_t := Σ_{s≤t} m_sβ_s** be the *cumulative scoring hazard*.

Then for every t₁ and every Λ > 0:

  P(z is not scored in rounds 1, …, t₁) ≤ P(Λ_{t₁} < Λ) + e^{−Λ}.

**Reading.** One scoring event is enough, and Λ_t is the expected number of scoring opportunities up to t. The only way discovery can fail is that the hazard stays O(1). That happens either because β is small at the temperatures visited (*time-to-score*, a kernel property) or because m_t falls to 0 first (*time-to-extinction*, a selection property). Extinction after the first score is irrelevant, by SR. The terminal rounds have no resampling, so a single particle in G at the end of the bridge contributes ≥ Σ_{t>T}β_t·1{it is still in G_t} to the hazard.

### Corollary BG1′ (BG1 with a temperature-dependent constant; final-run version) — PROVED

In Theorem BG1, replace (B) by **(B′)**: for every φ ∈ [φ_lo, 1] and every y ∈ 𝔅, one round at φ from y scores z with probability ≥ β(φ). Put β_* := inf_{φ∈[φ_lo,1]} β(φ). Then
- BG1's bound holds with β replaced by β_*;
- **the final run's first stage** satisfies the same bound with H → N and φ_lo = 0: P(z not scored in the final run's stage 1) ≤ Nπ₀(𝒜) + e^{−Nπ₀(x°)/8} + 1/K + exp{−Nβ_*/(1 + 2Kρ_𝒩)}, where β_* = inf_{φ∈[0,1]}β(φ);
- the conclusion P(z ∉ 𝒮) → 0 needs only **Hβ_* → ∞** (resp. Nβ_* → ∞). A constant β₀ is not needed.


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

### Proposition LH-rate (the scoring rate on LH, exact Gram) — 𝔅_M part PROOF SKETCH; uniform-in-φ proxy part CONJECTURE

Setting and objects as in Proposition LH, with c ≥ 1 fixed and λ_n := log(2p) + ½log(n+1).
- Let 𝔇 be the set of **dangerous labels**: the cg Gibbs labels of the masked groups C_{b_1}, …, C_{b_c}, the uniform swap, the B neighbour swaps and the independence proposal, so |𝔇| = cg + B + 2.
- Put P_c := 1/C(cg+B+2, c).
- Let c₂ > 0 be the gain constant of (P1e): log κ₁(y′, b_i) ≥ c₂n − O_P(log n) on every chain state y′ ∌ b_i, with or without one masked proxy.

**(a) Rate from the start mode (PROOF SKETCH).** W.p. → 1, **uniformly in φ ∈ [0,1]**,

  β_{S°}(φ) := P_{S°}(one round at φ scores S₀) ≥ P_c·(1 − o_P(1))·ᾱ_φ^{c−1},  ᾱ_φ := min_{y′,i} κ_φ(y′,b_i)/(1+κ_φ(y′,b_i)) ≥ ½·min{1, e^{φc₂n − λ_n − O_P(log n)}},

where the minimum runs over the chain states y′ = S° ∪ A, A ⊊ M. The order event is O := {within 𝔇, the c hub labels come first}, with P(O) = P_c.

**(b) Upper bound (PROOF SKETCH).** β_{S°}(φ) ≤ C_c·max_{y′,i}min{1, κ_φ(y′,b_i)}^{c−1} + 1 − π₀(S°) + O_P(n^{−1/2}). Here C_c is a combinatorial constant. Scoring S₀ in one round from S° requires c − 1 accepted hub additions, or a detour through a masked proxy, which needs at least as many accepted masked-content additions; the independence proposal draws a state with masked content with probability o_P(1).

**(c) Consequences for the stage-1 hazard of BG1′, restricted to the start-mode draws.** Write h₁ := n°·β_{S°}(φ₁), where n° ≈ Hπ₀(S°) (pilot) or Nπ₀(S°) (final run). Then:
- **(R1) c = 1:** h₁ ≥ n°P₁(1 − o_P(1)) → ∞ at **every** φ, including φ = 0. No temperature condition.
- **(R2) c = 2:** at φ = 0, ᾱ₀ ≍ (p√n)^{−1}e^{O_P(1)}, so h₁ ≳ H/(p√n) → ∞ iff p = o(√n) along R1 (where H ≍ max(n, p)). No temperature condition.
- **(R3) every c, pilot:** φ₁ ≥ 1/T_e and n/(T_eλ_n) → ∞ give ᾱ_{φ₁} → 1 and h₁ ≍ H. This is the predecessor's route.
- **(R4) scoring temperature.** In general h₁ → ∞ iff log H − (c−1)·[λ_n − φ₁c₂n]₊ → ∞ (up to O_P(log n) terms in the exponent). So define

  φ_sc(n) := [λ_n − log H/(c−1)]₊/(c₂n).

  Then φ_sc = 0 for c ≤ 2 (with p = o(√n) when c = 2). For c = 3 at fixed p, φ_sc is borderline: H·ᾱ₀² ≍ 1/p², so the hazard is Θ(1). For c ≥ 4, φ_sc ≍ (½ − 1/(c−1))·log n/(c₂n) > 0.

**(d) The proxy draws (CONJECTURE for the uniform-in-φ version).** Draws in 𝔅_P (S° plus one masked proxy k) occur with frequency ≍ cg/(p√n) and carry relative selection weight e^{φΔ_k}, where Δ_k = d(S°∪{k}) − d(S°) = Θ(n). Their one-round scoring probability is ≥ P_c^P·ᾱ_φ^{c}, which carries one more power of ᾱ than the start-mode chain.
- For φ ≥ 1/T_e under (R3), both are → 1·constant, and Proposition LH (iv) applies.
- For φ near 0, the proxies weigh ≤ (p√n)^{φ₁Δ_k/λ_n}·cg/(p√n) relative to S° and are harmless.
- In an intermediate window, the proxies can dominate the resampled population while ᾱ_φ < 1. There the stage-1 hazard is ≥ H·P_c^P·(p√n)^{−θ}, with θ := (1 − c₂n/Δ_k)₊ < 1 (a first-order computation, not proved).

So **(R1)–(R2) are PROOF SKETCH for p fixed** (then H(p√n)^{−θ} → ∞). For p → ∞ they are CONJECTURE until the window computation is written out.

**Obstruction (c ≥ 3, final run; PROOF SKETCH from (b), supported numerically).** The final grid's first stage is at the scale of the inverse fitness spread of V, because V contains S₀-type models: numerically n·φ₁ᶠ = 18, 21, 26, 29 at n = 400, 1600, 6400, 25600, so it grows at most logarithmically. By (b), the final run's stage-1 hazard is ≤ N·C_c·ᾱ_{φ₁ᶠ}^{c−1}·e^{O_P(1)}. If φ₁ᶠc₂n ≤ λ_n − (log N + ω_n)/(c−1), this tends to 0. Numerically it is Θ(1) for c = 3 (≈ 0.6–2.1 at n = 400; ≈ 1 at n = 6400), and the (R4) count makes it → 0 for c ≥ 4 unless φ₁ᶠ ≥ φ_sc. Discovery must then happen at a later stage t with φ_t ≥ φ_sc. With the near-geometric ESS grid this is O(log λ_n) = O(log log n) stages later, and Theorem BG2 needs the start-mode count m_t to stay ≍ N until then. That is a delivery (non-extinction) statement over O(log log n) stages, of the type of W4-SHARE D4/D5 on W ⊇ {S°}. This run does not prove it. **The hazard formulation shows it is exactly what is missing.**

### Theorem BG3 (locked start set + terminal downhill: the final run alone) — PROVED (deterministic given (L1), (L2))

Data and 𝓒 fixed. Take one final island: N iid π₀ draws, the grid 0 = φ₀ < φ₁ < … < φ_T = 1 with T ≤ T_e, multinomial resampling at each stage, then the L + 4 terminal rounds at φ = 1, which have **no resampling** (`v3_engine.h:352–373`). Let z ∈ Ω and 𝒰 ⊆ Ω with z ∈ 𝒰. Define:
- **(L1) lock:** ε_𝒰 := sup_{y∈𝒰, φ∈[0,1]} P_y(one round at φ ends outside 𝒰);
- **(L2) terminal downhill:** β₁ := inf_{y∈𝒰} P_y(one round at φ = 1 scores z).

Then

  P(z is not scored in the island) ≤ Nπ₀(𝒰ᶜ) + N(T + L + 4)·ε_𝒰 + exp{−N(L + 4)β₁}.

In words: if the start mass sits on a set that no round can leave except with exponentially small probability, and from which the φ = 1 kernel scores z with probability bounded below, then the terminal rounds score z. Every particle is still in 𝒰 at the end of the bridge, so selection never needs to be controlled. **Time-to-extinction** of 𝒰 is ≳ 1/(Nε_𝒰) rounds; **time-to-score** at φ = 1 is ≲ 1/(Nβ₁) rounds.

### Proposition LH-lock (premises of BG3 on LH exact Gram, p fixed) — PROOF SKETCH; the deterministic inputs are checked exhaustively for the two simulated designs

LH exact Gram as in Proposition LH (blocks = groups, so g ≤ B < 2g), with c ≥ 1 and **p fixed**, n → ∞. Let 𝒰 := {y ∈ Ω : y ⊇ S°}, and let f(T) := θ′R_{·T}R_{TT}^{−1}R_{T·}θ be the population fit; the sample fit is (n−1)f(T). Assume the deterministic gaps:
- (C1) f(T) − f(T∖j) > 0;
- (C2) f(T) − f(T∖j ∪ {l}) > 0;
- (C3) f(T ∪ {b}) − f(T) > 0;

for all T ⊇ S°, j ∈ S°, l ∉ T and masked hubs b ∉ T. Assume also their γ₀ analogues (C1′, C2′) for the block-table fit f₀(T) := Σ_groups f(T ∩ C). Then w.p. → 1:

- (i) π₀(𝒰ᶜ) ≤ e^{−c₃n};
- (ii) ε_𝒰 ≤ m·e^{−c₃n};
- (iii) β₁ ≥ (1 − o_P(1))/m!, with m = p + B + 2;

for some c₃ > 0 depending only on the gaps. Hence, for every fixed c,

  **P(S₀ ∉ 𝒮) ≤ o(1) + N(T_e + L + 4)·m·e^{−c₃n} + exp{−N(L+4)/(2·m!)} → 0,**

for the **original method's final run alone**, with no pilot, no temperature condition and no survival hypothesis. With T38(0) and (P) on LH [W1-EXP Thm 5(d)]: P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 without LS0.

**Status of the gaps.**
- (C1′) and (C2′) hold on LH for **every** parameter value: they are PROVED in §3.7, because the group table sees μ only through β_i(1−ψ_i²)x_{a_i}.
- (C4), zero gain for extras at T ⊇ S₀, is automatic, since μ ∈ span(S₀).
- The γ₁ gaps (C1)–(C3) are **verified by exhaustive enumeration** for both simulated designs (`bg3_popcheck`; c = 2: min C1 = 0.218, C2 = 0.030, C3 = 0.086; c = 3: 0.238, 0.051, 0.093). A proof for general (ρ, ψ, g, c) is open (§3.7), so the proposition is stated with the gaps as checkable design conditions, like (M2)/(M3) of T38(b1).

**Status of the constant.** 1/m! is a deliberately crude order constant: one fixed label order with the Λ labels first. The simulated q₁ is 0.02–0.17, far above it. The bound is useful only because N(L+4) → ∞ multiplies it.

**What breaks for p → ∞ (CONJECTURE).** Two things.
- (C1)–(C3) must hold *uniformly* over the 2^{p−|S°|} supersets of S°, with sample fluctuations O_P(√(n·K log p)) against gaps of order n. This needs size control (K log p = o(n) on the visited states, or a T03/SE-type uniform deviation bound).
- 1/m! must be replaced by a polynomial order constant. A multi-round version would do it: at φ = 1, each round deletes zero-gain extras with probability → 1, so the extras disappear in O(1) rounds.

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

### 3.4 Theorem BG2

Let U_t := 1{z is not scored in rounds 1, …, t}, with U₀ = 1.

Condition on 𝓕_t⁻. The stage-t round of particle i uses its own uniform permutation and fresh uniforms (EX-S), independent across particles and of 𝓕_t⁻. Each particle with Y_t^i ∈ G_t scores z in this round with conditional probability ≥ β_t. By independence,

  E[U_t | 𝓕_t⁻] ≤ U_{t−1}(1 − β_t)^{m_t} ≤ U_{t−1}e^{−m_tβ_t}.

U_{t−1} is 𝓕_t⁻-measurable, because the scoring events of earlier rounds are determined before the stage-t resampling.

Set M_t := U_t·e^{Λ_t}. Since Λ_t is 𝓕_t⁻-measurable (m_t and β_t are), E[M_t | 𝓕_t⁻] ≤ U_{t−1}e^{Λ_{t−1}} = M_{t−1}. Also 𝓕_{t−1}⁻ ⊆ 𝓕_t⁻. Hence E[M_t | 𝓕_{t−1}⁻] ≤ M_{t−1}, and E M_{t₁} ≤ M₀ = 1.

Then P(U_{t₁} = 1, Λ_{t₁} ≥ Λ) ≤ E[U_{t₁}e^{Λ_{t₁}}]e^{−Λ} ≤ e^{−Λ}. Add P(Λ_{t₁} < Λ). ∎

The proof never asks the scoring particle, or its descendants, to survive. That is SR: the evaluation is the event.

### 3.5 Corollary BG1′

In the proof of BG1 (§3.2), the only use of (B) is P(a 𝔅 particle scores z in the round at φ₁ | draws, resampled population) ≥ β. Under (B′) this probability is ≥ β(φ₁) ≥ β_*, because φ₁ ∈ [φ_lo, 1] by Fact F. The rest is unchanged.

**Final run.** Use the N iid π₀ draws of the final island, which are independent of 𝓒 (EX-A), and its first grid point φ₁ᶠ ∈ (0, 1], which is 𝓒-measurable.
- The uniform-in-φ normalisation e^{φΔ} ≤ 1 + e^{Δ} holds for every φ ∈ [0,1].
- Multinomial resampling (`v3_engine.h:229–258`) makes the resampled particles iid from the weighted empirical law, given the draws.
- So the same three events E₁, E₂, E₃ and the same Binomial step give the bound with H → N and φ_lo = 0.

The final run's scored models are in 𝒮 (SR). With K = K_n → ∞ and K_n = o(Nβ_*), the bound → 0 whenever Nβ_* → ∞. ∎

### 3.6 Proposition LH-rate (sketch)

**(a)** Apply Lemma R with x = S°, Λ = M, and the order event O := {in σ restricted to 𝔇, the c hub labels occupy the first c places}. P(O) = c!(|𝔇|−c)!/|𝔇|! = P_c. On O:
- every dangerous label other than a hub executes after the last hub label, so it is irrelevant (§3.1, final remark);
- the non-dangerous labels that can execute before the last hub label are Gibbs labels of null groups, of visible groups and of C_{a_i}∖{a_i} (null-like by (P1a, c, d)), and the Gibbs labels of S° members.

Their change probabilities, uniformly in φ ∈ [0, 1] (Lemma A: ε_l ≤ max{κ₀, κ₁}), are as follows.
- *Null-like additions:* ϖ-ratio × pure-noise Bayes factor at both endpoints, O_P((s₀/p)(n+1)^{−1/2}) each, so O_P(n^{−1/2}) summed over ≤ p labels. This uses the exponential-moment bound of LH (iii) for the γ₁ endpoint and the table structure for the γ₀ endpoint: the table r_b uses the full response, and the group is orthogonal to μ or has zero partial covariance given the present hub.
- *Deletion of S° members:* e^{−Θ(n)} at both endpoints. At γ₀, the table r_{b(a_i)} loses the a_i signal; at γ₁, the a_i are visible with coefficient β_i(1−ψ_i²) ≠ 0.

So Dep_φ = O_P(n^{−1/2}) uniformly. The forward steps are the c − 1 accepted hub additions before the last one, each at a chain state S° ∪ A, A ⊊ M, with no other masked content. By log-linearity, log κ_φ = (1−φ)log κ₀ + φ log κ₁. Here log κ₀ = log ϖ-ratio + log r_{b_i}({b_i}) = −λ_n + O_P(1), a pure-noise one-variable Bayes factor since C_{b_i} ⟂ μ, and log κ₁ ≥ c₂n − O_P(log n) by (P1e). Lemma R gives (a). The bound ᾱ ≥ ½min(1, κ) is t/(1+t) ≥ ½min(1, t).

**(b)** From S°, S₀ is evaluated in a round only:
- at a Gibbs step at a state y with y Δ S₀ = {l} (|y| = s₀ ± 1), or
- at a swap from a state of size s₀, or
- by the independence proposal.

The independence proposal draws a state with masked content with probability π₀(masked) = o_P(1) (LH (ii)). Every state y at distance ≤ 1 from S₀ contains at least c − 1 masked-group members. Each masked member enters through an accepted Gibbs addition or an accepted swap of a masked-group label at a state with ≤ c − 1 masked members. At such a state the acceptance odds are ≤ max_{y′,i}κ_φ(y′, b_i)·e^{O_P(1)}: proxies k ∈ C_{b_i}∖{b_i} have Δ-gain ≤ the hub's (W1-EXP Lemma 4.1(c)), up to the (P1e) factor. Within one round there are ≤ m labels. Summing over the C_c := m^{c−1} possible label sequences gives (b). This is a sketch: the swap Hastings factors and the proxy factor are not written out.

**(c)** (R1) is (a) with c = 1: the exponent is 0. For (R2), (a) at φ = 0 gives h₁ ≥ n°P₂ᾱ₀(1−o_P(1)), with n° ≥ Hπ₀(S°)/2 w.p. → 1 and ᾱ₀ = e^{−λ_n+O_P(1)}. For (R3), (a) with φ₁c₂n ≥ c₂n/T_e ≫ λ_n. For (R4), combine (a) with (b).

**(d)** This is not proved; the first-order computation is in the statement.

**Obstruction (heuristic part).** The candidate-grid rule ρ_V(0, b) ≥ 0.9 puts b at the inverse scale of the d-spread of V, which is ≥ c₂n − O(log n) once V contains S° and a state of S₀'s fit class. The precise size of φ₁ᶠ (numerically ≈ 20–30/n) is not derived here. Given φ₁ᶠ, (b) bounds the stage-1 hazard by N·C_c·ᾱ_{φ₁ᶠ}^{c−1}e^{O_P(1)}. Later stages are covered by BG2. The step "m_t ≍ N until φ_t ≥ φ_sc" is the open delivery input.

### 3.7 Theorem BG3 and Proposition LH-lock

**BG3.** Let E be the event "every particle is in 𝒰 at the start of every bridge round and of every terminal round".
- Resampling only copies particles, so it cannot take the population out of 𝒰.
- By a union bound over the N initial draws and the N(T + L + 4) particle-rounds, P(Eᶜ) ≤ Nπ₀(𝒰ᶜ) + N(T + L + 4)ε_𝒰. Each round of a particle in 𝒰 ends outside 𝒰 with conditional probability ≤ ε_𝒰, given the past, by EX-S.
- In the terminal rounds, apply Theorem BG2 with G_t = 𝒰 and β_t = β₁ for t = T+1, …, T+L+4. On E, m_t = N, so Λ_{T+L+4} ≥ N(L+4)β₁, and P(z unscored, E) ≤ e^{−N(L+4)β₁}. Formally, apply BG2 to the stopped counts m_t·1{E holds up to t}, which are predictable. ∎

**LH-lock (sketch).** p is fixed, so Ω is finite and every "w.p. → 1" below is a finite intersection. Sample fits are (n−1)f(T) + O_P(√n), uniformly over the finitely many T, because ‖X′ε‖ = O_P(√n) under exact Gram. With g = n, the Bayes factor gives log m(T) − log m(T′) = −((n−1)/2)·log(Q_T/Q_{T′}) + O(|T| log n). Here Q_T/(n−1) = f(S₀) − f(T) + σ*² + O_P(n^{−1/2}) is the scaled residual sum of squares. So a fit gap δ > 0 gives a log-score gap ≥ (n−1)δ/(2(f(S₀) + σ*²)) − O_P(√n) − O(log n) (σ*² > 0 is fixed).

- **(ii) Gibbs deletion of j ∈ S° at y ∈ 𝒰.** The probability is 1/(1 + κ_φ), with log κ_φ = (1−φ)log[γ₀(y)/γ₀(y∖j)] + φ log[γ₁(y)/γ₁(y∖j)]. By C1′ (the tables of the other groups cancel; ϖ-ratios are polynomial) and C1, both brackets are ≥ 2c₃n w.p. → 1, so the probability is ≤ e^{−2c₃n}.
- **(ii) Uniform or neighbour swap removing j ∈ S° for l.** The acceptance is min{1, h·ρ₀^{1−φ}ρ₁^φ}, with a Hastings factor h ≤ p, and ρ₀, ρ₁ ≤ e^{−2c₃n} by C2′ and C2.
- **(ii) Independence proposal.** It lands outside 𝒰 with probability π₀(𝒰ᶜ).

There are ≤ m labels per round, which gives (ii).

**(i)** Every y ∉ 𝒰 misses some j ∈ S°. γ₀ factorises over groups and j's group table gains ≥ 2c₃n when j is added, for every configuration of the rest of its group (C1′ ranges over all E = T ∩ C(j)). So γ₀(y) ≤ e^{−2c₃n}·poly(n)·γ₀(y ∪ {j}). Sum over the ≤ 2^p states.

**(iii)** Fix y ∈ 𝒰 and let Λ = (M∖y) ∪ (y∖S₀). Take the order O_y: first the missing-hub labels (any fixed order), then the labels of y∖S₀, then all other labels. P(O_y) = (m − |Λ|)!/m! ≥ 1/m!. On O_y no label outside Λ executes before the last Λ label.
- Each hub addition is accepted with probability → 1 at φ = 1, by C3 (gain ≥ (n−1)·min C3 − O_P(√n) − O(log n)).
- Each extra deletion happens at a state T ⊇ S₀. Its gain is exactly 0, because μ ∈ span(S₀) (checked as C4 = 0), so its keep-odds are ϖ-ratio·(n+1)^{−1/2}·e^{O_P(1)} → 0.
- The last Λ step is *evaluated*, which is SR, so S₀ is scored.

Hence β₁ ≥ (1 − o_P(1))/m!.

**Why the gaps hold on LH (sketch).** Pair blocks are mutually orthogonal (exact Gram), so all fits split over pair blocks and visible groups.
- *(C1)* Within pair block i, for any T ∌ a_i, let r := x_{a_i} − P_T x_{a_i}. Using x_{b_i} = ψ_i x_{a_i} + w_i, with w_i ⟂ C_{a_i}: ⟨r, μ_i⟩ = β_i[(1−ψ_i²)‖r‖² − ψ_i⟨r, w_i⟩]. When T contains no C_{b_i} member, ⟨r, w_i⟩ = 0, and the gap is β_i²(1−ψ_i²)²‖r‖² > 0. When T contains members of C_{b_i}, the gap is not identically positive in closed form for all (ρ, ψ). This is why (C1)–(C3) are stated as **deterministic checks**, verified by enumeration for the simulated designs and not claimed for every LH parameter value.
- *(C1′)* The group-C_{a_i} table uses only C_{a_i} columns: μ's projection on span(C_{a_i}) is β_i(1−ψ_i²)x_{a_i}, because x_{b_i} projects onto ψ_i x_{a_i}. So the gap is β_i²(1−ψ_i²)²(1 − R²(x_{a_i} | E)) > 0.
- *(C2′)* A swap j → l with l in another group C′ adds zero γ₀-fit. C′ either contains its hub (a-groups and visible groups: μ projects on span(C′) through the hub, which is present) or is a masked group, with μ ⟂ C_{b_i}. So C2′ = C1′; a within-group swap a_i → k loses β_i²(1−ψ_i²)²(1 − R²(x_{a_i} | E∖a_i ∪ k)) > 0.

(C1′) and (C2′) are PROVED for every LH parameter value, and the enumeration agrees: min C2′ = min C1′.
- *(C3)* Generic positivity, by the Prop M(a) mechanism: λ_min(R) ≥ (1−ψ₊)(1−ρ₊).

## 4. Evidence

`scripts/bg1_first_stage.py`, which uses the engine `scripts/bvs_core.py`. The engine is copied verbatim from theory/W4-SHARE: a faithful small-p re-implementation, exact scores, SR, every proposal recorded. Seed 20261102. The script runs the setup below and prints its output to `scripts/bg1_first_stage.txt`.
- Design: LH exact Gram, p = 16, g = B = 4, ρ = 0.7, ψ = 0.5, β = 1, σ = 1, c = 2.
- For each replicate (40 per n, fresh noise): H iid π₀ draws, the engine's pilot rule φ₁, multinomial resampling, ONE round at φ₁. S₀ counts as scored if it appears among the evaluated or proposed states of that round.

**Machine and seeds.** Laptop, ≤ 4 processes, numpy 1.26, Python 3.12. Seeds: bg1 20261102; bg2 1000c + n; bg3 7000 + 100c + n. Designs:
- LH exact Gram, ρ = 0.7, ψ = 0.5, β = 1, σ = 1;
- c = 2: p = 16, g = 4, S₀ = {0, 4, 8, 12}, S° = {0, 8};
- c = 3: p = 18, g = 3, S° = {0, 6, 12};
- B = min(⌊√n⌋, ⌊√p⌋, 16) = 4 in both, so g ≤ B < 2g.

Calibration is the idealised one of bvs_core (exact-law pilot, V over Ω). The pilot's stage 1 uses the particle rule of `v3_calib.h:30–46` on H iid π₀ draws.

### 4.1 Pilot stage 1 (`bg1_first_stage.py` → `bg1_first_stage.txt`; c = 2, 40 replicates per n)

| n | H | S₀ scored in the ONE stage-1 round | S₀ among the initial draws | median π(S₀) | min π₀(S°) | median φ₁ | max φ_hub | min basin fraction after resampling |
|---|---|---|---|---|---|---|---|---|
| 400 | 512 | 40/40 | 2 | 0.793 | 0.861 | 0.0426 | ∞ (one replicate) | 0.881 |
| 1600 | 512 | 40/40 | 0 | 0.893 | 0.928 | 0.0131 | 0.108 | 0.947 |
| 6400 | 1311 | 40/40 | 0 | 0.948 | 0.962 | 0.0040 | 0.0243 | 0.969 |
| 25600 | 5243 | 40/40 | 0 | 0.978 | 0.980 | 0.0011 | 0.0065 | 0.989 |

φ₁ is far below φ_hub, the temperature at which hub additions are favoured, yet S₀ is always scored. This is the point of Lemma R + SR: c − 1 accepted additions and one evaluation suffice. The crude endpoint bound W_out/n° is astronomically large (10³⁰–10³⁰⁰). The uniform-in-φ selection bound ρ_𝒩 is therefore an asymptotic device: the realised basin fraction after resampling is ≥ 0.88.

### 4.2 Scoring rate and first-score stage (`bg2_score_rate.py` → `bg2_score_rate.txt`)

Here q(φ) is the per-particle probability that one round from S° at φ scores S₀ (Monte Carlo, 20000 copies). "Hazard" is H·q(φ₁) for the pilot and N·q(φ₁ᶠ) for the final run's stage 1.

| c | n | reps | q(0) (median) | pilot hazard H·q(φ₁) | final stage-1 φ₁ᶠ (median) | final hazard N·q(φ₁ᶠ) | first-score stage in the final island | min start-basin count before the first score |
|---|---|---|---|---|---|---|---|---|
| 2 | 400 | 10 | 7.9e-3 | 8.8–17.4 | 0.045 | 48–69 | stage 1: 8; initial draw: 2 | ≥ 0.94N |
| 2 | 1600 | 10 | 4.0e-3 | 6.8–12.4 | 0.013 | 32–43 | stage 1: 9; initial draw: 1 | ≥ 0.97N |
| 2 | 6400 | 6 | 1.7e-3 | 12.8–22.5 | 0.0041 | 52–66 | stage 1: 5; initial draw: 1 | ≥ 0.98N |
| 2 | 25600 | 10 | 1.0e-3 | 30–57 | 0.00115 | 156–268 | stage 1: 9; initial draw: 1 | ≥ 0.99N |
| 3 | 400 | 10 | 7.5e-5 | 0.2–0.6 | 0.044 | 0.6–2.1 | stage 1: 8; stage 2: 2 | ≥ 0.94N |
| 3 | 1600 | 10 | < 5e-5 | 0.1–0.5 | 0.013 | 0.2–1.4 | stage 1: 10 | ≥ 0.97N |
| 3 | 6400 | 8 | < 5e-5 | 0.0–0.5 | 0.0040 | 0.0–1.3 | stage 1: 6; stage 2: 2 | ≥ 0.98N |

This matches Proposition LH-rate.
- For c = 2, q(0) ∝ (p√n)^{−1}: it halves as n quadruples. The hazard ≫ 1 at stage 1 even at φ = 0 scale, and n·φ₁ᶠ ≈ 18–29.
- For c = 3, q(0) ∝ (p√n)^{−2} is unmeasurable. The stage-1 hazard is Θ(1), discovery spills into stage 2, and the cumulative hazard grows with φ.
- The S°-only q understates the c = 3 hazard. The initial draws at one-hub states S° ∪ {b_i} (π₀ ≍ (p√n)^{−1} each, about 10 particles at N = 2500) need one accepted addition fewer, and they explain why stage 1 scores even when N·q(φ₁ᶠ) < 1.
- No extinction was ever seen before the first score.

### 4.3 Locked start set and terminal discovery (`bg3_locked.py` → `bg3_locked.txt`; `bg3_popcheck.py` → `bg3_popcheck.txt`)

| c | n | islands | π₀(𝒰ᶜ) | min over all stages and terminal rounds of N_𝒰/N | q₁ from S° | min q₁ over 28 states of 𝒰 (end population + proxy/extra states) | log₁₀ of (1 − min q₁)^{N(L+4)} |
|---|---|---|---|---|---|---|---|
| 2 | 400 | 5 | 8·10⁻¹²–5·10⁻⁹ | **1.0000** | 0.14–0.17 | 0.12–0.15 | −1812 to −2265 |
| 2 | 1600 | 5 | 10⁻⁴⁴–10⁻³¹ | **1.0000** | 0.13–0.15 | 0.12–0.13 | −2147 to −2301 |
| 3 | 400 | 5 | 5·10⁻⁸–5·10⁻⁷ | **1.0000** | 0.07–0.08 | 0.058–0.074 | −836 to −1085 |
| 3 | 1600 | 4 | 6·10⁻³⁵–2·10⁻²⁷ | **1.0000** | 0.05–0.07 | 0.019–0.065 | −321 to −1060 |

Population gaps over every T ⊇ S° (exhaustive enumeration):

| design | min C1 (γ₁ lock, deletion) | min C2 (γ₁ lock, swap) | min C1′ = C2′ (γ₀ lock) | min C3 (downhill hub addition) | max C4 (extras' gain) |
|---|---|---|---|---|---|
| c = 2 | 0.218 | 0.030 | 0.218 | 0.086 | 2·10⁻¹⁶ |
| c = 3 | 0.238 | 0.051 | 0.238 | 0.093 | 4·10⁻¹⁶ |

All of the gaps that must be positive are positive, and C4 = 0 to machine precision, as LH-lock requires.

## 5. What fails and why (and the precise obstruction)

- **The obstruction for discovery *during* the bridge is the scoring temperature, not survival, and it is milder than the first draft said.** The first draft required stage 1 to be above φ_hub, the temperature at which every hub addition is *favoured*. That is not needed. By Lemma R, only c − 1 additions must be *accepted*, and the c-th only *evaluated* (SR). By BG2, a scoring probability per particle of order 1/H is enough. The correct threshold is φ_sc (Proposition LH-rate (R4)), and **φ_sc = 0 for c = 1, and for c = 2 when p = o(√n)**. Numerically, the median φ₁ is well below the largest φ_hub (0.013 vs 0.108 at n = 1600; 0.004 vs 0.024 at n = 6400; bg1), and S₀ was still scored in round 1 in 160/160 replicates, with hazards H·q(φ₁) ≈ 7–57 (bg2).
- **For c ≥ 3, bridge-stage discovery is hazard-limited, but the final run does not need it (Theorem BG3).** The final run's stage-1 hazard is Θ(1) for c = 3 (bg2: N·q(φ₁ᶠ) ≈ 0.0–2.1 from S° alone, n = 400–6400), and later stages raise it. Any proof that relies on bridge-stage scoring then needs the start-mode count to survive until φ ≥ φ_sc. That is W4-SHARE's D4/D5 delivery input, which is not proved here. **BG3 bypasses this.** On LH the start set 𝒰 = {y ⊇ S°} is *locked*: leaving it costs e^{−Θ(n)} at both endpoints and at every φ, so no particle ever leaves it (bg3: min_t N_𝒰/N = 1 in every island). The L + 4 terminal rounds at φ = 1 have no resampling and are downhill to S₀. Extinction of 𝒰 takes ≳ e^{c₃n}/N rounds; scoring takes O(1/(Nβ₁)) rounds.
- **Where BG3 fails: precise obstructions and counterexample families.**
  - **(L2) fails on posterior-barrier designs.** W4-SHARE's design PB (λ_min(R_{S₀}) = 0.004) keeps its start mode {12} ⊂ S₀ occupied (delivery to 𝓡₀ in 200/200 islands), but every path from it to S₀ goes down by 6–15 nats at **both** endpoints. So β₁ ≈ 5·10⁻⁶ per particle-round, and the Prop X bound 0.48 per island matches the observed 0.51. This is a COUNTEREXAMPLE at finite n (W4-SHARE `s3_bvs_barrier`, `s3b_gate_rate`) to discovery by any local kernel, and no method change (LS0, T39) fixes it.
  - **(L1) fails** when a member of the start mode is not supported by its own block table: γ₀ does not lock it, while γ₁ does. Then 𝒰 leaks at small φ, and BG3 must be replaced by a delivery argument. No LH instance has this, by (C1′).
  - **p → ∞ (LH-iid, W3-PXN; or exact Gram with p ≍ n).** The uniformity of (C1)–(C3) over 2^{p−s₀} supersets and the order constant 1/m! are the open points (CONJECTURE).
- **The final run.** BG3 makes the final run alone sufficient on LH (p fixed, every c). Corollary BG1′ also covers its stage 1 at any φ₁ᶠ, since the uniform-in-φ selection bound needs no floor. That route gives stage-1 discovery for c = 1, and for c = 2 when p is fixed. The first draft's statement that "the final run's stage 1 is typically below φ_hub, so discovery is a multi-stage delivery problem" was right about φ_hub. It is superseded on LH, because delivery to the terminal rounds is automatic when the start set is locked.
- **The ESS share route (D2-style).** It does not iterate (W4-SHARE §5), and it needs NB, which fails whenever a masked proxy is drawn: d-spread Θ(n) ≫ T_e. BG1 sidesteps both. A drawn masked proxy is a *basin* state, so letting it take over the resampling is harmless.
- **Uniform swap with a useless proxy present.** This is a real Θ(1/|y|) disruption. It is handled only by protecting the swap labels in O_k, which costs a combinatorial constant (§3.3(iv)).

## 6. Needs escalation

1. **Proposition LH-lock: the score-level reduction to the population gaps (C1)–(C4).** These are the Bayes-factor monotonicity bound, the O_P(√n) uniformity over the finitely many states (p fixed), and the order constant.
   - Short and routine, but unreviewed. This is now the **critical path** for the no-LS0 masked theorem.
   - A general-parameter proof of (C1)–(C3) on LH would turn the enumeration check into a theorem for every (ρ, ψ, g, c), not just the two simulated designs. (C1′) is proved in closed form in §3.7. The γ₁ gaps (C1)–(C3) are not, when C_{b_i} members are present.
2. **Theorem BG3 and BG2: independent check.** The points to check:
   - the stopped-count application of BG2 in the terminal rounds;
   - that the code's terminal rounds really have no resampling. `run_island_s` (`v3_engine.h:352–373`) calls `population_round` only, and those rounds' evaluations are score events (SR_AUDIT item 4).
3. **Proposition LH (ii)–(iv) and LH-rate.** These are needed only for the bridge-stage discovery theorems (BG1/BG1′), which BG3 no longer requires on LH. They remain useful as the "discovery usually happens at stage 1" statement. Open points:
   - the reduction of (iii) to T03 with a common RSS shift;
   - null leakage next to S₀;
   - the proxy window of LH-rate (d).
4. **Code facts.** These are Fact F (the `pilot_next_phi` floor, read here: `v3_calib.h:38–44`) and the multinomial resampling (`v3_engine.h:229–258`, read here). Both are confirmed by reading; an independent check is still useful.

## 7. Outside scope

- **BG3 is a general template, not an LH-specific trick.** For any design whose start mode S° ⊆ S₀ is locked at both endpoints (each member supported by its own block table and by the likelihood), and from whose superset cone the φ = 1 kernel is downhill to S₀, the final run discovers S₀. This is the "R/SE + truth-subset start mode" regime of W4-SHARE Proposition M. W4-SHARE's E1a–E1e designs are candidates. E1d, whose start sits on supersets with start-favoured extras, needs 𝒰 := {y ⊇ start mode} with the extras deletable at φ = 1, which is the case there (W4-SHARE: deletable at φ ≈ 0.4–0.5). Checking (C1)–(C4) for those designs is a small script. That would extend the no-LS0 theorem beyond LH, and is recommended to HQ as the next task.
- **LH-iid (p ≫ n, W3-PXN).** The lock (C1′) survives with approximate orthogonality. The uniform γ₁ gaps over supersets need a T03-type uniform deviation bound. Status: CONJECTURE.
- **Finite-n reading.** The BG3 bound is numerically meaningful at n = 400 (π₀(𝒰ᶜ) ≈ 10⁻⁸, exits e^{−Θ(n)}, terminal miss ≤ 10⁻⁸⁰⁰). The paper can therefore cite it as a finite-n explanation of why the masked LH runs never miss S₀, not only as an asymptotic statement.

## 8. Confidence card

| target | refined statement | P(true) | P(provable at reasonable cost) | crux | method change? |
|---|---|---|---|---|---|
| **Theorem BG3** (locked set + terminal downhill) | §2 | 0.97 | done (candidate) | no resampling in the terminal rounds; stopped-count BG2 | no |
| **Prop. LH-lock, p fixed, every c** | §2 | 0.9 | 0.8 | score-level reduction to the gaps C1–C4; general-(ρ, ψ) proof of the γ₁ gaps | no |
| **T38(b) without LS0 on LH exact Gram, p fixed, every fixed c (final run alone)** | BG3 + LH-lock + T38(0) | 0.9 | 0.8 | as above | **no** |
| Same, for p → ∞ (exact Gram p ≍ n, or LH-iid) | CONJECTURE | 0.75 | 0.45 | uniform gaps over supersets; polynomial order constant | no |
| Theorem BG2 (hazard) | §2 | 0.98 | done (candidate) | predictability of m_tβ_t | no |
| Lemma R | §2 | 0.97 | done (candidate) | on-track chain rule with an order-only O | no |
| Theorem BG1 / Corollary BG1′ (pilot and final stage 1) | §2 | 0.95 | done (candidate) | uniform-in-φ selection bound; iid multinomial resampling | no |
| Prop. LH (ii)–(iv), LH-rate (a), (b) | §2 | 0.85 | 0.7 | T03 reduction with an RSS shift; uniform Dep with the dangerous labels protected | no |
| LH-rate (R1) c = 1 / (R2) c = 2: stage-1 discovery at any φ | §2 | 0.85 (p fixed) / 0.7 (p → ∞) | 0.65 / 0.5 | proxy window (d) | no |
| Bridge-stage discovery for c ≥ 3 without BG3 (survival to φ_sc) | OPEN | 0.75 | 0.35 | (TRACK)/(OSC) on W ⊇ {S°} | no; unnecessary on LH |
| Posterior-barrier designs (PB) | COUNTEREXAMPLE at finite n (W4-SHARE) | 0.95 | — | (L2) fails at both endpoints | no change helps |
