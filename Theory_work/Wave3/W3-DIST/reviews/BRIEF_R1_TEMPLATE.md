# BRIEF — council round R1, seat `@@SEAT@@` (@@SEATDESC@@) — blind first read

You are one of the two council seats for theory ticket W3-DIST of the SMC-BVS project (Bayesian variable selection by
sequential Monte Carlo). This file is your whole brief. Repo clone: `/home/fb31/Bayesian-Variable-Selection`. Paths below
are relative to the ticket folder `Theory_work/Wave3/W3-DIST/` unless they start with `Theory_work/`, `Scripts/`, `Docs/`
or `Papers/` (then relative to the repo root). **Change no git state. Write exactly one file:** `reviews/@@OUT@@`
(UTF-8). Edit nothing else. Start no agents. No cluster jobs. Effort high, not above. Any computation small, `nice`, at
most 2 cores. **Do not write any file outside the repo clone and set no TMPDIR.** Prefer inline computation with no
files. If you need scratch files, put them only in `/home/fb31/Bayesian-Variable-Selection/.rc_tmp/W3-DIST-R1-@@SEAT@@/`
(inside the clone, at its root; **never inside the ticket folder**, whose content is frozen, and never in `/tmp`), and
delete that folder at the end. Do not add it to git. Never run a command that asks for an approval: nobody can answer it.

## What the ticket claims
A distribution-level consistency theorem for the coded method, of the kind of Song–Liang (2015, Theorems 1–2):
- **DIST-1, DIST-2, DIST-3** (`STATEMENT.md` §1): the exact coded posterior, prior as coded, contracts in the Hellinger
  distance between joint (x, y) laws under a random design, with an explicit rate and an exponentially small
  exceptional probability; DIST-2 drops the non-degeneracy interface at the price of one logarithm; DIST-3 is an
  oracle bound at the parametric rate.
- **DIST-C** (§2): the same for what the coded sampler returns (domination transfer; the returned list of models).
- **Theorem A, Theorem B, Corollary C** (§1R): reader versions under primitive assumptions (A1)–(A6).
- Lemmas H, T, S, V, X, X′, P6, bridges B0, B1, B2-core, B2, B3 (§3), and Proposition NEC (§3: a fixed-design example
  showing that Lemma X's non-degeneracy hypothesis cannot be dropped; stated as touching no target clause).
`TARGET.md` §5 lists the target clauses TC1–TC9 fixed for this ticket; §2 compares the result with Song–Liang item by
item. `REPORT.md` §1 gives one row per claim (statement lines, proof file, status).

## Frozen content
The round is frozen in `reviews/MANIFEST_R1.txt`. Its first line is `MANIFEST @@DIGEST@@`. You may run (from the repo
root, read-only) `python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-DIST
Theory_work/Wave3/W3-DIST/reviews/MANIFEST_R1.txt`.

## Files you may read
The files listed in that manifest, namely:
- `STATEMENT.md` (version @@VER@@), `TARGET.md`, `REPORT.md`, `ASSUMPTION_MAP.md`, `API_CARDS.md` (common definitions);
- the proof files: `lemmas/X.md` (Lemma X: §0–§8; Lemma X′: §9), `lemmas/DIST12.md` (DIST-1, DIST-2), `lemmas/NEC.md`,
  `work/B_transfer/H.md`, `T.md`, `DIST3.md`, `work/C_size/S.md`, `V.md`, `work/D_output/P6_DISTC.md` (Lemma P6, DIST-C),
  `COR_C.md` (Corollary C), `work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`, `ASSEMBLY.md` (Theorems A, B);
- the numerics summaries `work/F_numerics/RESULTS.md`, `work/numerics/RESULTS.md` (evidence only, never a proof step);
- the external inputs listed in `reviews/INPUTS_R1.txt`: the locked proof [P1] that the coded posterior is the
  contrast-model posterior, the statements of consumed claims, the pinned code, the project's map of Song–Liang.
For context only (not frozen, not premises): the paper `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf`;
`Docs/Experiments/P1M/DECISIONS.md` row D-17 (cited by DIST-C (C-ii)(γ) as a description); and
`Theory_work/INFRA/registry/claims.tsv` (to check quoted statuses).
**Do not read** anything else in any `reviews/` folder (except the manifest and `INPUTS_R1.txt`), any `LOG.md` or
`CHECKPOINT*.md`, `DEPS.tsv`, `DEPS.md`, `ROUTES.md`, `PLAN.md`, `briefs/`, `work/api_attempts/`, `work/prior_probe/`,
`work/C_size/X12.md`, `lemmas/X_route_a.md` (not on the proof path), and do not use `git log`, `git show` or `git diff` on
the ticket folder. This is a blind first read: form your verdict without any earlier version, review, disposition or
score. Markers such as [S1-07], [P1-04], [L6-01], [v0.4], [amended, …] point to earlier internal rounds whose reports you
are not given; `REPORT.md` §2 lists them. Judge the mathematics and the records as they stand.

## What the council decides
Whether this package can be accepted as **checked mathematics**. You are briefed to break it: assume there is an error
and look for it. Re-derive; do not sample. Suggested weight: the key lemma `lemmas/X.md` and the assembly
`lemmas/DIST12.md` first (they carry DIST-1, the headline); then `work/B_transfer/T.md` (the distribution-free transfer),
`work/C_size/S.md`, the bridges and `work/E_bridges/ASSEMBLY.md` (Theorem A is what a reader will quote); then DIST-C and
Corollary C against the code; then Proposition NEC.

Six gates (each PASS or FAIL, with a justification that names what you re-derived and gives file:line evidence):
* **G1 — correctness of every step.**
* **G2 — hypotheses used = hypotheses stated**, claim by claim (`STATEMENT.md` against each proof file; §1R against
  `TARGET.md` §6; TC1–TC9 against what is proved, including TC3 / DIST-1 (c): the dependence of M₀ and of the radius
  constant on the sparsity).
* **G3 — no hidden assumptions** (independence between the transfer event and the interface events; conditioning on
  the design; moments of x; the intercept; the response scale; raw versus retained dimension and sparsity; true
  columns constant in the sample; s₀^r = 0; small p; measurability of events and of the cutoff).
* **G4 — imports have adequate status and say what is claimed** (each consumed claim of `STATEMENT.md` §4 used as stated
  in its source; statuses quoted correctly, none upgraded; conditions on inputs below PROVED-CHECKED carried as
  "conditional on …" in the statuses of `REPORT.md`; every new lemma has a cross-family check on file according to
  `REPORT.md` §1–§2).
* **G5 — constants and rates tracked** (every constant, exponent, threshold and range: where it comes from, what it
  depends on, whether the claimed uniformity over the class of laws and over t holds).
* **G6 — fidelity to the method as coded and honesty of scope** (the code facts of `STATEMENT.md` §2 and every
  `path:line` pin against `Scripts/SMC_BVS/core/`; the prior as coded; what the run returns; Proposition NEC's "what
  this does not say"; stretch items labelled as open; the comparison with Song–Liang in `TARGET.md` §2; `REPORT.md` and
  its registry blocks say no more than the statement and the proofs support).

**Named point to check (both seats).** Corollary C's conclusion about the most probable reported model (HPM) was
strengthened at v1.4: "if a completed run scored the true model and the posterior probability of that model exceeds ½,
then the list contains it, it is the model the method reports as most probable, and π(𝒯) > ½". Verify it line by line
(`work/D_output/COR_C.md` C2, `work/D_output/P6_DISTC.md` Corollary R1, the code: `Scripts/SMC_BVS/core/v3_run.R:142`, the store
in `Scripts/SMC_BVS/core/cpp/v3_ledger.h`), including ties, the exact-arithmetic convention and what "reports" means in
the code, and say in your review what you found.

Project convention (owner's rule, not a defect): every result here is asymptotic (n → ∞) unless marked deterministic.
Do not score the size of n at which a bound becomes informative, unoptimised constants, or the absence of finite-n
guarantees. Do score any asymptotic claim that is false, unproved, or stated more strongly than proved.

## Findings and what blocks
Tag every finding with one kind:
- **C** correctness: a step is wrong or unproved;
- **S** strength: the text claims more than is proved, or uses a hypothesis it does not state;
- **F** faithfulness: to the code as pinned, to a cited source, or to `STATEMENT.md` in a derived text (`REPORT.md`,
  `TARGET.md`, a registry block);
- **E** editorial: wording, notation, record, citation form, presentation of numerics.
Only C, S and F findings count: each must name the clause or line and say what fails. E findings never block and never
lower the score. "A stronger theorem is provable" is not a finding: list it separately as a better-theorem proposal.
**You must give `gates=FAIL` if you hold a C, S or F finding of your own, whatever severity you would give it.**

## Output format (in your one file)
```
Verdict summary: one paragraph.
Gate table: G1 … G6, each PASS or FAIL with its justification.
Per-claim table: | id | decision | for every id of REPORT.md §1 (W3-DIST:DIST-1, DIST-2, DIST-3, DIST-C, Thm-A, Thm-B,
        Cor-C, H, T, S, V, X, X', NEC, P6, B0, B1, B2core, B2, B3), decision = ACCEPT | REJECT | NOT-EXAMINED
        (one line of reason for REJECT or NOT-EXAMINED).
Findings: numbered (R1-@@SEAT@@-01, …), each with kind (C / S / F / E), location (file:line), the precise problem, and
        the repair you propose.
Better-theorem proposals: list, or "none".
Overall score: x.y / 10 (C, S and F only; 8.0 or more means acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```
The frozen content cannot be edited after this round without a new round.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST @@DIGEST@@` (round R1, seat `@@SEAT@@`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=@@DIGEST@@ seat=@@SEAT@@ score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

Final message: the gate verdicts, the score, your C / S / F findings (short), and the path of your file.
