# W7-SEC: The cheap secondary lemmas — T05 (disclosed negative), T33 (numerical margins), T32(i) (resource counts)

Three small, self-contained results that the paper's supplement needs and nobody has proved:
1. **T05** (`Docs/Theory/theorems/T05_A4_orthogonal_threshold.md`, one-pager `Docs/Theory/one_pagers/T05.md`): under orthogonal design, the g-prior + BB(1,p) HPM loses a √log n factor to the oracle threshold. The paper presents it as a **disclosed negative** remark. Prove it cleanly with explicit constants.
2. **T33** (`T33_T23N_numerical_margins.md`): numerical margins on a common scored set. Combine with W2-BOOK's VAL-FP contract (`theory/W2-BOOK`, Prop 2(f)) and give the floating-point error bound for F(S) as implemented in `Scripts/SMC_BVS/core/cpp/v3_score.h` (Cholesky / log-det path): a deterministic bound on |F̂(S) − F(S)| in terms of condition numbers, and the induced bound on HPM tie-breaking and on log Ẑ.
3. **T32(i)** (`T32_T23C_resource_counts.md`): the branch-specific arithmetic and storage counts. T38's cost corollary (c) rests on it and it is still a CONJECTURE (`theory/W4-T38FULL` item 5). W5-LOCKBOOK (`theory/W5-LOCKBOOK`, if pushed) may have started it — read it first and do not duplicate; if it is done, verify it instead and move on.

Each: statement with hypotheses, full proof, status word, confidence card.

**Deliverable:** `theory_campaign/W7-SEC/REPORT.md`.
