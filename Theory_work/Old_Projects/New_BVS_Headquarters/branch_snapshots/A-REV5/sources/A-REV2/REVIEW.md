# A-REV2 independent referee review

Reviewer: GPT-6 Astra, 2026-11-02. Branch: `theory/A-REV2`.

**Overall package verdict: GAP.** The T03♯ conditional theorem, the core refined greedy-repair theorem,
EXP′, and the bounded deterministic-chain mass law survive this audit. The submitted package cannot be
accepted unchanged: several auxiliary statements are **ERROR**, including two missed by the first
referees and one error in a referee's proposed repair. The random-partition and asymptotic repair
extensions retain their existing gaps.

`VERIFIED` below is a referee verdict on the specified statement and hypotheses, **not** an upgrade of
the author's status, adoption, or a change to the locked register. All source `PROOF SKETCH`,
`CONJECTURE`, and conditional labels remain unchanged. In particular, verification of the EXP′
implication does not edit the locked T22(iii) statement or discharge its other premises.

## 1. Versions, scope, and method fidelity

The seven exact branch heads are pinned in [SOURCES.md](SOURCES.md). Source abbreviations:

| Alias | Source |
|---|---|
| S03 | W1-T03R, `PROOF.md`, head `7e14d6f` |
| V03 | W2-VT03R, `REPORT.md`, head `b9f6d9b` |
| S37 | W1-T37R, `PROOF.md`, head `3bcc429` |
| V37 | W3-VT37R, `REPORT.md` and `REPAIRS.md`, head `4988b96` |
| SEX | W1-EXP, `PROOF.md`, head `722bd18` |
| VEX | W3-VEXP, `REPORT.md` and `REPAIRS.md`, head `7970fa0` |
| SU | W2-PREM, `PROOF.md` §2, head `988c5f5` |

The first T37 referee reviewed an older W1 head. Its statements that the report was unfinished and
the small-experiment files were empty are not descriptions of the pinned W1 head reviewed here.

I checked the imports against `Docs/Theory/proofs/LOCKED_PROOFS.md` and the actual files:
T01/T02 `PROOF_v3.tex`, T03 `PROOF_v2.tex`, T22(i)/(ii)/(iv) `PROOF_v3.tex`,
T22(iii) `PROOF_v2.tex`, and T27(i) `PROOF_v3.tex`. Their five SHA-256 values in
[baseline_sha256.txt](results/baseline_sha256.txt) match the locked register exactly.
The original T37 statement is
`Docs/Theory/PAPER_SELECTION_20261028/new_conjectures/T37_truth_dominance_greedy_repair.md`.

| Contract checked | Finding and consequence |
|---|---|
| `Docs/Methodology/METHODOLOGY_v3.md` §§4–5; `00_COMMON.md` §1; `v3_score.h::data_init`, `Scorer` | All principal proofs use the correct standardized score: `nu=n/2+0.01`, `H=(n+1)G+I`, `2b0=0.02`, and `w(k)=1/[2 C(2p-1,k)]`. The contrast rate is random, `b0*s_y²`; it is never treated as fixed in the T03 numerator identity. |
| Method §6.3; `v3_start.h::build_tables`, `build_start` | Tables score against the full response. The capped, normalized start is used in the chain telescope. No substitution of a block-specific response or an unnormalized reference mass is valid. |
| `v3_blocks.h::complete_linkage`, `make_blocks` | Complete linkage on `1-|r|`, union-lex merge ties, left-first cut, then next-fit packing. Fixed-X partitions are deterministic; conditioning on random X is different from conditioning on a selected block event. |
| Method §6.10; `v3_engine.h::local_search` lines 369–420 | All feasible flips and swaps are scanned with the centre frozen. Move only on strict improvement; neighbor ties use plain lexicographic order. After `ell` moves, an extra improving scan returns its best neighbor with `local_limit`, without certifying it. |
| `v3_core.cpp::cpp_final_run`, final search at lines 444–449; `v3_ledger.h` | The final centre is the running all-scored HPM. Every scanned candidate updates the ledger. Certification at the truth controls the final ledger, subject to the HPM tie rule. Pre-search and post-search HPMs must not be confused. |
| Method §6.2; `00_COMMON.md` §2 | Small-p experiments are component-law checks when production enumerates. They do not demonstrate SMC discovery. None of the reviewed mass laws alone is an algorithmic recovery guarantee. |

All numerical work ran as one small job at a time through the prescribed `owls_run -j 2` wrapper.
The initial system-Python attempt stopped before computation because NumPy was absent; an isolated
environment was then installed under this review directory. Package versions are recorded in
[python_packages.txt](results/python_packages.txt). No production or locked file was changed.

## 2. Verdict table

| Claim | Verdict | Qualification / repair |
|---|---|---|
| S03 Lemma E1(a)–(d) | **VERIFIED** | Exact BB size-marginal recurrence and both tail bounds, including `s0=0` in the upper bound. |
| S03 Lemma E2(i)–(iii) | **VERIFIED** | Keep the stated `s0>=1` restrictions and `n>=5` null-truth exception. |
| S03 Proposition E3 | **VERIFIED** | A barrier for the defined exact-tail cutoff and the specified numerator/denominator envelope; not a posterior lower bound or a universal impossibility theorem for other proof techniques. |
| S03 den′ and T02(i♯) | **VERIFIED** | Explicit constant and pointwise-in-m uniform tail-probability bound are correct. |
| S03 Lemmas I/B and T02(ii♯) | **VERIFIED** | Fixed unnormalized `g0>0` suffices on the anchored comparison unions. |
| S03 T03♯(i)–(v), under its SE and BM hypotheses | **VERIFIED** | C1–C10 checked against both locked proofs; no hidden normalized SE use on large unions found. |
| S03 Proposition D | **VERIFIED** | Duplicate-design counterexample under G and R, outside the SE hypotheses. |
| S03 reported proof-onset claim near `1.2e5` | **ERROR** | V03's correction is confirmed; the geometric-series condition still fails there (§3.5). |
| S37 Proposition 1 and swap identity | **VERIFIED** | Strict literal TD is contradictory for `d>=1`; equality has probability zero under the stated residual-rank condition. |
| S37 Lemma 0(a), (c) | **VERIFIED** | Completed scans; exact ties retained. The case where the initial centre already is the truth is trivial success. |
| S37 Lemma 0(b) as written | **ERROR** | New-delivery monotonicity inclusion survives; its post-search “posterior miss” inference does not (§4.2). |
| V37 R2 proposed exhaustive failure dichotomy | **ERROR** | It omits an inferior local maximum (and capped searches ending below the truth); counterexample and replacement in §4.2. |
| S37 Theorem A(A1)–(A4) | **VERIFIED** | Use the definition through the actual tie-broken greedy map, feasible region, closure, and sufficient move cap. |
| S37 Theorem A(A5), literal TD ⇒ TD′_P without POS | **ERROR** | Suppressor counterexample; V37 R1's POS repair is **VERIFIED** (§4.1). |
| S37 TD′_P ⇒ TD′_inf; converse fails | **VERIFIED** | Region closure is essential; independently reproduced combination proxy. |
| S37 definition `TD′_P iff (L) and all D_S` | **ERROR** | Strict separation is sufficient, not necessary with exact ties (§4.3). |
| S37 “weakest among at-most-Phi-move conditions” prose | **ERROR** | Necessity is for every move decreasing Phi, not merely for total length at most Phi; retain V37 R3's correction. |
| S37 Theorem B union-bound use / Theorem C extensions | **VERIFIED** / **GAP** | B's sufficient-event inclusion survives. C's sketches and V37 R4/R5 remain sketches; no asymptotic TD′ theorem is upgraded. |
| SEX Theorem 1 EXP′, exact remainder and stated bound | **VERIFIED** | Fixed-X actual blocks, uniform SE-blk, bounded B and polynomial family. Its displayed limiting constant needs the arithmetic correction below. |
| SEX/SU displayed `kappa -> 0.52/c_*` | **ERROR** | Actual limit is `0.51/c_*`; `0.52/c_*+o(1)` is only a valid looser upper bound (§5.1). |
| VEX R1 data-computable EXP′ certificate | **VERIFIED** | Deterministic; no high-probability event is necessary once realized SE and positive full-block RSS are checked. |
| SEX Theorem 3, deterministic fixed-length chain | **VERIFIED** | No response-selected chain; `1.01` upper multiplier is valid for the stated `n>=400`. |
| SEX Theorem 4, fixed CL(L) and normalized H3 | **VERIFIED** | Exact telescope; no independence between chain remainders needed. |
| SEX Theorem 4 growing-leakage bound / “iff” gloss | **VERIFIED** / **ERROR** | The bound gives sufficiency only; η is a leakage upper bound, not an exact threshold (§5.3). |
| SU Lemma U, expansion (U) on the declared family | **VERIFIED** | Same deterministic identity as EXP′; family union and rank bounds detailed in §6. |
| SU Lemma U's additional “every V ... used below” quantifier | **GAP** | Extra sets must be included in the cardinality budget, or L must be enlarged. The all-k application can be repaired explicitly (§6.2). |
| SU C3 zero-leakage upper bound | **VERIFIED** | A residual lower floor suffices, including when signal is omitted. |
| SU C3 matching lower bound under merely `delta=0` | **ERROR** | Omitted orthogonal signal dilutes the exponent; explicit counterexample in §6.3. Add `mu in span(X_T)` for the matching lower bound. |
| VEX random-design / actual-packing extensions | **GAP** | Preserve sketch status. Fixed-surrogate argument is sound in its restricted regime; general adaptive packing is not resolved. |

## 3. T03♯ audit

### 3.1 Exact size tail and cutoff

For `q_k=C(p,k)w(k)`, the ratio is `(p-k)/(2p-1-k)`. Thus the combinatorial multiplicity
cancels the apparent `1/p` penalty of a per-model addition. E1(a) is exact. For `i>=1`,
`log(2 rho_i)<=-(i-1)/(2p-2)`; the exceptional `i=0` inequality has the opposite sign inside
the exponent and is handled correctly. Summing `i-1` gives exactly the numerator in `gamma_m`.
The polynomial `t(t-1)` is nondecreasing on nonnegative integers, including the tie at 0 and 1.
The geometric sum starts at `m+1`, giving `2^{s0-m}`, not `2^{s0-m-1}`.

For the lower bound, `log(2 rho_i)=-log(1+(i-1)/(2(p-i)))`; bounding the denominator by `p-m`
is legitimate only in the stated range `s0>=1`, `m<=K-1`. E1(d)'s factor is a **lower bound on
the improvement factor**, not an exact expression for the improvement of the actual tail.

E2 follows by testing the proposed cutoffs in E1. In E2(iii), dropping
`(s0-1)(s0-2)>=0` weakens the lower bound in the correct direction. For E3, E2(i) gives
`m♯=O(log n)` and `p>=n^a` makes `m♯²/(p-m♯)=o(1)`. The binomial lower bound
`C(p,s0)>=(p/s0)^s0` then proves the displayed result. If the cap is reached, the tail is zero;
the statement expressly separates that case. Do not extend this calculation to all possible
data-dependent numerator estimates, or advertise it as the cutoff required by the true posterior.

### 3.2 T02(i♯): constants, rate, and quantifiers

Keep the ratio `R_m=varpi(|S|>m)/varpi(S0)` intact. At the deterministic rate `b_-`, the locked
density identity gives `E[N_m]=varpi(|S|>m)`. The integral over
`[sigma²,sigma²(1+n^-1/2)]` in the locked denominator proof gives den′ **before** its crude prior
lower bound is inserted. Consequently the constant is precisely
`c♯=kappa²/(c_IG sigma²)`, with no surviving factor 4.

On the rate-envelope event, `Theta♯<=c♯ exp(Lambda_n)Theta^(1)`. The split at `sqrt(L)`, Markov
for both nonnegative variables, and the locked envelope-probability bound prove the displayed
nonasymptotic inequality. `L>(c♯)²` makes its logarithmic denominator positive.

The quantifier is `sup_m P(Theta_nm>L)`, **not** `P(sup_m Theta_nm>L)`.
This is enough for the deterministic `m♯(omega_n)` and any deterministic real sequence `omega_n`.
It is not permission to select a cutoff from the response. For negative m, define `R_m` through
the prior-mass ratio, or truncate its summation lower index at 0. Empty tails have `Theta♯=0`.

### 3.3 Eigenvalue audit and T02(ii♯)

The determinant ratio in locked T01/T02 Lemma `spec(e)` holds for any fixed unnormalized `g>0`.
The exact chi-square law needs full column rank of the anchored union, also supplied by SE_w.
The upper smoother comparison uses normalized conditioning on the **smaller** model `S0` only:

`M_T-M_S0 <= n/(n+1) [(P_T-P_S0)+eta_n P_S0]`.

The larger model contributes only `M_T<=n P_T/(n+1)`. In particular there is no concealed
`lambda_min(R_T)>=phi0²` here. In the locked T02 proof, `onG(c)` already uses precisely this
one-sided argument. Replacing the determinant factor by `(1+1/g0)^(j/2)` gives the proposed
`a_n`, `bar r_n`, and `c2`; fixed `g0>0` leaves their rate unchanged. T02(i♯) handles the tail.

Anchoring is not a restriction to a small handpicked list of matrices. By interlacing it is
equivalent to the same bound on every nonempty T with `|T\S0|<=m` (and analogously for j0).
The substantive savings are the cutoff and the normalization for the larger sets. A
sequence `g0_n -> 0` is **not** covered by the stated fixed-constant rate.

### 3.4 T03♯ C1–C10 and assembly

| Step | Independent check |
|---|---|
| C1 | `s0<=m♯<=K` and `m♯<=C_m log n`; all deterministic good-event sequences have the required eventual bounds. |
| C2 | G1/G2 use Gaussian noise and rank upper bounds, not SE. G3 uses full rank of `S0 union J`. G4 needs only rank at most `s0`; B2 gives the stronger exact rank. |
| C3 | The only nontrivial eigenvalue use in the underfitting RSS upper bound is on S, which is a principal submatrix of the small anchored union. The restriction `|J′|<=j0` is stated. |
| C4 | Determinant: SE_w. Smoother upper bound: R on S0. Residual floor: G1/G2. This also covers algebraic comparison unions outside the cap. |
| C5 | The prior factor is multiplied by the truncated chi-square moment, then summed. No independence among chi-squares is invoked. The new fixed determinant factor enters q_n exactly once. |
| C6(a) | Prior ratio, determinant upper ratio, and monotonicity of Q give the crude bound without SE. The absent `exp(rho_n)` factor is a genuine saving. |
| C6(b), C7 | Both halves of the sharp smoother comparison, the RSS upper bound, and the signal Schur-complement bound are used only on small anchored unions. Interlacing supplies the condition on S. |
| C8 | Each union has at most `2^s0-1` underfitting preimages. Large `|J′|` uses C6(a), not the sharp comparison. The remaining prefactor times `Upsilon^{>j0}` has expectation `O(log(n)^((j0+1)/2)/n)`. |
| C9 | Exact-tail cutoff yields `O_P(n^-1/2)` above m♯; the cap case is zero. |
| C10 | `c>L_*` gives `(1-1/n)c>=L_*` eventually, at `n>=c/(c-L_*)`. BM-infinity eventually implies a fixed such constant. |

The last logarithmic-over-n rate is `o(r_n)` because `j0` is fixed. The final partition into
large models, strict supersets, and underfitting small models is exhaustive. PIP bounds are
deterministic. Boundedness of `1-pi(S0)` converts its convergence in probability to convergence
of its expectation, but does **not** provide an `O(r_n)` expectation bound; S03 correctly claims
only convergence for the frequentist HPM error. Screening uses the signal bound for each
strong coordinate and a union over at most fixed `s0` indices. For an empty strong set, retain
the locked proof's vacuous convention instead of leaving `min_empty PIP` undefined.

**Overall T03♯ verdict: VERIFIED under exactly its stated fixed-design, fixed-sparsity, anchored
SE and BM hypotheses.** This is posterior/global-HPM theory, not reported-HPM discovery.

### 3.5 Proposition D and finite-n disclosure

The rank-one formulas for `D_k` and `Q_k` are correct. For `k>=1`, the comparison with `m_1`
is bounded below by `sqrt(2/3)` and above by `exp(1.01)`. The tail constant is safe:
`sqrt(2/3)/(1/2+exp(1.01))>1/4`. Multiplying by the E1 lower bound gives the stated `2^(-m-4)`.
The squared sample correlation tends to the positive signal fraction when the fixed coefficient
is nonzero, so the event `m_empty<=m_1` has probability tending to one. The necessity statement
uses `m<=min(sqrt(p),K-1)`; a zero tail beyond K is not a counterexample to its restricted claim.

This example satisfies G and R but violates even size-two SE. It does not contradict T03♯.
Under T03♯, the posterior tail above `s0` itself is at most `1-pi(S0)=O_P(r_n)`.

I reproduced V03's geometric-series correction using stable products for the prior, avoiding
subtraction of large log-gamma values. With `s0=14`, `p=round(n^A)`, and the optimistically
vanishing `1/g0`, at the previously reported `n=130328`, q is about `5.53e22` for
`A=log(500)/log(200)` and `7.86e28` for `A=log(1000)/log(200)`, not at most 1/2.
At V03's respective points `2116048` and `2457025`, q is approximately 0.5.
The explicit `exp(2 epsilon_n)<=4` condition occurs much later, around the reported
`25571897` and `29755302`; my point evaluations agree. These are checks of the named
conditions, **not** a universal n0 for the theorem: other thresholds involve signal,
variance, eigenvalue constants, and the chosen BM sequence.

At `(n,p)=(200,500)` and `(200,1000)`, `m♯=100`, whereas the locked cutoffs are 201 and 215.
The cap removes the dimension-tail term there. It does not verify the anchored eigenvalue
hypotheses or make the asymptotic rate numerically informative.

## 4. Refined T37 audit and repairs

### 4.1 Literal TD, positivity, and the core Theorem A

At `S=S0-j+l`, the only missing-truth addition competes with the swap to S0. Literal TD
forces `F(S0+l)-F(S0)>=m`, whereas its S0 clause forces the same difference to be at most
`-m`. Thus m must be zero and equality must hold; strict TD is impossible. The nonconstant
analytic score difference has a null equality set when the extra column has a nonzero
residual on the truth. The cap hypotheses ensure both comparisons are feasible.

For `d=0`, “best move” need not mean “improving move.” Independently reproduced V37 CEX-1:
`n=100`, `p=12`, `corr(x1,x2)=.95`, signal `3*x1-2.8*x2`, ten orthogonal nulls, and a noise
vector orthogonal to all columns with squared norm 99. Literal strict TD holds on R0, but
the best addition from the empty model has gain **-2.2977998984**. The truth has gain
**20.9899772288** over empty and posterior mass **0.8645494125**. Search from empty certifies
empty. All comparisons witnessing the failure are strict and persist under small perturbations.

**POS repair, VERIFIED:** add positive gain for the move designated at each nontruth state.
Then strict literal dominance selects that progress move; the S0 clause supplies the terminal
condition. POS does not rescue the contradictory `d>=1` literal-TD premise.

For the refined theorem itself, the definition already includes `M(S)!=bottom`. In a finite
closed family, strict ascent visits distinct states and can terminate only at S0; conversely,
termination at S0 from every state gives closure and non-stalling. This proves A1 and its
score-rank length bound. In R_{a,d}, progress preserves the lattice. Counting additions,
deletions, and extra-to-truth swaps gives `tau=m+e-sigma`, with
`max(m,e)<=tau<=m+e`. The final certifying scan is available when `ell>=tau`; `ell>=a+d`
is sufficient, not necessary. This proves A2/A3, including the fixed-centre lattice version.

The necessity in A4 must keep its quantifier: all-start success gives posterior score
dominance on the whole starting family; success from one centre gives dominance only over
states on that path, not all alternative lattice states by its conclusion alone.

An independent combination-proxy example verifies nonconverse: orthogonal truths with
coefficients .3, `x3=.85*(x1+x2)/sqrt(2)+sqrt(1-.85²)*z`, and five orthogonal nulls.
The correlation minimum eigenvalue is .15; population gains at empty are .09 for a truth
and .13005 for the proxy. At `n=3000` with orthogonal noise, all 28 states in R_{2,1}
reach S0 inside that region, while the empty model first adds the proxy. TD′_inf holds
and TD′_P fails. This agrees with the first referee's substantive conclusion.

**Overall refined deterministic Theorem A verdict: VERIFIED for A1–A4 and the POS-repaired
literal-TD implication. The original A5(a) remains ERROR.** No G/SE/BM probability statement
is implied just by this deterministic result.

### 4.2 Lemma 0 and an error in V37's repair R2

For a genuinely new delivery, with `S_c!=S0` and ties set aside, strict ascent and the
pre-search ledger give the valid necessary condition
`F(S0)>F(S_c)=max_{S_pre}F`. If S0 is already the initial best model, success needs no
new-delivery event; the original wording should say so explicitly. Certification at S0
implies that every earlier scan was bounded by its chosen improving successor, and the
last scan has no higher score. This proves Lemma 0(c), without `pi(S0)>1/2`.

But a **post-search** competitor does not imply that the initial centre beat the truth.
The independent reproduction of V37 CEX-2 gives
`F({1,3})-F({1,2})=-2.2862503005` and
`F({1,2,3})-F({1,2})=7.2109846558`.
The search starts below the truth, moves to the superset, and certifies it. This refutes
the inference used to explain all 541 benchmark failures by initial monotonicity.
The per-fit initial scores are still required; this review did not obtain those data.

**Additional ERROR in V37 R2:** its proposed partition of every failed fit into
`E_LS^c` or `E_LS and terminal score >= F(S0)` omits an inferior local maximum.
The suppressor above has `E_LS` true and stops certified at empty, with score strictly
below F(S0). It satisfies neither proposed failure category. Thus the proposed proof
“Lemma 0(a) and (c)” does not establish an exhaustive dichotomy.

This is not merely a possible defect of arbitrary table-free scores. A checked variant has
`n=100,p=20,B=4`, two groups of four with within-group correlation .99 and hub cross-correlation
.95 (cross matrix `.95*R_a[:,hub]*R_b[hub,:]`), twelve orthogonal nulls, and signal
`3*x1-2.8*x5`. The true hubs remain in separate method blocks; every nonempty table model
has lower F than empty, every empty-centre flip is non-improving, and the two-hub truth has
higher F. The enumeration threshold is exceeded. Thus the table ledger does not force
discovery or exclude an empty centre in this variant. This is a local-search/ledger
counterexample; a full stochastic SMC run was not simulated.

**Repair:** classify failures by the pre-search and final ledger maxima, including:

1. `F_pre>=F(S0)`: the initial score obstructs a strict improving repair (handle equal-score HPM ties separately).
2. `F_pre<F(S0)` and `F_post<F(S0)`: an inferior local optimum or an insufficient move budget.
3. `F_pre<F(S0)<=F_post`: an explored competitor at least as good as the truth.

Use `F_post`, not necessarily the last moved centre: the extra scan at the move cap can
update the ledger and return an unscanned neighbor. This partition is exhaustive directly
from the two score comparisons. Categories 2 and 3 both fail delivery but have different causes.

### 4.3 Exact ties invalidate the asserted D_S equivalence

S37 defines TD′_P through the deterministic, tie-broken map M. It separately defines D_S
by **strict** score separation of progress neighbors from all nonprogress neighbors, and
asserts equivalence. The reverse implication is false under its fixed-data assumptions.

Concrete BVS counterexample: `n=100,p=2`, `x1=x2`, `S0={1}`, response
`.5*x1+e` with `e orthogonal x1`, `||e||²=99`. The singleton scores tie identically.
Their gain from empty is **7.6308489425**. Lexicographic order chooses truth 1.
At truth 1 the duplicate swap ties and is not a move; adding the duplicate has gain
**-0.0018640607**. Thus TD′_P(R0) holds, but D_empty is false because the null singleton
ties the progress singleton. No SE or NIS was assumed in the deterministic theorem.

**Repair:** retain D_S as a sufficient event only, or define `D_S^lex` to require
that the lexicographically first maximizer of F among all feasible neighbors is a
progress neighbor and has score greater than F(S). Then the equivalence with TD′_P
is exact. Bounds obtained by imposing the stronger strict D_S events remain valid.

The adjacent “weakest” prose makes a separate error: a bound on total path length
does not require every move to decrease Phi. A neutral step can be compensated by
a swap that decreases Phi by two. V37 R3 supplies the concrete three-move path
`{5,6,12}->{2,5,12}->{2,5,13}->{2,6,13}` for truth `{2,6,13}`, initially Phi=4.
Its first step is neutral. Keep the corrected necessity statement about **each move**;
the “weakest checkable condition” rhetoric has no defined class of certificates in
which a minimality theorem was proved.

### 4.4 Random centres and the remaining T37 gaps

Theorem B correctly unions over the deterministic family `Lat(C)`. For a response-selected
centre, one cannot replace that union by `2^Phi(S_c)` unconditional single-state probabilities.
The deterministic lattice implication is still useful after selection; the probability
calculation must pay for a fixed covering class or use an additional valid selection argument.

No upgrade of Theorem C or V37 R4/R5: the original noise-variance comparison fails for
nonnested projections; the union-model projection bound repairs that algebra but not the
whole uniform log-score expansion. The exceptional-null reduction needs the strengthened
dependence premise. Also, in V37 R4, once `2 log p` is subtracted from a threshold, the
result is the **excess above** the multiplicity penalty: if `t²=2 log p+u²`, then
`p P(|Z|>=t)` is bounded by a constant times `exp(-u²/2)`. The printed expression
`p P(|Z|>=u)` does not follow from that subtraction. Retain GAP for the asymptotic extension.
For example, with zero perturbation, `p=n` and `t²≈3 log n`, one has `u²≈log n`:
`p P(|Z|>=u)` grows like `sqrt(n/log n)` rather than vanishing. The repair is to put
the original t, not the excess u, in the Gaussian tail probability.

## 5. EXP′ and the chain laws

### 5.1 Theorem 1, checked lemma by lemma

Lemma 1.1: writing `eps=1/(n+1)`, the quantity
`tau=z'G^-1 z-z'(G+eps I)^-1 z` is nonnegative and at most `eps/phi²`.
The exact decomposition is
`Q=RSS^y+t/(n+1)+n*tau/(n+1)`, so the stated upper bound
`c_S<=1+1/(n phi²)` is valid. The empty-model convention is consistent.

Lemma 1.2: both Schur complements are taken in the correct matrices. In the notation
of SEX, `rho>=phi²(n-1)`, `N=(n+1)(rho+alpha1)`, and `M=rho+alpha2` with the
stated alpha intervals. The logarithm is Lipschitz with constant at most `1/rho`
on this interval, which gives the determinant remainder bound. Interlacing is
used only within the block (or within the pair in Theorem 3).

Lemma 1.3: substituting `0.02+Q_U=RSS^y_U+a_U` gives the displayed remainder identity
exactly. Both correction logarithms are nonnegative; their difference is bounded
by the larger one, so no factor two is missing. Raw and standardized RSS ratios
are equal; standardized response noise is never asserted to be conditionally Gaussian.

Lemma 1.4: `W=span(X_U,mu)` has dimension at most 17. Subtracting its projected noise
energy from total contrast noise gives the raw RSS floor. The Gaussian exponential
moment and union over at most `2^16 n^A` sets are legitimate for fixed X. The
normalization upper bound `||Y||²<=2Mn+4 sigma² n` yields the specified
`c_*=sigma²/[8(M+2 sigma²)]`. The elementary `(n-1)²>=n²/2` condition holds for n>=4.
The intersection of these events has probability tending to one uniformly over
the fixed-design class with the named fixed constants.

Thus the core theorem's exact expansion and deterministic bound on that event
are **VERIFIED**. It requires no cross-block orthogonality, beta-min, VIS, or NL.

**Minor ERROR, not a failure of the bound:** for fixed phi, the displayed expression
for kappa tends to `1.02/(2c_*)=0.51/c_*`, not `0.52/c_*`. For example
`sigma²=1,M=1,phi²=1` gives limit 12.24 rather than 12.48. The same error occurs
in SU. Replace the arrow by `->0.51/c_*`; an upper bound of the form
`<=0.52/c_*+o(1)` is valid. The `4.16` multiplier should be `4.08` for the exact limit.

VEX R1 is **VERIFIED**: nested projections make the smallest within-block RSS equal
to the full-block RSS. Substituting the realized `min_b RSS^y_{C_b}` gives a
deterministic certificate. Neither the asymptotic theorem nor its loose constant
proves that a particular n=200 dataset is on the probabilistic floor event.

### 5.2 Theorem 3: two-sided bounded-leakage ratios

Restrict Lemmas 1.1–1.3 to each chain pair; SE-chain suffices. The RSS-floor proof
requires no additional eigenvalue assumption outside those pairs. The exact identity is

`E_i = .5 log(n/(n+1)) - nu log(1-x_i) + R_i`.

Its lower bound follows from `x_i>=0`. For the upper bound,
`-log(1-x)<=x/(1-x)` and the nested RSS identity give
`nu*(delta_i+sigma Z_i)²/RSS_{T_i+l_i}`. The raw floor reduces the coefficient
to `(n+0.02)/(n-1)`, at most 1.01 for n>=103, hence for the theorem's n>=400.
This is a bound on an event with probability tending to one, not an everywhere
finite-sample guarantee.

Because the chain and its length c are deterministic in the fixed-X setting,
every Z_i is standard normal and `max_{i<c}|Z_i|=O_P(1)`, regardless of dependence.
Fixed L proves the two-sided H2 law. For growing L_n, the upper side is
`O_P(1)+1.01(L_n+O_P(1))²`; the lower side remains `-O_P(1)`.

**Quantifier boundary:** the locked T27(i) allows a data-measurable chain but assumes
H2 for that selected chain. SEX Theorem 3 discharges H2 only for its more restrictive
deterministic chain (or an independently chosen one with appropriate uniform
conditions). EXP′ alone does not preserve a standard-normal Z after response-based
selection. Do not apply this theorem to a selected trajectory without a uniform bound.

### 5.3 Theorem 4: normalized reference mass is essential

The telescope is exact, with the global cap and both normalizers canceling:

`log pi0(S0) = log pi0(Sref) + log[w(s+c)/w(s)] + sum_i log(table ratio_i)`.

For fixed s,c and `p>=2(s+c)`, adding `c log p` to the prior-ratio logarithm
leaves a deterministic bounded sum. H3 gives `log pi0(Sref)=O_P(1)`, since the
probability of falling below fixed `c0>0` tends to zero and pi0 is at most one.
The finite sum of tight E_i is tight without independent increments. The claimed
two-sided multiplier and its reciprocal are consequently tight. This is exactly
the locked T27(i) mass implication with H2 supplied by Theorem 3.

**Overall Theorems 3/4 verdict: VERIFIED with deterministic fixed-length chain,
fixed CL(L), and normalized H3 explicitly retained.** The H3-T22 route through
reference transfer retains SEX's `PROOF SKETCH` label; these theorems do not establish
H3 for arbitrary designs or actual delivered reference models.

The growing-leakage inequality also follows, with its upper exponent interpreted
as a high-probability / `o_P(1)` exponent statement. The subsequent “iff” is **ERROR**.
Counterexample: any exact-zero-leakage masked LH sequence satisfies CL(sqrt(log n))
with eta=1 as well as CL(0), yet the fixed-CL theorem still gives vanishing truth
start mass. A loose chosen upper bound eta cannot determine a necessary threshold.
Replace “iff” by “the displayed bound ensures the n-dependent masking factor
decays if eta<1/2.02.” If `p>=n^a`, the full upper bound has the less restrictive
sufficient exponent condition `a+1/2-1.01 eta>0`.

VEX R4 correctly removes “iff”, but its additional statement that `p^-c` **alone**
forces vanishing mass “whatever eta” is not justified: the multiplier in this
growing-leakage regime is not tight. Algebraically, the allowed form
`p^-c n^-c/2 * [p^c n^c/2/2]` is the nonvanishing mass 1/2. One must bound the
whole exponent. This objection concerns the inference from the upper envelope,
not the verified fixed-L theorem.

The optional limit law remains a sketch. VEX correctly distinguishes fixed p
from p tending to infinity in the prior constant. It also needs convergence of
the signal variance v if it is stated as convergence to one fixed distribution;
otherwise use subsequential limits or an n-indexed approximation.

### 5.4 Random X and random partitions

For EXP′, no response selection problem occurs: conditional on X, the partition
is fixed and epsilon remains Gaussian. Sparse covariance concentration on a
deterministic family of bounded-size subsets can supply SE-blk with high
probability, provided the signal-energy event is supplied too. This is the
scope of SEX §1.5; its original sketch label is unchanged. The claimed universal
study-covariance lower bound .15 is false for the .9 equicorrelation groups:
their minimum eigenvalue is .1, as VEX noted.

For the sharper random-design *start concentration* argument in VEX R3, the
fixed-partition surrogate is the right construction: define quantities over the
population groups before observing X, then identify them with actual-block
quantities on `{blocks=groups}`. Do not assert the unconditional Beta law after
conditioning on this selected event. For each fixed pair, Gaussian regression
independence gives the Beta partial-R² law and the truncated moment bound.
Its use before intersecting the partition event is valid. The positive margin
and `g<=B<2g` assumptions prevent packing groups together; a pairwise positive
margin is sufficient, while the stronger global margin used in the repair
should be stated if invoked.

For `B>=2g`, the group-packing choice can depend on the same predictor directions
used in the statistic. The surrogate argument is no longer supplied. This remains
a **GAP**, not a consequence of Theorem 1. The uniform LLN and full random-design
completion also retain their sketch labels. An additional exact-law correction:
after normalizing a Gaussian column, its direction is spherical, not Gaussian;
the masked projection delta conditional on the signal is not exactly normal as
SEX §4.3 claims. The needed `delta=O_P(1)` follows from its conditional second
moment and does not require that incorrect exact-normal assertion.

## 6. Lemma U: verified core, a quantifier gap, and a false lower corollary

### 6.1 Uniform expansion on the declared family

SEX's deterministic lemmas need only the pair's eigenvalue assumptions, not
membership in a block. For each set V in the declared family, project noise on
`span(X_V,mu)`; its dimension is at most `k+1`. With family size at most `n^A′`,
the exceptional probability for projected energy exceeding `L sigma² log n`
is bounded by `2^((k+1)/2) n^(A′-L/4)`. Hence `L>4A′` is sufficient. Total
contrast-noise concentration and the response-energy bound give the RSS^y floor
and the asserted constant. Uniformity is over a deterministic-in-X family, not
an arbitrary response-selected family of the same realized cardinality.

For E2's stronger projection onto `span(X_{V union S0})`, use a second union
bound with rank at most `k+s0`. Fixed s0 is a standing assumption in SU, so this
only changes the constant to `2^((k+s0)/2)`, not the exponent. No SE assumption
on the union with S0 is required for that noise projection. Since the union
contains the signal, RSS_V dominates its residual pure-noise energy. This fills
the terse parenthesis in SU without a hidden eigenvalue assumption.

C1, C2, C4, C5, and C6 follow from the exact odds identity, log inequalities,
and the uniform projection bounds on the needed sets. C6 additionally requires
its telescoping pairs to belong to the family; it is stated on `E_n(F_k)`,
which supplies them. C2 can use the stronger locked deterministic addition floor.

### 6.2 Cardinality must cover every additional set

The literal addition “and every V of size at most k used below” has no
cardinality premise tied to A′. Its E1 conclusion does not follow from the
displayed assumption on the original pair family alone. This is a **GAP** in
the statement's quantifiers, not a defect of the expansion identity.

Why a restriction is necessary: take `p=n-1` orthogonal columns, k=1, a single
pair family `{(empty,2)}`, A′=.1, and L=.5>4A′ (the two-set cardinality bound
holds eventually). If the extra V's include all singleton columns, their
projected noise energies are independent chi-square(1)'s and their maximum
is asymptotic to `2 log n`, not bounded by `.5 log n` with probability tending
to one. Merely fixing k does not fix the multiplicity budget.

**Repair:** explicitly define a deterministic auxiliary family H containing
all sets needed in E1/E2 and all chain endpoints. Require `|H|<=C n^a_H`, then
choose `L>4 max(A′,a_H)`. Alternatively restrict E1/E2 to the original endpoint
family. For the intended all-k use, `|H|<=C_k p^k<=C_k n^(kA)` and the stated
choice `L=4kA+1` suffices. For the block instance, use block subsets only; if
also controlling all k-subsets, use the larger budget. Fixed multiplicative
count constants are harmless in the union bound.

**Overall Lemma U verdict: VERIFIED for (U) and its events on an explicitly
budgeted family; GAP for the extra-family wording as submitted.** The same
`0.51/c_E` limit correction as EXP′ is needed. No status in W2-PREM is upgraded.

### 6.3 C3: zero leakage is insufficient for a matching lower bound

The C3 upper bound is valid: `delta=0` gives a pure-noise *increment*, and E2
lower-bounds the residual denominator. The parenthetical matching lower bound
uses E3 as though it also upper-bounded RSS_T by noise energy. That is false
when signal remains outside T.

**Counterexample, exact sufficient statistics:** let `n=1,000,000`, `p=2`,
`G=(n-1)I`, `S0={1}`, `mu=x1`, `sigma²=1`, `T=empty`, `l=2`, `phi²=M=1`.
Choose centered noise orthogonal to x1, with projection on x2 equal to
`sqrt(65)` in its unit direction and total squared norm `n-1`.
Thus delta is zero, `Z²=65`, `||Y||²=2(n-1)`, and the remaining orthogonal
noise energy is `n-1-65`. With L=5 all stated E1–E4 inequalities hold,
including the union-with-truth residual floor. The deterministic remainder
identity and floor hold as well.

The independent computation gives

| Quantity | Value |
|---|---:|
| kappa_n | 12.2400132448 |
| vartheta′_n | 0.7028313369 |
| Actual `log BF({2}) + .5 log(n+1)` | 16.2502645682 |
| Claimed lower bound `Z²/2-kappa_n-vartheta′_n` | 19.5571554183 |

The prior factor is identical on both sides of the odds bound and cancels.
This is a strict violation, stable under small perturbations of the noise.
It is also an asymptotic obstruction: along these orthogonal designs with
Gaussian noise, `log BF({2})+.5 log(n+1)` tends in distribution to `Z²/4`,
whereas the claimed lower bound tends to `Z²/2-12.24`. The violation probability
does not tend to zero (`P(Z²>48.96)>0`). A different high-probability event cannot
make the stated universal lower corollary true.

**Repair:** require `mu in span(X_T)` for the matching lower bound. Then
`RSS_T<=||C epsilon||²`; on E3,
`-nu log(1-x)>=nu sigma² Z²/RSS_T`, and E1 bounds the small coefficient error
by the proposed vartheta′_n. In particular this repair applies to null additions
at supersets of the truth. SU §3.4 uses the lower corollary at precisely such
supersets, so this finding does not itself refute that later construction.
The upper C3 bound at incomplete states is unaffected. The rest of W2-PREM's
terminal-kernel campaign is outside the requested Lemma U audit.

## 7. Independent small-scale reproduction

All outputs are in [checks.json](results/checks.json); executable code and seeds are in
[check_review.py](scripts/check_review.py). The script is independent of the author/referee
implementations. It uses the exact target formulas, Cholesky log determinants and solves;
the pseudoinverse is used for projection RSS in the intentional duplicate example.
Numerical comparisons allow rounding tolerances; exact ties in the tie counterexample
follow from duplicate-column symmetry, not a tolerance-based approximation to EX-A.

| Check | Reproduction result |
|---|---|
| E1/E2 | 6,190 tail/cutoff cases, with rational prior masses and integer squared cutoff comparisons; zero violations. |
| T03 B1/B3/C6(a) | 384 model comparisons on six small designs, three with a near-duplicate null pair; zero violations, largest numerical B3 eigenvalue residual `5.72e-15`. |
| Proposition D | At n=p=200/800/3200 the smallest n^-1/2 cutoffs are 4/5/6; the displayed lower bound holds in each checked case. The matrices are reduced analytically to rank-one sufficient statistics. |
| T37 core | 448 centres on 16 datasets; 224 capped certifications under TD′_P; A1 equivalence, lattice containment, move counting and ledger dominance all pass. |
| T37 counterexamples | Positivity failure, pre/post-search distinction, duplicate exact-tie failure, and combination-proxy nonconverse reproduced independently. The production-table-compatible suppressor variant also passes. |
| EXP′ / Lemma U | 696 additions over all sets of size at most three on p=8 AR(.5) designs. Maximum decomposition error `1.39e-13`; every deterministic certificate holds. Largest `|R|` is .9213, versus the loose kappa bound above 15. |
| Theorems 3/4 | Exact start enumeration on a p=12 linked-hub family, eight noise draws at each n=100/400/1600. All chain telescopes and two-sided inequalities pass. Normalized log-mass medians are .432/.549/.582, consistent with a bounded multiplier; this does not prove tightness. |
| Lemma U C3 | The strict counterexample in §6.3 is reproduced from a 2-by-2 Gram matrix; no million-row matrix is allocated. |
| T03 proof thresholds | Stable-prior point calculations confirm V03's correction and the cap at study dimensions; no large design matrices or production simulations. |

The small experiments corroborate identities and falsify universal claims. They do not
estimate the actual benchmark's 541-fit failure decomposition, verify SE over production
size subset families, establish an asymptotic rate, or validate floating-point execution
as exact arithmetic. Those would be different tasks.

## 8. Required disposition

1. Retain the T03♯ proof with its exact hypotheses; correct the finite-n disclosure and
   describe E3 as a barrier for this cutoff/envelope route only.
2. Retain Theorem A(A1)–(A4), apply POS to the literal-TD implication, replace the D_S
   equivalence by a sufficient implication or a tie-aware definition, and replace both
   the original posterior-miss explanation and V37 R2's incomplete dichotomy.
3. Retain EXP′ and Theorems 3/4 within their fixed-design and deterministic-chain scope;
   correct the limiting constant and the necessary/sufficient wording. Keep H3 explicit.
4. Specify Lemma U's full event family and cardinality budget. Restrict its matching
   lower corollary to residuals with no omitted signal; the upper corollary remains usable.
5. Leave all random-partition and T37 asymptotic extensions at their source status.
   No locked result, adoption decision, or campaign status has been changed by this review.
