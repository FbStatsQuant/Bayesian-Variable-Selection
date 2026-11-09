# W2-LOC2 — LOG

- 2026-11-09 08:09 Start. Read Wave2/Wave1C/Wave1 protocols, APP REPORT/STATEMENT/L3_LOC/L2_CT, GROW L0–L4, L6, GEN L1, FACA L7, FIN s6.
- 08:2x Diagnosis numerics d1_diag.py (74 runs) → numerics/D1_SUMMARY.md. Start modes ≫ log n in d = 2 and middle regime; LS0 succeeds in all runs.
- Located every use of |Q| = O(log n) in the LOC/GROW chain: (i) GEN L1 family sizes (polynomial) → L0′ quasi-polynomial;
  (ii) APP L3.6 Step 3 χ² union over 2^{|Q|} producing a √|Q| error → replaced by NA-R (atoms, ℓ¹); (iii) sample operator
  errors |S|ħ_n → still o(1) for polylog |S|; (iv) |I_l| polylog → still polylog; (v) log k = O(log log n) → unchanged.
- STATEMENT v1.0 + PLAN written; statement lock R01 requested.
- 08:34 Falsification numerics n4_nar_check.py → n4_out.txt: CT_d bound ratio ≤ 0.32 (2-D grids, 30 submatrices each);
  NA-R Step-1 identity exact (≤ 6e-16); decomposition bound holds in all tested (T,l); ‖Cr‖/‖Ce‖ ≤ 1.0009; |Z−Z^pop| ↓ with n.
- Drafted (pending lock) lemmas L1_toolkit, L2_NAR (key), L3_CTd, L4_LOCd, L5_assembly, L7_delivery. Waiting on R01.
- 08:41 R01 LOCK-WITH-CHANGES (2 MAJOR, 4 MINOR), all applied → STATEMENT v1.1 LOCKED (reviews/R01_disposition.md). Lemma files updated.
- 08:42 Launched R02 (L1+L3, Sol high), R03 (L2 NA-R key, Sol xhigh), R04 (L4+L5+L7, Sol high; first attempt ECONNRESET, relaunched), and a parallel Sol-high prover for (D3) polynomial decay → lemmas/L6_poly.md.
- 08:45 R04: L4 V-W-A, L5 V-W-A, L7 VERIFIED; 2 MINOR applied (reviews/R04_disposition.md).
- 08:48 R02: L1, L3 V-W-A; 1 MAJOR (CD_d indexing) + 3 MINOR + 1 NIT applied (reviews/R02_disposition.md). Status lines updated.
- 08:49 R03 (key lemma, Sol xhigh): VERIFIED-WITH-AMENDMENTS (1 MAJOR, 1 MINOR, 1 NIT), all applied. Key lemma checked → CHECKPOINT + mid-point next.
- 08:52 CHECKPOINT.md written; mid-point R05 (fresh Sol xhigh) launched; citecheck.py drafted (remaining misses = REPORT not yet written).
- 08:54 Prover returned lemmas/L6_poly.md: (D3) for α > 17/2 (Lemma BC: bounded conditioning keeps exponent α via cofactor paths; Lemma IR: banded+CT inverse exponent α−1; selection radius n^ρ; vanishing ℓ¹ atoms in NA). STATEMENT v1.2 fills α₀ = 17/2 (logged). Checks launched: R06a (Opus high, cross-family to Codex author), R06b (fresh Sol xhigh).
- 08:56 R05 mid-point (fresh Sol xhigh): CONTINUE, 1 MINOR (κ ≥ 1 convention) applied (reviews/R05_disposition.md). Next: sweep after R06a/b on L6.
- 09:03 R06b (fresh Sol xhigh) on L6_poly: VERIFIED-WITH-AMENDMENTS (1 MINOR: τ lower bound 1/2 in (P13)), applied. Waiting R06a (Opus).
- 09:08 R06a (Opus high, cross-family): L6 VERIFIED-WITH-AMENDMENTS (3 MINOR applied, NITs recorded). (D3) now checked by both families. Next: add (D3) class to F-LOC2 delivery, then exhaustive sweep R07.
- 09:09 (D3) class added to F-LOC2 (L7, STATEMENT (E)). Exhaustive sweep R07 (Sol xhigh) launched on all files.
- 09:24 R07 sweep: 0/0/10/6, all 16 fixed (reviews/R07_disposition.md).
- 09:25 REPORT written (pending council); citecheck 0 misses. Council round 1 launched (Sol xhigh + Opus high, Claude Work).
- 09:31 Council C1 Sol: 9.3, all six gates PASS; 1 MINOR (REPORT IR wording) applied. Waiting on Opus seat.
- 09:36 Council C1 Opus: 9.1, all gates PASS → COUNCIL PASSED round 1 (Sol 9.3 / Opus 9.1). Editorial items applied (reviews/C1_disposition.md); poly_check rerun PASS; citecheck 0 misses. RESULT PROVED-CHECKED.
