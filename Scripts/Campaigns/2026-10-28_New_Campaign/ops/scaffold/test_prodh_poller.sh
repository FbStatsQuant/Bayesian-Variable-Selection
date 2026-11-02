#!/bin/bash
# test_prodh_poller.sh : offline test of prodh_poller.sh exit logic with an ssh shim (no network). Cases: urgent 3, hold 4, still_held 4, error 5,
# all-left 0, p500-left 6 (and not again once the flag exists: then the 'continue' case runs until TIME_UP 2 with MAX=1 and an instant sleep).
set -u
S=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/scaffold
W=$(mktemp -d); NF=0
mk() { # mk POLLRC DECISION RUNJOBS P500JOBS
  cat > "$W/ssh" <<EOS
#!/bin/bash
echo '{"utc": "x", "decision": "$2", "urgent": false, "counts": {"finished": 7, "units": 2400}}'
echo POLL_RC=$1; echo RUNJOBS=$3; echo P500JOBS=$4
EOS
  printf '#!/bin/bash\nexit 0\n' > "$W/sleep"; chmod 755 "$W/ssh" "$W/sleep"; }
run() { PATH="$W:$PATH" bash "$S/prodh_poller.sh" X_prodH "$W/$1.log" "$2"; }
t() { local name=$1 want=$2 got=$3; if [ "$got" = "$want" ]; then echo "PASS $name rc=$got"; else echo "FAIL $name rc=$got want $want"; NF=$((NF+1)); fi; }
mk 3 HOLD_FAILED 3 1; run urgent 5; t urgent 3 $?
mk 0 HOLD 3 1;        run hold 5;   t hold 4 $?
mk 0 STILL_HELD 3 1;  run still 5;  t still_held 4 $?
mk 1 continue 3 1;    run err 5;    t poll_error 5 $?
mk 0 continue 0 0;    run done 5;   t all_left 0 $?
mk 0 continue 2 0;    run p5 5;     t p500_left 6 $?
touch "$W/p5b.p500_left.flag"
mk 0 continue 2 0;    run p5b 1;    t p500_not_again_timeup 2 $?
grep -h '^SUMMARY' "$W"/urgent.log "$W"/done.log | head -2
rm -rf -- "$W"; echo "poller test failures: $NF"; [ $NF -eq 0 ]
