# BRIEF — lemma line check LC1-C (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/LC1_C_line_check.md`. Do not edit any other file in the
repository. Do not start subagents. Use no effort setting above high. If you run code, keep your scripts outside the
repository (a temporary directory) or inline; the ticket's numerics may be re-run read-only.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_LC1.txt`. Its first line is
`MANIFEST 867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38`. **Quote this digest line verbatim at the top of your review.** You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_LC1.txt`.

## Files you may read
Only files listed in that manifest: the ticket's `STATEMENT.md` (the locked target, v1.3), `PLAN.md`, `BRIEF.md`,
`ASSUMPTION_MAP.md`, the `lemmas/` folder, the `numerics/` folder, and the external inputs listed in `reviews/INPUTS.txt`
(pinned code, wave documents, sources of the argument). Do not read any other file in any `reviews/` folder (except the
manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## Your task: line-by-line check of L3 and L5 (the key lemma of the ticket)
Object: `lemmas/L3_LEAK.md` (Lemma J, level vectors, bridge (B-L): Lemma L3.3, Proposition L3.4, Corollary F4) and `lemmas/L5_ASM_STARTF.md` (Lemma ASM (C1), Proposition L5.2 = (T1)(d), Theorem START-F (T1)(a)–(c)).
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read). The ticket consumes **no** registry claim: nothing may be imported as a premise from another ticket
(files under `Theory_work/Wave1*/` are sources of the argument only). In particular check:
* L3: (J0)–(J4) for every h ≥ 1, t ≥ σ; the event 𝓩_h and the tail budget (count 2^{15} per column, no independence,
  levels not depending on the response); the three domination statements of (B1), including s₀ = 0 and the ≤ 15 nulls
  sharing a block with all of S₀; the constants g⁰_n, g_n, x̄_n, ς_n and the claim ς_n → 0 (this is where ω_n log n → 0
  is needed); Lemma L3.3 line by line; the small-gain consequences (SG-b), (SG-0), (SG) of (J0); Proposition L3.4 —
  the bound of the maximum over conditioning sets by a sum, E V, the Markov step, what exactly is conditioned on, the
  case [p] ∖ Q = ∅, part (b) for T₁; the arithmetic of F4 (levels admissible, budget → 0, exponent (1 + 2A̲ − c)/2).
  Try to break the bridge: a design or level vector for which U_Q is not O_P(n^{−1/2}𝔏^b_n(Q; h)) although the premise
  holds; a place where a level depending on the conditioning set, or on the data, is used implicitly; a place where
  smallness of the gain is needed but not available.
* L5: (e1)–(e3); Lemma ASM (a)–(c) as a pure composition of (AGG) with the interface properties; Proposition L5.2 —
  the choice of (λ, c₀, C, C′, κ′, n₀), the list of events and the probability accounting (does it add up to
  ε + b_n(h)?), each inequality "on 𝒢", the use of (B1) at the end, and whether n₀, c₀, C depend only on (ε, κ) and
  the fixed constants — this is the uniformity that the random-design transfer (T3)(a) will use; the passage from L5.2
  to the O_P/o_P statements (a), (b); the first-order statement (c) (lower bound T₁ ≥ ½(n + 1)^{−1/2}, the two
  remainders, κ′ > ½). Take the results of `lemmas/L1_AGG_FLOOR.md`, `lemmas/L2_TK.md`, `lemmas/L4_VIS.md` as given
  where L3/L5 cite them (other reviewers check those files), but report any mismatch between what is cited and what
  those files state.
* Does the proved statement coincide with `STATEMENT.md` §5.1 (C1) and §5.3 (T1)(a)–(d), in hypotheses and
  conclusions? Any hidden use of a hypothesis that (T1) does not list?
Also: compare what is proved with what `STATEMENT.md` claims for these items (hypotheses, quantifiers, constants); and
attempt a numerical falsification of your own where it is cheap (small exact cases, random tables, numerical
integration). The lead's attempts are in `numerics/lemmas/` (`RESULTS_LEMMAS.md`): you may re-run or extend them, and
should say if a script does not test what it says.

## Output format (in your one file)
```
MANIFEST <digest>                      (verbatim first line of the manifest)
Verdict: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED      (one verdict per lemma file checked)
Findings: numbered; each with class (CRITICAL = a step or claim is false; MAJOR = a gap that needs a new argument or a
          changed hypothesis/constant; MINOR = wording, a constant to adjust, a missing remark), location (file:line),
          the problem, and the exact repair you propose (or "no repair known").
Checks performed: per section, what you re-derived and how; numerical checks you ran and their outcome.
Not checked: list.
```
VERIFIED-WITH-AMENDMENTS means every finding has a local repair that leaves the statement of `STATEMENT.md` unchanged.
End your reply with the verdict line(s) and the path of your file.
