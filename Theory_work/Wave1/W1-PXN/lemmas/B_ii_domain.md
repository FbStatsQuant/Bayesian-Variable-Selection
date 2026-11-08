# Repair of Lemma B(ii) (PROOF.md:225) — domain restriction (from reviewer R13, finding 1, ERROR)

Status: repair by this seat (wording proposed by R13), 2026-11-08; XF VERIFIED (R21).

**Defect (R13 #1).** B(ii) is stated for arbitrary A ⊇ S° with A ∖ S° neutral. When p ≫ n such A can have |A| ≥ n−2; then
x_{A,l} = 1 a.s. (|A| = n−2) or is undefined (|A| = n−1), while the claimed law Beta(½, (n−2−|A|)/2) is not a distribution.

**Repaired statement.** (ii) For deterministic A ⊇ S° with A ∖ S° neutral, |A| ≤ n − 3, and a deterministic neutral l ∉ A:
x_{A,l} := 1 − RSS_{A+l}/RSS_A ~ Beta(½, (n−2−|A|)/2). General Haar calculation (PROOF.md:230-233): require |U| + |W| ≤ n − 2.

**Downstream impact: none.** B(ii) is not used anywhere in PROOF §§6–10 (grep: Lemma B is used only through B(i) at
PROOF.md:252 (P3′), B(iii) at :283 (P4), and the Haar argument "as in Lemma B" at :319 (Λ(a)), all on sets of bounded
size, where |U| + |W| ≤ max(g, s₀+2) ≤ n − 2 for n ≥ n₀). B(i), (i′) satisfy the restriction eventually because g is fixed.
