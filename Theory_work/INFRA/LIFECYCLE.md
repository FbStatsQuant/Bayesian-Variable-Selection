# Claim lifecycle: review, rollback, supersession

Binding for every theory ticket from Wave 3 on (set by Theory HQ 2026-11-09; Felipe Bedoya, product owner). It
replaces the "ROLLBACK" protocol of the INFRA brief, with HQ's decisions of 2026-11-09 folded in. Tools live in
`Theory_work/INFRA/tools/` (standard-library Python; run from the repository root). Data is plain TSV in
`Theory_work/INFRA/registry/`.

Two risks are managed separately:
- **Correctness**: a result is wrong or its proof has a gap → *rollback* (§3).
- **Strength**: a result is right but not as good as it could be (weaker conclusion, stronger assumptions, narrower
  scope) → *supersession* (§5). In mathematics this is the more common way to build a paper on the wrong
  foundation, so it has its own gate (§4.2), its own CI step (§8) and its own decision rule (§5.3).

## 0. Who decides

| decision | who | recorded in |
|---|---|---|
| which results to pursue; adding a result to the paper headline (`headline=yes`) | **Felipe** | DECISIONS.md |
| any change to what the paper claims: RETRACT / NARROW / DEPRECATE / SUPERSEDE of a headline, COEXIST that changes which theorem is stated | **Felipe** approves, HQ executes | DECISIONS.md + PR label `major-claim` |
| PATCH, DOWNGRADE of a non-headline claim, SUSPECT / CLEAR, free supersessions, REMARK, DECLINE, re-point confirmations | **HQ** | events.log (+ DECISIONS.md for strength decisions) |
| launching an improvement ticket (with its kill budget) | HQ (Felipe if headline-changing) | DECISIONS.md |
| merging any PR | HQ | GitHub |
| freeze / unfreeze (`config.tsv freeze`) | Felipe | DECISIONS.md |

## 1. Objects

**Claim** (row of `claims.tsv`): one theorem / lemma / proposition / corollary / counterexample / obstruction /
audit verdict / implementation claim, or an **external anchor** `SOP:<row>` (State-of-Project inputs such as T03♯ =
`SOP:TH09`, M5(0) = `SOP:TH05.0`, T12 = `SOP:TH110`). Key fields:
- `file` + `lines` + `premises` + `sha256`: the statement text plus the spans it relies on (setting, hypotheses,
  event/threshold definitions written elsewhere); all are hashed together, so a silent change to a hypothesis is
  caught. `check.py` fails if the hash changes without a `rehash`. A LaTeX transcription (`tex`) is hashed
  separately (`tex_sha256`) when someone has compared it with the statement (`registry.py rehash ID --tex`); a
  changed transcription is a check ERROR, and an unreviewed one is flagged inside the generated paper block.
- `version` (semver), one policy for every tool: **major** = the claim changed (retract, narrow, a re-registered
  statement that changed in substance); **minor** = proof / status / lifecycle changed (patch, downgrade, supersede
  of X, deprecate, clear, a new ticket status); **patch** = coverage or transcription corrections (spans, premises,
  status source) and editorial changes.
- `status`: the ticket's status words **verbatim**, copied from ONE place (`status_source`, checked by C10).
  Never upgraded by tools: `registry.py set` cannot touch it; `registry.py correct-status` fixes a transcription
  error only if the new text occurs verbatim at the given source line; `propagate.py downgrade` refuses a stronger
  status; an upgrade needs a new ticket result (PR).
  A part split out of a bundled claim whose ticket gives no per-clause status carries
  `UNSPLIT-STATUS: <parent status verbatim>` (checked at the parent's source, strength inherited, WARN C10-unsplit);
  the parent depends on all its parts and implies each. From Wave 3 on, tickets state per-clause statuses and fill
  the REPORT registry block (`templates/ASSUMPTION_MAP.md`); `tools/ingest.py claims REPORT.md` reads the blocks
  directly (`ingest.py convert REPORT.md` prints the JSONL it derives; paths are relative to the REPORT's folder).
  Ingestion round-trips the registry schema (bound `consumes`, `method_commit`, `method_components`, binding-map
  rows, strength fields), rejects unknown fields and unresolvable references, and is all-or-nothing: any problem →
  nothing written, exit 1. At CP3: `ingest.py claims REPORT.md --staged` (applies to a disposable copy, runs the
  full `check.py --acceptance <every ingested id>` there and prints it, acceptance findings separately; exit 1 on
  any ERROR), then `--apply` only if that passed, then `check.py --acceptance <ids>` again before labelling or
  merging. REGISTRY-block fields are `name:` followed by zero or more spaces; inside a fenced block every non-blank
  line must be fields (anything else is reported, it never ends the block silently).
- `premises`: spans `path:a-b`; `path:a-b@archive:<ref>` reads the span as committed at `<ref>` (set by
  `rollback-ticket` when the file is reverted with a rolled-back ticket; the hash is unchanged).
- `state` (lifecycle, added by INFRA): `ACTIVE`, `CANDIDATE` (new result not yet at assurance parity),
  `SUSPECT` (an input is in doubt), `REBASE-NEEDED` (still true, but built on a superseded input and scheduled to be
  rebuilt), `NARROWED` (statement narrowed in place, dependents being checked), `RETRACTED`, `DEPRECATED`,
  `SUPERSEDED-VALID` (replaced by a better theorem, still true, restored automatically if the replacement falls).
- `depends_on`: **use-level edges** `id@use`, where `use` is `stmt` (the statement; default), `stmt:<clause>`,
  `proof:<fact>` (an event, rate, constant or lemma inside the other claim's proof), or `hyp` (the other claim is
  an explicit hypothesis of this statement — a conditional result; see acceptance A3 in §4). Propagation follows use-level
  edges: a PATCH reaches only `proof:` uses; a NARROW reaches only uses it no longer covers.
- `method_commit` + `method_components`: the method/code version the claim is about (§7).

**Assumptions are first-class** (`assumptions.tsv`): `A:*` = assumption (a hypothesis as stated), `P:*` =
interface property (what proofs actually use). Each has a version and an implication lattice (`implies`).
- **Interface rule (key rule).** Every *shared* assumption A has exactly one **bridge lemma** A ⇒ P (`bridge`).
  Theorems and lemmas *consume P* (`consumes`), never A directly; only headline statements and the bridge itself
  name A. Weakening A then means re-proving one bridge, not every theorem. A consumer binds the bridge it actually
  uses — family / clause specific — as `P:X@<claim id>` in `consumes`; that creates a `proof:P:X` edge to that claim
  (so retracting it propagates, and a supersession can propose re-pointing it). A plain `P:X` is informational.
- **Polarity.** A claim lists an assumption as a hypothesis (`A:X`), in a necessity result / counterexample
  (`A:X~nec`), or both directions (`A:X~iff`). Weakening an assumption globally is safe only where it has hypothesis
  polarity: `registry.py assumption-impact A:X` says whether to weaken or to **split** (keep A for the necessity
  results, add a weaker A′ for the hypotheses). Prefer splitting; the number of distinct headline assumption sets is
  capped (`config.tsv max_assumption_sets`, check S6).

**Strength fields** (headline theorems and shared assumptions only — not every lemma). The `assumptions` list is a
**conjunction**: when a theorem has alternative hypotheses ("exact Gram, or iid rows"), record the weakest common
hypothesis (e.g. the approximate-Gram condition with δ_n = 0 as an instance) or register the variants as separate
clause claims. Fields: `assumptions`, `consumes`,
`conclusion` (`identity < target < posterior < reported-model < delivery`, plus `negative`), `rate`, `scope`,
`implies` (Y ⇒ X), `superseded_by`, `coexists_with`, `gates`, derived `improvable`.
- `sharpness.tsv`: per (headline, assumption), the necessity evidence — `NECESSARY` (counterexample without it),
  `NECESSARY-FOR-ROUTE` (e.g. Prop SHARP: optimal for the lattice route only), `FAILED-REMOVAL` (a documented failed
  attempt — weak evidence; one row per attempt), `ARTEFACT` (known proof artefact), `WEAKENABLE`, `NONE`.
- An assumption is **settled** when it is NECESSARY or has ≥ 2 FAILED-REMOVAL rows. `improvable = yes(…)` lists the
  unsettled hypotheses of a headline.
- `binding.tsv` (**binding map**): for each headline assumption, the claim whose proof *forces* it, the mechanism,
  and early sub-par signals (§4.3). Improvement work targets binding claims only.

## 2. Life of a claim

```
            (new result of an improvement ticket)
                         CANDIDATE --promote (assurance parity)--> ACTIVE
ticket result ----------------------------------------------------> ACTIVE
ACTIVE --patch--> ACTIVE (minor bump; proof: dependents SUSPECT)
ACTIVE --downgrade--> ACTIVE with weaker status (dependents SUSPECT)
ACTIVE --narrow--> NARROWED --clear--> ACTIVE   (uncovered dependents SUSPECT)
ACTIVE --retract--> RETRACTED                   (dependents SUSPECT; what it superseded is restored; row kept)
ACTIVE --deprecate--> DEPRECATED                (dependents SUSPECT; FAILED_ROUTES.md; row kept)
merged ticket T --rollback-ticket--> every claim of T RETRACTED as a tombstone (archive tag), dependents SUSPECT
ACTIVE --supersede (by Y)--> SUPERSEDED-VALID --(Y retracted)--> ACTIVE
SUSPECT / REBASE-NEEDED --clear or confirm-repoint--> ACTIVE
```

## 3. Correctness rollbacks

`propagate.py` is DRY-RUN BY DEFAULT: it prints the impact report and writes nothing; add `--apply` to write (registry, DECISIONS.md, FAILED_ROUTES.md, issues/ — all under Theory_work/INFRA). Attach the dry-run report to the issue / PR first.

| level | trigger | statement | command | who |
|---|---|---|---|---|
| **PATCH** | a proof gap was found AND repaired (repair lemma-checked); the statement stands | unchanged | `propagate.py patch ID --reason R` (only `@proof:` dependents SUSPECT) | HQ |
| **DOWNGRADE** | evidence weaker than recorded (review withdrawn, gate failed) | unchanged | `propagate.py downgrade ID --status "<new verbatim>" --reason R` | HQ (Felipe for headline) |
| **NARROW** | statement too strong; a narrower one holds | edited in place | edit the statement → `propagate.py narrow ID --still-covers "stmt:(a);proof:E_n" --reason R` (owns the major bump) → `registry.py rehash ID --bump none --reason "narrowed text"` | Felipe (headline) / HQ |
| **RETRACT** | statement false | kept for history | `propagate.py retract ID --reason R` | Felipe (headline) / HQ |
| **DEPRECATE** | wrong target / dead route | kept, archived | `propagate.py deprecate ID --reason R` + archive branch + tag | Felipe (headline) / HQ |
| SUSPECT / CLEAR | possible gap / repair done | — | `propagate.py suspect ID` / `propagate.py clear ID` (refused while any consumed claim — through stmt / proof edges, transitively — is not ACTIVE; a non-ACTIVE `@hyp` input only with a `conditional on <it>` status; an `ack` never suffices) | HQ |

An OPEN proof gap (not yet repaired) is not a PATCH: mark the claim `suspect` (statement users become SUSPECT
too) or `downgrade` it, and PATCH only once the repair is checked.

Each SUSPECT dependent gets a repair issue (one per ticket, `--gh` creates them): re-check the step that uses the
upstream claim; PATCH and `clear` if it survives, else narrow/retract and propagate further.

**Git for each level** (never rewrite `main`; never force-push):
1. Before a RETRACT / NARROW / DEPRECATE / SUPERSEDE of a headline, tag the current state of the claim:
   `git tag -a claim/<id-with-:-as-_>/v<version> -m "<reason>" <commit>` (e.g. `claim/W2-FAC-A_Thm-FAC-L/v1.0.0`).
2. Work on `theory/<ticket>-<op>` (e.g. `theory/W2-FAC-A-narrow`), commit the statement edit + registry change +
   `issues/…/00_impact.md`, open a PR with the template, label `retraction` (+ `major-claim` for headlines).
3. To undo a *merged* wrong change, **never delete registry rows**: a retracted / deprecated claim stays in
   `claims.tsv` as a **tombstone** (state RETRACTED / DEPRECATED, `archive:<tag>` in its evidence), so later
   dependents keep a resolvable id and propagation has something to start from. `check.py` hashes and status-checks
   a tombstone at its archive tag, not in the working tree (C2-tombstone ERROR if the tag is missing or differs).
   One PR, in this order (ticket `T`, merge commit `M`; claims T *changed* but did not introduce are handled with
   `propagate.py narrow|retract …` on the current graph, not by rollback-ticket):
   ```
   git switch -c theory/T-rollback origin/main
   git tag -a retracted/T -m "rollback of T: <reason>" HEAD          # archive = current main (current text)
   python Theory_work/INFRA/tools/propagate.py rollback-ticket T --archive retracted/T --merge M --reason R  # 1. price
   python Theory_work/INFRA/tools/propagate.py rollback-ticket T --archive retracted/T --merge M --reason R --apply  # 2.
   git add Theory_work/INFRA; git commit -m "rollback T: registry (tombstones + propagation)"   # incl. issues/
   git revert -m 1 --no-commit M                                     # 3. revert T's non-registry files ...
   git checkout HEAD -- Theory_work/INFRA/registry Theory_work/INFRA/DECISIONS.md \
       Theory_work/INFRA/FAILED_ROUTES.md Theory_work/INFRA/issues   #    ... keeping the lifecycle rows
   python Theory_work/INFRA/tools/check.py                           # 4. no new ERROR; tombstones verified
   git commit -m "rollback T: revert ticket files (merge M)"; git push --follow-tags   # open the PR
   ```
   Step 1 prices the rollback on the CURRENT graph (dependents added after the merge included) and writes nothing.
   Step 2 retracts (`--as deprecate` for a dead route) every live claim of T in a staged copy, propagates SUSPECT to
   all later dependents (transitively), and moves every surviving claim's premise span that lies in a file the revert
   changes to the archive (`path:a-b@archive:retracted/T`, refused if the text there differs). It then runs the full
   `check.py` on the copy twice — as written, and on the proposed POST-REVERT tree (the files merge `M` changed, as
   at `M^1` or removed; without `--merge`, the ticket folder and its claims' statement files are taken as removed)
   — and writes the whole staged state only if neither adds an ERROR (a surviving claim whose statement or status
   source the revert removes must be moved first). If the revert conflicts with later work on T's files, resolve in favour of the later work and
   re-run step 4. A single claim can be tombstoned with `propagate.py retract|deprecate ID --archive <tag>`. Do not
   hand-edit `claims.tsv` state fields — use `propagate.py`.
4. DEPRECATE: `git branch archive/<ticket> <last commit of the route>` and `git tag -a deprecated/<ticket> …`, push
   both; add a `DEPRECATED` banner at the top of the ticket's REPORT.md via the PR; the route goes to
   FAILED_ROUTES.md (written by `propagate.py deprecate`).
5. Releases of the theory state: annotated tags `theory-vMAJOR.MINOR[-pre]` (e.g. `theory-v2.0-pre`) after HQ
   approval; the tag message lists `check.py` counts and the headline set.

## 4. Gates

A claim enters the paper headline only after BOTH gates; they are separate reviews with separate reviewers.
**Acceptance (HQ, CP3)** is mechanical and blocking: `check.py --acceptance <claim ids>` exits 1 (REFUSED) on any
ERROR, including
- A0: the claim is not ACTIVE, or a claim it consumes is not ACTIVE — every claim reached through `stmt` / `proof`
  / bound-bridge edges, transitively, whatever its status text or `acks`; a direct `@hyp` input that is not ACTIVE
  only if the status is `conditional on <it>`;
- A1: a headline without `correct:`, `lit:`, `necessity:` PASS with evidence, and without `better:PASS(evidence)` or
  a disposition for every better-theorem proposal (gates are parsed per `;`-entry `name:RESULT(evidence)`; an
  unparsable entry or contradictory results for one gate are errors); for ANY claim, an unparsable gate entry
  (`A1-gates`: malformed syntax never hides an evidence reference), and a gate entry — whatever its
  result (PASS, FAIL, PENDING, …), every `better-proposal` and `better-disposition` included — whose
  evidence does not resolve to an existing repository file (`A1-evidence`: the first token of the evidence, and every
  later path-like token, as `path[:a-b][@commit]`, relative to the repository root, the ticket folder, or the folder
  of the statement / status source; `@commit` pins it, and the file must then exist at that commit); and for EVERY
  checked claim, headline or not, neither `correct:PASS(<existing file>)` nor a valid council record
  (`A1-correct`);
- A2: a `better-proposal` without its review file, or with no evidence-backed disposition (a deferral is not a
  disposition; the disposition's evidence must resolve like any gate evidence, A1-evidence);
- A3: a PROVED-CHECKED-class status resting on a direct input of lower assurance — author-only / unchecked, PARTIAL
  / CONDITIONAL, OPEN, or unclassified — unless that input is a DECLARED hypothesis: every edge to it is `ID@hyp`,
  its id, an alias or its name occurs as a whole token in the hashed statement / premise text, AND the status text
  says `conditional on <its id or name>` (an incidental mention plus `@hyp` fails; the clause after "conditional on",
  up to the end of its sentence, `;` or `)`, is a `,` / `and` list of COMPLETE ids or names, and "not / no longer
  conditional on" does not count); every checked claim that consumes
  a conditional result (through `stmt` / `proof` edges, transitively) must carry the same `conditional on <W>` in its
  own status (`A3-condition`, checked on the consumer and, for existing consumers, on the conditional result); an
  `ack` never waives A0 or A3;
- A4: a checked claim without a CP3-PASS council record (§4.1): the record, its frozen manifest (still verifying
  on the current tree, and covering the statement, premise and status-source files — a status source that is the
  ticket's own `CHECKPOINT_<k>.md` only under the conditions of §4.1 "Checkpoint status source") and one matching
  `COUNCIL-VERDICT` line in each seat's review file;
- A5 (transitive assurance): a claim that consumes — through `stmt` / `proof` / bound-bridge edges, transitively, and
  through an `@hyp` edge unless the consumer is `conditional on` it — a PROVED-CHECKED-class claim that carries no
  durable acceptance record: an `accept` event in `events.log` for its CURRENT acceptance identity (written only by
  a PASS of `check.py --acceptance <ids> --record`, or `ingest.py claims F --staged --record`; it stores the version
  and the `fp2` fingerprint of the whole acceptance identity — row fields, provenance, effective inputs and the
  content of every cited artifact, §4.1 "Acceptance record" — so any later change makes it stale), and which still
  passes its own acceptance checks (A0-inputs–A4) on the current tree (revalidation, R04-N1), or a row of the frozen
  **legacy boundary** `INFRA/LEGACY_ACCEPTED.tsv` (the claims that were
  PROVED-CHECKED on main at tag `theory-v2.0-pre` — that tag only: a file naming any other tag or commit is not
  trusted — generated once by `bvsreg.py legacy-boundary`; a row counts only
  while the claim's id, version and statement hash are unchanged; `check.py` recomputes the file from the tag and
  reports any difference as an `L1-legacy` ERROR, which empties the boundary). Claims named in the same acceptance
  run count as accepted (the run refuses as a whole on any ERROR). So an intermediate admitted with `ingest --apply`
  but never accepted cannot carry a checked label into an accepted consumer.

**Recording.** Run acceptance with `--record` (`check.py --acceptance <ids> --record`): on a PASS — 0 ERROR in the
whole run — one `accept` event per named claim is appended; on REFUSED nothing is written. `--only` (a display
filter) is refused together with `--acceptance`, so no filtered run can print or record a PASS. A claim changed after
its acceptance (patch, new edge, new gates, relocated statement, edited or deleted evidence, withdrawn council verdict,
changed reviewed ticket content, a changed input, …) must be accepted again before an accepted claim may consume it.

A checked intermediate result that is not a headline is accepted without the strength gates (but with A0, A1
evidence / correct, A3, A4 and A5, recorded with `--record`); its headline admission stays pending. Before every continuation and merge,
`check.py --consumed-vs origin/main --tickets <T>` compares each claim T consumes with the registry on current main
(`git show <ref>:Theory_work/INFRA/registry/claims.tsv`): ERROR if it is absent or not ACTIVE there, or at a higher
major version there (rule 11).

### 4.1 Correctness gate (`correct:PASS(...)`)
The wave protocol: statement lock → lemma-by-lemma falsification numerics + cross-family line check → mid-point →
exhaustive sweep → council (Codex Sol high + Claude Opus high, both ≥ 8.0, all gates PASS). On GitHub, the council
pass is the PR approval (§9).

**Council record** (`council` field; one machine-readable format; required at acceptance for every checked claim):
```
R<k>; MANIFEST <64-hex digest>; <seat>=<score> PASS(<review file>); <seat>=<score> PASS(<review file>)
e.g.  R2; MANIFEST 3f9a…c1; sol=8.6 PASS(reviews/R2_council_sol.md); opus=8.3 PASS(reviews/R2_council_opus.md)
```
One record = the ONE passing round: its number, the digest of the frozen manifest both seats reviewed
(`manifest.py freeze <ticket> <ticket>/reviews/MANIFEST_R<k>.txt --extra <ticket>/reviews/INPUTS.txt`), and per seat
its score and `PASS` (all of that seat's gates passed) or `FAIL`, with its review file.

**Council verdict line** (finding R03-N2: a review binds an OUTCOME to the digest; a mention of the digest is not a
verdict). Every council review file contains, on a line of its own (optionally in backticks), exactly once:
```
COUNCIL-VERDICT round=R<k> manifest=<64-hex digest> seat=<seat> score=<x.y> gates=PASS|FAIL
e.g.  COUNCIL-VERDICT round=R2 manifest=3f9a…c1 seat=sol score=8.6 gates=PASS
```
`gates=PASS` means every gate of that seat passed on exactly that manifest. A review file is one seat's verdict in one
round on one manifest: a second verdict line — for the same digest, another digest or another round — is a
contradiction, and a line naming `COUNCIL-VERDICT` that does not match the grammar exactly is malformed. Blind briefs
require the line (`templates/COUNCIL_BRIEF.md`).

Acceptance (A4) requires: exactly one `R<k>` and one `MANIFEST`; at least two seats with distinct names and distinct
review files; every seat ≥ 8.0 and `PASS`; every review file resolving like gate evidence; the digest equal to the
header of an existing `reviews/MANIFEST_*.txt` of the ticket (tickets.tsv `folder`, else the statement file's folder)
and `manifest.py verify` of that manifest passing on the CURRENT tree (content changed after the round → refused);
and in every review file exactly one `COUNCIL-VERDICT` line for that digest, matching the cell's round, seat and
score, with `gates=PASS` and score ≥ 8.0, and no malformed or contradictory verdict line. `manifest.py bind
<manifest> <reviews…> [--council "<cell>"]` applies the same verdict rule (one round, distinct seats; with
`--council`, the cell must match the verdicts) and prints the council cell to record. Anything else — a failed or
exhausted council, scores from different rounds, free text, a digest quoted as "not reviewed" — is an A4 ERROR.
Pre-Wave-3 rows keep their free-text council history; they are not re-accepted (their claims sit in the legacy
boundary, A5).

**Checkpoint status source** (INFRA R05, HQ 2026-11-12). The frozen manifest must cover each claim's statement file,
premise files and status-source file. Wave 3 tickets write their per-claim status lines (and REGISTRY blocks) in their
own `CHECKPOINT_<k>.md`, which `manifest.py` never covers: a status line written after the council cannot be inside the
manifest the council reviewed. So a status source that is the claim's OWN ticket's `CHECKPOINT_<k>.md` (directly in the
ticket folder) is exempt from coverage — as status source only; statement and premise files stay covered — and A4
then also requires:
1. **Frozen at ingest.** `ingest.py` records the checkpoint's content digest (line-wise SHA-256) in the row's
   `status_sha256` (also `registry.py add / correct-status` and `propagate.py` status changes; never settable by
   `registry.py set`), committed with the ingest. The file must still have that digest: any later edit of an ingested
   checkpoint is a `check.py` C12-checkpoint ERROR (CI) and refuses acceptance. Corrections go to a new file.
2. **Ids = what both seats accepted.** Every claim id the checkpoint carries (its REGISTRY blocks, plus every row
   whose status source is that file) with a checked label (any status not explicitly below checked — open, partial /
   conditional, proved-unchecked — an empty status included) is accepted by EACH council seat in its per-claim table,
   and every id a seat accepted is in the checkpoint — a Markdown table with header `| id | decision |` (or
   `| Id | Disposition | … |`), a local id read in the ticket. Decisions are read by a **strict whitelist, fail
   closed** (INFRA R06, HQ ruling after Sol recheck 2): the decision cell, trimmed of surrounding spaces / tabs and
   the table pipes and nothing else (no case or Unicode folding, no emphasis removal), must be exactly `ACCEPT`
   (legacy tables: exactly `accepted`, `Accepted` or `ACCEPTED`) to accept, or `NOT-EXAMINED`; any other content
   (`accept`, `**ACCEPT**`, `ACCEPT.`, `accepted (F-1 verified)`, `accepted with non-blocking remarks`, …) is NOT
   accepted and refused with a message naming the claim. The header must be exact (a complete `|`-bounded line, first
   cell exactly `id` / `claim` / `claim id`, second exactly `decision` / `disposition`, case-insensitive, no emphasis or
   extra pipes) and directly followed by a delimiter row (`|---|---|`, optional `:`) of the same width; a header-like
   line that fails this still counts as a table, and all its rows read as NOT accepted. Review files are read raw
   (UTF-8, CRLF and LF the only line ends), so a CR, NEL or U+2028 in the file stays inside the row it splits. The
   table runs from its header to the first blank line and every other line in it must be a complete row: starts and ends with `|`, no escaped pipe, no line / paragraph separator
   (CR, VT, FF, NEL, U+2028, U+2029, …), the header's number of cells, every cell after the decision EMPTY (remarks go
   outside the table). A row continued or split (an incomplete line, a row without an id, a separator inside it)
   makes that row's claim and the previous row's claim NOT accepted; an id listed twice with different readings is
   NOT accepted. No extra checked id, no missing id; a review without such a
   table is refused. An id the seats did not accept may stay in the checkpoint only without a checked label (INFRA
   R06: a NOT-EXAMINED claim that lost its label).
3. **Cited rounds resolve and bind.** Each review round cited in the claim's status line (the line(s) of
   `status_source`, plus the recorded status text itself, which may continue past them) — written `<ROUND>:` or `<ROUND> (<note>):`, ROUND upper-case letters / digits / `-` with a digit,
   e.g. `LC1-A: VERIFIED` — resolves to exactly one file `reviews/<ROUND>_*` of the ticket (`-` read as `_`;
   dispositions, briefs and manifests excluded), and that file quotes the digest of an existing, internally valid
   frozen `reviews/MANIFEST_*.txt` of the ticket (well-formed rows whose digest is the header; an earlier round binds
   to its own manifest, which need not match the current tree). The acceptance round `R<k>` of the council cell resolves to the council seats' review files, which bind to
   the acceptance manifest with a PASS verdict (≥ 8.0, gates PASS) as above. A round named in free text without that
   form is not a citation.

**Seat tables by addendum; carrier files** (INFRA R06, HQ 2026-11-12). A per-claim table may be appended to a council
review file after its `COUNCIL-VERDICT` line as a dated addendum (same seat model, fresh thread, the frozen manifest
and the seat's own review; rows `ACCEPT` / `NOT-EXAMINED` only, no rescoring). The verdict line stays the one binding
outcome: an addendum with a second `COUNCIL-VERDICT` line (same or another digest) makes the review contradictory and
refuses A4. An id listed in the body and the addendum with different decisions is not accepted. When ANY seat's review
of the round has a per-claim table, a checked claim whose status source is NOT its own checkpoint must also be accepted
in a table of EVERY seat's review (a NOT-EXAMINED, unreadable, missing or contradictory id is refused); a council without any table
keeps the cell-only rule. `ingest.py claims <carrier>` reads REGISTRY blocks (`.md`, paths relative to its folder unless
they start with `Theory_work/`) or JSONL (repo-relative paths) from a carrier file anywhere, including outside the
frozen manifest (e.g. `reviews/` or `registry/fragments/`): the carrier itself is never a coverage input, but the
statement, premise and status-source files its rows name are, exactly as above.

**Line endings** (INFRA R06). A text file is the same input on an LF and on a CRLF checkout. `manifest.py freeze`
records the SHA-256 of each file's LF-normalised content (CRLF → LF); `verify` (and so A4) accepts a recorded hash
equal to the SHA-256 of the raw bytes, the LF-normalised or the CRLF-ised content, so manifests frozen earlier on mixed
LF/CRLF trees verify on any uniform checkout with the same verdict as on the frozen tree. This applies only to
EOL-normalisable text (no NUL byte, every CR part of a CRLF pair); any other file (binary, or with a lone CR such as
CR CR LF) is hashed raw only, so no variant of it matches different content (Sol R06FIX F1). Any byte change beyond a
CRLF ↔ LF conversion still fails. The registry fingerprints
(`sha256`, `tex_sha256`, `status_sha256`, the `fp2` artifact digests) were line-wise from their introduction (files read
in text mode and split into lines), so LF and CRLF clones give the same values and no raw-byte value exists to migrate.

**Acceptance record** (finding R04-N1/N2; `events.log`, action `accept`, column `after`):
```
v<version> fp2:<24-hex>
```
The fingerprint (`bvsreg.accept_stamp`) is SHA-256 over the claim's acceptance identity: the row fields `id ticket
kind name file lines premises sha256 version status status_source status_sha256 depends_on consumes assumptions gates
council headline`; the ticket folder that locates the frozen manifest (tickets.tsv `folder`, else the statement file's
folder); the names the claim answers to (id, aliases, name); the EFFECTIVE inputs (each resolved input with its uses,
version, statement hash and status, so an alias edit or a changed input counts); and the content (read line-wise, so
CRLF / LF checkouts agree) of every cited artifact — each gate evidence file (whatever the result), each council
seat's review file and each `reviews/MANIFEST_*.txt` with the council digest — a missing one recorded as MISSING.
At acceptance of a consumer, A5 requires every non-legacy checked input to match a recorded stamp AND to pass the
per-claim acceptance checks (A0-inputs, A1, A2, A3, A4) again on the current tree (memoised), so a change outside
the identity (e.g. reviewed ticket content that breaks the frozen manifest) also refuses the consumer. Legacy-boundary
claims are not revalidated (unchanged boundary; they predate CP3 records).
Migration: records in the earlier format `v<version> fp:<16-hex>` (row strings only) never match an `fp2` stamp; A5
reports them as predating the identity and the input must be accepted again (`check.py --acceptance <id> --record`).
No `accept` event existed on main when the format changed (80e6acd), so nothing needed migrating. The same held when
`status_sha256` joined the identity (INFRA R05, main c8a970f); the claims.tsv column is added on the next write.

### 4.2 Strength gate (sharpness gate) — `lit:`, `necessity:`, `better:`
(a) **Literature comparison** (`lit:PASS(file)`): each assumption and the conclusion compared with Song–Liang (2015)
    and the closest Bayesian variable-selection consistency results (written table: their hypothesis vs ours,
    stronger/weaker/incomparable; literature dominance is a red flag).
(b) **Necessity attempt per assumption** (`necessity:PASS`): for every headline hypothesis, a counterexample without
    it (→ NECESSARY), a route-optimality result (→ NECESSARY-FOR-ROUTE), or a written reason it is a proof artefact
    (→ ARTEFACT, which keeps the claim `improvable`). Recorded in `sharpness.tsv`; the binding map says where each
    assumption is forced.
(c) **"Better theorem" review** (`better:PASS(file)`): one fresh strongest reviewer (Codex gpt-6-astra high, or
    Claude at effort high) receives only the statement, the assumption entry map and the binding map, and is asked
    *only* to propose a strictly better provable statement (weaker hypothesis, stronger conclusion, wider scope,
    better rate) with a proof sketch. PASS = no credible better statement. Each credible proposal is recorded in
    `gates` as `better-proposal:<label>(<review file>)` and, once HQ decides, `better-disposition:<label>=<declined|
    adopted|ticket|remark>(<evidence: DECISIONS.md entry / ticket / new statement version>)`; repeat the review after a
    substantial statement change. Otherwise the proposal goes to HQ as a
    candidate improvement ticket.

### 4.3 Early sub-par signals (checked in the sharpness gate, the binding map and CI)
- **boundary-violation numerics**: simulate just outside each assumption; if the conclusion still holds → improvable
  (CI runs these: `ci/falsification.tsv kind=boundary`).
- **artefact thresholds**: exponents/constants obtained by balancing crude bounds (e.g. 1/6, 17/2).
- **single-use assumptions** that enter only through one union / worst-case bound.
- **family-named hypotheses** ("compound symmetry", "AR(1)"): restate as the property the proof uses (P:*).
- **literature dominance**: a published result already proves more under less.
- **prover divergence**: independent provers needed different/extra hypotheses for the same step.
- **unharvested conclusions**: rates or uniformity proved inside the proof but not stated.
Before heavy proving, each ticket writes a one-page **assumption map** (`ASSUMPTION_MAP.md`, Wave 3 protocol item 3) (`templates/ASSUMPTION_MAP.md`):
for every hypothesis, where it enters, how (bound/mechanism), and which signal applies.

## 5. Strength changes: candidates, supersession, coexistence

### 5.1 Candidate stage and assurance parity
A new result Y that may replace X enters as `CANDIDATE` (`registry.py add … --state CANDIDATE`). Work on X continues
until Y has passed **the same gates X passed** (correctness pipeline + strength gate); then
`propagate.py promote Y --parity-with X`. Every improvement ticket has a **kill budget** (proof attempts, agent time
or one wave; `tickets.tsv kill_budget`); on expiry the attempt is recorded with `propagate.py fail-route` (it becomes
FAILED-REMOVAL evidence) and the ticket stops.

### 5.2 The partial order
Y vs X per axis — assumptions (via the assumption lattice), conclusion (level), scope, rate:
`registry.py compare X Y [--axes scope=better,rate=equal]`. Y **dominates** X if it is at least as good on every
axis the paper uses and better on one; **incomparable** otherwise.

### 5.3 Decision rule (HQ, 2026-11-09)
| class | condition | action |
|---|---|---|
| **free** | interface-level implication Y ⇒ X recorded (`implies`) and verified | SUPERSEDE at the next quiet point. Dependents of X keep pointing to X (still true); re-points to Y are **proposed** in `repoints.tsv` and applied only after a cheap check that the used fact survives (`propagate.py confirm-repoint D --from X --to Y --checked-by …`). |
| **headline-changing** | X is a headline, Y does not imply X | SUPERSEDE once Y's key new step is independently checked (`--key-step-checked <evidence>`); Felipe approves. X → SUPERSEDED-VALID; direct dependents → REBASE-NEEDED (still true; one issue each with the exact hypothesis/conclusion diff). |
| **internal-only, not free** | X is not a headline and Y does not imply X | log as a remark (`propagate.py remark X --by Y`); no rebuild. |
| **incomparable** | neither dominates | COEXIST (`propagate.py coexist X --with Y`): X and Y are kept as **parallel theorems** (X is a corollary / special case of Y only if that restricted implication is proved and recorded in `implies`). Tie-break for which one the paper leads with: **design-agnosticism > range of p > rate > constants**. |
| declined | Y not worth the price | `propagate.py decline X --by Y --reason R` |

**Dispatch order.** (1) Is Y ACTIVE and at assurance parity, and is X ACTIVE? If not, nothing happens (Y stays
CANDIDATE). (2) Is Y ⇒ X recorded and verified? → free. (3) Otherwise compare axes: strictly better on some axis
and no worse on any → headline-changing (X headline) or internal-only (X not headline); equal → decline / remark;
incomparable → coexist; worse → decline. `propagate.py` enforces (1)–(3), including strict improvement.

**Reversibility.** A SUPERSEDED-VALID claim is still a true claim: correctness changes upstream reach it like any
other claim (it can become SUSPECT while keeping `superseded_by`). If Y is later retracted, every claim it
superseded that is still SUPERSEDED-VALID is restored automatically (→ ACTIVE); one invalidated meanwhile is not.
Confirmed re-points to Y are undone onto the latest VALID source in that dependent's re-point chain (normally the X it came from); a link that a later re-point already moved on is left alone; if no source in the chain is valid, the dependent keeps its edge to Y and is invalidated with it (transitively). An edge to Y that existed independently before the re-point is always kept. Re-point proposals record the versions of X and Y;
a confirmation against changed versions is refused, and REBASE-NEEDED is lifted only when every open proposal for
that dependent is resolved.

**Freeze.** When every headline hypothesis is settled (NECESSARY or ≥ 2 documented failed removal routes) and the
latest strategy review + adversarial round produced no headline-changing candidate, Felipe sets the freeze with
`registry.py freeze --set --reason …`, which refuses unless the criterion holds: each unsettled hypothesis needs
≥ 2 FAILED-REMOVAL rows whose evidence is a readable `path:line` (distinct by path:line; `propagate.py fail-route`
enforces the format), and `config.tsv` keys `last_strategy_review` and `last_adversarial_round` must name review
files containing the attested line `FREEZE-OUTCOME: no headline-changing candidate`. The outcome itself remains a
human attestation (HQ / Felipe); the tool only checks that it is recorded. `check.py` raises an ERROR if
`freeze=yes` while the criterion fails. Failed routes are procedural stopping evidence, not mathematical necessity.
While frozen, a new headline can only be promoted as a free replacement (it implies its reference claim).
After freeze only correctness rollbacks and free supersessions are allowed (`propagate.py` enforces it).
`check.py` reports the freeze criterion per headline (S8).

### 5.4 Decision log
Every supersede / coexist / decline / remark decision and every failed sharpening attempt goes to `DECISIONS.md`
(`propagate.py` appends automatically; add the human rationale in the PR).

## 5.5 What the tools enforce vs what people attest
Machine-enforced: statement + premise hashes; verbatim status at its source line (+3 lines; a status negated at its
source, e.g. "Not PROVED-CHECKED", is an ERROR); no status upgrade through any tool (`--status` only on
downgrade / retract / deprecate, source-backed and never stronger); use-level propagation, including explicitly bound
bridges (`P:X@id`) and transitive invalidation after reverts; lifecycle invariants (no valid claim on an invalid
input without an ack in the routine check; `clear` refuses while a consumed claim is not ACTIVE — an ack never
suffices — or a re-point proposal is open, and returns a replaced claim to SUPERSEDED-VALID); CANDIDATE → ACTIVE only against a reference claim with evidence-bearing
`k:PASS(evidence)` gates (one parser for every operation); supersede / coexist validity, strict dominance, gate
parity, proved incomparability (all axes declared) for coexist, freeze; re-point confirmation only against the
versions it was proposed for; retraction restores each dependent onto the latest VALID source in its re-point chain
(or leaves it on the retracted claim and invalidates it); freeze evidence format; all-or-nothing ingestion with the
full schema and a staged check that includes acceptance; tombstones verified at their archive tag; atomic
`rollback-ticket`, validated on the proposed post-revert tree, with dependents' premise spans kept at the archive;
CP3 acceptance (A0–A5: consumed claims ACTIVE, every gate / proposal / disposition evidence file exists,
correctness evidence and a dual-pass council record for every checked claim whose digest is a frozen manifest of the
ticket that still verifies and whose review files each carry one matching PASS `COUNCIL-VERDICT` line, strength
gates, proposal dispositions, assurance of direct inputs, conditional statuses carried downstream, a durable
acceptance record — or legacy-boundary row — for every checked claim consumed transitively); the legacy boundary
recomputed from its tag; `--consumed-vs` comparison with main; crash-safe multi-file transactions: the journal
`registry/.TXN_INPROGRESS` (backup locations) is written and fsynced before the first replacement and removed only
after the last, so a killed writer — or a failed restore (`registry/.TXN_FAILED`) — locks every tool (`manifest.py` included) and check.py
until `bvsreg.py recover` rolls the files back (restartable). (Single-file writes — `save_claims` followed by an
events.log append — are each atomic but not one transaction.)
Attested by HQ / Felipe in the PR (with the review files linked): that the reviews named in `gates` / `council`
examined the current statement version and say what the record claims (the tools check the files exist,
the frozen manifest still verifies, and each review's machine-readable verdict line matches the record — not that the
prose supports the verdict); that the manifest's INPUTS list is complete; reviewer
independence; that an `implies` edge is mathematically right; that a narrowing still covers the listed uses; the
binding-map mechanisms; that a premise declared `@hyp` (A3 exemption) is really stated as a hypothesis in the statement text;
that a proposal disposition is justified. The binding map and sharpness rows seeded on 2026-11-09 are DRAFTS until a headline's
strength gate confirms them.

## 6. Pricing a change
`propagate.py <op> … --dry-run` prints the rebuild cost in review units: for each direct dependent that must be
re-proved, 1 proof session + 1 cross-family lemma check; 1 sweep per ticket touched; 1 council + 1 strength gate per
dependent headline; paper regeneration (`assemble.py`) is free. A free supersession costs one cheap re-point check
per direct dependent.

## 7. Method pinning
Each claim about the method pins `method_commit` and the `method_components` it relies on
(`method_components.tsv` maps a component to code paths). `check.py` (M1) warns when a pinned component changed
after the pin: that is a **rollback trigger** — HQ re-checks the claim's implementation premises (code-reading audit
or the ticket's tests), then either re-pins (`registry.py set ID method_commit=<new> --reason …`) or opens a
`suspect` / `downgrade`.

## 8. Continuous review
`ci/run_ci.py` (see `ci/README.md`; scripts run only inside a disposable git worktree of HEAD, never in a working
checkout): registry check, paper freshness, cheap falsification re-runs and
boundary-violation numerics, citation re-checks, and one random PROVED-CHECKED claim per run for a fresh adversarial
re-audit. The **optimizer** step is event-triggered only (wave boundary, newly landed technique, new strategy-review
proposal): it picks one binding claim of an unsettled headline hypothesis and writes an improvement-ticket brief
priced in re-proof + re-review. HQ decides what to launch.

## 9. GitHub workflow
- Each ticket works on branch `theory/<ticket>` and opens one PR to `main` with `.github/pull_request_template.md`
  (statement, verbatim status, review trail, council scores, registry diff, dependencies touched, strength fields).
- Council pass = PR approval. All agents share the owner's GitHub account, which cannot approve its own PR, so HQ
  records the council pass as the label `council-pass` plus a PR comment quoting both scores and the review files.
- HQ merges (merge commit, no squash, so `git revert -m 1` can undo a ticket cleanly).
- Labels: `theory`, `lemma-gap`, `retraction`, `suspect`, `sim-request`, `strategy`, `editorial`, `major-claim`,
  `council-pass`, `improvement`. Issue templates in `.github/ISSUE_TEMPLATE/`.
- Repair issues are generated by `propagate.py --gh`; do not open issues by hand for SUSPECT dependents.

## 10. Paper assembly
`tools/assemble.py` regenerates, from the registry, the theorem-statement blocks (`paper/generated/blocks/<id>.tex`),
status boxes with verbatim statuses, and the provenance, dependency and strength tables. Prose stays hand-written and
`\input`s the blocks. A superseded claim's block renders its replacement; SUSPECT / REBASE-NEEDED / CANDIDATE inputs
show a visible flag. A claim gets a LaTeX statement by setting `tex=<path>:<a-b>` (e.g. a span in
`Wave1C/FINAL/sections/*.tex` or a file under `INFRA/paper/statements/`).

## 11. Quick reference
```
python Theory_work/INFRA/tools/check.py [--quiet] [--only C,M,S]
python Theory_work/INFRA/tools/check.py --acceptance ID [ID ...] [--record]  # CP3: blocking gates + assurance
                                                                           # --record: accept events on a PASS
python Theory_work/INFRA/tools/check.py --consumed-vs origin/main --tickets T   # continuation / merge (rule 11)
python Theory_work/INFRA/tools/ingest.py claims REPORT.md|F.jsonl [--staged [--record] | --apply]   # --staged
                                     # runs acceptance; --staged --record commits ingest + accept events on a PASS
python Theory_work/Wave3/tools/manifest.py bind <ticket>/reviews/MANIFEST_R<k>.txt <reviews...> [--council "<cell>"]
python Theory_work/INFRA/tools/propagate.py rollback-ticket T --archive TAG --merge M --reason R [--apply]
python Theory_work/INFRA/tools/bvsreg.py recover [--dry-run]    # only if registry/.TXN_INPROGRESS or .TXN_FAILED
                                                                 # exists (tools refuse); safe to re-run
python Theory_work/INFRA/tools/registry.py show|deps|rdeps|compare|sets|assumption-impact|stats ...
python Theory_work/INFRA/tools/propagate.py <op> ID ...          # dry run (default)
python Theory_work/INFRA/tools/propagate.py <op> ID ... --apply  # write
python Theory_work/INFRA/tools/assemble.py [--check]
python Theory_work/INFRA/ci/run_ci.py [--steps ...] [--event wave-boundary --note "..."]
```
