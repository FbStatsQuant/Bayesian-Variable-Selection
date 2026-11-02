import SmcBvs.T21HPM
import SmcBvs.T07Bayes
import SmcBvs.T11Miss
import SmcBvs.T37Greedy
import SmcBvs.T37Lattice
import SmcBvs.T12Core

/-! Axiom audit: every main declaration must depend only on `propext`, `Classical.choice`,
`Quot.sound` (no `sorryAx`). The `#print axioms` output appears in the build log. -/

-- T21
#print axioms SmcBvs.hpm_eq_truth
#print axioms SmcBvs.t21_event_subset
#print axioms SmcBvs.t21_decomposition
#print axioms SmcBvs.t21_decomposition'
#print axioms SmcBvs.markov_half
#print axioms SmcBvs.t21_C1
#print axioms SmcBvs.integral_le_eps_add_prob
-- T07
#print axioms SmcBvs.T07.ceiling
#print axioms SmcBvs.T07.no_size_prior_repairs
#print axioms SmcBvs.T07.ceiling_sharp
#print axioms SmcBvs.T07.risk01_eq
#print axioms SmcBvs.T07.risk01_min_iff
#print axioms SmcBvs.T07.hpm_min_risk01
#print axioms SmcBvs.T07.riskH_eq
#print axioms SmcBvs.T07.psi_Jplus_le
#print axioms SmcBvs.T07.psi_Jplus_unique_iff
#print axioms SmcBvs.T07.mpm_min_riskH
#print axioms SmcBvs.T07.mpm_unique_iff
#print axioms SmcBvs.T07.psi_capped_le
#print axioms SmcBvs.T07.exists_capped
#print axioms SmcBvs.T07.capped_mpm_min_riskH
#print axioms SmcBvs.T07.reported_eq_hpm_iff
#print axioms SmcBvs.T07.reported_min_risk01_iff
#print axioms SmcBvs.T07.reported_truth_needs_unscored
#print axioms SmcBvs.T07.excess_riskH_le
#print axioms SmcBvs.T07.mpm_hat_eq_iff
-- T11(iii)
#print axioms SmcBvs.t11_pow_le_exp
#print axioms SmcBvs.t11_miss_pi
#print axioms SmcBvs.t11_miss_pi_real
#print axioms SmcBvs.t11_miss_iid
#print axioms SmcBvs.t11_miss_iid_real
-- T37(i)
#print axioms SmcBvs.Greedy.exists_bestImprovement
#print axioms SmcBvs.Greedy.path_F_strictMono
#print axioms SmcBvs.Greedy.theoremA1
#print axioms SmcBvs.Greedy.theoremA1_converse
#print axioms SmcBvs.Greedy.theoremA2
#print axioms SmcBvs.Greedy.theoremA3
#print axioms SmcBvs.Greedy.theoremA3_hpm
#print axioms SmcBvs.Greedy.lemma0c
#print axioms SmcBvs.Greedy.lemma0c_hpm
#print axioms SmcBvs.Greedy.pd_of_reach
#print axioms SmcBvs.Lattice.progress_mem_Lat
#print axioms SmcBvs.Lattice.lemma2a
#print axioms SmcBvs.Lattice.theoremA2_lattice
#print axioms SmcBvs.Lattice.theoremA3_lattice
#print axioms SmcBvs.Lattice.Φ_le_of_mem_Rad
#print axioms SmcBvs.Lattice.card_le_of_mem_Rad
#print axioms SmcBvs.Lattice.theoremA2_lattice_count
#print axioms SmcBvs.Lattice.drop_two_swap
#print axioms SmcBvs.Lattice.swap_extra_truth_drop_two
#print axioms SmcBvs.Lattice.DS_move
#print axioms SmcBvs.Lattice.theoremA3_lattice_only
#print axioms SmcBvs.Lattice.theoremA3_lattice_tau
-- T12(i.a) partial
#print axioms SmcBvs.T12.invariance_step
#print axioms SmcBvs.T12.resample_move_step
#print axioms SmcBvs.T12.unbiased_of_step
