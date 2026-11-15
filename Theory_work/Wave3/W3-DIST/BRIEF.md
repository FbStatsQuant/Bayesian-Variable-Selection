# W3-DIST — distribution-level consistency (Song–Liang Theorems 1–2 analog) — scoping leg (HQ, 2026-11-15)

You are the **lead** of ticket W3-DIST (Claude Fable 5.2, effort high, provider **Claude Third**, machine **Owls**).
Repo clone `/home/fb31/Bayesian-Variable-Selection` (branch `main`); folder `Theory_work/Wave3/W3-DIST/`. Write only inside
that folder. **Change no git state** — the only git command you may run is the initial `git pull --ff-only`; HQ commits
your files. Never use effort above high.

## Why (owner request, 2026-11-15)
Felipe wants, next to selection consistency, **consistency of the distributions** as in Song & Liang (2015, JRSS-B 77(5))
Theorems 1–2: posterior consistency in Hellinger distance of the joint (x, y) density, random design, rate ε_n
(Thm 1 bounded predictors; Thm 2 their Condition 1, exponential moment; Cor 1 rates; (16) under Condition 2 in probability).
PDF (gitignored, copyright): `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf` — read §2.1–2.2 (pp. 949–956) in full.

## Read first
- `Theory_work/Wave3/PROGRAM.md` (presentation rule), `Theory_work/Wave3/PROTOCOL.md` (rules 9–16).
- `Theory_work/Wave1C/C-PACK/SONG_LIANG_MAP.md` — row-by-row map of Song–Liang vs our results; rows 1–4 record the gap
  ("No Hellinger/predictive analog"), row 8 and gap (iii) the shipped-output gap.
- What we already have (inputs, read critically, cite with their recorded status):
  - `Theory_work/Wave3/W3-POST2/STATEMENT.md` Claim D + `lemmas/D_hellinger.md` (Corollary H): **in-sample, fixed-design**
    average Hellinger contraction of the exact working-model posterior of (S, θ, v); D(a) rate M_n/√n given δ_n → 0;
    D(b) log n/n, no beta-min. Council-passed C1 (8.6/8.6), acceptance not yet recorded — cite as "council-passed,
    acceptance pending". Note the eb1f9da history ("D(b) suspect + repair") and that the repair passed council.
  - `Docs/Theory/proofs/T04_A3_contraction/` (STATEMENT.md, PROOF_v2.tex, FINAL_REPORT.md): contraction of Xθ, θ, v
    without beta-min at (s₀+1)ℓ_n/n under SE, with H-T02 as a hypothesis; "Not claimed: out-of-sample … random-design
    Hellinger". Legacy v3 pipeline (two reviewers VERIFIED), not in the registry.
  - C-PACK SL0/SL1/SL1′/SL2 (`Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md`): PIP consequences; SL2 = coded
    store-restricted PIPs jointly with output.
  - Selection inputs: SOP:TH09 (T03♯), W2-APP:POST (random Gaussian designs, LSF), W1-PXN (P), W1-GEN; the coded-method
    reported-model results (W3-RM2, W3-START/START2). Registry: `Theory_work/INFRA/registry/claims.tsv` (status column).
- Code as on `main` (`Scripts/SMC_BVS/core/`): what the method actually returns as its posterior approximation (particle
  measure / store / reported PIPs, `pip_primary`). Pin file:line + commit for every code fact.

## Targets (design-agnostic; families only in an examples table; all asymptotic; p ≤ n^A, p ≫ n allowed)
- **(i) Random-design Hellinger theorem (direct Song–Liang Thm 1–2 analog).** For the exact posterior of (S, β, σ²):
  Π(d(f, f*) > ε_n | D_n) → 0 in probability (exponential forms only if cheap), d = Hellinger between joint (x, y) laws,
  rows i.i.d. under a primitive tail condition (sub-Gaussian / Song–Liang Condition 1 or weaker, e.g. second moments as
  their Condition 2) plus a sparse upper-eigenvalue bound on Σ. Candidate route: d² ≲ (v/σ*² − 1)² + (θ−θ*)ᵀΣ(θ−θ*)/σ*²
  on small supports, from POST2-D / T04 parameter contraction, transferring sample to population Gram on sparse sets.
  Two rates: with selection (√(1/n)-type, beta-min) and without beta-min (log n/n-type). Compare with SL Cor 1.
- **(ii) Method-as-coded version.** The distribution the coded SMC returns (its weighted particle/store measure, and the
  BMA predictive built from it) is consistent: e.g. TV(π̂, δ_{S₀}) → 0 jointly with output, and Hellinger consistency
  of the plug-in/BMA predictive from the returned output. Identify precisely what the code returns and which delivery
  results (SL2, M1(i), M4, RM2/START) carry over; state honestly what is conditional.
- (iii) optional: in-sample → exponential-in-probability upgrade, only if a one-step argument exists.

## This leg: scoping to CP1 only (target ≈ half a day; token-efficient)
1. `PLAN.md`, `STATEMENT.md` v1.0: candidate theorems for (i) and (ii), each with numbered assumptions, rate, and the
   key lemma stated precisely; a consumes table (claim id, recorded status, exact statement used).
2. `ROUTES.md`: proof route(s) per target, the exact point where each could fail, difficulty estimate. Include whether
   (i) is "assembly" (POST2-D/T04 + sample-to-population transfer) or needs new probability.
3. Optional small local numerics (no NOTS, no cluster) if they inform a route; `numerics/` with scripts + RESULTS.
4. One fresh blind reviewer at the end: `delegate_task`, provider `codex`, model `gpt-6-astra`, reasoningEffort high,
   mode wait, on a frozen manifest (`python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/W3-DIST
   Theory_work/Wave3/W3-DIST/reviews/MANIFEST_S1.txt --extra Theory_work/Wave3/W3-DIST/reviews/INPUTS.txt` from repo
   root; INPUTS lists only the input files above, never wave documents or registry tables): break the candidate
   statements (counterexample as stated? missing assumption? does (ii) overclaim what the code returns?). If codex is
   unavailable on Owls, say so and skip — do not substitute. Disposition file.
5. **CP1:** `CHECKPOINT_1.md` — locked candidate statements, key lemmas, route ranking with failure points, consumes
   table, reviewer verdict + dispositions, and a recommendation: proof leg GO (who: Opus or Fable; kill budget; time
   estimate) or NO-GO with the obstruction; plus one paragraph "what this buys the paper vs Song–Liang". **End your
   run** with that content as your final message.

## Operating rules
- Read `Theory_work/Wave3/HOLDS.md` before each step. LOG.md heartbeat with real local time (`date`).
- Any Claude helper: provider **Claude Third** (`claudeAgent_claude_third`), Opus 5.5 preferred, effort high max.
  No other agents than item 4.
- Stay in your run while the reviewer works; do not end your turn until CP1 is written.

## ADDENDUM A1 (HQ, 2026-11-15 ~15:50 CT) — owner priority: distribution consistency is a MUST, at Song–Liang strength
Owner: "Consistency for distribution is actually a more valuable target than for variable selection … the former needs to
get done, pretty much as close as strong to Song results for their method." This overrides "(iii) optional" above.
**Parity checklist** — CP1 must state, for each item, the candidate result and whether it matches, beats or falls
short of Song–Liang (with the reason when short):
- **P1 metric:** Hellinger between the **joint (x, y) laws**, x random (rows i.i.d.), integrated as in their d(f, f*), not
  only the in-sample average.
- **P2 mode of convergence:** their exponential form (15),
  P*[Π(d > ε_n | D_n) > e^{−c n ε_n²}] < e^{−c n ε_n²}, under a sub-Gaussian / exponential-moment condition (their
  Condition 1 or weaker); and the in-probability form (16) under second moments only (their Condition 2).
- **P3 rate:** an explicit ε_n. Compare it with their Corollary 1 (n^{−(1−α)/2} log^{k/2} n, or n^{−min{1−α−q, 1−vq}/2}).
  We expect ε_n² ≍ s₀ log p / n or better.
- **P4 sparsity:** strict sparsity (their (4)) required. Approximate sparsity (their (3), Theorem 1) is a stretch item.
- **P5 prior:** the prior **as coded** (BB(1, p) capped at K, the coded slab, IG(0.01, 0.01)). No extra prior tuning.
  If their (8)–(14)-type prior conditions fail for the coded prior, say so and find the route that works for it.
- **P6 the method as coded (beyond Song–Liang):** the distribution the coded SMC returns. They prove results only for
  the exact posterior.
- **Scope:** p ≤ n^A with p ≫ n (theirs is P_n < exp(C n^α)). Exponential p is a stretch item, not required.
- **Design-agnostic:** primitive conditions only. Their Condition 3 is not needed for distribution consistency.

**Proof leg:** pre-authorized by HQ, Fable lead on Claude Third. At CP1 give a GO plan that reaches parity on P1–P3 + P5
(P6 next), with a kill budget per key lemma. Do not stop at the in-probability version if the exponential form is
reachable.
