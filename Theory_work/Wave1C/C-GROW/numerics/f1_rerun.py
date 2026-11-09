"""Re-run of the lattice task for the F1 row whose Q exceeds K (rho=0.8, p=199, n=200: |Q|=199 > K=100): infeasible T (|T|>K) are now skipped."""
import pickle, shutil, f_common as fc, f1_run
shutil.copy('f1_results.pkl', 'f1_results_v1_before_Kfix.pkl')
res = pickle.load(open('f1_results.pkl', 'rb'))
rid = 'F1_rho0.8_p199_n200'
row = f1_run.ROWS[rid]
new = fc.lattice_test(row, list(range(10))); new['wall'] = new['secs']
res = [r for r in res if not (r.get('id') == rid and r.get('kind') == 'lat')] + [new]
pickle.dump(res, open('f1_results.pkl', 'wb'))
print(rid, 'nT', new['nT'], 'skipped', new['nskip_infeasible'], 'K', new['K'], 'na_max', [round(v, 2) for v in new['na_max']], 'sw', [round(v, 1) for v in new['sw_max']], 'del', [round(v, 1) for v in new['del_max']])
