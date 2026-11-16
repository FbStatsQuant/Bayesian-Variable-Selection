# WP2: production start law pi_0 at p = 10^6 (MEASURED)

Source: `tools/bench_setup.cpp startlaw <design> 1000000 <n> 3 1 2000` (WP2 branch exp/P1M-wp2-setup, PR #13), Owls
(Xeon Gold 6148, shared, nice 19), 3 threads. Data: WP1 `gen` (seed 1), standardised by WP1 `prep::standardise`. Production
partition: truncated linkage (D-4/D-4a), B_V = 14 (D-19), packing by minimum index. Tables, start law and size law
are bit-equal to core/ (golden tests in PR #13).

- E|S|, q50/q90/q99: from size_logmass = log pi_0(|S| = k). The quantiles are the smallest k with cumulative mass >= q.
- E #blocks touched (exact) = sum_b (1 - P(k_b = 0)), from prefix and suffix size convolutions.
- MC: 2,000 pi_0 draws (Philox addresses, seed 9) as a cross-check, mean |S| / mean blocks touched (Monte Carlo SE about 0.03).
- ADJ-OPP has the same X as AR (same seed) but a different y, so its tables and pi_0 differ.

| design | n | K | J | E\|S\| | q50 / q90 / q99 | P(\|S\| = 0) | E #blocks touched (exact) | MC: mean \|S\| / mean blocks | wall, peak RSS |
|---|---|---|---|---|---|---|---|---|---|
| AR | 200 | 100 | 74,726 | 3.615 | 3 / 5 / 7 | 2e-08 | 3.615 | 3.580 / 3.580 | 26 min, 9.6 GB |
| IND | 200 | 100 | 71,574 | 3.862 | 4 / 5 / 7 | 0.0012 | 3.862 | 3.830 / 3.830 | 28 min, 11.7 GB |
| BLK | 200 | 100 | 96,183 | 3.352 | 3 / 5 / 6 | 0.00036 | 3.352 | 3.330 / 3.330 | 22 min, 7.0 GB |
| ADJ-OPP | 200 | 100 | 74,726 | 2.835 | 3 / 4 / 6 | 3.4e-13 | 2.835 | 2.800 / 2.800 | 26 min, 9.6 GB |

Updated 2026-11-16T07:45 (rows are added as runs finish; pending: see the WP2 report).
