# BRIEF — proof line check LC1-B (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START2 of the SMC-BVS project. This file is your
whole brief. Work only inside the worktree
`C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-0d1ae879-e1e1cd03cea23a59`. Paths below that start with
`lemmas/`, `numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `citecheck.py` are relative to the
ticket folder `Theory_work/Wave3/W3-START2/`; "BASE" means the frozen base ticket `Theory_work/Wave3/W3-START/`; all
other paths are relative to the worktree root. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-START2/reviews/LC1_B_line_check.md` (UTF-8). Do not edit any other file in the repository. Do not
start subagents. Use no effort setting above high. If you run code, keep your scripts and their outputs outside the
repository (a temporary directory) or inline; `numerics/falsify_P.R` and `citecheck.py` may be re-run only with an
output path outside the repository.

## Frozen content
The round is frozen in `reviews/MANIFEST_LC1.txt`. Its first line is
`MANIFEST ffeba7a53ceaa916e6b69a7a86597991ecb314673d74fe9e3d2557919d76d7af`. **Quote this digest line verbatim at the top of
your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START2
Theory_work/Wave3/W3-START2/reviews/MANIFEST_LC1.txt`.

## Files you may read
Only files listed in that manifest: the ticket `STATEMENT.md` (the locked target, version 1.4.1 — a delta statement
on the base statement), `PLAN.md`, `BRIEF.md`, `citecheck.py`, the `lemmas/` folder (P1–P4), the `numerics/` folder, and
the external inputs listed in `reviews/INPUTS.txt`: the pinned code, the base statement BASE `STATEMENT.md` (version
1.3.4), the base proof files BASE `lemmas/L1…L11`, one base numerics helper, and three source statements. Do not read
any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, any `CHECKPOINT*.md`, or
any `REPORT.md`.

## Standing of the base
The base statement and the base proof files are accepted work and are **not** under review: take their statements
and proof steps as given. What is under review is how the new proofs use them. Wherever a P-file cites a base line
range, open it and check that it says what the P-file takes from it (hypotheses included); report any mismatch.

## Your task: line-by-line check of `lemmas/P2_OVL.md` and `lemmas/P4_BR.md`
Read every line; re-derive every displayed inequality and every constant; check that each step uses only what is
available at that point. In particular:
* **P2.1** — the identity (a); the inequality (b): the decomposition of γ₀(T)/γ₀(S₀), the use of the base chain bound
  (CH) and path bound (P3) with their own hypotheses, the factor |Q|^a; edge cases Q = S₀, |Q| = K, s₀ = 0, a column of
  Q ∖ S₀ in a block without truths. Check (b) by your own enumeration on small positive tables.
* **P2.2** — P(𝓐) → 1: open base L5 (L5.2(i), L5.3(a)) and L4 and check that the lattice clause (T1)(a) holds under
  (V-m) **for the same Q** with nothing else needed; the bound on m_l: open base L10.2 steps (iii)–(iv) and check that
  they use only 𝓔^blk, 𝓨 and the toolkit items named (no visibility, no bound on e_n or U_Q, no event the new proof
  does not have); the exponent bookkeeping (ε/(3q̄), the factor 2(1 + s₀ + q̄)^{q̄}, E_n); the cases q̄ = 0 and Q = S₀ at
  some n; the consequence for P-OVL. Is (AL) for Q used only where the proof says?
* **P4.1** — read base `lemmas/L9_BR.md` L9.1–L9.6 in full and verify the table: is the cardinality of Q used in any
  step other than through "at most p columns l ∉ Q"? Does any "for n large" threshold depend on Q? Are (4.1), (4.2)
  what the base file proves, with right sides free of Q? The case Q = [p] (if K = p).
* **P4.2** — the design set and admissibility; (4.3); the threshold n_R and that it does not depend on the sequence
  Q_n; case (i) (is 1 − π₀(𝓛(Q)) ≤ 1 under the convention off the design sets?); case (ii): the use of base
  Proposition L8.2(i) in the form of Corollary L6.0′ at a single n, the inequality C_nϱ̄ + n^{−1} ≤ a_n; whether the
  uniformity in Q of base L5.2(i) is really available for every |Q| ≤ K; the two consequences. Try an oscillating
  sequence Q_n (small and large |Q_n| alternating).
* **P4.3** — the constant T_ε; both cases; the limsup; the meaning of O_P when the rate does not tend to zero.
* **P4.4** and the remark "(L-R) implies (L-R⁺)".

Also: compare what is proved with what `STATEMENT.md` claims for these items, word by word (hypotheses, quantifiers,
constants, the scope notes); say whether any step uses a hypothesis that the statement does not list; and attempt a
cheap numerical falsification of your own where one is possible. The author attempts are in `numerics/falsify_P.R`
(output `numerics/out_P.txt`): say if the script does not test what it says.

## Output format (in your one file)
```
MANIFEST <digest>                      (verbatim first line of the manifest)
Verdict: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED      (one verdict per P-file checked)
Findings: numbered; each with class (CRITICAL = a step or claim is false; MAJOR = a gap that needs a new argument or a
          changed hypothesis/constant/statement; MINOR = wording, a constant to adjust, a missing remark, a wrong line
          reference), location (file:line), the problem, and the exact repair you propose (or "no repair known").
Checks performed: per section, what you re-derived and how; numerical checks you ran and their outcome.
Not checked: list.
```
VERIFIED-WITH-AMENDMENTS means every finding has a local repair that leaves the statement of `STATEMENT.md` unchanged.
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** End your reply with the
verdict line(s) and the path of your file.
