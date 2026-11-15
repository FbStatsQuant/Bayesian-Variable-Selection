# BRIEF — lemma check LC2-C: L6, the examples (claim (C5)) (seat: Claude Opus 5.5, effort high) — blind first read

You are an independent line-by-line checker for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable
selection by sequential Monte Carlo; this ticket proves that the coded method reports the true model S₀ when the set
Q of columns that may "leak" signal has polynomial size n^b). The file under review was written by an OpenAI model (a parallel prover); you are the cross-family check. This file is your whole brief. Work only inside
the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-RM2/reviews/LC2C_L6_check_opus.md`. Do not edit any other file (scratch files for your own
checks go outside the worktree). Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞); do not flag "asymptotic only" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC2.txt`; its first line is
`MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6`. **Quote this digest line verbatim at the top of your review.**
Read only files listed in that manifest (the ticket folder except `reviews/`, `LOG.md`, `CHECKPOINT*.md`; and the
external inputs of `reviews/INPUTS.txt`). Do not read any other file in a `reviews/` folder, any `LOG.md` or
`CHECKPOINT*.md`. Markers such as [SL1-#], [MP1-#], [CP2-T6] point to earlier internal rounds whose reports you are
not given; judge the text as it stands.

## Object under review
`Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md`: E1 (inherited examples), E2 (Gaussian rows with polynomial
covariance decay, claimed cutoff α > 2 where the older theorem needed α > 17/2), E3 (exact-Gram polynomial decay,
α > 2), E4 (one truth with n^b weak proxies, every b < ½), E5 (one equicorrelated group, b < 3/10).
Context you may use: `STATEMENT.md` (v1.4: §1, §3.1, §3.2, §4 — the hypotheses each example must satisfy);
`lemmas/L2_width.md` §3–§4 (the sufficient forms of the width condition (W), **taken as given**);
`lemmas/L3_assemblyF.md`, `lemmas/L5_formR.md` (the two theorems and the containments, **taken as given**);
`Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md` (Lemma BC at 78-109, Lemma IR at 118-167 — **check that they are
applied within their hypotheses and that their recorded status is quoted, not upgraded**),
`Theory_work/Wave3/W3-RM/lemmas/L7_examples.md`, `Theory_work/Wave1C/C-GROW/STATEMENT.md` (the hypotheses (H0) of
Theorem 1 at 84-88), `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`, `L3_LOC.md`; `numerics/formR_checks.R`,
`formR_checks_out.txt` (K12, K13).

## Task
For each example, check that **every** hypothesis of the theorem it instantiates is verified, with the right
quantifiers and constants. At least:
1. §0: the refitting identity and (0.1)–(0.2) — recompute; are the column-sum norms J, D finite exactly when α > 2?
   Is Lemma BC applicable to conditioning sets of size ≤ 15 with constants uniform in positions?
2. E2: the size of Q and the leak level (2.2); (L-gain-R) at every conditioning set; (L-loc-R) with logarithmic
   neighbourhoods; (D-loc^b) (its exact definition in STATEMENT §3.2 / `L5_formR.md` §2); (T1-R), (FL-R), (L-feas) in
   both branches. Is anything in the hypothesis list of RM2-R not verified? Is the ledger explaining why 17/2
   disappears correct?
3. E3: (T1-F) clause by clause against the cited list; visibility under the separation condition (3.1); the leak
   level η and the admissible b; (W-loc) with its two inequalities exactly as defined in STATEMENT §3.1.
4. E4: the Gram matrix and its floor; every clause of (C1); the exactness of (W-loc) (recompute the regression of a
   proxy on an arbitrary lattice set).
5. E5: the regression coefficient, residual norm and the bound (5.1); the expectation bound (5.2); the comparison
   with the level and the resulting range b < 3/10; every other clause of (C1).
6. The examples table and the status lines: is any status stronger than what is shown?

## Output format (in your one file)
```
MANIFEST <digest>
Verdict per lemma/claim: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED (say which statement falls).
Findings: numbered; each FATAL / MAJOR / MINOR / NIT, with file:line, the problem, and the exact correction or the
  missing argument. A counterexample or a failing numerical test counts as FATAL.
Independent derivations: what you re-derived yourself, step by step, with constants.
Not checked: what you did not verify.
```
End your reply with one line per lemma/claim giving its verdict, and the path of your file.
