# T4 · Lemma ENC — PROOF v3 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Fix a valid input on the sampler branch with `cpp_setup` completing; assume EX-A.

## (ENC-a) The fields
*Data.* `v3_fit` builds `ctx <- v3_context(pre$X, pre$y, …)` (`v3_fit.R:118`) → `cpp_context` → `data_init`
(`cpp/v3_core.cpp:91-96`), which sets `D.p = p`, `D.K = std::min(p, n / 2)` = min(p, ⌊n/2⌋) (`cpp/v3_score.h:40`) and
`D.logprior` of length K + 1 with `D.logprior[k] = D.logw[k] − D.logWK`, `D.logw[k] = log(1/2) − log C(2p − 1, k)`,
`D.logWK = log Σ_{k≤K} C(p, k) w(k)` (`cpp/v3_score.h:61-70`): this is log ϖ(k) for the capped BB(1, p) prior, i.e. λ(k), finite since
every w(k) > 0 and W_K > 0.
`cpp_setup` takes `D = *g->D` with `g->D = h->D` (`cpp/v3_core.cpp:275-276`) and sets `st.D = &D` (`cpp/v3_core.cpp:277`).

*Blocks.* `st.blocks = make_blocks(D, B)` (`cpp/v3_core.cpp:279`): by T2 (BLK-d), on the executions of the Setting, this is C(X), each block nonempty with
1 ≤ |C_b| ≤ B ≤ min(16, K), and each block is sorted increasingly (`std::sort`, `cpp/v3_blocks.h:141`).

*`build_tables`* (`cpp/v3_start.h:76-98`, called at `cpp/v3_core.cpp:283`): `st.J = st.blocks.size()` = J
(`cpp/v3_start.h:78`); `blk`, `pos` are filled by `blk[blocks[b][i]] = b`, `pos[blocks[b][i]] = i` for every b, i
(`cpp/v3_start.h:79-80`). Since the blocks partition {0, …, p − 1} (BLK-b), every column x is written exactly once, so
`x = blocks[blk[x]][pos[x]]` for every x: the inverse maps. For each block, `logr[b]` gets length 2^{|C_b|} (NaN
initially; `cpp/v3_start.h:85-86`); for each code, U = {blocks[b][i] : bit i of code set} (`cpp/v3_start.h:91`), so
code(U) = Σ_{x∈U} 2^{pos(x)} with pos the position in the increasing list; entries with |U| > K are skipped
(`cpp/v3_start.h:92`) — none here, as |U| ≤ |C_b| ≤ K; otherwise U is scored against the full y and
`logr[b][code] = 0` for code 0 and `o.logm − D.logm0` otherwise (`cpp/v3_start.h:93-95`), i.e. log m(U) − log m(∅) =
ρ_b(U) (`D.logm0` = log m(∅), `cpp/v3_score.h:60`; the scorer's empty-model branch returns `D->logm0`,
`cpp/v3_score.h:231`). Under EX-A every log m(U) is finite, so every entry is set and finite. A `NumericalFailure` in
`build_tables` makes `cpp_setup` return `"numerical_failure"` (`cpp/v3_core.cpp:284-297`) and the fit stops at
`v3_fit.R:134-138`; on a run that continues, all entries were set.

*`build_start`* (`cpp/v3_start.h:101-151`, called at `cpp/v3_core.cpp:300`): with m = |C_b| and top = min(m, K) = m,
`codes_by_size[b]` has top + 1 lists and the loop over code = 0, 1, …, 2^m − 1 in increasing order appends each code to
the list of its popcount (`cpp/v3_start.h:107-112`), so `codes_by_size[b][j]` is the size-j codes in increasing numeric
order; `logprof[b]` has length top + 1 = m + 1 (`cpp/v3_start.h:113`). Bound: m ≤ B ≤ 16 ≤ 31 (BLK-b gives |C_b| ≤ B;
`check_B`, `cpp/v3_core.cpp:146, 274`, bounds B itself).

## (ENC-b) One object, never changed
`cpp_setup` creates `g->st` (`cpp/v3_core.cpp:277`) and wraps `g` in the returned pointer `ptr` (`cpp/v3_core.cpp:305,
314`); `v3_setup` stores it as `setup$ptr` (`v3_setup.R:70, 75`), which is passed to `cpp_cal_new`
(`v3_calib.R:148`) and `cpp_final_run` (`v3_run.R:227`). There it is read as `const Start& st = *h->st`
(`cpp/v3_core.cpp:392`), `Engine(D, *h->st, …)` with member `const Start& st` (`cpp/v3_core.cpp:410, 611`;
`cpp/v3_engine.h:60`), and `const Start& st = *c->h->st` (`cpp/v3_core.cpp:704`). `start_mode` takes `const Start&`
(`cpp/v3_start.h:271`). The only non-const writers of a `Start` are `build_tables`, `build_start` and the constructors at
`cpp/v3_core.cpp:207-212` (inspection helper `cpp_start`, not on the fit path), `cpp/v3_core.cpp:178-181` (a local
`Start` in `cpp_tables`, not on the fit path) and `cpp/v3_core.cpp:277-300`. The `Data`: written only by `data_init`
(`cpp/v3_core.cpp:96`); `cpp_setup` shares it with the context holder (`cpp/v3_core.cpp:275`), and every later use is
through `const Data&` or `const Data*` (e.g. `Start::D`, `cpp/v3_start.h:35`); only the `mutable` counters
(`cpp/v3_score.h:20-21`) change, and `start_mode` reads K, `logprior` and p only. So the
object LS0 reads at `cpp/v3_core.cpp:469` is the one built in (ENC-a), unchanged.

## (ENC-c) Consequence
(ENC-a) lists every field N3 (H1) names (`st.D`, `D->K`, `D->logprior`, `st.J`, `st.blocks`, `st.logr`, `st.logprof`,
`st.codes_by_size`), with the values (H1) requires for the instance (C(X), λ, ρ), and the strengthening (`st.blk`,
`st.pos` inverse maps; `D.p` valid; |C_b| ≤ 31; read entries finite). By (ENC-b) this holds for the object `start_mode`
reads in LS0. E4's remaining hypotheses are (H2) = EX-A and (H4). ∎
