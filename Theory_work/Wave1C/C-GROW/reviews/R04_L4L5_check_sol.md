# R04 — adversarial check of L4 and L5

Reviewed the supplied L4/L5 files against STATEMENT, METHOD_REQUIREMENTS, the statements of L1–L3, GEN L5's operational argument, the SoP M5 and TH09 cards, the LS0 specification, and the Wave-1C method-change rule. This is a conditional assembly/instance review, not a re-verification of L1–L3. No source files were edited and no state-changing git commands were used.

**Verdicts: L4 VERIFIED-WITH-AMENDMENTS (1); L5 VERIFIED-WITH-AMENDMENTS (2–7 below).** I found no counterexample to the principal consistency conclusions after these repairs. There are false subsidiary sentences and an inaccurate numerical-evidence citation; these should not survive into the paper.

## L4: line-by-line assembly check

- **Lines 6–8, sources and statuses:** correct. SoP `04_theory.tex:489` records the quoted T38-(0) status. The composition inequality must be read with the correction at lines 477–480: the pointwise miss is `1−π(S₀)` and the probability bound uses its expectation. L4 does so. TH09, lines 765, 775–782 and 788, supports the stated T03♯ status, hypotheses and probability rate. No expectation rate is being inferred from an O_P rate.
- **Lines 9–12, operational closure with MR1:** valid under the named implementation premises, interpreted for the explicitly modified LS0. Fix the data. The prescribed start centre and the integer cap `ℓ_n+|S̃₀|` are then fixed. LS0 uses no uniforms; its scans and scored set are deterministic. On a potential output run, OP-LS0 executes that search, GUARD-W rules out an interrupted LS0, and every scored model joins the all-scored set. Thus a deterministic LS0 that scores S₀ cannot coexist with a potential output omitting S₀. The exact branch scores S₀ directly. This is exactly GEN L5's pathwise argument; independence of the cap from the data is unnecessary. A longer cap can increase interruptions, but those cause no output and cannot invalidate this intersection bound. This does **not** prove delivery. The Wave-1C protocol expressly permits choosing parameters of the unshipped LS0; MR1 is recorded in both required statement/requirements files. OP-LS0 must continue to mean the version with that cap, not the old executable with an unchanged cap.
- **Lines 15–26, e4 and union bound:** valid. e4 supplies the prescribed maximiser. L3 supplies a simultaneous sandwich for **every** maximiser, so no uniqueness or GEN-style majority argument is needed. L4 retains e4 as a premise and does not claim its integration audit is closed. On the three-event intersection the emitted centre belongs to the feasible lattice, and L1.2(ii) applies. MR1 gives `ℓ_n+|S̃₀| ≥ |S̃₀\S₀|`, stronger than the scoring-only threshold of one fewer move. The zero-extra case is covered because the emitted centre itself is scored. Consequently the displayed D_n bound follows without conditioning on output or requiring independence of the events.
- **Lines 27–28, expectation and liminf:** valid. For every ε>0, `E₀[1−π(S₀)] ≤ ε+P₀(1−π(S₀)>ε)`, hence the expectation vanishes. M5(0) yields the vanishing reported-error intersection. Finally the exact identity is `P(𝒪∩{Ŝ⁺=S₀})=1−P(U_n)−P(𝒪∩{Ŝ⁺≠S₀})`. Taking liminf gives the claimed identity even if P(U_n) has no limit.
- **Lines 29–30, production cap:** valid eventually (n>1). Since δ₀∈(0,1), `(1−δ₀)ln n < ln n/ln 2 = log₂ n ≤ ceil(log₂(n+p+1))`. The cap exceeds the number of required moves, not merely the scoring threshold.
- **Lines 32–33:** the exact branch and the nested extra search are used correctly, on the stated premises.
- **Lines 34–36:** the worst-case polynomial bound is valid, but its first event qualification is wrong as written; see amendment 1.

**1. Required L4 amendment — event for the exact move count.** At lines 34–35 replace “On Sand_n LS0 makes … moves” by “On Sand_n ∩ NA(𝓛) ∩ TL(𝓛), LS0 makes … moves.” Sand_n alone says only where the initial centre lies; it says nothing about the scores of subsequent neighbours. The deletion path and its exact move count require NA and TL. The same qualification should accompany any standalone repetition of the exact-count assertion in note (5). This does not affect the theorem proof, which already uses the correct intersection.

## L5(a): population facts and hypothesis checks

- **Lines 8–14:** the exact centred Gram requires p≤n−1 and is realizable under that condition. Fixed nonzero coefficients on fixed-size support give uniform upper energy and a fixed positive beta-min. However, the displayed relevance set is subsequently changed inside the proof; amendment 2 is necessary to make the instance a single well-defined construction.
- **Lines 15–17, negative ρ:** correct. DΣD is the positive-|ρ| Toeplitz covariance. Column sign flips preserve every column span and residual projection, flip each residual direction only by the sign of its target column, and preserve δ², Z², RSS and the ridge score. The shipped partition uses `1−|r̂|` with deterministic index-based tie rules (SoP `02_method.tex:187–192`), so it is invariant too. Direction cardinality is preserved: for each l the family is merely multiplied by the fixed sign D_ll. It would be incorrect to assert P4's nonnegative covariance statement directly for negative ρ; the proof correctly reduces first.
- **P1, lines 20–22:** correct. The Fourier quadratic-form representation bounds every Toeplitz Rayleigh quotient by `(1−ρ)/(1+ρ)` and its reciprocal; interlacing supplies the same bounds for arbitrary principal submatrices. These bounds are uniform in p and apply to all anchored sets, not only contiguous ones.
- **P2, lines 23–24:** correct. In the path graph, the nearest observed coordinate on each side separates l from all other observations. Gaussian conditioning makes its conditional mean a linear combination of those one or two endpoints; with neither present it is zero.
- **P3, lines 25–26:** the lower bound is correct, as is the displayed precision description for p≥2. For p=1 the precision is [1], a harmless but literal exception to the described endpoint formula; amendment 4 records it. Conditional variance decreases under additional conditioning for this Gaussian vector, and the precision formula proves the stated uniform lower bound.
- **P4, lines 27–35:** correct for positive ρ. If T separates j and k, the corresponding components of the conditional precision graph are disconnected. Otherwise only the closest exterior endpoints matter. The bridge algebra is correct. For two endpoints, write A=`ρ^{2(j−a)}`, B=`ρ^{2(b−k)}`, C=`ρ^{2(k−a)}`; the ratio multiplying `ρ^{k−j}` is `(1−A)(1−B)/(1−BC)`. Since C≤A, its numerator is ≤ its denominator: their difference is `A+B−AB−BC = A(1−B)+B(1−C) ≥ 0`. Thus the bridge factor lies in [0,1]. With only a, the factor is `1−ρ^{2(j−a)}`; with only b, it is `1−ρ^{2(b−k)}`; with neither, it is 1. The absent-a notation should explicitly set the denominator's `ρ^{2(b−a)}` to zero as well, or simply state these cases.
- **P5, lines 36–39:** the identities are correct Schur-complement identities from `XᵀX=(n−1)Σ`, including the projection coefficients. They concern the unscaled signal μ=Xθ*, as required by STATEMENT; they do not mistakenly substitute the standardized noisy response into the population covariance. The shared symbol x denotes a Gaussian scalar coordinate on the covariance side and a deterministic column on the sample side; separating these symbols would improve readability but is not a mathematical gap.
- **H0, lines 43–45:** correct. The full uniform eigenvalue floor gives both SE_λ(j₀) and SE_w(m♯_n;1), regardless of the potentially large tail cutoff. Specifically `(n−1)φ₀²≥1` eventually for every subset, so no unproved estimate of m♯_n is needed. Fixed θ*_min>0 gives BM-∞, and the spectral upper bound gives R. The support is feasible eventually.
- **G1, lines 46–49:** the repair by enlarging Q works, but it must be made part of the definition; see amendment 2. The missing floor(n/2) condition is automatic eventually since the threshold is O(log n). In the enlarged case p=O(log n), so p≤floor(n/2) eventually and K=p. These observations remain valid for sequences that alternate between the two cases.
- **G2/G3a, line 50:** correct by P1.
- **TV, lines 51–54:** correct uniformly over arbitrary U excluding j. P3 bounds the own-signal term below, P4 and separation bound the possible cancellation by other truths above, and Var≤1 gives the stated positive lower bound for δ². Hence the stated M_n diverges.
- **NEG, lines 55–58:** correct. Truths already in U contribute zero; the remaining covariances obey P4. Outside the original radius all distances exceed d_n, yielding an O(1) noncentrality bound. This is eventually ≤ησ² log n for fixed positive η=η_A/2. Enlargement only removes indices from the NEG obligation.
- **G4-dir, lines 59–61:** correct after the definition repair. Given l and the closest a,b∈Q on either side, Gaussian regression coefficients depend only on the corresponding distances, not on other members of T. P5 transfers that identity exactly to the sample columns. Normalization is legitimate by the Gram floor. At most `p(|Q|+1)²` distinct directions occur, so `log N_n=O(log log n)=o(log n)`, also in the enlarged case.

**2. Required L5 amendment — define the relevance set piecewise and fix its bound.** Call the radius set P⁰_n and put Q⁰_n=S₀∪P⁰_n. Use it when Q⁰_n=[p] or `p≥2|Q⁰_n|+32s₀+1`; otherwise set P_n=[p]\S₀ and Q_n=[p]. An alternative using the proof's larger deterministic sufficient threshold is also valid, but choose and state one. After enlargement only the original set satisfies `|P⁰_n|≤2s₀d_n`; a valid uniform final bound is `|Q_n|≤4s₀d_n+34s₀+1=O(log n)`. The sharp original bound cannot be retained for P_n. Counterexample: s₀=1, p_n=4d_n+34, truth at 2d_n+17. For large n, |Q⁰_n|=2d_n+1, the required threshold is 4d_n+35, and enlargement gives |P_n|=4d_n+33>2d_n. This sequence satisfies p_n≤n−1 and the separation condition. Correct the corresponding post-enlargement bound in STATEMENT (C5)(a) too. Without an explicit enlargement the originally defined set does not establish G1 on this example.

**3. Required L5 amendment — remove the false AR(1) scope explanation.** Lines 63–65 assert unconditional logarithmic growth and say boundary proxies are neither VIS-strong nor NL-negligible. Fixed p is expressly allowed, so logarithmic growth needs a qualification such as the one already in STATEMENT. More seriously, a proxy at distance d_n has the same O(1) leakage bound proved for NEG (replace d_n+1 by d_n), uniformly in U excluding it. Its noncentrality divided by log n tends to zero: it is negligible in that sense. At intermediate distances the noncentrality may instead be comparable to log n. A growing collection of stronger interior proxies can obstruct GEN's bounded relevance-set assumptions, but the asserted explanation about the current radius boundary is false. The proof does not establish a nondegenerate “random subset” law either; retain only the proved sandwich statement.

**4. Minor L5 amendment — degenerate and one-sided cases.** At P3 add “for p≥2; for p=1, Var=1 and the bound is immediate.” At P4 explicitly give the three absent-endpoint formulas above. These repairs keep every claimed inequality intact.

## L5(b): S5 instance and evidence

- **Lines 69–71:** the covariance decomposition is correct; the coefficient layout is the diagnostic p=100 layout, not the production generator's declared truth. STATEMENT already makes that distinction, but this file calls it “the study's truth indices”; amendment 5 requests the same honest label here. The referenced GEN helper gives zero-based support (2,26,53,75).
- **Lines 72–80:** the conditional statement “TV iff τ₀>0” is correct. There are finitely many conditioning sets and their population quantities are n-independent. If τ₀=0, one δ² is identically zero; if τ₀>0, `(n−1)τ₀/log n→∞`. The eigenvalue floor 0.3 follows directly from the PSD decomposition. H0 follows as in (a), with a fixed upper spectral bound because p=100; |Q|≤K requires n≥200, which is included in “n large.” B=10 for n≥100, and exact Gram makes the partition n-independent under exact arithmetic and the stated deterministic ties. The fixed 96 nulls satisfy G4-χ only beyond `exp(96/(1−δ₀))`. This is astronomically large and explicitly disclosed. This threshold is a sufficient onset for that hypothesis, not an onset guarantee for all other high-probability events.
- **Lines 82–85:** the asymptotic warning is appropriate, but the last sentence makes an unsupported inference about practical NA; see amendment 7.

**5. Required L5 amendment — label the S5 truth layout.** Replace “the study's truth indices” by “the diagnostic p=100 truth layout used in the numerical port,” and give the support or the same production-layout caveat as STATEMENT (C5)(b). This prevents a claim about an unproved production-generator instance.

**6. Required L5 amendment — replace the dangling F2 evidence citation.** At inspection, `numerics/f2_run.py` existed, but there was no `f2_results.pkl` or report containing the claimed τ₀; the subsequently visible `f2_log.txt` was empty. Thus “τ₀ reported there” at line 74 was not supported by the named output. The runner alone is not a completed numerical check. I independently checked the finite quantity, so there is no remaining mathematical TV gap for this diagnostic design: **τ₀=1/25 for c=0.5 and τ₀=4/25 for c=1**. Cite this review for that independent check, or provide an actual script/output pair before claiming F2 has reported it.

The partition used in this independent check was the consecutive zero-based blocks `{10b,…,10b+9}`, b=0,…,9, obtained by the numerical port's `partition_from_corr(Σ,10)`. This partition also follows from the specified exact lexicographic complete-linkage rule: each five-element group forms first; tied between-group merges produce the increasing-index chain, the size cut retains its first two groups together and subsequent groups separately, and next-fit packs the latter in adjacent pairs. Every truth block contains one truth, four other coordinates in its group, and five coordinates in the paired group. Consequently its 512 conditioning sets reduce exactly to 30 cases (a,b), 0≤a≤4, 0≤b≤5, according to counts from those two groups.

Here is the complete exact-arithmetic reduction; it uses rational input and checks all 120 distinct truth/count cases, rather than treating a floating-point positive margin as proof:

```python
from fractions import Fraction as F
R, C = F(7,10), F(3,10)
mins = []
for t in (F(7,5), F(-1), F(9,5), F(-6,5)):
    vals = []
    for a in range(5):
        for b in range(6):
            if a and b:
                A, B = 1+(a-1)*R, 1+(b-1)*R
                det = A*B-a*b*C*C
                g, d = (R*B-b*C*C)/det, (A*C-a*C*R)/det
            elif a:
                g, d = R/(1+(a-1)*R), F(0)
            elif b:
                g, d = F(0), C/(1+(b-1)*R)
            else:
                g = d = F(0)
            h = R*t+C-a*g*(F(2,5)*t+C)-b*d*C
            v = 1-a*g*R-b*d*C
            vals.append(h*h/v)
    mins.append(min(vals))
print(mins)
print(min(mins), min(mins)/4)
```

Here g,d are the constant coefficients in the regression of x_j on the a within-group and b paired-group conditioning variables. The total coefficient sum is 1 at c=1. Thus the unconditioned covariance at j is `0.7t+0.3`; at a within-group null it is `0.4t+0.3`, and at a paired-group null it is 0.3. These facts give h and v in the code. Output:

```text
[2028/2945, 4/25, 3267/2945, 729/2500]
4/25 1/25
```

The minimum is attained at zero-based truth j=26 with U empty. Independent direct floating-point enumeration of all 2048 (j,U) cases for each c agreed: 0.16000000000000003 and 0.04000000000000001. These computations were run inline with Python 3.13; this review is their retained code/output record, respecting the requested single-file write restriction.

**7. Required L5 amendment — qualify the practical-NA conclusion.** Uncapped LS0 reaching S₀ in 80/80 runs does not establish NA on the entire lattice of 2^96 sets. The F2 runner's lattice routine samples that lattice when |P|>12 (`f_common.py:139–172`). At most, those observations show that the cap was a binding obstruction for those LS0 runs. Replace “the binding constraint … is … not NA” by a statement limited to the observed paths. This is consistent with the conservative sufficient condition for NA being astronomically delayed. Neither empirical success nor a sufficient-condition threshold identifies the true onset of NA.

## Additional falsification numerics

Using NumPy, seed 20261108, p=18, and 300 random conditioning sets/pairs for each ρ∈{0.5,−0.5,0.8}, I compared the exact bridge/one-sided expression with the conditional covariance Schur complement (after D-sign transformation for negative ρ). Across 900 cases:

```text
maximum absolute bridge error: 2.220446049250313e-16
minimum conditional covariance: -1.6653345369377348e-16
maximum excess over |rho|^|j-k|: 0.0
```

The tiny negative value is rounding at conditional covariance zero. This supports, but does not replace, the analytic P4 check above. No numerical counterexample to P1–P5 was found.

**Final verdict per lemma:**

- **L4: VERIFIED-WITH-AMENDMENTS — amendment 1.** The assembly, data-dependent-cap operational closure, e4 use, cap arithmetic, expectation limit and liminf identity are valid under the named inputs and implementation premises.
- **L5: VERIFIED-WITH-AMENDMENTS — amendments 2–7.** The core AR(1) inequalities and hypothesis verification survive the explicit piecewise relevance-set repair. The S5 TV reduction is valid and its missing positive-margin evidence is supplied above. The false growth/boundary commentary, post-enlargement cardinality bound, production-truth label and practical-NA inference require correction.
