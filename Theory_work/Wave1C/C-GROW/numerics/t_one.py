import time, sys, json
import d_common as d
for job in [(2,100,1.0,800,0,True),(5,100,1.0,3200,0,True)]:
    t=time.time(); r=d.run(job)
    print(job, round(time.time()-t,1),'s')
    for k in ['start','n_extra','n_missing','symdiff','extra_same_group','extra_same_block','extra_elsewhere','ell_n_S0_scored','ell_n_final_eq_S0','ell_n_local_limit','unc_tau','tau_minus_symdiff','unc_seq','D1b_log_sum_nb','D1b_max_nb_gap','D1a_LS_F_S0_minus_max','D1a_all_F_S0_minus_max','D1c_frac_S0_second_half','D1c_best_visited_F_minus_FS0','D1c_accept','D1_LS_empty_final_eq_S0','t_start','t_ls','t_total']:
        print('  ',k,r.get(k))
