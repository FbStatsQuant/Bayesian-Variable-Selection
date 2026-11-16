# Theory Department — queue (manager keeps this current)

Updated 2026-11-15 19:40 CT. Cap: ≤ 5 leads until Wed 11-18 18:00 CT (HQ temporary OK), then 3 (Claude Third, Opus 5.5 high).
Cut-off for riders: theory content freeze Wed 11-18 (CP3 Wed 18:00 CT, confirmed by HQ; a late rider ships at its last checked state). W3-DIST has priority on codex.

## Running
| ticket | contents | lead thread | worktree / branch | state | next |
|---|---|---|---|---|---|
| W3-START2-R (CP1 GO, D40) | T10 Gaussian-row rate √(log n/n) + T8 visibility at log n + 2 log p with (V-m) credit + START MIS/EX/F1/F3/F4 restated under START2 hyps + LEAK-0 wording; T9/T11 optional | mcp:launch:44aac259… | BVS-wt/W3-START2-R · theory/W3-START2-R | → CP1 | CP1 answer (manager); H5 card via HQ (headline: START-F, START-R, IF-START⁺) |
| W3-RM2-R | T4 constant-level (V)/BM + additive (BM-W) floor + Ex-Proxy decaying θ; T2(a) DLV-0, (b) mode interface, (c) down-closed 𝓛′; Ex-Equi 3/8 optional; Ex-PolyR/F to council | mcp:launch:86440d0e… | BVS-wt/W3-RM2-R · theory/W3-RM2-R | → CP1 | CP1; H5 card (headline: RM2-F) |
| W3-PSHARP-R | T12 Prop A/Cor A1 in expectation for every p, constant √((a+½)/π); A2C | mcp:launch:fab7385a… | BVS-wt/W3-PSHARP-R · theory/W3-PSHARP-R | CP1 GO (D37) → lemmas | CP1; H5 card (headline: Cor A1); before chapter sharpness section |
| PSMC-S0 | Part 1 T-N + T-CAL prelim + D-7 → CP1 (FR1 Sol running), as Engineering-facing notes; Part 2 CANCELLED (D18) | mcp:launch:c241a2d4… | BVS-wt/PSMC-S0 · theory/PSMC-S0 | → CP1 | CP1 summary ≤ 10 lines to HQ (owner OD-1/OD-2) |
| W3-MISR-R | T13 Cor-G(a), Cor-H (child agent; 6th slot per HQ) | child node …misr-r-lead-1 | BVS-wt/W3-MISR-R · theory/W3-MISR-R | → CP1 | CP3 Wed 18:00 |
| W3-EDIT | editorial pass; citation fixes MERGED (66b67f7d) + PR #10 merged (86191e17) | mcp:launch:950a7b4f… | BVS-wt/W3-EDIT · theory/W3-EDIT | citation fixes DONE (1a198e6), HQ pinged for PR #10; ledger in progress | CP1 by Wed 18:00 |

## Taken over from HQ (outside the lead cap)
| ticket | lead | state | next |
|---|---|---|---|
| W3-DIST (TOP PRIORITY) | Fable 5.2, mcp:launch:75635c1f… (root clone folder; snapshot → theory/W3-DIST) | CP2 (soft) met, CONTINUE (D38): BR1 NOT BROKEN; all line checks VERIFIED; L6 (DIST12) running → diff check → sweep → council → CP3 | CP2 = Lemma X + S + V line-checked → Astra break review |
| W3-READER | Opus, mcp:launch:2a4462b2… (BVS-wt/W3-READER) | bridge leg written (R1–R4, PoolZ); card v0.5 (H5 actions applied); Sol S2 running; gates tables in triage | CP1 → me → claims card to HQ (H5); READER_DELTA rows: thm3 PSHARP, thm4 MISR, thm5 START2, thm7 RM2-F |
| recorder | Opus, mcp:launch:563aa9b9… | task C (W2-APP PC1 Sol) running; task D (POST2) on hold | HQ decision on headline flags + conditional statuses |

## Ready (launch as a slot frees)
| ticket | contents | worktree / branch | note |
|---|---|---|---|

## To plan (charter §8)
| item | note |
|---|---|
| strength gates for headline candidates (lit / necessity / better, LIFECYCLE §4.2) | D17: W3-READER leg 2 after its CP1, five-pillar rows by Thu 11-19 18:00 CT (draft drafts/W3-READER_LEG2_GATES.md); 44 tool-set flags cleared per HQ/consultant (recorder task F) |

## Post-freeze riders (queued)
| ticket | contents | source |
|---|---|---|
| SAMP-R1 | truth-free D; TV re-centring of C; hybrid TR bound; LT rate under NC_r | SHARP3 triage (W3-READER TRIAGE_SHARP3.md) |
| POST2-O3 | E-floor+: bounded ridge cost in place of the floor on S₀ (design-agnosticism; FIRST post-freeze, owner tie-break); kill budget | H5 card 6 (D36) |
| POST2-O2 | E+: lower c₁; if c₁ < c₀, MIS(i′) covers C-MIS's inclusion range → C-MIS → MISR supersession (price the MISR rebuild); with POST2-R1; kill budget | H5 card 6 |
| POST2-R1 | matching expectation lower bound E δ_n ≳ √(log n/n) on every design with a floor (Thm 1 two-sided); one unverified step; kill budget | row 1.1 card (D35) |
| SCR-R1 | drop "fixed" signals (only use L3:69); ℓ¹ → total signal; exponential rate | SHARP3 triage |
| NARROW batch | 12 statement-precision narrowings (LIFECYCLE §3, priced) + H5 card for GEN C4 / FAC-CS C1 / SAMP:Pkg | ADJ_MINORS_iii.md (D31) |
| W2-APP Family-map diff round | F1–F4 + M57/M58 patches | PC1, D31 |
| errata batch | CHAPTER-ONLY errata held for riders (W3-EDIT CP1 groups) + F-UNI "eventually" (H5) | D19, D31 |
| record-format package | 38 rows free-text → file-path evidence | recorder task I |
| NOTS move | theory_w2/w3, /scratch theory_w2|3, P6 outputs → /home/fb31/SMC_Theory_Department on NOTS (+ scratch link, INDEX.md); one calm session; copies only, no deletion before Owls copy verified | D32/D33 (HQ approved) |

## Named open items (no tickets; for the chapter's open-problems section)
RM2-R aggregated leak (D) · START MIS with a general μ (D) · Ex-Equi b < 3/8 if not done in W3-RM2-R (O4′) · START2-O1 count (17 − s₀).

## Not ours
W3-PATH, T7, P6/D1 (HQ). Real recorder runs, CP3 acceptance, merges: HQ approves.

## Next campaign (proposal to HQ by Thu 11-19)
Consistency results first (owner, 11-15 evening) + Lean readiness of their deterministic cores; parallel-SMC theory parked (T-MERGE, EVAR/POOL). Draft v1: `NEXT_CAMPAIGN.md`.

