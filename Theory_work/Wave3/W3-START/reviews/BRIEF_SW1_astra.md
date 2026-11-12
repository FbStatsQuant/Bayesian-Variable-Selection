# BRIEF — exhaustive sweep SW1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are the exhaustive-sweep reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`, `numerics/`,
`reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md`, `citecheck.py` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/SW1_sweep_astra.md`. Do not edit any other file in the
repository. Do not start subagents. Use no effort setting above high. If you run code, keep your scripts outside the
repository or inline; the ticket's numerics and `citecheck.py` may be re-run read-only (do not let them overwrite
files: run copies outside the repository if they write output).

## Frozen content
The round is frozen in `reviews/MANIFEST_SW1.txt`. Its first line is
`MANIFEST 4dabd787fb4cf1625c352b79c52f153801c8b39ab85af56681df24afa5970868`. **Quote this digest line verbatim at the
top of your review.** You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_SW1.txt`.

## Files you may read
Only files listed in that manifest: `STATEMENT.md` (the target, v1.3.2), the eleven proof files `lemmas/L1_AGG_FLOOR.md`
… `lemmas/L11_EXAMPLES.md`, `PLAN.md`, `BRIEF.md` (HQ's ticket brief), `ASSUMPTION_MAP.md`, `citecheck.py`, the `numerics/`
folder, and the external inputs listed in `reviews/INPUTS.txt` (pinned code, wave documents, sources of the argument,
consumers' statements, the registry). Do not read any other file in any `reviews/` folder (except the manifest and
INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## What an exhaustive sweep is
The package claims that every item of `STATEMENT.md` §5 is proved in `lemmas/`: (C0), (C1), (C2); the bridges (B1),
(B-TK), (B-L), (B-V1), (B-V2), (B-R); the theorems (T0)–(T6); and that the proposed examples of (T7) verify the
hypotheses. Your task is to **list every flaw in the full package — not a sample.** Go through the statement and
all eleven proof files from the first line to the last. A flaw is anything that a careful referee would require to
be changed: a false step; a gap; a hypothesis used but not stated, or stated but different in the statement and in
the proof; a constant or exponent that does not follow; a quantifier or a probability space left ambiguous; a
citation that does not say what it is cited for; a status quoted incorrectly; an inconsistency between two places of
the statement or between the statement and a lemma file; a claim of the statement with no proof, or proved in a
weaker form; an undefined symbol; a wrong cross-reference. Be exhaustive on these axes:
1. **Step-by-step correctness** of each lemma file (re-derive the displayed inequalities and constants).
2. **Hypotheses used = hypotheses stated**, claim by claim: for each of (C0)–(C2), (B-·), (T0)–(T6), compare the
   hypotheses in `STATEMENT.md` with those the proof uses. Pay particular attention to: the bridge row (B-R) and
   (T3)(b) against `lemmas/L9_BR.md` (which parts of (E) are proved and which are assumed; the hypothesis p > s₀;
   consistency with §6 "Not claimed"); (T3)(a) against `lemmas/L8_TRANSFER.md`; the level vectors h and the tail budget
   in (AL), [LEAK(Q)], (C1), (T1), (T5) against `lemmas/L3_LEAK.md` and `lemmas/L5_ASM_STARTF.md`; the scope paragraph of
   (N2); Proposition OVL (its proviso in the statement against the proof in `lemmas/L10_INTERFACES.md`); the examples of
   (T7) against `lemmas/L11_EXAMPLES.md`.
3. **Cross-file consistency**: every use, in one lemma file, of a result, event, constant or threshold of another
   (names, hypotheses, what exactly is delivered); no circular dependence between the files.
4. **Hidden assumptions**: independence between Gaussian directions or between columns; a normalised Gram floor where
   only the unnormalised one is assumed; s₀ ≥ 1; p > s₀; p ≥ some bound; A ≥ 1; conditioning on events that are not
   measurable with respect to the stated σ-field; levels or sets depending on the response.
5. **Imports**: the ticket consumes no registry claim. Check that nothing is imported as a premise from another ticket;
   that the statuses quoted in `STATEMENT.md` §7 and in the lemma files are verbatim from
   `Theory_work/INFRA/registry/claims.tsv` or from the cited files; that the consumers' interfaces
   (`Theory_work/Wave3/W3-SAMP/STATEMENT.md`) are quoted correctly.
6. **Fidelity to the method as coded**: the pins of `STATEMENT.md` §1 against `Scripts/SMC_BVS/core/` (score, prior,
   cap K, partition contract, tables, start, normaliser, preprocessing); every `path:line` citation (you may use
   `citecheck.py` as a starting point, but check what the cited lines say).
7. **Design-agnostic form** (no design family in a statement; theorem hypotheses partition-free) and **honesty of
   scope** (§6 "Not claimed", the "proposed"/"expected" labels of (T7), the tightness clause of (B-R)).
8. **Numerics**: whether `numerics/lemmas/RESULTS_LEMMAS.md` and `numerics/RESULTS.md` describe what the scripts do, and
   whether anything in them contradicts a claim.

## Output format (in your one file)
```
MANIFEST <digest>                                  (verbatim first line of the manifest)
Summary: counts of CRITICAL / MAJOR / MINOR findings; one sentence on whether the package is ready for a council.
Findings: numbered consecutively, each with: class (CRITICAL = a claimed result is false or its proof has a gap with no
          local repair; MAJOR = a gap, mismatch or missing hypothesis that needs a new argument or a changed
          statement; MINOR = local wording, constant, citation or cross-reference repair), location (file:line), the
          problem, and the exact repair you propose (or "no repair known").
Per-claim table: for each of (C0), (C1), (C2), (B1), (B-TK), (B-L), (B-V1), (B-V2), (B-R), (T0), (T1), (T2) F1–F4,
          (T3)(a), (T3)(b), (T4), (T5) IF-START, (T5) OVL, (T6), (T7) — proved as stated | proved after the listed
          repairs (numbers) | gap | false.
Checks performed: per file. Not checked: list.
```
Do not stop at the first findings; a sweep that lists a sample is a failed sweep. If a section is clean, say so
explicitly per file. End your reply with the summary line and the path of your file.
