# FINAL REPORT — T03 (A2): selection, screening, PIPs and the global HPM

**Result label:** proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted. Adoption is Felipe's word.

**Final files:** `STATEMENT.md` (SHA-256 67e92149…a627b7), `proof/PROOF_v2.tex` (bbc0bc0a…885d0), `proof/PROOF_v2.pdf` (140ca00a…12585, 10 pages). Date 2026-10-22.

## What is proved
Under G, R, SE, the explicit hypothesis H-T02 (= v3 T02(i), being proved in a sibling thread), and BM-C (or BM-∞), in regime R1:
- (i) 1 − π(S₀) = O_P(r_n);
- (ii) max_j |PIP_j − 1{j∈S₀}| ≤ 1 − π(S₀) for every data set; P(MPM = S₀) → 1;
- (iii) P(S† ≠ S₀) ≤ 2E[1 − π(S₀)] → 0; on {π(S₀) > ½}, S₀ is the strict global maximiser of F;
- (iv) screening (no beta-min): Π(S ⊉ J_n | y) = O_P(r_n), min_{j∈J_n} PIP_j → 1;
- (v) null-truth vacuity and scale invariance of BM.

## Statement changes
None (proof.md step 1(a)). T02(i) enters as the explicit hypothesis H-T02, as the brief requires for unproved v3 results. T01 is not used: the only reduction needed (standardised score = contrast score with IG rate b = 0.01·s_y²) is proved inside the proof (Lemma 1). The theorem file's two closing sentences (no frequentist rate follows; M_* not sharp) are recorded as remarks, not claims (STATEMENT.md §4). Statement checker not used (no change to check).

## The BM-C constant (flagged provisional in THEOREM_MAP)
M_* = 2L_* + 1 works as stated. The proof uses BM-C only through (1 − 1/n)M_* ≥ L_*, so any fixed M > L_* also works (Remark 16). L_* itself comes from the noise threshold (L ≥ 4C_*) and the multiplicity/prior cost (L/32 ≥ s₀(A+1) + 2). Sharpness is not addressed.

## Source of the argument
The old label is T3, but the old `Proposed_project/proofs/T3_T11` proof is a different (fixed-p, start-limit) theorem. The argument was adapted from old `T7_T8/PROOF.md` §§1–5 (supersets size by size with a truncated chi-square moment; underfitting S compared with S ∪ S₀; finite j_* split). v3 changes handled: n − 1 contrast coordinates; random IG rate b = b₀s_y² (common to all models, so only bounded on the good event — no change-of-rate argument needed); eigenvalue scale (n − 1)φ₀²; prior and cap via ℓ = w·m; Laurent–Massart bounds re-proved in full (no external citation).

## Review history
- Round 1 (PROOF_v1): CP verified (4 exposition findings); CW verified (8 exposition findings). No fatal or gap findings → CLAIMS_OF_FATAL_FLAWS.md records none. All findings accepted → PROOF_v2 (renames y_c / υ_n / Υ_n, scope and tightness remarks, uniformity of n₀, direct bound in (iii), attribution removed). No mathematical step changed.
- Round 2 (PROOF_v2): CP verified (3 new exposition nits); CW verified (4 new exposition nits: υ vs ν look-alike; M-family overlap; s₀ ≤ K threshold is uniform since s₀ ≤ p; "bounded below" wording). Not applied: both verdicts are on v2 as it stands, and none affects correctness.
- Disclosure: in round 2 the CP reviewer ran a byte comparison of STATEMENT.md and REPORT_FORMAT.md against its own round-1 packet copies (identical); it opened nothing else outside its packet.
- Judge: not used.
- Reports: review/REVIEW_CP_r1.md, review/REVIEW_CW_r1.md, review/REVIEW_CP_r2_summary.md, review/REVIEW_CW_r2.md, review/CHANGES_v1_to_v2.md.

## Numerical checks
helpers/check_T03.py → helpers/check_T03.out: 1958/1958 checks pass (single seed, local): score identity, Gram/contrast identities, ridge-smoother bounds, Corollary, determinant ratios, signal bound, prior ratios, truncated chi-square moment. Both reviewers ran their own independent single-seed checks (0 violations).

## Open items
- Conditional on T02(i) (H-T02). If T02(i) is proved, T03 becomes unconditional given G, R, SE, BM.
- Optional polish for a later version: the four round-2 nits listed above.

## Agent counts
Lead: Opus 5.5 (high), 1. Helpers: 0. Statement checker: 0. Reviewers: 2 Opus 5.5 xhigh (CP Plan agent: 2 rounds via resume; CW via delegate_task: 2 rounds). Judge: 0. Fable: 0.
