#!/usr/bin/env bash
SP="/c/Users/felip/AppData/Local/Temp/claude/7f4deb75538d3cf7/03611146-335e-4730-9f01-d3ebd88e845b/scratchpad/suite"; E="/c/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-68de3711/Theory_work/Wave1C/C-ENG/numerics/existing_suite"; idx=$1
cd "$SP"
for spec in "A_orig_f16ce15|$SP/coreA/Scripts/SMC_BVS/core" "B_new_ls0off|$SP/coreB/core" "C_new_ls0on|$SP/coreC/core"; do
  name=${spec%%|*}; core=${spec#*|}
  s=$(date +%s); r=$(bash run_cfg.sh "$core" "$E/$name/seed_$idx" $idx 2>&1 | tail -n 1); echo "$name seed $idx: $r  elapsed=$(($(date +%s)-s))s" >> "$SP/chain_$idx.log"
done
echo done >> "$SP/chain_$idx.log"
