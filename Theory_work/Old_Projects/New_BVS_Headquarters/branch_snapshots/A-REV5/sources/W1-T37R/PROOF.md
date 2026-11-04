# W1-T37R — PROOF.md (long proofs and sketches)

Notation: 00_COMMON.md. Throughout, EX-A (exact scores and comparisons), X and S₀ fixed, s₀ ≥ 1.
Neighbourhood N(S) = all *feasible* flips and swaps of S (additions only if |S| < K). The production local
search (METHODOLOGY_v3 §6.10; engine `v3_core.cpp`, `E.local_search(led.hpmS, ell, …)`) is the map

  M(S) = argmax{F(S′) : S′ ∈ N(S), F(S′) > F(S)} (lexicographic tie rule on S′), M(S) = ⊥ if the set is empty,

iterated at most ℓ times from the centre S_c = the current global best scored model, followed by one scan.
For S ∈ Ω write m(S) = |S₀∖S| (missing truths), e(S) = |S∖S₀| (extras), Φ(S) = m(S) + e(S) = |S Δ S₀|.
Region R_{a,d} := {S ∈ R_d : m(S) ≤ a} (so R_d = R_{s₀,d}). Move classes, by the change (Δm, Δe):

| class | moves | (Δm, Δe) | ΔΦ |
|---|---|---|---|
| progress 𝒫 | add truth; delete extra; swap extra→truth | (−1,0), (0,−1), (−1,−1) | −1, −1, −2 |
| neutral 𝒩 | swap truth→truth; swap null→null | (0,0) | 0 |
| regressive ℛ | add null; delete truth; swap truth→null | (0,+1), (+1,0), (+1,+1) | +1, +1, +2 |

---------------------------------------------------------------------------------------------------------

## Lemma 0 (monotonicity obstruction; Ŝ after a certified repair). Status: PROVED.

**Statement.** Let S_c be the local-search centre and S_c = S⁰, S¹, …, S^r its path. Then
(a) F(S⁰) < F(S¹) < … < F(S^r); in particular S₀ ∈ {S¹,…,S^r} implies F(S₀) > F(S_c).
(b) In production S_c is the running global best over the pre-search scored set 𝒮_pre. Hence the local search
can make S₀ a centre, or make Ŝ = S₀ (up to exact ties), only on the event E_LS := {S₀ ∉ 𝒮_pre, F(S₀) >
max_{𝒮_pre} F}. On the complement — in particular on every posterior miss F(S₀) ≤ F(Ŝ) — no local search,
with any move cap, delivers S₀ (it may still *score* S₀ as a scanned neighbour, which changes nothing in Ŝ).
(c) If the path reaches S₀ and the search stops there with local_certified (S₀ is the returned scanned centre with
no improving neighbour), then every model scored during the search has F ≤ F(S₀), and Ŝ = S₀ after the
search, except for exact score ties (then the tie rule decides). No condition π(S₀) > ½ is needed.

**Proof.** (a) M(S) is defined only among S′ with F(S′) > F(S). (b) The engine starts from `led.hpmS`, the
argmax of F over 𝒮_pre (tie rule). If F(S₀) ≤ F(S_c) = max_{𝒮_pre} F and S₀ ≠ S_c, (a) excludes S₀
from the path; and Ŝ after the search is the argmax over 𝒮_pre ∪ (scanned models), which contains S_c with
F(S_c) ≥ F(S₀), so Ŝ ≠ S₀ except by an exact tie won by S₀ under the tie rule. If S₀ ∈ 𝒮_pre and F(S₀) >
max_{𝒮_pre∖S₀} F then S_c = S₀ already (nothing to repair). (c) Every model scored during the scan at S^i has F ≤ F(S^{i+1})
(the best-move rule takes the maximum of the scanned improvements; non-improving scanned models have
F ≤ F(S^i)). Chaining with (a), every model scored in scans before the last has F ≤ F(S^r) = F(S₀). The final
scan at S₀ finds no improvement, so all models it scores have F ≤ F(S₀). Models in 𝒮_pre have F ≤ F(S_c) <
F(S₀) by (a). Hence F(S₀) = max over the post-search scored set; Ŝ = S₀ unless a different model has exactly
equal score and wins the tie rule. ∎

**Remarks.** (i) The final local search is the last scoring event of a fit (M §6, "final local search; final
checks (flags only)"), so (c) gives Ŝ = S₀ at the end of the fit. (ii) Reading of the preliminary data: a centre
in R₂∖S₀ that is not repaired while the fit ends as a posterior miss (F(S₀) ≤ F(Ŝ)) is exactly what (b)
predicts; the 0/541 repair count is *forced by monotonicity* and carries no information about truth
dominance. (iii) Any repair theorem for this search implies posterior dominance over the states from which it
repairs: if every greedy path from 𝓡 reaches S₀ then F(S₀) > F(S) for all S ∈ 𝓡∖{S₀} (PD(𝓡)).

---------------------------------------------------------------------------------------------------------

## Proposition 1 (literal TD is unsatisfiable for d ≥ 1). Status: PROVED.

**Statement.** Let s₀ ≥ 1, d ≥ 1, s₀ + 1 ≤ K, p > s₀, m ≥ 0. Then TD(d, m) of the current T37 file holds only if
m = 0 and F(S₀ + l) = F(S₀) for every null l ∉ S₀. In particular TD(d, 0) *strict* never holds, TD(d, m) never
holds for m > 0, and under G (with no null column in span(X_{S₀}) — implied by SE) P₀(TD(d, 0) holds) = 0.
Consequently T37(i) is vacuous for d ≥ 1 and T37(iii) is false for every d ≥ 1 (on every design).

**Proof.** Fix j ∈ S₀ and a null l. Put S := (S₀ − j) + l. Then S ∈ R_d (U = S₀ − j, P = {l}, |P| = 1 ≤ d),
|S| = s₀ ≤ K, S ⊉ S₀ and S₀∖S = {j}. Both "add j" (S → S₀ + l, size s₀ + 1 ≤ K) and "swap l→j" (S → S₀)
are feasible moves at S. TD(1) at S names the only missing truth j and requires
  g(S, j) ≥ m + [F(S₀) − F(S)], i.e. F(S₀ + l) − F(S) ≥ m + F(S₀) − F(S), i.e. F(S₀ + l) − F(S₀) ≥ m.
TD(3) at S₀ applied to the feasible move "add l" requires F(S₀ + l) − F(S₀) ≤ −m. Together m ≤ −m, so m = 0
and F(S₀ + l) = F(S₀). Strict TD(·,0) requires strict versions of both inequalities: contradiction. For the
probability statement: by T01 (contrast reduction) F(S₀ + l) − F(S₀) = c_l − ν log[(2b₀ + Q_{S₀+l})/(2b₀ +
Q_{S₀})] with a constant c_l and Q_{S₀+l} < Q_{S₀} whenever u_{S₀,l}ᵀy ≠ 0; the set {y : F(S₀ + l) = F(S₀)} is
the zero set of a non-constant real-analytic function of y (it is non-constant because Q_{S₀} − Q_{S₀+l} is a
non-degenerate quadratic form in the component of y along u_{S₀,l} ≠ 0), hence Lebesgue-null. ∎

**The swap identity behind it (PROVED, one line).** For i ∈ S, j ∉ S with S − i + j feasible,
  F(S − i + j) − F(S) = g(S, j) + h(S + j, i) = h(S, i) + g(S − i, j)                                         (SW)
(telescoping through S + j, resp. S − i; both intermediate states are evaluated only as numbers, feasibility of
S + j is not needed for the identity). So the swap "i out, j in" beats the addition of j iff h(S + j, i) > 0,
i.e. iff i is *deletable after j enters*. Literal TD(1) asks every extra to be non-deletable after the missing
truth enters, while TD(2)/(3) ask extras to be deletable once S₀ is covered. At S = S₀ − j + l these are the
same comparison with opposite signs. This is the exact content of decision D18, and it is not "generic
failure": it is failure on every design and every y (up to the null tie set).

---------------------------------------------------------------------------------------------------------

## Definitions for the refined statement

For a finite family 𝓡 ∋ S₀ of feasible models:

* **TD′_∞(𝓡)** (no spurious local maximum + closure):
  (L) M(S₀) = ⊥ (S₀ has no strictly improving feasible flip or swap);
  (N) for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) ∈ 𝓡.
* **TD′_P(𝓡)** (progress): (L), and for every S ∈ 𝓡∖{S₀}: M(S) ≠ ⊥ and M(S) is a progress move
  (equivalently Φ(M(S)) < Φ(S); by the class table ΔΦ < 0 exactly on 𝒫).
* **TD′_path(S_c)**: the capped production search from the centre S_c returns S₀ with local_certified.
* **D_S** (one-state progress event), S ∈ Ω∖{S₀}: max_{S′∈𝒫(S)} F(S′) > max{F(S), max_{S″∈𝒩(S)∪ℛ(S)} F(S″)},
  where 𝒫(S), 𝒩(S), ℛ(S) are the feasible progress/neutral/regressive neighbours of S.
  (TD′_P(𝓡) ⟺ (L) ∧ ⋂_{S∈𝓡∖S₀} D_S, ties among top progress moves allowed.)
* **Lattice of a centre.** For S = U ∪ P (U ⊆ S₀, P ∩ S₀ = ∅): Lat(S) := {U′ ∪ P′ : U ⊆ U′ ⊆ S₀, P′ ⊆ P},
  |Lat(S)| = 2^{Φ(S)}. For a class 𝒞: Lat(𝒞) = ⋃_{S∈𝒞} Lat(S). R_{a,d} is a union of lattices.
* **NA_d** (no addable null over the superset tree): for all P′ ⊆ S₀ᶜ with |P′| ≤ d and |S₀ ∪ P′| < K and all
  nulls l ∉ S₀ ∪ P′: F(S₀ ∪ P′ ∪ {l}) < F(S₀ ∪ P′).
* **TL_d** (truths locked once covered): for all P′ with |P′| ≤ d, every feasible move from S₀ ∪ P′ that removes a
  truth (deletion of a truth or swap with a truth going out) has strictly negative gain.

## Lemma 2 (lattice closure; superset reduction). Status: PROVED.

(a) Progress moves map Lat(S) into Lat(S); R_{a,d} is closed under progress moves; Φ ≤ m(S) + e(S) on Lat(S).
(b) On NA_d ∩ TL_d: M(S₀) = ⊥, and for every S = S₀ ∪ P with 1 ≤ |P| ≤ d, M(S) is the deletion of an extra
(so D_S holds and M(S) ∈ R_{0,d}).

**Proof.** (a) S′ = U′ ∪ P′ ∈ Lat(S). Add truth j ∈ S₀∖U′: U′+j ⊇ U, ⊆ S₀. Delete extra l ∈ P′: P′−l ⊆ P.
Swap extra l → truth j: both. Membership in R_{a,d}: m and e do not increase and |S′| ≤ s₀ + d ≤ K.
(b) At S₀: an addition is a null addition, gain < 0 by NA_d with P′ = ∅; any deletion or swap removes a truth
(S₀ contains only truths), gain < 0 by TL_d. So M(S₀) = ⊥. At S = S₀ ∪ P, e = |P| ≥ 1: for l ∈ P, with
P′ = P − l (|P′| = e − 1 ≤ d − 1, |S₀ ∪ P′| = s₀ + e − 1 < K), NA_d gives F(S) < F(S − l), i.e. h(S, l) > 0. A
null addition l′ ∉ S (if |S| < K) has g(S, l′) < 0 by NA_d with P′ = P. A null→null swap l → l′ has gain
h(S, l) + g(S − l, l′) < h(S, l) by (SW) and NA_d at P − l. Truth-removing moves have negative gain (TL_d).
Hence the best gain is max_{l∈P} h(S, l) > 0, attained only by extra deletions; the lexicographic rule picks one of
them. ∎

## Lemma 3 (best truth addition under SE). Status: PROVED.

If S ⊉ S₀, M := S₀∖S, and λ_min(R_{S∪S₀}) ≥ φ₀², then max_{j∈M} δ²_{S,j} ≥ (n−1) φ₀⁴ ‖θ*_M‖²/|M| ≥ (n−1)φ₀⁴ θ²_min,
and adding the maximiser reduces Δ_S by exactly δ²_{S,j}/(n−1).

**Proof.** Let r_j = (I − P_S)x_j. Then (I − P_S)μ = Σ_{j∈M} θ*_j r_j, so (n−1)Δ_S = Σ_j θ*_j ⟨r_j, (I−P_S)μ⟩ ≤
‖θ*_M‖₁ max_j |⟨r_j, (I−P_S)μ⟩|. Since δ_{S,j} = ⟨r_j, μ⟩/‖r_j‖ = ⟨r_j,(I−P_S)μ⟩/‖r_j‖ and ‖r_j‖² ≤ ‖x_j‖² = n−1,
max_j |δ_{S,j}| ≥ (n−1)Δ_S/(‖θ*_M‖₁ √(n−1)). Also (n−1)Δ_S = θ*_Mᵀ[X_Mᵀ(I−P_S)X_M]θ*_M, and the bracket is the
Schur complement of G_S in G_{S∪M}, whose smallest eigenvalue is ≥ λ_min(G_{S∪M}) ≥ (n−1)φ₀². Hence
max_j δ²_{S,j} ≥ (n−1)²φ₀⁴‖θ*_M‖⁴/(‖θ*_M‖₁²(n−1)) ≥ (n−1)φ₀⁴‖θ*_M‖²/|M| by Cauchy–Schwarz. Finally
‖(I−P_{S+j})μ‖² = ‖(I−P_S)μ‖² − (u_{S,j}ᵀμ)² (Gram–Schmidt). ∎

---------------------------------------------------------------------------------------------------------

## Theorem A (refined T37(i): deterministic greedy repair). Status: PROVED.

Assume EX-A; X, y fixed; ℓ the production move cap.
(A1) *Characterisation.* TD′_∞(𝓡) holds iff for every S ∈ 𝓡 the uncapped greedy path from S stays in 𝓡 and
terminates at S₀. Under TD′_∞(𝓡) the path from S has at most r_𝓡(S) := #{S′ ∈ 𝓡 : F(S′) > F(S)} moves.
(A2) *Progress version.* Under TD′_P(R_{a,d}), from every S ∈ R_{a,d} the greedy path stays in Lat(S) ⊆ R_{a,d},
Φ strictly decreases at each move, and S₀ is reached after τ(S) = m(S) + e(S) − σ(S) ≤ Φ(S) moves, where σ(S) is
the number of extra→truth swaps used (τ(S) ≥ max{m(S), e(S)}).
(A3) *Production search.* If TD′_P(R_{a,d}) holds and ℓ ≥ a + d (or merely ℓ ≥ τ(S_c)), then from any centre
S_c ∈ R_{a,d} the production local search returns S₀ with local_certified, without local_limit, and after it
Ŝ = S₀ up to exact ties (Lemma 0(c)). The same holds with TD′_P(R_{a,d}) replaced by the *lattice* condition
(L) ∧ ⋂_{S′∈Lat(S_c)∖S₀} D_{S′}, which involves 2^{Φ(S_c)} states only.
(A4) *Necessity.* Each of the conclusions implies PD on the respective set (F(S₀) > F(S) for S ≠ S₀ in 𝓡,
resp. in Lat(S_c) along the path); the conclusion of (A1) for all S ∈ 𝓡 implies TD′_∞(𝓡); the conclusion
"every greedy path from R_{a,d} decreases Φ at each step and ends at S₀" implies TD′_P(R_{a,d}).
(A5) *Relation to literal TD.* Literal TD(d,0) strict ⇒ TD′_P(R_d); for d ≥ 1 the premise is never satisfied
(Prop 1), for d = 0 it is satisfiable. TD′_P(R_{a,d}) ⇒ TD′_∞(R_{a,d}); the converse fails (Exp 3).

**Proof.** (A1, ⇐) Take S ∈ 𝓡∖{S₀}; its path terminates at S₀ ≠ S, so M(S) ≠ ⊥ and M(S), the second state of
the path, lies in 𝓡: (N). The path from S₀ terminates at S₀; by strict monotonicity (Lemma 0(a)) it cannot leave
and return, so it is the trivial path and M(S₀) = ⊥: (L). (⇒) By (N) and induction every state of the path from
S lies in 𝓡. F strictly increases along the path, so its states are distinct and each S′ ≠ S on it has F(S′) >
F(S): length ≤ r_𝓡(S) < ∞. The path terminates at some T ∈ 𝓡 with M(T) = ⊥; by (N) T = S₀.
(A2) By Lemma 2(a) progress moves preserve Lat(S); Φ is a non-negative integer that drops by 1 (add truth, delete
extra) or 2 (extra→truth swap) per move, so the path cannot be longer than Φ(S); it terminates at a state with
M = ⊥ in R_{a,d}, which by TD′_P is S₀ (every other state has M ≠ ⊥). Counting: the m(S) truths enter and the
e(S) extras leave, one or two per move, giving τ = m + e − σ; each move fixes at most one truth and at most one
extra, so τ ≥ max(m, e).
(A3) The production search performs the greedy moves while a scan finds an improvement and the count is < ℓ, then
one further scan. With τ(S_c) ≤ Φ(S_c) ≤ a + d ≤ ℓ moves the centre is S₀ after τ moves; the next scan (inside the
loop or the final one) finds no improvement by (L), so the search stops with S₀ as a scanned centre with no
improving neighbour, i.e. local_certified, and local_limit is not set. Ŝ = S₀ by Lemma 0(c). For the lattice
version the same argument runs inside Lat(S_c), which is closed under progress moves (Lemma 2(a)).
(A4) PD: by Lemma 0(a) along each path. The other two are restatements of (A1, ⇐) and of the definition.
(A5) TD(1) makes an addition of a missing truth the best move (progress), TD(2) a deletion of an extra (progress),
TD(3) is (L); so literal TD(d,0) strict ⇒ TD′_P(R_d). TD′_P ⇒ TD′_∞ since progress moves stay in R_{a,d}. Exp 3
exhibits TD′_∞ without TD′_P. ∎

**What is "weakest".** Within statements of the form "for every centre in 𝓡 the search ends certified at S₀",
TD′_∞(𝓡) (with move bound r_𝓡) is necessary and sufficient (A1); within statements that also keep the move count
≤ Φ — the only form compatible with a cap ℓ that does not depend on 𝓡's geometry — TD′_P is necessary and
sufficient. The single-centre condition TD′_path(S_c) is weaker still but is the event itself; the lattice
condition of (A3) is the weakest *checkable* sufficient condition for a given centre that does not require
simulating the path. All of them imply PD (Lemma 0), which is where the n = 200 data fail (§5 of REPORT).

---------------------------------------------------------------------------------------------------------

## Theorem B (refined T37(ii): finite-n bound, lattice/path-wise). Status: PROVED (inclusions and union bound);
the description of the single events is a PROOF SKETCH.

Assume EX-A, G, fixed X. Let 𝒞 ⊆ R_{a,d} be any data-independent class of centres, ℓ ≥ max_{S∈𝒞} Φ(S).
Then
  P(production search from S_c fails to return S₀ certified)
    ≤ P(S_c ∉ 𝒞) + P₀(NA_d^c) + P₀(TL_d^c) + Σ_{S ∈ Lat(𝒞), m(S) ≥ 1} P₀(D_S^c),                      (B1)
and, for any data-independent designated progress move π(S) ∈ 𝒫(S),
  P₀(D_S^c) ≤ P₀(F(π(S)) ≤ F(S)) + Σ_{S″ ∈ 𝒩(S)∪ℛ(S)} P₀(F(π(S)) ≤ F(S″)).                                 (B2)
Counting: |{S ∈ R_{a,d}: m(S) ≥ 1}| = Σ_{i=1}^{a} C(s₀,i) Σ_{e≤d} C(p−s₀, e) ≤ (2s₀)^a (p+1)^d (no 2^{s₀}
unless a = s₀); per state |𝒩∪ℛ| ≤ p + s(p − s) ≤ (K+1)p; for a single centre |Lat(S_c)| = 2^{Φ(S_c)}.
NA_d is a union of ≤ Σ_{e≤d} C(p−s₀,e)(p−s₀−e) one-dimensional pure-noise events; TL_d of ≤ Σ_{e≤d} C(p−s₀,e)·s₀p
events with non-centrality ≥ (n−1)φ₀²θ²_min/σ*² (Lemma 3-type bound, SE).

**Proof.** If S_c ∈ 𝒞 and all events NA_d, TL_d, D_S (S ∈ Lat(S_c), m(S) ≥ 1) hold, then (L) holds and D_S holds on
all of Lat(S_c)∖{S₀} (superset states by Lemma 2(b), the rest by assumption); Theorem A(A3), lattice version, gives
the conclusion. Take complements and a union bound over Lat(𝒞) ⊇ Lat(S_c) — legitimate although S_c depends on
ε, since the union is over a data-independent family. (B2): D_S fails only if the designated π(S) does not beat S
and every non-progress neighbour. Counting is elementary. *Sketch for single events:* by T01, F(A) − F(B) is a
smooth function of the vector (Wᵀy, ‖(I − P_{A∪B})y‖²) with W an orthonormal basis of col X_{A∪B} ⊖ col X_{A∩B}
(dim ≤ |A Δ B| ≤ 4 for two neighbours of S), up to the O(1/n) ridge correction in H_S; Wᵀy is Gaussian with mean
Wᵀμ, so each event is a ≤ 4-dimensional non-central Gaussian event conditional on an independent residual
χ² (exactly, when μ ∈ col X_{A∪B}).

## Theorem C (refined T37(iii): asymptotics). Status: PROOF SKETCH (C1–C2); COUNTEREXAMPLE (C3); CONJECTURE (C4).

Regime R1 with G, R, SE, BM-∞; a, d fixed (so ℓ_n ≥ a + d for all large n; ℓ = 10 at n = 200, p = 500).
Additional named hypotheses:
* **PGD(η) on R_{a,d}** (population greedy dominance), fixed η ∈ (0,1]: for every S ∈ R_{a,d} with m(S) ≥ 1,
  R⁰(S) ≤ (1 − η)R⁺(S), where R⁺(S) = Δ_S − min_{S′∈𝒫(S)} Δ_{S′}, R⁰(S) = Δ_S − min_{S″∈𝒩(S)∪ℛ(S)} Δ_{S″}.
* **LD(d)** (local dependence of nulls): there are B′ and κ_n with κ_n log p → 0 such that for every P′ ⊆ S₀ᶜ,
  |P′| ≤ d, all but at most B′|P′| nulls l satisfy ρ²(l, P′ | S₀) ≤ κ_n (squared partial multiple correlation of x_l
  with X_{P′} given X_{S₀}). (COH implies LD(d) with B′ = 0.)

(C1) TL_d holds with probability → 1 (SE, BM-∞). NA_d holds with probability → 1 under LD(d); without LD the
union bound gives P(NA_d^c) ≲ Σ_{e≤d} p^{e}(s₀+e)n^{−1/2}(log n)^{−1/2}, which → 0 only if p^d = o(√(n log n)).
(C2) Under PGD(η): Σ_{S∈R_{a,d}, m≥1} P₀(D_S^c) → 0. Hence P₀(TD′_P(R_{a,d})) → 1 and, by Theorem A, from every
centre in R_{a,d} the production search returns S₀ certified, w.p. → 1.
(C3) PGD is not implied by SE + BM-∞: combination look-alike design (Exp 3) — TD′_P(R_{2,1}) fails w.p. → 1.
(C4) CONJECTURE: under SE + BM-∞ + LD(d + d₁), TD′_∞(R_{a,d+d₁}) holds w.p. → 1 for a design-dependent d₁ (number
of regressive null additions possible on population greedy paths), with move bound ≤ a + d + 2d₁.

**Sketch of (C1).** TL: removing truth k from T ⊇ S₀ loses (n/2)log(1 + θ_k²‖(I − P_{T−k})x_k‖²/(n v) + noise)
≥ c n φ₀² θ²_min/σ*² − O_P(√(n θ² log p)) ≫ log n + log p (BM-∞), uniformly over the ≤ p^d s₀ (p+1) moves by a
Gaussian maximal inequality. NA: with T = S₀ ∪ P′, g(T, l) ≥ 0 iff (up to O(1/n)) Z²_{T,l} ≥ c_k := log(n+1) +
2 log((2p−k)/(k+1)) + o(1), Z_{T,l} = u_{T,l}ᵀε/σ̂. For l with ρ²(l,P′|S₀) ≤ κ_n, the decomposition
(I − P_T)x_l = (I − P_{S₀})x_l − P_Ṽ(I − P_{S₀})x_l (Ṽ = (I−P_{S₀})X_{P′}) gives |Z_{T,l}| ≤ (1−κ_n)^{−1/2}
(|Z_{S₀,l}| + √κ_n ‖P_Ṽ ε‖/σ) and ‖P_Ṽε‖²/σ² ≤ 2d(1+ε)log p uniformly; with κ_n log p → 0 these events are
contained in {max_l Z²_{S₀,l} ≥ c_{s₀}(1 − o(1/log p))}, of probability ≲ p·e^{−c/2}/√c ≍ s₀/√(n log n) → 0. The
≤ B′|P′| exceptional l per P′ depend (through Z_{T,l}) only on P′ ∩ (their correlated neighbours), so the number of
distinct exceptional events is ≤ p·Σ_{e≤d}C(B′d, e), each of probability ≲ (s₀/p)n^{−1/2}: total → 0.
*Gap:* the reduction "depends only on P′ ∩ neighbours" needs the same perturbation bound applied to the
non-neighbour part — routine but not written out.
**Sketch of (C2).** For neighbours S′, S″ of S, ν log(Q_{S″}/Q_{S′}) = (n/2)[log v_{S″} − log v_{S′}] + N + O(log n),
where the noise term N has the form 2μᵀ(P_{S′} − P_{S″})ε/v + O(‖(P_{S′} − P_{S″})ε‖²/v), whose standard deviation is
≤ C σ*√(n (|Δ_{S′} − Δ_S| + |Δ_{S″} − Δ_S|)) ≤ Cσ*√(n R⁺(S)). By PGD the population part is ≥ (n/2)ηR⁺(S)/v_max
≥ c η n φ₀⁴ θ²_min (Lemma 3), which under BM-∞ is ≥ c′η M_n log n → ∞ faster than log n + log p and dominates
the noise √(nR⁺ log(p^{a+d+2})) uniformly over the ≤ (2s₀)^a p^{d+1}(K+1) comparisons. *Gaps:* the uniform
linearisation of ν log Q around (n−1)v_T including the ridge term (T01 material), and v_max ≤ σ*² + M (R).
**(C3).** See Exp 3 / REPORT §4: x₃ = a(x₁+x₂)/√2 + √(1−a²)z, a = 0.85, truths x₁, x₂ ⊥, θ₁ = θ₂. λ_min(R_{123}) = 1 − a
= 0.15 (SE holds); δ²_{∅,3} = 2a²θ²(n−1) > δ²_{∅,j} = θ²(n−1) for j = 1, 2; the first greedy move from ∅ is "add x₃"
in 200/200 draws at n = 3000; the uncapped path ∅ → {3} → {1,3} → {1,2} (swap 3→2) still reaches S₀ in 3 > Φ = 2
moves (TD′_∞ holds, TD′_P fails).
