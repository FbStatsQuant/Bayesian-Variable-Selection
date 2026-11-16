# T2 · Lemma BLK (the coded partition: a function of X, blocks of at most 16 columns) — STATEMENT v4 (draft, not locked)

Track A item T2 (`AUDIT.md` §6; CHECKPOINT_1 annex order 2). Tier B (code reading plus a finite combinatorial
invariant; no key lemma). **Lean target: yes for (BLK-b) (the cut-and-pack invariant, a finite statement); no for the
code correspondence.** Blocks rows 3.1, 3.6.

## Source of the premise
- `A:BLOCK-LE-16` (`Theory_work/INFRA/registry/assumptions.tsv:15`): "method partition is an X-measurable partition into
  blocks of size <=B=min(floor(sqrt n),floor(sqrt p),16)<=16", bridge "MISSING". Its registry source line
  (C-GROW STATEMENT line 61) is stale; the definition is the "Blocks" bullet
  `Theory_work/Wave1C/C-GROW/STATEMENT.md:65-67` ("a deterministic function of X; |C_b| ≤ B ≤ 16").
- As used in row 3.1: "an X-measurable partition with |C_b| ≤ 16. Nothing else about the partition is used anywhere
  below" (`Theory_work/Wave3/W3-RM/STATEMENT.md:46-48`); "a partition with blocks ≤ 16 that is a function of X"
  (`Theory_work/Wave3/W3-RM2/STATEMENT.md:217, 248, 254`).
- Checked part: `W3-SAMP:CC` CC7 "B = min(⌊√n⌋, ⌊√p⌋, 16) (`v3_preprocess.R:22`)" (row 3.6 uses only B ≤ 16, in
  `W3-SAMP:ST` (ST-c), `:LT#` (LT-b)).
- Method description: `Theory_work/State_of_Project/sections/02_method.tex:187-193`.

## Code of record
`Scripts/SMC_BVS/core/` at pin **4676af6** (= this branch's HEAD for the core). Paths relative to it.

## Setting
n ≥ 3 rows; a raw design X^r with p ≥ 1 non-constant columns (the theory's setting G: "fixed raw design X^r (n × p,
nonconstant columns)", `Theory_work/Wave1C/C-GROW/STATEMENT.md:57`). X := the centred, column-standardised design
(‖x_j‖² = n − 1), R̂ := XᵀX/(n − 1) its sample correlation matrix. EX-A (exact arithmetic).
Under a random design whose rows are i.i.d. and each of whose coordinates has an atomless marginal law (setting R of
`W3-RM`: rows N(m_n, Σ_n) with (Σ_n)_jj = 1, Σ_n not necessarily nonsingular, and the noise ε independent of the raw rows,
`Theory_work/Wave3/W3-RM/STATEMENT.md:41-42`)
the columns are non-constant almost surely (n ≥ 2); on the null set C is extended by any fixed Borel choice, and nothing
below depends on it.

**The partition map.** C(X) = (C₁, …, C_J) := `make_blocks(D(X), B)` (`cpp/v3_blocks.h:124-144`) with
B := min(⌊√n⌋, ⌊√p⌋, 16), defined for every X in the setting. The coded run computes it only on the sampler branch
(non-constant y, preflight passed: `v3_fit.R:99-103, 117, 120-133`), as `st.blocks` in `cpp_setup`
(`cpp/v3_core.cpp:272-279`); there the same object is used by the block tables, the start law and sampler, the
calibration and final engines, the candidate set V and the start mode of LS0 (`cpp/v3_core.cpp:283, 300, 410, 469, 611,
714`), and the reported diagnostic `cut_group` (`cpp/v3_core.cpp:811`; `v3_fit.R:141-142, 172`; not used by rows 3.1,
3.6). On the enumeration branch the partition is not computed and downstream statements refer to C(X) as a
hypothetical object (e.g. the start mode in 𝒦_n).

## Lemma BLK
- **(BLK-a) Block size parameter.** The code's B is min(⌊√n⌋, ⌊√p⌋, 16), and 1 ≤ B ≤ min(16, K), K = min(p, ⌊n/2⌋).
- **(BLK-b) Partition and size bound.** For every X, C₁, …, C_J are nonempty, pairwise disjoint, cover {1, …, p}, and
  |C_b| ≤ B ≤ 16 for every b. Hence J ≥ ⌈p/B⌉.
- **(BLK-c) Depends on X only.** C(X) is a function of (n, p, R̂) alone (not of y, the seed or any stream), and
  X ↦ C(X) is Borel (finite-valued with Borel level sets). Under setting R, C is σ(X^r)-measurable, equal almost surely
  to a Borel function of X, and independent of the noise ε.

(BLK-b) is a property of the cut-and-pack step for **any** full binary tree on p leaves (not only the complete-linkage
tree); nothing about the clustering's optimality is claimed.

## Not claimed
- That the dendrogram is the textbook complete-linkage tree, or any property of the blocks beyond (BLK-a)–(BLK-c) (none is
  used by rows 3.1, 3.6: `Theory_work/Wave3/W3-RM/STATEMENT.md:48`).
- Floating point in general (EX-A). The PROOF's last section also shows that (BLK-a) and (BLK-b) hold in binary64 as
  coded; (BLK-c)'s "function of R̂" then holds with R̂ replaced by the computed correlation matrix.
- Inputs with constant columns: the code drops them (`v3_preprocess.R:111-113`) and p then means the number kept.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track A T2 | `AUDIT.md` §6 T2 | — |
| v2 | setting, partition map, (BLK-c) | EQUAL in substance (C(X) defined on the whole setting; setting R a.s. line; source line fixed) | LC1 T2 #1, #2, #4, #5 | `reviews/LC1_reply_opus.md` | pending (gate) |
| v2 | binary64 bullet | EQUAL (now proved, PROOF last section) | LC1 T2 #3 | `reviews/LC1_reply_opus.md` | pending (gate) |
| v2 | (BLK-c) setting-R clause (σ(X)-measurable, independent of ε) | STRONGER (retagged from EQUAL) | LC1r #12 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v3 | setting R premise | EQUAL (premise stated exactly: atomless coordinate marginals) | LC1r #9 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v3 | downstream list; binary64 (BLK-c) sentence | EQUAL (editorial) | LC1r #10, #11 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v4 | setting R premise (atomless marginals cover singular Σ_n; ε independence stated) | STRONGER (retag of the v3 row) | LC1r2 #8, #9 | `reviews/LC1r2_reply_opus.md` | pending (gate) |
| v4 | (BLK-c) setting R: "σ(X)-measurable" → "σ(X^r)-measurable, a.s. a Borel function of X" | WEAKER (wording now matches the proof; downstream "X-measurable" uses are satisfied a.s.) | LC1r2 #10 | `reviews/LC1r2_reply_opus.md` | pending (gate) |
