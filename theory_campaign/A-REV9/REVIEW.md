# A-REV9 independent review — working checkpoint

The authoritative scope is W8-SYNTH §8 task 7. Source heads are pinned in SNAPSHOT.txt; readable source copies are under sources/ (Git blobs at those heads remain authoritative). Review verdicts do not alter author statuses or adopt results. Analysis is symbolic; no simulation or benchmark has been run locally or remotely.

## Certificate checkpoint

- Lemma M: VERIFIED in exact arithmetic. The push-through identity gives Q=y'y/(n+1)+n/(n+1)y'(I+(n+1)XX')^-1 y. Inversion reverses PSD order. For a column addition D'/D=h(n+1)/h(1), h'(c)=x'(I+cM)^-2 x>=0. BB weight ratio is (k+1)/(2p-1-k)<=1.
- C1(a): ERROR as literally quantified. It includes S=HPM in the claimed ratio <=exp(-g). Any strict best score with g>0 gives 1<=exp(-g)<1. Repair: exclude HPM, as C3(c) already does. The Z_T bound itself is VERIFIED.
- C1(b): VERIFIED simultaneous Markov implication under fixed-data frozen-run unbiasedness and stop-only output coupling. Original unscored-mass wording: ERROR; O-VCERT R1 correctly replaces it with mass outside T. This does not upgrade the original statement.
- C1(c): VERIFIED as a non-implication from unbiasedness alone; it does not exclude deterministic upper bounds on Z.
- C2: VERIFIED as a conditional implication with PW2, independent islands and frozen calibration. Cantelli gives B_T/(B_T+4 epsilon^2). It does not establish PW2 or completion probability.
- C3: VERIFIED ratios and fully rescored regions in exact arithmetic. Apply local certification to the returned/scanned centre; identifying it with the reported HPM requires checking identity, especially under exact ties.
- C4: VERIFIED exact-arithmetic box inequalities. w and D at L and Q at U give the maximum bound; summing the exact size weights gives the mass bound. The displayed mass lower bound is conservative even if the HPM leaf is not isolated. FP clause remains GAP without certified errors for the mixed-endpoint bound Phi, not merely errors for complete scores F.
- C5: ERROR if interpreted as a tie-aware posterior-miss certificate from a weak score inequality. Duplicate columns give equal-size equal-score models; if the unscored truth wins lexicographic ties, scoring it changes the report. The displayed probability inclusion for strict F(S0)>F(HPM) is VERIFIED. Repair the prose with strict inequality or the total HPM order and S0 feasible.
- C6: GAP pending R1, FP inflation R2, and explicit local/region certificate validation. Its exact-arithmetic union-of-claims argument is valid for the repaired claims under statistical-field stop-only coupling, not for the original card.

Further review in progress. LOCKABLE at this checkpoint: Lemma M; the deterministic Z_T inequality; C1(c); conditional C2; C3 ratios; exact C4 bounds; strict-score C5 probability inclusion. No original GAP is upgraded.
