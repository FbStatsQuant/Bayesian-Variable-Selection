#!/bin/bash
# test_cleanup_inplace.sh -- local test of B3 (HQ D44): cleanup_pilot.sh run the way OPS ran it, FROM INSIDE the tree it deletes
# (bash HOME/runs/<PID>/code/lowp/pilot/cleanup_pilot.sh, working directory inside that tree too), must still remove everything and VERIFY it.
#   bash tests/test_cleanup_inplace.sh WORKDIR
# On NOTS (NFS) the old script left a silly-renamed .nfs* file; on Windows an open script file blocks deletion in a similar way. The fixed
# script re-executes itself from memory after `cd /`. The old (revision 7c) script is run the same way for comparison (informational row).
set -u
W=${1:?usage: test_cleanup_inplace.sh WORKDIR}; rm -rf "$W"; mkdir -p "$W"; W=$(cd "$W" && pwd)
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); PILOT=$(cd "$HERE/.." && pwd)
STAMP=20261030T0313Z; PID=${STAMP}_lowp_pilot
FAIL=0; N=0
res() { N=$((N + 1)); if [ "$2" = "$3" ] && [ "${4:-0}" = 0 ]; then echo "| $1 | $2 | $3 | ok |"; else echo "| $1 | $2 | $3 (extra=${4:-0}) | **WRONG** |"; FAIL=$((FAIL + 1)); fi; }
B=$W/bin; mkdir -p "$B"
printf '#!/bin/bash\nexit 0\n' > "$B/squeue"; printf '#!/bin/bash\necho "7001|COMPLETED"\n' > "$B/sacct"; printf '#!/bin/bash\necho "GUARD OK"\nexit 0\n' > "$B/guard"; chmod +x "$B"/*
fixture() { # fixture ROOT SCRIPT : a staged pilot whose clean-up script is SCRIPT, copied into runs/<PID>/code/lowp/pilot/
  local R=$1; rm -rf "$R"; mkdir -p "$R/home/New_Campaign/runs/$PID/code/lowp/pilot" "$R/home/New_Campaign/code/shared" "$R/scr/New_Campaign/runs/${PID}_cache" "$R/scr/New_Campaign/runs/${PID}_tmp" "$R/scr/New_Campaign/results" "$R/scr/New_Campaign/logs"
  echo "lowp_pilot $STAMP staged" > "$R/home/New_Campaign/runs/$PID/OWNER"; printf 'step\tjobid\tarray\tdependency\ns0_build\t7001\t-\t-\n' > "$R/home/New_Campaign/runs/$PID/JOBIDS.tsv"
  mkdir -p "$R/home/New_Campaign/runs/$PID/study/truth"; echo t > "$R/home/New_Campaign/runs/$PID/study/truth/x.rds"; echo keep > "$R/home/New_Campaign/code/shared/x"
  cp "$2" "$R/home/New_Campaign/runs/$PID/code/lowp/pilot/cleanup_pilot.sh"; }
inplace() { # inplace ROOT : run the staged copy from inside the tree, cwd inside the tree
  local R=$1 RP=$1/home/New_Campaign/runs/$PID/code/lowp/pilot
  ( cd "$RP" && NC_HOME_ROOT="$R/home/New_Campaign" NC_SCR_ROOT="$R/scr/New_Campaign" GUARD="$B/guard" SQUEUE="$B/squeue" SACCT="$B/sacct" \
      bash "$RP/cleanup_pilot.sh" $STAMP --yes > "$R/clean.log" 2>&1 ); echo $?; }
echo "| Case | Expected | Got | Result |"; echo "|---|---|---|---|"
fixture "$W/fx" "$PILOT/cleanup_pilot.sh"; rc=$(inplace "$W/fx")
res "fixed script run FROM INSIDE runs/<PID> (cwd inside too): CLEANUP VERIFIED, exit 0" 0 "$rc" $(grep -q "CLEANUP VERIFIED" "$W/fx/clean.log" && echo 0 || echo 1)
res "  ... it re-executed from memory, and nothing of the pilot remains (runs/<PID>, _cache, _tmp gone); shared code untouched" 0 0 \
  $(grep -q "running from memory" "$W/fx/clean.log" && [ ! -e "$W/fx/home/New_Campaign/runs/$PID" ] && [ ! -e "$W/fx/scr/New_Campaign/runs/${PID}_cache" ] && [ -e "$W/fx/home/New_Campaign/code/shared/x" ] && echo 0 || echo 1)
fixture "$W/fx2" "$PILOT/cleanup_pilot.sh"; rc=$( ( cd "$W/fx2/home/New_Campaign/runs/$PID/code/lowp/pilot" && NC_HOME_ROOT="$W/fx2/home/New_Campaign" NC_SCR_ROOT="$W/fx2/scr/New_Campaign" GUARD="$B/guard" SQUEUE="$B/squeue" SACCT="$B/sacct" bash cleanup_pilot.sh $STAMP > "$W/fx2/dry.log" 2>&1 ); echo $? )
res "dry run from inside the tree: exit 0, changes nothing, no re-execution" 0 "$rc" $([ -e "$W/fx2/home/New_Campaign/runs/$PID/OWNER" ] && ! grep -q "running from memory" "$W/fx2/dry.log" && echo 0 || echo 1)
# R7D-3: relative roots and a relative helper path, given from the fixture root, work in the dry run AND in the --yes (re-exec) run
fixture "$W/fx3" "$PILOT/cleanup_pilot.sh"; cp "$B/guard" "$W/fx3/guard_rel"
rc=$( ( cd "$W/fx3" && NC_HOME_ROOT=home/New_Campaign NC_SCR_ROOT=scr/New_Campaign GUARD=./guard_rel SQUEUE="$B/squeue" SACCT="$B/sacct" bash home/New_Campaign/runs/$PID/code/lowp/pilot/cleanup_pilot.sh $STAMP > "$W/fx3/dry.log" 2>&1 ); echo $? )
res "R7D-3: relative NC_HOME_ROOT / NC_SCR_ROOT, dry run: exit 0, targets listed, nothing changed" 0 "$rc" $(grep -q "remove   .*runs/$PID" "$W/fx3/dry.log" && [ -e "$W/fx3/home/New_Campaign/runs/$PID/OWNER" ] && echo 0 || echo 1)
rc=$( ( cd "$W/fx3" && NC_HOME_ROOT=home/New_Campaign NC_SCR_ROOT=scr/New_Campaign GUARD=./guard_rel SQUEUE="$B/squeue" SACCT="$B/sacct" bash home/New_Campaign/runs/$PID/code/lowp/pilot/cleanup_pilot.sh $STAMP --yes > "$W/fx3/yes.log" 2>&1 ); echo $? )
res "R7D-3: relative roots and a relative GUARD path, --yes from the fixture root: CLEANUP VERIFIED (exit 0), resolved before cd /" 0 "$rc" \
  $(grep -q "CLEANUP VERIFIED" "$W/fx3/yes.log" && grep -q "GUARD OK" "$W/fx3/yes.log" && [ ! -e "$W/fx3/home/New_Campaign/runs/$PID" ] && echo 0 || echo 1)
OLD="$PILOT/../../../conformance/work/pilot_rewire_audit/baseline/pilot/cleanup_pilot.sh"
if [ -r "$OLD" ]; then fixture "$W/fx_old" "$OLD"; rc=$(inplace "$W/fx_old")
  echo "| (information) the OLD script (revision 6/7c) run the same way: exit $rc; $(grep -oE 'CLEANUP (VERIFIED|UNVERIFIED)[^.]*' "$W/fx_old/clean.log" | head -1) | - | - | info |"; fi
echo; echo "test_cleanup_inplace: $((N - FAIL)) passed, $FAIL failed"
[ "$FAIL" = 0 ]
