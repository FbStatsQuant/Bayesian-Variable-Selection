# BRIEF — council round R1, seat `astra` (Codex gpt-6-astra, reasoningEffort high; OpenAI seat) — blind first read

You are one of the two council seats for theory ticket W3-T03ACC of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `/home/fb31/BVS-wt/W3-T03ACC`. Paths below are relative to the ticket folder
`Theory_work/Wave3/W3-T03ACC/` unless they start with `Theory_work/` or `Scripts/`. **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-T03ACC/reviews/R1_council_astra.md` (UTF-8). Do not edit any other file. Do not
start subagents. Use no effort setting above high. Scratch files only under
`/home/fb31/SMC_Theory_Department/tmp/20261116-W3-T03ACC-R1-astra/` (create it; never /tmp; never inside the
repository); computations small, with `nice`, ≤ 4 cores. `citecheck.py` may be run only with an output path in that
scratch folder; `deps_hash.py` only without `--write`.

## Frozen content
The round is frozen in `reviews/MANIFEST_R1.txt`. Its first line is `MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6`. You may run
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-T03ACC Theory_work/Wave3/W3-T03ACC/reviews/MANIFEST_R1.txt`.

## Files you may read
The files listed in that manifest: `STATEMENT.md` (v1.1, LOCKED: the object), `REPORT.md` (claims table, checks
summary, registry block), `DEPS.tsv` (+ `deps_hash.py`), `ERRATA.md`, `PLAN.md`, `TARGET.md`, `READER_DELTA.md`,
`BRIEF.md`, `RIDER_RULES.md`, `citecheck.py`, and `sources/`: the proof under review `sources/W1-T03R/PROOF.md` (with
its `REPORT.md`, `NOTES.md`, `BRIEF.md`, scripts), the locked proofs it builds on, [P1] = `sources/P1/PROOF_v3.tex`
and [P3] = `sources/P3/PROOF_v2.tex` (with their `STATEMENT.md`, `STATUS.md`), the definitions
`sources/common/00_COMMON.md`, the statement sources `sources/statement/`, the pins `sources/PINS.md`; and the
external inputs in `reviews/INPUTS.txt` (the coded score and standardisation). **Do not read:** any other file under
`reviews/` (other than the manifest, INPUTS.txt and this brief), `LOG.md`, `CHECKPOINT*.md`, `sources/P1/FINAL_REPORT.md`,
`sources/P3/FINAL_REPORT.md`, any earlier verification of this proof named in `BRIEF.md` or `sources/PINS.md` §D, any
other ticket's folder, any registry table, or the web; do not use `git log`, `git show` or `git diff`. This is a blind
first read: form your verdict without any earlier review, disposition or score. (`REPORT.md` and `DEPS.tsv` name
review files and their verdicts; that is part of the record you check, not a reason to open them.)

## What the council decides
T03♯ (`STATEMENT.md` §3, claims `W3-T03ACC:T03S.1`–`T03S.5`) is an existing theorem about the exact SMC-BVS posterior.
Its proof (`sources/W1-T03R/PROOF.md` §§1, 2, 4, 6: E1, E2(i), den′, T02(i♯), Lemma I, Lemma B, (C1)–(C10), Assembly)
modifies two locked proofs, [P1] and [P3], whose consumed steps are listed in `STATEMENT.md` §5. Those locked proofs
were checked only within one model family, so **their consumed steps are under review here as well**. No new
mathematics is proposed. You decide whether T03♯, as stated in `STATEMENT.md` v1.1, is **proved by the proof as
written** and can be accepted as checked mathematics. You are briefed to break it: assume there is an error and look
for it. Re-derive; do not sample.

### Six gates (a gate PASSes only if you hold no C, S or F finding against it)
* **G1 — correctness of every step.** Every changed step (E1(a),(b),(d), E2(i), den′, T02(i♯), Lemma B, (C1)–(C10),
  Assembly) and every consumed [P1]/[P3] step it relies on. Particular attention: den′ is extracted from the *proof*
  of [P1] `lem:den` (`sources/P1/PROOF_v3.tex:324-360`); the quantifier sup_m P₀(·) in T02(i♯); the restriction of
  SE uses to |J′(S)| ≤ j₀ and the crude bound (C6)(a) on the large-J′ branch; the exponent count in (C8); the
  beta-min constant in (C10); the three-way split in the Assembly.
* **G2 — hypotheses used = hypotheses stated.** Every hypothesis the proof uses is in `STATEMENT.md` §2 (or a reading of
  §4), and nothing in §2 is unused without reason. In particular: the recorded exponent A (no A ≥ 1, §4 item 3); s₀ ≥ 1;
  p = 1 (§4 item 4); fixed g₀, φ₀, M, σ*²; deterministic M_n, c.
* **G3 — no hidden assumptions:** every eigenvalue, rank or full-column-rank fact is supplied by R, SE_λ(j₀),
  SE_w(m♯_n; g₀) or interlacing, on exactly the sets where it is used; no surviving use of the locked full SE or of
  H-T02; no response-dependent cutoff, set or threshold; independence used only where it holds.
* **G4 — imports and statuses.** Each [P1]/[P3] result is used as stated (or, where a proof body is used, the body
  says it); `STATEMENT.md` §5 lists the consumed labels completely and quotes their statuses verbatim
  (`sources/statement/registry_theory_main_L68.tsv`; for the NBH rows quoted there you may read only rows TH121–TH128 of
  `Theory_work/Old_Projects/New_BVS_Headquarters/ID_REGISTRY.md`).
* **G5 — constants, rates, uniformity.** Every constant, exponent and threshold: where it comes from and what it
  depends on; every O_P uniform where it is summed or maximised (over m, J, S, j ∈ J_n(c)).
* **G6 — fidelity.** `STATEMENT.md` is faithful to the statement of record (`sources/statement/W6-FIXREV2_STATEMENTS.md:15-61`)
  and the approved card (`sources/statement/TLF_434-499.md`); its §1 target matches the coded score, prior and
  standardisation (`reviews/INPUTS.txt`); `path:line` citations resolve (`citecheck.py`).

### Sweep duties (Tier B: no separate sweep; they are part of your review)
1. Statement copies vs proof statements: `STATEMENT.md` §2–§3 vs `PROOF.md:44-47,127-132,160-168` and the record.
2. Quantifiers and uniformity throughout (fixed vs uniform; deterministic vs data-dependent; "for n ≥ n₀").
3. Each lemma's scope vs every downstream use (e.g. (C3) only for |J′(S)| ≤ j₀; (C5) for |J| ≤ m♯_n, comparison
   models outside Ω; E2(i) on its p ≥ 2 domain).
4. `REPORT.md` and its REGISTRY block vs `STATEMENT.md`: line pointers resolve to the right clause, nothing restated
   that STATEMENT does not say, statuses not overstated.
5. `DEPS.tsv` spot-check without opening review files: run `python3 -B deps_hash.py` (stdout only) and confirm every
   row's `sha` equals its `checked_sha`, that the rows cover every proof step and consumed block, and that the named
   `checked_by` files exist.

### Tags and what blocks (protocol v4 §5)
Tag every finding **C** (correctness: a step is wrong or unproved), **S** (strength: a claim says more than is proved,
or the proof uses a hypothesis the statement does not state), **F** (faithfulness: to the statement of record, to a
cited source, to the code as pinned, or STATEMENT in a derived text) or **E** (editorial: wording, notation, record,
citation form; never blocks). Name the clause or line and say what fails. **You must give `gates=FAIL` if you hold
any C, S or F finding of your own, whatever severity you would give it.** "A stronger theorem is provable" is not a
finding (note it separately as a proposal). Project convention (owner's rule, not a defect): every result here is
asymptotic (n → ∞) unless marked deterministic; do not score the size of n at which a bound becomes informative, or
the absence of finite-n guarantees; do score any asymptotic claim that is false, unproved, or stated too strongly.

## Output format (in your one file)
```
Verdict summary: one paragraph.
Per-claim table:
| id | decision |           (ACCEPT / REJECT / NOT-EXAMINED, one row each for W3-T03ACC:T03S.1 … T03S.5)
Gate table: G1 … G6, each PASS or FAIL, with what you re-derived.
Findings: numbered; each tagged C / S / F / E, with location (file:line), the problem, and the repair you propose.
Sweep duties 1–5: one paragraph each.
Score: x.y / 10 (reflects C, S, F only; 8.0 or more = acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6` (round R1, seat `astra`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6 seat=astra score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---
