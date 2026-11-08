SCORE 9.0 / GATES G1 PASS; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 PASS

# Independent council review — W1-GEN, round 1

Reviewer: Codex GPT-6.1 Sol, high reasoning effort. Date: 2026-11-08.

Verdict: PASS. The score is uncapped. No required mathematical fixes were identified in STATEMENT.md v2.3 and the supplied proof package. This is a review of the stated sufficient theorem, including its named implementation premises and explicitly conditional external inputs; it does not discharge those premises or establish delivery.

I read PROTOCOL.md, STATEMENT.md, 00_MAIN.md, and L1–L8 in full. I checked the relevant score, partition, search and LS0 specifications in State_of_Project/sections/02_method.tex; the M5 and TH09 cards in 04_theory.tex; the agent brief and open-plan source; T22's aggregation statement and the T22(iii) proof text; the LH-iid setup and partition argument in the archived API-PXNGAP proof; and Scripts/Data_generators/gen_dev_data.R. The judgments below come from checking the arguments, rather than treating previous review verdicts as proof. No numerical experiments were run for this review.

## G1 — Correctness of every step: PASS

L1 correctly works on the raw-centred response before translating to the standardized shipped score. Its projection identities, union bounds, determinant expansion and bounded score remainder are valid. L2's substitution of a feasible bounded reference S* for the truth is legitimate: the borrowed residual and truncated-integral arguments need deterministic signal and bounded energy, while completion uses VIS, rather than global representability by S*. L3's best-truth decrement follows from the Schur complement and the l1/l2 inequality; SEP controls outside additions and swaps at the appropriate base sets. Its distinct treatment of missing-truth states and truth supersets closes the greedy-path argument without demanding a margin between competing moves inside the relevance set. L4's finite-state argument and scan-versus-move accounting are correct, and L5's operational inclusion, bounded-expectation argument and canonical conditional-probability construction complete the result. L8's exact and thresholded certificates follow from projection geometry and the reverse triangle inequality. I also checked L6's instance arguments and L7's growing-proxy construction; neither requires applying the bounded-reference concentration theorem outside its domain.

## G2 — Hypotheses used equal hypotheses stated: PASS

The hypotheses in the proof match the target statement. H0 transcribes TH09's anchored eigenvalue conditions, deterministic prior-tail cutoff and BM-infinity regime (04_theory.tex:775–782). H1 supplies the floors for every neighbour considered by L3, separation at both S and S minus an exchanged coordinate, and bounded cardinality for the extra-deletion family and path length. H2 supplies within-block invertibility, reference visibility, a uniform logarithmic leakage bound and the averaged exponential bound used by L2. Bounded energy is expressly included for the canonical certificate. The favourable route correctly dispenses with H1 because the emitted centre itself scores the truth. The random-design theorem demands deterministic-sequence validity on high-probability design events, with common constants and envelopes; L6 constructs events with precisely that purpose. L7 explicitly removes both size bounds and confines its negative conclusion to LS0 discovery.

## G3 — No hidden assumptions: PASS

The potentially problematic randomness and selection steps are addressed. Gaussian calculations use the raw noise, not an independence assertion about standardized errors. LH-iid fixed-group laws are established before intersecting partition recovery. For the study generator, Lemma SEL first uses unconditional fixed-pair Beta laws on a deterministic family of at most 2^75 possibilities per column, then controls the effect of the additionally selected null columns through uniformly small partial correlations. The sample scaling of the truth columns does not invalidate that Beta argument: the raw residual is independent of all truth columns, so also of their sample scales and the resulting mean. C4 uses a canonical measurable integral at every admissible design, avoiding a conditional-version exceptional-set problem. S* and the relevance set are oracle certificates, not claimed to be available from X alone. Exact arithmetic, complete scans, e4 and the operational output contracts remain explicit assumptions.

## G4 — Adequate status of cited inputs: PASS

The package preserves the quoted M5(0) and T03-sharp statuses, labels T22(iii) as PROVED-LOCKED CONDITIONAL in its original form, and supplies the additional score-expansion proof instead of silently removing that condition. T22(i)'s deterministic statement explicitly permits any feasible reference, which is the actual generality needed here. The LH partition input retains its same-family-only qualification; LH-iid remains conditional on the candidate W7-PART input and the stated concentration input. N3/e4 is visibly OPEN and stipulated as an implementation premise, rather than declared proved by this ticket. The operational inclusion in L5 has its own pathwise justification from the named contracts, so the candidate API-PXNGAP citation is corroboration rather than an unlabelled theorem upgrade. New results retain their author-side unchecked status pending this review pipeline.

## G5 — Constants and rates tracked: PASS

The important scales are explicit and sufficient: L1 has fixed-family constants and a uniform O(1) score remainder; L2 obtains O_P(2^B sqrt(log n) n^(-kappa)) and a superpolynomial completion bound, with B at most 16. L3's L_n/log n tends to infinity, overcoming all O(log n) costs, including the fixed positive separation factor 1-c_S. Finite-family noise deletions cost at most (log log n)^2, whereas additions retain a negative half-log-n margin after the BB prior cancels the log-p maximum-noise cost. L4's 2^vbar-1 move bound is eventually below the prescribed cap. L6's critical Beta exponential moment is O(n^(1/4)); Markov at n^(3/8) gives the claimed kappa=1/8, and SEL's perturbation contributes only O((log n)^(3/2)/sqrt(n)) in the exponent. L7 chooses d=16(2 ell+5) explicitly, giving the required strict distance obstruction while preserving VIS. No expectation rate is inferred from an O_P rate.

## G6 — Fidelity to the coded/specified method: PASS

The proof uses the shipped regularized g=n score and capped BB(1,p) prior, the actual complete-linkage/size-cut/next-fit partition, and exact block tables against the full response. Its local search uses posterior score F, complete flip/swap scans, a frozen centre, strict improvements, the specified tie rule and one scan after the move cap. It distinguishes scored neighbours from visited centres and distinguishes certification of a search endpoint from the public flag on the reported HPM. The all-scored HPM rule, table contributions, LS0 emission, GUARD-W and the additional search for R'>4 are preserved. The study instances establish unions of whole groups where that is warranted, rather than imposing blocks=groups when SIZE fails. The generator extension is expressly theoretical and asymptotic; neither an n=200 guarantee nor implementation-audit closure is asserted. These checks agree with 02_method.tex:187–211 and 463–506.

## Required fixes

None.

## Optional suggestions

1. **STATEMENT.md, (C1-prime), lines 91–93:** replace “after absorbing the small part” with the exact root-margin inequality in L8.2(ii), or an explicit pointer to that numbered inequality. The proof already contains the correct condition; reproducing it would make the statement independently checkable without interpreting the shorthand.

2. **L6_instances.md, Lemma SEL(iv), lines 160–162:** write the final probability bound explicitly as P((G_n intersect K_n)^c) plus O(n^(-1/8)), applying Markov to the deterministic-family sum. The current argument supports this bound, but the displayed domination holds on the good event; making the separation explicit would prevent a reader from interpreting it as a global expectation bound for the selected maximum.

3. **STATEMENT.md (C5)(d) and L6_instances.md, sequence definition:** spell out that c is a fixed positive study scale (or list the five positive scales from the generator). This is already the natural reading of “study generator” and is consistent with s0=14, but would remove a small ambiguity in standalone reuse.

The passing verdict applies to the complete package as scoped above. It does not establish unconditional full-method failure in C6, delivery probability tending to one, or consistency for S2/S5.
