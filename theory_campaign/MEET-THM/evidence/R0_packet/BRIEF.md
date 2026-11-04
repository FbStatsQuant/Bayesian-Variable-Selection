# Fresh-eyes theory plan for SMC-BVS v3.1

You are an independent theoretical statistician asked to look at a statistical method **with fresh eyes**. You see only the method. On purpose, you are given none of the theory work already done on it: we want your own view of what can be proved, not a review of ours.

## Isolation (binding)
Work only inside this folder. Do not open, list or search any other directory on this machine (in particular no git repositories, no other project folders, no session or agent logs). You may search the published literature (papers, textbooks, arXiv) to locate known results, but do not search for this project, its authors or its code online. Never invent a citation: if you are not sure a result exists in the form you need, say so.

## Read
1. `METHOD_v3.md`: the method (sections 1–8 of its report).
2. `METHOD_v3.1_ADDITIONS.md`: what v3.1 adds (parallel layer, stacking, LS0, reporting).
3. `code/`: the v3 implementation (R driver + C++ core), if you need to know exactly what is computed.

## What the project wants (the PI's words)
- **Objectives, in order:** (1) accuracy in recovering the true posterior (evidence Z, PIPs, joint inclusion, general posterior summaries); (2) parallel scalability: "the final methodology must be parallelizable enough so you could scale it to p values that you could not otherwise in sequential MCMC". The parallel axis is particles and islands: "We are not trying to parallelize over variables"; (3) Bayesian variable-selection accuracy. It must work well under **correlated designs**, where split-and-merge parallel BVS methods break.
- **Local-to-global** is the method's founding idea: exactly enumerated local blocks give a product start π₀, and SMC tempering corrects it to the exact global posterior.
- **Provable or nothing:** "a fancy heuristic and hypothetically gives me perfect accuracy but cannot be formally proved is as good as nothing to me."
- **Extraction standard:** "what I want ... is extract until the last drop of information the method has into provable results. No rock can remain unturned at the end." The benchmark is a strong statistics paper that proves essentially everything its method allows: consistency of what it targets, properties of each algorithmic stage, the merged/final output, and computational complexity of the parallel scheme.
- **Venue:** paper 1 is Biometrika-grade; every main theorem will later get its own proof campaign ending in a referee-checked proof and, for its finite/combinatorial core, a Lean certificate.

## Your task
Produce **`THEORY_PLAN.md`** in this folder: a thorough plan of the theory this method supports. Think from first principles about every component (preprocessing, target posterior and prior, exact branch, blocks and composite start, neighbour graph, move kernel, resampling and tempering schedule, calibration, final islands and stacking, local search and LS0, HPM/MPM decisions, PIP poolings, general-h summaries, evidence estimator, run card, parallel layer, cost) and every property one could want (exactness/validity at fixed data, unbiasedness, consistency in N and in R, finite-sample error bounds, behaviour under correlation and masking, stage counts and sequential depth, work and memory, selection consistency as n, p grow, finite-n selection bounds, impossibility or limitation results, comparisons with split-and-merge or plain MCMC).

Sections:
1. **Component × property map:** a table, each cell either a candidate result (ID) or "nothing provable / not relevant" with a one-line reason.
2. **Candidate theorems.** For each: ID; precise draft statement with every hypothesis; the guarantee in one plain sentence and which objective it serves; whether it is likely already known in the literature (cite only what you are sure of) or new; a credible proof route naming the key lemma; difficulty (routine / substantial / hard); which core could be certified in Lean (finite combinatorics, an identity, an inequality) and which rests on cited probability theory; dependencies on your other items.
3. **Negative results and limitations** you expect to be provable (impossibilities, counterexamples, what no run diagnostic can detect, etc.).
4. **Design conditions:** which assumptions on X (correlation structure, sparse eigenvalues, block separation, masking) each result needs, and whether they cover genuinely correlated designs.
5. **Your recommended list for paper 1** (ranked, about 10–20 main theorems, each with its lemmas) and what you would defer.
6. **The single headline theorem** you think best captures "in local-to-global SMC, correlation costs sequential depth and particles, never correctness", stated as precisely as you can, with its scope.

Use honest status words: everything you write is a proposal or a PROOF SKETCH by you, unchecked. Small numerical sanity checks are allowed (one core, a few minutes each); state what you ran. Be thorough rather than brief: this is your only contribution, and its value is in finding results others might miss.

When done, reply with a short summary: number of candidate theorems, your top 5, and anything you think is the most surprising or underrated result the method could support.
