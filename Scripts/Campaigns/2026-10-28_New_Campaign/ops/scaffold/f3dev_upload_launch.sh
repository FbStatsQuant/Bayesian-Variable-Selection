#!/bin/bash
# f3dev_upload_launch.sh RUN_ID UPSHA : (laptop; run via sshlock/with_lock.sh so the whole sequence holds the one NOTS connection slot)
# JOB.md step 3 (scp -r the prepared staging folder to /scratch/fb31/New_Campaign/upload/) and step 4 + launch (f3dev_stage_launch_remote.sh).
set -u
RUN_ID=${1:?run_id}; UPSHA=${2:?upload sha}
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
SRC=$CAMP/bench_audit/jobs/staging/$RUN_ID; EV=$CAMP/ops/evidence/ops7_f3dev_${RUN_ID%_bench_f3v2_dev}
[ -d "$SRC" ] || { echo "no staging folder $SRC"; exit 1; }
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p /scratch/fb31/New_Campaign/upload && test ! -e /scratch/fb31/New_Campaign/upload/$RUN_ID && echo UPLOAD_TARGET_FREE" || { echo "upload target exists or ssh failed"; exit 1; }
scp -r -o BatchMode=yes "$SRC" nots:/scratch/fb31/New_Campaign/upload/ > "${EV}_scp.txt" 2>&1 || { cat "${EV}_scp.txt"; echo "SCP FAILED"; exit 1; }
echo "SCP_OK"
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "RUN_ID=$RUN_ID UPSHA=$UPSHA bash -s" < "$CAMP/ops/scaffold/f3dev_stage_launch_remote.sh" > "${EV}_launch.txt" 2>&1
echo "launch_ssh_rc=$?" >> "${EV}_launch.txt"; cat "${EV}_launch.txt"
