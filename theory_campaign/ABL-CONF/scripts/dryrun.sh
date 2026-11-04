#!/bin/bash
# dryrun.sh -- ABL-CONF: apply the pre-registered rule (apply_rule.py) to (i) the ABL-START table and (ii) synthetic
# tables, BEFORE any ABL-CONF fit runs. Pure Python on small CSVs (no fits). Output: results/dryrun/.
set -e
cd "$(dirname "$0")/.."; O=results/dryrun; mkdir -p $O/input
git show origin/theory/MEET-v31:theory_campaign/MEET-v31/evidence/item1_per_fit.csv > $O/input/abl_start_item1_per_fit.csv
python3 scripts/abl_start_table.py $O/input/abl_start_item1_per_fit.csv $O/abl_start
python3 scripts/make_synthetic.py $O/synthetic
{
echo "# ABL-CONF rule dry run ($(date -Is)); rule = scripts/apply_rule.py sha256 $(sha256sum scripts/apply_rule.py | cut -c1-16)"
echo; echo "## (i) ABL-START table (12 designs x 1 seed; stand-in reference, see abl_start_table.py)"
for v in per_design pooled pooled_guardpass; do
  fav=S1; [ $v != per_design ] && fav=ALL
  echo; echo "### $v"; python3 scripts/apply_rule.py $O/abl_start/$v/per_fit.csv $O/abl_start/$v/reference.csv $O/abl_start/$v/rule --favourable $fav
done
echo; echo "## (ii) synthetic tables (make_synthetic.py)"
for s in expected no_difference B_fails_badly C_fails_badly reversed guard_fails; do
  echo; echo "### $s"; python3 scripts/apply_rule.py $O/synthetic/$s/per_fit.csv $O/synthetic/$s/reference.csv $O/synthetic/$s/rule
done
} | tee $O/DRYRUN_OUTPUT.txt
