#!/bin/bash
# detach_run.sh PIDFILE SCRIPT [ARGS...] : for PowerShell Start-Process launches. Records this process's PID (kept by exec) in PIDFILE, puts the NOTS
# ssh shim (global one-connection lock + stall bound) first in PATH, and execs bash SCRIPT ARGS. Refuses if PIDFILE names a live process.
P=${1:?pidfile}; shift
if [ -s "$P" ] && kill -0 "$(cat "$P")" 2>/dev/null; then echo "detach_run: $P names live pid $(cat "$P"); not starting" >&2; exit 7; fi
echo $$ > "$P"
PATH="/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold/sshlock:$PATH"; export PATH
exec bash "$@"
