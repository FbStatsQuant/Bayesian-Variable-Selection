# BRIEF — council round R1, seat `opus` (Claude Opus 5.5, effort high) — blind first read

You are a council reviewer for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection by
sequential Monte Carlo). The ticket claims to prove when the coded method **reports the true model S₀** when the set
Q of columns that may "leak" signal has polynomial size n^b, b < ½ — a strengthening of the paper's "Theorem 3" from
polylogarithmic to polynomial leakage sets, in a fixed-design form and a Gaussian-row form. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no
git state. Write exactly one file:** `Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md`. Do not edit anything else
(scratch files outside the worktree). Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞) by decision of the owner: never treat "asymptotic only" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt`; its first line is `MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a`.
Read only files listed in that manifest: the ticket folder `Theory_work/Wave3/W3-RM2/` except `reviews/`, `LOG.md`,
`CHECKPOINT*.md` — `STATEMENT.md` (v1.4), `lemmas/L0_toolkit_b.md`, `L1_sandF_b.md`, `L2_width.md`,
`L3_assemblyF.md`, `L4_sandR_b.md`, `L5_formR.md`, `L6_examples.md`, `SHARPNESS.md`, `ASSUMPTION_MAP.md`, `REPORT.md`,
`PLAN.md`, `BRIEF.md`, `citecheck.py`, `numerics/` — and the external inputs listed in `reviews/INPUTS.txt` (pinned
code under `Scripts/SMC_BVS/core/cpp/`; the parent ticket `Theory_work/Wave3/W3-RM/`; the engines
`Theory_work/Wave1C/C-GROW/`, `Wave1/W1-GEN/`, `Wave2/W2-LOC2/`, `Wave2/W2-UNI/`, `Wave2/W2-APP/`). This is a **blind
first read**: do not read any other file in a `reviews/` folder (earlier reviews, dispositions, scores), any
`LOG.md` or `CHECKPOINT*.md`. Markers such as [SL1-#], [MP1-#], [LC2A-#], [SW1-#] point to earlier internal rounds
whose reports you are not given; REPORT.md summarises them — judge the mathematics and the records as they stand.

## Your job: try to break the result, then score it
Check the two theorems — (C1) RM2-F (fixed design; `lemmas/L0`–`L3`) and (C2) RM2-R (Gaussian rows; `lemmas/L4`,
`L5`) — through the parent's core theorem RM-0 (`Theory_work/Wave3/W3-RM/STATEMENT.md:160-176`,
`lemmas/L0_core.md`), the width lemmas (C3), the containment of the parent theorems (C4), the examples (C5,
`lemmas/L6_examples.md`) and the sharpness record (C6, `SHARPNESS.md`). Read the NEW mathematics line by line:
* `L2_width.md`: no-addition on the whole lattice from a Gaussian-width gap with a size-dependent level (Lemma
  NA-W), its converse (W-conv), the sufficient forms, truth removal by an exact two-square identity (Lemma TL-W);
* `L1_sandF_b.md`: the fixed-design sandwich at |Q| ≤ n^b (where the size of Q is paid for);
* `L4_sandR_b.md`: the Gaussian-row sandwich — the product-form selection removal (Lemma 2), the spherical tail
  with a mean shift (Lemma 3), counting, ladder, junk exclusion;
* `L5_formR.md`: conditional use of the fixed-design lemmas under Gaussian rows (P8); from a joint-law bound to a
  conditional Gaussian width (P9a, P9); the posterior input and the p = 1 endpoint (P10); the assembly;
* `L6_examples.md`: E2–E5.
Look for: false steps; missing cases; hypotheses used but not stated, or stated but unused; quantifier and
uniformity gaps (every maximiser, every admissible run, every X-measurable partition, every "n ≥ n₀"); mismatch
between STATEMENT §3–§4, the lemma statements, REPORT §2–§3 and the registry block at the end of REPORT; constants
or rates that do not track; statuses of cited results quoted wrongly or upgraded (the conditions of (C1) on
SOP:TH09 and of (C2) on W2-APP:POST must be carried; examples E2, E3 on Lemma BC / Lemma IR); overclaims in
STATEMENT §0/§6, SHARPNESS, REPORT (flags, §1, §5, §6), ASSUMPTION_MAP — in particular about necessity, sharpness
and the numerics (LS0 re-implementation only, nominal classification); any design family inside a theorem
statement (forbidden: families only as examples); infidelity to the method as coded (the code pins of STATEMENT §1).

## Six gates (each: PASS / FAIL with a one-paragraph justification and file:line evidence)
G1 Correctness of every step.
G2 Hypotheses used = hypotheses stated.
G3 No hidden assumptions.
G4 Cited lemmas have adequate status (statuses quoted verbatim, none upgraded; each new lemma has a cross-family
   check on file according to REPORT §3–§4; conditions on inputs below "PROVED-CHECKED" carried into the statuses).
G5 Constants and rates tracked.
G6 Fidelity to the method as coded and to the binding program: design-agnostic statements (no design family in a
   theorem), partition-free where possible, examples and sharpness record honest, nothing claimed beyond what is
   proved.

## Output (in your one file)
1. Gate verdicts G1–G6.
2. A score from 0.0 to 10.0 (one decimal), with the reason for every point deducted.
3. Numbered findings: severity (FATAL / MAJOR / MINOR / NIT), location (file:line), the precise problem, the exact
   fix. Mark which findings are REQUIRED for a pass.
4. One paragraph: is the result, as stated in v1.4, fit to replace the parent's Theorem 3 as the paper's main
   reported-model theorem? What is the single most valuable strengthening still missing?
Pass rule (for your information): both seats ≥ 8.0 with all six gates PASS in the same round.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict.

Final message: gate verdicts, score, the REQUIRED findings (short), and the path of your file.
