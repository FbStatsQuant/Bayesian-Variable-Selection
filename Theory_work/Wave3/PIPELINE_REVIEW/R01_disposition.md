# R01 disposition (Astra, NOT-READY 3/10). HQ, 2026-11-11

All 11 findings accepted. Fixes (PROTOCOL.md = Wave3 resume rules 9–16):

| # | sev | fix |
|---|---|---|
| R01 | CRITICAL | Rule 15: `tools/manifest.py` freeze/verify; reviewers quote the digest; no edits during a round; post-round diffs get a fresh review (substantive) or a Sol-attested diff (editorial). Tested: a LOG edit is ignored, a STATEMENT edit is caught. |
| R02 | CRITICAL | Tool fix (INFRA tool-fix agent): tombstones plus an executable rollback sequence (`rollback-ticket`) in LIFECYCLE §3. Interim rule 16: no `--apply` on claims from merged tickets. |
| R03 | CRITICAL | Tool fix: ingest round-trips consumes, method pins and binding rows, and rejects unknown fields. Interim: explicit `depends_on` edges, and the registry catch-up agent records unstored bindings in `fragments/PENDING_BINDINGS_2026-11-11.md`. |
| R04 | MAJOR | Tool fix: all-or-nothing ingest, nonzero exit, staged check on a registry copy, converter from the REPORT block. Rule 10 CP3-PASS uses the staged check. Interim rule 16: no CP3 ingest or merge. |
| R05 | MAJOR | Rule 10 "Headline strength"; tool `check.py --acceptance`; CP1 dispositions for each better-theorem proposal; the better-theorem review is repeated if the statement changed materially. |
| R06 | MAJOR | Rule 11: a premise below PROVED-CHECKED must be an explicit hypothesis, carried into the status; tool `--acceptance` enforces it. |
| R07 | MAJOR | Rule 11: consumed-claim state checked against current main before each continuation and merge; HQ notifies consumers and the acknowledgement is logged; CP3 runs on the proposed merged tree. |
| R08 | MAJOR | Rule 15: scored reviews are blind first reads; earlier findings go to a separate reconciliation reviewer. |
| R09 | MAJOR | Rule 10 (compute): CP0 representative smoke manifest; nothing more queued before CP1; batch release under a 1,400 core-hour aggregate ceiling; invariant failures distinguished from resource-limit outcomes. |
| R10 | MAJOR | Rule 10: CP3-PASS vs CP3-EXHAUSTED; no council-pass or PROVED-CHECKED without a manifest-matched dual pass. |
| R11 | MAJOR | Rule 12: separate watchdog task (not bound to HQ); schedule IDs recorded before launch; proof work stops at checkpoints when HQ is absent; P6 ceiling enforced by the lead. Rule 14: review-layer waivers need Felipe. |

Next: a round-2 check after the tool fixes land. Per rule 15 it has two parts: a blind fresh review (no access to this file or to R01), and a separate reconciliation reviewer working per finding.
