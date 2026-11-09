# R09 — Independent Council seat: Sol, round 2

**SCORE: 8.8 / 10.0. Verdict: ACCEPT the Tier 1 reduction; retain RESULT = PARTIAL.**

All six gates PASS. I find no missing step in Theorem FAC-BCS-R, claims (C1), (C2-R), (C3-R), and (C4-R) of `STATEMENT.md` v2.3, under its stated implementation premises and inherited dependency qualifications. KL / (C5) remains open. No unconditional improvement beyond FAC-A's exponent 1/6 follows from this ticket. There are no required fixes for acceptance; one nonblocking numerical-reporting erratum is recorded below.

This is an independent review against `reviews/COUNCIL_BRIEF.md`, not a joint verdict with the other seat. I read the current statement, report, L1–L5, cited numerical scripts/results, the relevant SoP/FINAL sources, W1-GEN's [OP], HQ audits A2/A4, and the FAC-B predecessor. I also inspected the KL sources behind the frontier summary and FAC-A's stated range. I consulted the round-1 reports/disposition after first reading the current proof. Repository HEAD: `dce9e0b73e8250704560b9307421431785723def`. The production-core diff against `4676af6` is empty. I wrote only this review file.

## Six gates

| Gate | Verdict | Reason |
|---|---|---|
| G1 — correctness of every proof step | **PASS** | The Gaussian conditioning, exact score increments, uniform ridge bounds, start-mode argument, conditional path comparison, and probability assembly are valid. CC controls exactly the parents and deletion bases needed for every null-out swap. Truth-removing moves have a separate uniform order-n loss. No Tier 1 step uses an unchecked KL assertion. The minor empirical explanation below does not enter the theorem or change the frontier. |
| G2 — hypotheses used = hypotheses stated | **PASS** | Exact Gram, fixed positive correlation parameters, bounded group size, fixed support size/coefficient vector, growth restrictions, and FS-BCS are used in their stated places. C1 allows p up to n/2; the multiplier/path argument uses p=o(n), with the declared exponent below 1/2. FS-BCS is needed for the start, not for C2-R from the specified S*. The report now preserves the s0=4 and exact-noise-argmin restrictions of the research modules. |
| G3 — no hidden assumptions | **PASS** | Finite incidence patterns provide the uniform nonzero partial-signal minimum despite moving support locations. The bounded Gaussian family is indexed by coordinate and retained group-mate set, not by an adaptively chosen global model. No adaptive independence, sign symmetry, vanishing end-phase field, or data-measurability of CC is assumed. The enlarged-space union bound is legitimate. |
| G4 — cited lemmas have adequate status, without upgrading | **PASS** | T38-(0), T03-sharp, [OP], CAP, corrected F/F-GROW, and A4 retain their recorded qualifications. In particular [OP] remains author-proved/unchecked inside GEN; the delivery extension inherits the exact-arithmetic, machine, and code-reading premises. The d315c1e council check is distinguished from A4's later preflight addition. FAC-B supplies rechecked algebra/assembly, not an automatic BCS approval. KL files remain explicitly unchecked research. |
| G5 — constants and rates tracked | **PASS** | The repaired leakage has the necessary sqrt(k)/n^(3/2) term; the other ridge terms are O(k(1+|tau|+max|g|)/n^2). The determinant remainder is O(p/n), the multiplier error is polynomially small, and the log correction is O((log n)^2/n). They leave the fixed delta/8 log(n) margins. The truth-loss constant is positive and uniform. Bounded p and the failure of the multiplier limit at linear p are handled separately. |
| G6 — fidelity to v3.1 / main 4676af6 / MR1 | **PASS** | Pi uses the actual normalised-response ridge score and production lexicographic neighbour tie rule. Complete flip/swap scans, strict improvement, and the final scan match the inspected loop. MR1 gives a_n=ell_n+|S*| >= m0. Delivery imports the full amended fallback/allocation/preflight premises. Candidate-restricted runs and Python start-mode replicas are labelled; exact-noise-argmin research is not transferred to Pi. |

## Independent mathematical assessment

**L1.** Sherman–Morrison applied after the block inverses gives the stated negative precision off-diagonals. Inverting the relevant two-coordinate precision block gives positive conditional covariances. The group-mean posterior calculation yields

    e_R = [h/rho_b - sum_g omega_g ybar_g] / [1/rho_b + sum_g omega_g].

The within-group residual is independent of `(h,g_R)`, so its variance adds to `c_u^2 V_R`. The coefficient `c_u/s_u` decreases from `(1-rho_b)^(-1/2)`, proving the uniform tau bound. These identities apply to deterministic conditioning sets; using them pointwise for every set avoids any selection-law assumption.

The Schur-complement score identities agree with SoP `04_theory.tex:70–74`, including the BB prior ratios. For a null with all truths in the conditioning set, the ridge signal residual is exactly `a^(-1) beta_tilde' theta^R`. This gives the repaired leakage rate. FAC-B L1.5(b)'s Q-versus-RSS proof uses only the eigenvalue floor and signal containment and therefore transfers to BCS. E2 then gives the displayed uniform multiplier estimate for p=o(n). Summing the one-sided eigenvalue remainders gives the asserted determinant-increment bound.

**L2–L3.** FS-BCS excludes finitely many proper hyperplanes because the coefficients depend only on finitely many bounded incidence patterns. Thus positive block-table increments have a uniform order-n signal advantage. Zero pairs occur only in the method block containing all truths, and E_S is correctly restricted to its bounded family. Its Gaussian variance bound is valid for the ridge predictor. The flip-improvement dichotomy proves the unique maximiser `S*=[p] minus N0`, including nonempty N0. This argument does not use M_T tending to 1/2 at p/n near 1/2.

The Gaussian-family counts and chi-square bounds suffice for P(E_n) tending to one. E3 has bounded cardinality, E_A has at most `p*2^(qbar-1)` members, and E_S has a fixed bound independent of p. The crude all-set field bound follows from the convex-combination normal equation.

**L4.** CC covers e_T for additions and every e_(T-j) needed for retained-null deletions and additions after a null deletion, including initially excluded N0 nulls. The size thresholds are bounded below by Lambda_k up to the tracked determinant error and bounded `2/p` term. Consequently every null deletion has positive logarithmic gain, and adding any outside null after such a deletion has negative logarithmic gain. The exact deletion-plus-addition identity then puts every null-out swap below the best deletion.

For truth removal, the conditional Gram floor supplies squared bias at least `(n-1)d*theta_j^2`. E3 and the all-set field envelope bound the cross term by O(sqrt(n log n)); the total noise-projection allowance is o(n). Thus the residual and score losses are uniformly order n even for truth-out swaps. At S0 the terminal CC requirement handles additions and the signal argument handles every remaining neighbour. The cap and scored-set conclusions follow from the actual loop, including m0=0.

**L5.** The global eigenvalue floor verifies both anchored eigenvalue premises of FINAL's T03-sharp, and the fixed nonzero coefficients verify beta-min. Bounded posterior error therefore has expectation tending to zero. The discovery event K_n is data-measurable while E_n and CC may depend on the latent enlargement. The inclusion `E_n intersect CC subset K_n` gives the needed original-law failure bound without conditioning on CC. [OP] and T38-(0) yield C3-R. For C4-R, the input/scorer check and F's amended allocation give almost-sure delivery; D-prime's pathwise scored-set inclusion gives the error bound without CAL. Discovery is not inferred by reversing the operational-closure inequality.

## Frontier and round-1 disposition

The report now fixes the substantive round-1 scope problems: the start is S* rather than invariably the whole model; the essential-cap description is restricted to the growing-start regime; the 250-null/conditional-terminal specialisations retain s0=4; and exact-noise-argmin modules are separated from the exact-score Pi. The remaining special-case band is correctly stated using retained-null count versus total parent size.

The lattice obstruction has the stated interpretation. Choosing one designated coordinate from each of many truth-free groups supplies independent Gaussian observations. Retaining large same-sign observations gives normalised maximal field tending to `sqrt(1-theta)` at retained count approximately p^theta. Substitution into CC yields the cutoff `1/(2+4 sqrt(1-theta))`; a growing subpolynomial count gives the 1/6 limit. This obstructs the sufficient all-set CC route, not the actual greedy path or consistency. The report labels this research unchecked and does not use it to prove Tier 1. The middle-band field control and transfer from exact argmin to Pi remain open. RESULT = PARTIAL is accurate.

## Verification performed

With Python 3.13 and bytecode writes disabled, I reran `bcs_selftest.py`, `l1_identities.py`, and `l1_leak.py`. The five score comparisons reproduced a maximum flip-gain discrepancy about 5.22e-7 and best-swap discrepancy about 2.68e-8 at n=10^8. The identity check retained 361 of 400 generated instances, with maximum normal-equation error 1.42e-14 and no tau-bound violations. Leakage reconstruction and the two-term rate check reproduced the recorded results. These are floating-point falsification checks, not proofs.

I additionally ran four in-memory complete-neighbour paths at p=20, n=10^14, seeds 900, 901, 903, 904, with S5 correlations and two truth layouts. Two starts had N0 empty and two had three excluded nulls (admissible deterministic block layouts). All satisfied the tested CC(.05), followed best-null deletion, and ended at a strict S0 endpoint. Across these four paths the minimum deletion gain was 0.475 log(n), the minimum gap to additions/null-out swaps was 0.471 log(n), and every truth-removing gain was at most -0.155 n. Two separate p=10 endpoint checks cover m0=0 with an admissible single method block. No scratch file was created.

The saved complete-scan summaries report 15/15 successes each, with zero exact ties in the tie-rule rerun. I inspected the production neighbour scan, tie comparison, MR1 cap and relevant preflight code; this is not a new comprehensive implementation audit.

## Required fixes

None for acceptance of the claimed Tier 1 reduction and PARTIAL ticket result.

## Optional suggestions / nonblocking erratum

1. Correct `REPORT.md:108–110`'s explanation of negative CC margins. It is too strong to attribute all 16 negative rows to H_q^2 exceeding Lambda_k, or to say the diagnostics do not test CC itself. For p=500, n=10^12, seed 3, `s3_cc.py` reproduces the minimum margin -0.0372215 log(n) at two retained nulls (parent size k=6). There H_q^2=25.9985662 and Lambda_6=37.5426752: the zero-field margin is positive, about 0.417795 log(n), and the centre error causes the negative full margin. The script explicitly computes the formal CC(0) margin along its deletion path. Suggested wording: “The diagnostic CC(0) margin is negative in 16/18 rows. In many bulk cases H_q alone exceeds the threshold; some late-path failures also involve e_T. These finite-n checks do not establish the asymptotic high-probability CC assertion.” This changes no proof, numerical success count, or claimed frontier.
2. Keep a compact frontier table with each module's support restriction, path rule, field premise and unchecked status when preparing the HQ/paper version.

**Seat decision: ACCEPT, 8.8/10, G1–G6 PASS. Tier 2 remains unproved.**
