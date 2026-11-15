# BRIEF — "better theorem" review BT1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent senior reviewer for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo; this ticket is about when the coded method **reports the true model S₀** when the set Q of
columns that may "leak" signal has polynomial size n^b). This file is your whole brief. Work only inside the worktree
`C:/Users/felip/BVS-wt/W3-RM2` (all paths below are relative to it). **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/BT1_better_theorem_astra.md`. Do not edit any other file. Do not start subagents.
Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_BT1.txt`. Its first line is
`MANIFEST 65ee6108be26dc13108a18e0b4a9032f25d3092c50bcc17044beb84730e6bec7`. **Quote this digest line verbatim at the top of your review.**

## Files you may read
Only the files listed in that manifest:
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` — the locked target statement (nothing in it is proved yet);
* `Theory_work/Wave3/W3-RM2/ASSUMPTION_MAP.md` — where each hypothesis enters the planned proof, the binding map
  (where each hypothesis is forced), and the readings of the boundary-violation numerics;
* `Theory_work/Wave3/W3-RM2/numerics/RESULTS.md`, `SPEC.md` (and the scripts and CSV files next to them) —
  observations, not proofs;
* `Theory_work/Wave3/W3-RM2/PLAN.md`, `Theory_work/Wave3/W3-RM2/BRIEF.md` (HQ's ticket brief);
* the external inputs listed in `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt` (pinned code, the wave PROGRAM and
  PROTOCOL, the parent result W3-RM with its lemmas and sharpness record, the engines C-GROW / W1-GEN / W2-LOC2).
Do not read any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, any
`CHECKPOINT*.md`, or anything under `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`.

## Your only task
Propose **strictly better provable statements**: a weaker hypothesis, a stronger conclusion, a wider scope or a better
rate than what STATEMENT.md claims — each with a proof sketch concrete enough to judge (the key inequality or
construction, not a programme). You are not asked to check the correctness of the current statement (other reviews
do that), and you are not asked for presentation advice.

The project's preferences when improvements are incomparable (PROGRAM.md, tie-break): design-agnosticism > range of p
> rate > constants. Theorems must be stated under conditions on (X, θ*) (or on (Σ_n, θ*) for Gaussian rows) and the
deterministic set Q only — no design family and no block of the method's partition in a hypothesis. All results are
asymptotic (n → ∞, p ≤ n^A, p ≫ n matters most) and about the method as coded (pins in STATEMENT §1): do not propose
changing the method. One boundary of this ticket: a theorem with **no lattice condition at all** (path-level control
of the local search LS0) is a separate ticket with its own budget — a complete, provable path-level argument would
still be valuable to hear, but a programme for one is not what is asked here.

Directions the lead considers open (you may ignore them and find better ones):
1. **The exponent.** Fixed design: b < β(η, A) = ½ − η/2 − √(2Aη). Is b up to ½ (or beyond) provable with a counting
   form of the sandwich (the number of outside columns entering the start mode) instead of a maximum bound? Can the
   coupling between b and η be removed or improved? Gaussian rows: 15ρ + b < ½ — can the reference count n^{15ρ} be
   avoided or reduced?
2. **The lattice-width condition (W).** Is there a strictly weaker deterministic condition on (X, Q) that still gives
   what the deterministic descent lemma (C-GROW L1.1/L1.2, used through W3-RM RM-0) needs — for instance a width
   condition only on part of the lattice, a condition with levels that depend on more than |T|, or a condition
   under which descent holds although whole-lattice no-addition fails (the numerics observe exactly that)? Is there a
   primitive sufficient condition for (W) broader than (W-ref)/(W-loc) (for example one that covers a leak group
   sharing a common factor)?
3. **(BM-Q).** The signal floor at the lattice scale θ*²_min n ≫ |Q| + log n comes from a union over the 2^{|Q∖S₀|}
   lattice sets in the truth-removal step. Can it be replaced by BM-∞ (signal ≫ log n) plus a width-type condition on
   the truth-removal directions, or removed under (W)?
4. **Conclusions not yet harvested**: explicit polynomial failure-probability rates; uniformity over the class;
   a statement for the old cap; a statement about the realised start mode rather than the envelope Q.
5. **Form R**: (W-R) and its population sufficient form (D-R^b); the localisation clause; the leak scale n^{−1/2}.
6. The converse (C3)(b): can it be sharpened into an exact threshold, or extended into a statement about the
   *conclusion* (a design satisfying everything but (W) on which the coded LS0 provably fails)?

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
