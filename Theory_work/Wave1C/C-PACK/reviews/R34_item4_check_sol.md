# R34 — Independent adversarial review of item 4 and the Song–Liang map

**Verdict: ERROR as written.** The error is local: SL0(vi)'s attainment claim is false within the D0 posterior class specified in §0. Its construction proves sharpness for arbitrary finite probability laws, a larger class. SL0(i)–(v), the posterior-to-summary asymptotic transfers, and SL2's event argument survive independent checking, subject to the explicit boundary conventions below. The map also needs a substantive correction to the scope of Song–Liang's misspecification results. Neither issue requires withdrawing the main exact-posterior or store-restricted consistency implications.

This is a review of the files as read on 2026-11-08, not an edit or adoption of their statements. Only files under `Theory_work/Wave1C/C-PACK/` were written. No git command was run. The two target source files were left unchanged. All paths below are relative to `C:/Users/felip/Bayesian-Variable-Selection/`, unless absolute. `SoP` means `Theory_work/State_of_Project/sections`; `W1` means `Theory_work/Wave1`. Quotation marks identify exact source fragments; proposed replacements are labelled separately.

The attached Song–Liang PDF was extracted locally and its complete journal pages 952–958 were also rendered and visually inspected. Text extraction drops some relation signs; in particular, the strict sparsity condition counts **nonzero** coefficients, and Conditions 3 and 5 contain quantitative/nonzero inequalities. The review uses the page images for those signs. The supplied PDF contains the main article, not the online supplement. I do not certify the missing proof or hypotheses of Theorem S.

## Numbered findings and replacement text

### 1. MAJOR — SL0(vi) is not an attained D0 bound

**Locations:** `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:8`, `:21`, `:30`; `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:14`.

The objects section starts with:

> π is the exact posterior of the method's target (D0: shipped g = n score, a₀ = b₀ = 0.01, normalised capped BB(1,p)

SL0(vi) then says:

> (vi) The bound in (i) is attained: there are posteriors with max_{j∈S₀}(1 − PIP_j) + max_{j∉S₀} PIP_j = 2δ.

The proof assigns all probability to two models. That is a valid finite law, but a finite-data D0 posterior assigns **strictly positive mass to every model in Ω**, including the empty model. The ridge matrices are positive definite even when X is singular; the IG score and capped prior weights are positive. See `SoP/04_theory.tex:70`–`:72` for the formulas.

For a nonempty proper feasible truth, and any false coordinate k,

```
PIP_k <= pi(S != S0, S != empty) = delta - pi(empty) < delta.
max_true(1-PIP_j) <= delta.
```

Consequently the displayed max-sum is strictly less than `2 delta` for every such D0 posterior. Since Ω contains at least one other model, `delta > 0`. This is a general obstruction, not just a failure of the proposed example. The two-point construction also needs `1 <= s0 <= K` and `s0 < p` to choose j, k and a feasible same-size swap. It does not establish sharpness for an empty or full truth.

**Fix text:**

> (vi) As a bound over arbitrary probability laws on Ω, the constant 2 in (i) is sharp when 1 ≤ s₀ ≤ K and s₀ < p. Put mass 1−δ on S₀ and δ on a feasible one-for-one swap. This is not an attainment claim for the strictly positive finite-data D0 posterior.

Change map row 5's `bound 2δ for max-sum is attained (SL0(vi))` to `the constant 2 is sharp over arbitrary finite laws (qualified SL0(vi)); exact D0 attainment is not claimed`. Do not replace this with a claim that the constant is sharp *within the D0 class* without a separate approximating-design argument; none is supplied here.

### 2. MAJOR — The map's global capped-prior heading misstates the scope of Theorem 4 / Corollary 2

**Locations:** `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:8`, `:19`, `:20`; Song–Liang journal pp. 956–958, especially p. 958 remark (c).

The heading presents their setting as:

> content (their setting: random x, prior λ_n = r_n/P_n with size cap r̄_n, g-type V_ξ, IG(a₀,b₀))

Rows 10–11 only give the conclusions. But Theorem 4 concerns a **given fixed candidate subset s**, Condition 4's finite second moments, Gaussian coefficient/IG priors, and a model prior positive on **all** subset models. It gives almost sure Hellinger concentration about the KL-minimizing density f₀. Corollary 2 additionally assumes **no exact multicollinearity in x_s**. Its conclusion is inclusion of the projection support, not equality to it and not concentration on a single model.

On p. 958(c) the authors explicitly say:

> although corollary 2 does not hold anymore

when discussing the imposed size constraint. Their subsequent capped screening suggestion is not Corollary 2 as proved. Thus the global header silently puts a theorem under a prior that can violate its premises. The D0 cap becomes nonbinding eventually for fixed p, but this does not license the same transfer for a growing candidate set. Also V_ξ is a general positive-definite covariance in the theorem, not required to be a particular g-prior.

**Fix text for the heading:**

> Content (random-design setting; correct-specification prior from §2.1 unless the row states otherwise; V_ξ positive definite).

**Fix text for row 10:**

> Given fixed s, under Condition 4 and Gaussian/IG priors with positive prior mass on every subset model, π{d(f,f₀)>ε | D_n^s}→0 almost surely for every ε>0; f₀ is the KL projection. No growing-|s| or binding-cap extension is established here.

**Fix text for row 11:**

> Under Theorem 4's premises and no exact multicollinearity, π(s̃⊆ξ | D_n^s)→_P1, s̃=supp β₀, β₀=Σ_s⁻¹cov(x_s,y). This is screening of projection coefficients, not exact model selection. The paper explicitly withdraws Corollary 2 under a binding model-size cap (p. 958(c)).

Keep C-MIS labelled as a separate ticket, not a delivered result of C-PACK. At inspection its `STATEMENT.md:3` says `**v1 DRAFT (submitted for statement lock)**`; there is no final C-MIS report. The SoP comparison at `04_theory.tex:240` and the FW21 status at `04b_supplement.tex:1279` are genuine source statements, but neither proves a misspecification analog.

### 3. MINOR — Boundary conventions are missing from otherwise correct lemmas

**Locations:** `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:15`, `:37`, `:41`, `:56`, `:80`.

The displayed maxima over S₀, its complement, and J_n(c) are undefined when those index sets are empty. In particular the source explicitly notes that J_n(c) can be empty (`SoP/04_theory.tex:782`), whereas SL1′ displays its maximum without a convention. Likewise an empty true support and a full true support are allowed by §0.

SL1(d) evaluates h(S₀) with h only defined on Ω. For deterministic S₀, `delta_n→_P0` forces eventual feasibility (otherwise delta is identically 1 along an infinite subsequence), so its asymptotic conclusion is repairable. For arbitrary random S₀ the expression still needs an extension on the infeasible event. SL0(ii) itself correctly restricts its h clause to `s₀ ≤ K`.

The final clause of SL2 needs **positive** tolerances. Literally, `r_n=o(t_n)` also permits `t_n=-1`, when the bad event is all of 𝒪 and its probability need not vanish.

**Fix text near the objects:**

> Every maximum of the nonnegative errors over an empty coordinate set is defined as zero. For summary statements involving h(S₀), assume S₀∈Ω eventually, or define h on Ω∪{S₀} with the stated range on that union. Rate sequences and error tolerances are deterministic and positive.

Also replace `for every t_n with r_n = o(t_n)` by `for every deterministic t_n>0 with r_n=o(t_n)`.

No counterexample to (i)–(v) remains after these conventions. For s₀>K, delta=1, the event bounds and size bound are trivial, and the threshold/HPM antecedents fail. At delta=1/2, HPM ties and MPM errors are possible; the strict inequality in (iv) is essential. For strict `PIP>q`, the weaker sufficient condition `delta<=q` and `delta<1-q` is available, but the stricter condition actually printed in (iii) is valid and needs no repair.

### 4. MINOR — State the GEN joint rate and the LH rate with the sources that actually supply them

**Locations:** `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:47`, `:50`, `:52`, `:79`.

The heading promises `δ_n = O_P(r_n)` instances. I-c explicitly cites only fixed-design convergence/expectation in `W1/W1-GEN/lemmas/L5_assembly.md:37`–`:38`, then notes a rate on X-events. The stronger joint rate is valid under the stated (C4) quantifiers, but that short transfer should be written. I-d says `rate as there`, although the cited `SoP/04_theory.tex:845` only prints `π(S₀)→1`.

For GEN, `STATEMENT.md:115`–`:120` requires every deterministic design sequence in the high-probability X-sets to satisfy H0–H2 with the same constants and envelopes. T03♯ therefore applies at the same rate along **every** such sequence. The diagonal tightness argument used explicitly in PXN gives the joint rate: if conditional `delta_n/r_n` were not uniformly tight over those X-sets, choose successively larger thresholds, increasing indices and violating designs to build one deterministic sequence along which tightness fails. The complement of the X-set has probability tending to zero. Mere almost-everywhere conditional convergence, without these sequence quantifiers, would not suffice.

**Fix text for I-c:**

> Under GEN (C4), δ_n=O_P(√(log n/n)) under the joint law: apply T03♯ along every deterministic sequence in its X-events and use the diagonal tightness transfer of PXN P8♯, step 4. Hence Eδ_n→0. Sources: GEN STATEMENT.md:115–120, L5_assembly.md:57–77; PXN lemmas/P8_T03sharp.md:45–55.

**Fix text for I-d:**

> On the shared LH exact-Gram family, the hypotheses of S-T hold, so δ_n=O_P(√(log n/n)); M3(f) also records π(S₀)→1. Sources: SoP 04_theory.tex:775–782, :793, :824, :305. Thm5-LH retains its recorded SAME-FAMILY-ONLY status.

Finally, the PXN citation `FINAL_PROOF.md:68-73` in SL2 does not contain its scored-set event inclusion: it is at `:75`–`:79`. The actual inclusion is correct. Replace the citation with that range. For GEN cite both `L5_assembly.md:11`–`:16` (closure) and `:24`–`:38` (vanishing D_n); for its random-design extension cite `:66`–`:77`.

### 5. MINOR — Keep scalar stacking consistency distinct from simultaneous sure screening of p_n PIPs

**Locations:** `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:67`–`:71`; `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:17`.

The exact wording of M1(i)'s status is retained, but the surrounding screening discussion can suggest that logarithmic stacking already controls the maximum over all p_n inclusion probabilities. The clerk's integration note is narrower. `SoP/04_theory.tex:111` says:

> for a fixed finite set of declared summaries on families with D$_{*}$ = O$_{P}$(1)

and introduces the second configuration:

> R′$_{n}$ = 4⌈(n + p)⁶/4⌉ for simultaneous control over ≤ (n + p)² declared summaries

One cannot upgrade fixed-finite-list consistency to a growing-list maximum just by calling it a sure-screening analog. SL1(a) is different: its exact-posterior uniformity is supplied deterministically by delta, with no union bound.

**Fix text for R3 / row 8:**

> The cited cards contain no in-probability sure-screening theorem for the pooled shipped-R′=4 estimator. M1(i), status unchanged, supplies with-output consistency for a fixed finite list at R′_n=4⌈log₂(n+p+1)⌉ under its T03♯, discrepancy and implementation premises. For simultaneous control of a growing declared list, the card specifies the separate polynomial stacking configuration in its integration note; no uniform-p conclusion is inferred from the fixed-list statement alone.

The historical negative statement is accurate **for the cited cards/reports and the pooled SMC estimator**, including `W1/W1-N1/lemmas/R_remarks.md:29`–`:32`, which explicitly leaves the pooled clauses unproved there. It is not an impossibility theorem. In particular, a vacuous displayed M1(f) bound does not prove that no better fixed-R argument can exist. The exact-enumeration branch and store-restricted PIPs should remain separate scopes.

R2 is faithful for the **plain measured-endpoint** PIP: W1-N1 REPORT `:23`–`:31` identifies h=1{j∈S} with `pip_plain[j]` and gives the sharper delta bound. Add the source's localization, `a.s. on 𝒜∩{r≤R′}, for the potential run`, and retain the named START/KERNEL/CAL/MEAS premises. It does not identify the statistic with every shipped PIP field: `SoP/02_method.tex:1021` says `pip_primary` in the code/study is the equal-weight RB statistic. W1-N1's own status is a Wave-1 result, not a retroactive update of the frozen SoP N1 status.

### 6. MINOR — Own-result statuses and some input statuses are not actually presented verbatim

**Locations:** `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:3`, `:87`–`:99`; `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:6`, `:14`, `:17`, `:22`.

The lemma file calls every new statement:

> Status of each statement: PROVED (by this seat)

The binding Wave-1 protocol explicitly specifies `PROVED (by this seat, unchecked)` for an author-only proof; the new results do not become checked by pointing to a reviews directory. Likewise map row 13 uses `as carded` in a column promised to be verbatim, without giving M8's assembly status. The I-d input Thm5-LH's status is absent from §4 even though it is used in that instance. M3(f)'s final assembly status is not an independently checked result either.

**Fix text:** use `PROVED (by this seat, unchecked), pending R34 disposition` for the new author statuses, then record the actual R34 verdict and accepted corrections separately. Add the literal registry fragments for the newly used inputs:

From `Theory_work/Old_Projects/New_BVS_Headquarters/ID_REGISTRY.md:25`:

```
Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY**.
Final assembly: **PROOF SKETCH, unchecked**.
```

The two fragments above occur in the registry's TH03 row; use that row as the exact textual citation. For M8 use the registry's TH08 row (`ID_REGISTRY.md:30`), including:

```
MA-PropD "PROVED (counting, given the code's structure)" AUTHOR-ONLY
assembly PROOF SKETCH (by this seat, unchecked).
```

**What did pass the substantive status audit:**

* T03♯'s fragment matches `SoP/04_theory.tex:765`, `:788`; M1(i)'s fragment matches `:130`; neither is upgraded in §3.
* M4(a)'s candidate / not-reviewed / not-adopted / AUTHOR-ONLY qualifiers are preserved. M4(b)'s actual raw-TeX clause status at `:411` is `same as (a); W1PC1 §3 B.D3(b) COUNTEREXAMPLE repaired with ‖h‖$_{∞}$`; §4 expands the inheritance and transcribes the math. This is substantively faithful but should be labelled an expanded rendered quotation, not byte-verbatim text. M4(c)'s `N13: PROVED (PC1 claim 5)` is exact at `:412`.
* M5(0)'s fragment matches `:489` / `:843`. M5(b1-LH)'s verified-star qualifiers and `N3 "OPEN"` are preserved. Its source `:491` also explicitly excludes the conflicted iid subclaim; keep that exclusion when expanding the quote. No inference about LH-iid should be taken from that conflicted subclaim; use PXN instead.
* W1-PXN REPORT `:4`, `:49` and W1-GEN REPORT `:20`, `:63` support the reported Wave-1 `PROVED-CHECKED` / `XF VERIFIED` descriptions. W1-N1 REPORT `:47` really contains `PROVED under the same premises`. Their frozen-registry statuses are distinct and are not automatically upgraded.
* The e4 replacement is a new C-PACK lemma (`lemmas/I1_e4_replacement.md:120`–`:133`), not a modification to the old registry. Its exact-arithmetic uniqueness route retains LS0 integration as a premise; binary64 additionally needs FP-TAB. Saying “N3 replaced” must not erase those premises or claim the full tie invariant is proved.

### 7. MINOR — The map omits a Corollary 1 branch and Theorem 3's weaker conclusion

**Locations:** `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:12`, `:13`, `:14`; Song–Liang pp. 953–956.

Row 3 only gives the logarithmic-size-cap branch of Corollary 1. The PDF also gives the polynomial-cap alternative, subject to `0<q<min{1−α,1/v}`, with rate

```
epsilon_n = O(n^{-min{1-alpha-q, 1-v*q}/2}).
```

Its common premises include strict sparsity, `P_n<exp(C n^alpha)`, the prior setting, bounds on B(r_n) and B-tilde_n, and the assumptions of Theorem 2. Row 5 omits the second part of Theorem 3, which replaces the exponential **outer** probability bound by convergence to zero when Condition 2 replaces Condition 1. Equation (16) still uses an exponentially small **inner** posterior threshold; it is not a quantitative O_P rate for our delta.

**Fix text for row 3:** state both branches, including `r_n<r̄_n=o(log^k n)` or `r_n<r̄_n=o(n^q)`, their respective rates, and the covariance/prior conditions. Define this q separately from the PIP threshold q.

**Fix text for row 5:**

> Under Theorem 2 and identifiability, the displayed exponential bound holds for each true predictor. With Condition 2 replacing Condition 1 (other premises retained), the same failure event has probability →0, without the exponential outer rate. This is sensitivity only.

Row 4's informal second-moment / convergence-in-probability description is otherwise faithful. To avoid suggesting that second moments **alone** suffice, append `with the remaining Theorem 2 prior, sparsity and growth conditions retained`.

For completeness, row 2 should mention Theorem 2's `r_n→∞` and conditions (9)–(14), in addition to Condition 1 and strict sparsity. These omissions do not invalidate our posterior analog; they matter to a faithful source map.

### 8. MINOR — Condition 3 needs quantitative separation, not just absence of exact mimicry

**Location:** `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:18`; Song–Liang p. 955.

The row paraphrases Condition 3 as:

> no linear combination of ≤ r̄_n others mimics x_k

This captures the interpretation but loses the rate condition. The page image requires, uniformly over the competing predictors and coefficients, an exponential residual-moment gap `delta_SL,n >> epsilon_n^2`. Non-exact linear dependence alone can hold while that gap shrinks too fast. The covariance-floor sufficient conditions in the ensuing paragraphs also depend on epsilon_n (and, for the bounded-predictor example, r̄_n).

**Fix text:**

> Quantitative identifiability: uniformly over ≤r̄_n other predictors and real coefficients, E exp{−(x_k+Σ_i b_i x_ji)^2}≤1−delta_SL,n, with epsilon_n²=o(delta_SL,n). Our SE_λ/SE_w plus beta-min assumptions play a related identifiability role for selection, but are not asserted to be equivalent to this random-design condition.

The new name `delta_SL,n` prevents a collision with our posterior miss delta. GEN H1's Gram floor and H0's T03♯ conditions are genuine cited hypotheses (`STATEMENT.md:48`–`:59`); the analogy is descriptive, not a theorem ordering the two assumption classes.

### 9. MINOR — Qualify the complexity rate and finish the source-map coverage

**Locations:** `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md:3`–`:5`, `:17`, `:21`, `:22`; Song–Liang pp. 958–960, 968–971.

Row 13 says:

> K_n = √P_n splits, O(P_n^{(1+α)/2}) + O(nP_n)

The paper states the order `K_n=O(√P_n)` in a parallel analysis with enough processors, about equal subset sizes, `T=O((P_n/K_n)^alpha)`, the stated small-model inversion-cost assumption, and controlled average numbers selected per subset. The serial bound is different. This is a conditional cost accounting argument, not a sampler accuracy/mixing theorem. The source's α here is the simulation-iteration exponent, distinct from α in exponential-dimension Corollary 1.

**Fix text for row 13:**

> §6, p. 968: under the stated subset/model-size/iteration assumptions, enough processors and K_n of order √P_n, parallel time O(P_n^{(1+alpha_MC)/2})+O(nP_n); the paper also gives a serial bound with an additional √P_n factor. This is a conditional accounting comparison. Our M8 remains an accounting remark with its recorded statuses and no same-order, exact-output or speed claim.

The main numbered results are all represented: Theorems 1–4 and Corollaries 1–2, plus the main-text reference to supplementary Theorem S. No additional numbered main-article theorem is missing. Supporting results/qualifications still worth including are Condition 4 and the cap caveat (finding 2), Corollary 1's second branch and Theorem 3's second conclusion (finding 7), equation (19)'s projection identity, and §2.3's “iterate until no predictors are selected” guarantee under Condition 5. The latter is not a two-iteration theorem: the paper's choice of two iterations on p. 958(b) is its practical implementation.

Row 12 correctly quotes Condition 5 and GEN REPORT `:48`–`:49`'s description of the block certificate as allowing violations. It should still say this is an analogy: zero block-regression coefficients and zero full marginal covariance are different objects. The cited dedicated R32 review exists and is `VERIFIED-WITH-AMENDMENTS`, not an unqualified new adoption of GEN.

Row 8 should cite §3.2, p. 959, for SAMC's importance-weighted estimated quantities, and §7, p. 969, for the paper's explicit approximate uncertainty interpretation after screening. These are different from the exact posterior q_j defined on p. 955; the numerical estimation statement is not itself Theorem 3. Do not import the discussion's qualitative subset/full-PIP comparison as a proved monotonicity theorem.

The opening assertion that “only” the p. 956 sentence about Theorem S is available is too literal: pp. 959, 960 and 971 also discuss it. None gives the complete theorem or its proof, so the actual limitation is correct. Replace with:

> The supplied main article references Theorem S and describes its purpose, but does not contain its exact statement or proof; those hypotheses are not compared here.

## Independent mathematical audit of the surviving statements

### SL0 and SL1

For any event B, its indicator differs from its value at S₀ only off S₀. Thus

```
|pi(B) - 1_B(S0)| <= pi(S != S0) = delta.
```

This establishes all coordinate and joint-inclusion claims, including A=empty (both sides exactly 1 before subtraction), A infeasible, and an infeasible truth via the delta=1 extension. For feasible S₀, subtract h(S₀) inside the posterior sum to obtain the oscillation bound. In fact

```
sup_{0<=h<=1} |pi(h)-h(S0)| = TV(pi, pointmass_S0) = delta,
```

so SL1(d) is uniform over all such summaries without any cardinality restriction. This is a finite-law identity, not an empirical-process assertion.

The q-threshold argument is correct: true PIPs are at least `1−delta>q`, false PIPs are at most `delta<q`. At q=1−delta a true PIP can tie q and be excluded. At q=delta a false PIP can tie and is excluded by the strict rule; hence the printed symmetric condition is sufficient but conservative. If delta<1/2, the truth has more than half the total mass and is the unique mode, regardless of tie rule. Size concentration follows because the size-s₀ event contains the truth; if s₀>K, both its mass and `1−delta` are zero.

With positive `r_n→0` and `delta_n=O_P(r_n)`, delta tends to zero in probability. Boundedness in [0,1] gives expectation convergence without claiming any expectation **rate**:

```
E delta_n <= epsilon + P(delta_n>epsilon),   epsilon>0.
```

This is bounded convergence **in probability / uniform integrability**, so almost-sure convergence is not needed. The label “bounded convergence” in the source is acceptable with that interpretation. For a_n=min(q_n,1−q_n),

```
delta_n/a_n = (delta_n/r_n) (r_n/a_n) = O_P(1) o(1) = o_P(1).
```

No independence assumption is used. HPM failure implies `delta_n>=1/2`, so Markov yields exactly `P(HPM!=S0)<=2 E delta_n`. The size deficit is between zero and delta. These justify every SL1(a)–(e) conclusion after the domain conventions in finding 3.

**Instances checked:** I-a is exactly the T03♯ statement at `SoP/04_theory.tex:782` with all hypotheses at `:775`–`:778` retained. I-b is genuinely a joint-law rate, not a conditional heuristic: PXN `lemmas/P8_T03sharp.md:23`–`:24`, `:36`–`:55` verifies the high-probability sparse-design event, fixed-sequence T03♯ application and de-randomisation. The random design is independent of the Gaussian noise. It permits any fixed polynomial exponent A and does not require p≤n. I-c is valid under GEN (C4)'s every-sequence and common-envelope hypotheses, with the short additional rate transfer in finding 4. I-d follows by applying T03♯ directly to shared LH: fixed support, positive full normalized Gram floor, bounded energy, fixed nonzero coefficients and p of order n^(1/3). Merely quoting M3(f)'s limit would supply consistency but not the displayed rate.

**SL1′ checked:** for j∈J_n(c), `{j∉S}⊆{S⊉J_n(c)}`. Taking the maximum gives the same T03♯ posterior miss rate without any factor |J_n(c)|. It keeps R1/G/R/SE hypotheses while removing beta-min; it does not prove a random-design extension or specificity by itself. An empty J gives zero under the convention in finding 3. Its threshold and c₀ match the card.

### SL2: the scored-set reading, the store, and output events

M4(b) and M4(c) are applied correctly, subject to their statuses and named premises. Here is the source identification that the short proof leaves implicit:

* `SoP/04_theory.tex:397` defines 𝒮 as **the set of scored models**, 𝒯 as the **nonempty deduplicated reported store**, and π_𝒯 as π conditioned on 𝒯. This is not the particle support or a weighted particle approximation.
* `SoP/02_method.tex:468`–`:478` defines the HPM over **every model ever scored**, including tables, calibration, rejected proposals and searches. `:494` adds every LS0-scored model to the all-scored set and stores. M5 denotes that extended set by 𝒮⁺. Thus taking M4's 𝒮 to mean that run's 𝒮⁺ is justified; it does not identify the bounded store with the full scored set.
* `SoP/02_method.tex:486` gives the top-40p+1 target-score store. `:503`–`:505` states exactly the LS0 union-then-top-c update. The scored set grows; the bounded store need not be nested. Under exact scores/order, top-c of a previous top-c and new candidates is top-c of all candidates. Hence a unique global posterior maximizer, once scored, cannot be evicted when c≥1.
* The actual existing ledger confirms the top-store operation, not LS0 integration: `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp/v3_ledger.h:49`–`:56` inserts and removes only the worst entry; `:79` sets cap=40p+1; `:90`–`:95` offers every fresh score to the HPM/top stores. Inheritance/worker equivalence, SR, EX-A and OP-LS0 remain premises. `SoP/02_method.tex:1018`–`:1020` explicitly distinguishes the spec from the production core. This review does not certify an integrated LS0 that was not present in that core.

M4(b)'s marginal bound is indeed delta, not 2delta: if S₀ is stored, π(𝒯)≥π(S₀)=1−delta, and `TV(pi_T,pi)=1−pi(T)<=delta`. Any coordinate event differs by at most that TV. This confirms the use of M4(b) independently of its AUTHOR-ONLY provenance.

M4(c) is also directly re-derived: on `delta<1/2`, S₀ is the unique best posterior model, so if it belongs to the all-scored set, top-c retains it. Exact score ties cannot affect that conclusion. The store's own MPM then equals S₀ because `pi_T(S0)=pi(S0)/pi(T)>1/2`. This also explains why unqualified retention without the half-mass condition would be false.

For PXN, `FINAL_PROOF.md:75`–`:79` explicitly gives

```
O intersect {S0 notin S+}
  subset potential-O intersect {S0 notin potential-S+}
  subset {potential LS0 does not score S0}.
```

The middle probability is D_n in the ticket's convention. The bar on potential-O is **not** set complement. The exact branch only helps when the truth is feasible; finite n with infeasible truth uses its zero extension. GEN `L5_assembly.md:11`–`:16` gives the same closure under its named implementation premises, `:24`–`:38` makes D_n vanish, and `:66`–`:77` transfers both relevant events to the random-design law. Therefore both do supply `P(O intersect {S0 notin S+})→0`. No conditioning on successful output is used.

Consequently SL2's printed proof is valid:

```
P(O intersect {max_j |PIP^T_j-1_true(j)| > 2 delta_n})
 <= P(O intersect {S0 notin S+}) + P(delta_n>=1/2)
 <= D_n + 2 E delta_n -> 0.
```

For positive t_n, add `P(2delta_n>t_n)` to obtain the second result when `r_n=o(t_n)`. One can even sharpen the pathwise 2delta_n to delta_n once truth is stored, by applying SL0 directly to π_𝒯 and observing `1−pi_T(S0)<=delta_n`; the weaker printed constant 2 is correct. This is a **with-output** uniform PIP theorem, not a guarantee that P(O) tends to one.

### Map row-by-row disposition

| Row | Independent disposition |
|---|---|
| 1 — Theorem 1 | Hellinger tail formula and page correct. Retain boundedness, approximate sparsity (3), prior/eigenvalue conditions (8)–(14), and n ε_n²→∞. SoP FW20 and T03♯ citations opened and support exactly the stated lack of a delivered Hellinger analog and the separate selection result. No superiority in contraction is established. |
| 2 — Theorem 2 | Same Hellinger conclusion under Condition 1 and strict sparsity; correct at the stated level, with the missing r_n/growth qualifications in finding 7. PXN/GEN are correctly separate random-design selection analogs, not Hellinger analogs. |
| 3 — Corollary 1 | Displayed logarithmic branch correct; second branch missing. FW18 citation is exact in substance, and exponential p is not claimed for our theorem. See finding 7. |
| 4 — Condition 2/(16) | Correct convergence-mode comparison, with remaining hypotheses retained. No exponential expectation rate for our delta follows from O_P. |
| 5 — Theorem 3 | Exponential sure screening for each identifiable true predictor is faithfully transcribed. Add its weaker Condition-2 conclusion. Our exact-posterior uniform specificity is valid under its stronger selection hypotheses; attainment needs finding 1's correction. |
| 6 — ξ_q | Correct strict-threshold definition and screening interpretation. The paper prints a π(t⊂ξ_q) notation although ξ_q is a data function; a clean comparison is P*(t⊆ξ_q)→1. Fixed finite true support permits this consequence of Theorem 3. Our equality/MPM statement is justified by SL0, with its own assumptions. |
| 7 — Theorem S | Correctly refuses to claim the unavailable hypotheses have been checked. Exact HPM and reported scored-set HPM are different results. The latter is with output and LS0 premises, with no delivery claim. The SoP :491/:500 and item-1 citations were opened; the source's excluded iid conflict is not used to justify PXN. |
| 8 — reported PIPs | Islandwise delta bound and unchanged M1(i)/M4 statuses are substantively faithful. Add localization, the distinction from code/study RB primary, fixed-list/growing-list scope, and actual SAMC/discussion sources (findings 5, 6, 9). It does not prove pooled shipped-R′=4 sure screening. |
| 9 — Condition 3 | Qualitative intent correct, quantitative condition missing. See finding 8. GEN/T03♯ cited hypotheses exist; no equivalence is proved. |
| 10 — Theorem 4 | Conclusion direction correct; fixed candidate-set, positive-all-model-prior, Condition-4 and almost-sure scope must be explicit. C-MIS remains a separate draft at inspection. See finding 2. |
| 11 — Corollary 2 | Inclusion of projection support correct; no-exact-collinearity and binding-cap warning missing. FW21 is an open analytic-separation item, not a completed analog. See finding 2. |
| 12 — Condition 5 | Nonzero marginal covariance requirement and GEN's quoted descriptive analogy are correct. Keep the iterative-until-empty versus practical-two-iterations distinction and the R32 amendments; do not assert hypothesis equivalence. |
| 13 — §6 | Correct order formula as a qualified parallel accounting result; header shorthand omits the assumptions and M8 status. See findings 6 and 9. |

## Falsification experiment and reproducibility

Saved and executed:

* `Theory_work/Wave1C/C-PACK/numerics/R34_falsify.py`
* `Theory_work/Wave1C/C-PACK/numerics/R34_falsify_out.txt`

Command:

```
py -3.13 -B Theory_work/Wave1C/C-PACK/numerics/R34_falsify.py
```

The harness is independent of the project's numerical libraries. It implements D0 from `SoP/04_theory.tex:71`–`:72`, after sample centering/standardization:

```
H = (n+1) X_S'X_S + I
Q = y'y - n z'H^{-1}z
log m(S) = -.5(log det H - log det(G+I)) - (.01+n/2) log(.02+Q)
w(k) = 1 / (2 choose(2p-1,k)).
```

The common positive marginal-likelihood factor and cap-prior normalizer cancel. It enumerates every model in Ω and normalizes their masses; it does not approximate expectations by posterior draws. Positivity on all feasible states is explicitly asserted. The outputs use binary64 with absolute tolerance `8e-12`, so these are numerical falsification checks, not interval-arithmetic certificates.

There are **216 posteriors**, using n∈{6,12,24,60}, p∈{4,7,10}, six correlation structures (independent, equicorrelated, AR(1), blocks, a cancelling/masking pair, and singular duplicates), and three signal levels. These require **64,476 feasible model scores**. For each posterior the script checks every possible true subset, for **84,096 truth/posterior pairs**, including the empty/full truths and truths beyond the cap. The every-truth loop is a deterministic stress test of inequalities that do not depend on how a nominal truth generated the data; it is not a statistical simulation asserting each tested truth was the generator. A subset zeta transform checks joint inclusion probabilities for **every** A⊆[p]. Bounded-h tests, a finite TV identity, strict threshold implications, uniqueness of the HPM and size concentration are included.

Results: no inequality violation; maximum positive excess in SL0(i)–(v) is `1.332e-15`. The harness separately checks **80** two-point finite laws attaining `2delta` under the corrected arbitrary-law scope. Negative controls detect an HPM tie/MPM miss at delta=1/2, a true variable excluded at q=1−delta, and a false variable included when q<delta. Empty and full truths demonstrate why universal two-sided attainment cannot be claimed for those truths. A strictly positive law and the analytic empty-model argument in finding 1 expose the D0 sharpness issue; absence of a numerical equality is not used as its proof.

No asymptotic law, Song–Liang theorem, production integration, or D0 sharpness claim is certified by these finite computations. The source PDF extraction and page renders are additional inspection artifacts named `numerics/R34_song_liang_layout.txt` and `numerics/R34_SL-06.png` through `R34_SL-12.png`.

The requested central result can be retained after the local corrections: exact-posterior uniform PIPs and decisions follow from posterior concentration, and store-restricted PIPs have the stated uniform with-output implication under the named score/store/LS0 premises. The literal D0 attainment claim and the unqualified capped misspecification comparison cannot be retained as written.

**Verdict: ERROR — FATAL 0; MAJOR 2; MINOR 7; NIT 0.**
