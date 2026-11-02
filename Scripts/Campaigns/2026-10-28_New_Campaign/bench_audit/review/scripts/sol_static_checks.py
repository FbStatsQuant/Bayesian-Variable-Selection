from pathlib import Path
from hashlib import sha256
import csv
root = Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian')
methods = root/'02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/methods_dev'
low = root/'02_Experiments/I_2026-10-28_New_Campaign/code/bench_lowp/R/methods'
for folder, file in [('F1_Lasso','fit_F1_lasso.R'),('F2_ElasticNet','fit_F2_enet.R'),('F3_AdaptiveLasso','fit_F3_alasso.R'),('F5_ABESS','fit_F5_abess.R')]:
    a, b = methods/folder/'methods'/file, low/file
    print(file, 'same_bytes=', a.read_bytes()==b.read_bytes(), 'SHA256=', sha256(a.read_bytes()).hexdigest())
data = Path('C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/results')
runs = [('F1','20261019T2308Z_bench20261019_prod_F1_Lasso'),('F1','20261021T1615Z_bench20261019_prodc050_F1_Lasso'),('F3','20261019T2157Z_bench20261019_prod_F3_AdaptiveLasso'),('F3','20261021T1540Z_bench20261019_prodc050_F3_AdaptiveLasso')]
for method, run in runs:
    files = sorted((data/run).rglob(method+'.csv'))
    total = 0.0
    for file in files:
        with file.open(newline='', encoding='utf-8-sig') as stream:
            total += float(next(csv.DictReader(stream))['runtime_s'])
    print(run, 'n=',len(files),'summed_runtime_h=',total/3600)
script = Path(__file__).with_name('sol_review_checks.R')
print('sol_review_checks.R SHA256=',sha256(script.read_bytes()).hexdigest())
