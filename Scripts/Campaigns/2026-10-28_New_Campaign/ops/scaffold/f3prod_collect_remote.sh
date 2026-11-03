#!/bin/bash
# f3prod_collect_remote.sh : (NOTS; started detached by remote_bg.sh) BENCH_F3_PROD JOB.md "Terminal accounting, retry and acceptance" +
# "Download, verify, clean" (manifests step only). Never submits anything: if retry.py --dry-run selects any TIMEOUT unit, or any cell state is
# not COMPLETED, it stops with RETRY_NEEDED / DISPOSITION_NEEDED for OPS. env.sh (errexit) is only ever sourced inside subshells.
# Final markers: COLLECT_OK (reconcile rc 0, accounting, timing, manifests written) or COLLECT_STOP <reason>.
set -uo pipefail
R=20261102T1252Z_bench_f3v2_prod
U=/scratch/fb31/New_Campaign/upload/$R/runner; LG=/scratch/fb31/New_Campaign/logs/$R; RS=/scratch/fb31/New_Campaign/results/$R
export PYTHONDONTWRITEBYTECODE=1
stop() { echo "COLLECT_STOP $1"; exit 4; }
cd /scratch/fb31/New_Campaign || stop "cd"
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
q=$(squeue -h -u fb31 -o '%i %j %T' 2>&1) || stop "squeue failed: $q"
printf '%s\n' "$q" | grep -q 'f3v2_' && stop "F3 jobs still queued/running: $q"
echo "== sacct (all four cells)"; sacct -n -X -j 2503200,2504013,2507545,2509541 -o JobID%28,State%14,ExitCode,Elapsed 2>&1 | awk '{print $2}' | sort | uniq -c
echo "== retry --dry-run"
( source $U/env.sh; python3 $U/retry.py prod $R --dry-run ) > $LG/retry_dryrun.txt 2>&1; rrc=$?
grep -vE '^\s*[0-9]+\) |Inactive Modules|MODULEPATH|reloaded|^$' $LG/retry_dryrun.txt; echo "retry_dryrun_rc=$rrc"
[ $rrc -eq 0 ] || stop "retry dry run failed"
nsel=$(grep -oE 'timeouts_without_valid_result [0-9]+' $LG/retry_dryrun.txt | awk '{s+=$2; n++} END{print s+0, n+0}')
echo "retry selection (sum, cells): $nsel"
set -- $nsel; [ "$2" = 4 ] || stop "retry dry run did not report all 4 cells"
[ "$1" = 0 ] || stop "RETRY_NEEDED: $1 TIMEOUT units without valid result (OPS submits retry per JOB.md, at most once per cell)"
# (fix 22:50Z: the line continues with " timeouts_without_valid_result N" after the dict; the first run's $-anchored pattern never matched)
grep -E ' states ' $LG/retry_dryrun.txt | grep -vE "states \{'COMPLETED': [0-9]+\} timeouts_without_valid_result [0-9]+\$" | grep -q . && stop "DISPOSITION_NEEDED: a cell has states other than COMPLETED (see above)"
SRC=$(awk -F'\t' 'NR>1 {print $5}' $LG/jobs.tsv | grep -oE '\b[0-9a-f]{64}\b' | sort -u)
[ "$(printf '%s\n' "$SRC" | grep -c .)" = 1 ] || stop "source sha256 not unique in jobs.tsv: [$SRC]"
echo "source_sha256=$SRC"
echo "== reconcile"
( source $U/env.sh; set -o pipefail; python3 $U/reconcile.py --root $RS --kind prod --run-id $R --source-sha256 $SRC 2>&1 | tee $LG/reconcile.txt > /dev/null ); rec=$?
echo "reconcile_rc=$rec"; awk -F'\t' 'NF>=3 {print $3}' $LG/reconcile.txt | sort | uniq -c | sort -rn | head; tail -5 $LG/reconcile.txt
[ $rec -eq 0 ] || stop "reconcile nonzero"
echo "== accounting"
( source $U/env.sh; set -o pipefail; python3 $U/accounting.py $LG 2>&1 | tee $LG/accounting.tsv > /dev/null ); arc=$?; echo "accounting_rc=$arc"; cat $LG/accounting.tsv | tail -15
[ $arc -eq 0 ] || stop "accounting nonzero"
echo "== timing"
( source $U/env.sh; set -o pipefail; python3 $U/collect_timing.py prod $LG/timing | tee $LG/timing.tsv > /dev/null ); trc=$?; echo "timing_rc=$trc"; tail -8 $LG/timing.tsv
[ $trc -eq 0 ] || stop "timing nonzero"
echo "== manifests"
( source $U/env.sh; python3 $U/manifests.py --run-log $LG $RS/p0500 $RS/p1000 $LG ) 2>&1 | grep -vE '^\s*[0-9]+\) |Inactive Modules|MODULEPATH|reloaded|^$'; mrc=${PIPESTATUS[0]}
echo "manifests_rc=$mrc"; [ $mrc -eq 0 ] || stop "manifests nonzero"
for d in $RS/p0500 $RS/p1000 $LG; do echo "MANIFEST $d $(sha256sum $d/MANIFEST.sha256 | cut -c1-64) lines=$(wc -l < $d/MANIFEST.sha256)"; done
echo "COLLECT_OK $(date -u +%FT%TZ)"
