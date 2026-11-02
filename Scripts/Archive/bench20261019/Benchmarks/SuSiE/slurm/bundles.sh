# bundles.sh -- shared bundle definitions for finalize_run.sh and retry_prod.sh (sourced, not run).
# One bundle = one (case, method): <stem>.rds, .csv, .sha256, .done under
#   <results>/<pppp>/<case_id>/<method_id>, case_id = <dataset_id>_c100.
# The validity contract is the same as run_case.R::done_is_valid(): all four regular files exist and
# the .sha256 file has exactly two lines, "<hash>  <method>.rds" and "<hash>  <method>.csv", both of
# which verify.

A1_METHODS="A1 SuSiE-L100"
A1_CANARIES="dev_p0500_S4_r001 dev_p1000_S2_r001 dev_p1000_S6_r001"

# Dataset ids of array task $1 for chunk size $2 (tasks 1-120 production, 121 canaries).
task_datasets() {
  local t=$1 chunk=$2 p u s r0 r pp
  if [ "$t" -ge 1 ] && [ "$t" -le 120 ]; then
    if [ "$t" -le 60 ]; then p=500; else p=1000; fi
    u=$(( (t - 1) % 60 )); s=$(( u / 10 + 1 )); r0=$(( 10 * (u % 10) + 1 ))
    pp=$(printf "p%04d" "$p")
    for r in $(seq "$r0" $(( r0 + chunk - 1 ))); do echo "${pp}_S${s}_r$(printf %03d "$r")"; done
  elif [ "$t" -eq 121 ]; then
    for id in ${A1_CANARIES}; do echo "$id"; done
  else
    return 1
  fi
}

# Expand an sbatch array spec ("1-121%60", "91,121") into task ids, one per line.
array_tasks() {
  echo "${1%%\%*}" | tr ',' '\n' | while IFS=- read -r a b; do seq "$a" "${b:-$a}"; done
}

# Bundle stem (without extension) of dataset $2, method $3, under results dir $1.
bundle_stem() {
  local pp=${2#dev_}; pp=${pp%%_*}
  echo "$1/${pp}/${2}_c100/$3"
}

# 0 if the bundle at stem $1 is valid.
valid_bundle() {
  local stem=$1 d m
  d=$(dirname "$stem"); m=$(basename "$stem")
  for e in rds csv sha256 done; do [ -f "${stem}.${e}" ] || return 1; done
  [ "$(wc -l < "${stem}.sha256")" -eq 2 ] || return 1
  [ "$(sed -n '1s/^[0-9a-f]\{64\}  //p' "${stem}.sha256")" = "${m}.rds" ] || return 1
  [ "$(sed -n '2s/^[0-9a-f]\{64\}  //p' "${stem}.sha256")" = "${m}.csv" ] || return 1
  (cd "$d" && sha256sum -c --quiet "${m}.sha256" >/dev/null 2>&1)
}
