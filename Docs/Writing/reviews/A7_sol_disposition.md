# A7 Sol fidelity read: disposition (Writing manager, 2026-11-24)

Review: `reviews/A7_sol_fidelity.md` (gpt-6.2-sol, high): NOT-FAITHFUL, 87 findings (43 C / 24 S / 20 F / 0 E).
A01–A44 (definitions and algorithms against the code, §4.4 against F2): applied by a Sonnet transcriber, one row each in
`reviews/A7_sol_disposition_A.md`. B01–B38 and C01–C05: the manager, below. Files are under
`Docs/Writing/manuscript/spec/sections/`.

| id | sev | decision | change |
|---|---|---|---|
| B01 | C | ACCEPTED | Thm 1: DIM, SGR, EFS are stated on the p_raw raw columns; prior, cap and posterior use the retained columns (sp6). |
| B02 | C | ACCEPTED | FSb: α*, β* deterministic (sp5). |
| B03 | C | ACCEPTED | Thm 2: posterior undefined (fewer than two predictors, or constant response) → probabilities read as 1 (sp6); Prop S7 and Remark S9 inherit it. |
| B04 | S | ACCEPTED | Prop S7: the common exceptional set also contains every data set on which a predictor is removed. |
| B05 | S | ACCEPTED | Thm 3: delivery under C2 on the domain 𝔇, besides the C2p form. |
| B06 | C | ACCEPTED | C2(iv): valid non-degenerate input added. |
| B07 | C | ACCEPTED | C2p rewritten as "C2 with the two integer limits idealised away; every other validator and cap kept". |
| B08 | F | ACCEPTED | C1: "a statement that holds for every seed and calibration outcome says so". |
| B09 | C | ACCEPTED | Prop 5 restated: fixed data, a.s. on 𝒜, conditional on 𝒞; joint-law form conditional on (data, 𝒞); E[1_𝒜 Ẑ] = E[1_𝒜 Z]. |
| B10 | C | ACCEPTED | WIT: X_{S0}, θ* deterministic, with the conditional random extension. |
| B11 | F | ACCEPTED | App. B D1: reader numbering (Theorem 3(b), row thm3); the masters' growth conditions are implied (stated there), no HQ question. |
| B12 | C | ACCEPTED | Lemma S1: π(S0) := 0 if S0 ∉ Ω. |
| B13 | C | ACCEPTED | Thm S4: the sufficient-condition sentence needs C_β²φ0² > c1; margin holds with any fixed c_id in (c1, C_β²φ0²). |
| B14–B17 | C | ACCEPTED | Remark S6 rewritten from the Thm2X master: DIM, SP, Gaussian noise with variance σ² depending on n, deterministic α, β, fixed floor c on all 1 ≤ |T| ≤ 3(A+1)(s0+1) log n. |
| B18 | C | ACCEPTED | Thm S10(ii): only "l ∉ S0" becomes "l ∉ Q"; H_l and the truths unchanged. |
| B19 | S | ACCEPTED | Thm S10(ii): the |Q| ≤ n^{1/2−ε} corollary added. |
| B20–B22 | S | NO STATEMENT CHANGE | A6's stronger RMF hypotheses kept on purpose (safe direction; already disclosed); App. B K1 now names the three weaker reader forms. |
| B23 | S | NO STATEMENT CHANGE | SCR keeps the full floor (sufficient special case); disclosed in App. B K2. |
| B24–B26 | S | ACCEPTED | Cor S12 (FAMC) restated in the master's technical form: GR (Σ positive definite), DIM, FSt, C1, the families (Block: B1/Bs/Bg; AR: ARs/ARsep/ARg) with the separation bound and the bad set B of Lemma S13. |
| B27–B30 | S/C | ACCEPTED | Lemma S13 (VIS) restated in full, items (0)–(5) = (VIS-0)–(VIS-e): sign route for every U, B closed in general with the attained minimum, finite case, one fixed r in (ii), the further finite-pattern families, the sign-route instances. App. B D4 updated. |
| B31–B33 | S/C | ACCEPTED | Cor S14: on Theorem 3's events 𝒢_n; the log-evidence sandwich "where reported"; the t_n form with |log Z_𝒯 − log Z| ≤ 2t_n. |
| B34–B37 | S/F | ACCEPTED | Usage table regenerated: Remark S6 uses DIM, SP; Thm S4 drops EF, BM; FAMC uses GR, DIM, FSt, C1, C2, C2p (not EFS, V, RM); C2 now also used by Thm 3 and FAMC. |
| B38 | F | ACCEPTED | §1 regime sentence: not all statements are asymptotic (applied after the A-transcriber's sp1 edit). |
| C01 | F | ACCEPTED | SOP:TH09 status quoted with its clause map and its "Not upgraded" scope clause (council part elided). |
| C02 | F | ACCEPTED | Thm 6 tag: (a) W3-PSHARP:B; (b) W3-PSHARP:A (A1) and W3-PSHARP-R:AE (A1-E); A2C removed. |
| C03 | F | ACCEPTED | Remark S6 tag: Thm2X only. |
| C04 | F | ACCEPTED | Remark S17 tag: TR only; OVL named as discharging only P-OVL. |
| C05 | F | ACCEPTED | Box P2 and App. B H2: the owner fixed one AR-strong data set, n = 200, known truth, one fit, one seed; only its continuation and Q are open. |
