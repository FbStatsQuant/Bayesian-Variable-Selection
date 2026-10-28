# PROVISIONAL 100-replicate assessment analysis

Unverified core units: run_pipeline.py; benchmark_adapter.R; r1_contract.R; native_contract.R. Independent Sol cell recount and Astra review remain required. Synthetic runs use a D-owned schema mock, not certification of A's updated adapter; final A-R1 integration remains pending.

Observed unique rule rows: 122400. Missing expected rule opportunities: 2400. Exactly 1200 selected datasets / 2400 paired-scale cases: replicates 1..100, S1..S6, p500/p1000. Denominators are 100 per scenario cell and 600 per p/scale pooled; excluded replicates (if any) are not missing fits. See assessment_filter_checks.csv, selected_cases.csv, missing_rule_groups.csv and failure_summary.csv. All absent selected rows remain in denominators.

Published reproduction: 2 supplied reference tables compared after explicit key sort with R identical(), including column types. Unavailable reference tables: 20; see published_reference_gaps.csv. Regenerated tables without original references are not claimed independently reproduced. Byte equality is separate in published_reproduction.csv. Version names and paths are in manifest.json. Historical SUMMARY.md is not substituted for the supplied canonical version.

Supplementary uncertainty uses sample variance / n. Scenario-pooled MCSE uses fixed scenario strata: sqrt(sum_h (n_h/N)^2 s_h^2/n_h). For conditional successful-only means, observed successful n_h fix the weights; pooled FP/FN and complete-success-pair MCSEs condition on observed successful stratum counts and do not include randomness of failure-driven mixture weights or selection. n<2 in a nonempty stratum gives NA. No pooling across scales. Paired differences are SMC minus comparator within the same case; FP/FN use complete-success pairs. Missing/failed rows are zero for exact/selection and unavailable for FP/FN. T4 group units are case selection proportions, with within-case dependence retained. Runtime p95 is type 7; median, p95 and max have no fabricated MCSE.

Replicates per cell: 100. MCSE estimates are unstable at small n; zero observed sample variance and zero observed MCSE do not imply certainty or a zero population error rate.

All registered and derived rules remain present, including completely absent groups. Long-chain sensitivity requires a separately reviewed registry extension and cannot overwrite A3 baseline. See CONTRACT.md for limitations and gate requirements.
