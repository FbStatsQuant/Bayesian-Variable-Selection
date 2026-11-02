# Claims of fatal flaws and gaps

Round 1: neither reviewer reported any fatal or gap finding; both returned verified. Thus there are no fatal/gap claims to log. Their full verbatim reviews are in review/round_1/REVIEWER_1_REPORT.md and REVIEWER_2_REPORT.md.

## Exposition finding (included for complete processing history)

Reviewer 1, verbatim finding:

> - **Location:** §3, PDF p. 4, sentence following the Taylor-remainder inequality.
> - **Severity:** exposition.
> - **Claim:** The approximation holds “uniformly on that family.”
> - **Evidence:** The hypothesis \(\max_{i<c}nx_i^2=O_{P_0}(1)\) establishes uniformity over the selected chain comparisons. It does not establish uniformity over the potentially larger comparison family in (6). The displayed approximation uses the chain indices \(i\), so its chain interpretation is valid; the wording leaves its scope ambiguous.

Reviewer 2, verbatim finding:

> - **Location:** §3, PDF p. 4, paragraph beginning “The weaker condition,” sentence ending “uniformly on that family.”
> - **Severity:** exposition.
> - **Claim:** The referent of “that family” is ambiguous.
> - **Evidence:** The hypothesis \(\max_{i<c}nx_i^2=O_{P_0}(1)\) establishes Taylor-remainder control uniformly over the selected chain comparisons indexed by \(i\). It does not establish that control over every comparison in the potentially larger EXP-prime family. The displayed conclusion uses \(x_i\), so its chain-indexed interpretation is valid and agrees with `STATEMENT.md`.

Lead's answer: accepted and fixed in PROOF_v2.tex, section 3. The phrase now reads “uniformly over the selected chain comparisons i=0,...,c-1.” This changes no formula, hypothesis, quantifier in STATEMENT.md, or conclusion; it makes the existing chain-indexed scope unambiguous. No unresolved objection remains from round 1. Both reviewer roles receive the unified proof and this log for round 2.

## Final processing: round 2

Both reviewer roles returned verified on PROOF_v2 and explicitly agreed that the lead's fix resolves the finding. Neither reported a fatal error, gap, new exposition finding or unresolved objection. The complete verbatim final reports and task metadata are preserved in review/round_2/. No judge was needed. The proof is complete as a conditional implication; H2 and H3 remain statistical premises.
