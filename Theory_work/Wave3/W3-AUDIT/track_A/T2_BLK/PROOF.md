# T2 · Lemma BLK — PROOF v5 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

## (BLK-a) The parameter B
`v3_fit` calls `v3_setup(ctx)` (`v3_fit.R:133`), which sets `B <- b$B` with `b <- v3_budgets(ctx$n, ctx$p)`
(`v3_setup.R:67-70`), and passes it to `cpp_setup(ctx, B)`; there `check_B(B)` rejects B ∉ [1, 16]
(`cpp/v3_core.cpp:145-146, 274`) and `st.blocks = make_blocks(D, B)` (`:279`). `v3_budgets` computes
`B <- min(v3_isqrt(n), v3_isqrt(p), 16)` (`v3_preprocess.R:22`), where `v3_isqrt` returns ⌊√x⌋ exactly: it starts at
`floor(sqrt(x))` and corrects by the two integer loops `while ((r+1)^2 <= x)`, `while (r^2 > x)` (`v3_preprocess.R:14`). Here
n = `nrow(X)` and p = the number of non-constant columns (`v3_preprocess.R:103, 111-113`; `ctx` is built from the kept
columns, `v3_fit.R:118`), which is the theory's p in setting G. So B = min(⌊√n⌋, ⌊√p⌋, 16).

Bounds. n ≥ 3 (`v3_preprocess.R:106`) and p ≥ 1 (else status `no_predictors`, `:114`), so ⌊√n⌋ ≥ 1 and ⌊√p⌋ ≥ 1, hence
B ≥ 1; B ≤ 16 by the min. B ≤ ⌊√p⌋ ≤ p. B ≤ ⌊√n⌋ ≤ ⌊n/2⌋: for n = 3 both sides are 1; for n ≥ 4, √n ≤ n/2. So
B ≤ min(p, ⌊n/2⌋) = K (`v3_preprocess.R:21`; C++ `D.K = std::min(p, n / 2)`, `cpp/v3_score.h:40`).

## (BLK-b) Partition and size bound
`make_blocks` (`cpp/v3_blocks.h:124-144`) takes a tree `T` from `complete_linkage` and does two things.

*The tree.* For p = 1, `T` is the single leaf 0 (`:52`). For p ≥ 2, `complete_linkage` performs exactly p − 1 merges
(`:76`); each merge takes two distinct active clusters a ≠ b (`:82`; `best[i] ≠ i` by `:70`, and `best[i]` is active:
it is recomputed whenever it pointed to the slot that was deactivated, `:93, 99-103`), creates one internal node with
those two nodes as children and `size = size[left] + size[right]` (`:85-88`), and deactivates b. With ≥ 2 active
clusters every active i has `best[i] ≥ 0` (`:67-72`), so a pair exists at every step. Hence `T` is a full binary tree
whose leaves are 0, …, p − 1 (leaf size 1, `:49`), every internal node's size is the number of leaves below it, and the
root (`:106`) has size p. Only this structure is used below.

*The cut* (`:127-133`). A stack starts with the root; a popped node x with `size[x] ≤ B` is retained as the cluster of
its leaves (`subtree_leaves`, `:111-119`); otherwise both children are pushed. Claim: the retained nodes are exactly the
nodes x with `size[x] ≤ B` all of whose strict ancestors have size > B. (A node is pushed iff it is the root or its
parent was popped with size > B — induction on depth.) Along the root-to-leaf path of any leaf ℓ the sizes strictly
decrease (both children of an internal node are nonempty) from p to 1 ≤ B (B ≥ 1 by (BLK-a)), so exactly one node on
the path is the first with size ≤ B; that node is retained and contains ℓ, and any retained node containing ℓ lies on
this path and is that first node. So the retained clusters are nonempty, pairwise disjoint, cover {0, …, p − 1}, and
each has at most B members. The loop terminates: each push moves strictly down the finite tree.

*The packing* (`:134-141`). Next-fit over the clusters c in retained order with a current block `cur`:
if `|cur| + |c| > B` then `cur` is closed and emptied (`:137`), then c is appended (`:138`); the last nonempty `cur` is
closed (`:140`). Invariant: |cur| ≤ B after each step — if no closing occurs, |cur| + |c| ≤ B; if it does, |cur| becomes
|c| ≤ B. Every closed block is nonempty: closing at `:137` needs |cur| > B − |c| ≥ 0, and `:140` closes only a nonempty
`cur`. Every cluster is appended to exactly one block, so the blocks are disjoint and cover {0, …, p − 1}; sorting within a
block (`:141`) does not change it. The shift j ↦ j + 1 maps this partition of {0, …, p − 1} bijectively onto a partition
of {1, …, p} with the same block sizes. Hence (BLK-b), and J·B ≥ Σ_b |C_b| = p.

## (BLK-c) Function of X only
The inputs of `make_blocks` are `D` and B. It reads `D` only through `correlation_matrix(D)`
(`cpp/v3_blocks.h:53, 10-17`), r_jl = G_jl / √(G_jj G_ll) with G = `D.G`, the Gram matrix of the preprocessed design
`D.X` (`cpp/v3_score.h:44-53`), and through `D.p`. It reads no stream (no `VariateSource` in `v3_blocks.h`) and not y.
`D.X` is the matrix `Xs` of `v3_preprocess`: column j is `v3_standardise` of the raw column (`v3_preprocess.R:116-121`).
Under EX-A both branches of `v3_standardise` (`:37-68`) return (x − x̄1)/s_x (the anchored branch: d = x − x₁,
u = d/max|d|, `correction` = mean(u − ū) = 0 exactly, z = (u − ū)/sd(u) = (x − x̄1)/s_x). So G = XᵀX with the theory's X,
and r_jl = R̂_jl. Hence the dendrogram — which uses only `dist = 1 − |r|` (`:55`), the max-update (`:96`) and
index-list comparisons (`:20-30, 62-66, 86`) — and the blocks are functions of (p, R̂); B is a function of (n, p).

Borel measurability: for fixed (n, p) the computation is a finite decision tree. Each branch condition is a comparison
(`<`, `!=`, `<=`) between continuous functions of X (on the open set where every column is non-constant, R̂ is a continuous
function of X; `max` and `|·|` are continuous) or between index lists that do not depend on X. So each set
{X : blocks(X) = (C₁, …, C_J)} is a finite union of finite intersections of sets of the form {f(X) < g(X)},
{f(X) = g(X)} with f, g continuous: Borel. ∎

## Use downstream (faithfulness of "the method's partition")
The same `st.blocks` (and `h->B` = B, `cpp/v3_core.cpp:275`) feed the block tables (`build_tables(st, sc)`,
`cpp/v3_core.cpp:283`), the start law and sampler (`build_start(st)`, `cpp/v3_core.cpp:300`), the final engine
(`cpp/v3_core.cpp:410`), the calibration engine (`cpp/v3_core.cpp:611`), the candidate set V (`st.comp`,
`cpp/v3_core.cpp:714`) and LS0's start mode (`start_mode(st, …)`, `cpp/v3_core.cpp:469`), so the partition of rows 3.1
and 3.6 is C(X). The registry's CC7 fact (B ≤ 16, `Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md:102-104`) is (BLK-a).
(Code note, not a lemma defect: the comment at `cpp/v3_core.cpp:144` says "1 <= B <= 20"; the enforced limit is
`B_MAX = 16`, `cpp/v3_core.cpp:145-146`.)

## Setting R (random rows)
If the raw rows are i.i.d. and each coordinate's marginal law is atomless (setting R: (Σ_n)_jj = 1), and n ≥ 2, then
for each j, P(x^r_{1j} = x^r_{2j}) = 0 (independent copies of an atomless law), so each column is non-constant almost surely, so X^r lies a.s.
in the open set where the standardisation map X^r ↦ X is continuous; composing with the Borel map X ↦ C(X) of (BLK-c)
(extended by a fixed Borel choice on the null set) gives a σ(X^r)-measurable partition which, off the null set, is the Borel function C(X) of X; it is independent of ε
because ε is independent of the rows.

## Binary64 (supports the "Not claimed" bullet)
Qualification (Sol SL1LC2 #3): the following assumes the run executes with every integer size, index and allocation
size representable (the C++ `int` arithmetic such as `2 * p - 1`, `cpp/v3_blocks.h:49`, does not overflow; this fails for
p ≥ 2³⁰); it is a remark, not part of the lemma.
(BLK-a): n and p are R integers ≤ 2³¹ − 1, so ⌊√n⌋, ⌊√p⌋ ≤ 46341 and every square in `v3_isqrt`'s correction loops
is an integer below 2⁵³, computed exactly; hence `v3_isqrt` returns ⌊√x⌋ exactly and B is exact. (BLK-b): the tree
argument uses only that each merge joins two distinct active slots (`best[i] ≠ i`, `best[i]` active), the integer size
arithmetic, and the cut-and-pack integer comparisons; these hold whatever the floating comparisons return (NaN
included), so (BLK-b) holds as coded. (BLK-c) in binary64: `make_blocks` reads only `correlation_matrix(D)` and `D.p`
(section (BLK-c) above), and the binary64 standardisation is column-wise and does not read y (`v3_preprocess.R:116-121`),
so the blocks are a function of (n, p) and the computed correlation matrix.
