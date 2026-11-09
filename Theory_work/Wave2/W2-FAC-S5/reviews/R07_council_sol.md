# R07 — Independent Council seat: Sol, round 1

**SCORE: 7.8 / 10.0. Verdict: corrections required before package acceptance.**

I find the Tier 1 theorem in `STATEMENT.md` v2.3, claims (C1), (C2-R), (C3-R), and (C4-R), mathematically sound under its named premises and inherited dependency qualifications. I do not find a missing Tier 1 proof step. The package does not pass as written because `REPORT.md` overstates the start conclusion and omits material restrictions when summarising the unfinished KL work. These require reporting corrections, not a proof of KL. RESULT = PARTIAL is the correct ticket result.

This is an independent review against `reviews/COUNCIL_BRIEF.md`. I did not consult or coordinate with the other council seat. I wrote only this file. Repository HEAD inspected: `dce9e0b73e8250704560b9307421431785723def`; the production-core diff against the specified merge `4676af6` is empty.

## Six gates

| Gate | Verdict | Reason |
|---|---|---|
| G1 — correctness of every step | **FAIL, package level** | L1–L5 support Tier 1, as detailed below. However, the front-page assertion that the start is the whole model for every admissible design is false (`REPORT.md:5`, repeated at line 14). The actual result is S* = [p] minus N0. This is a mathematical scope error in the deliverable, although the formal theorem and its proof already have the correct exception. Required fix 1. |
| G2 — hypotheses used = hypotheses stated | **FAIL** | The report's 250-null endpoint result and conditional exponent 0.4126 omit the source assumption s0=4. Its singleton/champion/path summary also omits the exact-noise-argmin restriction, which is different from the score-defined Pi of Tier 1. Required fixes 2–3. The formal Tier 1 hypothesis accounting passes. |
| G3 — no hidden assumptions | **PASS** | Tier 1 uses exact Gram, fixed parameters/support size, a global eigenvalue floor, bounded group sizes, the stated genericity condition for the start, and the explicit centre event. The proof does not assume independence of adaptively selected statistics, vanishing centre error, conditional sign symmetry, or data-measurability of CC. The frontier scope errors are identified under G2; none is silently used to prove Tier 1. |
| G4 — adequate dependency status, no upgrading | **PASS** | T38-(0), T03-sharp, [OP], CAP, corrected F/F-GROW, and A4 retain their recorded qualifications. The new BCS delivery extension does not inherit council approval from FAC-CS or Proposition F. KL attempts are explicitly labelled unchecked and are not used in L1–L5. Those labels must remain when correcting their scope. |
| G5 — constants and rates tracked | **PASS for the claimed theorem** | The repaired leakage rate, determinant remainder, multiplier onset, Gaussian-family counts, fixed delta margins, and truth-loss constant suffice. Bounded p and the p/n boundary for the start are distinguished. The numerical 250/0.4126 frontier constants need their missing hypotheses restored under G2. |
| G6 — fidelity to v3.1 / 4676af6 / MR1 | **PASS for Tier 1** | Pi is defined by the exact ridge score, with lexicographic neighbour ties; null-out swaps are treated as exact deletion-plus-addition gains. Complete scans and the final scan give the stated cap consequences. The merged cap and delivery/preflight amendments are correctly imported. Numerical replicas and candidate-restricted scans are identified as such. This pass does not transfer exact-noise-argmin research lemmas to the actual score path; fix 3 must make that boundary explicit. |

The Council acceptance condition (all six gates PASS and score at least 8.0) is not met in this round.

## Independent proof audit

**L1: algebra and score.** The inverse formula has strictly negative off-diagonal entries, including across groups; taking the inverse of the two-coordinate precision block justifies positive partial covariances. The posterior normal equation for h, independence of the group residual from (h,g_R), and variance decomposition give the displayed tau identity. The coefficient c_u/s_u is maximised at u=0 and equals kappa0. The sign reduction preserves scores.

The Schur-complement gains use the shipped normalised response and ridge matrix. The null signal leakage is indeed a^(-1) beta-tilde' theta, giving the repaired sqrt(k)/n^(3/2) contribution. The Q-versus-RSS argument imported from FACB L1.5(b) uses only the eigenvalue floor and signal containment, so it applies here. With p=o(n), E2 gives the stated uniform multiplier limit. The eigenvalue calculation gives an o(1) determinant increment remainder in the path regime; the start uses only block-size increments and does not require that multiplier limit at p/n=1/2.

**L2–L3: start and probability event.** Fixed s0, fixed coefficients and finitely many incidence patterns make the nonzero population increments uniformly separated from zero. FS-BCS is used exactly where required. Signal-bearing block additions dominate the logarithmic penalties; the only zero pairs lie in the unique method block containing all truths. E_S is now block-local and its family has bounded cardinality. This proves the start S*, including the possibility N0 nonempty, without a union over exponentially many global sets. The other Gaussian and chi-square bounds are sufficient for P(E_n) tending to one. The truths require only finitely many A-statistics, while the null family has at most p times 2^(qbar-1) members.

**L4: conditional path.** CC includes the parent, every possible one-null-deletion base, and the terminal state. It therefore controls all the statistics needed for deletions, additions, and null-out swaps, including nulls excluded at the start. The size thresholds differ from Lambda_k only by the tracked determinant remainder and a bounded 2/p term. Regularisation and multiplier errors vanish fast enough that the fixed delta slack yields the delta/8 log(n) margins. The addition after any null deletion is negative, so its swap cannot beat the best deletion. Truth-removing moves use a separate order-n bias bound; the uniform noise bound follows from E3 and the all-set bound on e_R, without CC. This covers every feasible neighbour at S0 and establishes strict termination. The m0=0 case is included.

**L5: assembly and delivery.** The all-principal-submatrix eigenvalue floor verifies both anchored sparse-eigenvalue hypotheses of T03-sharp, and fixed nonzero coefficients verify beta-min. The data-measurable discovery event K_n contains E_n intersect CC on the enlarged space. Thus its failure probability is bounded by P-tilde(CC complement)+o(1), without conditioning on an unobservable latent event. [OP] and composition establish (C3-R). The CAL-free delivery argument separately verifies the input/scorer conditions and uses F's full amended allocation and D-prime's scored-set inclusion; it does not reverse the inequality D_n <= P(K_n complement). I checked these against FACB L5, FINAL s3/s6/s7, W1-GEN's [OP], SoP's D0/composition/status entries, and HQ audits A2/A4.

**Frontier.** Keeping KL open and retaining the unconditional exponent below 1/6 is justified. The round-2 lattice obstruction is a valid obstruction to this sufficient all-set CC route: select one designated coordinate in each of many truth-free groups, then retain sufficiently large same-sign observations. At size p^theta, the maximal normalised field has leading constant sqrt(1-theta); substituting into CC gives the cutoff 1/(2+4 sqrt(1-theta)). A growing subpolynomial retained count gives the 1/6 limit. This does not show the extremal set is reached by Pi, does not refute consistency, and does not make CC a necessary condition for the method. The report mostly makes those distinctions correctly. The restrictions below must also be preserved.

## Required fixes

1. **Correct the full-start claim in the report.** At `REPORT.md:5` replace “the start mode is the whole model for every p <= n/2” by “with probability tending to one, the unique start mode is S* = [p] minus N0, with |N0| <= 15; it is the whole model when N0 is empty.” At line 14 replace the parenthetical accordingly and qualify the essential-cap statement to the growing-start regime (for example, m0 much larger than log n).

   This exception is not hypothetical. The report's own `numerics/S4_out.txt` contains S5 with p=100, n=10^6, one truth and N0 of size 9, giving start size 91; its onegroup layout has N0 of size 8 and start size 92. The formal C1 and L2 already handle both correctly. No theorem change is required.

2. **Restore s0=4 and the precise endpoint regime in the KL summary.** In the opening flags and `REPORT.md:85–90`, specify that the final-two-null result, the final-250-null specialisation, and the numerical conditional terminal exponent are for s0=4 under the respective source hypotheses. Cite `lemmas/KL_attempt_sol/README.md:9–15`, `lemmas/KL_attempt_sol2/01_group_lattice.md:135–159`, and `lemmas/KL_attempt_sol2/05_conditional_terminal.md:3–29`. State the exact remaining range as at least 251 retained nulls and parent size k < ceil(p^0.06), in that specialisation; do not identify retained-null count with total parent size. The dense all-set bound itself need not be narrowed to s0=4.

   The missing support restriction affects the mathematics. With S5 parameters and s0=1, the truth anchor is lambda0=10/3. Choosing 250 extreme same-sign designated null coordinates from distinct truth-free groups gives asymptotically

       kappa0 |e_T| / sqrt(2 log p) -> 250/(250+10/3) = 75/76.

   At log(p)/log(n) -> 0.17, the corresponding parent CC ratio tends to

       [0.34/1.34] (1+75/76)^2
         = 387617/386992 = 1.0016150204... > 1.

   Existence of those 250 extremes with normalised level tending to one follows from the same designated-coordinate Gaussian order-statistic argument as the lattice obstruction. Hence the unqualified all-set 250-null assertion is false even for CC with delta=0 in an allowed truth-size regime. This is an all-set witness, not a counterexample to the actual path.

3. **Separate exact-noise-argmin path modules from the actual score path.** In `REPORT.md:12` and `REPORT.md:85–91`, label the singleton/cohort, champion, and conditional-terminal results as unchecked research for exact argmin of |tau_j(T)|. Add that perturbation stability/transfer to the exact ridge-score Pi is unproved. Preserve the pre-gate field assumptions and the conditional nature of the terminal exponent.

   The sources are explicit: `KL_attempt_sol/03_protected_champions.md` says its strict gap can be arbitrarily small and does not establish protection for near-argmin rules; `KL_attempt_sol2/03_singleton_cohorts.md` starts “Exact argmin deletions only”; `KL_attempt_sol2/05_conditional_terminal.md:6` assumes exact argmin and s0=4. By contrast `STATEMENT.md:97–100` defines Pi using the full score. The KL brief allows first studying exact argmin, but does not prove that these paths coincide. No stability theorem is needed to finish this PARTIAL ticket: accurate qualification of the research evidence is sufficient.

## Verification performed

I reran, with Python 3.13 and bytecode writes disabled, `bcs_selftest.py`, `l1_identities.py`, and `l1_leak.py` from `numerics/`. Their outputs reproduce the recorded five scorer comparisons, 361 retained identity instances (maximum normal-equation error 1.42e-14, zero tau-bound violations), and the leakage/reconstruction results at n=10^4, 10^6 and 10^8. The maximum absolute flip error in the scorer comparison was approximately 5.22e-7 at n=10^8; the maximum best-swap error was approximately 2.68e-8. These are falsification checks, not exact-arithmetic proofs.

I also ran an in-memory 12-case complete-neighbour scan at p=30, n=10^14, S5 parameters, three truth/start layouts and fixed seeds 700–711. All 12 satisfied the tested CC(0.05), followed the exact best-null-deletion path, and terminated at a strict S0 endpoint. Eight cases had nonempty N0, of sizes 4 or 6. The minimum deletion gain was 0.448 log(n), and the minimum null-out-swap gap was 0.454 log(n). No auxiliary test file was written.

The saved exhaustive runs reproduce 15/15 successful paths with zero reported exact ties in each scan directory. The candidate-restricted collection has 27/27 successful paths but 78 reported disagreements between score-best deletion and noise-argmin across its runs. Those finite-n observations are not an asymptotic counterexample; they reinforce why path identity must not be assumed. I inspected the production scan, neighbour tie rule, MR1 cap, and preflight premises; this is not a new comprehensive production-code audit.

## Optional suggestions

- Add one compact frontier table listing each research module's support size, path rule, field premise, exponent and unchecked status. That would prevent these reporting restrictions from disappearing in subsequent summaries.
- Keep general-loading extensions and random-row perturbation-rate heuristics explicitly separate from the proved ingredient list in REPORT section 7; those extensions are not established by this ticket.

**Disposition:** retain Theorem FAC-BCS-R and RESULT = PARTIAL. Correct the report as above and resubmit the package; do not promote KL or require its completion as part of these fixes.
