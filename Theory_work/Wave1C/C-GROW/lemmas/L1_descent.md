# L1 — Deterministic descent on a superset lattice (claim (C1))

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high, reviews/R03_L0L1L2_check_sol.md): VERIFIED. Deterministic (fixed data, EX-A). Model: T37R Lemma 2(b) ("PROVED",
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T37R/PROOF.md:103-115`), which proves the same
reduction for supersets with at most d extras; here the lattice is that of an arbitrary deterministic set Q ⊇ S₀ and
the move count is made explicit. Search semantics: GEN/lemmas/L4_search.md (M §6.10 as restated in SoP
`02_method.tex:463-467`; LS0: SoP `02_method.tex:490-499`).

## Setting

S₀ ⊆ Q ⊆ [p], |Q| ≤ K (so every T with S₀ ⊆ T ⊆ Q is feasible), 𝓛 := {T : S₀ ⊆ T ⊆ Q}. F(S) = log w(|S|) + log m(S)
on Ω. Neighbours of S (M §6.10): additions S ∪ {l} (l ∉ S; only if |S| < K), deletions S ∖ {i} (i ∈ S), swaps
(S ∖ {i}) ∪ {l} (i ∈ S, l ∉ S). Events (deterministic properties of the data):

* **NA(𝓛)**: F(T ∪ {l}) < F(T) for every T ∈ 𝓛 with |T| < K and every l ∉ T.
* **TL(𝓛)**: for every T ∈ 𝓛 and every feasible neighbour A of T with S₀ ⊄ A: F(A) < F(T).
  (Such A are exactly T ∖ {i} and (T ∖ {i}) ∪ {l} with i ∈ S₀, l ∉ T.)

## Lemma L1.1 (one step)

On NA(𝓛) ∩ TL(𝓛), for every C ∈ 𝓛:
(a) if C ≠ S₀: every deletion C ∖ {e}, e ∈ C ∖ S₀, satisfies F(C ∖ {e}) > F(C); every other feasible neighbour A of C
satisfies F(A) < max_{e∈C∖S₀} F(C ∖ {e}). Hence the set of maximisers of F over the feasible neighbours of C consists
of deletions of elements of C ∖ S₀ only, and each maximiser strictly improves F(C) and lies in 𝓛.
(b) if C = S₀: every feasible neighbour A of S₀ satisfies F(A) < F(S₀).

*Proof.* (a) Let e ∈ C ∖ S₀. Then T := C ∖ {e} ∈ 𝓛 (S₀ ⊆ T ⊆ Q), |T| = |C| − 1 < K and e ∉ T, so NA at (T, e)
gives F(C) = F(T ∪ {e}) < F(T) = F(C ∖ {e}). Now let A be a feasible neighbour of C that is not a deletion of an
element of C ∖ S₀. Cases:
* A = C ∪ {l} (l ∉ C, |C| < K): NA at (C, l) gives F(A) < F(C) < F(C ∖ {e}) for any e ∈ C ∖ S₀ (nonempty).
* A removes a truth (A = C ∖ {i} or (C ∖ {i}) ∪ {l}, i ∈ S₀, l ∉ C): S₀ ⊄ A, so TL gives F(A) < F(C) < F(C ∖ {e}).
* A = (C ∖ {e}) ∪ {l} with e ∈ C ∖ S₀, l ∉ C: T := C ∖ {e} ∈ 𝓛, |T| < K, l ∉ T, so NA at (T, l) gives
  F(A) < F(C ∖ {e}).
These cases exhaust the neighbours (an addition, a deletion of a truth or of an extra, a swap removing a truth or an
extra). Hence every non-deletion neighbour, and every truth deletion, has F strictly below the largest extra
deletion, which itself exceeds F(C).
(b) A neighbour of S₀ is an addition (NA at (S₀, l); |S₀| ≤ |Q| ≤ K, and additions exist only if |S₀| < K), or a
deletion or swap, which removes a truth (S₀ consists of truths): TL at T = S₀. ∎

## Lemma L1.2 (the path and the capped search)

On NA(𝓛) ∩ TL(𝓛), for every centre C ∈ 𝓛:
(i) the uncapped greedy path C = S⁰, S¹, … (scan-maximiser, lexicographic ties, move only on strict improvement)
satisfies S^{t+1} = S^t ∖ {e_t} with e_t ∈ S^t ∖ S₀, F(S⁰) < F(S¹) < …, and reaches S₀ after exactly
τ(C) = |C ∖ S₀| moves; it stops at S₀ (no strict improvement there);
(ii) the capped production search from C (cap ℓ moves, then one further scan) performs the same scans and moves up to
its cap; it scores S₀ whenever ℓ ≥ |C ∖ S₀| − 1 (if C = S₀, S₀ is the emitted centre, scored by OP-LS0 — LS0 scores its own centre — as in GEN L5.2; R10 S5); if ℓ ≥ |C ∖ S₀| its endpoint
is S₀, reached with a completed scan finding no strict improvement, without `local_limit`.

*Proof.* (i) Induction on t with L1.1(a): if S^t ∈ 𝓛 ∖ {S₀}, the scan maximisers are deletions of extras, the tie
rule picks one of them, S^{t+1} ∈ 𝓛 and |S^{t+1} ∖ S₀| = |S^t ∖ S₀| − 1. After |C ∖ S₀| moves the state is S₀; by
L1.1(b) the scan at S₀ finds no strict improvement.
(ii) The capped search coincides with the uncapped path while the move count is below ℓ (GEN L4.1(iii), whose proof
uses only the search semantics). S₀ = S^τ is a scanned neighbour of S^{τ−1}; the scan at S^{τ−1} happens iff
τ − 1 ≤ ℓ (inside the loop if τ − 1 < ℓ, as the one further scan if τ − 1 = ℓ). If ℓ ≥ τ, the τ-th move is made and
the next scan (inside the loop or the final one) finds no strict improvement by L1.1(b). ∎

**Remarks.** (1) No margin between moves and no bound on |Q| enters this lemma; the move count is linear in the
number of extras (GEN's bound was 2^{v̄} − 1). (2) The lemma is the growing-lattice form of T37R Lemma 2(b); NA there
is required only for |P′| ≤ d. (3) Ties between equal-F extra deletions are broken lexicographically; which extra
goes first is irrelevant for the count.
