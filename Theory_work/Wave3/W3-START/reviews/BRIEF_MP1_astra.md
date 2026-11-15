# BRIEF — independent mid-point review MP1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are the independent mid-point reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/MP1_midpoint_astra.md`. Do not edit any other file in the
repository. Do not start subagents. Use no effort setting above high. If you run code, keep your scripts outside the
repository or inline; the ticket's numerics may be re-run read-only.

## Frozen content
The round is frozen in `reviews/MANIFEST_MP1.txt`. Its first line is
`MANIFEST 8e08c10991fbe4adfda0b7213dd089f54a223f0ae9edb47b5832f60a1d972fe7`. **Quote this digest line verbatim at the
top of your review.** You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_MP1.txt`.

## Files you may read
Only files listed in that manifest: `STATEMENT.md` (the locked target, v1.3), the proof files so far
(`lemmas/L1_AGG_FLOOR.md`, `lemmas/L2_TK.md`, `lemmas/L3_LEAK.md`, `lemmas/L4_VIS.md`, `lemmas/L5_ASM_STARTF.md`),
`PLAN.md`, `BRIEF.md` (HQ's ticket brief), `ASSUMPTION_MAP.md`, the `numerics/` folder, and the external inputs listed in
`reviews/INPUTS.txt` (pinned code, wave documents, sources of the argument, the consumers' statements). Do not read any
other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`. You do
not get the lead's reasoning or log.

## What a mid-point review is
The ticket's target is `STATEMENT.md`. Its key result is the fixed-design theorem START-F, (T1)(a)–(d), with its
components: the deterministic table identities and the floor ((C0), (T0)); the toolkit under a constant unnormalised
Gram floor ([TK], bridge (B-TK)); the leakage bridge with column truncation levels ((B-L), [LEAK(Q)]); the visibility
bridges ((B-V1), (B-V2), [VIS]); and the assembly ((C1)). The lead claims these are now proved in the five lemma files.
Still unproved, and planned for the second half: the corollaries (T2) F1–F3 (F4's arithmetic is in L3), the necessity
clauses (C2)/(T4), the random-design transfer (T3)(a), the Gaussian-row bridge (B-R) and (T3)(b), the interface
corollaries (T5) including the provisional Proposition OVL, and the misspecified-candidate corollary (T6).

You are a fresh pair of eyes and you are briefed to break the work. Decide:
1. **Is the key result proved?** Read the five lemma files as one argument, from the hypotheses of (T1) to its four
   conclusions. Look for: a step that does not follow; a hypothesis used but not listed in (T1) (in particular a
   normalised Gram floor, small null gains where only (AL) is assumed, s₀ ≥ 1, a level depending on the response or on
   the conditioning set, independence between Gaussian directions); a mismatch between what a lemma file proves and
   what another file cites from it; a mismatch between the lemma files and the locked statement (quantifiers,
   constants, which functional carries which level vector, the exceptional probability ε + b_n(h) in (T1)(d)); circular
   use of an interface property; a constant claimed to depend only on the fixed constants that in fact depends on the
   design, p, Q or h. Spot-check the hardest steps in full rather than every line superficially: the fibre bound of L1
   and the lower bound o₀ ≥ c_sΞ; (E1), (E2) and the τ-form RSS bound of L2; the linearisation in L3.3 and the Markov
   step of L3.4; Steps 2–6 of L4.1; the probability accounting and the uniformity of L5.2; the first-order statement
   (T1)(c).
2. **Is anything claimed that the proofs do not deliver, or delivered more weakly than stated?** One status per claim.
3. **Is the second half viable as planned?** For each unproved item say whether the proved material supports it, what
   the main obstacle is, and whether you see a reason it should fail or should be restated. In particular: does the
   uniform form (T1)(d) as proved suffice for the transfer (T3)(a) with design-measurable targets; is the Gaussian-row
   bridge (B-R) (sample floors, sample visibility at every constant level, and 𝔏_n(Q) ≤ exp(C√log n) from the
   population conditions (FL-R16), (V-R), (L-R), with a maximum over conditioning sets selected by an X-measurable
   partition) plausible on the route the statement describes, and what would you watch for; are (N2), (N3) within
   reach of the toolkit as proved.
4. **Is the target still the right one?** If the proofs so far show that a claim of `STATEMENT.md` is false, vacuous,
   or strictly weaker than what the same argument gives, say so with evidence. Do not propose unrelated extensions.

You may run cheap numerical falsification of your own (small exact cases, numerical integration, simulation).

## Output format (in your one file)
```
MANIFEST <digest>                                  (verbatim first line of the manifest)
Verdict: CONTINUE | REDIRECT | STOP
Status of the key result: per claim — (C0), (T0), [TK]/(B-TK), [LEAK]/(B-L), [VIS]/(B-V1), [VIS]/(B-V2), (C1),
          (T1)(a), (T1)(b), (T1)(c), (T1)(d) — one of: proved as stated | proved with local amendments | gap | false.
Findings: numbered; class CRITICAL (a claimed result is false or its proof has a gap with no local repair), MAJOR (a gap
          or mismatch that needs a new argument, a changed hypothesis or a changed constant), MINOR (local wording or
          constant repair); location (file:line); the problem; the repair you propose or "no repair known".
Second half: per unproved item — viable as planned | viable with changes (which) | at risk (why).
Checks performed: what you re-derived and how; numerical checks and outcomes.
Not checked: list.
```
CONTINUE = the key result stands (possibly with local amendments) and the plan for the second half is viable.
REDIRECT = the key result needs a changed statement or route, or a second-half item should be restated before work
continues. STOP = the target is unsound. Give reasons for the verdict. End your reply with the verdict line and the
path of your file.
