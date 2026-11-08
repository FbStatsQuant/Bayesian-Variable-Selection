VERDICT: ERROR

Scope: I5 only; (D_S), (L), P3′ and posterior concentration are inputs, not re-proved here. The output composition is valid under the stated operational assumptions. The errors concern the unqualified move count and the sharper cost display; they do not invalidate the repaired asymptotic composition.

Paths below: NBH = `Theory_work/Old_Projects/New_BVS_Headquarters`; PROOF = `NBH/branch_snapshots/API-PXNGAP/PROOF.md`; W6 = `NBH/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md`; CPP = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp`.

| Claim / step (path:line) | Verdict | Reason |
|---|---|---|
| P5, PROOF:286–288; CPP/v3_start.h:178–239 | VERIFIED | A probability mass above 1/2 makes S° the unique global maximiser. Exact max-plus optimisation and reconstruction suffice; no prescribed choice among tied global modes is needed on this event. |
| Scan semantics, PROOF:373–377; Docs/Methodology/METHODOLOGY_v3.md:258–267; CPP/v3_engine.h:385–420 | VERIFIED | Frozen centre; all feasible flips and all swaps; strict score improvement; lexicographic neighbour ties; at most ℓ accepted moves followed by a complete scan. Centre emission is explicit for LS0. |
| Lemma LS(i), PROOF:379–387 | ERROR | Reaching S₀ as a centre after c moves requires ℓ ≥ c. The stated hypotheses omit this. Without (L), exactly c is the number of moves up to first arrival, not necessarily the total. |
| Lemma LS(ii), PROOF:381–389 | VERIFIED | For c ≥ 1 and feasible truth, the c-th scan scores S₀ after c−1 accepted moves, including when ℓ = c−1. Progress ties cannot obstruct this. |
| Lemma LS(iii), PROOF:383,389–391 | VERIFIED | With ℓ ≥ c and (L), the next scan certifies S₀; total is c accepted moves and c+1 scans, with no local_limit. |
| P6′ assembly, PROOF:395–399 | MINOR | Eventual scoring and certification follow from the stated inputs; explicitly require ℓ_n ≥ c for the arrival/certification clause. Since c is fixed and ℓ_n diverges, enlarge n₀. Cost errors are assessed separately below. |
| Deterministic HPM implication and Markov, PROOF:443–445 | VERIFIED | π(S₀)>1/2 makes S₀ the unique F maximiser; δ₁≥0 gives P(δ₁≥1/2)≤2Eδ₁ under the joint law. No conditioning on completion or independence is used. |
| Operational closure, PROOF:445–446; W6:32–51,71–78 | VERIFIED | Strict output excludes stopped runs; (G2) identifies the entire computation with R̄⁺ on output. OP-LS0 ensures completed LS0 and its emitted centre. Thus O⊆Ō and S⁺=S̄⁺ on O. Lemma RO is a consequence of these premises, not an additional assumption. |
| Composition conclusions, PROOF:436–440 | VERIFIED | The inclusions yield the displayed every-n bound. Success probability equals P(O) minus the output-error probability; the liminf identity follows even if P(U) does not converge. |
| Ledger and LS0 implementation bridge, CPP/v3_ledger.h:83–114; CPP/v3_util.h:120–125; W6:48–51,76–78 | VERIFIED | Running best uses F, then size, then lex; cache eviction does not erase the HPM. This supports the conditional premise, but does not establish that shipped fits execute LS0. |
| Sharper P6′ cost, PROOF:398 | ERROR | max over all k≤K cannot be bounded by restricting k to s₀. Moreover c+1 scans require (L); discovery alone allows further search after S₀. |
| General (K), PROOF:441 | VERIFIED | At most ℓ_n+1 scans, with ≤p+k(p−k) evaluations per scan and one centre evaluation. The c+1 clause is valid on the lattice-arrival-and-certification event, not on discovery alone. |

1. **ERROR — move-cap omission.** PROOF:379–387 asserts c moves without ℓ ≥ c. Take c=1 and ℓ=0, with the missing hub the strict best neighbour as (D_S) requires. CPP/v3_engine.h:413–418 completes the first scan, scores S₀, sets local_limit, and records zero accepted moves. Its `returned` field is the improving neighbour S₀, but this is not a move or a certificate. More generally, the search takes min(c,ℓ) accepted progress moves before arrival or cap, and first reaches S₀ as a centre iff ℓ≥c. **Repair:** replace (i) with “every accepted move before first arrival at S₀ adds one missing masked hub; if ℓ≥c, first arrival occurs after exactly c moves.” Keep (ii) independent of this added condition. With (L), the total is exactly c moves. In P6′ explicitly choose n₀ so ℓ_n≥c. No restriction on ties among progress neighbours is required: on this lattice S⊆S₀, only adding a missing truth reduces Φ; every swap is non-progress, and (D_S) strictly excludes it.

2. **ERROR — sharper cost and its event.** PROOF:398 writes `max_{k≤K}[p+k(p−k)] ≤ p+s₀p`, which is false when K is large relative to fixed s₀. Also the event in PROOF:396 excludes the additional event establishing (L): after reaching S₀, an improving neighbour can make the search continue. **Repair:** on `{S̃₀=S°} ∩ (D_S) ∩ (L) ∩ {ℓ_n≥c}`, write

   `N_scores ≤ 1 + Σ_{t=0}^c [p+(s+t)(p−s−t)] ≤ 1+(c+1)(p+s₀p)`.

   The maximum, if retained, must be over `0≤k≤s₀`, not `k≤K`. On arbitrary runs retain the correct bound `1+(ℓ_n+1)max_{0≤k≤K}[p+k(p−k)] = O(p² log(n+p))`. In §10(K) define “event of (T)” as the joint lattice/certification event, rather than merely `{LS0 scores S₀}`. The sharp count and O(p) bound then hold with probability tending to one given the inputs.

3. **MINOR — make feasibility and arithmetic scope explicit.** PROOF:379–399 should state `s₀≤K`, eventual automatically since s₀ is fixed, p→∞, n→∞. Each progress addition is then feasible even when the next state has size K; CPP/v3_engine.h:400–411 excludes only additions from a centre already at K and still scans every swap. No need for p≤n. For P5 retain EX-A plus exact maximisation/reconstruction of the capped start distribution. In exact arithmetic the DP computes, for each size k, the maximum sum of block log-ratios, then adds the size prior and maximises over k (CPP/v3_start.h:186–211); backtracking recovers an optimum (214–238). A second optimal partial configuration on a selected optimal path would produce a second global mode, impossible on `{π₀(S°)>1/2}`. Thus OB03's general N3 tie-DP invariant is bypassed on this event, not proved. Floating-point score/DP exactness is not established by the probability argument. **Repair:** add these qualifications; do not claim a general resolution of N3.

4. **MINOR — cite the closure premise precisely and retain implementation conditionality.** The exact chain is

   `O∩{S₀∉S⁺} ⊆ Ō∩{S₀∉S̄⁺} ⊆ {LS0 of R̄⁺ does not score S₀}`.

   First, O excludes guard stops (including a stopped post hoc LS0); (G2) gives identical status and computation with R̄⁺, hence identical scored sets on O. Second, R̄⁺ includes its deterministic LS0 by definition, also when R̄ has schedule_limit. This proves the chain from W6 as stated. Mere equality of reported HPMs would not prove scored-set equality, but W6:73 assumes the stronger equality of computation. Even scored-set containment `S̄⁺⊆S⁺` on O would suffice. See also NBH/branch_snapshots/W2-BOOK/PROOF.md:75–95 (Lemma RO); no additional statistical or independence premise is needed. The data-only Markov bound remains valid after adjoining run randomness and operational Ξ.

   CPP/v3_engine.h:388,395–411 emits the centre when requested and every scanned neighbour; CPP/v3_ledger.h:85–114 keeps an HPM independently of the bounded stores. Updating stores only on fresh scores is valid under the stated run-owned-cache invariant (ledger:97–99): cached models were already offered. LS0 must use `emit_centre=true` and a compatible ledger/cache or explicit union. NBH/branch_snapshots/O-LS0/REPORT.md:8–9,69–70,105,432–433 documents post hoc export and explicitly lacks an integrated production test. Registry OB02/OB03 (NBH/ID_REGISTRY.md:146–147), DF16 (:177), and ENG02 (Theory_work/State_of_Project/tables/registry_open.tex:23) do not discharge production integration. **Repair:** cite (G2)/RO explicitly and keep the theorem about v3+LS0 under OP, not an audited assertion about the shipped core. An unconditional implementation claim needs the merged-LS0 execution/replay and output-ledger bridge. This is an implementation obligation, not a gap in conditional (C).

A-dependence: The deterministic search, uniqueness, closure, Markov and general cost arguments require neither p≤n nor polynomial p. They hold for every fixed A≥1, including A>1, given the stated inputs and eventual s₀≤K. The search thresholds ℓ_n≥c−1 (scoring) and ℓ_n≥c (arrival/certification) introduce no A-dependent constant. A enters only through the supplied high-probability (D_S), (L), P3′ and posterior-concentration inputs and their onsets; those inputs are outside I5. Nothing here provides uniformity in A or removes their hypotheses.

---
## Disposition (W1-PXN lead, 2026-11-08)
Both ERRORs accepted (they concern the move count without ℓ ≥ c and the sharp cost display; neither affects (C), (T)-scoring
or the asymptotic conclusions, since ℓ_n → ∞). Repairs in lemmas/LS_P6_repair.md (ERRATA E-8..E-11), using the reviewer's
wording; to be re-checked by a NEW cross-family reviewer. Report item #5 (operational closure OP-LS0 + GUARD): VERIFIED
as a theorem under (OP) as stated in W6; production integration remains an implementation obligation (OB02(c), OB03,
DF16, ENG02). P5, (C) composition and Markov step VERIFIED. STATEMENT §2 (K) wording to be updated to the joint event.
