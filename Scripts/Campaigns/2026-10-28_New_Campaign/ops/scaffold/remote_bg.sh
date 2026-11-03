#!/bin/bash
# remote_bg.sh NAME REMOTE_SCRIPT LOCAL_OUT [VAR=VALUE ...] : (laptop; control lane, HQ D76) run a NOTS-side step that can exceed the 5-min control
# wall WITHOUT holding a connection: one short control ssh uploads REMOTE_SCRIPT to /scratch/fb31/New_Campaign/upload/ops_bg/NAME.sh and starts it
# detached on the login node (setsid nohup; stdout+stderr -> NAME.out; final line "BG_EXIT rc=<n>"); then short control polls (cat NAME.out) every
# 60 s until BG_EXIT. A poll that fails (timeout 124 / reset 255 / other) -> 15-min back-off (HQ rule), then continue. Refuses to start if NAME.out
# already exists on NOTS (never runs a step twice). Exit status = the remote rc (or 90 start failed, 91 never finished within MAX_POLLS).
# VAR=VALUE assignments must be simple tokens ([A-Za-z0-9_./:=-]); they are passed with env to the remote script.
set -u
NAME=${1:?name}; RS=${2:?remote script}; OUT=${3:?local out}; shift 3
for a in "$@"; do [[ "$a" =~ ^[A-Za-z_][A-Za-z0-9_]*=[A-Za-z0-9_./:=-]*$ ]] || { echo "remote_bg: bad assignment $a" >&2; exit 90; }; done
[[ "$NAME" =~ ^[A-Za-z0-9_.-]+$ ]] || { echo "remote_bg: bad name" >&2; exit 90; }
D=/scratch/fb31/New_Campaign/upload/ops_bg; MAX_POLLS=${MAX_POLLS:-300}
export NOTS_SSH_LANE=control
start=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "mkdir -p $D && test ! -e $D/$NAME.out && test ! -e $D/$NAME.sh && cat > $D/$NAME.sh || { echo REFUSED_EXISTS_OR_UPLOAD; exit 9; }; setsid nohup bash -c 'env $* bash $D/$NAME.sh; echo BG_EXIT rc=\$?' > $D/$NAME.out 2>&1 < /dev/null & sleep 1; test -e $D/$NAME.out && echo BG_STARTED $NAME" < "$RS" 2>&1); src=$?
echo "### remote_bg start $(date -u +%FT%TZ) rc=$src: $start" > "$OUT.progress"
[ $src = 0 ] && [[ "$start" == *"BG_STARTED $NAME"* ]] || { echo "remote_bg: start failed (rc=$src): $start" > "$OUT"; exit 90; }
n=0
while [ $n -lt "$MAX_POLLS" ]; do
  n=$((n+1)); sleep 60
  body=$(MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots "cat $D/$NAME.out" 2>&1); prc=$?
  echo "### poll $n $(date -u +%FT%TZ) rc=$prc lines=$(printf '%s\n' "$body" | wc -l)" >> "$OUT.progress"
  if [ $prc != 0 ]; then echo "poll failed rc=$prc: back off 15 min" >> "$OUT.progress"; sleep 900; continue; fi
  if printf '%s\n' "$body" | grep -q '^BG_EXIT rc='; then
    printf '%s\n' "$body" > "$OUT"; rc=$(printf '%s\n' "$body" | sed -n 's/^BG_EXIT rc=\([0-9]*\).*/\1/p' | tail -1); exit "${rc:-91}"
  fi
done
printf '%s\n' "$body" > "$OUT"; echo "remote_bg: no BG_EXIT after $MAX_POLLS polls" >> "$OUT"; exit 91
