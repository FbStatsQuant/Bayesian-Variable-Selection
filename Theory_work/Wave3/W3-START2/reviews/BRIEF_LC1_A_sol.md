# BRIEF — proof line check LC1-A (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START2 of the SMC-BVS project. This file is your
whole brief. Work only inside the worktree
`C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-0d1ae879-e1e1cd03cea23a59`. Paths below that start with
`lemmas/`, `numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `citecheck.py` are relative to the
ticket folder `Theory_work/Wave3/W3-START2/`; "BASE" means the frozen base ticket `Theory_work/Wave3/W3-START/`; all
other paths are relative to the worktree root. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-START2/reviews/LC1_A_line_check.md` (UTF-8). Do not edit any other file in the repository. Do not
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

## Your task: line-by-line check of `lemmas/P1_LEADING.md` and `lemmas/P3_NEC.md`
Read every line; re-derive every displayed inequality and every constant; check that each step uses only what is
available at that point. In particular:
* **P1.1** — the three facts about 𝔏^♯_n(h) (the use of (J0); which sets are maximised over; the identity with the base
  functional); the case p = s₀ + 1.
* **P1.2** — the split of the null columns; |𝒩_exc| ≤ max(0, 16 − s₀) (also for s₀ ≥ 17); δ_{S₀,l} = 0 and τ_{S₀} = σ.
* **P1.3 (Lemma LEAK-0)** — Step 0 (the prior factor); Step 1 (H is real and H ≤ z_n exactly on the stated range of λ;
  the law of each Z_l; the union bound 450e_κ/λ); Step 2 (is the small-gain premise of the base step bound L3.3
  available for every proper column and every exceptional column? is J ≤ p𝔏^♯_n(h) right?); Step 3 (the hypotheses of
  L3.3 for each column, the bound for exceptional columns, display (1.1)); Step 4 (E V ≤ 𝔏^♯_n(h); Markov); Step 5 (the
  constants 5 and 451); the event form (1.2); the consequence T₁ = O_P(·); uniformity. Is independence of the Z_l used
  anywhere? Is anything selected using the response?
* **P1.4** — that c₀, C, n₀ of base Proposition L5.2 can be kept: the range of λ = 4c_L/ε, the bound 451e_κ/λ ≤ ε/4, the
  event 𝒢^♯ and its probability, the inequality on 𝒢^♯ and the constant C^♯; the case s₀ = 0; the adaptation of base
  L6.0 and L6.0′ (constants λ_n, C^♯_n; is λ_n in the admissible range for every n ≥ 3?).
* **P1.5–P1.8** — (T1⁺)(a)–(d); F2⁺: does any step still need p/√log n → ∞, and is "exact order n^{−1/2}" right for
  bounded p; (T3⁺)(a) from P1.4 exactly as its base version follows from L5.2; IF-START⁺.
* **P3.1–P3.2** — the counting lemma; the choice of the witness and why it does not depend on the response; that the
  premise of (C2)(i) is met with the same constant; the case s₀ ≥ 16; the comparison with the base (N2).
* **P3.3** — every formula of the example (eigenvalues of G_n; realisability as a standardised centred design; Λ_V, τ²_V,
  ‖(I − P_V)x_l‖², δ²_{V,l}); (E) and (GF-16); that the premise holds for every s₀ ∈ {1, …, 15}; the remarks. P3.4.

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
