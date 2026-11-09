# N9 — L8 local falsification record

Command: `py -3.13 -B Theory_work/Wave2/W2-FAC-XA/numerics/N9_truth_start.py`.
Completed locally with NumPy 2.3.0, 8 distinct seeds (0 through 7), p=6.
Script: `N9_truth_start.py`; complete machine-readable output: `N9_results.json`.
The score is an independent real-arithmetic-formula implementation of production
D0 in floating point, not a test of the compiled production binary.

Every one of 64 models is scored per dataset; every truth deletion and
truth-out swap from every truth-containing model is tested. The composite
start is exhaustively maximized for singleton blocks, spread truths, and an
X-selected block containing both truths plus two nulls. The last layout checks
N0 nonempty; it selects nulls using sample correlations only.

There were 32 FS-satisfying datasets (two sample sizes, two correlations, eight
seeds), with 8 favorable truth moves and 32 start mismatches among 96 layout
checks. All favorable truth moves occurred at n=256, rho=.98. These results
falsify a claim of universal finite-sample negativity, which L8 does not make.
No asymptotic counterexample was established. They are retained as attempted
falsification, not discarded as inconvenient observations.

The strong-correlation regime is a GLOBAL-floor stress (population floor .02),
not a counterexample to a fixed positive floor. The n=256, p=6 cases lie outside
the illustrative p<=n^.24 envelope; the output explicitly flags this. The
n=4096 cases lie inside it. No extrapolation to an asymptotic theorem is made
from these checks.

Eight additional deliberately FS-violating datasets use rho=.5,
theta=(1,-2,0,0,0,0). Here c(empty,truth 0)=0 exactly. In all eight singleton
partitions, the start excludes that truth. This probes the omitted-visibility
claim, not the locked FS target; it agrees with the exact masked-population
identity in L8. General bounded positive factor loadings alone cannot supply V.

Independent subtraction/nonnegative forms of ridge Q agree to maximum absolute
error 1.9099388737231493e-11. All per-case ridge corrections, truth-move margins,
start scores, partition identities, projected-noise energies and Gram floors
are in the JSON. This is not cross-family review or a council pass.
