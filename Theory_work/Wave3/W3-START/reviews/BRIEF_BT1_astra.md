# BRIEF — "better theorem" review BT1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent senior reviewer for theory ticket W3-START of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo; this ticket is about the **start distribution** π₀ of the sampler). This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (all paths below are relative to it). **Change no
git state. Write exactly one file:** `Theory_work/Wave3/W3-START/reviews/BT1_better_theorem_astra.md`. Do not edit any
other file. Do not start subagents. Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_BT1.txt`. Its first line is
`MANIFEST b3fafa79685f4562886d5e268432b95eba30fc75075cc50eaa30591e3546b7b2`. **Quote this digest line verbatim at the
top of your review.**

## Files you may read
Only the files listed in that manifest:
* `Theory_work/Wave3/W3-START/STATEMENT.md` — the locked target statement (nothing in it is proved yet);
* `Theory_work/Wave3/W3-START/ASSUMPTION_MAP.md` — where each hypothesis enters the planned proof, the binding map
  (where each hypothesis is forced), and the readings of the boundary-violation numerics;
* `Theory_work/Wave3/W3-START/numerics/RESULTS.md` (and the scripts and CSV files next to it) — observations on the
  production code, not proofs;
* `Theory_work/Wave3/W3-START/PLAN.md`, `Theory_work/Wave3/W3-START/BRIEF.md` (HQ's ticket brief);
* the external inputs listed in `Theory_work/Wave3/W3-START/reviews/INPUTS.txt` (pinned code, the wave PROGRAM and
  PROTOCOL, premise sources and consumers).
Do not read any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any
`CHECKPOINT*.md`.

## Your only task
Propose **strictly better provable statements**: a weaker hypothesis, a stronger conclusion, a wider scope or a better
rate than what STATEMENT.md claims — each with a proof sketch concrete enough to judge (the key inequality or
construction, not a programme). You are not asked to check the correctness of the current statement (other reviews do
that), and you are not asked for presentation advice.

The project's preferences when improvements are incomparable (PROGRAM.md, tie-break): design-agnosticism > range of p
> rate > constants. Theorems must be stated under conditions on (X, θ*) (or on (Σ_n, θ*) for Gaussian rows) only — no
design family and no block of the method's partition in a hypothesis. All results are asymptotic (n → ∞, p ≤ n^A,
p ≫ n matters most) and about the method as coded: do not propose changing the method.

Directions the lead considers open (you may ignore them and find better ones):
1. the eigenvalue floor (FL-16) among null columns (the numerics suggest it is not needed);
2. the averaged leakage functional 𝔏_n(Q): the maximum over all 15-sets U, the truncation level z_n, and whether
   the leading functional 𝔏⁰_n can replace 𝔏_n(S₀) altogether;
3. the visibility condition: is the margin form (V-m) the right primitive condition for the truth-block functional
   Ξ, or is there a cleaner or weaker one; can the Gaussian-row theorem use it;
4. the Gaussian-row theorem (T3)(b): the factor exp(C_R√log n), the population leakage scale C_L n^{−1/2}, the
   localisation clause (L-loc-R), non-Gaussian rows;
5. growing s₀; non-Gaussian noise; a matching lower bound of order √(log p/n) when nothing leaks and the residual
   variance is σ²; a distributional limit for √n·o₀;
6. the interface to the consumers (W3-SAMP's P-START and P-OVL): is there a more useful property to deliver.

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
End your reply with the list of proposal labels and ratings, and the path of your file.
