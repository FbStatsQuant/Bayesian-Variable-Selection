#!/bin/bash
# prodl_close_enum_p5scan_remote.sh (ON NOTS via: ssh nots 'bash -s' < this): PROD-L JOB.md §5 step 8 (close enum20 + enum30: final after the main
# wave) and step 6 (submit the initial P5 scan). The run must be idle (no PROD-L job queued/running).
set -u
export STAMP=20261030T1811Z
RL=/home/fb31/projects/BVS/New_Campaign/runs/${STAMP}_lowp_prodL; B=$RL/code/prod_l
echo "date=$(date -u +%FT%TZ)"
squeue -h -u fb31 -o '%j' | grep -q lowpL_ && { echo "a PROD-L job is queued/running: stop"; exit 1; }
for p in enum20 enum30; do echo "== close $p"; bash $B/make_manifests.sh $STAMP --piece $p < /dev/null 2>&1 | tail -8; echo "close_${p}_rc=${PIPESTATUS[0]}"; done
ls $RL/manifests/ 2>&1; cat $RL/manifests/summary.tsv 2>&1
echo "== P5 scan initial"; bash $B/submit_prodl.sh --p5-scan --phase initial < /dev/null 2>&1 | tail -15; echo "p5scan_submit_rc=${PIPESTATUS[0]}"
squeue -h -u fb31 -o '%i %j %T' | grep -v f3v2
