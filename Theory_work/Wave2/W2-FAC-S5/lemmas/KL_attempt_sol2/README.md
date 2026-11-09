# RESULT: PARTIAL — sharper full-S5 range, exact singleton dynamics, conditional terminal theorem

The full corrected CC theorem is **not proved** above exponent 1/6.
There is also no counterexample to the actual greedy-path CC target here.
All writes are confined to this directory; no git operations were run.

## Exact unconditional progress

For full S5 (`rho_b=.3,rho_w=.7,qbar=5`), p tending to infinity and
eventually `log p/log n<=.17`, with s0=4 in any fixed truth layout,
with probability tending to one:

> **CC_n(1/10000) holds for every parent T containing S0 with either
> k=|T|>=ceil(p^.06), or at most 250 retained nulls, and for all its
> one-null-deletion neighbours.**

No path assumption, exact-argmin assumption, or positive lower bound
on `log p/log n` is needed for this assertion. In particular it applies
to the requested `1/6<limsup log p/log n<.17` regime on these sizes.
The uncovered sizes have at least 251 retained nulls and k<p^.06.

More generally, the polynomial-size range is

    k>=ceil(p^theta),
    alpha_hi<alpha_crit(theta)=1/[2+4 sqrt(1-theta)],
    R=2 alpha_hi(1+sqrt(1-theta))^2/[1+2 alpha_hi(1-theta)],
    delta=(1-R)/2.

At alpha_hi=.17 every theta>.0579584775086508 is permitted. The gain
comes from counting active groups: uniformly over every nonempty set,

    kappa_0 |e_T|
      <= sqrt(2 log(C_q p/|T|)+2 log log p+4 log 2),
    C_q=e q(2^q-1).

The leading constant one is optimal on the lattice; the first-round
bound had leading constant sqrt(23/7). This is the main unconditional
new result, not a claim to have filled the entire sparse middle range.
The brief already identified the optimal-order lattice route and its
1/6 barrier. This makes that route explicit and improves the displayed
first-round constant; it does not move the whole-lattice frontier.

## Exact path and orthogonality modules

1. A retained **null singleton never crosses the global centre** under
   exact greedy deletion, even when a different group changes size.
   For any fixed cohort of existing singletons, its deleted points form
   an interval. The CS asymmetry recurrence has an explicit additive
   forcing equal to twice the cumulative centre drift from noncohort
   deletions. No symmetry of a selected cohort is assumed.

2. The independent Gaussian pair `(X_l,A_j(U))`, for l in U, yields a
   uniform O(p)-family exception count. Under field bound EH and current
   deletion level at least tH, the exponent for leaving a group-mate
   with magnitude xH is

       J=x^2+(t-sqrt(3/11) E-nu)^2,

   for any fixed positive margin nu. If J>1, none of these transitions
   occur with high probability. This counts transitions at the specified
   high level; it does not count arbitrary early multimember deletions.

3. For retained truth-free multimember groups at minimum level tH,
   the corresponding uniform count exponent is

       J2=(14/11)(t-sqrt(3/11) E-nu)^2.

   With E=.05, t=.9495, nu=.001, J2=1.082836708774...>1:
   there are no such retained groups.

4. **All-history raw exceptions:** if `0<x<1` and the field history is
   bounded by EH with `E<=x/2`, the fraction of original xH-extremes
   deleted while a group-mate remains is at most

       exp[-(3/44)(xH)^2],

   with probability tending to one, simultaneously for every exact
   path. This includes early deletions and follows from the maximum
   principle plus an O(p) original-pair Gaussian count. More generally
   `04` gives the rate for every `E<(11/14)x`. It proves the suggested
   exponentially rare raw-exception mechanism under its explicit
   bounded-field premise. Relating a moving hole to a fixed raw threshold
   is still a separate step.

## Conditional terminal result and its exponent

Use the first-round protected champions with magnitude at least
`(1999/2000)H` in at least `floor(p^.000499875)` groups of each sign.
If the history satisfies `kappa_0|e_T|<=.05H` through the first
champion deletion, then on a single event of probability tending to one:

* At that parent, all null-containing groups are singleton.
* From that parent onward, every state and deletion neighbour satisfies
  CC for every fixed alpha_hi<`.412606129553...`, with explicit delta
  in `05`. At alpha_hi=.4, delta=.005 is valid.
* No `.05H` field condition is imposed after that parent.

This implication is path-uniform on the probability event; it is not
a probabilistic assertion conditioned on a selected history. It requires
exact argmin. Its exponent is **conditional**, not an unconditional
whole-path exponent.

## Checked obstruction and remaining gap

For k=s0+ceil(p^theta), the lattice maximum obeys

    max_T kappa_0|e_T|/H -> sqrt(1-theta).

Consequently any all-set CC theorem at that size fails if
`alpha>1/[2+4 sqrt(1-theta)]`. With a growing subpolynomial retained
count, the all-set cutoff is exactly 1/6. This proves that further
improvement has to use the path. It is not a reachable-path obstruction.

**Weakest/missing step:** no bound keeps the actual field below `.05H`
until the champion gate, and no sufficient bound is proved for the
noncohort forcing in the interval recurrence. Early multimember
deletions cannot be charged to the high-level orthogonality count;
the all-history raw-exception bound instead requires control of the
field relative to the raw threshold.
The interval result alone does not give Rademacher symmetry of a
data-dependent cohort. These are explicit gaps, not premises silently
used in any unconditional theorem here.

## Files

* `01_group_lattice.md`: uniform lattice inequality, CC conversion,
  explicit .17/.06/250-null partial theorem.
* `02_lattice_obstruction.md`: matching lower bound and sharp obstruction
  to all-set extensions; no greedy-path counterexample.
* `03_singleton_cohorts.md`: exact drift, null-singleton no-crossing,
  cohort interval theorem and asymmetry forcing.
* `04_orthogonal_transitions.md`: all-history raw-exception rate,
  independent-pair and retained-group counts, and champion scalarization.
* `05_conditional_terminal.md`: deterministic band trapping after the
  gate, including arbitrary deletion neighbours, and conditional exponent.
* `06_numerics.md`: scope and results of the local falsification checks.
* `numerics.py`, `numerics_raw.json`, `numerics_summary.json`: reproducible
  Python 3.13 checks and outputs.
