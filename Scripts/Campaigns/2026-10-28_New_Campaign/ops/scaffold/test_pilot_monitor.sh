#!/bin/bash
# test_pilot_monitor.sh : offline test of pilot_monitor.sh v2 with an ssh shim (no network). Three cases: early failure (exit 3), all terminal (exit 0),
# still running (exit 2 after 1 check; the 600 s sleep is shimmed away). Prints PASS/FAIL.
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
W=$(mktemp -d); NF=0
mkshim() { # mkshim CASE : ssh prints a canned squeue + sacct; sleep returns at once
  cat > "$W/ssh" <<EOS
#!/bin/bash
case "$1" in
  fail) printf '%s\n' '===SACCT===' '         2467487        lowp_p0_build      COMPLETED      0:0   00:00:26' '         2467488       lowp_p0_verify         FAILED      1:0   00:00:11' '         2467489    lowp_p0_truthlock      CANCELLED      0:0   00:00:00';;
  done) printf '%s\n' '===SACCT===' '         2467487        lowp_p0_build      COMPLETED      0:0   00:00:26' '  2467495_[0-27]          lowp_p2_smc      CANCELLED+     0:0   00:00:00';;
  run)  printf '%s\n' '2467495_3 lowp_p2_smc RUNNING bb1' '===SACCT===' '         2467487        lowp_p0_build      COMPLETED      0:0   00:00:26' '         2467495          lowp_p2_smc        RUNNING      0:0   00:01:00';;
esac
EOS
  printf '#!/bin/bash\nexit 0\n' > "$W/sleep"; chmod 755 "$W/ssh" "$W/sleep"; }
for c in "fail 3" "done 0" "run 2"; do set -- $c
  mkshim "$1"; PATH="$W:$PATH" bash "$S/pilot_monitor.sh" "$W/log_$1" 1,2,3 1; rc=$?
  if [ $rc -eq "$2" ]; then echo "PASS $1 rc=$rc"; else echo "FAIL $1 rc=$rc want $2"; NF=$((NF+1)); fi
  grep '^check' "$W/log_$1"
done
rm -rf -- "$W"; echo "monitor test failures: $NF"; [ $NF -eq 0 ]
