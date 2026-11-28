# A7 Sol fidelity review: disposition of findings A01-A44

Spec: `Docs/Writing/manuscript/spec/sections/` (file names below are relative to it). Every finding was checked against the
cited code (core at `method-v3.1.1-listpip`; §4.4 against `.rc_tmp/a6/sol_src/{f2,p1m}` and `p1m-freeze-F2`).
All 44 were confirmed, so none is rejected. No numbered algorithm line was added or removed (pins line counts 39/13/20/33/12/14/14/17 unchanged).
Compile: latexmk rc=0, no error, no overfull box, no undefined reference.

| id | verdict | change (file:line) |
|---|---|---|
| A01 | ACCEPTED | label map `col(j)` (retained index to original one-based column) and outputs in original column numbers: sp1_notation.tex:19-22; Alg. 1 header/line 22 and Alg. 8 `\Ensure` (sp4_algorithms.tex:6-7, 22). Symbol is `col`, not kappa (kappa is the SCR eigenvalue floor in sp5). |
| A02 | ACCEPTED | binary64 tie-set restriction (block choices attaining the computed optimum at every prefix): end of `def:startlaw`, sp3_distributions.tex; StartMode line sp4_algorithms.tex:122. |
| A03 | ACCEPTED | grid rule rewritten with v=1 snap at v>=1-1e-12 and the four failure conditions: sp3_distributions.tex:143. |
| A04 | ACCEPTED | neighbour rule: none if p=1, else the largest-|r| neighbour even below threshold, at most B, before symmetrisation: sp3 Table 1 neighbour row; sp4_sampler.tex:16-18 (`def:nbgraph`). |
| A05 | ACCEPTED | coded margin eta(S)=64 eps_mach[nu(y'y/Q_S)(1+|S|c_H)+|S|(c_H+c_A)+|log C_n|+nu|log(2b0+Q_S)|] (c_H, c_A squared max/min diagonal ratios of the factors; 1 for S=empty): sp4_algorithms.tex:284 (ReportExact); sp3 Table 1 margin row. **For Appendix B: the "not transcribed" line is now obsolete.** |
| A06 | ACCEPTED | exact preflight row: mean time of 200 timed scores x count: sp3_distributions.tex:210. |
| A07 | ACCEPTED | allocation not a list, or mem_gb/hours not a single positive finite number, raises an R error: sp4_algorithms.tex:19. |
| A08 | ACCEPTED | wall clock counts from entry to Run: sp4_algorithms.tex:20; Guard line :60. |
| A09 | ACCEPTED | anchored standardisation (if the largest absolute centred scaled entry <= sqrt(eps_mach): subtract first raw entry, divide by largest absolute difference, centre twice): sp4_algorithms.tex:25. **For Appendix B: now transcribed.** |
| A10 | ACCEPTED | duplicate components of G (|r|>=1-1e-10) recorded, reported only: sp4_algorithms.tex:29. |
| A11 | ACCEPTED | stage order Blocks, Tables, table-failure return (best scored table model), StartLaw, Neighbours: sp4_algorithms.tex:35. |
| A12 | ACCEPTED | label `ln:run-frozen` (:37); failure line covers inherited models or lines isl1-ls0, numerical_failure with calibration best model and saved score reconciled with the ledger: sp4_algorithms.tex:44. |
| A13 | ACCEPTED | LS0 Guard measures the duration of StartMode and this search: sp4_algorithms.tex:43. |
| A14 | ACCEPTED | tau_K timing charged only if the start-mode search is on and bytes <= 2^30; kept per model size, reused by later calls: sp4_algorithms.tex:55. |
| A15 | ACCEPTED | Tables use a direct scorer call recording its route (not Eval: no cache, no offer; table models offered to ledgers later): sp4_algorithms.tex:80. |
| A16 | ACCEPTED | Eval retries also on non-finite log m; SSq_S recomputed when below 1e-8 y'y as ||y-X_S b||^2+(||X_S b||^2+||b||^2)/n, b=nH^{-1}z: sp4_algorithms.tex:101. |
| A17 | ACCEPTED | cache emptied by an insertion that finds 500p entries stored; lookups still hit while full: sp4_algorithms.tex:101; sp3_distributions.tex:209. |
| A18 | ACCEPTED | P_k table all zero and never sampled when Phi_k(r)=0; cumulative tables set to 1 from last positive entry on: sp4_algorithms.tex:110. |
| A19 | ACCEPTED | set E built backwards with each step satisfying M_{k-1}(r-u)+mu_k(u)=M_k(r) exactly in binary64; tie-DP fallback as soon as the count reaches 1e6: sp4_algorithms.tex:122. |
| A20 | ACCEPTED | CalTier: a firing Guard or numerical failure in any line ends the tier with that status; partial pilot / diagnostic island ends the tier (before the search / later islands and the search): sp4_algorithms.tex:147, 148 and the diagnostic island line. |
| A21 | ACCEPTED | BuildGrid calls: numerical failure of rescoring ends the tier, firing Guard ends the tier, failed construction sets gridfail; V rescoring outside the score cache with no score event: sp4_algorithms.tex:151, 157, 165. |
| A22 | ACCEPTED | BuildGrid validation reads "not rho(u,v)>=0.90": sp4_algorithms.tex:164-165; sp3_distributions.tex:143. |
| A23 | ACCEPTED | resampler weights c_k = sum exp{log w_l - max log w} accumulated in particle order, test c_k/c_N >= u: sp4_algorithms.tex:190. |
| A24 | ACCEPTED | Gibbs: current state is a held score event; else-branch sets o_j=0 and scores nothing further; ϱ_j gets o_j also when o_j=0: sp4_algorithms.tex:212-213. |
| A25 | ACCEPTED | uniform-swap acceptance evaluated as min{1,exp(lambda'-lambda)}, lambda=log gamma_0(S)+xi*Delta(S) at each endpoint: sp4_algorithms.tex:218-222. |
| A26 | ACCEPTED | neighbour swap draws one uniform u, accepts iff u < probability (also when it is 1): sp4_algorithms.tex:222. |
| A27 | ACCEPTED | LocalSearch Eval(C) emitted and offered only in LS0, not in the final search or calibration searches: sp4_algorithms.tex:238. |
| A28 | ACCEPTED | Report list: R error if model and score counts differ, a model repeats, or a stored column is not retained; otherwise flags name the reason; size, full flag and source reported: sp4_algorithms.tex:278. |
| A29 | ACCEPTED | E1 (island bests vs F(Shat), including LS0), E2 (sd of island log Zhat_r), E3 (strict rise during LS1, measured before LS0): sp4_algorithms.tex:279. |
| A30 | ACCEPTED | island definition covers the adaptive (pilot) schedule and fixed grids (diagnostic, final): sp4_sampler.tex:11. |
| A31 | ACCEPTED | three stores in calibration and final sampler; enumeration keeps only the 40p+1 store: sp4_sampler.tex:50-51. |
| A32 | ACCEPTED | error list adds allocation, base move cap above 1e6, and l_n+|S0| above 2^31-1: sp4_sampler.tex:68. |
| A33 | ACCEPTED | Shat certified only if the run completed, Shat is the LS1/LS0 return and the last scan found no strict improvement; a stopped run is not certified: sp4_sampler.tex:45, 75-77. |
| A34 | ACCEPTED | reports log Z_T (field log_Z_list); exact run uses the 40p+1 store: sp4_sampler.tex:104-112. |
| A35 | ACCEPTED | §4.4 islands/merge: union with table and inherited models under the capped 40p+1 rule; LS1 from merged best, LS0 from start mode; island ledgers start empty: sp4_sampler.tex:127. |
| A36 | ACCEPTED | §4.4 particles: N a setting (2,500 default); 1e5 main rung N=1e4, twins 2,500; 1M runs 2,500 plus one planned N=1e4 comparison fit: sp4_sampler.tex:130-131. |
| A37 | ACCEPTED | §4.4 calibration: H=512 whatever final N; I_max a setting (driver default 3, campaign value 0), I_max <= l_n; m defaults to 1; fallback last successful grid else pilot schedule: sp4_sampler.tex:132. |
| A38 | ACCEPTED | §4.4 blocks: merge height fl(1-|r|) <= fl(1-tau), tau=sqrt(2 log p/n); top-down cut, next-fit by minimum index, at most min(B,14) per block: sp4_sampler.tex:138. |
| A39 | ACCEPTED | §4.4 scoring: o_j truncated to floor(2^63 o_j), summed exactly in 128 bits, converted to double times 2^-63, divided by 4N: sp4_sampler.tex:142. |
| A40 | ACCEPTED | §4.4 stores: no score cache; calibration keeps both 20p stores for V and inherited models; final islands and merge ledger keep none: sp4_sampler.tex:144-145. |
| A41 | ACCEPTED | offers below tau_cal dropped, equal offers kept; tau_cal = (40p+1)-st largest F among distinct inherited models, else -inf: sp4_sampler.tex:145-146. |
| A42 | ACCEPTED | log Z_T as log-sum-exp of stored F; stored F offered by the Gibbs scan is a batched-kernel score that a later canonical re-score does not replace: sp4_sampler.tex (§4.4 extra outputs). |
| A43 | ACCEPTED | evidence-weighted and store-renormalised PIPs beside equal-weight ones; optional predictive law: sp4_sampler.tex (§4.4 extra outputs). |
| A44 | ACCEPTED | occupancy evidence estimate only if every island supplies terminal supports (deferred, not a default output): sp4_sampler.tex (§4.4 extra outputs). |

Counts: **44 ACCEPTED, 0 REJECTED.** (Line numbers are for the edited files as of this run; sp4_sampler.tex lines for A42-A44 are the last bullets of §4.4.)

Pins: `a7_notes/S1_pins.md` updated (27 pin cells, plus a "Changes after the Sol fidelity review (A01-A44)" section).
Backups and scripts: `.rc_tmp/a7/` (sp3.bak, sp4alg.bak, sp4samp.bak, pins.bak, edit_*.py).

## Items for Appendix B (manager)
1. A05: the margin eta(S) is now transcribed in Algorithm 8 `ReportExact`; Appendix B's "not transcribed" statement must be removed or updated.
2. A09: the anchored standardisation is now transcribed (Algorithm 1 standardise line).
3. A01: the label map is written `\mathrm{col}(j)`, not kappa (kappa is already the SCR eigenvalue floor in sp5_assumptions.tex).
