# W3-START — STATEMENT (start-mass rate; PROGRAM item 2)

Ticket W3-START, Theory Wave 3. Lead: Claude Fable 5.2 (effort high).
Status of this file: **v1.3.4** (2026-11-11; record in `LOG.md`).
Protocol: `Theory_work/Wave3/PROTOCOL.md`. All results are asymptotic (n → ∞) unless marked *deterministic*. This file
states the claims; proofs are supplied in `lemmas/` (L1–L11), author-proved and awaiting independent acceptance. The
status of each claim is recorded outside this file: the author status in `REPORT.md`, the check record and the final
status in the ticket's final checkpoint file and in the registry. **No method change is requested.**

Abbreviations. CORE = `Scripts/SMC_BVS/core/`; GROW = `Theory_work/Wave1C/C-GROW/`; RM = `Theory_work/Wave3/W3-RM/`;
SAMP = `Theory_work/Wave3/W3-SAMP/`; MIS = `Theory_work/Wave1C/C-MIS/`; PXN = `Theory_work/Wave1/W1-PXN/`;
GEN = `Theory_work/Wave1/W1-GEN/`; T22 = `Docs/Theory/proofs/T22iii_T16_start_aggregation/STATEMENT.md` (registry SOP:TH116).

## 0. What is claimed, in one paragraph

Let π₀ be the start distribution exactly as `main` computes it and o₀ := (1 − π₀(S₀))/π₀(S₀) the start odds against
the true model. (i) *Deterministic (table identities):* o₀ is bracketed from both sides by explicit functionals of the
block tables — the sum T₁ of the single-null block Bayes factors and a truth-block functional Ξ — and every
unsaturated model S has 1 − π₀(S) ≥ c·n^{−1/2} on every data set, so when there is at least one null the exponent ½
cannot be beaten. (ii) *Fixed design:* under an energy bound, a constant floor on the unnormalised Gram matrix of
every small set, visibility of the truths,
and an **averaged leakage condition** on (X, θ*): o₀ = O_P(n^{−1/2}𝔏⁰_n + n^{−1}𝔏_n(S₀)²) + o_P(n^{−κ}) for every
κ < κ_V, where 𝔏⁰_n, 𝔏_n are deterministic leakage functionals (of order 1 to √log n when nothing leaks) and κ_V is
the visibility exponent; more generally the start mass outside the lattice {S₀ ⊆ S ⊆ Q} of a leakage set Q is
O_P((|Q| + 1)n^{−1/2}𝔏_n(Q)) + o_P(n^{−κ}). The truncation level inside the leakage functionals may be chosen column by
column within a summable tail budget (§2); this makes the condition sharp for isolated leaking columns (F4).
(iii) *Random designs:* the fixed-design bounds are uniform, so they transfer to random designs whose coefficients,
support and leakage set are functions of the design. *Gaussian rows, p ≫ n allowed:* under population visibility and
population no-leakage (W3-RM's (V-R), (L-R) with Q = S₀), π₀(S₀) ≥ 1 − n^{−1/2}e^{C√log n} with probability → 1 for some constant C, hence
π₀(S₀) ≥ 1 − n^{−c} for every c < ½. (iv) *Limits:* on the actual partition (component diagnostics (C2)), one null with
normalised gain above (1 + 2Ā) log n given the truths of its block, or one truth with normalised gain below
(1 + 2A̲) log n given the other truths of its block, sends π₀(S₀) → 0; the partition-free forms are (N2), which is
non-vacuous only for s₀ ≥ 16, and (N3)
(Ā, A̲ := limsup, liminf of log p/log n); masked truths and strong-factor designs are outside the hypotheses. (v) *Interfaces:* W3-SAMP's P-START with an explicit rate; a deterministic inequality for P-OVL and a primitive
corollary (Proposition OVL); the misspecified-candidate form (C-MIS). No design family appears anywhere. The theorems'
hypotheses are partition-free conditions on (X, θ*) or (Σ_n, θ*); blocks appear only where they must — in the
definition of the coded π₀ and in the component lemmas about its tables (§5.1), which are labelled as such.

## 1. Objects, code pins, settings

**Data as scored**. Raw inputs (X^r, y^r) with n ≥ 4 rows; valid inputs: finite entries, a non-constant
response and at least one retained non-constant predictor (p ≥ 1); constant raw columns are dropped and p denotes the number of **retained** (non-constant) columns
(CORE `v3_preprocess.R:111-127`). C := I − 11ᵀ/n; D_x := the diagonal matrix of the retained raw columns' sample
standard deviations; X := CX^rD_x⁻¹ (centred, ‖x_j‖² = n − 1); Y := Cy^r; s_y² := ‖Y‖²/(n − 1); the scored response is
y := Y/s_y (yᵀy = n − 1). G_S := X_SᵀX_S, z_S := X_Sᵀy.
**The start, as coded** (EX-A: exact arithmetic). Pins: the CORE tree as of commit 72785fe, the last commit touching CORE (the tree is unchanged since, in particular at the branch
base d6da494):
* score and prior: CORE `cpp/v3_score.h:39-72` (K = min(p, ⌊n/2⌋); w(k) = ½/C(2p − 1, k);
  W_K := Σ_{k=0}^{K} C(p, k)·w(k); ϖ(k) = w(k)/W_K),
  `cpp/v3_score.h:204-224` (log m(S) = log c_n − ½[log det H_S − log det(G_S + I)] − ν log(2b₀ + Q_S),
  c_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)), H_S = (n + 1)G_S + I,
  Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν = a₀ + n/2, scorer constants a₀ = b₀ = 0.01);
* partition: CORE `cpp/v3_blocks.h:124-144` (complete linkage on 1 − |r̂|, top-down cut, next-fit packing) with
  B = min(⌊√n⌋, ⌊√p⌋, 16), CORE `v3_preprocess.R:22`;
* tables: CORE `cpp/v3_start.h:76-98` (r_b(U) = m(U)/m(∅) for every U ⊆ C_b, scored against the full y);
* start: CORE `cpp/v3_start.h:68-70` (log γ₀(S) = log ϖ(|S|) + Σ_b log r_b(S ∩ C_b); log π₀ = log γ₀ − log Z̄₀),
  `cpp/v3_start.h:101-137` (Z̄₀ = Σ_{k≤K} ϖ(k)F_J(k), size-profile convolution truncated at K).
So on Ω = {S ⊆ [p] : |S| ≤ K}: **π₀(S) = γ₀(S)/Σ_{V∈Ω}γ₀(V), γ₀(S) := w(|S|)∏_b r_b(S ∩ C_b)**. From here on γ₀ denotes this
weight: it is W_K times the coded γ₀ of the previous line (which uses ϖ), and the constant W_K cancels in π₀ and in
every ratio used below. Since n ≥ 4,
B ≤ K and every block table is fully scored. "π₀" denotes this deterministic function of the data on every branch (a
component statement when the run dispatches to exact enumeration; PXN `STATEMENT.md:103-106`). Only two facts about
the partition are used: it is a function of X alone, and |C_b| ≤ 16.

**Setting F (fixed design)** = GROW `STATEMENT.md:51-64` (D0, model G), with s₀ ≥ 0 and any fixed A > 0 allowed (GROW has
s₀ ≥ 1 and A ≥ 1; neither restriction is used here): fixed raw design with
non-constant columns, y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), σ² > 0 fixed; hence Y = μ + Cε with μ := CX^rβ = Xθ*,
θ* := D_xβ; S₀ := supp β, s₀ := |S₀| fixed; p = p_n ≤ n^A, A > 0 fixed. Probability is over ε.
**Setting R (Gaussian rows)** = RM `STATEMENT.md:41-44`: raw rows iid N(m_n, Σ_n), Σ_n unit-diagonal, X as above,
Y = Xθ* + Cε with a deterministic θ*, ε ~ N(0, σ²I_n) independent of the raw design, s₀ ≥ 1 fixed,
|θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀ = supp θ*, p ≤ n^A; the scored response is y = Y/s_y. Probability is joint in
(X, ε). W denotes a population row.
In both settings μ, ε, RSS_U := ‖(C − P_U)Y‖² and every quantity of §2 refer to the **unscaled** Y; the tables are
computed from the scored y.

**Notation.** P_U projector on span X_U (P_∅ = 0); R̂_T := X_TᵀX_T/(n − 1); Λ_U := ‖(I − P_U)μ‖²; Δ_U := Λ_U/(n − 1);
**τ²_U := σ² + Δ_U** (noise plus the mean energy that U leaves unexplained). For l ∉ U with (I − P_U)x_l ≠ 0:
u_{U,l} := (I − P_U)x_l/‖(I − P_U)x_l‖, **δ_{U,l} := u_{U,l}ᵀμ** (so δ²_{U,l} = Λ_U − Λ_{U∪{l}}: the gain in explained mean
when l joins U), Z_{U,l} := u_{U,l}ᵀε/σ; if (I − P_U)x_l = 0 put δ_{U,l} := 0. b(l) := the block of l; U*_b := S₀ ∩ C_b;
𝔹* := {b : U*_b ≠ ∅} (the truth blocks; at most s₀). For a deterministic Q with S₀ ⊆ Q, |Q| ≤ K: the lattice
𝓛(Q) := {T : S₀ ⊆ T ⊆ Q} ⊆ Ω, and c_Q := |Q| + 15s₀. o₀ := (1 − π₀(S₀))/π₀(S₀). Logarithms are natural.
θ*_min := min_{S₀}|θ*_j| (when s₀ ≥ 1). x₊ := max(x, 0).

## 2. Quantities

**Table functionals** (functions of the block tables; defined for any data and any reference model S₀ ∈ Ω).
* m_l := max{r_b(T ∪ {l})/r_b(T) : U*_b ⊆ T ⊆ C_b ∖ {l}}, b = b(l), for l ∉ S₀ (largest one-step table ratio of l).
* U_Q := p⁻¹Σ_{l∉Q} m_l; U := U_{S₀}.
* T₁ := Σ_{l∉S₀} γ₀(S₀ ∪ {l})/γ₀(S₀) = [(s₀ + 1)/(2p − 1 − s₀)]·Σ_{l∉S₀} r_{b(l)}(U*_{b(l)} ∪ {l})/r_{b(l)}(U*_{b(l)}) if s₀ < K,
  and T₁ := 0 if s₀ = K: the prior-weighted sum of the single-null block Bayes factors.
* **Truth-block functional**. For b ∈ 𝔹* and U ⊆ C_b with U*_b ⊄ U put d := |U*_b ∖ U| ≥ 1 (truths of the block
  missing from U), a := |U ∖ (Q ∪ S₀)| (nulls outside Q in U), T_b(U) := (U ∩ Q) ∪ U*_b, and the prior weight
  ω^Q(U) := (2p)^{(d−a)₊}·(c_Q/p)^{(a−d)₊}. Then
  **Ξ_b(Q) := max over T′ with U*_b ⊆ T′ ⊆ C_b ∩ Q of Σ{ω^Q(U)·r_b(U)/r_b(T′) : U ⊆ C_b, U*_b ⊄ U, T_b(U) = T′}**,
  Ξ(Q) := max_{b∈𝔹*} Ξ_b(Q) (:= 0 if s₀ = 0). For Q = S₀: Ξ_b := Ξ_b(S₀) = Σ{ω(U)·r_b(U)/r_b(U*_b) : U ⊆ C_b, U*_b ⊄ U},
  ω(U) = (2p)^{(d−a)₊}(16s₀/p)^{(a−d)₊}: the prior-weighted table mass of every configuration of the truth's block that
  misses a truth, relative to the true configuration. Ξ := Ξ(S₀).
* e_n := 2p·max{[r_b(U)/r_b(U ∪ U*_b)]^{1/a′} : b ∈ 𝔹*, U ⊆ C_b, a′ := |U*_b ∖ U| ≥ 1} (e_n := 0 if s₀ = 0) — the cruder
  truth-deletion functional of v1.0 and of T22; used for (V-c) and for Proposition OVL.
* f_n(k) := (k + 1)(p − k)/((2p − 1 − k)√(n + 1)); c_s := (64·max(s₀, 1))^{−16}.

**Leakage functionals** (deterministic functions of (X, θ*, σ)). z_n := √(2 log(2²¹p) + 2 log log n).
*Truncation levels.* For a set Q ⊇ S₀, a **level vector** is h = (h_l)_{l∉Q} with **1 ≤ h_l ≤ z_n**; it may depend on
(X, θ*, σ, Q) but never on the response. Its **tail budget** is **b_n(h) := 2¹⁶·Σ_{l∉Q} exp(−h_l²/2)**. The **default**
is h ≡ z_n, for which b_n(h) ≤ 1/(32 log n). Wherever no level vector is displayed, the default is meant.
For d ∈ ℝ, t ≥ σ, h ≥ 1: **J_h(d, t) := E[exp((d + σZ)²/(2t²))·1{|Z| ≤ h}]**, Z ~ N(0, 1) — the truncated expected Bayes
factor of a null direction with mean gain d² and residual variance t²; J_n := J_{z_n}. Elementary bounds (Lemma J):
(J0) J_h(d, t) ≥ ¼exp(d²/(2t²)); (J1) for t > σ: J_h(d, t) ≤ (t/√(t² − σ²))·exp(d²/(2(t² − σ²)));
(J2) J_h(d, t) ≤ √(2/π)·h·exp(d²/(2t²) + |d|σh/t²); (J3) J_h(0, σ) = √(2/π)·h.
* **𝔏_n(Q; h) := p⁻¹Σ_{l∉Q} max{J_{h_l}(δ_{U,l}, τ_U) : U ⊆ [p] ∖ {l}, |U| ≤ 15}** (partition-free);
  𝔏_n(Q) := 𝔏_n(Q; z_n).
* **𝔏⁰_n(h)** (leading functional, Q = S₀): if s₀ ≥ 1,
  𝔏⁰_n(h) := p⁻¹Σ_{l∉S₀} max{J_{h_l}(δ_{U,l}, τ_U) : U ⊊ S₀, |U| ≤ 15} + 15√(2/π)z_n/p; if s₀ = 0,
  𝔏⁰_n(h) := √(2/π)·p⁻¹Σ_l h_l. 𝔏⁰_n := 𝔏⁰_n(z_n).
  (Only subsets of the truth are conditioned on; the last term accounts for the ≤ 15 nulls that can share a block
  with all of S₀.)
* Block-relative versions on the actual partition (smaller; used only in §5.1):
  𝔏^b_n(Q; h) := p⁻¹Σ_{l∉Q} max{J_{h_l}(δ_{U,l}, τ_U) : U*_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}} ≤ 𝔏_n(Q; h);
  𝔏^{b,0}_n(h) := p⁻¹Σ_{l∉S₀} J_{h_l}(δ_{U*_{b(l)},l}, τ_{U*_{b(l)}}) ≤ 𝔏⁰_n(h).
* ϱ_n(Q; h) := (|Q| + 1)·n^{−1/2}·𝔏_n(Q; h); ϱ_n(Q) := ϱ_n(Q; z_n).
(A smaller level h_l lowers J_{h_l}: it removes the part of the Gaussian tail that a column with a large gain would
otherwise be charged for, and it is paid for in the tail budget. A level belongs to a column, not to a conditioning
set.)

**Exponents.** κ_L(η, a) := ½ − η/2 − √(2aη), which is > 0 iff η < η_a := (√(2a + 1) − √(2a))². The visibility exponent
κ_V is (c_V − 1 − 2A)/2 under (V-c) and c_m/2 under (V-m) (§3.1).

## 3. Assumptions (ids for the registry)

Fixed constants: A > 0, M < ∞, g_* > 0, s₀, and c_V or (c_m, ε₀) (Corollary F2 has its own floor constant
φ₀ ∈ (0, 1]); for Setting R also c_Σ > 0, a_V > 0, θ_lo, θ_hi,
C_L ≥ 0 and a polylogarithm exponent κ_Q ≥ 1 (these are distinct from the scorer's a₀ = b₀ = 0.01).

### 3.1 Fixed design — partition-free conditions on (X, θ*)
* **(E) [A:START-E]** ‖μ‖² ≤ Mn; p ≤ n^A; s₀ fixed; p > s₀ for all large n (at least one null).
* **(GF-16) [A:START-GF]** λ_min(X_TᵀX_T) ≥ g_* for every T ⊆ [p] with 1 ≤ |T| ≤ 16: a **constant floor on the
  unnormalised Gram matrix** of every small set. (The normalised floor λ_min(R̂_T) ≥ φ₀² — the (FL-16) clause of RM
  (FL) — implies (GF-16) with g_* = φ₀² for every n ≥ 2. (GF-16) also allows correlation-matrix eigenvalues of order
  1/n, for example two columns at Euclidean distance of order 1.)
* **Visibility [A:START-V]**, one of:
  **(V-c)** (constant level): for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15: δ²_{U,j} ≥ c_V·τ²_U·log n, with
  c_V > 1 + 2A. (RM's (V), δ²_{U,j} ≥ M_n log n with M_n → ∞, implies (V-c) for every c_V, since τ²_U ≤ σ² + Mn/(n − 1).)
  **(V-m)** (margin form): there are c_m > 0 and ε₀ > 0 such that for every V ⊆ S₀ with 1 ≤ |V| ≤ 16, every nonempty
  D ⊆ V, every R ⊆ Q ∖ S₀ and N ⊆ [p] ∖ Q with |V| + |R| + |N| ≤ 16, writing U := (V ∖ D) ∪ R ∪ N, T := V ∪ R,
  W := V ∪ R ∪ N:
  **(Λ_U − Λ_W)/τ²_U ≥ [(1 + 2A)(|D| − |N|)₊ + c_m]·log n + (1 + ε₀)·(Λ_T − Λ_W)/τ²_W.**
  (Left: what the missing truths D gain once added to U. Right: the prior-plus-dimension price of the net number of
  deleted variables, a margin, and what the substituting nulls N gain given the truths. With N = ∅ this is visibility
  of D at the level (1 + 2A)|D| + c_m; for a swap |N| = |D| only a margin over the nulls' leakage is asked. (V-c) asks
  the single-truth gain at level c_V given **every** 15-set, including sets of close correlates of the truth; (V-m)
  does not.) For Q = S₀, R = ∅.
* **(AL) [A:START-AL]** averaged leakage outside a deterministic Q ⊇ S₀ with |Q| ≤ K: there is a level vector h for Q
  with **b_n(h) → 0 and ϱ_n(Q; h) → 0**. With the default levels this reads **ϱ_n(Q) → 0**.
  ("No leakage" is Q = S₀. The condition bounds an average over the null columns of an exponential of the normalised
  gain δ²_{U,l}/τ²_U; it does not bound the largest gain. By (J0) it forces δ²_{U,l} ≤ (2A + 1 + o(1))τ²_U log n for
  every l ∉ Q and |U| ≤ 15 — the small-gain regime in which the table steps can be linearised. Uniform
  sufficient forms are in Corollary F1–F3; F4 uses non-default levels.)

### 3.2 Gaussian rows — conditions on (Σ_n, θ*) (from RM `STATEMENT.md:134-145`)
* **(FL-R16) [A:START-R-FL]** λ_min(Σ_{n,S}) ≥ c_Σ for every S with |S| ≤ 16 + s₀ — the small-set part of RM's (FL-R);
  RM's floor on Q ∪ {l} is not needed here (it is unused by the start component: RM `lemmas/L3_SANDR.md:42-44`).
* **(V-R) [A:START-R-V]** = PTV(a_V): |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a_V for every j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15.
* **(L-R) [A:START-R-L]** a deterministic Q ⊇ S₀ with |Q| ≤ (log n)^{κ_Q} and |Q| ≤ K, and for every l ∉ Q a
  deterministic H_l ⊇ {l} ∪ S₀ with |H_l| ≤ (log n)^{κ_Q} such that for every U ⊆ [p] ∖ {l} with |U| ≤ 15, U₀ := U ∩ H_l:
  (L-gain-R) |Cov(W_l, W_j | W_{U₀})| ≤ C_L n^{−1/2} for j ∈ S₀ ∖ U₀;
  (L-loc-R) |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n for v ∈ U ∖ H_l, j ∈ S₀ ∖ U₀, with a
  deterministic r_n, r_n(n log n)^{1/4} → 0. (RM's (L-feas) is not needed.) "No leakage" is Q = S₀.

### 3.3 Implementation premises (named, not proved)
EX-A (exact scores, convolutions and comparisons; all claims are about the exact mathematical π₀, not binary64);
[A:BLOCK-LE-16] the partition is a function of X alone with |C_b| ≤ 16 (true of the coded partition). No calibration,
sampler, random-number, LS0 or delivery premise is used by any claim about π₀.

## 4. Interface properties (PROTOCOL item 5)

Each is a property of the coded start on its actual partition. The component lemmas of §5.1 consume them; the bridge
lemmas of §5.2 deliver them from the partition-free assumptions; the theorems of §5.3 are the compositions.

| id | property | delivered by (bridge) | consumed by |
|---|---|---|---|
| [TK] | the toolkit event 𝓔^blk has probability → 1. 𝓔^blk: concentration events for the family of block subsets, on which, for every U inside a block, RSS_U = (n − 1)τ²_U(1 + ρ_U) with max\|ρ_U\| ≤ ω_n, where ω_n is deterministic and ω_n log n → 0, and log m(U) = c′_n − ½\|U\| log(n + 1) − ν log RSS_U + R_U with \|R_U\| ≤ κ_E, a constant depending only on (g_*, M, σ²) | B-TK: (E), (GF-16) ⇒ [TK] (Lemma TK, proved in this ticket) | ASM, NEC |
| [VIS(κ; Q)] | P(Ξ(Q) > n^{−κ}) → 0 | B-V1: (V-c), [TK], [LEAK(Q)], (AL) ⇒ every κ < (c_V − 1 − 2A)/2; B-V2: (V-m), [TK] ⇒ every κ < c_m/2 | ASM |
| [LEAK(Q)] | for a level vector h with b_n(h) → 0: if (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) → 0 then U_Q = O_P(n^{−1/2}𝔏^b_n(Q; h)); if Q = S₀ and n^{−1/2}𝔏^{b,0}_n(h) → 0 then T₁ = O_P(n^{−1/2}𝔏^{b,0}_n(h)) | B-L: [TK] and the small-gain consequence of the displayed premises | ASM |
| **P-START** | 1_𝒜·o₀ → 0 in probability (SAMP `STATEMENT.md:76`) | START-F / START-R at Q = S₀ | SAMP Theorem C |
| **P-OVL** | D_r·π₀(S₀) → ∞ in probability on 𝒜 (SAMP `STATEMENT.md:82`) | P-START; Proposition OVL | SAMP Theorem D |

**Quantitative form of [TK].** The bridges (B-L), (B-V1), (B-V2) and the diagnostics (C2) use [TK] in the
quantitative form that Lemma TK delivers under (E) and (GF-16): the event 𝓔^blk with an explicit failure probability,
the deterministic envelope ω_n ≤ ω̄_n = O(n^{−1/3}) depending only on (n, A), the constant κ_E(g_*, M, σ²), and the
log-ratio bounds that follow, uniformly over the designs and coefficient vectors satisfying (E) and (GF-16) with the
same constants. Lemma ASM (C1) needs only the interface properties [LEAK(Q)] and [VIS(κ; Q)] as displayed.

## 5. Claims

### 5.1 Component lemmas (about the coded start and its block tables; blocks appear by necessity)

**(C0) Lemma AGG (table identities; deterministic, any data).** Let n ≥ 4, valid inputs, EX-A, any partition with
blocks of size ≤ min(16, K), **any** reference model S₀ ∈ Ω (not necessarily the truth) and any Q ⊇ S₀ with |Q| ≤ K.
* (AGG-a, lattice) If U_Q < 1: 1 − π₀(𝓛(Q)) ≤ ∏_{b∈𝔹*}(1 + Ξ_b(Q))·(1 − U_Q)^{−(c_Q+1)} − 1.
* (AGG-b, two-sided at S₀) If s₀ < K and U < 1, with R₂ := (1 − U)^{−(s₀+1)} − 1 − (s₀ + 1)U:
  **T₁ ≤ o₀ ≤ T₁ + R₂ + [∏_{b∈𝔹*}(1 + Ξ_b) − 1]·(1 − U)^{−(16s₀+1)}**, and T₁ ≤ (s₀ + 1)U. If moreover s₀ + 16 ≤ K:
  **o₀ ≥ c_s·Ξ**. (So o₀ → 0 forces T₁ → 0 whenever s₀ < K and, under the feasibility condition s₀ + 16 ≤ K, also
  Ξ → 0; conversely T₁ → 0, Ξ → 0 and U → 0 imply o₀ → 0.)
* (AGG-c, for P-OVL) If U_Q < 1, with m_l defined as in §2 also for l ∈ Q ∖ S₀:
  1/π₀(S₀) ≤ (1 + e_n)^{s₀}(1 − U_Q)^{−(|Q|+1)}∏_{l∈Q∖S₀}(1 + |Q|m_l/p).
* (AGG-d, Ξ versus e_n) If c_QU_Q ≤ 1: Ξ_b(Q) ≤ 2¹⁶·max(e_n, e_n¹⁶) for every b ∈ 𝔹*.
* (FLOOR) For every S ∈ Ω with |S| < K and every l ∉ S: m(S ∪ {l})/m(S) ≥ (n + 1)^{−1/2}; hence for every model
  with **|S| < K**: 1 − π₀(S) ≥ f_n(|S|)/(1 + f_n(|S|)), and f_n(k) ≥ ½(n + 1)^{−1/2} whenever k < p. (Nothing is claimed
  for saturated models |S| = K: there the start mass can be exponentially close to 1.)
Predecessor: T22(i) (SOP:TH116), re-proved here in lattice form with the leading term isolated; Ξ, the lower bound
o₀ ≥ c_sΞ and (FLOOR) are new.

**(C1) Lemma ASM (assembly).** Setting F, a deterministic Q ⊇ S₀ with |Q| ≤ K, s₀ fixed, p > s₀ eventually, a level
vector h for Q with b_n(h) → 0. Suppose [TK], [LEAK(Q)] with (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) → 0, and [VIS(κ; Q)] for some
κ > 0. Then
(a) 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)n^{−1/2}𝔏^b_n(Q; h)) + O_P(n^{−κ}), with o_P(n^{−κ′}) for every κ′ < κ;
(b) if Q = S₀: o₀ = O_P(n^{−1/2}𝔏^{b,0}_n(h) + n^{−1}𝔏^b_n(S₀; h)²) + O_P(n^{−κ});
(c) if Q = S₀, κ > ½ and n^{−1/2}𝔏^b_n(S₀; h)² → 0: o₀/T₁ → 1 in probability.
(Composition of (C0) with the interface properties; no other input.)

**(C2) Lemma NEC-b (component diagnostics; Setting F, (E), [TK]).** With Ā := limsup log p/log n,
A̲ := liminf log p/log n, on the actual partition:
(i) if for all large n some null l = l_n has δ²_{U,l} ≥ c·τ²_U·log n at U = U*_{b(l)}, c > 1 + 2Ā fixed, then
P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1 − 2Ā)/2;
(ii) if for all large n some truth j = j_n has δ²_{U,j} ≤ c·τ²_U·log n at U = U*_{b(j)} ∖ {j}, c < 1 + 2A̲ fixed, then
P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 + 2A̲ − c)/2.

### 5.2 Bridge lemmas (each delivers one interface property)

| id | statement | new in this ticket |
|---|---|---|
| (B1) | (GF-16), (V-c), (V-m) and the functionals 𝔏_n(Q; h), 𝔏⁰_n(h) imply / dominate their block-relative versions for **every** partition with blocks ≤ 16 | elementary |
| (B-TK) | Lemma TK: Setting F (s₀ ≥ 0), (E), (GF-16) ⇒ [TK]. The block family has ≤ 2¹⁶p sets of size ≤ 16 with unnormalised Gram floor g_*; for each of them det H_U/det(G_U + I) = (n + 1)^{\|U\|}·e^{η_U} with −\|U\| log(1 + 1/g_*) ≤ η_U ≤ 0, and 0 ≤ Q_U − RSS^y_U ≤ 1 + 1/g_* (RSS^y_U := ‖(I − P_U)y‖²) | new: the toolkit is re-proved here under (GF-16); no registry claim is consumed |
| (B-L) | [TK] ⇒ [LEAK(Q)]: on 𝓔^blk and {\|Z_{T,l}\| ≤ h_l for all block pairs (T, l) with l ∉ Q} (the complement has probability ≤ b_n(h): a column has at most 2¹⁵ conditioning sets inside its block), each step with small gain is ≤ e^{2κ_E+o(1)}(n + 1)^{−1/2}exp((δ_{T,l} + σZ_{T,l})²/(2τ²_T)); a truncated expectation gives J_{h_l} | new (τ-form RSS bounds; Lemma J; column levels) |
| (B-V1) | (V-c), [TK], [LEAK(Q)], (AL) ⇒ P(e_n > n^{−κ}) → 0 and, by (AGG-d), [VIS(κ; Q)], every κ < (c_V − 1 − 2A)/2 | new (constant level; union over the ≤ s₀ truth blocks only) |
| (B-V2) | (V-m), [TK] ⇒ [VIS(κ; Q)], every κ < c_m/2 | new |
| (B-R) | Setting R with p > s₀ for all large n, (FL-R16), (V-R), (L-R) ⇒ with probability → 1 the design satisfies (E) (its energy bound holds with M = s₀²θ_hi²; p ≤ n^A, s₀ fixed and p > s₀ are assumed, they are not consequences of the population conditions), the normalised floor λ_min(R̂_T) ≥ φ₀² for 1 ≤ \|T\| ≤ 16 with a constant φ₀ > 0 (hence (GF-16)), (V-c) for every fixed c_V, and 𝔏_n(Q) ≤ exp(C√log n), default levels. If C_L = 0: 𝔏_n(Q) = O_P((log n)^{15κ_Q+1/2}) (a tightness statement; a bound with a fixed constant and probability → 1 is not claimed) | new |

### 5.3 Theorems (partition-free hypotheses)

**(T0) Theorem FLOOR (deterministic).** For every valid data set (n ≥ 4, EX-A) and every model S with |S| < K:
1 − π₀(S) ≥ f_n(|S|)/(1 + f_n(|S|)) ≥ ⅓(n + 1)^{−1/2}. In particular, whenever s₀ < K (true for all large n when
p > s₀): o₀ ≥ T₁ ≥ f_n(s₀) ≥ ½(n + 1)^{−1/2}: no condition on the design can give a start-mass rate better than n^{−1/2}.

**(T1) Theorem START-F (fixed design).** Setting F, the start as coded. Assume (E), (GF-16), visibility ((V-c) or
(V-m)), and (AL) for a deterministic Q ⊇ S₀ with |Q| ≤ K, with level vector h (default: h_l = z_n for l ∉ Q, giving
ϱ_n(Q; h) = ϱ_n(Q); when Q = S₀ this also gives 𝔏⁰_n(h) = 𝔏⁰_n and 𝔏_n(S₀; h) = 𝔏_n(S₀)). Then, for every κ ∈ (0, κ_V):
* (a) **lattice form.** 1 − π₀(𝓛(Q)) = O_P(ϱ_n(Q; h)) + o_P(n^{−κ}).
* (b) **no leakage, Q = S₀.** o₀ = O_P(n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ}); in particular π₀(S₀) → 1 in
  probability.
* (c) **first-order form** (Q = S₀). If moreover κ_V > ½ and n^{−1/2}𝔏_n(S₀; h)² → 0, then o₀/T₁ → 1 in probability
  (T₁ > 0 because p > s₀): the start odds against the truth are, to first order, the prior-weighted sum of
  the single-null block Bayes factors.
* (d) **uniformity.** For every ε > 0 and κ ∈ (0, κ_V) there are C < ∞, c₀ > 0 and n₀ depending only on (ε, κ) and the
  fixed constants (A, M, σ², g_*, s₀ and c_V or (c_m, ε₀)) such that for n ≥ n₀ and every (X, θ*, Q, h) — a fixed
  design with p ≤ n^A retained columns, |supp θ*| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, h a level vector for Q — satisfying at n
  the inequalities ‖μ‖² ≤ Mn, (GF-16), the visibility condition and ϱ_n(Q; h) ≤ c₀:
  P(1 − π₀(𝓛(Q)) > Cϱ_n(Q; h) + n^{−κ}) ≤ ε + b_n(h), and, for Q = S₀,
  P(o₀ > C[n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²] + n^{−κ}) ≤ ε + b_n(h).
Proof structure: (B1), (B-TK), (B-L), (B-V1)/(B-V2) deliver the interface properties; (C1) concludes.
Predecessor: T22(iii) ("PROVED-LOCKED (wave 2) + CONDITIONAL on EXP', VIS, NL_eta, NL_avg(kappa)", SOP:TH116). Here
the expansion EXP′ is derived from the Gram floor and (E), the uniform bound NL_η is not assumed, visibility is at a
constant level or in margin form, the hypotheses are partition-free, and the leading term, the lattice form and the
two-sided table identities are new.

**(T2) Corollaries (sufficient conditions for (AL); Setting F, (E), (GF-16), visibility with exponent κ_V; default
levels in F1–F3).**
* **F1 (uniform leakage; RM's (L-gain) form).** If δ²_{U,l} ≤ η·τ²_U·log n for every l ∉ Q and every U ⊆ [p] ∖ {l} with
  |U| ≤ 15, with a fixed η ∈ [0, η_A), then 𝔏_n(Q) ≤ n^{η/2+√(2Aη)+o(1)}; if moreover (|Q| + 1)n^{−κ₁} → 0 for some
  κ₁ < κ_L(η, A), then (AL) holds and P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)n^{−κ} + n^{−κ}) → 1 for every κ < min{κ_L(η, A), κ_V}.
  With η = 0 (no column outside Q gains anything): 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)√(log n/n)) + o_P(n^{−κ}), κ < κ_V.
* **F2 (strong signals; Q = S₀).** Let s₀ ≥ 1, θ*_min ≥ θ_lo > 0 fixed, λ_min(R̂_{S₀}) ≥ φ₀² with a fixed φ₀ ∈ (0, 1] (so Δ_U ≥ φ₀²θ_lo² for every
  U ⊊ S₀), p/√log n → ∞, n^{−1/2}𝔏_n(S₀)² → 0, and suppose δ²_{U,l} ≤ η′·Δ_U·log n for every l ∉ S₀ and every U ⊊ S₀
  with |U| ≤ 15, with a fixed η′ ∈ [0, 1). Then o₀ = O_P(n^{−(1−η′)/2}) + o_P(n^{−κ}) for every κ < κ_V. If η′ = 0 and
  κ_V > ½: **o₀ is of exact order n^{−1/2}** (o₀ = O_P(n^{−1/2}), and o₀ ≥ ½(n + 1)^{−1/2} by (T0)).
* **F3 (bounded gains).** If δ²_{U,l} ≤ C₀τ²_U for every l ∉ Q, |U| ≤ 15, and (|Q| + 1)n^{−1/2}e^{C₁√log n} → 0 for every
  fixed C₁: P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)n^{−1/2}e^{C₂√log n} + n^{−κ}) → 1 for every κ < κ_V, with C₂ = C₂(C₀, A).
* **F4 (isolated leaking columns; non-default levels).** Let I_n ⊆ [p] ∖ Q be deterministic with |I_n| ≤ ī (fixed), and
  suppose δ²_{U,l} ≤ c·τ²_U·log n for every l ∈ I_n and every U ⊆ [p] ∖ {l} with |U| ≤ 15, with a fixed
  c < 1 + 2A̲ (A̲ := liminf log p/log n). Put h_l := min(z_n, √(4 log log n)) for l ∈ I_n and h_l := z_n otherwise. Then
  b_n(h) → 0 and ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)·n^{−(1+2A̲−c)/2+o(1)}, where ϱ^{−I}_n(Q) is ϱ_n(Q) with the columns of
  I_n left out of the sum. Hence (AL) holds, and (T1) applies with this h, whenever ϱ^{−I}_n(Q) → 0 and
  (|Q| + 1)n^{−κ₁} → 0 for some κ₁ < (1 + 2A̲ − c)/2. (A bounded number of columns may leak at any constant level below
  1 + 2A̲; by (C2)(i) one column leaking above 1 + 2Ā given the truths of its block destroys the start mass. With the default levels, bound (J2) charges
  such a column n^{(c−1)/2+√(2Ac)+o(1)}/p when log p/log n → A; this upper bound tends to zero only for
  c < (√(4A + 1) − √(2A))², which is strictly below 1 + 2A. That is a threshold for the displayed upper bound, not a
  necessary threshold for the default functional.)

**(T3) Theorem START-R (random design).**
* (a) **transfer (any design law; design-measurable targets).** Let X^r be a random raw design and let α, β, Q and a
  level vector h be measurable functions of X^r. Suppose that, conditionally on X^r, y^r = α(X^r)1 + X^rβ(X^r) + ε with
  ε | X^r ~ N_n(0, σ²I), σ² > 0 fixed. Put θ* := D_xβ(X^r), S₀ := supp β(X^r) (after dropping constant columns). This
  contains the case of a deterministic β with ε independent of X^r, and Setting R. Suppose there are fixed constants
  (A, M, g_*, s₀ and c_V or (c_m, ε₀)), deterministic ϱ̄_n → 0 and b̄_n → 0, and measurable sets 𝒳_n with
  P(X^r ∈ 𝒳_n) → 1 such that every design in 𝒳_n satisfies, at n, with its own (θ*, S₀, Q, h): p ≤ n^A retained
  columns, |S₀| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, ‖μ‖² ≤ Mn, (GF-16), the visibility condition, b_n(h) ≤ b̄_n and
  ϱ_n(Q; h) ≤ ϱ̄_n. Then under the joint law, for every κ < κ_V: 1 − π₀(𝓛(Q)) = O_P(ϱ̄_n) + o_P(n^{−κ}), where
  𝓛(Q) = {T : S₀(X^r) ⊆ T ⊆ Q(X^r)}; for Q = S₀, if moreover n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)² ≤ r̄_n on 𝒳_n for a deterministic r̄_n ≥ 0:
  o₀ = O_P(r̄_n) + o_P(n^{−κ}), with o₀ the start odds against S₀(X^r). (Immediate from (T1)(d): given X^r the targets
  are fixed and the noise has Setting F's law; the constants of (T1)(d) depend only on the displayed bounds. Supports,
  coefficients or sets Q selected using the response are not covered.) *Convention off the design sets.* The design
  law is constrained only on 𝒳_n. On realisations where the start, the lattice or the odds are not defined as in §1
  (no retained column, an invalid response, S₀ ∉ Ω, S₀ ⊄ Q or |Q| > K), the quantities 1 − π₀(𝓛(Q)) and o₀ are set to 0;
  this is only a convention that makes the joint-law statements meaningful — nothing is claimed about a coded start
  on invalid inputs. The same convention applies in (T3)(b) and in the random-candidate clause of (T6).
* (b) **Gaussian rows.** Setting R with p > s₀ for all large n (at least one null, as in (E); nothing is claimed when
  p = s₀, §6). Assume (FL-R16), (V-R), (L-R). Then there is C_R < ∞, depending only on the fixed
  constants, with **P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)·n^{−1/2}·exp(C_R√log n)) → 1**. In particular with Q = S₀ (no leakage):
  P(π₀(S₀) ≥ 1 − n^{−c}) → 1 for every c < ½, for p ≤ n^A including p ≫ n. If C_L = 0 (exactly zero population
  leakage): 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)·n^{−1/2}·(log n)^{15κ_Q+1/2}).
  Proof structure: (B-R), then the uniform bound (T1)(d) conditionally on the design, as in (a) (with a slowly
  decreasing ε for the first display, and with the tightness of 𝔏_n(Q) for the clause C_L = 0). The averaged functional absorbs the Gaussian fluctuation of the off-block signal
  (δ_{U,l}/√Δ_U is a √n-scaled sample partial correlation), which a uniform bound δ²_{U,l} ≤ ητ²_U log n with η < η_A
  does not (RM `STATEMENT.md:271-273`).

**(T4) Proposition NEC (limits; Setting F, (E), (GF-16)).**
* (N1) = (T0): the exponent ½ in (T1)–(T3) is optimal; under F2 with η′ = 0 and κ_V > ½ the order is exact.
* (N2) **one leaking null.** If for all large n some null l = l_n has δ²_{V,l} ≥ c·τ²_V·log n for **every** V ⊆ S₀ with
  |V| ≤ 15, with a fixed c > 1 + 2Ā, then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1 − 2Ā)/2.
  **Scope of (N2).** When s₀ ≤ 15 the premise cannot hold: V = S₀ is among the sets, and δ_{S₀,l} = 0 for every null
  l because μ ∈ span X_{S₀}. So (N2) is a partition-free limit only for s₀ ≥ 16. For s₀ ≤ 15 the one-column failure
  threshold is claimed on the actual partition only, by (C2)(i), whose conditioning set U*_{b(l)} can be a proper
  subset of S₀. V = S₀ is not removed from (N2): a null whose block contains all the truths gains nothing given them
  and does not destroy the start mass.
* (N3) **one weakly visible truth.** If for all large n some truth j = j_n has δ²_{V,j} ≤ c·τ²_V·log n for **every**
  V ⊆ S₀ ∖ {j} with |V| ≤ 15, with a fixed c < 1 + 2A̲, then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 + 2A̲ − c)/2.
  So the constant 1 + 2A of (V-c) and (V-m) cannot be lowered.
  ((N2), (N3) follow from (C2), because the block-relative sets U*_{b(l)} and U*_{b(j)} ∖ {j} are among the sets V.)
* (N4) **outside the hypotheses.** Masked truths: PXN (S), "π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}"
  (PXN `STATEMENT.md:58-60`), is the law on PXN's family; strong-factor designs at p > K (PROGRAM decision D1,
  `BRIEF.md:20-21`) are outside the proved hypotheses and nothing is claimed for them.

**(T5) Interface corollaries.**
* **IF-START.** Under (T1) with (AL) at Q = S₀ and level vector h: for every event 𝒜 and every κ with 0 < κ < κ_V, 1_𝒜o₀ = O_P(r_n) with the
  deterministic rate **r_n := n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)² + n^{−κ}** → 0; under (T3)(b) with Q = S₀ the same with
  r_n := n^{−1/2}exp(C_R√log n). Hence P-START holds, and SAMP Theorem C (C-v)'s rate clause applies with
  1_𝒜δ̄ = O_P(max(r_n, r^{post}_n)) whenever P-CONC holds with a deterministic rate r^{post}_n. Only the start interface
  is supplied: P-CONC, P-MAP and SAMP's algorithm premises are not.
* **Proposition OVL (start mass under a bounded leakage set).** Setting F, (E), (GF-16), (V-c); Q = Q_n ⊇ S₀
  deterministic with |Q ∖ S₀| ≤ q̄ fixed and (AL) for Q; and deterministic levels a_{n,l} with 0 ≤ a_{n,l} ≤ ā < ∞ for a
  fixed ā, uniformly in n and l ∈ Q_n ∖ S₀, such that δ²_{U,l} ≤ a_{n,l}·τ²_U·log n for every l ∈ Q ∖ S₀ and every
  U ⊆ [p] ∖ {l}, |U| ≤ 15. Then for every ε > 0: P(π₀(S₀) ≥ n^{−E_n−ε}) → 1, E_n := Σ_{l∈Q∖S₀}[(a_{n,l} − 1)/2 − log p/log n]₊.
  Hence P-OVL in SAMP Theorem D's production form (max(n, p)·log₂(n + 1)·π₀(S₀) → ∞) holds whenever
  limsup(E_n − max(1, log p/log n)) < 0 — also when the start mode is not S₀.

**(T6) Corollary MIS (misspecified candidate set)**. Setting of MIS `STATEMENT.md:39-58` with a
**fixed** candidate design and (GR). Lemma R′ (re-proved in this ticket; the same algebra as MIS Lemma R, which is
therefore not consumed): under (GR), y^r = (α + a)1 + X^r_𝒞β^𝒞 + ε′ with ε′ ~ N_n(0, σ_𝒞²I), i.e. the candidate data
follow model G with (p, β, σ²) := (p_𝒞, β^𝒞, σ_𝒞²), truth S₀^𝒞 = supp β^𝒞. Hence each of (C0)–(C2), (T0)–(T2), (T4), (T5)
holds for the start π₀^𝒞 of the method re-run on the candidate data **provided all of that claim's hypotheses hold
after this substitution**; in particular concentration π₀^𝒞(S₀^𝒞) → 1 requires the substituted (E), (GF-16), visibility
and (AL) at S₀^𝒞, and then π₀^𝒞(S₀ ∩ 𝒞) ≤ 1 − π₀^𝒞(S₀^𝒞) → 0 whenever S₀ ∩ 𝒞 ≠ S₀^𝒞 eventually. For random candidate
designs the corollary is claimed through (T3)(a), under (GR) in its conditional form (given X^r_𝒞: ξ ~ N_n(0, τ²I) and
ε ~ N_n(0, σ²I) independent, (a, γ) measurable functions of X^r_𝒞): then ε′ | X^r_𝒞 ~ N_n(0, σ_𝒞²I), and the candidate
coefficients β^𝒞 = β_𝒞 + γ(X^r_𝒞), their support S₀^𝒞 and the set Q may be measurable functions of the candidate
design, on the high-probability design sets of (T3)(a). Candidate sets, supports or coefficients selected using the
response are not covered.

**(T7) Examples table** (families verifying the hypotheses; none is a hypothesis). **Examples verified in**
`lemmas/L11_EXAMPLES.md` **(author-verified, awaiting independent acceptance like the other proofs).** Fixed design,
p ≤ n − 1:
orthogonal designs with no leakage (F1 with η = 0, subject to visibility; F2 gives exact order n^{−1/2} for s₀ ≥ 1, fixed
nonzero signal strengths bounded away from zero and bounded above, and p/√log n → ∞); near-duplicate null columns at
distance of order 1 (covered by (GF-16), not by a normalised floor); one truth with fifteen nulls, each correlated
with it at ρ² = 0.4, signal θ*₁² = 2(1 + 2A)σ² log n/(n − 1), p = min(⌊n^A⌋, n − 1), A ∈ [0.1, 1] (covered by (V-m), not by
(V-c); default-level (AL) fails and F4 applies; this entry replaces the separate isolated-leaking-column entry of
v1.3). Gaussian rows, p ≫ n allowed: independent columns (C_L = 0, H_l = {l} ∪ S₀); block-diagonal Σ_n with bounded
groups, at most one truth per group and the truths' groups in Q (lattice form). **Expected, not verified in this
ticket:** UNI-0 families and exact-separation AR(1) with their relevance sets Q (lattice form); their verification of
(V-R), (L-R) is in sources of author-only status. Outside the hypotheses, with the reason: masked hubs (PXN:
visibility fails); strong factors at p > K.

## 6. Not claimed
* P(𝒜) → 1, delivery, anything about the sampler, the bridge, Ẑ or the reported model (SAMP, RM).
* π₀(S₀) → 1 under leakage: with Q ≠ S₀ only the lattice mass and the lower bound of Proposition OVL are claimed.
* A universal FLOOR bound for saturated reference models (|S| = K); any asymptotic claim when p = s₀.
* Necessity of (GF-16) (the proof route uses it; whether the Gram floor can be dropped altogether is open item
  W3-START-O2), of the form of the level vectors in J_h, of (L-loc-R), or sharpness of the factor e^{C_R√log n} in
  (T3)(b). A Gaussian-row statement with a population leakage level and an explicit exponent (open item W3-START-O1).
* A matching lower bound of order √(log p/n) when 𝔏⁰_n ≍ √log n (shown only in examples/numerics).
* A Gaussian-row bridge to (V-m) (only (V-c) is delivered by (B-R)); Proposition OVL under (V-m).
* Growing s₀ (the table identities are explicit in s₀; not harvested; open item W3-START-O3); non-Gaussian noise; a
  binary64 theorem; leakage sets beyond polylogarithmic size in (T3)(b); masked truths; strong-factor designs;
  supports, coefficients, leakage sets or level vectors selected using the response.

## 7. Dependencies (statuses verbatim; registry id @ version)
* Consumed: **none**. C-GROW:L0.1@1.0.0 "PROVED-CHECKED" and C-GROW:L0.2@1.0.0 "PROVED-CHECKED" (toolkit: events
  𝒟₁–𝒟₃, RSS floor, score differences for block tables; GROW `lemmas/L0_toolkit.md:19-53`) are stated with the
  normalised Gram floor and for s₀ ≥ 1; they are **not consumed**. Lemma TK re-proves the toolkit in this ticket under
  (GF-16) and for s₀ ≥ 0 (`lemmas/L2_TK.md`); those files and GEN `lemmas/L1_lemmaE.md` are sources of the argument only.
* Consumers: W3-SAMP:C@1.1.1 "PROVED-CHECKED", W3-SAMP:D@2.1.1 "PROVED-CHECKED" (their premises P-START, P-OVL).
* Cited as a limit, not consumed: W1-PXN:Thm-PXN(S)@1.0.0 "XF VERIFIED".
* Not consumed (lower or differently labelled assurance; re-proved here where needed): SOP:TH116@1.0.0 (T22(i), (iii));
  C-MIS:LemR@1.0.0 "R02 VERIFIED; council R07/R08 PASS" (Lemma R′ re-proves the reduction); W3-RM:B1@1.0.0,
  W3-RM:B2tau@1.0.0, W3-RM:SAND-R@1.0.0 "PROVED (by this seat, unchecked)" — the τ-form RSS bounds and the
  Gaussian-row sample-level facts needed for (B-R) are proved in this ticket (`lemmas/L2_TK.md`, `lemmas/L9_BR.md`).
