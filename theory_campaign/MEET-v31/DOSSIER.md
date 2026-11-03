# Methodology: final meeting on v3.1 (dossier, frozen 2026-11-03)

Prepared by HQ ("SMC-BVS New HQ" thread). The chair and the seats read this file first. It is frozen: later evidence is added only as files in `theory_campaign/MEET-v31/evidence/`, each one dated.

## 0. Purpose

Decide the method that paper 1 ships. When the meeting ends, every open question about the method is either closed by evidence or a proof check, or recorded as an **inherent limitation** (a limit of the SMC structure, the prior, or the problem itself, stated in the paper). **No open question may remain**: theory proving starts only after this meeting. HQ approves the final version and brings it to Felipe. The chair does not vote.

## 1. Ground rules (Felipe's words, 2026-11-03; binding on every seat)

1. **Baseline and burden of proof.** "About the method we go with, I don't conceive a strong reason for which it should be fairly different to the one run here [the v3 study]. It can surely be refined into a more parallel strategy, but the composite likelihood, SMC structure and HPM rule seems to be quite accurate and a very fertile terrain for a lot of important theorems. In principle I'm open to anything as long as it is highly parallel and mathematically proven, but unless I'm blind I don't see a reason for which it should deviate fundamentally from this approach. So again, everything is on the table and can be changed, but I'd need irrefutable reasons, given the accuracy, the scalability potential given the SMC nature and the smooth theoretical flow HPM brings."
2. **Real issues only.** "Changes are not random proposal of any agents, it must address real issues like theorems breaking down or parallel computing orientation."
3. **Provable or nothing.** "We can add / remove any selection rule. Current version uses HPM but anything is on the table, provided it works well and its presence do not make theoretical work harder. We need strategies that work computing wise but also results that can be provable, a fancy heuristic and hypothetically gives me perfect accuracy but cannot be formally proved is as good as nothing to me."
4. **What parallel means.** "Parallel computing is the final goal but it is not the main driver, the final methodology must be parallelizable enough so you could scale it to p values that you could not otherwise in sequential MCMC." "We are not trying to parallelize over variables." The parallel axis is particles and islands: stack CPUs/GPUs, compute a large total number of particles, derive an accurate BVS from them.
5. **Local-to-global.** "Local to global is not strictly mandatory but it is foundational for scalability and parallel computing, I'm open to dropping it but I need a very serious, irrefutable argument."
6. **Objectives, in order:** (1) accuracy in recovering the true posterior; (2) parallel scalability; (3) BVS selection accuracy. It must work well under correlated designs, unlike Song & Liang (2015) split-and-merge.
7. **Theory standard (context for item 7 of the agenda).** The theory must reach every goal of the Local-to-Global proposal (`theory_campaign/inputs/Local_to_Global_proposal.pdf`, §5.1–5.4, §13.1), and must extract "until the last drop" the provable information the method has, as Song & Liang (2015) did for theirs (`theory_campaign/inputs/SongLiang2015.pdf`). A method choice that makes this harder counts against it.
8. **Re-runs.** If the final method is close to v3 (e.g. stacking SMC islands, small additions), the 2,400-fit study is not re-run now; it is re-run at the end only if needed. Empirical checks here use at most 10–20 seeds.

## 2. The method on the table: v3.1

**v3 (the study method)** is `Docs/Methodology/METHODOLOGY_v3.md`:
- correlation-clustered blocks (B = min(⌊√n⌋, ⌊√p⌋, 16)), each enumerated exactly against the full y;
- product start π₀ = ϖ(S)∏_b r_b(S∩C_b)/Z̄₀ (the composite / "local" step);
- an SMC tempering bridge from π₀ to the exact posterior, with a random-order Gibbs round, swap and neighbour-swap moves, and independence moves;
- calibration (pilot, up to ℓ = ⌈log₂(n+p+1)⌉ grid rebuilds, 4 diagnostic islands, tiers) and then a final run of 4 islands × N₀ = max(2500, n, p) on a frozen grid;
- local search, the HPM (best model ever scored) decision, equal-weight PIPs (primary), unbiased Ẑ per island, and flags E1–E3.

**v3.1 = v3 unchanged as a statistical method, plus** (HQ proposal, from `theory/METH-AUDIT:theory_campaign/METH-AUDIT/REPORT.md` §5):
- (a) final islands as concurrent workers (own cache and ledger, merged by Lemma S): bitwise-identical to serial (Prop W);
- (b) the calibration's diagnostic islands as concurrent workers (Prop W-cal; code reading only, not executed yet);
- (c) local-search scans in parallel (lexicographic max-reduction);
- (d) optional stacked islands R′ = 4k at N_e, with R′ declared before final randomness;
- (e) the Ẑ-weighted PIP computed and reported (already in the spec §6.11, missing from `v3_run.R`);
- (f) LS0: a local search also run from the start mode. It changed 0 of 2,394 study HPMs in the O-LS0 test export, it is not in the production core yet, and it makes the T38(b1) route a theorem about the shipped method;
- (g) `fit$log_Z` = NA on stopped fits (API-AUDIT hazard).
- Declared v3.2 path (law-preserving): per-particle counter-based streams (particle-parallel islands, depth free of N); a Gram-free scorer for p ≳ 3·10⁴.
- Rejected by METH-AUDIT: splitting N_e into many small islands (C8), shortening calibration (C9), a parallel-in-particle move kernel (C10).

## 3. Agenda (every seat answers every item)

1. **Local-to-global versus a plain start.** Does the block/composite start earn its place (fewer stages, i.e. less sequential depth; better Ẑ; better PIPs; better HPM) against an independent-Bernoulli start (blocks of size 1) and a prior start, at matched compute? Should the backfit start (API-RESID: favourable on 79–92% of study fits, versus about 1/2,394 for the block start by THM-INV's count) be considered? Evidence: ABL-START (running; §5).
2. **Selection rule.** Is HPM the right primary? Should anything be added (MPM with either PIP, a certified local-search HPM, an HPM-vs-MPM disagreement flag), given ground rule 3? All candidates can be scored after the fact on the saved study fits.
3. **The parallel execution layer** (a)–(g) and the v3.2 path: is it right, complete and correctly classified? Is anything missing for "scale p beyond sequential MCMC"? Is the per-round depth factor m = p + B + 2 an inherent limitation to state, or a real issue to fix?
4. **Calibration.** It has no theorem for rebuild convergence or for P(schedule_limit), and it is the most sequential part. Keep as is with a stated contract, simplify, or change? Changes must not invalidate the study (ground rule 8) unless irrefutable.
5. **Which PIP is primary:** equal-weight (study's choice; bias set by N per island) or Ẑ-weighted (consistent as R grows; can be noisy under masking)?
6. **Flags and diagnostics** (E1–E3, ESS, grid flags): all current theory about them is negative. Keep as heuristics, add one with a provable positive property, or drop?
7. **Theory fit.** Given `theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md`, does any method choice block a proposal goal or make the theory harder? (This is a method meeting; the theorem list itself is decided later.)
8. **Anything else** a seat considers a real issue under ground rule 2.

## 4. HQ's open objections (to be answered, not inherited)

1. The block start may contribute little: in the masked regime π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, and the bridge plus moves do most of the work. The ablation (agenda 1) decides it.
2. Under masking, the backfit start is far more often favourable (API-RESID), but switching would be a WORKHORSE change.
3. The two PIP rules pull in opposite directions (agenda 5).
4. Calibration is the least theorised and most sequential component (agenda 4).
5. Concurrency evidence: Prop W executed bitwise on smoke + 2 study designs so far (third running); W-cal not executed.
6. LS0 must be shown additive in the production core, not just the test export.
7. Default R′ and the R-versus-N guidance must be fixed before final runs.
8. Flags have no positive power result.

HQ's candidate inherent limitations: the per-round Θ(p) sequential steps; each worker holds XᵀX (8p² bytes; shared read-only per node); SMC weight variance through a masked crossing; no run can upper-bound Z; Markov-only Ẑ lower bound; weight-based diagnostics can certify too early (Chatterjee–Diaconis Thm 2.1); at n = 200 the exact posterior often misses S₀ (565 of 2,400 study fits are posterior misses), so selection accuracy is limited by statistics, not the sampler.

## 5. Evidence index (read with `git show origin/<branch>:<path>`, after `git fetch origin`)

| What | Where |
|---|---|
| Method spec | `Docs/Methodology/METHODOLOGY_v3.md` (this branch) |
| Production engine | `Scripts/SMC_BVS/core/` (C++ `v3_engine.h`, `v3_core.cpp`, `v3_runtime.h`; R driver `v3_run.R`) |
| Parallel audit, work/depth map, robustness table, candidate changes | `theory/METH-AUDIT:theory_campaign/METH-AUDIT/{REPORT.md,PROOFS.md}`; results in `results/` |
| Concurrency runs (HQ re-run) | design p0500_S1_r001: bitwise PASS, serial 358 s → 189 s with 4 workers, R=32×312 max ΔPIP 2e-4. Design p0500_S4_r001: bitwise PASS, serial 672 s → 352 s, R=32×312 max ΔPIP 2.3e-3, HPM ≠ S₀ (both). Design p0500_S5_r002: running. Log: `evidence/concurrency_runs.log` |
| Theory inventory (component × property map, gaps) | `theory/THM-INV:theory_campaign/THM-INV/REPORT.md` (+ `digests/`) |
| Draft theorem list, tiers, HQ plan | `theory/THM-SYNTH:theory_campaign/THM-SYNTH/{THEOREM_LIST.md,HQ_PLAN.md,REPORT.md}` |
| Parallel-BVS literature and the gap claim | `theory/LIT-PAR:theory_campaign/LIT-PAR/REPORT.md` |
| Other literature | `theory/LIT-{SMC,MCMC,STAT,VENUE}:theory_campaign/LIT-*/REPORT.md` |
| Start alternatives (backfit), residual analysis | `theory/API-RESID:theory_campaign/API-RESID/REPORT.md` |
| Production-code audit (LS0, GUARD, IND-T) | `theory/API-AUDIT:theory_campaign/API-AUDIT/REPORT.md` |
| Registry of results | `theory/T38-RECORD:theory_campaign/T38-RECORD/{REGISTRY_v2.md,T38_STATEMENT.md}` |
| Start ablation (agenda 1) | `theory/ABL-START:theory_campaign/ABL-START/REPORT.md` (running; the chair folds it in at Round 2) |
| Proposal, Song–Liang 2015 | `theory_campaign/inputs/` |
| Study data (2,400 fits, inputs, truths) | `/home/fb31/ls0_work/study/` (local, read-only) |
