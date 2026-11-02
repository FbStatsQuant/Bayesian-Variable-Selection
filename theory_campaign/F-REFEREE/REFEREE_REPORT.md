# F-REFEREE — Referee report on the theory section of the SMC-BVS paper (JRSS-B Series B standard)

Referee: F-REFEREE (Fable 5.1), 2026-11-02, branch `theory/F-REFEREE`. Role: a hostile but fair Series B referee.
Companion file: `RESPONSE_PLAN.md` (the authors' best honest response, the one tier-raising change, and ranked task specs).

**Object reviewed (the theory "as it stands tonight").** The drafted theory section `theory/S-PAPER:theory_section.tex`
(744 lines, Theorems 1–6, Propositions 1–2, the n = 200 disclosure); the architecture and confidence cards
`theory/F-REFINE` (ARCHITECTURE.md, CARDS.md); the assembled main theorem `theory/W4-T38FULL` and its corrected version
`theory/W6-FIXREV1` (T38_STATEMENT.md, T38_PROOF.md, CONSOLIDATED.md); the story `Docs/THEORY_PRIORITIES.md`; the
cross-family reviews `theory/A-REV1`, `theory/A-REV2`; the novelty audit `theory/A-DRAFT` §1; the empirical headline
`Results/SMC_BVS_v3_production/HEADLINE_TABLES.md`. I also looked at the headlines of the in-flight branches
(O-BGIBBS, W5-B2ENV, O-MIX, F-MASKPIP, W5-FAVIID, O-CERT, O-SWAP, W5-VMASK) only to judge what a response could
honestly promise; none of them is part of the reviewed paper.

**How to read this.** I write as the referee would, in the second person to the authors. Each major point gives (i) the
exact statement attacked, (ii) why it fails or underwhelms, (iii) the evidence the referee would demand, (iv) the
strongest honest rebuttal, and (v) the fix. Status words are the campaign's and are never upgraded. Where I cite
external literature I say what I am confident of and what should be checked against the source before it is quoted.

---

## 0. Summary verdict

**Recommendation: major revision.** The theory section is unusually candid, internally consistent, and the
composition inequality (Theorem 4) is exactly the right organising principle. But in its present form the section
does not support the paper's empirical claims, and its headline theorem (Theorem 5(b1)) is about an algorithm
(v3 + LS0) that the reported simulations did not run. Three structural problems decide the tier:

1. **Every statistical theorem is asymptotic with proof thresholds at n ≈ 2·10⁶, while the simulations are at
   n = 200 with s₀ = 14, in a start regime (dilution) that no theorem describes.** The section says so itself, at
   length (§6). A referee will not punish the honesty; a referee will ask what the theorems are *for*.
2. **The masked regime, which is the paper's reason to exist, is proved only with a method change (LS0), and the
   routes for the method that was evaluated are hypotheses-as-conclusions** ((b1′), (b2): conditional on DELIV, REP,
   NB′, all OPEN on every family at the time of writing).
3. **The theory is not positioned against the rapid-mixing literature for Bayesian variable selection** (Yang,
   Wainwright & Jordan 2016, AoS; Zhou, Yang, Vats & Roberts 2022, JRSS-B), which proves *more* (polynomial mixing to the
   full posterior, hence HPM, PIPs and everything) under hypotheses of the same kind (sparse eigenvalues plus beta-min),
   for simpler algorithms, with no method tweak. A Series B referee will raise this in the first paragraph. The novelty
   audit on `theory/A-DRAFT` does not mention these papers.

What survives and is publishable now: Theorem 4 (exact composition, every n, matched by the data: all 565 misses are
posterior misses), Theorem 1 as a target-specific consistency result with an exact size tail, Proposition 2 (frozen-run
identities, with the correct islandwise wording), Theorem 3's exact deterministic part (Theorem A, Lemma LS-score),
and the two negative results (literal truth dominance is unsatisfiable; bridge mass does not imply delivery, C1).

**The one change that most raises the tier** (details in `RESPONSE_PLAN.md` §2): state and prove the masked-regime
half of the main theorem **for the algorithm that produced the tables**, on the explicit family LH, and show the
predicted transition numerically with the production code at growing n. Three candidate routes already exist on
in-flight branches (O-BGIBBS pilot-stage discovery, W5-B2ENV route (b2) under STAB-LH, O-MIX mixture start); one of
them cross-family verified turns Theorem 5(b) from "a theorem about v3 + LS0" into "a theorem about v3", and the
growing-n simulation turns "asymptotic with thresholds at 10⁶" into "the mechanism is visible from n ≈ 10³–10⁴".

---

## 1. Major points

### M1. All theory is asymptotic, the thresholds are at n ≈ 2·10⁶, and the simulations are at n = 200

**Statement attacked.** Theorem 1 (T03♯), Theorem 2(iii), Theorem 3(W), Theorem 5, Theorem 6, and the sentence in §3
"The paper proves that the two terms vanish".

**Why it underwhelms.** Section 6 of the draft concedes, item by item: (a) the deterministic steps of Theorem 1's proof
hold only from n ≈ 2.1·10⁶ (binding condition q_n ≤ ½); (b) the beta-min constant exceeds the executed signal by ≥ 43×
and the O_P constants are unspecified; (c) the start rates carry 2^B and are vacuous below n ≈ 10⁹; (d) the start at
n = 200 is dilution-masked (6–12 of 14 truths missing from the start mode at every signal scale), a mechanism that
appears in no theorem; (e) the HPM at n = 200 is found by Gibbs flips, a route with no completed theorem. Taken
together, the section proves properties of a limit the study never approaches, for a regime (fixed s₀, cancellation
masking on LH with g ≤ B < 2g) that the study's designs (groups of 5, B = 14, s₀ = 14 ≈ √n) do not realise. The referee's
sentence will be: "The theorems explain a mechanism; the simulations exhibit a different mechanism; the paper does not
connect them."

A sharper sub-point on Theorem 1: the restated SE_w ranges over ≤ 114 columns at n = 200 only because the cap K = 100
binds, which the draft admits; the greedy-adversarial probes give λ_min(G) ≤ 0.22 in S4 and the feasibility of any
fixed g₀ is unverified. So the paper's own explanation of its misses ("posterior misses, the 2E₀δ₁ term") is not
covered by Theorem 1 at the study size: the posterior term is observed to dominate, but nothing proved says it is small.

**Evidence demanded.** (i) A simulation on the family the theorems are proved for (LH, exact Gram and iid rows), with
the production code, at n ∈ {400, 1600, 6400, 25600} and c ∈ {1, 2, 3}, reporting start-mode misses, stage at which S₀
is first scored, and P(Ŝ = S₀), so that the predicted transitions (π₀(S₀) = p^{−c}n^{−c/2}, start mass at S° → 1,
D_n → 0) are visible. (ii) For Theorem 1, the explicit constant c₀(s₀, A) and a table of the smallest n at which each
deterministic step holds for the study's (p, s₀). (iii) A one-paragraph statement of what, if anything, is claimed at
n = 200, placed *before* the theorems rather than after them.

**Strongest honest rebuttal.** (a) Theorem 4 is exact at every n and is confirmed by the data: 0 discovery misses, all
565 wrong HPMs are posterior misses, so the decomposition is not decorative. (b) Asymptotic selection consistency with
unverifiable constants is the norm in this literature (Narisetty & He 2014; Castillo, Schmidt & van der Vaart 2015); a
Series B paper is not rejected for that. (c) The exact finite-n statements (Theorem A, Lemma LS-score, Proposition 2,
the T02 size tail which is non-asymptotic) are genuinely finite-n and are stated as such. (d) The disclosure is a
strength: few BVS papers compute their proof thresholds.

**Fix.** Keep the theorems; add the LH growing-n experiment (RESPONSE_PLAN task R2); give Theorem 1 an explicit
constant (task R9); rewrite §3 "The story" so that the sentence "the paper proves the two terms vanish" is followed by
"in the regime R1 of §1.2; at the study's size the first term is observed, not proved, to carry the error". Move the
n = 200 disclosure to a short remark after Theorem 4 and a short paragraph in the simulation section; the present §6
(9 items, 2 pages) reads as a list of reasons to reject.

### M2. The main theorem requires a method tweak (LS0) that the reported simulations did not run

**Statement attacked.** Definition 2 (LS0) and Theorem 5(b1), (b1-LH): "With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no
statistical input left open." Also the sentence in Theorem 5's hypotheses "LS0 is part of the method".

**Why it fails.** The 2,400 fits in HEADLINE_TABLES were produced without LS0. So the headline theorem is about
algorithm A′ and the tables are about algorithm A. The draft's own §6 item 6 says LS0 "does not change the picture at
n = 200" (113/128 scored S₀ when |S̃₀ Δ S₀| ≤ ℓ + 1, 13/32 beyond; cannot fix posterior misses). The referee will read
this as: the tweak exists to make a theorem provable, not to make the method better, and the paper cannot show that A′
performs as A because the pilot (O-LS0) had not reported when the draft was written. Under the paper's own "investment
rule" that is an unmet gate.

A second, subtler objection: LS0 is centred at the *exact* start mode S̃₀ = argmax π₀ and the theorem needs
P₀(π₀(S°) > ½) → 1 (M1) so that S̃₀ = S°. That is a favourable-start condition *at the reference*; (b1) is therefore
"favourable at S°, then c deterministic greedy moves". The referee will say the masked regime of (b1) is the favourable
regime in disguise, one lattice away. That is fair as a description, and the paper should say it.

**Evidence demanded.** (i) LS0 run post hoc on all 2,400 datasets with every changed reported HPM listed (correct→wrong,
wrong→correct, wrong→wrong) and the added compute; (ii) or, preferably, a masked-regime theorem for A itself.

**Strongest honest rebuttal.** LS0 is deterministic, data-only, adds at most 1 + (ℓ+1)max_k[p + k(p−k)] scores, and under
the HPM rule it can change a *correct* report only by exhibiting a model that the true posterior prefers to S₀, i.e.
only by revealing a posterior miss that was already present; it can never create a discovery miss. Post hoc execution is
exactly equivalent to running it in the fit (the ledger is a union). So the tables with LS0 are the tables without LS0
plus a non-negative number of corrections toward the true HPM, and reporting both costs nothing.

**Fix.** Two options, and the referee will accept either but prefers the first. (1) Prove (b) for the unmodified method
on LH: three candidates exist tonight — O-BGIBBS Theorem BG1 (the pilot's first stage scores S₀ for every fixed c ≥ 1;
structure PROVED, score estimates PROOF SKETCH; needs n ≳ 10⁴ at T₀ = 1000), W5-B2ENV Theorem B2-LH (route (b2) for every
c ≥ 1 under the checkable population inequality STAB-LH, which fails at (ρ, ψ) = (0.85, 0.5)), and W5-B2ENV Corollary
D2-LH (NB′ PROVED on LH, c = 1, so (b1′) holds when p/√n → ∞). Cross-family verification of one of them makes (b1) a
remark ("LS0 removes the pilot-stage temperature condition") instead of the headline. (2) If LS0 stays, present the
method as v3 + LS0 from the start, rerun or post hoc-complete all 2,400 fits with LS0, and report the diff; never write
"no method change needed".

### M3. The masked regime without LS0 rests on unproved particle-level hypotheses, and the paper's own mechanism at n = 200 has no theorem

**Statement attacked.** Remark "Conditional routes" ((b1′), (b2)), Theorem 5's "Not claimed: masked-regime consistency
without LS0 on any explicit family (OPEN)", Theorem 4 route (e′), and §6 item 5 "the HPM at this size is found by Gibbs
flips, a route with no completed theorem".

**Why it fails.** The draft reports that 98% of fresh scores at n = 200 come from Gibbs flips and the final local search
repaired 0 fits; i.e. the method works through route (b2). Route (b2) is stated with DELIV(𝔛_n) (delivery of an eligible
particle to the terminal boundary) and REP(𝔛_n) (repair in L + 5 rounds), both OPEN, and the draft's own counterexample
C1 shows that start mass ≈ 1 on a region plus bridge mass ≥ 0.9997 plus zero exits still lets every eligible particle
die in 56–100% of islands. So the paper proves that the natural sufficient condition is *not* sufficient and offers no
other. The single-particle Gibbs-path bound β_H is vacuous at n = 200 (Hη ≈ 4–16, v > H possible). A referee will say:
"the theorem for the route that the method actually uses is a hypothesis with a name".

Also: A-REV1 classified the whole supplied T38(b)-R statement as GAP; W6-FIXREV1 repaired it to "PROVED as a conditional
theorem", which is a statement of the form "if the discovery term vanishes then the error vanishes" plus three named
sufficient conditions, two of them unverified on any family. The paper must not call that a consistency theorem for the
masked regime.

**Evidence demanded.** One explicit family on which DELIV and REP (or any replacement) are proved for the unmodified
method, or the honest statement that the masked regime is proved only with LS0 and that the n = 200 mechanism is
observed, not proved.

**Strongest honest rebuttal.** The campaign has, tonight, three candidate no-tweak instances on LH (see M2 Fix): the
pilot-stage theorem BG1 avoids delivery altogether (everything happens in one round, so extinction never enters);
B2-LH proves confinement (Prop. CONF) and one-round scoring at φ = 1 under STAB-LH; D2-LH closes (b1′) at c = 1. None is
reviewed; one of them verified answers M3 for LH. For the study's designs (dilution, s₀ = 14) nothing will be proved at
n = 200, and the paper should say that the n = 200 behaviour is evidence for the route, not for a theorem.

**Fix.** Promote one verified no-tweak instance into Theorem 5(b); move (b1′)/(b2) as general conditional routes to the
supplement; keep C1 in the main text as the reason the envelope route needs a confinement argument; delete "a route with
no completed theorem" once BG1 or B2-LH is in.

### M4. The favourable regime is where the sampler is unnecessary; what does the bridge provably buy?

**Statement attacked.** Theorem 5(a), Theorem 6, and the story's first bullet ("the start already finds the truth, so
the final run's iid π₀ draws score S₀").

**Why it underwhelms.** Theorem 5(a) is T11(iii): Q_f iid draws from a start that puts mass → 1 on S₀ score S₀. No
bridge, no Gibbs, no islands, no tempering enters the proof. Theorem 6 (evidence and PIP consistency) is stated only in
this regime and needs (T_n + 1)Δ_n → 0 with Δ_n = max{1 − π₀(S₀), 1 − π(S₀)}, i.e. the start and the target already
agree on S₀; then the bridge is a short walk between two distributions that both sit on S₀. The referee: "every theorem
in which the SMC machinery is provably useful is conditional; every unconditional theorem is one in which it is
unnecessary". And the data agree: 1 of 2,394 fits is favourable at n = 200.

**Evidence demanded.** A separation statement: on an explicit masked family, (i) iid draws from π₀ followed by local
search fail with any polynomial budget, (ii) one-shot importance correction π/π₀ fails (χ² → ∞), (iii) the bridge
succeeds with a polynomial budget. And at least one statement about Ẑ or PIPs that holds in the masked regime.

**Strongest honest rebuttal.** (i)–(iii) is exactly the W7-SEP task now running (start-only methods fail for c ≥ 2
by the n^{−c/2} law; importance weights have χ² → ∞ by F-DRAFT Theorem W; v3 succeeds by (b1)/BG1). For evidence and
PIPs in the masked regime, F-MASKPIP Proposition M1 (candidate PROVED) gives an evidence-weighted PIP accuracy bound
E[(Ẑ_r/Z)·max_j|PIP̂_rj − 1{j∈S₀}|] ≤ δ₁ + ρ̄ + u_π with no premise on the start: PIPs can be wrong only on islands
whose evidence is a gross underestimate. That is a genuinely masked-regime statement about the reported quantities, and
it is the kind of thing a referee will like.

**Fix.** Add the Separation Theorem (W7-SEP) as the conceptual spine, in the main text, with explicit budget exponents;
add Prop. M1 next to Theorem 6; rewrite Theorem 5(a) as a corollary ("the bridge is harmless when unnecessary"), not a
regime of equal standing.

### M5. The 2^B factor, the vacuous rates, and Theorem 6's budgets

**Statement attacked.** Theorem 2(iii) (rates O_P(2^B √log n n^{−κ}), O_P(2^B n^{−1/2})), Theorem 2(v)(a), Remark
"Discipline", Theorem 6 Remark (deterministic-budget form vacuous below n ~ 10⁸), and the (P1) premise "with the realised
T_n".

**Why it fails.** 2^B at B = 14 is 16,384; the draft computes 2^B√(log n/n) = 2.7·10³ at n = 200, 497 at n = 10⁴, 61 at
n = 10⁶. A rate that first drops below 1 at n ≈ 10⁹ is not a rate a referee will let into a main theorem without
comment. For Theorem 6 the premise (P1) is stated in terms of the *realised* number of stages T_n, which is an output of
the algorithm's own calibration on the same data; a hypothesis on the algorithm's output is circular unless a family is
exhibited on which it holds, and the only such family (ORTH) is a PROOF SKETCH with the deterministic budget T^max =
4,000 giving (T^max + 1)Δ_n ≥ 44 at n = 163,840.

**Evidence demanded.** A 2^B-free start rate on a named family with the actual partition (the paper's own W3-PXN claims
O_P(√(log n/n)) without 2^B for iid rows, unverified; W5-FAVIID claims the same on block-diagonal iid designs including
S1/S3/S4/S6, unverified). For Theorem 6, a bound on T_n from the calibration rule (bisection on the ESS of the
discrepancy), so that (P1) becomes a theorem on a family rather than an assumption on the run.

**Strongest honest rebuttal.** The 2^B is a union over the block size profile and is an artefact of exact-Gram
analysis; on iid designs the per-block ratios have exact Beta laws independent of y (W3-PXN Lemma B) and the factor
disappears. The realised T_n in the study is 1–2 (exact p = 18 scans give (T + 1)Δ_n ≈ 0.02 at the largest n), so the
realised-budget premise is the right one and is small in practice.

**Fix.** Verify W3-PXN Lemma B / W5-FAVIID cross-family (task R6) and state Theorem 2(iii) with the 2^B-free rate as the
primary clause, the exact-Gram 2^B rate as a remark; prove a T_n bound on ORTH/FAV from the ESS bisection (task R5) and
restate Theorem 6 with it.

### M6. What is genuinely new, and the missing comparison with rapid-mixing results for BVS

**Statement attacked.** The implicit novelty claim of the whole section, and the absence of any comparison with
computational guarantees for BVS samplers.

**Why it fails.** The novelty audit (A-DRAFT §1) positions the work against Schäfer–Chopin 2013, Zanella–Roberts 2019,
Lindsten et al. 2017, Del Moral–Doucet–Jasra 2006, Song–Liang 2015 and Gutierrez–Guhaniyogi 2022, and concludes,
correctly, that the SMC machinery (geometric bridge, ESS bisection, resampling, Rao–Blackwell PIPs, unbiased Ẑ, Markov
lower bound) is standard and that the genuine content must be the start law and a discovery/repair theorem on a family
where the start fails. But the audit does not mention the papers that prove *computational* guarantees for BVS:
- Yang, Wainwright & Jordan (2016), "On the computational complexity of high-dimensional Bayesian variable selection",
  Annals of Statistics 44(6): rapid (polynomial in n, p) mixing of an add/delete/swap Metropolis–Hastings chain on
  sparse models, under sparse-eigenvalue-type conditions, a beta-min condition with a large constant, and a size bound.
- Zhou, Yang, Vats & Roberts (2022), "Dimension-free mixing for high-dimensional Bayesian variable selection", JRSS-B
  84(5): dimension-free mixing of an informed (locally balanced) MH sampler under similar conditions.
- Also relevant: Zanella & Roberts (2019) on tempered Gibbs for BVS (already in the library), and Griffin, Łatuszyński
  & Steel (2021, Biometrika) on adaptive MCMC for BVS.
(Check exact titles, volumes and conditions against the sources before quoting; I am confident of the papers and their
thrust, not of every page number.)

These results conclude *mixing to the posterior*, hence HPM, PIPs, and any posterior functional, from any sparse start,
for a simpler algorithm, under hypotheses of the same family as T03's (SE + beta-min). Theorem 5 concludes only that
S₀ is scored, with a method tweak, on a family (LH) that, as far as I can see, satisfies the eigenvalue and beta-min
conditions of those papers (fixed nonzero coefficients, λ_min(R_{S₀∪J}) ≥ φ₀²); so an informed MH from the empty model
would also find S₀ on LH in polynomial time, without any block start. The referee's question is then unavoidable: what
does the theory section establish that the mixing-time literature does not already imply for a simpler method?

**Evidence demanded.** A paragraph, with a precise statement, of what T38 adds: (i) a finite budget *indexed by n*
with an explicit polynomial score count (T38(c)), versus mixing bounds with unspecified constants, if that is true;
(ii) the evidence Ẑ with an unbiased estimator and a certified lower bound, which MCMC does not provide; (iii) an
analysis of an exact start that is masked, showing that the sampler's success does not come from the start; (iv) a
regime (if any) where the mixing results' conditions fail and T38's hold. And a check whether LH satisfies the
conditions of Yang–Wainwright–Jordan / Zhou et al.; if it does, say so.

**Strongest honest rebuttal.** The paper's contribution on the computational side is not a stronger discovery theorem;
it is (a) the exact composition for the *reported* HPM of a budgeted run (best model ever scored, every n), (b) an
unbiased evidence estimate with islandwise identities and an output-level bound, which no MCMC-mixing result gives, (c)
the explicit start law and the proof that its masking is real and is repaired by the bridge, with a polynomial budget,
and (d) a separation from start-only and one-shot-IS methods (W7-SEP). The correct claim is "a BVS-specific
construction and analysis within established SMC principles" (A-DRAFT's words), and the theory section should say it in
its first paragraph.

**Fix.** Add a "Relation to computational guarantees for BVS" paragraph after the story (task R3), with the LH check.
Drop every phrase that reads as "first consistency theorem for a BVS sampler". Make Ẑ and the composition the stated
contribution; make the discovery theorem the explanation of the method's design.

### M7. The evidence and PIPs mean nothing in the masked regime, and the 95% bound is Markov

**Statement attacked.** Theorem 6 ("favourable regime only"), Proposition 2(d) ("P(Z ≥ 0.05Ẑ) ≥ 0.95"), and the paper's
reporting of Ẑ, PIPs and the bound in every scenario.

**Why it fails.** The method reports Ẑ, PIPs, the MPM and a 95% lower bound on Z in every fit; the theory says the PIPs
and Ẑ are consistent only when 1 − π₀(S₀) → 0, which holds in 1 of 2,394 fits. Δ_n ≈ 1 at n = 200 (§6 item 7), so
Theorem 6 is silent on every reported number. The 95% bound is Markov's inequality on a non-negative unbiased
estimator: it is valid, but a factor-20 lower bound is not an interval, and the draft itself proves (O-CERT, candidate)
that no *upper* bound on Z, hence no lower bound on π(Ŝ), follows from unbiasedness. And Proposition 2(c) says the
reported pooled PIP is biased by −Cov/Z, non-zero in general. A referee will ask why the paper reports quantities its
theory cannot certify outside a regime it admits is empty at the study size.

**Evidence demanded.** A masked-regime statement about the reported Ẑ and PIPs, or an explicit disclaimer in the
simulation section that PIPs and Ẑ are reported as diagnostics with only the unbiasedness/Markov guarantees.

**Strongest honest rebuttal.** F-MASKPIP Proposition M1 (candidate): evidence-weighted PIP accuracy in every regime; its
Corollary M2: an island whose terminal population is off S₀ reports Ẑ_r ≤ √δ₁·Z except with probability 2√δ₁, so the
PIPs can be wrong only where the evidence is grossly low. And Proposition M3 shows no conditional evidence theorem can
exist, which justifies *not* conditioning. A relative-variance bound (PW2) would turn Markov into a two-sided band; it
is in progress (O-PW2) and should not be promised.

**Fix.** Add Prop. M1/M2 as Theorem 6′ (every regime), keep Theorem 6 as the favourable-regime consistency; state in the
simulation section that the 0.05Ẑ bound is a one-sided certificate and that the reported PIP is the pooled, biased one
(or report the islandwise product, which is unbiased).

### M8. Verification status, the cost corollary, and implementation facts as hypotheses

**Statement attacked.** The STATUS comments and §6 items 8(x) and 9: "all verification by the campaign is same-family";
Theorem 5(c) "Conditional on T32(i), which is a CONJECTURE"; Assumptions SR and GUARD ("implementation fact", "needs an
independent code check").

**Why it fails.** (i) A theorem whose clause (c) is conditional on a conjecture cannot be stated as a theorem; (c) must
be a remark or T32(i) must be proved (it is bookkeeping: count the score calls of each stage under the v3 budgets). (ii)
SR ("both Gibbs configurations are scored") and GUARD ("the resource guard is stop-only") are properties of the
algorithm, not assumptions; they must be part of the algorithm's definition in the method section, with the code as the
reference implementation, not hypotheses of a theorem. As written, the theorems are conditional on the correctness of
unaudited code. (iii) The paper's own note that every "VERIFIED" is Claude checking Claude, except two cross-family
reviews that cover only part of the material (Lemma M, LS-score, LH-LAT, Theorem W, W3-PXN, W4-SHARE, W2-T26, W2-BOOK
all unreviewed cross-family), is not something a referee can act on, but an editor can: the proofs must be in a
supplement and must be checkable by a human in finite time. Tonight the supplement is "see branch X, file Y, §Z".

**Evidence demanded.** The supplement with complete proofs; T32(i) proved; SR and GUARD moved into the algorithm
definition (with the P(U) issue of minor point m14 resolved).

**Strongest honest rebuttal.** The campaign protocol is stricter than most papers' internal review: every candidate has
at least one adversarial verifier, two cross-family reviews found real errors (Prop. U, Lemma S attainment, E3(ii),
Lemma U's constant, Lemma 0(b), the 1.2·10⁵ threshold) and all were repaired and re-checked. T32(i) is a deterministic
count. SR and GUARD are two code facts with line references.

**Fix.** Prove T32(i) (W7-SEC is on it); write the supplement; move SR and GUARD into the method; finish the two code
audits (W5-LOCKBOOK) and say "audited" only after they report.

---

## 2. Minor points

m1. **Notation clash: m(S).** §1.1 defines m(S) as the marginal likelihood; §1.5 defines m(S) = |S₀∖S|. Both are used
    in the same theorems (Theorem 3(A2) uses m(S) + e(S); Theorem 1 uses m(S) implicitly through F). Rename the missing
    count (e.g. μ(S) or m₀(S)) or the marginal likelihood.
m2. **Notation clash: D_S.** §1.1 defines D_S = det H_S/det(G_S + I); §1.5 defines D_S as the one-state progress event.
    Rename the event (e.g. 𝒟_S or Prog_S).
m3. **Theorem 2 is never stated as a theorem.** The parts are produced by \stepcounter and a thmpart environment; there is
    no "Theorem 2" with hypotheses. State one theorem with parts (i)–(v) and a single hypothesis block.
m4. **Undefined constants in theorem statements.** Theorem 2(i): q, e "the table constants of the locked T22(i)" are not
    defined in the paper. Theorem 2(iii)(F1): κ is undefined in the text. Theorem W: ε in (H2), B′ and ρ* in (H3), and
    LD♭ are defined only by reference to a branch file. Theorem B′: c_*(x), v(x), η(x) "of the Supplement", ε_del
    undefined. Every statement must be self-contained.
m5. **Hypotheses defined by reference to a file outside the paper.** "VIS, NL_η, NL_avg(κ), EXP′ are those of Section 3
    of the common-definitions file". Define them or drop (F1).
m6. **"Not claimed" lists inside theorem statements** (Theorem 5, Theorem 6) are unusual and read as hedges. Move to
    a remark after each theorem; keep one sentence per item.
m7. **Branch names in the main text.** "W4-T38FULL", "W3-PXN", "A-REV1" appear in theorem text and remarks (Theorem 5
    (b1-LH-iid), Remark Conditional routes, §6). Strip all campaign bookkeeping from the paper; the STATUS comments are
    fine in the source but no verdict word (VERIFIED, GAP, ERROR) may appear in typeset text.
m8. **Theorem 5 includes a clause about an unverified single run** ("a masked p ≫ n instance until the single-run LH-iid
    argument is verified"). A theorem cannot contain a statement about the state of its own verification. Either the
    iid realisation is proved (then state it) or it is not (then omit it).
m9. **s₀ fixed versus s₀ = ⌊√n⌋.** Regime R1 fixes s₀; the simulation generator uses s₀ = ⌊√n⌋ = 14 at n = 200. State
    once, in the simulation section, that the theory's regime is s₀ fixed and the generator's growing rule is not covered.
m10. **K = min(p, ⌊n/2⌋)** (W6 correction S3) must be used consistently; §1.1 has it, Theorem 1's "s₀ ≤ K eventually" is
    fine, but Proposition 1(iii) says "if s₀ ≤ K" and Remark ceiling mentions "min(K, N₊)" without defining N₊.
m11. **Theorem 1(iv) "no beta-min"** is a separate result and should be a corollary; (v) "scale invariance of the
    conclusions" is a one-line remark, not a theorem clause.
m12. **Lemma 0 (what survives)** is a one-sentence inclusion; fold it into Theorem 3 or the supplement. The negative
    Lemma (literal TD unsatisfiable) belongs in the supplement with one sentence in the text ("the naive condition that
    greedy descent always adds a missing truth is contradictory; see S.4").
m13. **EX-A (exact arithmetic)** is declared but the method runs in floating point and VAL-FP has not been measured.
    State the floating-point contract once (Proposition 2(f)) and say it is unmeasured, or measure it.
m14. **P(U) is not a probability in the model.** The no-output event U depends on the "operational element Ξ"
    (allocation, clock, load), on which no law is placed. Theorem 4 then reads P(U or Ŝ ≠ S₀) ≤ P(U) + …, with P(U)
    undefined. Either define U through a deterministic score-count budget (then U ∈ σ(R̄) and, with T32(i) proved and the
    budget set above the ceiling, U = ∅ on the potential run), or state the result conditionally on Ξ and report the
    empirical stop rate as a separate operational fact.
m15. **Theorem 6's premise (P1) is on the realised T_n**, a random output of the calibration (see M5). At minimum say in
    the statement that T_n is the realised stage count and that Remark T26B is the only family on which (P1) is known.
m16. **Theorem 5(0): "liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup P(U)".** Fine, but then say explicitly that recovery with
    probability → 1 additionally requires P(U) → 0, "which this theorem does not provide" (W6 has this sentence; the
    draft does not).
m17. **Proposition 1(iv):** "equal size" follows from equal outer products; say "hence |S| = |S′|" rather than "they then
    have equal size" as if it were an extra conclusion.
m18. **Theorem 2(v)(a) "hence π₀(𝓡_d) → 1 for every d ≥ 0"**: 𝓡_d is defined in §1.5 as 𝓡_{s₀,d}; the implication from
    π₀(S°) → 1 is trivial since S° ∈ 𝓡_0; delete "for every d".
m19. **The |ψ| < ρ cliff and g ≤ B < 2g** are stated in a remark as "part of the theorem and must be stated"; put them in
    the theorem's hypothesis line and delete the remark.
m20. **§6 is too long for a main text** (9 numbered items, two pages). Keep items 1, 2, 3 as one paragraph after
    Theorem 4 and one after Theorem 1; move items 4–9 to the supplement; delete the list 8(i)–(xii) "statements the paper
    must not make" (it is an internal checklist, not paper content).

**Move to the supplement:** Theorem 2(ii) EXP′ (technical lemma; keep one sentence), the literal-TD lemma, Theorem B′
and the remark on its asymptotic premises, Lemma RO, Proposition 2(c)–(d) with the ¾-covariance formula, Theorem 5(c)
until T32(i) is proved, Remark "Conditional routes" unless one route is proved, and §6 items 4–9.

---

## 3. Verdict and the one change that most raises the tier

**Verdict.** Major revision. Not reject: the composition theorem, the exact size tail, the start law with its masking
theorem, the explicit masked family LH, the negative results, and the frozen-run identities are correct, careful and
useful, and the candour of §6 is a model. Not minor: the headline theorem is about an unrun algorithm, the masked regime
for the run algorithm is open, the computational-guarantee literature is unaddressed, and the connection between the
theorems and the tables is absent.

**The one change.** *Make Theorem 5(b) a theorem about the algorithm that produced the tables, on the explicit family LH,
and show its predicted transition with the production code at growing n.* Concretely: cross-family verify one of the
three in-flight no-tweak routes (O-BGIBBS BG1, W5-B2ENV B2-LH under STAB-LH, W5-B2ENV D2-LH for c = 1) and run LH at
n ∈ {400, 1600, 6400, 25600} with c ∈ {1, 2, 3}, reporting start-mode misses, first-scoring stage and P(Ŝ = S₀) with and
without LS0. This single change answers M2 and M3 outright, answers the first half of M1 (the mechanism becomes
visible at n ≈ 10³–10⁴ rather than 10⁶), gives M4 its separation (start-only fails on the same runs), and leaves LS0 as
an optional robustness device. Everything else in this report is wording, positioning (M6), or a supplement.

If only one *theory* task can be run, run the verification of BG1 / B2-LH (RESPONSE_PLAN task R1). If only one *compute*
task can be run, run the LH scaling study (task R2).

---

## 4. What a referee would say about the empirical headline, in one paragraph

The tables are strong where the paper's story says they should be (c = 0.5: SMC-BVS 370/600 and 340/600 against SuSiE
220/205 and SSL 303/255) and weaker where the story says the sampler is unnecessary (c = 1: 559/560 against SuSiE
585/582). The theory section currently explains neither number. The c = 0.5 advantage is a posterior-miss story
(same-size swaps and subsets at S4–S6, Proposition 1's ceiling) plus a discovery story (Gibbs flips) with no theorem; the
c = 1 deficit is the method reporting the HPM of a posterior that, by the paper's own count, prefers a superset in most of
its misses. The paper should say that the comparison with SuSiE/SSL is a comparison of *targets* as much as of
*algorithms*, and that the theorems are about the algorithm reaching its target. O-SWAP (finite-n theory of the
posterior-miss rates) and O-CERT (a posteriori certificates) are the right kind of finite-n content to add if they
survive review; they are candidates tonight.
