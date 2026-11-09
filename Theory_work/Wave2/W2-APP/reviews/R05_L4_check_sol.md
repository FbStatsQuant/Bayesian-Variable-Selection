Verdict: **FALSE as written**. The principal positive implications can be retained after repairs, but the map contains false exclusions and overstates several cited inputs. No FATAL finding; six MAJOR and three MINOR findings below. This review takes L1_POST, L2_CT, L3_LOC and L5_VN as given, and checks their application rather than reopening their proofs.

1. **MAJOR — Factor row applies equicorrelation conclusions to a much larger class.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:100-107,124`.

   Problem: the summary says that equicorrelation / factor designs are obstructed whenever the coefficient sum is nonzero and p grows, and labels the whole class “not LOC.” L5 (V4) requires a growing set of null loadings bounded below and a fixed positive factor exposure. Neither follows from a correlation eigenvalue floor or a nonzero coefficient sum. For a concrete counterexample, take b_j = 2^{-j}, Ψ_jj = 1-b_j², S₀={1}, θ₁=1. Then ψ_j≥3/4, the coefficient sum is 1, and p can grow polynomially. Nevertheless |Σ_jk|=2^{-(j+k)}≤2^{-|j-k|}; the spectrum lies in [3/4,4/3], so this is LOC with fixed constants. PTV holds with a₀≥3/4, and Theorem LOC applies. For each fixed b₀>0 the loaded null set is bounded, so VN does not give the table's obstruction.

   The prose also allows varying ρ_n under only a floor on 1-ρ_n. That suffices for POST, but not for the fixed-ρ VN (V3) conclusion: e.g. ρ_n=n^{-1}, p=n, s₀=1 gives squared visible-null correlations of order n^{-2}, violating nκ_n/log n→∞. Even λ_max≈p is false for this extension.

   Repair: split fixed positive equicorrelation, varying equicorrelation, and general factor models. For fixed positive equicorrelation state the uniform coefficient-sum floor; for one-factor models state all V4 loading/exposure floors and the growth conditions on the loaded null set. For varying correlation verify VNF quantitatively before asserting obstruction. Replace general factor “not LOC” by “locality depends on loadings; pervasive fixed positive equicorrelation is not LOC.”

2. **MAJOR — Growing bandwidth does not imply failure of LOC.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:75-76`.

   Problem: “b_n→∞: not LOC with fixed constants” is false, even for the minimal bandwidth in the displayed ordering. Put p_n=n and Σ_n=I+(e^{-(p_n-1)}/4)(e₁e_pᵀ+e_pe₁ᵀ). Its exact bandwidth is p_n-1, its spectrum is in [3/4,5/4], and its only off-diagonal pair satisfies LOC-Σ with K=1/4, a=1. With one truth, PTV is automatic and LOC applies. More generally a growing support range can coexist with uniform exponential decay. An alternative ordering may also greatly reduce bandwidth.

   Repair: write “growing bandwidth alone does not provide fixed LOC constants; covered if uniform exponential decay and spectral bounds hold, otherwise not classified here.” Do not label every such sequence non-LOC.

3. **MAJOR — MIS neighbour equivalence omits the single-active-omission hypothesis.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:63-65`.

   Problem: Prop. P(d) applies with exactly one active omitted variable k, and Θ is the precision of the marginal vector (W_𝒞,W_k). The entry does not impose that hypothesis. With multiple active omissions, neighbouring contributions can cancel. Example: AR(1), ρ=1/2, 𝒞={2}, omitted actives {1,3}, raw slopes β₁=1, β₃=-1. Candidate 2 is a precision-neighbour of both omissions, but γ₂=(1/2)-(1/2)=0; it is not a proxy. This follows directly from MIS (iii), not a failure of that result.

   Repair: explicitly restrict the iff statement to one active omitted variable, nonzero omitted raw slope, and the marginal precision. Explain that AR(1) neighbours mean nearest retained coordinates on either side, when present, rather than necessarily k±1 in the full original index set. With multiple omissions give only support containment and warn about cancellation. Source: `Theory_work/Wave1C/C-MIS/STATEMENT.md:79-90`; FIN `s3_posterior.tex:46`.

4. **MAJOR — Summary drops LOC-B's indispensable enlarged-Q bound.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:123` (compare correct prose at lines 93-94).

   Problem: the table grants LOC-B from s₀(g_n-1)≤(1-δ₀)log n alone. L3.8B additionally requires p-s₀≤(1-δ₀)log n when the enlargement rule gives Q=[p]. For example, one truth, g_n≈0.75 log n and two equal groups give p≈1.5 log n. The initial inequality holds with δ₀=0.2, but enlargement occurs because p<2|Q⁰|+33, and the enlarged χ bound fails. The cited lemma does not cover this case. Thus “covered small-log” also needs qualification; the stated middle regime is not the entire unresolved region.

   Repair: put both inequalities in the table, or explicitly say “LOC-B under all its stated hypotheses, including the post-enlargement bound”. Describe uncovered cases by failure of either bound. Source: `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md`, §L3.8B; STATEMENT claim (C), v1.2.

5. **MAJOR — Bounded block size alone does not supply the spectral floor.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:79-81,122`.

   Problem: entry (e) and its table label omit the fixed spectral hypotheses present in F2 and target claim (E). “F2⇒LOC” is only valid when every block has spectrum in a common [c,C], c>0. Bounded size by itself is insufficient: independent size-two blocks with within-correlation ρ_n=1-n^{-2} have λ_min=n^{-2}. Neither POST's LSF(i) nor LOC's fixed spectral floor follows. One truth per block gives a conditional-variance bound involving n^{-2}, not the required fixed a₀. For bounded g and unit diagonal, the uniform upper bound follows from g; the lower bound still must be assumed.

   Repair: add “with a uniform positive spectral floor (hence spectrum in fixed [c,C])” to the family heading and table row. State that equicorrelation parameters stay uniformly away from the singular endpoints. Retain the correct fixed-ρ examples in F2.

6. **MAJOR — PXN citation silently changes the signal convention.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:5-7,84-85,122`.

   Problem: the global setting fixes coefficients on sample-standardised columns, while the cited LH-iid PXN model uses fixed raw slopes, with exact population masking in the raw model. In GEN L6(b) this distinction is explicit: y^r=X^rθ+ε and θ*=D_xθ. In FIN's PXN family the masked pair uses β_i and -ψ_iβ_i on the raw scale. Fixing those same values on sample-standardised columns does not preserve the exact finite-sample masking relation used in the cited theorem. A theorem for the resulting perturbation is not supplied by L1-L3-L5. The file already makes the necessary model override for F4/MIS but not here.

   Repair: label this as a separate cited raw-slope LH-iid model, give its masked-pair convention, and retain PXN's complete LH-iid assumptions and SIZE. Alternatively prove a standardised-signal perturbation extension before claiming coverage. Also identify bounded independent components as linked pair units of size at most 2g, rather than implying that the linked g-groups themselves are independent blocks.

7. **MINOR — Study citations need the actual asymptotic sequence and layout restrictions.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:47-48,62-63,81-83,116,118,122`.

   Problem: “groups of 5, one truth per group” is not the complete scope of GEN (C5)(d). Its cited sequence has p_n=5G_n→∞, p_n≤n^A, s₀=14, one of the fixed step-7/step-13 high-p layouts, the specified 14-entry coefficient pattern times a fixed c>0, and σ²=1. It is not a citation covering arbitrary layouts, the p=30 layout, shrinking scales, or a finite n=200 run. GROW explicitly covers asymptotic extensions of the p=500/1000 S2 layouts. The table's “AR(1): not covered” GEN cell also generalises the specific GEN L6(d) S2 exclusion to every AR(1) regime (fixed p in particular is different).

   Repair: give one precise shared “study sequence” definition and reference it in each citation. State S2/S5 are outside GEN L6(d)'s sufficient class for that sequence; do not generalise that exclusion to all AR(1). Preserve the production-cap statements for GEN/SEL and the shipped augmented cap for GROW/LOC. Broader coverage can separately be derived from LOC under its actual hypotheses.

8. **MINOR — Summary's unconditional “covered” and “iff” wording is stronger than the map.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:34,117-122`.

   Problem: rows with genuine added PTV/separation conditions have a bare “covered” in the reported-model column. The +θ legend helps, but a standalone status cell should not discard the condition. The bounded-spectrum row's “LOC iff exp.-local ordering, +PTV” also mixes covariance-class membership with the signal hypothesis: membership does not require PTV, and no necessity theorem for reported consistency was proved. Similarly the explicit masked block at line 34 is in the covariance class LOC; it is outside Theorem LOC's signal hypotheses.

   Repair: use “covered under PTV / separation and implementation premises” in the affected status cells; distinguish “Σ∈LOC” from “Theorem LOC applies.” Replace “Such masked configurations are outside LOC” by “fail PTV and are not covered by Theorem LOC.” None of these results establishes delivery probability tending to one.

9. **MINOR — Long-memory use needs an explicit extension of F1's hypotheses.**

   Location: `Theory_work/Wave2/W2-APP/lemmas/L4_families.md:14-19,69-70,120`.

   Problem: F1 formally assumes absolute summability and a bounded spectral density. Its long-memory parenthesis and later application leave that stated domain. The desired lower bound is correct, but it should follow from a separately stated spectral-representation assumption rather than the absolutely convergent Fourier-series definition in line 15. A pointwise assertion f(0)=∞ is by itself not a definition of long memory, since changing a density at one point does not change the covariance.

   Repair: state the lower-bound variant for a stationary covariance with an integrable spectral density f and γ(h)=∫e^{ihλ}f(λ)dλ, with f≥m>0 almost everywhere and the normalised lower bound uniform in n. The same finite-polynomial integral proof gives λ_min≥2πm/γ(0) without summability or a finite upper bound. Define any non-LOC long-memory subclass by its actual tail or unbounded essential spectral density.

Checks that passed (including numerical recomputation):

- F1's 2π/γ(0) factors and Parseval calculation are correct on its stated summable domain. Every finite principal submatrix is covered, including nonconsecutive indices.
- F2's banded constants K=e^{g-1}, a=1 are correct for correlation matrices with the stated spectral floor. The precision-banded input uses K=e^b/c, as L2 specifies. For g=5, the study eigenvalue intervals are [1,1], [0.3,3.8], [0.15,4.4], and for S6 a common envelope [0.1,4.6].
- F3(i), the conditional-covariance decomposition, and F3(ii)'s D*=t₂^{-1}log(2s₀θ_hiK₂/(cθ_lo)) are valid sufficient bounds. Using s₀ instead of s₀-1 is conservative; singleton truth separation is vacuous. F3(iii)'s a₀=(θ_lo/2)(1-ρ²)/(1+ρ²) agrees with GROW L6.2. The cancellation example yields Σ(1,-2)ᵀ=(0,-1.5)ᵀ, so U=∅ genuinely violates PTV at coordinate 1.
- F4's projected-support containment and |S₀^𝒞|≤s₀ max_G|G| are correct. The latter bound includes both retained truths and omitted-truth blocks. It supplies bounded support size, not automatically a fixed positive support cardinality, projected beta-min, or fixed residual variance; the file correctly retains MIS's additional premises. The iid formula at line 49 is correct in MIS's separately stated raw-slope model.
- Recomputed the 14-entry pattern: sum=0.8, sum of squares=24.64, so the P-SEL energy envelope is 49.28c²+1 and the S5 null-group population covariance is 0.24c. The step-7 and step-13 truth layouts have minimum index gaps 32 and 62. At ρ=1/2, the maximum ratio of the LHS of (6.0) to its RHS is respectively approximately 1.16819541695×10^{-9} and 1.08796676336×10^{-18}; every fixed positive scale cancels from these ratios. Thus the S2 separation citation is numerically sound for those layouts.
- STAR's spectrum {1/2,1,3/2}, count min(K-1,m_n-15), and its route-only interpretation match V1. The growing-block VN conclusions match V2 under fixed positive within-correlation and one truth per block. The fixed-positive-equicorrelation count min(K-s₀,p-16s₀) matches V3 under its quantified signal floor.
- The quoted package statuses GEN, PXN, C-GROW and C-MIS “PROVED-CHECKED,” and SEL “VERIFIED-WITH-AMENDMENTS,” agree with FIN and the amendments. GEN L6(d)'s literal “Not covered: S2 ... and S5 ...” is a sufficient-class exclusion, not method inconsistency. C-GROW (C6) is explicitly “Frontier (with evidence, not proved).” No FAC report was present at either ticket's REPORT.md path; no FAC result was inferred or upgraded.

Review performed read-only apart from this requested review file and the permitted scratch directory. Numeric calculations used `C:/Users/felip/anaconda3/python.exe`. No git commands were run.
