# W2-SIM family PK — DESIGN (v2, 2026-11-09; v1 + fixes of design review R01, reviews/PK_R01_design.md / PK_R01_disposition.md)

Informs ticket W2-FAC-PK (compound symmetry with p > K = ⌊n/2⌋). Request: `Theory_work/Wave2/W2-FAC-PK/numerics/SIM_REQUEST.md`
(R1, R3; R2 is run by the W2-SIM lead) + task item 1 remainder (S5 with p > K). Brief: `W2-SIM/briefs/PK.md`.
Theory statuses copied from W2-FAC-PK/STATEMENT.md v3 (LOCKED): Theorem NEG (P2) and Theorem PATH (P3) are
"proved, under review" in SIM_REQUEST.md; nothing here upgrades them.

## Common objects (all experiments)
* Score / prior / start / LS0 = the ticket's exact objects (imported **unchanged** from the ticket snapshot
  `code/tickets_20261109T0943/.../W2-FAC-PK/numerics/`, sha256 identical to the repo copies; each output line records the
  sha256 of pk_core, cs_core, bvs_core, fac_core):
  score D0 log m(U) = −½[logdet((n+1)G_U+I) − logdet(G_U+I)] − ν log(0.02 + Q_U), ν = 0.01 + n/2; prior
  log w(k) = −log(2·C(2p−1,k)), k ≤ K = min(p, ⌊n/2⌋); start mode = exact block DP (argmax γ₀ on Ω); LS0 = production
  local search (flip + swap neighbourhood, best strict improvement, exact float ties → lexicographically smallest set),
  **uncapped**, from the start-mode centre; every move recorded.
* Truths: S₀ = {2, 26, 53, 75} (0-based, as pk_core/n1_scale and fac_core.study_layout), ϑ aligned (1.4, 1, 1.8, 1.2)
  or mixed (1.4, −1, 1.8, −1.2) (both have θ̄ ≠ 0), σ = 1.
* ℓ_n = ⌈log₂(n + p + 1)⌉; MR1 cap a_n = ℓ_n + |S̃₀|; cap₂ = ℓ_n + 2|S̃₀|.
* **k_hit** = smallest scan index k (centre C_0 = start, C_k after k moves) with S₀ ∈ N(C_k) ∪ {C_k}. By the single-search
  prefix property LS0 with cap a scans centres C_0..C_min(a, m*), hence **LS0(a) scores S₀ ⇔ k_hit ≤ a** (k_hit = None ⇒
  never). Reported: MR1_scores (k_hit ≤ a_n), cap2_scores, excess = k_hit − a_n.
* **Censoring and numerics (R01-3, R01-4):** fac_core.ls0_path records the proposed move of the last scan before its
  move-limit test; the drivers (pk_common.trace_general) keep executed moves only, flag `limited` (censored: the last
  scan still had a strictly better neighbour), and censored units are excluded from endpoint/m*/k_hit statistics and
  listed (max_moves 10⁶ general, 10⁷ R1). Every scan is checked for NaN/+inf (run aborts with an error, rc ≠ 0, so the
  unit is visible as failed in ends.jsonl/sacct). Direct (Cholesky) re-scoring of the centre and the 5 best neighbours at
  scans 0, 1, every 250th, the last scan and the first 50 near-tie scans (winner margin < 10⁻⁶); recorded
  max |F_scan − F_direct|, whether the direct order keeps the scan winner first, and the minimum winner margin. R1: NaN
  guards, exact-tie counts, minimum margin among the candidates pk_core evaluates, arrival, limit flag. Endpoints ≠ S₀
  get direct F(final) and F(S₀). Genuine near-ties exist (e.g. R1 pilot ρ = .5 n = 6000: two swap-out nulls with almost
  equal centred z, margin 7·10⁻¹²); they change which null leaves, not the counts.
* Path statistics: m* (moves of the uncapped path), m*/K, W = leading swaps (moves before the first non-swap), number of
  swaps / deletions / additions, swaps and additions after the first deletion, final == S₀, arrival (scan index at which
  the centre equals S₀), the run-length-encoded move sequence (tags sN>N, -N, +T, … from the ticket code), F-gains of the
  best add / null-delete / truth-delete / swap at the first scans and at the first deletion (general-scorer runs).
* Seeds: `pk_common.cell_seed(EXP, cell…, layout, rep)` = SeedSequence([0x504B, EXP-hash, cell params, layout-hash, rep]) —
  deterministic, recorded per run, distinct across experiments, cells and replicates; reps 0..9. Pilot runs use EXP = PILOT
  (different seeds; not pooled with production).
* One data set per Slurm array task (`sim/submit_table.sh`, frozen scripts + manifest with sha256), raw JSONL per task in
  `/scratch/fb31/theory_w2/<RUN_ID>/raw/`; compact copies + summaries in `W2-SIM/results/FAC-PK/{R1,R3,S5PK}/`.

## R3 — iid-row CS, including p ≫ n (priority 1)
* **Informs:** frontier (F1) of W2-FAC-PK (NEG/PATH proved only for exact Gram, K < p ≤ n − 1). Question: with random
  rows, does the NEG mechanism (saturated start |S̃₀| = K and a leading swap phase long enough that k_hit > ℓ_n + |S̃₀|)
  persist, in particular for p ≫ n; does the uncapped path still end at S₀ (PATH analogue), and does ℓ_n + 2|S̃₀| score S₀?
* **Reading rules (fixed, R01-1):** cap conclusions are drawn **only** from the observed k_hit compared with the cap
  (MR1 scores ⇔ k_hit ≤ ℓ_n + |S̃₀|; cap₂ scores ⇔ k_hit ≤ ℓ_n + 2|S̃₀|); scoring (k_hit), arrival (centre = S₀) and
  certified endpoint (final == S₀, path not censored) are reported separately. Saturation and W are mechanism
  descriptors, not substitutes for k_hit. Possible outcomes: (i) MR1 misses in saturated runs at p ≫ n — evidence that the
  NEG mechanism is not an exact-Gram artefact at these n; (ii) MR1 scoring in most runs — evidence that MR1's slack suffices
  empirically there; (iii) cap₂ misses or uncensored paths not ending at S₀ — evidence against the sufficiency of
  ℓ_n + 2|S̃₀| beyond exact Gram (an endpoint ≠ S₀ by itself does not show that larger caps cannot score S₀: the path may
  have scored S₀ earlier; k_hit decides); (iv) n-trend of W at fixed p/n (descriptive). All finite-n outcomes are
  evidence; none is a proof or disproof of an asymptotic statement.
* **Design:** rows iid N(0, Σ), Σ = 0.5·I + 0.5·11ᵀ (X = √ρ η1ᵀ + √(1−ρ) Z), X standardised (bvs_core.standardize_X),
  y = Xθ + ε then standardised (bvs_core.make_y_std); scorer bvs_core.Problem; partition bvs_core.partition(X) (complete
  linkage on the sample correlations, B = min(⌊√n⌋, ⌊√p⌋, 16)); start bvs_core.start_mode; path fac_core.ls0_path (closed-form
  Schur scans of every flip/swap neighbour).
  (n, p) ∈ {(200, 500), (500, 1000), (1000, 2000), (2000, 1500)} (request) ∪ {n ∈ {200, 400, 800} × p/n ∈ {2.5, 5, 10}}
  (task item 1, n = 800 added since the pilot is fast; (200, 500) shared) ∪ {(2000, 4000), (4000, 3000)} (n-trend at p/n = 2
  with (500, 1000), (1000, 2000), and at p/n = 0.75 with (2000, 1500)) = 14 cells × {aligned, mixed} × 10 reps = 280 data sets
  (configs/pk_r3_tasks.tsv, generated by scripts/make_tasks.py).
* **Validation (rule 3):** fac_core.ls0_path is not the brief's bvs_core.local_search (whose explicit Cholesky scoring of
  K·(p−K) swap neighbours per scan is infeasible at K = 1000). Agreement check `validate_general.py`: 28 small iid-row cases
  (CS ρ = 0.5 and S5; n ∈ {60, 80, 100}; p/n ∈ {0.8 … 3}; aligned/mixed), same start, uncapped: identical path of sets,
  identical final, max |F_scan − F_direct| along the path. Local run 28/28 identical (`results/FAC-PK/validation/`); repeated
  on NOTS (pilot task 1).

## R1 — exact-Gram CS, large n, closed form (priority 2)
* **Informs:** Theorem NEG (W ≥ n^β, β < ½, ⇒ MR1 never scores S₀) and Theorem PATH (path ends at S₀, m* ≤ (1+δ)K).
* **Outcomes flagged by the request as theory-relevant** (R01-1: a finite-n occurrence is diagnostic evidence requiring
  investigation — e.g. a check of the run's hypotheses and of numerics — not a contradiction of an asymptotic probability
  statement): final ≠ S₀ at n ≥ 6·10⁴ with |S̃₀| = K (against PATH's prediction); m*/K not approaching 1 across n; W not
  growing with n (against NEG's mechanism); a saturated run where MR1 scores S₀ at n ≥ 6·10⁴.
* **Design:** pk_core unchanged (make_cs exact-Gram sufficient statistics; cs_partition — equal to the method's partition,
  W2-FAC-PK pk_selftest; start_mode_cs; path_from), driver r1_cs.py = n1_scale.run pattern. ρ ∈ {0.2, 0.5, 0.8};
  p/n ∈ {0.6, 0.8, 0.99} (p = min(round(frac·n), n − 2)); n ∈ {2·10⁴, 6·10⁴, 2·10⁵}; aligned + mixed; 10 reps = 540 runs.
  Larger n only if a validated faster path is written (not planned unless time allows).

## S5PK — S5 (ρ_b = 0.3 global, ρ_w = 0.7 within groups of 5) with p > K (priority 3)
* **Informs:** task item 1 of W2-FAC-PK / W2-FAC-B §5(b): is NEG's mechanism (saturated start + long swap phase) a CS
  feature or does it appear for S5 too; does the uncapped path end at S₀; MR1 vs cap₂.
* **Reading (rules as R3):** MR1 misses (k_hit > ℓ_n + |S̃₀|) in S5 runs ⇒ evidence that the MR1 cap problem extends to S5
  (study scenario); MR1 scoring in most runs ⇒ evidence that it does not at these n; cap₂ misses ⇒ evidence that
  ℓ_n + 2|S̃₀| is not enough for S5; uncensored endpoints ≠ S₀ are listed with direct scores F(final), F(S₀).
* **Exact Gram** (s5_exact.py): fac_core.ExactGram (X'X = (n − 1)Σ_S5 exactly; factor pieces drawn), p/n ∈ {0.6, 0.8, 0.99},
  n ∈ {600, 2000, 4000}; aligned + mixed; 10 reps = 180 runs. Partition = closed form (consecutive groups of 5 packed
  next-fit into blocks of size ≤ B) — equal to bvs_core.partition_from_corr(Σ_S5, B) (validate_s5_partition.py; asserted
  in-run for p ≤ 1200). NB (corrected, R01-2): the pilot's first closed form (⌊B/5⌋ whole groups per block)
  disagreed in **5/27** cases (pilot validate_s5_partition.jsonl: (333,14), (1001,14), (2003,14), (3001,14), (3001,16) —
  whenever a final partial group fits into the previous block). Fixed to next-fit packing of group sizes; the complete
  validation of the revised frozen scripts is run as a separate prerequisite run (pk_val01) and production arrays are
  released only if both validators exit 0 (they now exit 1 on any disagreement). Production S5-exact p: 360, 480, 594 (n = 600), 1200,
  1600, 1980 (n = 2000), 2400, 3200, 3960 (n = 4000); only p = 594 has a partial group (asserted in-run, p ≤ 1200).
* **iid rows** (r3_iid.py design s5: X = √.3 η1ᵀ + √.4 ζ_group + √.3 Z): p/n ∈ {1, 2.5, 5, 10} × n ∈ {200, 400, 800}
  plus (1600, 1600), (1600, 4000); aligned + mixed; 10 reps = 280 runs.

## Analysis plan (fixed before the batch; summarize.py v2 after R01-5/6)
Units are reconciled against the frozen task tables (expected unit = output file named in the task command): identical
duplicate records collapse, conflicting ones are excluded and listed, missing units listed, module sha256 must match the
reference set. Event counts and run counts are reported separately; the excess k_hit − a_n is summarised over the units
with finite k_hit (count shown).
Per cell: #saturated/10; |S̃₀| (median, range); #start ⊇ S₀; W (median, range); m*/K (median, range); #swaps after first
deletion; #additions; #final == S₀; #MR1 scores; #cap₂ scores; k_hit − a_n (median, range); #scan ties. Trends across n
(R1: n = 2·10⁴ → 2·10⁵; R3/S5-iid: n = 200 → 2000) reported descriptively (least-squares slope of log median W on log n
per (ρ, p/n, layout) as a descriptive number only — evidence, not a limit). Every run with final ≠ S₀, cap₂ miss, MR1 score
in a saturated run at n ≥ 6·10⁴, or any tie is listed individually with its seed.

## Pilot (pk_pilot01, job 2633080; results/FAC-PK/pilot/pk_pilot01/, EXP = PILOT seeds, not pooled)
validate_general on NOTS 28/28 identical paths; R3 (2000, 1500) 131 s wall, (1000, 2000) 78 s, (400, 4000) 233 s (partition
214 s ~ p³); R1 ρ = .8 n = 6·10⁴ 59 s; S5 exact n = 2000 p = 1980 132 s; n = 2·10⁵ R1, S5 exact n = 4000, S5 iid (800, 8000)
still running at review time (timings added to LOG when done).

## Throttle / resources
Allotment 25 concurrent 1-CPU tasks. Pilot `pk_pilot01` (14 tasks: both validations, largest cells of each experiment)
fixes --time / --mem per batch. commons partition unless all tasks surely < 1 h (then scavenge, rerun preempted).
