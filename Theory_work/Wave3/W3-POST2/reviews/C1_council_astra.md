# W3-POST2 — Council seat A, round C1

Reviewer: GPT-6 Astra, high. Review date: 2026-11-09. Reviewed STATEMENT v1.2, ASSUMPTION_MAP v1.3 and the supplied package against the actual source proofs and code. Earlier verdicts were not used as mathematical premises. No subagents, git operations, or changes to the package. Paths below are relative to `Theory_work/Wave3/W3-POST2/` unless explicitly stated otherwise.

**Verdict: PASS. Uncapped score: 8.6/10. All six gates PASS.**

No FATAL or MAJOR mathematical finding. Two MINOR reporting findings and one NIT remain below. This is this seat's assessment, not a declaration that both council seats passed or that HQ approved the scope deviation.

## Gate verdicts

| Gate | Verdict | Reasons |
|---|---|---|
| G1 — correctness of every step | PASS | Re-derived the new steps in A–E and checked the inherited steps they actually consume. Rank domination, truncated moments, approximate-reference denominator, favorable-side integration window, ridge-loss comparison, and uniform conditional posterior contraction all close. No theorem-breaking inequality or counterexample found. The auxiliary numerical interpretations need the wording corrections below. |
| G2 — hypotheses used = hypotheses stated | PASS | A retains the inherited beta-min qualifications; its 5(a) uses only F₀. C is explicitly conditional on hypotheses holding at the given n. B requires deterministic references and fixed/common M,B for its tightness consequence. D(b) uses OS and F₀, not global ID, F_λ or beta-min. E uses ID^M only on bounded-excess underfits. |
| G3 — no hidden assumptions | PASS | Empty and singular competitors, rank-zero increments, zero size tails, algebraic comparison unions outside Ω, and fixed small p are covered. G2* really is supplied by P3's per-size proof. Random-design transfer retains independence and common constants/envelopes. The parameter result is centered and in-sample; it does not silently claim an intercept or population-predictive theorem. |
| G4 — cited lemmas have adequate status | PASS | The source chain exists and supplies the cited statements. W3-POST is council-passed C3, while its REPORT explicitly reserves the full PROVED-CHECKED process label pending HQ's review-layer substitution. POST2 preserves the literal author statuses rather than upgrading them. The new steps are written out and have the recorded line checks; I checked substantive repairs against the current files. Citation-script success is not treated as proof verification. |
| G5 — constants/rates tracked | PASS | OS's two distinct bounds pay the two different completion sums. C1's deterministic constant and C2's O(n^−1/2)+O(1/n) tail suffice for Eδ=O(r_n). E's strict c>c₁ absorbs its remainders. D's C_H depends only on s₀,A,σ*²; other constants can affect the onset. The common chi-square fluctuation gives the root-n variance rate uniformly over retained models. |
| G6 — coded posterior target | PASS | Directly checked `Scripts/SMC_BVS/core/cpp/v3_score.h:40–71,196–224` and `Scripts/SMC_BVS/core/v3_preprocess.R:111–127`: retained columns, K=min(p,floor(n/2)), H=(n+1)G+I, determinant denominator G+I, Q, ν=.01+n/2 and capped BB weights agree. P1's joint contrast transformation yields IG shape .51 before the contrast likelihood, hence exactly the same posterior ν. Results concern the real-arithmetic target, not sampler delivery or floating-point guarantees. |

## Numbered findings

1. **MINOR — scope flag omits a statement-level effect on item 5.** `REPORT.md:14–21`, compared with `reviews/R03b_disposition.md:11` and `lemmas/E_visibility.md:3–4`.

   Calling these “two strengthenings” is defensible as a count of the two ranked R03b proposals C+ and D+. But the top-level flag lists only effects on items 3 and 4 and ends “No other proposal was adopted.” In fact D+'s ridge comparison was also adopted into Claim E, weakening its hypothesis from ID to ID^M. This is a change to a third theorem item, even if it is a subsidiary consequence of D+. The review table at REPORT:155 and the disposition disclose it, so this is an incomplete scope summary rather than a concealed proof change.

   **Concrete fix:** say “Two ranked proposals were adopted, affecting items 3 and 4 and additionally weakening item 5 from ID to ID^M through D+'s ridge-loss lemma.” Add that third effect to the flag and replace the last sentence by “No other ranked proposal was adopted.” Retain the explicit admission that prior HQ approval was not obtained. Wave3/PROTOCOL.md rule 3 assigns that decision to HQ; extra checks do not retrospectively supply authorization. HQ must resolve that process issue. This seat's mathematical pass does not resolve it, and the alleged synchronous unavailability of HQ is not independently established by this review.

2. **MINOR — two sharpness sentences still read more strongly than their numerical evidence.** `REPORT.md:133,140`; related `ASSUMPTION_MAP.md:27` and `lemmas/A_occam.md:33`.

   The report correctly introduces these as finite-n observations, but “an achieved margin of 4 log n suffices” reads as an asymptotic sufficiency statement. N4 is a coefficient-scale experiment, its achieved minimum is slightly below 4 log n, and it does not establish a new uniform margin theorem. Likewise N2's four decreasing weighted ratios do not, by themselves, prove OS along an infinite sequence. The general implication ADG⇒OS is proved; strict separation by this particular duplicate-pair example needs its own asymptotic argument if stated as a proved example.

   **Concrete fix:** replace the N4 sentence by “At coefficient scale c=4, the achieved margins are approximately 3.67–3.99 times log n and the observed δ/r_n is 0.75–1.18; no smaller universal margin constant is proved.” For N2 use “consistent with strict weakening to OS,” or append a short deterministic example proof. Such a proof is feasible: at fixed p with otherwise orthogonal independent directions and one duplicated null pair, the determinant ratio is of order n^j unless both duplicates are included, when it is of order n^(j−1). Track the corresponding rank-sensitive weights and the amplified j>j₀ sum explicitly. This corrects evidential wording; it does not invalidate A0/A1 or E.

3. **NIT — citation-check count is stale.** `REPORT.md:162` says 119 checks; the inspected `reviews/CITECHECK.txt:1` says **120 checks, 0 failures**.

   **Concrete fix:** copy the current count, or report only “0 failures; selected mechanical checks” with the output pointer. The script itself correctly discloses selected coverage and does not certify mathematics, literature accuracy or review summaries.

## Independent mathematical audit

**A.** P1's determinant interlacing establishes F_w⇒DG for arbitrary positive g₀. Averaging gives ADG. The function d↦(xj/d)^(d/2) is increasing on 1≤d≤j for x=eC_A log n, including a valid separate d=0 case; thus a_J≤(2eC_A log n)^(j/2). The prior multiplicity and geometric tail prove both OS inequalities, with the amplified shell of order (log n)^((j₀+1)/2)/n=o(r_n). In the single-superset comparison, T03R B3 requires a floor only on the smaller true model. No full rank is smuggled into G3 or the truncated moment. Absorption exp(jε_n)≤2^(j/2) works termwise and needs no additional m♯ε_n condition. Completion multiplicities and the cap extension are valid. A2 follows by summing distinct feasible superset odds and solving δ≥(1−δ)O⁰. Its necessity claims follow for fixed and random designs in their respectively stated modes.

**B.** Evaluating the variational Q at the reference produces B_T+2εᵀr. Centering gives the stated cross-term variance. P1's scale event and positive-density numerator identity remain valid for arbitrary deterministic means, including means outside col X. The fixed-rate mixed numerator/denominator comparison is essential and correctly used. Retaining D_T is legitimate for rank-deficient and empty references. Exact-reference recovery of L1a′ with its exact constant uses the improved zero-cross-term proof in B Remark 1, not a false equality C″_Λ(M+M′)=C′_Λ. The growing-cost remark now states only an upper payment. The fixed-p growing-cost counterexample to necessity also has a deterministic explanation: the finitely many positive R_m^∅ are bounded below and π≤1, so Θ″=O(n^−1/2) regardless of the mean.

**C.** With Q₀≤σ*²E′+ρ̄, the density-ratio integral is correct. The selected window makes F′(1)(u−1) nonnegative. On E′≤2N and u∈[3/4,5/4], the triangle bound is |F″|≤(152/27)N<6N, yielding F≥−3. A data-dependent subinterval is allowed for a pointwise positive-integral bound. C2 drops an indicator from a nonnegative numerator, not from an uncontrolled likelihood ratio; no independence assumption is needed. The chi-square exceptional bound and exact cutoff yield the asserted expected tail. The remaining terms are bounded in expectation by the truncated sums, rather than inferred from O_P alone. Decision and PIP inequalities are deterministic/Markov consequences.

**E.** For a_S=(I−M_S)μ_c, ||a_S||²≤L_S; the union count gives P((G⁵)^c)≤1/n. Subtracting the true-model residual comparison gives

`Q_S−Q_{S′} ≥ L_S + 2eᵀa_S − eᵀ(P_{S′}−P₀)e − R_n`.

Only F₀ controls R_n. Rank domination controls the projection increment even for singular completions. The prefactor bound and the split D≥B′/D<B′ are correct. Substituting c₁ into φ(c)=c−2sqrt(2C_x c)−C_Aj₀ gives exactly (2/log 2)[s₀(A+1)+2]. Strict c>c₁ supplies the eventual slack. Restricted-family assembly proves coordinate-specific recovery as well as global selection.

**D.** The normal affinity, its bound, conditional Gaussian covariance trace and IG moments are correct. D(a) uses fixed true-model rank and bounded ridge loss; vanishing wrong-model mass suffices for probability conclusions. D(b)'s near family is deterministic given design/truth. E1 is applied only to far members; it does not impose global ID on the near family. G2* and G⁵ give simultaneous O(log n) remainder control. The repaired true-model cross term lies in col X₀ and is controlled by G2*. The leading variance fluctuation is the same ||e||²−Nσ*² for all models, which proves uniform root-n tightness without a union bound over conditional IG means. Markov controls fitted-mean posterior spread at a fixed large log n threshold. Choosing M_n=sqrt(log n) gives the stated fixed C′_H Hellinger threshold.

The bounded-family cutoff assertion used in D/E is valid even at small fixed p: for any fixed integer B, if K≥B then q_B/w(s₀) is bounded below uniformly over p≥B, so m♯≥B eventually; otherwise sufficiently large n implies K=p<B, and the finitely many such p have m♯=K eventually. This supplies the ranges needed by G2*/G3.

## Relations, sharpness and source verification

The registry relations are substantively correct. A1 recovers the base theorem through F_w⇒OS with beta-min qualifications retained. A2 recovers LB on **1≤s₀<p, s₀+1≤K**. B recovers the exact-reference tail as explained above. C adds an expectation rate and implies its probability rate by Markov; this does not remove its selection hypotheses. E contains the selected base conclusions only for beta-min constants above c₁, using a fixed intermediate c′; coexistence below that threshold is appropriately recorded. D is new, with no out-of-sample relation claimed.

The important sharpness limits are honestly present: OS is a sufficient envelope with a four-part gap from its necessary counterpart; no converse for ID^M is proved; F₀ remains; the expectation gap is sqrt(log n) on LB's domain; no lower bound for D(b) is claimed. D(a)'s mean scale has nondegenerate fixed-rank conditional Gaussian spread. Numerical expectations of upper bounds do not prove D(b) sharpness. The remaining numerical-language issues are finding 2.

I inspected the attached Song–Liang PDF directly with pdftotext, PDF pages 6–8 / printed pages 952–954. Theorems 1–2 use the design-integrated distance and exponential inner/outer thresholds; Corollary 1's logarithmic-size branch and factor d²=2H² match the qualified current comparison. No claim about their supplementary proofs was needed. Local source: `C:/Users/felip/.t3/userdata/attachments/647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf`.

The inherited proof checks used the actual W1-T03R B3/C4–C10, P1 slab/spectral/contrast/envelope/denominator arguments, P3 per-size union bound and completion assembly, W3-POST L1a′ and LB, W2-APP POST step (5), and C-PACK SL0/SL1. The review trail L01, R03b, K-AE, K-BC, K-D, K2, M01 and S01 and their dispositions was checked against current substantive repairs. In particular the old G2 error, missing rank factor in numerical a_J, and simultaneous-event gap are repaired in the supplied versions.

## Independent checks and limits of this review

Ran `py -3.13 -I Theory_work/Wave3/W3-POST2/reviews/C1_scratch_astra/check.py`; output is `C1_scratch_astra/check_out.txt`.

- C1 grid: n=16,17,32,100,1000,10000; 101 E′ values and 301 points in each selected window. Minimum F=−0.292384456612; maximum |F″|/N=1.5. Both bounds pass.
- D1/E1: 768 models over n=16,40,100 and regular, duplicated-null, dependent-truth-combination and near-duplicate designs. SVD smoothers avoid unstable singular-Gram inversion. Maximum Q-decomposition error 8.53e−14; minimum gain-bound slack 0.00107535416. All tested inequalities pass.

I inspected the numerical implementation and saved outputs, including the corrected weights and full margin family; I did not rerun the entire 20-seed experiment suite or overwrite CITECHECK.txt. The small independent checks are falsification attempts, not proofs. Only this review and its permitted scratch files were written.
