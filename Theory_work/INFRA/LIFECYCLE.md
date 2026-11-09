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
- `state` (lifecycle, added by INFRA): `ACTIVE`, `CANDIDATE` (new result not yet at assurance parity),
  `SUSPECT` (an input is in doubt), `REBASE-NEEDED` (still true, but built on a superseded input and scheduled to be
  rebuilt), `NARROWED` (statement narrowed in place, dependents being checked), `RETRACTED`, `DEPRECATED`,
  `SUPERSEDED-VALID` (replaced by a better theorem, still true, restored automatically if the replacement falls).
- `depends_on`: **use-level edges** `id@use`, where `use` is `stmt` (the statement; default), `stmt:<clause>`, or
  `proof:<fact>` (an event, rate, constant or lemma inside the other claim's proof). Propagation follows use-level
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
ACTIVE --retract--> RETRACTED                   (dependents SUSPECT; what it superseded is restored)
ACTIVE --deprecate--> DEPRECATED                (dependents SUSPECT; FAILED_ROUTES.md)
ACTIVE --supersede (by Y)--> SUPERSEDED-VALID --(Y retracted)--> ACTIVE
SUSPECT / REBASE-NEEDED --clear or confirm-repoint--> ACTIVE
```

## 3. Correctness rollbacks

Always run the operation with `--dry-run` first and attach its impact report to the issue / PR.

| level | trigger | statement | command | who |
|---|---|---|---|---|
| **PATCH** | a proof gap was found AND repaired (repair lemma-checked); the statement stands | unchanged | `propagate.py patch ID --reason R` (only `@proof:` dependents SUSPECT) | HQ |
| **DOWNGRADE** | evidence weaker than recorded (review withdrawn, gate failed) | unchanged | `propagate.py downgrade ID --status "<new verbatim>" --reason R` | HQ (Felipe for headline) |
| **NARROW** | statement too strong; a narrower one holds | edited in place | edit the statement → `propagate.py narrow ID --still-covers "stmt:(a);proof:E_n" --reason R` (owns the major bump) → `registry.py rehash ID --bump none --reason "narrowed text"` | Felipe (headline) / HQ |
| **RETRACT** | statement false | kept for history | `propagate.py retract ID --reason R` | Felipe (headline) / HQ |
| **DEPRECATE** | wrong target / dead route | kept, archived | `propagate.py deprecate ID --reason R` + archive branch + tag | Felipe (headline) / HQ |
| SUSPECT / CLEAR | possible gap / repair done | — | `propagate.py suspect ID` / `propagate.py clear ID` | HQ |

An OPEN proof gap (not yet repaired) is not a PATCH: mark the claim `suspect` (statement users become SUSPECT
too) or `downgrade` it, and PATCH only once the repair is checked.

Each SUSPECT dependent gets a repair issue (one per ticket, `--gh` creates them): re-check the step that uses the
upstream claim; PATCH and `clear` if it survives, else narrow/retract and propagate further.

**Git for each level** (never rewrite `main`; never force-push):
1. Before a RETRACT / NARROW / DEPRECATE / SUPERSEDE of a headline, tag the current state of the claim:
   `git tag -a claim/<id-with-:-as-_>/v<version> -m "<reason>" <commit>` (e.g. `claim/W2-FAC-A_Thm-FAC-L/v1.0.0`).
2. Work on `theory/<ticket>-<op>` (e.g. `theory/W2-FAC-A-narrow`), commit the statement edit + registry change +
   `issues/…/00_impact.md`, open a PR with the template, label `retraction` (+ `major-claim` for headlines).
3. To undo a *merged* wrong change: first price it on the CURRENT graph (`propagate.py retract|narrow … --dry-run`
   on the claims the merge introduced or changed — later work may depend on them), then `git revert -m 1
   <merge-commit>` on a branch, then apply the propagation the dry run showed for the dependents added after the
   merge, and `check.py`, all in one PR. Do not hand-edit `claims.tsv` state fields — use `propagate.py`.
4. DEPRECATE: `git branch archive/<ticket> <last commit of the route>` and `git tag -a deprecated/<ticket> …`, push
   both; add a `DEPRECATED` banner at the top of the ticket's REPORT.md via the PR; the route goes to
   FAILED_ROUTES.md (written by `propagate.py deprecate`).
5. Releases of the theory state: annotated tags `theory-vMAJOR.MINOR[-pre]` (e.g. `theory-v2.0-pre`) after HQ
   approval; the tag message lists `check.py` counts and the headline set.

## 4. Gates

A claim enters the paper headline only after BOTH gates; they are separate reviews with separate reviewers.

### 4.1 Correctness gate (`correct:PASS(...)`)
The wave protocol: statement lock → lemma-by-lemma falsification numerics + cross-family line check → mid-point →
exhaustive sweep → council (Codex Sol high + Claude Opus high, both ≥ 8.0, all gates PASS). On GitHub, the council
pass is the PR approval (§9).

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
    better rate) with a proof sketch. PASS = no credible better statement; otherwise the proposal goes to HQ as a
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
Confirmed re-points to Y are reverted exactly (the recorded `before` edge is put back; an edge to Y that existed
independently before the re-point is kept, so that dependent is still invalidated by Y's retraction); a dependent
restored onto an input that is no longer valid becomes SUSPECT. Re-point proposals record the versions of X and Y;
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
input without an ack; `clear` refuses while an input is invalid or a re-point proposal is open, and returns a
replaced claim to SUPERSEDED-VALID); CANDIDATE → ACTIVE only against a reference claim with evidence-bearing
`k:PASS(evidence)` gates (one parser for every operation); supersede / coexist validity, strict dominance, gate
parity, proved incomparability (all axes declared) for coexist, freeze; re-point confirmation only against the
versions it was proposed for; retraction restores each dependent onto the latest VALID source in its re-point chain
(or leaves it on the retracted claim and invalidates it); freeze evidence format. Attested by HQ / Felipe in the PR
(with the review files linked): that the reviews named in `gates` examined the current statement version; reviewer
independence; that an `implies` edge is mathematically right; that a narrowing still covers the listed uses; the
binding-map mechanisms. The binding map and sharpness rows seeded on 2026-11-09 are DRAFTS until a headline's
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
python Theory_work/INFRA/tools/registry.py show|deps|rdeps|compare|sets|assumption-impact|stats ...
python Theory_work/INFRA/tools/propagate.py <op> ID ... --dry-run
python Theory_work/INFRA/tools/assemble.py [--check]
python Theory_work/INFRA/ci/run_ci.py [--steps ...] [--event wave-boundary --note "..."]
```
