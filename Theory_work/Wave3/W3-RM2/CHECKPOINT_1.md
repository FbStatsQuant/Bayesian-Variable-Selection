# W3-RM2 — CHECKPOINT 1 (target fixed) — 2026-11-11

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-RM2`, no git state changed.
**Nothing is proved yet.** This checkpoint fixes the target: STATEMENT v1.2 is locked, the sharpness gate has run,
and two improvements are recommended for HQ's decision. No proof work beyond sketches.

## 0. Flags (read first)
1. **The theorem reaches b < ½, not only b < ¼ — but it still carries a lattice condition.** At |Q| = n^b RM's
   condition (N) does not survive in either form. What replaces it is a Gaussian-width condition **(W)** on the
   residual directions of the lattice [S₀, Q]. It contains RM's (N), has primitive sufficient forms, and a planned
   converse shows the route cannot do with less. "(V) + (L) alone" is not claimed (path-level; not this ticket).
2. **One observed failure outside the assumptions.** With every outside column leaking at nominal level η = 1
   (far above the threshold), LS0 stopped at its move cap before S₀ in 4 of 6 runs at n = 1600 (10/10 fine at
   n = 400). So the leak condition is not only a proof device. Everywhere else — b up to 0.75, the width condition
   violated, a weak truth, leak levels near the frontier — LS0 still ended at S₀ (202/202 runs).
3. Form R (Gaussian rows) is stated but costs more than Form F; examples at p ≫ n exist only in Form R.
4. `manifest.py bind` refuses non-council reviews (it needs a COUNCIL-VERDICT line); every review here quotes its
   digest and `verify` passes. The brief's "then bind" step cannot be met by a lock or better-theorem review.
5. The n = 3200 numerics layer was not run (stopped: too slow locally); one n = 1600 run finished after the
   review freeze and is reported in an addendum.

## 1. Locked statement (`STATEMENT.md` v1.2 LOCKED)
Setting, method objects, events and the core RM-0 are W3-RM's (RM-0 has no size restriction on Q; W3-RM:RM-0@1.0.0,
W3-RM:E4@1.0.0 consumed). Code pins: LS0's centre, cap and scan (`cpp/v3_core.cpp:465-476`, `cpp/v3_engine.h:392-414`).

* **(C1) RM2-F, fixed design.** Theorem 1's conditions, the eigenvalue floors, visibility (V), leakage (L) with a
  deterministic Q, **|Q| ≤ n^b**, leak level η outside Q, **b < β(η, A) = ½ − η/2 − √(2Aη)** (b < ½ when nothing
  leaks), the signal floor (BM-Q): nθ*²_min ≫ |Q| + log n, and **(W)**: the expected maximum over the lattice of
  |u_{T,l}ᵀg| − √(2 log(p/(|T| + 1)) + (1 − δ₀) log n) is ≤ 0. Then one data event of probability → 1 on which every
  output run (every seed, N_e, R′, calibration outcome) reports Ŝ⁺ = S₀; LS0 makes |S̃₀ ∖ S₀| ≤ n^b deletions and its
  archive is certified; the shipped cap is never binding.
* **(C2) RM2-R, Gaussian rows.** Population visibility; localised leakage with |Q| ≤ n^b and reference
  neighbourhoods |H_l| ≤ n^ρ, **15ρ + b < ½**; (W) on the realised design with probability → 1 (sufficient: the
  reference/atom conditions of LOC2's Lemma NA-R at polynomial size, for every δ₀ < 1 − 2b).
* **(C3) Width lemmas.** (a) (W) ⇒ whole-lattice no-addition w.p. → 1, with a size-dependent level; (b) converse:
  if the width exceeds the level with the opposite slack, whole-lattice no-addition fails w.p. → 1; (c) sufficient
  forms: (W-χ) = RM's (N-χ); (W-ref): directions = a reference in one of ≤ p·n^h low-dimensional frames (h + b < ½)
  + an ℓ¹-small combination of atoms + an ℓ²-small remainder; (W-loc): every column's regression on any lattice
  set is carried by ≤ h log n/log 2 lattice members up to a small ℓ¹ error.
* **(C4)** RM-F and RM-R are special cases (so RM2 would supersede them for free once proved; HQ's decision).
* **(C5) Examples** (to verify in the last leg): RM's examples; exact-Gram polynomial decay α > 2 (Form F);
  polynomial covariance decay α > 17/2 = W2-LOC2's class (Form R). One candidate (equicorrelated leak group).
* Conditional on SOP:TH09 (Theorem 1), W2-APP:POST and W3-RM:B9 (Form R), W1-GEN:L1 (toolkit; planned
  self-contained). Not claimed: no lattice condition; b ≥ ½; data-dependent envelopes; delivery.
No design family and no block in any hypothesis.

## 2. Review record
| round | seat | manifest | verdict | files |
|---|---|---|---|---|
| SL1 | Sol, blind | 1397b036… | LOCK WITH CHANGES: 2 MAJOR, 4 MINOR, 4 optional; no CRITICAL. Checked by hand: the sandwich's only size-sensitive step, the width lemma, the converse, the three sufficient implications, containment | `reviews/SL1_statement_lock_sol.md`, `SL1_disposition.md` |
| RC1 | Sol, reconciliation | 94c0349e… | 9 of 10 items RESOLVED; R4 partially (registry edges, MAJOR, record only); 1 new MINOR | `reviews/RC1_reconciliation_sol.md`, `RC1_disposition.md` |
| RC2 | Sol, diff check | 510e9a05… | all hunks required or record-only; "editorial/record only — v1.2 can be locked" | `reviews/RC2_diffcheck_sol.md` |
| BT1 | Astra, blind | 65ee6108… | 3 proposals: 2 ADOPT NOW, 1 WORTH A TICKET; 8 directions with no credible improvement | `reviews/BT1_better_theorem_astra.md`, `BT1_disposition.md` |
SL1's two MAJOR items: the sufficiency of the population conditions for (W-R) holds only for δ₀ < 1 − 2b (now
stated); the registry block listed alternatives as joint assumptions and overstated a necessity (rewritten). No
hypothesis of (C1)/(C2) changed after v1.0. No review layer was skipped. `verify` passes on MANIFEST_BT1.

## 3. Necessity reading per assumption (`ASSUMPTION_MAP.md`; numerics `numerics/RESULTS.md`)
Numerics: production partition, tables and score; start mode and LS0 re-implemented and validated against
production (306 scores to 3e-13; path identical to a brute-force LS0). p = 2n, n = 400 and 1600, 208 runs,
nominal classification. "Held" = LS0 from the start mode ends at S₀, certified. Observations, not proofs.

| assumption | where it enters | reading | numerics outside it | flag |
|---|---|---|---|---|
| \|Q\| ≤ n^b, b < β(η, A) | sandwich, junk exclusion only | sufficient budget; heuristic boundary at start-mode size ≈ √n (the prior stops paying for excluding the best of p noise columns); not proved necessary | b = 0.5, 0.625, 0.75: held 48/48, although an outside column sits in the start mode in 5/12 runs and path-level no-addition fails in up to 4/6 (n = 1600); ≤ 4 non-deletion moves per run against a cap slack of 15 | `improvable` (conclusion); artefact threshold |
| (W) lattice width | no-addition on the lattice | **forced for the route** up to slack (planned converse); not derived from (V), (L); not needed for the conclusion as observed | width violated by design (B2): whole-lattice no-addition truly violated at a probed set in 6/6 runs (b = 0.5, n = 1600), never along the path; held 48/48 | `improvable` for the conclusion only |
| (BM-Q) | truth removal on the lattice | a union bound over 2^{\|Q∖S₀\|} sets; weakenable (BT1 P1) | not isolable at feasible n (weak-truth runs: held 32/32, LS0 re-adds the truth) | single-use union bound → P1 |
| leak level η (L-gain) | sandwich | sufficient; coupled to b through a max bound that a counting argument reproduces | η = 0.05, 0.2: outside columns enter the start mode and are deleted, held 32/32. **η = 1: held 10/10 at n = 400, 2/6 at n = 1600** (start modes of ~600 columns, 19–73 swaps, cap hit) | near the frontier `improvable`; far outside the conclusion fails under the shipped cap |
| \|H_l\| ≤ n^ρ, 15ρ + b < ½ (Form R) | reference count in the Gaussian-row sandwich | artefact of counting conditioning sets (the 17/2-type threshold) | not probed | artefact threshold |
| (V), floors, (L-feas), "15" | as in W3-RM | as in W3-RM's sharpness record | (V) at finite n: see weak truth | inherited |
Inside every assumption (b ≤ 0.375): sandwich, path-level no-addition and deletion-only descent in 32/32 runs.

## 4. Better-theorem proposals and dispositions (`reviews/BT1_disposition.md`)
| id | proposal | disposition (lead's recommendation; HQ decides) |
|---|---|---|
| P1 | replace (BM-Q) by a width condition on the truth-removal directions: nθ*²_min ≫ d_n² + log n; (BM-Q) implies it; BM-∞ suffices when d_n² = O(log n) | **ADOPT.** Weaker hypothesis, cheap; rests on an exact identity (checked numerically, error 1e-14) |
| P2 + G1 | state (W) as "width gap → −∞" instead of a fixed fraction of log n; add an explicit rate n^{−c} for no-addition. Lead's refinement G1: with the constant-free level √(log n + 2 log(p/(k + 1))) the converse becomes "gap → +∞ ⇒ fails", an almost exact characterisation of whole-lattice no-addition | **ADOPT** (in the G1 form) |
| P3 | Form R: leak scale o(√(log n/n)) and localisation rate o((n/log n)^{−1/4}) | **DEFER as open item O3**, or attempt inside the Gaussian-row sandwich lemma with a one-attempt budget — HQ's choice |
| G2 | polynomial rate for the search event in Form F | adopt if cheap at proof time (remark; no hypothesis change) |
| G3 → O1 | b ≥ ½ and leak beyond the frontier: path-level control with cap accounting | **DEFER** (separate ticket); the η = 1 failure mode is its input |
| G4 → O2 | leak-profile (counting) form of (L) to decouple b from η | **DEFER**; reviewer confirms no gain under the present worst-case hypothesis |
| O4 | equicorrelated leak-group example | verify or drop at the examples stage |
Reviewer found no credible improvement for: the b/η coupling; the n^{15ρ} count; b ≥ ½ with a deterministic
sandwich; a descent condition tolerating lattice additions; an exact converse threshold; a rate for the whole
theorem; the old cap.

## 5. Decisions asked of HQ
1. Adopt **P1** and **P2/G1** into a v1.3? (Then: one fresh Sol check of the change before proving.)
2. **P3**: defer (O3) or attempt inside the Form R sandwich with a one-attempt kill budget?
3. Keep **Form R** in this ticket (recommended: yes, after Form F's key lemma), or split it off?
4. Registry: RM2-F/RM2-R as CANDIDATES that imply RM-F/RM-R (free supersession once at parity)?

## 6. Plan for CP2 (key lemma) — sketch only until HQ replies
Key lemma = `lemmas/L2_width.md`: no-addition on the polynomial lattice from the width condition (size-dependent
levels), its sufficient forms, the converse, and truth removal (under (BM-Q) or P1's width form) — with the
toolkit at polynomial cardinality (`L0`) and the fixed-design sandwich (`L1`) proved alongside. Then Sol lemma
checks with falsification numerics (width functional estimated by Monte Carlo on small lattices; score margins),
and the independent Astra mid-point → CP2.
* **Estimate:** 4–6 hours of lead time for Form F to CP2, 4–5 reviewer runs (2–3 Sol checks, 1 Astra mid-point);
  Form R adds a parallel Sol prover for the Gaussian-row sandwich, one Opus cross-family check (Claude Work) and
  roughly another 4–6 hours, most of it after CP2.
* **Risk:** low for Form F — SL1 re-derived every step of the sketch by hand; the kill budget (3 failed attempts)
  is unlikely to be reached. Medium for Form R (long re-run; the passage from the joint law to the conditional
  width). The hard question — the theorem without any lattice condition — is outside this ticket.

## 7. Files (`Theory_work/Wave3/W3-RM2/`)
STATEMENT.md (v1.2 LOCKED), PLAN.md, ASSUMPTION_MAP.md, LOG.md, CHECKPOINT_1.md; numerics/ (SPEC.md, RESULTS.md,
rm2_common.R, validate.R, validate_out.txt, run_all.R, summarise.R, results_raw.csv, summary.csv);
reviews/ (INPUTS.txt; MANIFEST_SL1/RC1/RC2/BT1; briefs; SL1, RC1, RC2, BT1 replies verbatim; three dispositions;
STATEMENT_v1.1_as_reviewed_by_RC1.md; post_BT1_addendum/).
Agents in this leg: lead (Claude Fable 5.2, Claude Work); SL1, RC1, RC2 (Codex gpt-6.1-sol, high); BT1 (Codex
gpt-6-astra, high). Claude tally: CW 1 / CP 0. No NOTS use.
