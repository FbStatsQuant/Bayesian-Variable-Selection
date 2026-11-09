Reviewer: Codex gpt-6-astra, high

Overall verdict: VERIFIED-WITH-AMENDMENTS at the mathematical-proof level; the reporting and evidence package needs the corrections below. I found no FATAL or MAJOR defect in the locked v1.1.2 theorem. In particular, I did not break LOCL, the U-LOC reference/atom construction, its entropy-stratified factor union, its empty-set extension, the sample coupling, or the uniform deterministic o(sqrt(log n)) remainder used by UNI-1. The UNI-0 geometric replacements accommodate zero and subunit distances: shell zero, restricted growth, conditional decay, and the counting bounds suffice at the places examined in the source chain. The delivery and OBS-k arguments retain their stated qualifications. The production core uses the claimed cap and complete scans under the named configuration/premises; one numerical surrogate does not implement that complete-scan contract. I reviewed the completed N4 base and supplemental outputs. All findings below concern actual claims, evidence, or tooling, not the fact that the theorems are asymptotic. I did not consult the prohibited prior reviews, logs, checkpoints, or plans, and did not independently authenticate review verdicts by opening their review files. Locations below are repository-relative; UNI denotes Theory_work/Wave2/W2-UNI. Files were being updated during this sweep, so the quoted text identifies the reviewed version as well as the line numbers.

1. **MINOR — The report's PLR headline drops the output qualification.**

   **Locations:** UNI/REPORT.md:30–33; compare UNI/STATEMENT.md:93–99 and Theory_work/Wave1C/FINAL/sections/s5_hpm.tex:5–9.

   **Argument:** “+ LSF ⇒ reported-model consistency” does not state the output intersection, and “equals S0 w.p. → 1 (with output)” is ambiguous between an intersection and conditioning on output. The proved conclusion without delivery is P(O ∩ {S-hat-plus != S0}) → 0. It neither supplies P(O) → 1 nor, without further control, supplies P(S-hat-plus = S0 | O) → 1. For example, an abstract event sequence with P(O)=1/n and every output erroneous satisfies the intersection conclusion and has conditional error probability one. This is an overstatement in the headline, not a gap in the corrected locked statement or L5.

   **Exact fix:** Replace the PLR ending with “+ LSF ⇒ P(O ∩ {S-hat-plus != S0}) → 0; unconditional reported-model consistency additionally uses F-UNI's delivery premises.” Replace UNI-0's “w.p. → 1 (with output …)” with the same explicit intersection formula, followed by its separate delivery conclusion.

2. **MINOR — Bounded subset-exposure ratio is not stronger than average pervasiveness.**

   **Locations:** UNI/REPORT.md:93–94; compare UNI/STATEMENT.md:63–71.

   **Counterexample:** With singleton groups, lambda_j=n^{-1} for every j and Psi=(1-n^{-2})I, Sigma=lambda lambda' + Psi has unit diagonal, uniform idiosyncratic spectral bounds, and metric locality. Here c_G=n^{-2}/(1-n^{-2}), kappa'=n^{-1}/sqrt(1-n^{-2}), and kappa=1. Nevertheless p^{-1} sum_j lambda_j^2=n^{-2}→0, so the usual nonvanishing average-pervasiveness condition fails. Conversely, take Psi diagonal, one lambda_j=0 and all other loadings a fixed nonzero value below one: average pervasiveness holds as p→∞, but the singleton with zero loading gives c_G=0. The conditions are incomparable. The report actually acknowledges the first counterexample's mechanism in the same sentence (“a vanishing common loading scale is allowed”), contradicting “stronger.”

   **Exact fix:** Replace “it is stronger than average pervasiveness” with “it controls every subset and is not equivalent to average pervasiveness; neither condition implies the other.” Retain the vanishing-scale qualification.

3. **MINOR — The report overgeneralizes the GMRF example.**

   **Location:** UNI/REPORT.md:91–92 (“GMRFs with bounded spectrum”).

   **Counterexample:** Bounded spectrum alone does not put a GMRF in LOC_M. For p→∞ let Sigma_p=(1-1/p)I+(1/p)11'. Its eigenvalues are 1-1/p and 2-1/p. Every off-diagonal covariance is 1/p, and every off-diagonal precision entry has magnitude 1/[p(1-1/p)(2-1/p)]. For either branch of LOC_M, a fixed exponential envelope would therefore force every pairwise distance to be O(log p). Polynomial growth with fixed constants would then imply p≤C0(1+O(log p))^d0, a contradiction. This Gaussian field is Markov with respect to its complete precision graph and has bounded spectrum. Thus “GMRFs with bounded spectrum” is too broad without a locality/geometry condition.

   **Exact fix:** Say “GMRFs whose precision has fixed-range or uniformly exponential decay on a polynomial-growth geometry, with uniform spectral bounds.” Likewise make “fixed bandwidth” and uniform stability/locality explicit if the adjacent banded/ARMA examples are meant as class-level containments.

4. **MINOR — Two corollary-table exclusions mistake failure of a class-wide reduction for disjointness of classes.**

   **Locations:** UNI/lemmas/C_corollaries.md:23–24; Theory_work/Wave2/W2-LOC2/STATEMENT.md:76–84.

   **Counterexamples:** “Growing groups violate fixed C0” is true for the particular pseudometric that collapses each whole group to distance zero, not for every possible LOC_M representation. LOC-BF explicitly permits all b_v=0, giving Sigma=I even when the declared groups grow. The line metric puts I in LOC_M with fixed constants, so that member is UNI-0 as well as PLR. Similarly, a polynomial-decay upper bound does not put a matrix “outside LOC_M”: I, finite-band matrices, and exponentially decaying matrices also satisfy polynomial-decay bounds. Neither row should imply that the named classes and LOC_M are disjoint.

   **Exact fix:** Row 6: “PLR; LOC-BF is not contained in UNI-0 as a whole. Its zero-within-group metric has unbounded C0 for growing groups, and genuinely pervasive growing groups also violate the uniform upper spectral bound; overlapping subclasses may satisfy UNI-0.” Row 7: “Separate polynomial-decay extension; polynomial decay alone does not imply LOC_M, although the classes overlap.”

5. **MINOR — N4's search is screened, so its LS0/certification claims are not complete-scan production-method observations.**

   **Locations:** UNI/numerics/n4_r2_pseudo.py:6–8, 40, 223, 280–281; UNI/lemmas/L2_k0.md:212–214; Theory_work/Wave2/W2-APP/numerics/n3b_fastls.py:1–9, 84–92, 107–110; Scripts/SMC_BVS/core/cpp/v3_engine.h:370–378, 394–405.

   **Argument:** N4 imports ls_fast, whose own opening warning says it is a SCREENED search and its certified flag is not a complete-scan certificate. It rescans only swaps whose approximate score is within a fixed 1e-5 window of the approximate maximum. It provides no error enclosure ensuring that discarded swaps cannot win. Production local_search evaluates every feasible swap. Consequently the displayed ls_certified=True and “LS0 ends at S0 in 119/120” are observations about this surrogate unless the complete-neighborhood equivalence is checked for these runs. Validation on other datasets is not that check. This does not invalidate the theorem's explicit complete-scan premise or establish that a reported path is wrong; it limits what this experiment demonstrates.

   **Exact fix:** Run the complete bc.local_search or production neighborhood scanner for the reported runs, or audit all omitted swap scores at every visited center and verify both the chosen move and terminal certificate. Until then label these outputs “screened-search endpoint” and “screened-search termination,” propagate the source warning into N4's docstring and L2's numerical summary, and avoid calling the flag a production LS0 certificate.

6. **MINOR — The numerical “TL margin” omits truth-removing swaps.**

   **Locations:** UNI/numerics/n4_r2_pseudo.py:28–29, 200–204, 264–269, 287; UNI/numerics/n4_r2_pseudo_out.txt:83–87; UNI/lemmas/L2_k0.md:212–213; Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md:15–17.

   **Argument:** TL requires F(T)>F(A) for every feasible truth-losing neighbor A, including (T\{i})∪{l} for i∈S0. tl_margin only evaluates T\{i}. Positive deletion loss does not imply positive swap loss: adding a replacement variable after deletion can recover enough fit to reverse the inequality. The script's detailed docstring accurately says “truth-deletion loss,” but the output label “min TL” and the lemma's unqualified “TL margin positive in 120/120” conceal that only one clause was probed. I am not treating a sampled check as a proof or demanding exhaustive lattice enumeration; the omitted neighbor type is the issue.

   **Exact fix:** Rename the current statistic to “sampled truth-deletion margin,” including in L2 and the output headers. To describe it as a sampled TL margin, also minimize F(T)-F((T\{i})∪{l}) over all feasible truth-removing swaps at each sampled T, using the actual score.

7. **MINOR — N4 mixes out-of-lattice path states into a claimed lattice lower bound.**

   **Locations:** UNI/numerics/n4_r2_pseudo.py:25–30, 230–235, 242–246, 283–285; UNI/numerics/n4_r2_pseudo_out.txt:130.

   **Argument and reproduction:** Q_lat is built from S0, start-mode extras and up to 60 nearby nulls. The later maximum max(lsup,max(path_max_h)) is only a lower bound for the stated lattice supremum if every contributing path state belongs to [S0,Q_lat]. No such restriction is imposed. Reproducing the completed PC2, n=2000, p=300, seed=3 run gives mode (37,62,63,90,178,222,223), followed by (37,62,63,75,90,178,223). Variable 75 is outside Q_lat and its distance to S0 is 3.6492079744967767. Every subsequent path state also contains 75. Thus an actual completed experiment reaches precisely the situation the aggregation fails to distinguish. In this particular run I do not claim that the out-of-lattice value dominates lsup; the defect is that the claimed lower-bound property is not ensured by the computation.

   **Exact fix:** Store lattice_sup_h=lsup and derive lattice NA proxy flags from lsup only. Keep path_max_h and path-based flags separate. Alternatively include path states only after checking S0⊆T⊆Q_lat; if Q_lat is enlarged to include the path, rebuild the corresponding lattice definition, q and threshold consistently.

8. **MINOR — The new numerical summary has an incorrect numerator and denominator.**

   **Locations:** UNI/lemmas/L2_k0.md:211–215; UNI/numerics/n4_r2_pseudo_out.txt:84–87; UNI/numerics/n4_r2_pseudo_out_n8000.txt:44–45.

   **Argument:** The summary says radius-3 sandwich “holds in 95/100 runs,” while describing 120 runs. The six completed groups report radius-3 successes 19,20,20,19,20,19, each out of 20: total 117/120. Independently summing sand_R3 in the two result CSVs gives 117 of 120. No 100-run subpopulation is identified. This is an arithmetic/evidence-reporting error, not an asymptotic objection.

   **Exact fix:** Replace “95/100” with “117/120” and generate all such aggregate counts from the completed result files to avoid stale hand transcription. If a different subset was intended, identify its inclusion rule and recompute both counts.

9. **MINOR — The citation resolver contradicts the advertised no-fallback rule.**

   **Locations:** UNI/citecheck.py:7–11, 105–128, 192–194; UNI/reviews/CITECHECK.txt:2.

   **Argument:** The documented rule says a nonexistent rule-selected path is a MISS and accepts no alternative. resolve instead builds a list of ticket-context, UNI-local, repository-root and other candidates, picks the first existing file, and finally performs a unique-basename search. For example, resolving bare L1_metric.md in an immediately preceding FACA context first tries the nonexistent FAC-A paths, then silently accepts UNI/lemmas/L1_metric.md. Thus a misspelled or misattributed source can obtain OK solely because another source has the filename. Explicit ticket-prefixed paths do avoid this fallback, but abbreviation-context paths do not. Also the actual resolver searches the previous line, contrary to the opening docstring's same-line rule. This finding does not allege that the separately mentioned manual audit was performed incorrectly; that audit was outside the permitted reading set.

   **Exact fix:** Resolve the intended ticket deterministically before testing existence; when a ticket context selects a file that is absent, emit MISS without falling back to the local ticket or a basename search. Specify one consistent rule for previous-line context. Record the rule-selected path in every output. Remove the unique-basename fallback from validation, or treat any such suggestion as unresolved until an explicit mapping is supplied.

10. **MINOR — The automated status check does not establish the advertised verbatim-status coverage.**

    **Locations:** UNI/citecheck.py:18, 69–81, 183–187; UNI/reviews/CITECHECK.txt:1; UNI/REPORT.md:62–75.

    **Argument:** The checker only searches for twelve manually listed substrings anywhere in a source file. It neither extracts every status quotation from the ticket nor checks a status field at the cited result. One entry is just VERIFIED, which would also match VERIFIED-WITH-AMENDMENTS or NOT VERIFIED; FAC-A's status and qualification are checked as two independent substrings. Many quoted statuses, including the T03/M5 provenance strings and OPEN/AUDITED qualifications, are outside this automatic list. The output accurately counts twelve strings, but that is not validation of the broader rule “verbatim status strings quoted in this ticket must occur in their sources,” and it cannot reject a status-strengthening typo such as VERIFIED in place of VERIFIED-WITH-AMENDMENTS.

    **Exact fix:** Maintain an explicit mapping for each quoted status to a source result/status field, compare the entire normalized status value (allowing Markdown markup removal only), and check that every quotation is covered. Until that exists, change the documented scope to “twelve selected substring smoke checks; no automatic validation of complete statuses or quotation coverage,” and leave the omitted statuses explicitly to the manual audit.

11. **NIT — A status advertised as verbatim is abbreviated inside quotation marks.**

    **Locations:** UNI/lemmas/C_corollaries.md:3, 25; Theory_work/Wave2/W2-FAC-A/REPORT.md:20.

    **Argument:** Row 8 quotes “PROVED-CHECKED (for the narrowed, flagged target …)” under a “status verbatim” heading. The source's qualification is “(for the narrowed, flagged target STATEMENT.md v1.2)”. The ellipsis does not strengthen the status, but it fails the requested verbatim-status convention and drops the target version identifying the certified scope.

    **Exact fix:** Quote “PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)” in full, as L4 already does, or explicitly label the cell an abbreviated status rather than verbatim.

12. **NIT — The draft report names an obsolete locked version and stale completed citation totals.**

    **Locations:** UNI/REPORT.md:6, 15, 49, 80–81; UNI/STATEMENT.md:3–5; UNI/reviews/CITECHECK.txt:1.

    **Argument:** The report still identifies STATEMENT v1.1.1 although the binding target is v1.1.2. Its citation totals are 107 path citations and 12 tokens, whereas the completed v2 CITECHECK observed at the end of this review contains 125 path citations and 19 tokens (12 status strings). This is not a complaint about the intentionally pending RESULT or sweep/council placeholders; it is stale identification of already available artifacts.

    **Exact fix:** Change the report's target/version references to v1.1.2, describe its three scope edits accurately, and copy the completed checker totals at report freeze. Associate the totals with the checker version or a snapshot identifier so a subsequent source edit cannot masquerade as the checked snapshot.

13. **NIT — N2's tiny-rate evaluation does not preserve its claimed one-sided numerical direction.**

    **Locations:** UNI/numerics/n2_metric.py:11–13, 24–38; UNI/numerics/n2_metric_out.txt:2.

    **Argument and reproduction:** The analytic series is correctly transcribed, but 1-exp(-t*(m+1)) suffers cancellation when the computed rate is approximately 1e-17. S_fun(1e-20,1,1,1,1) returns 0 although the mathematical series is positive. For the first cluster2d Sigma-branch example, holding the same t1 and other inputs fixed, the implemented second root is 1.2134375073793284e-17; replacing the subtraction by -expm1 and bisecting gives 1.213437509084355e-17. The implemented rate is slightly smaller, not larger, contrary to the unconditional “OVER-estimates t*, … never looser” description. At the implemented root the original and stable series evaluations are approximately 0.05819521725966672 and 0.05819522435157766. The discrepancy is tiny and does not threaten any mathematical lemma or reported zero-violation conclusion, but it disproves the claimed numerical direction once floating-point evaluation is included.

    **Exact fix:** Evaluate the factor with -np.expm1(-t*(m+1)). Qualify the one-sided truncation statement as an exact-arithmetic statement; if certified one-sided constants are desired, add an explicit tail bound and directed/error-controlled evaluation. Recompute the numerical constants after this change.

Counts: FATAL 0; MAJOR 0; MINOR 10; NIT 3.
