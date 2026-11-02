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
