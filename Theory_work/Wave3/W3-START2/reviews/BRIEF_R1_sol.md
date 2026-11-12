# BRIEF — council round R1, seat `sol` (Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are one of the two council seats for theory ticket W3-START2 of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree
`C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-0d1ae879-e1e1cd03cea23a59`. Paths below that start with
`lemmas/`, `numerics/`, `reviews/` or are `STATEMENT.md`, `REPORT.md`, `PLAN.md`, `BRIEF.md`, `citecheck.py` are relative to
the ticket folder `Theory_work/Wave3/W3-START2/`; "BASE" means the base ticket `Theory_work/Wave3/W3-START/`; all other
paths are relative to the worktree root. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-START2/reviews/R1_council_sol.md` (UTF-8). Do not edit any other file in the repository. Do not
start subagents. Use no effort setting above high. If you run code, keep your scripts and their outputs outside the
repository or inline; do not let any script write into the repository (`citecheck.py` and `numerics/falsify_P.R` may
be run only with an output path outside the repository:
`python Theory_work/Wave3/W3-START2/citecheck.py <file outside the repository>`).

## Frozen content
The round is frozen in `reviews/MANIFEST_R1.txt`. Its first line is
`MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f`. You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START2 Theory_work/Wave3/W3-START2/reviews/MANIFEST_R1.txt`.

## Files you may read
The files listed in that manifest: `STATEMENT.md` (the claims, version 1.4.1 — a **delta statement** on the base
statement), the four proof files `lemmas/P1_LEADING.md`, `lemmas/P2_OVL.md`, `lemmas/P3_NEC.md`, `lemmas/P4_BR.md`,
`REPORT.md` (the technical report: claims table, assumption ids, relations to existing results, sharpness record, open
items), `PLAN.md`, `BRIEF.md` (the ticket brief), `citecheck.py`, the `numerics/` folder, and the external inputs listed
in `reviews/INPUTS.txt`: the pinned code, the base statement BASE `STATEMENT.md` (version 1.3.4), the base proof files
BASE `lemmas/L1…L11`, one base numerics helper, and three source statements. In addition, for context only (not part
of the frozen content, not proof premises): `Theory_work/INFRA/registry/claims.tsv` (to check quoted statuses) and
`Theory_work/Wave3/PROTOCOL.md`. **Do not read** any other file in any `reviews/` folder (except the manifest and
INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`, and do not use `git log`, `git show` or `git diff` on the ticket
folder: this is a blind first read, and you must form your verdict without any earlier version, review, disposition
or score.

## Standing of the base
Version 1.4 of the start-mass statement is the base statement v1.3.4 with one definition added, one assumption
replaced and nine claims of `STATEMENT.md` §3 (eight replace base claims of the same name; Lemma LEAK-0 is new). The
base statement and the base proof files are the content of another ticket and are **not** under review here: take
their statements and proof steps as given. What is under review is every new step, and every use of a base result:
wherever a proof cites a base line range, open it and check that it says what is taken from it, hypotheses included.

## What the council decides
The package claims that every item of `STATEMENT.md` §3 — Lemma LEAK-0, (T1⁺) START-F, F2⁺, (T3⁺)(a) TRANSFER, (T3⁺)(b)
START-R, bridge (B-R⁺), (T4⁺) NEC, IF-START⁺, OVL⁺ — is proved in `lemmas/`, and that each of the eight replacing
claims implies the base claim it replaces (`STATEMENT.md` §5). `REPORT.md` §3 gives one line per claim. You decide
whether this package can be accepted as **checked mathematics**. You are briefed to break it: assume there is an
error and look for it. Score the package on six gates; a gate PASSes only if you found no blocking issue for it.

* **G1 — correctness of every step.** Re-derive the arguments; do not sample. Give most of your effort to the new
  steps: in `lemmas/P1_LEADING.md` the split of the null columns and the count of exceptional columns (P1.2), every
  step and constant of Lemma LEAK-0 (P1.3: the cut-off H and the admissible range of λ, the availability of the
  small-gain premise of the base step bound for each column, the union bound, Markov, the constants 5 and 451), and
  the claim that the constants c₀, C, n₀ of the base Proposition L5.2 can be kept (P1.4); F2⁺ without a growth
  condition on p (P1.6). In `lemmas/P2_OVL.md` the identity and the product inequality of Lemma P2.1 and the claim that
  the lattice clause holds under (V-m) for the same Q. In `lemmas/P3_NEC.md` the counting lemma, the choice of the
  witness, and every formula of Example P3.3. In `lemmas/P4_BR.md` the record that the base steps L9.1–L9.6 never use
  the size of Q (read BASE `lemmas/L9_BR.md` in full), and the two case distinctions at a fixed n (P4.2, P4.3),
  including an arbitrary oscillating sequence Q_n.
* **G2 — hypotheses used = hypotheses stated.** For each claim compare `STATEMENT.md` with what its proof uses.
* **G3 — no hidden assumptions** (independence between Gaussian directions or columns; s₀ ≥ 1 where s₀ = 0 is
  claimed; p → ∞; a bound on |Q| beyond |Q| ≤ K; a rate tending to zero where none is assumed; conditioning on a
  non-measurable event; witnesses, supports, sets or levels depending on the response).
* **G4 — imports have adequate status and say what is claimed.** Check that each base result is used as it is
  stated; that nothing is used as a premise from any ticket other than the base; that `STATEMENT.md` §5 and
  `REPORT.md` §4 describe the dependence on the base ticket correctly and claim no status for it that the files you may
  read do not support; that the consumers' interfaces (`Theory_work/Wave3/W3-SAMP/STATEMENT.md`) are quoted correctly
  and receive exactly what (T5⁺) says; and each row of the supersession table (`STATEMENT.md` §5): does the new claim
  really imply the base claim it replaces?
* **G5 — constants and rates tracked.** Every constant, exponent and threshold: where it comes from, what it depends
  on, and whether the claimed uniformity (in (T1⁺)(d), in Lemma LEAK-0, and in Q for (T3⁺)(b)) really holds.
* **G6 — fidelity to the method as coded.** The delta makes no new statement about the code: "π₀" is the start
  distribution exactly as pinned in the base statement §1. Check that no new claim needs a property of the coded
  start beyond those the base statement pins (the prior formula, the cap K, the partition contract with blocks ≤ 16,
  the tables), and that the `path:line` citations resolve to what is said (`citecheck.py`).

Also check `REPORT.md`: that each line of its claims table matches the statement and the proof it names; that the
assumption ids, the relations to existing results, the sharpness record and the numerics paragraph say no more than
the proofs and `numerics/out_P.txt` support; that the honesty of scope (`STATEMENT.md` §4; the exclusion of s₀ = 0 in
LEAK-0 and (N2⁺); the ε-dependent constant of (T1⁺)(d); "fewer than 17 − s₀ nulls: not claimed"; the trivial range of
(T3⁺)(b); the tightness clause for C_L = 0) is adequate.

Project convention (owner's rule, not a defect): every result of this project is asymptotic (n → ∞) unless marked
*deterministic*. Do not score the size of n at which a bound becomes informative, or the absence of finite-n
guarantees, as an issue; do score any asymptotic claim that is false, unproved, or stated more strongly than proved.

## Output format (in your one file)
```
Verdict summary: one paragraph.
Gate table: G1 … G6, each PASS or FAIL with a justification that names what you re-derived.
Per-claim table: every id of REPORT.md §3 — accepted | accepted with non-blocking remarks | not accepted (why).
Issues: numbered; each BLOCKING (prevents a gate from passing) or NON-BLOCKING, with location (file:line), the
        problem and the repair you propose.
Overall score: x.y / 10 (8.0 or more means: acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```
The frozen content cannot be edited after this round without a new round, so say clearly which issues, if any, must
be fixed before acceptance (BLOCKING) and which can wait for a later version (NON-BLOCKING).

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f` (round R1, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---
