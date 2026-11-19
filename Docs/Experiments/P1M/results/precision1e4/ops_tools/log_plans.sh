#!/usr/bin/env bash
# log_plans.sh -- O-1: one PLANS line per batch in deploy_leg.log (UTC, batch, PLANS, sha256 of plans/<batch>.json, code_commit, -, -, -, who),
# and a check against the committed waves.json plan_sha256 values (results/precision1e4/waves.json, exp/P1M a6037ab0).
set -euo pipefail; . "$(dirname "$0")/common.sh"
if [[ ${1:-} == B1 ]]; then   # the boundary wave B1 (ADDENDUM_1_BOUNDARY): plan shas as committed there (9a1235ab… / ab30848d…), logged as PLANS lines
  for b in PL_B1_1 PL_B1_2; do
    sha=$(sha256sum "$STG/current/plans/$b.json" | cut -d' ' -f1)
    case $b in PL_B1_1) exp=9a1235ab;; PL_B1_2) exp=ab30848d;; esac
    [[ $sha == $exp* ]] || { echo "PLAN SHA DIFFERS from ADDENDUM_1: $b $sha (expected $exp…)" >&2; exit 1; }
    log_leg $b PLANS "$sha" "$(python3 -c "import json;print(json.load(open('$STG/current/plans/$b.json'))['code_commit'])")" - - -
    echo "$b $sha"
  done; exit 0
fi
W=${1:-/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/precision1e4/waves.json}
python3 - "$STG/current/plans" "$W" <<'PY' | while IFS=$'\t' read -r b sha cc; do log_leg "$b" PLANS "$sha" "$cc" - - -; done
import hashlib, json, os, sys
plans, w = sys.argv[1], json.load(open(sys.argv[2]))
n = bad = 0
for wv, x in w.items():
    for b in x["batches"]:
        raw = open(os.path.join(plans, b["batch"] + ".json"), "rb").read(); sha = hashlib.sha256(raw).hexdigest(); n += 1
        if sha != b["plan_sha256"]:
            bad += 1; print("PLAN SHA DIFFERS from the committed waves.json: " + b["batch"], file=sys.stderr)
        print("%s\t%s\t%s" % (b["batch"], sha, json.loads(raw)["code_commit"]))
print("%d batches, %d differ from the committed waves.json" % (n, bad), file=sys.stderr)
sys.exit(1 if bad else 0)
PY
