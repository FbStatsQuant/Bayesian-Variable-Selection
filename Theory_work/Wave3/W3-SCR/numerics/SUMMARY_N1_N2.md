# N1 — production core (main @ 2252d57, numerics/core_copy): frequency of the printed condition

S0 has 4 truths, theta = bscale*(1.4,-1.0,1.8,-1.2), sigma = 1. 'cert' = fit$local_certified; '|S|<=8' = reported model of size <= 8;
'cap' = a move cap was hit (local_limit); 'S0 in S' = reported model contains the truth; '= S0' exact.
'cert&sparse&miss' = certified, size <= 8, and a truth missing (the event of the theorem).

| design | n | p | bscale | fits | completed | cert | cert by (both/final/ls0/none) | cap | sizes of reported model (min/med/max) | cert & |S|<=8 | S0 in S | = S0 | cert&sparse&miss | LS0 start size (med) | median sec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ar(0.7) | 100 | 400 | 0.35 | 10 | 10 | 10 | 7/3/0/0 | 0 | 0/3/4 | 10 | 1 | 1 | 9 | 1 | 505.6 |
| ar(0.7) | 100 | 400 | 1 | 10 | 10 | 10 | 10/0/0/0 | 0 | 4/4/4 | 10 | 10 | 10 | 0 | 3 | 487.6 |
| cs(0.5) | 100 | 400 | 0.35 | 10 | 10 | 10 | 8/2/0/0 | 0 | 0/1/4 | 10 | 0 | 0 | 10 | 1 | 351.9 |
| cs(0.5) | 100 | 400 | 1 | 5 | 5 | 5 | 5/0/0/0 | 0 | 4/4/4 | 5 | 5 | 5 | 0 | 2 | 1175.6 |
| fac(k=3) | 100 | 400 | 0.35 | 9 | 9 | 9 | 9/0/0/0 | 0 | 0/1/3 | 9 | 0 | 0 | 9 | 1 | 135.9 |
| fac(k=3) | 100 | 400 | 1 | 7 | 7 | 7 | 7/0/0/0 | 0 | 4/4/4 | 7 | 7 | 7 | 0 | 2 | 472.6 |
| iid | 100 | 400 | 0.35 | 10 | 10 | 10 | 10/0/0/0 | 0 | 0/3/4 | 10 | 1 | 1 | 9 | 1 | 258.9 |
| iid | 100 | 400 | 1 | 10 | 10 | 10 | 10/0/0/0 | 0 | 4/4/5 | 10 | 10 | 9 | 0 | 3 | 229.2 |

All fits: 71; completed 71; certified 71; certified and size <= 8: 71.

Uncertified completed fits (detail):

Certified archive endpoints (all completed fits): 142 certified endpoints; of size <= 8: 142; of these missing a truth at bscale = 1: 0; at bscale < 1: 75.

# N2 — boundary numerics (own implementation of the coded search; 10 draws per scenario; n = 100, p = 400 unless noted)

Each draw: coded local search (unlimited moves) from 24 starts (empty, truth, proxies, 10 random of size 5, 5 of size 15, 3 of size 30, 3 of size K-2 = 48, no truths in random starts); every endpoint is LO.

| scenario | assumption violated | draws with an LO endpoint of size <= 8 missing a truth | ... size <= 16 | ... any size | draws where S0 is an endpoint | draws with an LO strict superset of S0 | endpoint sizes (0-8 / 9-16 / 17-49 / K) |
|---|---|---|---|---|---|---|---|
| ar_strong | none | 0/10 | 0/10 | 0/10 | 10/10 | 0/10 | 10 / 0 / 0 / 0 |
| cs_strong | none asymptotically; at n = 100 the visibility margin is not met at the offending model (noiseless ratio 0.8-1.2, n2_out/DIAG_visibility.txt) | 1/10 | 1/10 | 1/10 | 8/10 | 4/10 | 11 / 0 / 4 / 0 |
| dupnoise | sparse floor (near-duplicate noise columns); the one miss is a visibility-margin failure at n = 100 (ratio 0.80) | 1/10 | 1/10 | 1/10 | 10/10 | 0/10 | 11 / 0 / 0 / 0 |
| fac_p1000 | none found (p = 1000) | 0/10 | 0/10 | 0/10 | 10/10 | 2/10 | 11 / 0 / 1 / 0 |
| fac_strong | none asymptotically; at n = 100 the visibility margin is not met at the offending model (noiseless ratio 0.8-1.2, n2_out/DIAG_visibility.txt) | 1/10 | 1/10 | 1/10 | 10/10 | 2/10 | 11 / 2 / 1 / 0 |
| iid_strong | none | 0/10 | 0/10 | 0/10 | 10/10 | 0/10 | 10 / 0 / 0 / 0 |
| iid_weak | visibility (weak signal) | 9/10 | 9/10 | 10/10 | 1/10 | 1/10 | 11 / 1 / 28 / 0 |
| masked | visibility only (masked pair; margin holds) | 10/10 | 10/10 | 10/10 | 10/10 | 2/10 | 20 / 0 / 25 / 2 |
| noisecs98 | sparse floor only (anchored floor holds) | 0/10 | 0/10 | 0/10 | 10/10 | 9/10 | 25 / 0 / 0 / 0 |
| twin90 | identifiability margin (twin r=.9) | 0/10 | 0/10 | 1/10 | 10/10 | 0/10 | 10 / 0 / 1 / 0 |
| twin99 | identifiability margin (twin r=.99) | 7/10 | 7/10 | 8/10 | 5/10 | 1/10 | 13 / 0 / 1 / 0 |
| twin999 | identifiability margin (twin r=.999) | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10 / 0 / 0 / 0 |

SCR-C boundary: LO supersets of the form S0 + {j, l} (exhaustive over pairs, strong signals):

| scenario | draws where S0 is LO | LO pair-supersets per draw | draws with at least one LO strict superset (pair or single) |
|---|---|---|---|
| pairs_cs20 | 10/10 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | 0/10 |
| pairs_cs50 | 8/10 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | 2/10 |
| pairs_cs80 | 9/10 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | 0/10 |
| pairs_iid | 10/10 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | 0/10 |
