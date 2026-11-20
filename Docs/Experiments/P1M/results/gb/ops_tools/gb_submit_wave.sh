#!/usr/bin/env bash
# gb_submit_wave.sh <WAVE G1|G2> -- G-B pilot set: submit the wave's two batches through each batch's own driver submit.sh (GO=yes). Batch a (pilot, I_max 0) first; batch b (the I_max 3 twin) only after
# (GB_PLAN §2.2): the pilot's setup AND calibrate stages are COMPLETED and each billed <= 2 x its E (setup 0.41 -> 0.82, calibrate 1.1 -> 2.2 core-h), and >= 5 min after batch a (GAP_S, default 300).
# The gate polls with ONE ssh (one sacct) per 5 min (POLICIES §12.7), at most MAXPOLL polls (default 8 = 40 min); anything but COMPLETED within 2 x E, or no result in time: exit 70, batch b NOT submitted, report to the manager.
# Only after gb_presubmit.sh passed and the manager's GO. Send the monitor START line after the LAST batch.
set -euo pipefail; . "$(dirname "$0")/common.sh"
[[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
WAVE=${1:?WAVE}; BL=${BATCHES:-$(batches_of "$SCRIPTS" "$WAVE")}; GAP=${GAP_S:-300}; MAXPOLL=${MAXPOLL:-8}; n=0; FIRST=""
SETUP_E2=${SETUP_E2:-0.82}; CAL_E2=${CAL_E2:-2.2}
gate() {   # $1 = the pilot batch: both stages COMPLETED and within 2 x E
  local out; out=$(ssh $NOTS "S=\$(grep -o '\"stage\":\"setup\",\"fit\":\"all\",\"job\":\"[0-9]*' $D/scratch/runs/$1/submissions.jsonl | grep -o '[0-9]*\$'); C=\$(grep -o '\"stage\":\"calibrate\",\"fit\":\"all\",\"job\":\"[0-9]*' $D/scratch/runs/$1/submissions.jsonl | grep -o '[0-9]*\$'); sacct -X -P -n -j \$S,\$C --format=JobID,JobName,State,CPUTimeRAW" 2>/dev/null || true)
  echo "$out" | sed "s/^/   gate: /"
  python3 - "$SETUP_E2" "$CAL_E2" <<PY
import sys
se2, ce2 = float(sys.argv[1]), float(sys.argv[2]); rows = [l.split("|") for l in """$out""".strip().splitlines() if l.strip()]
st = {"setup": None, "calibrate": None}
for r in rows:
    if len(r) < 4: continue
    k = "setup" if "setup" in r[1] else ("calibrate" if "calibrate" in r[1] else None)
    if k: st[k] = (r[2].split()[0], int(r[3] or 0) / 3600.0)
bad = [k for k, v in st.items() if v and v[0] not in ("COMPLETED", "PENDING", "RUNNING", "CONFIGURING", "COMPLETING")]
if bad: print("GATE BAD: " + ",".join(bad)); sys.exit(2)
if not all(st.values()) or any(v[0] != "COMPLETED" for v in st.values()): print("GATE WAIT"); sys.exit(1)
if st["setup"][1] > se2 or st["calibrate"][1] > ce2: print("GATE OVER 2xE: setup %.2f (<= %.2f) calibrate %.2f (<= %.2f)" % (st["setup"][1], se2, st["calibrate"][1], ce2)); sys.exit(3)
print("GATE OK: setup %.2f <= %.2f, calibrate %.2f <= %.2f core-h, both COMPLETED" % (st["setup"][1], se2, st["calibrate"][1], ce2))
PY
}
for B in $BL; do
  if [[ $n -gt 0 ]]; then
    echo "-- waiting ${GAP}s before $B (>= 5 min after $FIRST; then the pilot gate)"; sleep "$GAP"; p=0
    while :; do
      set +e; g=$(gate "$FIRST"); rc=$?; set -e; echo "$g" | tail -1
      [[ $rc -eq 0 ]] && break
      [[ $rc -ne 1 ]] && { echo "GATE FAILED for $FIRST: $B NOT submitted (report to the manager)" >&2; exit 70; }
      p=$((p+1)); [[ $p -lt $MAXPOLL ]] || { echo "GATE: no clean result after $p polls: $B NOT submitted (report to the manager)" >&2; exit 70; }
      sleep 300
    done
  fi
  echo "== submit $B"; ssh $NOTS "cd $D/scripts/$B && CONFIRM=yes bash submit.sh"; [[ $n -eq 0 ]] && FIRST=$B; n=$((n+1))
done
