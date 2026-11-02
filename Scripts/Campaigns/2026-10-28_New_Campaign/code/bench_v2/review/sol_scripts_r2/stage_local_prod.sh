#!/usr/bin/env bash
# OPS supplies /scratch/fb31/New_Campaign/upload/RUN_ID with runner, source and manifest.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
UPLOAD=$1
UPLOAD_HASH=$2
test "$UPLOAD" = C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/packaging_pass2/staging/20261030T154800Z_bench_f3v2_prod
test -d "$UPLOAD/runner"
C:/Users/felip/AppData/Local/Programs/Python/Python313/python.exe "$UPLOAD/runner/upload_check.py" "$UPLOAD" "$UPLOAD_HASH"
cmp "$UPLOAD/MANIFEST_SHA256.txt" "$UPLOAD/runner/MANIFEST_SHA256.txt"
: # local-only path-mapped check; remote disk guard separately unit-tested
C:/Users/felip/AppData/Local/Programs/Python/Python313/python.exe C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/mapped_frozen.py C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/frozen.py C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/installed/prod/F3_AdaptiveLasso stage "$UPLOAD/F3_AdaptiveLasso" "$UPLOAD/MANIFEST_SHA256.txt" "$UPLOAD/runner/freeze.json" /home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso
C:/Users/felip/AppData/Local/Programs/Python/Python313/python.exe C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/mapped_frozen.py C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/frozen.py C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/review/sol_scripts_r2/installed/prod/F3_AdaptiveLasso check /home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso "$UPLOAD/runner/MANIFEST_SHA256.txt" "$UPLOAD/runner/freeze.json"
echo "STAGED_OK"
