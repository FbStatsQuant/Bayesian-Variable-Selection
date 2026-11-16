#!/usr/bin/env bash
# test_competitors.sh -- the competitor harness end to end on this machine (no installs; methods whose package is missing
# must give package_missing records, which the evaluator records without metrics).
#   tools/competitors/test_competitors.sh <build-dir with smcbvs4>
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
B=${1:?build dir}; BIN=$B/smcbvs4
W=$(mktemp -d "${TMPDIR:-.}/wp5_comp_XXXXXX"); trap 'rm -rf "$W"' EXIT
"$BIN" gen --design AR --n 100 --p 200 --seed 7 --s0 5 --out "$W/raw.bin" --truth "$W/truth.json" > /dev/null
"$BIN" prep --in "$W/raw.bin" --out "$W/data.bin" > /dev/null
nice -n 19 Rscript "$here/p1m_competitors.R" --check-packages --out-dir "$W" > /dev/null
nice -n 19 Rscript "$here/p1m_competitors.R" --raw "$W/raw.bin" --truth "$W/truth.json" --out-dir "$W" --seed 3
fail=0
for f in "$W"/comp_*.json; do
  m=$(basename "$f" .json); m=${m#comp_}
  rc=0; "$BIN" eval --competitor "$f" --data "$W/data.bin" --truth "$W/truth.json" --out "$W/ev_$m.bin" \
      --n-draws 500 --n-x 200 --n-test 1000 > /dev/null || rc=$?
  line=$(python3 - "$W/ev_$m.bin.json" "$f" <<'PY'
import json, sys
r = json.load(open(sys.argv[1])); c = json.load(open(sys.argv[2]))
d = r.get("dist", {}).get("C") if isinstance(r.get("dist"), dict) else None
h2 = d["plugin"]["h2"] if d else None
sel = r.get("selection", {})
print("%-14s comp=%-16s eval=%-10s hpm_eq_S0=%-5s plugin_h2=%s" % (c["method"], c["status"], r["status"], sel.get("hpm_eq_S0"), h2))
PY
)
  echo "  $line"
  [[ $rc == 0 ]] || { echo "  FAIL: eval rc=$rc for $m"; fail=1; }
done
python3 - "$W" <<'PY' || fail=1
import json, os, sys
W = sys.argv[1]
r = json.load(open(os.path.join(W, "ev_ols_oracle.bin.json")))
assert r["selection"]["hpm_eq_S0"] is True, "oracle OLS must select S0"
assert json.load(open(os.path.join(W, "comp_sis_screen.json")))["status"] == "completed"
assert os.path.exists(os.path.join(W, "sis_cols.txt"))
for m in ("marg_ols", "ols_oracle"):
    assert json.load(open(os.path.join(W, "comp_%s.json" % m)))["status"] == "completed", m
pk = json.load(open(os.path.join(W, "packages.json")))
missing = [p["package"] for p in pk["packages"] if not p["installed"]]
print("  packages missing here:", ", ".join(missing) or "none")
PY
[[ $fail == 0 ]] && echo "competitor harness: OK" || { echo "competitor harness: FAILED"; exit 1; }
