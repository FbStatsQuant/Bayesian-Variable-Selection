# Repair of Lemma LS (PROOF §8.4), Theorem P6′ (§8.5), (K) (§10) and P5 qualifications — from reviewer R15

Status: repair by this seat (wording largely proposed by R15); XF VERIFIED WITH MINOR FIXES (R21), fixes applied — v2, 2026-11-08.
PROOF = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`; CPP =
`Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp`.

## Defects found by R15
- ERROR 1 (PROOF:379-387): Lemma LS(i) asserts exactly c moves to reach S₀ without assuming ℓ ≥ c (counterexample: c = 1,
  ℓ = 0: the first scan scores S₀, sets local_limit, zero accepted moves; CPP/v3_engine.h:413-418).
- ERROR 2 (PROOF:398): "max_{k≤K}[p + k(p−k)] ≤ p + s₀p" is false for K ≫ s₀; and the c+1-scan count needs (L), which is
  not in the event of PROOF:396.

## Lemma LS (repaired)
Setting as PROOF:374-379, with s₀ ≤ K (eventual: s₀ fixed, p → ∞, n → ∞). Suppose (D_S) holds for every
S ∈ Lat(S°) ∖ {S₀} (progress ties allowed) and the centre is S° with Φ(S°) = c ≥ 1.
(i) Every accepted move before the first arrival at S₀ adds one missing masked hub (states stay in Lat(S°)); the search
    makes min(c, ℓ) accepted moves before arrival or cap, and first reaches S₀ as a centre iff ℓ ≥ c, after exactly c moves.
(ii) S₀ is scored at the c-th scan, which is performed iff ℓ ≥ c − 1 (if c − 1 = ℓ it is the final scan). Hence
    S₀ ∈ 𝒮_LS0 whenever ℓ ≥ c − 1. (Unchanged; R15: VERIFIED.)
(iii) If moreover (L) holds and ℓ ≥ c, the search returns S₀ with local_certified and without local_limit, after exactly
    c accepted moves and c + 1 scans. (Unchanged; R15: VERIFIED.)
*Proof of (i).* At S ∈ Lat(S°) ∖ {S₀}, S ⊆ S₀ has no extras, so the only Φ-decreasing neighbours are additions of missing
masked hubs (every swap and every deletion is non-progress), and (D_S) makes the best scanned score strictly exceed F(S)
and be attained only at such additions; the lexicographic rule picks one; Φ drops by 1. Each such addition is feasible
because |S| < s₀ ≤ K (CPP/v3_engine.h:400-411 excludes additions only from a centre already of size K). So moves continue
while the move count is < ℓ and the centre is not S₀: after min(c, ℓ) accepted moves either the centre is S₀ (c ≤ ℓ) or
the cap is reached (ℓ < c). ∎

## Theorem P6′ (repaired)
Let 𝒯_n := 𝒜_n ∩ Ω_n ∩ 𝒵_n ∩ {S̃₀ = S°} (Theorem R / (R′), Lemma E, Lemma Λ, (L) via lemmas/L_strict_localmax.md, P5).
Choose n₀ with ℓ_n = ⌈log₂(n+p+1)⌉ ≥ c and s₀ ≤ K for n ≥ n₀. Then P(𝒯_n) → 1 and, on 𝒯_n, for n ≥ n₀: LS0 of R̄⁺ scores
S₀ (needs only Ω_n-part (D_S) and ℓ_n ≥ c − 1), reaches S₀ after exactly c moves and returns it with local_certified, using
c + 1 scans and
  N_scores ≤ 1 + Σ_{t=0}^{c} [p + (s+t)(p − s − t)] ≤ 1 + (c+1)(p + s₀p).
On arbitrary data the bound 1 + (ℓ_n+1) max_{0≤k≤K}[p + k(p−k)] = O(p² log(n+p)) holds (PROOF:441, R15: VERIFIED).
(K) in STATEMENT §2 reads "c + 1 scans on the event 𝒯_n" (the joint lattice/certification event), not on {LS0 scores S₀}.

## P5 qualifications (R15 #3)
On {π₀(S°) > ½}, S° is the unique global maximiser of π₀; exact max-plus maximisation and backtracking (CPP/v3_start.h:
178-239) then return S° (a second optimal configuration would be a second global mode). This **bypasses** the N3 tie-DP
invariant (OB03) on this event; it does not prove N3. Premise retained: EX-A (exact scores and exact DP arithmetic);
floating-point exactness is not established by the probability argument.

## Closure citation (R15 #4)
𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 of R̄⁺ does not score S₀}: the first inclusion by (G2) of GUARD (W6:71-73; Lemma RO,
`NBH/branch_snapshots/W2-BOOK/PROOF.md:75-95`): on 𝒪 no guard stopped the run (a stopped post hoc LS0 is in U by OP-LS0),
so the run performs exactly the R̄⁺ computation and 𝒮⁺ = 𝒮̄⁺; the second because R̄⁺ contains its deterministic LS0 with
the emitted centre by definition (W6:48-51), also when st̄ = schedule_limit. The theorem is about v3 + LS0 under (OP);
the production bridge (merged LS0 with emit_centre = true, replay; OB02(c), OB03, DF16, ENG02) remains an implementation
obligation, not a step of the proof.
