# Final council, round 3 — Sol

**Verdict: ACCEPT.** The chapter passes G1–G6. I found no BLOCKING, MAJOR, MINOR or NIT issue requiring a chapter edit. In particular, Lemma CAP, A1's corrected Proposition F and the A2/A3 GROW extension are mathematically sound under the premises actually stated. This is an independent seat verdict, not a declaration that the two-seat council has passed.

## Review boundary and evidence

I read `COUNCIL_BRIEF_R3.md` and `COUNCIL_BRIEF.md`, all nine chapter sections and the front matter, and checked the compiled 25-page `consistency.pdf` by text extraction. I compared the statements with the Wave-1 statements/reports, C-PACK's corollaries and amendments, the C-MIS/C-GROW/C-DLV statements and relevant proof files, the SoP method/theory cards, and HQ audits A1–A3. I read the relevant Song–Liang main-paper pages in the supplied PDF, including printed pp. 950–960 and 968–969. I did not obtain or inspect their online Theorem S.

No `FINAL/reviews/C1_council_*.md` or `C2_council_*.md` was opened before this verdict. Historical summaries quoted in the chapter and source reports were not used as mathematical evidence for CAP or either assembly. Disposition checking, if recorded below, occurs after saving this independent verdict.

The engineering source is the brief's immutable snapshot **8a27652599ea65c70b293d42e973950580b6c4df**, read with `git show`. The moving `origin/w1c/ls0-merge` ref now resolves to `493579abecec3339806dae7f917fbe3da4ba386c`; its later preflight changes must not be substituted for the chapter's snapshot. `FINAL/citecheck.py:14` already pins `8a27652`. The chapter's statements that the cited snapshot does not charge the enlarged LS0 term in preflight agree with `8a27652:Theory_work/Wave1C/C-ENG/REPORT.md:62–64`. I used no state-changing git command and created no verification artifacts.

## Gate verdicts

| Gate | Verdict | Reason |
|---|---|---|
| G1 — statement fidelity | **PASS** | The posterior, N1/E, PXN, GEN, GROW, misspecification and delivery statements preserve their source assumptions and conclusions. The explicitly identified C-PACK amendments, A1 correction, A2/A3 extension and CAP transfers account for the changes from the older statements. I found no consequential weakening or scope enlargement without a stated proof. |
| G2 — status fidelity | **PASS** | Ticket-level `PROVED-CHECKED` is kept distinct from registry adoption and from individual proof-file statuses. C-DLV remains `PARTIAL`; its inventory and S.3 remain code-reading audits. CAP and the corrected/extended F statements are not presented as already council-passed. LH's `SAME-FAMILY-ONLY`, N1's unfulfilled Lean item, and the inherited operational premises remain visible. |
| G3 — new mathematics | **PASS** | CAP's exact scan bookkeeping and scored-set monotonicity hold. The amended resource allocation removes resource exits on the stated ideal machine; the complete tier-1 fallback removes the remaining grid exit. Direct data-event arguments then give consistency without importing CAL-bearing headline assemblies. Full checks are below. |
| G4 — Song–Liang map | **PASS** | The map distinguishes density/Hellinger contraction from exact-model selection, sensitivity from specificity, support inclusion from equality, exponential inner/outer bounds from polynomial-rate convergence, and random-design from fixed-design domains. The positive-power lower growth assumption and the missing Theorem-S supplement are disclosed. Theorem 4/Corollary 2 and the binding-cap qualification agree with the main paper. |
| G5 — honest scope/frontier | **PASS** | Polynomial dimension, fixed sparsity, asymptotic onsets, study-size limitations, S5/factor exclusions, shipped-calibration delivery, pooled reported PIPs, EP's size-tail obstruction, quadratic memory, exact arithmetic and unmerged implementation status are all retained. The ideal-machine delivery theorem is not promoted into a reliability guarantee for the binary/default allocation. |
| G6 — internal consistency | **PASS** | The two MR1 labels, the distinction between e4/e4′/some maximiser, the original and enlarged caps, potential versus delivered output, the several PIP objects, and the two different results named F are distinguished. Delivery and cost statements use the appropriate envelopes. The compiled document has resolved section references; its build log reports 25 pages and no undefined-reference or missing-character warning. |

## Independent mathematical checks

### 1. Lemma CAP and the transfer list

**Code/specification check.** `SoP/02_method.tex:463–467,483–500` and `8a27652:Scripts/SMC_BVS/core/cpp/v3_engine.h:379–414` implement the same control flow: evaluate the emitted centre; complete a scan with the centre frozen; select the largest-F neighbour, using ordinary lexicographic order on exact neighbour ties; test strict improvement; only then test the move cap. At a binding cap the improving neighbour is already scored and is returned, but the move counter is not advanced. This is precisely why the final scan is included in CAP. The HPM's separate size-then-lex rule does not enter the choice of the next centre.

For a fixed data set let the uncapped centres be C_0,...,C_m. Strict increase and finiteness give m<infinity. At iteration k the next scan and its chosen neighbour are functions of C_k and F only. A cap a therefore scans exactly C_0,...,C_min(a,m), makes min(a,m) moves, and scores

    {C_0} union union_{0 <= k <= min(a,m)} N(C_k).

When m<=a, the no-improvement test fires before the cap test and both larger-cap searches are identical, including the archive/return/flags of that LS0 search. When m>a, the last returned neighbour is in N(C_a), so it is already included in the displayed scored set. No off-by-one counterexample results from that return convention. This verifies `sections/s7_impl.tex:45–60`, including random data-measurable finite integer caps, pointwise in the data.

`8a27652:Scripts/SMC_BVS/core/cpp/v3_core.cpp:443–481` places LS0 after the pre-existing final search and computes its cap only after obtaining the start mode. It consumes no final uniforms or particles. In the potential uninterrupted specified method, changing the cap leaves calibration and the pre-LS0 run fixed. Exact enumeration has already scored every feasible model; a schedule-limit branch executes neither LS0. These branch cases justify CAP(b), including the common potential-output event. The finite-word cap-range exception is expressly excluded by IDEAL-W; actual runtime stops are expressly not claimed monotone.

On delivered output, GUARD-W identifies the actual and potential scored records. If pi(S_0)>1/2 and the smaller-cap scored set contains S_0, its F is strictly larger than every competitor's F. Thus CAP(c)'s event inclusion follows, and Markov gives the factor 2. The closure bound D_n<=P(LS0 misses S_0) is used in the correct direction.

As an independent control-flow falsification, I ran an in-memory exhaustive check on p=3, K=2: all 3^7 assignments of scores in {0,1,2} to the seven feasible models, every emitted centre, and all cap pairs 0<=a<=a'<=4. All **229,635** comparisons passed the exact move-count/scan-centre/scored-set formula, inclusion and certified-run identity. Including caps below ell_n tests a stronger control-flow property, not a proposed relaxation of the statistical hypotheses. The same enumeration checked all available NA-and-TL lattice cases for a singleton truth; all six starting-centre cases obeyed the asserted deletion descent. These finite checks supplement, rather than replace, the induction and lattice argument.

**Transfer audit.** `sections/s7_impl.tex:67–81` makes the right distinctions:

- PXN discovery transfers by set inclusion. Its certified-return and c+1-scan clauses transfer because their smaller-cap searches have already terminated certified, not merely because of scored-set inclusion.
- GEN retains its every-sequence/common-envelope hypotheses and onset. Discovery needs a>=tau(C)-1; certification needs a>=tau(C). The larger cap preserves both relevant implications.
- C-MIS D/D′ use GEN; H is cap-independent. The M5(b1-LH) discovery statement and SL2 discovery input transfer. Top-c retention remains a property of the update rule, not monotonicity of store contents.
- The pathwise part of C-DLV D′ transfers, while delivery and worst-case cost need the amended allocation. The enlarged count is at most 1+(ell_n+K+1)q(p), with q(p)=p+p^2/4.
- GEN(C6)'s negative small-cap result, off-event flags, archive/store contents and the actual no-output event are correctly excluded from verbatim transfer.

### 2. Proposition F: delivery and LH/LH-iid/GEN consistency

`sections/s6_delivery.tex:28–39` retains A1's corrected method, cap, complete fallback and allocation. The resource increment is sufficient: increasing only LS0's cap by at most K adds at most K scans of q(p) neighbours. C-DLV `lemmas/L1_resources.md:32–43` bounds each request, including cache/store overhead, by C[n^3+p(n+2)]. Extra LS0 path/scanned-centre storage is O(K(K+1)). Therefore W_G and M_G cover the change; the allocation separately covers peak bytes, both preflights, exact-branch timing and the wall guard's elapsed-plus-last-operation test. Polynomial certificate budgets, fixed concurrency and raw dimension are retained. The old time shape is not silently reused.

C-DLV `lemmas/L3_grid.md:35–48` proves that a completed pilot has strictly increasing temperatures from 0 to 1 and at most T_1 intervals: every nonfinal increment is at least 1/T_1. A successful construction has the same endpoint/progress/cap properties. Hence either fallback candidate is a complete valid frozen grid. There is no need for its restricted ESS to pass. A failed or partial prefix is not a candidate.

At the pinned code snapshot, `v3_calib.R:120–126` retains the last successful construction after a rebuild failure, or the completed tier-1 pilot after a preliminary failure. `v3_calib.R:141–190` carries it through validation and the ordinary freeze using tier-1 budgets and inherited scored state. Numerical/resource stops return earlier and are not disguised as fallback success. The first failed construction terminates the tier without retries.

Under EX-A, H=(n+1)G+I and G+I are positive definite and Q>=y'y/(n+1)>0, so scoring cannot introduce a numerical stop. Gaussian noise makes a constant response null; the stated nonconstant-column assumptions eliminate predictor degeneracy. MACH/IDEAL-W and the allocation exclude the remaining operational/resource exits, relative to the expressly inherited exit audits. Replacing schedule_limit by the complete fallback therefore gives P(no output)=0 for every admissible n>=3. This is an ideal-machine statement with essential premises, not a statement about every numeric input or physical execution.

For consistency, let K_n denote deterministic LS0 discovery. The data-only PXN(T)/(P), GEN(C1)/(C2) and T03-sharp inputs used by DLV `lemmas/L4_delivery.md:56–77` give P(K_n^c)->0 and E[1-pi(S_0)]->0 under their respective hypotheses. CAP preserves discovery for the enlarged cap. Pointwise on output and K_n, posterior mass above 1/2 forces the reported HPM to be S_0. Consequently

    P(output and HPM != S_0)
      <= 2 E[1-pi(S_0)] + P(K_n^c) -> 0.

Delivery then removes the output qualifier. Neither the old CAL-bearing assembly nor an estimate of fallback probability is needed. LH's SIZE/instance-status qualification, LH-iid's SIZE and p_n->infinity, and GEN's full statistical/envelope hypotheses remain necessary and are retained.

### 3. Proposition F-GROW

`sections/s6_delivery.tex:45–51` uses A2 with all five A3 amendments. The input/numerical extension is valid: fixed GROW columns are nonconstant; each iid AR(1) raw column is nonconstant almost surely; conditional on X the centred noise is nondegenerate on 1-perp, even though raw beta may depend on the column scales. Thus the retained p equals deterministic p_raw almost surely. Ridge positivity needs neither full-design rank nor bounded relevance, so p>>n adds no scoring obstruction. The same enlarged resource proof gives delivery.

For the statistical part the proof starts with the three data events, rather than trying to infer discovery from D_n->0. On Sand intersect NA intersect TL, every start maximiser lies between S_0 and Q. For any extra j in a centre T, NA at T\{j} makes deletion of j improve F. An addition is worse by NA at T; a truth-losing neighbour is worse by TL; an extra-for-null swap is worse than the corresponding deletion by NA at T\{j}. The best improving neighbour must therefore delete one extra. Iteration reaches S_0 in exactly |T\S_0| moves. The stated cap exceeds that number and the emitted-centre convention covers T=S_0.

It follows directly that P(K_n^c) is bounded by the three event-failure probabilities. Fixed designs obtain these from GROW under (H0),(G1)–(G4). Exact-Gram AR(1)'s piecewise relevance set ensures feasibility/K-gap eventually, its Markov regression gives the required direction count, and the separation condition supplies truth visibility. For iid AR(1), L6 supplies the three events jointly; the chapter correctly does not claim fixed-design NEG or exact G4-dir on its random realisations.

For the posterior input, fixed designs use T03-sharp under (H0). L6.2 and `C-GROW/lemmas/L6_random_AR1.md:478–489` give the iid design events with common constants/envelopes; a violating sequence would contradict the fixed-design theorem, yielding the joint-law limit. Bounded posterior miss then gives its expectation limit. Combining with the same pointwise inequality and delivery proves the claimed unconditioned consistency. Fixed-p enumeration, the diagnostic S5 population instance, the exclusion of random-row S5/growing factor designs, and the absence of a study-n=200 guarantee are stated accurately.

## Numbered findings

1. **None.** No BLOCKING, MAJOR, MINOR or NIT finding requiring replacement text. The acceptance is for the specified method and the pinned source snapshot, with the chapter's recorded implementation/audit/statistical qualifications intact.

## Post-verdict disposition check

After saving the independent verdict and score above, I read only `C1_disposition.md` and `C2_disposition.md`, not the earlier council review files. I checked their listed repairs against the current chapter. No unresolved earlier finding was identified; the verdict and score are unchanged.

- **C1 Sol S1–S5:** fixed-data/stream-only expectations are explicit in `sections/s4_sampler.tex:5`; Theorem F's contrast coordinates, full-mean energy and both cutoff discharges are in `sections/s3_posterior.tex:49`; GEN's favourable random-design alternative is in `sections/s5_hpm.tex:52`; Theorem D/D′ use the sufficient allocation in `sections/s6_delivery.tex:8,12,19`; BM(c), empty maxima and the coded-routine e4′ conditions are supplied in `sections/s3_posterior.tex:11,24` and `sections/s5_hpm.tex:13,16`.
- **C1 Opus O1–O14:** the cap/allocation distinction and limits on transfer are in `sections/s7_impl.tex:72,78–81`; the fallback and audit qualifications are in `sections/s6_delivery.tex:31,55`; some-maximiser versus unique-maximiser requirements, both MR1 labels, status distinctions, Song–Liang Condition 4, sharpness conditions and PXN's full probability conclusions are present at the locations independently checked above. The implementation statements describe the pinned unmerged branch, not a completed merge or registry adoption. The title/byline and source date are supplied explicitly in `consistency.tex:6–9` and `preamble.tex:37–38`.
- **C2 Sol 1–3:** the formerly missing threshold domain and deterministic-sequence quantifiers are explicit in `sections/s1_setting.tex:13`, `sections/s3_posterior.tex:27` and `sections/s2_map.tex:17`; the misspecification frontier now includes the proved EP and null-projection alternatives in `sections/s8_scope.tex:11`; the author block is split across `consistency.tex:6–8` and the extracted PDF contains the complete byline.
- **C2 Opus 1–10:** random-GEN nonconstant-column regularity, ideal-machine wording, the finite-word cap exception, fixed-concurrency constants, joint-law algorithm randomness and the e4 delivery qualification appear in `sections/s6_delivery.tex:33,39,47`, `sections/s2_map.tex:18,31`, `sections/s7_impl.tex:39` and `sections/s8_scope.tex:15`. The cap/example wording is in `sections/s7_impl.tex:25,74`; CAP's provenance and the title-source disposition commit are in `sections/s9_prov.tex:28` and `consistency.tex:9`. The optional additional fallback citation was explicitly not required. The citation checker pins the intended engineering commit at `citecheck.py:14`.

SCORE: 9.3/10; GATES: G1 PASS; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 PASS
