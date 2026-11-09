<!-- Theory PR template (Theory_work/INFRA/LIFECYCLE.md §9). Non-theory PRs: delete what does not apply. -->
## Ticket
`theory/<TICKET>` — one line: what this PR establishes or changes.

## Statement
- File and lines: `Theory_work/WaveN/<TICKET>/STATEMENT.md:a-b` (version vX.Y, locked on <date>)
- Change vs the card / previous version (narrowed? strengthened? new?): …

## Status (verbatim)
`PROVED-CHECKED` / `PARTIAL` / … — copied from REPORT.md §1, never upgraded.

## Review trail
- statement lock: <file> — <verdict>
- lemma checks: <files> — <verdicts>; falsification numerics: <scripts>
- mid-point: <file> — CONTINUE / REDIRECT / STOP
- sweep: <file> — FATAL/MAJOR/MINOR/EDITORIAL counts, all dispositioned
- citecheck: <CITECHECK.txt> — misses

## Council scores
| reviewer | score | gates | file |
|---|---|---|---|
| Codex gpt-6.1-sol high | | | |
| Claude Opus 5.5 high | | | |

Council pass = PR approval: HQ adds the `council-pass` label and a comment quoting both scores.

## Strength (headline candidates only; LIFECYCLE §4.2)
- assumptions / consumes / conclusion level / rate / scope:
- assumption entry map: <file>; sharpness rows added: …; binding map rows: …
- literature comparison: <file> (lit:PASS?) · necessity attempts: … · better-theorem review: <file>
- relation to existing claims: implies … / supersedes … (dry run attached) / coexists with …

## Registry diff
- `python Theory_work/INFRA/tools/check.py --quiet` → paste the summary line
- rows added / changed (ids, version bumps, states), `events.log` lines, `DECISIONS.md` entries

## Dependencies touched
- uses (id@use): …
- dependents affected (`registry.py rdeps <id>`), propagation run (`propagate.py … --dry-run` report attached?): …
- method pin (`method_commit`, components): …

## Checklist
- [ ] statuses verbatim; nothing upgraded
- [ ] `check.py` has 0 ERROR (or each one explained here)
- [ ] `assemble.py --check` passes (or generated blocks committed)
- [ ] `major-claim` label if the paper's headline statements change (Felipe approves)
