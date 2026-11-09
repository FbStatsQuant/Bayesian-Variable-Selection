**Counts: FATAL 0 / MAJOR 1 / MINOR 5 / EDITORIAL 5.**

**Verdict: VERIFIED-WITH-AMENDMENTS for the mathematical proof; correct the implementation handoff before adoption.** I found no fatal mathematical flaw or unresolved major mathematical gap in (P1)–(P5) on their stated, narrowed exact-Gram classes. The MAJOR finding below concerns the proposed implementation instructions, not an asymptotic counterexample. P6 remains open.

Locations below are relative to `Theory_work/Wave2/W2-FAC-PK/` unless a repository-root path is given. These are all the remaining issues I found; repeated occurrences of one issue are grouped together. Finite-n failures of asymptotic inequalities are not findings.

1. **MAJOR — The proposed new option cannot be implemented by the advertised two lines and labels.** Location: `METHOD_REQUIREMENTS.md:36–41`.

   The proposal promises the chosen cap “under a new option value.” The existing R-to-C++ interface destroys that distinction: `Scripts/SMC_BVS/core/v3_run.R:101` maps every value other than `"ell_n"` to `"ell_n_plus_mode"`, and `Scripts/SMC_BVS/core/cpp/v3_core.cpp:394,404` stores only a Boolean distinguishing the legacy cap from every other value. Editing `v3_core.cpp:473` alone therefore either leaves the new value inaccessible or changes the existing MR1 option too. The proposed unconditional replacement at `v3_fit.R:44` likewise does not select a rule-specific preflight bound. The formula and envelope proved in L4 are sound, but this handoff does not implement the option behavior it specifies.

   **Concrete fix:** replace “two lines + labels” by an explicit option-plumbing requirement. Preserve and validate distinct legacy/MR1/MR-PK values in `v3_run.R:101`; carry an enum/string rather than the current Boolean through `v3_core.cpp:394,404`; select the cap after the start mode at line 473 and the matching label at line 479. Pass the selected worst-case scan count into the initial and escalation preflights (`v3_fit.R:115,145`), preserving the existing bounds for retained old options. If a parameterized δ rule is selected, specify its fixed value or validation and its ceiling. Alternatively state explicitly that adoption replaces the MR1 rule globally and remove the promise of a new option value. No production edit is requested by this review.

2. **MINOR — The example of a smaller admissible cap is not an admissible rule on every input.** Location: `STATEMENT.md:90–92`; compare `STATEMENT.md:73–77` and `METHOD_REQUIREMENTS.md:33–34`.

   The rule `⌈1.001|S̃₀|⌉` can be below ℓ_n when the emitted mode is small, whereas P4 requires `a ≥ max(ℓ_n,⌈(1+δ)|S̃₀|⌉)` as a datawise rule. Calling it an “admissible” example is inconsistent with that requirement. The named N1 realization happens to satisfy the lower bound, but that does not establish admissibility of the whole rule.

   **Concrete fix:** use `max(ℓ_n,⌈1.001|S̃₀|⌉)`, as METHOD_REQUIREMENTS already does. This preserves the intended counterexample: in N1's `n=600, p=360, seed=0` row, ℓ_n=10, the start has size 244, the smaller cap is 245, the uncapped path has 248 moves, and MR1's cap is 254.

3. **MINOR — “Largest finite-n margin” is false across the three candidate rules.** Location: `METHOD_REQUIREMENTS.md:19`.

   The p-based cap can greatly exceed `ℓ_n+2|S̃₀|` when the start is unsaturated. The first frozen N3 row has `n=2000, p=1100, |S̃₀|=10, ℓ_n=12`: the doubled-mode cap is 32, while `max(ℓ_n+|S̃₀|,p)=1100`. The p-based cap exceeds the doubled-mode cap in 198/360 frozen N3 rows. Thus the table's unqualified comparison is not supported even by its own data. This is an error in a finite-n comparison, not an objection to an asymptotic theorem.

   **Concrete fix:** say “largest of the displayed linear-in-mode allowances” or qualify the comparison by `|S̃₀|=K`; under saturation and `p≤n−1`, the doubled-mode rule does dominate the other displayed rules.

4. **MINOR — The quoted N3 multiplier interval excludes its observed extrema.** Location: `lemmas/L2_neg.md:78`.

   The statement `M_W ∈ [0.5,2.7]` is not literally true of the frozen data. `numerics/N3_raw_final360.jsonl:15` has `MW=0.483793291871218`, and line 33 has `MW=2.723272799360076`. These are the minimum and maximum over all 360 rows. This does not refute the eventual analytic lower bound on M_T; it is a numerical-reporting error.

   **Concrete fix:** write “observed range approximately 0.484–2.723,” or use an outward-rounded enclosing interval such as `[0.48,2.73]`. Keep this observation separate from the asymptotic multiplier bound.

5. **MINOR — A 24-hour preflight outcome is presented as though it were an observed run.** Locations: `STATEMENT.md:94–96` and `METHOD_REQUIREMENTS.md:52–55`.

   `numerics/full_method/NF_summary.md:8–11` records three 2-hour attempts and one 1000-hour timeout; it records no 24-hour attempt. Its recorded estimate of 527,480 seconds would exceed 24 hours, but that is an inference using the recorded charge. A new fit remeasures seconds per score, so the file does not establish an observed 24-hour outcome or a uniform outcome for every design at those dimensions.

   **Concrete fix:** distinguish the evidence: “The 2-hour attempts returned resource_limit; the recorded ≈146.5-hour preflight charge would also reject a 24-hour allocation if that same charge were used. The 1000-hour attempt timed out after 1200 seconds.” Keep the default-allocation conclusion explicitly labeled as this extrapolation.

6. **MINOR — Growth of the measured seconds per score is asserted without supporting evidence or a proved bound of that kind.** Location: `METHOD_REQUIREMENTS.md:56`.

   The exact preflight formula supports the stated `K·p²·ŝ_K` scaling on this dimension regime. The additional assertion “ŝ_K itself grows with K” does not follow from L4, MACH's upper envelope, or the full-method observations, which benchmark only K=300. Operation-count upper bounds do not establish monotonic growth of a measured runtime across inputs, dimensions and machine conditions.

   **Concrete fix:** delete the parenthesis or replace it with “ŝ_K is measured separately at size K; its dependence on K was not measured here.” A claim about its empirical growth would need attributed measurements at several K values.

7. **EDITORIAL — METHOD_REQUIREMENTS names the obsolete statement version.** Location: `METHOD_REQUIREMENTS.md:3`.

   It identifies “STATEMENT v2,” although the reviewed lock is v3.1 and the method file incorporates later R02/R05 restrictions.

   **Concrete fix:** identify `STATEMENT v3.1 — LOCKED`, including the flagged cap-evaluation restriction for delivery.

8. **EDITORIAL — Several cross-references point to a report that does not exist in the reviewed package.** Locations: `METHOD_REQUIREMENTS.md:3`, `STATEMENT.md:106`, and `STATEMENT.md:108`.

   `Theory_work/Wave2/W2-FAC-PK/REPORT.md` is absent. Consequently the promised status inventory, p≫n heuristics and design-agnostic ingredient list cannot be inspected at the cited destination. Their absence does not invalidate the proofs that are present, but these are dangling package references.

   **Concrete fix:** supply the report before final delivery, or point status readers to STATEMENT §6/L4's input paragraph and replace the frontier references by explicit pending-deliverable wording. Do not present an unwritten ingredient list as existing evidence.

9. **EDITORIAL — L2's numerical-evidence header still points to a nonexistent future script.** Location: `lemmas/L2_neg.md:5–6`.

   It says `numerics/l2_static.py` is “to be added.” That file is absent, while the actual static checks are in `l12_check.py`/`L12_check.jsonl` and `l2_chain.py`/`L2_chain_summary.txt`. R03's review already requested this header update, and its disposition reports stale numerical references as replaced.

   **Concrete fix:** cite the existing files and state their limits: all six L1 samples have N_n=0, and none of the 66 L2 static samples satisfies the extreme-outside-null condition. The chain experiment checks individual inequalities using actual outside extremes; it does not directly observe the proof's threshold event. This limitation is compatible with the asymptotic proof.

10. **EDITORIAL — The coded-partition remark and the statement assign different proof statuses to (PB).** Location: `lemmas/L1_start.md:73–78`, versus `STATEMENT.md:52–54`.

   L1 begins categorically “(PB) holds for the method's partition ... under EX-A”; STATEMENT explicitly treats this as a sketched argument with five numerical checks and says it is not a proved property of the coded partition. R01's disposition likewise retains (PB) as a hypothesis. The theorem itself correctly assumes (PB), so no P1/P2 conclusion needs this implementation assertion.

   **Concrete fix:** label L1.4(3) “Sketch suggesting (PB) for the coded partition; not used as a proved implementation property,” and retain the independent (PB) hypothesis. Alternatively provide and consistently label a complete audit/proof of all relevant clustering, tie-breaking, cutting and packing rules.

11. **EDITORIAL — NEG's formal cap quantifier omits its lower domain bound.** Location: `lemmas/L2_neg.md:59`.

   The headline event says “∃ integer a ≤ ...,” while LS0(a) is defined only for nonnegative integer caps (`STATEMENT.md:39–40`) and the proof at L2:62–63 explicitly uses that domain. The global definition makes the intended meaning clear, but the formal event should carry the restriction, especially because nonnegative caps were an accepted R01 amendment.

   **Concrete fix:** write `∃ a ∈ ℤ_{≥0}` with the displayed upper bound. This aligns the lemma with P2 and METHOD_REQUIREMENTS without changing any mathematical conclusion.

**Proof and source audit.** I independently checked L0–L4 and the locked statement against FACB L1–L5, FINAL s3/s6/s7, HQ audits A1/A2/A4, GEN's [OP], SoP's score/start/search definitions, and the cited production lines. The quoted dependency statuses agree with their records, including VERIFIED*, [OP]'s unchecked-by-seat qualification, CAP's council check, and the separation between Proposition F's council-reviewed form and A4's later preflight addition. The new PK theorem does not acquire council approval by importing those results.

The mathematical checks pass: the algebra extends to p=n−1 with r=0; L1's exchange and concavity bounds are uniform over block subsets and maximisers; its saturation argument uses PK′ rather than truth keeping. L2's threshold density has the stated constant −17, its regular-block count and Chernoff comparison are valid, and its counting argument excludes scoring S₀ in the extra scan as well as visiting it. L3's projection lower tail is uniform over all relevant sets: its union bound is `2^n(ce)^(n/8)=2^(−n/8)` for the stated c. The tail-count interpolation, one-sided coefficient, small-distance case, small-energy import and two large-m regimes give the stated deletion gains. Endpoint existence is now proved before using F(S₀) as a budget; later additions do not invalidate the remaining-potential argument. The 2.39/2.4 constants, the `(1+6ε)K` budget and the final choice of ε leave the required fixed δ slack. P4 uses discovery plus posterior concentration, without reversing [OP]; delivery retains the total fallback, cap-evaluation restriction, ideal-machine premises and recharged allocation. No optimality or two-phase path theorem follows, and none is needed.

**Numerical audit.** I used the specified Python 3.13 with NumPy and independently recomputed the saved aggregates. N1 has 60 rows, 55 saturated starts, the five stated unsaturated sizes, exactly 53 MR1 misses (all saturated), 60 doubled-cap discoveries, and the four stated p/n=0.95 swap-count ranges. Every N1 path has the stated null-swap/null-deletion form. N3 has 360 rows, the four correlations and five layouts, no additions or swaps after the first deletion, exactly nine endpoint misses in the stated near-cancelling layout, 360 doubled-cap discoveries, and maximum m*/K exactly 1.26. Its truth-inserting swaps and occasional truth deletions do not contradict the more limited N3 description in STATEMENT. Both frozen SHA-256 digests match their manifest.

The L2 chain summary recomputes exactly (48 passing rows; 42 applicable and passing implications). The six L3 static summaries agree with their 988 raw rows; all stored best-deletion gains are positive. The nine small-m summary minima agree with the 288 raw rows. I reran `l3_trend.py`; its parsed output equals `L3_trend.txt` exactly. The self-test output supports five partition comparisons, eight start-mode/path comparisons at the stated level of detail, and the FACB N2 reproduction (300-variable start, 19 swaps, 296 deletions, 315 moves). The N2 diagnostic files support L1's three mixed-block/lowest-50 assertions. The full-method files support incompleteness and the recorded preflight/timeout observations, subject to finding 5.

For an additional independent algebra check, I constructed centered exact-Gram matrices directly, without importing the ticket's scorer, at n=14, p=13, with mixed-sign truths and two (ρ,σ) configurations. Across 5,620 feasible neighbour comparisons, the maximum gain discrepancy was 9.29×10⁻¹⁴; the maximum ψ discrepancy was 8.27×10⁻¹⁴, and no Q-versus-RSS bound failed. These are identity checks, not finite-n tests of PK′ or asymptotic onset.

I checked R01–R06 dispositions against the current files. Their substantive mathematical repairs are present: narrowed scope, no TK, no-ties event, corrected static dependencies/error terms, endpoint-before-budget ordering, exponent slack, and the v3.1 delivery restrictions. Findings 2, 9 and 11 identify remaining presentation/domain inconsistencies associated with those amendments, not missing versions of the repaired arguments.

Only `reviews/R07_scratch/` and this review file were written. Reproducible checks are in `reviews/R07_scratch/audit.py`, with results in `audit_output.txt` and `trend_rerun.txt`. No git state, proof source, numerical source or production file was changed.
