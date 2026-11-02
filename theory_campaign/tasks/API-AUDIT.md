# API-AUDIT: referee-response task R10 (CODE-AUDIT)

Copied verbatim from `theory/F-REFEREE:theory_campaign/F-REFEREE/RESPONSE_PLAN.md` §3, task R10. Run `git fetch origin` and read the branches it names; also read the campaign synthesis `theory/W8-SYNTH:theory_campaign/W8-SYNTH/SYNTHESIS.md` for the current state, and the open PR branch `theory/E-SPINE` (the story is now 'moving off the start is needed', not 'tempering is needed').

### R10. CODE-AUDIT: SR, GUARD, emit_centre, scan-before-limit, IND-T stream reading

**Paper role:** the algorithm's definition (M8, m13). Operations, not theory; reuse W5-LOCKBOOK if it reports.

**Claim to check, in code.** SR (`v3_engine.h::step_gibbs`: both configurations evaluated and offered to the ledger
before the accept draw; no call site disables emission); GUARD (`v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`: no guard
path reads an RNG or changes a setting; a run no guard stops is the R̄ computation); the local search's scan-before-limit
rule (`local_search` lines 369–420); LS0's `emit_centre`; IND-T's sequential stream reading (`run_island_s`). VAL-FP:
one replay in extended precision on 10 fits to measure η, ε of Proposition 2(f).
**Deliverable.** `theory_campaign/CODE-AUDIT/AUDIT.md` with line-referenced findings and the VAL-FP numbers.
