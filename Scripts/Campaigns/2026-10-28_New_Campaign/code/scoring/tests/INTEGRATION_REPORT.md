# Integration check: one real p = 20 fit

```
dataset p0020_S1_r001 c100: n=200 p=20 truth=3;7;14;16 method_seed=5220001
v3_fit status completed in 2 s; branch smc; names(fit) include pip_plain: TRUE; instrumentation: stages,best_before_local,best_after_local,stop,escalation,cut_group_large,cut_group_large_any,version,scored,scored_set
extract_smc: ok=TRUE log_Z=-85.087 islands=-85.087,-85.089,-85.088,-85.084 hpm=3;7;14;16 mpm=3;7;14;16 mpm_plain=3;7;14;16
registry: log_mass_scored=-85.0833 n_distinct=6464 scored_set rows=6464 score_fresh=5935 stages_final=1 min_ess=2333.5 tier=0
flags: escalated=FALSE checks_passed_final=TRUE E1/E2/E3=FALSE/FALSE/FALSE low_ess=FALSE cut_group=TRUE local_limit=FALSE grid_unconverged=FALSE
lowp_exact: 15 s; names of the per-scale list: status,scope,log_Z,log_m0,log_Z_rel_m0,pip,hpm,hpm_F,hpm_size,hpm_eta,hpm_eta_kind,second_F,margin,certificate_bound,certificate_bound_kind,global_certified,certified_over_scored_models,mpm,size_logmass,size_logjoint,top,numerics
lowp_exact run status: exact; complete: TRUE
accuracy row: e=-0.0037 relative error=-0.0037 lb_cover=TRUE se=0.0013 hpm_eq_exact=TRUE exact_hpm_eq_truth=TRUE F_gap=0 hpm_F_mismatch=0 truth_mass=0.7681
PIP errors RB: max=1.41e-05 mean=4.54e-06 true=0 null=5.68e-06; plain: max=0.00186 mean=0.000442; MPM RB = exact: TRUE; plain = exact: TRUE
scored coverage = exp(log_mass_scored - log Z) = 0.999973 (log -2.655e-05); must be <= 1: TRUE
exact vs scorer: log_Z (enumerator) = -85.0832841355; exact HPM F = -85.347164042 vs scorer F(exact HPM) = -85.347164042; SMC native hpm_F vs scorer: 0
theory: pi0(S0)=0.7382 pi0(R0)=0.7394 pi0(R1)=0.9591 pi0(R2)=0.9953; blocks_match (record vs recomputed)=TRUE; truth_scored=TRUE first phase/mech=pilot/init_draw; miss_class=hit
TD d=1 (enum), literal: clause-a centres 255, violating 240, clause b 0/16, total 240, min margin -5.5884, violators beaten by a truth-in swap 240; toward: violations 0, min margin 3.0716, holds_strict TRUE; scores 19072
TD d=2 (enum), literal: clause-a centres 2055, violating 2040, clause b 0/136, total 2040, min margin -5.5884, violators beaten by a truth-in swap 2040; toward: violations 0, min margin 2.6811, holds_strict TRUE; scores 180352
R stand-in td_slow, same dataset, d=1: literal violating clause a 240 of 255, min margin -5.5884; toward violations 0, min margin 3.0716; truth-in-swap violators 240
Reference (enumerator worker, VALIDATION.md, same dataset): d=1 literal 240 violating clause-a centres of 255, min margin -5.5884; d=2 2040 of 2055; toward 0 violations, min margins 10.7527 / 3.0716 / 3.0716 (d=1).
ASSERTIONS PASSED: SMC record valid; kept maps agree; coverage in (0,1]; blocks equal; native hpm_F = scorer F; lower-bound identity; TD literal 240/255 and 2040/2055 (all beaten by a truth-in swap), toward 0 violations
ad hoc dataset (earlier report), d=1: literal violating clause a 180 of 255, all clauses 180, min margin -5.5799
ad hoc dataset (earlier report), d=2: literal violating clause a 1885 of 2055, all clauses 1885, min margin -5.5799
```
