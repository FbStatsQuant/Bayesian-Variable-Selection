# R05 — batch 2 independent proof check

Reviewed 2026-11-08 against locked `STATEMENT.md` v1.1. Line numbers below refer to the files as read in this review. L1–L5 are accepted as given; their statements and notation were consulted to check the uses here. This is a read-only review of the proofs and frozen code, with review experiments confined to `reviews/R05_scratch/`.

## Verdicts

| Lemma | Verdict | Finding |
|---|---|---|
| L6, `lemmas/L6_assembly_and_deviation.md` | **CORRECT** | Assembly, full D_m maximiser family, S*, every claimed cap, and p <= 22 bound all verified. |
| L-FP, `lemmas/LFP_floating_point.md` | **CORRECT-WITH-MINOR-FIXES** | Clause (e) is correct. One parenthetical justification of monotonicity is too broad about choices at a shared rounding midpoint; the fixed ties-to-even rule resolves it immediately. |
| L7, `lemmas/L7_tie_aware_dp.md` | **CORRECT** | Constrained DP, greedy invariant, operation count, and Python transcription verified. |

No GAP or WRONG verdict. No counterexample to clauses (a)–(f) under their stated hypotheses was found.

## L6: line-by-line audit

- Lines 6–14: D_m is a valid abstract instance for every m >= 0: K=m+2 <= p=2m+4, the blocks partition the indices, block sizes are 2 or 4 (within 31), and all read table entries are specified and finite. Empty entries are zero by the instance definition. In particular, at m=0, K=2 and the unspecified size-3/4 entries are never needed. No scorer-realizability assumption is used or established.
- Lines 17–20: (a) is exactly L4 plus L5(B),(D) and the accepted L1 reduction. `res.lg0` is assigned once at code line 213; the later enumeration changes only the selected set, count, and flag. At least one leaf exists and is processed because N>=1 and cap>=1. (b) follows from the cited enumeration results without an extra hypothesis.
- Lines 21–24: when N<=cap, all N smallest-size maximisers are processed, including the equality case N=cap. The equality case has `truncated=true` but still returns S*. Conversely, `truncated=false` implies N<cap. The combinatorial bound is valid: N<=binom(p,k*)<=binom(p,floor(p/2)). The central coefficient is nondecreasing in p (e.g. by embedding subsets into the next ground set and maximizing over sizes). Direct integer calculation gives binom(22,11)=705432 and binom(23,11)=1352078. Thus p<=22 is exactly the range of the *uniform binomial sufficient condition* at cap=1000000. This does not assert that every instance at p>=23 fails, or even truncates.
- Lines 25–26: the first sentence is independently supplied by L5(D). Choosing m with 2^m>=cap makes the family below a deviation for any cap>=1. The reference back to (d) at line 39 is not circular: only this already-proved prefix characterization is used, not the family-existence conclusion.
- Lines 29–33: each of the m inner terms is <=1, with equality only for a singleton, and the last term is <=5, with equality only for the two distinguished pairs. All deficits are nonnegative, so equality in the sum requires equality term by term. Every such combination has size m+2=K and is feasible. Consequently the *entire* maximiser family, not just a subfamily, is

  `A = { {x_0,...,x_(m-1)} union T : x_i in {2i,2i+1}, T in {{2m,2m+3},{2m+1,2m+2}} }`.

  Thus k*=K, A*=A, N=2^(m+1), and max f=m+5. This also covers the vacuous inner family at m=0.
- Lines 34–36: the smallest differing inner pair supplies the least symmetric-difference element, which belongs to E_m; if there is no differing inner pair, the comparison is between the two last-block pairs and the least difference is a=2m. All sets have the same size, so L1(iii) applies. Therefore S*=E_m union {2m,2m+3}.
- Lines 37–42: the leading DFS coordinates are the last-block size and code. Every maximiser has last-block size 2, and code 6 precedes code 9. There are exactly 2^m code-6 completions. Therefore **for every integer cap in [1,2^m]**, the visited prefix stays within that family. Its first leaf has inner codes all 1, so it is E_m union {2m+1,2m+2}. That leaf is also the lexicographic minimum of the entire code-6 family. It belongs to every nonempty prefix, and no later code-6 leaf can replace it with a smaller set. Hence the claimed `res.S` holds throughout the entire cap range, including cap=2^m. In this range `res.ties=cap`, `res.truncated=true`, and N>cap. The m=0 endpoint is correct.
- Lines 45–56: the cited specification at `METHOD_v3.1_FINAL.md:150,183` does prescribe a truncation fallback and records the N3 obligation. Frozen `v3_start.h:214–240` has only capped enumeration and no fallback. The scope exclusions are appropriate: this abstract-table result does not prove a scorer-generated counterexample or discharge the integrated LS0 premise. Line 52's “conditional is necessary” is understood as “cannot be dropped from the general guarantee”; it is not a claim that N<=cap is necessary for correctness of each individual run.
- Lines 59–63: the explicit values and family predictions were reproduced, as detailed below. The old aggregate counts are historical evidence; the fresh run here used seed 502.

Hypotheses: only H1, H2, H3 and accepted L1–L5 are used. In particular L6 does not use `comp`, the additional inverse maps needed for (e), block order matching index order, a particular prior, or scorer realizability.

## L-FP: line-by-line audit

### Minor finding FP-1 — lines 9–10, parenthetical only

The phrase “a nearest value of u′ cannot lie below one of u when u <= u′” is false if it permits independent nearest-value choices at the *same* midpoint. For example, u=u′=1+2^-53 has both 1 and 1+2^-52 as nearest binary64 values. Choosing the upper for u and lower for u′ reverses those choices. This is not a counterexample to the claimed **round-to-nearest-even map**, which chooses 1 in both cases.

Minimal repair: replace the parenthetical by: “For u<u′, nearest rounded values cannot reverse order: if r>r′ were their respective outputs, nearestness would imply u>=(r+r′)/2>=u′, a contradiction. For u=u′ the deterministic ties-to-even rule gives identical outputs.” The inequalities follow by comparing each chosen value with the other representable candidate. This proves the asserted nondecreasing map, including ties, without adding a hypothesis.

### Remaining audit

- Lines 7–11: with FP-1 repaired, monotonicity in each operand follows by composing monotone exact addition with monotone rounding. No associativity, strict monotonicity, or cancellation of rounded additions is assumed. Finiteness concerns numerical additions; the unreachable-state -infinity sentinel remains present in comparisons, as explicitly handled later.
- Lines 13–17: the fold matches the actual source exactly. `comp` sorts block/position pairs, visits nonempty intersections in increasing block order, forms their codes by OR, and performs a left fold starting from 0. H1's (e)-specific inverse-map requirement is essential and is explicitly used. Empty intersections are skipped both by this fold and by the DP's j=0 branch. The prior addition is performed after the fold, as at code line 69.
- Lines 20–27: the block maxima and ascending arg lists depend only on comparisons of finite stored doubles. Reusing the comparison-only part of L2 does not import H2's exact addition assumption. Each size j<=t_b has a nonempty set of codes, so its maximum is finite and its arg list nonempty.
- Lines 29–35: the induction proves both a pointwise upper bound and attainment. For a feasible tuple its prefix fold is bounded by the attainable prefix maximum, and its last-block value is bounded by the block maximum. Monotonicity gives the desired rounded upper bound. Conversely, choose an attaining prefix and any block argmax for an attaining j; disjoint blocks permit their concatenation, and it computes the exact candidate value used by the DP. Finite-intermediate H2-FP is used here: a reachable candidate cannot become -infinity or NaN and be confused with an unreachable cell. The all-unreachable case is handled correctly. Feasible prefix folds are also folds of feasible full sets obtained by leaving later blocks empty, so the `log_gamma0` finiteness premise covers these folds.
- Lines 37–40: for every k<=K<=p there is a size-k subset. The attainable maximum prefix fold maximizes the prior-added value by monotonicity; rounding can add other maximisers but cannot raise the maximum beyond that attained value. The code's strict ascending size scan therefore returns max ĝ and the smallest size attaining it. In particular a rounding-created tie across sizes does not break the smallest-size conclusion.
- Lines 42–50: the repaired indexing is correct. The root is q_J=kbest; choosing block c gives q_c=q_(c+1)-|S_c|. A leaf has q_0=0, so forward summation yields q_b=sum_(c<b)|S_c|=R_b. The recorded equalities can then be replayed in **forward block order**, proving F_b=M[b][R_b] for all b and hence ĝ(S)=vbest. There is no invalid backward subtraction or assumption that every rounded maximiser has tight prefixes. The omitted subscript on the two `⊕′` symbols in line 49 is determined by the displayed F_(c+1) recurrence and is harmless shorthand for |S_c|.
- Lines 51–57: every reachable nonleaf has at least one attaining j and a nonempty arg list; the first path reaches and processes a leaf before truncation can become true. `bestS` is initialized there and thereafter selected only from processed leaves. Consequently the returned set attains the DP value under its own code fold, at the smallest maximizing size, even under truncation. Completeness over *all* rounded maximisers is correctly not claimed.
- Lines 59–66: both examples are correct. At 1000 the half-ulp is 2^-44, larger than both small perturbations. At 2^54 the ulp is 4; addition of 2 lands at a midpoint and ties-to-even rounds down to 2^54. Both examples retain two rounded maximisers of the selected size while the arg lists admit only the nonlexicographic one.
- Lines 69–74: a fallback triggered only by truncation cannot repair these untruncated examples. The proposed rounded-feasibility direction is explicitly marked unproved; this review does not infer an unconditional native-double lexicographic theorem from L7.
- Lines 77–79: fresh stress checks below support (iii)–(iv); the proof, rather than sampling, establishes the universal result.

Hypotheses: only H1 (including inverse maps), H2-FP (finite tables, finite intermediate sums, prescribed binary64 execution order), and H3 are needed. Finite stored values alone would not suffice if overflow were allowed. RN monotonicity suffices despite its being non-strict. Thus the lemma proves equality to the maximum of the **code's own fold**, not to an exact reassociation of the table sum. Except for FP-1's explanatory wording, no missing argument or error was found.

## L7: line-by-line audit and Python transcription

- Lines 8–16: per-block inclusion/exclusion constraints are correctly encoded; disjoint IN/OUT is maintained. The extended-real convention is max(empty)=-infinity and -infinity absorbs addition, including infeasible/infeasible transitions. Unlike the unconstrained code, a constrained block can have no candidate of a particular size, which this recurrence handles.
- Lines 19–21, 24–29: splitting a constrained set into block intersections is a bijection preserving all constraints and the size sum. Under exact arithmetic independently chosen block maxima can be added, with infeasible terms absorbing. Hence Φ is exactly the constrained size-k optimum, and the initial DP computes V* and k*. The finite instance guarantees attainment whenever Φ is finite.
- Lines 31–40: the invariant identifies the entire decided prefix of S*, not merely consistency with some optimum. If i belongs to S*, that set witnesses the equality test. Otherwise, any optimal consistent completion containing i would share all earlier decisions with S* and have least symmetric difference i on its own side, contradicting S*'s lexicographic minimality among equal-size maximisers. A constrained family is finite; consequently absence of a V*-attainer implies Φ<V*, including Φ=-infinity. After p decisions IN=S*. Disjointness and prefix coverage are preserved in both branches. This includes K=0, k*=0, K=1, forced exclusions, and K-binding cases.
- Lines 42–45: one scan of each block's 2^|C_b| codes supplies all constrained maxima, using block masks and popcounts. Mask construction costs O(sum_b |C_b|)=O(p), absorbed by sum_b 2^|C_b|. The block-width bound |C_b|<=31 permits fixed-width mask tests; alternatively popcounts can be precomputed in a linear code scan. The convolution has at most J(K+1)^2 transitions. Row initialization, prior addition, size selection and decisions are within the displayed bound. There is one initial DP plus p constrained evaluations, and p>=1 allows p+1=O(p). Thus the claimed total **arithmetic-operation/comparison** bound holds. It is not a claim about bit complexity of arbitrary rational arithmetic or Python interpreter work. No maximiser enumeration is performed, even though all local block codes are scanned.
- Lines 48–53: the cited spec describes this greedy feasibility approach. The exact-arithmetic guarantee is correctly scoped. Native arithmetic would require a corresponding constrained-fold argument, including handling empty intersections, not arbitrary reassociation of additions.
- Lines 56–57: the transcription and its claimed exact output were tested afresh.

`numerics/tdp.py`: lines 22–36 construct the required/forbidden block masks and constrained maxima, skipping sizes>K before reading those entries. Lines 39–52 implement the constrained convolution with `None` as -infinity and skip either infeasible operand. Lines 55–61 select V* and the minimum maximizing size. Lines 62–69 perform exactly the greedy tests and return `(V*, k*, sorted(IN))`; the third component is the mathematical algorithm's output. `exact` retains integers/Fractions and converts each double to its exact dyadic rational, so this is an exact-table algorithm, not a native-double fallback. No discrepancy found.

Hypotheses: the abstract instance and exact arithmetic suffice; no special prior, block/index-order relation, realizability, cap assumption, or bound on the number of global maximisers is used. The block-width condition supports the mask implementation and cost model.

## Fresh numerical checks

`sh` was not available on PATH. I compiled the existing harness source directly with the flags from `build.sh`, placing the executable in the permitted scratch directory, without changing the source or frozen headers:

```text
g++ -O2 -std=gnu++17 -D_USE_MATH_DEFINES -msse2 -mfpmath=sse -ffp-contract=off
  -IScripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp
  Theory_work/Wave1/W1-N3/numerics/sm_harness.cpp
  -o Theory_work/Wave1/W1-N3/reviews/R05_scratch/sm_harness.exe
python -I -B Theory_work/Wave1/W1-N3/reviews/R05_scratch/check.py
```

The scratch driver overrides only `n3lib.HARNESS` in memory and runs the existing scripts via `runpy`; `-B` prevents cache writes outside scratch. Results:

- D_m, **every cap 1..2^m**, m=0..8: 511/511 output/value/count/flag checks passed.
- D_m, m=0..4: brute-force equality of the *complete* maximiser family, S*, k*, N, and code-6 DFS prefix passed.
- Existing `cex_family.py`: 50/50 passed, m=0..12, including caps 2^m+1 and N. At N the full optimum is found and `truncated=true`, as claimed.
- Existing `cex_default_cap.py`: frozen result `{0,2,...,38,41,42}`, value 25, ties 1000000, truncated 1; TDP and closed form both give `{0,2,...,38,40,43}`.
- Existing `fp_example.py`: both nontruncated lex failures reproduced; returned ĝ equals `res.lg0` equals max ĝ in both.
- Additional seed-502 stress: 1200 random ordered partitions with p<=9, all K ranges, caps 1/2/1000000, signed/cancelling values with exponents from -1074 to 900, including subnormals. Exhaustive rounded objectives verified clause (e) in every case. Exact Fraction brute force independently verified TDP's value, size and lex choice on all 1200 cases. These exponents and small block counts keep intermediate sums finite.
- Full existing `run_checks.py`, seed **502**, with the same scratch harness and `python -I -B`: **38,978 instances; zero reported failures**. Counts: exhaustive p<=3 19,950; constructed 548; random integer families 13,000; DATA 400; cap-edge 2,080; floating stress 3,000. Floating stress had 415 cases with multiple rounded smallest-size maximisers and 24 rounded lex differences, all allowed by clause (e).

The full-suite driver checks reported failure counters rather than treating an exit code alone as success; none appeared. Empirical checks supplement the proofs and do not establish scorer realizability of D_m or production integration of the fallback.

## Required fixes

1. **L-FP lines 9–10 (FP-1):** qualify/replace the parenthetical nearest-rounding argument to use the fixed ties-to-even rule at equal midpoint inputs, for example with the two-case argument given above. No theorem, hypothesis, algorithm, or code change is required.
