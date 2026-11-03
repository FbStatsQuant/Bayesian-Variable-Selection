# Independent benchmark tie-out

Recovery: read the manifest dataset IDs, p and scenario; truth `active`; benchmark `rows` fields `rule_id`, `status`, and `support`; and SMC `pip_plain`. Compare supports as sets; failed or missing benchmark rows and missing SMC records count as unrecovered. SMC selects PIP strictly greater than 0.5.

ABESS: read X and the named Y scale, center Y, calculate no-intercept least-squares RSS for the selected support, and compare it with `leaps::regsubsets` exhaustive minimum RSS at the same size, using the specified tolerance. Empty supports use sum of squares directly. The manifest supplies 100 or 600 expected cases. Missing truth, malformed fields, or unavailable size comparisons produce UNVERIFIED.

## Mismatches
- Cell 6: claimed 94; recomputed 91.
- Cell 16: claimed 547; recomputed 550.
- Cell 19: claimed 81; recomputed 83.
- Cell 21: claimed 88; recomputed 91.

## Data observations
- Cell 24 above optimum: p0030_S4_r022_c100 k=6 RSS=183.38579443 best=183.312774513
- Cell 25 above optimum: p0020_S2_r096_c050 k=5 RSS=188.575392916 best=186.295835997 | p0020_S4_r049_c050 k=4 RSS=223.042277782 best=222.774112972 | p0020_S4_r053_c050 k=4 RSS=165.059754423 best=164.290278127 | p0020_S4_r067_c050 k=5 RSS=228.86263628 best=228.127668694 | p0020_S5_r051_c050 k=4 RSS=260.969133163 best=258.760723588

Verdict: 21 MATCH / 4 MISMATCH / 0 UNVERIFIED.
