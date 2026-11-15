# BRIEF — lemma line check LC1-B (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/LC1_B_line_check.md`. Do not edit any other file in the
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

## Your task: line-by-line check of L2 and L4
Object: `lemmas/L2_TK.md` (Lemma TK: events, (TK-a)–(TK-f)) and `lemmas/L4_VIS.md` (bridges (B-V2), (B-V1): Propositions L4.1, L4.2, Corollary L4.3).
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read). The ticket consumes **no** registry claim: nothing may be imported as a premise from another ticket
(files under `Theory_work/Wave1*/` are sources of the argument only). In particular check:
* L2: identity (2.1); the three tail bounds and the union counts (2^{16}p sets, ranks ≤ 16; no independence); the
  definition and size of ω_n (is ω̄_n log n → 0 delivered, as `STATEMENT.md` §4 [TK] requires?); (TK-a) including the
  AM–GM step; (TK-b) constants C_R, c_E; (E1) and (E2) from the pinned scorer
  (`Scripts/SMC_BVS/core/cpp/v3_score.h:204-224`) under an **unnormalised** Gram floor only; the remainder bounds κ₁, κ₂;
  the empty set; (TK-d); (TK-e) (projections, ΠC = Π, the one-step identity); (f1)–(f3) with the right τ² in each
  denominator. Is s₀ ≥ 1 or a normalised floor used anywhere silently? Is anything imported from another ticket?
* L4: the event 𝓧 (count of nested pairs, rank, tail bound, ζ_n); inequality (Q±); in L4.1 — that (V, D, R, N) built
  from U is an instance of the quantifier of (V-m) in `STATEMENT.md` §3.1 and that T = T_b(U); Steps 1–7 line by line
  (signs, which τ² appears where, the choice of ε₁ and the two inequalities claimed for it, the price bound of Step 5
  in both cases including c_Q/p ≤ 16s₀, the final exponent); in L4.2 — the single-step bound, the choice of ε₁, the
  exponent arithmetic A − (c_V − 1)/2 + (κ_V − κ)/2 = −(κ_V + κ)/2, the geometric-mean step for e_n, and the use of
  (AGG-d) (take (AGG-d) from `lemmas/L1_AGG_FLOOR.md` as given; another reviewer checks it). Does either proposition
  need the gains of the null columns to be small? Are the thresholds n₃, n₄ functions of the fixed constants only?
* Edge cases: s₀ = 0; a truth block containing all of S₀; |U*_b| = 16; d − a at its extremes; Q ≠ S₀ with R ≠ ∅.
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
