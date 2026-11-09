"""Export the SAME (X, y) as the Python runs (study generator, iid rows, c = 1, p = 100, s0 = 4, step 5) for D4: d4_data/{X,y}_S{scen}_n{n}_s{seed}.csv"""
import os, sys, numpy as np
import study_common as sc
os.makedirs("d4_data", exist_ok=True)
ns = [int(v) for v in sys.argv[1].split(",")]; seeds = int(sys.argv[2])
for scen in (2, 5):
    for n in ns:
        for seed in range(seeds):
            spec, X, y = sc.build_xy((scen, 100, 4, 5, 1.0, n, seed, "iid"))
            np.savetxt("d4_data/X_S%d_n%d_s%d.csv" % (scen, n, seed), X, delimiter=",", fmt="%.17g")
            np.savetxt("d4_data/y_S%d_n%d_s%d.csv" % (scen, n, seed), y, delimiter=",", fmt="%.17g")
print("ok")
