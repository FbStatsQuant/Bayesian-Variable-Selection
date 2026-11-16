# Next campaign — parallel-SMC theory (Theory Department proposal to HQ; DRAFT v0, 2026-11-15)

Final version due Thu 11-19, after PSMC-S0 CP1 (T-N, T-CAL audits). Sources: `research/PSMC_DIGEST.md` (pinned facts),
`ENG_INTERFACE.md` (premise tickets and Engineering's dates), `Docs/Experiments/P1M/ENGINEERING_SPEC.md` §4.2,
`OWNER_DECISIONS.md` OD-1/2/4/5/8/9/12, `REQUESTS.md` R6 + THEORY-1..3, W3-SCALE `DESIGN_v1.md` obligations O1–O21.

## 1. Goal in one paragraph
The p = 1M run uses a parallel engine that differs from v3.1 **in law** in five places (OD-12): fixed N per island,
R′ = 16 process islands with a merge, position-addressed counter streams, a truncated-linkage partition and a
bounded calibration. Only the compat mode is bit-identical. The paper's claim is "the same theorems, with each premise
re-checked change by change". Phase A delivers exactly that, in time for Engineering's gates. Phase B explains and
handles the evidence-variance problem: σ̂(log Ẑ_r) ≈ 0.09 at p = 2k but 0.76–1.15 at p = 5k–20k (N = 2,500),
not cured by 4N, with R_eff falling from ≈ 16 to 1.6–4.2. That is research for the scaling paper.

## 2. Phase A — premise tickets (Tier B; the "short note" for 1M)
| ticket | content | consumes | tier | needed by (Eng soft / hard) | order |
|---|---|---|---|---|---|
| PSMC-S0 (running) | audits: T-N, T-CAL prelim (CP1 Thu 11-19); T-PART (CP2 Tue 11-24) | registry, code | scoping | 11-20 / 11-25 | now |
| **T-N** | in-law transfer (digest P1): every given-𝒞 result holds with N_e → N, 4 → R′; restate TH01(e)(f)(i), TH06, TH08 for general (N, R′); confirm RM-0, LT♯, TR, D unchanged | T12 §2, N1, W3-SAMP, RM-0(b) | B | audit 11-20 / 11-23; proofs by 11-27 | Mon 11-23 |
| **T-CAL** | bounded calibration (I_max, no escalation except construction failure): frozen-𝒞 results untouched; C-DLV and card items reading E2 / tiers / grid convergence restated | C-DLV, LT♯, TR, card | B | prelim 11-20 / full 12-04 | with T-N (one lead) |
| **T-STREAM** | counter-based position-addressed generator as an ideal stream (EX-S, O5); independence on the enlarged address map (IND-T, O18); Prop W "deterministic for any thread count" | EX-S, IND-T, Prop W | B (audit-heavy) | 11-27 / 12-04 | Mon 11-23 |
| **T-PART** | the theorems hold for the OD-5(c) partition, or the bridge needed, over Engineering's full consumer list (π₀, γ₀/d(S) → bridge path, start mode → LS0, stores, (V) via B − 1); ≥ vs > | START, START2, RM2, N1/LT♯/C/TR, SAMP D | B (A if a new key lemma appears) | 11-25 / 12-04 | after PSMC-S0 CP2 (11-24) |
| **T-MERGE** | pooling under evidence-weight degeneracy: (P2) any convex pooling rule inherits PIP/MPM consistency from TR / Theorem C with no condition on Ẑ, so OD-4 becomes a theorem; (P5) Ẑ-weighted merge LLN/CLT and R_eff/R′ → 1/E[W²]; (P6) union HPM ⪰ HPM(4), discovery with R′ islands; O19 lower bound, O20 flags at R′ ≠ 4, O21 card items on the merged HPM | TR, C, LT♯(d), T12(ii), D(ii), Lemma S | B | 11-30 / 12-18 | after T-N and T-STREAM (~11-27) |

Dependencies: T-MERGE needs T-N (general R′) and T-STREAM (IND-T for R′ streams). T-PART needs PSMC-S0 Part 2.
T-CAL and T-N share the audit and one lead.

## 3. Phase B — the evidence-variance problem (scaling paper)
| ticket | content | tier | when |
|---|---|---|---|
| **EVAR** | (i) an upper bound on P(\|log Ẑ_r − log Z\| > u \| 𝒞) that does not depend on N, T or p, and vanishes when start or posterior concentrate (restatement from C-iii); (ii) an honest limit: an abstract (π, π₀, grid) construction, design-agnostic, p ≤ n^A, where posterior mass ≥ c is unreached by fixed-N islands, so σ(log Ẑ_r) is unbounded and R_eff/R′ → 0 at fixed N and calibration | A for (ii) (new key lemma; a Fable lead needs owner permission via HQ: reason + size, per the 11-15 memo) | from ~11-30 |
| **POOL** | robust evidence pooling: trimmed or tempered weights declared before the final streams, consistency as R′ → ∞ using only E[W_r \| 𝒞] = 1, bias and MSE bounds; never worse than equal weights in the concentrated regime (with P2) | B | after EVAR (i) |
| numerics | coordinate with Engineering's rung A stage-level re-run (5k/10k) and the 64-island census (Full tier): what to record (mode occupancy per stage) so EVAR (ii) can be tested | — | spec to Engineering by 11-30 |

Risks: EVAR (ii) may need a bottleneck or mixing hypothesis that reads as design-specific (keep it at the level of
(π, π₀)); POOL's rule must be declared before the final streams (`02_method.tex:389`), and its rate needs a tail
condition that EVAR (ii) may show fails.

## 4. Stretch (after W3-DIST closes)
Approximate sparsity and exponential p for W3-DIST.

## 5. Resources and schedule (3 leads from Thu 11-19)
- Week of 11-23: lead 1 T-N + T-CAL; lead 2 T-STREAM; lead 3 PSMC-S0 Part 2 → T-PART.
- Week of 11-30: T-MERGE (as T-N/T-STREAM land); EVAR (Tier A; Fable only with owner permission, else Opus with a kill budget); POOL after EVAR (i).
- Codex (NORMAL): Tier B ≈ 4 reviews × 5 tickets ≈ 20; EVAR Tier A ≈ 11. DIST keeps priority.

## 6. Found while scoping (for HQ)
- **Pooling in the method text vs the code.** `State_of_Project/sections/02_method.tex:444-451` says v3.1 made the
  Ẑ-weighted PIP primary. The code pools with equal weights (`Scripts/SMC_BVS/core/v3_run.R:162`
  `pip_primary <- rowMeans(P)`; log Ẑ is the plain mean of Ẑ_r, `:154`). Theory (LT♯, TR) is proved for the coded
  equal-weight RB PIP. The chapter and paper must follow the code.
- W3-SCALE O1(c) ("N1 does not cover the shipped Rao–Blackwellised PIP") looks closed by T12(ii) (digest §4;
  to verify in T-MERGE).
