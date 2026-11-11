# BRIEF — lemma line check LC1-A (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/LC1_A_line_check.md`. Do not edit any other file in the
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

## Your task: line-by-line check of L1
Object: `lemmas/L1_AGG_FLOOR.md` (Lemma AGG: (AGG-a)–(AGG-d), (FLOOR), Theorem (T0); deterministic).
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read). The ticket consumes **no** registry claim: nothing may be imported as a premise from another ticket
(files under `Theory_work/Wave1*/` are sources of the argument only). In particular check:
* Every use of the prior ratios (P1)–(P3): ranges of k, the condition k − D + a ≤ p, the direction of each inequality.
* The decomposition of a model relative to the lattice (L1.1): is the map S ↦ (T(S), bad blocks, (U_b), N) well defined
  and injective on each fibre; are the exponents of ω^Q(U) exactly those of `STATEMENT.md` §2; is a_b ≤ 15 and E ≤ 15s₀
  right; does the split of the rising factorial give c_Q^E and (c_Q + 1)_{a′} (and (|T| + 1)_{a′} when there is no bad
  block); is the fibre sum bounded by Ξ_b(Q) as defined (maximum over T′ with U*_b ⊆ T′ ⊆ C_b ∩ Q)?
* (AGG-b): the exact term T₁, the remainder R₂, the constant 16s₀ + 1, and the lower bound o₀ ≥ c_sΞ (feasibility of
  S_U, injectivity, both prior cases, the constant c_s = (64·max(s₀, 1))^{−16}).
* (AGG-c), (AGG-d): each factor; the use of e_n for U with a′ ≥ 1; the bound m_l ≤ pU_Q; the case split d ≥ a / a > d.
* (FLOOR): Q_S as a ridge criterion (verify the identity from the pinned scorer
  `Scripts/SMC_BVS/core/cpp/v3_score.h:204-224`), the Schur-complement determinant ratio and its monotonicity in λ,
  rank-deficient X_S, the arithmetic of f_n(k) ≥ ½(n + 1)^{−1/2} and f/(1 + f) ≥ ⅓(n + 1)^{−1/2}, and (T0).
* Edge cases: s₀ = 0; Q = S₀; Q = [p] (when |Q| ≤ K); s₀ = K; K < p; blocks of size 1; a truth block entirely inside S₀;
  p = s₀ + 1; U_Q close to 1.
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
