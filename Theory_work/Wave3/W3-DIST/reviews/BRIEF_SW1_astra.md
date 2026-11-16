# BRIEF — exhaustive sweep SW1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are the exhaustive-sweep reviewer for theory ticket W3-DIST of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo). This file is your whole brief. Repo clone: `/home/fb31/Bayesian-Variable-Selection`. Paths
below are relative to the ticket folder `Theory_work/Wave3/W3-DIST/` unless they start with `Theory_work/`, `Scripts/`,
`Docs/` or `Papers/` (then relative to the repo root). **Change no git state. Write exactly one file:**
`reviews/SW1_sweep_astra.md`. Edit nothing else. Start no agents. No cluster jobs. Effort high, not above. Any
computation small, `nice`, at most 2 cores; temporary files only under
`/home/fb31/SMC_Theory_Department/tmp/20261116-W3-DIST-SW1/` (never `/tmp`), removed when done; no script may write into
the repository.

## What the ticket claims
A distribution-level consistency theorem for the coded method, of the kind of Song–Liang (2015, Theorems 1–2): the
exact coded posterior contracts in the Hellinger distance between joint (x, y) laws, random design, with an explicit
rate and an exponentially small exceptional probability (Theorems DIST-1, DIST-2, DIST-3); the same for what the coded
sampler returns (Theorem DIST-C); and reader versions with primitive assumptions (Theorem A, Theorem B, Corollary C).
Project convention (owner's rule, not a defect): all results are asymptotic (n → ∞) unless marked deterministic. Do not
list the size of n at which a bound becomes informative, or unoptimised constants, as a flaw. Do list any asymptotic
claim that is false, unproved, or stated more strongly than proved.

## Frozen content
The sweep is frozen in `reviews/MANIFEST_SW1.txt`. Its first line is `MANIFEST @@DIGEST@@`. **Quote this line verbatim at
the top of your review.** You may run `python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-DIST
Theory_work/Wave3/W3-DIST/reviews/MANIFEST_SW1.txt` (from the repo root; read-only).

## Pass 1 — blind first read (do this pass completely before Pass 2)
Read only:
- `STATEMENT.md` (the claims; §0 setting, §1 master theorems, §1R reader versions, §2 coded output, §3 lemmas, bridges
  and Proposition NEC, §4 consumes table, changelog) and `TARGET.md` (assumption map, parity table with Song–Liang,
  the fixed target clauses TC1–TC9 in §5, companion results TC10);
- the proof files: `lemmas/X.md` (Lemma X: §0–§8; Lemma X′: §9), `lemmas/DIST12.md` (DIST-1, DIST-2), `lemmas/NEC.md`
  (Proposition NEC), `work/B_transfer/H.md`, `T.md`, `DIST3.md`, `work/C_size/S.md`, `V.md`, `work/D_output/P6_DISTC.md`
  (Lemma P6, Theorem DIST-C), `COR_C.md` (Corollary C), `work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`,
  `ASSEMBLY.md` (Theorem A, Theorem B);
- `API_CARDS.md` (common definitions), `ASSUMPTION_MAP.md`;
- the external inputs listed in `reviews/INPUTS_R1.txt` (the locked proof [P1] of the identification of the coded
  posterior; statements of consumed claims; the pinned code; the project's map of Song–Liang). For context only, not
  frozen: the paper itself, `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf`, and
  `Docs/Experiments/P1M/DECISIONS.md` row D-17 (cited by DIST-C (C-ii)(γ) as a description, not a premise).
In this pass do **not** read `REPORT.md`, `DEPS.*`, `LOG.md`, `CHECKPOINT_*.md`, `ROUTES.md`, `PLAN.md`, `briefs/`, anything in
`reviews/` except the manifest and `INPUTS_R1.txt`, `work/api_attempts/`, `work/C_size/X12.md`, `lemmas/X_route_a.md`
(the last three are not on the proof path), and do not use `git log`, `git show` or `git diff` on the ticket folder.

**List every flaw in the whole package, not a sample.** Go through the statement and every proof file from the first
line to the last. A flaw is anything a careful referee would require to be changed. Named duties:
1. **Step-by-step correctness** of every proof file: re-derive the displayed inequalities, probabilities and constants.
2. **Statement copies against lemma statements**: every statement in `STATEMENT.md` against the statement proved in its
   proof file (hypotheses, constants, ranges of t and n, events, the order of quantifiers); §1R against `TARGET.md` §6
   (the two reader blocks must agree); the target clauses TC1–TC9 against what is proved. In particular TC3 and
   DIST-1 (c): the dependence of M₀ and of the radius constant C on the sparsity, through `lemmas/X.md` §0 and
   `lemmas/DIST12.md` D.1, D.4.
3. **Quantifiers and uniformity**: constants independent of the law of the data; one n₀ for the whole range of t; what
   is uniform over the class (RD) and what is not; measurability of events and of the cutoff; raw versus retained
   dimension and sparsity (p_raw, p_ret = r, s₀^r, s₀), true columns that are constant in the sample, s₀^r = 0, p = 2.
4. **Each lemma's scope against every downstream use**: wherever one file uses a result, event, constant or threshold
   of another, check the hypotheses and what exactly is delivered (H, T, X, X′ → DIST-1, DIST-2; S, V → X; DIST-1,
   DIST-2, DIST-3 and B0–B3 → Theorems A, B; Theorem A and DIST-C → Corollary C; P6 → DIST-C). No circular dependence.
5. **Hidden assumptions**: independence between the transfer event and the interface events; conditioning on the
   design; the intercept; the response scale (σ* arbitrary; bridge B0); moments of x; the window q_n for small p.
6. **Imports**: every consumed claim in `STATEMENT.md` §4 is used exactly as stated in its source, with its recorded
   status quoted correctly and its conditions carried ("conditional on …" in Theorem B, DIST-C, Corollary C).
7. **Fidelity to the method as coded**: the code facts of `STATEMENT.md` §2 against `Scripts/SMC_BVS/core/` (what the
   run returns, the store, its size, HPM/MPM, the mixture over models that the store law is); every `path:line` pin.
8. **Honesty of scope**: Proposition NEC and its "what this does not say" list (it must touch no target clause);
   the stretch items S-APX, S-EXP, S-FIT (labelled as candidates or open, nothing claimed); Remarks of §1R; the
   comparison with Song–Liang in `TARGET.md` §2 (each "matches / beats / short" row).
9. **Corollary C's reported-model conclusion (named point to check).** Corollary C's conclusion about the most
   probable reported model (HPM) was strengthened at v1.4: "if a completed run scored the true model and the posterior
   probability of that model exceeds ½, then the list contains it, it is the model the method reports as most
   probable, and π(𝒯) > ½". Verify it line by line (`work/D_output/COR_C.md` C2, `work/D_output/P6_DISTC.md` Corollary R1,
   the code: `Scripts/SMC_BVS/core/v3_run.R:142`, the store in `Scripts/SMC_BVS/core/cpp/v3_ledger.h`), including ties, the
   exact-arithmetic convention and what "reports" means in the code.
10. **Unharvested strength** (short): any strictly stronger statement that the existing proofs already give at no
   extra cost, or a hypothesis that the proofs never use.

## Pass 2 — records (only after Pass 1 is written down)
Now also read `REPORT.md`, `DEPS.tsv` and, for spot checks only, the review files it names in `reviews/`.
11. **REPORT and the registry blocks against STATEMENT**: every row of REPORT §1 (line ranges, proof file, status);
    every REGISTRY block at the end of REPORT (statement and premise line spans, assumptions, consumes, conclusion,
    rate, scope, depends_on, implies, sharpness) against `STATEMENT.md`; nothing restated differently, nothing upgraded.
12. **DEPS rows spot-checked against review files**: for at least eight rows, among them X, TC/DIST-1, T, S, B2, P6, NEC
    and R/Theorem-A, check that the file hash recorded is the current one, that the review file named exists and says
    what the row says, and that the state is right. Do not let the review files change your Pass 1 findings.

## Output format (in your one file)
```
MANIFEST <digest>                                  (verbatim first line of the manifest)
Summary: counts of CRITICAL / MAJOR / MINOR findings; one sentence on whether the package is ready for a council.
Findings: numbered consecutively (SW1-01, …), each with: class (CRITICAL = a claimed result is false or its proof has a
          gap with no local repair; MAJOR = a gap, mismatch or missing hypothesis that needs a new argument or a
          changed statement; MINOR = local wording, constant, citation or cross-reference repair), kind
          (C correctness / S strength: claims more than proved or uses an unstated hypothesis / F faithfulness to the
          code, to a cited source or to STATEMENT in a derived text / E editorial), location (file:line), the problem,
          and the exact repair you propose (or "no repair known").
Per-claim table: for each of DIST-1, DIST-2, DIST-3, DIST-C, Theorem A, Theorem B, Corollary C, Lemmas H, T, S, V, X, X′,
          P6, Proposition NEC, bridges B0, B1, B2-core, B2, B3, and each target clause TC1–TC9: proved as stated |
          proved after the listed repairs (numbers) | gap | false.
Unharvested strength: list, or "none found".
Checks performed: per file. Not checked: list.
```
Do not stop at the first findings; a sweep that lists a sample is a failed sweep. If a file is clean, say so
explicitly. End your reply with the summary line and the path of your file.
