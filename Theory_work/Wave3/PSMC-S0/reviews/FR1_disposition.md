# FR1 — disposition (lead, PSMC-S0)

Verdict received: FIDELITY-VERDICT: FAIL (Sol, `FR1_fidelity_sol.md`). All findings accepted; none touches the D-7
leader-store verdict or the "any N / any frozen 𝓒" confirmations, which FR1 confirmed on the proofs.

| # | finding (tag) | disposition | where fixed |
|---|---|---|---|
| 1 | Thm D (ii) equivalence fails with fallback on (S) | ACCEPT. (ii) is for the unpatched law; carry Prop F for delivery; construction failure diagnostic | AUDIT_CAL §0, row 1 |
| 2 | "only p ≤ 17 ever enumerated, whatever n" false (C) | ACCEPT. Now "fixed p ≤ 17 eventually enumerated; fixed p ≥ 18 eventually SMC"; C-GROW remark "for large n" | AUDIT_N §0, rows 9, 10, T-N-4 |
| 3 | TH06 draw-count orders unsupported (C) | ACCEPT. Exact count N_e(1+T+L+4) ≥ N_e(L+6); no order claimed | AUDIT_N row 4 |
| 4 | TH08(c) LS0 cap mismatch (S, inherited) | ACCEPT. Recorded as independent of OD-1; T-N-2 splits the counts | AUDIT_N row 5, T-N-2 |
| 5 | "a fortiori" resources need the A1 amended allocation (S) | ACCEPT | AUDIT_N row 8; AUDIT_CAL §0, rows 4, 6 |
| 6 | D2 / L2 S.3 omitted; `escalation_blocked` flag omitted (M) | ACCEPT. Row 15; tier-0 freeze must install the grid (Engineering requirement) | AUDIT_CAL §0, rows 12, 15 |
| 7 | Missing consumers (M) | ACCEPT. Delivery consumers (FAC-B/PK/S5/X/XA), grid lemmas, CC6, C-ENG inventories, SoP CJ06/OB11/CJ19/OB15, TH17, W2-APP family map, method rows 629/631/643/695 | AUDIT_CAL rows 4, 16–20; AUDIT_N rows 10, 12, §0 |
| 8 | Preprocessing citations; H = 512 unsourced (C) | ACCEPT. Lines 25-26, 30; H = 512 labelled assumed (OWNER_DECISIONS.md:161); H added to the tier question | AUDIT_N opening, §0 |
| 9 | `v3_fit.R:165-169` range short (C) | ACCEPT. 165-170 | AUDIT_CAL row 12 |

No second fidelity read: the ticket is closed at Part 1 by the manager's scope change (theory stays at p = 10⁴), and
the corrected items are inventory additions and wording, not new verdicts. The manager may order a re-read.
