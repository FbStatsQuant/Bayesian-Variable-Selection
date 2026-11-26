#!/usr/bin/env bash
# s2_throttle_ctl.sh -- run on OWLS by a systemd --user timer every 10 min (HQ rule 2026-11-26). ONE ssh per run
# (ControlMaster) to NOTS runs the deployed s2_throttle.sh --reserve 300 --apply, which re-tunes ONLY the ArrayTaskThrottle of fb31's
# s2smc_* arrays (never S1, BQTF or any other job); the decision line ("THROTTLE ...", "SET ...") is appended to
#   /home/fb31/Bayesian-Variable-Selection/_local/engineering/logs/S1S2_throttle.log
# A run is skipped if the previous one still holds the lock. Launch (transient timer + service, survives T3 restarts):
#   systemd-run --user --unit=s1s2-s2throttle --on-calendar='*:00/10:00' --timer-property=AccuracySec=10s --collect \
#     --quiet <this script>
# Stop: systemctl --user stop s1s2-s2throttle.timer
set -uo pipefail
NSL=/home/fb31/SMC-BVS/_local/engineering/S1S2/deploy/S1S2/slurm
LOG=/home/fb31/Bayesian-Variable-Selection/_local/engineering/logs/S1S2_throttle.log
exec 9> "${XDG_RUNTIME_DIR:-/tmp}/s1s2-s2throttle.lock"
flock -n 9 || { echo "CTL $(date -u +%FT%TZ) previous run still active; skipped" >> "$LOG"; exit 0; }
RESERVE=${S2_RESERVE:-300}    # task slots kept free for S1 p=5000 (HQ 2026-11-26)
out=$(timeout 300 ssh -o ConnectTimeout=60 nots "$NSL/s2_throttle.sh --reserve $RESERVE --apply" 2>&1); rc=$?
{ echo "$out"; (( rc == 0 )) || echo "CTL $(date -u +%FT%TZ) ssh/controller error rc=$rc"; } >> "$LOG"
exit 0
