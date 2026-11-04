# ADVISER_DECISIONS (L-LEAN)

One line per adviser remark: adopted or rejected, and why.

Fable fidelity report (`fidelity/FABLE.md`, OVERALL GREEN). Minor remarks:
1. Adopted. Added `Greedy.theoremA3_hpm` (the HPM clause of Lemma 0(c)) and reworded the docstring.
2. Adopted. Reworded the `exists_bestImprovement` docstring.
3. Adopted. Added `Lattice.card_le_of_mem_Rad`: when s₀ + d ≤ K, `Rad` is the feasible R_{a,d}.
4. Adopted as documentation. The τ = m + e − σ count is listed as not formalised in the T37Greedy header.
5. Adopted as documentation. Listed as not formalised in the T37Greedy header.
6. Rejected. The statement is frozen and the form is harmless, as the reviewer says.
7. Adopted. Added `t11_miss_iid_real`.
8. No action needed. Already covered by A-T07-2.
9. No action needed. The Lean version is strictly more general.
10. No action needed. The W2-BOOK (iii′) attribution is correct (W2-BOOK PROOF.md §3 (iii′)). The excerpt was simply missing from the packet.
11. Adopted. Added the stage-0 convention to the `unbiased_of_step` docstring.
12. No action needed. This is the brief's form, as intended.

Astra fidelity report, round 1 (`fidelity/ASTRA_round1.md`): OVERALL RED. All findings concern T37 coverage; T21, T07, T11 and T12 are GREEN.
- Objection 1 (A2 move accounting missing). Adopted. Added `theoremA2_lattice_count` (τ + σ = m + e, max(m, e) ≤ τ ≤ Φ, each move lowers Φ by 1 or 2), and `drop_two_swap` / `swap_extra_truth_drop_two` (σ counts exactly the extra→truth swaps).
- Objection 2 (A3 not connected to the reported HPM). Adopted. Added `lemma0c_hpm`: the pre-search ledger has `S_c` as its running best, and the conclusion covers the post-search ledger, ties, and an injective tie rank. Also added `theoremA3_hpm`.
- Objection 3 (Lemma 0(c) only under TD′_P; no lattice-only A3; cap given as ℓ ≥ Φ). Adopted. Added `lemma0c` (general form), `DS` with `DS_move` and `theoremA3_lattice_only`, and `theoremA3_lattice_tau` (ℓ ≥ τ).
- Minor remarks: the docstring of `exists_bestImprovement` is fixed (same point as Fable's remark 2). The feasibility of `Rad` is handled by `card_le_of_mem_Rad`. The T11 and T12 scope is already disclosed (A-T11-1 and the T12Core docstring).
