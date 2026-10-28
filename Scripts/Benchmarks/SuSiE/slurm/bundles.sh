# bundles.sh -- shared bundle definitions for finalize_run.sh and retry_prod.sh (sourced, not run).
# One bundle = one (case, method): <stem>.rds, .csv, .sha256, .done under
#   <results>/<pppp>/<case_id>/<method_id>, case_id = <dataset_id>_<scale key> (canaries: always _c100).
# c050 copy: production map of 400 tasks x 3 datasets (A1_CHUNK = 3), canary task 401; pilot map of
# 4 tasks x 3 datasets (replicate 1 of S1-S6 x p 500/1000).
# The validity contract is the same as run_case.R::done_is_valid(): all four regular files exist and
# the .sha256 file has exactly two lines, "<hash>  <method>.rds" and "<hash>  <method>.csv", both of
# which verify.

A1_METHODS="SuSiE-refine"      # refine tree: runs SuSiE-refine only (A1 / L100 production untouched)
A1_CANARIES="dev_p0500_S4_r001 dev_p1000_S2_r001 dev_p1000_S6_r001"

A1_CHUNK_C050=3
A1_CANARY_TASK=401

# Dataset ids of array task $1 under map $2 ("prod": tasks 1-400 production, 401 canaries;
# "pilot": tasks 1-4). Production: tasks 1-200 p = 500, 201-400 p = 1000; within a p, u = (t - 1) mod 200
# covers positions 3u .. 3u + 2 of the scenario-major order (position i: scenario i div 100 + 1,
# replicate i mod 100 + 1), the same dataset order as c = 1.
task_datasets() {
  local t=$1 map=$2 p u i s r pp
  if [ "$map" = pilot ]; then
    [ "$t" -ge 1 ] && [ "$t" -le 4 ] || return 1
    if [ "$t" -le 2 ]; then pp=p0500; else pp=p1000; fi
    for s in $(seq $(( 3 * ((t - 1) % 2) + 1 )) $(( 3 * ((t - 1) % 2) + 3 ))); do echo "${pp}_S${s}_r001"; done
  elif [ "$map" = prod ] && [ "$t" -ge 1 ] && [ "$t" -le 400 ]; then
    if [ "$t" -le 200 ]; then p=500; else p=1000; fi
    u=$(( (t - 1) % 200 )); pp=$(printf "p%04d" "$p")
    for i in $(seq $(( A1_CHUNK_C050 * u )) $(( A1_CHUNK_C050 * u + A1_CHUNK_C050 - 1 ))); do
      s=$(( i / 100 + 1 )); r=$(( i % 100 + 1 ))
      echo "${pp}_S${s}_r$(printf %03d "$r")"
    done
  elif [ "$map" = prod ] && [ "$t" -eq "${A1_CANARY_TASK}" ]; then
    for id in ${A1_CANARIES}; do echo "$id"; done
  else
    return 1
  fi
}

# Expand an sbatch array spec ("1-121%60", "91,121") into task ids, one per line.
array_tasks() {
  echo "${1%%\%*}" | tr ',' '\n' | while IFS=- read -r a b; do seq "$a" "${b:-$a}"; done
}

# Bundle stem (without extension) of dataset $2, method $3, under results dir $1, scale key $4
# (canary datasets dev_* always use c100, the scale of the dev pilot they are compared with).
bundle_stem() {
  local pp=${2#dev_} sk=$4; pp=${pp%%_*}
  case "$2" in dev_*) sk=c100 ;; esac
  echo "$1/${pp}/${2}_${sk}/$3"
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
