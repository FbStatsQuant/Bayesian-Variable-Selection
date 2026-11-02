#!/bin/bash
set -euo pipefail
STAMP=${1:?usage: retune_throttle.sh STAMP --profile alone|withH [--yes]}; shift; export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/bench.env"
SQUEUE=${SQUEUE:-squeue}; SCONTROL=${SCONTROL:-scontrol}; profile=; yes=0; drain=0
while (($#)); do case $1 in --profile) profile=${2:?}; shift 2;; --yes) yes=1; shift;; --check-drained) drain=1; shift;; *) exit 2;; esac; done
[[ $profile == alone || $profile == withH || $drain == 1 && -z $profile && $yes == 0 ]] || exit 2
[[ -r $RUN_HOME/JOBIDS.tsv ]] || exit 2
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
ids=$(awk -F'\t' 'NR>1 && $3 ~ /^[0-9]+$/ {print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -)
[[ -n $ids ]] || exit 2
if ((drain)); then
  billed=$(printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{if(NF!=4 || $1 !~ /^[0-9]+(_[^|]+)?$/ || $4 !~ /^[0-9]+$/){bad=1;next}split($1,b,"_");if(x[b[1]] && $3=="RUNNING")sum+=2*int(($4+1)/2)} END{if(bad)exit 1;print sum+0}') || exit 4
  echo "PROD-L RUNNING billed CPUs: $billed (limit $CEIL_WITHH)"
  ((billed<=CEIL_WITHH)); exit $?
fi
# raising to the alone profile (132 billed) is refused while any PROD-H job is still queued or running (D47.4, D49: 68 while PROD-H runs)
if [[ $profile == alone ]] && printf '%s\n' "$q" | awk -F'|' '$2 ~ /_prodH/ {f=1} END{exit !f}'; then echo "REFUSED: PROD-H jobs are still queued or running; keep --profile withH" >&2; exit 2; fi
# working files in a private scratch temp folder; ONE record LOG_RUN/launch/retune_<utc>.txt is written only when --yes applies updates
mkdir -p -- "$TMP_ROOT"; wd=$(mktemp -d "$TMP_ROOT/retune.XXXXXX"); trap 'rm -rf -- "$wd"' EXIT
plan="$wd/plan.tsv"; queue="$wd/squeue.txt"; receipt="$wd/ceiling_receipt.txt"; actions="$wd/actions.txt"; : > "$actions"
printf 'step\tcpus\tmax_concurrent_tasks\tphase\n' > "$plan"
printf '%s\n' "$q" > "$queue"
record() {  # record STATUS : the single retune record (plan, queue before, admission receipt, updates, queue after, status)
  mkdir -p -- "$LOG_RUN/launch"; local f="$LOG_RUN/launch/retune_$(date -u +%Y%m%dT%H%M%SZ).txt"
  { echo "# retune $(date -u +%FT%TZ) by $(id -un)@$(hostname) profile=$profile status=$1"
    echo "## plan"; cat "$plan"; echo "## squeue before"; cat "$queue"; echo "## ceiling receipt"; cat "$receipt" 2>/dev/null
    echo "## updates"; cat "$actions"; echo "## squeue after"; cat "$wd/after.txt" 2>/dev/null; echo "STATUS $1"; } > "$f"
  echo "retune record: $f"
}
declare -a update_ids update_values
while IFS=$'\t' read -r wave step id array dep; do
 [[ $id =~ ^[0-9]+$ ]] || continue
 if [[ $array == - ]]; then
  cpus=$(printf '%s\n' "$q" | awk -F'|' -v id="$id" '$1==id {if($4 !~ /^[0-9]+$/)exit 1; print $4}') || exit 4
  if [[ -n $cpus ]]; then printf '%s\t%s\t1\tfit\n' "$step" "$cpus" >> "$plan"; fi
  continue
 fi
 printf '%s\n' "$q" | awk -F'|' -v id="$id" '$1 ~ ("^" id "_") {found=1} END{exit !found}' || continue
 case $step in s1_bench) p=bench;; s2_benchretry) p=benchretry;; *) continue;; esac
 if [[ $profile == alone ]]; then v=THR_A_$p; else v=THR_H_$p; fi
 n=${!v}; c=CPUS_$p
 printf '%s\t%s\t%s\tfit\n' "$step" "${!c}" "$n" >> "$plan"
 update_ids+=("$id"); update_values+=("$n")
done < "$RUN_HOME/JOBIDS.tsv"
(( ${#update_ids[@]} )) || { echo 'No live arrays' >&2; exit 2; }
export CEIL_ALONE CEIL_WITHH CEIL_COMBINED
if ! "${PYTHON:-python3}" "$HERE/ceiling_check.py" --profile "$profile" --plan "$plan" --squeue "$queue" --own-ids "$ids" --receipt "$receipt"; then
  echo "REFUSED by the ceiling check (nothing changed):" >&2; cat "$receipt" >&2 2>/dev/null; exit 2
fi
for ((i=0;i<${#update_ids[@]};i++)); do
  id=${update_ids[i]}; n=${update_values[i]}
  printf 'scontrol update JobId=%s ArrayTaskThrottle=%s\n' "$id" "$n" | tee -a "$actions"
  if ((yes)); then "$SCONTROL" update "JobId=$id" "ArrayTaskThrottle=$n" >> "$actions" 2>&1 || { echo "scontrol FAILED for $id" | tee -a "$actions" >&2; record "FAILED (scontrol)"; exit 4; }; fi
done
((yes)) || { echo "(dry run: nothing changed; add --yes to apply)"; exit 0; }
after=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || { echo "squeue failed after the update" > "$wd/after.txt"; record "NOT CONFIRMED (squeue failed)"; exit 4; }
printf '%s\n' "$after" > "$wd/after.txt"
bad_ids=
for ((i=0;i<${#update_ids[@]};i++)); do
  id=${update_ids[i]}; n=${update_values[i]}
  printf '%s\n' "$after" | awk -F'|' -v id="$id" -v n="$n" '$1 ~ ("^" id "_\\[") && $3=="PENDING" {if($1 !~ ("%" n "\\]$"))bad=1} END{exit bad}' || bad_ids="$bad_ids $id"
done
if [[ -n $bad_ids ]]; then record "NOT CONFIRMED: squeue still shows a different throttle (mismatch) for$bad_ids"; echo "throttle NOT confirmed for$bad_ids" >&2; exit 4; fi
record "CONFIRMED"

