# BRIEF — statement-lock review SL1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-T03ACC of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `/home/fb31/BVS-wt/W3-T03ACC` (all paths below are relative to it). **Change no git
state. Write exactly one file:** `Theory_work/Wave3/W3-T03ACC/reviews/SL1_statement_lock_sol.md`. Do not edit any other
file. Do not start subagents. Use no effort setting above high. Any scratch files go under
`/home/fb31/SMC_Theory_Department/tmp/20261116-W3-T03ACC-SL1/` (create it; never /tmp); use `nice`, ≤ 4 cores.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-T03ACC/reviews/MANIFEST_SL1.txt`. **Quote its first line (`MANIFEST
<digest>`) verbatim at the top of your review.** You may run `python3 -B Theory_work/Wave3/tools/manifest.py verify
Theory_work/Wave3/W3-T03ACC Theory_work/Wave3/W3-T03ACC/reviews/MANIFEST_SL1.txt` and report its result.

## Files you may read
Only the files listed in that manifest: `STATEMENT.md` (the object under review), `PLAN.md`, `TARGET.md`,
`READER_DELTA.md`, `BRIEF.md` (the department's ticket brief), and everything under `sources/` (the proof under
review `sources/W1-T03R/PROOF.md`, its REPORT/NOTES/scripts, the locked proofs `sources/P1/`, `sources/P3/`, the
definitions `sources/common/00_COMMON.md`, and the statement sources `sources/statement/`; pins in
`sources/PINS.md`). Do not read anything else in the repository: in particular no file in any `reviews/` folder other
than the manifest, no `LOG.md`, no `CHECKPOINT*.md`, no `api/` folder, no other ticket's files, and none of the
earlier verification reports named in `BRIEF.md` or `sources/PINS.md` §D (W2-VT03R, A-REV2, A-REV5). No web access.

## What is under review
`STATEMENT.md` restates an existing theorem, T03♯ (posterior concentration of the exact SMC-BVS target), so that a
council can accept it on its existing proof. It is **not** a new or changed theorem: the restatement must be faithful
to the recorded statement and to the proof's own statement, with every hypothesis explicit. The proof itself is
line-checked later; this round does not re-prove it, but you should flag any clause that the proof as written
plainly does not deliver.

## What a statement-lock review is
You decide whether the target statement is fit to be locked before the line checks start. You are briefed to break
it. Check, with file:line evidence:
1. **Faithfulness.** Compare STATEMENT §2–§3 item by item with (a) the statement of record
   `sources/statement/W6-FIXREV2_STATEMENTS.md:15-61`, (b) the approved card `sources/statement/TLF_434-499.md:15-18,29`
   and `sources/statement/SoP_04_theory_767-812.tex:14-23`, (c) the proof's own statement `sources/W1-T03R/PROOF.md:44-47,
   127-132, 160-170`. Every hypothesis, quantifier, constant, convention and conclusion: same content? Is anything
   added, dropped, weakened or strengthened? Is each difference listed in STATEMENT §4 really a reading (no change of
   content), and is any difference missing from §4?
2. **Every hypothesis explicit and every object defined.** STATEMENT §1 must define every symbol used in §2–§3
   (check against `sources/common/00_COMMON.md:9-14,29,35-38` and `sources/P3/STATEMENT.md:5-27`). Look for a
   hypothesis the proof uses but the statement does not state — e.g. in `PROOF.md:9` (p ≥ 2), `PROOF.md:170` (what the
   thresholds depend on), [P3]'s R (A ≥ 1, ‖μ‖²/n ≤ M, eventually s₀ ≤ K), the fixedness of g₀, φ₀, M, σ*², the
   deterministic nature of M_n and c, the s₀ ≥ 1 restriction, and the definitions of R_m, m♯_n, j₀, C_*, L_*. Check the
   claim in STATEMENT §4 item 3 (A < 1 covered by max(A,1)) and item 4 (p = 1).
3. **Each clause well-posed and plausibly delivered.** What is random, what is fixed, which limit; O_{P₀} uniform in
   what. Do clauses 1–5 follow from the proof's conclusions (`PROOF.md:168`) and Assembly (`PROOF.md:203`) as written,
   at the level of a statement check? In particular clause 3's "→ 0", clause 4's J_n^∞ sentence, clause 5's content
   (compare `sources/P3/STATEMENT.md:43`, `sources/P3/PROOF_v2.tex:380`).
4. **Consumes table (STATEMENT §5).** Are the consumed labels of [P1] and [P3] complete for §§1, 2, 4, 6 of PROOF.md
   (compare `PROOF.md:205-207`)? Are the statuses quoted verbatim from the cited places
   (`sources/statement/registry_theory_main_L68.tsv`; NBH ID_REGISTRY rows quoted there — you may read
   `Theory_work/Old_Projects/New_BVS_Headquarters/ID_REGISTRY.md` rows TH121–TH128 only, to check the quotes)? Is the
   claim that T03♯ does not use H-T02, Prop. D, Prop. E3 or T02(ii♯) right?
5. **Plan viability.** Do PLAN.md §2's three batches cover every step of the proof as written and every consumed
   [P1]/[P3] step, with correct line ranges? Anything missing?

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: LOCK | LOCK WITH CHANGES | DO NOT LOCK
Required changes: numbered; each with location (file:line), the problem, and the exact change you require.
Optional suggestions: numbered.
Checks performed: what you verified and how, per item 1–5.
Not checked: list.
```
Classify each required change as CRITICAL (a clause is false, ill-defined, or not the recorded statement), MAJOR (a
hypothesis or scope must change or be made explicit) or MINOR (wording, citation, missing definition). Use DO NOT LOCK
only if a CRITICAL change cannot be made by editing the restatement. Tag each required change also with the v4 kind:
C (correctness), S (strength: claims more than proved, or uses an unstated hypothesis), F (faithfulness to the
sources) or E (editorial).
