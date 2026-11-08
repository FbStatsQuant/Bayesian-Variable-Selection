# W1-N3 numerics

All runs are local and small. Full enumeration of Ω_K (every S with |S| ≤ K) is used in `run_checks.py`,
`lemma_probes.py`, `eng10_n2.py`, `fp_example.py` and for the m ≤ 4 members (p ≤ 12) of `cex_family.py`. The larger
deviation instances (`cex_family.py` m = 5..12, i.e. p = 14..28; `cex_default_cap.py`, p = 44) are checked against the
closed form of L6 and against TDP (`tdp.py`), not by enumeration. Declared seeds: `run_checks.py` 20261108 and 7;
`lemma_probes.py` 11; `eng10_n2.py` 2. p ≤ 12 for enumeration follows the ticket's explicit request ("p <= 12").

Oracles. Input representability and sum exactness are separate requirements. The encoder rejects integers not
representable as doubles; and in every integer-table script every table/prior value has magnitude ≤ 10⁹ (run_checks:
≤ 1,000; lemma_probes: BIG = 10⁹ plus values ≤ 2; cex scripts: ≤ 10) with at most 23 terms per sum (≤ 22 blocks plus
the prior), so every partial sum the code forms is an integer of magnitude ≤ 2.3·10¹⁰ < 2⁵³ and is exact in binary64.
A native run on these families is therefore an exact-arithmetic run: they validate (a)–(d) and (f).
DATA-mode tables are the coded scorer's doubles: there the frozen code's (res.S, ties, truncated) are compared with the
prediction from the exact-table f (`Fraction` of each double) — an informational comparison with an exact-table
oracle, not an execution under (H2) — and clause (e) is checked natively against the Python replica ĝ of `log_gamma0`.
Doubles cross the harness boundary losslessly (`%a` / `float.hex`).

## Files and results

| file | what | result |
|---|---|---|
| `sm_harness.cpp`, `build.sh` | drives the FROZEN `start_mode` (`#include "v3_start.h"` from the v2.2.1 tree, read-only), SSE2 doubles, no FMA contraction; TABLE mode and DATA mode (full coded pipeline: `data_init`, `make_blocks`, `Scorer`, `build_tables`, `build_start`) | MinGW g++ 16.2 (`-std=gnu++17 -D_USE_MATH_DEFINES` for `M_PI`/`M_LN2`) |
| `n3lib.py` | definitions transcribed from STATEMENT §1: exact f, prescribed S*, ≺_DFS key, predicted output (a)–(d); ĝ replica for (e); harness driver | — |
| `tdp.py` | reference tie-aware DP (clause (f), L7), exact arithmetic | — |
| `run_checks.py` | see per-family table below | `out_run_checks_seed20261108.txt`, `out_run_checks_seed7.txt`: 0 failures |
| `lemma_probes.py` | L2 (single-block μ and argmax count), L3 (M[b][k] for every prefix b and feasible prefix size k via λ isolating k), L5 (prefix output/count/flag checks for cap = 1..min(N,60); internal visiting order not observed) | seed 11: 1,500 + 2,521 + 1,551 probes, 0 failures (`out_lemma_probes_seed11.txt`) |
| `check_union_order.py` | L1(iii), exhaustive p ≤ 8 | 17,066 pairs, 0 violations (`out_check_union_order.txt`) |
| `cex_default_cap.py` | p = 44 instance (D_20), default cap 10⁶, through the frozen code; closed form + TDP | code returns {0,2,…,38,41,42} (ties = 10⁶, truncated = 1) ≠ S* = {0,2,…,38,40,43}; f = 25 for both (`out_cex_default_cap.txt`) |
| `cex_family.py` | D_m, m = 0..12 (p = 4..28), caps {1, 2^m, 2^m+1, 2^{m+1}}; closed form + TDP for all, full enumeration for m ≤ 4 | 50/50 as predicted (`out_cex_family.txt`) |
| `fp_example.py` | clause (e): two binary64 examples (prefix-addition and prior-addition rounding) | code output ≠ ĝ size-then-lex choice, while ĝ(code S) = lg0 = max ĝ (`out_fp_example.txt`) |
| `eng10_n2.py` | n = 2 boundary: full coded pipeline (routine only), p = 1..12 × 3 | 36/36 agree; S* = {0} at p = 1, ∅ for p ≥ 2 (log r = 0.33389 < log(2p−1)); singleton log r not always bitwise equal (2 distinct last-bit values in 10 of 36 runs) (`out_eng10_n2.txt`) |
| `eng10_preprocess_n2.R` | the frozen public preprocessing rejects n = 2 | `invalid_input` / "n < 3" (`out_eng10_preprocess_n2.txt`) |

## `run_checks.py` coverage per family (instances per seed: 20261108 / 7)

| family | instances | clauses checked |
|---|---|---|
| exhaustive p ≤ 3 (all ordered partitions, all K, all {0,1} tables and priors, caps 1/2/10⁶) | 19,950 / 19,950 | (a)–(d), (f) |
| constructed (all-zero tables, code≠lex within block, allocation ties, cross-size ties, K binding inside a block; some with cap 1–7) | 548 / 548 | (a)–(d), (f) |
| random integer tables: heavy ties 4,000; {0,1} 3,000; small caps 3,000; small K 2,000; wide range 1,000 | 13,000 / 13,000 | (a)–(d), (f) |
| cap edge (cap ∈ {N−1, N, N+1}, incl. K = 0 with cap = 1) | 2,053 / 2,087 | (a)–(d), (f) |
| **integer-table total** | **35,551 / 35,585** | (a)–(d), (f) |
| DATA (coded scorer, real prior; n ∈ {2,3,4,6,10,20}; duplicated columns; caps 1/2/10⁶) | 400 / 400 | res.S / ties / truncated vs exact-table prediction (informational); native (e) |
| fp_stress (magnitudes 1 to 2⁵², sub-ulp perturbations) | 3,000 / 3,000 | (e) only; 429 / 411 instances with more than one smallest-size ĝ-maximiser; float size-then-lex choice ≠ res.S in 26 / 32 (allowed by (e)) |

Truncated instances with res.S ≠ S* (all as predicted by (d)): exhaustive 529 / 529; constructed 125 / 124; small caps
219 / 219; small K 70 / 67; cap edge 16 / 24.
