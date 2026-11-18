# BRIEF SL1 — statement lock, W3-RM2-R (Sol, gpt-6.1-sol, reasoningEffort high; fresh, blind first read)

You are the statement-lock reviewer for ticket W3-RM2-R (Theory Wave 3, Tier B rider). You have not seen this ticket
before. Work read-only in the worktree `/home/fb31/BVS-wt/W3-RM2-R` (all paths below are relative to it). Write
nothing except your reply; do not change git state.

## Your job
Check the delta statement and the plan against the sources: right target, faithfully stated, every hypothesis
explicit, every "takes X from PARENT at file:line" pointer correct, every implication claimed in the dependency table
true, and the plan viable (each planned proof step actually works with the stated constants). Try to **break** it:
find a clause that claims more than the sources and the plan can give, a constant that is wrong, a quantifier that is
off, a code fact that is false at the pinned code. A finding blocks only on correctness, strength or faithfulness
(PROTOCOL_v4 §0); mark others editorial.

## Files to review (the ticket)
- `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (delta, v0.1)
- `Theory_work/Wave3/W3-RM2-R/PLAN.md`
- `Theory_work/Wave3/W3-RM2-R/TARGET.md` (context only)

## Sources the statement consumes (read the parts it cites)
- PARENT: `Theory_work/Wave3/W3-RM2/STATEMENT.md` (v1.4), `lemmas/L0_toolkit_b.md` (constants C_R, (T4)),
  `lemmas/L1_sandF_b.md` (sandwich; Step 2(a) uses visibility), `lemmas/L2_width.md` (§4 Lemma TL-W, identity (4.1);
  Lemma d), `lemmas/L3_assemblyF.md`, `lemmas/L6_examples.md` E4 (lines 330-384).
- RM: `Theory_work/Wave3/W3-RM/STATEMENT.md` (§1 lines 32-68; RM-0 lines 160-176), `lemmas/L0_core.md`.
- GROW: `Theory_work/Wave1C/C-GROW/STATEMENT.md:84-88` ((H0)), `lemmas/L1_descent.md` (L1.1, L1.2).
- Theorem 1 with BM(c): `Theory_work/State_of_Project/sections/04_theory.tex:768-790` (TH09 card),
  `Theory_work/Wave3/W3-POST/STATEMENT.md:55-100`.
- Delivery: `Theory_work/Wave1C/C-DLV/STATEMENT.md`, `lemmas/L1_resources.md`, `lemmas/L2_degenerate.md`,
  `lemmas/L4_delivery.md`; `Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md`; `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`.
- Code as pinned (this branch): `Scripts/SMC_BVS/core/` — in particular `v3_fit.R`, `v3_calib.R` (fallback grid,
  lines ~120-124 and ~141-185), `v3_run.R`, `cpp/v3_core.cpp`, `cpp/v3_engine.h`.
- Motivation (what the change is meant to deliver): `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md` rows/sections T2 and
  T4; `Theory_work/Wave3/API_AUDIT/sharp1b/TRIAGE.md` (T2(c), lines 14-35 and 78-81);
  `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` rows W3-RM2:RM2-F and W3-RM2:Ex-Proxy (lines 45-48) and line 74.
- Registry statuses: `Theory_work/INFRA/registry/claims.tsv` (grep the ids named in STATEMENT §6).

## Points to check in particular (not conclusions — check them yourself)
1. (V♭): does Step 2(a) of the sandwich go through with a fixed M_V > M_V⁰ as defined, and is (V) used anywhere
   else in the Form F route?
2. (BM-W⁺): does Lemma TL-W go through with exactly the two inequalities and c_TL⁰ as defined? Is (BM-W) ⇒ (BM-W⁺)
   and (BM-Q♭) ⇒ (BM-W⁺) correct?
3. (T1-F♭): is BM(c) really part of the hypothesis list of SOP:TH09 (not only of another card), and does Theorem 1
   under BM(c) give [POST] as RM2's assembly uses it? Is BM-∞ used anywhere else in RM2-F's route?
4. RM0-plus (a′): do L1.1–L1.2 use NA/TL only at sets in the down-closed family? (b⁺): does the RM-0(b) proof use
   π(S₀) > ½ only through uniqueness of the F-maximiser? (c⁺): is "valid non-degenerate input w.p. one" right for
   Settings F and R?
5. DLV-0: at the pinned code, is every exit of `v3_fit` excluded by the input conditions, EX-A, (D)? In particular the
   tier-1 grid fallback, the `e == 1` condition, the `v3_check_grid` test on the fallback, the escalation preflight,
   the LS0 cap arithmetic, `no_predictors`. Is DLV-0 provable as a re-audit (no new mathematics), as PLAN says?
6. Ex-Proxy-d: is the bound in (a) right; are (b), (c) right, and is κ₀ enough for every clause?
7. Dependency table: does each new claim imply the parent claim named?
8. Is anything in BRIEF's targets missing or mis-stated (`Theory_work/Wave3/W3-RM2-R/BRIEF.md` §Targets)?

## Reply format
1. Verdict: LOCK / LOCK WITH CHANGES / DO NOT LOCK.
2. Findings, numbered, each tagged C (correctness), S (strength), F (faithfulness) or E (editorial), each naming the
   STATEMENT/PLAN line and saying exactly what fails and the fix.
3. Per-point answers to 1–8 (one short paragraph each).
4. Optional suggestions (clearly marked non-blocking).
