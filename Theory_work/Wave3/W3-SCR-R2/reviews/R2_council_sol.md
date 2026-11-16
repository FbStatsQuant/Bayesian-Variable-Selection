# W3-SCR council R2 — sol

Seat: OpenAI sol; fresh independent review. Timestamp obtained with `date -u`: 2026-11-16 08:19:02 UTC.

## 1. Frozen manifest

Before reviewing, I ran the required verifier, with `nice -n 10` and `OMP_NUM_THREADS=1`, from `/home/fb31/BVS-wt/W3-SCR-R2`:

```text
verify: OK MANIFEST 96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93
```

Exit status: 0. This report reviews that manifest. I read the seat brief in full, did not read earlier reviews or dispositions, did not use the optional earlier Sol report, started no subagents, and ran no git command. Writes are confined to this report and `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-SCR-R2-sol/`. Short Python checks used `nice -n 10`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and `-B`; no production experiment was launched.

## 2. Seat task: independent A1 proof-chain walk

All file references below are relative to `Theory_work/Wave3/W3-SCR/` unless a production path is given. I read STATEMENT.md:1–246, all seven lemma files, CODE_CHECK.md:1–83, ASSUMPTION_MAP.md:1–45, PLAN.md:1–41 and REPORT.md:1–167. Binding target checked: `Theory_work/Wave3/PROGRAM.md:58–59`.

### Setting and definitions — OK

**Lines read:** STATEMENT.md:12–75, 158–169, 214–246; L1_score.md:3–18, 73–82.

I checked that the response is the centred Gaussian model divided by its sample SD, that X is deterministic and centred with column norm squared n−1, and that y'y=n−1. The positive ridge λ₀=1/(n+1) makes every G_S+λ₀I invertible even with duplicate or singular columns. From the SVD or the penalised least-squares minimum, R_S is positive definite, R_S²≤R_S≤I, preserves centring, and dominates the orthogonal residual quadratic form. Thus σ²≤σ_S²≤τ_n². The witness is deterministic in the model parameters, and the model families in Γ, Ψ and the noise events are independent of the noise. Since q≤K−1, every truth addition used by screening is feasible.

No inference of an anchored floor from a directional floor is needed: A1's parenthetical “in particular” lists successively stronger sufficient assumptions. The actual implication is SF⇒AF⇒DF, as explicitly stated at STATEMENT.md:243 and proved in B3/B2d.

### Score algebra — OK

**Lines read:** L1_score.md:7–82, especially 35–65; STATEMENT.md:25–29, 51–56.

I re-derived H_S=(n+1)(G_S+λ₀I) and

`q_S(v)=||v||²/(n+1)+n v'R_Sv/(n+1)`.

The Schur complement gives a_λ, the rank-one update `R_{S+t}=R_S−R_Sx_tx_t'R_S/a`, and the quadratic gain `q_S(v)−q_{S+t}(v)=n g_v/(n+1)`. The two determinant increments give `D=(n+1)a/a_1`. Its upper bound n+1 follows from monotonicity of a_λ; its lower bound 1 follows by comparing the two variational minima; a_1≤n also gives D≥(n+1)a/n. The size prior increment is exactly `−log((2p−1−k)/(k+1))`.

Writing `ρ=n g_y/((n+1)(0.02+Q_S))`, I checked 0≤ρ<1 and the sufficient addition threshold. Since Q_S≤n−1, ν>n/2 and n−0.98<n, the likelihood increment is strictly greater than `n g_y/[2(n+1)]`; the prior plus determinant penalty is at most `log(2p−1)+0.5 log(n+1)`. Therefore g_y≥T_n really gives a strict improvement, including at equality. The self-normalised version follows from `−log(1−ρ)>ρ` for ρ>0 and `ρ̄_n(n−1)≤T_n`. I also checked the deletion inequality and the augmented representation used by the bridges and L5.

### Gaussian events — OK

**Lines read:** L2_noise.md:3–57, especially 11–39; L3_screening.md:7–24.

For one fixed witness, `(R_Sx_t)'ε` has variance `σ² x_t'R_S²x_t≤σ²a(t|S)`. The two-sided Gaussian tail with `r_n²=2 log(2N_q)+2x` costs e^(−x)/N_q per model. There is one deterministic witness per model, so no s₀ multiplier is required. E1 therefore fails with probability at most e^(−x).

For E2⁺ I expanded `||μ+Cε||²` and used `2σ||μ||≤sqrt(n−1)τ_n²`: the resulting upper factor is `1+(2+sqrt(2))a_x+2a_x²≤(1+2a_x)²`. Thus τ̂≤τ̄_n with failure at most 2e^(−x). The lower event, cross-term event and sparse-subspace χ² bounds also check: the augmented noise projection is a Gaussian contraction of rank at most k, and summing with log binomial weights gives the stated 2q and geometric-series failure factors.

### Screening and transfer to the output — OK

**Lines read:** L3_screening.md:6–24; STATEMENT.md:28–47, 79–90; CODE_CHECK.md:20–59; production locations below.

For every sparse S missing a truth, reverse triangle inequality on E1 gives `sqrt(g_yc)≥sqrt(Γ_n)−σr_n`. MC makes this positive and greater than `τ̄_n sqrt(T_n)≥τ̂ sqrt(T_n)`. After dividing by τ̂, L1.5 supplies a feasible strictly improving addition. Hence such S cannot be LO, simultaneously for all sparse S. The union event costs at most 3e^(−x).

I checked the two event inclusions in L3:22. They use the reported model's own certificate and the explicitly defined certified archive endpoints, not the provenance of an earlier HPM. The empty-family intersection convention is consistent. Completion, certification and small reported size are intersected events; none is asserted to occur with probability tending to one. EX-A is sufficient to interpret the actual coded strict comparisons as exact comparisons.

### Asymptotic reduction A-inf — OK

**Lines read:** L3_screening.md:26–35; STATEMENT.md:14–21, 87–90.

With x_n=sqrt(log n), x_n→∞, x_n=o(log n), and a_x→0. I checked `N_q≤(p+1)^q` also at q=0, and `q log(p+1)≤q log p+q/p≤q log p+1` because q<p. This gives

`r_n≤sqrt(2q log p)+sqrt(2 log 2+2+2x_n)`.

The last term is o(sqrt(log n)); σ≤τ_n absorbs it into the first denominator term. Likewise T_n=(2 log p+log n)(1+o(1)) uniformly over the allowed sequences. A liminf ratio strictly above one therefore gives MC eventually, with failure 3exp(−sqrt(log n))→0. No polynomial-p, bounded-s₀, fixed-σ, or start assumption is hidden in this reduction.

### Bridges L4.0, B1, B2, B2o, B2d and B3 — OK

**Lines read:** L4_bridges.md:3–68; STATEMENT.md:69–75, 147–156.

In augmented space set `w=(I−P̃_S)X̃_T θ_T` and `||b̃||=c_θ`. I re-derived

`Σ θ_t x_t'R_S μ=||w||²−w'b̃≥||w||(||w||−c_θ)`, with `||w||²≥Δ(S)`.

For sqrt(Δ)≥c_θ the scalar map is monotone and the weighted maximum plus a(t|S)<n yields L4.0. Minimising and replacing ||θ_T||₁ by ||θ*||₁ gives B1. For B2 I used `Δ(S)≥κ(n−1)||θ_T||₂²`, `||θ_T||₁²≤|T|||θ_T||₂²`, and `||θ_T||₂≥sqrt(|T|)θ_min`; all squared brackets are nonnegative under the displayed hypothesis. This yields precisely the stated B2 formula.

For B2o, u=||w||≥2c_θ gives `(u−c_θ)²≥u²/4` and `(u+c_θ)²≤9u²/4`. Dividing by the residual scale and using monotonicity of `u⁴/(A+Bu²)` and `V/(4σ²+9κV)` gives the denominator `4σ²+9κs₀θ_min²`. Both proofs consume only the directional lower bound for Δ, so B2d follows without an eigenvalue assumption on other directions. B3 is the Schur-complement variational lower bound on S∪T, of size at most q+s₀; its superset-floor conclusion is immediate.

### A1's fixed parameters and numerical constant — OK

**Lines read:** L3_screening.md:65–76; STATEMENT.md:158–163.

The bounds ||θ*||₂≤M and ||μ||≤M sqrt(n−1) imply τ_n²≤τ_*²=M²+σ². Since κ,b,M are fixed and b,κ>0, eventually `sqrt(κ(n−1))b≥2M/sqrt(n+1)`, satisfying B2d's bias restriction with room to halve the bracket. Thus

`Γ_n(q_n)≥κ²b²(n−1)²/(4n)≥κ²b²n/16`.

The denominator of A-inf, squared, is at most

`2τ_*²[2(q_n+1)log p+log n]≤4τ_*²c₁n`.

Consequently the squared liminf ratio is at least `κ²b²/(64τ_*²c₁)=200/64=3.125>2`. This proves the claimed conservative ratio at least sqrt(2). For fixed A and p≤n^A, q_n=o(n/log n) makes `(q_n+1)log p+log n=o(n)`, so the stated growth inequality eventually holds.

**Hypothesis audit:** A1 states the directional floor κ>0, θ_min≥b>0, ||θ*||₁≤M, fixed κ,b,M,σ, the legal q_n range and the explicit growth bound. Model G and EX-A are global premises for these results (STATEMENT.md:12–47, 215–216). These are all the hypotheses used by this proof. In particular there is no extra restriction on individual coefficient convergence, s₀, non-true-column collinearity, search start, calibration or seed. The bounded support consequence s₀≤M/b is implied, not an added hypothesis.

### SCR-G imports and the master gap — OK

**Lines read:** STATEMENT.md:103–145; L7_master.md:7–117, especially 97–110.

SCR-G explicitly imports all A1 hypotheses, explicitly repeats fixed κ,b,M,σ and additionally requires `(q_n+1)log p+log n=o(n)`. M4 uses exactly these conditions and the maximising witness. I checked `r_n²=o(n)`, `g⁻_S≥κ²b²n/25`, `Ū_S≤1.01nτ_*²`, and `u_S≥κ²b²/(26τ_*²)` eventually. The directional-floor bound at S=∅ gives κb≤M, justifying u*≤1/26. The uniform penalty B_S=o(n) then gives `δ_S>κ²b²n/[104τ_*²]=c₂n`. The ≤c₂n comparison in SCR-G is therefore strictly below δ_𝓗.

For SCR-M itself, I checked the signed unit-ball witness and residual directions; both counting and Gaussian-width tails; the fact that the smaller of two deterministic thresholds selects one valid tail bound without an extra union cost; the numerator positive part; both denominator bounds and their minimum; and monotonicity of −log(1−u). The extended value +∞ can occur only off the constructed event. Importantly the theorem establishes a lower bound on a score difference and does **not** assert that it is positive without an additional gap condition.

M1 and M2 then follow directly from LO and the ledger maximum. For M5, a move dropping a truth leaves exactly one missing truth in the destination N. Re-adding it gives C in a deletion or C plus the swap-in column in a swap; the latter was also scanned at C and cannot beat the selected best neighbour N. This contradicts δ_N>0. The size restriction ensures that addition is legal even in the swap case. Induction and the returned-best-neighbour rule establish all three SCR-G conclusions, including capped searches. M3's MC/MCo implications and M6's one-dimensional orthogonal-truth example also check.

### Certificate and exact-score interface against production — OK

**Lines read:** CODE_CHECK.md:7–72; `Scripts/SMC_BVS/core/v3_fit.R:70–160`, `v3_run.R:115–215`, `v3_exact.R:1–19`, `v3_preprocess.R:35–68,95–132`; `cpp/v3_engine.h:50–104,370–419`; `cpp/v3_ledger.h:32–113`; `cpp/v3_core.cpp:345–490,521–567`; `cpp/v3_score.h:7–245`.

CC1/CC4: engine:394–406 scans every legal flip and every swap; additions at K are skipped. The scan is recorded complete at 407. Strict best-neighbour improvement and cap handling are at 408–412; only a complete scan with no strict improvement sets the archive certificate at 414.

CC2/CC3: run.R:179 and 193 require equality of the reported HPM with the respective certified returned endpoint. Their OR at 194 is the top-level flag; failure status clears it at 143–148. fit.R's initial false flag and exact-branch propagation agree with this. Exact enumeration recursively visits every subset up to K (core.cpp:537–555), so exact.R:15 certifies a true maximiser under EX-A. Equal-score HPM displacement therefore does not transfer an unrelated endpoint's certificate.

CC5/EX-A: score.h uses a₀=b₀=0.01, ν=a₀+n/2, the stated binomial size prior and H=(n+1)G+I, A=G+I. The determinant and quadratic formulas agree exactly with STATEMENT. The nonnegative Q recomputation is the same quadratic evaluated at β=nH⁻¹z; its objective minimum equals y'y−nz'H⁻¹z. Cholesky/refactor/augmented-QR routes factor the same positive definite matrices in exact arithmetic. Preprocessing gives the stated centring and n−1 norms. No floating-point certificate is claimed or inferred from the heuristic error bound.

CC6: every scan calls emitting eval; fresh scores enter offer_stores and offer_hpm. The final run constructs a fresh ledger/cache together, rescoring inherited models into that ledger. The non-emitting initial centre is its already-offered HPM. A cache entry first created by that call is therefore safe too. Final search and LS0 share the ledger/cache. The HPM consequently dominates every scanned neighbour. Scanned centres, completeness, scores, path and returned neighbour are serialized as claimed.

I independently compared the eight requested production files with numerics/core_copy. They are identical after LF/CRLF normalisation. All eight recorded source hashes match an LF or CRLF serialization of the current text; two production/copy pairs differ only by newline encoding. This is no algorithmic drift and creates no faithfulness defect in CC.

### Remaining claims — independent derivations

**SCR-Ao and Ao-inf:** L3_screening.md:37–63. Expanding y_c'R_Sy_c, bounding the cross term by `2σm_S r_n≤σ_S² sqrt(n−1)r_n`, and retaining the 1.02τ̄_n² term yields precisely ϑo. The normalised witness gain exceeds the self-normalised addition threshold. Under q log p=o(n) and ||μ||=o(nσ), all four contributions to ϑo tend to zero, giving Ao-inf.

**A1o:** L3_screening.md:78–86. The ||θ*||₂ bound is exactly the bias condition `sqrt(κ(n−1))θ_min≥2c_θ`. B2o/B2d gives Ψ≥8𝐋_n using both the beta-min bound and s₀𝐋_n≤κn/576. The squared Ao-inf denominator is at most 4𝐋_n; the separate ||μ||=o(nσ) assumption completes the reduction. The beta-min bound alone is not the theorem.

**L5.1/L5.2:** L5_exact.md:7–79 and STATEMENT.md:177–192. I checked conditional lengths via diagonal inverse Gram entries and the dual-direction correlation matrix. The determinant lower bound plus the non-improving deletion inequality imposes the per-excess-column gain lower bound with factor 1−1.02/n. The augmented residual norm lower bound produces the stated η. Summed gains are at most ω times projected excess-noise-plus-bias energy. Division by mσ² gives EC′. The eigenvalue specialisation α≥φ, ω≤1/φ gives EC. The stated union failure probability follows from E2chi/E3a/E3b. The single-excess upper bound on α follows even if Λ≤0, since R_1/A≥0. L5.2 is the contradiction between screening, EC′ for every LO strict superset, and its assumed violation. Vacuous sizes q≤s₀ cause no problem.

**SCR-C:** L5_exact.md:81–103 and STATEMENT.md:171–176. Uniformly over k≤q, q log p=o(n) gives U(k,2 log n)=o(n), and ||θ*||₂=O(σsqrt(n)) gives η=o(1). Bounded s₀ makes the k-to-m logarithmic loss bounded. With ℓ=log(p/m), the floor gives `φ(2ℓ+log n)−2ℓ≥ε(2 log p+log n)`. This dominates all uniform o(𝐋), sqrt(𝐋), constant and 2ε₁log n terms. EC is violated for every admissible m, and the stated failure probabilities vanish. The polynomial-p simplification follows by monotonicity of the displayed ratio.

**SCR-R:** L5_exact.md:111–119 and STATEMENT.md:194–199. Screening gives μ∈span X_C, whence prediction error is P_Cε. The uniform sparse-projection event with x=2 log n supplies the stated prediction bound without a floor. Under the extra floor, the inverse Gram operator is bounded by 1/[φ(n−1)], giving the coefficient bound even though C is selected using y.

**SCR-N:** L6_sharp.md:5–52 and STATEMENT.md:201–212. At ∅ I independently obtained D=n and the exact equivalence between a non-improving singleton and `g_yc≤τ̂²B_n`. The two Gaussian union bounds and E2⁻ yield the finite-sample assertion. The elementary exponential bounds give B_n≤L_n and B_n/L_n→1 when log p=o(n). The orthogonal single-truth construction solves a positive scalar equation with θ₁² asymptotic to a constant times log n/n; its noise terms are lower order and it defeats any smaller threshold constant. The nearly cancelling pair with 1−r=1/n and b²=(log n)² has Δ asymptotic to 2(log n)² but Γ asymptotic to (log n)²/n; the same proposition makes ∅ LO with probability tending to one. These are statements about LO models, as expressly delimited.

### Supporting scratch and better-theorem note

Scratch: `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-SCR-R2-sol/check_review.py` and `check_review.out`. The hash checks pass. The independent finite-sample counterexample for finding 1 below has probability of any strictly improving truth addition 0.009630322866, whereas the report's master-event probability lower bound at x=3 would be 0.800851726529. This is supporting arithmetic; the proof counterexample is also given below.

**Better-theorem note, not a finding:** M4's o(n) entropy assumption can be relaxed with the constants already available in A1. With x_n=sqrt(log n), A1's B2d bound actually gives Γ≥κ²b²n/5 eventually. Its growth condition gives σr_n≤κb sqrt(n)/10+o(sqrt(n)), hence g⁻≥κ²b²n/9 eventually. Then Ū≤1.01nτ_*² yields u_S≥κ²b²/(10τ_*²) eventually, while B_S≤c₁n+O(1). Thus δ_S≥κ²b²n/(20τ_*²)−c₁n−O(1)>c₂n. Consequently REPORT:34's omission of the extra o(n) assumption is not itself a correctness finding: this stronger conclusion is derivable. This does not fix the unconditional assertion of an improving addition in REPORT:32–34 for general families without a positive-gap hypothesis.

## 3. Per-claim decisions

ACCEPT labels below concern the mathematical/code claims in the authoritative statement and their proofs. Finding 1 is a false derived summary in REPORT, and does not invalidate those 21 formal claims.

| id | decision | Independent check |
|---|---|---|
| CC | ACCEPT | CC1–CC6 traced through production scorer, scan, ledger, R flags and exact enumeration under EX-A. |
| L1 | ACCEPT | L1.1–L1.7: ridge identity, Schur update, determinants, exact score change, addition/deletion tests and augmentation. |
| L2 | ACCEPT | All E1/E2/E3/E4 variance, χ² and counting bounds, including zero-variance and vacuous cases. |
| SCR-A | ACCEPT | L3:6–24: uniform improving truth addition and both certified-output event inclusions. |
| A-inf | ACCEPT | L3:26–35: x_n=sqrt(log n), N_q bound, scale comparison and eventual MC. |
| SCR-Ao | ACCEPT | L3:37–56: residual-scale expansion and exact ϑo upper bound. |
| Ao-inf | ACCEPT | L3:58–63: every term of ϑo vanishes under the stated two growth conditions. |
| SCR-M | ACCEPT | L7:7–95,112–117: signed noise bounds, deterministic minimum thresholds, score-gap inequality and M1/M2/M3/M5/M6. |
| SCR-G | ACCEPT | L7:97–110 and M2/M5: fixed parameters, entropy o(n), c₂ and capped-path conclusions. |
| B1 | ACCEPT | L4:5–22: augmented weighted gain, monotonicity and minimisation over S. |
| B2 | ACCEPT | L4:24–33: anchored residual energy and l₁/l₂ inequalities with nonnegative brackets. |
| B2o | ACCEPT | L4:35–47: joint gain/residual bound and scalar monotonicities yield constants 4 and 9. |
| B2d | ACCEPT | L4:49–57: the directional energy inequality is all B2/B2o consume. |
| B3 | ACCEPT | L4:59–64: Schur-complement variational bound and direct superset floor. |
| A1 | ACCEPT | L3:65–76: all fixed-parameter steps, Γ lower bound, 200/64 margin and polynomial-p consequence. |
| A1o | ACCEPT | L3:78–86: bias restriction, Ψ≥8𝐋_n, denominator≤4𝐋_n and Ao-inf hypotheses. |
| SCR-C | ACCEPT | L5:81–103: uniform η=o(1), bounded-s₀ logarithmic loss and floor margin force EC violation. |
| L5.1 | ACCEPT | L5:7–69: inverse Gram dual geometry, per-deletion lower bound, joint upper bound and EC′ consequences. |
| L5.2 | ACCEPT | L5:71–79: screening plus violation of every strict-superset necessary inequality; probability union checked. |
| SCR-R | ACCEPT | L5:111–119: uniform projection bound after screening, then inverse-Gram floor for coefficients. |
| SCR-N | ACCEPT | L6:5–52: exact empty-score threshold, probability bound, B_n asymptotics and both explicit countersequences. |

## 4. Findings

1. **F — Unconditional strict-improvement claim in the derived report.** Location: `REPORT.md:32–34`. Quote: “On one event of probability ≥ 1 − 4e^{-x}, every model S of a deterministic family that misses a truth has a truth-addition improving F by at least an explicit deterministic gap δ_S”. What fails: SCR-M (`STATEMENT.md:113–117`, `L7_master.md:24–33,63–65`) proves only `F(S+t(S))−F(S)≥δ_S`; δ_S can be negative. A strictly improving addition requires a positive-gap hypothesis. Counterexample within Model G and EX-A: p=2, duplicated centred standardised true columns x₁=x₂, θ*=(1,−1), σ=1 and 𝓗={∅}. Then μ=0, both truth additions coincide, γ=0 and δ_∅=−log 3−0.5 log n<0. The probability that either addition strictly improves is exactly the upper tail at `v_n=n(n−0.98)(1−exp(−L_n/(n+0.02)))/(n−1)²` of a Beta(1/2,(n−2)/2) variable, because the noise direction is uniform in the centred (n−1)-dimensional subspace. At n=100 and x=3 it is 0.009630322866, below 1−4e^(−3)=0.800851726529. Equivalently, SCR-N with x_n=sqrt(log n) proves ∅ is LO with probability tending to one in this example, so no event of the asserted size can guarantee an improvement. **Required fix:** replace “a truth-addition improving F by at least” by “a truth-addition whose score difference is bounded below by”, and explicitly say strict improvement follows when δ_S>0. No change to the formal SCR-M theorem or proof is required. This is F, not E: the present sentence asserts a probabilistic conclusion that is false under its stated hypotheses.

No C or S finding is held against the formal 21 claims. No additional finding is held over newline serialization or version-history wording.

## 5. Gates

- **G1 FAIL:** All formal proof steps checked are correct, but REPORT:32–34 incorrectly promotes an unrestricted score-difference lower bound to a strictly improving addition (finding 1).
- **G2 FAIL:** A1 and SCR-G use exactly their stated hypotheses; the derived report omits the positive-gap condition needed for its unconditional improvement assertion (finding 1).
- **G3 PASS:** No additional hidden design, start, seed, calibration, rank, support-size or noise premise is required by the formal proofs.
- **G4 PASS:** Gaussian/χ² tails and Gaussian concentration are standard established results at the stated strength; the package supplies the required deterministic reductions. No conjecture, empirical check or earlier review is used as a proof premise here.
- **G5 PASS:** Score constants 0.01/0.02/1.02, ridge n+1, c₁=κ²b²/[200(M²+σ²)], c₂=κ²b²/[104(M²+σ²)] and uniform asymptotic errors check.
- **G6 PASS:** CC1–CC6 and EX-A match the inspected production algorithms, preprocessing, feasible neighbourhood, score, exact branch and output flags; newline-only source serialization differences do not alter them.

## 6. Score

**7.9/10.0.** The 21 formal claims are accepted, including the independently re-walked headline A1 chain and the post-change fixed-parameter import into SCR-G. One false probabilistic summary remains in the frozen package. The score reflects that F finding only; there is no editorial deduction. Per the round's mandatory rule, holding that finding requires gates=FAIL even though its repair is local and the formal theorem is sound.

COUNCIL-VERDICT round=R2 manifest=96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93 seat=sol score=7.9 gates=FAIL
