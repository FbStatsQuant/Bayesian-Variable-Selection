# INFRA — research infrastructure for the SMC-BVS theory program

The theory program run like a software project: every result is a versioned registry entry with use-level
dependencies, statuses are checked against the files continuously, and results can be rolled back (when wrong) or
superseded (when a better theorem is found), with consequences propagated mechanically.

| file | purpose |
|---|---|
| `LIFECYCLE.md` | **the protocol**: who decides what, states, correctness rollbacks (PATCH / DOWNGRADE / NARROW / RETRACT / DEPRECATE) with git steps, the correctness and strength (sharpness) gates, candidates, supersession / coexistence decision rule, freeze, method pinning, GitHub workflow |
| `FAILED_ROUTES.md` | routes that did not work and obstructions (Prop SHARP, Lemma VN/STAR, Theorem NEG, (C6), C-GROW, OBS-k, SoP RF items) |
| `DECISIONS.md` | decision log (supersede / coexist / decline / remark / retract / narrow / failed sharpening attempts) |
| `registry/claims.tsv` | one row per claim (Wave 1, 1C, 2 + State-of-Project anchors `SOP:*`) |
| `registry/tickets.tsv`, `aliases.tsv` | tickets (verbatim results); alias → id for external names (T03♯ → SOP:TH09, …) |
| `registry/assumptions.tsv`, `sharpness.tsv`, `binding.tsv` | strength layer: assumptions/properties with bridges, necessity evidence, binding map |
| `registry/repoints.tsv`, `method_components.tsv`, `config.tsv`, `events.log` | proposed re-points, method pin components, freeze/caps, audit trail |
| `registry/fragments/` | seed transcriptions (helper output) and their briefs; not used after seeding |
| `tools/check.py` | registry ↔ repository consistency audit (tombstones checked at their archive tag); `--acceptance ID…` = HQ's blocking CP3 gate (consumed claims ACTIVE, evidence files exist, council record bound to a manifest digest, strength gates, better-proposal dispositions, assurance and conditional statuses); `--consumed-vs REF --tickets T` = consumed claims vs main |
| `tools/propagate.py` | lifecycle operations + propagation + repair issues (dry run by default prices a change; `--apply` writes); `rollback-ticket T --archive TAG --merge M` = the registry part of reverting a merged ticket, validated on the post-revert tree (LIFECYCLE §3) |
| `tools/registry.py` | show / deps / rdeps / add / set / rehash / compare / sets / assumption-impact / stats / dot |
| `tools/assemble.py` | generates the paper's theorem blocks and provenance / dependency / strength tables from the registry |
| `tools/ingest.py` | add a new ticket's claims (fragment JSONL, or a Wave 3 REPORT.md read directly: `convert` shows the JSONL) or split bundled claims into parts; full schema, unknown fields rejected, all-or-nothing (exit 1 on any problem); dry run by default, `--staged` checks the result (acceptance included) on a copy, `--apply` writes |
| `tools/bvsreg.py` | shared library; `bvsreg.py recover` undoes a multi-file write whose own restore failed (`registry/.TXN_FAILED`; every tool refuses to run while it exists) |
| `tools/build_registry.py` | one-off seeding from fragments (refuses to overwrite a live registry) |
| `ci/run_ci.py`, `ci/README.md`, `ci/falsification.tsv` | continuous audit and how HQ schedules it |
| `templates/ASSUMPTION_MAP.md` | one-page map each ticket writes before heavy proving |
| `../../.github/` | PR template and issue templates |

Start with `python Theory_work/INFRA/tools/check.py --quiet` and `python Theory_work/INFRA/tools/registry.py stats`.
