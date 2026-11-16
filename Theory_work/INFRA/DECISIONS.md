# Decision log

Every SUPERSEDE / COEXIST / DECLINE / REMARK decision, every RETRACT / NARROW / DEPRECATE, and every failed
sharpening attempt (a failed attempt to remove or weaken an assumption counts as weak necessity evidence). Rules:
`LIFECYCLE.md` §5. `propagate.py` appends entries automatically; the human rationale goes into the PR that carries
the registry change. Newest entries at the bottom. Format:

```
## <date> — <KIND> <X> [/ <Y>]
- decided by: Felipe | HQ
- reason: ...
- axes (Y vs X): assumptions=…, conclusion=…, rate=…, scope=…
- class / price / key-step check / restored / failed removal count ...
```

## Seeded entries (narrowing decisions already taken inside Wave 1C–2 tickets; recorded 2026-11-09 by INFRA)

## 2026-11-09 — NARROW (historical) W2-FAC-A:Thm-FAC-L
- decided by: the ticket under the wave protocol, flagged to HQ (REPORT flag 1)
- reason: proved for one global factor + bounded local blocks under limsup log p/log n < α₀(κ̄) (= 1/6 for block
  compound symmetry), not for p ≤ n^A; Proposition SHARP shows 1/6 is optimal for the full-lattice route
- source: Theory_work/Wave2/W2-FAC-A/REPORT.md:3-8

## 2026-11-09 — NARROW (historical) W2-FAC-X:Thm-FAC-CS-iid
- decided by: the ticket, flagged to HQ
- reason: Target 1 holds up to log p/log n < 1/2; uniform-over-n (C2)(ii) is false beyond 1/2; Cor FAC-NCS exact-Gram
  (G) branch withdrawn (imported multiplier bound false for exact Gram)
- source: Theory_work/Wave2/W2-FAC-X/REPORT.md:27; lemmas/X7_near_cs_loadings.md:3

## 2026-11-09 — NARROW (historical) C-MIS:Thm-MIS(i)
- decided by: the ticket ("narrowed form in §2")
- reason: target is the exact sparse projection S₀^𝒞 under (EP); examples E1–E3 show the alternatives fail
- source: Theory_work/Wave1C/C-MIS/REPORT.md:23

## 2026-11-09 — COEXIST (historical) C-DLV:Prop-F / W2-FAC-A:Prop-F-FAC, W2-LOC2:F-LOC2, W2-UNI:F-UNI
- decided by: HQ (delivery results proved per design class)
- reason: the Proposition F family is proved class by class (GROW class via HQ audit A2; FAC-A; LOC2; UNI); none
  implies the others, all are kept

## 2026-11-11 — NARROW W3-SAMP:PC

- decided by: HQ
- reason: W3-SAMP sweep SW1 #1 (MAJOR): clause (ii) no longer says the reported HPM is a function of the island records (it is the hpm_better-maximum of the final ledger's offered set M, which also holds tables, inherited models, final local search and LS0); also strengthened: (i) now includes the evaluated-model sets M_r (C1 Opus #1). All dependent uses (completed records, M contains the union of M_r, S-hat = max of M) are still covered; the corrected text passed SW1 and council C1
- 0 dependents SUSPECT; restored: —

## 2026-11-11 — NARROW W3-SAMP:ST

- decided by: HQ
- reason: SW1 #14: ST-c now assumes explicitly the T12 (R3) round path law, realised by the code under EX-A, H-U, KERNEL (W1-N1 Lemma B (B-b)); before, only KERNEL was named. The dependents (C, LT#, TR) all run under the N1 premises, which include EX-A, H-U, KERNEL, so their uses stay covered
- 0 dependents SUSPECT; restored: —

## 2026-11-11 — NARROW W3-SAMP:D

- decided by: HQ
- reason: C1 Opus #2: KERNEL added to Theorem D's hypotheses (used only through the control-flow clause of W1-N1 Lemma B (B-b)); the registry's assumption list already held A:N1-KERNEL. HEADLINE: LIFECYCLE §0 requires Felipe's approval of this NARROW (pending)
- 0 dependents SUSPECT; restored: —

## 2026-11-11 — NARROW W3-SAMP:TR

- decided by: HQ
- reason: SW1 #2 (MAJOR): the honest label's non-nesting claim (TR's premise is neither implied by nor implies pi0(S0)->1) is now stated only for abstract positive targets (three-state example and its converse; not a realisation of the coded target; coded separation open); SW1 #28: the conditioning is island by island on the island's own bridge history. TR-a to TR-d are otherwise unchanged. HEADLINE: LIFECYCLE §0 requires Felipe's approval of this NARROW (pending)
- 0 dependents SUSPECT; restored: —

## 2026-11-15 — SUPERSEDE W3-RM:RM-F / W3-RM2:RM2-F

- decided by: HQ
- reason: card 1 (W3-RM -> W3-RM2): W3-RM2:RM2-F implies W3-RM:RM-F (implies W3-RM:RM-F = claim W3-RM2:Cont-F ((C4), Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240), accepted by both council seats: Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md:45 and Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md:192 (re-checked :212); (C4) covers both hypothesis routes of RM-F, (N-chi) and (N-D): Theory_work/Wave3/W3-RM2/reviews/LC1B_L2L3_check_sol.md:39 (item 14, containment of RM-F VERIFIED), Theory_work/Wave3/W3-RM2/reviews/SW1_sweep_astra.md:51). approver: HQ consultant (Fable 5.2) AGREE on card 1, 2026-11-15, under PROTOCOL_v4 H5 (replaces the owner approval of LIFECYCLE §0); recorded per Theory_work/Wave3/ACCEPTANCE/RECORD_BRIEF_2026-11-15.md. Conditions match in substance (TH09 / W2-APP:POST); W2-APP:POST@1.0.1 is unchecked (weak point). RM-0 and E4 stay ACTIVE.
- axes (Y vs X): assumptions=incomparable, conclusion=equal, rate=unknown, scope=unknown
- class free; key step check: —; dependents: 2 direct

## 2026-11-15 — SUPERSEDE W3-RM:RM-R / W3-RM2:RM2-R

- decided by: HQ
- reason: card 1 (W3-RM -> W3-RM2): W3-RM2:RM2-R implies W3-RM:RM-R (implies W3-RM:RM-R = claim W3-RM2:Cont-R ((C4), Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240), accepted by both council seats: Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md:50 and Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md:197 (re-checked :217); Theory_work/Wave3/W3-RM2/reviews/SW1_sweep_astra.md:51). approver: HQ consultant (Fable 5.2) AGREE on card 1, 2026-11-15, under PROTOCOL_v4 H5 (replaces the owner approval of LIFECYCLE §0); recorded per Theory_work/Wave3/ACCEPTANCE/RECORD_BRIEF_2026-11-15.md. Conditions match in substance (TH09 / W2-APP:POST); W2-APP:POST@1.0.1 is unchecked (weak point). RM-0 and E4 stay ACTIVE.
- axes (Y vs X): assumptions=incomparable, conclusion=equal, rate=unknown, scope=unknown
- class free; key step check: —; dependents: 2 direct

## 2026-11-16 — NARROW W3-MISR:Cor-H

- decided by: HQ
- reason: HQ GO real run (2026-11-16) (task S): NARROW of Cor-H, correctness event. KL reading at STATEMENT.md:191-195 restricted to a deterministic intercept (false for a random intercept: W3-MISR-R reviews/L1_statement_lock_sol.md:7 L1-1, reviews/K1_linecheck_sol.md:7-11 K1-1). Statement-change check: Theory_work/Dept/research/MISR_NARROW/DIFF_sol.md@d890acb5 (Sol DIFF PASS, WEAKER). 0 dependents. HQ GO (Cor-H not headline; HQ authority).
- 0 dependents SUSPECT; restored: —

- 2026-11-16 correctness event (rollback history): W3-MISR:Cor-H 1.0.0 -> NARROWED 2.0.0 -> cleared ACTIVE 2.1.0. Cause: the KL reading (STATEMENT.md:191-195) was false for a random intercept (counterexample L1-1 / K1-1, W3-MISR-R reviews). Statement-change check: Theory_work/Dept/research/MISR_NARROW/DIFF_sol.md@d890acb5 (Sol DIFF PASS, WEAKER). 0 dependents. Erratum: Theory_work/Wave3/W3-MISR/reviews/ERRATA.md. HQ GO (task S).

## 2026-11-16 — SUPERSEDE W3-MISR:Cor-G(a) / W3-MISR-R:CorG-min

- decided by: HQ
- reason: HQ GO real run (task Q, H5 card 10, 2026-11-16): free supersession (CorG-min implies Cor-G(a), STATEMENT §8 row 181, statement lock L1:59)
- axes (Y vs X): assumptions=incomparable, conclusion=equal, rate=equal, scope=unknown
- class free; key step check: —; dependents: 1 direct

- 2026-11-16 correctness event (rollback history, W2-UNI): W2-UNI:F-UNI v1.1.0 ACTIVE -> SUSPECT (status and hash unchanged). Cause: every-n delivery cites Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered by the cited proof (W2-UNI lemmas/L5_delivery.md Step 2 via W2-FAC-A lemmas/L7_delivery.md:35-38 -> C-DLV:Prop-F, method cap ℓ_n, C-DLV lemmas/L4_delivery.md:7,53; W3-RM2-R STATEMENT.md:219). Sol transfer check (manager) decides: erratum + PATCH + clear, or NARROW (task S2). Consumers noted, no status change. HQ GO (task S1).

- 2026-11-16 correctness event (rollback history, HQ_AUDIT-W1C): HQ_AUDIT-W1C:A2, HQ_AUDIT-W1C:A3 ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-A): W2-FAC-A:Prop-F-FAC, W2-FAC-A:Thm-FAC-L ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-B): W2-FAC-B:Thm-FAC-CS, W2-FAC-B:L5 ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-PK): W2-FAC-PK:Thm-FAC-PK ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-S5): W2-FAC-S5:Thm-FAC-BCS-R, W2-FAC-S5:L5, W2-FAC-S5:L5.C4-R ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-X): W2-FAC-X:Thm-FAC-CS-iid, W2-FAC-X:Thm-FAC-GL, W2-FAC-X:X10 ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-FAC-XA): W2-FAC-XA:X4 ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

- 2026-11-16 correctness event (rollback history, W2-LOC2): W2-LOC2:F-LOC2, W2-LOC2:F-LOC2.exp, W2-LOC2:F-LOC2.poly ACTIVE -> SUSPECT (status, hash and version unchanged). Cause: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W. Same event as W2-UNI:F-UNI (task S1). Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4. Issue folder Theory_work/INFRA/issues/2026-11-16_suspect_S3_method-pin. HQ GO (task S3).

## 2026-11-16 — NARROW W2-UNI:F-UNI

- decided by: HQ
- reason: HQ GO real run (task S2, 2026-11-16): NARROW of F-UNI, correctness event. Every-n delivery cited Prop-F's cap-ℓ_n method; shipped cap ℓ_n+|S̃₀| not covered (TR1: transfer NO, Theory_work/Dept/research/FUNI_transfer/TR1_sol.md). Narrowed: (a) delivery under IDEAL-W on the bounded domain 𝔇; (b) every n and P(Ŝ⁺ = S₀) → 1 under A:IDEAL-W⁺. Statement-change check Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md@fc30c749 (Sol DIFF PASS, WEAKER, 1.1.0 -> 2.0.0). Clear to 2.1.0 in S4 with W2-FAC-A:Prop-F-FAC (manager 11-16).
- 6 dependents SUSPECT; restored: —

- 2026-11-16 correctness event (rollback history, W2-UNI): W2-UNI:F-UNI 1.1.0 SUSPECT (task S1) -> NARROWED 2.0.0 (task S2); clear to ACTIVE 2.1.0 in S4 with W2-FAC-A:Prop-F-FAC. Cause: every-n delivery cited Prop-F's cap-ℓ_n method (transfer NO: Theory_work/Dept/research/FUNI_transfer/TR1_sol.md). Narrow: (a) IDEAL-W on 𝔇, (b) A:IDEAL-W⁺ (new assumption; IDEAL-W unchanged). Statement-change check: Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md@fc30c749 (Sol DIFF PASS, WEAKER). UNI-0/UNI-1 stay SUSPECT (S4); SAND-R, SAND-Rp, RM-R, Examples stay SUSPECT via UNI-0 (noted). HQ GO (task S2).
