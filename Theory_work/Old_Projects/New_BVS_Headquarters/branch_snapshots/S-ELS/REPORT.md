# S-ELS: E_LS ledger extraction (PROD-H, 2,400 fits)

Data clerk report for HQ. Branch `theory/S-ELS`. All numbers come from the per-fit records, not from summaries.

## 1. Plain answer to the open question

**On the PROD-H ledgers there is no fit with F(S₀) > F(S_c), and no fit in which the local search did anything.**

- In **all 2,394 completed fits the final local search made 0 moves**: E3 never fired, the HPM never changed, and every search ended `no_improvement`, `local_certified = TRUE`, `local_limit = FALSE`. So Ŝ = S_c = returned model in every completed fit.
- **S₀ was scored by the fit in all 2,394 completed fits**: it is in the 20,001-model top store, and the store's F(S₀) equals the offline F(S₀) to 1e-12. The event E_LS (S₀ not scored before the search and better than the best scored model) is **empty in the data (0 of 2,394)**.
- For **all 565 posterior misses, F(S₀) < F(Ŝ) strictly**. The smallest margin is 0.0049 (23 fits are within 0.1). There are **0 search misses**, **0 ties** and **0 cases of F(S₀) > F(S_c)**.
- The **541** fits with S_c ∈ 𝓡₂∖{S₀} all fall in one class: **F(S₀) < F(S_c), median gap −1.33, range −9.05 to −0.0049**. So the "0/541 repaired" count **is forced by monotonicity (Lemma 0), in every one of the 541 cases**. W3-VT37R's repair R2 (CEX-2) is a valid logical correction, but its counterexample pattern does not occur in these data: it needs the search to move, and it never moved.
- **The referee's sampled F(S₀) > F(S_c) cannot be reproduced from these ledgers.** I checked the same quantity (F of the final local-search centre, which equals `hpm_before_local`) against F(S₀) from two independent sources (see §6). I do not know what the referee compared. Candidates I cannot confirm: a different centre or a different F convention (for example F relative to m(∅), or log Ẑ), or a different set of fits. HQ should ask for the case IDs.

Consequence for the theory: PROD-H says nothing about whether a greedy repair *works*, because the repair never operated. The production search is, empirically, a **pure certificate** that Ŝ is a 1-flip/swap local maximum (2,394/2,394).

## 2. Definitions used

- Ŝ, F(Ŝ): `fit$hpm`, `fit$hpm_F` (the final HPM, after the final local search).
- **S_c, F(S_c)**: `fit$local_search$centre`, `centre_F`. This is the start of the final search, the global best scored model `led.hpmS` (engine: `v3_engine.h`, `local_search(led.hpmS, ell, …)`). It equals `hpm_before_local` in all 2,394 completed fits. In the engine the final centre is the start of the path; with 0 moves it is also the returned model.
- Returned model: `local_search$returned`, `returned_F`. Move cap ℓ = 10 (`budgets$ell`, ⌈log₂(n+p+1)⌉ at both p).
- 𝓡_d = {U ∪ P : U ⊆ S₀, |P| ≤ d} (`00_COMMON.md`), so S ∈ 𝓡₂ ⇔ |S∖S₀| ≤ 2. This reproduces the 541 (cells 218 / 40 / 246 / 37).
- S₀ and **F(S₀)**: S₀ from the scoring truth copy. F(S₀) = `F_truth` from the H2 analysis (`case_theory_H.csv`), scored with the fit's frozen scorer. Cross-checks are in §6.
- Move distance from S_c to S₀: with m missing truths and e extras, the fewest flip/swap moves is max(m, e). S₀ ∈ N(S_c) iff that is 1.
- Classes (task 2): *exact recovery* (Ŝ = S₀); *posterior miss* (F(S₀) ≤ F(Ŝ)); *search miss* (F(S₀) > F(Ŝ)); tie tolerance 1e-6 (never needed). The task's "S₀ unscored" never occurs: S₀ is scored in every completed fit. What does occur is 6 fits with **no final ledger** (below).
- Data: PROD-H run `20261030T0934Z_prodH` (records pulled and manifest-verified). H2 showed that these 2,400 records reproduce the 2026-10-23 fits exactly (max |diff| = 0 on 11 fields), so the old fits give the same ledger.

## 3. Task 2: classification of the 2,400 fits

| p | c | exact recovery | posterior miss | search miss | no final ledger (stopped) |
|---|---|---|---|---|---|
| 500 | 0.5 | 370 | 230 | 0 | 0 |
| 500 | 1 | 559 | 40 | 0 | 1 |
| 1000 | 0.5 | 340 | 258 | 0 | 2 |
| 1000 | 1 | 560 | 37 | 0 | 3 |
| **all** | | **1,829** | **565** | **0** | **6** |

The 6 stopped fits (`resource_limit`, all S5) have no final local search and no `hpm_before_local`, so S_c is undefined. Their partial HPM-so-far has F(Ŝ) ≥ F(S₀) in every case: 3 equal S₀, and 3 have F(S₀) below F(Ŝ) by 0.21, 3.39 and 1.15. They are not counted as recoveries (headline convention). Per-scenario counts at c = 0.5 are in `tables/class_counts_c050_by_scenario.csv`.

Other ledger facts for the 2,394 completed fits: E1 fires 0 times, E2 83 times (10 of them among the posterior misses), E3 0 times, `local_limit` 0 times, one scan per fit (`ls_n_scans` = 1).

## 4. Task 3: the 541 fits with S_c ∈ 𝓡₂∖{S₀}

All 541 are posterior misses with Ŝ = S_c ≠ S₀, 0 moves, certified, and 0 returned S₀.

| p | c | n | F(S₀)−F(S_c) min | median | max | F(S₀) > F(S_c) | S₀ ∈ N(S_c) | max moves to S₀ | within cap ℓ = 10 | certified | hit cap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 0.5 | 218 | −9.05 | −1.29 | −0.0049 | 0 | 180 | ≤ 4 | 218 | 218 | 0 |
| 500 | 1 | 40 | −6.21 | −0.66 | −0.086 | 0 | 37 | ≤ 2 | 40 | 40 | 0 |
| 1000 | 0.5 | 246 | −8.39 | −1.49 | −0.027 | 0 | 182 | ≤ 4 | 246 | 246 | 0 |
| 1000 | 1 | 37 | −3.67 | −0.85 | −0.0085 | 0 | 35 | ≤ 2 | 37 | 37 | 0 |
| **all** | | **541** | **−9.05** | **−1.33** | **−0.0049** | **0** | **434** | **4** | **541** | **541** | **0** |

(Source: `tables/c541_summary.csv`. The "max moves" column is max(m, e) at the worst case in the cell; `c541_cases.csv` has it per fit.)

**By distance |S_c Δ S₀|** (`tables/c541_by_distance.csv`):

| \|S_c Δ S₀\| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| fits | 267 | 197 | 39 | 32 | 4 | 2 |
| median F(S₀)−F(S_c) | −0.94 | −1.45 | −2.55 | −2.16 | −4.48 | −4.13 |
| of which F(S₀) > F(S_c) | 0 | 0 | 0 | 0 | 0 | 0 |

**By region.** Of the 541, 133 have S_c ∈ 𝓡₀∖{S₀} (no extras, so S_c ⊊ S₀; all at c = 0.5), 346 are in 𝓡₁∖𝓡₀ and 62 in 𝓡₂∖𝓡₁. The other 24 posterior misses (all c = 0.5, 12 at each p) have S_c outside 𝓡₂ (3 or 4 extras), and F(S₀) < F(S_c) there too.

**Why the search did not reach S₀** (`tables/c541_reason.csv`):

| reason | n |
|---|---|
| A. F(S₀) < F(S_c): Lemma 0 forbids S₀ on any path; S₀ was scored by the fit and lost | **541** |
| B. F(S_c) < F(S₀) ≤ F(Ŝ) (CEX-2 pattern: the search climbed past S₀) | 0 |
| C. F(S₀) > F(Ŝ) (a true search miss): C1 cap ℓ hit / C2 local max with 0 moves / C3 moved, then local max | 0 / 0 / 0 |

In 434 of the 541 (267 single add/delete plus 167 swaps) S₀ was a one-move neighbour: the single scan scored it, and it was worse than S_c. The other 107 were 2–4 moves away. The cap ℓ = 10 was never close to binding.

**Verdict on Lemma 0 and R2.** Lemma 0(a)–(b) holds in the data with room to spare, and the weakness R2 identified (a posterior miss can coexist with E_LS) has zero instances. The data fact W3-VT37R asked for, "F(S₀) − F(S_c) per fit", is now extracted. It is negative in 541 of 541.

## 5. Task 4: strict same-size posterior misses at c = 0.5 (input for Prop 1's swap certificate)

Definition: Ŝ ≠ S₀, |Ŝ| = |S₀| = 14, and F(S₀) < F(Ŝ) strictly (all posterior misses are strict, so no ties are dropped). `swaps_k` counts misses with |Ŝ∖S₀| = k, so k = 1 is a single-swap miss.

| scenario | p = 500: all post. misses | same-size strict | of which 1 swap | p = 1000: all | same-size strict | 1 swap | **pooled same-size strict** |
|---|---|---|---|---|---|---|---|
| S1 | 21 | 2 | 2 | 29 | 2 | 2 | **4** |
| S2 | 16 | 0 | 0 | 25 | 2 | 2 | **2** |
| S3 | 36 | 17 | 17 | 33 | 8 | 7 | **25** |
| S4 | 75 | 55 | 39 | 65 | 46 | 30 | **101** |
| S5 | 41 | 10 | 10 | 67 | 13 | 11 | **23** |
| S6 | 41 | 22 | 19 | 39 | 24 | 22 | **46** |
| **all** | 230 | **106** | 87 | 258 | **95** | 74 | **201** |

So 201 of the 488 posterior misses at c = 0.5 are strict same-size misses, 161 of them single swaps, 30 two-swap, 6 three-swap and 4 four-swap. S4 supplies half of them. The remaining 287 misses are not same-size: by |Ŝ| − s₀ (−3, −2, −1, 0, +1, +2) the c = 0.5 counts are 5, 21, 142, 201, 106, 13 (`tables/post_miss_size_offset.csv`). At c = 1 there are only 6 (3 each at p = 500 and p = 1000, all S4). Full table: `tables/strict_same_size_misses.csv`.

## 6. Checks (`tables/checks.txt`, all PASS)

1. S₀ in the ledger equals H2's S₀ in all 2,400 fits; H2's `F_smc_hpm` equals the ledger's F(Ŝ) (max diff 2e-12).
2. S_c = `hpm_before_local` model and F(S_c) = its F, in all 2,394.
3. F(Ŝ) ≥ F(S_c) everywhere; S_hat = returned model everywhere; E3 ⇔ F(Ŝ) > F(before local) (both never); moves > 0 ⇔ E3 (both never).
4. **F(S₀) cross-check:** the offline `F_truth` equals the fit's own top-store F(S₀) in 2,394/2,394 (max diff 1e-12), and equals F(Ŝ) on the 1,829 exact recoveries (max diff 1e-12). So F(S₀) is the same score the fit used, and S₀ was in the fit's top-20,001 store every time.

## 7. What I did not do, and limits

- I did not recompute F(S₀) from the data matrix. I took the H2 scoring output and validated it against the fit's own store (check 4). The store holds the top 20,001 scored models, so that check covers S₀ only because S₀ scored high enough to be kept, which it always was.
- The ledger is for the final local search only. The pilot and calibration searches (iteration ≥ 0) are not in the per-fit record fields I read; they only matter for how S_c was reached, not for E_LS at the end.
- I could not see the referee's sample, so I cannot say why they saw F(S₀) > F(S_c). §1 lists what I ruled out.
- The 6 stopped fits have no final search; they are described, not classified.
- The whole result is for the PROD-H design (n = 200, p ∈ {500, 1000}, S1–S6, c ∈ {1, 0.5}) at ℓ = 10 with the v2.2.1 engine. It says nothing about weaker regimes where the HPM is not already a local maximum.

## 8. Files

- `scripts/extract_ledger.R`: per-fit extraction from `SMCBVS.rds` (3 workers, ~28 min on the laptop, ≤ 4 cores). Run: `Rscript extract_ledger.R <H2>/theory/cases_new.tsv <out>/ledger_raw.csv K 3` for K = 1..3.
- `scripts/analyse_ledger.py`: classification and tables. Run: `python -I analyse_ledger.py <out>/ledger_raw.csv <H2>/case_theory_H.csv tables`.
- `tables/ledger_per_fit.csv` (2,400 rows: Ŝ, F(Ŝ), S_c, F(S_c), returned, F(S₀), flags, class), `tables/c541_cases.csv`, `tables/c541_summary.csv`, `tables/c541_reason.csv`, `tables/c541_by_distance.csv`, `tables/class_counts*.csv`, `tables/referee_check*.csv`, `tables/strict_same_size_misses.csv`, `tables/post_miss_size_offset.csv`, `tables/numbers.json`, `tables/checks.txt`.
- `<H2>` = `C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102`. Fit records: `C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261030T0934Z_prodH/p{0500,1000}/<case>/SMCBVS.rds`. No raw fit data is in git; the tables carry model supports as strings only.
