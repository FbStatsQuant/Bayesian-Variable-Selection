I checked L3 against STATEMENT.md §§1–2, L0, GEN-L1, and the method’s block definition. I found no counterexample to the stated sandwich and no proof gap requiring an amendment. This assessment uses the full stated (G1), including |Q| ≤ K, and the fixed constants and fixed s₀ in G.

1. **Per-block optimality and feasibility — L3 lines 28–30, 38–40, 76–86.**

   For any maximiser S̃ and proposed within-block set U, the comparison model is
   S′ = (S̃ ∖ C_b) ∪ U. Its size is exactly k̃ − |Ũ_b| + |U|, and all other block factors cancel. Thus (3.1) is correct whenever the displayed cap condition holds. This does not require S̃ to be a coordinatewise unique maximiser.

   The Step 1 comparison deletes all N_b, so it is feasible even when k̃ = K. The NEG telescoping sets are all subsets of C_b; they need not be globally optimal or feasible replacements, because they are used only to decompose a projection. All table sets are scored by the method, with B ≤ K eventually.

   Truth addition in Step 2(a) is feasible: if Q ≠ [p], the ladder gives k̃ ≤ 2|Q| + 32s₀ < K. If Q = [p], (G1) and K ≤ p give K = p. A maximiser missing a truth then has k̃ < p = K. Junk deletion in Step 2(b) is always feasible. There is no circular use of truth inclusion to establish addition feasibility.

2. **The initial size bound (3.2) — lines 34–36.**

   Every bad block contains at least one omitted truth; disjointness of the partition bounds the number of bad blocks by s₀. Their total selected size is at most s₀B. On good blocks, selected elements are either in Q or in N_b. Consequently
   \[
   k̃\le |Q|+s₀B+\sum_{b\ {\rm good}}|N_b|
      \le k₀+B\,\#\{b\ {\rm good}:N_b\ne\varnothing\}.
   \]
   Counting all of Q and then all selected elements of bad blocks may overcount, which is harmless for this upper bound. The argument includes maximisers missing truths and maximisers at the cap.

3. **Derivation of (3.3) — lines 38–48.**

   Put d = |N_b| and V = Ũ_b. The exact prior ratio gives
   \[
   \log\frac{w(k̃-d)}{w(k̃)}
      =\sum_{t=k̃-d+1}^{k̃}\log\frac{2p-t}{t}
      \ge d\log\frac p{k̃},
   \]
   because every t ≤ k̃ ≤ K ≤ p. The prior’s direction and sign are correct, including k̃ = p.

   Since U ⊆ V and the within-block Gram is nonsingular, Π = P_V − P_U is an orthogonal projection of rank d. Centering gives ΠC = Π, and hence
   \[
   {\rm RSS}_U-{\rm RSS}_V=\|\Pi\mu+\Pi\varepsilon\|^2.
   \]
   The displayed split has the correct coefficients:
   \[
   \|a+b\|^2\le(1+\varepsilon_1)\|b\|^2
                    +(1+\varepsilon_1^{-1})\|a\|^2.
   \]

   The successive residualised directions form an orthonormal basis of the increment space: each new direction is orthogonal to the span of all preceding columns. Therefore
   \[
   \|\Pi\mu\|^2=\sum_{s=1}^d\delta_{U_{s-1},l_s}^{\,2}.
   \]
   Every conditioning set still contains the block’s truths, and every added variable lies outside Q. NEG applies at every step, so this sum is at most dησ² log n. No cross-block orthogonality is assumed.

   L0.2(b)’s **second** display applies to the whole nested pair U ⊆ V and uses the RSS floor at V. No small-x condition is needed here. Together with the two-score remainder,
   \[
   d\log(p/k̃)\le-\tfrac d2\log(n+1)
       +\tfrac{1+\vartheta_n}{2}
        \big[(1+\varepsilon_1)dW_b+
                    (1+\varepsilon_1^{-1})d\eta\log n\big]+2\kappa_E.
   \]
   After multiplying by 2/d, the remainder is 4κ_E/d. Replacing it by 4κ_E weakens the resulting lower bound on W_b because d ≥ 1. This proves precisely (3.3). There is no missing factor d or accumulation of d score remainders.

4. **Chi-square tail, pair count, and (3.4) — lines 20–24, 55–60.**

   For each deterministic pair (V,N), the increment projection has rank d = |N| ≥ 1, so its noise energy divided by σ² is χ²_d. The Chernoff bound
   \[
   \Pr(\chi_d^2\ge d\tau)
        \le(\tau e^{1-\tau})^{d/2}
        \le\sqrt{e\tau}\,e^{-\tau/2},\qquad \tau>1,
   \]
   is correct. A block of size t has exactly 3^t − 2^t admissible pairs: a coordinate is outside V, in V∖N, or in N, with N nonempty. Thus 3¹⁶ is a valid uniform upper bound.

   The method produces nonempty disjoint blocks partitioning [p], so J ≤ p despite possible packing gaps. This justifies the factor p in E C(τ); replacing it by an assumption such as J = ⌈p/B⌉ would not be justified, but the proof does not do that. No independence between blocks is used.

   With a_n = 1 + ε₂ and η₁ as defined in the proof,
   \[
   e^{-\tau_n(k)/2}
      \le e^{2\kappa_E/a_n}
        n^{-(1-\eta_1)/(2a_n)}(k/p)^{1/a_n}
      \le e^{2\kappa_E}
        n^{-(1-\eta_1)/(2a_n)}(k/p)^{1/a_n}.
   \]
   Positivity of the numerator and a_n ≥ 1 justify the upper bound on τ_n(k) used for its square-root prefactor. The power of p in (3.4) is therefore p^{ε₂/(1+ε₂)}, exactly as written. The estimate holds uniformly for deterministic 1 ≤ k ≤ p.

5. **Choice of ε₁, continuity, and the size ladder — lines 52–70.**

   For η > 0, minimising
   \[
   A\varepsilon_1+\frac{\eta}{2\varepsilon_1}+\frac\eta2
   \]
   gives ε₁ = √(η/(2A)) and minimum √(2Aη) + η/2. The strict inequality required by the proof is equivalent to
   \[
   \eta<(\sqrt{2A+1}-\sqrt{2A})^2.
   \]
   For η = 0 the infimum is not attained, but the proof separately supplies a valid positive ε₁ < 1/(2A); the word “minimum” in the general explanatory sentence causes no substantive issue.

   The continuity step can be made explicit. If
   \[
   \xi_*=\frac{1-(1+\varepsilon_1^{-1})\eta}{2}
                         -A\varepsilon_1>0,
   \]
   then
   \[
   \varepsilon_2=\varepsilon_1+(1+\varepsilon_1)\vartheta_n,\qquad
   \xi_n=\xi_*-\vartheta_n
       \left[\frac{(1+\varepsilon_1^{-1})\eta}{2}
                             +A(1+\varepsilon_1)\right].
   \]
   Since ϑ_n → 0 deterministically, eventually ξ_n ≥ ξ_*/2. Also ε₂ ≥ ε₁ > 0 and ε₂ stays bounded. Thus both the geometric-series constant and the final positive exponent are uniform in n. No rate restriction on p beyond p ≤ n^A is hidden here.

   The intervals (m_i,m_{i+1}] cover every k̃ > 2k₀, including ladder endpoints. For any offending maximiser,
   \[
   C\!\left(\tau_n(\min(m_{i+1},K))\right)>\frac{m_i}{2B}
   \]
   for some i. Its threshold is deterministic and independent of the maximiser. Taking a union over these count events therefore bounds the existence of **any** oversized maximiser; it is stronger than a bound for a preselected tie rule.

   The input min(m_{i+1},K) is at most K ≤ p, as required for (3.4). Bounding its power by (2m_i)^{1/(1+ε₂)} is legitimate even when 2m_i > p: (3.4) is applied before that replacement. Extending the sum to all i only enlarges the bound.

   Finally,
   \[
   \frac{(2m_i)^{1/(1+\varepsilon_2)}}{m_i}
      \le2\,2^{-i\varepsilon_2/(1+\varepsilon_2)}
   \]
   because k₀ ≥ 1. Using B ≤ 16 and p ≤ n^A yields the exponent
   \[
   -\frac{(1-\eta_1)/2-A\varepsilon_2}{1+\varepsilon_2}
      =-\frac{\xi_n}{1+\varepsilon_2},
   \]
   bounded away from zero on the negative side. Thus the probability tends to zero, even for highly dependent block noises and near-saturated candidate modes.

6. **Truth inclusion — lines 76–82.**

   GEN-L1.4(b) has the required direction: a nested RSS decrease gives a likelihood gain at least ΔRSS/(2C_R). The prior addition cost is bounded below by −log(2p). The quadratic inequality
   \[
   (\delta+\sigma Z)^2\ge\tfrac12\delta^2-\sigma^2Z^2
   \]
   holds for either sign of δ and Z.

   Consequently the log-start-weight gain from adding a missing truth is at least
   \[
   \left[
       \frac{M_n}{4C_R}
       -\frac{\sigma^2(A+1)}{C_R}
       -A-\frac12
   \right]\log n-O(1),
   \]
   uniformly over all relevant blocks, conditioning sets, and maximisers. It is eventually strictly positive because M_n → ∞. The proof needs positivity of this entire gain, not merely of ΔRSS; its stated estimates establish the stronger fact. The Q = [p] full-cap case is handled correctly.

7. **Junk exclusion and uniformity in L — lines 84–91.**

   After truth inclusion, the conditioning set Ũ_b∖{l} satisfies NEG. Set t = log n and h = log log n. Uniformly for 0 ≤ L ≤ At,
   \[
   (\sqrt{\eta t}+z_n)^2
      \le\eta t+2L+2\sqrt{2\eta Lt}
                                      +O(\sqrt{th}+h).
   \]
   This follows from z_n² ≤ 2L + c₃h and
   √(a+b) ≤ √a + √b; no division by L is involved. Hence it remains valid when p is bounded or L/t → 0.

   Substituting this bound into the deletion gain gives
   \[
   \begin{aligned}
   \Delta\log\gamma_0
   \ge{}&\tfrac t2-\tfrac{\eta t}{2}-\sqrt{2\eta Lt}
        -\vartheta_n\left[L+\tfrac{\eta t}{2}
                                      +\sqrt{2\eta Lt}\right]\\
        &-\log k̃-2\kappa_E-O(\sqrt{th}+h).
   \end{aligned}
   \]
   Under the stated threshold,
   η/2 + √(2Aη) < 1/2. Thus the bracket multiplying ϑ_n is at most L + t, justifying the slightly looser bound in line 89. This coefficient is not a missing factor.

   The ladder gives k̃ ≤ 2C_Q log n + 32s₀, so log k̃ = O(log log n) uniformly; k̃ ≥ s₀ ≥ 1 after truth inclusion. Also ϑ_n(L+t) = o(t) uniformly. The remaining coefficient
   \[
   \tfrac12-\tfrac\eta2-\sqrt{2A\eta}
   \]
   is strictly positive exactly under η < η_A. The deletion is therefore a strict improvement for every possible junk variable in every maximiser. Retaining the −log k̃ term until after the ladder is essential and is done correctly.

8. **Probability-one-limit events and simultaneous coverage — lines 15–19, 69–74.**

   The actual partition is deterministic under fixed-design G. With D = A, C_F = 2¹⁶, D_V = 2A, and C_V = 2C_F², the block family and residual-vector family satisfy GEN-L1.1. The block rank bound is fixed at 16. Hence E^blk has probability tending to one; its h_n² and t_n are O(log n), and L0’s ω_n and ϑ_n tend to zero deterministically.

   A block of size t contributes t2^{t−1} single-add directions. The proof’s larger bound 2²⁰p is valid, and its Gaussian union bound gives P(Z-event fails) ≤ 1/log n exactly as stated for sufficiently large n.

   The ladder’s count events require neither independence from E^blk nor independence from the Gaussian direction event. An ordinary union bound suffices. All score, RSS, TV-noise, and NEG-noise estimates hold on common events over the complete deterministic block families. Choosing a data-dependent maximiser after imposing these events is legitimate. There is no uncounted union over maximisers or hidden assumption about absence of ties.

9. **A mode near K is possible in the Q = [p] branch, without contradicting L3.**

   The result proves O(log n) size, not k̃/K → 0 uniformly over both branches of (G1). If Q = [p], then p = O(log n) and K = p eventually; the size ladder is trivially satisfied because k₀ > p.

   For a concrete permitted asymptotic regime, take p = ⌊log n⌋, an exact centred equicorrelation Gram
   R = (1−ρ)I + ρ11ᵀ with fixed 0 < ρ < 1, one truth S₀ = {1}, and μ = x₁. Such designs exist for p ≤ n−1. Choose Q = [p]. The signal norm is n−1, the within-block Gram floor is 1−ρ, TV holds with M_n of order n/log n, and NEG is vacuous.

   In any block not containing variable 1, conditioning on m other variables from that block gives an additional proxy’s squared partial signal
   \[
   \delta^2=(n-1)\,
     \frac{\rho^2(1-\rho)}
          {[1+(m-1)\rho][1+m\rho]},\qquad 0\le m\le15.
   \]
   This is bounded below by a positive constant times n. On the common block events, every such addition gives a likelihood gain of order n against a penalty of order log n. Since K = p, every maximiser must fill every block not containing the truth. Therefore
   \[
   |S̃|\ge p-|C_{b(1)}|+1\ge p-15,\qquad |S̃|/K\to1
   \]
   with probability tending to one. This construction works for the actual partition because the argument uses only its block-size bound.

   This is not a counterexample: S₀ ⊆ S̃ ⊆ Q still holds, and |S̃| = O(log n). If Q ≠ [p], the final sandwich and (G1) instead imply |S̃| ≤ |Q| ≤ (K−32s₀−1)/2 with probability tending to one, ruling out near-cap modes in that branch.

10. **Local numerical checks.**

    I ran Python 3.13 with bytecode writing disabled. A correlated-block projection test gave a telescoping error of 2.66×10⁻¹⁵. The exact deletion-prior inequality passed for every 1 ≤ d ≤ k ≤ p ≤ 100. Threshold, continuity, and uniform L/log n coefficient checks passed in 16 parameter cases, including η = 0 and η = 0.999999η_A. Using bvs_core.partition and start_mode on a centred orthogonal n = 256, p = 64 design, with S₀ = Q = {0} in Python indexing and K = 64, all ten noise draws returned the truth alone. These are finite numerical diagnostics; the simultaneous asymptotic claim is supported by the proof checks above.

VERIFIED

