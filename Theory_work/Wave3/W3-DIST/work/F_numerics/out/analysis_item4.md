## Item 4 — Lemma T: search for sup of E_x min{1,(a+u'x)²/c} − 2·(sample mean), p_raw = 50

`best` = largest value found over the restarts of a data set (a LOWER bound on the supremum, which is ≥ 0 trivially via u = 0, a = 0). η² = η²_n(d, 0.05) of STATEMENT §3. `max best` is the maximum over the data sets of that cell; `#sets best > η²` counts data sets in which the lemma (probability ≥ 0.95) would be violated.

| n | d | law | #sets | median best | max best | η²_n(d,0.05) | max best / η² | #sets best > η² | #sets best > 0.001 |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 1 | gauss | 10 | -0.0000 | -0.0000 | 1.269 | -0.000 | 0 | 0 |
| 100 | 1 | t2.1 | 10 | 0.0045 | 0.0200 | 1.269 | 0.016 | 0 | 9 |
| 100 | 1 | atom | 10 | 0.0086 | 0.0100 | 1.269 | 0.008 | 0 | 9 |
| 100 | 2 | gauss | 10 | -0.0000 | 0.0000 | 1.761 | 0.000 | 0 | 0 |
| 100 | 2 | t2.1 | 10 | 0.0155 | 0.0262 | 1.761 | 0.015 | 0 | 10 |
| 100 | 2 | atom | 10 | 0.0100 | 0.0100 | 1.761 | 0.006 | 0 | 10 |
| 100 | 3 | gauss | 10 | -0.0000 | 0.0023 | 2.205 | 0.001 | 0 | 1 |
| 100 | 3 | t2.1 | 10 | 0.0196 | 0.0344 | 2.205 | 0.016 | 0 | 10 |
| 100 | 3 | atom | 10 | 0.0100 | 0.0100 | 2.205 | 0.005 | 0 | 10 |
| 1000 | 1 | gauss | 10 | -0.0000 | -0.0000 | 0.164 | -0.000 | 0 | 0 |
| 1000 | 1 | t2.1 | 10 | 0.0001 | 0.0002 | 0.164 | 0.001 | 0 | 0 |
| 1000 | 1 | atom | 10 | 0.0009 | 0.0010 | 0.164 | 0.006 | 0 | 0 |
| 1000 | 2 | gauss | 10 | -0.0000 | -0.0000 | 0.231 | -0.000 | 0 | 0 |
| 1000 | 2 | t2.1 | 10 | 0.0001 | 0.0003 | 0.231 | 0.001 | 0 | 0 |
| 1000 | 2 | atom | 10 | 0.0010 | 0.0010 | 0.231 | 0.004 | 0 | 0 |
| 1000 | 3 | gauss | 10 | -0.0000 | -0.0000 | 0.294 | -0.000 | 0 | 0 |
| 1000 | 3 | t2.1 | 10 | 0.0002 | 0.0003 | 0.294 | 0.001 | 0 | 0 |
| 1000 | 3 | atom | 10 | 0.0010 | 0.0010 | 0.294 | 0.003 | 0 | 0 |

Total data sets 180; violations of the lemma (best > η²): 0.  Largest ratio best/η² = 0.016 at (n, d, law) = (100, 1, 't2.1').

Reference scale: for n = 100, η²_n(d, 0.05) > 1 for every d ≥ 1 (the lemma is vacuous since the left side is ≤ 1); for n = 1000, η² = d=1: 0.164, d=2: 0.231, d=3: 0.294.