# Numerical falsification notes

Run from the repository root:

    py -3.13 Theory_work/Wave2/W2-FAC-S5/lemmas/KL_attempt_sol/numerics.py

Python reported 3.13.17. The script writes only beside itself. It implements
the precision formulas directly, without invoking a production score path:
all block-path decisions are exact argmin of the noise deletion statistic.
The initial random seed is 20261109; the final raw and summary JSON files
were regenerated after adding the three-alpha scalar sweep.

## Candidates tested before writing the proofs

**Fixed-field group maximum principle.** 180,000 independent trials, group
sizes 2 through 10, positive b,d ranging over exp([-4,3]), and varying
coordinate scale: no unique maximum of absolute shifted coordinates was
the minimum-distance group deletion. The proof is `03`, section 1.

**Original group champion remains until singleton.** False. In the final
60 exact S5 paths at p=1000, all 60 had a counterexample in some truth-free
group. The first is stored in the summary and quoted in `03`. This rules
out replacing the field-dependent maximum by the original maximum without
a margin condition. An earlier sweep with the same 60-path design and a
different consumed RNG state had 57 counterexamples; the final JSON is
the authoritative reproducible run.

**Shifted group champion protection.** The same 60 paths had zero failures
of the fixed-field statement at their actual data-dependent e_T. This is
only a numerical falsification check; the path-uniform claim comes from
the deterministic proof, not these 60 samples.

**Monotone deletion level.** False, even for scalar CS. All 72 scalar paths
in the final sweep had at least one strictly decreasing deletion level.
Accordingly none of the proofs assumes deletion levels are nondecreasing.

## Scalar CC finite-size sweep

There are 72 paths: null counts 100, 1000, 5000; anchors 217/57 and 19/3;
alpha .2, .35, .49; four draws for each combination. The anchor numerator
B is N(0,1); the deterministic scalar proof applies to any fixed bounded
Gaussian variance, so these paths test the reduction independently of a
particular truth-data draw. Four truths are included in the parent-size
and CC-denominator bookkeeping.

* At alpha=.2, 17/24 paths had a CC ratio below one. The range was
  .7417728 to 1.1439995.
* At alpha=.35, 0/24 had a ratio below one; the range was 1.2484797 to
  1.8008568.
* At alpha=.49, 0/24 had a ratio below one; the range was 1.7083498 to
  2.4502622.

These are **finite-size failures of CC**, not empirical verification of
the asymptotic theorem. At these p, the additive terms
`2 qbar log 2+2 log log n` in H_q^2 are large. For example at alpha=.49
they already make the centre-free bulk requirement fail at the tested p.
The proof takes those terms as o(log p); its onset can be extremely large.
No finite-n success claim is made at alpha close to one half.

## Checked constants

The final summary verifies numerically:

    protected-shell Chernoff exponent = 1.0045512803030305,
    protected-shell field margin     = .004750000000000032,
    worst S5 truth-anchor lambda     = 3.807017543859649,
    one-deletion-neighbour coefficient = .34441087613293053,
    end CC ratio at alpha=1/2        = .9037203019322569,
    end-only exponent cutoff         = .6192405950443117.

The proofs use the corresponding exact rational constants, so floating
point signs near a boundary are not being substituted for rigorous bounds.

## Principal unresolved inference

Extreme shell champions can be protected up to a field stopping time, but
their singleton deletion times need not follow a fixed sign-symmetric
reference order while the other groups evolve. Neither the frozen-field
experiment nor the maximum principle supplies the missing bound on that
effect. No claim that the full q=5 CC target is proved is justified by
these computations.
