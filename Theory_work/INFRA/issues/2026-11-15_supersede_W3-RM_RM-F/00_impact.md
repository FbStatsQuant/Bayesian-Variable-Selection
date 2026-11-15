# supersede W3-RM:RM-F (by W3-RM2:RM2-F)

- reason: card 1 (W3-RM -> W3-RM2): W3-RM2:RM2-F implies W3-RM:RM-F (implies W3-RM:RM-F = claim W3-RM2:Cont-F ((C4), Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240), accepted by both council seats: Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md:45 and Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md:192 (re-checked :212); (C4) covers both hypothesis routes of RM-F, (N-chi) and (N-D): Theory_work/Wave3/W3-RM2/reviews/LC1B_L2L3_check_sol.md:39 (item 14, containment of RM-F VERIFIED), Theory_work/Wave3/W3-RM2/reviews/SW1_sweep_astra.md:51). approver: HQ consultant (Fable 5.2) AGREE on card 1, 2026-11-15, under PROTOCOL_v4 H5 (replaces the owner approval of LIFECYCLE §0); recorded per Theory_work/Wave3/ACCEPTANCE/RECORD_BRIEF_2026-11-15.md. Conditions match in substance (TH09 / W2-APP:POST); W2-APP:POST@1.0.1 is unchecked (weak point). RM-0 and E4 stay ACTIVE.
- (C1) Theorem RM-F (fixed design) [W3-RM] v1.0.0 state ACTIVE; status `PROVED-CHECKED`
- replacement W3-RM2:RM2-F: Theorem RM2-F (fixed design, polynomial leakage) state ACTIVE; status `PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefdd`
- axes (Y vs X): {'assumptions': 'incomparable', 'conclusion': 'equal', 'rate': 'unknown', 'scope': 'unknown'} -> **undetermined**
- decision-rule class: **free**

## Statement diff

- hypotheses ADDED (each dependent must now verify them or the property it consumes): A:RM2-BM-W (RM2 signal floor at the truth-removal width (BM-W)), A:RM2-LFEAS-GAIN (RM2 (L-feas) + (L-gain), fixed design), A:RM2-LSIZE-B (RM2 polynomial leakage size (L-size^b), fixed design), A:RM2-W (RM2 lattice width (W))
- hypotheses DROPPED: A:RM-L (RM-L), A:RM-N (RM-N)
- consumes: `P:SAND@W3-RM:B2; P:SAND@W3-RM:B2tau; P:NA-TL@W3-RM:B3; P:NA-TL@W3-RM:NA-F; P:NA-TL@C-GROW:L2.3; P:POST-CONC@SOP:TH09` -> `—`
- conclusion: `reported-model: P(𝒪∩{Ŝ⁺≠S0})→0 for every seed, N_e, R′ and calibration outcome (no delivery claim)` -> `reported-model: one data event of probability -> 1 on which every admissible output run reports S0`
- rate: `—` -> `none claimed`
- scope: `fixed design; s0 fixed; p ≤ n^A; |Q| ≤ (log n)^κ; any partition with blocks ≤ 16; shipped LS0 configuration` -> `fixed design; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b`
- method_commit: `2252d57` -> `—`
- statements: Theory_work/Wave3/W3-RM/STATEMENT.md:178-185 -> Theory_work/Wave3/W3-RM2/STATEMENT.md:206-214

## Rebuild cost

- free: 2 re-point(s) PROPOSED (one cheap check each), no rebase, no re-review

| dependent | uses | action |
|---|---|---|
| W3-RM2:Cont-F | stmt | propose re-point |
| W3-RM:Examples | stmt | propose re-point |
