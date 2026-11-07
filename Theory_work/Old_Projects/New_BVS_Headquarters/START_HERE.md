# START HERE: New BVS Headquarters archive (for the Theory Meta HQ)

This folder is the complete, self-contained record of the T3 thread **"New BVS Headquarters"** (2026-11-02 → 2026-11-04). That thread ran the SMC-BVS theory campaign and chose the method and the paper-1 theorem list. Read this page first, then follow the reading order below.

**Source (fallback if anything here is unclear):** threadId `5e38497d-7dfd-48f9-88e9-b21895922f58`, environmentId `b18966a3-98dd-4510-a488-d5dfb1650daa` (Owls). Read it with `t3_thread_read` only; don't message it. Repo: `FbStatsQuant/Bayesian-Variable-Selection`, branches `origin/theory/*` (all snapshotted in `branch_snapshots/`). On Owls the clone is `/home/fb31/Bayesian-Variable-Selection`. The thread's original working dir `/home/fb31/BVS_GH/Bayesian-Variable-Selection` no longer exists, and that is why the thread's last three runs failed [pos 1672, 1674, 1676].

## Where the theory stands (one page)

**Paper-1 thesis** (HQ at [pos 1044]): "In split-and-merge, correlation breaks correctness. In local-to-global SMC, correlation costs only sequential depth and particles, never correctness." Felipe's objectives, in order ([pos 1020], [pos 1030], MEET-v31 ground rule 6):
1. accuracy in recovering the true posterior;
2. parallel scalability over particles and islands, not over variables [pos 1113];
3. BVS selection accuracy.

Target venue: Biometrika, with Lean certificates for the key results [pos 1015].

**Method: SMC-BVS v3.1, approved by HQ** ([pos 1557], [pos 1584]; Felipe approved the four method-process decisions at [pos 1304]). Statistically it is v3 unchanged: g = n g-prior, BB(1,p) size prior, cap K = min(p,⌊n/2⌋), a correlation-clustered block start π₀ that can be sampled exactly, a tempering bridge with invariant moves, islands, unbiased Ẑ, and HPM = the best model ever scored. On top of that it adds:
- a parallel execution layer over islands (checked bit for bit on 3 of 3 designs);
- optional stacking;
- LS0, a start-mode local search (changed 0 of 2,394 study HPMs);
- the Ẑ-weighted PIP as the primary PIP;
- a general-h accumulator;
- a certificate card;
- NA outputs.

The 2,400-fit study stands; no re-run is needed. Full spec: `branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`; in plain language: `branch_snapshots/MEET-v31/FOR_FELIPE_FINAL_METHOD.md`. Settings and their (n,p) rules are in `notation_and_conventions.md`.

**Theorem list: 8 main cards and 12 supplement cards.** The theorem meeting closed with "Open questions: none" [pos 1626], and HQ approved it with one change [pos 1639]. **Felipe had NOT yet approved the list when the thread ended** [pos 1673]. Plain-language table from [pos 1650]:

| ID | Card | Guarantee (HQ's plain words, [pos 1650]) |
|---|---|---|
| TH01 | M1 V/H | Validity under any correlation, plus error bounds for PIPs, joint inclusions and general summaries |
| TH02 | M2 WS | Weight stability: the start-to-posterior distance is controlled by cross-block correlation; the bridge stays stable as correlation grows; the literal one-shot form is proved false |
| TH03 | M3 START | Laws for the start: guaranteed mass, error decomposition, masking, dilution |
| TH04 | M4 Z𝒯 + card | Evidence brackets, a sound certificate card, and a proved accuracy result for masked designs |
| TH05 | M5 HPM | Selection by the reported best model: a finite-n bound; consistency with LS0 on masked designs |
| TH06 | M6 SEP + Lemma KL | Why the merge alone fails: one-shot correction needs polynomially many draws |
| TH07 | M7 STG | Stage laws: correlation costs about log₂(masking depth) sequential stages |
| TH08 | M8 Prop D | Work, depth and width at the island level, compared with Song–Liang §6 |

The supplement cards are TH09–TH20 (S-T, S-TARGET, S-BLOCKS, S-KERNEL, S-IDENT, S-CERT, S-OUT, S-Z, S-POOL, S-LIM, S-REP, S-LEAK). Future work is FW1–FW27 = CJ01–CJ27; the 6 drops are DR01–DR06. The exact statements are in `02_theory.md` §A2–§A3, copied verbatim from `branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md`.

**Proof status, honestly:**
- Most card clauses are "PROVED (candidate)", "PROVED (by this seat, unchecked)" or "PROOF SKETCH". Checks are recorded per clause: same-family (SF), cross-family (XF: Astra A-REV1–9, Sol PC1) or Lean.
- Nothing has been adopted or locked by Felipe; adoption is his decision.
- The Lean library has 101 theorems, 0 `sorry`. It covers the T21 inequality, T07, T11(iii) and Theorem A; the T21 inequality and Theorem A are cores of M5 (K72, K65).
- The main open edges:
  - the p ≫ n versions (API-PXNGAP is a repair candidate, not cross-checked);
  - N1 for general h (binding §13.1);
  - the §5.3 constants, useful only for ε ≲ n^{−1/2}/p;
  - the Song–Liang separation, NOT proved (only a numerical counterexample, 20/20 vs 5/318);
  - asymptotic thresholds near n ≈ 2·10⁶ versus the study's n = 200 (N200 gives the finite-n account: 558 predicted vs 571 observed wrong reports).

**Empirics:**
- 2,400 fits (n = 200, p ∈ {500, 1000}): 1,829 exact, 565 posterior misses, **0 search misses**, 6 stopped. SMC-BVS is best at c = 0.5 (370/600, 340/600) and slightly behind SuSiE, SSL and horseshoe at c = 1 [pos 933].
- ABL-CONF (confirmatory start test): the prior start underestimates the evidence on every design (Claim 2 LICENSED). "The block start is cheaper" is INCONCLUSIVE overall [pos 1669].

**What was next:** Felipe approves or edits the list (decisions at [pos 1650]). Then wave 1 of the per-theorem HQs runs: M1, M3 and the foundations pack LP-FOUND (charters in `branch_snapshots/MEET-THM/HQ_CHARTERS/`). Each HQ loops to a refereed proof plus a Lean certificate.

## Reading order

1. **This file**, then `README.md` (layout and conventions).
2. `05_open_questions_and_next_steps.md`: what is pending and what to do next.
3. `02_theory.md`: the final state, with verbatim cards, IDs, statuses and dependencies. Use `ID_REGISTRY.md` to look up any ID or native name.
4. `03_results_and_conclusions.md`: the final results (theory and numbers), with files.
5. `notation_and_conventions.md`: symbols, priors, settings, and the conventions that changed.
6. `03b_reasoning_and_traces.md`: why things are as they are: the decision log, dead ends, reversals and reviewer findings.
7. `02b_theory_campaign_history.md`: the full history of every campaign-era result (T01–T39, waves W1–W8, F-/O-/A-/API- runs), with verbatim statements, refutations and counterexamples. Large (≈2.7 MB), so grep it.
8. `01_overview_and_timeline.md`: the arc of the thread by phase.
9. `04_code_and_files_index.md`: every branch, path, script, thread and credential location.
10. `transcript/INDEX.md` → verbatim messages (`transcript/part_*.md`) and traces (`transcript/traces/`).
11. `branch_snapshots/`: the verbatim .md/.tex/.lean of every `theory/*` branch plus the pre-campaign `Docs/` (main@c4ef0dc). **These are the authoritative mathematical texts.**

## Which file for what

| Need | File |
|---|---|
| Exact statement of a final card | `02_theory.md` §A2/§A3 → `branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md` |
| Status, who checked it, dependencies | `ID_REGISTRY.md`, `02_theory.md`, `branch_snapshots/MEET-THM/REGISTRY_PAPER1.md` (K-numbers) |
| History of a result (versions, repairs, refutations) | `02b_theory_campaign_history.md` (grep the native name or ID) |
| Why a decision was made | `03b_reasoning_and_traces.md` (DEC entries), then `transcript/traces/` |
| The exact words of Felipe or HQ | `transcript/part_*.md` by `[pos N]` |
| Proof texts | `branch_snapshots/<BRANCH>/PROOF.md`, `REPORT.md`, `*.tex`; Lean in `branch_snapshots/L-LEAN/` |
| HQ charters for the next phase | `branch_snapshots/MEET-THM/HQ_CHARTERS/` and `MEET-THM/MINUTES.md` §2.5 |
| Data, scripts, result files (not copied) | `04_code_and_files_index.md`, `branch_snapshots/NONTEXT_INDEX.tsv` (git blobs) |
