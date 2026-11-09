"""D3 add-on: how the extras S~0 \ S0 distribute over the blocks of the start mode (S5, c = 1; S2 for comparison).  -> D3_blocks_raw.csv, D3_blocks_summary.md"""
import sys, numpy as np, pandas as pd
import bvs_core as bc, study_common as sc
rows = []
for scen in (5, 2):
    for p in (100, 200, 400):
        for n in (200, 800, 3200):
            for seed in range(5):
                spec, X, y = sc.build_xy((scen, p, 4, 5, 1.0, n, seed, "iid"))
                S0 = set(spec["S0"]); prob = bc.Problem(X, y); blocks = bc.partition(X); info = bc.start_mode(prob, blocks)
                mode = set(info.mode)
                per = [(len(mode & set(b)) - len(mode & set(b) & S0), bool(S0 & set(b)), len(b)) for b in blocks]
                ex_truth = [e for e, t, s in per if t]; ex_null = [e for e, t, s in per if not t]
                rows.append(dict(scen=scen, p=p, n=n, seed=seed, J=len(blocks), B=bc.block_size(n, p), n_extra=len(mode - S0), n_truth_blocks=len(ex_truth),
                                 extras_in_truth_blocks=sum(ex_truth), extras_in_null_blocks=sum(ex_null), null_blocks=len(ex_null),
                                 null_blocks_with_extra=sum(1 for e in ex_null if e > 0), mean_extra_per_null_block=float(np.mean(ex_null)), max_extra_in_block=max(e for e, t, s in per),
                                 block_sizes=str(sorted(set(s for _, _, s in per)))))
df = pd.DataFrame(rows); df.to_csv("D3_blocks_raw.csv", index=False)
g = df.groupby(["scen", "p", "n"]).agg(runs=("seed", "count"), J=("J", "first"), B=("B", "first"), extras=("n_extra", "mean"), in_truth_blocks=("extras_in_truth_blocks", "mean"),
                                      in_null_blocks=("extras_in_null_blocks", "mean"), null_blocks=("null_blocks", "mean"), null_blocks_with_extra=("null_blocks_with_extra", "mean"),
                                      mean_extra_per_null_block=("mean_extra_per_null_block", "mean"), max_in_block=("max_extra_in_block", "max")).round(2)
with open("D3_blocks_summary.md", "w") as f:
    f.write("## D3 add-on: distribution of the extras S~0 minus S0 over blocks (5 seeds per row, c = 1; script d3_extras_blocks.py -> D3_blocks_raw.csv)\n\n" + g.reset_index().to_string() + "\n")
print(open("D3_blocks_summary.md").read())
