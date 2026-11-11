# ASSUMPTION_MAP.md — <TICKET> (Wave 3 protocol item 3; one page, written after the statement lock, before heavy proving)

Target statement: `STATEMENT.md` vX.Y, claim id `<TICKET>:<local_id>`. Rules: `Theory_work/INFRA/LIFECYCLE.md` §4.3.

| hypothesis (A:/P: id, or new) | where it enters (lemma / step) | how (bound or mechanism) | property actually used (P:*) | necessity evidence so far | early sub-par signal? |
|---|---|---|---|---|---|
| A:… | L2 step 3 | union bound over the lattice | P:… | none / Prop … / failed route … | single-use-union-bound / artefact-threshold / family-named / boundary-numerics / literature-dominance / prover-divergence / unharvested-conclusion |

Conclusion level (identity < target < posterior < reported-model < delivery): …; rate: …; scope (p range; design
class; law): …

Unharvested conclusions (rates / uniformity the proof gives but the statement does not state): …

Boundary-violation numerics planned (simulate just outside each assumption; add to `ci/falsification.tsv` with
`kind=boundary`): …

Closest literature result and how ours compares (Song–Liang 2015 and …): …

---
## Registry block for the final REPORT.md (Wave 3 protocol item 7) — copy, fill, keep the format

```
REGISTRY
claim: <TICKET>:<local_id> | kind: theorem | statement: STATEMENT.md:a-b | premises: STATEMENT.md:c-d
status: <verbatim> | status_source: REPORT.md:<line>
assumptions: A:… ; A:… (new ones: id | name | statement | source | shared yes/no | bridge lemma)
consumes: P:… ; P:…
conclusion: <identity|target|posterior|reported-model|delivery|negative>: <text> | rate: … | scope: …
depends_on: <id>@stmt ; <id>@proof:<fact> …
implies: <existing registry ids this statement implies, each with a one-line reason>
sharpness: A:… = NECESSARY|NECESSARY-FOR-ROUTE|FAILED-REMOVAL|ARTEFACT|WEAKENABLE|NONE (evidence: file:line)
binding: A:… forced by <claim id> via <mechanism> [signals]
gates: correct:PASS(<council files>) ; lit:… ; necessity:… ; better:PASS(<review file>)
council: R<k>; MANIFEST <64-hex digest>; sol=<score> PASS(reviews/<sol review>.md); opus=<score> PASS(reviews/<opus review>.md)
```

Rules the CP3 acceptance check enforces on this block (LIFECYCLE §4, §4.1):
- Fields are `name:` followed by zero or more spaces. Every non-blank line inside the fence must be fields.
- Every `PASS(<evidence>)` names an existing file (paths relative to this folder or the repository root;
  `file@<commit>` pins it).
- A PROVED-CHECKED status needs the `council:` line of the ONE passing round: both seats ≥ 8.0 with all gates PASS,
  the digest of the round's frozen manifest `reviews/MANIFEST_R<k>.txt` (which must still pass `manifest.py verify`
  on the final tree), and two review files that each contain exactly one line
  `COUNCIL-VERDICT round=R<k> manifest=<digest> seat=<seat> score=<x.y> gates=PASS` matching this `council:` line
  (and no other COUNCIL-VERDICT line). `manifest.py bind reviews/MANIFEST_R<k>.txt <both reviews>` prints the
  `council:` value to copy. Quoting the digest in prose is not a verdict.
- Every gate evidence — FAIL / PENDING entries, `better-proposal` and `better-disposition` included — names an
  existing file.
- Every PROVED-CHECKED claim this result consumes (transitively) must itself have been accepted
  (`check.py --acceptance <id> --record`) or be in `INFRA/LEGACY_ACCEPTED.tsv`.
- A premise below PROVED-CHECKED is used only as `depends_on: <id>@hyp`, named in the statement, with
  `conditional on <id or name>` in the status; every checked result that uses this one carries the same condition.
