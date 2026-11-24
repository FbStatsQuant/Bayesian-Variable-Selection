# H2: the frozen 1M engine (F2) and sources for the PLANNED results

Helper H2 (Sonnet research sub-agent, Writing Department), 2026-11-23. Read-only research; this file is the only output.
Nothing in the repo was changed, checked out, committed or pushed. Scratch copies of the cited files are in
`/home/fb31/BVS-wt/WRITING/.rc_tmp/h2/` (git-show copies; their line numbers equal the repo line numbers at the pins below).
No 1M results are quoted. Verdicts quoted are pass/fail verdicts on the 10^4 overlap and on the frozen-configuration re-score only.

## Pin legend (every fact below carries one)

| tag | meaning |
|---|---|
| **TAG** | git tag `p1m-freeze-F2` = commit `e993ece226b355058e26400f05f9faad6daf16ca` (code only; read with `git show p1m-freeze-F2:<path>`). Engine tree `Scripts/SMC_BVS/engine_v4/`; method core tree `61b0a582…` |
| **P1M** | the department docs, at `origin/exp/P1M` = `7fc2201c` (`git show origin/exp/P1M:Docs/Experiments/P1M/<file>`). Docs are not in the tag. The P1M clone HEAD is `6d68ae0c`, seven commits ahead; the files cited were identical to the ones read here |
| **HQD** | `Theory_work/Wave3/HQ_DECISIONS.md` in this worktree (HEAD `0f362503`); line numbers are this file's |
| **DEC** | `Docs/Experiments/P1M/DECISIONS.md` (D-n = Engineering design decisions, H-n = HQ rulings logged by Engineering) |
| **SPEC** | `Docs/Experiments/P1M/ENGINEERING_SPEC.md` (status line 3: "v2 DRAFT (EXP-CP1 v2), 2026-11-15"; "Where §0-v2 and §0–§7 disagree, §0-v2 wins") |
| **QDT** | `Theory_work/Dept/QUEUE.md` on `origin/dept/theory` (`06653556`, 2026-11-20, "owner break, full hold"). The copy in this worktree is older (it lacks the 11-17/18 riders and the 11-20 status block), so QDT is the one cited |
| **MAIN** | `origin/main` |

The theory department is on hold (HQD:890, QDT:1-3). Nothing in section B is current beyond 2026-11-20, except the PRE-LEAN branch log (last entry 2026-11-23).

---

# A. The p = 10^6 engine as frozen at `p1m-freeze-F2`

## A0. Identity of the freeze

| fact | value | source |
|---|---|---|
| F (first freeze, 2026-11-18) | `eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463`; every 10^4 overlap record carries this git_commit | `P1M results/overlap1e4/OVERLAP_1e4_VERDICT.md` §1 (provenance table); HQ order H-14, `TAG Scripts/SMC_BVS/engine_v4/CAMPAIGN_FREEZE.md` l.1-3 |
| F2 | merge of PR #88 into `exp/P1M-engine` with `--match-head-commit 09fc8fa2` → **`e993ece226b355058e26400f05f9faad6daf16ca`**, tag `p1m-freeze-F2` (tag object `ab0e3e6c`) | DEC l.122 (H-31, HQ 11-19) |
| F2 binary | `BUILD_F2` sha256 `da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a`, island_isa `sapphirerapids`, built once on NOTS from a clone of e993ece2 | `P1M results/vn_minileg/F2_IDENTITY_CHECK.md` l.5 (row "build") |
| method under it | `method-v3.1.1-listpip` (tag object `15a6d841…`), commit `7100bb3b5a341aed5cbcd3b03fa5851a6345f0dd`, `Scripts/SMC_BVS/core/` git tree `61b0a5822019b2737fe415ff15625e410f3227b2`; any later change under `core/` is refused at plan generation | `TAG CAMPAIGN_FREEZE.md` §1 (l.12-26) |
| "F2 = F bit for bit" | HQ's own wording, 2026-11-20: "V-N mini-leg verdict ACCEPTED … (… 15/15 fits, 236.5 core-h; F2 = F bit for bit)". What was checked: one fit (AR r01, n = 200), the F2 binary against the F-build record, at **default N = 2,500, I_max 3, m 1**: 16/16 `logZ_r` bit-equal, HPM equal, 16/16 island output hashes equal, 24 JSON sidecars equal after dropping provenance keys, 0 scientific differences. The N ≠ 2,500 paths (the V-N feature itself) are not exercised by that check | HQD:850; `P1M F2_IDENTITY_CHECK.md` l.3 and l.9-12, "Scope and limits" paragraph; DEC l.122 (H-31 (1): this check "must PASS before ANY F2 run") |
| what F2 changed vs F | #85–#88 (PR #88 = "V's N settable", Opus ACCEPT-WITH-FIXES, 35/37 objects byte-identical to F, default-N bit identity re-verified). The details of #85–#87 were not read | DEC l.122; HQD:822 |

## A1. What the engine is, and each documented change against the theorem-covered method

**The engine.** "v4" (`smcbvs4`), C++, in two configurations of one engine: **T** = the theorem-covered method as coded (core `method-v3.1.1-listpip`), run in a compat mode (serial v3.1 streams, bit-identical to revision D, only for p ≤ 5k) and a law mode (addressed streams, threaded, checkpointed) at 10^4; **V** = the engineered variant for 10^5/10^6. "The paper presents V as an engineered variant validated against T (POLICIES §8)." Source: SPEC §0-v2.1, l.43-50.

**The complete change list V vs T** is SPEC §0-v2.2 (l.52-64), amended by the DEC rows below. One line each, in the SPEC's order:

| # | change (V vs T) | state at F2 | source |
|---|---|---|---|
| 1 | **Fixed N per island** (T: N = max(2500, n, p), tier 1 = 4×N) | N = 2,500 default; settable (PR #88). Which N is used where: A2 below | SPEC l.55, l.44; DEC D-1 (l.39); `TAG calib.h` l.7-9 |
| 2 | **R′ = 16 process islands + merge**: one process per island, no communication between islands; union of stores; equal-weight RB PIP (`pip_eq`) primary; evidence = plain mean of the island Ẑ_r | R′ = 16 at every rung | SPEC l.56, l.253-262 (§3 table: "none between islands"); DEC D-6 (l.44), D-11 (l.50); `OVERLAP_1e4_PREREG.md` §3.3-3.4 (l.57-70: `pip_primary` = `pip_eq`, log Ẑ = "plain mean of the island Ẑ_r, v3_run.R:155") |
| 3 | **Position-addressed, counter-based uniforms** (address = seed, role, phase, stage/round, particle, position, slot); result independent of thread count, block size, G | on | SPEC l.57; DEC D-5 (l.43) |
| 4 | **Label-major batched kernel, class-A arithmetic** (bordered update, FMA, vector log/exp; ≈ 10⁻⁹ relative agreement with the coded scorer). T uses the bit form (equals `v3::Scorer` bits) | on in V. **ISA rule:** class-A bits depend on FMA, not vector width, so `island_isa` is mandatory in every V plan, minimum x86-64-v3; production uses `sapphirerapids` | SPEC l.58, l.78-81; DEC D-15 (l.55), D-32 (l.99); `F2_IDENTITY_CHECK.md` l.5 |
| 5 | **Partition**: complete linkage truncated at 1 − τ_n on the sparse graph {\|r\| ≥ τ_n}, τ_n = r_n; the coded top-down cut for clusters > B; next-fit packing by minimum index; **block cap B_V = min(B, 14)** at every n | on; `bv_cap = 14` | SPEC l.59; DEC D-4 (l.42), D-19 (l.85); `TAG include/v4/setup.h:78`, `src/setup/partition.cpp:219` |
| 6 | **Bounded calibration**: pilot + preliminary grid + at most I_max rebuilds; **no tier escalation at all** (H = 512, N = the calibrate parameter, tier 0 only); a grid-construction failure installs the last constructed grid, else the pilot schedule, flag `grid_fallback`, never "no output"; flag `grid_unconverged` if the last grid is not bitwise converged (documented as "bounded-stop") | I_max: A2 below | `TAG include/v4/calib.h` l.7-12 (header comment), l.60 (`grid_fallback = true`), l.179 (check `0 <= I_max <= ell`); DEC D-2 (l.40), D-26 (l.93); HQD:827 |
| 7 | **Grid refinement** m: every interval of the frozen grid split into m equal parts | m = 1 (i.e. none) | `TAG calib.h:62` (`refine_m = 1`); DEC D-12 (l.52); DEC l.121 (H-30) |
| 8 | **New estimators beside the coded ones**: log Z_𝒯 (deterministic lower bound; "no deterministic upper bound exists"), PIP_𝒯, `law.bin` (the store-BMA law = Π̂^𝒯 of DIST-C(i)), and log Ẑ_occ (store sum over the top-M models, M = 1, 10, 100, 1,000; "consistent in N, no theorem yet") | returned. log Ẑ_occ's ≤ 0.05 criterion was **replaced** in the 10^4 overlap by the log Z_𝒯 lower-bound consistency check; the occ fields still exist (GC_PREREG C2 uses `occ[M=1000]`) | SPEC l.62; DEC D-8 (l.46), D-13 (l.53), D-21 (l.87); `OVERLAP_1e4_PREREG.md` §3.5 (l.81-85) |
| 9 | **Systematic resampling; more N-swap labels per round** | **off**: the frozen configuration is "resampling off ('not tested')", i.e. the method's multinomial resampling is kept; so this is not a change in F2 | SPEC l.63; DEC l.121 (H-30); `GC_PREREG.md` l.10 |
| 10 | **No score cache, no `fresh`, no leader stores in final islands**; each island keeps a store of its 40p + 1 best models | on; cost reported as `logical` score counts | SPEC l.64; DEC D-3 (l.41), D-7 (l.45) |
| not in SPEC §0-v2.2 | **Offer floor τ_cal** (V mode): final islands offer to the store only above the calibration floor; merge checks floor ≤ cut-off | on in V; compat/law keep the full store | DEC D-29 (l.96) |
| not in SPEC §0-v2.2 | **Exact fixed-point RB sum** (128-bit, order-independent) in place of the core's double sum (class A against core) | on in V | DEC D-22 (l.88) |
| not in SPEC §0-v2.2 | **Canonicalised accepted states**: every accepted state re-scored by the full bit scorer, one value per model, no path dependence | on in V | DEC D-23 (l.89) |
| not in SPEC §0-v2.2 | **Final local search tail on the merged store** (HPM "certified by the final local search"; `local_certified`) | part of merge | SPEC l.67, l.199, l.259; `GC_PREREG.md` C2 row |
| not in SPEC §0-v2.2 | **Rolling-admission kernel** (WP6 K5), default on in F2, absent in the 11-17 code `2cfaa9e5`: changes pass composition (counters), not the state | on | `GC_PREREG.md` §3 (I3 row and "Why the gate is built this way") |

## A2. The frozen parameters, and the N story

| knob | frozen value | where it applies | source |
|---|---|---|---|
| **refine_m** | **1** (binary default also 1) | all F2 campaign fits | `TAG calib.h:62`; DEC l.121 (H-30: "m = 1"); `GC_PREREG.md` l.10 |
| **I_max** | **0** in the campaign configuration (pilot-only: no rebuild). **The binary default is 3** (`int I_max = 3;`): the 0 is set explicitly in every campaign plan, not a code default | all 10^4 science fits re-scored as `VF`, the 10^5 rung, the 1M fits | `TAG calib.h:61`; `GC_PREREG.md` l.10 ("explicit in every plan"); DEC l.121 (H-30); HQD:824, HQD:856 ("**I_max = 0 stands**", the G-B registered rule PASS); DEC l.131 (H-40) |
| how I_max = 0 was chosen | FZ (precision freeze) accepted "as the registered rule reads it", HQ: "although the I_max = 0 adoption is fragile (M3 1.130 vs 1.15; about 60–70% re-run stability)". Then re-tested at 10^5 on two pairs (G-B): same rule, PASS (geometric ratios 1.007 / 0.927 / 0.904 vs 1.15; per dataset 0.89–1.01 vs 1.30; HPM identical). HQ noted the low power: the two pairs "detect only a GROSS I_max failure" | | HQD:824-825, 856; DEC l.121, l.130 (H-39); `P1M results/gb/GB_PREREG.md` l.5, l.18-21 |
| **N: default** | **2,500** per island, "equal to v3.1 for p ≤ 2,500 and n ≤ 2,500" | the default of the binary; the N threads below | DEC D-1 (l.39); `F2_IDENTITY_CHECK.md` l.3 |
| **N: where 2,500 applies** | the **10^4 science and precision legs** (N 2,500 provisional), the 1M replicates (AR-strong r01–r20, ADJ-OPP, AR-weak), option D (n = 1,000), the conditional 20-seed block, and the 2 continuity twins at 10^5 | | HQD:824 ("N 2,500 (provisional)"), 850 (S2), 856-861; `GC_PREREG.md` l.10, l.15-17 |
| **N: where 10^4 applies** | **N\* = 10⁴** by the pre-declared mini-leg rule, **for the 10^5 rung and the G-B pilots** ("10^5 rung at N 10^4"); and, as planned, **ONE** N = 10⁴ 1M fit on the rep-1 data (`VN10K`) | | HQD:850-851; DEC l.129 (H-38); DEC l.131 (H-40); `GC_PREREG.md` l.15 |
| the rule that gave N\* = 10⁴ | MINILEG_PREREG §3 (pre-declared before any fit): ADOPT N = 10⁴ iff, on each of M1 (`sd_log_Z_occ_r`, M = 1000), M2 (`pip.island_spread.max_sd`), M3 (σ̂ = sd(log Ẑ_r)), the geometric-mean island-sd ratio r ≤ 1/√c_X (c_X = measured islands-cost ratio ≈ 3.85, so r ≤ ≈ 0.51) and r < 1 in every dataset, and HPM identical; else KEEP 2,500. Under plain 1/√N scaling the true ratio sits at the bar (P(ADOPT) ≈ 0.25), "the expected verdict is KEEP". **Outcome: ADOPT**, "fragile (M2 margin 0.0019); the meaning is 'not worse per core-h', not 'better'. No post-hoc override." | | `P1M results/vn_minileg/MINILEG_PREREG.md` l.8-9, l.30-33, l.44-45, l.51-54; HQD:850 |
| the S2 consequence (adopted) | "10^5 rung at N 10^4; 1M replicates at N 2,500 plus ONE N 10^4 1M fit on the rep-1 data; the conditional 20-seed block at N 2,500". Continuity twins (2 fits at 10^5, N 2,500, same data and seeds as 2 rung fits) connect the two N threads | | HQD:850-851; DEC l.129 (H-38) |
| **status of the N = 10⁴ 1M fit** | **Planned, never run.** The owner stopped the 1M AR-0.6 block after W2: "After W2 submit NOTHING (no W3+, no N 10⁴ 1M fit, no 20 seeds)". This matters for any sentence that says 10^4 is "one arm" or "one doubling fit" | | DEC l.144 (H-53); HQD:888 |
| **R′ (islands)** | **16** process islands, one socket each (48-core threads), calibration diagnostic islands separate (4 threads of one process; I_max + 1 sequential rounds). **How pooled:** union of the 16 island stores (top store 40p + 1 kept); primary PIP = the equal-weight island mean `pip_eq` (the method's pooling, `v3_run.R:162`); evidence log Ẑ = plain mean of the island Ẑ_r (`v3_run.R:155`); returned beside it: PIP_Z (with R_eff, max W_r), PIP_𝒯, log Z_𝒯, `law.bin`; then the final local search tail. "Do not weight islands by Ẑ at p ≥ 5k" (island evidence spread) | | SPEC l.56, l.253-262; DEC D-6, D-7, D-8, D-11 (l.44-46, l.50); `OVERLAP_1e4_PREREG.md` §3.3-3.4; Theory's CLAIMS_CARD l.93-101 (pillar 4.1, 4.3) |
| block cap | B_V = min(B, 14) | | `TAG setup.h:78` |
| grid / calibration budget | H = 512 always; tier 0 only; the 11-17 pilot's `calib.bin.json` settings read K 100, H 512, Hm 4, L 8, T_e 1000, ell 20, N_final 2500 (as recorded in a Sonnet extraction note, **not** re-read from the file) | | `P1M results/scale1e7/PHASE0_NOTES.md` §1.3 (marked DRAFT, unreviewed); `TAG calib.h` l.8 for H = 512 |
| store | top store 40p + 1; one store per process with bounded thread buffers; G ≤ 256 chosen by admission (largest that fits) | | SPEC l.23; DEC D-7 (l.45), D-24 (l.90) |
| ESS / resampling | resampling "off ('not tested')" (multinomial of the method kept); π₀(S₀) "deferred". A `low_empirical_ESS` flag is reported but is not gating | | DEC l.121 (H-30), l.138-140 (H-47 to H-49) |
| time scale of the final islands | T = 27 expected at 10^6, n = 200 (stage count); 30 bridge rounds at 10^5 T5 (an older build) | | `GC_PREREG.md` l.35 (I4 row); `PHASE0_NOTES.md` §1.2 |
| seeds | data seed = engine seed, e.g. 602020001 for the AR-strong rep 1; AR replicates 602020002…20; the conditional seed block 602020001 + 100(i−1) | | `GC_PREREG.md` l.15-17 |
| evaluator | n_x 4,000, n_gh 64, n_draws 10⁴, n_test 10⁴, rel_cut 1e-12, top_k 1,000, tail_r 1,000, tail_groups 8, block_rows 500; eval seed = the dataset's data seed | | `GC_PREREG.md` l.9 |
| precision targets (reported, never used to switch estimators) | PIP sd over islands ≤ 0.005; evidence sd of log Ẑ_occ,r ≤ 0.05; σ̂ goal ≤ 0.5; HPM certified | | SPEC l.66-70 (§0-v2.3); `GC_PREREG.md` l.35-37 |

## A3. How V was validated against T on the overlap rung (pre-declared criteria; verdicts only)

**What was run.** The only head-to-head against the theorem-covered method is at **p = 10^4**: T (new engine, law mode, coded calibration with escalation) vs V, **10 datasets × 2 seeds × 2 arms = 40 fits** (AR-strong 4, AR-weak 2, ADJ-OPP 2, IND 1, NULL 1; n = 200). Source: SPEC §0-v2.7 (l.109-122); `OVERLAP_1e4_PREREG.md` §1-2 (l.14-45).

**Pre-declared criteria** (`OVERLAP_1e4_PREREG.md` §3-4, committed before W0; "nothing in the thresholds below is tuned on data", l.3):
- **D** delivered 40/40 (§3.1, l.51-53); **PAIR** X and y content hashes equal within a dataset (INVALID otherwise, §4 rule 1).
- **S1** HPM(V) = HPM(T) as sets in ≥ 9 of 10 datasets (both seeds); **S2** no seed pair with F_T > F_V + 10⁻⁶; **S3** MPM equal in all 20 pairs; **S4** NULL: no PIP > 0.5 in all 4 null fits (§3.2, l.54-58).
- **P** per dataset, max_j |PIP_V − PIP_T| ≤ max(0.01, 3 combined s.e.) (§3.3, l.57-66).
- **E1** |Δ log Ẑ| ≤ 3 combined s.e. for all 10 datasets, with a pooled seed-to-seed yardstick (§3.4, l.67-77).
- **E2** log Z_𝒯 is a lower bound: log Z_𝒯,T ≤ mean log Ẑ_V + 3 s.e., and the mirror, and per fit log Z_𝒯 ≤ log Ẑ + 3 s.e. (§3.5, l.81-85). This **replaced** SPEC's |log Ẑ_occ,V − log Ẑ_occ,T| ≤ 0.05 (D-21, H-18).
- **H** Hellinger distance between the store-BMA predictives d_H(V,T) ≤ 10% of d_H(T, f\*) per dataset (§3.6, l.86-93).
- **C** cost: every fit ≤ 1.5 × its arm's model (V ≤ 15.0, T ≤ 172.5 core-h) (§3.7, l.95-96).
- **Outcome rules** (§4, l.98-103): INVALID / NOT CLEAN (≥ 2 HPM misses, any F_T > F_V, or ≥ 2 predictive fails) / MARGINAL / INCOMPLETE / CLEAN (all criteria pass **and** an independent review ACCEPTs).

**Verdicts.**
- **CLEAN under the v2 scorer** (`compare_overlap_v2.py`, operative per ADDENDUM_1 / H-21): 40/40 delivered, 11/11 criteria PASS, independent Opus review ACCEPT-WITH-FIXES (10 documentation fixes, none changing an outcome); HQ accepted it on 2026-11-19. Source: `P1M results/overlap1e4/OVERLAP_1e4_VERDICT.md` l.1, l.6-8 (summary items 1-2); HQD:811.
- **The registered script does not print CLEAN**: it prints MARGINAL (the registered outcome per §4 would be INCOMPLETE) because of a script defect: the 3 escalated T fits count as "not delivered" and S1 has no NOT_EVALUATED branch. The independent review found it, and "the printed MARGINAL is a script defect". A manuscript sentence should say "CLEAN under the scorer amended by ADDENDUM_1", not "CLEAN" without that qualifier. Source: VERDICT summary item 1.
- **Re-score of the frozen configuration** (ADDENDUM_2_VF: 14 V fits re-run at I_max = 0 and scored against the existing T fits): scored CLEAN, 11/11 PASS on the mixed 40-fit set, H 14/14. "No newly failed criterion". Source: `P1M results/precision1e4/LEG_READBACK.md` l.6 and l.9 (summary items 1 and 4); HQD:835.
- **Not found / not done** (stated plainly, not guessed): (a) **no T arm at 10^5**: SPEC §0-v2.7 lists "overlap 10⁵ (owner option): T vs V, 1 dataset, ≈ 6,100 core-h" (l.115), but nothing I read shows the owner bought it. The 10^5 rung is V-only (12 fits, and its acceptance rests on its own precision/cost/restart criteria, plus the two N-continuity twins). (b) The **exact level** (p ≤ 25, SMC branch forced vs enumeration) and the **5k anchor** (unmodified revision D vs the new engine's T vs V) are listed in SPEC l.112-113 as gate G-A items; **I found no read-back document confirming either was run** (the file `F2_IDENTITY_CHECK.md` and the G-A closing ruling HQD:835 do not mention them). Treat both as "listed in the spec, status unverified" until Engineering confirms. (c) The overlap compares V and T **estimates** on 10^4; no claim about equality at 10^5 or 10^6 is validated against T anywhere.

## A4. Comparison with `supplement.tex` §"The engine for p=10^6" (l.466-491)

Status of the text as read: it is a **plan-stage description** ("the planned engine", "will be reported") taken from the 2026-11-15 draft spec. F2 was frozen on 2026-11-19. Findings, sentence by sentence (line numbers are `Docs/Writing/manuscript/sections/supplement.tex`):

| line | sentence / row | verdict against F2 | what is true |
|---|---|---|---|
| 466 | heading "The engine for p = 10^6 (an engineered variant)" | OK | |
| 468 | "It is the engine of the planned runs at p = 10^6" | **STALE** (tense) | The engine is frozen (TAG e993ece2) and the 1M fits have been run (G-C2 pilot accepted, DEC l.136 (H-45, H-46); W1/W2 waves, DEC l.137-147). The 1M results are out of scope for this edition, so say "the frozen engine (tag `p1m-freeze-F2`) used for the p = 10^6 runs" and do not quote results |
| 470 | "To run at p = 10^6, the planned engine changes the method as listed in Table …, taken from the draft engineering specification of 2026-11-15" | **STALE** | Source is the frozen engine; DEC D-n/H-n and `CAMPAIGN_FREEZE.md` supersede the draft. SPEC itself is marked "v2 DRAFT" |
| 470-471 | "entries marked 'to be decided' depend on a precision study" | **WRONG now** | They are decided (A2): m = 1, I_max = 0, N = 2,500 (and 10⁴ for the 10^5 rung); the precision study (FZ) closed on 2026-11-19 (HQD:824) |
| 471-473 | "reported as an engineered variant validated against the method … on shared problem sizes (p = 10^4, and p = 10^5 where possible)" | **WRONG on 10^5** | The T-vs-V comparison exists at 10^4 only (A3). 10^5 had no T arm. State: "validated against the method at p = 10^4 (10 datasets, two seeds, 40 fits, CLEAN under the amended scorer), and at 10^5 and 10^6 checked only by its own pre-declared precision, cost, memory and restart criteria" |
| 477 | row "particles per island": "fixed, 2,500 (10^4 in one arm of the precision study)" | **INCOMPLETE / misleading** | 2,500 is the default and the 10^4-science / 1M-replicate value. N\* = 10⁴ was adopted for the 10^5 rung and G-B (A2); "one arm of the precision study" is the V-N mini-leg, not the precision study; the one planned N = 10⁴ 1M fit was **never run** (H-53) |
| 477 | method column "4^i max(2500, n, p)" | **OK in substance** | SPEC l.44: N = max(2500, n, p); tier 1 is 4× (core coded rule). Not re-checked against `core/` |
| 478 | row "islands: sixteen, separate processes, merged (union of stored models; equal-weight inclusion probabilities as the primary estimate)" | **OK** (add one item) | Add: the evidence is the plain mean of the island Ẑ_r, and the final local search runs on the merged store |
| 479 | row "random numbers: addressed by position (counter-based)" | OK | |
| 480 | row "scoring: batched kernel, different floating-point arithmetic, ≈ 10⁻⁹ relative" | **OK** (add) | Add: the FMA instruction-set family is mandatory (`island_isa sapphirerapids`), every accepted state is canonicalised by the bit scorer, and the RB sum is an exact fixed-point sum (D-32, D-23, D-22) |
| 481 | row "blocks: … truncated at a correlation threshold, same top-down cut, packing by smallest index; B ≤ 14" | **OK** | τ_n = r_n; `bv_cap = 14` (`TAG setup.h:78`) |
| 482 | row "calibration: the pilot and at most a fixed number of rebuilds (0 or 3, to be decided), **no move to tier 1 except after a failed construction**" | **WRONG (two errors)** | (i) I_max is decided: **0**. (ii) V has **no tier escalation at all**; after a failed grid construction V installs the last good grid, else the pilot schedule, flag `grid_fallback` (`calib.h` l.7-12; D-26). The method column ("at most one move to tier 1") is right |
| 483 | row "grid: optionally each interval split into m ∈ {1,4} (to be decided)" | **STALE** | m = 1: no refinement in the frozen configuration |
| 484 | row "estimates: the same, plus a deterministic lower bound on log Z from the stored models, an evidence estimate based on how often the islands visit the stored models, and inclusion probabilities from the stored models" | **PARTLY STALE / loose** | The three additions exist, but (a) it omits `law.bin`, the store-BMA law (D-8), which feeds the distribution evaluation; (b) the occupancy estimate is a store sum over the top-M models, not a visit frequency, and it is not used as a validation criterion on the overlap rung (D-21); (c) "no theorem yet" label (D-13) |
| 485 | row "resampling and moves: systematic resampling and more neighbour swaps per round, off unless the precision study shows a gain" | **STALE: the row should be deleted or turned into "unchanged"** | The frozen configuration keeps the method's multinomial resampling ("resampling off (not tested)"); this is not a change in F2 |
| 486 | row "caches: no score cache and no stores of 20p in the final islands; each island keeps a store of its 40p + 1 best models" | **OK** | Add the offer floor τ_cal (D-29), absent from the table |
| (missing) | — | **MISSING rows** | offer floor; fixed-point RB sum; canonicalised states; the mandatory ISA; final local search tail on the merged store; N settable (PR #88); `law.bin` |
| (placement) | — | note | `sections/or4_sampler.tex` l.275-277 (untracked) holds a placeholder `ENGINE-PENDING` with the same label `sec:supp-1m`; `manuscript.tex` inputs only `supplement.tex` and `appendices.tex`, so only the supplement text above is live |

---

# B. Sources for the PLANNED results (print as PLANNED, not claimed)

Overall state: all four are **not started or not completed**, and **Theory is on hold entirely** (HQD:890; QDT:1-3). Resumption "until the owner restarts it".

## B1. The trap theorem

- **Intended statement.** Per `Docs/Writing/ASSIGNMENT_6.md:37` (the only place the statement is written): "a mixing lower bound for single-flip MCMC (and wTGS) on a multimodal design, plus our consistency on the same design". That is all the repo states. No formal statement, no design family, no rate, no hypotheses and no theorem number exist.
- **Where it is mentioned.** HQD:849 (HQ, 2026-11-19 night, recording the owner): "the whole post-1M package (the 10^7 single shot, the full theory analysis, the trap benchmark) comes AFTER the 1M mission, conditional on 1M going well and quickly … **Theory plan for later: (c) the trap theorem first, then 10^7 coverage.**" The label "(c)" is not defined by any line I found (not NEXT_CAMPAIGN's §(c), which is "Parked": T-MERGE etc.).
- **Drafts / plan files.** **None found**: no file on `origin/main`, `origin/dept/theory`, `origin/exp/P1M` or `origin/theory/*` contains "trap theorem". The `git grep` for "trap theorem|mixing lower bound" returns only ASSIGNMENT_6:37, HQD:849 and one literature row (LIT-MCMC REPORT.md:87, Kim & Ročková, Bayesian CART, "UNVERIFIED", not BVS). The wTGS name occurs in older literature notes only. The files `Theory_work/Wave2/W2-FAC-K2/numerics/N1_A_trap_indep.jsonl`, `N1_C_trap_corr.jsonl` are a **different use of "trap"** (local-search trap cases for a factor-model experiment); they are not this theorem.
- **The trap BENCHMARK** is a separate Engineering item (HQD:849 lists it separately; the owner's instruction). No benchmark plan file was found either.
- **Status:** PLANNED, no draft. **Owner:** Theory Department (HQD:849), on hold. **Order:** after the 1M mission and conditional on it (HQD:849); before the 10^7 coverage ("the trap theorem first, then 10^7 coverage").
- **Open question for HQ (write down, do not guess):** what "our consistency on the same design" refers to. The registered consistency results are Thm 6 / Cor 6L (delivery, true model by the sampler) and the posterior-concentration rows; which of them is meant on a multimodal design, and what the design is, is not specified.

## B2. Coverage at p = 10^7

- **What is documented.** HQD:840-849 (HQ, 2026-11-19 night, owner): 10^7 is "seriously considered", then "NOT gradual": a new engine derived from F2 whose validation is inherited by bit-identity at p ≤ 10^6; then **one fit, one seed, a showcase** on a simulated AR-strong n = 200 dataset with known truth, ≈ 3–4k core-h, with per-stage checkpoint/restart and a kill rule (HQD:847-848; DEC l.126-128, H-35 to H-37). The whole post-1M package comes after 1M (HQD:849); the Phase-0 desk study is **paused** (DEC H-35; `P1M results/scale1e7/PHASE0_NOTES.md` is a DRAFT, "unreviewed, paused 2026-11-20 by HQ", a data-extraction dump, not the requested feasibility note; no `FEASIBILITY_1E7.md` exists). Budget note: after 1M plus 20 seeds about 3k remains in 28.3k, so the 10^7 shot "will need more allocation or a trade-off. Decided after 1M" (HQD:855, item 5 of the 11-20 S2 ruling).
- **"Coverage" itself is not defined anywhere.** The only statement is "Theory plan for later: … then 10^7 coverage" (HQD:849) and ASSIGNMENT_6.md:38. Closest candidate readings (neither stated in a source): (i) **theory coverage**: whether the registered theorems' hypotheses and delivery conventions cover p = 10^7 at n = 200 (HQD:840 item (4) lists "the theory regime at n = 200" among the feasibility risks; Theory's card states delivery for inputs R can represent, n, p_raw ≤ 2^31−1, so p = 10^7 is inside that integer range, but the card does not address n = 200 against p = 10^7); (ii) **claim coverage**: which claims the single shot can legitimately carry (one fit, one seed supports no replicate or coverage-probability claim). I recommend the manuscript says only "PLANNED: a theory analysis of what the p = 10^7 single fit does and does not support", and asks HQ which reading is meant.
- **Status:** PLANNED; engine design paused; theory analysis not started. **Owner:** Theory (analysis), Engineering (engine; paused). **Order:** after 1M, after the trap theorem (HQD:849).

## B3. Lean certificates

**Governance (chronological):**
- Department set up, ready, not started (HQD:385-387, 2026-11-15); owner gate: "no Lean code until HQ, the consultant and the owner agree the theory is final; Lean done = final", wait for HQ's GO (`Lean/BRIEF.md:1`).
- Launch had been set for Thu 11-19 / Mon 11-23 (HQD:459, 711); owner: the work is **in-house** (HQD:776); **method signed final 2026-11-18** (HQD:777); then **"the Lean conversion is PAUSED until he has read the whole theorem set and signed off … Lean happens when the owner brings it back"** (HQD:794, 796). 2026-11-19: **"Lean starts only on his word, spread to Feb/March"** (HQD:821). So: **not started; owner-gated.**

**What exists.** Only a scaffold: branch `origin/lean/BVSCert` (head `69378fa7`, auto snapshots only) with `Lean/BRIEF.md`, a lake project (`lean4:v4.35.0-rc2`, Mathlib `065356127b1d…`, same as BNP) and one smoke lemma `BVSCert.smoke` (`0 ≤ a*b`) in `Lean/BVSCert/BVSCert/Basic.lean`. No `TARGETS.md`, `CERTIFICATES.md`, `FIDELITY.md` or `AXIOMS.md`, no theorem certified. The folder `/home/fb31/SMC_Lean_Department/` does not exist.
- A sorry-free snapshot from an earlier campaign is available for reuse (`hpm_eq_truth`, `markov_half`, `t21_C1`, `T37Lattice` for RM-0, `T12Core` step algebra): `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/L-LEAN/` (STATUS.md:3-11, per `Lean/BRIEF.md` and `LEAN_READINESS.md`; I did not open the snapshot).

**Targets and order (Lean/BRIEF.md, updated 11-17/18; Theory's `LEAN_READINESS.md`, 2026-11-15):**
1. This week's targets (Level 1: deterministic cores, no `sorry`, axioms only `propext`, `Classical.choice`, `Quot.sound`): (1) Thm 3(a), the rate lower bound on every design (`W3-PSHARP:B`) on a shared score base; (2) the deterministic posterior summaries (SL0, `C-PACK:SL0`, with the pooling bound LT-d); (3) the distribution layer's deterministic core: domination transfer (the whole proof of Cor 9C and of track D #5′) and the Hellinger reduction (`W3-DIST:H`, Lemma D0). `Lean/BRIEF.md` "Starting material".
2. **December** (Level 2, one theorem at a time): **Thm 1 (true model)** and **Thm 9 (distribution)**; standard published facts (Gaussian/χ² tails, VC) enter as **named axioms**, one file per source, audited by Codex; cheap axioms discharged in Lean. Then (not now): the coded posterior's closed form; row 3.5's unbiasedness. `Lean/BRIEF.md` "December plan" and "Starting material".
3. **Out of scope:** probabilistic key lemmas of Thms 1 and 9; Level 3 (full probability formalisation); DLV-0 (a code audit, "not a Lean target"); full N1 unbiasedness (product-law plumbing); `LEAN_READINESS.md` rows 15-16, §3.
4. Readiness list (16 rows, Level-1 table; Level-2 skeletons S1 DIST-1, S2 W3-POST:Thm-1 items 1-5, S3 RM2-F⁺): `Theory_work/Dept/research/LEAN_READINESS.md` (note: dated 2026-11-15; it predates the pre-Lean corrections).
- **Fidelity and naming rules** (HQD:789-791; `Lean/BRIEF.md` "Fidelity", "Naming"): only a MATCH may be called a certificate of a paper theorem by its number; WEAKER gets its own lemma label; each Level-2 headline names its first paper-only dependency and every named axiom. A counterexample found during formalisation suspends the claim (SUSPECT), goes to HQ, and stops that target. For the manuscript: no Lean certificate may be claimed, and the planned list should read "Lean certificates of the key results (PLANNED; Thm 3(a), SL0 + LT-d, the Cor 9C / Hellinger core first; Thms 1 and 9 as Level-2 skeletons later)".

**The pre-Lean pass (the theory-side hardening that precedes Lean; owner GO 2026-11-18, HQD:775):**
- Brief: `Theory_work/Wave3/PRE_LEAN_PASS_BRIEF.md` (on main). Targets T1–T10: T1 Thm 3(a), T2 SL0 + LT-d, T3 domination transfer + Hellinger + D0 (the three shortlist items, Level 1); T4 Thm 1 + Thm 2SG and T5 Thm 9 (December, Level 2); T6 Thm 6 + Cor 6L + Cor-FAMC; T7 Thm 4 (omitted variables); T8 Thm 7 + Thm 5; T9 row 3.5 + Thm 10 + pooling (4.1); T10 Thm 8 (certified screening). Method: Astra/Sol adversarial reads at about 5 + 5 calls, Fable rulings and Lean-readiness notes.
- State on `origin/theory/PRE-LEAN` (head `ed9ff033`, 2026-11-23): Sol-7 read of NA_DROP v1.5 returned FAIL (8.6 / 8.8, not attested, not bound, nothing applied); item 7 Opus PURE 9.5 PASS; landing set updated (`Theory_work/Wave3/PRE_LEAN_PASS/LOG.md`, last entries). The correction batch landed on main on 11-18 (`97f9c8c3`, QDT:3). **Remaining, per QDT:4:** item 7 PURE (PRE-LEAN `ab9719a6`) → NA_DROP v1.6 (Sol-7 b‴-1, b‴-2) → Opus PURE → one tiny Sol confirm → MEAS-D / NA_DROP / T12 landing dry run → A re-pin (D5Pa v4, DLV-0 blind-triage fixes, T6-3, `CLAIMS_CARD.md:2`, INV-SCORE-BITS, stop() rows) → SUMMARY. All on hold.
- Lean-readiness notes from the three shortlisted targets (T1–T3 Fable cards) are in `Theory_work/Wave3/PRE_LEAN_PASS/BLUEPRINT_NOTES.md` (on `theory/PRE-LEAN`): e.g. T1 split into L1 (finite Ω odds), L2 (combinatorics), L3 (linear algebra); T2 SL0 as one master lemma ∀B, |π(B) − 1_B(a)| ≤ 1 − π(a); T3 domination transfer as finite sums. Level-1 targets have no paper-only dependency.
- Wording note from this pass for Writing: `Docs/Writing/from_theory/PRELEAN_WORDING_NOTE_2026-11-18.md` (8 lines): (1) `Docs/Writing/results/sections/sec3_selection.tex:432-433` overclaims "no condition on how Σ, β, σ² vary with n"; suggested wording "Σ, β and σ² may vary with n; no condition beyond (A1)–(A3) is placed on how they vary" (A2–A3 restrict them); (2) use the 11-18 sharpened Cor 6L ↔ Cor 9C sentence (`COR6L_9C_NOTE_2026-11-17.md`, correction note at its end). No theorem changes. Applies to Writing's own text, not to Lean.
- **Status:** PLANNED, not started. **Owner:** the Lean department (own manager; Theory Dept supplies readiness), HQ + owner gate. **Order:** as above; December for Level 2 (HQD:821 now says "spread to Feb/March").

## B4. `Theory_work/Dept/QUEUE.md`: the named open items

The queue (QDT, 161 lines) is largely a work queue as of 2026-11-15, with later riders. For the "planned results" list, the items that stand for **open mathematical content** (as opposed to editorial or housekeeping riders) are below, with the one-line meaning and the QDT pin. Items that are editorial, tooling, relabelling, hygiene or citation drift (the majority: the READER-ED residuals QDT:125, the core-drift / manifest-verify tooling item QDT:154, precedent notes, the NOTS move) are not listed as results.

| item | one line | pin | state |
|---|---|---|---|
| **Raw-scale search bridge** (READER B6.7) | needed for the **probability form** of "Cor 6L supplies Cor 9C's list-mass premise"; the registered link is by a deterministic/Cor-6L statement, the probability form is open. "Follow-up paper / open item; not a ticket" | QDT:116 (D121) | OPEN, no ticket |
| **RM2-R aggregated leak** | the aggregated leak term of the Gaussian-row version of the reported-model result (RM2-R) | QDT:117 | named open item (D) |
| **START MIS with a general μ** (W3-START2R-O1) | Corollary MIS (missed-signal inclusion) for a general deterministic μ ∉ span X_𝒞 without the (GR) condition | QDT:117; `Theory_work/Wave3/W3-START2-R/REPORT.md` §7 (l.89 area, "STATEMENT.md:253-254") | named open item |
| **Ex-Equi b < 3/8** | the equicorrelated example for b below 3/8, "if not done in W3-RM2-R (O4′)" | QDT:117 | named open item |
| **START2-O1 count (17 − s₀)** | an open count in the START2 statements; no further description in the queue | QDT:117 | named open item; I did not trace it |
| **T9 (START2)** | F1 with the exact Laplace exponent; F3 with G_n = o(log n), no growth premise; F4 at n^ι columns (adds three corollary rewrites to LC1) | `W3-START2-R/REPORT.md:91`, `PLAN.md:55-56`, `CHECKPOINT_1.md:52`; QDT:21, QDT:131 (the later T9 H1 line is about T12 adoption, a different "T9") | not adopted (CP1, 11-15, D40) |
| **T11 (START2)** | factorised OVL⁺; (N2⁺⁺) many leakers | same pins as T9 | not adopted |
| **T12 (SOP:TH110)** | owner adopted 2026-11-18; relabel to the PC carrier "precedent Prop-LB"; scoped to (i.a)–(i.c), (ii), (R3) via W3-AUDIT-AX:FR; (iii)/(iv) stay wave-1 PROVED-LOCKED, "not consumed by any presented result". The landing (MEAS-D / NA_DROP / T12) is pending | QDT:131 (T9 H1 line), QDT:141 ("T12 scoped relabel"), QDT:4 | adopted, landing pending |
| **Prop-LB** | appears only as the **precedent** for the T12 relabel and as a "Prop-LB check": `Theory_work/Dept/research/IMPL_PSHARPB_PROPLB_opus.md` (implementation check of PSHARP B / Prop-LB, not opened). **I found no open "Prop-LB check" item in the queue** | QDT:131; research file name | no open item found; ambiguous |
| **Lemma 1a′ check** | `W2 Lemma 1a′ registry label 'unchecked' is stale (check history R01, R02, C1, C3; X3 re-check)` (recorder note) and "L1a′ + TH128 acceptance: council acceptances free POST2:C (Thm 1′)". Theory's later card text says SOP:TH09 / SOP:TH128 are PROVED-CHECKED (main 6cd699dd), so the **acceptance part looks resolved**; the stale label and X3 re-check remain as editorial riders | QDT:69, QDT:86; CLAIMS_CARD abstract "Outcome: Form A" | acceptance resolved (card); label/re-check open, editorial |
| **Parallel-method pillar 4** | Theory's CLAIMS_CARD pillar 4, "The parallel method preserves it (mostly open)": **4.1** pooling over the coded 4 islands PROVED-CHECKED (LT-d, PoolZ); **4.2** "an output-identical parallel engine inherits every guarantee": empirical (24/24 production-hash, 10/10 supplementary byte-identical to serial) + "inheritance statement is a note in progress (W3-SCALE)", **no theorem, no registry row**; **4.3** many islands, island weighting, fixed N per island at p = 10^6: **OPEN**, "moved to the scaling paper" (island log-evidence spread grows with p; do not weight islands by Ẑ at p ≥ 5k). Parked as T-MERGE (convex pooling), EVAR / POOL (evidence variance), T-N, T-PART, T-STREAM, T-CAL; W3-SCALE O1(c) "looks closed by T12(ii)" | `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:93-101`; `Theory_work/Dept/NEXT_CAMPAIGN.md:5, 42, 52-53`; QDT:123 | OPEN / parked, scaling paper |
| **Row 3.6 / MEAS-D** | MEAS-D (calibration record, island records and Ẑ measurable in (data, seeds); "proved, not assumed") serves PoolZ, W3-SAMP D/LT/C/TR, Thm 10, DIST-C; lands with D5P and NA_DROP | QDT:134 | pre-Lean, in the landing set; on hold |
| **POST2-R1** | matching expectation lower bound E δ_n ≳ √(log n / n) on every design with a floor (Thm 1 two-sided); one unverified step | QDT:80 (row 1.1 card, D35) | post-freeze, kill budget |
| **POST2-O1 / O2 / O3** | O1: design-free sufficient condition for (OS) (makes "no eigenvalue condition off S₀" literally true); O2: lower c₁, MIS(i′) covers C-MIS's inclusion range; O3: E-floor⁺, a bounded ridge cost in place of the floor on S₀ (design-agnosticism; FIRST post-freeze, owner tie-break) | QDT:77-79 | post-freeze, kill budget |
| **SAMP-R1** | truth-free D; TV re-centring of C; hybrid TR bound; LT rate under NC_r | QDT:76 | post-freeze |
| **SCR-R1** | corollary of SCR-A + B2d with κ_n b_n²(n²−1) ≥ 4M_n²; drop "fixed" signals, exponential rate | QDT:81 | post-freeze |
| **Post-freeze DIST sharpness review** | (A4) via narrower (ND), 8(a) + 10 log(p ∨ n) rate with explicit A, 9 linear s₀ in (iii) | QDT:98 | post-freeze (consultant order) |
| **MISR riders / check X** | rider P1: contraction at log n/n without beta-min, Gaussian candidate rows (feeds pillar 2); check X: does Cor G b-plus E[1−π] = O(√(log n / n)) + design transfer cover Theorem 2's setting (candidate master for row 1.2) | QDT:109-110 | post-freeze |
| **Post-freeze (W3-AUDIT) T-D2, T-D3, T-D5′** | check X (1 d / kill 1.5 d) → sub-Gaussian Thm 2 (2 d / kill 3 d) → store-restricted clause (1–2 d / kill 3 d); #1 and #4 deferred | QDT:52-53 | **T-D5′ may have been recorded 11-17/18 (D5P v1.1 landed; QDT:3); the others not tracked here** |
| **Tier B line checks of W1-N1 steps** (island control flow, stopping time, B-0 / B-d, B-d MEAS; the freezing extension beyond fixed c) | when checked, R4 / DIST-C / OVL discharge | QDT:61 ("week of 11-23") | queued |

**What I could not establish.** (1) The queue has no one place that says which open item the owner counts as a "planned result"; the "Named open items" section (QDT:115-117) is the closest, titled "for the chapter's open-problems section". I would print those (raw-scale bridge, RM2-R aggregated leak, START MIS general μ, Ex-Equi b < 3/8, START2-O1 count) plus pillar 4.2/4.3 as the open-problems list, and treat POST2-R1 / O1–O3 as "possible strengthenings", all PLANNED or OPEN, none claimed. (2) T9/T11 appear in two senses in the repo (START2 optional items vs T9/T10 pre-Lean target labels). (3) The WRITING-worktree `QUEUE.md` and `origin/dept/theory`'s copy differ (the latter has 36 more lines, mostly the 11-17/18 riders and the 11-20 status block).

---

## Open questions for HQ (collected)

1. Trap theorem: which design family and which of our consistency results is "our consistency on the same design"; is "(c)" in HQD:849 a label in a plan not in the repo?
2. p = 10^7 "coverage": theory coverage (hypotheses at n = 200, p = 10^7) or claim coverage of the single shot?
3. Was the 5k anchor and the p ≤ 25 exact T8 level run? Is there a read-back? (SPEC l.112-113.)
4. Was the 10^5 T arm (SPEC l.115, ≈ 6,100 core-h) ever bought? I found no sign that it was; the manuscript should then say validation against T is at 10^4 only.
5. For the supplement table: the label for the evidence estimator (`log Ẑ_occ`) and the treatment of resampling (unchanged) are decided in code; please confirm the wording before the table is rewritten.
