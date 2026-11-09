import time, f_common as fc
row = fc.make_row_ar1(100, 200, 0.5, nseeds=3)
print(row['id'], 'dn', row['dn'], '|P|', len(row['P']), 'S0', row['S0'])
t=time.time(); print(fc.pop_margins(row)); print('pop', time.time()-t)
t=time.time(); r=fc.seed_run(row,0); print(r); print('seed', time.time()-t)
row2=dict(row); 
t=time.time(); r=fc.lattice_test(row,[0,1]); print({k:(v if k not in ('na_arg','z2_arg','zm_arg','sw_arg') else v) for k,v in r.items()}); print('lat', time.time()-t)
