# W2-PREM working notes (not a deliverable; see REPORT.md / PROOF.md)

Run of 2026-11-02, branch theory/W2-PREM, from theory/campaign @ 2f6d0ab.
Inputs read: PROTOCOL, tasks/W2-PREM.md, THEORY_PRIORITIES, 00_COMMON, METHODOLOGY_v3 §6,
W1-T24G REPORT/PROOF (origin/theory/W1-T24G), W1-EXP REPORT/PROOF, W1-T03R REPORT, engine cpp/v3_engine.h, v3_core.cpp, v3_util.h, v3_start.h.

## Naming issue found at the start
The task file defines IND = "conditional independence of terminal trajectories" and calls it open in the
masked regime. In W1-T24G the code IND(F) is the *independence-proposal bad-acceptance* premise
(PROOF §6 table, row "independence bad acceptance"), and conditional independence is the separate fact (R5).
They are different objects. This run treats both: IND-T (trajectories) and IND-M (move).

## Plan
1. IND-T from the engine's stream usage (one Xoshiro stream per island, consumed sequentially by particles).
2. Lemma U: uniform log-BF expansion over bounded-size sets (EXP' Thm 1 generalised; shared lemma).
3. Phase-2 premises: truth deletion, UDEL, NL0 -> partner-graph condition PG; counterexample (equicorrelated nulls).
4. Phase-1 premises: BTP replaced by pointwise addability (new Prop B1'); TS; TL; look-alike family defect.
5. IND-M via start concentration on a reference S0-degree (S°).
6. LH family (W1-EXP Thm 5): discharge everything that can be discharged; numerics at p = 20.

## Log
- IND-T: engine uses one xoshiro stream per island, particles consume sequentially at state-dependent rates.
  Stopping-time lemma => independence under EX-S. Last stage round (phi_T = 1) is after the last resampling: H' = L+5.
- Lemma U = EXP' Lemmas 1.1-1.4 with the block restriction removed (they never used it). Numerics max|R| ~ 0.8.
- NL0 counterexample: equicorrelated nulls. Asymptotics far away for the max (log factors; n ~ 1e11), but the SUM
  Lambda_2(1) visibly does not decay (3.8-7.7) while block nulls decay. Corrected my first claim (sum of probabilities,
  each <= 1).
- B1': pointwise addability via uniform argmin of arrival times; BTP dropped. PA needs only SE + BM-inf.
- [B] family defect: neighbour-graph A includes group-mates of the PRESENT partner hub (symmetric union), useless;
  junk-for-useless-look-alike swaps exit with O(1) prob. Fixed with monotone look-alike map (Theorem B#).
- LH: TS, ZJL, CS, GS proved from the population algebra (xi = part of x_b orthogonal to x_a; xi ⊥ C_a). FS
  substitutes are cross-pair (added masked hub <-> other pair's hub / look-alikes), D' = 4 at config B; neighbour gap
  0.168; ULR 0.0137 (numerical only).
- IND-M: reference bound beta_I <= (1-pi0(S°)) + 1{S° bad} pi(S°)/(pi(W)pi0(S°)); bad iff W meets M (x ⊇ S°).
  Open: superset starts.
