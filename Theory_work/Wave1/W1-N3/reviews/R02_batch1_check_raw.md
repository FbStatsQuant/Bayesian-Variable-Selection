# R02 — batch-1 independent proof check

Reviewed against locked STATEMENT v1.1, especially §§1–2. Paths below are relative to `Theory_work/Wave1/W1-N3/` unless prefixed `CODE/` or `SoP/`, with those aliases as in STATEMENT. No source, lemma, statement, or numerical-evidence files were changed.

| Lemma | Verdict |
|---|---|
| L1 | GAP |
| L2 | CORRECT |
| L3 | CORRECT-WITH-MINOR-FIXES |
| L4 | CORRECT-WITH-MINOR-FIXES |
| L5 | WRONG (A as stated); B–D are repairably proved |

## L1 — reduction and order facts

**Verdict: GAP.** The mathematical reduction and order facts are valid; the asserted connection to `comp` needs an assumption unavailable here.

1. **Unstated encoding assumption:** `lemmas/L1_reduction.md:10,28–30`, specifically “which by (H1) equals code(S_b).” H1 requires `st.blk`/`st.pos` to invert `st.blocks` **for (e) only** (`STATEMENT.md:87–88`). L1(ii) invokes them under exact arithmetic, outside that extra condition. H1 for (a)–(d) allows these fields to be empty or incorrect. Thus even with exact arithmetic `comp` need not compute the stated sum; empty fields can cause invalid access.

   Concrete, fully initialized counterexample: p=2, K=1, J=2, C_0=[0], C_1=[1], λ=(-10,0), ρ_0(∅)=ρ_1(∅)=0, ρ_0({0})=1, ρ_1({1})=2. Supply all H1 lengths and code lists normally, but set `st.blk=[1,0]`, `st.pos=[0,0]`. This satisfies the H1 requirements applicable under H2. For S={0}, the mathematical composite sum is 1, whereas source lines 56–63 read `logr[1][1]` and return 2. H2 and any valid cap do not repair this.

   Required fix: state the `comp` identification conditional on the inverse-map condition already named in H1 for (e), or restrict this part to objects produced by `build_tables`. The equality of the two mathematical sums itself needs no extra condition. Do not silently strengthen the locked H1.

2. **Abstract-domain proof omission:** `lemmas/L1_reduction.md:20–24` identifies the arbitrary λ and ρ of §1 with the particular normalized BB prior and scorer Bayes factors. These identifications hold for the method specialization, not every abstract instance. Example: p=1, K=0, λ(0)=7 is permitted, whereas the normalized capped prior on the sole empty model has log prior 0. No scorer realization of arbitrary ρ is assumed either.

   Missing argument (sufficient repair): for abstract tables define γ_0(S)=exp(f(S)) and Zbar_0=Σ_{S∈Ω_K}exp(f(S)); finiteness and positivity give the log identity and identical maximizers. Then identify these quantities with D0's prior/Bayes-factor expressions in the method specialization. This does not require a normalized exp(λ) prior, scorer realizability, or additional hypotheses. STATEMENT §1 already intends this table-defined interpretation.

3. **Numerical-evidence wording:** `lemmas/L1_reduction.md:47–48` says the DATA family computes exact-table f and the native value and that they “agree on the maximiser in all non-FP-tie cases.” The actual DATA assertions (`numerics/run_checks.py:236–260`) compare the returned set/count/flag with the exact-table prediction, and separately test native value/membership/minimum size. They do not define or select a “non-FP-tie” subfamily or directly compare `res.lg0` with exact-table max f. Report these actual checks instead; no mismatch was reported on the 400 DATA cases per stored seed.

Line audit: (i), lines 7–8 and 20–26, correct after the abstract-domain clarification; (ii), lines 10 and 28–30, mathematical equality correct but code identification lacks the inverse-map condition; (iii), lines 12–13 and 32–40, correct, including the equal-size argument ensuring the next Y entry exists; (iv), lines 15–17 and 42–44, correct. The retained-column order is verified by preprocessing lines 112 and 118–120, fit line 123, and score lines 18 and 39–43.

Hypotheses only? **No as written:** inverse maps are used outside their stated scope, and the proof specializes arbitrary tables without supplying the abstract argument. No additional hypothesis is needed for (iii)–(iv).

Code quotations/citations: the inline formula quotations at lines 24–25 are faithful mathematical paraphrases of `v3_start.h:69–70`, not literal C++ expressions. `kept <- which(!constant)` matches the first expression of preprocessing line 112; the fit/score mapping and `lex_less` citations match. The cited `comp` mechanics and table construction match the source; their applicability under H1 is the issue. D0/EX-A source references at `SoP/04_theory.tex:70–86` match. No erroneous code transcription found.

## L2 — block maxima

**Verdict: CORRECT.**

Line audit: lines 21–24 follow from the complete increasing size-code lists; lines 27–31 correctly establish domain, bijection, and nonemptiness; lines 33–39 give a valid three-case scan invariant; lines 40–41 correctly treat j=0. Finite real entries ensure the first value beats NEG_INF. This includes K=0 and K smaller than a block.

Hypotheses only? **Yes:** H1 and H2 suffice; no block-order/index-order relation, scorer realization, inverse maps, or cap assumption is used.

Code quotations: all 12 numbered lines at `lemmas/L2_block_maxima.md:6–17` match `CODE/cpp/v3_start.h:186–197`. Supporting references to lines 95 and 107–112 match. Numerical claim at lines 44–45 matches the seed-11 probe and its rerun. No required fixes.

## L3 — max-plus DP

**Verdict: CORRECT-WITH-MINOR-FIXES.** The mathematical proof is correct; fix the numerical-coverage statement.

Line audit: definitions at lines 25–27 correctly handle b=0 and infeasibility. Lines 34–44 establish the base row and the max-plus recurrence by a disjoint decomposition into last-block size and independent prefix/last-block choices. Skipping NEG_INF and omitting addition of μ(0)=0 preserve that recurrence. Lines 45–46 correctly prove full-row finiteness using K≤p and the partition bijection. No mathematical gap found.

**Coverage correction:** `lemmas/L3_L4_dp_and_size.md:59–61` says “for every ... k ≤ K.” The probe actually sets `Kb=min(I0.K,pb)` and tests k=0,…,Kb (`numerics/lemma_probes.py:55–60`). It does not test unreachable prefix cells k>pb up to the original K, or row b=0; finite priors cannot isolate an infeasible target size to make the output −∞ because other feasible sizes remain. State “every feasible prefix size k≤min(K,|C_0∪…∪C_{b−1}|).” Its 2,521 probes are accurate. These are black-box output checks, not direct inspection of internal M cells.

Hypotheses only? **Yes:** H1, H2, and the correctly proved L2. The evidence wording issue does not affect the proof.

Code quotations: the portion `CODE/cpp/v3_start.h:198–206` quoted at lemma lines 6–14 matches exactly, as does the remainder through line 213 used for L4. No transcription errors.

## L4 — size selection

**Verdict: CORRECT-WITH-MINOR-FIXES.** The mathematical proof is correct; fix the shared numerical summary.

Line audit: lines 49 and 52–56 correctly use finiteness of every final-row entry, the size-specific constant λ(k), the ascending size scan, and strict replacement. The initial k=0 candidate is real and beats NEG_INF, so kbest is defined. The scan invariant proves both the value and the smallest maximizing size, including K=0 and cross-size ties.

**Evidence correction:** `lemmas/L3_L4_dp_and_size.md:61–62` and `lemmas/L5_enumeration.md:107` say approximately 41,000 instances per seed. The stored family totals are 38,951 (20261108) and 38,985 (7), including 3,000 per seed testing only floating-point clause (e). Accordingly those 3,000 are not checks of exact-arithmetic (a) or (b)/(d). The DATA family also uses the distinct checks described under L1 above. Give the actual family counts and distinguish the exact-integer, DATA, and FP-only checks. `numerics/README.md:10` gives the old total 33,898 before the cap-edge and FP additions; this explains neither an exact 41,000 count nor broader assertion coverage.

Hypotheses only? **Yes:** H1, H2, and L3. No tie-enumeration result is needed for kbest or res.lg0.

Code quotations: `CODE/cpp/v3_start.h:207–213` at lemma lines 15–21 match exactly, including strict comparison and ascending k. No transcription errors.

## L5 — enumeration

**Verdict: WRONG as stated.** Part (A)'s first characterization is false. Parts (B)–(D), and the intended enumeration result in the title, survive the repair below.

1. **False equivalence and invalid converse:** `lemmas/L5_enumeration.md:38–40`. The first RHS requires prefix optimality only for P_0,…,P_{J−1}, together with each block's per-size optimality. It never requires that the chosen last-block size produce an optimal full allocation. It is not equivalent to the parenthetical condition requiring P_J=M[J][R_J]. At proof line 50, “P_J(S)=M[J][k*]” is assumed without justification from that first RHS.

   Concrete counterexample satisfying H1–H3, with even correct inverse maps: p=2, K=1, J=2, C_0=[0], C_1=[1], λ(0)=−10, λ(1)=0, ρ_0({0})=1, ρ_1({1})=2, empty scores zero, cap=100. Then M[1][0]=0, M[1][1]=1, M[2][1]=2, k*=1, and A*={{1}}. Take S={0}. At b=1 its block-0 choice attains μ_0(1)=1 and P_0=M[0][0]=0. At b=2 its empty block-1 choice attains μ_1(0)=0 and P_1=M[1][1]=1. Thus every condition on the first RHS is satisfied, but f(S)=1<2 and S∉A*. The claimed parenthetical equivalent fails because P_2=1≠M[2][1]=2.

   Frozen-harness confirmation on exactly these tables: `R L5-A-counterexample 0x1p+1 1 0 1 1` (lg0=2, one tie, not truncated, returned S=[1]). The counterexample targets (A), not the enumeration code.

   Required fix: add P_J(S)=M[J][k*] to the first RHS, or use the parenthetical all-prefix version as the primary statement, or explicitly require tight transitions M[b−1][R_{b−1}]+μ_{b−1}(|S_{b−1}|)=M[b][R_b] for every b. Under the all-prefix version, line 50 is valid. The forward proof at lines 51–59 is correct and proves that stronger version from membership.

2. **False numerical-order inference:** `lemmas/L5_enumeration.md:106`, “this recovers the visiting order itself, since res.S at cap=c changes exactly when a new lex-minimum is visited.” Observing prefix minima does not recover all visited elements or their order. For example, visit sequences ([0],[1],[2]) and ([0],[2],[1]) have identical returned best set at every cap, identical tie counts, and identical flags, while their orders differ. This can occur within an all-tied singleton model where the first visited set is already lex-minimal. The assertion that a change identifies a new record minimum is true, but does not imply recovery of the non-record visits.

   Required fix: describe the 1,551 runs only as output/count/flag checks against the predicted prefixes. To claim empirical verification of the actual full order, record and compare individual visits in a separately instrumented scratch harness. The proof of (C) itself does establish order and needs no empirical replacement. The same overclaim occurs in `numerics/lemma_probes.py:7–9,69`.

3. **Minor explicit argument worth adding:** at `lemmas/L5_enumeration.md:41–43,63–68`, justify that no call with b>0 is a terminal node: its finite M[b][r] is a maximum of finitely many recurrence terms, at least one of which is finite and tight; L2 supplies a nonempty arg list for that term. Hence every such call has a child. This follows from already proved L2–L3 and introduces no extra hypothesis.

4. The shared instance-count/coverage correction at `lemmas/L5_enumeration.md:107` is detailed under L4.

Remaining line audit: notation at lines 33–34 is valid on feasible sets. The invariant at lines 61–67 preserves both size and objective by exact addition. Lines 68–81 correctly show r=0 at every bottom call, correct assembled subsets, completeness using the valid forward half of (A), and injectivity. Suffix choices are assigned before descent; stale lower-level entries are overwritten before reaching a bottom call. Lines 83–88 correctly derive DFS order from increasing (j,c) child labels. Lines 90–101 correctly stop exactly at min(N,cap), handle N=cap with truncated=true, and keep the lex-minimum of processed sets. Since cap is the function's positive `long` argument, count reaches cap before any further increment; this argument does not require an unbounded integer counter. No assumption equating code order with set lexicographic order is used.

Hypotheses only? **Yes for the repaired proof:** H1–H3 and L2–L4 suffice. Part (A) as written fails under those very hypotheses; strengthening H1–H3 is unnecessary. L1's `comp` gap does not infect this enumeration proof: it uses the table objective, not `comp`.

Code quotations: all 25 numbered lines at `lemmas/L5_enumeration.md:6–30` match `CODE/cpp/v3_start.h:214–238`. Comments, tests, reset, recursion, flag, and assignments all match. No code transcription errors.

## Verification and required fixes

Read the requested source ranges, including table construction, prior construction, preprocessing/original-index propagation, `lex_less`, NEG_INF, and D0/EX-A definitions. All 53 numbered quotation lines in L2, L3/L4, and L5 were also compared mechanically against their numbered source lines, ignoring surrounding indentation: zero mismatches. L1's inline code/formula citations were checked manually as described above.

Reran existing scripts with isolated Python and bytecode writing disabled (`python -I -B ...`):

- `lemma_probes.py 11`: L2=1,500, L3=2,521, L5=1,551; all reported failure counts zero.
- `check_union_order.py`: 17,066 ordered distinct equal-size pairs; zero violations.
- `run_checks.py 20261108`: output matches the stored seed summary; no reported failures/mismatches. FP-only lex differences are permitted by the locked statement and are not failures.
- Sent the two-singleton L5(A) counterexample directly to the existing frozen harness; result recorded above. The L1 malformed-inverse example follows directly from `comp` lines 56–63; no claim of a harness rerun of that malformed object is made.

Required fixes, in priority order:

1. Repair L5(A)'s first RHS and its converse proof; retain its valid forward argument and B–D.
2. Scope L1(ii)'s code identity to valid inverse maps, without treating the (e)-only H1 clause as universal.
3. Supply L1(i)'s exponential-weight normalization argument for arbitrary abstract λ,ρ; label BB/scorer formulas as specialization.
4. Remove the claim that output prefix minima recover traversal order; narrow the numerical claim or instrument visits in scratch.
5. Correct L3's feasible-prefix coverage and the L3/L4/L5 instance-count/assertion-coverage summaries; clarify L1's DATA evidence wording.
6. State explicitly why every finite nonterminal DP state has a tight child in L5(B).

These findings do not refute the intended exact-arithmetic value/size/enumeration conclusions. They do prevent accepting the submitted batch verbatim.
