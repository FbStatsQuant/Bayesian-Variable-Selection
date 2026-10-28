# Exact_reference — the exact control posterior per dataset, and the comparison of every method with it

Not a benchmark. The methodology asks (i) that PARNI's PIPs be compared with the exact reference and (ii) that every
method's support be compared with the exact Bayesian decisions. Both need the exact posterior over all 2^30 models of
the control model for each of the 600 sealed datasets. It is computed once here, with the frozen SMC engine's compiled
enumerator (`engine/`, byte-identical to Experiment 1's; hashes in `engine/SHA256SUMS`), and read only after the
methods have been fitted. No method reads these files.

## Run (from the Benchmarks root, ~/projects/BVS/Benchmarks)

```bash
sbatch --array=1-6       Exact_reference/exact.slurm smoke        # replicate 1 of every scenario, ~8 min each
sbatch --array=1-600%300 Exact_reference/exact.slurm production   # all 600 datasets
ls Exact_reference/output/exact | wc -l                           # 600 .rds + 600 .json when complete
Rscript --vanilla Exact_reference/compare_to_exact.R runs/<RUN_DIR>            # after a method run finished
Rscript --vanilla Exact_reference/compare_to_exact.R runs/<RUN_DIR> Exact_reference/output/exact PARNI SuSIE
```

`compute_exact.R` verifies the dataset against `data/manifest.csv` (or `data_S6/manifest.csv`), enumerates, checks that
every model was visited and the probabilities sum to one, and writes `output/exact/<case>.rds` (log Z, PIPs, HPM, MPM,
truth, bookkeeping, data and engine hashes, versions) plus a JSON receipt. It refuses to overwrite.

`compare_to_exact.R RUN_DIR` writes `RUN_DIR/exact_comparison/`:
`supports_vs_exact.csv` (every method and rule: agreement with the exact MPM and HPM, exact recovery, FP/FN),
`pip_vs_exact.csv` (PIP methods: MAE, max AE, RMSE, by signal/proxy/null groups), `parni_repeats_vs_exact.csv`
(plain and RB PIP error per repeat, SD across repeats), `exact_ceilings.csv` (exact MPM/HPM recovery per dataset),
the per-scenario summaries and `SUMMARY_EXACT.md`.

Cost: Experiment 1 measured about 8 minutes and under 1 GB per enumeration on NOTS (`--mem=2G`, 1 h limit).
