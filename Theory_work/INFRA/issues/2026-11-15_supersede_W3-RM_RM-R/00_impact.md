# supersede W3-RM:RM-R (by W3-RM2:RM2-R)

- reason: card 1 (W3-RM -> W3-RM2): W3-RM2:RM2-R implies W3-RM:RM-R (implies W3-RM:RM-R = claim W3-RM2:Cont-R ((C4), Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240), accepted by both council seats: Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md:50 and Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md:197 (re-checked :217); Theory_work/Wave3/W3-RM2/reviews/SW1_sweep_astra.md:51). approver: HQ consultant (Fable 5.2) AGREE on card 1, 2026-11-15, under PROTOCOL_v4 H5 (replaces the owner approval of LIFECYCLE §0); recorded per Theory_work/Wave3/ACCEPTANCE/RECORD_BRIEF_2026-11-15.md. Conditions match in substance (TH09 / W2-APP:POST); W2-APP:POST@1.0.1 is unchecked (weak point). RM-0 and E4 stay ACTIVE.
- (C2) Theorem RM-R (Gaussian rows, polylogarithmic Q) [W3-RM] v1.0.0 state ACTIVE; status `PROVED-CHECKED`
- replacement W3-RM2:RM2-R: Theorem RM2-R (Gaussian rows, polynomial leakage) state ACTIVE; status `PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab89433b2f65dbfb`
- axes (Y vs X): {'assumptions': 'incomparable', 'conclusion': 'equal', 'rate': 'unknown', 'scope': 'unknown'} -> **undetermined**
- decision-rule class: **free**

## Statement diff

- hypotheses ADDED (each dependent must now verify them or the property it consumes): A:RM2-HSIZE-RHO (RM2 reference neighbourhood size), A:RM2-LFEAS (RM2 (L-feas), Gaussian rows), A:RM2-LGAIN-R (RM2 (L-gain-R) leak bound at every conditioning set), A:RM2-LLOC-R (RM2 (L-loc-R) localisation without rate), A:RM2-LSIZE-B-R (RM2 polynomial leakage size, Gaussian rows), A:RM2-W-R (RM2 lattice width on the realised design (W-R))
- hypotheses DROPPED: A:NA-FRAME (Reference frames/atoms for no-addition (R1)-(R3)), A:RM-LR (RM-LR)
- consumes: `P:SAND@W3-RM:SAND-Rp; P:NA-TL@W3-RM:B8a; P:NA-TL@W3-RM:B8b; P:POST-CONC@W3-RM:B9` -> `—`
- conclusion: `reported-model: P(𝒪∩{Ŝ⁺≠S0})→0 under the joint law of (X, ε), for every seed, N_e, R′, calibration outcome (no delivery claim)` -> `reported-model: as RM2-F under the joint law of (X, eps)`
- rate: `—` -> `none claimed`
- scope: `iid Gaussian rows; s0 fixed; p ≤ n^A (p ≫ n allowed); |Q| ≤ (log n)^κ; any X-measurable partition with blocks ≤ 16` -> `Gaussian rows; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b, |H_l| <= n^rho`
- method_commit: `2252d57` -> `—`
- statements: Theory_work/Wave3/W3-RM/STATEMENT.md:187-189 -> Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218

## Rebuild cost

- free: 2 re-point(s) PROPOSED (one cheap check each), no rebase, no re-review

| dependent | uses | action |
|---|---|---|
| W3-RM2:Cont-R | stmt | propose re-point |
| W3-RM:Examples | stmt | propose re-point |
