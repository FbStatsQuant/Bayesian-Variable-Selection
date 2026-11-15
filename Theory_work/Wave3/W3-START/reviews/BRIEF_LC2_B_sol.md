# BRIEF — lemma line check LC2-B (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/LC2_B_line_check.md`. Do not edit any other file in the repository. Do
not start subagents. Use no effort setting above high. If you run code, keep your scripts outside the repository (a
temporary directory) or inline; the ticket's numerics may be re-run read-only.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_LC2.txt`. Its first line is
`MANIFEST 053bc169c5da3c032943e217e7bd5ddb76d4268ba821b09579be126d9961a155`. **Quote this digest line verbatim at the top of your review.** You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_LC2.txt`.

## Files you may read
Only files listed in that manifest: the ticket's `STATEMENT.md` (the locked target, v1.3.1), `PLAN.md`, `BRIEF.md`,
`ASSUMPTION_MAP.md`, the `lemmas/` folder (L1–L11), the `numerics/` folder, and the external inputs listed in
`reviews/INPUTS.txt` (pinned code, wave documents, sources of the argument, consumers' statements). Do not read any
other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## Your task: line-by-line check of L10 and L11
Object: `lemmas/L10_INTERFACES.md` (IF-START; Proposition OVL; Lemma R′ and Corollary MIS) and `lemmas/L11_EXAMPLES.md` (five example families).
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read; the files L1–L5 may be taken as given where they are cited, but report any mismatch between what is
cited and what they state). The ticket consumes **no** registry claim: nothing may be imported as a premise from
another ticket. In particular check:
* L10.1: that IF-START delivers exactly W3-SAMP's P-START (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:76-77`) and the rate
  premise of its (C-v) (`:158-162`) — quote the consumer's wording and compare; the Gaussian-row version (odds versus
  mass); what is explicitly not supplied.
* L10.2 (Proposition OVL): the use of (AGG-c) (read its statement in `lemmas/L1_AGG_FLOOR.md` L1.4); the events and their
  probabilities (in particular the event with λ′_n and the Markov step borrowed from `lemmas/L3_LEAK.md` L3.4); the bound
  on m_l for l ∈ Q ∖ S₀ via (f3) (is the gain small enough, are all conditioning sets T ⊇ U*_b covered by the hypothesis
  on a_l, is the noise event sufficient); the exponent E_n with the positive part; the constants; the consequence for
  the production form of P-OVL (`W3-SAMP/STATEMENT.md:103-105`, and `:82-83` for what P-OVL is). Is (V-c) really needed,
  and is anything used that the proposition does not assume?
* L10.3: Lemma R′ against `Theory_work/Wave1C/C-MIS/STATEMENT.md:39-58`; that nothing is consumed from C-MIS; the
  fixed-design corollary ("provided its hypotheses hold after the substitution"); the random-candidate clause through
  `lemmas/L8_TRANSFER.md`.
* L11: for **each** example re-derive every claimed property against the **partition-free** hypotheses of
  `STATEMENT.md` §3 (all sets of size ≤ 15/16, not one block): the frame of L11.0 (existence for p ≤ n − 1, that the
  design is its own standardisation); F-1; F-3 (all Gram matrices, the distance, zero null gains for every U); F-2 —
  the formula for the residual energies q_k, (E), (GF-16), every instance of (V-m) with Q = S₀ (and the value of c_m),
  the failure of (V-c), the level 0.8(1 + 2A) for the fifteen correlates over **all** conditioning sets, the F4
  conclusion, and the lower bound showing that default-level (AL) fails (check the exponent arithmetic at A = 0.1 and
  A = 1); G-1 and G-2 — (FL-R16), (V-R), (L-gain-R), (L-loc-R) with the stated Q and H_l, and that the conclusion drawn
  from (T3)(b) is exactly what `STATEMENT.md` allows. Try to break an example numerically (build the design for a
  moderate n and compute the quantities).
Also: compare what is proved with what `STATEMENT.md` claims for these items (hypotheses, quantifiers, constants); and
attempt a numerical falsification of your own where it is cheap. The lead's attempts are in `numerics/lemmas/`
(`falsify_L6_L11.R`, `RESULTS_LEMMAS.md`, second half): you may re-run or extend them, and should say if a script does
not test what it says.

## Output format (in your one file)
```
MANIFEST <digest>                      (verbatim first line of the manifest)
Verdict: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED      (one verdict per lemma file checked)
Findings: numbered; each with class (CRITICAL = a step or claim is false; MAJOR = a gap that needs a new argument or a
          changed hypothesis/constant/statement; MINOR = wording, a constant to adjust, a missing remark), location
          (file:line), the problem, and the exact repair you propose (or "no repair known").
Checks performed: per section, what you re-derived and how; numerical checks you ran and their outcome.
Not checked: list.
```
VERIFIED-WITH-AMENDMENTS means every finding has a local repair that leaves the statement of `STATEMENT.md` unchanged.
End your reply with the verdict line(s) and the path of your file.
