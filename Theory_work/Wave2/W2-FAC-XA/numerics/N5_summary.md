# N5 fuzzy geometry falsification

UNCHECKED pending Claude. Standard library only. Seeds exactly 0 through 19.

Run from repository root:

    python Theory_work/Wave2/W2-FAC-XA/numerics/N5_fuzzy.py
    python Theory_work/Wave2/W2-FAC-XA/numerics/N5_verify.py

16 deterministic exhaustive subset searches (p<=9), 60 Gaussian exhaustive
subset searches (p=10), 240 sampled Gaussian paths (p=512). Maximum retained
deleted-hull depth divided by additive distance tolerance: respectively
1.0000000000000002, 1.4373876890351853, 0.9999609795931377.

The exhaustive search stores one history per reachable subset, which suffices
for eligibility and hull depth; it does not enumerate all shadow histories.
Sampled policies: random eligible, farthest eligible, next-hull-depth greedy,
and direction switching. No score, gain coupling, event-E_n, or entry-majority
test. No logarithmic propagation claim follows from absence of larger failures.

N5_fuzzy_results.json stores cases and witnesses. N5_fuzzy_trace.json records
the worst small Gaussian witness. N5_verify_results.json records an exact
rational version and 256 successful shadow-construction checks on stored
witness paths. The rational case refutes hull depth<=epsilon, not a general
O(epsilon log p) band bound. See ../lemmas/L3_fuzzy_attempt.md for the rigorous
polynomial shadow bound and the explicit remaining gap.
