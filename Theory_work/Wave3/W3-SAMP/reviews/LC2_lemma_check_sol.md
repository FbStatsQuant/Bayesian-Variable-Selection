# LC2 — cross-family lemma check (Sol)

Reviewed 2026-11-09. Scope: new v3 material specified in the brief. Read-only review; only this report was written in the repository. No git operations or source edits. Verdict: **VERIFIED WITH AMENDMENTS** overall. No counterexample found to the substantive finite-sample inequalities. One MAJOR localization defect remains in the stated TR premise; the other findings are MINOR proof/notation repairs.

## Item verdicts

| Scoped item | Verdict | Findings |
|---|---|---|
| C Step 4: telescoping evidence budget and beta | VERIFIED | Loss inequality, rescaling at stage zero, c, W, and both budgets check out. |
| C Step 5: uniform error, MPM, bias | VERIFIED WITH AMENDMENTS | Issue 2: replace two false equalities by inequalities; constants survive. |
| C Step 6: convergence and rates | VERIFIED WITH AMENDMENTS | Limits and rates hold locally without launch probability tending to one; clarify named-premise equivalence in issue 5. |
| TR: minorization, composition, Doeblin, arbitrary bridge, asymptotics | VERIFIED WITH AMENDMENTS | Finite-sample proof works. Issue 1 changes the stated asymptotic premise; issue 4 defines its boundary convention. |
| LT Step 2′ / LT-b′ | VERIFIED WITH AMENDMENTS | Weighted argument works; issue 2 also applies to its displayed equality. |
| LT-e′ | VERIFIED WITH AMENDMENTS | Issue 3: the MPM tie requires a non-strict Markov bound or a smaller threshold. |
| D section 3 / D-iii / D-iv | VERIFIED | MAP premise, tie rule, discovery transfer, and Q=infinity extension are correct. |
| STATEMENT v3 versus proofs | VERIFIED WITH AMENDMENTS | Constants match; issues 1 and 5 concern hypotheses/localization, rather than a failed numerical constant. |

## Numbered issues

1. **MAJOR — P-OVL-infinity as written silently forces launch probability to one.** `STATEMENT.md:75`, `lemmas/TR_theorem.md:18`, `STATEMENT.md:157` (compare `STATEMENT.md:31-35,163`). The literal assertion `1_A L/M -> infinity in probability` implies `P(A^c) -> 0`: its left side is zero on A^c. It is not equivalent to `M=o_P(log n) on A`, and conflicts with the advertised absence of a launch-success premise. Unlike P-OVL at `STATEMENT.md:76`, this definition supplies no infinity-off-A convention.

   **Fix:** define `Q_TR := L/M on A, infinity on A^c`, and require `Q_TR -> infinity in probability`. Equivalently require `P(A intersect {L/M <= H}) -> 0` for every finite H, or `1_A exp(-L/M) -> 0 in probability`. The production equivalent is `1_A M/log(n) -> 0 in probability`. Use this definition in the theorem file as well. For example, with P(A)=1/2, M=1 and L tending to infinity, the intended localized condition holds, while the displayed indicator-times-divergence condition fails. The proof at TR lines 54-56 already works under the corrected weaker premise. This is an incorrectly strong premise/mismatch, not a counterexample to TR under its literal stronger hypothesis.

2. **MINOR — upper bounds are substituted as equalities.** `lemmas/C_theorem.md:61,65`: `E(1-W)^+ = beta/2` is false in general; Step 4 proves only `E(1-W)^+ <= beta/2`. The same issue occurs at `lemmas/LT_theorem.md:39`: the minimum containing the actual `E[W Lambda_bar]` need not equal the minimum with its upper bound substituted.

   **Fix:** change these equality signs to `<=`. Every claimed bound and constant remains valid. Explicit C counterexample within the arbitrary-positive-target identity framework: N=1, T=1, pi0=(0.8,0.1,0.1), s=first state, exp(a)=(1,0.5,2). Then c=1.05, `E(1-W)^+=0.090476190476...`, whereas `beta/2=0.095238095238...`. Mutation after weighting cannot change this evidence calculation. This counterexample targets the equality, not C-iv or its constants.

3. **MINOR — LT-e′ invokes a strict-tail bound at an inclusive MPM threshold.** `lemmas/LT_theorem.md:78` says the MPM conclusion follows with u=1/2 from the preceding bound for `P(E_r>u)`. MPM failure implies a pooled error at least 1/2, and truth coordinates can be excluded at a tie; strict error greater than 1/2 is not necessary.

   **Fix:** either use u=1/4 and the inclusion `{pooled error >= 1/2} subset union_r {E_r>1/4}`, or explicitly strengthen LT-b′ to `P(E_r>=u | C) <= g/(u eta)+P(W<eta | C)`. The latter follows immediately by the same Markov argument and keeps u=1/2. No extra asymptotic assumption or factor p is required. The finite-sample C and TR MPM arguments use expectation plus non-strict Markov directly and do not have this problem.

4. **MINOR — state the M=1, L=0 convention.** `lemmas/TR_theorem.md:8,31-33`, `STATEMENT.md:151`: e_L=(1-1/M)^L includes 0^0 for an allowed component configuration. The M=1 argument correctly gives K_1=Pi, but at L=0 the initial point mass need not equal pi.

   **Fix:** define e_0=1 for every M; for L>=1 use the displayed power. Thus for M=1, e_L=0 only when L>=1. This is a boundary-definition clarification; with the usual zeroth-power convention the inequalities already hold.

5. **MINOR — distinguish localized concentration from the globally defined P-CONC.** `STATEMENT.md:143`, `lemmas/C_theorem.md:70`: `1_A delta_bar -> 0` is equivalent to `1_A o_1 -> 0` and P-START. It is not equivalent to globally defined P-CONC (`STATEMENT.md:69`) plus P-START unless the phrase “on A” explicitly redefines/localizes P-CONC. Concentration can fail on A^c when P(A^c) does not vanish.

   **Fix:** write the equivalence using `1_A o_1 -> 0`, and separately state that P-CONC plus P-START is sufficient. The C proof itself uses only localized concentration, including its HPM term `P(A intersect {delta>=1/2})`; no P(A)->1 is needed.

## Checks of the fragile arguments

**C Step 4 — VERIFIED.** V is positive, so the loss inequality is precisely convexity of x -> (1-x)^+ applied to the empirical mean. MR-a is applied to f_t=(1-exp(Delta_t a))^+, which is uniformly bounded by one even over calibration values, and is data-and-C-measurable. At t-1=0, V_0=1 and the initial empirical measure has mean pi0; no mutation or resampling identity at a negative index is being assumed. Dividing the unnormalized MR identity by `Z0 exp(phi d(s))` gives exactly `sum pi0(S) exp(phi a(S)) f(S)`.

For a(S)<0 the expected loss bound is the difference of consecutive exp(phi a(S)) terms; summing over the frozen increasing grid telescopes. The normalization is c=pi0(s)/pi(s), not its reciprocal, and W=V_T/c. Since a(s)=0, the truth contributes zero to both b-minus and b-plus. Consequently b-minus<=delta0, b-plus<=c delta, and delta0/c=(1-delta)o0. The expression `b_minus+(c-1)^+=max(b_minus,b_plus)` is exact. No T, N_e, or cap-dependent factor is lost.

**C Step 5 — VERIFIED after issue 2.** For any E in [0,1], `E[(1-W)E] <= E(1-W)^+ <= beta/2`. For a bounded coordinate estimate f, mean-zero 1-W gives both signs of `E[(1-W)f]` bounded by that same deficit. Thus the bias constant beta/2 is correct. Averaging islands requires no independence. The constants 21, 22, and 44 follow from ST's kappa<=o1, delta<=o1, lambda<=19o1. Discovery follows already from initial draws.

**C Step 6 — VERIFIED locally.** Bounded random conditional tail bounds converging in probability to zero have expectations tending to zero. This needs neither almost-sure convergence nor convergence of untruncated expectations. To justify the O_P(r_n) assertion explicitly, set D_n=1_A delta_bar. For X equal to evidence error or uniform PIP error and any K,H>0, the conditional first-moment bounds imply

`P(A intersect {|X|>H r_n}) <= P(D_n>K r_n) + C K/H`.

Tightness of D_n/r_n then gives localized tightness of X/r_n. For log evidence use `1-exp(-H r_n) >= H r_n/2` for large n at fixed H. No joint L1 rate follows or is claimed. The W3-POST rate citation at its STATEMENT lines 79-80 is accurate, with its antecedents retained by the ticket's premise registry.

**TR kernel and path arguments — VERIFIED.** The diagonal is safe: proposing the current state has mass pi0(x), is accepted with probability one, and is a self-loop; rejected other proposals only add diagonal mass. Thus the minorization holds on every singleton, including the diagonal. In `K_pre K_I K_post`, only stochasticity of the prefix and pi-invariance of the suffix are needed. Each fixed permutation has these properties; averaging over fresh state-independent orders preserves the minorization. The Doeblin residual Q is stochastic and pi-invariant when M>1, giving the displayed TV contraction. At M=1, minorization with coefficient one forces K_1=Pi.

The per-particle chain given the pre-measurement history is justified. T12 R3 gives the same one-round conditional law at every population-round boundary; iterating conditional expectations gives each particle's future path law from its own entering state. Code `v3_engine.h:343-360` has no post-T resampling or interacting state update. Shared earlier ancestry does not invalidate the marginal Markov property. The common RB accumulator records values and does not feed transitions (`:128,354-356`). The “bad-round” function psi is bounded in [0,1]; its stationary mean is at most delta+(1-delta)lambda. Burn-in therefore costs just e_L for this whole four-round functional, not four e_L and not p e_L. In fact the proof yields the bound conditional on the entire bridge history, which validates “any bridge outcome.” The endpoint refinement delta+e_(L+q) in the lemma is stronger than, and implies, the statement's delta+e_L. Asymptotics then work under the repaired localized premise in issue 1.

**LT Step 2′ and LT-e′ — VERIFIED after issues 2-3.** W is determined by initial draws and bridge weighting, hence measurable before every measured round. Code updates logZ only at bridge line 322 and returns the unchanged value at line 365. At fixed c, MR-b at s=L+q-1 gives `E[W A_(r,q-1)]=pi(s)=1-delta`. Random L causes no optional-time problem: freeze c first (equivalently partition on its integer values). Multiplying the conditional leave bound by nonnegative history-measurable W is valid. The two pointwise upper bounds W E_r<=W and W E_r<=W(kappa+B_bar+Lambda_bar) give the claimed g.

A data-and-C-measurable eta_n can be inserted in the frozen inequality. The hypothesis `1_A o1/eta_n -> 0` makes the truncated tail integrand vanish, while the assumed lower-tail probability handles collapse. Endpoints also follow using delta<=o1 in LT-a; discovery uses LT-c, and the retained P-CONC supplies the HPM/MAP step. Eta_n need not literally tend to zero for this result. No launch-success premise is needed.

**D section 3 — VERIFIED.** Under exact arithmetic, `v3_util.h:121-125` orders by F, then size, then lexicographic order, so the exact HPM is unique even with score ties. The sufficient premise is S-dagger=S0, not necessarily delta<1/2. Discovery then transfers to the reported HPM on completed runs by PC. The probability bound correctly allows failure of the MAP premise, and delta<1/2 is merely a sufficient condition for it. The new Q definition equals D_r pi0(S0) on A and infinity off A, so `exp(-Q)=1_A exp(-D_r pi0(S0))`. P-OVL, with its explicit infinity-off-A convention, implies this bounded integrand vanishes in probability and expectation. This does not need P(A)->1. The production lower bound and exponent 4D_r only under IND-T match the statement.

## Numerical falsification and limitations

Inspected `samp_sim.py`, `run_checks_v3.py`, and the existing `RESULTS_v3.txt`. Did not re-run the existing writer, which would overwrite another repository file. Instead ran additional Python 3.13 checks from a scratch directory outside the repository, with bytecode writing disabled.

Seed 9917; 12 arbitrary positive targets: p=1 or p=3, caps K=1,2,3 where applicable, and flat, mixed, or concentrated target/start pairs. Enumerated every fixed round order (up to 720), checked minorization, averaged round kernels, and checked TV and the uniform-error path envelope for L=0,1,4 from every possible bridge terminal state. Enumerated all N_e=1 bridge state paths on grids [0,1] and [0,0.1,0.6,1], checking the expected total loss and expected absolute evidence error exactly up to floating point.

Zero violations beyond floating-point tolerance. Largest positive residuals: minorization 1.23e-15; TV 1.69e-14; path envelope 0; telescoping loss 2.78e-15; evidence error 0. The strict-equality counterexample in issue 2 was also computed directly. These checks support the algebra; they do not establish asymptotic localization or replace the inherited START/KERNEL/ideal-stream premises. No new problem found in the cited T12 identities, R3, ST constants, or PC transfer within the scoped material.
