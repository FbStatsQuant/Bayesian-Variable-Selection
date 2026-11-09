# MAP — correspondence table for the consolidated W1-PXN proof

Abbreviations (this file only; MAP.md may contain old-file references):
PROOF = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md` (486 lines);
FP = `Theory_work/Wave1/W1-PXN/FINAL_PROOF.md`; ST = `.../STATEMENT.md` (v2, §5 precedence); ER = `.../lemmas/ERRATA.md` (E-1..E-22);
lemma files (all in `Theory_work/Wave1/W1-PXN/lemmas/`): P8 = P8_T03sharp, CR = CR_corr_tails, LSM = L_strict_localmax,
LSR = LS_P6_repair, RBR = R_branch_repair, BII = B_ii_domain. Reviews in `.../reviews/` are cited as Rxx / C1.

Rule used: FP says which text proves each step; a lemma file supersedes PROOF where FP says so; each erratum is applied at its place.

| FP § | Content | PROOF lines used | Lemma files | Errata applying to those lines | Consolidated file / section |
|---|---|---|---|---|---|
| §0 | standing conventions, exact arithmetic, onset | 36-73 (setting, notation), 24-32 (list of cited results → external citations) | RBR §3 (exact branch) | E-18 (exact-branch convention) | 00 §0.1-§0.5, §0.7 |
| §0 | group versions / Lemma T | 69-71, 104-119 | – | – | 00 §0.6 |
| §0 | population facts F2–F5, λ₀, φ₀², M, b_min | 55-58, 213-217 | P8 step 2 | – | 00 §0.2 |
| §1 | [LM] | 26 (statement), 143 | CR header | – | 01 §1.1 |
| §1 | Lemma CR, [CONC′] | (replaces [CONC], 27-28) | CR (all) | – | 01 §1.2 |
| §1 | Lemma Tr-J | 123-156 | – | E-6 (table wording, "uniformly bounded"); family thresholds indexed by D (R30 #5, FP §1) | 01 §1.3 |
| §1 | Lemma E, 𝒟_start, 𝒟_search | 160-207 | – | E-1 (factor 2), E-2 (ℰ*), E-3 (remark 4), E-4 (explicit C₂); R30 #2 (two events) | 01 §1.4 |
| §2 | cutoffs m♯_n ≤ k_n, L_n; event ℰ♯_n | 213-220 (P2 superseded) | P8 steps 1-2 (v2: [CONC′]) | – | 02 §2.1 (Lemma K, L_n), §2.2 (ℰ♯_n) |
| §2 | Theorem R (R-a,b,c), deterministic part, (R′) | 77-100 | RBR §1-§2; CR (R′) | E-15 (display split), E-16 (delete "0.17"), E-17 (A0(c) replaced by direct argument) | 02 §2.3 (Lemma R0, Theorem R), §2.4 ((R′)) |
| §3 | Lemma B | 222-234 | BII | E-7 | 03 §3.1 |
| §3 | P3′ | 238-268 | – | E-19 (delete "sharp in order"), E-20 ("on {q<1}", "ã_hj1_{𝒢_n} ≤"), E-6 (name of row), 𝒢_n with 𝒟_start | 03 §3.2 |
| §3 | P4 | 277-284 | – | – | 03 §3.3 |
| §3 | P5 | 286-288 | LSR "P5 qualifications" | E-10 | 03 §3.4 |
| §4 | Lemma Λ | 307-326 | – | E-5 | 04 §4.1 |
| §4 | Lemma U | 296-305 | – | R17 note (explicit onset e_n ≤ c′H/(4H+c′)); margin function renamed mar_n | 04 §4.2 |
| §4 | (D_S) lattice margins | 328-355 | – | E-13 (cross-component swaps), E-14 (min ∅ := +∞) | 04 §4.3 |
| §4 | (L) | 357-370 (addition step 363-367 superseded) | LSM (all) | E-12 (replacement), E-14 (heuristic wording at 368-370) | 04 §4.4 |
| §4 | Lemma LS, P6′ | 372-399 superseded | LSR (Lemma LS repaired, Theorem P6′ repaired), PROOF 372-377 (search definition) | E-8, E-9; general cost bound from 441 | 04 §4.5-§4.6 |
| §5 | P8♯, de-randomisation | 403-417 (§9 superseded in input) | P8 steps 3-4 | – (D1 repair) | 05 §5.1 (T03♯), §5.2 (de-randomisation), §5.3 (P8♯) |
| §6 | (C) | 436-446 | LSR "Closure citation", RBR §3 | E-11 (closure), E-18 (exact branch), R30 #1 / R21 #1 (s₀ ≤ K cases), R30 #4 (every n vs n ≥ n₀) | 05 §6.1-§6.3 |
| §6 | Theorem assembly | 421-441 | LSR, RBR | E-9 ((K)), E-15 | 05 §6.4 |
| §7 | A-dependence | – (ST §3, FP §7) | – | – | 06 §7 |
| (PROOF §11) | obstructions / not claimed | 461-486 | – | E-21 (O3), E-22 (O5 numbers) | 06 §8 |
| appendix | assessment only | – | I8_lean_readiness (excluded) | – | 06 Appendix A (one-line note) |

Per-erratum location (detail in APPLIED_ERRATA.md): E-1,E-2,E-3,E-4 → 01 §1.4; E-5 → 04 §4.1; E-6 → 01 §1.3; E-7 → 03 §3.1;
E-8,E-9 → 04 §4.5-§4.6; E-10 → 03 §3.4; E-11 → 05 §6.2; E-12 → 04 §4.4; E-13 → 04 §4.3; E-14 → 04 §4.3, §4.4;
E-15,E-16,E-17 → 02 §2.3; E-18 → 00 §0.5, 05 §6.2; E-19 → 03 §3.2, 00 §0.4, 06 §8; E-20 → 03 §3.2; E-21 → 06 §8 (O3); E-22 → 06 §8 (O5).
