# Proposed bounded-block refinement — awaiting statement lock

This extends the current initial-swap route; it does not replace or restart the ticket. No proof is claimed here. Fixed centered exact-CS X with rho=1/2; sigma=1; p=floor(3n/4), K=floor(n/2); fixed support S0={0,16}, both coefficients 1. Deterministic consecutive blocks of 16, with one final remainder if needed. For sufficiently large n, B=16. This profile is a specified example until a source audit establishes whether the production tie convention emits it for exact CS; no identification with production is presupposed.

## Target statements

B1: with probability ->1 every start maximizer has size K, contains both truths, and every full truth-free block receives either 10 or 11 variables. Within each such block the selected variables are exactly its largest u null xi values (u its allocated size), under the usual enlarged-space independent-noise representation. No claim of unique population allocation across identical blocks.

B2: with probability ->1 for every fixed C>0 the first ceil(C log n) greedy F moves exist and are null swaps. Consequently LS0's own closed scanned neighborhoods miss S0 under cap ell+K with probability ->1. For each fixed C the event is separate; no simultaneous uncountable-C assertion is intended. The full method can still discover S0 through SMC/final search. The two truths lie in different blocks, so table containment alone does not settle discovery.

B3 (source audit target): determine the exact block-size profile induced by shipped linkage ties and packing under an exact-CS input. If it differs from the specified profile, retain B1/B2 only as an explicit-profile example or re-lock an appropriate class. Do not silently regard source numerical partition as exact implementation identity.

## Candidate route to test, not a proof

The population response variance is v=4. A pure-null u-subset explains 2u/(u+1), leaving R_N(u)=2+2/(u+1). A u-subset in a one-truth block containing the truth explains 2.5-.5/(u+1), leaving R_T(u)=1.5+.5/(u+1). Candidate table utility is -.5 log(R(u)/4), with u=0 handled separately. Check both formulas independently. Pure-null utility is strictly increasing/concave, so a size-preserving transfer should force all full null-block allocations to differ by at most one; the mean fill tends to 32/3, yielding 10/11. Sample profile errors need to be uniformly o(n) across O(n) bounded blocks. The truth's first population increment exceeds every pure-null first increment, and including truth at fixed u should beat an all-null subset; neither statement should be assumed without a gap calculation.

Within a fixed-size pure-null block, exact quadratic exchange comparisons may show that larger z always wins on the uniform positive-marginal event, without an asymptotic gap assumption on noise order statistics. Since 10/11<16, each pure-null block excludes its minimum xi. Independent disjoint block minima should leave polynomially many outside values below -sqrt(1.5 log n). An early adaptive family with O(log n) exchanges can remove only O(log n) of them.

For initial swap comparison, a full retained-null distribution may be unnecessary: global sum|xi|=O_P(n) bounds the scalar centre of every size-K truth-containing model, and sufficiently many globally bounded xi force each size-K model to contain a bounded null. L2 exact score formulas then compare an extreme incoming null with a bounded outgoing null against all deletions. Check uniformity and truth-out moves carefully.

This would strengthen the explicit-partition obstruction and provide ingredients for a design-agnostic theorem, but still relies on exact-CS scalar reduction. No cap remedy or full-method failure follows. No experiment substitutes for proof. Numerical falsification must precede downstream use of each proved lemma.
