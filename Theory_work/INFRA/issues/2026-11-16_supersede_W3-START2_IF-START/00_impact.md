# supersede W3-START2:IF-START (by W3-START2-R:IF-START)

- reason: HQ GO real run (task U, H5 card 14 (A), 2026-11-16): free supersession (card 14 (A), STRONGER; W3-START2-R:IF-START implies W3-START2:IF-START, STATEMENT.md supersession table)
- Corollary IF-START (start interface with the sharp rate) [W3-START2] v1.0.0 state ACTIVE; status `PROVED-CHECKED`
- replacement W3-START2-R:IF-START: IF-START++ (start interface for the sampler theorems; Gaussian-row rate sqrt(log n / n)) state ACTIVE; status `PROVED-CHECKED; council R2, MANIFEST 12bb52cd32c6870e14de43b0918827bc0ca9364d1ff04d6f16122b8a2a951ff5 (= R2 90886d06 re-`
- axes (Y vs X): {'assumptions': 'better', 'conclusion': 'equal', 'rate': 'unknown', 'scope': 'unknown'} -> **undetermined**
- decision-rule class: **free**

## Statement diff

- hypotheses DROPPED: A:BLOCK-LE-16 (Blocks of size <=16), A:EX-A (EX-A), A:START-AL (Averaged leakage with a level vector), A:START-E (Energy bound and polynomial dimension), A:START-GF (Constant unnormalised Gram floor on sets of size at most 16), A:START-V (Visibility of the truths)
- conclusion: `target: 1_A o0 = O_P(r_n) with r_n = n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2 + n^{-kappa} tending to 0 (fixed design), or r_n = n^{-1/2} exp(C_R sqrt(log n)) (Gaussian rows, Q = S0); hence P-START with a rate` -> `target: 1_A o0 = O_P(r_n) with the rates at STATEMENT.md:242-243`
- rate: `r_n` -> `—`
- scope: `only the start interface is supplied` -> `fixed design and Gaussian rows`
- statements: Theory_work/Wave3/W3-START2/STATEMENT.md:176-180 -> Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-246

## Rebuild cost

- free: 0 re-point(s) PROPOSED (one cheap check each), no rebase, no re-review
