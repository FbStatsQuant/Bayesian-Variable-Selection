# S1 pins: code location of every printed algorithm line

Generated from the `%@` comments in `S1_algorithms.tex` by a script that counts the numbered lines (`\Procedure`, `\State`, `\If`, `\Else`, `\For`, `\While`; `\Require`, `\Ensure` and the `\End...` lines are not numbered). The per-algorithm line counts were checked against the compiled PDF: **39, 13, 20, 33, 12, 14, 14, 17** (all agree). Paths are relative to `Scripts/SMC_BVS/core/` (`.R` files here, `cpp/` for `.h` and `.cpp`: `v3_engine.h`, `v3_calib.h`, `v3_blocks.h`, `v3_start.h`, `v3_ledger.h`, `v3_runtime.h`, `v3_score.h`, `v3_util.h`, `v3_core.cpp`). Structural lines (procedure headers, loops, `else`) have no `%@` comment in the `.tex`; their pins are given here only. Cross-references to lines inside Algorithm 1 use `\label`/`\ref`, so they follow the numbering.

Algorithm numbers are the order of appearance: 1 Run (with Check, Guard); 2 Blocks, Tables, Neighbours; 3 Eval, StartLaw, DrawStart, StartMode; 4 Calibration (Calibrate, CalTier, BuildGrid, NextTemperature); 5 Island; 6 Markov moves; 7 Local search (with TwoSearches); 8 Outputs (Better, Offer, Report, ReportExact).


## Algorithm 1: \textsc{Run}: a complete run (stage~1, and the order and the statuses of stages 2--7).

| line | text (start) | code pin |
|---|---|---|
| 1 | Run | v3_fit.R:71-176 (top-level function; order of stages 133-176) |
| 2 | if s is not a single integer in [1,2^31-1] then return status texttti | v3_fit.R:88-89; v3_preprocess.R:7-11 |
| 3 | if the allocation is not two positive finite numbers then raise an R | v3_fit.R:91-94 |
| 4 | start the wall clock that every Guard call below reads | v3_fit.R:74,96; v3_runtime.h:13-20 |
| 5 | if Xr is not a numeric matrix, yr not a numeric vector, absyrne n, an | v3_preprocess.R:99-107; v3_fit.R:99-103 |
| 6 | drop every column whose entries are all exactly equal; kappa:= the re | v3_preprocess.R:111-112 |
| 7 | if p=0 then return status textttno_predictors, Shat=emptyset, no esti | v3_preprocess.R:114; v3_fit.R:99-102 |
| 8 | if all yr_i are exactly equal then return status texttty_constant, Sh | v3_preprocess.R:115; v3_fit.R:99-102 |
| 9 | standardise each retained column and yr (divide by the largest absolu | v3_preprocess.R:37-68,118-123 |
| 10 | Kgetsmin(p,lfloor n/2rfloor); Bgetsmin(lfloorsqrt nrfloor,lfloorsqrt | v3_preprocess.R:19-33 (K 21, B 22, ell 23, L 24, N0 25, H0 26, T0 27, tiers 30) |
| 11 | absOmgetssum_k=0^Kbinom pk (exact integers, stopped once above the th | v3_core.cpp:72-85; v3_preprocess.R:28; v3_fit.R:105-106 |
| 12 | if Check(exact or sampler, tier~0) then return status textttresource_ | v3_fit.R:115-117 |
| 13 | build the data context: G=X^top X, z=X^top y, y^top y, log m(emptyset | v3_fit.R:118; v3_score.h:39-72; v3_core.cpp:91-106 |
| 14 | exact | v3_fit.R:120 (exact branch); v3_core.cpp:524-559 |
| 15 | visit every SinOm in depth-first order (the empty model, then each mo | v3_core.cpp:524-559; v3_exact.R:6-19 |
| 16 | if a scoring fails numerically (Cholesky, Cholesky from a recomputed | v3_core.cpp:556; v3_score.h:227-238; v3_fit.R:125-131 |
| 17 | status gets textttexact; return ReportExact (Algorithm~refalg:outputs | v3_fit.R:120-131 |
| 18 | (stages~2--3) Blocks, Tables, Neighbours (Algorithm~refalg:blocks); S | v3_fit.R:133-140; v3_core.cpp:272-318 |
| 19 | (stage~4) (textstatus_c,textfrozen)gets Calibrate (Algorithm~refalg:c | v3_fit.R:149-160 |
| 20 | frozen =(0=grid0<dots<gridTs=1, i, N_i, Lbi, textthe models of the th | v3_fit.R:161-162; v3_run.R:88-104,225-231; v3_core.cpp:407-442 |
| 21 | r=1,dots,4 | v3_core.cpp:443-451 (final islands, streams 10-13) |
| 22 | (Zhat_r,PIPhat_r,cdot)gets Island(r,N_i,gridcdot,Lbi) on random strea | v3_core.cpp:443-446 |
| 23 | if Guard fired inside the island then status gets textttresource_limi | v3_core.cpp:451; v3_engine.h:335-338 |
| 24 | if status = completed then LS_1gets LocalSearch(the best model scored | v3_core.cpp:453-459 |
| 25 | if status = completed then tSzgets StartMode; if ell_n+abstSz>2^31-1 | v3_core.cpp:465-481 |
| 26 | if a scoring failed numerically in lines~refln:run-isl1--refln:run-ls | v3_core.cpp:483-484 |
| 27 | if status ne completed then return status, Shat:= the best model scor | v3_run.R:143-148; v3_fit.R:84-85 |
| 28 | status gets textttcompleted; return Report (Algorithm~refalg:outputs) | v3_run.R:150-221; v3_fit.R:171-176 |
| 29 | Checkbranch, iCommenttrue iff the allocation is exceeded | v3_fit.R:10-68 (resource estimate) |
| 30 | branch is exact | v3_fit.R:26-34 (exact branch of the estimate) |
| 31 | k^*getsmin(K,lceil p/2rceil); bytes gets8(3np+p^2)+8(40p+1)(k^*+8)+32 | v3_fit.R:10-14,31-34 |
| 32 | return [bytes >g,2^30 or seconds >3600h] | v3_fit.R:60 |
| 33 |  | v3_fit.R:36-47 (sampler branch of the estimate) |
| 34 | Ngets N_i, Wgetslceil p/64rceil, Cgets500p; bytes gets8(3np+3p^2)+16l | v3_fit.R:36-41 |
| 35 | if the search from the start mode is on (default): sigmagetsell_n+K+1 | v3_fit.R:43-45,113-115 |
| 36 | exceeded gets [bytes >g,2^30]; if bytes le g,2^30 then tau_Kgets mean | v3_fit.R:47,60,65 |
| 37 | return exceeded | v3_fit.R:67 |
| 38 | GuarddeltaCommentcalled after every bridge stage, grid construction an | v3_runtime.h:21-27 |
| 39 | if (time elapsed since line~refln:run-clock of Run) + delta>3600h the | v3_runtime.h:21-27; call sites v3_engine.h:335, v3_core.cpp:459,480,645,692, v3_calib.R:354-355 |

## Algorithm 2: Stage~2: blocks, block tables and the neighbour graph.

| line | text (start) | code pin |
|---|---|---|
| 1 | Blocks | v3_blocks.h:46-141 |
| 2 | hat r_jlgets G_jl/sqrtG_jjG_ll; d_jlgets1-abshat r_jl | v3_blocks.h:10-17,55 |
| 3 | complete-linkage tree: start from p singleton clusters; p-1 times mer | v3_blocks.h:46-108 (pair order 62-66, choice 76-83, left child 85-86, max rule 94-98) |
| 4 | cut top-down: stack gets root; while the stack is not empty pop a nod | v3_blocks.h:128-132 |
| 5 | pack next-fit in emission order: curgetsemptyset; for each cluster c: | v3_blocks.h:134-141; v3_core.cpp:145-149 |
| 6 | Tables | v3_core.cpp:282-298; v3_start.h:76-98 |
| 7 | kinset J and every Usubseteq C_k with abs Ule K (coded by the bits of | v3_start.h:76-98; v3_core.cpp:282-298 |
| 8 | log h_k(U)getslog m(U)-log m(emptyset), with h_k(emptyset)=1, log m(U | v3_start.h:76-98 (score 93, entry 95); v3_core.cpp:282-298 |
| 9 | Neighbours | v3_blocks.h:152-171 |
| 10 | if p=1 then mathcal N(1)getsemptyset and stop; rho_ngetssqrt2log p/n | v3_blocks.h:152,154 |
| 11 | jinset p | v3_blocks.h:157-168 |
| 12 | order the lne j by abshat r_jl decreasing, ties by smaller l; a_jgets | v3_blocks.h:157-168 |
| 13 | mathcal N(j)getsl: linch_j textor jinch_l, increasing (a symmetric gr | v3_blocks.h:170-171 |

## Algorithm 3: Stage~3: model evaluation, the start law $\pi_0$ with its exact sampler, and the start mode $\tSz$.

| line | text (start) | code pin |
|---|---|---|
| 1 | EvalSCommentthe score of a model abs Sle K; used by every algorithm | v3_engine.h:89-100; v3_start.h:54-69 |
| 2 | log m(S)gets the cached value if present, else the scorer (Cholesky o | v3_engine.h:89-96; v3_score.h:176-187,227-238; v3_core.cpp:409 |
| 3 | cgetssum_klog h_k(Scap C_k) over the blocks that S meets | v3_start.h:54-66 |
| 4 | loggamma_0(S)getslogvarpi(abs S)+c;  Delta(S)getslog m(S)-log m(empty | v3_engine.h:97; v3_start.h:69 |
| 5 | Offer(S) (Algorithm~refalg:outputs) if the score was computed afresh | v3_engine.h:98-100; v3_ledger.h:104-113 |
| 6 | StartLaw | v3_start.h:106-150 |
| 7 | e_k(a)getssum_Usubseteq C_k, abs U=ah_k(U) for kinset J, a=0,dots,min | v3_start.h:106-120 |
| 8 | Phi_0(0)gets1, Phi_0(a)gets0 for a>0; for kinset J, a=0,dots,K: Phi_k | v3_start.h:121-131 |
| 9 | bar Z_0getssum_a=0^Kvarpi(a),Phi_J(a);  q(a)getsvarpi(a)Phi_J(a)/bar | v3_start.h:132-138 |
| 10 | for kinset J, r=0,dots,K, ulemin(absC_k,r): P_k(umid r)gets e_k(u),Ph | v3_start.h:139-150 |
| 11 | DrawStartCommentone exact draw from pi_0; the uniforms are used in thi | v3_start.h:155-175 |
| 12 | draw asim q (inverse CDF: the smallest index whose cumulative probabi | v3_start.h:160; v3_start.h:18-20 |
| 13 | rgets a; for k=J,J-1,dots,1 while r>0 do draw a_ksim P_k(cdotmid r) a | v3_start.h:161-166 |
| 14 | for k=1,dots,J with a_k>0 do draw U_ksubseteq C_k, absU_k=a_k, with p | v3_start.h:168-173 |
| 15 | return S=bigcup_kU_k | v3_start.h:174-175 |
| 16 | StartMode | v3_start.h:201-305 |
| 17 | mu_k(a)getsmax_Usubseteq C_k,abs U=alog h_k(U);  A_k(a):= the set of | v3_start.h:201-210 |
| 18 | M_0(0)gets0;  M_k(a)getsmax_ulemin(absC_k,a)M_k-1(a-u)+mu_k(u) (nothi | v3_start.h:211-219 |
| 19 | a^*gets the smallest a attaining max_alogvarpi(a)+M_J(a) (a strict co | v3_start.h:220-224 |
| 20 | mathcal Egets the sets of size a^* whose block choices (a_k,U_kin A_k | v3_start.h:271-305 (enumeration 281-301, tie DP 237-270, used 303) |

## Algorithm 4: Stage~4: calibration (adaptive tempering): pilot, grid, rebuilds, tier rule, fallback, freeze.

| line | text (start) | code pin |
|---|---|---|
| 1 | Calibrate | v3_calib.R:144-190; v3_core.cpp:603-740 |
| 2 | persistent state: a ledger (best model, mathcal T the 40p+1 best by F | v3_calib.R:147-148; v3_core.cpp:603-614, (ingest_tables 372-388) |
| 3 | igets0 | v3_calib.R:144 (argument tier = 0) |
| 4 | true | v3_calib.R:150-159 |
| 5 | (textst,textgrid,texttrig,textfb)gets CalTier(i); if st ne ok then re | v3_calib.R:151-153 |
| 6 | if no trigger of trig is true or i=1 then leave the loop (at tier~1 t | v3_calib.R:154-155 |
| 7 | if Check(sampler, tier~1) then return textttresource_limit (the escal | v3_calib.R:157; v3_fit.R:144-148 |
| 8 | igets1 (stores, cache and the score ledger carry over; the temperatur | v3_calib.R:158; v3_core.cpp:626,667 |
| 9 | if grid =emptyset and i=1 then grid gets fb (valid fallback) | v3_calib.R:163-169 |
| 10 | if grid =emptyset then return textttschedule_limit (for i=0 the code | v3_calib.R:170 |
| 11 | freeze: grid, tier i, N_i, Lbi, and the models of mathcal Tcupmathcal | v3_calib.R:160,184-190; v3_core.cpp:728-740 |
| 12 | CalTieri | v3_calib.R:44-126 |
| 13 | (Xi,textforced)gets Island(0,Nc_i,textadaptive,Lbi) on stream 0 if i= | v3_calib.R:44; v3_core.cpp:626-636 |
| 14 | LSgets LocalSearch(best scored model, ell_n); Guard; E_3gets[F(textbe | v3_core.cpp:640-648; v3_calib.R:25,59-60 |
| 15 | trig getsE_1=textfalse,E_2=textfalse,E_3, textforced>0, textgridfail= | v3_calib.R:60-61 |
| 16 | grid gets BuildGrid(Xi); Guard; if the construction failed then trig. | v3_calib.R:79-82,362 |
| 17 | the construction succeeded | v3_calib.R:79-82,84 |
| 18 | iota=1,dots,ell_n | v3_calib.R:84-119; v3_core.cpp:657-692 |
| 19 | for r=1,dots,4: (Zhat_r,cdot)gets Island(r,Nc_i,textgrid,Lbi) on stre | v3_core.cpp:657-686; v3_calib.R:86 |
| 20 | LSgets LocalSearch(best scored model, ell_n); Guard; E_3,iotagets[F(t | v3_core.cpp:687-692; v3_calib.R:103 |
| 21 | E_1gets[exists r: b_r<F(textbest)-1];  E_2gets[sd(logZhat_1,dots,logZ | v3_calib.R:101-102,109-110 |
| 22 | grid'gets BuildGrid(Xi) (the sets mathcal L_0,mathcal L_1 have been u | v3_calib.R:111-114 |
| 23 | if grid' has exactly the same temperatures as grid then grid gets gri | v3_calib.R:115-116 |
| 24 | if not trig.gridfail and not converged then trig.unconverged gets tru | v3_calib.R:118 |
| 25 | if trig.gridfail and i=1 then fb gets the last grid built successfull | v3_calib.R:120-126 |
| 26 | BuildGridXi | v3_calib.h:49-95; v3_core.cpp:699-724 |
| 27 | mathcal Vgetsemptysetcupmathcal L_0cupmathcal L_1, in lexicographic o | v3_core.cpp:703-724; v3_calib.h:49-58; v3_calib.R:64-66 |
| 28 | gridgets(0); ugets0; while u<1: bgets the smallest element of Xi abov | v3_calib.h:70-76 |
| 29 | if rho(u,b)ge0.90 then vgets b; else logets u, higets b, any gets fal | v3_calib.h:78-88 |
| 30 | if vge1-10^-12 then vgets1; if not v>u or rho(u,v)<0.90 then fail; ap | v3_calib.h:89-95 |
| 31 | NextTemperaturexi; Delta_1,dots,Delta_NCommentthe pilot's rule; N=Nc_i | v3_calib.h:19-45 |
| 32 | if ESS(1-xi)ge0.90N then return 1; else logetsxi, higets1, and 60 tim | v3_calib.h:19-23,30-37 |
| 33 | if lo-xi<1/Tmax_i then fgetsmin(1,xi+1/Tmax_i); if fge1-10^-12 then f | v3_calib.h:38-45 |

## Algorithm 5: Stage~5: one island (the final run, a diagnostic island or the pilot), the PIP estimator $\PIPhat_{r,j}$ and the evidence estimator $\Zhat_r$.

| line | text (start) | code pin |
|---|---|---|
| 1 | Islandr,N,textschedule,Lbi | v3_engine.h:283-367 |
| 2 | for v=1,dots,N: S_vgets DrawStart; Eval(S_v) (the N draws are indepen | v3_engine.h:283-292 |
| 3 | logZhat_rgetslog m(emptyset)+logbar Z_0;  xigets0;  tgets0 | v3_engine.h:299-302 |
| 4 | true | v3_engine.h:303-338 |
| 5 | if the schedule is the grid: stop when t=Ts, else xi'getsgridt+1; if | v3_engine.h:303-315 |
| 6 | omega_vgetsexp(xi'-xi),Delta(S_v) for v=1,dots,N;  logZhat_rgetslogZh | v3_engine.h:316-322 |
| 7 | multinomial resampling: draw N uniforms u_1,dots,u_N first; a_vgets t | v3_engine.h:234-259,324-327 |
| 8 | for v=1,dots,N in order: Round(S_v,xi') (Algorithm~refalg:moves);  xi | v3_engine.h:330-334; v3_engine.h:215-218 |
| 9 | if Guard(the duration of this stage) fires then the island is partial | v3_engine.h:335-338 |
| 10 | Tsgets t; for l=1,dots,Lbi: for v=1,dots,N: Round(S_v,1) (burn-in, no | v3_engine.h:340-347 |
| 11 | varrho_jgets0 for jinset p; for h=1,dots,4: for v=1,dots,N in order: | v3_engine.h:349-360,128 |
| 12 | PIPhat_r,jgetsvarrho_j/(4N) for jinset p;  Zhat_rgets m(emptyset),bar | v3_engine.h:363-367; v3_run.R:150-162 (stored as log\_Z, pip) |

## Algorithm 6: The Markov moves: one round, and the four kinds of move with their acceptance probabilities.

| line | text (start) | code pin |
|---|---|---|
| 1 | RoundS,xi | v3_engine.h:195-214 |
| 2 | draw a uniformly random order of the m labels G_1,dots,G_p,U,N_1,dots | v3_engine.h:195-214 |
| 3 | GibbsS,j,xiCommentinclusion update of predictor j | v3_engine.h:111-131 |
| 4 | if jin S then S^+gets S, S^-gets Ssetminusj; else if abs S<K then S^+ | v3_engine.h:115-127 |
| 5 | agetsgamma_xi(S^+)/gamma_xi(S^-) and o_jgets a/(1+a) (evaluated as a | v3_engine.h:122-128; v3_util.h:30-34 |
| 6 | draw u (one uniform, also when o_jin0,1); include j iff u<o_j; Sgets | v3_engine.h:129-131 |
| 7 | UniformSwapS,xi | v3_engine.h:148-158 |
| 8 | if abs Sin0,p then do nothing (no uniform used) | v3_engine.h:148 |
| 9 | jgets a member of S, lgets a non-member, each uniform (lfloor ukrfloo | v3_engine.h:150-158 |
| 10 | NeighbourSwapS,xi | v3_engine.h:164-179 |
| 11 | if S=emptyset then do nothing; jgets a uniform member of S; mathcal C | v3_engine.h:164-170 |
| 12 | lgets uniform in mathcal C (increasing list); S'gets(Ssetminusj)cupl; | v3_engine.h:171-179 |
| 13 | IndependenceS,xi | v3_engine.h:182-191 |
| 14 | S'gets DrawStart (an exact draw from pi_0; always scored); accept wit | v3_engine.h:182-191 |

## Algorithm 7: Stage~6: the local search, certification, and the two searches of a run.

| line | text (start) | code pin |
|---|---|---|
| 1 | LocalSearchC_0,cap | v3_engine.h:380-415 |
| 2 | Cgets C_0; Eval(C); mvgets0 | v3_engine.h:382-383 |
| 3 | true | v3_engine.h:386-415 |
| 4 | bestgets none; for every Q below, Eval(Q) and: if best is none or F(Q | v3_engine.h:387-393 |
| 5 | for j=1,dots,p in order: Qgets Csetminusj if jin C; Qgets Ccupj if jn | v3_engine.h:394-399 |
| 6 | for jin C increasing, for lnotin C increasing: Qgets(Csetminusj)cupl | v3_engine.h:400-406 |
| 7 | best is not none and F(best)>F(C)Commenta strict improvement; an equal | v3_engine.h:408-412 |
| 8 | if mvgecap then return (best, certified = false, limit = true) (the e | v3_engine.h:408-411 |
| 9 | Cgetsbest; mvgetsmv+1 | v3_engine.h:412 |
| 10 |  | v3_engine.h:413-415 |
| 11 | return (C, certified = true, limit = false) (no strictly better neigh | v3_engine.h:413-415 |
| 12 | TwoSearchesCommentafter the islands; lines~refln:run-ls1--refln:run-ls | v3_core.cpp:453-481 |
| 13 | LS_1gets LocalSearch(the model with the best F scored so far under Be | v3_core.cpp:454-459; v3_run.R:91 (ell) |
| 14 | tSzgets StartMode (Algorithm~refalg:start);  LS_0gets LocalSearch(tSz | v3_core.cpp:465-481 (mode 469, cap 473-475); v3_run.R:98-101 |

## Algorithm 8: Stage~7: the ledger, the reported model, pooling, the certification flag, the list $\mathcal T$ and the list-renormalised fields.

| line | text (start) | code pin |
|---|---|---|
| 1 | BetterS,F,S',F'CommentS before S' in the reported-model order | v3_util.h:117-126 |
| 2 | return F>F' or [F=F' and (abs S<absS' or (abs S=absS' and S precedes | v3_util.h:117-126 |
| 3 | OfferSCommentcalled by Eval on a fresh score; the stores are sets, so | v3_ledger.h:84-94 |
| 4 | best model gets S if Better(S,F(S),textbest,F(textbest)) | v3_ledger.h:84-88 |
| 5 | mathcal Tgets the 40p+1 models with the largest F (ties: smaller size | v3_ledger.h:35-64,72,76-80,89-94 |
| 6 | ReportCommentstatus completed | v3_run.R:119-222 |
| 7 | Shatgets the best model of the ledger (the best F over every model sc | v3_run.R:142; v3_ledger.h:84-88 |
| 8 | logZhatgetslogsum_r=1^4Zhat_r-log4 (log-sum-exp); lower bound log(0.0 | v3_run.R:150-157 |
| 9 | PIPhat_jgetsfrac14sum_r=1^4PIPhat_r,j (equal weights);  MPMhatgetsj:P | v3_run.R:159-163 |
| 10 | cert_1gets[LS_1 certified wedge Shat= its returned model];  cert_0get | v3_run.R:178-179,185-197 |
| 11 | mathcal Tgets the store mathcal T with its log scores F (absmathcal T | v3_run.R:210; v3_ledger.h:72,78 |
| 12 | list-renormalised fields: F_maxgetsmax_Sinmathcal TF(S); u_SgetsexpF( | v3_run.R:176,245-268 |
| 13 | diagnostics, reported only (never change an output): E_1,E_2,E_3 on t | v3_run.R:169-209 |
| 14 | return Shat,PIPhat,MPMhat,logZhat,log(0.05Zhat), certified, mathcal T | v3_run.R:119-222; v3_fit.R:176 |
| 15 | ReportExactCommentstatus exact (every SinOm was scored) | v3_fit.R:120-131; v3_core.cpp:524-567 |
| 16 | Shatgets the best model under Better (the highest posterior model); l | v3_core.cpp:557-559; v3_exact.R:13-15; v3_fit.R:125-127 |
| 17 | certified gets true; the global-certificate flag gets[F(Shat)-eta(Sha | v3_fit.R:128-129,131; v3_run.R:271-279; v3_core.cpp:560-567; v3_score.h:241-243 |

## A6 prose vs code differences

Both sides are pinned; the sampler follows the code. Most are omissions in the A6 prose; none contradicts a formula or constant that A6 states (every constant of Appendix "All constants" that I compared agrees with the code).

1. **Exact run: extra outputs.** A6 (`or4_sampler.tex:155-156`; `appendices_or.tex` constants table) lists for an exact run $\hat S$, every PIP, the MPM and $\log Z$. The code also returns the lower bound $\log(0.05)+\log Z$ (`v3_fit.R:125-127`) and the global-certificate flag from the heuristic margin (`v3_fit.R:128-129`; `cpp/v3_score.h:241-243`; `cpp/v3_core.cpp:560-567`). The margin appears in A6's constants table; the exact-run lower bound does not appear anywhere.
2. **A fourth way for the grid construction to fail.** A6 lists three (no numerical progress; an appended temperature fails the 0.90 check; more than $\Tmax_i$ steps). The code also fails when no pilot temperature lies above $u$ (`cpp/v3_calib.h:70-76`). I could not construct an input that reaches it.
3. **Where the start mode is computed.** A6 lists the start-mode enumeration among the blocks-and-start constants (`appendices_or.tex`, constants table, pinned to `cpp/v3_start.h:271-305`) and uses $\tSz$ only in stage 6; the code computes it only after the islands, inside the final run, from the same block tables (`cpp/v3_core.cpp:465-481`). The value is the same.
4. **Exact runs and the list-renormalised fields.** A6 (`or4_sampler.tex:183`) describes the list-renormalised $\mathrm{pip}_{\mathcal T}$, median model and $\log Z_{\mathcal T}$ for completed runs. For an exact run the code sets the first two to the exact PIP and MPM and computes $\log Z_{\mathcal T}$ from the $40p+1$ best models (`v3_run.R:271-279`; `v3_fit.R:128-131`).
5. **Where the resource guard is called.** The appendix says the elapsed time plus the last operation is checked "after every step, grid construction and local search". In the code the guard runs after each bridge stage of an island (`cpp/v3_engine.h:335-338`), after each grid construction (`v3_calib.R:354-355`) and after each local search (`cpp/v3_core.cpp:459,480,645,692`); it does not run after burn-in or measured rounds.
6. **Stage 1 wording.** A6 (`or4_sampler.tex:79`): "Invalid inputs stop the run with no model". In the code a bad seed, a non-numeric or non-finite $X$ or $y$, a length mismatch, $n<3$ or $p_{\mathrm{raw}}<1$ all give status `invalid_input` (`v3_fit.R:88-89,99-103`; `v3_preprocess.R:7-11,99-107`), but an invalid allocation raises an R error (`v3_fit.R:91-94`; the appendix, "Runs without estimates", states this; the main-text sentence does not). The conditions $n<3$ and $p_{\mathrm{raw}}<1$ are stated nowhere in A6.
7. **Statuses.** A6 names three endings (exact, completed, stopped, `or4_sampler.tex:149-152`). The code's statuses are `exact`, `completed`, `invalid_input`, `no_predictors`, `y_constant`, `resource_limit`, `numerical_failure` and `schedule_limit` (`v3_fit.R:84-85,115-160`; `v3_calib.R:170`, where the no-grid case at tier 0 is named `grid_failure_no_escalation`). `numerical_failure` can arise in the exact branch (`v3_fit.R:125-131`), in the block tables (`v3_fit.R:133-140`) and in the calibration or final run (`cpp/v3_core.cpp:483-484`); A6 says only that the run stops without estimates when "all three score computations fail".
8. **Random numbers used by no-op moves.** A6 says a move that cannot be made "does nothing". In the code a Gibbs update always draws its uniform, an independence move always draws its uniform and draw from $\pi_0$, while a uniform swap on $\abs S\in\{0,p\}$ and a neighbour swap with no candidate draw nothing further (`cpp/v3_engine.h:129-131,148,164-170,182-191`). This matters only for reproducing streams exactly.

## Could not determine

* **Exact stream seeding.** Algorithm 4 line 2 says stream $j$ is seeded by $(s,j)$. I read the stream numbers (`v3_run.R:8-11`; `cpp/v3_core.cpp:444,626,667`) but did not trace the seeding function itself, so the way $s$ and $j$ combine is not transcribed.
* **The rounding margin $\eta$.** Algorithm 8, `ReportExact`, says "heuristic rounding bound" without its formula: `cpp/v3_score.h:241-243` was read only in part (A6: 64 machine epsilons times a conditioning factor).
* **Parts of files read only partly:** `cpp/v3_score.h`, `cpp/v3_util.h` and `cpp/v3_core.cpp` lines 330-399; pins into them rest on the parts read. I did not check that the statement in Algorithm 4 (`Calibrate`, the `schedule_limit` line) that the no-grid case at $i=0$ (`grid_failure_no_escalation`) is unreachable; this is argued from the trigger list (a failed grid is a trigger at tier 0).
* **The anchored standardisation** (Algorithm 1 line 9, `v3_preprocess.R:37-68`) is summarised in words; its exact formula was not transcribed.
* **Cache clearing and memory-estimate constants** (Algorithm 1, `Check`: the factors $29$, $80p+1$, $4096$, etc.) are copied from `v3_fit.R:36-47`; I did not test them numerically.
