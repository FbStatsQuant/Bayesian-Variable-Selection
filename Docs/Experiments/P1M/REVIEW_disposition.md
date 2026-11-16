# REVIEW_disposition — Fable 5.2 independent review of the P1M plan (2026-11-15)

Review: `REVIEW_fable.md` + `SPEC_SKELETON_fable.md`. Brief: `briefs/BRIEF_fable_review.md`. Disposition by the
Engineering manager (Opus 5.5).

Spot-checks of the review's factual claims before dispositioning (all confirmed):
- the seven triggers, incl. `grid_unconverged` and `local_limit` (`v3_calib.R:60-61, 115-118, 154`);
- B3 rebuilds 13 / 14 / 15 = ℓ at 5k / 10k / 20k (`b3_census.tsv`);
- leader stores 2 × 20p (`v3_ledger.h:72-78`, `std::set`);
- `islands_same_best = FALSE` in the three `resource_limit` rows of `b3_census.tsv`;
- AR(0.6) lag-1 correlation 0.6 > r_n = 0.372 (n = 200, p = 10⁶).

Verdicts: **ADOPT**, **ADOPT-MOD** (adopted with a change, stated), **OWNER** (needs a decision; moved to
`OWNER_DECISIONS.md`), **DEFER** (with the trigger to revisit), **REJECT** (with reason). No item was rejected outright.

## Ranked opportunities

| id | item | verdict | action / where |
|---|---|---|---|
| R1a | Escalation hole: OD-2(b) missed `grid_unconverged` and `local_limit`; the rebuild loop hit ℓ in 3 of 3 B3 runs at p ≥ 5k | **ADOPT** (R6: `grid_unconverged` fired at 10k and 20k; 5k converged on its last allowed rebuild; E2 fired at 5k–20k, so the coded rule escalates at every p ≥ 5k in B3) | OD-2 rewritten. Plan §0, risk R2 corrected. REQUESTS R6 (read `calibration$converged`, `triggers` from the B3 records) |
| R1b | Bounded calibration (I_max rebuilds, no escalation except construction failure), class [Δ𝒞] | **ADOPT-MOD → OWNER (OD-2)** | Recommended. I_max fixed **before** rung A from a three-arm comparison at 10⁴ (coded-but-no-escalation / I_max = 3 / pilot schedule only; 5 datasets, ≈ 300 core-h, added to A2). Default for the spec: I_max = 3 |
| R1c | Hidden serial work per rebuild at 1M (V re-scored, grid sums over V) | **ADOPT** | spec §7 row "calibration serial part"; T5 measures it at 10⁵ |
| R1d | Cost model: I = ℓ, 0.5–0.8 island-eq per rebuild | **ADOPT** | plan §6.1 and spec §7 use I = ℓ for the coded rule |
| R2a | Bandwidth floor of the Gram-free direct step (1.6 KB of X per step; ≈ 168 TB per 1M island) | **ADOPT** | plan risk R5 rewritten; T5 bandwidth gate added before G-B |
| R2b | Position-addressed uniforms (counter-based) | **ADOPT** | Replaces OD-8(b)'s "per-particle streams" as the production stream design (same class [OP-law]). With it, any execution order gives the same bits (T3) |
| R2c | Label-major round kernel (one pass over X serves a particle group) | **ADOPT-MOD → OWNER (OD-16)** | A 2-agent-day Owls prototype at 10⁵ decides it. Because of R2b it is a drop-in kernel behind the same output (T3), so the engine is built particle-major first and label-major replaces the kernel if the prototype wins. The reviewer's 5–15× saving is a **guess** and is not used in any budget until measured |
| R2d | Fallback items: no global cache, prefetch along the drawn round order, Gram-row cache for long-lived members | **ADOPT** | spec §2/§3; the cache removal needs OD-3 = B2-3 |
| R2e | Correction: bordered update is [OP-bit] only as prefix reuse in sorted order; rank-one updates are class A | **ADOPT** | ENGINEERING_STRATEGY §3 superseded by spec §1 interface `flip_scores` |
| R2f | Correction: RB sums need a declared reduction order (class A against compat) | **ADOPT** | spec §3 rule 3, §4.2 |
| R3 | Partition: threshold components fail on AR(0.6) (one component of size p); use complete linkage **truncated at height 1 − τ_n** on the sparse graph; packing by minimum index | **ADOPT → OWNER (OD-5) + T-PART** | OD-5 and plan G3 rewritten; T11 gate (truncated = exact dendrogram cut below 1 − τ_n, p ≤ 20k). The T-PART question to SMC-Theory uses this rule's wording, including the new packing order |
| R4.1 | Zero-cost diagnosis of the evidence variance: per-stage variance of cumulative log increments; log Z_𝒯 = log Σ_𝒯 e^F against log Ẑ_r | **ADOPT-MOD** | R6 answer: the B3 census records hold neither stage tables nor store F values, so it is not zero-cost. Moved to rung A: 2 datasets at 5k and 10k (16 islands, N = 2,500, stage-level records + top store) on the compat/revision-D engine, ≈ 60 core-h, before G-B |
| R4.2 | Report the evidence as a sandwich (log Z_𝒯 ≤ log Z; log Ẑ, σ̂; `log_Z_lower95`) | **ADOPT** | plan §3.4 |
| R4.3 | PIP_𝒯 (store-renormalised, weight-free) as a third reported PIP | **ADOPT → OWNER (OD-15)** | It is a new returned field, so the owner decides (OD-15). Computed by `eval` in any case |
| R4.4 | Keep equal-weight primary; do not use R′ = 8 if PIP_Z is reported | **ADOPT** | OD-4 kept; OD-9 lever R′ = 8 withdrawn |
| R4.5 | `islands_same_best = FALSE` in three B3 rows vs CP2 §3 "every island found the same best" | **RESOLVED (R6)** | every completed island has the same best F; the FALSE comes from islands that never ran or did not finish. CP2 §3 stands. The flag must exclude unfinished islands (W3-SCALE `b3_census_table.R`; spec: merge statuses never pool unfinished islands) |
| R5.1 | Ablations per dataset: start mode / + LS0 / pilot + local / full | **ADOPT** | plan §3.1; under 100 core-h total |
| R5.2 | Screening-adversarial cell (adjacent AR truths of opposite sign) at every rung incl. 1M | **ADOPT → OWNER (OD-14)** | ADJ-OPP cell defined in plan §2.2 |
| R5.3 | Weak-signal cell at 1M | **ADOPT → OWNER (OD-14)** | |
| R5.4 | C2 at 1M worded as feasibility (3/3 gives a 95% lower bound of 0.37) | **ADOPT** | plan §1 C2 reworded |
| R5.5 | Second seed on the same dataset | **ADOPT** | 10 datasets at 10⁴, 1 at 10⁵, 1 at 10⁶ (if budget) |
| R5.6 | Occupancy check (terminal particles vs exact store weights) | **ADOPT-MOD** | needs terminal supports (OD-15); diagnostic only |
| R5.7 | Null control (y ⊥ X) at 10⁴, 10⁵ | **ADOPT** | plan §2.3 |
| R5.8 | Equal-budget model-space MCMC | **ADOPT-MOD** | at 10⁴; at 10⁵ **DEFER** until the rung-A cost is measured |
| R5.9 | Exact reference at p ≤ 25 (SMC branch forced against enumeration) for every law change | **ADOPT** | gate T8 |
| R5.10 | Freeze configuration, evaluator and competitors before rung C; report every submitted fit | **ADOPT** | plan gate G-C |
| R5.11 | SIS (d = 10⁴) → our own method as a competitor | **ADOPT** | plan §4 |
| R6 | Missing memory/I/O items: leader stores; table ingestion per ledger; inherited models; `start_mode` recursion depth J ≈ 10⁵; tie-aware DP cost; R standardisation arithmetic; capacities ∝ p; `--mem` 32 GB | **ADOPT** (leader stores in final islands → **OWNER OD-13**; capacities → **OWNER OD-13**) | plan G7, G11 rows extended; spec §2; OD note 2 corrected to 32 GB |
| R7 | Bill by socket (request the saturating CPU count); A1 is an equal-particle comparison (40,000 final particles either way); scavenge with checkpoints | **ADOPT** (scavenge **DEFER**: needs HQ on billing and preemption, after T6) | spec §3 request shape |

## Screening (review §2) — ADOPT
The claim stays screening-free. No law-changing shortcuts (v0 P9). A cell where screening loses is included (R5.2).

## Draws / predictive option (review §3) — ADOPT-MOD → OWNER (OD-15)
Recommendation forwarded unchanged:
- terminal supports always archived as a labelled diagnostic;
- the store-BMA file (`law.bin`) is the "distribution output", since it is exactly Π̂^𝒯 of DIST-C(i);
- particle-based laws stay out of headline claims until SMC-Theory supplies a terminal-population statement.

New returned fields change the method's output list, so they need the owner and a registry entry.

## Risks and blind spots (review §4)

| # | item | verdict |
|---|---|---|
| 1–3 | escalation, bandwidth, partition | ADOPT (above) |
| 4 | 1M design too friendly | ADOPT (R5.2, R5.3; OD-14) |
| 5 | five law changes vs "output-identical inherits every theorem" | **ADOPT**. Premise table in spec §4.2. Tickets proposed to SMC-Theory: T-N, T-PART (existing), **T-STREAM** (O5/O18 for the counter generator), **T-CAL** (bounded calibration), **T-MERGE** (O1, O10, O19–O21). Owner framing question → OD-12 |
| 6 | n = 400 at 1M: tables ≈ 2·10⁹ codes (≈ 16 GB `logr`) | ADOPT: n = 400 at 1M stays Full-tier only and needs a table-memory check first |
| 7 | PIP calibration thin | ADOPT-MOD: weak arm at 10⁴ raised to 20 reps (cheap); exact-PIP agreement at small p via T8 |
| 8 | Timeline across Thanksgiving | ADOPT: **Minimal tier is the stated expectation for December** |
| 9 | Pinned libm vs v3.1 reference records | ADOPT: rebuild the reference against the pinned routines (≈ 20 task-h), compare once |
| 10 | AR generator undefined across chunks | ADOPT: one sequential recursion over columns |

## "Wrong in the plan" table (review §5)
All 10 points are accepted. The corrections are in plan v0.2, OD-2, OD-5, OD note 2 and ENGINEERING_SPEC v1.
ENGINEERING_STRATEGY v0.1 is superseded by ENGINEERING_SPEC v1.

## Owner questions (review §6) → OWNER_DECISIONS.md
Q1 → OD-2 (rewritten) · Q2 → OD-12 · Q3, Q8 → OD-13 · Q4 → OD-14 · Q5 → OD-15 · Q6 → OD-16 · Q7 → OD-6 (amended).

## Free requests (review §7) → REQUESTS.md R6 (for HQ, read-only)
