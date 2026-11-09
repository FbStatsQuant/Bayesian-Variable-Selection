# KL/CC research result: PARTIAL

The section 6 update to the brief was incorporated. The original
`kappa_0 |e|=o(H)` claim is not asserted, including in the scalar case.
All assertions here concern the corrected size-dependent CC target.

## What is proved

1. **Full S5 partition, final two-null region.** With s0=4 and any truth
   layout, for any fixed `0<alpha_lo<=log p/log n<=alpha_hi<1/2`,
   `CC_n(.04)` holds with probability 1-o(1), simultaneously for every
   parent set with at most two nulls and all its one-null-deletion
   neighbours. There is no path or exact-argmin requirement for this
   endpoint result. If the four truths are in distinct groups, the same
   statement holds for the final four-null region with `CC_n(.01)`.

2. **Whole path, restricted partition.** If every null-containing group is
   a singleton (truth-only groups may be grouped), exact-argmin paths
   satisfy the full corrected CC target. Write

       lambda=(1-rho_b)[1/rho_b+sum_truth_groups t/(tb+d)],
       c=2/(lambda+2),
       R=max{2 alpha_hi, [2 alpha_hi/(1+2 alpha_hi)](1+c)^2}.

   If `R<1`, the proved constant is `delta=(1-R)/2`. For S5 parameters
   and s0=4, every `alpha_hi<1/2` is permitted, since
   `lambda>=217/57` and `c<=114/331`.

3. **Full partition, structural protection.** In a truth-free retained
   group with at least two members, its unique maximum of
   `|y_j+e_T|` is never the exact greedy deletion. With S5 parameters,
   w.h.p. at least `floor(p^.000499875)` extreme groups of each sign have
   champions that cannot be deleted before their group is a singleton,
   throughout any history with `kappa_0 |e_T|<=.75 H`.

4. **Full partition, dense sizes.** A completely explicit lattice bound
   proves CC on `k>=ceil(p^(1-beta))+1` when
   `beta<(7/23)[1/sqrt(2 alpha_hi)-1]^2` in S5. This is a baseline, not a
   claimed improvement over the known lattice method.

## What is not proved

There is no full CC theorem here for the genuine q=5-null-group S5 model.
The unresolved range lies between the dense-size bound and the constant
endpoint region. In particular, the .75 H field bound in the champion
lemma is a stopping condition, not an established bound along the path.

The weakest/missing step is converting protected champions into uniform
control of the singleton-deletion order and its level deficit while
multimember groups are still evolving. No assertion of conditional
Rademacher symmetry for path-dependent group states is made.

## Files

* `01_restricted_CC_theorem.md`: exact restricted theorem and conversion to CC.
* `02_CS_event_and_path.md`: explicit high-probability event and full path proof.
* `03_protected_champions.md`: deterministic group lemma and uniform extreme shell.
* `04_full_model_endpoints.md`: full-S5 endpoint theorem and dense baseline.
* `05_numerical_checks.md`: numerical interpretation and falsified candidates.
* `numerics.py`: reproducible local falsification script, Python 3.13.
* `numerics_summary.json`, `numerics_raw.json`: outputs of that script.

The strongest proved statements for the originally requested full S5
partition are items 1 and 3 above. The whole-path theorem in item 2 has
an explicit additional assumption and should not be cited as full S5.
