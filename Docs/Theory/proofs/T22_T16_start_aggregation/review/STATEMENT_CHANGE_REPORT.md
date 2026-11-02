# Statement change report — T22 (T16) parts (i), (ii), (iv)

To the statement checker. Files: ORIGINAL_T22.md (the source statement; the proof-route hint has been removed as the protocol requires), 00_COMMON.md (shared definitions), STATEMENT.md (the precise statement proposed for proof). Only parts (i), (ii), (iv) are in scope.

## Proposed change C1 (added hypothesis)

(ii) and (iv) assume S₀ ∈ Ω, i.e. s₀ = |S₀| ≤ K = min(p, ⌊n/2⌋).

Why it is necessary. π₀, q_φ and π are probability distributions on Ω = {S : |S| ≤ K}. If s₀ > K, then S₀ ∉ Ω and π₀(S₀) = 0 (or is undefined). The right side of (ii-a), π₀(S°)·[w(s₀)/w(s)]·∏_b r_b(S₀∩C_b)/r_b(S°∩C_b), is strictly positive for every feasible S° (all w(k) > 0, all tables > 0, π₀(S°) > 0). So (ii-a) is false. Concrete instance: n = 3, p = 2 gives K = min(2, 1) = 1; with S₀ = {1,2} and S° = ∅, π₀(S₀) = 0 while the right side is π₀(∅)·[w(2)/w(0)]·r_b(...) > 0. In (iv), R_i = 1/q_i(S₀) − 1 is then undefined (division by 0). The source's own regime R assumes "eventually s₀ ≤ K", so the hypothesis costs nothing asymptotically.

## Readings (no change of content intended; please confirm or object)

- C2: the source (iv)'s last sentence, "With T03 and (iii) this gives uniform concentration on [0,1]", is stated as (iv-c): a conditional consequence in which the conclusions of T03 (1 − π(S₀) → 0 in probability) and of part (iii) (1 − π₀(S₀) → 0 in probability) are explicit hypotheses. T03 and (iii) are unproved conjectures being handled elsewhere; this run may use them only as hypotheses.
- C3: δ^{comp} = sup over S ⊉ S° is read with S ranging over feasible models; this gives a smaller supremum and hence a stronger bound, which implies the reading with S ranging over all subsets of [p].
- C4: "Normalised reference mass remains essential" (end of (ii)) is recorded as an interpretive remark, not a mathematical claim.
- C5: the remaining definitions in STATEMENT.md (a_{bj}, D_b, q, e, u, uncapped weight, conventions for s = 0 and s = p, r_k, R_i) are intended to be verbatim transcriptions of the source and 00_COMMON.md.

## EXP

Parts (i), (ii) and (iv) are deterministic statements about fixed data (exact arithmetic, EX-A). The lead's assessment is that none of them needs EXP or EXP′; (iii) is out of scope.

## Questions for the checker

1. Is C1 necessary, and is it the minimal fix?
2. Is STATEMENT.md a faithful transcription of the source's (i), (ii), (iv) otherwise (definitions, conventions, quantifiers)? Point to any mismatch.
3. Do you see any other hypothesis that (i), (ii) or (iv) silently needs (including EXP/EXP′)?
4. Is any of the claims in STATEMENT.md false as stated? If so, give a counterexample.
