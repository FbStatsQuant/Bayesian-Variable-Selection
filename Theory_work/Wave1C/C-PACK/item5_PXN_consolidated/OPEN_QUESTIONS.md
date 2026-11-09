# OPEN_QUESTIONS — ambiguities, source conflicts and judgement calls (for the lead; nothing was resolved silently)

1. **Algorithm definitions behind Lemma R0 (02 §2.3).** The sources give the deterministic recovery argument only as three assertions — complete linkage completes each group first;
   "under g ≤ B a group node is retained by the top-down cut and under B < 2g no union of groups is"; "next-fit cannot put two groups of size g > B/2 into one bin" — plus the direct
   argument of the repair note. The precise top-down cut rule and next-fit rule (the method's make_blocks) are not stated in the sources I was given (they sit in the method code and W7-PART
   §0). I reproduced the assertions without inventing the rules. Decision needed: inline the make_blocks definition from W7-PART for self-containedness?

2. **Theorem R, (R-b) rests on an external theorem whose archive status has a GAP.** I cite W7-PART Theorem B/Corollary B with the registry status copied verbatim ("… Corollary B XF GAP (A-REV9,
   L2 constants)"). The ticket's reviews (R14, R30) re-checked the Hotelling density, Lemma 2 and the constant independently, which is why the closed form is kept; the sources do not contain
   that derivation (it is only summarised in R14's review), so I did not inline it. Route (R′) (02 §2.4) is fully self-contained and covers every later use. Decision: keep the citation, or
   inline the W7 Lemma 2 derivation from the W7-PART file? Also: the displayed form "S(t*) ≤ K_n for n ≥ 5" in my statement of [W7-B] is the (R-b) of the repair note, not a verbatim W7 sentence.

3. **Statuses not available verbatim.** For [LM], Lemma RO, the W6 operational premises and W3-PXN (00 §0.7) the sources do not give a registry status string; I wrote descriptive entries
   (marked as such). T22 and T03♯, W7 Theorems A/B statuses are copied from the dependency ledger of review R16 / the lemma files. External statements (T22(i-a), (ii-a), T03♯ hypotheses) are
   quoted as they appear in PROOF and the lemma files; I did not open the external STATEMENT files to compare wording. Please confirm against those files if a verbatim check is required.

4. **F1.** PROOF (deletion quantity of P3′) writes "(PXN §6, using F1)"; F1 is not defined in PROOF (its facts list starts at F2). I removed the cross-reference and inlined one sentence
   (E[x_{j_b}|X_{C_a}] = ψx_{j_a}, hence Cov(x_{j_a}, y | X_U) = β(1−ψ²)Var(x_{j_a}|X_U), other signal components and noise contribute zero covariance) taken from reviewer R16's verification text, not from
   PROOF or a lemma file. Keep or drop?

5. **Haar step (Lemma B, 03 §3.1).** PROOF's proof is "condensed; PXN §4 has the full version" (a cross-reference to W3-PXN). To make the document self-contained I inlined the detailed Haar-span
   derivation from reviewer R13 (finding 2), and the Beta(½,(n−2)/2) law of each r̂²_{j_b,y} in (iii) (R13 table). This text comes from a review file, not from PROOF or the lemma files. Keep or drop?
   (The same Haar step is used by name in Lemma Λ(a) and for T = A₀ null columns.)

6. **(U3) constants (04 §4.2).** PROOF writes |Δprior| ≤ 2 log(2p) ≤ 2A log n + 2; with |Δdet| ≤ log(n+1) this gives a constant slightly above 2 in "(2A+1) log n + 2". I used
   2 log(2p) ≤ 2 log 2 + 2A log n and the observation from review R17 (endorsed in FINAL_PROOF §0) that 2 log 2 + log(1+1/n) < 2 for n ≥ 2, so the stated mar_n(c′) holds exactly. The explicit onset
   e_n ≤ c′H/(4H+c′) is also from R17/FINAL_PROOF. No constant of the statement changes.

7. **PROOF (O2) names [T03] and [CONC].** FINAL_PROOF replaces them (T03♯, [CONC′]); I changed the names in (O2) accordingly (06 §8). The conjecture inside (O2) (discovery half survives log p = o(n))
   is kept verbatim as "CONJECTURE, not written".

8. **(O5) "(2A+1) log n ≈ 20".** The retained comparison figure is the source's; for A = 1 and n = 200 it is 3 log 200 ≈ 15.9, and ≈ 18.5 for A = log 750/log 200. E-22 keeps "≈ 20" and says the conclusion is
   unchanged (it is: the margin 0.775 is far below any of these). Left as in the source; flagged because the figure depends on A.

9. **Gloss words I added (small).** (i) 00 §0.5: "budget constants H₀, N₀ of the method" for the exact-enumeration threshold (the sources give only Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p). (ii) 04 §4.5: "(p flips,
   k(p−k) swaps)" as the decomposition of the per-scan count p + k(p−k) (the sources give only the total). (iii) 04 §4.6: the count paragraph for N_scores spells out "one scan at each of the sizes s, s+1, …, s₀";
   the formula itself is from the repaired P6′. (iv) 00 §0.1: Lat(S°) := {S° ∪ 𝓜′ : 𝓜′ ⊆ 𝓜} is my explicit definition (PROOF only writes Lat(S°)∖{S₀} = {S° ∪ M′ : M′ ⊊ M}); I did not check W6's own definition
   of Lat.

10. **Implementation pointers.** Code locations (v3_engine.h:400-411, v3_start.h:178-239, v3_core.cpp:447 and :504-524) are copied from the lemma files; I did not re-open the code to verify them. They appear
    only as parenthetical implementation pointers (03 §3.4, 04 §4.5, 05 §6.2, 00 §0.3).

11. **Notation changes** (APPLIED_ERRATA §D) were made to remove clashes present in the sources (masked set M vs constant M; q in Theorem R vs start-mass q; m_n SE cutoff vs margin m_n(c′); t_n in three roles;
    b₀ beta-min vs prior b₀). The letter A (exponent vs generic subset) was kept as in the sources and flagged in 00 §0.2 rather than renamed. Please say if you prefer a full rename of the generic subsets.

12. **L_n in STATEMENT §3 vs P8.** STATEMENT §3 lists the SE range as s₀ + max{m_n, m♯_n, j₀, g, s₀+2}; the replacement lemma defines L_n with k_n in place of m♯_n (m♯_n ≤ k_n). I used the lemma file's L_n
    (02 §2.1), which is the larger and therefore covers both.

13. **Constant C_q.** The sources give C_q only up to proportionality (C_q ∝ C_e g e^{2κ_E}√(A+1)) and "2.3 C_e g ξ_n =: C_q√(log n/n)(1+o(1))". I kept exactly this and did not compute the explicit value.

## Disposition (lead, after fidelity check R36, `../reviews/R36_item5_fidelity_sol.md`)
All 13 items resolved as R36 Q5 recommends: keep R0's direct margin argument (1); keep (R-b) as cited, D2 resolved by R14/R21
and both council seats, R′ does not replace (R-b) (2); statuses vs descriptive provenance distinguished (3, fix #5 applied);
keep the F1 deletion-covariance and Haar expansions from R16/R13 (4, 5); keep the U3 bookkeeping from R17 (6); keep T03♯ /
CONC′ labels (7); keep "≈ 20" as the rough comparison (it is (2A+1) log 200 ≈ 15.9 already at A = 1) (8); glosses kept,
"at most p flips" reading (9); code pointers are source pointers only (10); notation kept (11); larger L_n kept (12); C_q
up to a fixed dominating constant (13). R36 findings 1–6 applied in place.
