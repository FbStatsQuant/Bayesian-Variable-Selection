# WP2 — setup: correlations, neighbour graph, partition, tables, start law, start mode (Opus 5.5 builder)
Read BUILD_COMMON.md first. Branch: `exp/P1M-wp2-setup`. Use `Docs/Experiments/P1M/INTERFACES.md` when it appears (WP1
writes it within hours). Until then, start from the v3 code (`core/cpp/v3_blocks.h`, `v3_start.h`, `v3_core.cpp:150-310`)
and keep your types easy to adapt.

Scope (ENGINEERING_SPEC §0-v2.2 #5, §1 `setup`, §2, §5 T11; REVIEW_fable R3, R6; DECISIONS D-4):
1. **Streamed correlation tiles**: each entry is a sequential dot product (same order as `core/cpp/v3_score.h:45-53`) with
   lanes over pairs. O(p·B + edges) memory; threaded (≤ 3 threads on Owls). Outputs: the neighbour graph, **bit-equal to
   `core/cpp/v3_blocks.h:149-170`** (r_n threshold, ≥ 1 neighbour, ≤ B, symmetric union, tie by index); the duplicate
   components (|r| ≥ 1 − 1e-10); the edge set {|r| ≥ τ_n}.
2. **Partition, two modes:**
   - *exact* (theory mode; feasible to ≈ 2·10⁴–10⁵ by memory): the v3 complete linkage + top-down cut + leaf-order packing,
     bit-equal to `v3_blocks.h:46-145`;
   - *truncated* (V-1M): complete linkage restricted to merges at height ≤ 1 − τ_n on the sparse graph (τ_n = r_n =
     √(2 log p / n), edges |r| ≥ τ_n), R13 ties, left-child rule, the coded top-down cut for clusters > B, next-fit packing
     by minimum member index.
   - Gate **T11**: the truncated forest equals the exact dendrogram's merges of height ≤ 1 − τ_n (p ≤ 20k; AR, BLK, IND,
     plus a tie case).
3. **Tables** by depth-first enumeration with prefix reuse (bit-equal to `core/cpp/v3_start.h:76-98`), threaded over
   blocks. Compact storage; `logm_tab`/`route_tab` dropped after the table top stores are built.
4. **Start law** (size profiles, convolutions, log Z̄₀, sampler tables; `v3_start.h:101-157`) bit-equal. **Start mode**
   with an **iterative** enumeration (no `std::function` recursion of depth J; `v3_start.h:271-301`), bit-equal, incl. the
   tie-DP path.
5. `setup.bin` writer/reader per INTERFACES.md.
6. Measured on Owls: time and memory of every stage at p = 10⁴ and 10⁵ (n = 200), and of the correlation pass at 10⁶ if it
   fits in ≤ 16 GB and ≤ 15 min with 3 threads. Otherwise project it and say so.
