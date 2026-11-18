> **SUPERSEDED by TRACK_B_v1.4.md + WRITING_DELTA_v1.4.md.**

# Writing delta — assumptions section, TRACK_B v1.2 → v1.3 (audit Fable, 2026-11-16)

Cause: Song–Liang's supplement was read (Theorem S on MAP consistency, supp p. 13; proofs). Source: `TRACK_B.md` §S, §T2.

**The headline changed.** Replace the v1.2 sentence "Their assumptions are of the same kinds as Song–Liang's … where they
differ ours are the stronger as stated …" by:

> The posterior theorems hold on all our designs. Their assumptions are of the same kinds as Song–Liang's and are
> neither uniformly stronger nor uniformly weaker. Against their selection theorem (Theorem S of their supplement) we
> ask a narrower range of p (n^A against n^{κ log n}) and a fixed eigenvalue floor on bounded sets; we ask less elsewhere:
> no upper eigenvalue bound, only a 1/n-level floor on O(log n) columns and nothing on larger sets, no tuning of the
> prior, and signals as small as √(log n/n) in the fixed-design theorem. Against their Hellinger theorems (1–2) we add
> the range of p, a c/n collinearity floor and a row law. Our conclusions are stronger, and none of these differences
> excludes any of our designs.

**Four sentences to change wherever they appear.**
1. Coefficient size. Old: "stronger than what Song–Liang state". New: "Song–Liang's theorems state no condition on the
   size of the nonzero coefficients, but their proofs treat them as constants (supplement pp. 5 and 15); our theorems
   state this, and the fixed-design theorem allows signals down to √(log n/n)."
2. Eigenvalue floor. Keep "stronger in level than their Condition 3". Add: "Their selection theorem (Theorem S) asks
   two-sided eigenvalue bounds on every model of |t| + r̄_n columns ((22)–(23)); ours has no upper bound and, beyond
   bounded sets, only a 1/n-level floor on O(log n) columns."
3. Their MAP result. Old: "their MAP consistency is in their supplement" (not compared). New: "Their Theorem S gives the
   posterior mode only, max_{k≠t} π(k | D_n)/π(t | D_n) → 0 in probability, with no rate; our rate for 1 − π(S₀ | y)
   implies it."
4. Sampler output (also card row 3.1 and Corollary 9C's comparison). Old: "they prove nothing about its selection
   output". New: "their statements on the sampler's output are limits in the number of iterations at fixed data (their
   Lemma S₂ and a citation, supplement pp. 12–13, 16–17); they prove nothing at a finite computational budget or
   jointly in n."

**Unchanged:** every inside/outside entry for our designs; B1, B3, B7 (label), B8, B9, B10, B11; the core 2 comparison
(same Hellinger distance; their divergences d_t are proof devices only); range of p against their Hellinger theorem.
Range of p against Theorem S: "narrower, by little" (new clause).
