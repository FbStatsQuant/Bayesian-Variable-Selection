#!/bin/bash
# run_queue.sh <queue_file> -- ABL-CONF worker pool. Run under owls_run (it sets OWLS_JOB_CORES and single-threaded BLAS):
#   setsid nohup ~/.config/bvs-hq/owls/owls_run -j 2 -- bash scripts/run_queue.sh results/queue.txt < /dev/null > LOG 2>&1 &
# Starts OWLS_JOB_CORES single-threaded workers. All workers of all jobs walk the SAME queue in order and claim a fit
# atomically (mkdir $W/claims/<name>), so 3 jobs x 2 workers = 6 fits at a time with dynamic packing.
# A fit is skipped if $W/status/<name>.txt exists (terminal outcome recorded) or it is claimed by another worker.
# Per-fit wall cap (PREREG section 4): CAP seconds of process wall time, enforced with `timeout` on the whole Rscript
# process (R start-up included). Terminal outcomes written to $W/status/<name>.txt:
#   completed  rc = 0 and the .rds exists          (fit-level status, e.g. completed / schedule_limit, is in the .rds)
#   capped     killed by the cap (rc 124/137 and wall >= CAP - 5)
#   failed     any other non-zero rc of the R process itself (rc 1, R error)
# A process killed from OUTSIDE (rc 143/137/129 before the cap, e.g. a server restart) is NOT terminal: it is logged to
# $W/killed.log, its claim is released and relaunch.sh re-runs it.
Q=$(readlink -f "$1"); cd "$(dirname "$0")"
export ABL_WORK=${ABL_WORK:-/home/fb31/ablconf_work}
W=$ABL_WORK; CAP=${ABL_CAP:-4500}
mkdir -p $W/fits $W/logs $W/status $W/claims $W/tmp
P=${OWLS_JOB_CORES:-1}
worker() {
  local wid=$1
  grep -v "^#" "$Q" | while read -r name id sk arm off role k; do
    [ -z "$name" ] && continue
    [ -f $W/status/$name.txt ] && continue
    mkdir $W/claims/$name 2>/dev/null || continue
    echo "$(hostname -s) $BASHPID $(date +%s) job=${OWLS_JOB_ID:-?} worker=$wid" > $W/claims/$name/owner
    if [ -f $W/status/$name.txt ]; then rm -rf $W/claims/$name; continue; fi
    tmp=$W/tmp/$name.rds; rm -f $tmp
    echo "=== $(date -Is) start $name (cap ${CAP}s)" >> $W/logs/$name.log
    t0=$(date +%s.%N)
    timeout --signal=TERM --kill-after=30 $CAP Rscript abl_fit.R $id $sk $arm $tmp $off < /dev/null >> $W/logs/$name.log 2>&1
    rc=$?
    t1=$(date +%s.%N); wall=$(echo "$t1 - $t0" | bc)
    capped=$(echo "$wall >= $CAP - 5" | bc)
    if [ $rc -eq 0 ] && [ -f $tmp ]; then mv $tmp $W/fits/$name.rds; out=completed
    elif { [ $rc -eq 124 ] || [ $rc -eq 137 ]; } && [ "$capped" = 1 ]; then out=capped
    elif [ $rc -eq 143 ] || [ $rc -eq 137 ] || [ $rc -eq 129 ] || [ $rc -eq 130 ]; then out=killed
    else out=failed; fi
    if [ $out = killed ]; then
      echo "$(date -Is) $name rc=$rc wall=$wall killed-from-outside (will be re-run by relaunch.sh)" >> $W/killed.log
    else
      echo "$name $out rc=$rc wall_s=$wall cap_s=$CAP role=$role k=$k arm=$arm id=$id scale=$sk seed_offset=$off end=$(date -Is)" \
        > $W/status/$name.txt
      echo "$(date -Is) $name $out wall=${wall%.*}s | $(tail -1 $W/logs/$name.log)" >> $W/progress.log
    fi
    rm -f $tmp; rm -rf $W/claims/$name
  done
}
for w in $(seq 1 $P); do worker $w & done
wait
echo "$(date -Is) run_queue.sh: queue walk finished (job ${OWLS_JOB_ID:-?})"
