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
```
