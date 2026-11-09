# Patch P-LHiid — GEN (C5)(b) without "W7-PART Theorem B (candidate)" and "[CONC]" (item 2)

Proof: `lemmas/I2_LHiid_unconditional.md` (v2); check R35 (`reviews/R35_item2_check_sol.md`, VERIFIED-WITH-AMENDMENTS,
amendments applied). Wave1 files are not edited; HQ applies these when adopting W1-GEN.

1. `Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md:68-69` — replace
   "P(ℛ_nᶜ) → 0 by Theorem R = W7-PART Theorem B (**candidate**; A-REV6 "VERIFIED on SIZE"; PROOF.md:77-100)."
   by
   "P(ℛ_nᶜ) → 0 by Theorem R as repaired in W1-PXN (`Theory_work/Wave1/W1-PXN/lemmas/R_branch_repair.md` §1–2, (R-b)/(R-c);
   XF VERIFIED R14, R19, R21 there), or by route (R′) (`.../W1-PXN/lemmas/CR_corr_tails.md`), with blocks read as the
   deterministic make_blocks(X, B_n) data function on every branch (exact-branch convention, R_branch_repair.md §3); see
   C-PACK Lemma I2(i)."
2. `L6_instances.md:71-72` — replace "[CONC] (max|r̂_jk − Σ_jk| ≤ C√(log p/n), operator error O(log n)·C√(log p/n) = o(1)
   at these orders)" by "[CONC′] (W1-PXN Lemma CR: max|r̂_jk − Σ_jk| ≤ δ_n = 32√(2(A+1) log n/(n−1)) w.p. ≥ 1 − 3n^{−2};
   operator error ≤ L′_nδ_n = O((log n)^{3/2}n^{−1/2}) = o(1); C-PACK Lemma I2(ii))".
3. `L6_instances.md:83` — replace "**conditional on W7-PART Theorem B (candidate)** and [CONC]" by "using the repaired
   Theorem R and [CONC′] of W1-PXN (C-PACK Lemma I2); no candidate input".
4a. (R38 #2) `STATEMENT.md:129-131` — replace the whole (C5)(b) paragraph by: "(b) *LH-iid* in the common family of W1-PXN
   STATEMENT §1 and L6(b), with eventual SIZE, 18 ≤ p_n ≤ n^A, p_n → ∞, and fixed A ≥ 1: (C4) applies on the X-event
   constructed in L6(b). Partition recovery and the correlation bound are supplied by repaired W1-PXN Theorem R (or R′) and
   Lemma CR/[CONC′], as proved in C-PACK Lemma I2. Blocks and start objects have I2's exact-branch convention. The separate
   verifications of (H1), (H2), and all other components of the X-event, with their common constants and deterministic
   envelopes, are retained. Neither candidate Theorem B nor [CONC] is an additional assumed input; all other method and
   implementation premises remain."
4b. (R38 #2) In the L6(b) header at `L6_instances.md:4-5`, retain `PROVED (by this seat, unchecked)` and replace
   `conditional on W7-PART Theorem B (candidate) and [CONC]` by `using repaired W1-PXN Theorem R (or R′) and Lemma
   CR/[CONC′] via C-PACK Lemma I2, with GEN's remaining hypotheses unchanged`. The untouched Wave1 authorship/check
   statuses must not be upgraded by applying this dependency repair.
4c. `STATEMENT.md:172-173`, `lemmas/00_MAIN.md:38`, `REPORT.md:22, 65, 98` — drop
   "W7-PART Theorem B (candidate)" and "[CONC] (classical)" from the dependency lists for (b); list "W1-PXN Theorem R
   (repaired) and Lemma CR/[CONC′] (Wave-1 PROVED-CHECKED ticket, not adopted by HQ)".
   (R39 #2) In `W1/W1-GEN/REPORT.md:22`, replace `(conditional on the candidate W7-PART Theorem B)` by `(using repaired W1-PXN
   Theorem R and Lemma CR/[CONC′] via C-PACK Lemma I2, with GEN's remaining hypotheses retained)`. In REPORT:65 replace
   `**conditional on W7-PART Theorem B (candidate)** and [CONC]` by `using repaired W1-PXN Theorem R and Lemma CR/[CONC′]
   via C-PACK Lemma I2; GEN's other hypotheses are unchanged`. In REPORT:98 replace `W7-PART Theorem B for LH-iid` by `the
   repaired partition-recovery and correlation inputs of C-PACK Lemma I2 for LH-iid`. Preserve historical review verdicts
   and label these as C-PACK dependency addenda.
5. `L6_instances.md` (d), lines 123-191 — [CONC] → [CONC′] as in Lemma I2 §4 last paragraph (rate O(√(log n/n)); possibly
   weaker than √(log p/n), sufficient everywhere; or Lemma CR at δ = 32√(3 log p/(n−1)) for the original rate).
Meaning of "unconditional": removal of these two input conditions only; GEN's other hypotheses, implementation premises,
LS0 integration obligations and statuses remain.
