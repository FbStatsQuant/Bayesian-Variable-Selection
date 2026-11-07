#!/usr/bin/env bash
# Compile ONE OR MORE section files in an isolated temp folder (safe while other agents work).
# Usage: bash scripts/check_section.sh sections/02_method.tex [sections/A_notation.tex ...]
# Reports LaTeX errors and dropped glyphs, then runs check.py on those files. The full build
# (scripts/build.sh) is run only by the lead.
set -u
DOC="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="/c/Users/felip/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH"
TMP="$(mktemp -d)"
mkdir -p "$TMP/sections" "$TMP/tables" "$TMP/figures"
cp "$DOC/preamble.tex" "$TMP/"
cp -r "$DOC/tables/." "$TMP/tables/" 2>/dev/null
cp -r "$DOC/figures/." "$TMP/figures/" 2>/dev/null
{
  echo '\documentclass[11pt]{article}'
  echo '\input{preamble}'
  echo '\begin{document}'
  for f in "$@"; do cp "$DOC/$f" "$TMP/$f"; echo "\\input{${f%.tex}}"; done
  echo '\end{document}'
} > "$TMP/main.tex"
cd "$TMP"
for i in 1 2; do lualatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 || break; done
if grep -q '^!' main.log; then echo "LaTeX ERROR:"; grep -m5 -A6 '^!' main.log; else echo "LaTeX OK ($(grep -o 'Output written on main.pdf ([0-9]* pages' main.log | grep -o '[0-9]* pages'))"; fi
grep "Missing character" main.log | sed 's/.*There is no //' | sort | uniq -c | sed 's/^/DROPPED GLYPH: /'
echo "overfull boxes: $(grep -c 'Overfull' main.log)"
cp main.pdf "$DOC/checks/preview_$(basename "${1%.tex}").pdf" 2>/dev/null && echo "preview: checks/preview_$(basename "${1%.tex}").pdf"
cd "$DOC"

python scripts/check.py --files "$@" 2>&1 | grep -v "^C7"
rm -rf "$TMP"
