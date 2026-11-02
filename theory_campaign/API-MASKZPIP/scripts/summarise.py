"""Summarise results/check_*.jsonl and results/vgrid_*.jsonl into a compact table (stdout)."""
import json, glob, sys, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
for f in sorted(glob.glob(os.path.join(base, 'check_*.jsonl'))):
    for l in open(f):
        d = json.loads(l)
        if d['kind'] == 'setting':
            print('\n##', d['design'], 'n=%d N=%d' % (d['n'], d['N']), 'diff_bits', d.get('diff_bits'), 'start_mode', d['start_mode_bits'],
                  'log pi0(S0)=%.2f log pi(S0)=%.3f a=%.2f Lambda=%.2f phi*=%.3f D=%.2f xm_is_S0=%s delta1=%.3g pi0(A)=%.3g' % (
                      d['log_pi0_S0'], d['log_pi_S0'], d['a'], d['Lambda'], d['phi_star'] or -1, d['D'], d['xm_is_S0'], d['delta1'], d['pi0_A']))
            print('| grid | T | logW q05 / med / q95 (engine) | iid-refresh q05 / med / q95 | late-switch pred | sandwich ok | mean f_endT | TV(nubar,pi) | max bias | E2 S0: P(miss at t=T) , frac W>20kappa |')
            print('|---|---|---|---|---|---|---|---|---|---|')
            continue
        e2 = d.get('E2', {}).get('S0')
        e2s = '%.2f, %.2f' % (e2['P_miss'][-1], max(e2['frac_W_gt_kappa_over_eta'])) if e2 else '-'
        print('| %s | %d | %.2f / %.2f / %.2f | %.2f / %.2f / %.2f | %s | %d/%d | %.3f | %.4f | %.4f | %s |' % (
            d['grid_name'], d['T'], d['q05_logW'], d['median_logW'], d['q95_logW'], d['iid_q05'], d['iid_median_logW'], d['iid_q95'],
            '%.2f' % d['late_pred'] if d['late_pred'] is not None else '-', d['sandwich_ok'], d['sandwich_applicable'],
            d['mean_f_endT'], d['TV_nubar_pi'], d['bias_max'], e2s))
for f in sorted(glob.glob(os.path.join(base, 'vgrid_*.jsonl'))):
    print('\n## V-grid', os.path.basename(f))
    for l in open(f):
        d = json.loads(l)
        print('pilot %d %-8s T=%3d S0inV=%s |V|=%d pi(V)=%.3f logW q05/med/q95 = %.2f / %.2f / %.2f' % (
            d['pilot'], d['grid_name'], d['T'], d['S0_in_V'], d['V_size'], d['pi_V'], d['q05'], d['median_logW'], d['q95']))
