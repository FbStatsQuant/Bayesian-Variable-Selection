# L4: table discovery and posterior-to-reported-model transfer

Status: PROVED (by this seat, unchecked). Design-agnostic component statement, not a new posterior-consistency theorem. This supplies the full-scored-set conclusion for the s0=1 singleton diagnostic, even though its LS0 route fails.

## Statement

For each admissible data set let the method partition predictors into blocks C_b, form all feasible subset scores of each block, and ingest these into its global all-scored HPM ledger. Assume exact score arithmetic, the complete table-ingestion behavior of the merged method, and the potential/actual output contract GUARD-W. Let A_n be the event that S0 is feasible and contained in a block. Then

{potential output and S0 not scored} is a subset of A_n^c.

Consequently D_n<=P(A_n^c), and
P(actual output and reported HPM != S0)<=P(A_n^c)+2E[1-pi(S0|data)].

Thus if P(A_n)->1 and posterior mass pi(S0|data)->1 in probability, the joint-with-output error tends to zero. If also P(actual output)->1 under an independently justified allocation, reported-HPM consistency follows. No design structure, iid law, factor rank, or LS0 path assumption is used in this transfer. Those assumptions may be used only to establish its two statistical inputs or delivery.

## Method-side premise and proof

The production final run calls ingest_tables before SMC (Scripts/SMC_BVS/core/cpp/v3_core.cpp:408). The routine starts at Scripts/SMC_BVS/core/cpp/v3_core.cpp:372, iterates all block masks, computes F=logprior[|U|]+logm(U), and offers them to the ledger. We assume admissibility/exact arithmetic so a feasible truth subset is not a NaN table entry. For large n, B<=K; feasibility is explicit in A_n regardless. The exact-enumeration branch already scores every feasible model. On other potential-output branches with complete ingestion, if S0 is contained in C_b its mask is among those ingested, and its score is the full F(S0), not a product-block approximation. Hence the inclusion for D_n.

On actual output GUARD-W identifies the reported all-scored record with the potential one. If A_n holds and pi(S0)>1/2, S0 has strictly greater posterior mass (and F) than every other model, so the all-scored HPM is S0. Therefore the error event is contained in A_n^c union {pi(S0)<=1/2}. Markov gives P(pi(S0)<=1/2)<=2E[1-pi(S0)]. Boundedness of 1-pi in [0,1] turns convergence in probability into convergence of its expectation. Finally add P(no actual output) to obtain unconditional consistency when delivery is separately established.

## Application and limits

For s0=1 and K>=1, A_n holds for every partition, deterministically. In L2's one-truth subclass, the full method therefore scores S0 and D_n=0 despite LS0 missing it with probability ->1. This establishes full-method discovery, not a new proof of the required posterior concentration or delivery premises. Under any independently established posterior-consistency and delivery theorem, the displayed transfer completes reported consistency on this subclass.

For two truths in distinct singleton blocks, A_n fails, and this lemma is silent. It neither rescues that case nor establishes inconsistency. The argument works for arbitrary designs whenever block containment holds; it is an ingredient suitable for the design-agnostic main theorem.

Falsification: numerics/n7_table_discovery.py and N7_table_discovery.json (exhaustive small partition/mask inclusion and a posterior-to-HPM control). Source fidelity must also be independently reviewed; the numerical control does not claim to execute the C++ ledger.
