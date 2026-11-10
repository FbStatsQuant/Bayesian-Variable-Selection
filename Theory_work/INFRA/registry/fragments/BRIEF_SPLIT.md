# Split-curation brief (helpers)

Some registry rows bundle several distinct results; downstream proofs use the parts separately. HQ decision
(2026-11-10): split them now, from the ticket files. You transcribe; no mathematics. Work only in
`C:\Users\felip\BVS-infra` (read-only except your output file). No git commands, no subagents. Use grep and targeted
`sed -n`. Inspect a row with `python Theory_work/INFRA/tools/registry.py show <id>` and its users with
`python Theory_work/INFRA/tools/registry.py rdeps <id>`.

For each PARENT id assigned to you:
1. Identify the parts (sub-lemmas, clauses, classes) exactly as the source labels them, and for each part the
   statement span (label line through last statement line, no proof), premise spans (setting/definitions it relies
   on, `path:a-b`), kind, and the proof uses (use-level edges `id@stmt` / `id@proof:<fact>`).
2. Status per part: if the ticket states THIS part's own status somewhere, copy it verbatim and give the
   `path:line` where it STARTS. If not, the status is exactly `UNSPLIT-STATUS: <parent status verbatim>` and the
   status_source is the parent's status_source — never invent or upgrade.
3. Re-points: for each existing dependent of the parent (rdeps), say which part it actually uses (read the citing
   line), so its edge can move from the parent to that part. Only when the citing text names the part.

## Output: `Theory_work/INFRA/registry/fragments/splits/<BATCH>.tsv`
Tab-separated, header `kind_of_row	parent	id	field	value	evidence`. Rows:
- `part` rows: one per (part, field) with fields `local_id`, `kind`, `name`, `file`, `lines`, `premises`, `status`,
  `status_source`, `depends_on`, `notes` (id = `<TICKET>:<parent local_id>.<part>` e.g. `W2-FAC-A:L1.U(a)`).
- `repoint` rows: id = the dependent; field `edge`; value `<old item> => <new item>` (e.g.
  `W2-FAC-A:L1@stmt => W2-FAC-A:L1.U(d)@stmt`); evidence = citing `path:line`.
Print every new span to confirm it before writing. Final message ≤ 10 lines: parts per parent, how many got their
own status, re-points.
