# W3-MISR-R — CHECKPOINT 1 (hard; 2026-11-15 22:13 CST; lead Claude Opus 5.5 high, Claude Third)

Tier B rider (T13), NORMAL mode. HOLDS.md (origin/main): no holds. Reviews relied on: L1 statement lock — Sol
(gpt-6.1-sol, high), fresh, blind, NORMAL mode: LOCK-WITH-AMENDMENTS; all 4 findings accepted (`reviews/L1_disposition.md`).

## Locked delta statement
`STATEMENT.md` v1.1 (locked) + v1.2 [LA-1] (one clause added after the lock; changelog §10; statement-change check owed,
planned in the Sol line-check batch). Delta over W3-MISR v1.3 (registry @1.0.0). New claims:
1. **W3-MISR-R:CorG-min** (§2) ⇒ W3-MISR:Cor-G(a). Candidate design of any law; only (N) Gaussian noise ⫫ design and
   (OV^c) "given the candidates, the omitted contrasts are N(0, τ²(X)I) around a linear candidate predictor" (γ, τ² may
   depend on the design); Σ_𝒞𝒞 ≻ 0 dropped (Moore–Penrose example); (c) necessary and sufficient under (N); (d) Cramér converse.
2. **W3-MISR-R:CorGb-plus** (§3) ⇒ W3-MISR:Cor-G(b). Gaussian candidate rows + (OV) (no joint Gaussianity); floor on the
   correlation matrix only (no C₀, no global Σ ≻ 0); liminf beta-min; explicit bound E δ_n ≤ C r_n + (2 + 2k_n)n⁻² + n⁻¹.
3. **W3-MISR-R:CorH-plus** (§4) ⇒ W3-MISR:Cor-H. (a′) under (SZ), (E^σ), (F₀), δ_n →_P 0 (no (OS), no margin); (b)
   unchanged; (KL) in-sample KL clause; KL reading scoped per L1-1.
4. **W3-MISR-R:CorH-U** (§5) ⇒ CorH-plus. Uniform-over-class forms (U-a), (U-b); conditional random-design form (RD) by
   freezing (BASE M.3); (G) Gaussian-row instance [LA-1].

## Target clauses (for HQ to fix)
CorG-min (a)–(e); CorGb-plus display (both bounds) under its hypotheses; CorH-plus (a′), (b), (KL); CorH-U (U-a), (U-b),
(RD), (G). Rates: r_n = √(log n/n) (CorGb-plus); M_n/√n Hellinger, M_n/n KL ((a′)); log n/n ((b)). No WEAKER clause vs BASE.

## Headline impact
MIS(i), (i′), (ii) (headline masters, card row 1.4): **unchanged**. Their Gaussian-row reader version (row thm4) changes:
**STRONGER** (weaker hypotheses, same displays) via CorGb-plus (+ CorG-min examples) and the remark via CorH-plus/CorH-U
(G). Draft: `READER_DELTA.md` (model "given the candidates, y Gaussian with linear mean, constant variance"; floor on the
correlation matrix). Needs HQ + consultant (v4 H5) after CP3. **Asks:** (i) go on CorGb-plus's extension beyond the
brief's cosmetics (Gaussian candidate rows + (OV) instead of joint Gaussianity: a one-line consequence of CorG-min);
(ii) go on [LA-1] (CorH-U (G)); (iii) OK to fold the [LA-1] statement-change check into the line-check Sol agent.

## Evidence files
`TARGET.md` (assumption map, parity: beats BASE on every changed clause; "short" vs SL Thm 4 only in metric/mode
(in-sample, in probability), with reason), boundary numerics `numerics/N1_out.txt` (no visible change just outside (OV^c);
(OV^c) is the boundary of the exact reduction, not of the phenomenon). DIST pointer: REPORT, HEURISTIC/OPEN only (not yet written).
Errata: W3-EDIT I4-F2 absorbed (§7 full status quotes); no other routed erratum restated.

## Plan with hours (`PLAN.md` v1.1)
Lemmas G1_min, G2_corr, H1_plus, H2_uniform (1.0 h) → one Sol line-check batch (+ LA-1 change check) → REPORT, DEPS,
citecheck (0.4 h) → council Sol + Opus (0.3 h + waits) → CP3. Lead ≈ 3.5 h total, ~1.2 h spent. CP3 target: Tue
2026-11-17, well before the Wed 18:00 CT cut-off. Codex used so far: 1 review (lock). Kill budget 3: unused.
