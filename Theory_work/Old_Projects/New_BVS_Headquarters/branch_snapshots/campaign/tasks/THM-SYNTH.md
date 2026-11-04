# THM-SYNTH: the final theorem list for paper 1 (Track B, step 2)

**Project goal (Felipe, 2026-11-03).** Paper 1 is not "another BVS". Sequential samplers (MCMC), however good, cannot keep scaling p. The aim is to start replacing them with PARALLEL samplers that keep MCMC-level guarantees AND work under correlated designs. Song & Liang (2015, JRSS-B, split-and-merge; `theory_campaign/inputs/SongLiang2015.pdf`) is parallel and has theory, but it breaks under correlation (Condition 5; Thm 4/Cor 2 with eq. (19)), and its merged output has no theorem. Our method is local-to-global (`theory_campaign/inputs/Local_to_Global_proposal.pdf`): exact enumeration of correlation-clustered blocks → product start π₀ (the merge) → SMC tempering to the EXACT posterior (the correction), run as independent islands with unbiased Ẑ. Thesis sentence (draft): "In split-and-merge, correlation breaks correctness; in local-to-global SMC, correlation costs only sequential depth and particles, never correctness." Objectives in order: (1) accuracy of the posterior (Ẑ, PIPs, joint inclusion, E_π[h]); (2) parallel scalability; (3) selection accuracy. Existing theory goals (T03♯, T38, N200, …) are KEPT. Felipe wants the Song–Liang instinct, a parallel algorithm with ambitious theory, at a much larger scale because agents do the proving. Version 1 must be Biometrika-grade, with Lean certificates for the parts that can carry them; harder results go to a later tier.

**Method decision (HQ, fixed input; do not reopen).** The method shipped is **v3.1 = v3 unchanged as a statistical method + a parallel execution layer**, following `theory/METH-AUDIT:theory_campaign/METH-AUDIT/REPORT.md` §5:
- (a) concurrent final islands (Prop W, bitwise); (b) concurrent diagnostic islands (Prop W-cal); (c) parallel local-search scans;
- (d) optional stacked islands R′ = 4k at fixed N_e, R′ declared before final randomness;
- (e) the Ẑ-weighted PIP is computed and reported next to the equal-weight PIP;
- (f) **LS0 is added** (local search also run from the start mode). It is a deterministic scan, it changed 0 of 2,394 study HPMs, and it makes the verified T38(b1) route a theorem about the shipped method;
- (g) `fit$log_Z` is NA on stopped fits (API-AUDIT hazard).
- Declared v3.2 path (law-preserving, no theorem changes): per-particle counter-based streams (particle-parallel islands, depth free of N), and a Gram-free scorer for p ≳ 3·10⁴.
- Rejected: splitting N_e over many islands, shortening calibration, a parallel-in-particle move kernel. So the per-round depth factor m = p + B + 2 stays and must be stated honestly (METH-AUDIT Prop D; LIT-PAR §3.3).
- Caveat: METH-AUDIT §1 says "3/3 study designs" bitwise, but only the smoke problem and one design (p0500_S1_r001) actually completed. HQ is running the other two; treat the empirical claim as 1/1 + smoke.

**Read (in this order).**
1. `theory/THM-INV:theory_campaign/THM-INV/REPORT.md` (the inventory; §5 is the gap list) and its `digests/`.
2. `theory/METH-AUDIT:theory_campaign/METH-AUDIT/{REPORT.md,PROOFS.md}` (Props W, W-cal, P, D, Cor V; §3 robustness table).
3. `theory/LIT-PAR:theory_campaign/LIT-PAR/REPORT.md` (gap claim, G4 counterexample, what is KNOWN—CITE).
4. `theory/T38-RECORD:theory_campaign/T38-RECORD/{REGISTRY_v2.md,LOCKABLE_v2.md,T38_STATEMENT.md}`.
5. As needed: the other LIT-* and API-* REPORTs, `Docs/Methodology/METHODOLOGY_v3.md`, both PDFs (proposal §§4–5, §13; Song–Liang §§2–4, §6).
6. Find the project's Lean work (search the repo and `theory/*` branches for `*.lean` / lakefile) so the Lean-feasibility column is grounded in what already exists (e.g. Theorem A is sorry-free).
`git fetch origin` first; read branches with `git show origin/theory/<ID>:<path>`.

**Do.**
1. **The list.** Produce the final list of theorems for paper 1, organised in these groups (add or merge groups only with a reason):
   - **G1 Validity under parallel execution**: exactness at fixed data for any R, concurrency, pooling rules, the "R fixed in advance" rule.
   - **G2 Posterior accuracy** (objective 1, the main gap): Ẑ (two-sided where possible, masked regime included), PIPs (both poolings), joint inclusion, general E_π[h]. This is proposal §13.1.
   - **G3 Parallel work/depth**: the counterpart of Song–Liang §6 in the same units; depth as a function of p, correlation/masking (stage laws: Theorem G, STG-M, O-STAGES), R and N; the R-vs-N trade-off. This is the formal "costs only depth and particles".
   - **G4 Why the bridge / why the merge alone fails**: start-quality laws (T22, T27, DIL, SEP-A/B), the one-shot correction cost scale (Chatterjee–Diaconis exp(KL)), Prop M repaired or dropped.
   - **G5 Correlation robustness vs split-and-merge**: an analytic separation: on a masked family, Song–Liang's procedure loses a true predictor with probability bounded away from 0 (or → 1) over random splits, while v3.1's output is correct (exact target + selection result). Use the JRSS-B text (Condition 5, Thm 4/Cor 2, eq. (19)), not slides; LIT-PAR G4 is the numerical seed.
   - **G6 Selection accuracy of the reported output**: T03♯, T07, T21, N200, T38 (with the LS0 route now in the shipped method), delivery P(U).
   For each theorem give: (i) a precise draft statement, with hypotheses; (ii) the guarantee in one plain sentence and why the thesis or a referee needs it; (iii) current status, verbatim from sources, and the components it covers (THM-INV §1 rows); (iv) novelty verdict. KNOWN—CITE results become **cited lemmas**, not theorems, and the list must say so; (v) difficulty and a credible proof route; (vi) Lean feasibility: which core (finite combinatorics, inequalities, an identity) can be Lean-certified and which parts rest on cited probability theory; (vii) dependencies on other list items.
2. **Tiering.** Mark each item **v1** (Biometrika paper: must be provable within the campaign with a credible route now) or **v2** (later, more ambitious). v1 must still cover all three objectives and the parallel claim. Say explicitly which THM-INV §5 gaps v1 closes, which it states as limitations, and which are deferred.
3. **The thesis sentence as a theorem.** Give the formal version that the v1 list actually proves (with its exact scope, e.g. fixed data vs n → ∞, favourable vs masked), or say what wording the paper may use if it is not proved in full.
4. **Disagreements.** Settle what you can from the sources: D1 (API-POS vs LIT-MCMC on rapid mixing for our prior; what may the paper say), D5, D6. Leave the rest as escalations with a named check.
5. **HQ plan.** Group the v1 items into per-theorem HQs (one HQ = one main theorem or a tight cluster, each looping to a referee-checked proof and Lean certificate). For each HQ: scope, the input results it depends on, the first concrete step, the risk, and a rough cost class (S/M/L in agent runs). Give the dependency graph and the order to start them. Keep shared notation: point to the registry IDs.

**Deliverables** (under `theory_campaign/THM-SYNTH/`):
- `THEOREM_LIST.md`: the list itself, one entry per theorem with fields (i)–(vii) and the tier; a one-page summary table at the top.
- `HQ_PLAN.md`: item 5.
- `REPORT.md`: items 2–4, plus what you dropped from the current registry for the paper and why, and a confidence card.
No new proofs are required; short proof sketches are welcome where they decide feasibility. Use honest status words. Never invent a citation, and never upgrade a status.
