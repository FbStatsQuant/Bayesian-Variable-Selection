# W3-EDIT — the editorial pass (Theory Department, 2026-11-15; recording path approved by HQ)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. Editorial only (v4 §0.1: nothing here changes a hypothesis,
a conclusion or a proof step). Worktree `/home/fb31/BVS-wt/W3-EDIT`, branch `theory/W3-EDIT`, ledger folder
`Theory_work/Wave3/W3-EDIT/`. Read `RIDER_RULES.md` §4, §6 (agents, stops) and PROTOCOL_v4 §5.3 (E findings).

## Why this ticket edits other folders
Rider rule 1 (parents read-only) is lifted for the files listed below, **for wording-only changes recorded in the
ledger**. Never edit a `CHECKPOINT_<k>.md` that is a registry status source (check.py C12), never a council manifest
of a ticket not yet accepted, never W3-DIST / W3-READER / Docs / Lean.

## Items (sources)
1. API audit MINORs: pass 1 (21; `API_AUDIT/pass1/TRIAGE.md` "MINOR" + pass1b), pass 2 (13; `pass2/TRIAGE.md`),
   pass 3 (5; `pass3/TRIAGE.md`). Each verdict's text is in `<pass>/results/f*.md`.
2. C-DLV:Prop-F wording: `Wave1C/C-DLV/lemmas/L4_delivery.md:83-84` → Sol's minimal restatement
   (`API_AUDIT/pass1/R-AUD1_sol.md`).
3. W3-PSHARP E1–E9 (`W3-PSHARP/reviews/R2_disposition.md`).
4. W3-MISR errata (council/sweep dispositions in `W3-MISR/reviews/`, `CHECKPOINT_3.md`) + `ASSUMPTION_MAP.md:27`
   cross-cite to PSHARP (sharp2 triage).
5. W3-START2 errata E1–E8 (`W3-START2/CHECKPOINT_2.md` §3) + the LEAK-0 "sharpens" wording at `STATEMENT.md:87-88`
   (sharp2 triage §0).
6. Citation fixes: C-MIS citecheck (6 line-drifted cites into SoP `04_theory.tex`, CI 11-13); `W2-FAC-X/reviews/
   citecheck.py` path prefixes miss W2-FAC-A/B REPORT cites → script fix + refresh `CITECHECK.txt`. These unblock
   PR #10 (Actions CI).

## Method
1. `LEDGER.tsv`: one row per item — `id | claim | file:line | finding (source) | class | before | after | route`.
   class = WORDING / CITATION / TYPO / NOT-EDITORIAL. route = IN-PLACE (patch bump) or CHAPTER-ONLY (fixed in the
   chapter transcription; the frozen file stays). Any item that touches a hypothesis, conclusion or proof step is
   NOT-EDITORIAL: do not apply it, list it for the manager.
2. Apply IN-PLACE rows in the worktree. Run every affected ticket's citecheck, `check.py --quiet` (expect hash
   changes on the affected rows only: list them).
3. One Sol review, "editorial only" diff check (v4 §5.3): the full diff + LEDGER; does any edit change mathematics?
4. `CHECKPOINT_1.md` (= final): ledger summary, Sol verdict, the list of registry rows needing `registry.py rehash`
   (patch bump) for the HQ recorder, the CHAPTER-ONLY list for the Writing Department. End your run.

## Recording path (HQ, 2026-11-15)
You never run `registry.py rehash`, `--record` or any write to `claims.tsv`. HQ merges `theory/W3-EDIT` and its recorder
rehashes the listed rows (patch bump, LIFECYCLE §1 "patch = editorial"). To make that a mechanical step, CHECKPOINT_1
gives a table `claim id | file | old sha256 (from claims.tsv) | lines touched | ledger rows`, and a dry run of
`check.py --quiet` on your branch showing that the only new findings are hash mismatches on exactly those rows.
The citation fixes in item 6 unblock PR #10: put them first and say when they are done (the manager tells HQ).

Budget ~4–6 Opus hours; 1 helper allowed (Sonnet 5.5 for citecheck bookkeeping).
