# L2 — Lemma LIST-CODE (code reading at the pin) — proof

Claim: STATEMENT.md (C2), §3. Status: code reading by the lead, not yet line-checked.
**Code of record:** `Scripts/SMC_BVS/core/` at 4676af6 = the core on main 029bb748 (`git diff 4676af6 029bb748 --
Scripts/SMC_BVS/core` is empty; last change 72785fe). Paths below are relative to `Scripts/SMC_BVS/core/`; line
numbers are those of this worktree (branch theory/W3-D5P). Premises: EX-A (every score is computed exactly), EX-S, SR,
the shipped configuration (`ls0 = TRUE`, `v3.ls0_cap` unset ⇒ `"ell_n_plus_mode"`, `ls0_tie_dp = TRUE`, `ls0_ell` =
`b$ell` = ℓ_n; `v3_run.R:88-103`). Consumed: W3-SAMP:CC@1.1.2 "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)"
(`Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md`, CC2 :40-63, CC5).

Notation. "The final run" is the call `cpp_final_run` (`cpp/v3_core.cpp:391-518`) made by `v3_final_run`
(`v3_run.R:223-229`) from `v3_fit` (`v3_fit.R:162`). Its ledger `led` and cache `cache` are local objects created at
`cpp/v3_core.cpp:407` and `:409` (empty: `Ledger` constructor `cpp/v3_ledger.h:76-80`; `ScoreCache::init`
`cpp/v3_score.h:264-270`). 𝓜^run := the set of models S for which `led.offer_stores(S, …)` is called during the final
run (`cpp/v3_ledger.h:89-94`). "Sampler branch" := `fit$branch_run == "smc"` (`v3_fit.R:106`).

## Step A — the only writers of the HPM and of the top store, and the offered set
A1. `led.hpmS` is assigned only in `Ledger::offer_hpm` (`cpp/v3_ledger.h:84-88`; no other assignment to `hpmS` in
`cpp/`), and it replaces the current value iff `hpm_better(F, S, hpmF, hpmS)` (`:85`). `offer_hpm` is called at
`cpp/v3_ledger.h:90` (inside `offer_stores`) and at `cpp/v3_core.cpp:502`, which is inside the
`catch (NumericalFailure&)` handler (`:483-508`) [LC1-8], entered only after `status = "numerical_failure"` (`:484`).
A2. `led.top.offer` is called only at `cpp/v3_ledger.h:91`, inside `offer_stores`, immediately after `offer_hpm(S, F, …)`
with the same (S, F). (The store at `cpp/v3_core.cpp:549` is the enumeration's own `top`, Step E.)
A3. `offer_stores` is called from `Ledger::event` when `is_fresh` (`cpp/v3_ledger.h:112`) and directly for inherited
models (`cpp/v3_core.cpp:427`). Hence, on every final run whose status stays "completed", the sequence of HPM offers
equals the sequence of top-store offers, and both are the sequence of calls of `offer_stores`; the set of offered
models is 𝓜^run.
A4. 𝓜^run ⊆ Ω (CC5; directly: tables only |U| ≤ K, `cpp/v3_start.h:91-93` and NaN entries skipped
`cpp/v3_core.cpp:379`; inherited models checked `:425`; engine moves keep |S| ≤ K, CC5), and ∅ ∈ 𝓜^run (block-table code
0, `cpp/v3_core.cpp:376-384`), so 𝓜^run is nonempty.
A5. Every offered value is F(S): tables F = `D.logprior[|U|]` + `logm_tab` (`cpp/v3_core.cpp:382`) with `logm_tab` = the scorer's log m(U)
(`cpp/v3_start.h:93`); inherited F = `D.logprior[|S|]` + `sc.score(S).logm` (`cpp/v3_core.cpp:426-427`); `eval` F = `D.logprior[k]` + lm
with lm the scorer's or the cached scorer's value (`cpp/v3_engine.h:89-101`). `D.logprior[k]` = log ϖ(k), the size prior
normalised on Ω (`cpp/v3_score.h:60-70`). Under EX-A each is exactly F(S) = log ϖ(|S|) + log m(S) (CC2 :46-47). In
particular the value of an offer is a function of the model.

## Step B — (i) Link 1: completed ⇔ output, and LS0 ran on the final run's ledger
B1. *Status and estimates.* On the sampler branch, `v3_fit` returns at `v3_fit.R:117` (status `resource_limit`), `:137`
(`numerical_failure`), `:159` (`cal$status` ≠ "ok") with `estimates_available` FALSE (initial value `:78`; `finish`
`:79-87` sets it only through `v3_unavailable_estimates`, which sets FALSE, `v3_run.R:110-114`), or after the final run
at `v3_fit.R:173`, where every field of `fr` is copied into `fit` (`v3_fit.R:171`), including `status` (`v3_run.R:121`) and
`estimates_available`. In `v3_assemble_final`, if `raw$status != "completed"` the function returns with
`estimates_available` FALSE (`v3_run.R:143-149`); otherwise it reaches `:218` and sets it TRUE. `finish` changes
neither field when `estimates_available` is TRUE (`v3_fit.R:84` concerns `resource_limit` only; `:85` requires FALSE). An
R-level error (`stop`, including C++ `Rcpp::stop`, e.g. `cpp/v3_core.cpp:474`) returns no fit object at all. Hence on
the sampler branch: `fit$status == "completed"` ⇔ `fit$estimates_available` is TRUE. The output event 𝒪 is "the coded
fit returns with `estimates_available = TRUE`" (DLV-0, `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:144-147`).
B2. *LS0 ran.* `status` is initialised to "completed" (`cpp/v3_core.cpp:413`) and changed only to "resource_limit"
(`:451`, `:459`, `:480`) or "numerical_failure" (`:484`); it is never reset to "completed". If it is "completed" at the
end, then: the island loop ran all `o.islands` islands (`:443-452`; `o.islands` is read from `ro` at `:396` and is 4 at `v3_run.R:91`; the argument uses no property of this number) [LC1-10]; the block `cpp/v3_core.cpp:453-482` ran; in it the guard check after the
final local search did not fire (`:459`), so the condition at `:465` (`o.ls0`, TRUE by `v3_run.R:94` and
`cpp/v3_core.cpp:400`) held and LS0 ran: `start_mode(st, 1000000, o.ls0_tie_dp)` (`:469`) and
`E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0)` (`:476`) returned (no exception: a `NumericalFailure` would
have set `numerical_failure`; any other exception aborts the fit, B1). `E.cache` = `&cache`, `E.led` = `&led` (`:411`).
B3. *Every model LS0 evaluates is in 𝓜^run.* `local_search` (`cpp/v3_engine.h:379-419`) evaluates the centre by
`eval(C, ME_LOCAL, emit_centre)` with `emit_centre = true` for LS0 (`cpp/v3_engine.h:382`, `cpp/v3_core.cpp:476`) and every scanned
neighbour by `eval(q, ME_LOCAL)` (`emit = true`, `cpp/v3_engine.h:391`). In `eval` (`:89-101`): on a cache miss the
scorer runs, `fresh = true`, the result is inserted in the cache (`:91-94`), and `led->event(…, fresh || !cache, …)`
(`:99`) calls `offer_stores` (`cpp/v3_ledger.h:112`), so S ∈ 𝓜^run. On a cache hit, the entry was inserted by an earlier
`eval` of the same model in this final run (the cache is created empty at `cpp/v3_core.cpp:409`, and `insert` is called
only at `cpp/v3_engine.h:93`; `find` matches the model exactly, `cpp/v3_score.h:274-282` with `same` at `:271-273`) [LC1-8]. That earlier `eval` either had
`emit = true` and was fresh, so it offered S, or had `emit = false`. The only `emit = false` call in the final run is the
centre of the final local search, `E.local_search(led.hpmS, o.ell, o.tier, false)` (`cpp/v3_core.cpp:456`), whose centre
is `led.hpmS`, a model already passed to `offer_hpm`, hence (A1, A3: before any numerical failure) already in 𝓜^run.
(A cache clear, `cpp/v3_score.h:284`, only causes a later miss and a repeated, idempotent offer.) Hence every model LS0
evaluates is in 𝓜^run. (This is CC2 (a), `CC_code_check.md:48-53`, specialised to LS0.)
B4. *LS0 in the run is the search of 𝒦_n.* The control flow of `local_search` reads only the centre, the move cap, p, K
(`cpp/v3_engine.h:384`), and the models and values F produced by `eval` (`:387-418`: scan order flips j = 0..p−1 then
swaps in ascending order; best by larger F then `lex_less`; strict-improvement rule `:408`; cap rule `:409-411`). The
event context `ev` (`:381, :386, :390`) [LC1-8] is bookkeeping and is not read by the control flow. `eval` returns
F = `D.logprior[k]` + lm, where lm is either a fresh scorer value or a cached scorer value of the same model; under
EX-A both are log m(S) exactly (A5). The centre is `m.S` = `start_mode(st, 1000000, TRUE).S` (`cpp/v3_core.cpp:469`), a
function of the data through the start tables `st` (setup, no uniforms), and the cap is ℓ_n + |m.S| (`:473`, with
`o.ls0_ell` = ℓ_n). Hence the sequence of models LS0 evaluates, and its termination, are functions of the data alone and
coincide with the deterministic LS0 of the definition of 𝒦_n (RM `STATEMENT.md:52-53`: complete scans, cap ℓ_n + |S̃₀|,
started from the coded start mode; configuration RM `STATEMENT.md:59-67`), whose scan order, tie rule and stop rules are
those fixed by the code pins W3-RM2 `STATEMENT.md:60-67` (imported by RM2R `STATEMENT.md:39-41`): centre and cap
`cpp/v3_core.cpp:465-476`, scan `cpp/v3_engine.h:394-406`, ties `:392`, strict improvement `:408`, stops `:409-414` —
the very lines read above [LC1-4]. (W3-RM:E4 is context only: 𝒦_n is defined from the coded start mode itself.) In particular, on 𝒦_n (that search scores S₀), S₀ is evaluated by LS0 in every completed run, so S₀ ∈ 𝓜^run
by B3. ∎(i)

## Step C — (ii) Link 2: `hpm` = Ŝ⁺
On a completed run, `fit$hpm` = `out$hpm` = `led$hpm$model` (`v3_run.R:141-142`, copied at `v3_fit.R:171`) =
`to_orig(D, L.hpmS)` (`cpp/v3_core.cpp:364`, via `ledger_to_list` at `:510`). By A1 and A3, `led.hpmS` is the running
hpm_better-maximum over the sequence of `offer_stores` calls, i.e. the hpm_better-maximum of 𝓜^run (`hpm_better` is a
strict total order on distinct models with values given by A5: larger F, then smaller size, then lexicographic,
`cpp/v3_util.h:121-126`; a running maximum under a strict total order is the maximum of the offered set). This is
CC2's conclusion "Ŝ = the hpm_better-maximum of 𝓜" (`CC_code_check.md:60-63`). RM and RM2R define Ŝ⁺ as the reported
model (RM `STATEMENT.md:54`), and RM-0's pathwise step uses exactly this description: "the reported HPM Ŝ⁺ — the
≻-maximum of the scored set" (C-DLV `lemmas/L4_delivery.md:66-70`), with ≻ the HPM order and the scored set the set
of models that joined the final run's all-scored set. That set is 𝓜^run [LC1-11]: every score event of the final run
that is an `eval` or `held` event is offered or is a re-visit of an offered model (CC2 (a)–(b), `CC_code_check.md:48-54`),
tables and inherited models are offered directly (CC2 "Other offers", `CC_code_check.md:55-57`); conversely every
offered model was scored (tables `cpp/v3_start.h:93`, inherited `cpp/v3_core.cpp:426`, evaluations `cpp/v3_engine.h:92`). So `fit$hpm` = Ŝ⁺, written in original
indices. 𝓜^run ⊆ Ω by A4. ∎(ii)

## Step D — (iii) The returned list
D1. *What is returned.* `fit$top_store` = `out$top_store` = `led$top` (`v3_run.R:210`, `v3_fit.R:171`) =
`store_to_list(L.top, D)` (`cpp/v3_core.cpp:366`): `models[i]` = `to_orig(D, e.S)` and `value[i]` = `e.v` for the entries e
of the set `L.top.s` in its order (`:358-362`), `capacity` = `L.top.cap` = 40p + 1 (`cpp/v3_ledger.h:78`, p = `D.p` =
p_ret, `cpp/v3_score.h:40`). `to_orig` maps internal indices to `D.orig` (`cpp/v3_core.cpp:38-42`), the retained original
indices `pre$kept` (`v3_fit.R:118`), which are also the names of `pip_primary` (`v3_run.R:160-162`, `setup$ctx$orig`).
D2. *TopStore invariant.* `TopStore` (`cpp/v3_ledger.h:43-57`) holds a `std::set` ordered by `TopCmp` with
`hpm_order = true` (`:46-47`, `:78`): e before e′ iff e.v > e′.v, or e.v = e′.v and |e.S| < |e′.S|, or equal values and
sizes and `lex_less(e.S, e′.S)` (`:37-41`). This is a strict total order on pairs (v, S), and it ranks entries exactly as
`hpm_better` ranks (F, S) (`cpp/v3_util.h:121-126`). By A5 the value is a function of the model, and every model vector offered is in sorted (canonical) form [LC1-9a]:
`to_internal` sorts (`cpp/v3_core.cpp:34`), blocks are sorted (`cpp/v3_blocks.h:141`, so table models are), `start_mode`
sorts (`cpp/v3_start.h:287`), moves use `sorted_insert`/`sorted_erase` (`cpp/v3_util.h:129-130`), and the enumeration
appends increasing j. Hence two entries are equivalent iff they carry the same model: the set holds distinct models. `offer(v, S)` (`:49-57`): (1) returns if cap = 0
(not the case: cap = 40p + 1 ≥ 41, since p = p_ret ≥ 1 on both branches — a fit with no retained column returns
`no_predictors` before branching, `v3_fit.R:99-102` [LC1-9b]); (2) rejects e = (v, S) if the set is full and e is not strictly before the last
element; (3) returns if e is already present; (4) otherwise inserts e and, if the size then exceeds cap, erases the last
element. *Invariant:* after every offer, the set contains only offered entries, has size ≤ cap, and contains the
TopCmp-first entry e* among all entries offered so far. Induction on the offers. Initially the set is empty and nothing
has been offered. *First offer* [LC1-9c]: the set is empty, so (2) and (3) do not apply; e is inserted, no erasure
(1 ≤ cap), and e = e*. *Later offer* e (e* exists). If e is not strictly before the current e*, then e* stays first; in cases (2) and (3) the set
is unchanged; in case (4) the only erased element is the last one of a set of size cap + 1 ≥ 42 ≥ 2, which is not its
first element, and e* is first (it precedes every element of the set, all of which were offered); so e* stays. If e is
strictly before e*, then e is strictly before every element of the set (e* precedes or equals each of them), in
particular before the last, so (2) does not reject; e is not present (it is strictly before every element), so (3) does
not return; e is inserted as the first element and, the set having size ≥ 2 if an erasure happens, it is not the erased
last element. In all cases the set holds the new e* and only offered entries, with size ≤ cap. ∎(invariant)
D3. *Conclusion.* By A2–A3 the offers to `led.top` on a completed run are exactly the pairs (F(S), S), S ∈ 𝓜^run; by
D2, 𝒯 (the models of `top_store`) consists of distinct elements of 𝓜^run, |𝒯| ≤ 40p + 1, each returned with value F(S)
(A5), in original indices (D1), and 𝒯 contains the TopCmp-first offered entry, which is the hpm_better-maximum of
𝓜^run (same order, D2). ∎(iii)

## Step E — (iv) Exact branch
On the exact branch `v3_fit` calls `v3_enumerate(ctx)` (`v3_fit.R:121`) = `cpp_enumerate` (`v3_exact.R:7`;
`cpp/v3_core.cpp:524-568`). The recursion `rec` (`:537-555`) [LC1-8] starts from S = ∅ (`rec(0)`, `:556`) and, from a sorted S
with |S| < K, calls itself on S ∪ {j} for every j greater than the last element of S (`:553-554`); it therefore visits
every subset of [p] of size ≤ K exactly once, i.e. every S ∈ Ω (Ω = {|S| ≤ K}, K = `D.K` = min(p, ⌊n/2⌋),
`cpp/v3_score.h:40`). At each visit it computes F = `D.logprior[|S|]` + logm (`cpp/v3_core.cpp:539`) [LC1-8] and offers (F, S) to its own
`TopStore top` with cap 40p + 1 (`:531`, `:549`). If no `NumericalFailure` occurs, status is "exact" (`:536`, `:556`).
Then: `pip[j]` = numer[j]/total (`:559`) where, by the rescaled streaming log-sum-exp (`:542-547`; each rescale
multiplies numer and total by the same factor), numer[j]/total = Σ_{S∋j} e^{F(S)}/Σ_S e^{F(S)} = PIP_j under EX-A;
`log_Z` = mx + log(total) = log Z (`:557`); `v3_enumerate` names `pip` by `ctx$orig` and sets `mpm` = the retained
columns with pip > 0.5 (`v3_exact.R:8-13`), i.e. MPM; `hpm` is the running hpm_better-maximum over all S ∈ Ω (`cpp/v3_core.cpp:548`).
`v3_fit` copies `fit$pip_primary` = `e$pip`, `fit$mpm` = `e$mpm`, `fit$hpm` = `e$hpm`, and `fit$exact` = `e` (which
contains `top` = `store_to_list(top, D)`, `:565`) (`v3_fit.R:122-127`). By the invariant D2 (same `TopStore` code), 𝒯^ex
(the models of `fit$exact$top`) consists of distinct models of Ω with values F(S) (EX-A) and contains the
hpm_better-maximum of Ω. ∎(iv)

## Step F — (v)
Assume F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}. *Sampler branch, completed run with S₀ ∈ 𝓜^run.* Since 𝓜^run ⊆ Ω (A4) and
`hpm_better` ranks by F first, S₀ is the hpm_better-maximum of 𝓜^run; by (ii) `hpm` = S₀ and by (iii) S₀ ∈ 𝒯.
*Exact branch.* S₀ ∈ Ω (the hypothesis presumes it) is the hpm_better-maximum of Ω; by (iv) `hpm` = S₀ and S₀ ∈ 𝒯^ex. ∎(v)

## Remarks for the checker
- The new code facts relative to CC2 are A2 (the top store receives exactly the HPM's offers), D2 (the store never loses
  its first entry) and B4 (LS0 at code level equals 𝒦_n's search). B1–B3 and C restate CC2 with line references.
- The end-to-end run `numerics/e2e_small.R` (27 small cases through this core) is consistent with (i)–(v): S₀ ∈
  `top_store` and `hpm` = S₀ whenever S₀ was the posterior mode (`numerics/e2e_small_out.txt`). It is falsification only.
