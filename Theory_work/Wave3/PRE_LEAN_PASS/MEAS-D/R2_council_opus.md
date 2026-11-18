Manifest verify printed `verify: OK MANIFEST 00426ac2fe589ac2d6de074c068942d86e0864d49a0f28631e476bf51dad6800` (exit 0). The converter ran on a scratch copy in `.rc_tmp/measd_r2_opus/`. I edited no tracked file, committed nothing and started no subagents.

# R2 council review (Opus seat): W3-SAMP:MEAS-D

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 | ACCEPT | Every R1 finding is closed by the diff (sub-lines below). Two R1 pins are wrong, and the author copied them. `v3_core.cpp:475` should be `:474` (E9, below). |
| 1·F1 | ACCEPT | The fix narrows the statement instead of reading H-U/SI jointly, at `STATEMENT.md:190` and `MEAS_D.md:24`. Step 5 is now stated per island (`MEAS_D.md:42-46`) and has a "Several islands" paragraph (`:48`). The narrowed sentence is true. Step 5's list of routes for (C-v) and (TR-d) is missing inputs (F4). |
| 1·F2 | ACCEPT | Checked at `v3_blocks.h:149-173`. The candidates are stable-sorted by fabs(r_jl), descending, with ties going to the smaller index. The code keeps those with fabs(r_jl) > (2 log p/n)^{1/2}, at least 1 and at most B, symmetrises them, and gives no edges when p = 1. r comes from `correlation_matrix` (`:10-17`), Gram entries over √(G_jj G_ll), which is continuous on a cell. The graph is used at `v3_core.cpp:410` and `v3_engine.h:169, 173`. The Step 2 sentence (`MEAS_D.md:32`) and the Step 4 input list (`:37`) are correct. |
| 1·F3 | ACCEPT | `depends_on` cites `W1-N1:F@stmt`, which is in claims.tsv. Step 5 cites `L3_freezing.md:21-23`, which is the Statement of Lemma F (checked). |
| 1·E1 | ACCEPT | `T1_GW/STATEMENT.md:99-102` is the "probability model for clock readings" bullet (checked). |
| 1·E2 | ACCEPT | `W3-READER/STATEMENT.md:22-23` is the claim, and `:28-33` is the linearity and joint-law step (checked). |
| 1·E3 | ACCEPT | "every statistical field of P°'s output" appears in `STATEMENT.md:190`, `MEAS_D.md:24` and REGISTRY "P0's output". |
| 1·E4 | ACCEPT | The {completed} sentence is at `MEAS_D.md:83`. It goes only through 𝒪 ∩ A ⊆ 𝒪° ∩ A°, which is GW-iv at `T1_GW/STATEMENT.md:87-88` (checked). |
| 1·E5 | ACCEPT, with E9 | `v3_score.h:237` is the `throw NumericalFailure` (checked). `:175-183` defines H = (n+1)G_S + I and A = G_S + I, which are positive definite, so the first `try_chol` returns under EX-A. The LS0 `stop` is at **`v3_core.cpp:474`**; `:475` is `int ls0_cap = (int)cap_ll;`. That `stop` sits at the call site, not inside the search. The `|S| > K` throw at `v3_score.h:230` is not named (E9). |
| 1·E6 | ACCEPT | The enumeration-cell line is at `MEAS_D.md:40`. |
| 1·E7 | ACCEPT | There are three `stop` rows in `v3_list_fields` (`v3_run.R:251` count mismatch, `:253` duplicate model, `:263` column outside the retained set). Each branches on a Borel predicate. `MEAS_D.md:91` is correct. |
| 1·E8 | ACCEPT | "(H-U/SI, :35-36)" is now in `STATEMENT.md:190`. |
| 2 | ACCEPT | (a) is not an added premise. Reason in §2. Suggested wording in E10. |
| 3 | REJECT | (C-v) and (TR-d) are both NOT COVERED by the route Step 5 names (`MEAS_D.md:48`). Both hold once the missing single-island inputs are cited (F4). |
| 4 | ACCEPT | The potential-only scope holds (`STATEMENT.md:190`, `MEAS_D.md:10-13`, REGISTRY "nothing is claimed about the actual A, O or the guard"). The narrowed "Consequently" sentence claims only what Step 5 and its sums, monotone comparisons and unions give. No clause gains an independence premise, given (a). E3 cannot be read as the actual output. E4 goes only through GW-iv. |
| 5 | ACCEPT | `ingest.py convert` on the scratch copy exits 0 and returns one record: W3-SAMP:MEAS-D, lines [190, 192], status_source `lemmas/MEAS_D.md:3`, and 8 `depends_on` items with no spaces. `STATEMENT.md:188-192` contains no `|` or `‖`. The REGISTRY block (`REPORT.md:199-206`) uses `|` only as a field separator. `W1-N1:F`, `W1-N1:B`, `W3-AUDIT-A:{GW, CAL-C, OPC, TDP, BLK}` and `W3-SAMP:CC` are all present in claims.tsv. §§0-3 still differ from HEAD only at `:36`. |
| 6 | REJECT | New: F4 (Step 5's route list) and E9-E12 (one pin, wording, and the gates pointer). |

## 2. Verdicts on (a) and (b)

`(a) IND-T "with the data adjoined": NOT AN ADDED PREMISE`

- **Why.** IND-T (`STATEMENT.md:64-66`) is a premise of the fixed-data clause (D-ii). Fixed-data claims are "conditional on the data" (`:29`), and integrating them under the joint law treats them as such (`:34-35`). So IND-T says that, given the data, U^{(10)}, …, U^{(13)} are mutually independent and jointly independent of U^{(0:9)}.
- **What follows.** Per-island SI under the joint law (`:35-36`) adds that each U^{(9+r)} is independent of the data, so its conditional marginal is the fixed law μ. Then the conditional law of U^{(10:13)} given (data, U^{(0:9)}) is the constant μ^{⊗4}. So U^{(10:13)} is independent of (data, U^{(0:9)}), and hence of (data, 𝓒°).
- **Consequence.** The joint reading is derived from premises already stated, not added. Only the 4D_r variant of (D-iii) (`:102-103`) uses it. If the clause were dropped, nothing else would break.

`(b) (C-v): NOT COVERED`

- **Covered.** The PIP and MPM clauses are covered by (C-iv)'s first clause (`STATEMENT.md:156`): E[‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g + β/2.
  - This is an expectation bound, and its right side depends on the data only (g, β; `:131`, `:153-154`), so it is the same for every r.
  - So ¼Σ_r gives g + β/2. Then {MPM ≠ S₀} ⊆ {‖pip_primary − 1_{S₀}‖_∞ ≥ ½}.
  - The sum needs no per-island probability bound, no event on which the p̂_r are controlled, and no independence across islands.
- **Not covered by (C-iv).** (C-iv) says nothing about Ẑ.
  - (C-v)'s Ẑ/Z, log Ẑ and NC_r clauses (`:159-160`), and their O_P(r_n) forms (`:160-161`), need (C-iii)'s per-island bound E[|W_r − 1| | 𝓒] ≤ β (`:153`). They also need Ẑ = ¼Σ_r Ẑ_r (`:52-53`), so that |Ẑ/Z − 1| ≤ ¼Σ_r|W_r − 1|.
  - The P(completed ∩ {Ŝ ≠ S₀}) clause needs (C-iv)'s P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ̄ for one fixed r, the pathwise Ŝ clause of (LT-d) with Lemma PC (`:134-135`, `:90-95`), and GW-iv for {completed}.

`(b) (TR-d): NOT COVERED`

- **What is missing.** (TR-c) (`STATEMENT.md:169`) states the pip_primary bound only for the pooled quantity across the four islands. Its only per-island clause is P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ + e_L. So the ¼Σ_r route cannot be run from (TR-c).
- **What it needs.** It needs (TR-b)'s per-island bound E[‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g + e_L (`:168`). That right side is σ(data, 𝓒)-measurable and the same for every r: e_L = (1 − 1/M)^L, with M data-only and L in 𝓒. Again no event and no independence across islands is needed.
- **The Ŝ clause** needs the same inputs as for (C-v): (TR-c)'s per-island 𝓜_r bound, (LT-d) with PC, and GW-iv.

## 3. Findings

**F4 (Step 5's route list for (C-v) and (TR-d) is missing inputs). `MEAS_D.md:48`.**
- **Problem.** "(C-v) from (C-iv) and (TR-d) from (TR-c) through ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r‖p̂_r − 1_{S₀}‖_∞" is false as written: (C-iv) has no Ẑ clause, and (TR-c) has no per-island PIP bound. The claim at `STATEMENT.md:190` ("which is all that the joint-law clauses of §2 use") is still true.
- **Exact correction.** Replace that phrase by:

  > "(C-v) from (C-iii) and (C-iv) for each fixed r: the Ẑ, log Ẑ and NC_r clauses through |Ẑ/Z − 1| ≤ ¼Σ_r|W_r − 1| and (C-iii)'s per-island bound E[|W_r − 1| | 𝓒] ≤ β; the PIP and MPM clauses through ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r‖p̂_r − 1_{S₀}‖_∞, {MPM ≠ S₀} ⊆ {‖pip_primary − 1_{S₀}‖_∞ ≥ ½} and (C-iv)'s per-island bound g + β/2, whose right side depends on the data only. (TR-d) likewise from (TR-b)'s per-island bound g + e_L (σ(data, 𝓒)-measurable, the same for every r). In both, the Ŝ clause comes from the one-island bound on P(S₀ ∉ 𝓜_r | 𝓒) ((C-iv), (TR-c)), the pathwise Ŝ clause of (LT-d) with Lemma PC, and 𝒪 ⊆ 𝒪° (GW-iv)"

- **Also.** Change "(TR-d) from (TR-c)" in the fix-card notes to match. Nothing else changes.

**E9 (pin and the list of exits). `MEAS_D.md:38`.**
- `cpp/v3_core.cpp:475` → `cpp/v3_core.cpp:474`.
- "The only non-operational exits inside these searches are" → "The only non-operational exits of these final-run searches, inside them or at the LS0 call site, are".
- Add: "the scorer's `|S| > K` throw (`cpp/v3_score.h:230`), unreachable because the search skips additions at size K (`cpp/v3_engine.h:397`) and swaps keep the size".

**E10 (state the IND-T reading as derived). `MEAS_D.md:48`.**
- Replace "under IND-T read, like SI in `STATEMENT.md:35-36`, with the data adjoined" by:

  > "since IND-T, a premise of a fixed-data clause, holds given the data (`STATEMENT.md:29`), and each final stream is independent of the data (SI, `:35-36`), the conditional law of U^{(10:13)} given (data, U^{(0:9)}) is the fixed product law, so U^{(10:13)} is independent of (data, 𝓒°)"

**E11 (REGISTRY wording). `REPORT.md:203`.**
- "clauses that assume IND-T hold for the four final streams jointly" → "in clauses that assume IND-T, the same conditional form holds for functions of the four final streams jointly". This matches `STATEMENT.md:190`.

**E12 (gates pointer). `REPORT.md:205`.**
- `gates: correct:PENDING(reviews/R1_council_opus.md)` should name the R2 record (`R2_council_opus.md`) when this is recorded.

## 4. Gates

- **G1 correctness: FAIL.** Step 5's route list for (C-v) and (TR-d) cites the wrong inputs (F4). Steps 1-4, the F2 neighbour-graph addition and the IND-T derivation are correct.
- **G3 faithfulness and scope: PASS.** The scope is potential-only, the narrowed sentence matches Step 5 plus sums, comparisons and unions, and no premise is added.
- **G4 statuses and pins: PASS.** Ids and statuses match claims.tsv, and the F3 id is fixed. One code pin is off by one line (E9) and needs fixing before freeze.
- **G5 registration form: PASS.**

## 5. Score

**8.7.** There is one F (F4), fixable in a single sentence, and no C or S.

## 6. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R2 manifest=00426ac2fe589ac2d6de074c068942d86e0864d49a0f28631e476bf51dad6800 seat=opus score=8.7 gates=FAIL
