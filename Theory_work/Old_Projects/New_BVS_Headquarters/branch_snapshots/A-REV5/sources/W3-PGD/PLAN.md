# W3-PGD plan (working notes; the deliverable is REPORT.md)

Inputs read: PROTOCOL, tasks/W3-PGD.md, THEORY_PRIORITIES, 00_COMMON, T37 file,
W1-T37R (REPORT, PROOF: Lemma 0, Prop 1, Thm A, B, C; td_core.py), W1-T38E REPORT, W1-T03R (anchored SE).

Plan
1. Population side (deterministic): PGD <= GERC (OLS-type exact recovery condition, theta-free)
   + TRC (truth retention); block reduction (exact iff under block orthogonality);
   necessity of PGD (reverse PGD => TD'_P fails w.p. -> 1); stability / random-design transfer.
2. Noise side: score representation lemma; population-gap comparison lemma (m >= 1 states under PGD,
   truth-removing moves); superset states (m = 0) by chi-square union bounds:
   d = 1 needs no LD; restricted extras set D with |D|^{d-1} = o(n^{1/2}) needs no LD;
   general d: LD replaced by a constant-threshold local/far condition (star).
   Counterexample: d = 2, arbitrary extras, equicorrelated nulls r > 1/2, p ~ n: TD'_P fails w.p. -> 1.
3. Numerics: S1-S6 population (block designs exactly; S5 by exchangeability; S2 windows),
   n = 200 realised designs (Python generator, same law, not same bits), greedy-path margins.
4. Main theorem with full proof (PROOF.md), REPORT.md.
