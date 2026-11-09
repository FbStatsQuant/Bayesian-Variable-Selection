# W2-FAC-XA statement v1 — LOCKED research target (not a theorem)

R01 verdict LOCK-WITH-CHANGES, R1–R12 applied below and in PLAN.md.

## Setting and target
This is an independent extension attempt, not an assertion of a proved theorem.
Use precisely D0, the centered and standardized score, prior, implementation premises,
start-mode routine, and LS0 cap ell_n + |start| in W2-FAC-B/STATEMENT.md sections 1 and 4.
No method change is proposed. Fixed s0 >= 1, fixed nonzero standardized coefficients,
fixed noise variance, independent Gaussian errors. Random-design response convention:
Y = X theta + C epsilon, with theta fixed on the standardized scale (as FAC-A).

Priority target C1: raw iid Gaussian rows with covariance (1-rho)I + rho 11', fixed
rho in (0,1), centered and standardized by the method; FAC-B (FS) for the fixed
coefficients. Initially seek every p <= n^a with fixed a < 1/4; the research target
is the largest possible exponent, ideally p=o(n) or p<=n/2. Changing the proposed
rate requires a logged statement revision and fresh lock; no rate is claimed yet.
Conclusions sought under the joint design/noise law: LS0 scores S0 with probability
tending to one; D_n -> 0; P(output and reported model != S0) -> 0. Under ALL
Proposition F premises and amended allocation inherited in FAC-B (C4), additionally
P(reported model = S0) -> 1. The delivery step must verify Lemma S inputs and use
the pathwise inclusion; it cannot infer discovery from D_n alone.

Priority target C2: exact standardized Gram diag(1-lambda_j^2)+lambda lambda',
lambda_j in a fixed compact subinterval of (0,1), then iid Gaussian rows with this
population covariance, with p<=n^a, a<1/4 initially. Impose a uniform positive lower
bound on absolute population partial covariances c(U,j), for |U|<=15 and j not in U,
whenever j is a truth or U does not contain S0. This explicit stronger visibility
assumption supplies a potential near-full start; no claim is made without it.

For any narrower conclusion, state precisely its hypotheses, proof obstruction and
whether it is a limitation of the technique or a counterexample to the method.
Exact ordering agreement is NOT a required conclusion: moves may reorder while
remaining safe deletions. No positive swap margin is assumed from FAC-B.

## Source status discipline
FAC-B REPORT: "PROVED-CHECKED". FAC-A REPORT: "PROVED-CHECKED (for the narrowed,
flagged target STATEMENT.md v1.2)". T03 sharp: "PROVED; SF VERIFIED (W2-VT03R);
XF VERIFIED (A-REV2)". FAC-B STATEMENT section 6 describes Proposition F as:
"Proposition F (A1 corrected statement, council round 3 passed; preflight
addition checked in A4 \"OK-WITH-FIXES\") and F-GROW (A2 \"PROVED (A2), checked by A3\")".
These are dependency statuses, never the status of XA. FAC-A covers iid CS with
limsup log p/log n < 1/6 under GC-CS, and singleton unequal loadings with exponent
alpha0(kappa)=1/[2 kappa(kappa+2)], kappa=max(lambda/sqrt(1-lambda^2))/min thereof.
Our visibility/full-start hypotheses differ from FAC-A's GC-CS/TV-pop hypotheses;
no blanket implication between the theorems is asserted. New ranges sought are
above these baselines. No result in XA is currently proved or checked.

## Precise scope supplement (controlling in case of ambiguity above)
C1: fixed rho, no sign flips. C2-E: deterministic centered standardized design with
exact Gram as above, necessarily p<=n-1. C2-R: iid Gaussian raw rows, subsequently
centered/standardized. C2-E is a secondary stretch; C2-R follows only after C2-E.
In both C2 cases loadings and truth positions may vary with n; all bounds are
uniform in n. Positive loadings only. The ordered vector of s0 true standardized
coefficients is fixed. For each fixed 0<a<1/4, every sequence p_n<=n^a eventually
is targeted, including bounded and oscillating sequences. Enumeration plus T03
sharp covers the small-p branch; remaining estimates must be uniform across the
other indices. Larger exponents remain research ambitions outside this lock.

Visibility V: on the population Sigma scale let mu=sum_{i in S0}theta_i x_i and
c(U,j)=Cov(x_j,mu | x_U). Require inf_n min |c(U,j)| >= c0>0, where the minimum
is over |U|<=15, j not in U, and either j in S0 or U does not contain S0.
This deliberately quantifies over all U, beyond the actual blocks. Conditional
variances lie between 1-lambda_hi^2 and 1; equivalence to normalized visibility
and the factor formula for c(U,j) are proof obligations, not assumed identities.

Let N0 be nulls in any block containing every truth, S*=[p] minus N0, m0=|S*|-s0.
Claims X1–X3 target every deterministic partition with block size <=16. For random
rows condition on X: the actual partition is X-measurable and error-independent.
X4 uses the actual partition and Proposition F invariants including B<=K. All
implementation premises apply to each design realization. Under continuous iid
rows nonconstant raw columns are retained almost surely, p=p_raw.

X1 (start): under C1+FS or C2-E/C2-R+V, fixed signal/noise and rate conditions,
S* is the unique start mode with probability tending to one.
X2 (key path): under the same statistical assumptions, every move from S* until
S0 is a safe move (deletion of a null from a set containing S0); truth deletions
and truth-out swaps are excluded. There are exactly m0 moves and S0 has no
improving neighbor. Thus the merged cap a_n=ell_n+|start| reaches S0 and certifies
the search endpoint. A weaker route allowing swaps/additions must explicitly
bound swaps+2*additions by ell_n+s0 (endpoint), or one greater (scoring only),
and revise this clause before use. Scoring requires total path length <=a_n+1.
X3 (reported model): X1/X2 statistical assumptions plus FAC-B section 1 premises
including CAL give D_n->0 and P(output and wrong report)->0.
X4 (delivery): same statistical assumptions plus ALL FAC-B C4 Proposition F
premises/allocation, including A4 preflight terms, CAL-free, give P(correct report)->1.
X5 (frontier): numerical evidence and exact technique obstructions, distinguished
from method inconsistency; no positive theorem is attached to this clause.

Random-design transfer obligation: construct design events A_n of probability
tending to one with common H0/envelope constants, then prove uniform conditional
convergence or the every-deterministic-sequence diagonal argument (FINAL s3 Random
designs, FAC-A L5). Conditional convergence alone is insufficient. Delivery must
check Lemma S and pathwise discovery as above.

Norm discipline: absolute ||Rhat-Sigma||=O_P(sqrt(p/n)) is forbidden as an input.
Every perturbation lemma must identify and prove its norm bound for the centered,
sample-sd-standardized Rhat. Candidate useful norm: relative/whitened deviation;
absolute norm can have p/sqrt(n) scale (R01 section A). A random CS component may
be absorbed into rho only if the residual is separately bounded. FAC-B REPORT's
frontier sqrt(p/n) remark is not used as an absolute norm fact.

## Review gates
Statement lock before proof; each lemma gets falsification numerics and a fresh
Claude Personal Opus 5.5 high review before downstream use; fresh independent
midpoint CONTINUE required; exhaustive Claude sweep; citation check; council with
Claude Opus 5.5 high and fresh Codex gpt-6.1-sol xhigh, both >=8 and all six gates.
REDIRECT/STOP at midpoint ends the run and triggers report to HQ.
Checkpoint at key lemma or about three hours, whichever first. Three failed reviewed
attempts on a lemma => STUCK/report. Target counterexample => stop/report immediately.
