# BRIEF — "better theorem" review BT2 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent senior reviewer for theory ticket W3-START of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo; this ticket is about the **start distribution** π₀ of the sampler). This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (all paths below are relative to it). **Change no
git state. Write exactly one file:** `Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md`. Do not edit any
other file. Do not start subagents. Use no effort setting above high. If you run code, do not let it write into the
repository.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_R2.txt`. Its first line is
`MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885`. **Quote this digest line verbatim at the
top of your review.**

## Files you may read
Only the files listed in that manifest:
* `Theory_work/Wave3/W3-START/STATEMENT.md` — the final statement (v1.3.4) of the ticket;
* `Theory_work/Wave3/W3-START/lemmas/` L1–L11 — the proofs (use them to judge what a strengthening would cost: which
  step uses which hypothesis);
* `Theory_work/Wave3/W3-START/REPORT.md` — claims table, assumption ids, sharpness record, open items;
* `Theory_work/Wave3/W3-START/ASSUMPTION_MAP.md` — where each hypothesis enters, where it is forced, what the
  numerics show;
* `Theory_work/Wave3/W3-START/numerics/` — observations on the production code, not proofs;
* `Theory_work/Wave3/W3-START/PLAN.md`, `Theory_work/Wave3/W3-START/BRIEF.md` (HQ's ticket brief), `citecheck.py`;
* the external inputs listed in `Theory_work/Wave3/W3-START/reviews/INPUTS.txt` (pinned code, sources of arguments,
  consumers' statements).
Do not read any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any
`CHECKPOINT*.md`, and do not use `git log`, `git show` or `git diff` on the ticket folder.

## Your only task
The statement is final and its proofs are written. Before its main results are presented as headline results, the
project asks one question: **is there a strictly better provable statement?** — a weaker hypothesis, a stronger
conclusion, a wider scope or a better rate than what `STATEMENT.md` claims — each with a proof sketch concrete enough
to judge (the key inequality or construction, not a programme). You are not asked to check the correctness of the
current statement (other reviews do that), and you are not asked for presentation advice. Concentrate on the headline
claims: Theorem FLOOR (T0), Theorem START-F (T1) with the corollaries F1–F4, Theorem START-R (T3)(a),(b), the limits
(C2)/(T4), and the interface results (T5).

The project's preferences when improvements are incomparable (tie-break): design-agnosticism > range of p > rate >
constants. Theorems must be stated under conditions on (X, θ*) (or on (Σ_n, θ*) for Gaussian rows) only — no design
family and no block of the method's partition in a hypothesis. Every result is asymptotic (n → ∞, p ≤ n^A, p ≫ n
matters most) and about the method as coded: do not propose changing the method, and do not propose finite-n
refinements or treat the size of n at which a bound becomes informative as a weakness. Out of scope by decision of
the project (do not propose): strong-factor designs at p > K and masked truths (the start provably fails there);
new design-family results.

Directions the lead considers open (`REPORT.md` §7; you may ignore them and find better ones):
1. Gaussian rows with a population leakage level and an explicit exponent, instead of the scale C_L n^{−1/2}; the
   factor exp(C_R√log n) in (T3)(b); a fixed-constant, probability → 1 bound when C_L = 0; non-Gaussian rows;
2. the constant Gram floor (GF-16) and the energy bound (E): are they needed, or only the proof route's;
3. the averaged leakage condition (AL): the maximum over all 15-sets, the truncation levels and the tail budget; is
   there a weaker condition under which the same rate holds, or a matching necessity statement for (AL) itself;
4. visibility: (V-c)/(V-m) against the limit (C2)(ii) — is the gap between sufficiency and the limit closed;
   the partition-free form of the leaking-null limit (N2), which has content only for s₀ ≥ 16;
5. growing s₀; non-Gaussian noise; a distributional limit for √n·o₀; a matching lower bound of order √(log p/n);
6. the interfaces to the consumers (W3-SAMP's P-START and P-OVL): is there a more useful property to deliver.

## Output format (in your one file)
```
MANIFEST <digest>
Proposals: numbered P1, P2, ... Each with
  - Statement: the exact improved hypothesis/conclusion (what replaces what, by section/label of STATEMENT.md);
  - Why it is strictly better (weaker hypothesis / stronger conclusion / wider scope / better rate);
  - Proof sketch (key steps; which existing lemma or toolkit bound it uses; what is new);
  - Risk: where the sketch could fail; a quick numerical or algebraic test that would refute it;
  - Your rating: ADOPT NOW (cheap and safe) / WORTH A TICKET / SPECULATIVE.
No credible improvement found for: list the hypotheses/conclusions you tried to improve and could not, with the
obstruction (a counterexample or the step that breaks).
```
If you find no credible strictly better statement at all, say so plainly ("PASS: no credible better statement").
End your reply with the list of proposal labels and ratings, and the path of your file. Do not write any line
containing the word `COUNCIL-VERDICT`.
