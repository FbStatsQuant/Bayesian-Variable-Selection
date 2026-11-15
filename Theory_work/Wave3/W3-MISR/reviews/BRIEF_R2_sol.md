# BRIEF R2 — council (short re-round), seat `sol`: Sol (codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are one of two independent council seats for ticket W3-MISR (Theory Wave 3), round R2. Score the proof package
as it now stands. You are briefed to **break** it, not to confirm it. Repository root = your working directory.
Read-only, with two exceptions: your single output file, and an optional scratch folder
`Theory_work/Wave3/W3-MISR/reviews/R2_scratch_sol/`. Do not create, edit or regenerate any other file (nothing inside
`Theory_work/Wave3/W3-MISR/` outside `reviews/`: the content is frozen). No git state changes. No subagents.
Do **not** read: any other file under a `reviews/` folder (of this or any ticket) except `reviews/CITECHECK.txt`;
any `LOG.md`, `PLAN.md`, `CHECKPOINT_*.md`; `REPORT.md` §2 ("Review trail"); anything under `Theory_work/Wave3/API_AUDIT/`.

## Why this round is short, and how to work efficiently
The package is a revision (STATEMENT v1.3) of a version frozen at commit `2f360ed` (STATEMENT v1.2). The revision is
meant to contain only wording, bookkeeping and numerics-description changes, plus one clause (§3(a)) restated over
the class its proof uses. You judge the **new** package on its own; but to spend your effort where it matters:
1. Read the diff first (read-only git): `git diff 2f360ed -- Theory_work/Wave3/W3-MISR/STATEMENT.md Theory_work/Wave3/W3-MISR/lemmas Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md Theory_work/Wave3/W3-MISR/numerics Theory_work/Wave3/W3-MISR/REPORT.md`.
   For every changed line decide: is it correct, and does it change a hypothesis, a conclusion, a proof step, a premise
   or a code pin? Does anything that depends on it still hold?
2. Then read `STATEMENT.md` and the three lemma files once in full (they are short) and give the six gate verdicts for
   the whole package. Open the sources only for the lines you need. Targeted reads; do not paste long files.

## Package
- `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.3): Lemma R′ (a), (a′), (a″), (b), (c); Theorem MIS-R (i), (i′) (a)–(d),
  (ii) (a)–(c); Corollaries G(a), G(b), H; Remarks SNR, P, U.
- `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md`, `M_misr.md`, `G_corollaries.md` — the proofs.
- `Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md`, `Theory_work/Wave3/W3-MISR/numerics/` (falsification and boundary evidence
  only, never a proof), `Theory_work/Wave3/W3-MISR/REPORT.md` (§1, §3–§7), `Theory_work/Wave3/W3-MISR/reviews/CITECHECK.txt`.

## Sources to check against
`Theory_work/Wave3/W3-POST/STATEMENT.md`; `Theory_work/Wave3/W3-POST2/STATEMENT.md` and
`Theory_work/Wave3/W3-POST2/lemmas/{A_occam,B_tail_approx,C_expectation,D_hellinger,E_visibility}.md` — the W3-POST2
claims (A0, A1, B, C, D, E) are **declared hypotheses** of this ticket: do not re-audit their proofs, but check that
they are used exactly as stated or as their proof files literally give; `Theory_work/Wave1C/C-MIS/STATEMENT.md`,
`Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L4_theoremF,L5_frontier,L6_null}.md`;
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`,
`…/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/{T03_A2_selection_consistency/PROOF_v2.tex,T01_T02_contrast_dimension/PROOF_v3.tex}`;
code `Scripts/SMC_BVS/core/{v3_preprocess.R,v3_fit.R,v3_setup.R,cpp/v3_score.h,cpp/v3_core.cpp}`;
registry statuses, if you want to check a quotation: `Theory_work/INFRA/registry/claims.tsv` (columns id, status).

## Context (two lines)
The project's Bayesian variable-selection posterior is run on a candidate subset of the columns; the omitted columns
make the candidate model misspecified. The ticket claims that an exact scale invariance of the coded posterior removes
version 1's fixed-variance requirement and reduces the problem, in signal-to-noise form, to the theorems of W3-POST2.

## Gates (each PASS / FAIL, with reasons and file:line evidence)
1. **Correctness** of every step (invariance, reduction in law, projective form and total-variation bound, MIS-R (i),
   the per-n expectation assemblies of (i′) (a)–(d) — in particular (a) over the class 𝒦⁰′_n with its own threshold —
   the conditioning arguments of (ii), Corollaries G and H, Remarks SNR, P, U).
2. **Hypotheses used = hypotheses stated** (class definitions incl. 𝒦⁰′_n, "at that n", which (OS) inequality, margins).
3. **No hidden assumptions.**
4. **Cited inputs**: statuses quoted verbatim, nothing upgraded; inputs used as stated; "conditional on …" complete.
5. **Constants / rates / thresholds** tracked (free of the variance; what each threshold depends on; c″; C_H).
6. **Fidelity to the method as coded** (R′(a″), R.3 and the numerical observation).
Also judge: every number quoted from `numerics/` against the output files; any overclaim relative to Song–Liang (2015)
§2.3 or to C-MIS; whether the "Not claimed" list is honest; whether the revision introduced anything substantive that
is wrong or unproved.

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/R2_council_sol.md`: the six gate verdicts; a verdict on the diff (every
change correct? any change that alters a hypothesis, conclusion, proof step, premise or code pin, and is it right?);
numbered findings graded FATAL / MAJOR / MINOR / NIT with file:line evidence and the exact fix; an overall **score
from 0.0 to 10.0** (one decimal; pass mark 8.0 with all gates PASS); and the verdict line below.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103` (round R2, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103 seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---
Your final chat message: the six gate verdicts, the counts of findings per grade, and your score.
