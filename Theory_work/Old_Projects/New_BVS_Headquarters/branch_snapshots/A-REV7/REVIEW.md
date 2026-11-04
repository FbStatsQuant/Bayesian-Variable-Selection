# A-REV7: no-LS0 masked-regime referee review

Reviewer: GPT-6 Astra; 2026-11-02. Independent Sol checks covered engine/GU and B2 confinement. All conclusions below were integrated and checked by Astra. Candidate source statuses are preserved; a referee verdict is not adoption or an edit to the campaign registry. Frozen branch SHAs are in `sources/refs.json`. Sources cited below are the frozen copies, not moving branch heads.

**Conclusion: a no-LS0 masked theorem is available on an explicit exact-Gram LH subfamily.** W5-B2ENV's B2-LH confinement/repair argument is VERIFIED conditional on STAB-LH, with the small event-bookkeeping correction below. Section 4 supplies an Astra-authored analytic sufficient condition for STAB-LH, so this conclusion need not rest on a numerical premise. D2-LH is also VERIFIED for qualitative consistency, for one linked pair and p/sqrt(n) tending to infinity; its stated unconditional rate is a GAP. Neither result establishes unrestricted LH or the production study's random designs, finite-n accuracy, or probability of successful completion.

## 1. Verdicts and scope

| Candidate | Source status (unchanged) | Referee verdict | Exact scope / remaining issue |
|---|---|---|---|
| O-BGIBBS BG3 | PROVED, conditional | VERIFIED | Abstract round-boundary lock and terminal scoring inequality, given EX-A/EX-S/SR. |
| O-BGIBBS LH-lock | PROOF SKETCH | VERIFIED **conditional fixed-p implication** | Section 3 fills the implication from strict C1–C3 and block keep margins. General LH locking is false; do not remove those hypotheses. |
| F-SHARE F1 | PROVED | VERIFIED | Round-boundary closure only, given KEEP; does not itself supply repair. |
| F-SHARE F2 | PROOF SKETCH | GAP | Proxy-condition coverage, cap-sensitive mass mapping, and erroneous displayed ridge identity need repair. Literal c=1 exemption from DOM: ERROR with counterexample in §5. |
| W5-B2ENV D2-LH, c=1 | PROVED given cited results | VERIFIED for consistency; GAP for stated rate | p/sqrt(n)→infinity, exact Gram, groups equal blocks. Retain unconditional o(1), not the asserted quantitative unconditional rate. |
| W5-B2ENV B2-LH | PROVED under STAB-LH | VERIFIED conditional theorem | Uniform bounded-extra confinement is valid. Correct the minor RSS event-rate statement; §4 proves STAB on an explicit subfamily. |
| W7-SEP GU | PROVED, candidate | VERIFIED as a greedy-search theorem | GAP as a standalone no-LS0 growing-p theorem: the actual HPM search centre need not lie in its isolated finite relevant set. |

No source PROOF SKETCH or CONJECTURE is silently relabelled PROVED. The new arguments are explicitly Astra-authored. A positive verdict below means the stated, qualified implication has been checked; it does not mean all assertions in the source report are correct.

## 2. Method and locked-result audit

`Docs/Methodology/METHODOLOGY_v3.md` §§5–6 and `Scripts/SMC_BVS/core/cpp/v3_engine.h` agree on the relevant operations:

* Each bridge stage, **including the stage ending at phi=1**, reweights and resamples, then mutates. After that stage's mutation there are L burn-in and four measured rounds without resampling. BG3 uses these L+4 rounds; F-SHARE counts the stage-T mutation as well, giving L+5 after the last resampling. Both counts are consistent.
* Each round has p Gibbs labels, one uniform swap, B neighbour swaps, and one independence proposal, in fresh random order. A proof only for flips does not establish a lock.
* Gibbs scores its current state and feasible flip before choosing. Swaps and independence moves score proposals before acceptance (`v3_engine.h:113–194`). `v3_ledger.h` offers the scored states to the HPM tracker. Rejected proposals count; occupation is unnecessary.
* The independence proposal is an exact start-law draw. For closure its exit probability is bounded by pi0(W-complement), regardless of its acceptance rule. It is **not** necessary to bound its acceptance by endpoint target ratios.
* Neighbour-swap Hastings factors must be included (a polynomial bound p suffices here). Uniform endpoint score gaps survive such factors.
* The final local search starts from the best model already scored, not an arbitrary start particle or S°. GU cannot replace that centre by S°.

HQ's frozen `SR_AUDIT.md` is substantively correct about scored-state coverage. Its blanket wording that no call passes `emit=false` is too strong: `v3_core.cpp:447,610,657` pass false through `local_search`, whose centre evaluation uses `emit_centre`. These centres are already-scored ledger HPMs, so the exception does not invalidate the scoring arguments. No LS0 is used here.

All probability statements use the campaign's exact-arithmetic/fresh-randomness assumptions and potential execution convention. Locked T21 composes posterior concentration with *ever scoring* the truth. It yields P(output and wrong)→0, or liminf P(output and correct)≥1−limsup P(no output). It does not prove completion, or conditional accuracy given an arbitrarily rare output. T03's statistical assumptions are retained. W1-EXP's LH exact Gram has a global eigenvalue lower bound, fixed nonzero signals and Gaussian noise, which supply the T03 inputs asymptotically. No quantile-sampler lambda prior is involved in this BVS model.

For fixed p, the production method eventually takes exact enumeration (Methodology §6.2). BG3/LH-lock at fixed p is therefore an SMC **component** result. The growing-p subfamily in §4 avoids that limitation.

## 3. Astra-authored completion of conditional BG3/LH-lock

Fix p and the LH parameters. Eventually K=p, so all sets below are feasible. Let U={T:T contains S°}. Suppose the finitely many population deletion/swap losses C1/C2 and missing-hub addition gains C3 are strictly positive. The start-block losses C1'/C2' hold on LH: the projection onto a visible a-group is beta(1−psi²)x_a, onto an unlinked visible group is beta_h x_h, and onto a masked group is zero. A cross-block swap loses the visible block signal and adds only a zero partial-signal variable in the other block. Within-block swaps leave a positive residual by positive definiteness. These statements concern the separate block likelihoods, not a fictitious joint likelihood for their summed fits.

**One common data event.** For the finite family of sets, unstandardised RSS(T)/(n−1)=sigma²+Delta(T)+o(1), uniformly in probability. One can take a deterministic tolerance tending to zero, e.g. n^(-1/4), and use Gaussian and chi-square tails. Response normalisation is bounded above/below on the same event. The ridge score has Q(T)=RSS_y(T)+O(1), uniformly, and one-step determinant/prior terms are O(log n). Consequently every strict population loss or gain gives a log-score margin at least a n for one deterministic a>0, on a single event E_n with P0(E_n)→1. The same holds for the finite block comparisons. This supplies actual fixed constants rather than treating a random O_P(sqrt(n)) separately at every algorithmic visit.

**Start mass.** If T omits a visible reference hub, add it. The associated table improvement is exponential for every configuration of its group, and the size-prior penalty is polynomial. Since K=p, this injection is feasible even away from U. Summing over at most 2^p sets gives pi0(U-complement)≤C exp(−a n), after reducing a.

**All move types.** Until a first departure from U, each visible-truth Gibbs deletion has probability at most exp(−a n). Each swap removing one has probability at most p exp(−a n), including the Hastings factor. The probability that the single independence proposal is outside U is at most pi0(U-complement). Additions cannot leave U. Thus a first-step-exit union gives a uniform one-round bound epsilon_U≤C m exp(−a n), m=p+B+2. In particular this bounds end-of-round exits, which is all BG3 needs.

**Terminal repair.** From any y in U, order all missing-hub Gibbs labels first, then all labels of y outside S0, then the remaining labels. This event has probability at least 1/m!. Each missing hub is added with probability 1−o(1), uniformly, by C3. Once all hubs are present, each extra has zero signal gain and keep odds O_P(n^(-1/2)); a finite uniform event makes all such deletion probabilities 1−o(1). No swap or independence label intervenes before repair. The last needed flip scores S0 whether or not accepted. If y=S0 it is already scored. Therefore beta_1≥(1−o(1))/m! on E_n.

**BG3 inequality without conditioning on a future survival event.** A first bad initial draw or round-boundary exit has probability at most N pi0(U-complement)+N(T+L+4)epsilon_U. Sequentially expose terminal particle-rounds; on every history that remains good and has not yet scored S0, the next round's scoring probability is at least beta_1. Multiply the conditional failure bounds, stopping at a bad history. This gives

P(S0 unscored | data, calibration) ≤ N pi0(U-complement)+N(T+L+4)epsilon_U+exp(−N(L+4)beta_1).

This proves the claimed conditional implication. Since N and T_e are polynomial/logarithmic, N(T_e+L+4)m exp(−a n)→0. Add P0(E_n-complement) **once**, not once per visit. This is the required uniformity over all events. Fixed-p constants and 1/m! cannot be exported to growing p.

**Why the unrestricted sketch cannot be filled:** C2 is false for allowed LH parameters (§5). Strict gaps are not a technical regularity that follows from |psi|<rho. The conditional proposition is useful and correct; a universal locking theorem is not.

## 4. B2-LH and an explicit fully closed no-LS0 route

The W5 proof uses N={S contains S°, at most 19 neutral extras} and N' with at most 40. Masked-group proxies are unrestricted, but their total number cg is fixed. All states used have a fixed size bound; their total number grows polynomially with p. This avoids F2's arbitrary-size superset difficulty.

**Uniform likelihood events.** U1/U2 follow from the score expansion, the global eigenvalue bound, Gaussian cross-term tails, and chi-square tails, unioned over O(p^vmax) sets. Exact unit orthogonality reduces each residualised noise coordinate to a within-unit configuration: at most p 4^g distinct normals. Lemma J truncates their squares at 2 log(p4^g)+2 log log n. The elementary integral E[exp(Z²/2)1{|Z|≤z}]=2z/sqrt(2pi) gives sum of neutral inclusion bounds epsilon_n=O_P(sqrt(log n/n)), with constants depending on the fixed parameters. The supremum single-coordinate bound is O_P(log n/sqrt(n)).

**Small correction (Astra-authored):** the displayed U2 event with chi-square error n^(2/3) gives relative RSS error O(n^(-1/3)), not the O(sqrt(log n/n)) written in Lemma J. Use eta_n=O(n^(-1/3)+sqrt(log n/n)) there. Since eta_n log n→0, its exponential correction is still 1+o(1), and all conclusions and stated orders for epsilon_n survive. No stronger event is necessary.

**Confinement checked against actual moves.** Predraw the single independence proposal. Conditional on it and the label order, the probability that r specified neutral Gibbs labels end included before the stopping time is bounded by the product of their q_l. Summing yields epsilon_n^r/r!. At the end of a round every surviving neutral is attributable to such an inclusion, to one of at most B+1≤17 swap additions, or to the independence proposal. Initial neutrals have all faced their own label; they cannot simply be counted as persistent. The temporary 40-extra envelope also covers the unprocessed initial neutrals. Leaving the 19-extra class requires at least three Gibbs/proposal neutral inclusions, unless a reference truth is removed. STAB bounds the latter exponentially at both endpoints. Independence exits additionally use its start tail. Hence a_n=O_P((log n/n)^(3/2)), uniformly over starting states, temperatures and histories up to first exit. Multiplying by N T_e=O(n log² n) gives O_P(log^(7/2)n/sqrt(n))→0. Resampling only copies states and needs no fitness-envelope hypothesis on the good histories.

**Repair checked.** R1 orders the finitely many relevant extra/masked-group Gibbs labels before all B+2 non-Gibbs labels and each missing masked hub before its group's proxies. The exact order probability is bounded below by

c_* = g^(−c)/choose(2cg+19+B+2, B+2)>0.

Missing hubs have uniformly positive population gains: their partner a is already present, the unit has only one missing true coefficient, and its residual variance is at least lambda_0 psi_i² beta_i². After addition, proxies are noise-only. Neutral-addition failure sums tend to zero by J, and reference truths are retained by the deletion part of STAB. Thus a stage-T particle scores S0 with probability ≥c_*−r_n, r_n→0, independently conditional on its entering state/history. Multiplication over fresh particle random blocks gives (1−c_*+r_n)^N. Stage T already suffices; no post-T resampling assumption is needed for this route.

These checks establish B2-LH's conditional bound. Integrate the bound truncated at one over the common data event to obtain unconditional convergence. Its conditional O_P rate is not automatically an unconditional numerical rate.

### Astra-authored analytic STAB certificate

Let R_M=sum_i beta_i² psi_i²(1−psi_i²)=Delta(S°), b_vis²=min_{j in S°}theta_j² and lambda_0=(1−max_i|psi_i|)(1−rho_max). If

**lambda_0 b_vis² > R_M,**

then STAB-LH holds, with margin at least lambda_0 b_vis²−R_M, for every proxy configuration and every number of orthogonal null columns.

Proof: for V containing S°, Delta(V)≤R_M. Every deletion V−j or swap V−j+l, j in S°, l outside V, omits j. For any such set W, the Schur-complement eigenvalue bound gives Delta(W)≥lambda_0 ||theta_(S0 outside W)||²≥lambda_0 theta_j². Subtract Delta(V). This simultaneously proves C1 and C2, including cross-unit swaps; it does not rely on proxy enumeration. C3 follows from the one-missing-hub calculation above. The block keep bounds were proved in §3. QED. This certificate and the following concrete instantiation were independently checked by a Sol reviewer after Astra wrote them; the check agreed.

**Concrete growing-p subfamily.** Take g=9, c=2, no unlinked visible groups, rho=.4, psi=.2 for both pairs, beta_1=beta_2=1, sigma²=1; append null groups and choose p_n=9 floor(n/18). For large n B=16 and g≤B<2g, so W1-EXP's deterministic partition lemma gives groups=blocks. Exact centred Gram exists since p_n≤n−1. Here lambda_0=.48, R_M=.0768, b_vis²=1: the analytic STAB margin is ≥.4032. The signal set is fixed, eigenvalues stay bounded below and all nonzero coefficients are fixed, so the LH start and T03 statistical premises hold. B2-LH therefore proves P(output and wrong)→0 for the unchanged method on this explicit family. There is no numerical or unproved STAB premise left.

It is genuinely masked: W1-EXP gives pi0(S0)=(p sqrt(n))^(−2) exp(O_P(1)), whereas the final iid proposal budget is O(n log²n); their product tends to zero. The exact-branch state count grows exponentially with p, so the asymptotic algorithm uses SMC. This is the strongest positive answer of this review. General LH-iid and parameter choices violating STAB remain outside it.

## 5. Counterexamples and F-SHARE limitations

### ERROR: unconditional LH swap locking

One pair, g=4, rho=.85, psi=.5, beta_a=1.4, beta_b=−.7. Index a=0, b=4, with a-proxies 1,2,3. Set V={0,1,2,3}, W={1,2,3,4}. The independent residual calculation gives

Delta(V)=.3675, Delta(W)=.3627106863596872.

Thus the swap 0?4 **improves** the population fit by .004789313640313. Its posterior acceptance tends to one. It is an allowed uniform swap with fixed positive proposal probability, and it removes a member of S?. This is an explicit counterexample to C2 for general LH and to an exponentially small *single-step* exit bound. It refutes the purported universal two-endpoint locking mechanism. It is not, by itself, a counterexample to an end-of-round bound: subsequent moves may repair an exit. No exact round-end lower bound or failure of the overall algorithm is claimed here.

The type enumeration reproduces W5's negative margin for g=9 as well (rho=.85, psi=.5, beta_a=1.4). Thus failure is not limited to g=4, which would cease to equal the method's blocks when p grows.

### ERROR: “DOM is void when c=1” with visible groups

Take one pair, g=4, rho=.4, psi=.2, beta_a=1, and a separate visible hub h=8 with beta_h=.01. From S°={a,h}, swap h→b. The residuals are .0384 before and .0001 after. This is a profitable cross-unit swap even though there is just one masked hub. F-SHARE's exemption from DOM in F2 is therefore false when visible groups are present. The c=1 **no-visible-group** case is different: its only reference truth is a and its swap to b is within the same unit. The counterexample does not refute F2 with an actual full DOM assumption.

### F2 sketch: what is fillable and what is not supplied

1. Lemma 1.2's pointwise display is not the proved bound. Its proof requires suprema over all intermediate y in W, and (B+1) swap labels with their Hastings factors. A safe replacement is s sup_(y,j)max(kappa_0,kappa_1)+(B+1)p sup_(y,j,l)max(rho_0,rho_1)+pi0(W-complement). F1 with this eta is valid. KEEP controls round ends, not every intermediate state.
2. PK(g−1) as defined counts total proxies in a **pair unit**; that unit has 2(g−1) proxies. W includes configurations beyond g−1. Hence “every proxy configuration” does not follow from the written hypothesis. One must prove the omitted configurations or assume the full finite set of inequalities. Cross-unit masked **proxies**, not only masked hubs, also require a swap-gain comparison. They can be bounded by the hub gain using the unit projection identity, but that argument must be supplied.
3. Lemma 3.4's Schur formula has a real factor error. With A=I−X_U(G_U+I/(n+1))^(-1)X_U', the correct increment is

Q_U−Q_(U+j) = [n/(n+1)] (x_j' A y)² / (x_j' A x_j+1/(n+1)),

not n times that quotient. At n=10, U empty, x_j'x_j=9 and x_j'y=1, the actual increment is .1; the printed expression gives 1.1. Also an O(n^(-2)) *relative* approximation is unjustified near zero signal, and standardised y is not an unscaled Gaussian shift. These mistakes are repairable with an additive bound and explicit normalisation.
4. For fixed p and full strict population gaps, §3 supplies the missing Gaussian/ridge proof. For growing p, exact orthogonality indeed leaves only O(p4^g) residual directions for local comparisons. A common noise event, a global RSS floor and a cap-aware mass argument are still required. F2(a)'s map y→y union S° can exceed K; its repeated keep inequality also invokes W bounds at states outside W after more than one deletion. Neither is justified as written. B2's small-set/start-tail split avoids both problems.
5. F2 supplies delivery only. Its subsequent §4 contains the expressly conjectural extras/resampling argument 4.3. Closing a Gaussian estimate alone does not close that scoring route. For fixed p BG3 replaces it; for growing p B2's bounded-extra construction is the verified alternative.

Consequently F2 remains GAP in its stated generality. These gaps should not be described as merely omitted numerical constants.

## 6. D2-LH, M-LH, and GU

**D2-LH:** the no-blow-up event must use corrected NB' (ESS at 1/T0 at least .9H, or initial scoring of S0), as in W3-VT38E and W6-FIXREV1. The elementary ESS share argument, first-stage resampling, and the order placing the single missing-hub label before its proxies and non-Gibbs labels are valid. At that label S0 is scored even when its acceptance probability is tiny. The neutral departure sum from S° is o_P(1). W5's NB' bound is O_P(sqrt(n)/p+n^(-1/2)), so p/sqrt(n)→infinity gives discovery in the pilot with probability tending to one. Pilot scores enter the eventual reported HPM; this is no LS0.

The unconditional O(sqrt(n)/p) claim does not follow just from these O_P quantities. Its stated remainder must also cover the data events giving start mass≥1/2 and departure sum≤1/2. A complete qualitative statement is obtained by intersecting these events and integrating the probability bound truncated at one. Quantitative expectation/tail control is the minimal remaining gap for its literal rate. The proof does not establish its heuristic matching lower-rate remark either.

**M-LH versus A-REV3:** the lattice proof uses exact RSS logarithms, not the invalid quadratic/log expansion previously criticised for W4-SHARE M(b). Fixed nonzero LH coefficients also satisfy the stronger asymptotic signal regime; this is not a new BM-C-uniform claim. Retain the exact constants carefully: writing (1−o(1)) and then “absorbing” it into the same defined g_* is not a valid algebraic step. Here it is fillable: for every R_i>0 the actual limit log(1+R_i/(sigma²+sum R−R_i)) is strictly larger than log(1+R_i/(sigma²+sum R)); the finite minimum has strictly positive slack. Uniform convergence eventually makes the posterior log odds ≥n g_*/2, including O(log n) penalties. This justifies the stated crossing threshold on this fixed-parameter lattice. B2 does not depend on M-LH in any case.

**GU:** the Schur-complement lower bound and l1/l2 argument give best truth-addition reduction at least (lambda_min/s0)Delta. The score comparison then makes each greedy underfit move reduce Delta by a fixed factor, and isolates the path inside R. On supersets, the chi-square union over 2^r p directions makes additions unfavourable; deleting an extra beats swapping that extra for a new variable. The source report's casual phrase “every swap loses” is stronger than needed: the proof correctly compares an extra swap to its corresponding deletion. This establishes the stated move bound and eventual certification under its hypotheses. It is a greedy best-neighbour argument, not a random Gibbs-round argument. For growing p the actual best-scored centre may include nulls outside R. Showing its eligibility, or adding a search from S° (LS0), is still necessary to use GU alone. For fixed p take R=[p], and remember that production eventually enumerates.

## 7. Numerical evidence and reproducibility

All numerical calculations ran on `owls.stat.rice.edu` under `/home/fb31/theory_campaign/A-REV7`; no simulations or numerical validation ran on Felipe's laptop. Applicable `/AGENTS.md`, `/home/AGENTS.md`, `/home/fb31/AGENTS.md`, and the task-directory ancestor AGENTS paths were checked before execution; none existed at those paths. The unrelated recursive home search was not used as permission to work in another project.

`reproduce.py` (Astra-authored) independently calculates the explicit residual witnesses and production-formula sample log odds. Its type enumeration imports the frozen W5 implementation, clearly distinguished from the independent calculations. It runs four noise replicates per n=400,1600,6400, seed 20261102, and records all raw values in `remote/results.json`. `sources/O-BGIBBS/scripts/bg3_popcheck.py 2` is also rerun unchanged, exhaustively checking the c=2,p=16,g=4 candidate's population gaps; output is `remote/bg3-c2.log`. The reproduced BG3 minima are C1=.217969, C2=.030469, C3=.085793, with maximum C4 error 2.22e-16. The W5 type checks give swap margins .3051199262 (g=4,rho=.7,psi=.5), ?.0047893136 (g=4,rho=.85,psi=.5), .6069265045 (g=9,rho=.4,psi=.2), and ?.0550749319 (g=9,rho=.85,psi=.5), with the coefficients explicitly recorded per case in the raw JSON. This is a small algebra/score reproduction, not a full production SMC benchmark or proof of uniformity.

The successful process ID was 2570276. Transferred result/log SHA-256 hashes were independently compared with the remote hashes and match (`AUDIT.json`); that file also records the methodology and engine file hashes. The persistent launch is `nohup sh run.sh > launcher.log 2>&1 < /dev/null &`, with PID saved in `remote/pid.txt`. `remote/started.txt`, `finished.txt`, `environment.txt`, `exit-status.txt`, `input-sha256.txt`, `output-sha256.txt`, and logs preserve the audit trail. The first launch failed because system Python lacked numpy; its files are retained in `remote/failed-launch/`. The successful launch used `/home/fb31/envs/dl/bin/python`, not a local fallback. Saved exit status is 0. The shell wrapper and exact source are committed here. No claim is made that four Gaussian replicates estimate an asymptotic probability.

## 8. Referee recommendation

Use B2-LH with an explicit verified stability condition, preferably the analytic sufficient condition in §4, as the no-LS0 masked theorem. State exact Gram, fixed signal units/parameters, growing p≤n−1, EX-A/EX-S/SR/CAL and the output-potential convention. D2-LH supplies a second qualitative c=1 route. Keep BG3 as a fixed-p component lemma and F1 as an abstract closure lemma. Do not cite F2 or GU alone as an unrestricted growing-p no-LS0 guarantee.

The minimal gap for **unrestricted** LH is control of profitable swaps out of the visible-superset class: either avoid proxy-rich states with a proved occupancy bound, allow temporary missing visible truths and prove delivery/repair, or use a different argument that does not claim closure. The explicit counterexamples preclude filling the general lock sketch by Gaussian concentration alone.

Summary 1/8: VERIFIED — BG3 as a conditional component theorem.
Summary 2/8: VERIFIED — fixed-p LH-lock implication with strict gaps; unrestricted gaps fail.
Summary 3/8: VERIFIED — F1; GAP — F2; ERROR — its c=1 DOM exemption with visible groups.
Summary 4/8: VERIFIED — D2-LH qualitative consistency; GAP — its asserted unconditional rate.
Summary 5/8: VERIFIED — B2-LH with STAB and the event correction; an analytic LH subfamily is supplied.
Summary 6/8: VERIFIED — GU as greedy repair; GAP — eligibility of the actual growing-p search centre.
Summary 7/8: Owls saved-output reproduction completed; no LS0 or production algorithm change.
Summary 8/8: Reproduction source head SHA: 2d672a08a32b570aabedef01527bf047fffc1f77; final delivery head is in the accompanying message.
