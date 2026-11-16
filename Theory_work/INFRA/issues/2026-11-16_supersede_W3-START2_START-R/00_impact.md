# supersede W3-START2:START-R (by W3-START2-R:START-R)

- reason: HQ GO real run (task U, H5 card 14 (A), 2026-11-16): free supersession (card 14 (A), STRONGER; W3-START2-R:START-R implies W3-START2:START-R, STATEMENT.md supersession table)
- Theorem START-R(b) (Gaussian rows; leakage set of any size at most K) [W3-START2] v1.0.0 state ACTIVE; status `PROVED-CHECKED`
- replacement W3-START2-R:START-R: Theorem START-R (b), Gaussian rows: o0 = O_P(sqrt(log n / n)) with uncorrelated nulls state ACTIVE; status `PROVED-CHECKED; council R2, MANIFEST 12bb52cd32c6870e14de43b0918827bc0ca9364d1ff04d6f16122b8a2a951ff5 (= R2 90886d06 re-`
- axes (Y vs X): {'assumptions': 'incomparable', 'conclusion': 'equal', 'rate': 'unknown', 'scope': 'unknown'} -> **undetermined**
- decision-rule class: **free**

## Statement diff

- hypotheses ADDED (each dependent must now verify them or the property it consumes): A:START2R-R-L (localised leakage with reference sets of size exp(kappa_H sqrt log n)), A:START2R-R-L0 (null columns uncorrelated with true columns given proper subsets of S0, up to C0 (n log n)^(-1/2))
- hypotheses DROPPED: A:BLOCK-LE-16 (Blocks of size <=16), A:EX-A (EX-A), A:START2-R-L (Localised bounded leakage with a leakage set of any size at most K)
- conclusion: `target: 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) with probability tending to 1; with Q = S0, pi0(S0) is at least 1 - n^{-c} for every c below 1/2; with size of Q at most n^{1/2 - eps_Q}, pi0(L(Q)) is at least 1 - n^{-c} for every c below eps_Q; with zero population leakage the rate is O_P((size of Q + 1) n^{-1/2} (log n)^{15 kappa_Q + 1/2})` -> `target: STATEMENT.md:228-235`
- rate: `(size of Q + 1) n^{-1/2} exp(C_R sqrt(log n))` -> `sqrt(log n / n) under (D5) at Q = S0 (STATEMENT.md:234-235)`
- scope: `Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed, s0 fixed; the display is trivial where its right side is at least 1` -> `Gaussian rows; p <= n^A (p >> n allowed)`
- statements: Theory_work/Wave3/W3-START2/STATEMENT.md:134-145 -> Theory_work/Wave3/W3-START2-R/STATEMENT.md:226-240

## Rebuild cost

- free: 1 re-point(s) PROPOSED (one cheap check each), no rebase, no re-review

| dependent | uses | action |
|---|---|---|
| W3-START2:IF-START | proof | propose re-point |
