# Key-lemma checkpoint

2026-11-09 10:03 CST (approximate). Key diagnostic lemma drafted: lemmas/L2_singleton_start_swaps.md, PROVED (by this seat, unchecked), following R03 LOCK-WITH-CHANGES. It proves a proposed early-swap lower bound for singleton partitions and an LS0-only cap obstruction; production-profile target remains OPEN. Proof compares a tail-null swap against every deletion uniformly over O(log n) adaptive swaps. It uses a residual upper bound, not the failed p<=n/2 residual lower bound. Fresh lemma check required before midpoint use.

Important scope: singleton truth is already scored through block tables; for s0=1, D_n=0 under ideal output. The s0=2 variant avoids table discovery but does not analyze SMC/final search. No full-method failure or cap remedy is proved. HQ design-agnostic ingredient map in GENERAL_ASSUMPTIONS.md; cluster request nonblocking.

2026-11-09, before key path lemma. Target T2 remains OPEN.

Statement v2 applies R01 LOCK-WITH-CHANGES. Draft L0 gives rank iff; draft L1 gives saturation under nonzero total signal and p-16s0>=K uniformly over bounded partitions. Both PROVED (by this seat, unchecked), awaiting R02; neither used downstream.

Numerics N1_exact_grid.jsonl records the actual capped-DP start and uncapped adapted CS path. n=800,p=680, seeds 0 and 1 miss truth under merged LS0 cap, but reach truth uncapped. No asymptotic failure or full-method failure inferred. Script n1_exact_grid.py; dense controls and rank/increment falsification in n2_checks.py and N2_checks.json. Small-n negative increments are retained, not suppressed.

Outstanding: noise-selected start allocation and truth inclusion, swap count, late path, SMC/final-search discovery, cap remedy/minimality, population-CS experiments. Independent midpoint and final review gates not reached.
