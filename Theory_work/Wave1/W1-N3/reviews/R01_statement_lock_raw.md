# R01 — statement-lock review (draft v1.0)

Read-only review; no proof-status upgrade. Citations below use these repository-relative prefixes:

- `W/` = `Theory_work/Wave1/`; `N/` = `Theory_work/Wave1/W1-N3/`.
- `S/` = `Theory_work/State_of_Project/sections/`.
- `C/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.
- `M` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`.

## 1. Right target? — FIX

The code audit plus explicit deviation theorem is the right response to the available implementation: the header enumerates capped ties and has no fallback (`C/cpp/v3_start.h:214-238`); production status is correctly reported (`S/02_method.tex:789,830-838`). The specification requires a fallback (`M:150,183`). However, (a)–(e), even together with reference algorithm (f), do **not** discharge unconditional e4 for an emitted LS0 centre: e4 is precisely the emitted-centre equality (`S/04_theory.tex:84,505,532`), and FR05 flags N3 failure/deviation for escalation (`S/06_open_and_plan.tex:124-126`). State the deliverable explicitly as a characterization/conditional correctness result for frozen code, an abstract-table deviation, and a supplementary reference repair; N3 remains OPEN for integrated code. An arbitrary-table counterexample is not automatically a counterexample on data-generated tables or LH (`N/STATEMENT.md:85` already recognizes this distinction).

## 2. Faithful abstract instance? — FIX

The mathematical model correctly captures packing order, within-block numeric codes, the K cap, arbitrary size weights, zero empty-block contribution, and sorted-vector lex order (`C/cpp/v3_start.h:37-69,85-95,107-112,189-204`; `C/cpp/v3_util.h:117-125`). No index-order assumption between blocks is needed. The retained-to-original map is increasing (`C/v3_preprocess.R:112`; `C/v3_fit.R:123`). NEG_INF really is minus infinity (`C/cpp/v3_util.h:22`).

Make the encoding contract explicit: `st.J = J`, nonnull/live `st.D`, correctly dimensioned fields, and, for (e), `blk`/`pos` inverse to `blocks` (`C/cpp/v3_start.h:35-38,56-63,78-80,185`). These are currently only implicit in “as built” (`N/STATEMENT.md:62-65`). Arbitrary real lambda/rho are a deliberate enlargement of the shipped BB-prior/scorer domain, not literally all and only production inputs (`C/cpp/v3_score.h:40,63-70`; `C/cpp/v3_start.h:93-95`). Distinguish the table-defined target from exact mathematical scores when tables originate in floating-point scoring: shared EX-A includes exact scores, whereas Fraction-of-double tables only idealize subsequent arithmetic (`S/04_theory.tex:78,84`).

Correct source pointers: Start/bridge is `S/04_theory.tex:73`, EX-A is `:78`, not `:74`/`:77` as cited at `N/STATEMENT.md:45,66`. Restore the missing `Theory_work/` prefix on archive/State-of-Project links or define aliases.

## 3. Clauses (a)–(e)? — OK, subject to the encoding clarification

- **(a) OK.** Per-size block maxima and the max-plus recurrence give the exact optimum; the ascending strict-improvement scan chooses its smallest size (`C/cpp/v3_start.h:191-211`). Every enumerated leaf attains that value under EX-A (`:229-233`).
- **(b) OK.** Count is the number of visited smallest-size optimal sets, not all optimal sizes. The flag is **true at equality**: it is set immediately after visiting leaf `cap`, even if no leaf remains (`:224-226`). Thus ties = min(N,cap), truncated = [N >= cap] is correct; the stopped enumeration is a prefix, not necessarily the whole family (`N/STATEMENT.md:77-79`).
- **(c) OK.** Equality N = cap still visits every relevant set and returns S*, despite the true flag. Lex selection is explicit (`C/cpp/v3_start.h:225`). The p <= 22 sufficient bound is valid: the largest binomial coefficient at p = 22 is 705432.
- **(d) OK.** DFS uses decreasing block index, then increasing size, then increasing code (`:229-233`), exactly the key in `N/STATEMENT.md:55-58`. Concrete verification of the proposed family: take 20 inner pairs {4,5},...,{42,43}, followed by outer block {0,1,2,3}; K=22. Each inner singleton has score 1; outer {1,2} (code 6) and {0,3} (code 9) have score 2. Empty scores are 0, all other nonempty scores -1000; lambda(22)=0, other lambda=-1000. There are 2^21 optimal size-22 sets. The first 2^20 use outer {1,2}; S* uses {0,3}. Hence cap=10^6 misses S*. Replacing 20 by m with 2^m >= cap proves the abstract family for every cap. This confirms the claimed deviation, rather than refuting (d).
- **(e) OK as an IEEE sequential-operation claim.** Monotone rounded addition preserves maximum values through each fold, but not all maximizing witnesses. The selected DP path evaluates to the same value in `comp`'s block order (`C/cpp/v3_start.h:58-69,203-211,230-233`). Finite inputs can still overflow: the proof must handle positive infinity and discarded negative-overflow prefixes, or narrow the hypothesis to finite intermediate results. A negative-overflow path cannot beat the finite empty-set score. Specify no reassociation/fast-math as well as no extended precision. A concrete lex-failure example is p=2, K=1, one block {0,1}, lambda(0)=0, lambda(1)=2^54, rho({0})=1, rho({1})=2: both direct scores round to 2^54, but only {1} is a local exact maximizer and is returned. There can also be ties created by rounding at prefix/prior addition; local pruning is not the only mechanism.

No counterexample found to the stated mathematical conclusions (a)–(e).

## 4. Supplementary (f)? — OK

It is clearly labeled a reference algorithm, not frozen code (`N/STATEMENT.md:94-98`), and follows the seat-derived route (`M:183`). Greedy inclusion is appropriate only after fixing k* and preserving existence of an optimal completion at that size. L7 must specify forced/excluded indices and the feasibility test before proving correctness/complexity. This does not establish implementation or integration of the repair.

## 5. Plan/numerical companion? — FIX

The structural cases are well chosen (`N/PLAN.md:20-24`), including interleaved blocks, ties, binding K, duplicates and random tables. Required corrections:

- Separate EX-A and native-double oracles. Compiler flags do not make C++ exact. Fraction-of-double brute force cannot unconditionally validate (a)–(d) against native C++ on DATA tables (`N/PLAN.md:20-21`). Use an exact-arithmetic control-flow interpreter for EX-A, and native C++ for (e); integer-table comparisons are valid only when all relevant sums are exactly representable. Serialize doubles losslessly.
- Explicitly test N = cap-1, cap, cap+1 (including K=0, cap=1); NaNs in unread |U|>K entries; rounding ties at local, prefix and final-prior stages; cancellation and overflow, unless excluded. Random trials need declared seed counts <=20 (`W/PROTOCOL.md:18`).
- n=2 must be a direct standardized-data/routine test plus a separate assertion that the public preprocessing rejects it; it is not a production-pipeline success case (`C/v3_preprocess.R:106`; `M:182`).
- Reconcile p<=12 brute force and the p=44 million-leaf run with the binding local enumeration limit p<=10 (`W/PROTOCOL.md:18`; `N/PLAN.md:22-23`). Keep <=10 until an explicit scope exception exists; the large construction can be established analytically.
- The batched L2–L6 review happens too late if these lemmas have already been used downstream; it also straddles the planned mid-point after L5 (`N/PLAN.md:27-28`). Sequence checks before dependent proof work and stop at the mid-point gate (`W/PROTOCOL.md:23,25`). The broader FR05 assembly/LH-replica deliverables remain HQ work unless explicitly added here (`S/06_open_and_plan.tex:126`; `S/04_theory.tex:534`).

## Required fixes

1. State explicitly what remains OPEN: emitted-centre e4/integration is not closed by conditional frozen-code correctness plus reference TDP; distinguish abstract-table deviation from a data/LH counterexample.
2. Spell out the Start encoding invariants, table-domain enlargement and exact-score versus exact-table distinction; repair source paths/line numbers.
3. Specify the floating-point execution model; handle overflow in L-FP or add a finite-intermediate hypothesis.
4. Split exact/native numerical validation, preserve doubles losslessly, and add equality-cap and floating-point boundary tests.
5. Reconcile compute limits, bound random seeds, distinguish the n=2 routine test from preprocessing, and sequence review gates before downstream use.

## Overall verdict: LOCK-AFTER-FIXES

The core exact-arithmetic target is coherent. The required changes concern scope, explicit encoding/execution hypotheses and the verification plan; they do not require replacing clauses (a)–(d).
