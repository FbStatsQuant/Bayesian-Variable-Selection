#!/bin/bash
# Retry an owls_run job until it is accepted (exit 75 = REFUSED). Usage: run_with_retry.sh <log> -- <cmd...>
log=$1; shift; shift
for i in $(seq 1 200); do
  /home/fb31/.config/bvs-hq/owls/owls_run -j 1 -- "$@" > "$log" 2>&1
  rc=$?
  if [ $rc -ne 75 ]; then echo "rc=$rc attempt=$i" >> "$log"; exit $rc; fi
  sleep 30
done
echo "gave up" >> "$log"; exit 75
