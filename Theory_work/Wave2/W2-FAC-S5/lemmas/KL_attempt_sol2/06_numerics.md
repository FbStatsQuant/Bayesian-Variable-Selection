# Local falsification and verification notes

Run from the repository root:

    py -3.13 Theory_work/Wave2/W2-FAC-S5/lemmas/KL_attempt_sol2/numerics.py

Python version: 3.13.17. RNG seed: 2026110902. The standalone script
writes only the two JSON files beside itself. It does not import or run
repository production code. Every probability claim in the proof files
has an analytical finite union bound or deterministic argument; these
checks are for falsification and algebra only.

## Checks performed before writing the corresponding proofs

* All 32767 nonempty subsets at p=15, three groups of five, were
  enumerated. The variance bound `V_T*(ell/a+1/rho_b)<=1` held, attaining
  one. There were no violations of the explicit lattice event bound
  on that one draw. This does not estimate its asymptotic probability.

* Twelve exact full-S5 null-deletion paths at p=2000 were generated
  directly from the precision formula. The parent-field identity at
  pair-to-singleton births agreed with the deletion statistic to
  `1.34e-15` in maximum absolute error.

* There were zero crossings of surviving **null singletons**, and zero
  violations of the fixed-cohort interval property. The largest observed
  ratio of singleton centre drift to its preceding distance was
  `.132237066814...`; the deterministic proof bounds it by .75.
  An initial check without excluding protected truth singletons did
  have crossings. The proof correctly requires that the compared
  singleton be a null eligible for the argmin.

* A literal core defined only by
  `|X_j| > running_max |tau_deleted| + running_max |e|/sqrt(a)`
  failed in every path: a member can be deleted while a group-mate
  remains. In the first saved example the very first deletion has
  `X_j=.460442159890...`, level `.0001985608046`, and field maximum
  `.0027886713156`. Its original group coordinates in y-units are

      (.0323301614045, .3852335497111, 1.5510567456439,
       -.3339617110677, .5816156899766).

  This only falsifies a core using the singleton coordinate alone.
  It does not falsify a core defined by immunity under every relevant
  within-group statistic, or the protected-champion construction.

* The maximum observed deficit of the current deletion level below its
  running maximum was `.352641528582... H`. Hence a running maximum
  cannot simply replace the current level in the orthogonality count.
  No universal vanishing-deficit assertion is inferred from these
  finite paths.

* For every truth-free multimember deletion with `|X_j|` greater than
  the running field maximum E, the script checked the necessary original
  pair condition used in (04.R3): a same-sign group-mate at least as
  large, or a signed group-mate at most `2E-|X_j|`. There were zero
  violations. The Gaussian pair count in `04` then turns this deterministic
  condition into the all-history raw-exception probability bound.

* Two hundred additional scalar paths with magnitudes in `[.8995,1]`,
  balanced initial signs, anchors of small absolute size, and lambda
  in `{217/57,19/3}`, tested the deterministic band bounds in `05`.
  There were no visited-state or arbitrary-neighbour bound violations.

## Additional independent dense-matrix check

The final run also checks the parent-field formula and drift update
at every coordinate of 1200 random retained states at p=15, against
an independently inverted dense covariance matrix. See
`dense_matrix_checks` in the JSON: the maximum statistic error is
`2.00e-15` and the maximum field-update error is `5.28e-16`. This covers
all retained group sizes, not only pair-to-singleton transitions.

## All-set obstruction and finite-size caveat

The script also selects top designated observations at p up to 10^6.
With theta=.01 or .06, `ceil(p^theta)` is only two or three there;
the finite anchor dominates. Those simulations are not close to the
asymptotic all-set obstruction and are not claimed to be so.

The separate analytic tail-count benchmark instead takes `log p=10000`,
theta=.01, alpha=.17, and threshold `.99H`. Its log expected qualifying
count is `191.5298791...`, versus log selected count 100. The anchor
failure bound at `|B0|>50` is less than `3.85e-86`, and the CC ratio
lower benchmark is `1.008070942...`. A Chernoff bound certifies an
overwhelming excess of qualifying coordinates. This checks the strict
constants in the analytical all-set obstruction. It is neither a
realized sample at that enormous size nor a greedy-path counterexample.

## What the numerics do not establish

They do not establish the `.05H` field history needed for the gate, a
small cumulative noncohort drift, any whole-path exponent above 1/6,
or robustness of the exact-path modules under near-argmin perturbations.
