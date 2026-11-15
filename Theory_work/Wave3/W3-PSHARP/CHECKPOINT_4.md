# W3-PSHARP — CHECKPOINT 4: HQ acceptance record (2026-11-12)

HQ decision 2026-11-12 (PROTOCOL rules 10, 11; INFRA R05 safeguard 1: the ticket's own checkpoint is the status
source). Council cell: `R2; MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14; sol=9.2 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)`.
Both seats accepted every claim below in their dated per-claim addenda (R06 rule; no rescoring). Nothing in the
frozen manifest changed. REGISTRY blocks: REPORT.md §6 (frozen), with the status (this file) and the HQ-decided edits only.

Status lines (one per claim; status text, then the claim id):

PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-PSHARP:S
PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-PSHARP:A
PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-PSHARP:B
PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-PSHARP:C

## Registry blocks

```
REGISTRY
claim: W3-PSHARP:S | kind: lemma | statement: STATEMENT.md:32-44 | premises: STATEMENT.md:16-30
name: Lemma S (one-step supersets with the fit factor kept)
status: PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:10
conclusion: identity: D_{S+j}/D_S <= n (equality iff x_j orthogonal to col X_S); Q_S - Q_{S+j} = n (x_j'rho_S)^2/s_{S,j}; odds against S0 >= [(s0+1)/(2p-1-s0)] n^{-1/2} sum_j exp(nu gamma_j) | scope: any n >= 3, any design, any data, |S|+1 <= K
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14; sol=9.2 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-PSHARP:A | kind: proposition | statement: STATEMENT.md:46-77 | premises: STATEMENT.md:16-30
name: Proposition A (the sqrt(log p) factor is attained; rate lower bound on witness designs)
status: PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:11
assumptions: A:GAUSS-NOISE ; A:ENERGY ; A:PSHARP-COEF (new | coefficient bound on S0 | squared norm of theta* at most n M' | STATEMENT.md:50 | shared no) ; A:PSHARP-WORTH (new | orthogonal null block | null columns of N_n mutually orthogonal and orthogonal to col X_S0 | STATEMENT.md:54-55 | shared no) ; A:PSHARP-WSPH (new | spherical null block | null directions iid uniform on the unit sphere of 1-perp, independent of eps; (log N)^2 = o(n), (rank X_S0 + 1) log N = o(n) | STATEMENT.md:56-60 | shared no)
conclusion: negative: P(delta/(1-delta) >= (1-eps) Lambda_n) -> 1 under A:PSHARP-WORTH or A:PSHARP-WSPH; with all nulls and fixed s0, delta_n >= (1-o_P(1))(s0+1) sqrt(log p/(pi n)) and liminf E delta_n/that >= 1 | rate: (s0+1) sqrt(log p/(pi n)) (lower bound) | scope: witness designs; p <= n-1 (orthogonal) or (log p)^2 = o(n) (spherical, p >> n)
depends_on: W3-PSHARP:S@proof:S(2),S(4)
sharpness: A:ENERGY = WEAKENABLE (evidence: ASSUMPTION_MAP.md:12) ; A:PSHARP-COEF = WEAKENABLE (evidence: ASSUMPTION_MAP.md:12) ; A:GAUSS-NOISE = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:11)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:P2(reviews/K01_break_astra.md) ; better-disposition:P2=adopted(reviews/K01_disposition.md)
council: R2; MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14; sol=9.2 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-PSHARP:B | kind: corollary | statement: STATEMENT.md:90-114 | premises: STATEMENT.md:16-30
name: Corollary B (sparsity obstruction on every design)
status: PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:12
conclusion: negative: for every design and data set with 0 <= s0 <= K-1, delta/(1-delta) >= O_lb_n >= c(p,s0)/sqrt(n); consequences for sequences with s0 <= min(K-1, p/2), where c >= (s0+1)/3: pi(S0) -> 1 needs s0 = o(sqrt n), and rate r_n needs s0 = O(sqrt(log n)); if in addition s0/p -> 0 and s0 ~ lambda sqrt n, limsup pi(S0) <= exp(-lambda/2) | rate: c(p,s0)/sqrt(n) (lower bound; equal to (1+o(1))(s0+1)/(2 sqrt n) when p -> infinity and s0/p -> 0) | scope: inequality: any n >= 3, any design, any data, 0 <= s0 <= K-1; consequences: s0 <= min(K-1, p/2)
depends_on: W3-PSHARP:S@proof:S(1),S(2)
implies: W3-POST:Prop-LB (j = 1 term with c(p,s0) >= 1 and n <= n+1, on LB's domain)
sharpness: A:EXT-FEAS = NECESSARY (evidence: ASSUMPTION_MAP.md:9)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:P1(reviews/K01_break_astra.md) ; better-disposition:P1=adopted(reviews/K01_disposition.md)
council: R2; MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14; sol=9.2 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-PSHARP:C | kind: counterexample | statement: STATEMENT.md:116-149 | premises: STATEMENT.md:16-30
name: Proposition C (ridge-cost control of the reference cannot be dropped)
status: PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:13
conclusion: negative: on the design D_n the reference T = {1,2} represents mu exactly and (E) holds, but pi(|S| > m^T_n(log n/2)) -> 1; Lemma 1a' fails without the coefficient bound, Lemma 1a'' fails with any cost allowance B_n >> (log n)^2 | scope: one design sequence, n >= 200, n b_n^2 >= 1200 (sigma*^2 + bbar^2)(log n)^2
depends_on: W3-PSHARP:S@proof:Lemma-V,S(1)
sharpness: A:COEF-REP = FAILED-REMOVAL (evidence: lemmas/C_counterexample.md:100)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14; sol=9.2 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)
```
