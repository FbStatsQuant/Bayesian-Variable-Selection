#!/usr/bin/env bash
# Build the State of Project PDF and run all checks. Run from anywhere (Git Bash on Windows with MiKTeX).
set -u
DOC="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DOC"
export PATH="/c/Users/felip/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH"
PY="${PYTHON:-python}"

echo "== generate tables"
[ -f scripts/make_tables.py ] && "$PY" scripts/make_tables.py || echo "(no make_tables.py yet or it failed)"
"$PY" scripts/registry_to_tex.py

echo "== lualatex (3 passes)"
for i in 1 2 3; do
  lualatex -interaction=nonstopmode -halt-on-error main.tex > build_pass$i.out 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "lualatex pass $i failed (rc=$rc); see main.log"; grep -m5 -A4 '^!' main.log; break; fi
done
rm -f build_pass*.out

echo "== checks"
"$PY" scripts/check.py --log main.log "$@"
[ -f main.pdf ] && cp main.pdf "State_of_Project_$(grep -o 'sopversion}{[^}]*' preamble.tex | cut -d'{' -f2).pdf"
ls -la *.pdf 2>/dev/null
