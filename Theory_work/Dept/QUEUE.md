# Theory Department — queue (manager keeps this current)

Updated 2026-11-15 20:25 CT. Cap: ≤ 3 ticket leads running at once (Claude Third, Opus 5.5 high).
Cut-off for riders: theory content freeze Wed 11-18 (aim CP3 Wed 18:00 CT; HQ to confirm). W3-DIST has priority on codex.

## Running
| ticket | contents | lead thread | worktree / branch | state | next |
|---|---|---|---|---|---|
| W3-START2-R | T10 Gaussian-row rate √(log n/n) + T8 visibility at log n + 2 log p with (V-m) credit + START MIS/EX/F1/F3/F4 restated under START2 hyps + LEAK-0 wording; T9/T11 optional | mcp:launch:44aac259… | BVS-wt/W3-START2-R · theory/W3-START2-R | → CP1 | CP1 answer (manager); H5 card via HQ (headline: START-F, START-R, IF-START⁺) |
| W3-RM2-R | T4 constant-level (V)/BM + additive (BM-W) floor + Ex-Proxy decaying θ; T2(a) DLV-0, (b) mode interface, (c) down-closed 𝓛′; Ex-Equi 3/8 optional; Ex-PolyR/F to council | mcp:launch:86440d0e… | BVS-wt/W3-RM2-R · theory/W3-RM2-R | → CP1 | CP1; H5 card (headline: RM2-F) |
| W3-PSHARP-R | T12 Prop A/Cor A1 in expectation for every p, constant √((a+½)/π); A2 e^λ−1 on (W-orth) | mcp:launch:fab7385a… | BVS-wt/W3-PSHARP-R · theory/W3-PSHARP-R | → CP1 | CP1; H5 card (headline: Cor A1); before chapter sharpness section |

## Ready (launch as a slot frees)
| ticket | contents | worktree / branch | note |
|---|---|---|---|
| W3-MISR-R | T13 Cor-G(a) minimal hypothesis; Cor-H(a) under δ_n →_P 0, uniform + conditional random-design forms | BVS-wt/W3-MISR-R · theory/W3-MISR-R (brief committed ef4f92a) | first free slot; output feeds W3-DIST (HQ) |
| PSMC-S0 | T-PART + T-N premise audits (Engineering OD-5, OD-1) to CP1 by Thu 11-19 12:00 CT | to create (brief drafts/PSMC-S0_BRIEF.md) | time-critical for Engineering; asked HQ for an extra slot |
| W3-EDIT | editorial pass (HQ_NOW): pass-1/2/3 API MINORs (21+13+5), C-DLV:Prop-F wording, PSHARP E1–E9, MISR/START2 errata (incl. LEAK-0 "sharpens" at START2 STATEMENT:87-88; MISR ASSUMPTION_MAP:27 cross-cite PSHARP), C-MIS citecheck (6 drifted cites → SoP 04_theory.tex), W2-FAC-X citecheck.py path fix + CITECHECK refresh | to create (brief drafts/W3-EDIT_BRIEF.md) | HQ approved rehash path; citation fixes first (PR #10) |

## Named open items (no tickets; for the chapter's open-problems section)
RM2-R aggregated leak (D) · START MIS with a general μ (D) · Ex-Equi b < 3/8 if not done in W3-RM2-R (O4′) · START2-O1 count (17 − s₀).

## Not ours
W3-DIST, W3-READER, recorder runs, W2-APP:POST@1.0.1 check (HQ recorder/Sol), W3-PATH, T7, P6/D1.

## Next campaign (proposal to HQ by Thu 11-19)
Parallel-SMC theory + evidence-variance problem σ̂(log Ẑ_r) ≈ 1 at p ≥ 5k, coordinated with Engineering's spec and
output-preservation contract, with the five premise tickets T-N, T-PART, T-STREAM, T-CAL, T-MERGE (ENG_INTERFACE.md). Stretch: approximate sparsity, exponential p for W3-DIST (after it closes). Draft: `NEXT_CAMPAIGN.md`.
