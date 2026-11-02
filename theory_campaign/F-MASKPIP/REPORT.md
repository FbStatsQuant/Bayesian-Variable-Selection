# F-MASKPIP REPORT — what Ẑ and the PIPs mean in the masked regime

Run F-MASKPIP (Fable 5.1), branch `theory/F-MASKPIP`, 2026-11-02, laptop. Everything here is a **candidate**: not
reviewed, not adopted. Status words follow `theory_campaign/PROTOCOL.md`. Notation: `00_COMMON.md`, the locked
statements of T12, T14(i), T15, T23(ii), T31(i), and W2-T26 (Theorem A, Lemmas 2–3). Scripts and raw outputs by the
helper run are in `scripts/` and `results/` (see §4 and `results/SIM_NOTES.md`).

## 1. Headline

1. **Evidence-weighted PIP accuracy (Proposition M1) — PROVED, every regime, every frozen grid.** For each island,
   E_𝓒[ (Ẑ_r/Z) · max_j |PIP̂_rj − 1{j∈S₀}| ] ≤ δ₁ + ρ̄ + u_π, with no premise on the start. The island evidence
   weight sits exactly on the realisations whose PIPs are right. Consequences (Corollary M2, PROVED): an island
   whose terminal population is off S₀ reports Ẑ_r ≤ √δ₁·Z except with probability 2√δ₁; an island with
   Ẑ_r ≥ cZ has PIP error ≤ ε except with probability (δ₁+ρ̄+u_π)/(cε); the same for the pooled Ẑ with the
   Ẑ_r-weighted PIP. So in the masked regime **the reported PIPs can be wrong only on islands whose evidence is a
   gross underestimate**, never the other way round.
2. **No conditional evidence theorem exists (Proposition M3) — PROVED.** E_𝓒[Ẑ_r/Z | crossing] ≥ (1−2δ₁)/P_𝓒(crossing):
   conditioning on the bridge having delivered the population to S₀ makes the island evidence *overestimate* in mean
   by the reciprocal of the crossing probability, and no first-moment input bounds P(Ẑ_r/Z < c | crossing). A
   "restart T26" for Ẑ needs a second-moment input (PW2 / T25(iv)); the locked tools cannot give it.
3. **Restart theorem for PIPs (Theorem R) — PROVED as a composition, CONDITIONAL on two masked-regime inputs.**
   E_𝓒 max_j|PIP̂_rj − 1{j∈S₀}| ≤ δ_𝔛 + β_H + (L+4)ρ̄ + u_π, where δ_𝔛 is the expected fraction of the population
   outside a repair basin 𝔛 at the end of stage T and β_H the uniform H-round entrance failure from 𝔛. It uses **no
   evidence quantity at all**. With T03 (δ₁, u_π → 0, (L+4)(B+3)u_π → 0), PIP and MPM consistency in the masked
   regime reduce to population delivery (DELIV-POP, OPEN; stronger than T38's one-particle DELIV) and repair
   (REP, W1-T24G Theorem B, candidate).
4. **The negative route is real (Proposition N) — (a) PROVED, (b) PROOF SKETCH on an explicit family.** (a) In any
   family where the terminal population is off S₀ at the end of stage T with probability bounded away from 0, Ẑ_r
   underestimates Z there by a factor ≥ δ₁^{−1/2} → ∞ (≥ (n/log n)^{1/4} under T03's rate), while T31(i)'s 95% lower
   bound stays valid and becomes uninformative. (b) On an omission-masked (LH-type) family with the one-stage grid
   T = 1, Ẑ_r/Z ≤ e^{−Θ(n)} with probability → 1, and the terminal Gibbs path still repairs the population, so the
   PIPs are consistent: **evidence and PIPs separate completely.** Confirmed numerically at p = 18 (§4.1, 3,840
   island-runs): with a one-stage or a blind restricted-ESS grid, median log Ẑ_r/Z = −4 to −12 while the island PIP
   error equals the exact posterior's to four digits and the MPM is right in 100% of runs; (I2) and (I3) = (M1-c)
   hold in every run. Independent corroboration: W4-SHARE's PB design (delivery 200/200 islands, median log Ẑ/Z = −67).
5. **Why they separate (Proposition W4, F-DRAFT).** Ẑ is an L²/χ² object along the bridge (one-step ESS
   1/(1+χ²(π‖π₀)) ≥ … ≥ π₀(S₀)/π(S₀)², i.e. ≈ 10⁻¹² at the study scale), the PIPs are an L¹/occupancy object (the
   fraction of particles at S₀ in the measured rounds, a TV-type quantity the terminal kernel can fix). W4 shows the
   two scales already diverge in the favourable BO regime (KL, TV → 0 while χ² → ∞); the masked regime only widens the gap.
6. **At n = 200** the paper can claim: E Ẑ = Z, the 95% lower bound and E log Ẑ ≤ log Z (regime-free); the
   pathwise PIP bound (error ≤ fraction of measured paths leaving S₀ + u_π); and the evidence–PIP coupling of M1–M2.
   It cannot claim Ẑ/Z ≈ 1, any relative accuracy of Ẑ, or PIP accuracy from the evidence; and with the measured
   median π₀(𝓡₂) ≈ 0.8, Theorem R's finite-n bound is not small. Details in §7.

## 2. Setting and notation

Island r of the final run, given data and a successful 𝓒 (EX-A, EX-S, CAL, START; T12 §2). W_r := Ẑ_r/Z,
W̄ := Ẑ/Z = ¼Σ_r W_r. Terminal positions τ_s, s = 0, …, L+3: "after s terminal rounds" (τ₀ = end of stage T). f_{r,s}
:= fraction of island r's particles outside S₀ at τ_s. B̄_r as in T23(ii) (fraction of (particle, measured round)
pairs whose path, start included, leaves S₀). err_r := max_j |PIP̂_rj − 1{j∈S₀}|; err_prim, err_sec the same for the
primary (equal-weight) and secondary (Ẑ_r-weighted) pooled PIPs. δ₁ = 1 − π(S₀), u_π = δ₁/π(S₀). ρ̄ := probability
that one round at φ = 1 started at S₀ has a state ≠ S₀ on its path (a data-only number, since the order law is
uniform); W2-T26 Lemma 2 (candidate, from locked T09(ii)) gives ρ̄ ≤ (B+3)u_π. Crossing event C_{r,s} := {f_{r,s} ≤ ½}.
Masked regime: π₀(S₀) → 0 while δ₁ → 0 (F-DRAFT §0). Throughout S₀ ∈ Ω; if S₀ ∉ Ω then u_π = ∞ and all bounds are trivial.

## 3. Statements and proofs

### Proposition M1 (evidence-weighted PIP bound). PROVED.

For every data set, every successful 𝓒 (any frozen grid, any N ≥ 1), every island r and every s ∈ {0, …, L+3}:

  (M1-a) E_𝓒[W_r f_{r,s}] = δ₁ and E_𝓒[W_r] = 1;
  (M1-b) E_𝓒[W_r B̄_r] ≤ δ₁ + ρ̄;
  (M1-c) E_𝓒[W_r err_r] ≤ δ₁ + ρ̄ + u_π.

*Proof.* (a) T12(i.b) (locked) at the position τ_s with f = 1_{Ω∖{S₀}}, a function fixed given 𝓒: E_𝓒[Ẑ_r q̂_{r,τ_s}(f)] =
Zπ(Ω∖{S₀}) = Zδ₁; divide by Z. With f ≡ 1 it gives E_𝓒 W_r = 1 (T12(i.a)). W_r is the same random variable at every
terminal position because the terminal rounds carry no weights.
(b) W2-T26 Lemma 3 (candidate; one line): B_{i,h} ≤ 1{X_{i,L+h−1} ≠ S₀} + 1{X_{i,L+h−1} = S₀}D_{i,h}, where D_{i,h}
indicates that particle i's path in measured round L+h leaves S₀. Multiply by W_r ≥ 0 and average over (i, h):
W_r B̄_r ≤ ¼Σ_h W_r f_{r,L+h−1} + (4N)⁻¹Σ_{i,h} W_r 1{X_{i,L+h−1} = S₀} D_{i,h}. The first sum has expectation δ₁ by (a).
For the second, let H be the σ-field of everything before round L+h. W_r and 1{X_{i,L+h−1} = S₀} are H-measurable
(Ẑ_r is fixed at stage T). By T12's (R3) (uniform order independent of H, path a Markov chain with the elementary
kernels), E_𝓒[D_{i,h} | H] = ρ̄ on {X_{i,L+h−1} = S₀}. Hence the second expectation is ≤ ρ̄ E_𝓒 W_r = ρ̄.
(c) T23(ii-a,b) (locked, pathwise): err_r ≤ B̄_r + u_π on every realisation. Multiply by W_r, take E_𝓒, use (b) and
E_𝓒 W_r = 1. ∎

*Remarks.* (i) No independence across particles, no union bound over coordinates, no premise on π₀(S₀), no bound on
T, no condition on N. (ii) The right side is exactly W2-T26's (A-0)(c) bound with the two "2b(𝓒)" terms deleted: the
evidence weight replaces the evidence lower tail. (iii) It is **not** an identity: E_𝓒[W_r f_{r,s}] = δ₁ is, and the
rest is the T23 pathwise step.

### Corollary M2 (dichotomies). PROVED.

For every c ∈ (0,1), ε ∈ (0,1], s, r:

  (M2-a) P_𝓒(f_{r,s} > ½ ∧ W_r ≥ c) ≤ 2δ₁/c. In particular, with c = √δ₁: P_𝓒(f_{r,s} > ½ ∧ W_r ≥ √δ₁) ≤ 2√δ₁.
  (M2-b) P_𝓒(err_r > ε ∧ W_r ≥ c) ≤ (δ₁ + ρ̄ + u_π)/(cε); P_𝓒(MPM̂_r ≠ S₀ ∧ W_r ≥ c) ≤ 2(δ₁ + ρ̄ + u_π)/c.
  (M2-c) Secondary PIP: P_𝓒(err_sec > ε ∧ W̄ ≥ c) ≤ (δ₁ + ρ̄ + u_π)/(cε).
  (M2-d) Primary PIP: P_𝓒(err_prim > ε ∧ min_r W_r ≥ c) ≤ (δ₁ + ρ̄ + u_π)/(cε).
  (M2-e) E_𝓒[W_r 1{f_{r,s} > ½}] ≤ 2δ₁ and E_𝓒[W_r 1{C_{r,s}}] ≥ 1 − 2δ₁.

*Proof.* (a) On {f > ½, W ≥ c}, W f ≥ c/2, so the indicator is ≤ 2Wf/c; take E_𝓒 and use (M1-a). (b) Same with
W·err ≥ cε and (M1-c); MPM̂_r ≠ S₀ forces err_r ≥ ½. (c) |P̃_j − 1{j∈S₀}| = |Σ_r W_r(PIP̂_rj − 1{j∈S₀})|/Σ_r W_r ≤
Σ_r W_r err_r/(4W̄) ≤ Σ_r W_r err_r/(4c) on {W̄ ≥ c}; Markov with E_𝓒 Σ_r W_r err_r ≤ 4(δ₁+ρ̄+u_π). (d) err_prim ≤
¼Σ_r err_r ≤ Σ_r W_r err_r/(4 min_r W_r). (e) 1{f > ½} ≤ 2f; and E W_r = 1. ∎

*Reading.* (M2-a) with c = √δ₁ says: **a non-crossing island underestimates Z by a factor ≥ δ₁^{−1/2}** except on an
event of probability 2√δ₁. (M2-b,c) say: **an island (or the pooled run) whose evidence is not a gross
underestimate has accurate PIPs.** Both are statements about the joint law given 𝓒; neither conditions on an
observed event, so T12(iv.e)'s warning (conditioning on favourable diagnostics breaks the identities) does not bite:
the inequalities are stated for intersections, exactly as Theorem A states its conclusions on 𝒪_n ∩ {…}.

### Proposition M3 (no conditional evidence theorem from first moments). PROVED.

Let C = C_{r,s} be any crossing event with P_𝓒(C) =: κ > 0. Then
  E_𝓒[W_r | C] ≥ (1 − 2δ₁)/κ  and  E_𝓒[W_r | Cᶜ] ≤ 2δ₁/(1−κ).
Moreover, for every κ ∈ (0,1) and δ₁ ∈ (0, ¼) there is an abstract instance of T15's setting (W_r > 0, f_r ∈ [0,1],
E W_r = 1, E[W_r f_r] ≤ δ₁) in which P(W_r < c | C) = 1 for some c < 1 (take W_r = c on a subset of C of mass
κ − κ′ and W_r = (1 − c(κ−κ′))/κ′ on the rest, with f_r = 0 on C and f_r = 1, W_r = 0 on Cᶜ; the identity constraints
are all satisfied).

*Proof.* (M2-e) and E W_r = 1 give E[W_r 1_C] ≥ 1 − 2δ₁ and E[W_r 1_{Cᶜ}] ≤ 2δ₁; divide by κ, 1−κ. The instance is a
direct check. ∎

*Reading.* Conditioning on delivery does not restore Ẑ: on average over crossing realisations the island
overestimates by 1/κ, and the dispersion of W_r on C is unconstrained by every first-moment identity we have
(T12(i), T15, T14(i) with η₀ ≈ 1). Any masked-regime evidence statement needs a second-moment input (PW2 → T25(iv))
or a different estimator. The one thing that survives everywhere is T31(i): P_𝓒(Z ≥ αẐ) ≥ 1 − α and E_𝓒 log Ẑ ≤ log Z.

### Theorem R (restart theorem for the PIPs; no evidence input). PROVED as a composition.

Fix data, a successful 𝓒 and an island r. Let 𝔛 ⊆ Ω be fixed given 𝓒 with S₀ ∈ 𝔛 (a *repair basin*), and H ∈
{1, …, L}. Define
- δ_𝔛 := E_𝓒[N⁻¹Σ_i 1{X_{i,0} ∉ 𝔛}] (expected fraction outside 𝔛 at the end of stage T; "late delivery");
- β_H := sup_{x∈𝔛} P_x(X_h ≠ S₀ for all h = 1, …, H) under H rounds of the φ = 1 kernel (uniform entrance failure).
Then
  (R-a) E_𝓒 err_r ≤ δ_𝔛 + β_H + (L+4)ρ̄ + u_π, and the same for err_prim;
  (R-b) P_𝓒(MPM̂ ≠ S₀) ≤ 2[δ_𝔛 + β_H + (L+4)ρ̄ + u_π].

*Proof.* By T23(ii-a,b), err_r ≤ B̄_r + u_π. Fix (i, h). If X_{i,0} ∈ 𝔛 and the particle enters S₀ at some terminal
round h′ ≤ H, then B_{i,h} = 1 only if its path leaves S₀ in one of the rounds h′+1, …, L+h, at most L+4 rounds,
each with conditional departure probability ρ̄ given the σ-field before that round and the particle at S₀ (T12 (R3),
as in M1(b)); the union bound gives ≤ (L+4)ρ̄. Hence E_𝓒 B_{i,h} ≤ P_𝓒(X_{i,0} ∉ 𝔛) + E_𝓒[1{X_{i,0} ∈ 𝔛}·P(no entrance
by H | X_{i,0})] + (L+4)ρ̄ ≤ P_𝓒(X_{i,0} ∉ 𝔛) + β_H + (L+4)ρ̄, using the Markov property of the terminal rounds given
the end-of-stage-T population (T12 (R3); no resampling in the terminal rounds). Average over (i, h): E_𝓒 B̄_r ≤
δ_𝔛 + β_H + (L+4)ρ̄. The primary PIP obeys the same bound as in W2-T26 §3(c). (R-b): MPM̂ ≠ S₀ forces err ≥ ½. ∎

**n-indexed form (Corollary R′).** PROVED as a composition, CONDITIONAL on its inputs. On a triangular array R1 with
OUT and (Ω) as in Theorem A, assume
- (DELIV-POP) for every x > 0, P(𝒢_n ∩ {δ_𝔛 > x}) → 0, for some sequence of 𝓒-measurable basins 𝔛_n ∋ S₀;
- (REP-ENT) for every x > 0, P(𝒢_n ∩ {β_{L_n} > x}) → 0 on the same 𝔛_n;
- (P) δ₁ → 0 in P₀-probability at a rate with L_n(B+3)u_π → 0 (T03's √(log n/n) with L_n = O(log n) suffices);
- (P-ex) as in Theorem A for the exact branch.
Then P(𝒪_n ∩ {max_j |PIP̂_j − 1{j∈S₀}| > ε}) → 0 (islandwise and primary) and P(𝒪_n ∩ {MPM̂ ≠ S₀}) → 0.
*Proof.* Theorem R on A_x = 𝒢_n ∩ {δ_𝔛 ≤ x, β_L ≤ x, (L+4)(B+3)u_π ≤ x, u_π ≤ x} gives E_𝓒 err ≤ 4x; Markov; the
rest is verbatim Theorem A's conversion (W2-T26 §3). ∎

*Where the inputs come from.*
- β_H: W1-T24G Theorem B (candidate) bounds P_x(S₀ not *scored* within H rounds) ≤ v(1−c_*)^{⌊H/v⌋} + Hη. Scoring
  is weaker than entering; the gap is closed by the acceptance step: a Gibbs step that scores S₀ as its alternative
  enters it with probability o ≥ π(S₀)/(π(S₀)+π(S₀⊕j)) ≥ 1 − u_π; a uniform-swap proposal of S₀ is accepted with
  probability 1 ∧ π(S₀)/π(S) ≥ 1 ∧ 1/u_π = 1 when u_π ≤ 1; a neighbour-swap proposal with probability ≥ 1 ∧ 1/(Bu_π)
  = 1 when u_π ≤ 1/B. So β_H ≤ [Theorem B bound] + u_π once u_π ≤ 1/B. Corollary P1 of W1-T24G (distance-one
  particles enter S₀ next round with probability ≥ a₁ ≥ 0.14 at n = 200) is the finite-n instance.
- δ_𝔛: this is the **population** version of T38(b2)'s DELIV ("at least one particle in 𝔛_n after the last
  resampling"). It is OPEN. Mechanism (CONJECTURE): once a W-particle exists at a stage t < T, the next resampling
  amplifies it by e^{Δ_{t+1}(d(W) − d(outsiders))} = e^{Θ(n)/T_e} ≫ N (Prop. NM gap, Δ_t ≥ 2^{−60} is not enough but
  the method's grid has Δ_t ≥ 1/T_e at the pilot), so the population collapses onto W (W4-SHARE Lemma PD, Prop. SH
  threshold); if the arrival is at stage T itself, only the arriving particles are in W and the rest must be in the
  repair basin already (𝔛 ⊇ Lat(S°) in the LH family, where the whole start basin is downhill to S₀ at φ = 1 by
  W4-SHARE Prop. M). So DELIV-POP ⇐ DELIV ∧ (an amplification stage remains, or 𝔛 ⊇ start basin).

*What Theorem R does not use.* Any evidence quantity; any bound on T; any ESS; the start mass π₀(S₀). It is the
masked-regime analogue of Theorem A's PIP clause with the evidence lower tail (T15) replaced by delivery + repair.
Note the price: the (L+4)ρ̄ term is back (W2-T26 Lemma 3 removed it only through T15's re-control at each round start,
which needs the evidence lower tail that the masked regime lacks). Under T03's rate it is harmless asymptotically.

### Proposition N (the negative route: evidence collapses, PIPs survive).

**(N-a) PROVED (general).** Let (data, 𝓒) be any sequence with δ₁ → 0 and liminf P_𝓒(f_{r,0} > ½) ≥ κ > 0 (the terminal
population misses S₀ with probability ≥ κ). Then
  P_𝓒(f_{r,0} > ½ ∧ W_r < √δ₁) ≥ κ − 2√δ₁ → κ:
on the non-crossing realisations the island underestimates Z by a factor ≥ δ₁^{−1/2} → ∞; under T03's rate the factor
is ≥ (n/log n)^{1/4}(1+o(1)). T31(i) still holds (P_𝓒(Z ≥ 0.05Ẑ_r) ≥ 0.95), with the true Z above the reported bound by
a factor ≥ 20δ₁^{−1/2}. If κ → 1 this holds with probability → 1. *Proof:* (M2-a). ∎

**(N-b) The reflected comparator (what W_r actually is on a non-crossing realisation). PROOF SKETCH.** If the
population stays in a set M ∌ S₀ through stages 0, …, T−1 and at each stage is approximately distributed as
q_{t−1}(·|M), then q̂_{t−1}(G_t) ≈ Z̄_t(M)/Z̄_{t−1}(M), the product telescopes, and
  W_r ≈ π(M)/π₀(M) = r_M (the comparator mean Z·r_W of `00_COMMON.md` §2) ≤ δ₁/π₀(M).
So the underestimation is by the ratio of the posterior mass to the start mass of the region the bridge actually
explored, ≈ δ₁ when the start basin M carries almost all of π₀. (N-a) is the rigorous, weaker form (√δ₁ instead of δ₁).

**(N-c) An explicit split family. PROOF SKETCH (deterministic core PROVED; family-level claims rest on candidates).**
Take the one-stage grid T = 1, φ = (0, 1) (admissible: T ≥ 1; all locked results hold for any frozen grid). Then
exactly W_r = q̂₀(e^d)/E_{π₀}[e^d] (T14(i-a)). Let M_D := {x ∈ Ω : d(x) ≤ d(S₀) − D}. On the event A := {all N initial
draws lie in M_D},
  W_r ≤ e^{−D}/π₀(S₀)    (PROVED: E_{π₀}e^d ≥ π₀(S₀)e^{d(S₀)} and q̂₀(e^d) ≤ e^{d(S₀) − D} on A),
and P_𝓒(Aᶜ) ≤ Nπ₀(Ω∖M_D). On the LH exact-Gram family of W1-EXP §4 (omission masking of c ≥ 1 hubs M; start mode
S° = S₀∖M), take M_D := {x : x ∩ M = ∅} (hub-free models) and D := d(S₀) − max_{x∩M=∅} d(x). The claim needed is
D = Θ(n): d(S₀) − d(S°) = Θ(n) (Prop. NM: the hubs' signal is visible to the full posterior and invisible to the
tables), and a hub-free x gains over S° at most the extras' O_P(log n) discrepancies each (the dilution term of
F-DRAFT Lemma W1 is already in d(S°)), so max_{hub-free} d ≤ d(S°) + O_P(K log n) — PROOF SKETCH. Then π₀(Ω∖M_D) =
π₀(some hub present) = c·p^{−1}n^{−1/2}e^{O_P(1)} (W1-T38E E1, O-BGIBBS Prop. LH), and with N = N_e = O(n + p) the
event A has probability → 1 whenever p/(√n log² n) → ∞ (the T38(b1-LH) c = 1 condition; p ≤ n − 1 on exact-Gram LH).
Hence **W_r ≤ e^{−Θ(n)}·p^{c}n^{c/2} = e^{−Θ(n)} with probability → 1**: the 95% bound is off by e^{Θ(n)}. Meanwhile the whole start basin Lat(S°) is downhill to S₀ at φ = 1 (W4-SHARE Prop. M(b), PROOF SKETCH),
so 𝔛 = Lat(S°) has δ_𝔛 ≤ 1 − π₀(Lat(S°)) → 0 by W1-EXP Thm 6 at S° (candidate), and Theorem B / Prop. LH give
β_L → 0; Theorem R then gives PIP and MPM consistency on the same family, with the same output.
*Caveat on the grid.* Whether the method's calibration produces T = 1 on such data is OPEN: the pilot's restricted
ESS (T13) is computed on the candidate set V, and if V ∌ hub-containing states the weights seen are flat and φ₁ = 1
is plausible (O-BGIBBS code fact F: φ₁ ≥ min(1, 1/T_e)), but this is not shown. With any grid, (N-a) applies as soon
as non-crossing at stage T has positive probability. The empirical instance is W4-SHARE headline 4: on the PB design,
delivery to 𝓡₀ succeeded in 200/200 islands while the median log Ẑ/Z was −67.

### Proposition W4 and the split (interpretation; no new claim).

F-DRAFT Proposition W0(ii)–(iii) and W4 (PROOF SKETCH there): 1 + χ²(π‖π₀) = 1/ρ_Ω(0,1) ≥ π(S₀)²/π₀(S₀), while
KL(π‖π₀) and TV(π,π₀) can be O_P(n^{−1/2}·polylog) at the same time (favourable BO regime). The evidence product
is a chain of importance-sampling steps whose relative error is governed by the χ²-type quantities 1/ρ_Ω(φ_{t−1},φ_t)
(T13(i); the ESS rule targets 0.9 on V, not on Ω) and, in the masked regime, by whether the population *contains* the
states carrying the mass (M1–M3): a second-moment / support property. The RB PIPs are an occupancy average over
the measured rounds: a first-moment / TV-type property of the terminal population, which a π-invariant kernel can
deliver from a start that is in TV distance 1 from π (π₀ ≈ δ_{S°}, π ≈ δ_{S₀}) as long as a downhill path exists.
In the masked regime 1 + χ²(π‖π₀) ≥ π(S₀)²/π₀(S₀) ≈ 10¹² at the study scale (median π₀(S₀) ≈ 10⁻¹², §5 of
THEORY_PRIORITIES), so one-step weight stability is impossible and the bridge must cross; M3 says that even a
crossing bridge gives no first-moment handle on Ẑ. Occupancy, by contrast, only needs the terminal rounds to move
the particles from 𝓡₂ (median π₀(𝓡₂) ≈ 0.8) to S₀, which the data say the Gibbs flips do (98% of fresh scores).

## 4. Evidence

Numerical checks were delegated to a helper (brief: `HELPER_BRIEF_SIM.md`; outputs `results/SIM_NOTES.md`,
`results/masked_sim.jsonl`, scripts in `scripts/`, adapted from W2-T26's exact-score final-run simulator at p = 18).
The checks target (I1) = (M2-e), (I2) = T23(ii-a,b) pathwise, (I3) = (M1-c), on the W2-T26 `masked` design with three
frozen grids: T = 1; the ideal full-space ESS grid; a "blind" restricted-ESS grid. See §4.1 below for what ran.

Already on record from other branches (not produced here):
- W2-T26 §4.3, §7: `masked` design, Δ_n = 1, ideal grid T = 10–20, N = 2500: |Ẑ/Z − 1| ≈ 1.4–2.1%, PIP error equal
  to the exact-posterior error (the bridge crosses at p = 18 with the full-space grid). At N = 50, 16% evidence error.
  Consistent with M1 (W_r ≈ 1 and PIPs right), not a test of the split.
- W4-SHARE headline 4 (PB design, n = 4000/16000): delivery to 𝓡₀ in 200/200 islands; median log Ẑ_r/Z = −67. This is
  (N-a)/(N-b) in the wild: occupancy without evidence.
- THEORY_PRIORITIES §5 (n = 200, p ∈ {500, 1000}, 2,400 fits): median π₀(S₀) ≲ 10⁻¹², median π₀(𝓡₂) ≈ 0.8; all
  misses posterior misses.

### 4.1 Helper simulation (Opus 5.5 helper; `results/SIM_NOTES.md`, `results/masked_sim.jsonl`, `scripts/masked_sim.py`)

Exact scores at p = 18 (B = 4, s₀ = 3), data seed 0, two masked designs (`masked`: corr(x₃,x₀) = 0.6, β₃ = −0.6;
`masked8`: corr 0.8, β₃ = −0.8, zero population covariance of x₃ with μ), n ∈ {640, 5120}, N ∈ {2500 (20 reps),
50 (40 reps)}, 4 islands per rep, three frozen grids: G1 one stage φ = (0,1); G2 the ideal full-space ESS grid
(T = 10 at n = 640, 20–21 at n = 5120); G3 a "blind" grid bisecting the ESS restricted to the states V of one pilot of
N π₀ draws (S₀ ∉ V in every setting). 24 settings, 3,840 island-runs. All seeds fixed.

**Inequalities.** (I2) = T23(ii-a,b) pathwise: max over all island-runs of err_r − (B̄_r + u_π) is −0.047 (never
positive). (I3) = (M1-c): E[W_r err_r] ≤ δ₁ + ρ̄ + u_π holds in all 24 settings; the closest is 0.069 against 0.372
(masked, n = 640, N = 50, G1). (I1) = (M2-e): the left side was identically 0, because **no island ever had f_r > ½**
(max 0.44): at p = 18 the stage-T round, which is at φ = 1, already puts 56–80% of the particles on S₀ even when
π₀(S₀) ≈ 10⁻³⁶ or 10⁻⁴⁸. So (M2-a) was not tested; it needs a design where the φ = 1 round fails to deliver.

**The split.** Selected rows (medians of log W_r; island PIP error vs exact-posterior PIP error; "split islands" :=
W_r < 0.05 and err_r < 0.10):

| design | n | N | grid | T | median log W_r | q05–q95 | mean f_r (end T) | island PIP err | exact PIP err | MPM correct | split islands |
|---|---|---|---|---|---|---|---|---|---|---|---|
| masked | 640 | 2500 | G1 | 1 | −4.32 | −4.37, +1.19 | 0.204 | 0.0391 | 0.0391 | 100% | 56/80 |
| masked | 5120 | 2500 | G1 | 1 | −5.88 | −11.7, −4.78 | 0.217 | 0.0067 | 0.0067 | 100% | 80/80 |
| masked | 5120 | 50 | G1 | 1 | −11.7 | −11.7, −11.6 | 0.257 | 0.0067 | 0.0067 | 100% | 158/160 |
| masked8 | 5120 | 2500 | G1 | 1 | −10.8 | −10.8, −10.8 | 0.256 | 0.0094 | 0.0094 | 100% | 79/80 |
| masked | 5120 | 2500 | G2 | 20 | −0.007 | −0.052, +0.039 | 0.037 | 0.0067 | 0.0067 | 100% | 0/80 |
| masked8 | 5120 | 2500 | G2 | 21 | −0.002 | −0.032, +0.048 | 0.049 | 0.0094 | 0.0094 | 100% | 0/80 |
| masked | 5120 | 2500 | G3 | 10 | −5.13 | −5.29, −4.56 | 0.142 | 0.0067 | 0.0067 | 100% | 76/80 |
| masked8 | 5120 | 2500 | G3 | 1 | −10.8 | −10.8, −10.8 | 0.256 | 0.0094 | 0.0094 | 100% | 80/80 |
| masked8 | 5120 | 50 | G3 | 1 | −10.8 | −10.8, −10.7 | 0.262 | 0.0094 | 0.0094 | 100% | 160/160 |

Readings.
- **One-stage grid (G1):** the evidence collapses by e^{4}–e^{12} (N-c's mechanism: W_r = q̂₀(e^d)/E_{π₀}e^d with no
  S₀-basin draw), while the island PIP error equals the exact posterior's to four digits and the MPM is always right.
  The repair is done by the single stage-T round at φ = 1 plus the L terminal rounds (Theorem R with 𝔛 = the start
  basin, β small; W1-T24G's measured per-round progress).
- **Blind restricted-ESS grid (G3):** at n = 5120 the pilot set V (3–29 states, never containing S₀) makes the
  restricted ESS rule either jump straight to φ = 1 (T = 1, masked8) or stop at T = 10 instead of 20 (masked), and
  the evidence collapses as under G1 (median log W_r −5.1 to −10.8) with exact PIPs. This is the T13(iii) blindness
  that (N-c)'s caveat asked about, realised at p = 18 with a one-pilot proxy of the method's candidate set. At
  n = 640, G3 ≈ G2 (log W_r ≈ 0).
- **Full-space grid (G2):** no collapse (|median log W_r| < 0.03 at N = 2500), as in W2-T26 §7.
- **Unbiasedness is carried by rare islands:** in collapsed settings the top 5% of islands hold 99–100% of ΣW_r; in
  masked8 n = 5120 N = 50 none of 160 islands carried it (mean W_r = 2·10⁻⁵). This is M3 in action: E W_r = 1 while
  the typical W_r is e^{−11}.
- The 95% lower bound 0.05Ẑ_r is valid in every run and off by a factor ≈ 20·e^{5…11} in the collapsed settings.

What the simulation does **not** show: a non-crossing population at the end of stage T (hence no test of (M2-a)),
and nothing about p ≫ n or about the method's actual calibration (G3 is a proxy with one pilot of size N).

## 5. What fails and why

- **Evidence restart conditioned on crossing.** False in mean (M3): E[W_r | C] ≥ (1−2δ₁)/P(C). The unbiasedness
  identity forces all the evidence mass onto the crossing realisations. A conditional relative-error statement needs
  P(W_r < c | C) → 0, which no first-moment identity gives; the abstract instance in M3 satisfies every identity and
  has W_r = c < 1 on all of C. Route: PW2 → T25(iv) (second moment), or report the islands' log-spread as a
  diagnostic knowing T12(iv.e)'s caveat.
- **T15 for late delivery.** T15(i) with 𝔄 = 𝔛 gives E f^𝔛 ≤ π(𝔛ᶜ)/c + P(W_r < c); in the masked regime P(W_r < c) ≈ 1
  on non-crossing (N-a), so it is vacuous. Occupancy of the repair basin must come from the bridge dynamics
  (W4-SHARE D4/D5, O-BGIBBS BG1), not from the evidence.
- **Removing (L+4)ρ̄ in Theorem R.** W2-T26 Lemma 3 re-controls occupancy at every round start through T15, i.e.
  through the evidence lower tail. Without it one pays departure over all terminal rounds after entrance. Under
  T03's rate this is o(1); at n = 200 it is the dominant term of the bound (W2-T26 §4.1: (L+4)ρ* ≈ 10–13 at
  n ≤ 640 even in favourable designs).
- **Making the T = 1 family the method's own.** The calibration's grid is not controlled by any locked result;
  (N-c) is stated for a frozen grid. (N-a) is grid-free.

## 6. Needs escalation

1. **M1(b)'s conditional step** E_𝓒[D_{i,h} | H] = ρ̄ on {X_{i,L+h−1} = S₀}: I use T12's (R3) exactly as W2-T26 Lemma 3
   does; an independent check that W_r's H-measurability is all that is needed (it is: Ẑ_r is a function of the
   stage-0..T populations) would close M1 as a locked-level composition.
2. **ρ̄ ≤ (B+3)u_π** is W2-T26 Lemma 2 (candidate). M1–M3 and Theorem R hold with ρ̄ defined directly; the bound only
   converts it to a posterior quantity.
3. **Theorem R's "entrance" vs Theorem B's "scored".** The acceptance argument (β_H ≤ Theorem-B bound + u_π for
   u_π ≤ 1/B) is elementary but should be written against the method's exact Hastings factor for neighbour swaps.
4. **DELIV-POP** (population delivery) is the one genuinely open input for masked-regime PIP consistency; it is
   strictly stronger than T38's DELIV. The amplification mechanism (one resampling after arrival collapses the
   population onto W) deserves a lemma of its own (W4-SHARE's branching envelope is the right tool).
5. **(N-c) family-level claims** rest on W1-EXP Thm 6, O-BGIBBS Prop. LH and W4-SHARE Prop. M(b), all candidates.

## 7. What the paper can and cannot claim about the reported Ẑ and PIPs at n = 200

**Can claim (regime-free, locked or candidate-composition of locked results).**
1. E_𝓒 Ẑ = Z, E_𝓒 log Ẑ ≤ log Z, and 0.05Ẑ is a 95% lower bound on Z, not conditional on completion or flags
   (T12(iii), T31(i)). In the masked regime the bound is valid and expected to be loose by a factor that can be
   astronomically large (N-a, N-c); the paper should say so.
2. Pathwise: on every island, max_j|PIP̂_rj − 1{j∈S₀}| ≤ (fraction of measured paths that leave S₀) + u_π (T23(ii)).
   The PIPs are exactly as good as the terminal occupancy of the truth; nothing about the bridge or the evidence
   enters. (The analogous fraction relative to the reported Ŝ is observable and could be reported as a diagnostic;
   this is a reporting suggestion, not a theorem.)
3. Coupling (M1–M2): an island whose evidence is within a factor c of Z has PIP error ≤ ε except with probability
   (δ₁+ρ̄+u_π)/(cε); an island whose terminal population misses S₀ reports Ẑ_r ≤ √δ₁ Z except with probability 2√δ₁.
   So wrong PIPs and accurate evidence cannot coexist, while accurate PIPs with collapsed evidence can and do.
4. Under delivery + repair (the inputs T38(b2) already needs, in population form) and T03, the PIPs and the MPM are
   consistent in the masked regime with no evidence condition (Theorem R, Corollary R′).

**Cannot claim.**
1. Ẑ/Z → 1, or any relative accuracy of Ẑ, in the masked regime: false on non-crossing realisations (N-a), and not
   derivable from first moments even on crossing ones (M3). The E2 flag (island log-spread ≤ 1 nat) is a diagnostic
   whose conditioning breaks the identities (T12(iv.e)); four islands that all fail to cross agree with each other.
2. PIP accuracy from the evidence identity: E[Ẑ_r PIP̂_rj] = Z·PIP_j (T12(ii)) is a product identity; the normalised
   PIP is biased (T12(iv.b)) and in the masked regime the bias can be the whole signal.
3. Any finite-n rate at n = 200. With median π₀(𝓡₂) ≈ 0.8, Theorem R's bound is ≥ 0.2 before the repair and
   departure terms; it explains the mechanism, not the study's numbers. (The study's misses being posterior misses
   is consistent with Theorem R: occupancy of the posterior mode is what the PIPs report, and the posterior mode is
   wrong there.)

## 8. Outside scope

- **A self-diagnostic the method could emit at no cost:** the fraction of measured (particle, round) paths that
  leave the reported MPM̂ (or Ŝ). By T23(ii-a) it bounds the PIP error against the reported model's indicator; by
  M2 it is small whenever the evidence is trustworthy. Method change: reporting only; not pursued.
- **Secondary PIP.** FROZEN_LIST drops it. M2(c) shows it is the one for which the evidence–PIP coupling is cleanest
  (weights W_r are exactly the coupling weights). Not pursued.
- **ρ̄'s exact form** 1 − ∏_e(1 − k_e) (W2-T26 §7) makes the (L+4)ρ̄ term of Theorem R 4–8× smaller than with ρ*.

## 9. Confidence cards

| Item | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| M1 (evidence-weighted PIP bound) | E_𝓒[W_r err_r] ≤ δ₁ + ρ̄ + u_π, every regime and grid | high | PROVED here (composition of locked T12(i.b), T23(ii), W2-T26 Lemmas 2–3) | the conditional step via T12 (R3) | no |
| M2 (dichotomies) | non-crossing ⇒ W_r ≤ √δ₁ w.p. ≥ 1−2√δ₁; W_r ≥ c ⇒ PIPs accurate w.p. ≥ 1 − (δ₁+ρ̄+u_π)/(cε); pooled/secondary analogue | high | PROVED here (Markov on M1) | none | no |
| M3 (no conditional evidence theorem) | E[W_r | C] ≥ (1−2δ₁)/P(C); first moments cannot bound P(W_r < c | C) | high | PROVED here | none; a positive result needs PW2 | no |
| Theorem R / R′ (masked PIP restart) | E err ≤ δ_𝔛 + β_H + (L+4)ρ̄ + u_π; consistency under DELIV-POP, REP-ENT, T03 | high (bound); medium (inputs hold on LH-type families) | bound PROVED; DELIV-POP OPEN (medium cost: amplification lemma via W4-SHARE D4); REP from W1-T24G (candidate) | population delivery, not one-particle delivery | no |
| N-a (evidence collapse on non-crossing) | factor ≥ δ₁^{−1/2} underestimation on non-crossing, w.p. → κ | high | PROVED here | none | no |
| N-c (explicit split family) | LH-type masking, T = 1 grid: W_r ≤ e^{−Θ(n)} w.p. → 1 while PIPs consistent | medium-high for a frozen grid; low-medium that the method's calibration realises T = 1 | deterministic core PROVED; family claims need W1-EXP Thm 6, O-BGIBBS LH, W4-SHARE M(b) | whether the restricted-ESS grid is blind to the crossing (T13(iii)) | no |
| Paper claim at n = 200 | §7 lists 4 claimable and 3 non-claimable statements | high | — | — | optional diagnostic (§8) |
