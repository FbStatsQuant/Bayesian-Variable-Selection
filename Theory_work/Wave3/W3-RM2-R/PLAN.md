# W3-RM2-R — PLAN (v0.1, 2026-11-15)

Tier B rider, NORMAL mode. Statement: `STATEMENT.md` (delta over W3-RM2 v1.4 and W3-RM RM-0). Cut-off: CP3 by
Wed 2026-11-18 18:00 CT. Budget ~8–10 Opus hours; ≤ 2 helpers; OpenAI reviews about 4 (lock, 2 line-check batches,
council seat).

## 1. Proof plan per lemma (each a copy of the parent with [R-#] marks, or a new short file)

| file | claim(s) | what is proved | how | risk | hours |
|---|---|---|---|---|---|
| `lemmas/Q1_sandF_c.md` | SAND-F-c | PARENT `lemmas/L1_sandF_b.md` with (V_b♭) | copy; change Step 2(a) only: (δ + σZ)² ≥ (√(M_V log n) − σz_n)² when √(M_V log n) ≥ σz_n; then (√M_V − σ√(2A))² log n/(2C_R) − (A + ½) log n − O(log log n) > 0 iff M_V > M_V⁰. Steps 1, 2(b) do not use (V) (check) | low | 0.5 |
| `lemmas/Q2_TL_c.md` | TL-F-c, and Q3 (POST/MODE-F) | PARENT `lemmas/L2_width.md` §4 with (BM-W⁺); [POST], [MODE] from SOP:TH09 at BM(c) | copy §4; replace "|Z_{A,i}| ≤ ½√λ_n for n ≥ n₀" by the first clause of (BM-W⁺); first square ≥ σ²λ_n/4; RSS_A − RSS_T ≥ σ²(λ_n/4 − (2A + 2) log n); score ≤ (A + ½) log n + C − σ²(λ_n/4 − (2A+2) log n)/(2C_R) < 0 iff c_TL > c_TL⁰ (for n ≥ n₀, a margin ∝ log n beats the constants). Q3: TH09 item 1 under BM(c), Markov as PARENT `L3_assemblyF.md:22-24`; [MODE] from {π(S₀) > ½} ⊆ 𝓜_n | low (kill budget 2 on the TL step per BRIEF) | 0.75 |
| `lemmas/Q4_core_plus.md` | RM0-plus | (a′), (b⁺), (c⁺) | copy RM `lemmas/L0_core.md`; (a′): re-read GROW L1.1–L1.2 (NA, TL used only at C and C ∖ {e} for the current state C), down-closure keeps the path in 𝓛′; (b⁺): RM-0(b)'s proof uses π(S₀) > ½ only through "F(S₀) > F(S), S ≠ S₀" (`L0_core.md:53-55`); (c⁺): DLV-0 makes 𝒪 sure; null-set remark for Settings F, R | low | 0.75 |
| `lemmas/Q5_dlv0.md` | DLV-0 | deterministic delivery at the pin | walk `v3_fit` (core at 72785fe): every exit is (i) an input/degenerate exit excluded by "valid non-degenerate" (S.1 deterministic form: finite X, ≥ 1 non-constant column so `no_predictors` cannot fire; y non-constant), (ii) a scorer failure excluded by EX-A (S.2, for every input), (iii) a resource/preflight exit excluded by (D) (Corollary R re-derived: LS0 cap ℓ_n + \|S̃₀\| ≤ ℓ_n + K, preflight charge of ef33f91), (iv) `schedule_limit`, excluded by the shipped fallback (`v3_calib.R:120-124, 162-170`): check that the recorded fallback (last successful tier-1 construction, else the tier-1 pilot schedule) always passes `v3_check_grid` (DLV L3 Lemmas 3.3, 3.4) and that the fallback branch is reached whenever a tier-1 construction failed; (v) the checked 64-bit additions (C-ENG GROW-MR1) excluded by IDEAL-W; (vi) S.3 unreachable paths re-audited; re-check the P1 inventory for exits added since v3.1 (C-ENG commits 36c0cfe, bf093a8, 0638af9, ef33f91, 98fac03, 72785fe) | medium (code audit; no new mathematics) | 2.0 |
| `lemmas/Q6_assembly.md` | RM2-F-plus, RM2-R-plus, Cont-plus | assembly | copy PARENT `L3_assemblyF.md` and the assembly part of `L5_formR.md`; inputs Q1–Q5; containment line by line | low | 0.75 |
| `lemmas/Q7_proxy_d.md` | Ex-Proxy-d | (a) d_n = O(1); (b), (c) | explicit residual u_{P,1} = (√(1−r²)e₁ − rΣ_{j∈P}e_j)/√(1 − r² + r²\|P\|) for every proxy set P (outside columns orthogonal); E max ≤ √(2/π)(1 + r(q − 1))/√(1 − r²); r q → 0 for b < ½; recheck each RM2-F / RM2-F-plus clause of PARENT E4 with θ_n (only (V), (BM), BM-W depend on θ) | low | 1.0 |

Copies are made before editing; DEPS rows record parent hashes. No new key lemma is expected; if one appears (e.g.
DLV-0 needs new mathematics on the grid fallback), early checkpoint (Tier A).

## 2. Numerics (boundary, TARGET.md) — helper H1 (Sonnet 5.5, high), after CP1

`numerics/SPEC.md`: on the Ex-Proxy design (n ∈ {400, 1600}, b ∈ {0.3, 0.45}) and on one AR-type design with a
polynomial Q, sweep θ_n² = κσ² log n/n over κ ∈ {0.5, 1, 2, 4, 8, 16} (the sufficient constants κ₀ are ≫ these, so the
sweep shows where the route's events (truth in start mode, TL, NA) and the LS0 probe actually fail), using PARENT's
validated LS0 re-implementation (`W3-RM2/numerics/rm2_common.R`, read-only; copied). Report per κ: start-mode
inclusion of S₀, NA/TL at probed lattice sets, LS0 endpoint, posterior mode = S₀ (exact on small cases). Purpose:
boundary numerics for (V♭) and (BM-W⁺); not evidence for necessity. ~1 h helper time.

## 3. Review chain and hours

| step | who | when (target) |
|---|---|---|
| statement lock SL1 | Sol (gpt-6.1-sol high), fresh, blind | Sun 11-15 evening |
| CP1 | manager | Sun/Mon |
| lemmas Q1–Q7 + numerics | lead (+ H1 numerics) | Mon 11-16 (~6 h) |
| line check LC-A: Q1, Q2, Q7 | Sol, new agent | Mon |
| line check LC-B: Q4, Q5, Q6 | Sol, new agent | Mon/Tue |
| repairs + re-checks | new Sol agents | Tue |
| REPORT, READER_DELTA final, citecheck, DEPS all OK, freeze MANIFEST_R1 | lead | Tue |
| council R1: Sol seat + Opus 5.5 seat (Claude Third) | fresh, blind | Tue/Wed |
| diff round if needed; CP3 | | Wed by 18:00 CT |

Total lead time ≈ 8 h; OpenAI reviews 4 (+ re-checks if any).

## 4. Optional items and open items

* Quantile form of (W) (PARENT `L2_width.md:77-86`): gains only under superconcentration (sharp2 triage). **Proposed:
  drop to a named open item (O-Wq)** unless HQ wants it at CP1.
* Ex-Equi b = 3/8 and converse (O4′): only if CP3 by Wed 18:00 stays safe after LC-B; otherwise stays O4′.
* Form R aggregated leak: named open item (BRIEF), not a target.
* RM2's Ex-PolyR, Ex-PolyF: **not consumed or restated** by this delta (RM2-F-plus's hypotheses are implied by
  RM2-F's, so they remain examples through Cont-plus without restatement) → listed in CHECKPOINT_1 for the manager.

## 5. Stop rules (RIDER_RULES §6)

Early checkpoint on: a counterexample or WEAKER change to a target clause; DLV-0 failing against the code (e.g. an
exit not covered by (D)) — then T2(a) drops to "on output" and RM2-F-plus keeps the (b⁺) form only; a kill budget
spent (TL step: 2); a hold on a consumed claim; cut-off at risk.
