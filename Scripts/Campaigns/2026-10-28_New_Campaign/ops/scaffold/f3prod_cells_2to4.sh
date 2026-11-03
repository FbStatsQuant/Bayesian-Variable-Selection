#!/bin/bash
# f3prod_cells_2to4.sh : (laptop; detached via detach_run.sh) BENCH_F3_PROD cells 2-4 sequentially (HQ D65): each cell launches only after the
# previous cell's monitor log says ALL_TERMINAL. Launch = f3prod_stage_launch_remote.sh with STAGE=0 (ceiling check + dry run + launch.py, which
# itself refuses unless the preceding cell is terminal). Any EARLY_FAILURE / MAX_CHECKS_REACHED / missing job id stops the chain (finding for OPS
# triage; never a retry here). Output per cell: ops/evidence/ops8_f3prod_cell<i>.txt (+ CELL<i>_JOB=), monitor ops8_f3prod_cell<i>_monitor.log;
# chain status lines in ops8_f3prod_cells_chain.txt (CHAIN STOP / CHAIN DONE).
set -u
RUN_ID=20261102T1252Z_bench_f3v2_prod; UPSHA=b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence; C=$E/ops8_f3prod_cells_chain.txt
export NOTS_SSH_LANE=control NOTS_SSH_LOCK_WAIT_S=1800    # HQ D76 control lane (the bulk pull no longer blocks it)
stop() { echo "CHAIN STOP $(date -u +%FT%TZ): $1" >> $C; exit 1; }
echo "start $(date -u +%FT%TZ)" >> $C
for i in 2 3 4; do
  prev=$E/ops8_f3prod_cell$((i-1))_monitor.log
  until grep -qE '^(ALL_TERMINAL|EARLY_FAILURE|MAX_CHECKS_REACHED)' $prev 2>/dev/null; do sleep 60; done
  grep -q '^ALL_TERMINAL' $prev || stop "cell $((i-1)) monitor ended with $(grep -E '^(EARLY_FAILURE|MAX_CHECKS_REACHED)' $prev | tail -1)"
  echo "cell $((i-1)) ALL_TERMINAL; launching cell $i $(date -u +%FT%TZ)" >> $C
  # HQ D76: control lane; the launch (ceiling + dry run + launch.py gate, ~10-15 min) runs detached on NOTS, polled by short control calls
  bash $S/remote_bg.sh f3prod_cell${i}_$(date -u +%Y%m%dT%H%M%SZ) $S/f3prod_stage_launch_remote.sh $E/ops8_f3prod_cell$i.tmp RUN_ID=$RUN_ID UPSHA=$UPSHA STAGE=0
  echo "ssh_rc=$?" >> $E/ops8_f3prod_cell$i.tmp
  JID=$(grep -oE '[0-9]{7} submitted' $E/ops8_f3prod_cell$i.tmp | grep -oE '[0-9]{7}' | head -1)
  [ -n "$JID" ] && echo "CELL${i}_JOB=$JID" >> $E/ops8_f3prod_cell$i.tmp
  mv $E/ops8_f3prod_cell$i.tmp $E/ops8_f3prod_cell$i.txt
  [ -n "$JID" ] || stop "cell $i not launched (see ops8_f3prod_cell$i.txt)"
  echo "CELL${i}_JOB=$JID $(date -u +%FT%TZ)" >> $C
  bash $S/array_monitor.sh $E/ops8_f3prod_cell${i}_monitor.log $JID 'f3v2_' 60
done
echo "CHAIN DONE $(date -u +%FT%TZ)" >> $C
