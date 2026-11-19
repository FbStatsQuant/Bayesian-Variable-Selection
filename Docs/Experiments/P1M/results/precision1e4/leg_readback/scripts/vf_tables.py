import csv, json, math, sys
def rd(p): return list(csv.DictReader(open(p)))
vf = {(r['dataset'], r['seed']): r for r in rd('out/vf_pairs/wave_check.csv')}
v3 = {(r['dataset'], r['seed']): r for r in rd('out/v3_pairs/wave_check.csv')}
keys = sorted(k for k, r in vf.items() if r['V_delivered']=='True')
def f(x, nd=4):
    try: return ('%.'+str(nd)+'g') % float(x)
    except: return x
print("pair | HPMeq VF/V3 | MPMeq | T>F | dlogZ VF (se) | dlogZ V3 (se) | pip ratio VF/V3 | dH_T | dH_V* VF/V3 | triangle VF/V3 | dH_VT V3 | coreh VF/V3 | tierT")
for k in keys:
    a, b = vf[k], v3[k]
    print(' | '.join([k[0].replace('4-','').replace('-n200','')+' s'+k[1], a['hpm_equal']+'/'+b['hpm_equal'], a['mpm_equal']+'/'+b['mpm_equal'], a['T_higher_F']+'/'+b['T_higher_F'],
        '%+.5f (%.2f)'%(float(a['logZ_diff_VminusT']), float(a['logZ_diff_in_se'])) if a['logZ_diff_VminusT'] else 'NA',
        '%+.5f (%.2f)'%(float(b['logZ_diff_VminusT']), float(b['logZ_diff_in_se'])) if b['logZ_diff_VminusT'] else 'NA',
        f(a['pip_worst_ratio_isl'])+'/'+f(b['pip_worst_ratio_isl']), f(a['dH_T_to_fstar']), f(a['dH_V_to_fstar'])+'/'+f(b['dH_V_to_fstar']),
        f(a['dH_VT_lower_bound_triangle'])+'/'+f(b['dH_VT_lower_bound_triangle']), f(b.get('dH_VT_over_dH_T','')), f(a['core_h_V'],3)+'/'+f(b['core_h_V'],3), a['tier_final_T']+'/'+a['N_final_T']]))
