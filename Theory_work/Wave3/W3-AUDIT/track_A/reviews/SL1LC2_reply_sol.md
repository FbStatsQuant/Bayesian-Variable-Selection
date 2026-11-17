# SL1+LC2 reply — Codex gpt-6.1-sol (high), delegate_task fed82308, launched 17:07, returned ~18:0x CST 2026-11-16 (verbatim)

**Part 1 — statement lock**

- **T1: LOCK WITH CHANGES.** Extend the operational/internal-value definition to cover the allocation parameter used during guard construction, or narrow (GW-iv)’s quantification over local variables. Finding 1 is required.
- **T2: LOCK WITH CHANGES.** Explicitly convert the partition’s internal indices to mathematical column indices and qualify the supplemental binary64 claim. Findings 2–3 are required.

Both lemmas address the premises consumed by the cited downstream statements. I found no substantive failure of stop-only delivery or of the cut-and-pack invariant.

**Part 2 — line check**

- **T1: VERIFIED WITH AMENDMENTS.** The check-site inventory, stop propagation, unavailable-estimate handling, comparison with the potential run, calibration-event inclusion and complete-search argument check out for the stated resource checks. The all-fields allocation claim needs the amendment in finding 1.
- **T2: VERIFIED WITH AMENDMENTS.** The parameter bounds, active-cluster invariant, cut, packing, dependence on the design alone and Borel argument check out after the index conversion is stated. The setting-R argument correctly permits singular covariance matrices: atomless coordinate marginals suffice. The supplemental binary64 argument needs an execution-bounds qualification.

The requested `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` returned exit code 0.

**Numbered findings**

1. **S — T1’s allocation exception misses a local parameter of guard construction.**
   [T1_GW/STATEMENT.md:36](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md:36), [T1_GW/STATEMENT.md:83](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md:83); repeated in [T1_GW/PROOF.md:120](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/PROOF.md:120).

   A field expressly includes a local variable. At [cpp/v3_core.cpp:764](/home/fb31/BVS-wt/W3-AUDIT/Scripts/SMC_BVS/core/cpp/v3_core.cpp:764), `cpp_runtime_new` receives the parameter `double hours`, supplied from the normalised allocation. This parameter is neither a clock/environment reading nor a value computed or written by a check body. It is also distinct from the explicitly internal guard member `RuntimeGuard::allocation`.

   Consequently, under the current definitions, this parameter is statistical state. Changing the input allocation changes it in P°, contradicting “every other statistical field” being a function of `(X, y, seed)` and options alone. Saying that the helper’s **output** is operational does not classify its input parameter as operational.

   **Fix:** explicitly include the dedicated guard-construction parameter `cpp_runtime_new::hours` among internal values, and apply the operational classification to its forwarding copies. Alternatively, restrict the allocation-independence assertion to the statistical records actually needed downstream. Update Step 4 accordingly. This defect does not affect the reported estimates or the stop-only comparison.

2. **F — T2’s partition definition omits the index conversion.**
   [T2_BLK/STATEMENT.md:32](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/STATEMENT.md:32), [T2_BLK/STATEMENT.md:43](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/STATEMENT.md:43); [T2_BLK/PROOF.md:40](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/PROOF.md:40).

   `make_blocks` returns subsets of `{0, …, p−1}`. The statement defines C(X) as that return value but then claims coverage of `{1, …, p}`. Already at `p = 1`, its literal definition gives `({0})`, not `({1})`. The proof establishes coverage of the internal index set and then passes directly to (BLK-b).

   The actual R interface performs the missing conversion through `blocks_to_R` → `models_to_list` → `to_orig` at [cpp/v3_core.cpp:143](/home/fb31/BVS-wt/W3-AUDIT/Scripts/SMC_BVS/core/cpp/v3_core.cpp:143).

   **Fix:** define `C_b(X) = {j + 1 : j ∈ make_blocks(D(X), B)_b}` in the stated no-dropped-columns setting. Explain that `st.blocks` is its internal representation and that reported blocks use `D.orig`. Add this conversion at the end of the partition proof.

3. **S — The supplemental binary64 assertion needs integer/execution bounds.**
   [T2_BLK/STATEMENT.md:55](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/STATEMENT.md:55); [T2_BLK/PROOF.md:75](/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/track_A/T2_BLK/PROOF.md:75).

   Exactness of the squares in `v3_isqrt` does not establish that the tree’s integer arithmetic is safe throughout the stated R dimension range. For example, [cpp/v3_blocks.h:49](/home/fb31/BVS-wt/W3-AUDIT/Scripts/SMC_BVS/core/cpp/v3_blocks.h:49) evaluates `2 * p - 1` using signed `int`; on the 32-bit integer model used by this argument, `p = 2^30` already overflows the intermediate multiplication. Thus “these hold whatever the floating comparisons return” omits a separate representability requirement.

   **Fix:** qualify the supplemental binary64 result by successful execution with all integer sizes, indices and allocation sizes representable. Alternatively, remove that supplemental claim. The exact-arithmetic combinatorial argument is unaffected.

SL1LC2-VERDICT: T1 lock=LOCK WITH CHANGES, check=VERIFIED WITH AMENDMENTS; T2 lock=LOCK WITH CHANGES, check=VERIFIED WITH AMENDMENTS
