# A-REV9 independent analytical check: masked PIPs and PW2

Review scope: F-MASKPIP M1–M3 and N-a; O-PW2 Theorems A–B, including Corollary B2. No simulation, numerical experiment, or computational validation was run. These are independent review candidates, not changes to any original campaign status. Root owns the final verdict.

## Audited sources and assumptions

- `origin/theory/F-MASKPIP`: commit `dbe45faf6e7cd4bda027d3da16309d99f81600ed`, `theory_campaign/F-MASKPIP/REPORT.md`.
- `origin/theory/O-PW2`: commit `e685ead7d08b7a8eff553ccd6cb2d622a168bffe`, `theory_campaign/O-PW2/REPORT.md`; inspected the setup/scoring portion of `scripts/pw2_exact.py` as contextual source, without execution.
- Local locked-reference baseline HEAD: `581e4baeacc0901c7bbaef417828eda57769b5c3`; read `Docs/Theory/theorems/00_COMMON.md`, T12, T23, T03, T25. Read the detailed T12 `STATEMENT.md` through `git show origin/theory/F-MASKPIP:...`.
- Read authoritative local `METHODOLOGY_v3.md` at the path recorded in `00_COMMON.md`. Its round order is fresh for every particle and round; resampling is multinomial at every bridge stage, including the final bridge stage; terminal burn-in/measured rounds do not resample; final islands have fresh separated streams. These details support the conditional iid-child argument below.

All affirmative findings concern the exact frozen SMC component conditional on successful calibration, with exact positive target/start weights, exact iid start sampling (START), EX-A, EX-S, CAL, and independent particle mutations. They do not certify floating-point code, actual calibration success, operational completion, or the full method's exact-enumeration branch. The theorem inventory's original conjectured status is preserved.

## F-MASKPIP

### VERIFIED candidate: M1 and M2

Let `W=Zhat_r/Z`, `f_s` be the fraction outside truth at the specified terminal position, and `delta=1-pi(S0)`. Locked T12's unit-potential extension gives `E[W f_s]=delta`, `E W=1`. For a measured path indicator `B_ih`,

`B_ih <= 1{start != S0} + 1{start = S0} D_ih`.

At that round start, W is already measurable and the conditional departure probability on truth equals `rho_bar`. Thus `E[W Bbar] <= delta + rho_bar`; T23's pathwise RB inequality gives `E[W err] <= delta+rho_bar+u_pi`. No particle independence is needed here. The bound `rho_bar <= min(1,(B+3)u_pi)` is already T23(iii), so the mathematical content need not depend on an unreviewed W2 lemma.

Each M2 intersection bound follows by Markov applied to the corresponding nonnegative weighted quantity. In particular `1{f>1/2} <= 2f`, and secondary pooling obeys `Wbar err_sec <= (1/4) sum_r W_r err_r`. For MPM use `err>=1/2` directly, including equality. These are joint/intersection bounds conditional on calibration, not statements conditional on observing a high evidence estimate. Informal wording such as 'PIPs can be wrong only on low-evidence islands' must retain the displayed exceptional probability.

### VERIFIED candidate with endpoint repair: M3 conditional means

For `C={f<=1/2}`, `kappa=P(C)`, the identities imply

`E[W 1_C] >= 1-2delta`, `E[W 1_Cc] <= 2delta`.

The reported conditional-mean inequalities follow when `0<kappa<1`. As written M3 assumes only `kappa>0`, so its second conditional expectation is undefined at `kappa=1`; omit that clause there or restrict kappa. The first inequality alone does not assert overestimation for every kappa: its lower bound exceeds one only when `kappa<1-2delta`.

### ERROR candidate: M3's claimed lower-tail example

The assertion `P(W<c | C)=1` for some `c<1`, for every `kappa in (0,1), delta in (0,1/4)`, is false. For example, `kappa=1/2, delta=1/10` forces `E[W|C]>=1.6`, incompatible with `W<c<1` almost surely on C. The proposed example itself puts a very large W on a positive-probability subset of C, directly contradicting its claimed probability one. It also sets `W=0` on C-complement despite assuming `W>0`.

Repair preserving the intended first-moment obstruction: fix `0<kappa<1`, `0<delta<1/4`, and choose `0<a<min(c,(1-delta)/kappa)` for a chosen `0<c<1`. For small `0<kappa'<kappa`, partition C into masses `kappa-kappa'` and `kappa'`, set `f=0` there, and set W respectively to

`a`, and `b=[1-delta-a(kappa-kappa')]/kappa'`.

On C-complement set `f=1`, `W=delta/(1-kappa)`. All weights are strictly positive, `E W=1`, `E Wf=delta`, and C is exactly `{f<=1/2}`. For sufficiently small kappa', b exceeds c and

`P(W<c | C)=1-kappa'/kappa -> 1`.

Thus no useful universal conditional lower-tail guarantee follows from these first moments alone, while the exact probability-one claim must be withdrawn. This is an abstract moment counterexample, not a construction of a v3 BVS dataset/run.

### VERIFIED candidate / precision GAP: N-a

The exact finite-index consequence is

`P(f_0>1/2, W<sqrt(delta)) >= P(f_0>1/2)-2sqrt(delta)`.

Consequently `delta_n->0` and `liminf P(f_0>1/2)>=kappa` give liminf of the left side at least kappa. They do not imply the report's literal finite-n lower bound `kappa-2sqrt(delta_n)` without the stronger premise `P(f_0>1/2)>=kappa` at each index. Replace it by the displayed probability or `kappa-o(1)-2sqrt(delta_n)`.

The underestimation factor on the event is at least `delta_n^(-1/2)` and the true evidence / reported 0.05 evidence bound is at least `20 delta_n^(-1/2)`. T03 states only `delta_n=O_P(sqrt(log n/n))`; it does not imply the report's unit-constant factor `>= (n/log n)^(1/4)(1+o(1))`. It yields an inverse-order-in-probability lower scale: for every fixed error probability choose a finite C with `delta_n<=C sqrt(log n/n)` with that asymptotic probability, obtaining factor `>= C^(-1/2)(n/log n)^(1/4)`. Keep data randomness and frozen-run randomness distinct.

## O-PW2

### VERIFIED candidate: Fact F and A1–A4

Conditional on the preceding population, multinomial ancestors and independent mutation randomness produce iid children with law mu_s. W_s is measurable before those children are generated. With `Q_t=g_t K_t`, target invariance gives `q_(t-1) Q_t=q_t`, hence `q_s h_(s,T)=1`. Then

`M_s=W_s qhat_s(h_(s,T))`, `E[M_s|F_(s-1)]=M_(s-1)`, `M_(T-1)=W_T`.

At s=0 use the trivial pre-start sigma-field, W_0=1, mu_0=q_0. Conditional iid sampling gives

`E[(M_s-M_(s-1))^2 | F_(s-1)] = W_s^2 Var_mu_s(h_(s,T))/N`.

Orthogonality proves A2. Writing `m_s=E M_s^2`, `e_s=E[W_s^2 mu_s(h^2)]` yields

`m_s-1=(1-1/N)(m_(s-1)-1)+(e_s-1)/N`,

which proves A3 by unrolling from m_-1=1. For N=1 the final coefficient with exponent zero is 1, including the usual `0^0` empty-product convention. A4 is the direct identity `W_t=W_(t-1) qhat_(t-1)(g_t)`. No mixing or reversibility beyond target invariance is used. Shared random mutation orders across particles would invalidate Fact F, but the inspected methodology explicitly prescribes fresh orders per particle.

### VERIFIED candidate: B1–B3 and pooled factor

For fixed `h=h_(s,T)`, weighted unbiasedness gives `E[W_s mu_s(h^2)]=q_s(h^2)`. Therefore

`e_s-(1+sigma_sT^2)=E[W_s(W_s-1) mu_s(h^2)]`,

whose absolute value is at most `H_sT^2 E[W_s |W_s-1|] <= H_sT^2 sqrt((1+V_s)V_s)` by Cauchy–Schwarz. This proves B1 with zero initial error. Its monotone recursion proves B2. Conditional independence of the four final island streams gives precisely `Var(Wpool)=V_T/4`, bounded by U_T/4; this does not imply the same unconditional variance formula across shared random calibration.

B3's induction is valid: `U_t<=x+y sqrt(2x(1+2x))<=2x` when `2y^2(1+2x)<=x`. The upper-bound use of the undiscounted sum of variances is valid because the A3 coefficients are at most one.

### VERIFIED candidate with scope GAP: Corollary B2 / asymptotic wording

B1 implies `N(V_t-V_(t-1)) <= S_t-S_(t-1)+eta_t+eta_(t-1)` because dropping the discount factors only enlarges the nonnegative eta terms. Replacing the signed difference by its positive part and multiplying it by `v_(t-1)>=1` yields the proposed PW2 constants. Define `S_0=eta_0=0` explicitly. Sign handling remains correct even if the variance increment is negative.

The `O(N^(-3/2))` slack and bounded limiting a_t conclusions hold for fixed finite input, fixed frozen grid/T, and fixed kernels as N grows: then all H and sigma constants are fixed, B3 applies eventually, and U_s=O(1/N). They are not uniform claims along the actual growing n,p,T budgets. Any growing-budget claim requires displayed control of H, variance sums and the B3 condition. The report acknowledges the missing useful constants; the finite-state identities alone do not remove the substantive study-scale PW2 obligation in locked T25(iv).

## Review boundary

No fresh validation of stored numerical outputs, no approval of F-MASKPIP N-b/N-c or Theorem R, no review of O-PW2 Theorem C beyond reading it for context, and no theorem-status upgrade is made here. In particular the source campaigns' historical laptop computations are not reproduced or treated as new remote validation.
