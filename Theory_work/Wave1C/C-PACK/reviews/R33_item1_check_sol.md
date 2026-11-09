VERDICT: GAP

Independent mathematical/code review of `lemmas/I1_e4_replacement.md` and `STATEMENT.md`, Item 1. The core exact-arithmetic Lemma UM is correct. The core UM-FP implication is also correct, subject to the boundary/domain clarifications below. The literal exhaustive audit is false, and the binary64 alternative must be restricted to the start-mode identification step. These issues prevent verification of Item 1 as currently worded; I found no counterexample to either core lemma on its well-defined domain.

Version note: the sources changed during this review. This final review incorporates the subsequently observed **LOCKED v2** of STATEMENT (Item 1 at lines 9–37) and the **143-line** I1 lemma file, including its added numerical paragraph and §5. The v2 target correctly narrows several requirements; the remaining findings concern the lemma/deliverable not yet meeting that target. References below use that latest inspected version unless an unchanged earlier section is identified.

Paths below are relative to `C:/Users/felip/Bayesian-Variable-Selection`. Abbreviations: CP = `Theory_work/Wave1C/C-PACK`; W1 = `Theory_work/Wave1`; NBH = `Theory_work/Old_Projects/New_BVS_Headquarters`; CODE = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core`.

1. **MAJOR — The exhaustive audit omits GEN (C6) and the explicitly different T38 data-dependent-centre route.**

   Locations: `CP/STATEMENT.md:10–16`; `CP/lemmas/I1_e4_replacement.md:14`, `:34`, `:124`.

   The lemma's audit conclusion says exactly:

   > Conclusion of the audit: in PXN, GEN and M5(b1-LH), the start-mode tie rule and e4 are used **only** on an event of the
   > form {π₀(R) > ½} for a deterministic (given X) reference R ∈ {S°, S\*}, and only to conclude that the LS0 centre
   > equals R. The lexicographic rule, the size rule, the cap and the truncation flag are never used. (Rules named "lexicographic"

   That is too broad. `W1/W1-GEN/STATEMENT.md:145` includes (C6), whose proof is `W1/W1-GEN/lemmas/L7_counterexample.md`. At lines 63–64 it says:

   > Pick a proxy k ∈ C_b and put S′ := S̃₀ ∪ {k} ∈ Ω. Only block b's factor and the prior change:
   > log γ₀(S′) − log γ₀(S̃₀) = log[w(q + 1)/w(q)] + log[r_b(U ∪ {k})/r_b(U)] ≥ −log(2p) + log[r_b(U ∪ {k})/r_b(U)]

   Lines 73–74 conclude:

   > the gain is ≥ θ²(n − 1)a²/(4C_R d) − log(2p) − ½ log(n + 1) − 2κ_E > 0 for n ≥ n₀ (d log n/n → 0), contradicting
   > maximality of S̃₀. Hence on the intersection of these events every b ∈ 𝔅 contains a selected element outside S₀ (a

   This uses the maximality of the random start centre itself. No event identifying it with a deterministic reference of mass greater than one half is invoked. This remains a legitimate use of the *maximiser* content of the centre definition even though size/lex ties are irrelevant. Under EX-A it is supported by N3(a) globally, including truncation. The proposed reference-margin FP-TAB contract does not by itself transfer that obstruction proof to native doubles: rounded maximality does not imply exact maximality. Fortunately (C6) is not one of the positive consistency conclusions.

   Also, `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:263` says exactly:

   > *Alternative for (M2), with a data-dependent centre.* If TD′_P(R_{a,d}) holds with probability → 1 and ℓ ≥ a + d, then [W1-T37R Thm A(A3)] gives repair from *every* centre in R_{a,d}. So (M1) can be weakened to P(S̃₀ ∈ R_{a,d}) → 1.

   This alternative uses membership of a data-dependent centre in a repair region. It does not require a reference R with π₀(R) > ½. It is not used in the displayed proof of Corollary b1-LH; explicitly exclude it rather than silently subsuming it. Its cited status is PROOF SKETCH at line 264.

   The locked v2 target now expressly requires listing and resolving uses outside that event; this audit has not done so. **Concrete fix text for the audit conclusion:**

   > In the positive consistency proofs PXN (E)/(T)/(C), GEN (C1)/(C3)/(C3-fav)/(C4) and their instances, and the deterministic-reference proof of M5(b1-LH), centre correctness is needed only to identify the centre with the stated reference on {π₀(R)>½}. No smallest-size or lexicographic start-mode property is needed there. This statement excludes GEN (C6), which uses global maximality and is instead supported under EX-A by N3(a), and excludes the optional data-dependent-centre route in T38_PROOF.md:263–266. Structural integration and transfer identities are accounted for separately.

   Add audit rows for those exclusions and for Findings 2 and 4. Do not claim every occurrence in the entire GEN package is a uniqueness-event occurrence.

2. **MAJOR — PXN's group-version transfer includes an off-event centre identity; changing to capped coded outputs requires an explicit repair of that identity.**

   Locations: `CP/lemmas/I1_e4_replacement.md:18`, `:34`, `:128`; `W1/W1-PXN/FINAL_PROOF.md:14`.

   FINAL_PROOF invokes Lemma T, referring to `NBH/branch_snapshots/API-PXNGAP/PROOF.md:104–119`. Its exact wording at lines 106–108 is:

   > **Lemma T.** (i) On 𝒜_n every block object equals its group version: r_b = r̃_h for the group h = C_b, π₀ = π̃₀, S̃₀ = S̃₀^~,
   > (a_bj, D_b, q, e) = (ã_hj, D̃_h, q̃, ẽ), and the LS0 centre is S̃₀^~. (ii) Consequently, for any event E defined through
   > block objects, P(E) ≤ P(Ẽ) + P(𝒜_nᶜ), where Ẽ is E with every block object replaced by its group version. (iii) The laws

   This asserts equality of centres on all of 𝒜_n, including {π₀(S°)≤½}. The proof at lines 112–113 uses equality of the *unordered* block and group index sets. The prescribed mathematical size/lex maximiser is independent of block enumeration order. The frozen capped routine need not be: N3(d) makes the truncated choice depend on DFS order. In floating point, even the objective ĝ can depend on block order.

   **Explicit counterexample to the implicit order-invariance assertion:** p=2, K=1, λ=(-10,0), singleton blocks with each nonempty entry 1, cap=1. Ordered blocks `[[0],[1]]` return `{0}`; `[[1],[0]]` return `{1}`. Same unordered partition, same mathematical π₀, exact integer arithmetic, valid H1–H4, both runs truncate. Neither singleton has mass greater than one half. The new falsification script runs both through the frozen harness and checks these outputs. This is an abstract-table counterexample to the unqualified structural inference, not a claimed data-generated LH counterexample.

   The actual packing order is dendrogram leaf order (`CODE/cpp/v3_blocks.h:121–143`), whereas the group version at API-PXNGAP line 70 is indexed by `C_1,…,C_{G_n}`. Equality of partitions as sets is not an order-matching assumption. The audit never checks this additional use. No such identity is necessary for the intended *consistency* result: transfer the mass event, then apply UM to the actual centre.

   **Concrete fix text for PXN's transfer, supplied as a CP-local amendment rather than an edit of Wave1:**

   > The unconditional transfer identity on 𝒜_n is used for the mathematical tables, π₀ and aggregation quantities. For a centre defined by the capped coded routine, do not assert off-event equality with a group-version centre merely from unordered partition equality. Instead, on 𝒜_n∩{π̃₀(S°)>½}, π₀(S°)=π̃₀(S°)>½ and Lemma UM gives the actual centre S°. Thus P(C₀≠S°)≤P(𝒜_nᶜ)+P(π̃₀(S°)≤½). In the start-mode-only FP variant, add the probability of the corresponding margin/encoding/execution failure. Any stronger equality of coded group and block centres requires identical ordered encodings and execution contracts.

   This preserves the positive proof and does not need a lexicographic fallback. It does require admitting that the literal audit assertion was stronger than the proof needs.

3. **MAJOR — H2-FP + FP-TAB can replace the start-mode arithmetic idealisation only; it cannot replace the consumers' full EX-A premise.**

   Locations: `CP/lemmas/I1_e4_replacement.md:105`, `:111`, `:128`, `:134`; `CP/STATEMENT.md:31–37`.

   The replacement offers exactly:

   > binary64, (H2-FP) + FP-TAB on the relevant event)."

   The concluding language is:

   > not in the production core; C-ENG), plus FP-TAB if EX-A is dropped. The lexicographic rule and the e4 truncation

   The locked v2 target at lines 35–37 already correctly excludes this interpretation. The lemma's replacement text must match it, and its requested source-by-source patches must retain the other EX-A assumptions.

   Read as a native-binary64 replacement for full EX-A, this is unsupported. The shared EX-A definition is exact (`SoP/04_theory.tex:78`):

   > \par\smallskip\noindent\textbf{EX-A.}\enspace Exact mathematical scores, arithmetic, sums and comparisons. This is an idealisation, not a validated floating-point property.

   H2-FP controls only `start_mode` and `log_gamma0`; η controls the composite start tables. Neither controls full-model scores at LS0's scanned neighbours, their ordering, HPM ordering, sampler validity, or actual/potential-run agreement in the presence of numerical failures. GEN L4's strict progress argument (`L4_search.md:30–40`), PXN's D_S argument, and T38 LS-score (`T38_PROOF.md:180–185`) use precisely those other computations. T38 already warns at lines 94–96:

   > `numerical_failure` cannot occur in R̄ (EX-A). In the actual run it occurs only if EX-A fails, and then GUARD's
   > "st = st̄ on 𝒢ᶜ" fails too. A floating-point statement needs a VAL-FP-type contract (W2-BOOK Prop. 2(f)), which is
   > outside this theorem.

   The logical deficiency is concrete: two runs may have identical perfectly certified start tables and hence identical η, ε, Δ and start centre, but arbitrarily different computed scores for multi-block neighbours outside those tables. FP-TAB cannot distinguish those runs or force the strict LS0 progress comparisons. No new counterexample to the actual coded scorer is asserted.

   Also, a per-run sufficient condition is not automatically an asymptotic guarantee. If FP-TAB is assumed pointwise on every relevant mass event, that is enough for the centre step; if it is a random run condition, explicitly require the exceptional probability to vanish.

   **Concrete fix text:**

   > All consumer assumptions, including EX-A outside the start-mode subcomputation, are retained. Under EX-A, UM discharges the needed start-mode identification. Alternatively, for this identification step alone, assume H1, H2-FP, H3, H4 and FP-TAB. Writing E_n={π₀*(R_n)>½}, an asymptotic centre conclusion follows if P(E_n)→1 and P(E_n∩{Δ(R_n)≤2(η_n+ε_n)})→0, with encoding/execution failures likewise excluded or of vanishing probability. This does not give a native-binary64 consistency theorem for the full method; dropping the remaining EX-A assumptions requires additional scorer, search, ordering and operational contracts.

4. **MINOR — Make the inherited integration, objective and execution requirements explicit in e4′, including the exact branch.**

   Locations: `CP/lemmas/I1_e4_replacement.md:129`; `CP/STATEMENT.md:31–35`.

   The exact text is:

   > on the run's own tables (`build_tables`/`build_start`, so (H1) holds), with cap ≥ 1; arithmetic per EX-A (or, in

   Building tables alone does not establish every H1 precondition: it assumes a valid D, matching K/prior, a partition with sorted indices and allowed block sizes, and correct inverse encoding. Nor does it establish H4 (representable dimensions/cap, allocations, recursion and enumeration completion). The lemmas correctly assume H4, but the displayed replacement does not say it inherits it.

   Locked v2 T1.d now explicitly requires H1 and H4; propagate that into I1's actual replacement text.

   More materially, the actual exact branch may have no tables at all. The adopted PXN convention, `W1/W1-PXN/lemmas/R_branch_repair.md:29–34`, states:

   > enumeration when Σ_{k≤K} C(p,k) ≤ (5H₀+4N₀)p, which can hold for p ≥ 18 when p_n grows very slowly (e.g. p_n = g⌈log₂log₂(n+4)⌉);
   > then no partition or block start is built. The locked statement allows such sequences and must not acquire a lower growth
   > bound on p. **Convention adopted.** In STATEMENT §2, "blocks", π₀, S̃₀ and "LS0 of R̄⁺" denote the deterministic
   > make_blocks / block-table / start-mode / local-search objects computed from the data on **every** branch (hypothetical when
   > the actual run takes the exact branch). (R), (S), (E), (T) are statements about these data functions and hold as proved

   Hence “run's own tables” must include these hypothetical objects for centre-law statements. Physical LS0 execution on that branch is unnecessary for output consistency, because exact enumeration scores the truth once feasible. On the SMC/potential-output branch, OP-LS0 must identify the *same* centre, emit it, complete scans, and insert scored models into the all-scored ledger. GEN's L5:11–16 uses this structural identification on all data; its closure is not itself confined to the uniqueness event.

   **Concrete fix text to append to the repaired e4′:**

   > H1 and H4 of N3 are explicit inherited assumptions. The routine uses the same retained indices, K=min(p,⌊n/2⌋), ordered actual partition, full-response block tables and capped BB(1,p) prior as the mathematical π₀ in the consumer. Define the coded centre as a deterministic measurable data function on every branch, using hypothetical block/start objects on exact-enumeration branches. Wherever LS0 is required, its emitted starting centre is this data function, with the unchanged OP-LS0/scored-set/guard contracts. Its use is not vetoed merely because `res.truncated` is true. The cap is fixed in advance or a specified deterministic measurable data function satisfying H3–H4.

   This is a clarification of necessary integration assumptions, not a claim they have been implemented. In particular, at cap=1 a unique mode still has `truncated=true`.

5. **MINOR — The auxiliary per-entry maxima include undefined or NaN, deliberately unread entries as presently written.**

   Locations: `CP/lemmas/I1_e4_replacement.md:76`, `:78`, `:112`.

   The definitions include exactly:

   > η_ρ := max_{b, U ≠ ∅} |ρ̂_b(U) − ρ\*_b(U)| (each S meets at most |S| ≤ K blocks);

   and:

   > ε ≤ γ_K (Λ̂ + K·T̂), Λ̂ := max_k |λ̂(k)|, T̂ := max_{b,U} |ρ̂_b(U)|;

   N3 defines real ρ only for |U|≤min(|C_b|,K). `build_tables` fills all entries with NaN at code line 86 and skips scoring |U|>K at line 92. Thus H1/H2-FP allow NaNs outside the feasible domain. A maximum over all U is not a finite real bound in those cases, although η and ε defined over feasible S are fine. This does not invalidate the central UM-FP inequality; it invalidates the stated auxiliary bounds until their domains are restricted.

   **Concrete fix text:**

   > In all table-error and magnitude maxima, k ranges over 0,…,K and U ranges over subsets of C_b with |U|≤min(|C_b|,K). For η_ρ require also U≠∅, and define η_ρ=0 when this index set is empty. Entries above the cap are excluded and may remain NaN.

   Counterexample to the unrestricted definition: p=2, one block {0,1}, K=1; its double table entry for {0,1} is NaN in the permitted encoding. The test suite includes such unread NaNs.

6. **MINOR — Define the singleton-domain margin and endpoints, and state feasibility in the short target.**

   Locations: `CP/lemmas/I1_e4_replacement.md:79`, `:96`; `CP/STATEMENT.md:18–28`.

   The definition is:

   > - margin: Δ(R) := f\*(R) − max_{S ∈ Ω_K ∖ {R}} f\*(S).

   For K=0, Ω_K={∅}; the displayed maximum is empty and has no stated value. This leaves UM-FP undefined on an explicitly allowed N3 boundary. Similarly, `t < ½` at line 96 includes t=0, where the ordinary real expression log((1−t)/t) is undefined. With finite objectives and a nonsingleton domain, π₀*(R)<1 automatically; with K=0 it equals 1.

   Locked v2 T1.c:26 already supplies the empty-maximum convention. Copy it into the standalone lemma. Likewise retain the explicit ku<1 requirement now present at target lines 27–28 for every γ index used, including K in the crude bound.

   **Concrete fix text:**

   > R∈Ω_K throughout T1.b and T1.c. Define max∅=−∞ and Δ(∅)=+∞ when K=0. In that case ε=0, and start_mode returns ∅ directly. For the mass-to-margin bound assume 0<t<½; handle t=0 by the singleton-domain case (or explicitly use the +∞ endpoint convention).

   The empty model as a winner with K>0 causes no difficulty: m(∅)=0 and its prior-plus-zero evaluation is exact. R outside Ω_K is excluded, not an additional covered case. If a consumer zero-extends π₀ off Ω_K, π₀(R)>½ cannot hold there.

   For fidelity to the stronger locked v2 T1.b, state UM first under `argmax f={R}`, then make π₀(R)>½ a sufficient condition. Existing proof steps (ii)–(iii) prove that stronger claim immediately. Likewise T1.c's unique-ĝ formulation follows directly from N3(e), independently of how that uniqueness is certified.

7. **MINOR — The precision discussion overstates what the upper bounds and concentration rates establish; its per-entry condition is not equivalent to FP-TAB.**

   Locations: `CP/lemmas/I1_e4_replacement.md:98–117`, `:137–143`.

   The cited rates themselves are correct: PXN FINAL_PROOF:48, GEN L2_centre:18–19, and T38_PROOF:318 give exactly the rates used. B≤16 is essential when absorbing 2^B. They imply *lower bounds* for the margin, not an asymptotic equality. For a_n→0 and 1−π₀*(R)=O_P(a_n), the precise statement is that log(1/a_n)−Δ(R) is bounded above in probability. More explicitly, for every fixed δ>0,

   `P(Δ(R) ≥ (c−δ) log n) → 1`,

   with c=1/2 for PXN and M5, and c=κ for GEN. One can also obtain a deterministic o(log n) slack by letting the tightness threshold increase slowly. The fixed-M display at line 99 alone is a 1−ε′ statement, not already a probability tending to one statement for that same M. Calling this “order log n” is acceptable only as a lower-bound description.

   Line 105 instead says exactly:

   > **What is needed in binary64 (exact statement).** On the run, 2(η + ε) < Δ(R). The margin side grows like c log n. The

   At lines 107–108:

   > log Bayes factors T̂ and log prior Λ̂ can be of order n log n and K log p, so the sufficient bound ε = O(u K² T̂) eventually
   > exceeds log n as n → ∞ with u fixed. Hence:

   An upper O-bound cannot establish that ε itself eventually exceeds anything. The elementary displayed upper bound is γ_K(Λ̂+KT̂), or O(uKΛ̂+uK²T̂) when Ku is bounded away from 1. Dropping the Λ̂ contribution requires a stated domination assumption. Large possible magnitudes show that these estimates do not provide a uniform asymptotic certificate; they do not prove actual numerical failure or an actual error lower bound.

   Finally, line 117 calls the per-entry condition exactly:

   > 2(η + ε) < Δ(R) on the run" (equivalently: the scorer's per-entry error η_ρ is ≪ Δ/K). No claim is made that FP-TAB

   This is not an equivalence. η_λ and ε can violate FP-TAB even if η_ρ=0; conversely, table/prior errors can cancel in f̂−f*, so a large η_ρ need not violate it. Even with η_λ=0, the sufficient worst-case sum bound is not necessary. The informal ≪ condition is neither the same finite-run threshold nor enough without controlling the other terms.

   The revised illustration at lines 112–113 now explicitly bounds both Λ̂ and T̂ by 10³, and its roughly 1.1×10⁻⁹ arithmetic is correct. That improvement resolves the earlier missing-Λ̂ qualification. The newly added DATA paragraph at lines 114–115 instead needs a notation correction: it reports “Δ/(2ε) ≥ 7·10¹²” using Δ defined here from f*. Its numerical source expressly uses f̂. `numerics/item1_um_checks.py:598` describes f̂ as the exact sum of the code's doubles and disclaims assessment of η; `:583–584` extracts the corresponding table-defined margin. The source output's part (C) confirms this. These diagnostics establish a margin for the stored-table objective, not the mathematical margin Δ, and their π₀(R) is likewise the stored-table law. Relabel them Δ̂ and π̂₀, or explicitly describe f*=f̂ as an artificial diagnostic convention. The claim that η is the binding term remains unestablished: it is not measured at all. The latest §5 correctly says η was not tested; retain that limitation consistently.

   **Concrete replacement text for lines 105–115:**

   > The cited concentration rates give logarithmic lower bounds on Δ, with the explicit probability quantifier above. They do not give Δ∼c log n. For Ku bounded away from 1, ε≤γ_K(Λ̂+KT̂)=O(uKΛ̂+uK²T̂); these crude upper bounds do not by themselves establish the margin condition uniformly at fixed precision, nor do they prove a lower bound on the actual error. At K=100, conditional on Λ̂,T̂≤10³, the bound is about 1.1×10⁻⁹. The DATA diagnostics report the stored-table margin Δ̂ and law π̂₀, not the mathematical Δ and π₀*. They do not establish which error term dominates. FP-TAB is the run condition 2(η+ε)<Δ(R). A sufficient, non-equivalent per-entry condition is 2[η_λ+Kη_ρ+γ_K(Λ̂+KT̂)]<Δ(R). No scorer-error guarantee is asserted.

The following checks passed; they are recorded to distinguish the gaps above from objections to the mathematical core.

- **Exact UM, I1:41–58.** H1 defines a finite nonempty Ω_K and finite real objectives. π₀(R)>½ implies strict superiority to every other feasible model, hence 𝒜=𝒜*={R}, N=1 and k*=|R|. H3 supplies N≤cap. N3(c) applies with exactly H1–H4; N3(a) alone is sufficient. I checked the supporting L2 block maxima, L3/L4 DP and size selection, L5 enumeration, and L6 assembly against the frozen loops. No lexicographic assertion under truncation is needed. K=0 and an empty R are safe for UM. All *read* NaNs are excluded by H1; unread above-cap NaNs are harmless. Default cap gives no truncation at N=1; cap=1 gives ties=1 and truncated=true without changing the returned set. H4 is necessary, not implied by numerical uniqueness.

- **FP evaluation and fold, I1:62–94.** `comp` sorts (block,position) pairs, ORs their bitmasks, and adds exactly one stored nonempty entry per met block in increasing block order (`v3_start.h:54–66`). `log_gamma0` adds the prior last at line 69. The DP skips empty intersections at line 204, reproduces the same fold, and adds the prior at line 210. Treat the first 0+x as exact. There are m relevant rounded additions for m+1 terms; for m=0 the sole λ+0 is exact. Commutativity, not associativity, justifies exchanging the operands of the final addition. Signed terms do not affect the absolute forward-error bound.

  Under the stated IEEE model with gradual underflow, addition of two represented binary64 numbers whose exact sum is subnormal is exact: the operands and their sum lie on the same 2^−1074 lattice. Thus this use of the relative-error model does not need an omitted absolute underflow term. Flush-to-zero or reassociation would be outside H2-FP. Expanding the recursive sums gives products of at most m factors (1+δ), bounded by γ_m; multiplying each term by its absolute value proves the stated bound. It covers cancellation. No separate bound for DP comparisons or a factor for the number of candidate paths is needed: N3(e) identifies an actual global ĝ-maximiser.

  I rechecked the crucial N3(e) argument in `W1/W1-N3/lemmas/LFP_floating_point.md:31–74`: rounded addition is monotone in each input, so the DP retains a maximum rounded prefix for each size; some tight path is attained and processed at cap≥1; its leaf has the advertised value under the same fold. This proves membership in argmax ĝ, even though some rounded ties are not enumerated. Consequently the strict separation Δ>2(η+ε) forces `res.S=R` exactly as I1:91–94 says. Neither global lex correctness nor completeness of rounded tie enumeration is being imported from N3(c).

- **Reference determinism and objective identity.** PXN's R=S° is a fixed support-minus-masked-index set (`W1/W1-PXN/STATEMENT.md:13–19`), hence deterministic given X with the model parameters fixed. GEN assumes a deterministic certificate in H2 (`STATEMENT.md:64–80`) and explicitly permits only X-measurable certificates for random designs (`:115–120`; `L5_assembly.md:68–82`). Its dependence on β and σ² does not mean dependence on response noise; it is an oracle certificate, not an estimator from X alone. T38 b1 assumes deterministic S° at line 249; b1-LH fixes it at line 276. The alternative at line 263 is the excluded exception, not a flaw in those base hypotheses.

  The three positive consumers use the same mathematical start: Ω={|S|≤min(p,⌊n/2⌋)}, normalized capped BB(1,p) prior, and r_b(U)=m(U)/m(∅) scored against the full response. PXN states this at STATEMENT:24–30; GEN at STATEMENT:26–28; M5 uses D0 (`SoP/04_theory.tex:70–73`, card:484) and T38's cap (`T38_PROOF.md:12`, `T38_STATEMENT.md:52`). The frozen code sets K at `v3_score.h:40`, λ=log w−log W_K at `:63–70`, and ρ=log m(U)−log m(∅) at `v3_start.h:92–95`. GEN's proportional use of w instead of varpi differs only by a common log constant; choose λ*=log varpi in the FP comparison so η is aligned. In PXN, arbitrary actual blocks and hypothetical group blocks are different objectives off partition recovery; mathematical π₀ transfers on recovery, while coded centres need the repair in Finding 2.

- **Positive downstream uses.** PXN LS_P6:15–27 and FINAL_PROOF:63–65 need only centre=S° on the good event; its move tie rule can choose any best progress addition. GEN L2:57–59 needs reference identification, L4:30–46 permits any maximizing move because all such moves remain in the relevance set, and L5:31–39 uses equality of the actual and reference centres only on that good event. L5's separate all-data structural closure was accounted for in Finding 4. The C3-fav route emits the truth as centre. T38 LS-score:168–185 is a fixed-data lemma for arbitrary feasible C₀, including its centre-emission condition; b1 applies it with C₀=S° at :258. The LH corollary does not invoke the data-dependent alternative. No positive consistency argument uses a smallest-size preference, lexicographic start preference, the tie count, or a truncation flag. Those facts justify the repaired, restricted exact-arithmetic premise replacement.

Falsification artifacts and observed results:

- Script: `CP/numerics/R33_falsify.py`; transcript: `CP/numerics/R33_falsify_out.txt`. Executed with `python -B -X utf8 Theory_work/Wave1C/C-PACK/numerics/R33_falsify.py`. It imports no repository modules, writes no bytecode, and writes only its CP-local transcript.
- Uses the existing `W1/W1-N3/numerics/sm_harness.exe`, whose source includes the frozen header. Inputs use the documented TABLE format and lossless hex floats. The transcript records SHA256 digests of the harness and current frozen header; the executable was not rebuilt or modified.
- Enumerates every feasible set for 2,407 instances with p≤8. Uses exact rational arithmetic for f*, f̂, η, ε and the strict margin comparison; independent exact-real table perturbations exercise nonzero η. Families cover integer tables, sub-ulp gaps, cancellation, magnitudes from 2^−500 through 2^500, subnormals, empty winners, K=0, unread NaNs, shuffled block order, and caps 1/2/10^6. It checks the fold bound for every enumerated set, N3(e) against every returned result, and UM-FP wherever its strict condition holds.
- **1,912 instances satisfy the strict UM-FP condition; zero violations.** K=0 and an empty winner at cap=1 return the expected set with ties=1 and truncated=true.
- Negative control: blocks [{0},{1,2}], K=2, λ=(0,0,0), ρ_0({0})=1000 and ρ_1({1})=10^−14, ρ_1({2})=2×10^−14, ρ_1({1,2})=−5. The unique exact winner is {0,2}, but the code returns {0}. Its margin is 10^−14, below 2(η+ε)≈4.4408920985006272×10^−13, so UM-FP correctly makes no promise.
- The two order controls in Finding 2 return different tied modes, as predicted. They falsify off-event order invariance, not UM-FP. No data-generated scorer error bound or universal numerical correctness is inferred from these finite tests.

Writes made for this review are confined to the three requested CP-local artifacts. No source proof, frozen code, executable, or git state was changed.

VERDICT: GAP — FATAL: 0; MAJOR: 3; MINOR: 4; NIT: 0.
