#!/bin/bash
# progress.sh -- ABL-CONF progress check (read-only, no compute).
cd "$(dirname "$0")/.."; W=${ABL_WORK:-/home/fb31/ablconf_work}
tot=$(grep -vc "^#" results/queue.txt); done_=$(ls $W/status 2>/dev/null | wc -l)
echo "terminal outcomes: $done_ / $tot   ($(cat $W/status/*.txt 2>/dev/null | awk '{print $2}' | sort | uniq -c | xargs))"
echo "running now (claims):"; for c in $W/claims/*/; do [ -d "$c" ] && echo "  $(basename $c)  $(cat $c/owner)  age $(( $(date +%s) - $(awk '{print $3}' $c/owner) ))s"; done
echo "worker jobs alive:"; ps -u fb31 -o pid,etime,args | grep "[r]un_queue.sh" | grep -v xargs | sed 's/^/  /'
echo "owls:"; jq -c '{ts,state,compute_cores,load_avg}' ~/.config/bvs-hq/owls/status.json
echo "recent outcomes:"; tail -n ${1:-8} $W/progress.log 2>/dev/null | sed 's/^/  /'
[ -s $W/killed.log ] && { echo "killed from outside (to re-run):"; sed 's/^/  /' $W/killed.log; }
exit 0
