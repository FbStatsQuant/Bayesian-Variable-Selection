import sys
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,hashlib,difflib
P=pathlib.Path
C=P('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
V=C/'code/bench_v2';S=V/'review/sol_scripts';L=C/'code/bench_lowp';B=V/'lowp_port/baseline_bench_lowp'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
with (S/'static_extra.log').open('w',encoding='utf-8') as out:
 for rel in ['R/methods/fit_F4_mcp.R','R/methods/fit_F5_abess.R','R/methods/fit_A1_susie.R','R/methods/fit_A2_ssl.R','R/methods/fit_A3_horseshoe.R']:
  out.write(f'{rel}: byte identical {sha(B/rel)==sha(L/rel)}\n')
  if sha(B/rel)!=sha(L/rel):out.writelines(difflib.unified_diff((B/rel).read_text().splitlines(True),(L/rel).read_text().splitlines(True)))
 old=(V/'lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt').read_text().splitlines()
 new=(V/'lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt').read_text().splitlines()
 out.write('r2 changed lines: '+str([(a,b) for a,b in zip(old,new) if a!=b])+'\n')
 # All deployed source baseline hashes are read directly from the mirror, not from reports.
 dep=P('C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks')
 out.write((V/'BASELINE_SHA256.txt').read_text())
 for folder in ['F1_Lasso','F2_ElasticNet','F3_AdaptiveLasso']:
  for f in ['config.R','common.R','run_case.R','methods/glmnet_helpers.R','methods/'+{'F1_Lasso':'fit_F1_lasso.R','F2_ElasticNet':'fit_F2_enet.R','F3_AdaptiveLasso':'fit_F3_alasso.R'}[folder]]:
   out.write(f'DEPLOYED {folder}/{f} {sha(dep/folder/f)}\n')
