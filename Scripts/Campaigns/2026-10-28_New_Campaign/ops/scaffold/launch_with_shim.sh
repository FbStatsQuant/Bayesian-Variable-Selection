#!/bin/bash
# launch_with_shim.sh SCRIPT [ARGS...] : run a bash SCRIPT with the NOTS ssh shim first in PATH (global one-connection lock + stall bound).
# Used for detached launches (PowerShell Start-Process) of the PROD-H poller, the PROD-L waiter and the dev-pilot monitor.
PATH="/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold/sshlock:$PATH"
export PATH
exec bash "$@"
