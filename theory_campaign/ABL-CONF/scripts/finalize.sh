#!/bin/bash
# finalize.sh [out_dir=results/final] -- summary + pre-registered rule + tables. Run when progress.sh shows all fits
# terminal (an earlier run is an interim reading and apply_rule.py says so). Small R job through owls_run -j 1.
set -e; cd "$(dirname "$0")/.."; O=${1:-results/final}; mkdir -p $O
export ABL_WORK=${ABL_WORK:-/home/fb31/ablconf_work}
~/.config/bvs-hq/owls/owls_run -j 1 -- Rscript scripts/summarise.R results/queue.txt $O
python3 scripts/apply_rule.py $O/per_fit.csv $O/reference.csv $O/rule
python3 scripts/report_tables.py $O
