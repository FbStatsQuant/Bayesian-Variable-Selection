# CLAIMS OF FATAL FLAWS — T21
Both independent Sol reviewers returned verified with no findings. No proof-review fatal or gap findings were received. The statement-check rejection below is a pre-review scope issue; the checker did not assign a fatal/gap severity.

## Statement checker round 1: verbatim report

**REJECTED — one narrow probability-scope correction is required.**

In [PROPOSED_STATEMENT.md, line 71](/<OLD_ROOT>/01_Methodology_and_Theory/Theory_architecture_v3/proofs/T21_T14H_HPM_composition/review/PROPOSED_STATEMENT.md:71), the sentence

> “A predictable, uniformly positive lower bound b_* … can replace b in the same stopped-opportunity bound.”

is insufficiently qualified. The displayed bound is an unconditional numerical inequality with a fixed scalar \(b\). Predictability alone permits a random or time-varying lower bound; it does not justify substituting that bound unchanged into \(\delta+(1-b_*)^D\).

Replace it with:

> A deterministic lower bound \(b_*\in(0,1]\), valid at every counted neighbour-swap opportunity before discovery, can replace \(b\). A random \(b_*\) may be used in the conditional version when it is measurable with respect to the information conditioned on and bounds every subsequent counted opportunity. Unconditional averaging then requires the corresponding expectation of \((1-b_*)^D\).

This is a **local restriction and clarification of the neighbour-swap extension**, not an algorithm change. No broader revision is required.

The remaining consequential readings are acceptable:

- **Dependency boundary:** H03, H10 and H24 correctly assume the needed conclusions without claiming that their primitive sufficient conditions have been proved. These are the user-authorised changes to the theorem’s hypothesis structure.
- **Route (a):** Full execution matches wave-1 T11(iii), particularly its setting item 5. The proposal correctly avoids conditioning on future completion or diagnostic success. The one-deletion intensity statement is understood on launched runs.
- **Occurrence and exposure:** Routes (b) and (d) are deterministic scoring implications with explicit occurrence conditions; route (c)’s uniform-swap statement requires exposure; route (e) retains eligibility, execution and rate conditions.
- **Terminal repair:** The uniform kernel and exit bounds, and the asymptotic repair inputs, remain explicit hypotheses. No unproved implication from LK, EXIT, GAIN or T03 is asserted.
- **Sufficient dimension range:** “The lower bound supplies no proof of failure above [the range]” correctly resolves the source’s ambiguous wording without invoking T27.
- **Ledger and exact branch:** Including tables in the explicitly defined pre-final ledger, and defining unused component objects abstractly on the exact branch, are compatible with the method.

I found no further blocking formalisation issue in C1 or routes (a)–(f). This report assesses the statement only; it does not approve a proof.

## Lead answer

Accepted. Reanalysed the source statement and narrowed the neighbour-swap extension exactly as requested: deterministic fixed b_* for the unconditional scalar bound; random b_* measurable at the conditioning boundary and then averaged. The original proposal is preserved as review/PROPOSED_STATEMENT_r1.md. The corrected statement was approved in statement-check round 2 (review/STATEMENT_CHECK_R2.md). No algorithm or source theorem file was changed. One statement-analysis restart; no counterexample submitted.

## Proof-review findings

Round 1 complete. Reviewer 1: verified, no findings. Reviewer 2: verified, no findings. The lead inspected both reports and accepts both verdicts. There are no outstanding proof findings. The statement-check scope correction above was resolved before either proof review. Final PROOF_v2 differs from reviewed PROOF_v1 only in the author/status metadata; mathematics is unchanged.


