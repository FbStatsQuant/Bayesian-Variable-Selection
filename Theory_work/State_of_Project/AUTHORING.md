# AUTHORING RULES — State of the Project (read fully before writing anything)

This document is the **ground truth handed to an agentic theory loop** (agents + a review council) that will
iterate on it to produce theoretical results. It is also read by Felipe Bedoya (project lead). Optimise for an agent
that has *only this document* and must (a) know exactly where the project stands, (b) find any detail fast, and
(c) never repeat a failed route or overstate a result.

Everything lives in `Theory_work/State_of_Project/` of the repo `FbStatsQuant/Bayesian-Variable-Selection`.
Repo root on this PC: `C:\Users\felip\Bayesian-Variable-Selection`. Sources are frozen at commit **21ebc28**.

## 0. Hard rules (a violation fails review)

1. **No new mathematics.** Do not prove, extend, sharpen or "fix" anything. Report what the sources say.
2. **Formal statements are transcribed, not paraphrased.** Put each one in a `stmt` box with its source span.
   Only LaTeX formatting may change (Unicode → LaTeX math, line breaks). Every symbol, hypothesis, quantifier,
   constant, rate and exponent must survive. If a source statement is too long, transcribe it in full anyway.
   If you must abridge, write `[…]` at the cut and say so in the box; never silently drop a hypothesis.
3. **Status words are copied verbatim** inside `\status{...}`, e.g.
   `\status{PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))}`. Never upgrade or soften
   (a PROOF SKETCH is not "proved"; "SF only" is not "cross-checked"; "candidate" stays "candidate").
4. **Every claim-bearing sentence or table row cites its source** with `\src{path:line}` (or `\src{path:a-b}`,
   `\src{path §x}`) and/or `\pos{N}` (position in the source-thread transcript). Line numbers refer to the file at
   commit 21ebc28. Verify each line number you cite by reading the file.
5. **Conflicting sources** → an `uncertain` box quoting both sides with sources. Do not pick a winner unless a
   source explicitly resolves it (then cite that resolution).
6. **Plain-language readings are allowed and wanted** (`plain` box), but they may not claim more than the
   statement: keep the regime (any X / LH / W / LH-iid / study design), the asymptotic vs finite-n nature, and
   the "jointly with output" qualifiers.
7. **Say what is NOT proved** for every result (`notproved` box) when the sources record limits, gaps or scope.
8. **The theorem list is approved.** On 2026-11-07 Felipe approved the paper-1 theorem list (M1–M8 = TH01–TH08,
   supplement cards TH09–TH20) as the current targets. Write `\approvedFB` where approval is relevant. This does
   not change any proof status. Future demotions/reformulations/additions are outputs of the theory loop.
9. **Do not run git** (no add/commit/push/checkout/stash). Do not edit files outside the paths you are assigned.
   Do not modify any source file. Do not read `review/` (it holds the evaluation key).

## 1. Where things are (paths for `\src`)

- `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/` — the archive of the theory campaign thread
  ("New BVS Headquarters", 2026-11-02→04). Start with `NBH/START_HERE.md`, `NBH/README.md`.
  - `NBH/02_theory.md` final state (verbatim cards, IDs); `NBH/ID_REGISTRY.md` every stable ID with exact status;
    `NBH/02b_theory_campaign_history.md` (2.7 MB; grep it) full campaign history; `NBH/03_results_and_conclusions.md`;
    `NBH/03b_reasoning_and_traces.md`; `NBH/05_open_questions_and_next_steps.md`; `NBH/notation_and_conventions.md`;
    `NBH/04_code_and_files_index.md`; `NBH/01_overview_and_timeline.md`.
  - `NBH/branch_snapshots/<BRANCH>/` = the verbatim .md/.tex/.lean of each `theory/*` branch. **These are the
    authoritative mathematical texts.** Key: `MEET-THM/THEOREM_LIST_FINAL.md` (final cards),
    `MEET-THM/REGISTRY_PAPER1.md` (K-numbers), `MEET-THM/FOR_FELIPE_THEOREM_LIST.md`, `MEET-THM/HQ_CHARTERS/`,
    `MEET-v31/METHOD_v3.1_FINAL.md` (method spec), `MEET-v31/FOR_FELIPE_FINAL_METHOD.md`, `L-LEAN/` (Lean).
  - `NBH/transcript/part_*.md` verbatim messages by position; `NBH/transcript/INDEX.md`.
- Repo (outside the archive): `Results/` (final result tables), `Docs/HQ/STATUS.md`, `Docs/HQ/DECISIONS.md`,
  `Docs/Methodology/`, `Docs/Theory/` (pre-campaign theory, T01–T39), `Scripts/Campaigns/2026-10-28_New_Campaign/`
  (frozen production code v2.2.1 and analysis scripts), `README.md`.
- When the archive and an older repo doc disagree, the archive's final-state files win **unless** the newer file
  says otherwise; flag it.

## 2. LaTeX conventions (LuaLaTeX; see `preamble.tex`)

- Unicode is fine **in text mode** (π₀, Ẑ, 𝒪, ≤, ♯, ⚑ …). In **math mode** do not use precomposed accented letters
  or ♯: write `\hat{S}`, `\hat{Z}`, `\sharp`; `^` and `_` only inside math. The build fails on any dropped glyph.
- Section files start with `\section{...}\label{sec:...}`; no `\documentclass`, no packages (ask the lead).
- IDs: define each ID once with `\defid{TH05}` (or the `card` environment, which defines it); reference it with
  `\rid{TH05}`. Use the archive IDs (TH01–TH22, TH01.a clause rows, OB01–OB17, CJ01–CJ27, DR01–DR06,
  LIM01–LIM09, DF.., RL.., MD.., DS.., CL.., and Part-B TH101+/LM101+/CJ101+/RF101+/CE101+) and also give the
  native name (e.g. "M5 · Theorem HPM", "T03♯", "Theorem A", K-numbers) at first mention.
- Boxes: `card{ID}{title}`, `stmt{source span}`, `plain`, `notproved`, `uncertain`, `divergence`, `agentnote`.
- Tables: `booktabs`; long tables `xltabular`/`longtable`. Generated tables live in `tables/` and are `\input`.
- Use `\todo{...}` for anything you could not resolve; the lead will see it. Do not leave silent gaps.

## 3. The registry (`registry/*.tsv`)

UTF-8, tab-separated, one header row, one row per ID. Columns (exact order):

`id  native  kind  short  status_exact  checked_by  regime  depends_on  used_by  open_items  tex_label  sources`

- `kind` ∈ main-card, supp-card, clause, remark, obligation, future-work, drop, limitation, definition, ruling,
  method-decision, dissent, cited-lemma, history-result, refuted, counterexample, decision-pending,
  engineering, frontier.
- `status_exact` = verbatim status words (for archive IDs: identical to the status column of `NBH/ID_REGISTRY.md`).
- `checked_by` = compact: e.g. `SF:W2-VT03R; XF:A-REV2; Lean:none`.
- `regime` = where it holds: e.g. `any X`, `LH`, `W`, `LH-iid p<=n^A`, `fixed design (T03♯ hyps)`, `n/a`.
- Lists inside a field are `;`-separated. Empty field = leave empty (two tabs).
- `tex_label` = the ID itself if defined in the .tex (via `\defid`/`card`), else empty.
- Each agent writes only its own TSV file. `scripts/registry_to_tex.py` renders Appendix B from all of them.

## 4. Checks (`scripts/check.py`, run by `scripts/build.sh`)

It verifies: every `\src` path exists and the cited lines exist; cited files unchanged since 21ebc28;
every `\rid` resolves; IDs defined once; registry statuses equal `NBH/ID_REGISTRY.md`; coverage of in-scope IDs;
LaTeX log has no missing glyphs or undefined references. Run it on your own files before reporting:
`python Theory_work/State_of_Project/scripts/check.py --files sections/<yours>.tex registry/<yours>.tsv`.

## 5. Ownership (who defines which IDs and writes which files) — never `\defid` an ID you do not own

| Agent | Files it writes | IDs it defines (`\defid` / `card`) |
|---|---|---|
| Lead | `sections/00_agent_brief.tex`, `sections/01_problem.tex`, `main.tex`, `preamble.tex`, scripts | — |
| M (method) | `sections/02_method.tex`, `sections/A_notation.tex`, `registry/method.tsv` | MD01–MD13, DF01–DF25 |
| E (empirics) | `sections/03_empirics.tex`, `scripts/make_tables.py`, `tables/emp_*.tex`, `figures/emp_*`, `registry/empirics.tsv` | new IDs EMP01, EMP02, … (key empirical facts) |
| T1 (main theory) | `sections/04_theory.tex`, `figures/depgraph.tex`, `registry/theory_main.tsv` | TH01–TH09 and their clause rows (TH01.a, …) |
| T2 (supplement) | `sections/04b_supplement.tex`, `registry/theory_supp.tsv` | TH10–TH22, OB01–OB17, CJ01–CJ27, DR01–DR06, LIM01–LIM09, CL01–CL23 |
| H (history/open) | `sections/05_history.tex`, `sections/06_open_and_plan.tex`, `sections/C_files.tex`, `sections/D_glossary.tex`, `registry/history.tsv`, `registry/open.tsv` | RL01–RL06, DS01–DS06, every Part-B ID (TH101+, LM101+, CJ101+, RF101+, CE101+) it discusses, and new IDs DEC01… (pending decisions), ENG01… (engineering), FR01… (frontier problems) |

Reference anyone's IDs freely with `\rid{...}`; unresolved references to other agents' IDs are expected until
the lead's full build. New-ID prefixes EMP/DEC/ENG/FR are defined by this document (not the archive); give each a
registry row.

## 6. Checking your work (safe while others work)

- `bash scripts/check_section.sh sections/<yours>.tex [more.tex]` — compiles your files alone in a temp folder,
  reports LaTeX errors / dropped glyphs, writes `checks/preview_<name>.pdf`, then runs `check.py` on them.
- `python scripts/check.py --files registry/<yours>.tsv` — registry format, statuses vs `NBH/ID_REGISTRY.md`, sources.
- Do **not** run `scripts/build.sh` (the lead runs the full build).
- Your section must compile with 0 errors and 0 dropped glyphs, and `check.py` must report 0 errors, before you finish.
