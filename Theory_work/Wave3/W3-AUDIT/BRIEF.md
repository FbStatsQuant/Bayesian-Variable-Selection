# W3-AUDIT: are our assumptions reasonable? (HQ brief, 2026-11-16; owner direction)

**Owner, 11-16:** "That would be the first question we will receive and we should try to solve it beforehand."

Owner: Theory Department, which leads. Writing presents the result in the advisor report. Engineering supplies NOTS
time for track C. Start at the resume, as the first priority after the in-flight recordings.

## Scope: the core theorems (main text, HQ decision 11-16)
| | Core theorem | Rows |
|---|---|---|
| 1 | The posterior finds the true model | 1.1, 1.2 |
| 2 | The posterior finds the true distribution | 2.1 (Thm 9) |
| 3 | The coded algorithm reports the true model | 3.1 |
| 4 | The run's estimates are consistent | 3.6, + 3.5 |
| 5 | The rate cannot be improved (remark) | 1.3 |

Everything else goes to the supplement with a one-line "why it matters", or is cut. Writing restructures accordingly.

## Track A: assumptions on mathematical objects (owner: must be known or proved)
For every assumption of the core theorems that concerns a distribution, divergence, prior property, kernel or
algorithm property (not the data):
- list it, with its source;
- give its status: proved-and-checked (cite the claim), proved-unchecked, or missing;
- close the gaps with small lemmas, checked as usual (Tier A/B per PROTOCOL_v4);
- tag each one as a Lean target (the SMC - Lean Department, launching about Thu 11-19).

## Track B: assumptions on the design and data (owner: explained, not necessarily proved)
For each design-side assumption, produce a reasonableness dossier for the advisor report:
1. **Plain meaning,** with a small example.
2. **Song & Liang (2015) as the reference point**, checked against the paper. Is our assumption the same as theirs,
   weaker, comparable, or stronger? Where it is the same or weaker, the owner treats it as a "blank check". Also
   compare it with standard conditions where useful (restricted eigenvalue, sparse Riesz, etc.).
3. **Where it holds**, with a proof or citation where one exists (W2-APP and W2-FAC results first), and **where it
   fails** (strong factors, and so on).
4. **Our simulations:** each design of the 2,400-fit study, P6 and the 1M experiment, with a reasoned "inside",
   "outside" or "unclear". Also whether a typical user is plausibly inside.
5. **Candidate corollaries:** one per core theorem, stated only in primitive terms (Σ, β, σ², n, p) for standard
   random designs, where provable.

**Length and form (owner, binding: "precise and concrete arguments / evidence, not pages upon pages").**
- At most about half a page per assumption in the report.
- Lead with a one-line verdict: "same as Song–Liang (their (4))", "weaker than …", or "holds for designs X, Y (Prop …); fails for Z".
- Then the single strongest piece of evidence: an exact citation with its equation number, a proved proposition,
  or one concrete example or counterexample.
- No surveys and no hedging paragraphs. The whole track-B section is 3–5 pages, plus one summary table
  (assumption × Song–Liang comparison × our designs).

## Track C: light empirical check (internal only; not for the paper)
Simulations across many design types (IND, AR, block, Toeplitz, factor of several strengths, real-data-like
designs), tracking computable proxies of the design assumptions: sparse eigenvalues on small sets, visibility and
leakage-set sizes, local-regression margins, and so on, with n and p growing.
- The question is whether the data look inside the assumptions, and whether that improves with n.
- Small budget: ≤ 150 core-h on NOTS through Engineering, or Owls for small runs. Pre-announce the plan to HQ.

## Output and timing
- `Theory_work/Wave3/W3-AUDIT/AUDIT.md`: one table per core theorem, giving each assumption, its track (A/B), its
  status or dossier, and the Song–Liang comparison.
- A first version within about 3 working days of the resume. Track A lemmas and the corollaries follow as tickets.
- Writing drafts the advisor-report section from it.
- **Freeze:** the Fri 11-20 freeze stands for the statements already recorded. The audit adds lemmas and corollaries
  after it. If an assumption is found unreasonable or false, it goes through the usual correctness route
  (SUSPECT/NARROW).
