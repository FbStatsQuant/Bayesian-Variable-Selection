# SMC-BVS v3.1: final method of paper 1, written as a diff against METHODOLOGY_v3

Amended by HQ on 2026-11-04 (AMENDMENT_HQ_01.md) after independent review.

**Status: FINAL from MEET-v31 (chair), for HQ approval.** Not yet approved by HQ or Felipe. Item 1 (block start versus plain start) is closed by the pre-registered rule as **Outcome 2** (`ITEM1_ABL_START.md`). Nothing in this file is implemented, verified or proved unless a cited source says so. Status words (PROVED, OPEN, PROOF SKETCH, ...) are copied from their sources and never upgraded. Results argued by one seat and not yet proof-checked are marked **"seat-derived, unchecked"**.

**Closure gate and binding goals (HQ, 2026-11-04).** Open method questions: none, **conditional on N9** (running). If N9 fails, the method question reopens before the theorem meeting. N9 (kernel reversibility and self-adjointness, exact start sampler; THEOREM_REVISION_INPUTS N9) is a closure gate, checked against the code on branch `theory/N9-KERNEL`. For every obligation whose failure would leave a binding proposal goal unmet (N1 / general h, §13.1; S4 weight stability, §5.3; N9, §5.1): if it fails, the binding goal is not met by withdrawal; HQ escalates to Felipe for a method reconsideration or an explicit scope change.

**Baseline.** `Docs/Methodology/METHODOLOGY_v3.md` (written "M" below; § numbers are M's).

**Decision sources** (all in `theory_campaign/MEET-v31/`):
- `SYNTH_R1.md` (S1), `SYNTH_R2.md` (S2: §1 status table, §2 item-1 rule, §3 proposals), `SYNTH_R3.md` (S3: adopted texts R3-1 to R3-7);
- `DOSSIER.md` §2 (the v3.1 proposal (a)–(g));
- seat files `R2_A/B/C.md`, `R3_A/B/C.md`;
- `evidence/2026-11-03_PC1_proof_check.md` (PC1), `evidence/2026-11-03_PC2_certificate_card.md` (PC2), `evidence/AMEND_01_general_np.md` (AMEND_01), `evidence/2026-11-03_concurrency_runs.md` (CONC), `evidence/2026-11-03_pip_rescore/REPORT.md` (RESCORE);
- background: `origin/theory/METH-AUDIT:theory_campaign/METH-AUDIT/REPORT.md` §4–5 (MA), whose change classes are used throughout:
  - **ADDITIVE**: outputs on completed fits are unchanged or nested;
  - **POST HOC**: computable from saved fits, no re-run;
  - **LAW-PRESERVING**: same law, different seed-to-uniform map;
  - **WORKHORSE**: changes the method's law.

---

## 0. Summary

**v3.1 is v3 unchanged as a statistical method, plus a list of additions.** The following all stay exactly as in M:
- the target posterior (M §5);
- the blocks, tables and composite start (M §6.3);
- the neighbour graph (M §6.4);
- the move round (M §6.5) and resampling (M §6.6);
- the calibration law (M §6.6–6.9);
- the budgets (M §3);
- the HPM decision (M §6.10);
- the evidence estimator (M §6.12).

The additions fall into five groups:
1. **A parallel execution layer.** Final islands, diagnostic islands, local-search scans and the block-table stage run concurrently, with results bitwise-identical to serial execution where this has been checked.
2. **Optional stacking**, R′ = 4k final islands at unchanged N_e.
3. **LS0**: a local search from the start mode, run after the final local search.
4. **Reporting changes.** The Ẑ-weighted PIP becomes primary. A general-h accumulator and a POST HOC certificate card are added. Unavailable outputs give explicit NA fields.
5. **Wording and classification fixes** from the (n, p)-generality audit (item 9).

Sources: S1 item 3, S2 §1, S3 R3-1 to R3-4, MA §5.

**Does the 2,400-fit study need a re-run? No.** The study stands as **v3.1 at R′ = 4, with POST HOC additions** (MA §5; DOSSIER §1 ground rule 8; S2 §1). This means its saved sampler estimates are reusable with stated reporting limitations. Full v3.1 records are not yet produced: LS0 integration and flags, the NA interface, the certificates and the primary rescoring are pending; no statistical refit is needed for these POST HOC tasks. The answer for each change is in the "effect on the 2,400 fits" column of §2. In short:
- **Bitwise-neutral on completed fits.** The parallel layer (a), (b), (c), (h) and process workers. (a) has been executed bitwise on smoke plus 3/3 study designs (CONC). (b) has not been executed yet (W-cal, §6).
- **Not exercised by the study.** Stacking: the study is R′ = 4, and its islands 1–4 are the baseline record.
- **LS0.** It changed the HPM in 0 of 2,394 completed fits in the O-LS0 test export (DOSSIER §2(f)). It is not yet in the production core, and the integrated replay is pending (§6).
- **POST HOC from the saved per-island outputs.** These are the Ẑ-weighted primary PIP, both MPMs and R_eff, and the certificate card.
- **Wording only.** The output convention, calibration contract, cost and depth statement, and item-9 rows e1–e8 and w1–w7. Every one of these rows says "study effect: none" (S2 §3 P-9 table).

**What is NOT claimable for the study:**
- **Joint posterior summaries** (pair inclusions, size distribution via the general-h accumulator). The measured-round populations were not saved (S3 R3-3: "No joint-summary claims for the 2,400 study fits").
- **The Ẑ-weighted (now primary) PIPs and MPM on the full study.** These are claimable only after the full rescoring on the NOTS/laptop bundles. So far only 3 designs have been rescored (S2 §0.2; RESCORE). The study's equal-weight PIPs (e.g. MPM_eq = S₀ in 1,779/2,394) remain valid, labelled as the **secondary** PIP.
- **Any stacking (R′ > 4) result.** The R = 32 × 312 concurrency runs split the population; they are not stacking at N_e and must not be cited as validating it (R2_C §2; THEOREM_REVISION_INPUTS V3 note 5).
- **A 4-core speed-up.** The 1.9× figure is a 2-core measurement (S1 §0.1; R2_A §2).
- **"Bitwise" for the concurrent calibration (b)** until W-cal runs (S1 item 3).
- **"Depth free of N, H, R"** (S2 D3d).
- **LS0 as "run by the production core"** until the merged-LS0 replay runs (S2 D3c; §6).
- **The certificate card**, wherever the study's top store was not saved. Whether the bundles contain the stores was not checked here (R3_B R3-1: "computable for any saved fit whose top store is on disk").
- **Any depth or speed claim for the block start.** Item 1 closed as Outcome 2: no such claim (§2 row 0; `ITEM1_ABL_START.md`).

**Optional re-runs, all HQ decisions, none of them method questions:**
1. **The 6 `resource_limit` fits.** These are S5 wall-time stops (MA §4 C1). They can be replayed under the parallel layer as operational evidence, labelled as a separate execution result. Such a replay cannot establish a delivery theorem (S2 D8; R2_C D8).
2. **Full POST HOC PIP rescoring.** This is not a refit. It needs the per-island `pip_r` and `log_Z_r` from the NOTS bundles (`/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/`) and the laptop. The script is `evidence/2026-11-03_pip_rescore/pip_rescore.R` (S2 §0.2).
3. **A final re-run at the end of the project, only if needed** (ground rule 8; MA §5: a final run with stacked islands "can only improve it").

---

## 1. What stays (by § of METHODOLOGY_v3)

Unless §2 lists a change, each section stays verbatim.

| M § | Content | v3.1 |
|---|---|---|
| Header, Requirements (2)–(5) | scalable; theory-aligned; no bare tuning constants; Felipe's decisions kept | unchanged. Requirement (1) gets wording change e8 (§2 #22). |
| §1 | one-paragraph description | unchanged (S1 item 3; THEOREM_REVISION_INPUTS M1) |
| §2 Inputs | X, y, seed, allocation | unchanged as data. The allocation is re-classified as a declared (c) input (§2 #22). |
| §2 Outputs | HPM with provenance, near-tie list, PIPs, MPM, evidence, flags, diagnostics, maps | kept, with additions (§2 #11–#17) |
| §2 Statuses | `exact`, `completed`, `schedule_limit`, `numerical_failure`, `resource_limit`, `y_constant`, `no_predictors`, `invalid_input` | kept. Two are added: `degenerate_n` (e3) and `unsupported_size` (e7). |
| §2 Flags | `escalated`, `checks_passed_*`, `forced_pilot_steps`, `grid_unconverged`, `local_limit`, `low_empirical_ESS`, `near_tie_truncated`, `local_certified` | kept. `ls0_improved` is added. `global_certified` keeps its field name for compatibility and is documented as a heuristic numerical flag (e5). |
| §3 Notation and budgets | K, B, ℓ, L, N₀, H₀, T₀, R = 4, tiers | **values unchanged**. Labels and classes change (B*, T₀ note; §2 #23–#26). |
| §4 Preprocessing, rules 2–6 | constant-column drop, y constant, stable standardisation, duplicate report, preflight | unchanged. Rule 1 (input domain) changes (e3). Rule 6 / §8.6 gets a better estimate (e6). |
| §5 Target posterior and reduction statement | g = n, τ = 1, IG(0.01, 0.01), BB(1, p), cap ⌊n/2⌋ | **unchanged** (Felipe's model) |
| §6.1 Execution order | preprocess → exact or (blocks, calibration, freeze, final, local search, report) | unchanged in order. Additions: concurrency, R′ islands, extra search from c₄, LS0 last (§2 #1–#10). |
| §6.2 Exact branch | streaming enumeration, rule Σ C(p, k) ≤ (5H₀ + 4N₀)p | rule unchanged. Wording w2 (§2 #27). |
| §6.3 Blocks, tables, start | complete linkage, size cut, next-fit packing, exact tables, product start π₀ with exact Z̄₀, bridge γ_φ | **unchanged.** The table stage runs in parallel (§2 #4). Start: kept; item 1 = Outcome 2 (§2 row 0). Wording w5. |
| §6.4 Neighbour graph | r_n = √(2 log p / n), ≤ B partners, forced best partner, symmetric union | unchanged. Fallback stated (w3). |
| §6.5 Move round | m = p + B + 2 steps in a fresh random order per particle and round | **unchanged.** Changing it is WORKHORSE (THEOREM_REVISION_INPUTS M1; MA §4 C10). |
| §6.6 Resampling and pilot | multinomial each stage; ESS 0.90; 60 halvings; floor 1/T_e | unchanged. ESS 0.90 is classified (c) (§2 #25). |
| §6.7 Candidate set and grid | V; restricted ESS; construction; rebuild loop ≤ ℓ; grid-equality convergence | **unchanged** (S1 item 4: rule and budgets kept; C9 rejected) |
| §6.8 Calibration and final runs | pilot, diagnostic islands, final islands on fresh streams | unchanged in law. Concurrency is added (§2 #1–#2). Streams extended to R′ (§2 #6). |
| §6.9 Checks and escalation | E1–E3, forced steps, grid flags, `local_limit`; final flags only | unchanged as calibration triggers, which define the law of 𝓒 (S1 item 6). Labelled heuristics. Under stacking, flags are reported per record (§2 #7). LS0 does not fire E3 (§2 #9). |
| §6.10 Local search and HPM | ≤ ℓ moves + one scan; HPM = strict max over every scored model; exact-equality ties | unchanged. Scans run in parallel (§2 #3). LS0 joins "every scored model" (§2 #9). Near-tie list extended (e2). |
| §6.11 PIPs | RB average of o_j over 4 measured rounds per island | estimator per island unchanged. **Primary and secondary pooling swap** (§2 #11). |
| §6.12 Evidence | Ẑ_r unbiased given frozen 𝓒; pooled Ẑ; 0.05Ẑ Markov bound | unchanged. The card adds max{Z_𝒯, 0.05Ẑ} (§2 #13). |
| §6.13 Numerics | Cholesky; Q recompute below 10⁻⁸·yᵀy; QR fallback; `numerical_failure` | unchanged (class (d), S2 §3) |
| §7 Pseudocode | — | updated as in §2 (#1–#10) |
| §8.1–8.5 Cost | preprocessing, tables, SMC, grid, local search | unchanged as formulas, except §8.5's local-search bound: the scan size p + K(p − K) is corrected to p + k*(p − k*) per scan, with k* = min(K, ⌊p/2⌋), times (ℓ + 1) scans (K can exceed p/2, and SMC can dispatch with K = p). A depth statement and calibration share are added (§2 #19). |
| §9 By construction | exact branch exact; exact iid start; reversible moves; unbiased Ẑ_r given 𝓒; HPM best of scored | unchanged. Precision added (§2 #21). |
| §9 Not guaranteed | global mode; accuracy of Ẑ or PIPs; modes never reached | unchanged. Limitation wordings refined (§2 #21). |
| §10 Assumptions | data, design, signal, computation | unchanged, except the neighbour-scale sentence (w1, §2 #27) |
| §11 Theory programme V1–V13 | — | superseded for the theorem meeting by THM-SYNTH's THEOREM_LIST plus `THEOREM_REVISION_INPUTS.md`. Method-relevant edit: V6's "R-consistency of the secondary pooling" now refers to the **primary** pooling (§2 #11). |
| §12 Differences from v2 | — | kept. A "v3 → v3.1" table is added, equal to §2 of this file. |
| §13 Open items | — | "outer limit of B" closed by e1. Grid-cost measurement folded into the cost account (S2 D3e). Implementation and verification of v3.1 → §6 of this file. |
| §14 Sources | — | add the MEET-v31 files listed at the top |

---

## 2. What changes

Column "class" uses MA's classes, or "spec text" for wording that does not change any computed value. "Effect on the 2,400 fits" says whether any study value changes and whether a re-run is needed.

### Row 0: start (item 1, closed: Outcome 2)

| # | change | M § | spec text | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 0 | **Composite block start** | §6.3, §1 | "The v3 block start is retained in every outcome of the agreed ABL-START rule (SYNTH_R2 §2). Item 1 closed as **Outcome 2 (keep, reframe)**: the start is presented as the exactly computable, theorem-bearing local step (S1/S2) plus the parallel table stage, with **no depth or speed claim**. The ablation may be printed as exploratory (12 designs × 1 seed)." | none (start unchanged) | none | S2 §2 (rule); S3 R3-6 (procedure); `ITEM1_ABL_START.md` (outcome) |

For the record, the agreed rule allows exactly three outcomes (S2 §2, S3 R3-6). The result was **Outcome 2**: 9 of 12 designs were complete for arms A–C, and all 9 were inconclusive because arm C's log Ẑ was 2.6–13.3 nats below A and B (`ITEM1_ABL_START.md` §2–3). Certified count: arm C's log Ẑ is below the best score found by any arm on 10/12 designs, so Ẑ < Z in exact arithmetic; arms A and B on 0 (`evidence/item1_scripts/HQ_NOTE_v2.md`). The three outcomes:
- **Outcome 1:** keep the start, depth claim allowed.
- **Outcome 2:** keep the start and reframe it as the exactly computable, theorem-bearing local step plus the parallel table stage, with no depth or speed claim. This is also the result when fewer than 9 designs are conclusive. The committed v1 script (`apply_rule.py`) lacked this absolute gate; HQ's corrected `evidence/item1_scripts/apply_rule_v2.py` enforces need = max(9, ⌈0.75·complete⌉) and reproduces Outcome 2 (`HQ_NOTE_v2.md`, commit 8f6051b).
- **Outcome 3:** a real issue is flagged. v3.1 still ships the block start; the ablation is reported; a ≤ 20-seed paired check runs on the two worst designs; a WORKHORSE candidate goes to Felipe only if that check confirms.

No outcome reopens item 1 in this meeting (S3 R3-6). The backfit start is rejected regardless (§4).

### Parallel execution layer

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 1 | **(a) Concurrent final islands** | §6.1, §6.8, §7, §8.6 ("Islands may run sequentially") | "The R′ final islands run as concurrent **process** workers, each with its own score cache and ledger. Their stores and running HPM are merged by Lemma S before the final local search. Output is bitwise-identical to serial execution (Prop W). 'Bitwise' is scoped to one binary (`Makevars.v3`: `-ffp-contract=off -march=x86-64-v2`), single-thread BLAS and process workers." | ADDITIVE (bitwise) | none. Executed bitwise on smoke + 3/3 study designs (CONC; S1 §0.1). Serial study output = v3.1 output. No re-run. | DOSSIER §2(a); S1 item 3; R2_B D3f; MA §4 C1 |
| 2 | **(b) Concurrent diagnostic islands** | §6.7–6.8 | "In each rebuild iteration the 4 diagnostic islands run as concurrent process workers (persistent per tier), merged before each local search and before V is rebuilt (Prop W-cal). 'Bitwise' may **not** be claimed for (b) until W-cal has been executed (§6)." | ADDITIVE (bitwise) **claimed from code reading only**. If W-cal fails, it becomes LAW-PRESERVING and the wall-clock claim is capped at the D4 numbers (R2_B §5 item 4). | none. The study ran calibration serially, so its calibration is the reference that W-cal must reproduce. No re-run. | DOSSIER §2(b); S1 item 3; S3 R3-7 note; MA §4 C2 |
| 3 | **(c) Parallel local-search scans** | §6.10 | "Each scan's candidates (p + k(p − k) flips and swaps) may be scored in parallel. The best strict improvement is chosen by a max-reduction that keeps the lexicographic tie rule, so the search path equals the serial one." | ADDITIVE (bitwise if the reduction keeps the tie rule) | none. No re-run. | DOSSIER §2(c); S1 item 3; MA §4 C3 |
| 4 | **(h) Block-table stage as the explicit parallel local step** | §6.3, §8.2 | "Block tables are scored in parallel over blocks and sub-models; each score is independent. No floating-point summation order may change under a bitwise claim. Parallel convolution and other reductions need a separately specified order, or a narrower numerical-equivalence claim." | ADDITIVE (bitwise) | none. No re-run. | S2 D3e; R2_C D3e; R2_A D3e; R2_B D3e |
| 5 | **Process workers; counter rule** | §6.1 (new sentence) | "Workers are processes. If threads ever share `Data`, the mutable diagnostic counters (`cpp/v3_score.h:20–21, 231–236`) must become per-worker private counters, merged deterministically." | ADDITIVE (engineering) | none | S2 D3f; S1 §0.4 [chair-checked] |
| 6 | **GUARD-W semantics** | §2 statuses, §8.6, §6.1 | "Any worker stop, LS0 stop or guard stop ⇒ no output. The fit returns the corresponding unavailable status with all estimate fields NA (#15), never a partial estimate." Here an LS0 stop is an operational interruption (worker, guard or resource stop) before LS0 completes. A completed LS0 that ends on its move cap is not a stop: it returns output with `local_limit`, and L1 = "n/a" (#10). Lemma RO (a guard that reads no uniforms is stop-only) stays as recorded (XF VERIFIED). That the v3.1 worker, merge and LS0 code satisfy GUARD-W is a **code-audit obligation** (§6), not a mathematical gap. | ADDITIVE (spec) | none on completed fits. The 6 `resource_limit` fits stay stops. | S1 item 3; S3 R3-1 (B), R3-5(ii); R3_B R3-1 amendment 1 |

### Stacking

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 7 | **Optional stacking R′ = 4k at N_e** | §3 (R), §6.1, §6.8, §6.9, §7 | <ul><li>"R′ = 4 by default. Optionally R′ = 4k, at **unchanged N_e**, declared before final randomness (before stream 10)."</li><li>"Final islands use streams 10, …, 9 + R′. Islands 1–4 keep streams 10–13. **N_e is never split** across more islands."</li><li>"With R′ > 4, an **extra local search runs from the islands-1–4 centre c₄**, besides the search from the expanded centre. The post-search scored set is then nested and HPM(R′) ⪰ HPM(4) (Cor W-R with the extra search, PC1 claim 6)."</li><li>"Two records are kept. The **expanded record** covers all R′ islands, pooled Ẑ over R′ and the expanded store; it carries the run's reported flags. The **baseline record** covers islands 1–4, with its own baseline HPM, the search from c₄ and its own E1–E3, low-ESS and `local_certified`. It is kept whenever baseline reproducibility is claimed."</li><li>"Each record has its own certificate card (#13)."</li></ul> | ADDITIVE (nested) | none. The study is R′ = 4, and each study fit is its own baseline record. No re-run. | DOSSIER §2(d); S2 D3a, D3b, P-9 w7; S3 R3-4 (w7); PC1 claim 6; THEOREM_REVISION_INPUTS M7 |

PC1 claim 6 notes that E1, E2 and low-ESS on islands 1–4 match the v3 run. E3 and `local_certified` match only when they are evaluated on the search from c₄. The baseline record therefore holds both of those.

### LS0

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 8 | **LS0: local search from the start mode** | §6.10, §6.1, §7, §2 (provenance) | <ul><li>"After the final local search (and after the extra search from c₄ when R′ > 4), run one local search with the §6.10 rules from the start mode S̃₀ = argmax γ₀. S̃₀ is computed exactly by the block DP, with the size-then-lexicographic tie rule."</li><li>"LS0 reads no uniforms. Every model it scores joins the all-scored set and the stores."</li><li>"Models first scored by LS0 have provenance `ls0`. The flag `ls0_improved` is set if LS0 raised the best score."</li><li>"**An LS0 improvement does not fire E3.** E3 refers only to the final local search from the HPM centre."</li><li>"An operational LS0 interruption means no complete output (GUARD-W, #6). A completed LS0 capped at `local_limit` still returns output (#10)."</li><li>"Start-mode ties: keep the enumeration fast path (cap 10⁶, `cpp/v3_start.h:183`). On truncation, use a deterministic tie-aware DP that returns the prescribed smallest-size, lexicographically smallest maximiser without enumerating ties (e4, #29)."</li></ul> | ADDITIVE | Production had no LS0. In the O-LS0 test export LS0 changed **0 of 2,394** HPMs, which implies `ls0_improved` = FALSE on all 2,394. 0/2,400 tie truncations; all 2,400 had a single tie (`/home/fb31/ls0_work/agg_final/ls0_per_fit.csv`, R2_C §4.2 E2). The merged-core replay is pending (§6). No re-run. | DOSSIER §2(f); S1 item 2, D3c; S2 D3c; R2_B D3c; S2 P-9 e4; S3 R3-4 (e4) |
| 9 | **D3c wording for LS0** | paper / §12 | "Appending LS0 preserves the preceding sampler computation. Island outputs, Ẑ and PIPs are unchanged. The all-scored set is enlarged (nested) and the best score cannot fall. The bounded top store is **𝒯_new = top_c(𝒯_old ∪ 𝒮_added)**, not a superset of 𝒯_old, because of eviction (`cpp/v3_ledger.h:41`). Near ties, provenance, flags and certificates are recomputed for the returned model. HPM unchanged on 2,394/2,394 (test export)." The sentences "stores nested" and "bitwise fit" are **struck**. | spec text | none | S2 D3c (C's correction + B's flag); R2_C D3c |
| 10 | **Certificate attaches to the returned Ŝ** | §6.10, card | "`local_certified` and card item L1 are evaluated on the finally returned Ŝ, from whichever search ended on it (final search, extra search from c₄, or LS0). A completed LS0 that ends on its move cap (`local_limit`) gives L1 = 'n/a'; the fit's output is still returned. An operational LS0 interruption is a GUARD-W stop (#6)." | ADDITIVE (spec) | none (LS0 changed no HPM) | S3 R3-1 (A); R3_A R3-1 addition 2 |

### Reporting: PIPs, evidence, general h, certificates, unavailable outputs

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 11 | **Ẑ-weighted PIP primary; equal-weight secondary; both MPMs; R_eff** | §6.11, §2 outputs, §11 V6 | <ul><li>"**Primary:** PIP̂_j = Σ_r Ẑ_r PIP̂_rj / Σ_r Ẑ_r over the R′ final islands."</li><li>"**Secondary (named):** the equal-weight mean over islands."</li><li>"Report MPM_Ẑ = {j : primary PIP̂_j > ½} and MPM_eq. Either may exceed K and is reported as computed."</li><li>"Report R_eff = (Σ_r W_r)² / Σ_r W_r² with W_r ∝ Ẑ_r."</li><li>"Neither normalised estimate is generally unbiased at a finite budget."</li><li>"The R-scaling guarantee is stated for the primary PIP; the equal-weight PIP keeps its single-island bias for every R (Prop P(i))."</li></ul> | POST HOC | No refit. The study's equal-weight PIPs and MPM_eq stay valid as the secondary. The primary and MPM_Ẑ need the full rescoring from the NOTS bundles. Done so far on 3 designs: MPMs never differ, max\|ΔPIP\| ≤ 1.3·10⁻³, island ESS 1.88 on S5 r002 (S2 §0.2). | DOSSIER §2(e); S1 item 5; S2 D5; R2_B D5 (R_eff); MA §4 C5 |
| 12 | **General-h accumulator** (adopted text) | new §6.11b | **Declaration.** "𝓗 is a finite list of bounded model-space functions. The default list is fixed from (X, y): model-size indicators, and joint inclusion on neighbour-graph edges (≤ 2pB pairs). A user may also declare h measurable in (X, y, 𝓒), fixed before stream 10. An h defined from other calibration information (streams 0–9) is covered only if that information is included in 𝓒 before it is frozen (enlarge 𝓒 when necessary); measurability in streams 0–9 need not imply measurability in the compressed 𝓒. No final-run selection." **Accumulation.** "H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi), taken after each complete measured round (φ = 1, equal weights after multinomial resampling). Report μ̂(h) = Σ_r Ẑ_r H_r(h) / Σ_r Ẑ_r and the equal-weight version." **Not allowed.** "Products of marginal RB-PIPs are not joint estimates. v3.1 ships plain measured-round particle averages for joint h (c_h = 0). Rao–Blackwellisation is used only for the marginal PIPs. No RB joint estimator ships." **Archive (optional).** "The measured-round populations as a key → count multiset. An h chosen adaptively after the run does not inherit the fixed-h guarantee." **Continuous parameters.** "Use h̄(S) = E[h \| S, X, y]." **Descriptive only.** "The measured-round frequency of the returned HPM is **not** in 𝓗. It may be printed as a descriptive diagnostic with no theorem, next to e^{F(Ŝ)}/Ẑ." Placement in code: `cpp/v3_engine.h:351–359`. The identity for general h is a PROOF SKETCH (N1). | ADDITIVE (reads no uniforms) | none. Not recoverable for the study, so **no joint-summary claims** for the 2,400 fits. | S2 D7, P-D7; S3 R3-3 (adopted text); R3_A, R3_B, R3_C R3-3 |
| 13 | **Certificate card** (POST HOC) | new §6.14; §2 outputs; §6.12 | **PC2's "Recommended minimal card for v3.1"**: G1, G2, L1, L2, L3 always; R optional. Spec text in §2.1 below. | POST HOC | Computable for any saved fit whose top store is on disk; L1/L2 also need a cheap rescoring (R3_A R3-1; R3_B R3-1). Not checked here whether the NOTS bundles contain the stores. Not a gate. | S2 D2; S3 R3-1; PC2 summary + minimal card |
| 14 | **Z_𝒯 and the underestimation certificate** | §6.12 | "Report Z_𝒯 = Σ_{S∈𝒯} e^{F(S)} over the deduplicated reported store. Ẑ < Z_𝒯 implies Ẑ < Z." This is part of G1 and ships in any case. | POST HOC | as #13 | S1 item 6; PC2 G1; THEOREM_REVISION_INPUTS M10 |
| 15 | **Unavailable output = explicit NA** | §2 statuses, §7 | "On every return without complete output (`resource_limit`, `schedule_limit`, `numerical_failure`, GUARD-W stops, LS0 stop, degenerate statuses), `fit$log_Z` and **every estimate field** (Ẑ_r, Ẑ, bounds, PIPs, MPMs, μ̂(h), card) are NA by exact name. Partial calibration or island values may be archived under their own labels; they never masquerade as final estimates." This fixes the partial-match hazard, where `fit$log_Z` silently returned `log_Zbar0` (API-AUDIT §2b). | ADDITIVE (interface) | Completed fits are untouched. Only the 6 stopped fits' records change: a consumer can no longer print a wrong evidence for them. | DOSSIER §2(g); S1 item 8; R1_B §2.8.1; R1_C:256 |

### Conventions, contract, cost

| # | change | M § | exact new spec text (short) | class | effect on the 2,400 fits | decided in |
|---|---|---|---|---|---|---|
| 16 | **Output convention** | Requirements (1), §2, §9 | "Every estimate on the output event 𝒪 is a function of (X, y, seed, binary). The allocation and hardware decide **delivery only** (stop-only guard, Lemma RO). Guarantees are stated for the potential (uninterrupted) run and as **P{𝒪, ·}** (joint with output), never as P(· \| 𝒪). P(no output) is an operational frequency that depends on the allocation and hardware, and is reported with them (V13)." | spec text | none. The 6 stops are delivery events. | S2 P-9 e8; S3 R3-4; R2_A §4; R2_C §4.4; PC2 C6 item 4 |
| 17 | **Paper sentence on the card's probability** | §9 | "The probability that a run returns a card with a false claim is at most 5%." The sentence "claims hold with probability ≥ 95% given the run reports" is **not** proved and is struck. | spec text | none | PC2 C6 item 4 |
| 18 | **Calibration contract** | §6.7–6.9 (new paragraph) | "The calibration output 𝓒 (grid, budgets N_e, tier, R′, V-independent settings) is frozen before any final randomness. Validity of the final estimates (unbiased Ẑ_r, PIP identities) holds conditionally on **any** frozen 𝓒, whatever happened in calibration. The grid satisfies Theorem G's cap. There are ≤ ℓ rebuilds per tier (≤ 2ℓ in total with escalation, `v3_calib.R:85, 141–149`). The restricted ESS controls one-step weight dispersion on V only. The statuses `schedule_limit`, `grid_unconverged` and `escalated` are distinguished. Rebuild convergence, P(S₀ ∈ V) and P(schedule_limit) are **OPEN theorem obligations, not inherent limitations**. Rebuilds, tier, T and convergence are tabulated POST HOC from saved fits." | spec text | none. The tabulation is POST HOC (§6). | S1 item 4; S2 D4; THEOREM_REVISION_INPUTS M8 |
| 19 | **Depth and cost statement at the implemented (island) level** | §8 (new §8.8) | <ul><li>"With island parallelism, the particle-round contribution to depth is N_e·(T + L + 4)·(p + B + 2) **sequential elementary-step slots** per island at tier e (not scorer operations or seconds). Score costs, setup (Gram, correlations, clustering, tables), calibration, grid construction, reductions and finite-worker scheduling are added and counted. If R′ exceeds the worker count, islands run in waves."</li><li>"'Depth free of N, H, R' is **not** claimed for v3.1."</li><li>"For a single tier, calibration trajectory work relative to the final run is (1 + 4I)·H₀ / (4N₀) = 0.0512 + 0.2048·I, with I ≤ ℓ the number of rebuilds in that tier. With escalation (two tiers) it is [H₀(1 + 4I₀) + H₁(1 + 4I₁)] / (4N₁). These ratios count trajectory lengths only; other costs still differ. This is **seat-derived, unchecked** (R2_A D4). It matches 3 designs: predicted 0.46 / 0.67 / 1.69, observed 0.45 / 0.62 / 1.76."</li><li>"Calibration can exceed the final run (S4: 1,184.5 s versus 671.8 s), so any wall-clock claim counts calibration, and W-cal is on its critical path."</li><li>"Island-parallel results may be reported with their actual cost. A particle-parallel depth claim, or any demonstrated fit with p > 2,500, requires C6 (§3; HQ's union trigger)."</li><li>"No speed-up versus sequential MCMC is claimed without a stated comparator at matched accuracy."</li></ul> | spec text | none | S2 D3d, D4; S1 §0.2 [chair-checked]; R2_A D4; R2_C D3d |
| 20 | **D6(i) memory wording** (adopted) | §8.1, §8.6, §9 | "A full-coordinate move round visits all p coordinates and requires scoring access to every predictor, through X or sufficient statistics (8np bytes for X). That access may be local, shared or distributed; its computation and communication costs must be counted. Neither a private copy of all X nor a private 8p² Gram matrix per worker is inherent. C7 is the declared Gram-free scoring path, law-preserving in exact arithmetic, with floating-point fidelity checked separately." | spec text | none | S3 R3-2 |
| 21 | **§9 limitation wordings** (THM-SYNTH A2-type corrections) | §9, §6.12 | <ul><li>**(ii)** Restate M §9's "without a usable upper bound on Z" as what is proved. (1) T31(c) (PROVED-LOCKED; PC2 C1(c)): the properties of Ẑ behind the 95% bound (positive, finitely many values, mean Z, iid islands) imply no two-sided relative-error bound: for every c₀ > 0 and η ∈ (0, 1) some such law has P(Ẑ < c₀Z) ≥ 1 − η, so {Z ≥ αẐ} places no upper limit on Z/Ẑ. This is a non-implication from the estimator's law, not a data-specific impossibility. (2) An analytic bound exists, Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} (PC1 claim 1, PROVED). Its gap to Z is data-dependent; PC1's ν·log(n+1) compares against m(∅), not against Z, and is not a universal looseness. The blanket "no *useful* upper bound on Z from the run's record alone" is **not** claimed.</li><li>**(iii)** "The assumption-free part of the evidence lower bound is Markov. max{Z_𝒯, 0.05Ẑ} keeps 95% coverage on the output event" (PC1 claim 2, PROVED; output form CORRECT WITH AMENDMENT).</li><li>**(iv)** "Masked weight variance: the mechanism is PROVED in kind (E1/E2, SEP-B); its severity on the production grid is OPEN (V11)."</li><li>**Checked:** M §9 and §6.12 do **not** contain the A2 sentence "Ẑ errs/can fail only downward". No deletion is needed in M. If the paper discusses the masked regime, it uses PC1 claim 4's corrected wording: "Ẑ underestimates Z with high probability; the complementary rare event carries compensating overestimates of the same total mean; Markov caps them, P(Ẑ > 20Z) ≤ 0.05; the certificate Ẑ < Z_𝒯 detects underestimation only."</li></ul> | spec text | none | S2 §0.1, D6; PC1 claims 1, 2, 4; THEOREM_REVISION_INPUTS M14 |

### Item-9 resolutions: e1–e8 (adopted, with S3 refinements)

| # | id | change | M § | exact new spec text (short) | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|---|
| 22 | e8 | "Seed alone" versus `resource_limit` | Requirements (1), §2 | Requirement (1) becomes: "Runnable from X, y and one integer seed, with no statistical tuning beyond published defaults. The job's allocation (memory, wall time) is a declared (c) input that decides delivery only. Every estimate on 𝒪 is a function of (X, y, seed, binary)." The literal "seed alone" sentence is corrected. | spec text | none | S2 P-9 e8; S3 R3-4 |
| 23 | e1 | B* = 16 relabelled | §3 table, §8.7, §13 | "B* = 16 is a declared **(c) budget for exhaustive tables**. It keeps table work ≤ 2^{B*}·p/B* = 4,096p scores and memory linear in p. An unbounded B = ⌊√p⌋ would make tables super-polynomial. W7-PART's g_max ≤ B < 2g_min is a hypothesis of one partition theorem (B = 14 covers g ∈ 8..14; B = 16 covers 9..16), not a method parameter. The study's g = 5 is the theorem obligation PART-pairing." §8.7's "implementation limit … C++ start (about B ≤ 20)" is replaced by this text. | spec text | none (B = 14 in all 2,400) | S2 P-9 e1; S3 R3-4 |
| 24 | e2 | Near-tie window | §6.10 | "Keep the 10⁻⁹-nat near-tie list (informational; the HPM uses exact equality). Also print η(Ŝ), the scorer's error expression, and a second near-tie list at max(10⁻⁹, 2η(Ŝ)) labelled **heuristic**. The exact pairwise margin is η(S) + η(Ŝ). The store keeps only (F, S), so 2η(Ŝ) is the labelled proxy." | POST HOC | none to any decision | S2 P-9 e2; S3 R3-4 (A, B) |
| 25 | e3 | Input domain | §4 rule 1, §2 statuses | "Reject n = 0. n = 1 → status `degenerate_n` (centred y is 0; no estimates). Zero predictors → existing `no_predictors`. **n = 2 is admitted**: K = 1, B = 1, E = p + 1, so the exact branch runs. At n = 2 every centred non-constant column is proportional to (1, −1), so all singleton models have exactly equal F. The exact output is ∅, or the lexicographically smallest singleton with a p-fold exact tie, reported as such." This n = 2 output statement is R3B's, **seat-derived, unchecked**. Duplicates are kept and reported, not collapsed (M §4 rule 5; `cpp/v3_core.cpp:715–728`); that chair-checked code fact is not a proof of the n = 2 output. The n = 2 admission is a proposed extension: current preprocessing still rejects n < 3 and raw p = 0 (`v3_preprocess.R:103–107`). | ADDITIVE | none | S2 P-9 e3; S3 R3-4 (e3, chair-checked fact; B's sentence) |
| 26 | e4 | LS0 start-mode tie cap | §6.10 (LS0) | as in #8. The invariant "DP output = the prescribed choice" is an OPEN obligation (N3). A and B sketch a greedy index-by-index route with a feasibility max-plus DP (seat-derived, unchecked). | ADDITIVE | none (0/2,400 truncated) | S2 P-9 e4; S3 R3-4 |
| 27 | e5 | `global_certified` | §2 flags, §6.2, §9 | "The exact-branch comparison against the scorer's error expression (`cpp/v3_score.h:240`, `cpp/v3_core.cpp:535`) is a **heuristic numerical margin**, reported as a labelled numerical flag. 'Certified' is reserved for validated arithmetic." M §2's "with numerical comparisons validated" and M §9's "the exact branch returns the exact HPM, PIPs and Z" stay true in exact arithmetic; the floating-point claim is labelled heuristic. | POST HOC (interface) | none (the study used the SMC branch, where the flag is always FALSE, `v3_run.R:147`) | S2 P-9 e5; PC2 `global_certified` verdict |
| 28 | e6 | Memory preflight | §8.6, §4 rule 6 | "Before setup use J ≤ p blocks (not ⌈p/B⌉); after setup use the actual J. Shared and per-worker memory are accounted separately (each concurrent worker's populations, cache, archive). The result is labelled 'estimate', not 'certified peak'." | ADDITIVE (engineering) | none at study size. J = 46–60 (p = 500) and 95–120 (p = 1,000) versus proxies 36 and 72 [chair-checked]; still well under 8 GiB. | S2 §0.5, P-9 e6 |
| 29 | e7 | Checked arithmetic | §2 statuses, §6.2, §7 | "Integer, stream-id and allocation arithmetic are checked before use. Overflow returns the explicit status `unsupported_size`." (Name fixed in MINUTES §4.) | ADDITIVE (engineering) | none | S2 P-9 e7; S3 R3-4 |

### Item-9 wording fixes w1–w7

| # | id | change | M § | exact new spec text (short) | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|---|
| 30 | w1 | Neighbour scale in §10 | §10 (design bullet) | Replace "between-cluster correlation at the √(log n / n) scale — the same scale as the neighbour threshold" with "… at the r_n = √(2 log p / n) scale of the neighbour threshold". The two scales agree (up to constants) only when log p = Θ(log n); an upper bound p ≤ n^A alone is not enough. No familywise-screening interpretation of r_n. | spec text | none | S2 P-9 w1; S3 R3-4 |
| 31 | w2 | Exact-branch boundary | §6.2 | "all p ≤ 3,000 at n ≤ 5" → "all p at n ≤ 5" (K ≤ 2, E ≈ p²/2 < 4N₀p) [chair-checked] | spec text | none | S2 §0.5, P-9 w2 |
| 32 | w3 | Neighbour fallback | §6.4 | "When r_n ≥ 1 (equivalently p ≥ e^{n/2}; equality cannot occur for positive integers n, p, so this is p > e^{n/2}) no pair exceeds the threshold, so for p > 1 each j keeps only its forced single largest-\|r\| partner: the graph is the symmetric 1-nearest-neighbour graph." | spec text | none | S2 P-9 w3 |
| 33 | w4 | T₀'s ℓ² term | §3 | "For integer n, p and ℓ = ⌈log₂(n + p + 1)⌉, the ℓ² term exceeds 1,000 exactly when n + p ≥ 2³¹ (inclusive; at equality ℓ = 32). T₀ = 1,000 in every practical case." | spec text | none | S2 P-9 w4; S3 R3-4 (C's text) |
| 34 | w5 | No correlation cut | §6.3 (added sentence) | "The dendrogram is cut by node size only (≤ B). There is no correlation-height threshold." This corrects AMEND_01's and any other text implying a correlation cut. M §6.3 itself already describes a size-only cut. | spec text | none | S2 P-9 w5 |
| 35 | w6 | Stale "up to 20" comment | code comment only | the bound is 16 | none | none | S2 P-9 w6 |
| 36 | w7 | Stream map for R′ | §6.1, §6.8, §7 | "Final streams are 10..9+R′, with R′ declared before stream 10." (= #7) | spec text | none | S2 P-9 w7 |

**Constants paragraph (adopted, S3 R3-4, C's text).** "Retain every listed numerical value. The following are declared (c) effort/storage budgets, combined with their (b) dimension-dependent formulas:
- the population and stage floors;
- the calibration ratio;
- the island and measured-round counts;
- the tier multiplier;
- the store and cache limits;
- the exact-dispatch threshold.

ESS 0.90 is class (c): a one-step dispersion/effort budget, not a modelling convention or a full-posterior accuracy guarantee. The 60 bisection halvings are class (d), a numerical implementation convention. One-nat diagnostic thresholds are declared (c) escalation/diagnostic criteria, not rounding tolerances. These values are conventions, not derived optima; changing them is not automatically law-preserving."

"No separate p ≪ n / p ≫ n rule is needed: K, B, N₀, the exact-branch rule and r_n switch regime by formula" (S2 §3; S3 R3-4).

### 2.1 Certificate card: spec text (PC2 minimal card + S3 R3-1 additions)

**Header (applies to every item).**
- Every line is stated in exact arithmetic.
- Until SC(η_F) is established by validated arithmetic and VAL-FP holds at production size, every computed number carries the label **"numerical implementation of an exact-arithmetic certificate"**, with η printed (`v3_score.h:242–246`).
- **L1, L2 and R run under one declared certificate budget** (scores and B&B nodes, printed with the card). On exhaustion the item reports "unresolved". A failed or unfinished certificate never changes the fit's status (A).
- The card is computed after the run and never feeds back into calibration (S1 item 6).
- **Under stacking there is one card per reported record** (baseline and expanded), each with its own 𝒯 and Z_𝒯 (B).

**G1 (deterministic).** 𝒯 is the deduplicated reported store and Z_𝒯 = Σ_{S∈𝒯} e^{F(S)}. Then:
- Z_𝒯 ≤ Z;
- π(S) ≤ e^{F(S)}/Z_𝒯 for every S;
- π(A) ≤ Σ_A e^F / Z_𝒯 for every A ⊆ 𝒯;
- π(S)/π(Ŝ) ≤ e^{−g} on 𝒯 ∖ {Ŝ}, with g = F(Ŝ) − max_{𝒯∖{Ŝ}} F;
- Ẑ < Z_𝒯 ⇒ Ẑ < Z.

**G2 (one-sided, output-level).** Simultaneously for all S:
- π(S) ≤ min{1, e^{F(S)}/max(Z_𝒯, 0.05Ẑ)};
- π(Ω ∖ 𝒯) ≥ 1 − Z_𝒯/(0.05Ẑ). This is mass **outside the reported store** (never scored, or scored and evicted). It is **not** a bound on never-scored mass.

G2 fails only on {Z < 0.05Ẑ}, and P(run returns output and G2 is false) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05. This is a probability **joint with output, never conditional on completion** (C). Premises are PC1 claim 2 (i)–(iv). Premise (i) reads: "Lemma RO (XF VERIFIED) plus GUARD-W, the implementation fact 'any worker stop, LS0 stop or guard stop ⇒ no output' for v3.1 code: a code-audit obligation, not a mathematical gap" (B). If Z_𝒯 ≥ 0.05Ẑ, G2 holds surely (C6′).

**L1 (local).** Evaluated on the finally returned Ŝ, from whichever search ended on it. A completed LS0 that ends on its move cap (`local_limit`) gives "n/a" (A); an operational LS0 interruption gives no output (GUARD-W). If `local_certified`, then F(S) ≤ F(Ŝ) for every feasible flip or swap. Report:
- g_add, with +∞ if |Ŝ| = K;
- g_del, with +∞ if Ŝ = ∅;
- g_swap, with +∞ if there are no swaps;
- ρ_loc = π(Ŝ | {Ŝ} ∪ 𝒩(Ŝ)).

**L2 (subsets).** g_sub = F(Ŝ) − max_{S⊊Ŝ} F(S) and Σ_{S⊊Ŝ} π(S)/π(Ŝ). With max ∅ = −∞: when Ŝ = ∅, g_sub = +∞ and the relative subset mass is 0.

**L3 (best-of-scored).** If 𝒯 = top-(40p+1) of the realised scored set 𝒮 and |𝒯| ≥ 2, then π(S) ≤ e^{−g}π(Ŝ) for all S ∈ 𝒮 ∖ {Ŝ}, with g = F(Ŝ) − F(top[2]). This holds under LS0 because 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) (R3_B R3-1).

**R (optional).** A declared region rule U(X, y, Ŝ) ∋ Ŝ, with node budget and τ printed. B&B on [∅, U] ∩ Ω, dropping leaves with |L| > K, gives (a)–(c) as in PC2. "Unresolved" on budget exhaustion. In floating point, (a) needs Φ̃ ≤ F̃(Ŝ) − 2η_F.

**Card-level statement.** "The probability that a run returns a card with a false G2, L or R claim is at most 5%", in exact arithmetic. G1, L and R are true surely. The floating-point version (≤ 0.05e^η + ε) needs validated SC **and** VAL-FP, neither of which is established, so it carries the numerical label (C).

**Excluded:**
- C2 (conditional on PW2);
- C5 (needs S₀);
- the "unscored mass" wording;
- the B&B cost remark;
- any rigorous reading of `global_certified`.

Sources: PC2 lines 194–235; S3 R3-1.

---

## 3. Declared v3.2 path (not shipped in v3.1)

| id | change | class | condition / note | source |
|---|---|---|---|---|
| C6 | Per-particle counter-based random streams, e.g. stream = f(seed, island, stage, particle). This enables particle-parallel islands, so the move-round depth loses the N_e factor; population reductions remain. The serial map stays the default reproducibility mode. | **LAW-PRESERVING** (IND-T restated over distinct (island, stage, particle) triples; a one-line re-proof) | **Implemented and law-checked** (R = 4, two stream maps, 20 seeds, compare log Ẑ and PIP distributions) **iff paper 1 claims particle-parallel depth or demonstrates any fit with p > 2,500.** This is HQ's disposition: the union of the two recorded conditions (Seats A/B: any p > 2,500, R2_A:23, R2_B:21, R3_B:44; Seat C: a particle-parallel depth claim). The narrower trigger was not unanimously adopted. Felipe decided (2026-11-03) that paper 1 claims island-level depth only, and the study has p ≤ 1,000, so neither trigger currently fires. Island-parallel results may be reported with their actual cost. | S2 D3d; MA §4 C6; R2_A D3d; R2_B D3d; R2_C D3d; R3_B; HQ (AMENDMENT_HQ_01) |
| C7 | Gram-free scorer, for p ≳ 3·10⁴ or wherever the 8p² private Gram binds | LAW-PRESERVING in exact arithmetic; floating-point fidelity checked separately (VAL-FP-type η) | Declared path for memory (D6(i), §2 #20). Chunked distance computation with the same ordering rule keeps the blocks bitwise (R2_A §4). | S3 R3-2; MA §4 C7 |
| C11 | Faster exact complete linkage (nearest-neighbour chain, O(p²)). The neighbour-graph sort, grid bisection, convolution and pooling also go into the cost account and the roadmap. | ADDITIVE if blocks are reproduced exactly (tie rule kept) | Roadmap for p ≳ 10⁴. Current clustering is O(p²) memory, O(p²)–O(p³) time (`cpp/v3_blocks.h:46–108`). | S2 D3e; MA §4 C11; R2_A D3e |

---

## 4. Rejected changes

| Change | One-line reason | Source |
|---|---|---|
| Backfit start (API-RESID) | WORKHORSE; it needs a full re-run and has no theorem; no exact sampler with a known normaliser was exhibited for it (why arm D was dropped), so Ẑ unbiasedness is not available; ground rules 1, 5, 8 not met. The earlier "headline gain capped at 6/2,400" rationale is withdrawn: a changed start does not nest scored sets. The backfit start is recorded as future work. | S1 item 1; HQ (AMENDMENT_HQ_01) |
| C8: split N_e into R ≫ 4 smaller islands | Neutral for Ẑ to first order (Cor V), but equal-weight PIP bias grows ∝ R/N_tot and masked delivery per island may fall. In effect WORKHORSE (changes a declared budget). | MA §4 C8; S1 item 3 |
| C9: shorter or shared calibration | WORKHORSE (schedule rule). It touches T38(b1′), Theorem G and (0_H). Calibration depth is addressed by (b) and C6 instead. | MA §4 C9; S1 item 4 |
| C10: parallel-in-particle move kernel (informed or tempered-Gibbs flips) | WORKHORSE (move kernel). It breaks R5(b2), BG3 and V5's self-adjointness proof. The m = p + B + 2 factor is inherent to the chosen kernel and is stated, not fixed. | MA §4 C10; S1 item 3; THEOREM_REVISION_INPUTS I1 |
| HPM–MPM disagreement flag | No provable power. Uninformative at π(Ŝ) ≤ 0.37. HPM stays the only decision rule; MPMs are reported descriptively. | S1 item 2 |
| Truth-based gate for the primary PIP (B's R1 rule) | Closeness to the binary truth is objective 3, not posterior accuracy (objective 1). B withdrew it. | S2 D5; R2_B D5; R2_C D5 |
| Rao–Blackwellised joint estimator | The kernel never computes pair conditionals (`cpp/v3_engine.h:349–364`); it would be new code with its own unverified identity. v3.2 at most. | S3 R3-3(b) |
| PSIS-k̂ / R̂ flags | No positive property. Weight-based diagnostics from the observed record have no universal detection guarantee for never-visited modes (E1c, V12; Chatterjee–Diaconis Thm 2.1). | S1 item 6 |
| Feeding certificates back into calibration | POST HOC is the adopted policy: the card is computed after the run and never feeds back. This is a policy, not a mathematical necessity: a certificate computed only during calibration could in principle be frozen into an enlarged 𝓒, while feedback from final-run information would break the frozen-𝓒 contract (§2 #18). | S1 item 6; R3_A R3-1 |

---

## 5. Generality in (n, p) (ground rule 9): the required table

The settings are merged from R2_A §4, R2_B §4 and R2_C §4.1. Classes are the **final** ones (S2 §3 P-9 + S3 R3-4), using AMEND_01's labels:
- (a) modelling convention with a stated reason;
- (b) explicit function of (n, p) or X;
- (c) declared resource budget;
- (d) numerical tolerance;
- (e) arbitrary.

**No setting is class (e) in the method's law** (S2 §3; all seats). Every (e)-by-label item is resolved by e1–e8 or w1–w7. Numerical boundaries quoted from seats are seat-derived unless marked [chair-checked].

| # | setting (value; source) | class | reason | behaviour as n, p grow | action |
|---|---|---|---|---|---|
| 1 | g = n, τ = 1 (M §5; `v3_score.h:175`) | (a), (b) | unit information; ridge keeps m(S) finite for collinear X_S | p-free; τ matters more for p ≫ n (collinear sub-models) | keep (Felipe) |
| 2 | IG(0.01, 0.01) (M §5) | (a) | proper, as the proofs require | pairwise effect ≤ n·b₀\|1/Q₁ − 1/Q₂\| on standardised data; relative to the gap it is not uniformly negligible (two equal-size, nearly collinear singleton models give a relative rate effect → 0.0142; review check, SOL1 #43); negligibility needs residual-scale assumptions; not negligible at tiny n | keep; no universal "negligible" claim (R2_C) |
| 3 | BB(1, p), w(k) = ½/C(2p−1, k), W_K explicit (M §5) | (a), (b) | sparse, multiplicity-aware; the project theory is for it | defined for every finite p; dense growing truths are not its regime | keep |
| 4 | Cap K = min(p, ⌊n/2⌋) (M §3, §5) | (a), (b) | keeps near-interpolating models out | void for p ≤ n/2; binds for p ≳ n/2; K = 1 at n = 2, 3; s₀ > K unrecoverable by definition | keep |
| 5 | Input domain: n ≥ 2, p ≥ 1 (v3.1, proposed; current code rejects n < 3, `v3_preprocess.R:103–107`) | (b) | standardisation and the target are defined at n = 2 | n = 2 → exact branch (K = B = 1, E = p + 1); n = 1 → `degenerate_n`; n = 0 rejected | **e3** (§2 #25) |
| 6 | Exact-constant column drop; `y_constant`; `no_predictors` (M §4) | (a) | removes undefined scales | regime-free | keep |
| 7 | Standardisation: max-abs, centre, SD (n−1) (M §4) | (a), (b) | affine and permutation invariance | regime-free | keep |
| 8 | Near-constant anchored two-pass route at √ε_mach (`v3_preprocess.R:47`) | (d) | cancellation protection, not screening | regime-free | keep; document (R2_C) |
| 9 | Duplicate report \|r\| ≥ 1 − 10⁻¹⁰ (M §4 rule 5; `v3_core.cpp:722`) | (d) | reporting only; duplicates are kept | regime-free | keep |
| 10 | B = min(⌊√n⌋, ⌊√p⌋, B*) (M §3) | (a), (b) | Felipe's rule; B ≤ K and B ≤ p | √p binds for p < n, √n for p > n; B = 1 at n = 2, 3 | keep |
| 11 | **B* = 16** (M §3, §8.7; `v3_core.cpp:142`) | **(c)** | exhaustive-table budget: ≤ 4,096p scores and 65,536p bytes | binds once n, p ≥ 289; theorem SIZE condition: B = 16 covers groups 9..16 | **e1** (§2 #23) |
| 12 | ℓ = ⌈log₂(n + p + 1)⌉ (M §3) | (b), (c) | local-search move cap and rebuild cap | 10–11 at the study, 20 at n + p ≈ 10⁶; not guaranteed enough for growing support (obligation) | keep |
| 13 | L = max(4, ⌈log₂(n + 1)⌉) (M §3) | (b), (c) | burn-in at φ = 1; floor binds for n ≤ 15 | grows with n, not with p; "L logarithmic versus t_mix possibly polynomial" is V10 OPEN | keep |
| 14 | N₀ = max(2,500, n, p) (M §3) | (b), (c) | floor: the 2,500 is a declared budget. "Per-island RB-PIP MC SD ≤ 0.01" is an iid-sampling benchmark only (1/(2√N)); resampling creates dependence, so it is not a guarantee. Grows with dimension | floor binds at the study; N₀ = max(n, p) above 2,500 ⇒ Θ(p·max(n, p)) move steps per stage, Θ(p²) only when n = O(p); score-size costs extra (preflight reports it) | keep; C6 iff a particle-depth claim or any demonstrated fit with p > 2,500 (§3) |
| 15 | H₀ = ⌈512·N₀/2,500⌉ (M §3) | (b), (c) | declared calibration/final ratio 0.2048 | grows linearly; single-tier calibration/final = 0.0512 + 0.2048·I ≤ ≈ 2.1 at I = ℓ = 10 (seat-derived; ≤ ℓ rebuilds per tier) | keep; print the formula (§2 #19) |
| 16 | T₀ = max(1,000, ℓ²) (M §3) | (b), (c) | finite stage ceiling; exceeding it ⇒ `schedule_limit` | the ℓ² term binds only for n + p ≥ 2³¹; ideal-grid T* = O(log log p); as-coded T_n OPEN (Conjecture P) | keep; **w4** (§2 #33) |
| 17 | Tiers e ∈ {0, 1}, factor 4, ≤ 1 escalation (M §3, §6.9) | (c) | bounded escalation, decided before final randomness | ≤ ≈ 16× bridge work; no unbounded rescue; beyond → `schedule_limit` | keep |
| 18 | R = 4 final islands; optional R′ = 4k at N_e, declared before stream 10 (M §3; §2 #7) | (c) | replication and parallel width | fixed 4 gives no growing-dimension accuracy; stacking at N_e lowers the variance of the averaged evidence exactly ∝ 1/R′; for normalised PIPs and general h, 1/R′ is an asymptotic (delta-method) rate under moment conditions, not finite-R monotonicity | keep; **w7** |
| 19 | 4 diagnostic islands per rebuild (M §6.8) | (c) | E2 is an SD over 4 values | regime-free | keep |
| 20 | 4 measured rounds (M §6.11) | (c) | RB averaging after burn-in | constant; correlated rounds are not 4 replications | keep; general-h accumulator (§2 #12) |
| 21 | Exact branch Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p (M §6.2) | (b), (c) | enumerate when it costs about one SMC stage of all populations | fixed p is eventually exact as n grows (N₀ ≥ n); all p at n ≤ 5 [chair-checked]; n = 10: p ≤ 36; n ≥ 22: every p ≤ 17 is exact (a uniform sufficient range; the maximum for n ≤ 2,500, while larger n can admit more, e.g. n = 3,000, p = 18; review check, SOL1 #33); growing p ≪ n need not be exact | keep; **w2** |
| 22 | Clustering: complete linkage on 1 − \|r\|, size-only cut, next-fit packing, lexicographic ties (M §6.3) | (b), (c) | deterministic X-dependent partition under the table budget | no correlation cut; O(p²) memory, O(p²)–O(p³) time; packing can merge separated groups | keep; **w5**; C11 (§3) |
| 23 | Tables (all subsets per block, exponent 1, full y) and start π₀ (M §6.3) | (a), (b) | exactly computable composite step, corrected at φ = 1 | constant B bounds each table; the number of blocks grows with p | keep; item 1 = Outcome 2: no depth or speed claim for the start |
| 24 | Neighbour graph: r_n = √(2 log p / n), strict exceedance, forced best partner, ≤ B outgoing, symmetric union (M §6.4) | (b), (c) | chance-correlation scale of p columns; proposal heuristic | r_n → 0 when log p = o(n); r_n ≥ 1 iff p ≥ e^{n/2} (equality impossible for integer n, p) ⇒ 1-NN graph for p > 1; degrees may exceed B | keep; **w1**, **w3** |
| 25 | `cut_group` diagnostic at ρ = r_n (`v3_core.cpp:760–770`) | (b) | descriptive only | can give large components or none | keep, descriptive |
| 26 | Move round m = p + B + 2, fresh random order; multinomial resampling each stage (M §6.5–6.6) | (b), (c) | reversible, self-adjoint kernel; fixed mutation allocation | Θ(p) sequential steps per particle per round: inherent to the kernel (I1) | keep; changing it is WORKHORSE |
| 27 | ESS threshold 0.90, pilot and grid (M §6.6–6.7; `v3_calib.h:31, 79`) | **(c)**, with B's caveat | one-step dispersion budget (weight CV² ≤ 1/9). Caveat: "defines the law of 𝓒; carried by the theorems as a hypothesis (Theorem G needs the same threshold for pilot and grid)" | dimensionless; does not control accumulated error or omitted mass | keep; S3 R3-4 records (c) over B's (a) |
| 28 | 60 bisection halvings; endpoint snap 10⁻¹² (`v3_calib.h:34–43, 82–94`) | (d) | 2⁻⁶⁰ below double resolution on [0, 1] | at very sharp crossings, progress may not resolve; failure is reported | keep |
| 29 | Pilot floor 1/T_e (M §6.6) | (b), (c) | exploratory progress within the ceiling; forced steps counted and trigger escalation | shrinks as T_e grows | keep |
| 30 | V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}, \|V\| ≤ 40p + 1 (M §6.7) | (b), (c) | O(p) = size of a 1-flip neighbourhood; caps grid cost 60·\|V\|·T_e | the retained fraction of model space vanishes; omitted mass not controlled | keep |
| 31 | Grid convergence = grid equality; ≤ ℓ rebuilds (M §6.7) | stopping rule (b), a deterministic rule (reclassified from the lead's (a), R2_B row 20, by HQ amendment 01; values unchanged); cap (b)/(c) | a flat posterior keeps V changing by MC noise | convergence and P(S₀ ∈ V) OPEN (obligations) | keep; contract (§2 #18) |
| 32 | E1 > 1 nat, E2 SD > 1 nat, E3, forced steps, grid failure/non-convergence, `local_limit` (M §6.9) | (c) diagnostic criteria (S3 R3-4) | odds factor e; triggers define the law of 𝓒 | scale-free; no positive power as dimension grows | keep; labelled heuristics |
| 33 | Low-ESS flag: final stage < 0.5N (M §2) | (c), (b) | report flag | regime-free | keep |
| 34 | Top store 40p + 1; leader stores 20p (M §6.10) | (b), (c) | HPM survives eviction; near-ties, Z_𝒯 and the card read it | linear in p; may truncate many near-equivalent models; restricted summaries labelled restricted | keep |
| 35 | Score cache 500p, clear when full (M §8.6) | (b), (c) | a hit returns identical bits; no effect on the law | key storage up to O(pK) | keep |
| 36 | Near-tie window 10⁻⁹ nat (M §6.10) | (d) | informational; the HPM uses exact equality | can fall below scorer error at large n; η depends on k, Q and conditioning, not on n alone, so a numerical crossing point needs a specified design and model (η ≈ 6·10⁻¹⁰ at n = 200; seat-derived) | keep + **e2** heuristic list (§2 #24) |
| 37 | HPM tie rule: exact equality, then smallest \|S\|, then lexicographic (M §6.10) | (a) | argmax convention | scale-free | keep |
| 38 | MPM threshold ½; α = 0.05 for the Markov bound (M §6.11–6.12) | (a) | Hamming-loss rule; declared confidence | dimension-free; MPM may exceed K | keep |
| 39 | Q recompute below 10⁻⁸·yᵀy; Cholesky → refactor → augmented QR → `numerical_failure` (M §6.13) | (d) | stable evaluation of one score | conditioning worsens with n, K; failure explicit | keep |
| 40 | Scorer error expression η (64ε…), used by `global_certified` (`v3_score.h:240`) | (d) as an indicator; (e) only if read as rigorous | the source calls it heuristic | no uniform validity established | **e5** (§2 #27) |
| 41 | LS0 start-mode tie enumeration cap 10⁶ (`v3_start.h:183`) | (d)/(c) fast path | DP argmax exact; only the tie choice can truncate | ties can proliferate with duplicates or symmetry | **e4** (§2 #26) |
| 42 | Certificate budget (scores, B&B nodes), region rule U, τ (card) | (c) declared certificate-region settings | PC2: Seat C's correction 6 upheld | "unresolved" on exhaustion; L2 needs 2^{\|Ŝ\|} − 1 scores | new in v3.1 (§2.1) |
| 43 | Default 𝓗: size indicators, neighbour-edge pairs ≤ 2pB (§2 #12) | (b) | fixed from (X, y) via the graph | linear in pB | new in v3.1 |
| 44 | Allocation (default 8 GiB, 24 h), preflight, stop-only wall guard (M §2, §8.6) | **(c) declared input** | decides delivery only (Lemma RO) | a fixed allocation cannot support unrestricted growth (V13, by definition); the setup component alone, 8(3np + 3p²) bytes, gives p ≤ [−n + √(n² + 4·8·2³⁰/24)]/2 at 8 GiB (18,818 at n = 200; 11,398 at n = 20,000; review check, SOL1 #39); this excludes all other allocations and workers and is not a feasible-fit threshold (seat-derived) | **e8**, **e6** (§2 #22, #28) |
| 45 | Seed ∈ [1, 2³¹ − 1]; stream map 0–9 (calibration), 10..9+R′ (final); 53-bit uniforms; integer dimensions | (c), (d) | reproducibility conventions; "bitwise" is per binary and BLAS | integer ranges can be exceeded at huge sizes | **e7** (§2 #29); IND-T for 10..9+R′ (§6) |
| 46 | Workers: processes; worker count (§2 #1–#5) | (c) | delivery only; bitwise to serial | regime-free | new in v3.1 |
| 47 | Archive/export limits: V snapshot all if p ≤ 25, else ≤ 10⁴; R Gram copy only for p ≤ 2,000 (`v3_calib.R:15–20`; `v3_setup.R:9`) | (c) | storage choices; full V still builds the grid | truncation grows with p; never reconstruct a "full" V from a snapshot | keep; expose truncation |
| 48 | Other operational constants: exact-branch timing (200 scores, ≥ 64 columns), duplicate-check chunk 512, compiler-lock waits | (c) | profiling and workspace | hardware-dependent; outside the theory | keep |
| 49 | Gram-based scorer; O(p²) correlations and distances (M §8.1) | (c) implementation of the exact target | — | the dominant practical storage limit of v3.1; integer-dimension, stream and allocation ranges and checked-arithmetic rejection are also hard implementation limits (§2 #29, row 45) | v3.2: C7, C11 (§3) |

Sources for rows: R2_A §4 table; R2_B §4 table (rows 1–34); R2_C §4.1 table and §4.2; S2 §0.5, §3; S3 R3-4.

### 5.1 Per regime

- **Tiny n (n ≲ 20).**
  - The method runs. n = 2 is admitted (e3).
  - n ≤ 5 is enumerated exactly for every p; n = 6–21 is exact up to the computed p, with SMC above that (B = 2–4, K ≤ 10). The graph is often 1-NN (w3).
  - Fixed-data guarantees hold: exact-branch exactness, unbiased Ẑ_r given 𝓒, HPM = best scored. No asymptotic theorem applies, and lack of identifiability is not a sampler defect.
  - Sources: R2_A §4; R2_B §4; R2_C §4.5.
- **Fixed p, n → ∞.**
  - Eventually exact, because the exact-branch threshold grows with N₀ ≥ n (R2_C §4.4 calls this PROVED; seat-derived). Output claims then reduce to target-posterior theory (V2–V4) plus numerical and delivery conditions.
  - A fixed-p Gibbs result (V9) is a component result, not a description of the production branch.
- **Growing p ≪ n.** Same rules. K = p eventually, but enumeration can still be infeasible. Polynomial-dimensional target theory applies under its other assumptions. Logarithmic L and ℓ are not automatically enough (obligations).
- **p ≈ n.**
  - The ridge target stays proper and K ≈ n/2.
  - Exact-Gram LH (p ≤ n − 1) is the home of T38(b1-LH)/(b2-LH) under the SIZE hypothesis g_max ≤ B < 2g_min.
  - Proofs that need a positive-definite full Gram cannot extend to p ≥ n. That is a restriction of those proof families, not of the target.
- **p ≫ n, polynomial (p ≤ n^A).**
  - Selection theory T01–T03 applies. T38(b1-LH-iid) has XF GAP. Cost is polynomial (T32(i)).
  - The study generator (g = 5, 2g ≤ B) is the obligation PART-pairing (N8).
  - Costs: in this regime N₀ = p gives Θ(p²) move steps per stage (Θ(p·max(n, p)) in general; score-size costs extra), and setup is about 24p² bytes. Both are declared budgets.
- **p ≤ e^{Cn^α}.**
  - The method is defined for every finite pair. r_n = O(n^{(α−1)/2}) → 0, but N₀ ≥ p and quadratic setup become very large.
  - No current theorem covers this range. Song–Liang's Corollary 1 rests on their own prior, support-size, tail and covariance conditions and cannot be imported.
  - Whether our prior admits this range is **OPEN, not impossible** (R2_C §4.5; S2 §3).
- **Joint growth.**
  - Every budget grows polynomially: N₀ and H₀ linearly, L and ℓ logarithmically, B constant, T₀ eventually ℓ².
  - The by-definition limits are the fixed allocation (row 44), the Θ(p) round (row 26) and finite precision.
  - General consistency or useful precision is OPEN.
  - Sources: R2_B §4; R2_C §4.5.

### 5.2 Theory scope (adopted, S2 §3 / S3 R3-4)

"The p ≤ n^A scope of the selection theorems comes from the target theory (Felipe's prior and the proof technique), not from a sampler choice. Song–Liang's e^{Cn^α} rests on their own prior and conditions and cannot be imported. Whether our prior admits it is OPEN, not impossible."

Method-induced restrictions, stated as such:
- the cap K excludes s₀ > K by definition;
- fixed B limits whole-group recovery to g ≤ B. Here "whole-group" means recovery **as a single block**, not impossibility of posterior support recovery when g > B (R3_C R3-4);
- bounded stores can omit posterior mass;
- logarithmic ℓ and L may be short for some proof routes (theorem obligations);
- N₀ ≥ p and full-coordinate rounds impose real computational growth.

---

## 6. Engineering checks before the paper's claims (not method changes)

None of these can change a method decision taken in MEET-v31 (S3 R3-7; R3_A R3-7). Each one gates only the **claim** named.

| # | Check | Gates which claim | Source |
|---|---|---|---|
| 1 | **W-cal**: bitwise replay of `v3_calibrate` with concurrent diagnostic islands on the 3 replay designs (S1 r001, S4 r001, S5 r002). About 1 h on Owls with the METH-AUDIT harness. | "bitwise" for (b); any wall-clock claim (calibration is on the critical path) | DOSSIER §4.5; MA §4 C2; S1 item 3; S3 R3-7 |
| 2 | **Merged-LS0 replay**: integrated core versus the O-LS0 export on the 3 designs. Covers HPM, stores, flags, E3 unchanged, `ls0_improved`, stream endpoints, and a deterministic eviction/tie example. | "LS0 is in the shipped core"; T38(b1-LH) as a theorem about the shipped method | S2 D3c; R2_B §5 item 5; R2_C D3c |
| 3 | **GUARD-W audit**: code audit that the v3.1 worker, merge and LS0 paths satisfy "any worker stop, LS0 stop or guard stop ⇒ no output" (OP-LS0 included). Plus API-AUDIT's forced-stop table (10 fits) after the `log_Z` NA fix. | premise (i) of G2 and of every P{𝒪, ·} statement | S3 R3-1 (B), R3-5(ii); R1_B §2.8.1 |
| 4 | **IND-T for streams 10..9+R′**: independence of the final streams from calibration streams for every declared R′ | stacking (#7) theorems; the frozen-𝓒 contract | S3 R3-7; THEOREM_REVISION_INPUTS M12 |
| 5 | **VAL-FP at production size**: long-double replay on 2 study designs at p = 500 (measured so far only at p ≤ 40; ε scales with R′/4) | the floating-point card statement (with validated SC). Removing the numerical label needs validated arithmetic (SC) **and** VAL-FP; a long-double replay alone is not enough | R1_A §2 item 2, Q10; PC2 C6 item 5 |
| 6 | **Preflight fixes** (e6) and an allocation audit of concurrent peak memory and stop behaviour | `resource_limit` estimates labelled "estimate" | S2 P-9 e6; R2_C §4.2 E4 |
| 7 | **Checked arithmetic** (e7): boundary tests for integer, stream-id and allocation overflow | support at huge (n, p) | S2 P-9 e7 |
| 8 | **Full POST HOC PIP rescoring** on the NOTS/laptop bundles (`pip_rescore.R`), with R_eff per fit; A's D5 reversal criterion is read against it by HQ | Ẑ-weighted primary PIP and MPM_Ẑ for the 2,400 fits | S2 §0.2; S3 R3-7; R3_A R3-7 |
| 9 | **Calibration timing tabulation**: `timings$calibration` and `timings$final` (`v3_fit.R:124, 136`) plus rebuilds, tier, T and convergence from the saved fits | the cost wording (§2 #19); calibration contract tabulation | R2_B D4, §5 item 3; S1 item 4 |
| 10 | Also listed by seats: the e4 tie-DP invariant (N3, a proof obligation) and the n = 2 boundary tests (e3) | LS0 under truncation; n = 2 support | S3 R3-4 |

---

## Points settled by the chair after drafting

1. **Item 1:** Outcome 2 under the pre-registered rule (`ITEM1_ABL_START.md`).
2. **ESS 0.90:** class (c) with Seat B's caveat; B's preference for (a) is a recorded label difference (MINUTES §4), not an open method question.
3. **Names:** e7 status `unsupported_size`; `global_certified` keeps its field name and is documented as heuristic (e5).
4. **HPM terminal frequency:** not in 𝓗; descriptive only (SYNTH_R3 R3-3).
5. **Calibration-cost ratio 0.0512 + 0.2048·I (single tier; rounded 0.05 + 0.2·I):** seat-derived, unchecked; quoted as such; matches the three logged designs.
6. **Certificate card on the study fits:** computable wherever the saved top store exists (NOTS bundles; HQ action), otherwise not claimed.
7. **A2 wording:** a THEOREM_LIST edit (PC1 claim 4); no METHODOLOGY_v3 sentence needs deleting.
