# T4 · Lemma ENC (the start object is built as Lemma E4 assumes) — STATEMENT v2 (draft, not locked)

Track A item T4 (`AUDIT.md` §6; CHECKPOINT_1 annex order 4). Tier B (code reading; registers N3's encoding premise as a
code-check). **Lean target: no** (code fact). Blocks row 3.1 (through `W3-RM:E4`, the start-mode clause of RM-0).

## Source of the premise
- `W3-RM:E4` (Lemma E4, "PROVED-CHECKED") assumes "N3 (H1) (the `Start` object encodes the ordered actual partition, the
  tables log r_b, the prior and K), **strengthened** to require `st.blk` and `st.pos` to be the inverse maps of the
  ordered actual blocks on every branch and a valid `D.p` (as in ENG lemmas/TDP_E.md:28-36)" [backticks dropped in the quote]
  (`Theory_work/Wave3/W3-RM/STATEMENT.md:219-222`).
- N3 (H1) (`Theory_work/Wave1/W1-N3/STATEMENT.md:92-98`): `st.D` a valid pointer to a `Data` with `D->K = K` and
  `D->logprior` of length K + 1 equal to λ; `st.J = J`; `st.blocks[b]` = C_b (increasing); `st.logr[b]` of length
  2^{|C_b|} with `st.logr[b][code(U)] = ρ_b(U)` for |U| ≤ min(|C_b|, K) and `st.logr[b][0] = 0`; `st.logprof[b]` of length
  min(|C_b|, K) + 1; `st.codes_by_size[b][j]` the size-j codes in increasing numeric order; code(U) = Σ_{x∈U} 2^{pos(x)},
  pos(x) = x's position in the increasing list C_b (`Theory_work/Wave1/W1-N3/STATEMENT.md:56-57`). ENG adds |C_b| ≤ 31
  and finite read entries (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:29-32`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); paths relative to it.

## Setting
A valid input on the sampler branch of the shipped `v3_fit`, so that `v3_setup` → `cpp_setup` completes
(`v3_fit.R:133-138`; `v3_setup.R:67-77`). EX-A (exact scores and arithmetic). C(X) = (C₁, …, C_J) is the partition of
T2 (BLK); λ(k) := log ϖ(k) = log w(k) − log W_K, the capped BB(1, p) log-prior per model of size k; ρ_b(U) :=
log m(U) − log m(∅) = log r_b(U).

## Lemma ENC
Let `st` be the `Start` object `*g->st` built by `cpp_setup` (`cpp/v3_core.cpp:272-305`). Then:
- **(ENC-a) Fields.** `st.D` points to the run's `Data` D with `D.p = p`, `D.K = K = min(p, ⌊n/2⌋)` and `D.logprior` of
  length K + 1 with `D.logprior[k] = λ(k)`, finite (w(k) > 0); `st.J = J`; `st.blocks[b]` = C_b as an increasing list, for the block order
  of C(X); `st.blk`, `st.pos` are the inverse maps (x = `st.blocks[st.blk[x]][st.pos[x]]` for every column x, and
  `blk[blocks[b][i]] = b`, `pos[blocks[b][i]] = i`); `st.logr[b]` has length 2^{|C_b|}, `st.logr[b][0] = 0` and
  `st.logr[b][code(U)] = ρ_b(U)` for every U ⊆ C_b (all |U| ≤ |C_b| ≤ B ≤ K, so every entry is set and finite);
  `st.logprof[b]` has length min(|C_b|, K) + 1 = |C_b| + 1; `st.codes_by_size[b][j]` lists the size-j codes in increasing
  numeric order; 1 ≤ |C_b| ≤ 16 ≤ 31.
- **(ENC-b) One object, never changed (and its `Data`).** The same object is the one read by `start_mode` in LS0
  (`cpp/v3_core.cpp:392, 469`), by the engines and by the calibration (`cpp/v3_core.cpp:410, 611, 704`); after
  `cpp_setup` returns it is accessed only through `const Start&`. The `Data` it points to is written only by `data_init`
  and afterwards read through `const Data&`/`const Data*`; its only changing fields are the `mutable` counters
  (`cpp/v3_score.h:20-21`), which `start_mode` does not read.
- **(ENC-c) Consequence.** The hypotheses N3 (H1) strengthened of `W3-RM:E4` hold on every run that reaches LS0;
  together with EX-A (E4's (H2)) and (H4), E4 gives that the LS0 centre S̃₀ maximises γ₀ on Ω.

## Not claimed
- (H4) (integer ranges, allocation, recursion depth) — an execution premise, not a code-reading fact.
- Binary64 values of the tables (EX-A); the tables' finiteness in binary64 is ENG's (H2-FP) matter.
- The alternative constructor `cpp_start` (`cpp/v3_core.cpp:204-212`), used only by the inspection helper
  `v3_start` (`v3_setup.R:38`), not by `v3_fit`.

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (code check of E4's (H1) strengthened) | track A T4 | `AUDIT.md` §6 T4 | `CHECK.md` |
| v2 | (ENC-a) finiteness of λ; (ENC-b) the `Data` | STRONGER (two facts added) | LC2 #5, #8 | `reviews/LC2_reply_opus.md` | pending (gate) |
