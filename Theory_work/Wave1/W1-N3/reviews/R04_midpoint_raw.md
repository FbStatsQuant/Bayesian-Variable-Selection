# R04 — Independent midpoint review

**Verdict: CONTINUE.** The project is on track to deliver a correct, meaningful result for the locked target. I find no fatal flaw in the repaired L1–L5 chain, and the later-stage drafts have sound arguments for the deviation, native-double value/membership result, and exact-arithmetic reference algorithm. This is a qualified continuation: the deliverable characterises the frozen routine and proves a supplementary algorithm; it does not establish the unconditional e4 invariant for an integrated emitted LS0 centre.

## Review basis

Read STATEMENT.md and all seven files in lemmas/. Checked the frozen `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp/v3_start.h`, including `comp`, table construction, the value DP, and backtracking. Also consulted the cited method specification, State-of-Project sections 02, 04, and 06, and the cited utility, score, preprocessing, and fit sources. I did not open LOG.md, PLAN.md, any reviews/ input, or any numerics/ file. The numerical claims embedded in the lemmas are not independently verified evidence in this review.

## 1. Fidelity of the target

The original obligation is the prescribed smallest-size, lexicographically smallest maximiser of the start distribution. The locked target correctly identifies that distribution: normalisation does not affect maximisers, and its exact-arithmetic objective is the size prior plus the sum of the block log ratios. It also correctly transports index order through the increasing retained-column map.

The target is faithful to the frozen code rather than to an imagined implemented fallback. The code builds per-size block maxima, performs a max-plus convolution, picks the smallest maximising size by a strict ascending scan, and enumerates optimal paths with a cap. It has no fallback branch. The specification's truncation fallback is an additional requirement, and the target reports that deviation explicitly. The cited implementation table independently supports the distinction between the header routine and production LS0 integration.

This is a useful partial resolution of FR05/OB03, not a proof of its full operational premise. In particular, an abstract-table counterexample disproves unconditional correctness on the enlarged input class, but does not establish a failure on scorer-generated tables or LH. STATEMENT §0 makes these limits sufficiently explicit. Preserve them in the final theorem, conclusion, and any status update.

## 2. L1–L5: the central proof

**The repaired L5 is sound and proves what (a)–(d) need.** L1 separates abstract tables from the method specialisation and makes the extra inverse-map requirement local to interpreting `comp`. L2's running-maximum invariant correctly gives complete, ordered, nonempty per-size argmax lists. L3's independent block decomposition and L4's strict ascending size scan establish the correct value and smallest maximising size.

L5(A) now includes the final-prefix condition at b = J. Its reverse implication follows immediately from that condition. Its forward implication correctly chains two upper bounds and uses exact real addition to force equality in both the prefix and local block terms. Thus it avoids assuming that an arbitrary allocation of individually optimal block subsets is globally optimal.

L5(B)'s suffix invariant establishes soundness of every leaf; the recurrence and nonempty local argmax lists exclude dead ends; (A) supplies a path for every smallest-size maximiser. Disjoint blocks and injective codes give uniqueness. The nested increasing size/code loops then give precisely the stated reverse-block DFS key, independently of global index order. The cap proof matches both early-return sites in the code, and the lexicographic accumulator takes the minimum only among processed leaves.

The argument covers binding K: all local sizes are bounded by both the remaining size and min(block size, K), and prefix replacement preserves total size. At K = 0 the unique all-empty path is valid. At cap = 1 the first leaf sets `bestS` before truncating. At N = cap all N leaves are processed and `truncated` is nevertheless true; at N = cap + 1 only cap are processed. No assumption that numeric code order is lexicographic subset order, or that block order follows index order, enters this proof.

## 3. Remaining clauses

**(d), L6:** The D_m construction is valid, including m = 0 and K smaller than the last block. The independent block upper bounds are simultaneously attainable at size K. Exactly 2^(m+1) maximisers result. The last block's code 6 precedes code 9, so its entire 2^m-element family precedes the family containing S*. Its first leaf is already the lexicographic minimum within the code-6 family. This establishes the asserted wrong tie choice for every positive cap, including the stated p = 44, K = 22 default-cap example. No data-realisation claim follows from this construction.

**(e), L-FP:** The route is sound. Rounded addition is monotone, so replacing a block value and prefix fold by their maxima preserves an upper bound and yields an attainable DP maximum. The fold order, including skipping empty blocks, matches `comp`; the final prior addition matches `log_gamma0`. Backtracking tight equalities can be propagated forward without cancellation or reassociation. This proves value, membership, and smallest size for the code's own rounded objective. It does not prove completeness of the rounded maximiser family. Both examples correctly exploit that distinction, including rounding at the prior addition. The stated execution and finiteness hypotheses are material.

There is a minor indexing defect in the written invariant in L-FP(iv): it defines r_c as the remainder at level c+1, but then uses r_(c+1) for that remainder. Define q_b as the argument of `rec(b, q_b)` along the path, q_J = kbest, and q_c = q_(c+1) − popcount(c_c). The displayed equality is then M[c+1][q_(c+1)] = M[c][q_c] ⊕'_(popcount(c_c)) mb[c][popcount(c_c)]. The subsequent forward-induction argument already has the correct intended structure.

**(f), L7:** The constrained max-plus DP computes the required exact feasibility value. Fixing k* first makes the smallest-symmetric-difference lexicographic argument valid. The include-if-feasible induction proves S* for arbitrary block packing, without enumerating global ties. The stated arithmetic-operation bound is justified by block mask scans and at most p+1 convolutions; it is not a bit-complexity or wall-clock guarantee.

## Most important issues before final review

1. **Keep the closure claim precise.** Deliver frozen-code conditional correctness, a scoped deviation, and reference-algorithm correctness. Do not mark the integrated emitted-centre e4 premise discharged by these alone, or describe D_m as a scorer/LH counterexample.
2. **Make the floating-point consequence explicit in the assembly.** A fallback triggered only by `truncated` cannot in general repair rounded lexicographic errors: the L-FP examples fail even with ample cap and no truncation. L7 establishes exact-arithmetic correctness; a native-double integration needs its own rounded-feasibility argument and cannot inherit L5's enumeration-completeness claim.
3. **Repair the L-FP(iv) remainder indexing.** Present the path equalities with consistent level indices before final proof checking. Retain explicit handling of K = 0, N = cap, and arbitrary block/index order in the assembled proof; those cases are already supported by the current arguments.

No redirection of the central mathematical approach is warranted.
