All three round-1 objections are **RESOLVED**. The additions complete the missing coverage; the frozen statements remain valid component results.

I reviewed only the five specified files. This is a statement-fidelity judgment: proof bodies were not assessed, and no commands, builds, or jobs were run.

References: source items below refer to [SOURCES.md §4](C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/theory-L-LEAN/theory_campaign/L-LEAN/fidelity/packet2/SOURCES.md:166). `G` denotes `SmcBvs.Greedy` in [T37Greedy.lean](C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/theory-L-LEAN/theory_campaign/L-LEAN/fidelity/packet2/lean/T37Greedy.lean); `L` denotes `SmcBvs.Lattice` in [T37Lattice.lean](C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/theory-L-LEAN/theory_campaign/L-LEAN/fidelity/packet2/lean/T37Lattice.lean).

**Objection decisions**

1. **A2 move accounting — RESOLVED.**  
   `theoremA2_lattice_count` supplies the exact identity
   \[
   \tau+\sigma=m(S)+e(S),\qquad
   \max\{m(S),e(S)\}\le\tau\le\Phi(S).
   \]
   Its inequalities restrict every pre-τ potential drop to exactly 1 or 2, and its filter counts precisely the two-unit drops over steps `0,…,τ−1`. `drop_two_swap` and `swap_extra_truth_drop_two` identify these drops, in both directions, with extra→truth swaps. Strict decrease before τ and terminality at `S₀` exclude stationary padding from the count. Together with `theoremA2_lattice`, this covers the source’s lattice containment, progress, and quantitative conclusions.

2. **Reported HPM — RESOLVED.**  
   `lemma0c_hpm` explicitly connects the pre-search score bound, certified arrival, post-search ledger, and reported maximiser. It concludes equal score with `S₀`, equality of models without ties, and equality under an injective rank when the reporting rule and `S₀`’s tie preference agree. These are faithful meanings of “`Ŝ = S₀` up to exact ties.” No posterior-majority hypothesis appears.

   Its ledger assumptions are sufficiently general: the actual cumulative ledger is an instance of the permitted `L`. Requiring `S₀ ∈ L` expresses the returned centre’s scoring; the path equality identifies that centre. The absence of `Sc ∈ pre` and of an exact-union equation weakens the premises without excluding the production case.

3. **Generality and lattice-only/sharp-cap A3 — RESOLVED.**  
   `lemma0c` requires only a best-improvement map, arrival at `S₀`, and `M S₀ = none`; it permits successful paths containing neutral or regressive potential moves.

   `DS` faithfully expresses the source’s strict separation: some feasible progress neighbour improves the current score and beats every nonprogress neighbour. Although the witness need not itself maximise among progress neighbours, finite-neighbourhood maximisation makes this equivalent to the source’s maximum inequality. `DS_move` consequently guarantees progress for every admissible tie rule.

   `theoremA3_lattice_only` restricts the one-state assumptions to `Lat(Sc)∖{S₀}`. The sharp-cap conclusion is covered compositionally: `DS_move` and lattice closure supply abstract `TDP`; `theoremA2` supplies the actual move count; `path_stays` applies to every cap at least that count. `lemma0c_hpm` then supplies reported-HPM recovery. The analogous `Rad` route is covered as well. See the interface qualification below.

**Theorem table**

GREEN below means faithful within the theorem’s stated component scope and the combined coverage supplied by this packet; it does not mean each core theorem independently contains all of A2 or A3.

| Name | Source item | GREEN/RED | Reason |
|---|---|---|---|
| `G.path_zero` | Greedy iteration | GREEN | Starts at the specified centre. |
| `G.path_succ` | Greedy iteration | GREEN | Correct one-step recurrence. |
| `G.step_of_some` | Greedy move | GREEN | A selected neighbour becomes the next centre. |
| `G.step_of_none` | Stopping convention | GREEN | Terminal states remain fixed. |
| `G.path_stays` | Termination | GREEN | Correct stationary continuation after stopping. |
| `G.exists_bestImprovement` | Definition of `M` | GREEN | Supplies an admissible best strict-improvement map. |
| `G.path_F_le` | Lemma 0(a) | GREEN | Correct nondecrease for the stationary-padded path. |
| `G.path_F_mono` | Lemma 0(a) | GREEN | Correct monotonicity across arbitrary iteration indices. |
| `G.path_F_strictMono` | Lemma 0(a) | GREEN | Strict increase follows an actual selected move. |
| `G.path_mem_of_TDinf` | TD′∞ closure | GREEN | Preserves region membership, including after termination. |
| `G.theoremA1` | A1, forward | GREEN | Includes closure, termination, and the rank-above move bound. |
| `G.theoremA1_converse` | A1, reverse | GREEN | Region-preserving termination implies TD′∞. |
| `G.theoremA2` | A2, abstract core | GREEN | Supplies actual moves, progress, closure, and bounded arrival. |
| `G.theoremA3` | A3, certification/score core | GREEN | Certified return and search-score bound; additions complete coverage. |
| `G.theoremA3_hpm` | A3 / Lemma 0(c), ledger bound | GREEN | Extends the score bound to previously scored models. |
| `G.lemma0c` | Lemma 0(c), search-score bound | GREEN | Uses certified arrival without a regional progress assumption. |
| `G.lemma0c_hpm` | Lemma 0(c), reported HPM | GREEN | Explicit maximiser, no-tie, and ranked-tie conclusions. |
| `G.pd_of_reach` | A4, PD component | GREEN | Arrival from a distinct start forces strict score dominance. |
| `L.Φ_eq` | Potential definition | GREEN | Identifies symmetric-difference size with missing truths plus extras. |
| `L.mem_Lat` | Centre lattice | GREEN | Correct interval characterisation of the source lattice. |
| `L.mem_Rad` | Region definition | GREEN | Correct missing/extra bounds, with feasibility handled separately. |
| `L.mem_nbhd` | Feasible neighbourhood | GREEN | Exactly a flip or swap with feasible resulting size. |
| `L.S₀_mem_Rad` | Region setting | GREEN | Truth has zero missing indices and extras. |
| `L.self_mem_Lat` | Centre lattice | GREEN | Every centre belongs to its lattice. |
| `L.S₀_mem_Lat` | Centre lattice | GREEN | Every centre lattice contains the truth. |
| `L.Φ_insert_of_mem` | Progress move table | GREEN | Adding a missing truth lowers potential by one. |
| `L.Φ_insert_of_notMem` | Regressive move table | GREEN | Adding a null raises potential by one. |
| `L.Φ_erase_of_mem` | Regressive move table | GREEN | Deleting a truth raises potential by one. |
| `L.Φ_erase_of_notMem` | Progress move table | GREEN | Deleting an extra lowers potential by one. |
| `L.progress_mem_Lat` | Move table / Lemma 2(a) | GREEN | A decreasing-potential flip or swap stays in the start’s lattice. |
| `L.mis_ext_le_of_mem_Lat` | Lemma 2(a) | GREEN | Missing truths and extras cannot increase within a lattice. |
| `L.Lat_subset` | Lattice closure | GREEN | Correct nesting of descendant lattices. |
| `L.lemma2a` | Lemma 2(a) | GREEN | Supplies progress closure of the lattice and region. |
| `L.TDP_of_TDP'` | Concrete-to-abstract TD′P | GREEN | Derives the abstract closure requirement from concrete moves. |
| `L.theoremA2_lattice` | A2, path geometry | GREEN | Supplies lattice/region containment and strict progress to truth. |
| `L.theoremA3_lattice` | A3, sufficient-cap corollary | GREEN | Correct certified-return result for `ℓ ≥ Φ(Sc)`. |
| `L.Φ_le_of_mem_Rad` | A3 / Repair R3 | GREEN | Establishes why `ℓ ≥ a+d` suffices. |
| `L.card_le_of_mem_Rad` | Feasible-region connection | GREEN | Establishes feasibility when `s₀+d ≤ K`. |
| `L.flipSwap_sdiff_card` | Move-table accounting | GREEN | One move adds and removes at most one index each. |
| `L.mis_ext_step` | A2 lower-bound accounting | GREEN | Each move reduces each discrepancy count by at most one. |
| `L.Φ_self` | Potential at truth | GREEN | Correct zero terminal potential. |
| `L.theoremA2_lattice_count` | A2, quantitative conclusion | GREEN | Exact swap-adjusted identity, lower/upper bounds, and drop sizes. |
| `L.drop_two_swap` | Move table / A2 swap count | GREEN | Every two-unit drop is an extra→truth swap. |
| `L.swap_extra_truth_drop_two` | Move table / A2 swap count | GREEN | Every extra→truth swap produces a two-unit drop. |
| `L.DS_move` | One-state progress event | GREEN | Strict separation forces any best-improvement choice to progress. |
| `L.theoremA3_lattice_only` | A3, lattice-only alternative | GREEN | Uses only `(L)` and `D_S` within the centre lattice. |
| `L.theoremA3_lattice_tau` | A3 / Repair R3 | GREEN | Concrete cap/score result; actual-count interpretation is supplied compositionally. |

**Objections**

None remain blocking. The round-1 RED entries concerned missing coverage; the added statements now supply that coverage without changing the frozen cores.

**Minor remarks**

- **The standalone A3 interfaces could identify τ more explicitly.** Their existential witnesses are not expressly declared first hitting times. This is not a remaining coverage failure: A2’s strict pre-τ moves and terminality force its witness to be the actual move count, and `path_stays` yields certification for every larger cap. An explicit first-hit or actual-move clause would make the named A3 results easier to use directly.

- **`theoremA3_hpm` itself is a ledger score-bound theorem.** The explicit reported-maximiser and tie conclusions occur in `lemma0c_hpm`. The package covers recovery, but that distinction should remain clear.

- **Production semantics remain the recorded abstraction.** Under A-T37-2, stationary padding and `M(returned)=none` represent capped iteration and the final certification scan. There is no separate runtime `local_limit` flag or implementation-verification claim.

- **Feasibility is now connected explicitly.** `Rad` still omits a size predicate, but `card_le_of_mem_Rad` supplies the stated `s₀+d ≤ K` bridge. The lattice-size comment `2^Φ` agrees with the lattice definition, although no standalone cardinality theorem is exported.

- **The A4/A5 scoping is honest.** The header explicitly limits A4 coverage to the recorded components and excludes A5. It does not claim that progress is necessary merely for arrival within Φ; therefore it respects Repair R3. Those excluded clauses do not create a fidelity failure here.

OVERALL (T37): GREEN
exit 0
