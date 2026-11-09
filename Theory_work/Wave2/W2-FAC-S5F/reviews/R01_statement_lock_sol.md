REJECT

The target class is relevant to HQ, and separating a hypothetical-start bulk theorem from conditional end-phase completion is legitimate. However, v1 contains a false gain formula, a contradictory terminal-set clause, missing hypotheses in the method-level conclusion, and unsupported frontier/evidence claims. The plan is a plausible research programme, not yet a sufficient justification of the advertised conditional exponent. These are statement-lock objections, not objections to asymptotic scope or large onsets. I used no git commands and wrote only this review file.

Required changes

1. Correct the gain formula and distinguish additions, deletions and swaps.

   Sentence to change: “all neighbour gains are size terms plus −(n/2)log(1 + σ²Z²/RSS_T) + O(1)” (`Theory_work/Wave2/W2-FAC-S5F/STATEMENT.md:16`).

   Replacement: “For null flips at T containing S₀, the proposed uniform reductions are G_del(j;T) = Δ_k − (n/2)log(1 + σ²Z²(j;T)/RSS_T) + O(1) and G_add(l;T) = −Δ_{k+1} − (n/2)log(1 − σ²Z²(l;T)/RSS_T) + O(1). Swaps use the exact telescoping identity below. L0 must specify the simultaneous event, uniform remainder and domain of each reduction.”

   Reason: RSS increases on deletion and decreases on addition. The printed formula assigns additions the wrong likelihood sign. For an addition with positive RSS increment, the likelihood contribution must be positive. This follows directly from D0, `Theory_work/State_of_Project/sections/04_theory.tex:71`, and the RSS definitions at STATEMENT:56–58. Retain the ridge, global response scaling and .02 rate in proving the O(1) approximation; RSS itself is not the exact shipped Q score. Do not extend this null-flip approximation to arbitrary truth moves without a separate error argument. Amend PLAN:7–9 accordingly.

2. Remove the terminal-set contradiction in (C3).

   Sentence to change: “(i)–(ii) of (C2) hold at every visited set” (STATEMENT:91–92).

   Replacement: “(i)–(ii) of (C2) hold at every visited set T ≠ S₀. At S₀ every feasible neighbour has strictly smaller F.”

   Counterexample to the literal wording: take any successful path ending at S₀, including the admissible case m₀ = 0. At S₀ there is no null to delete and no improving chosen move, whereas (C2)(i) requires both. FAC-B correctly excludes S₀ in its path lemma (`Theory_work/Wave2/W2-FAC-B/STATEMENT.md:110–120`).

3. Add start-mode visibility to the method-level consequences.

   Sentences to change: “Under the hypotheses of (C3) (incl. (CC_θ)) and the implementation premises” and “Unconditionally, when p_n ≤ n^{c₀}/C₀ eventually, the same conclusions hold without (CC_θ)” (STATEMENT:96–99).

   Replacements: “Under the hypotheses of (C3), (FS-B), and the implementation premises …”; and “Under G, (BCS), (P), (θ), (FS-B), the implementation premises, and p_n ≤ n^{c₀}/C₀ eventually, the same conclusions hold without (CC_θ).”

   Reason: (C2) and (C3) concern a search artificially started at S*. Only (C1), which assumes (FS-B), identifies the emitted production start with S*. Neither e4′ nor the prefix property identifies an arbitrary start maximiser with S*. The source theorem retains FS in its assembly (`Theory_work/Wave2/W2-FAC-B/STATEMENT.md:124–134`). Alternatively prove a different discovery argument without FS-B; it cannot be inferred from the present claims. Preserve the inherited Proposition F allocation and ideal-machine premises and the exact-enumeration convention (`Theory_work/Wave1C/FINAL/sections/s7_impl.tex:40–48`).

4. Repair the bulk move count and the zero-null case.

   Sentence to change: “Consequently the path performs exactly m₀ − m_e + 1 … i.e. all its first m₀ − m_e + 1 moves are null deletions (it visits sets with m_T = m₀, m₀ − 1, …, m_e − 1)” (STATEMENT:85–86).

   Replacement: “Let d_bulk := max{0, m₀ − m_e + 1}. The first d_bulk moves are null deletions; when d_bulk > 0 their centres have null counts m₀,…,m_e and their final destination has m_e − 1 nulls. If m_e = 1, the path reaches S₀ after m₀ moves, with a separate terminal-neighbour argument establishing termination, also when m₀ = 0.”

   Reason: the current count can be negative. Bounded p and a method block containing all variables can give S* = S₀. Define min ∅ = +∞ and max ∅ = 0 for the nonnegative level/hole statistics, or explicitly restrict their domains to nonempty index sets. The terminal-neighbour result does not follow from a statement quantified only over m_T ≥ 1. Fixed-p enumeration is part of the method, not a limitation (`Theory_work/State_of_Project/sections/02_method.tex:167–170`).

5. Make section 3 a usable lock, including the CC quantifiers and the signed drift residual.

   Sentences to change: “for T ⊇ S₀ and null l this is the squared standardized partial correlation …, a χ²₁ variable for fixed (T,l)” (STATEMENT:57–58); “c̄_T − c̄_{T∖j} = κ_T(j)·r_j(T) with κ > 0” (STATEMENT:20); and the CC definition at STATEMENT:70–72.

   Replace “squared standardized partial correlation” with “[x_lᵀ(I−P_T)ε]²/[σ² x_lᵀ(I−P_T)x_l], a squared standardized Gaussian projection, χ²₁ for deterministic (T,l). No χ² or independence assertion is made conditional on an adaptively selected T.”

   Define r_j(T) := g_j − Σ_{j,A}Σ_{A,A}^{−1}g_A, A := T∖{j}. Then the exact drift coefficient is Cov(√aη,g_j | g_A)/Var(g_j | g_A), which is positive for this BCS model. If another normalization of r_j is intended, give its corresponding coefficient. Squared Z statistics cannot determine the signed drift. Define the signed local statistics, s_max, and the s and c_m used in (C3), which currently have no definitions. Also define U_G := T∩G and distinguish the bound on true projection statistics from any ridge scanner approximation.

   Replace CC by a quantified simultaneous bound: for fixed class parameters and θ, specify a deterministic r_n = o(H_n) and events E_n with P(E_n)→1 on which the displayed bound holds simultaneously for all stated centres and one-below sets. Specify whether the path is stopped at the first departure from [S₀,S*], or extend all relevant definitions to arbitrary visited sets. Do not condition independent local noises on the selected path. PLAN:16–19 must construct simultaneous configuration/order-statistic events first. The enlarged Gaussian representation and posterior-mean interpretation are otherwise consistent.

6. Separate statistical groups from method blocks, and make sign correction explicit.

   Sentences to change: “where H_n is the indicator matrix of a deterministic partition …” (STATEMENT:38–40) and “λ_min(Σ_n) = c =: c_min” (STATEMENT:40).

   Replacement: “Let G₁,…,G_{J_G} denote the statistical correlation groups defining H_n, distinct from the actual method blocks C_b incorporated from FAC-B. No coincidence of these partitions is assumed. After replacing X by XΥ_n and θ* by Υ_nθ*, all subsequent Σ, g and partial-covariance formulas use Σ = a11ᵀ+bH_n+cI. We use the uniform lower bound λ_min(Σ_n) ≥ c =: c_min.”

   Reason: equality with c is false in the permitted singleton-group case: H_n=I gives minimum eigenvalue b+c for p≥2. The lower bound suffices for H0. N₀ must use method blocks C_b, not correlation groups. The production partition has correlation linkage, lexicographic merge ties, size cuts and packing; it is not simply the S5 group partition (`Theory_work/State_of_Project/sections/02_method.tex:187–211`). FS-B must be evaluated after sign correction, not by multiplying the signed Σ by the already sign-corrected ϑ. State the coordinate ordering of ϑ as in FAC-B STATEMENT:76–78. K=p is correct under (P); retain the production score-tie rule rather than imposing an alternative residual-based rule.

7. Supply the missing pathwise hole and one-below argument; the listed tools alone do not close it.

   Sentence to change: “hole bound via L0.2 within the group plus the centre; the four gain comparisons with margins c₂ log n” (`Theory_work/Wave2/W2-FAC-S5F/PLAN.md:19–20`).

   Replacement: “Prove a pathwise bound for every previously deleted null, in terms of explicitly defined historical local deletion energies and current centre; account separately for initially omitted N₀. Establish the needed no-addition bound at every T∖j for every outgoing null j, including at the bulk/end boundary. Only then apply the exact swap identity and compare every deletion with the best exact-score deletion.”

   Reason: the Pythagorean inequality is correct: with A=T∖j and B=T∪l, RSS_A−RSS_B equals both Z²(j;T)+Z²(l;T) and Z²(l;A)+Z²(j;B), in σ² units. But iterating it produces accumulated historical energies, not automatically (q−1) times the current level. Local a=0 statistics also require transfer to the chosen exact-score deletion. Non-improvement of additions at T says nothing by itself about additions at T∖j. Initial omissions N₀ never incurred a deletion energy and are absent from h(T), although they remain feasible additions and swap entrants. The bulk claims at m=m_e additionally need one-below sets with m=m_e−1. The swap telescoping identity is exact and sufficient once all these one-below additions have negative gain. A Gaussian counting bound and a top-order-statistic centre bound do not replace this missing pathwise lemma.

8. State an actual conditional exponent, and distinguish the remaining research target from an achieved improvement.

   Sentence to change: “there is an explicit A*(θ) … with A*(θ) → min{1,(q−1)/(2q−4)} as θ → 0” (STATEMENT:88–90).

   Required replacement or reason: provide a formula for a sufficient A*(θ), its allowed θ range, and the inequalities from which its positivity and limit follow; otherwise label the displayed limit a conjectured target rather than a locked conclusion. Identify which structural bounds are to be proved unconditionally, and which gain comparisons actually use CC. Include a proof obligation treating bounded, slowly growing and oscillating p separately from estimates requiring H→∞ or L_n=o(H). For bounded p, a fixed deterministic θH+o(H) bound on the nondegenerate Gaussian centre generally cannot hold with probability tending to one; the unconditional small-p route should carry that case.

   HQ asks for the largest provable unconditional improvement beyond 1/6 if full p≤n/2 is out of reach. A conditional 2/3 target plus an unquantified c₀ does not establish such an improvement. Give an explicit unconditional exponent if obtained; otherwise report PARTIAL with the unresolved end-phase lemma. The current “not claimed” paragraph honestly disclaims unconditional improvement, and that distinction must survive into REPORT. Exact-Gram S5 is relevant, but does not cover iid-row study designs, which FAC-A treats separately (`Theory_work/Wave2/W2-FAC-A/REPORT.md:32–43`).

9. Replace unsupported “exact obstruction” and sharpness wording by route-specific open obligations.

   Sentences to change: “that part is stated as an explicit hypothesis (CC) and is the exact obstruction” (STATEMENT:26); “(CC_θ) is the exact obstruction” (STATEMENT:100); and “nearly attained numerically … and limits A*(0) to …; sharper within-group control (a gap-type invariant) would be needed beyond” (STATEMENT:103–104).

   Replacement: “CC_θ is an unproved sufficient end-phase hypothesis for this proposed route. No necessity for consistency, or optimality among proof routes, is claimed. The proposed hole estimate yields the stated sufficient exponent only after the historical-energy and gain comparisons are proved; its optimality is open.”

   Reason: no theorem here shows CC necessary, or a counterexample when it fails. A finite numerical hole/current-level ratio is not a lower bound saturating a uniform local historical-energy inequality with vanishing centre bias. FAC-A's sharp result is different: it supplies an explicit noise-selected full-lattice witness on CS, not a path witness on S5 (`Theory_work/Wave2/W2-FAC-A/lemmas/L6_sharp.md:12–18,29–47`). Qualify STATEMENT:12 as “FAC-A proves sharpness of the full-lattice exponent on CS, hence for a theorem uniform over the containing class”; it does not prove S5-specific route sharpness. The HQ audit similarly insists on retaining signed swap information (`Theory_work/Wave2/HQ_AUDIT/B3_facB_redteam.md:17–42`).

10. Correct the numerical evidence before using it to motivate CC or full production paths.

    Sentence to change: “numerics N2 observe θ ≤ 0.13 (≤ 0.05 in the bulk) and pure deletion paths to S₀ for log p/log n up to 0.92” (STATEMENT:101–102).

    Replacement: “Exploratory flip-only trajectories are recorded by numerics/n2_centre.py and numerics/n2_log.txt; they do not verify production flip-and-swap trajectories or CC_θ. The logged statistic omits the factor offset and uses a different normalization and bulk definition from CC. No numerical upper bound on θ is asserted until those quantities and the scanner are corrected.”

    Evidence: `Theory_work/Wave2/W2-FAC-S5F/numerics/n2_centre.py:42–44` records δ = aΣỹ/d/(1+aW), with √aη/(1+aW) stored separately. CC uses δ′=δ−√aη/(1+aW), and normalizes by √d₁ H, whereas N2 reports δ/H. At `:71` it calls want_swaps=False; `numerics/bcs_core.py:192,268–275` confirms swaps are omitted from the actual scan. N2's “bulk” is k≥50 (`n2_centre.py:78`), not m≥m_e. Even its different logged ratio reaches 0.169 (`numerics/n2_log.txt:12`), exceeding 0.13. Likewise N3's monitored paths disable swaps (`numerics/n3_tools.py:238`). Keep these as exploratory checks, or redo the relevant comparisons with complete scans. Numerical observations do not prove CC or the claimed limiting exponent.

Optional suggestions

- Keep C1, hypothetical-start C2, conditional C3, and method assembly C4 as separate theorem cards. This makes the dependence on FS-B and CC visible.
- The level-counting and top-order-statistic strategies are reasonable: there are O(p2^q) local configurations and independent Gaussian group noises before adaptive selection. Prove simultaneous events from those primitives; do not assert independence of statistics conditional on the retained groups.
- Use the valid exact projection identity and signed posterior-update identity as early checked lemmas. Require the later hole-history lemma to state precisely which energy maximum appears; avoid switching between current level, running level and local historical level.

This verdict does not refute consistency of the merged method on S5. It rejects locking v1 as written. No objection concerns asymptotic-only validity or the size of n₀.
