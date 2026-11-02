#!/bin/bash
set -euo pipefail
STAMP=${1:?}; shift; yes=0; [[ ${1:-} != --yes ]] || { yes=1; shift; }; (($#==0)) || exit 2

[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/bench.env"
source "$HERE/stale_lib.sh"
SQUEUE=${SQUEUE:-squeue}; SACCT=${SACCT:-sacct}
[[ -r $RUN_HOME/JOBIDS.tsv ]] || { echo 'missing JOBIDS' >&2; exit 3; }
ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || exit 3
[[ -n $ids ]] || exit 3
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then echo 'active jobs' >&2; exit 3; fi
acct=$("$SACCT" -X -n -P -j "$ids" -o JobID,State) || exit 4
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF>=2{split($1,b,"_");if(x[b[1]]){seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/)bad=1}} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo 'accounting not terminal or missing' >&2; exit 3; }

roots=(); d="$SCR_ROOT/results/${STAMP}_lowp_benchres"; [[ ! -d $d ]] || roots+=("$d")
((${#roots[@]})) || exit 0
mapfile -t found < <(stale_find "${roots[@]}")
archive=$LOG_RUN/cleanup/$(date -u +%Y%m%dT%H%M%SZ)
for path in "${found[@]}"; do
 [[ -e $path ]] || continue; echo "$path"
 if ((yes)); then rel=${path#"$SCR_ROOT/results/"}; dest=$archive/$rel; [[ ! -e $dest ]] || exit 2; mkdir -p "$(dirname "$dest")"; mv -- "$path" "$dest"; printf '%s\t%s\n' "$path" "$dest" >> "$archive/listing.tsv"; fi
done

