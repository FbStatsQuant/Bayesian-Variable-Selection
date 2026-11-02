# API-PXNGAP — plan (2026-11-02)

Goal: close A-REV3's p ≫ n GAP for Thm 5(b1) (LS0 route) on LH-iid, answering each objection explicitly.

A-REV3 / A-REV6 objections on W3-PXN that are still open (as of A-REV6):
1. P6 Lemma Λ(a) invokes Lemma Tr(c) outside its range (family ~ p^{s₀+2}, dimension s₀+2 possibly > 16).
2. P6 Lemma U(U1): the displayed "≤ 1" is false; U3 must absorb the RSS error into the signal margin.
3. P6 strict-margin sentence must exclude ties among progress additions.
4. P7 (no-tweak route): W5 R1 again calls Tr(c) outside its range; c = 1 only. (Not needed for (b1).)
5. Random-partition quantifier: fixed-group laws must be established unconditionally and intersected with recovery.
6. Partition recovery needs an explicit probability (W7 Theorem B, VERIFIED on SIZE by A-REV6).
7. LS0 stays a method change; operational hypotheses (OP-LS0, GUARD) must be retained.

Plan:
- PROOF.md: §1 family + hypotheses; §2 partition recovery with explicit bound (W7-B restated, short proof);
  §3 transfer lemma (quantifier); §4 Lemma Tr-J (any fixed dimension, polynomial family) — PROVED;
  §5 Lemma E (self-contained uniform score expansion; replaces W1-EXP citations; explicit κ_E) — PROVED;
  §6 start mass (P3) with Tr-J and E; §7 masking law (P4); §8 eligibility (P5); §9 TD′ on the lattice (P6 repaired)
  + lattice lemma for the production search (M §6.10) proved directly; §10 posterior (P8); §11 assembly;
  §12 obstructions (SIZE, polynomial p).
- scripts/: check_trJ.py (Beta bounds), check_lemmaE.py (expansion constants on LH-iid at n = 200),
  check_margins.py (population D_S margins), check_route.py (LS0 route end-to-end at small sizes). All via owls_run -j 2.
- REPORT.md: point-by-point answers, theorem, evidence, confidence card.
