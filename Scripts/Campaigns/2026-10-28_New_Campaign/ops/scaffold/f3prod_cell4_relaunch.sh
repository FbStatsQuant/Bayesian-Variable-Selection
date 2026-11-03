#!/bin/bash
# f3prod_cell4_relaunch.sh : (laptop; detached via detach_run.sh; control lane, HQ D76) BENCH_F3_PROD cell 4 (p1000_c050) relaunch after the D79
# home clean-up (HQ). Cells 1-3 (2503200, 2504013, 2507545) are terminal; launch.py submits only the next unsubmitted cell (cell 4) and itself
# refuses unless the preceding cell is terminal. Detached NOTS step = gate.sh standalone + ceiling check + dry run + launch (STAGE=0).
# Then the cell-4 array monitor. Output ops/evidence/ops8_f3prod_cell4.txt (+ CELL4_JOB=), monitor ops8_f3prod_cell4_monitor.log.
set -u
RUN_ID=20261102T1252Z_bench_f3v2_prod; UPSHA=b7d0e36bec8ada2fd991e706da8b895a2bd2a579d9f64aaa4916355284b15424
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
S=$CAMP/ops/scaffold; E=$CAMP/ops/evidence
export NOTS_SSH_LANE=control
cat $S/f3prod_cell4_gate_prefix.sh <(sed '1d' $S/f3prod_stage_launch_remote.sh) > $S/_f3prod_cell4_remote.sh
bash $S/remote_bg.sh f3prod_cell4_relaunch_$(date -u +%Y%m%dT%H%M%SZ) $S/_f3prod_cell4_remote.sh $E/ops8_f3prod_cell4.tmp RUN_ID=$RUN_ID UPSHA=$UPSHA STAGE=0
echo "ssh_rc=$?" >> $E/ops8_f3prod_cell4.tmp
JID=$(grep -oE '[0-9]{7} submitted' $E/ops8_f3prod_cell4.tmp | grep -oE '[0-9]{7}' | head -1)
[ -n "$JID" ] && echo "CELL4_JOB=$JID" >> $E/ops8_f3prod_cell4.tmp
mv $E/ops8_f3prod_cell4.tmp $E/ops8_f3prod_cell4.txt
[ -n "$JID" ] && exec bash $S/array_monitor.sh $E/ops8_f3prod_cell4_monitor.log $JID 'f3v2_' 60
