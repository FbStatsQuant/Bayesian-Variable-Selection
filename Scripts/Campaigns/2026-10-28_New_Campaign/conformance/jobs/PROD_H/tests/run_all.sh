#!/bin/bash
# run_all.sh -- run every local dry-run test of the PROD-H bundle and write one log per suite into tests/ (Git Bash on Windows; R 4.4.1 for the parser check).
#   bash run_all.sh            about 6 minutes (2,400-unit trees are fabricated several times)
# Logs: syntax.log tables.log py_tests.log shell_tests.log (+ SHELL_TESTS.md) cli_parser.log summary.log
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; B="$(cd "$HERE/.." && pwd)"
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
mixed() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else echo "$1"; fi; }
PY="py -3"; command -v py >/dev/null 2>&1 || PY=python3
RSCRIPT="${RSCRIPT:-C:/Program Files/R/R-4.4.1/bin/Rscript.exe}"; [ -x "$RSCRIPT" ] || RSCRIPT=Rscript
rc_all=0
{ for f in "$B"/runner/*.sh "$B"/runner/*.sbatch "$B"/stage_local.sh "$HERE"/*.sh; do bash -n "$f" && echo "PASS bash -n ${f#"$B"/}" || { echo "FAIL bash -n $f"; rc_all=1; }; done
  for f in "$B"/runner/*.py "$HERE"/*.py; do $PY -c 'import sys; compile(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1], "exec")' "$(mixed "$f")" && echo "PASS python compile ${f#"$B"/}" || { echo "FAIL python $f"; rc_all=1; }; done
  if grep -rIl $'\r' "$B"/runner "$B"/stage_local.sh "$HERE"/*.sh "$HERE"/stubs >/dev/null 2>&1; then echo "FAIL CR characters in a script"; rc_all=1; else echo "PASS no CR characters in scripts or stubs"; fi
  command -v shellcheck >/dev/null 2>&1 && shellcheck -S warning "$B"/runner/*.sh || echo "(shellcheck not available)"; } > "$HERE/syntax.log" 2>&1
$PY - "$(mixed "$B/tables")" > "$HERE/tables.log" 2>&1 <<'EOF'
import csv, sys
from pathlib import Path
t = Path(sys.argv[1])
units = list(csv.DictReader(open(t / "units.tsv", newline=""), delimiter="\t"))
chunks = list(csv.DictReader(open(t / "chunks.tsv", newline=""), delimiter="\t"))
ds = {u["dataset_id"] for u in units}
assert len(units) == 2400 and len({u["case_id"] for u in units}) == 2400 and len(ds) == 1200 and len(chunks) == 1200
assert {(u["p"], u["scenario"]) for u in units} == {(p, str(s)) for p in ("500", "1000") for s in range(1, 7)}
assert {(u["p"], int(u["replicate"])) for u in units} >= {("500", 1), ("500", 100), ("1000", 1), ("1000", 100)}
assert all(u["scale"] in ("c100", "c050") for u in units)
for c in chunks:
    assert c["scales"] == "c100,c050"
    assert (int(c["task"]) <= 600) == (c["p"] == "1000")
    assert c["task"] == str(chunks.index(c) + 1)
order = [(u["dataset_id"], u["scale"]) for u in units]
assert all(order[2 * i][0] == order[2 * i + 1][0] and order[2 * i][1] == "c100" and order[2 * i + 1][1] == "c050" for i in range(1200))
base = {"500": 1410000, "1000": 1510000}
assert all(int(u["data_seed"]) == base[u["p"]] + 10000 * int(u["scenario"]) + int(u["replicate"]) and int(u["method_seed"]) == int(u["data_seed"]) + 4000000 for u in units)
print("PASS: 1200 datasets, 2400 unique units, scale order c100 before c050, p1000 tasks 1-600 / p500 tasks 601-1200, audit seeds (listed for audit only, never passed)")
EOF
[ $? = 0 ] || rc_all=1
$PY -I "$(mixed "$HERE/test_py.py")" "$(mixed "$W")" > "$HERE/py_tests.log" 2>&1; [ $? = 0 ] || rc_all=1
bash "$HERE/test_shell.sh" "$W/shell" > "$HERE/shell_tests.log" 2>&1; [ $? = 0 ] || rc_all=1
cp "$W/shell/SHELL_TESTS.md" "$HERE/SHELL_TESTS.md" 2>/dev/null
rm -rf "$HERE/logs_shell"; mkdir -p "$HERE/logs_shell"; cp "$W"/shell/*.log "$HERE/logs_shell/" 2>/dev/null
"$RSCRIPT" "$(mixed "$HERE/cli_parser.R")" "$(mixed "$B/../../../code/core/v2_2_1/study/run_case.R")" "$(mixed "$HERE/vectors_final.txt")" > "$HERE/cli_parser.log" 2>&1; [ $? = 0 ] || rc_all=1
{ echo "run_all $(date -u +%FT%TZ)"; grep -a -h -E "^(test_py|test_shell):" "$HERE/py_tests.log" "$HERE/shell_tests.log"; grep -h "^PASS: real CLI" "$HERE/cli_parser.log" || echo "FAIL cli_parser"
  echo "syntax: $(grep -c '^PASS' "$HERE/syntax.log") PASS, $(grep -c '^FAIL' "$HERE/syntax.log") FAIL; tables: $(grep -c '^PASS' "$HERE/tables.log") PASS"; echo "overall exit $rc_all"; } > "$HERE/summary.log"
cat "$HERE/summary.log"
exit $rc_all
