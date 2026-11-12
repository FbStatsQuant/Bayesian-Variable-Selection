# BRIEF R1 — council, seat `opus`: Opus (Claude Opus 5.5 on Claude Work, effort high) — blind first read

You are one of two independent council seats for ticket W3-MISR (Theory Wave 3). Score the finished proof package.
You are briefed to **break** it, not to confirm it. Repository root = your working directory.
Read-only, with two exceptions: your single output file, and an optional scratch folder
`Theory_work/Wave3/W3-MISR/reviews/R1_scratch_opus/` for your own computations. Do not create, edit or regenerate any
other file (in particular nothing inside `Theory_work/Wave3/W3-MISR/` outside `reviews/`: the content is frozen).
No git state changes. No subagents.
Do **not** read: any other file under a `reviews/` folder (of this or any ticket) except `reviews/CITECHECK.txt`;
any `LOG.md`, `PLAN.md`, `CHECKPOINT_*.md`, `REPORT.md`; anything under `Theory_work/Wave3/API_AUDIT/`.

## Package (read all of it)
- `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.2) — the claims: Lemma R′ (a), (a′), (a″), (b), (c); Theorem MIS-R (i),
  (i′) (a)–(d), (ii) (a)–(c); Corollaries G(a), G(b), H; Remarks SNR, P, U.
- `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md`, `M_misr.md`, `G_corollaries.md` — the proofs.
- `Theory_work/Wave3/W3-MISR/ASSUMPTION_MAP.md` and `Theory_work/Wave3/W3-MISR/numerics/` (scripts and outputs:
  falsification and boundary evidence only, never a proof); `Theory_work/Wave3/W3-MISR/reviews/CITECHECK.txt`.

## Sources to check against (open them; verify every citation you rely on)
- `Theory_work/Wave3/W3-POST/STATEMENT.md` (the coded target π; Theorem 1; hypotheses).
- `Theory_work/Wave3/W3-POST2/STATEMENT.md` and `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,B_tail_approx,C_expectation,D_hellinger,E_visibility}.md`.
  The W3-POST2 claims (A0, A1, B, C, D, E) are **declared hypotheses** of this ticket ("conditional on …" in each
  status): do not re-audit their proofs for correctness, but do check that this ticket uses them exactly as stated or
  as their proof files literally give (hypotheses, "at that n", thresholds, what the constants depend on).
- `Theory_work/Wave1C/C-MIS/STATEMENT.md`, `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L4_theoremF,L5_frontier,L6_null}.md` (version 1).
- `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`;
  `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`
  and `…/T01_T02_contrast_dimension/PROOF_v3.tex` (locked older proofs).
- Code: `Scripts/SMC_BVS/core/v3_preprocess.R`, `v3_fit.R`, `v3_setup.R`, `cpp/v3_score.h`, `cpp/v3_core.cpp`.

## Context (two lines)
The project's Bayesian variable-selection posterior is run on a candidate subset of the columns; the omitted columns
make the candidate model misspecified. Version 1 (C-MIS) required fixed noise and omitted-part variances. This
ticket claims that an exact scale invariance of the coded posterior removes that requirement, and reduces the
misspecified problem, in signal-to-noise form, to the well-specified theorems of W3-POST2.

## Gates (each PASS / FAIL, with reasons and file:line evidence)
1. **Correctness** of every step: the invariance and equivariance; the reduction in law; the projective form and the
   total-variation bound; MIS-R (i) and its consequences; the per-n expectation assemblies of (i′) (a)–(d); the
   conditioning, slicing and tight-constants arguments of (ii); Corollary G (both parts); Corollary H and its
   reference-law paragraph; Remarks SNR, P (including the Theorem F table and the counterexample), U.
2. **Hypotheses used = hypotheses stated** (class definitions, "at that n", (SZ), which (OS) inequality, the margin
   and its coordinate form, (GR^c ∣ 𝓕_n), the population conditions of G(b), regimes of the transferred claims).
3. **No hidden assumptions** (measurability, non-constancy, uniqueness of β, tie rules, p random, design columns,
   σ² = 0, the intercept, anything about floating point).
4. **Cited inputs**: statuses quoted verbatim and nothing upgraded; every W3-POST2 / C-MIS input used as stated; the
   "conditional on …" statuses of the lemma files are complete for what each proof uses.
5. **Constants / rates / thresholds** tracked: constants free of the variance; what n₀, n₀′, C, C′ depend on; the
   arithmetic turning each term into ≤ const·r_n; c″ ≥ cn/(n − 1); C_H at unit variance; O(1/n) bad events in G(b).
6. **Fidelity to the method as coded**: is the target of the statement the one the code scores (standardisation of
   the response, the constant IG rate on the standardised scale, nothing on the raw scale reaching a score, a prior
   or a branch decision)? Is R′(a″) accurate line by line, and is its numerical observation described correctly?
Also judge: any overclaim relative to Song–Liang (2015) §2.3 (Theorem 4, Corollary 2) or to C-MIS; whether the
"Not claimed" list is honest; whether any clause is vacuous or weaker than it looks.

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/R1_council_opus.md`: the six gate verdicts; numbered findings graded
FATAL / MAJOR / MINOR / NIT, each with file:line evidence and the exact fix; an overall **score from 0.0 to 10.0**
(one decimal; pass mark 8.0 with all gates PASS); and the verdict line below.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---
Your final chat message: the six gate verdicts, the counts of findings per grade, and your score.
