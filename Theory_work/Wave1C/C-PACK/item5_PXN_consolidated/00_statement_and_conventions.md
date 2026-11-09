# Consolidated proof of the W1-PXN theorem — Part 0: setting, theorem, conventions

This document proves the theorem of §0.4 (Theorem PXN: partition recovery, masked-regime start, LS0 discovery, posterior
concentration and composition on the masked correlated design LH-iid with p ≤ n^A). It is self-contained except for the
external results listed in §0.7, which are cited with their statements and statuses and are not re-proved.
Parts: 00 (this file), 01 tools, 02 design events, 03 start, 04 search, 05 posterior and output, 06 A-dependence and scope.

## 0.1 Setting: the family LH-iid

**Fixed parameters.** Integers g ≥ 2, c ≥ 1, v ≥ 0; ρ ∈ (0,1); ψ₁,…,ψ_c with 0 < |ψ_i| < ρ, ψ̄ := max_i|ψ_i|;
nonzero β₁,…,β_c and β^vis_1,…,β^vis_v; σ² > 0; a fixed A ≥ 1 (A > 1, i.e. p ≫ n, is allowed; no lower bound p ≥ n^a is used).

**Design.** p = p_n = G_n g with 18 ≤ p_n ≤ n^A and p_n → ∞. [p] is cut into G_n groups C₁,…,C_{G_n} of size g; the first
member of each group is its hub j_h. Groups 1..2c form c linked pairs (a_i, b_i) = (2i−1, 2i); groups 2c+1..2c+v are
visible; the others are null. Rows of X^r are iid N(0, Σ):
- within each group, equicorrelation ρ (unit diagonal);
- distinct groups independent, except Σ[C_{a_i}, C_{b_i}] = ψ_i Σ[C_{a_i}, j_{a_i}] Σ[j_{b_i}, C_{b_i}] (rank one through
  the hubs: corr(j_a, j_b) = ψ, corr(j_a, k) = ψρ for k ∈ C_b∖j_b, corr(k′, k) = ψρ² off the hubs).
The sequence is indexed only by admissible sample sizes n≥3 with integer G_n≥2c+v, so all named signal groups exist.
Standardization is on the probability-one event of nonconstant columns and response. Every-n assertions below mean every
such admissible n; changing or omitting a finite initial segment has no effect on the asymptotic conclusions. (R39 #5)

**Truth.** θ_{j_{a_i}} = β_i, θ_{j_{b_i}} = −ψ_iβ_i, θ_{j_h} = β^vis_h (visible groups), all other coefficients 0;
y^r = X^rθ + ε, ε ~ N(0, σ²I_n) independent of X^r. So s₀ := 2c + v, S₀ := supp θ = {j_{a_i}, j_{b_i}}_i ∪ {visible hubs}.
The **masked set** is 𝓜 := {j_{b_i}}_{i≤c} (written 𝓜 to keep it apart from the constant M of §0.2); the **reference** is
S° := S₀ ∖ 𝓜, s := |S°| = c + v, Φ(S) := |S Δ S₀|, so Φ(S°) = c. **Neutral variables:** l ∉ S₀ ∪ ∪_i C_{b_i}.
**Proxies:** C_{b_i} ∖ {j_{b_i}}. The **lattice** is Lat(S°) := {S° ∪ 𝓜′ : 𝓜′ ⊆ 𝓜}; it contains S° and S₀.

**(SIZE).** g ≤ B_n < 2g for n ≥ n₁, with B_n = min(⌊√n⌋, ⌊√p⌋, 16) (the method's block size). Since B_n = 16 once
n, p ≥ 256, this means 9 ≤ g ≤ 16 asymptotically (at n=200 and p≥196, B_n=14 and SIZE means 8≤g≤14; for smaller p use B_n=min(14,floor(sqrt p))). n₁ is the SIZE onset of the sequence p_n.

## 0.2 Notation, population facts, constants

**Population facts.** (F2) Cov(X_{C_{b_i}}, μ_i) = 0 with μ_i := β_i(x_{j_{a_i}} − ψ_ix_{j_{b_i}}); (F3) C_{a_i} ⊥ C_{b_i} | x_{j_{a_i}};
(F4) λ₀ := λ_min(Σ) ≥ (1 − ψ̄)(1 − ρ) > 0; (F5) the components K_i := C_{a_i} ∪ C_{b_i}, V_h := C_h (visible groups) and the
null groups are mutually independent, and μ := X^rθ = Σ_i μ_i + Σ_h β^vis_h x_{j_h} (population signal). 𝒮𝒱 := ∪_i K_i ∪ ∪_h V_h
is a fixed finite index set, |𝒮𝒱| = g s₀.

**Constants.** φ₀² := λ₀/2; M := 2θᵀΣθ + 1; b_min := ½ min_{i,h}(β_i²ψ_i², β_i², (β^vis_h)²) (min over empty visible
family := +∞).

**Letters.** The letter A denotes the fixed exponent in p_n ≤ n^A (and in D = A, D = A(s₀+2), (2A+1) log n, …) and also, as in
the sources, generic subsets A, A′, A_s, A₀ of [p]; the context always separates the two. M is the constant above; the
masked set is 𝓜. In Theorem R the letter q_R (not q) denotes √((1−ψ̄²)/(1−ρ²)); q, e without subscript are the start-aggregation
quantities of §3.2. The score margin of §4.2 is written mar_n(c′); the SE cutoff of §2.1 is m_n. The Mills threshold of §4.4 is
u_n. Truncation thresholds of Tr-J are indexed by the family exponent: t_{n,D} := 8(D+1) log n, τ_{n,D} := t_{n,D}/n.

**Standardised objects.** C := I − 11ᵀ/n; X = CX^rD_x⁻¹ (columns of squared norm n−1), y = Cy^r/s_y. Y := Cy^r (raw-centred
response), μ = CX^rθ = Xθ* with θ* = D_xθ (sample version of the signal). R̂ := XᵀX/(n−1) (sample correlation), R̂_T its
principal submatrix on T. For A ⊆ [p]: P_A the projection onto span X_A, Π_A^⊥ := C − P_A, RSS_A := ‖Π_A^⊥Y‖² (raw-centred
scale), RSS^y_A := ‖Π_A^⊥y‖² = (n−1)RSS_A/‖Y‖², Λ_A := ‖Π_A^⊥μ‖².

## 0.3 Target, method, runs, operational premises

**Target (posterior).** K = min(p, ⌊n/2⌋), Ω = {S : |S| ≤ K}. G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I,
D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, a₀ = b₀ = 0.01, ν = a₀ + n/2;
m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}; w(k) = ½/C(2p−1, k); W_K = Σ_{k≤K} C(p,k)w(k);
F(S) = log[w(|S|)m(S)/W_K]; π(S) ∝ e^{F(S)} on Ω (ridge-type g-prior with g = n, BB(1,p) size prior, IG(a₀, b₀)).
Block tables: r_b(U) = m(U)/m(∅) for U ⊆ block b.
For S ∈ Ω, define γ₀(S) := [w(|S|)/W_K]∏_b r_b(S ∩ C_b),
Z̄₀ := Σ_{S∈Ω} γ₀(S), and π₀(S) := γ₀(S)/Z̄₀; set π₀(S) := 0 outside Ω.
Here C_b denotes a method block; the group version uses the population groups instead.
For a feasible reference S° let U_b° := S° ∩ C_b and s := |S°|. Define
a_bj := Σ_{U_b°⊆U⊆C_b, |U∖U_b°|=j} r_b(U)/r_b(U_b°),
D_b := max_{1≤j≤|C_b∖U_b°|}(j!a_bj)^{1/j}, with an empty maximum equal to 0,
q := (p−s)^{−1}Σ_b D_b if s < p, and q := 0 if s = p,
e := 2p max{[r_b(U)/r_b(U ∪ U_b°)]^{1/a} : b, U ⊆ C_b, a := |U_b°∖U| > 0}, with an empty maximum equal to 0.
These are the actual-block T22(i) quantities on every data set. On 𝒜_n they equal
the group versions in §3.2; there each nonempty U_h° is a singleton, so a = 1.

**Method.** SMC-BVS v3 as frozen (partition by complete linkage on 1 − |r̂| + top-down cut + next-fit packing with capacity
B_n; exact block start π₀ from the block tables; tempering; islands; HPM = best scored model), **plus LS0**: one production
local search — scan all flips and swaps of the centre; move to the best scanned model if it strictly beats the centre
(lexicographic ties); at most ℓ_n = ⌈log₂(n+p+1)⌉ moves, then one final scan — centred at the exact start mode
S̃₀ = argmax π₀ (max-plus convolution of block tables, deterministic tie rule); the centre is the first evaluation and is
offered to the HPM; every scan is completed; LS0 is a deterministic function of the data. Concretely, LS0 =
`local_search(S̃₀, ell_n, tier, emit_centre = true)` on the start mode returned by `start_mode`, executed after R̄ on every
fit counted in 𝒪; the current production core calls only `local_search(led.hpmS, ell, tier, false)`
(`Scripts/SMC_BVS/core/cpp/v3_core.cpp:447`), so LS0 is a method change and the theorem concerns v3 + LS0 under (OP).
A **flip** adds or deletes one variable; a **swap** exchanges one member for one non-member; a move is **feasible** if the
result lies in Ω.

**Runs, scored sets, output.** R̄ = the potential uninterrupted run (exact-arithmetic EX-A, guards removed), with status
st̄ ∈ {exact, completed, schedule_limit}; R̄⁺ = R̄ followed by LS0. The actual run's status st and outputs are functions of
(R̄, Ξ) (Ξ = allocation, clock, load). Strict output event 𝒪 := {st ∈ {exact, completed}}, U := 𝒪ᶜ; 𝒪̄ := {st̄ ∈ {exact,
completed}}. 𝒮 = every model scored by the run, 𝒮_LS0 = models scored by LS0, 𝒮⁺ := 𝒮 ∪ 𝒮_LS0, **Ŝ⁺ := the reported HPM = the
best model in 𝒮⁺** under (F, −|S|, lex); barred symbols are the R̄⁺ versions.

**Operational premises (OP)** (assumptions, not discharged implementation claims): EX-A, EX-S, CAL (declared idealisations);
SR; GUARD ((G1) the guard reads only the clock, consumes no random number, changes no setting; (G2) a run no guard check
stops performs exactly the R̄ (R̄⁺) computation); OP-LS0 (LS0 executed, centre emitted, scans completed, on every fit counted
in 𝒪; post hoc execution allowed; a stopped LS0 counts in U). The v3 budgets are indexed by n; in particular ℓ_n =
⌈log₂(n+p+1)⌉. EX-A includes exact arithmetic for scores and for the start-mode DP.

## 0.4 The theorem

**Theorem PXN.** Assume LH-iid with (SIZE), 18 ≤ p_n ≤ n^A (A ≥ 1 fixed, A > 1 allowed), p_n → ∞, s₀ = 2c+v fixed, and (OP).
As n → ∞ (conclusions (S), (E), (T), (P) concern the data (X, ε) and the deterministic LS0 of R̄⁺; only (C) involves the actual run):

- **(R)** P(𝒜_nᶜ) → 0 with Σ_n P(𝒜_nᶜ) < ∞, and P(𝒜_nᶜ) ≤ p^{−C} for n ≥ max{n₁, n₀(A, C, ρ, ψ̄)}, where 𝒜_n := {blocks = groups}.
  Explicit form (Theorem R, §2.3): for n ≥ 5 with SIZE at n, P(𝒜_nᶜ) ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I*}, with
  I(t; r) := −½ log[(1−r²)(1−t²)/(1−rt)²], q_R := √((1−ψ̄²)/(1−ρ²)), t* := (q_R−1)/(q_Rρ−ψ̄) ∈ (ψ̄, ρ), I* := I(t*; ψ̄) = I(t*; ρ) > 0.
- **(S)** 1 − π₀(S°) = O_P(√(log n/n)), with the explicit truncated-moment and tail bounds of §3.2
  (E[q̃1_{𝒢_n}] ≤ C_q√(log n/n), P(q > x) ≤ C_q√(log n/n)/x + P(𝒢_nᶜ)); π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} → 0, more precisely
  log π₀(S₀) + c log p + (c/2) log n →_d Σ_{i≤c} log((s+i)/2) + ½χ²_c (§3.3): the masked regime.
- **(E)** P(S̃₀ = S°) → 1; S° ⊆ S₀ has no extras and Φ(S°) = c; S° is a lattice reference (S° ∈ Lat(S°)).
- **(T)** P(LS0 of R̄⁺ scores S₀) → 1 and P(LS0 of R̄⁺ returns S₀ with local_certified) → 1.
- **(P)** δ₁ := 1 − π(S₀) = O_P(√(log n/n)) under the joint law of (X^r, ε); hence E₀δ₁ → 0 (E₀ = joint expectation).
- **(C)** For every n: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) ≤ P(LS0 of R̄⁺ does not score S₀), and
  D_n → 0. Hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0, liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U), and
  P(𝒪 ∩ {Ŝ⁺ = S₀}) → 1 − u whenever P(U) → u.
- **(K)** LS0 costs ≤ 1 + (ℓ_n+1) max_{k≤K}[p + k(p−k)] = O(p² log(n+p)) scores; on the joint event 𝒯_n of §4.6 (lattice arrival
  + (L) + ℓ_n ≥ c) it uses c + 1 scans and ≤ 1 + (c+1)(p + s₀p) scores.

**Headline.** On the masked correlated design LH-iid with p ≤ n^A (A > 1 allowed), for v3 + LS0:
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, i.e. P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U_n)) → 0, so liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
**Not claimed:** P(U) → 0 (delivery); the method without LS0; masked PIP/evidence accuracy; the study's own design (groups of 5
violate SIZE); superpolynomial p; any quantitative finite-n consistency guarantee, in particular none at n = 200 (the proven
margins are vacuous there, §8 (O5)); no uniformity in A. ((C) itself holds at every n and (K) is deterministic.)
In (S) no statement that the rate √(log n/n) is sharp in order is made.

## 0.5 Conventions

**Exact arithmetic.** EX-A: scores and the start-mode DP are exact. GUARD and OP-LS0 are hypotheses.

**Exact-branch convention.** The production dispatch runs exact enumeration when Σ_{k≤K} C(p,k) ≤ (5H₀+4N₀)p (budget
constants H₀, N₀ of the method), which can hold for p ≥ 18 when p_n grows very slowly (e.g. p_n = g⌈log₂log₂(n+4)⌉); then no
partition or block start is built. The theorem allows such sequences and acquires no lower growth bound on p. Therefore
"blocks", the block tables, π₀, S̃₀ and "LS0 of R̄⁺" denote the deterministic make_blocks / block-table / start-mode /
local-search functions of the data computed on **every** branch (hypothetical when the actual run takes the exact branch).
(R), (S), (E), (T) are statements about these data functions and are proved without reference to the branch. The handling of
the exact branch in (C) is in §6.2.

**Onset.** n₀ is taken large enough that, for n ≥ n₀: SIZE holds (n ≥ n₁); s₀ ≤ K; ℓ_n ≥ c; n ≥ 2(s₀+2) + g; and every
"for n ≥ n₀" condition of the lemmas below holds (Tr-J: n ≥ 8(J+1), t′ ≥ 6J, τ_n ≤ ½; Lemma E; (U3): C₂n^{−1/3} ≤ c′H/(4H+c′)
with H = σ²+M, c′ = c₂/2; mar_n(c₂/2) > 0; L_nδ_n ≤ λ₀/2; (L): x_l ≤ ¼ and the additive remainder ≤ 1). All listed conditions
hold eventually for every fixed A; each onset is an explicit polylog-versus-polynomial condition in n, depending on A and the
fixed parameters, plus the SIZE onset n₁ of the sequence p_n; a sufficient envelope for the slowest of them (L_nδ_n ≤ λ₀/2 and
the (L) remainder) is n/(log n)³ ≥ C(A, fixed parameters).

## 0.6 Group versions and Lemma T

**Group versions.** Every object the method builds from the blocks (tables r_b, γ₀, π₀, S̃₀, and the aggregation quantities
a_bj, D_b, q, e of §3.2) has a *group version*, built with the groups C₁,…,C_{G_n} in place of the blocks, written with a
tilde: r̃_h, π̃₀, S̃₀^~, ã_hj, D̃_h, q̃, ẽ. These are functions of (X, y) that never look at the partition.

**Lemma T (transfer: the random-partition quantifier).** (i) On 𝒜_n every block object equals its group version: r_b = r̃_h
for the group h = C_b, π₀ = π̃₀, S̃₀ = S̃₀^~, (a_bj, D_b, q, e) = (ã_hj, D̃_h, q̃, ẽ), and the LS0 centre is S̃₀^~. (ii) Consequently,
for any event E defined through block objects, P(E) ≤ P(Ẽ) + P(𝒜_nᶜ), where Ẽ is E with every block object replaced by its
group version. (iii) The laws of the group statistics used below (Lemma B, Lemma Λ) are their **unconditional** laws under the
joint law of (X^r, ε); they are never conditioned on 𝒜_n, on ℰ♯_n, or on any selection.

*Proof.* (i) is the definition of the group versions: on 𝒜_n the block index set {C_b} coincides with {C_h}, and every listed
object is a function of the data and the partition only. (ii) E ∩ 𝒜_n = Ẽ ∩ 𝒜_n by (i). (iii) is a rule of use: every
probability statement below is first proved for the tilde objects on the whole probability space, and 𝒜_n is intersected at
the end through (ii). ∎

*Remark.* Nothing below conditions a Beta law on 𝒜_n. The partition is σ(X)-measurable and independent of ε, but that fact is
not used; only (i)–(ii) are.

## 0.7 External results cited (not re-proved)

Quoted archive statuses are reproduced verbatim where given; other entries
explicitly describe provenance or the role of an assumed input and do not assign
a new verification status. NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`. CODE = the frozen core
`Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/` (other copies, e.g. `Scripts/SMC_BVS/core/`, are named by full path).

| Label | What is used | Source | Status quotation or descriptive provenance |
|---|---|---|---|
| [LM] | Laurent–Massart (2000), eqs (4.3)–(4.4): for k ≥ 1, x > 0, P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x}, P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x} | Laurent & Massart, Ann. Statist. 28(5) (2000), p. 1325 | published inequality (citation checked in review) |
| T22(i-a) | for every partition and positive tables and every S° ∈ Ω: if q < 1 then 1 − π₀(S°) ≤ (s+1)q/(1−q) + se (deterministic) | `NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md:35` | "PARTLY PROVED: (i), (ii), (iv) PROVED-LOCKED (wave 1; (iv-c) premises 1 - pi(S0) -> 0 from T03 and 1 - pi0(S0) -> 0 from (iii))"; same row: "same-family and cross-family (Astra); not adopted" (`NBH/ID_REGISTRY.md:264`) |
| T22(ii-a) | on recovered blocks, for feasible S₀: π₀(S₀) = π₀(S°)[w(s+c)/w(s)]∏_i r_{b_i}({j_{b_i}}) exactly (S₀ and S° differ only in the b-blocks, where S° is empty) | same, `STATEMENT.md:40-41` | same row |
| T03♯ | theorem of record TH128; fixed-design posterior concentration; statement quoted in §5.1 | `NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-60`; card `Theory_work/State_of_Project/sections/04_theory.tex:763-818` | "Status: PROVED (S03 §6; changed steps C1–C10 written in full there); V03 and A-REV2: VERIFIED under exactly these hypotheses." (`STATEMENTS.md:51-52`); "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (`04_theory.tex:788`) |
| W7 Theorem B / Corollary B | pair-tail union bound and the closed form S(t*) ≤ K_n of §2.3 (Hotelling density, Lemma 2, Corollary 1) | `NBH/branch_snapshots/W7-PART/PROOF.md` | "PROVED (W7-PART); Theorem B XF VERIFIED* (A-REV6 restricted scope; A-REV9 B-exact VERIFIED); Corollary B XF GAP (A-REV9, L2 constants)" (`NBH/ID_REGISTRY.md:311`) |
| W7 Theorem A | (A4 ⇒ A1 ⇒ A3) global margin ⇒ laminarity ⇒ blocks = groups; used only inside route (R′) | same | "PROVED (W7-PART); XF VERIFIED* (A-REV9: A1-A4 VERIFIED, A2 extra premise; A-REV6: A0(c) GAP)" (`NBH/ID_REGISTRY.md:310`) |
| (OP) / composition | operational premises EX-A, EX-S, CAL, SR, GUARD, OP-LS0; output/scored-set conventions; definition of R̄⁺ | W6-FIXREV1 `T38_STATEMENT.md` (conventions at 41-44, R̄⁺ at 48-51, GUARD at 56-73) | candidate premises of the theorem, taken as hypotheses |
| Lemma RO | replay inclusion under GUARD | `NBH/branch_snapshots/W2-BOOK/PROOF.md:75-95` | "PROVED" and "SF/XF-reviewed" (as recorded in the council review of the ticket; not adopted) |
| W3-PXN | the F2–F5 population computations and the heuristic threshold of §4.4 | `NBH/branch_snapshots/W3-PXN/PROOF.md` | cited for computations only |

Which of the cited statements feed which step: [LM] → §1; T22(i-a) → §3.2; T22(ii-a) → §3.3; T03♯ → §5; W7 Theorem B/Cor. B →
§2.3 (R-b), with the self-contained route (R′) of §2.4 (Lemma CR + W7 Theorem A) as an independent summable alternative;
OP, Lemma RO → §6.
