#!/usr/bin/env bash
# rung_submit_wave.sh <WAVE R1|R2|R3> -- 10^5 rung (RUNG_PLAN §2-§3): submit the wave's batches in order, each through its own driver script (submit.sh; RG_T6: submit_t6.sh) with GO=yes, batches >= 5 min apart (GAP_S, default 300).
# GATE (same pattern as G-B's gb_submit_wave.sh): the FIRST batch of the wave is the pilot of the wave; the next batch is submitted only when the first batch's setup and calibrate stages are all COMPLETED (no pending / running row) and each stage's
# total billed core-h <= n_fits x its cap (setup 1.5, calibrate 5.0 core-h per fit = ~3 x the G-B measurements 0.5 / 1.8; n400 and IND are unmeasured at 10^5). Polled with ONE ssh (one sacct) per 5 min, at most MAXPOLL (8) polls; anything else: exit 70,
# the next batch is NOT submitted, report to the manager. Only after rung_presubmit.sh passed and the manager's GO. Send the monitor START line after the first batch (the probe says "batch not submitted yet" until the last is out).
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$SCRIPTS" "$WAVE")}; GAP=${GAP_S:-300}; MAXPOLL=${MAXPOLL:-8}; n=0; FIRST=""
SETUP_CAP=${SETUP_CAP:-1.5}; CAL_CAP=${CAL_CAP:-5.0}
gate() {   # $1 = the first batch of the wave
  local nf out; nf=$(python3 -c "import json,sys; print(len(json.load(open('$SCRIPTS/$1/plan.resolved.json'))['fits']))")
  out=$(ssh $NOTS "S=\$(grep -o '\"stage\":\"setup\",\"fit\":\"all\",\"job\":\"[0-9]*' $D/scratch/runs/$1/submissions.jsonl | grep -o '[0-9]*\$'); C=\$(grep -o '\"stage\":\"calibrate\",\"fit\":\"all\",\"job\":\"[0-9]*' $D/scratch/runs/$1/submissions.jsonl | grep -o '[0-9]*\$'); sacct -X -P -n -j \$S,\$C --format=JobID,JobName,State,CPUTimeRAW" 2>/dev/null || true)
  echo "$out" | sed "s/^/   gate: /"
  python3 - "$nf" "$SETUP_CAP" "$CAL_CAP" <<PY
import sys
nf, sc, cc = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]); rows = [l.split("|") for l in """$out""".strip().splitlines() if l.strip()]
st = {"setup": [], "calibrate": []}
for r in rows:
    if len(r) < 4: continue
    k = "setup" if "setup" in r[1] else ("calibrate" if "calibrate" in r[1] else None)
    if k: st[k].append((r[0], r[2].split()[0], int(r[3] or 0) / 3600.0))
bad = [k for k, v in st.items() if any(s not in ("COMPLETED", "PENDING", "RUNNING", "CONFIGURING", "COMPLETING") for _, s, _ in v)]
if bad: print("GATE BAD: " + ",".join(bad)); sys.exit(2)
if any(not v or any(s != "COMPLETED" or "[" in j for j, s, _ in v) or len([1 for j, _, _ in v if "[" not in j]) < nf for v in st.values()): print("GATE WAIT"); sys.exit(1)
ts, tc = sum(c for _, _, c in st["setup"]), sum(c for _, _, c in st["calibrate"])
if ts > sc * nf or tc > cc * nf: print("GATE OVER CAP: setup %.2f (<= %.2f) calibrate %.2f (<= %.2f)" % (ts, sc * nf, tc, cc * nf)); sys.exit(3)
print("GATE OK: setup %.2f <= %.2f, calibrate %.2f <= %.2f core-h, all COMPLETED (%d fit(s))" % (ts, sc * nf, tc, cc * nf, nf))
PY
}
for B in $BL; do
  if [[ $n -gt 0 ]]; then
    echo "-- waiting ${GAP}s before $B (>= 5 min apart)"; sleep "$GAP"
    if [[ $n -eq 1 ]]; then   # the gate, once, on the first batch
      p=0
      while :; do
        set +e; g=$(gate "$FIRST"); rc=$?; set -e; echo "$g" | tail -1
        [[ $rc -eq 0 ]] && break
        [[ $rc -ne 1 ]] && { echo "GATE FAILED for $FIRST: $B NOT submitted (report to the manager)" >&2; exit 70; }
        p=$((p+1)); [[ $p -lt $MAXPOLL ]] || { echo "GATE: no clean result after $p polls: $B NOT submitted (report to the manager)" >&2; exit 70; }
        sleep 300
      done
    fi
  fi
  echo "== submit $B"
  if [[ $B == RG_T6* ]]; then ssh $NOTS "cd $D/scripts/$B && CONFIRM=yes bash submit_t6.sh"; else ssh $NOTS "cd $D/scripts/$B && CONFIRM=yes bash submit.sh"; fi
  [[ $n -eq 0 ]] && FIRST=$B; n=$((n+1))
done
echo "all batches submitted: $BL"
