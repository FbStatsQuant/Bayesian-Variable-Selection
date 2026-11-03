# MEET-v31 · Chair synthesis of Round 2

Inputs: `R2_A.md`, `R2_B.md`, `R2_C.md` (fresh tasks; each read the dossier, Amendment 01, all R1 files, `SYNTH_R1.md` and `evidence/`), plus the evidence filed since Round 1:
- `evidence/2026-11-03_PC1_proof_check.md` (+ scripts): proof check PC1 (Opus 5.5, Claude Work);
- `evidence/2026-11-03_pip_rescore/`: post hoc PIP rescoring (partial; see §0).

ABL-START had no results when the seats wrote (draft design only), so item 1 is decided in Round 3 against a rule fixed now (§2).

## 0. New chair-checked facts (Round 2)

1. **PC1 verdicts** (all candidate proofs, checked line by line with exact-enumeration scripts):
   - Seat C's upper bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} is **PROVED** for the spec's m(S), for any y. It is very loose (≈ ν·log(n+1) nats).
   - P(max{Z_𝒯, 0.05Ẑ} > Z) ≤ 0.05 is **PROVED** for the potential run; the two events are equal. The output-event form is **CORRECT WITH AMENDMENT**: it needs Lemma RO/GUARD, a successful 𝓒, CAL/EX-S and distinct store entries.
   - Seat C's finite-R bound is **PROVED** (W_r ≥ 0 must be stated). The measured-round identity E[W_r H_r] = π(h) stays a premise.
   - THM-SYNTH A2's plain sentence "can only fail downward" is literally false (**COUNTEREXAMPLE**); formal A2(iii) is not refuted. Corrected wording is in PC1 §4.
   - Seat B's "top-store MPM needs δ₁ < ⅓" is **FALSE**. The amended result is PROVED: δ₁ < ½ suffices and is sharp, and under it the HPM and MPM^𝒯 certificates are equivalent. Seat C reached the same ½ in R2.
   - D3a: the post-search HPM is **not** monotone in R′ without the extra local search from the R = 4 centre (**COUNTEREXAMPLE**). No theorem in THEOREM_LIST needs the monotonicity; it is needed only for nesting or "stacking never worsens Ŝ" claims. Cor W-R as written (pre-search nesting) is **PROVED**.
2. **PIP rescoring is partial.** The per-island `pip_r` and `log_Z_r` of the 2,394 completed study fits are not on this machine. They are on NOTS (`/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/`) and the laptop. On the 3 designs with per-island data (S1 r001 c100, S4 r001 c050, S5 r002 c100):
   - equal-weight and Ẑ-weighted MPMs never differ, and max|ΔPIP| ≤ 1.3·10⁻³;
   - island ESS is 1.88 on S5 r002.
   Over all 2,394 fits, MPM_eq = S₀ in 1,779 and HPM = S₀ in 1,829. The full Ẑ-weighted rescoring is a reporting action for HQ (script: `evidence/2026-11-03_pip_rescore/pip_rescore.R`). It does not gate the decision (§1, D5).
3. **ABL-START arm A = production on a study design.** On p0500_S1_r001_c100 (seed 5420001), arm A's `log_Z_r` and `pip_r` are bitwise identical (`identical()` TRUE) to the METH-AUDIT production re-run. That re-run's HPM and F match the production ledger to 10 significant digits (`evidence/2026-11-03_pip_rescore/REPORT.md`). This closes Seat B's R2 request (0.3).
4. **ABL-START worker status.** The SDK worker ended its session at $2.45 while waiting (log `/home/fb31/api_workers/ABL-START.log`). Its 48 fits (12 designs × arms A–D) are still running in 3 Owls jobs: 6 done at 17:55 UTC. The chair is watching the jobs and will have them summarised with ABL-START's own `scripts/summarise.R`.
5. **Item 9 fact checks.**
   - The preflight's convolution and table proxy uses ⌈p/B⌉ blocks. The study's actual J is 46–60 at p = 500 (proxy 36) and 95–120 at p = 1,000 (proxy 72) (`/home/fb31/ls0_work/agg_final/ls0_per_fit.csv`), so the proxy underestimates (Seat C, E4). The bytes involved are small against 8 GiB.
   - The exact-branch boundary at n ≤ 5: Seat B is right ("all p"). With K = 2, E ≈ p²/2 < 4N₀·p ≤ RHS, since N₀ ≥ p. Seat A's "p ≈ 25,000" used N₀ = 2,500 fixed.
   - `global_certified` (exact branch) compares against the scorer's error expression, which the source calls heuristic (`cpp/v3_score.h:240`, `cpp/v3_core.cpp:535`). PC2 is checking it.
6. **PC2 commissioned** (Opus 5.5, Claude Work): line-by-line check of every O-CERT card item with Seat C's six corrections, and a recommended minimal card. This closes D2.

## 1. Status of D1–D8

| # | Item | Round 2 positions | Status |
|---|---|---|---|
| D1 | ABL-START rule | All three converge on a rule fixed before results: keep with a depth claim / keep but reframe / flag an issue, still ship the block start and run a 20-seed check. B withdrew "majority ⇒ change". | **Rule agreed (§2); result pending → Round 3** |
| D2 | Certificate card | All accept a POST HOC card of checked components only (A, B: gated on a proof check; C: six corrections). | **PC2 running → Round 3 confirms the card** |
| D3a | Extra local search from the R = 4 centre | A conceded; B, C keep. PC1: needed only for nesting or monotonicity claims. Its cost is ≤ ℓ + 1 scans and it keeps (d) ADDITIVE (nested). | **Closed: keep** (all three) |
| D3b | Flags under stacking | All: the expanded run reports flags over all R′ islands; a separately named baseline record (islands 1–4, with the baseline HPM and search) is kept when baseline reproducibility is claimed. | **Closed** |
| D3c | LS0 wording | All: island outputs, evidence and PIPs are unchanged; the scored set is nested and the best score cannot fall; HPM unchanged on 2,394/2,394. C corrected the wording, and A and B's "stores nested" falls: the bounded top store is 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), not a superset (eviction; `cpp/v3_ledger.h:41`). B added: LS0 must not fire E3; it gets its own provenance and an `ls0_improved` flag. | **Closed** (wording: C's correction + B's flag) |
| D3d | "Scale p" claims, C6 | All: state depth at the implemented level (islands only: N_e(T+L+4)(p+B+2) plus setup, calibration, grid and reductions) and drop "free of N, H, R". C6 stays the declared v3.2 path (LAW-PRESERVING). A and B tie the C6 trigger to "paper shows p > 2,500"; C rejects that threshold (N₀ also grows with n) and ties it to "paper claims particle-parallel depth". | **Closed as a conditional:** C6 is implemented and law-checked (20 seeds, two stream maps) iff paper 1 claims particle-parallel depth. Island-parallel results may be reported at any p with their actual cost. Paper scope is HQ's call; no method question remains |
| D3e | Extra parallel steps | All: (h) block tables as the explicit parallel local stage (bitwise). Clustering (C11), neighbour graph, grid bisection, convolution and pooling go into the cost account and the roadmap. C: no change of floating-point summation order under a bitwise claim. | **Closed** |
| D3f | Thread safety | All: process workers; threads need private counters merged deterministically. | **Closed** |
| D4 | Calibration cost | Closed by evidence (0.2 of SYNTH_R1). A's formula: calibration / final work ≈ 0.05 + 0.2·I (I = rebuilds), against observed 0.45 / 0.62 / 1.76 (predicted 0.46 / 0.67 / 1.69). W-cal is on the critical path of any wall-clock claim; the rule is unchanged. | **Closed** (rule kept; paper wording counts calibration) |
| D5 | Primary PIP | All three: Ẑ-weighted primary, equal-weight named secondary, both MPMs reported, R_eff = (ΣW)²/ΣW² per fit (B). POST HOC. B withdrew the truth-based gate. | **Closed** |
| D6 | Limitation wordings | (ii) and (iii) closed by PC1. (iv): the mechanism is PROVED in kind (E1/E2, SEP-B); severity on the production grid is OPEN (V11), a theorem obligation (all). (i) memory: A and B say "every worker needs all of X or G" is inherent; C says only *access* to all columns is inherent, since shared or distributed storage is possible at a communication cost; all agree the private 8p² Gram is not inherent. | **(ii)–(iv) closed; (i) wording → Round 3** (chair proposal §3) |
| D7 | General-h estimator | All: add a measured-round accumulator, ADDITIVE, no randomness, Ẑ-weighted across islands. The proposals differ only in scope: A archives the measured-round populations; B a declared list (size distribution, pairwise inclusion on neighbour edges, HPM frequency); C gives the formula H_r(h) = (4N_e)⁻¹Σ_qΣ_i h(S_rqi) after each complete measured round, at `cpp/v3_engine.h:351–359`. Not recoverable for the 2,400 fits. Identity = theorem obligation. | **Spec merge → Round 3** (chair proposal §3) |
| D8 | 6 resource_limit fits | All: not a method question; optional operational replay (HQ), labelled as such. | **Closed** |

## 2. Agreed decision rule for item 1 (fixed before any ABL-START result is read)

Merged from R2_A, R2_B and R2_C. Arms are as built: A = production block start; B = singleton factors × capped size prior (not independent Bernoulli); C = capped prior; D = backfit tables (v2 evidence only). Kernel B, neighbour graph and budgets are the production ones. Per design (12 designs × 1 seed) record:
- T_final and pilot T, rebuilds, tier and status;
- calibration and final seconds, with setup charged; arm D's table generation is charged (C);
- |log Ẑ_X − log Ẑ_ref|, max_j |PIP_X − PIP_ref| (Ẑ-weighted), and σ_r = SD of the arm's 4 log Ẑ_r.

The reference is leave-one-arm-out. It measures agreement, not certified error (C). A design whose arms' pooled log Ẑ disagree by > 1 nat is inconclusive for evidence error and is judged on depth only (A).

- **Outcome 1: keep, depth claim allowed.** Arm A has T ≤ min(T_B, T_C) and rebuilds ≤ min on ≥ 9/12 designs, and its accuracy is not worse than B's or C's by > σ_r on ≥ 9/12.
- **Outcome 2: keep, reframe** (no depth or speed claim; the start is justified as the exactly computable, theorem-bearing local step, S1/S2, plus the parallel table stage). Accuracy is not worse on ≥ 9/12, but Outcome 1's depth condition fails. An inconclusive result is Outcome 2.
- **Outcome 3: real issue flagged; v3.1 still ships the block start.** B or C beats A on accuracy by > σ_r on ≥ 9/12 designs, including both S4 and both S5 designs, and is not worse on depth on any S4/S5 design (A). Then:
  - the ablation is reported;
  - a ≤ 20-seed paired check on the two worst designs is commissioned;
  - a start change goes to Felipe as a WORKHORSE candidate only if that check confirms (ground rules 1, 5, 8).
- HPM counts are reported but do not decide (C's amendment: another start *can* change discovery, but HPM recovery is objective 3, not objective 1).

## 3. Chair proposals for Round 3 (for the seats to accept or amend)

**P-D6(i) wording.** Inherent (by definition of a full-coordinate move round): every move round reads all p columns of X (or the Gram entries), so every worker needs access to all of X, either local or shared/distributed at a communication cost. Not inherent: a private 8p² Gram per worker (C7 Gram-free scorer, LAW-PRESERVING up to floating point).

**P-D7 estimator spec.**
- For a list 𝓗 of bounded model-space functions, declared from (X, y) before any randomness, each island accumulates H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi) after each complete measured round (C's formula and placement). Report μ̂(h) = Σ_r Ẑ_r H_r(h) / Σ_r Ẑ_r, together with the equal-weight version.
- 𝓗 default (B): model-size distribution, pairwise inclusion on neighbour-graph edges (≤ 2pB pairs), and terminal frequency of the returned HPM.
- Optionally (A), archive the measured-round populations as model keys, so that any further h can be computed post hoc from the same draws.
- Marginal RB-PIPs are not multiplied to estimate joint events (C). Continuous-parameter functionals need h̄(S) = E[h | S, X, y] (C).
- Class: ADDITIVE. No study re-run; joint summaries are claimable only for new runs.

**P-9 consolidated item-9 resolutions.** All three seats find no setting that is class (e) *in the method's law*. The candidate (e) items and wording defects found, with proposed resolutions:

| id | Setting | Found by | Proposed resolution | Class | Study effect |
|---|---|---|---|---|---|
| e1 | B* = 16 called "implementation limit" | A, B, C | Re-label as (c): a budget for exhaustive tables. It keeps table work ≤ 2^{B*}·p/B* scores and memory linear in p; B = ⌊√p⌋ unbounded would make tables super-polynomial. W7-PART's g_max ≤ B < 2g_min is a hypothesis of one partition theorem (B = 14 covers g ∈ 8..14, B = 16 covers 9..16). The study's g = 5 is outside it; that is a theorem obligation (PART-pairing), not a method defect | spec text | none (B = 14) |
| e2 | Near-tie window 10⁻⁹ nat, absolute | A, B; C calls it a reporting tolerance | It silently drops below the scorer's error expression for n ≳ 10³. Keep the 10⁻⁹ list (study-compatible, informational; the HPM uses exact equality) **and** report η(Ŝ) beside it, with a heuristic near-tie list at max(10⁻⁹, 2η(Ŝ)) labelled heuristic (merges A, B and C) | POST HOC | none to any decision |
| e3 | Input domain n ≥ 3 | C | Extend to n = 2 (K = 1, B = 1, E = p + 1 ⇒ exact branch), route n = 1 and zero-predictor inputs to explicit degenerate statuses, reject n = 0. Seat A's reason "K ≥ 1 needs n ≥ 3" is wrong (K = ⌊2/2⌋ = 1) | ADDITIVE | none |
| e4 | LS0 start-mode tie enumeration cap 10⁶ (`cpp/v3_start.h:183`) | B (state it), C (e) | Keep the fast path. On truncation, use a deterministic tie-aware DP that selects the prescribed smallest-size and lexicographic maximiser without enumerating ties. Otherwise the LS0 status is explicit | ADDITIVE | none (0/2,400 truncated; all 2,400 had 1 tie) |
| e5 | `global_certified` uses a heuristic error bound | C | Label it a heuristic numerical margin; reserve "certified" for validated arithmetic (PC2 checks) | POST HOC (interface) | none (study used the SMC branch) |
| e6 | Memory preflight uses ⌈p/B⌉ blocks (underestimates J) and ignores per-worker replication | C; chair-confirmed (0.5) | Use J ≤ p before setup and the actual J after; account shared vs per-worker memory; label it "estimate" | ADDITIVE (engineering) | none at study size |
| e7 | Integer, stream-id and allocation arithmetic unchecked at huge sizes | C | Checked arithmetic, returning an explicit unsupported-resource status | ADDITIVE (engineering) | none |
| e8 | "Runnable from X, y and one seed alone" vs `resource_limit` | all | Re-classify the allocation as (c), a declared input. Every estimate on 𝒪 is a function of (X, y, seed, binary). The allocation and hardware decide only delivery (stop-only guard, Lemma RO). Guarantees are stated for the potential run and as P{𝒪, ·} (C's form, adopted by A and B). The literal "seed alone" sentence is corrected | spec text | none |
| w1 | Spec §10: neighbour scale "√(log n/n)" | A, B, C | Correct to r_n = √(2 log p / n); no familywise-screening interpretation | spec text | none |
| w2 | Spec §6.2: "all p ≤ 3,000 at n ≤ 5" | B (chair-checked) | "all p at n ≤ 5" | spec text | none |
| w3 | Unstated fallback: r_n ≥ 1 when p > e^{n/2} ⇒ forced 1-nearest-neighbour graph | A, B, C | State it | spec text | none |
| w4 | T₀ = max(1,000, ℓ²): the ℓ² term binds only for n + p > 2³¹ | A | State it | spec text | none |
| w5 | "Correlation cut" of the clustering | A, B, C | There is none; the cut is by size only. Correct any text implying a correlation cut | spec text | none |
| w6 | Stale "up to 20" block-width comment | C | Code comment: bound is 16 | none | none |
| w7 | Stream map for R′ > 4 (streams 10..9+R′) and R′ declared before stream 10 | A, B, C | State it | spec text | none |

The remaining constants (2,500 and 1,000 floors, 512/2,500, R = 4, tier ×4, 4 measured rounds, 20p and 40p+1, 500p, ESS 0.90, 60 halvings, 1-nat flag units, exact-branch rule) are kept and written as declared (c) budgets or (a) conventions with their stated reasons. Their values are conventions, not derived optima (C). Changing them later is not automatically law-preserving. **No separate p ≪ n / p ≫ n rule is needed** (all three): K, B, N₀, the exact-branch rule and r_n switch regime by formula.

**Theory scope (all three, merged).** The p ≤ n^A scope of the selection theorems comes from the target theory (Felipe's prior and the proof technique), not from a sampler choice. Song–Liang's e^{Cn^α} rests on their own prior and conditions and cannot be imported. Whether our prior admits it is OPEN, not impossible (C). Method-induced restrictions are stated as such:
- the cap K excludes s₀ > K by definition;
- fixed B limits whole-group recovery to g ≤ B;
- bounded stores can omit posterior mass;
- logarithmic ℓ and L may be short for some proof routes (theorem obligations);
- N₀ ≥ p and full-coordinate rounds impose real computational growth.

## 4. Round 3 agenda

Only these items:
1. ABL-START result against the §2 rule.
2. Certificate card per PC2.
3. P-D6(i) wording.
4. P-D7 estimator spec.
5. P-9 table (e1–e8, w1–w7).

Each seat accepts or amends each proposal; a hold must name the evidence that would change it. Everything else in §1 is closed and recorded in the minutes.
