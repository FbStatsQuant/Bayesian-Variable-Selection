# Rider tickets — common rules (Theory Department, 2026-11-15)

Binding for every rider ticket the Theory Department opens (W3-START2-R, W3-RM2-R, W3-PSHARP-R, W3-MISR-R, W3-EDIT).
On top of: `Theory_work/Wave3/PROTOCOL_v4.md` (H1–H6), `Theory_work/Wave3/PROGRAM.md` (presentation rule +
**Readability**), `Theory_work/INFRA/LIFECYCLE.md` where v4 points to it. Your ticket's `BRIEF.md` says what to prove.

## 1. Where you work
- Your worktree is `/home/fb31/BVS-wt/<TICKET>` (branch `theory/<TICKET>`, cut from `origin/main`). Work **inside the
  worktree**; write only in `Theory_work/Wave3/<TICKET>/`. Change no git state: the department's snapshot cron commits
  your folder in place every 15 min and pushes (restore points; a new `CHECKPOINT_<k>.md` or `MANIFEST_*` gets an RP label).
- **The parent ticket's folder is read-only.** Its `STATEMENT.md`, lemmas and `CHECKPOINT_<k>.md` files are hashed in
  the registry (`claims.tsv` sha256, `status_sha256`); editing them breaks recorded claims. You restate and re-prove
  in your own folder.
- **Delta statement.** Your `STATEMENT.md` is a delta over the parent's recorded version, in the pattern of
  `W3-START2/STATEMENT.md` v1.4 over W3-START v1.3.4: it states in full every definition, hypothesis and claim that
  differs, takes everything else from the parent by `file:line`, and has a §"Dependencies and supersession" table
  (new claim ⇒ parent claim, one line of why). It asserts no proof status. Claim ids are new (`<TICKET>:<name>`);
  the recorder registers them with `implies` edges to the parents; supersession of headline rows goes through HQ and
  the HQ consultant (v4 H5), not you.
- **Interpretive sentences (HQ/consultant rule, 11-16).** A "hence …", "this means …", "reading" or "interpretation" sentence
  inside a registered statement span is either moved out of the span (a remark below it, not registered) or stated and
  checked as a claim, with a reviewer seat asked about it by name. Both council seats passed a false one (W3-MISR
  STATEMENT:191-195, KL reading with a random intercept). Council briefs ask each seat to list every such sentence in
  the claimed spans and give each a verdict.
- New proofs go in new files under `lemmas/`. Where you reuse a parent lemma unchanged, cite it (`file:line`, the
  registered id and version). Where you change a step, copy the lemma into your folder, mark the changed lines
  `[R-#]`, and that copy is what gets line-checked.

## 2. Files (v4 §1)
`BRIEF.md` (from the department; do not edit) · `STATEMENT.md` (delta; changelog table at its foot, v4 §4.2) ·
`TARGET.md` (one page: assumption map of the changed hypotheses, parity row per changed clause vs the parent and the
closest published result, boundary numerics if a hypothesis is weakened) · `DEPS.tsv` (v4 §4.1, kept by hand with
`sha256sum` until `deps.py` exists) · `PLAN.md` · `LOG.md` (timestamps from `date`, local time; every agent started,
with model and role) · `lemmas/` · `numerics/` · `reviews/` (each brief saved **before** launch, each reply verbatim,
each disposition) · `ERRATA.md` · `READER_DELTA.md` (§5) · `CHECKPOINT_<k>.md` (k = 1, 3; plain integers, the
registry tools read only `CHECKPOINT_<digit>.md`) · `REPORT.md` with its REGISTRY block (template
`Theory_work/INFRA/templates/ASSUMPTION_MAP.md`; REPORT restates nothing, v4 §3).

## 3. Chain (Tier B, NORMAL mode)
1. **Statement lock** — one Sol review, fresh, blind first read: delta STATEMENT + PLAN + the parent files you
   consume + the triage rows that motivate the change. Fix, lock.
2. **CP1 (hard)** — `CHECKPOINT_1.md`: locked delta statement, target clauses, which clauses change a headline
   statement (STRONGER / NEW-CLAIM), `TARGET.md`, plan with hours, `READER_DELTA.md` draft. **End your run**; the
   department manager answers CP1 (usually within the hour). No Astra better-theorem review unless the brief asks for
   one: these targets come from a blind sharpness audit, which served as the better-theorem input.
3. **Line checks** — Sol, 2–4 lemmas per review, new agent per batch, blind to LOG and earlier reviews. Repaired
   lemma → re-check by a new Sol agent on the repair and every STALE DEPS row.
4. (Tier B: no break review.) Sweep duties go into the council briefs (statement copies vs lemma statements;
   quantifiers; each lemma's scope vs downstream uses; REPORT/registry block vs STATEMENT; DEPS rows spot-checked).
5. **Citation check** 0 MISS (copy the parent's `citecheck.py` into your folder and point it at your files).
6. **Council** — freeze `reviews/MANIFEST_R1.txt` with `python Theory_work/Wave3/tools/manifest.py freeze
   Theory_work/Wave3/<TICKET> Theory_work/Wave3/<TICKET>/reviews/MANIFEST_R1.txt --extra <INPUTS.txt>` from the
   worktree root, only when every DEPS row under a claim is OK. Two seats, fresh, blind first read: Sol (OpenAI seat)
   and Opus 5.5 high on Claude Third (Claude seat). Each brief contains the block from
   `Theory_work/INFRA/templates/COUNCIL_BRIEF.md`, asks for the per-claim table `| id | decision |`, findings tagged
   C/S/F/E, the six gates, and states that a seat **must** give `gates=FAIL` when it holds a C, S or F finding of its own.
   E findings go to `ERRATA.md` and never block. Accepted C/S/F findings → diff round (v4 §5.5).
7. **CP3 (hard)** — `CHECKPOINT_3.md`: the passing round, `manifest.py bind` output, DEPS all OK, citecheck,
   `python Theory_work/INFRA/tools/ingest.py claims Theory_work/Wave3/<TICKET>/REPORT.md --staged` output, per-claim
   statuses verbatim. **End your run.** HQ does acceptance and recording; you never touch main or the registry.

## 4. Agents
- Reviews: `delegate_task`, provider `codex`, model `gpt-6.1-sol` (Sol) or `gpt-6-astra` (Astra), reasoningEffort
  `high` always ("Codex level N" is the company pacing level, POLICIES §14, never an effort setting), mode wait. If codex is unavailable or rate-limited, say so in LOG and to the manager; never substitute a
  Claude reviewer for an OpenAI step. W3-DIST has priority on codex in any conflict.
- Helpers: at most 2 at once, `delegate_task`, provider `claudeAgent_claude_third`; Sonnet 5.5 or Haiku 5.5 for routine
  work (bookkeeping, citecheck, numerics), Opus 5.5 only for proof work; no Fable (owner pacing, 11-16); effort high max. A helper never reviews what it wrote.
- API proof attempts (Fable via the Console) only through the manager → HQ as an "API card"; they are proof material,
  never reviews (v4 H3).

## 5. Readability (owner rule; binding)
Any claim that changes a headline statement (START2 (T1⁺)/(T3⁺)(b)/IF-START⁺, PSHARP Prop A / Cor A1, RM2-F) needs its
**reader version** updated: numbered primitive assumptions, one to three displays with explicit rates, no internal ids
in the reader text (PROGRAM "Readability"). Write `READER_DELTA.md`: the current reader version (from
`/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md` if it exists; read only), what changes,
the new text, and the bridges it needs. The manager passes it to HQ for W3-READER. Do not write in W3-READER's folder.

## 6. Stops and reporting
- Read `Theory_work/Wave3/HOLDS.md` (on `origin/main`: `git show origin/main:Theory_work/Wave3/HOLDS.md`) at each
  checkpoint and before each freeze.
- Early checkpoint (end your run with a `CHECKPOINT_<k>.md`): a counterexample to a target clause; a WEAKER change to
  a target clause; a new key lemma appears (this makes the ticket Tier A); a kill budget spent (3 failed attempts on
  a lemma, each with a reviewer verdict); a hold on a consumed claim; you cannot finish before the cut-off.
- **Cut-off:** theory content freezes **Wed 2026-11-18**. Aim for CP3 by **Wed 18:00 CT**. If a clause will not make
  it, drop it to a named open item at the earliest checkpoint rather than run late.
- Heartbeat in LOG.md at least every 2 h while working. Your final message at each checkpoint = the checkpoint's
  content in ≤ 25 lines.
- Temp work: `export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/<YYYYMMDD>-<TICKET>-<what>` (CI runs: `/home/fb31/SMC_Theory_Department/ci`), never /tmp; remove when done (POLICIES §12 rules 8–9; /home/fb31/SMC_Theory_Department/INDEX.md).
  **Exception — Codex reviewers (Sol/Astra) are sandboxed:** a write outside their worktree raises an approval request nobody
  can answer, and the reviewer stalls forever (11-16, START2-R RC1). Their briefs must say: no TMPDIR, no writes outside
  the worktree; scratch only in `<worktree root>/.rc_tmp/` (git-ignored for all worktrees via the shared
  `.git/info/exclude`; never inside the ticket folder, where manifest.py would count it), deleted at the end.
- **Patch application (HQ rule, 11-16, after a silent `git apply` skip):** run every patch from the repo root with
  `git apply --verbose` (or `patch -p1 --verbose`); a "Skipped" or 0-hunk result is a hard failure. After applying, verify each
  target file's sha256 against the expected post-apply hash from the dry run (or the prepared LINES_CHECK); any mismatch → stop.
- Do not touch: `Theory_work/Wave3/W3-DIST/`, `W3-READER/`, `PROTOCOL_REVIEW/`, `Docs/`, `Lean/`, `Theory_work/Dept/`.

- **HQ 11-16 (17:07): better-theorem review skip.** Code-reading lemmas with no CP1 target (W3-AUDIT track A T1–T5, T10; extended by HQ to T6–T9; manager-confirmed 18:32 for the re-checks X1, X3, X5 at 17:58, premise-closers) skip the better-theorem review. Record "skipped (HQ 11-16)" in each CHECK.md.

- **HQ 11-16 (20:44): no registry files in council manifests.** No council manifest may freeze registry files
  (`Theory_work/INFRA/registry/claims.tsv`, `assumptions.tsv`, or any other registry table) as EXT inputs: they change
  with every recording and void the council. Cite the registry rows (id + status, verbatim) in the brief instead. Applies
  to every new freeze and re-freeze. Post-freeze tool item: manifest.py warns when an EXT input is a registry file.
- **HQ 11-17 (12:55): extended.** The same applies to INFRA/DECISIONS.md and any other live log (files appended by lifecycle tools): no council manifest freezes them as EXT inputs. The manifest.py warning covers live logs too.

- **HQ 11-17 (14:11, owner; POLICIES §5, main b40abc79): Sol model.** All future Sol reviews use **gpt-6.2-sol** (provider codex,
  reasoningEffort high), not gpt-6.1-sol. Reviews already in flight finish as started. Record the model id in each review's header.

- **Fuel (HQ 11-17, owner):** every agent and every review subagent explicitly on `claudeAgent_personal`; never Claude Third/Work. Codex only for the remaining key checks and the 3 SOL62 A/B calls.
- **Finished folder to main at recording (HQ 11-17, owner):** each ticket's finished folder goes to main as part of its recording, not later. No long tail of branches/PRs.
- **Card-requote re-freezes (HQ 11-17):** automatic in the recorder script; each stays CITATION-ONLY and is PURE-checked by Opus (stated in the carriers).
- **D80 scope (HQ 11-17):** if main moved only through live logs (HQ_DECISIONS.md, HQ_NOW.md, never manifest-frozen), that is not a stop. Any manifest, registry or theory-file drift is a hard stop.
- **Sol model (owner 11-17 night; POLICIES §5 00d90758; supersedes D122):** default `gpt-6.1-sol` (codex, high) for all Sol reviews; `gpt-6.2-sol` only in the SOL62 A/B. The model id goes in each review header.
- **No attested verdicts (HQ 11-17):** never write a carrier or verdict that contradicts the seat's own file. If a second seat is missing, run a real continuation seat (HQ GO).
- **Round labels:** council round labels must be `R<digits>` (manifest.py VERDICT grammar). Never use suffixes such as R3S.
- **Recorder pushes (HQ 11-17):** prepush.sh in every recorder clone requires LAND=yes, set only on an explicit GO. Commits use the repo's normal author identity. An accidental land is fixed forward (note + CITATION-ONLY if needed), never by force-push.
- **Sol model (owner GO 11-17 late; POLICIES §5 44803272; supersedes the 6.1 revert):** default `gpt-6.2-sol` (codex, high). **6.2 verdicts are input, never decisions:** the lead triages each point against the acceptance filter (it made a false Thm2X REJECT in the A/B). Log real-gate reviews in SOL62_QUALITY.md. No re-runs of past 6.1 seats.
