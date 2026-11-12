# BRIEF — better-theorem review BT2 on the final statement (seat: Codex gpt-6-astra, reasoningEffort high) — blind

You are a senior reviewer for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection by
sequential Monte Carlo; the ticket proves when the coded method **reports the true model S₀** when the set Q of
columns that may "leak" signal has polynomial size n^b). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/BT2_better_theorem_astra.md`; edit nothing else.
This file is your whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are
relative to it). **Change no git state.** Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞) by design; do not flag "asymptotic only" or "no finite-n statement" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SW1.txt`; its first line is
`MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd`. **Quote this digest line verbatim at the top of your review.**
Read only files listed in that manifest: `Theory_work/Wave3/W3-RM2/STATEMENT.md` (v1.4, the final statement),
`ASSUMPTION_MAP.md`, `SHARPNESS.md`, `REPORT.md`, `lemmas/L0`–`L6` (the proofs — to see what the arguments actually
use), `numerics/RESULTS.md`, and the external inputs of `reviews/INPUTS.txt`. Do not read any other file in a
`reviews/` folder, any `LOG.md` or `CHECKPOINT*.md`.

## Your only task: propose a strictly better provable statement
The statement was strengthened twice after an earlier review of this kind (signal floor at the truth-removal
width; width condition as a diverging gap with a converse; Gaussian-row leak condition in product form with no
localisation rate). Now look at the **final** statement and its proofs and ask, for each hypothesis and each
conclusion of (C1), (C2), (C3) and for the examples (C5): **is there a strictly better statement that the present
arguments (or a short extension of them) would prove?** Better = a weaker hypothesis, a stronger conclusion, a
larger range of a parameter (b, ρ, η, α, δ₀, the conditioning size 15), a sharper rate, a cleaner design-agnostic
formulation, or an unharvested conclusion the proofs already deliver. Do not review correctness as such; do not
propose design families inside theorem statements; do not propose finite-n statements.
For each proposal give: (i) the exact improved statement; (ii) the proof sketch and which step of which lemma file
changes; (iii) your confidence that it is provable (HIGH / MEDIUM / LOW) and the main risk; (iv) a class:
**ADOPT NOW** (follows from the written proofs with a few lines), **WORTH A TICKET** (real work, likely true),
**SPECULATIVE**. Also list the directions you examined and found **no credible improvement** in, with one line of
reason each (in particular: b ≥ ½; removing the lattice-width condition; the bounded-gap regime; the count n^{15ρ};
the leak scale κ√(log n/n) in Gaussian rows; the cutoff α > 2 in the examples; the equicorrelated example beyond
b = 3/10; a rate for the reported-model event).

## Output format (in your one file)
```
MANIFEST <digest>
Proposals: P1, P2, … each with (i)–(iv).
No credible improvement: list.
Summary line: counts of ADOPT NOW / WORTH A TICKET / SPECULATIVE.
```
End your reply with the summary line and the path of your file.
