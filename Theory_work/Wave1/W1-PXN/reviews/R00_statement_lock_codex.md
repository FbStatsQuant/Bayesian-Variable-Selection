VERDICT: LOCK WITH CHANGES

Paths below are repository-relative; NBH = Theory_work/Old_Projects/New_BVS_Headquarters; PXN = NBH/branch_snapshots/API-PXNGAP; W1 = Theory_work/Wave1/W1-PXN; SOP = Theory_work/State_of_Project/sections.

1. **MAJOR — Q1/Q2: the headline strengthens the source's probability conclusion.**
   Evidence: W1/STATEMENT.md:42-49; PXN/PROOF.md:437-440; NBH/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md:123-128.
   Section 2(C) correctly gives a liminf identity, but the headline says the success probability converges to `1 - limsup P(U)`. Without convergence of P(U), that need not hold. “Any finite-n statement” is also excluded even though (C) is an every-n inequality and (K) a deterministic bound.
   Required change: replace the headline's limit assertion by `P(O ∩ {Ŝ⁺ = S₀}) - (1-P(U_n)) → 0; hence liminf P(O ∩ {Ŝ⁺ = S₀}) = 1-limsup P(U_n)`. State convergence to `1-u` only if `P(U_n) → u`. Replace the finite-n exclusion by “no quantitative finite-n consistency guarantee, in particular at n=200.”

2. **MAJOR — Q1/Q2: specify the exact target and execution convention.**
   Evidence: W1/STATEMENT.md:24-32,40; PXN/PROOF.md:62-71,425-428; NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md:7-10; NBH/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md:32-51,68-78,170-173.
   “g-prior g=n ...” is insufficient to identify the ridge target actually used: the source uses H_S=(n+1)G_S+I and det(H_S)/det(G_S+I), standardized X and y, and IG hyperparameters a₀=b₀=0.01. A classical unregularized g-prior would be a different target. Also, (T) concerns the potential uninterrupted LS0 computation; OP permits actual runs to stop, so unconditional execution/certification of the actual run cannot follow.
   Required change: replace the ellipsis with the exact standardization, feasible space, score/prior formulas (or a precise incorporation of the cited definitions), including ridge and IG parameters. Explicitly define the potential uninterrupted run, say that (T) and its failure probability refer to its deterministic LS0, and retain GUARD/OP-LS0 for transfer to actual strict output. The existing list of operational premises is otherwise faithful by reference; these premises remain assumptions, not discharged implementation claims.

3. **MINOR — Q1: restore omitted source conclusions and define D_n.**
   Evidence: W1/STATEMENT.md:37-44; PXN/PROOF.md:240-244,431-441.
   Apart from findings 1–2 and flagged D1/D2, the family, fixed-parameter quantifiers, SIZE, and principal rates faithfully match the candidate. The draft weakens the source by omitting (S)'s explicit truncated-moment/tail bound, (E)'s eligibility `S° ∈ R₀, Φ(S°)=c`, (C)'s two-sided identity/conditional limit, and (K)'s displayed big-O corollary. It leaves D_n unspecified rather than defining it as the potential-output discovery miss.
   Required change: define `D_n := P(Ō ∩ {S₀ ∉ S̄⁺})`; restore the omitted conclusions or explicitly label them omitted corollaries instead of claiming “without change of content.” Incorporate P3′'s explicit bound by an exact reference. No additional lower bound `p ≥ n^a` should be introduced.

4. **MAJOR — Q3: D1 is correct, but its proposed discharge needs a cutoff and quantifier check.**
   Evidence: W1/STATEMENT.md:61-66; W1/PLAN.md:23-24; PXN/PROOF.md:213-219,405-417; NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md:24-25,31-33; NBH/ID_REGISTRY.md:264,271,276; SOP/04_theory.tex:775-788.
   Locked T03 really requires H-T02; T03♯ has the stated XF-verified replacement hypotheses. T22(i-a),(ii-a) are correctly cited deterministic locked inputs, with no EXP′ or T22(iii) dependency. However, P2(a) controls sets only through the locked cutoff m_n+s₀. Knowing m♯_n=O(log n) does not itself show that its anchored sets lie inside that particular event.
   Required change: in the D1 repair define an X-event controlling all sets through `s₀ + max{m_n,m♯_n,j₀,g,s₀+2}` (or prove the required cutoff containment). Define m♯_n by the exact prior-tail criterion. Prove its O(log n) upper bound, normalized SE_λ, unnormalized SE_w with a fixed g₀>0, energy and BM-∞ on this event. Then verify T03♯ for every deterministic design sequence in it and apply de-randomisation. Cite TH128 / W6-FIXREV2/STATEMENTS.md:19-35,51-60 as the theorem of record, with TH09 its final card. Do not present the random-design extension as already supplied by TH09. No other omitted conjectural mathematical input was identified; [CONC] and Laurent–Massart still need precise citations or derivations in the item reviews.

5. **MAJOR — Q1/Q3: D2 is correct; the explicit recovery bound is not yet an accepted input.**
   Evidence: W1/STATEMENT.md:37,67-70; PXN/PROOF.md:79-96; NBH/ID_REGISTRY.md:311.
   Theorem B's XF-verified exact-tail statement does not validate Corollary B's constants: that corollary is explicitly XF GAP. The draft also uses I* without defining it. A qualitative fallback must preserve (R)'s summability, not just recovery in probability.
   Required change: define t*, I(t;r), and I* exactly as PXN/PROOF.md:82-84; qualify the bound by n≥5 and SIZE at that n. Make the constant conditional pending I4, or lock a weaker recovery clause and identify the strengthening as pending. If replacing the explicit bound, prove a summable bound directly or establish `P(blocks≠groups)≤p^{-C}` eventually for every fixed C>0 **and** an n-summable estimate; with arbitrarily slowly growing p, a single polynomial-in-p bound is insufficient. Any changed (R) must propagate through the statement and final synthesis.

6. **MAJOR — Q4: the plan silently changes FR01's sixth review item.**
   Evidence: W1/PLAN.md:3-5,19-20; SOP/06_open_and_plan.tex:80-82; PXN/REPORT.md:133-144.
   FR01 explicitly includes Lean-readiness among its six checks. The plan substitutes dependency status and claims an HQ brief overrides it, without providing that brief as evidence.
   Required change: restore a short explicit Lean-readiness assessment of the finite deterministic cores and outstanding formalization obligations (not a requirement to formalize the theorem), retaining dependency review as an additional check. Alternatively cite an actual authorized scope amendment and report the deviation. I1–I7 otherwise cover PROOF §§1–10; make final assembly depend on verified D1/D2 repairs and their revised statements rather than treating the repairs as independent of downstream claims.

7. **MAJOR — Q4: N1–N7 are labels, not yet meaningful falsification specifications.**
   Evidence: W1/PLAN.md:9-17,25-26,35; Theory_work/Wave1/PROTOCOL.md:18,23; PXN/PROOF.md:41-53; PXN/REPORT.md:65-108.
   The mapping is sensible, but no sample grids, measured inequalities, tolerances, or failure criteria are supplied except the N4 tail comparison. Full enumeration at p≤10 cannot test this theorem's design: asymptotic SIZE needs g≥9, and B_n≥g requires n,p≥g². Small algebra checks cannot establish partition recovery or the p>n route.
   Required change: specify N1 exact Beta quadrature/tails across j,u>16 and both D values; N2 score-expansion/RSS identities and bounds; N3 Gaussian residual-span/Beta and conditional-independence diagnostics; N4 exact correlation-tail comparisons for both signs and limiting parameter cases; N5 population enumeration of lattice move types plus sample margins; N6 production LS/ledger checks (centre, ties, move cap/final scan, stopped output); N7 exact T22 aggregation/odds and deterministic cutoff/eigenvalue checks. Give inputs, tolerances, and failure criteria for each. Separate p≤10 component enumerations from feasible-SIZE simulations with p>n, using exact block tables/DP rather than full model enumeration and at most 20 seeds. Include c>1, unequal links/signals, and v=0. Label empirical distribution checks as diagnostics, never proofs of Haar laws or asymptotic rates.

8. **MINOR — Q5: arbitrary fixed A is plausible; complete the accounting and strengthen the flagged (L) repair.**
   Evidence: W1/STATEMENT.md:54-57; W1/PLAN.md:27-29; PXN/PROOF.md:162-199,213-219,294-305,357-367,470-473; SOP/04_theory.tex:775-782.
   No reviewed step requires A≤1, p≤n, or a nonsingular full sample Gram. Only bounded-size/O(log n) sub-Grams are inverted; their entrywise error is `O((log n) sqrt(log p/n))=o(1)` for every fixed A. The listed Tr-J exponents and linear-n versus log-n margins are correct. Section 3 omits Lemma E's family exponent/failure bounds, the enlarged T03♯ cutoff, and the error budget in (L).
   Required change: add those entries. In I7 explicitly replace the (L) proof's reliance on E3 by E5 with Λ_{S₀}=0: `RSS_{S₀}/(nσ²)=1+O(n^{-1/3})`. Uniformly `Z_l²=O(log p+log log n)`, the omitted remainder is `O(n^{-1/3}log n+(log n)²/n)=o(1)` for fixed A. Merely writing `1+o(1)` would not justify the displayed additive o(1) after multiplication by log p. Keep all constants/onsets parameter-dependent; this is not a uniform theorem over growing A.

**Q2 overall:** yes, this is the right polynomial-p masked reported-HPM target for FR01 once the changes above are made. LH-iid, SIZE, fixed sparsity, operational idealisations, LS0 as a method change, strict joint-with-output reading, and absence of a delivery claim are the right scope. It is not the study's g=5 design and does not settle superpolynomial p. The earlier TH160 XF GAP and exact-Gram M5 result cannot supply the missing iid proof: SOP/05_history.tex:203; SOP/04_theory.tex:484,521-524,845-848. This is a statement/plan lock review, not verification of the candidate proof or implementation.

---
## Disposition (W1-PXN lead, 2026-11-08)
1. Accepted: headline rewritten in the liminf/difference form; finite-n exclusion reworded (STATEMENT v2 §2).
2. Accepted: exact score/target, method, potential run R̄/R̄⁺, actual run, (OP) as assumptions (STATEMENT v2 §1).
3. Accepted: D_n defined; (S) explicit bound referenced, (E) eligibility, (C) two-sided/conditional limit, (K) big-O restored.
4. Accepted: lemmas/P8_T03sharp.md now uses TH128 as theorem of record, exact m♯ definition, proved O(log n) bound, design
   event over all sets of size L_n = s₀ + max{m_n, m♯_n, j₀, g, s₀+2}; random-design extension stated as this ticket's step.
   [CONC] replaced by the self-proved [CONC′] (lemmas/CR_corr_tails.md).
5. Accepted: I(t;r), q, t*, I* defined; n ≥ 5 and SIZE at n; (R) first-line form (summable, ≤ p^{−C}) separated from the
   pending explicit constant; fallback (R′) written with an n-summable bound.
6. Accepted: Lean-readiness restored as I8; the HQ brief's substitution recorded verbatim in LOG.md.
7. Accepted: numerics specs with failure criteria in PLAN v2; N8 feasible-SIZE p > n simulation added.
8. Accepted: A-accounting completed (STATEMENT v2 §3); (L) repaired via (E5) with an additive remainder bound
   (lemmas/L_strict_localmax.md).
Result: STATEMENT v2 LOCKED.
