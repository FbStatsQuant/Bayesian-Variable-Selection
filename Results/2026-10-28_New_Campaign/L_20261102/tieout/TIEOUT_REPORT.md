# Independent tie-out report

Computed locally with R 4.4.1 from the input manifest, truth active indices, primary and repeat SMC records, and corresponding exact enumeration records. Dataset ID and scale key select exact scale and SMC case; log evidence uses fit$log_Z and scales[[scale]]$log_Z. Full-length adapter pip and pip_plain are compared with exact pip; sets use strict PIP > 0.5. Sample standard deviations use six seeds; quantiles use R type 7. Missing cases cause UNVERIFIED.

Posterior miss uses exact complete enumeration and certified-over-scored-models when the SMC HPM equals exact HPM; otherwise the core scorer evaluates both truth and SMC HPM. Start mass is independently reconstructed from raw X and matching Y, core preprocessing, recorded blocks, core block tables and start distribution; reconstructed log normalizer is checked against the saved fit.

## Mismatches

- Cell 5: claimed 0.023817; recomputed 0.0110542115457.
- Cell 28: claimed 125.0; recomputed 100.
- Cell 35: claimed 90.0; recomputed 93.
- Cell 37: claimed 0.024263; recomputed 0.0114106541507.
- Cell 41: claimed 2.0; recomputed 4.

## Data observations

No missing, failed, or misaligned records encountered in the selected cases.

Overall: MATCH 38, MISMATCH 5 .
