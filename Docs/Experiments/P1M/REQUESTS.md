# REQUESTS to HQ — NOTS queries (read-only; nothing submitted)

Format: id, exact command(s), why. Please paste the output under each item, or into `requests/R<id>.txt`.

## R1 Node inventory: memory, cores, threads per core, features (commons)
```
sinfo -p commons -N -o "%N %c %m %f %G %T" | sort -u -k2,4 | head -80
scontrol show node bb2u24c1 | egrep "CPUTot|ThreadsPerCore|CoresPerSocket|Sockets|RealMemory|AvailableFeatures"
scontrol show node bc12u01c1 2>/dev/null | egrep "CPUTot|ThreadsPerCore|RealMemory|AvailableFeatures"
```
Why: the memory per node bounds exact linkage (OD-5: about 180k at 251 GB) and the number of 1M islands per node. Threads
per core decides how threaded tasks are billed (R2). We also need to know whether any node has ≥ 1 TB of memory.

## R2 Billing of a threaded task
```
sacct -j 2692690 -o JobID,AllocCPUS,ReqCPUS,CPUTimeRAW,ElapsedRaw,NodeList
scontrol show partition commons | egrep "MaxTime|DefMemPerCPU|MaxMemPerNode|OverSubscribe|TRES"
```
Why: P6 found AllocCPUS = 2 per single-thread task. For G8 we need to know whether `--cpus-per-task=16` bills 16 or 32,
and whether 2 threads per allocated core pair are allowed (this could halve core-h).

## R3 Partition limits
```
scontrol show partition commons scavenge | egrep "PartitionName|MaxTime|MaxNodes|PreemptMode|GraceTime"
sacctmgr show assoc user=fb31 format=Account,Partition,MaxJobs,MaxSubmit,MaxTRES,GrpTRES -p
```
Why: the 24 h limit and the 150-task cap drive checkpoint design (G9) and the 1M wall time.

## R4 Storage quotas
```
quota -s 2>/dev/null; df -h /scratch/fb31 /home/fb31/projects/BVS 2>/dev/null; du -sh /scratch/fb31 2>/dev/null
```
Why: stores, RB arrays and checkpoints at 1M (several GB per island and fit) go to /scratch; we must plan the cleanup.

## R5 Per-phase records of the B3 runs (already on NOTS; read-only) — ANSWERED by Engineering via ssh nots (NOTS_FACTS.md)
```
ls /scratch/fb31/w3scale/out/b3_p*/res | head; sacct -j 2698178,2698179,2698180 -o JobID,Elapsed,MaxRSS,NodeList -X
```
Why: the per-step µs at 10k/20k under revision D, the I and T per tier, and the peak RSS per phase feed the cost model. If
they are already in `origin/theory/W3-SCALE` results, point me to the file instead.

Nothing in this file asks for a submission.

## R6 B3 calibration and island records (read-only; from the Fable review §7; added 2026-11-15)
Files: `/scratch/fb31/w3scale/out/b3_p*/res/census_p*.rds` (exact names as on disk). In R on a login node, for each file:
```
x <- readRDS(f); str(x$calibration$converged); str(x$calibration$triggers); str(x$calibration$diag_sd)
lapply(x$runs, function(r) r$island_best)           # per-island best F for each N
```
Also, if present, per island: the stage table's cumulative log increment (`cum_log_Z`, or `log_increment` cumsum) by stage,
and the top-store F values (for log Σ e^F against log Ẑ_r).

Why:
1. Does `grid_unconverged` fire at p ≥ 5k? If so, escalation survives even with E2 disabled (OD-2).
2. `islands_same_best = FALSE` in three rows of `b3_census.tsv`, while CP2 §3 says every island found the same best model:
   which is true?
3. At which stage the log Ẑ_r dispersion arises (R4 of the review).

### R6 — ANSWER (HQ, 2026-11-15 ~20:00 CT; read-only from `/scratch/fb31/w3scale/out/b3_p*/res/census_p*.rds`, R 4.5.2)
Calibration:

| p | converged | rebuilds (ℓ) | E2 | grid_unconverged | other triggers | diag_sd range |
|---|---|---|---|---|---|---|
| 2k | TRUE | 8 (12) | F | F | none | 0.09–0.36 |
| 5k | TRUE | 13 (13) | T | F | none | 0.49–3.86 |
| 10k | FALSE | 14 (14) | T | T | none | 0.47–4.43 |
| 20k | FALSE | 15 (15) | T | T | none | 0.16–1.50 |

Runs (islands done/requested; sd log Ẑ_r; R_eff; HPM = truth):

| p | N | islands | sd log Ẑ_r | R_eff | HPM = truth |
|---|---|---|---|---|---|
| 2k | 2,500 | 16/16 | 0.086 | 15.9 | T |
| 2k | 10,000 | 16/16 | 0.029 | 16.0 | T |
| 5k | 2,500 | 16/16 | 0.755 | 8.9 | T |
| 5k | 10,000 | 14/16, resource_limit | 1.348 | 1.6 | T |
| 10k | 2,500 | 6/16, resource_limit | 1.152 | 2.0 | T |
| 20k | 2,500 | 11/12, resource_limit | 0.954 | 4.2 | T |

Findings:
1. `grid_unconverged` fires at p ≥ 10k (not at 5k, which converged at its 13th = last allowed rebuild); E2 fires from 5k.
   Under the coded rule, escalation is certain at p ≥ 5k in these runs. OD-2(c) is confirmed as necessary.
2. island_best: every *completed* island has the same best F (−110.17 / −114.87 / −150.54 / −130.02 at 2k / 5k / 10k / 20k).
   −Inf entries = islands that never ran; −245.07 at 20k = the one unfinished island. CP2 §3 is right for completed
   islands; the `islands_same_best` flag in `b3_census_table.R` should exclude unfinished islands (for W3-SCALE).
3. The census records have no stage table and no top-store F values. The stage at which the dispersion arises needs a
   re-run with stage-level output (planned in rung A, see REVIEW_disposition R4.1).
4. R_eff collapses from ≈ 16 (2k) to 1.6–4.2 at p ≥ 5k: evidence-weight degeneracy, to be planned around in pooling.

---
# THEORY interface (Engineering → SMC - Theory Department). Engineering writes only here; Theory writes only in
# `Theory_work/Dept/ENG_INTERFACE.md`. Canonical premise table: ENGINEERING_SPEC.md §4.2.

## THEORY-1 T-PART: the exact rules (current, and proposed OD-5(c))
**Current exact rule (v3.1, code at daa08a3; spec text `Theory_work/State_of_Project/sections/02_method.tex:187-222`):**
- B = min(⌊√n⌋, ⌊√p⌋, 16) (`v3_preprocess.R:22`). Distance d_jl = 1 − |r_jl|, with r from the standardised Gram
  (`cpp/v3_blocks.h:10-17`).
- Complete linkage (`cpp/v3_blocks.h:46-108`):
  - merge the pair with the smallest complete-linkage distance; among exactly equal distances, the pair whose union has
    the lexicographically smallest sorted index list (R13, `:20-30`, `:66-70`);
  - the left child is the child with the smaller minimum index (`:87-89`);
  - Lance–Williams max update (`:94-98`).
- Top-down cut and packing (`cpp/v3_blocks.h:124-145`):
  - from the root, split every node with more than B members into its two children (left first), until each retained
    cluster has ≤ B members;
  - next-fit packing of whole clusters, **in dendrogram leaf order**, into blocks of ≤ B members;
  - members sorted within each block.
- Called at `cpp/v3_core.cpp:161, 279`.

**Proposed rule OD-5(c) (large-p mode).** τ_n = r_n = √(2 log p / n), with p = retained columns.
1. Edge set E = {(j, l) : |r_jl| ≥ τ_n}, computed by streamed tiles. **Open sub-choice:** ≥ as written, or > as in the
   neighbour graph (`v3_blocks.h:155-163`). Theory's preference wins.
2. Complete linkage restricted to merges at height ≤ 1 − τ_n: two clusters may merge only if every cross pair is in E.
   Same merge order, tie rule R13 and left-child rule as above. This gives a forest whose merges equal the exact
   dendrogram's merges of height ≤ 1 − τ_n (complete linkage is monotone; gate T11 tests the equality at p ≤ 20k).
3. Each forest root is a cluster. A cluster with > B members is split by the same top-down cut on its own subtree.
4. Next-fit packing of the clusters ordered by **minimum member index** (not dendrogram leaf order; the exact leaf order
   above 1 − τ_n does not exist here), into blocks of ≤ B; members sorted.

What differs from the exact rule: the merges above 1 − τ_n (absent) and the packing order. For noise-level columns this
means index-order packing of singletons and small clusters.

**Every consumer of the partition** (all must be covered by T-PART, not only START):
| consumer | code | used by (theory) |
|---|---|---|
| block tables log r_b(U) (every subset of every block scored) | `cpp/v3_start.h:76-98`; `v3_core.cpp:181, 283` | START/START2 (π₀) |
| π₀: size profiles, convolutions, normaliser log Z̄₀, exact sampler | `cpp/v3_start.h:101-157, 158-` (`draw_pi0`) | START/START2; SAMP D (draw discovery: P(miss) = (1 − π₀(S₀))^{D}) |
| composite log γ₀(S) and the discrepancy d(S) = log BF(S) − Σ_b log r_b | `cpp/v3_start.h:54-69`; `v3_engine.h:95` | the SMC bridge path γ_φ = γ₀·e^{φ d}: N1, LT♯, C (concentrated bridge), TR |
| initial particles and the independence move (exact π₀ draws) | `v3_engine.h:108, 182-193` | N1, D, C |
| leader store γ₀ (order by log γ₀) → calibration set V → grid | `v3_ledger.h:72-78`; `v3_core.cpp:703-716` | frozen-𝒞 results (no premise; T-CAL) |
| start mode S̃₀ (argmax π₀; tie-DP) → LS0 centre and cap ℓ + \|S̃₀\| | `cpp/v3_start.h:271-301`; `v3_core.cpp:469` | RM-0/RM/RM2 (LS0 from the start mode; E4), GEN/GROW (block-level centre certificate), MR1/MR2 |
| table models offered to the ledger (HPM, stores) | `v3_core.cpp:372-386` | SL2 / DIST-C (store contents) |
| (V) visibility "≤ 15 conditioning variables" | B − 1 | RM/RM2 (V), START |
| `cut_group` report (uncapped ≥ threshold graph) | `v3_core.cpp:794-816` | reporting only |

The neighbour graph (`v3_blocks.h:149-170`) does **not** depend on the partition.

## THEORY-2 Dates Engineering needs each answer by
| ticket | needed for | soft date | hard date |
|---|---|---|---|
| T-PART | rule frozen in WP2 setup code (the code can take τ_n, ≥/>, packing order as parameters, so coding is not blocked); production config frozen before gate T11 / G-A | **11-25** (verdict on the rule + sub-choices) | 12-04 (before G-A 12-07) |
| T-N | owner decision OD-1 (HQ batch after EXP-CP1) | **11-20** | 11-23 (WP3 start) |
| T-CAL | owner decision OD-2 (same batch); I_max is chosen from the rung-A three-arm test, so a preliminary "which delivered results read E2 / tiers / grid convergence" is what is needed first | **11-20** preliminary | 12-04 full |
| T-STREAM | WP3 fixes the counter-based generator and address map (≈ 11-27); gate T4 law check at G-A | 11-27 (generator acceptable as EX-S / IND-T?) | 12-04 |
| T-MERGE | WP4 merge outputs (all PIPs computed regardless, so code is not blocked); claims wording before G-C | 11-30 | 12-18 (before the 1M pilot, G-C ≈ 12-21) |

## THEORY-3 OD-4 and the evidence base for T-MERGE
- Working assumption for WP4 (not yet owner-approved): equal-weight `pip_primary` is primary. The merge computes and
  returns PIP_eq, PIP_Z (with R_eff, max W_r) and PIP_𝒯 (store-renormalised, OD-15) in every case, so "which is primary" is a label switch, not a code dependency.
- Evidence (complete as of 11-15). These are the only many-island data; there are no stage-level records yet:
  - B3: REQUESTS R6 answer (σ̂ and R_eff by p and N; every completed island found the same best model);
  - W3-SCALE DESIGN_v1 §4.4 (25 saved fits with R = 4; diagnostic-island σ̂; the P6 E2 table);
  - CP2 §3.
- Rung A adds the stage-level re-run at 5k / 10k (REVIEW_disposition R4.1) and the 64-island census (Full tier).

## THEORY-4 Registry wording (HQ-confirmed decisions D-3, D-8) and one consumer check (D-7). Staged by SMC-Theory; HQ approves the recording run.
**Entry A: D-3, cost column (kind: implementation / reporting rule; no change to any estimate).**
> In runs of the large-p engine (v4, production and compat modes), the published cost measure is `score_counts$logical`:
> the number of logical score events per phase and mechanism, defined exactly as in v3.1 (`cpp/v3_ledger.h:74`; every
> evaluated or held configuration counts once, cache or not). `score_counts$fresh` and cache statistics are
> implementation-dependent. They are reported only with a declared fixed cache capacity, labelled "implementation
> counter", and never enter a published table or theorem check. Published v3.1 tables (EVIDENCE §8, RERUN_SPEC cost
> column, `evidence_h2.py:98-105, 139-141`) keep their values and their definition.
> Scope: W3-SCALE ruling O17, case (a) by redefinition (option B2-3).

**Entry B: D-8, new returned outputs (kind: implementation; additions only; every existing output unchanged).**
Notation: 𝒯 = the merged `top_store`, i.e. the 40p + 1 best-scored distinct models offered to the final ledger(s),
merged over R′ islands as the top-c of the union (O10). F(S) = log ϖ(S) + log m(S), exact scores (CC2).
> (i) `pip_store[j]` = Σ_{S∈𝒯, j∈S} e^{F(S)} / Σ_{S∈𝒯} e^{F(S)}: the store-renormalised PIP. It needs no island weights
>     and is the j-th marginal of Π̂^𝒯 (W3-DIST DIST-C(i)).
> (ii) `log_Z_store` = log Σ_{S∈𝒯} e^{F(S)}. Under EX-A, log_Z_store ≤ log Z deterministically (F is the log of the
>     unnormalised posterior mass of S, and 𝒯 ⊆ Ω).
> (iii) `law.bin`: the store-BMA law Π̂^𝒯, truncated at relative weight 10⁻¹² (the dropped relative mass is reported).
>     Per model it stores S, F(S) and the conjugate posterior parameters of (θ_S, v) on the standardised scale, plus the
>     column standardisation constants. It is the object of DIST-C(i). Draws from it, if requested, use streams disjoint
>     from the engine's.
> (iv) Terminal particle supports (after the last measured round), archived as a **diagnostic**, explicitly not an
>     estimate. No theorem covers a particle-based law.

**Check C: D-7, leader stores.** Please confirm that no theorem, claim or check consumes the **final-run** leader stores
`leaders_gamma0` / `leaders_gamma1` (`v3_run.R:210`; built in `cpp/v3_ledger.h:72-78`).
- Engineering's search:
  - 0 hits for "leader" in `Theory_work/INFRA/registry/claims.tsv`;
  - the only script reference is the study schema listing the field (`Scripts/SMC_BVS/study/SCHEMA.md:146, 148`);
  - in calibration they feed the set V for the grid (`cpp/v3_core.cpp:703-716`), and that use is kept.
- Proposed: final islands do not build them, and the fit does not return them. This is a change to the output list; the
  registry entry follows your confirmation.

## THEORY-5 Pins for Entry B(ii) and for Check C (answers to Theory's caveats, 11-15)
**B(ii): log_Z_store ≤ log Z. File:line chain, core at daa08a3.**
1. Score of a model: `cpp/v3_engine.h:97`, `q.F = D.logprior[k] + lm`, with lm = log m(S) and
   logprior[k] = log w(k) − log W_K = log ϖ(S) (`cpp/v3_score.h:62-70`).
   This F is what the ledger stores: `led->event(q.S, q.F, …)` (`v3_engine.h:99`) → `offer_stores(S, F, …)`
   (`cpp/v3_ledger.h:89, 112`). For inherited and table models: `cpp/v3_core.cpp:426-427` (`D.logprior[S.size()] + lm`).
2. The target of the bridge at φ = 1: log γ_φ(S) = lg0 + φ d (`v3_engine.h:14`), lg0 = logprior + comp, d = (lm − logm0) − comp
   (`:97`). So at φ = 1, log γ₁(S) = logprior[k] + lm − logm0 = F(S) − log m(∅).
3. The island estimate: it starts at `logZ = D.logm0 + st.logZbar0` (`v3_engine.h:299`), where Z̄₀ = Σ_S γ₀(S), the exact
   normaliser of the start law (`cpp/v3_start.h:131-135`). It then adds the stage increments (`:319-322`). So Ẑ_r estimates
   m(∅)·Σ_S γ₁(S) = Σ_{S∈Ω} e^{F(S)} =: Z. Pooled: `v3_run.R:154`.
4. Ω = {|S| ≤ K}: the prior is capped (`v3_score.h:62-70`), and Gibbs blocks |S| > K (`v3_engine.h:116-119`).

Hence Z = Σ_{S∈Ω} e^{F(S)} with the same F as in the store. For any 𝒯 ⊆ Ω,
log Σ_{S∈𝒯} e^{F(S)} ≤ log Z, under EX-A (the F values are floating-point evaluations of the exact scores).

**Check C, inherited stores (02_method.tex:357-359).** Correct. The frozen calibration record carries its top store and
both leader stores. The final run *offers their models* to its own ledger with provenance "inherited"
(`cpp/v3_core.cpp:418-428`: score, then `offer_stores` to the top store, both leader stores and the HPM). Under D-7 that
offering stays: in the large-p engine the inherited models are offered once, at the merge, to the top store and the HPM
(ENGINEERING_SPEC §4.2, "class B for stores and HPM"). What D-7 drops is only the *final-run* leader stores as a data
structure and as a returned field (`v3_run.R:210`). The question for Theory is therefore whether any result reads the
returned `leaders_gamma0/1` of the final run. The inherited models' effect on the top store and the HPM is unchanged.
