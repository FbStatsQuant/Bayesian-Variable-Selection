# Lemma PC — completed runs carry the potential island records

Status: PROVED-CHECKED (lemma checks LC1/LC2 Codex Sol; mid-point MP1 CONTINUE; sweep SW1 fixed; council C1 PASSED round 1 (gpt-6-astra 9.1, Claude Opus 5.5 8.8; all six gates PASS on both seats); C1 non-blocking edits applied). Text history: v1, 2026-11-09. Statement: STATEMENT.md v3 §2 "Lemma PC". Code paths relative to
`Scripts/SMC_BVS/core/`. This is the limited comparison SL1 item 4 asked for, not the full GUARD-W audit.

## Proof

Fix the data, a calibration value on 𝒜 and the final streams; assume EX-A.

(i) *Islands.* The only early return inside an island is the guard check after each bridge stage
(`cpp/v3_engine.h:335-338`), which sets `res.partial = true`. In `cpp_final_run`, a partial island sets
`status = "resource_limit"` and breaks the island loop (`cpp/v3_core.cpp:451`); later guard checks (final local search
`:459`, LS0 `:480`) and any `NumericalFailure` (`:483`) also leave `status != "completed"`; nothing resets `status` to
"completed". Hence on {completed} no island returned early: each island executed the whole of `run_island_s` (bridge
`:303-339`, burn-in `:343-347`, measured `:351-360`). Under EX-A, the island's statistical record is a function of
(c, island stream) only — the guard, clock, cache and ledger do not feed any transition, weight or evidence increment
(W1-N1 Lemma B step (B-0), `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md`, valid on main by the CC header). The guard only
decides *whether* to stop, and on {completed} it never stopped. So the record equals the potential (uninterrupted) record
computed from the same stream; the same holds for the set 𝓜_r of models island r evaluated (incl. rejected proposals),
which is a function of (c, island stream) through the augmented record of `D_theorem.md` §1 (C1 Opus #1).

(ii) *Reported fields.* On {completed}, `v3_assemble_final` skips the incomplete branch (`v3_run.R:143`) and sets
`log_Z_r`, `log_Z` (`:150-154`), `pip_r`, `pip_primary`, `mpm` (`:159-163`) from the island results, which are the
fields `logZ`, `pip` of (i) (`cpp/v3_engine.h:362-365`); these are the functions of §0 of the island records. `out$hpm` is the ledger's running best (`v3_run.R:142`); it is
**not** a function of the island records alone (the records exclude rejected proposals, tables, inherited models, the final
local search and LS0) — see (iii) (SW1 #1).

(iii) *Ledger.* Every model evaluated by island r goes through `eval` with `emit = true` (CC1–CC2), so it is offered to
the HPM at its first evaluation in the run; the ledger lives for the whole final run (`cpp/v3_core.cpp:407`) and is never
reset. So 𝓜 ⊇ ∪_r 𝓜_r (𝓜 also contains tables, inherited models, final-search and LS0 evaluations), 𝓜 ⊆ Ω (CC5), and by CC2
Ŝ = the hpm_better-maximum of 𝓜. ∎

Consequence used downstream: for any event G about the potential island records (evidence, PIPs, MPM, particle states), {completed} ∩ G is the same as {completed} ∩
G evaluated on the reported fields; so P(completed ∩ {reported error}) ≤ P(𝒜 ∩ {potential error}).
