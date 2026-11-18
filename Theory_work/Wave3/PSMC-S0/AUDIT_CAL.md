# AUDIT_CAL — T-CAL preliminary: bounded calibration (OD-2(c)) and final-run leader stores (OD-13 / D-7)

PSMC-S0 Part 1, Theory Department, 2026-11-15. Lead: Claude Opus 5.5 (high). Premise audit only; no statuses asserted.
Code of record: `Scripts/SMC_BVS/core/` on this branch (cut from `origin/main`).

**Change audited (OD-2(c); ENGINEERING_SPEC §4.2 row "bounded calibration").** v3.1 escalates once to tier 1
(N, H, T × 4) if any of seven triggers fires: E1, E2, E3, forced pilot steps, grid failure, `grid_unconverged`,
`local_limit` (`v3_calib.R:60-61` trigger list; E1/E2 `:101-102`; rebuild loop of at most ℓ iterations `:85-117`;
`grid_unconverged` `:118`; escalation on any trigger `:154-158`; tier-1 fallback grid `:120-125`, `:163-169`).
OD-2(c): no escalation except grid-construction failure; at most I_max rebuilds, then freeze the last grid with the
flag `grid_unconverged`; all triggers still recorded; the C-DLV tier-1 fallback is kept. Class C (changes the frozen
calibration only).

## 0. Verdict (plain words)
- **Every result stated "for any frozen calibration 𝓒" needs nothing under OD-2(c)** (N1, LT♯, C, TR, finite parts of
  D, RM-0/RM2, TH01(a)–(i), TH04, TH05(0)). They condition on the frozen record on the success event 𝒜 and use only
  that 𝓒 is a function of the calibration randomness, frozen before final randomness. OD-2(c) keeps both
  (SPEC §4.3: "R′ and N are fixed in the manifest before any final address is read. No final quantity triggers a
  rerun"). The coded rule already freezes an unconverged grid at tier 1 (`v3_calib.R:118, :126` return the last
  successful construction even when `grid_unconverged`); OD-2(c) does the same at tier 0 after I_max rebuilds.
- **C-DLV (delivery) survives, and gets easier.** It uses escalation in the walk "a tier-0 construction failure forces
  escalation" (`C-DLV/lemmas/L4_delivery.md:31-34`) and in L2 S.3's exclusion of D2 `grid_failure_no_escalation`
  (`C-DLV/lemmas/L2_degenerate.md:37-40`) [FR1]; OD-2(c) keeps both. Theorem D (ii)'s identification "construction
  failure ⇔ `schedule_limit`" is a statement about the **unpatched** law; with the fallback on, a tier-1 construction
  can fail and calibration still return ok (`v3_calib.R:163-170`) [FR1]. The delivery result to carry is
  Proposition F: with the tier-1 fallback and the amended CONFIG/allocation of
  `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md:9-12` (needed for the current LS0 cap ℓ + |S̃₀|, independent of
  OD-2) [FR1], P(no output) = 0 holds by the same proof; construction failure becomes a diagnostic event. The open obstruction (O) becomes moot for
  the method with the fallback, and its route (O-a) weakens from "no tier-0 trigger fires" to "no tier-0 construction
  fails".
- **No registered theorem reads E2, the tier, `grid_unconverged` or grid convergence as a hypothesis or conclusion.**
  The items that mention them are: rebuild/escalation counts in TH07(a) and TH08(b) (deterministic caps that hold a
  fortiori with I_max ≤ ℓ); the open obligation OB05(b) and future-work item CJ17 (not claims); and v3.1 empirical
  records (escalation columns in SoP §3 tables, P6, B3) that describe v3.1 and must not be pooled with large-p runs.
- **One premise to carry: the production binary is new code.** C-DLV's Theorem D rests on a code-reading inventory of
  every no-output exit of v3.1 (P1, `C-DLV/STATEMENT.md:52-53`) and on Lemma R's resource count. Both must be redone
  for the production binary (new exits: process islands, checkpoints, the merge, internal_error invariants). That is
  an engine audit, not a calibration premise; proposed follow-on T-DLV (below).
- **Leader stores (D-7): SAFE TO DROP from final islands and from the output**, provided the calibration leader
  stores still feed (i) the candidate set V and (ii) the inherited models offered to the final run (§3).
- **Small requests to Engineering:** require I_max ≤ ℓ = ⌈log₂(n+p+1)⌉ (true at the spec default I_max = 3, since
  n ≥ 3 gives ℓ ≥ 3), so that every "≤ ℓ rebuilds per tier" statement keeps holding; and say whether a failed tier-0
  rebuild construction escalates (as coded, `v3_calib.R:114` then `:154`) or freezes the last successful tier-0
  construction. Either choice keeps delivery, **provided** the freeze variant actually installs that grid: as coded, a
  failed construction clears the tier grid (`v3_calib.R:126`) and, without escalation, the wrapper returns D2
  `grid_failure_no_escalation` (`v3_calib.R:170`), a no-output exit [FR1].

## 1. Items that read E2, the tier, escalation, `grid_unconverged` or grid convergence

| # | item (id@version) | where (file:line) | what it reads | effect of OD-2(c) | action / effort |
|---|---|---|---|---|---|
| 1 | C-DLV Theorem D (`C-DLV:Thm-D`@1.0.0, PROVED-CHECKED relative to P1/P3 audits) | `C-DLV/lemmas/L4_delivery.md:13-22`; escalation used at `:31-34` ("a tier-0 construction failure forces escalation"; `schedule_limit` iff tier 1 and a construction failed) | escalation rule and tier-1 status | (i) and (iii) unchanged; (ii) unchanged in form: 𝒮ℒ_n = {escalation to tier 1 and some tier-1 construction fails}, but under OD-2(c) escalation happens only after a tier-0 construction failure, so 𝒮ℒ_n is reached by fewer paths. The proof walk needs one new step: the tier-0 loop stops at I_max and freezes a successful construction (`L3` Lemma 3.4 gives validity) | re-walk L4:24-40 for the bounded rule; state (ii) for the unpatched law only — with the fallback, construction failure is diagnostic, not `schedule_limit` (`v3_calib.R:163-170`) [FR1]: 1 h |
| 2 | C-DLV (C1) conditional delivery (`C-DLV:C1-CondDelivery`@1.0.0) | `C-DLV/STATEMENT.md:68-74` "E_n = {some tier-0 trigger fires}" | tier-0 triggers | stronger: E_n shrinks to {some tier-0 construction fails}. The measured remark "in all 134 production fits no tier-0 trigger fired" (`:74`) is a v3.1 record (and B3 shows triggers fire at p ≥ 5k, REQUESTS R6) | restate E_n: 0.25 h |
| 3 | C-DLV Proposition F (`C-DLV:Prop-F`@1.0.0, headline flag; PROVED-CHECKED for the patched calibration law) and its implementation `C-ENG:Impl-DLV-B`@1.0.0 | `C-DLV/lemmas/L4_delivery.md:79-91`; code `v3_calib.R:120-125, :141-143, :163-169` | tier-1 fallback after a tier-1 construction failure | **holds unchanged** if the production engine keeps the tier-1 fallback (OD-2(c) says "C-DLV fallback kept"). The proof's other inputs (Lemma R stage cap; validity of a frozen pilot schedule) do not depend on the trigger set | confirm in WP4 code review that the fallback is implemented as in `v3_calib.R:122-124`: Engineering |
| 4 | Delivery consumers through `P:NO-OUTPUT-ZERO` / total fallback: `W2-FAC-A:Prop-F-FAC`@1.0.0 (headline flag), `W2-FAC-A:Thm-FAC-L`, `W2-LOC2:F-LOC2(.exp,.poly)`, `W2-UNI:F-UNI`@1.1.0; HQ audits A1/A2/A4, B1; [FR1] also `W2-FAC-B:Thm-FAC-CS`, `:L5` (`W2-FAC-B/STATEMENT.md:127`), `W2-FAC-PK:Thm-FAC-PK` (`W2-FAC-PK/STATEMENT.md:79`), `W2-FAC-S5:Thm-FAC-BCS-R`, `:L5`, `:L5.C4-R` (`W2-FAC-S5/lemmas/L5_assembly.md:39`), `W2-FAC-S5:KL` (OPEN; conditional delivery, `W2-FAC-S5/STATEMENT.md:125`), `W2-FAC-X:Thm-FAC-CS-iid`, `:X6`, `:X6.X6.4` (`W2-FAC-X/STATEMENT.md:93`; `lemmas/X6_assembly.md:58`), `W2-FAC-X:Thm-FAC-GL`, `:X10` (`STATEMENT_T2.md:62`), `W2-FAC-XA:X4` (`W2-FAC-XA/STATEMENT.md:85`) | `W2-FAC-A/lemmas/L7_delivery.md:22-24`; depends_on rows in `claims.tsv` | P(no output) = 0 from Prop F | **unchanged** if Prop F transfers with its amended premises (A1 allocation); each keeps its own premise and status qualifications [FR1] | none |
| 5 | C-DLV open obstruction (`C-DLV:O`@1.0.0, OPEN) | `C-DLV/STATEMENT.md:79-84` route (O-a) "no tier-0 trigger (E1–E3, forced pilot steps, grid failure/unconvergence, local_limit) w.p. → 1" | all seven triggers | route (O-a) becomes "no tier-0 construction fails"; with the fallback, (O) is not needed for delivery | note only |
| 6 | C-DLV Lemma R / Cor R (`C-DLV:L1-R`, `:Cor-R`@1.0.0) | `C-DLV/lemmas/L1_resources.md:9-10, :47-53` ("≤ ℓ rebuilds", N̄ = 4N₀ with escalation) | rebuild count and escalated budgets | in the rebuild count: holds a fortiori if I_max ≤ ℓ; the envelope must be the amended A1 allocation (`HQ_AUDIT/A1_propF_redteam.md:9-12`) for the current LS0 cap [FR1] | none, given I_max ≤ ℓ |
| 7 | TH07(a) STG (`SOP:TH07.a`@1.0.0) | `04_theory.tex:639` "build_grid terminates, every appended point has ρ_V ≥ 0.9, ≤ ℓ rebuilds per tier; T ≤ T_e on success"; note `:632` | rebuild cap, T ≤ T_e | holds (I_max ≤ ℓ; T_e per tier unchanged) | none |
| 8 | TH08(b) Prop D calibration work (`SOP:TH08.b`@1.0.0) | `04_theory.tex:714` "I_e ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation)" | rebuild count, escalation | holds as a bound; the restatement (AUDIT_N T-N-2) should read I_e ≤ I_max per tier, at most two tiers only after a construction failure | inside T-N-2 |
| 9 | TH03 premise H4 (CAL) (`SOP:TH03`@1.0.0) | `04_theory.tex:320` "calibration uses streams 0-9 only … and escalation precedes final randomness" | timing of escalation | holds (escalation, when it happens, still precedes final randomness; stream names are T-STREAM) | none |
| 10 | Obligation OB05(b) calibration contract (`SOP:OB05`@1.0.0, OPEN) | `theory_supp.tsv:19` "(b) OPEN: rebuild convergence, P(S₀ ∈ V), P(schedule_limit), P(grid_unconverged), as-coded masked T_n" | convergence and failure probabilities | P(grid_unconverged) and rebuild convergence stop mattering for delivery (the flag no longer escalates); P(S₀ ∈ V) and T_n stay open. Not a claim | note only |
| 11 | Future work CJ17 (`SOP:CJ17`) | `registry_future.tex:22` "positive power of the E1/E2/E3 and low_empirical_ESS flags" | diagnostic flags | still meaningful: all triggers are still recorded under OD-2(c), and the final-run flags E1/E2/E3 (`v3_run.R:202-205`) are untouched | none |
| 12 | Output flags `escalated`, `escalation_blocked` [FR1], `checks_passed_calibration`, `grid_unconverged`, `calibration_triggers`, `grid_fallback` | code `v3_calib.R:177-183`; `v3_fit.R:165-170` [FR1]; final-run flags `v3_run.R:202-205` | — | reporting only; no theorem takes any of them as hypothesis or conclusion (registry grep: no ACTIVE claim mentions them outside the C-DLV/C-ENG rows above). Under OD-2(c) `escalated` = TRUE means "a tier-0 construction failed", a different event from v3.1's; it should be documented as such | Engineering/Writing note |
| 13 | v3.1 empirical records that read escalation: SoP §3 (`03_empirics.tex:397, :400, :443`), tables `emp_highp_cost.tex:8`, `emp_highp_flags.tex:8` (escalated column); P6 probes (`W3-P6/DESIGN.md:52-57`); B3 census (REQUESTS R6 answer) | as cited | escalation rates and grid convergence of v3.1 | true of v3.1. They describe a different calibration law from the large-p method: never pooled with, or quoted as properties of, OD-2(c) runs | Writing note |
| 14 | W3-SAMP setting: 𝒜 = {SMC branch and `v3_calibrate` returns "ok"} (`W3-SAMP/STATEMENT.md:38-42`) | success event | under OD-2(c) "ok" also covers "tier 0, I_max reached, grid frozen with `grid_unconverged`" — already "ok" in v3.1 at tier 1. Every claim is "given 𝓒 on 𝒜" or intersected with 𝒜, never conditional on 𝒜 (`:30-36`), so a larger 𝒜 changes no statement | none |
| 15 | [FR1] C-DLV L2 S.3, exclusion of D2 `grid_failure_no_escalation` (`C-DLV:L2-S3`@1.0.0, AUDITED) | `C-DLV/lemmas/L2_degenerate.md:37-40` | "a tier without a grid had a failed construction … since e = 0, the loop either escalates … or stops with `resource_limit`" | holds under OD-2(c) as long as a tier-0 construction failure still escalates; a freeze-at-tier-0 variant must install the last successful grid (`v3_calib.R:126, :170`) or D2 becomes reachable | Engineering requirement (§0) |
| 16 | [FR1] C-DLV grid lemmas `C-DLV:L3-3.3`, `L3-3.4`, `L3-3.5a`, `L3-3.5b`, `Cor-5.3`@1.0.0 | `C-DLV/lemmas/L3_grid.md:30, :42, :61, :68`; `L5_insertions.md:79` | tier pilot schedule, T_e cap | component statements survive (T_e per tier unchanged); they describe constructed grids, not fallback grids — keep the distinction | none |
| 17 | [FR1] W3-SAMP CC6 production stage cap (`W3-SAMP:CC`@1.1.1) | `W3-SAMP/lemmas/CC_code_check.md:94` | T ≤ T_e including the tier-1 fallback | holds (fallback kept; T_e unchanged) | none |
| 18 | [FR1] C-ENG implementation inventories `C-ENG:Impl-LS0-preflight`, `C-ENG:Impl-Merge`@1.0.0 | `C-ENG/REPORT.md:73, :29` | escalation preflight; implementation inventory | v3.1 implementation records; the production binary needs its own (T-DLV) | Engineering |
| 19 | [FR1] SoP obligations/future work `CJ06`, `OB11`, `CJ19`, `OB15` | `theory_supp.tsv:37, :50`; `04b_supplement.tex:1116, :1204` | rebuild convergence, cap non-binding, calibration work/depth | not claims; under OD-2(c) rebuild convergence no longer drives escalation; calibration work bounded by I_max | note only |
| 20 | [FR1] Method text: `02_method.tex:629, :631, :643, :695` | H₀ and calibration/final ratio; tier, forced-step, convergence and trigger rules; end-to-end escalation description | v3.1 rules | true of v3.1; large-p method needs version-specific wording | Writing note |

## 2. Confirmation: "for any frozen calibration 𝓒" results need nothing under OD-2(c)

What these results use from calibration (premise CAL, `W1-N1/STATEMENT.md:29-30`; `04_theory.tex:116` "CAL: 𝓒 frozen
on streams 0–9"): (a) 𝓒 (grid, tier, N_e, L, R′, …) is σ(calibration randomness)-measurable and frozen before any
final randomness; (b) the grid is valid (0 = φ₀ < … < φ_T = 1, T ≤ T_e). OD-2(c) changes the *map* from calibration
randomness to 𝓒, not (a) or (b): the frozen grid is always a successful construction (L3 Lemma 3.4) or the C-DLV
fallback (valid by `L4_delivery.md:85-87`), and SPEC §4.3 freezes the manifest before final addresses are read.

| claim@version | quoted text showing "any frozen 𝓒" | file:line |
|---|---|---|
| `W1-N1:Thm-N1`@1.0.0 (N1) | "Calibration record 𝓒 (grid, tier, N_e, L, R′ and every other setting the final run uses) … all are σ(𝓒)-measurable and frozen before stream 10" | `Theory_work/Wave1/W1-N1/STATEMENT.md:29-30` |
| `W3-SAMP:LT#`@2.0.1 | "(LT-e) … with no condition on 𝓒 beyond 𝒜" | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:136-138` |
| `W3-SAMP:C`@1.1.1 | "given 𝓒 on 𝒜 … any frozen parameters (any valid grid, any T ≥ 1, any N_e ≥ 1, any L ≥ 0)" | `W3-SAMP/STATEMENT.md:149-150` |
| `W3-SAMP:TR`@2.1.1 | "any frozen parameters … with no condition on Ẑ, the bridge, N_e or the grid (no condition on 𝓒 beyond 𝒜)" | `W3-SAMP/STATEMENT.md:165, :171` |
| `W3-SAMP:D`@2.1.1 | "given 𝓒 on 𝒜, for the potential run" (finite parts for any frozen parameters, `:43-46`) | `W3-SAMP/STATEMENT.md:97-105` |
| `W3-RM:RM-0`@1.0.0 | "pathwise, for every seed, N_e, R′ and calibration outcome … CAL is not used for (b)" | `Theory_work/Wave3/W3-RM/STATEMENT.md:168, :175` |
| `W3-RM2:RM2-F`@1.0.0 | "every admissible output run — every seed, N_e, R′ and calibration outcome" | `Theory_work/Wave3/W3-RM2/STATEMENT.md:209` |
| `SOP:TH01.c`@1.0.0 | "(a),(b) hold conditionally on any successful frozen 𝓒" | `State_of_Project/sections/04_theory.tex:117` |
| `SOP:TH05.0`@1.0.0 (headline) | "v3.1 with LS0 … any frozen grid; pooling not involved" (registry fidelity note) | `State_of_Project/registry/theory_main.tsv:6` |
| `SOP:TH04`@1.0.0 | "coded grid: yes (no grid hypothesis)" | `04_theory.tex:429` |
| `C-DLV:Cor-Dp`@1.0.0 | "for either calibration law … CAL is not used" | `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:70-77` |

Stream labels "0–9 / 10–13" in these premises become address ranges under position-addressed streams; that is
T-STREAM (O5, O18), not T-CAL.

## 3. D-7 (OD-13): does anything consume the final-run leader stores?

**Code path.** The ledger keeps three stores, offered independently: top-(40p+1) by F, top-20p by log γ₀ (`lead0`),
top-20p by log γ₁ (`lead1`) (`cpp/v3_ledger.h:72, :78`); `offer_stores` updates the HPM, `top`, `lead0`, `lead1`
separately (`v3_ledger.h:89-94`), so the HPM and the top store never read the leader stores.
- **Calibration side (keep):** the calibration leader stores enter V (`cpp/v3_core.cpp:707-708`, `cpp_cal_V`; this is
  C-DLV's "S₀ ∈ V persistence (leader store keeps the γ₁-maximiser)", `C-DLV/PLAN.md:13`) and the **inherited** set
  exported to the frozen object = top ∪ lead0 ∪ lead1 of the calibration ledger (`cpp/v3_core.cpp:725-736`;
  SoP `02_method.tex:357-359`). The final run offers every inherited model to its own stores and HPM
  (`cpp/v3_core.cpp:418-428`); W3-SAMP Lemma PC (iii) counts these inherited models in the offered set 𝓜
  (`W3-SAMP/STATEMENT.md` §2 Lemma PC).
- **Final-run side (droppable):** the final ledger's `lead0`/`lead1` are read only by `ledger_to_list`
  (`cpp/v3_core.cpp:366-367`, called at `:510`), which copies them to the output fields `leaders_gamma0` /
  `leaders_gamma1` (`v3_run.R:210`). No later code reads those fields (grep of `Scripts/SMC_BVS/`: only `v3_run.R:210`).

**Theory side.** No ACTIVE registry row mentions leader stores (grep of `claims.tsv`). Mentions in theory files:
`02_method.tex:357-359` (inherited calibration stores, calibration side), `:486` and `:648` (settings rows; row 34's
"near-ties, Z_𝒯 and the card read it" refers to the top store: TH04's 𝒯 and DIST-C's 40p + 1 store), `C-DLV/PLAN.md:13`
(calibration side). Test harnesses `C-ENG/tests/compare_regress.R:92`, `compare_replay.R:30` compare `leaders_gamma*` as
regression fingerprints only (compat mode keeps them, SPEC §4.1 class B). W3-DIST (in progress, not touched) has no
"leader" mention in its folder.

**Verdict for CP1: SAFE TO DROP** the final-run leader stores from final islands and from the output, **on one
condition**: the calibration leader stores must still (i) feed V and (ii) be exported into the inherited model set that
the final run offers to its top store and HPM (`v3_core.cpp:732-733` → `:418-428`). Dropping (ii) would change the
offered set 𝓜, hence possibly the reported HPM and the top store (a class Δ change, not a reporting change). SPEC §4.2
row "table and inherited models offered at the merge" keeps (ii) as long as "inherited" still means top ∪ lead0 ∪ lead1
of the calibration ledger.

## 4. Proposed follow-on (T-CAL full, by 12-04) and one new engine-audit ticket
| ticket | content | tier | hours | consumes |
|---|---|---|---|---|
| T-CAL (full) | delta statement of C-DLV Thm D (ii) and (C1) for the bounded rule; Prop F re-walk; I_max ≤ ℓ as a stated method requirement | B (rider of C-DLV) | 3 | C-DLV:Thm-D, C1, Prop-F, L1-R; SPEC calibration section once frozen |
| T-DLV (new) | inventory of every no-output exit of the production binary and its resource envelope (C-DLV P1 + Lemma R analogue), so that Prop F and every `P:NO-OUTPUT-ZERO` consumer transfer | B (code audit; Sol code read) | 6–8 | production code at WP4/WP5 freeze (≈ 12-04) |

## FR1 dispositions (Sol fidelity read `reviews/FR1_fidelity_sol.md`; dispositions `reviews/FR1_disposition.md`)
Edits marked [FR1]: Theorem D (ii) restricted to the unpatched law; Prop F carried with the amended A1 allocation;
D2 / L2 S.3 and the tier-0 freeze requirement added; delivery-consumer list completed; grid lemmas, CC6, C-ENG
inventories, SoP obligations and method-text rows added; `escalation_blocked` flag and `v3_fit.R:170` added.
The leader-store verdict (§3) and the "any frozen 𝓒" confirmations (§2) were confirmed by FR1.
Asymptotic conclusions of the §2 results still need their stated concentration, non-collapse or overlap premises;
those are not automatically established for a changed calibration law (FR1).
