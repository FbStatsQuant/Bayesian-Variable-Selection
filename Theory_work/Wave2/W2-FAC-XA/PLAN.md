# Plan
1. Numerics first: reuse FAC-B scorers without modifying sources; compare exact-CS,
   iid-CS, unequal-loadings exact and iid paths. At most 20 seeds, local only.
   Record deletion margins, swaps/additions, truth loss, cap exhaustion, and score
   ordering instability. Validate small cases by direct score enumeration.
2. Obtain statement lock. No proof work before lock.
3. Attempt a perturbation-robust gap/balance invariant (not literal path coupling).
   Study relative/whitened Gram deviations separately from absolute operator norm;
   a pervasive spike may invalidate an unqualified sqrt(p/n) absolute norm claim.
   Every lemma has its own file, falsification test and cross-family review.
4. Write checkpoint at the key lemma; fresh independent midpoint reviewer sees
   statement/proofs only and must return CONTINUE/REDIRECT/STOP. Obey stop verdict.
5. If CONTINUE, assemble start, path, posterior and delivery clauses, then sweep,
   citation script and two-seat council (maximum three rounds). Report exact frontier.
Only write inside W2-FAC-XA. No git state changes. Do not read or coordinate W2-FAC-X.

R01 amendments, 2026-11-09: C1 perturbation lemmas must name their norm and prove
the centered/standardized bound; never assume absolute sqrt(p/n). Investigate
relative norm and factor-adapted representation with random loadings separately.
C2-E is secondary: work in idiosyncratically whitened coordinates with loading
lambda/sqrt(1-lambda^2), seeking a weighted-center invariant controlling the
history-dependent band. C2-R only after that deterministic case.
N1 completed grid: seeds 0–9, n=512,2048, p=16,32,64,128, rho=.5 or loadings
linspace(.4,.85,p), truths first two coefficients (1,1.3), sigma=1. Norm diagnostics
included. Next N2 planned: Bartlett Wishart sufficient statistics, n=10^6,10^8,
p=32,100,200, rho=.5 or same unequal loading array, same truth/noise, seeds 0–4.
Centering uses Wishart degrees n-1; rescale diagonal; sample response conditional
on Gram including residual chi-square norm. Validate smaller n against N1 law.
This reaches large n locally without large raw matrices. Use general direct scorer
and production tie rule. Record cap budget, non-deletion moves and ties.
Checkpoint due at key lemma or ~3 hours. Three reviewed failures => STUCK/report;
target counterexample => immediate report. Midpoint Claude must return CONTINUE
before assembly. Citation script before council, saved reviews/CITECHECK.txt.

Post-R05 route (early midpoint CONTINUE; not post-X2 gate):
L5 RN-log -> L1 same-state coordinate coupling; L6 production null-order transfer;
L7 shadow midpoint/occupancy/end entry under direct tolerance. Each awaits its
own cross-family check before use. L8 independent truth/start proof in progress.
Assembly must explicitly compare OLS vs ridge CS centers; quantify deterministic
envelopes conditional on X; handle X-dependent N0 without a noise-dependent union;
cover small/oscillating p; then prove X2 and obtain a fresh post-key midpoint.
Only then X3/X4 assembly, sweep, citecheck, council. Council skill read; protocol
overrides its defaults: Sol xhigh, Claude high, six gates and maximum three rounds.
