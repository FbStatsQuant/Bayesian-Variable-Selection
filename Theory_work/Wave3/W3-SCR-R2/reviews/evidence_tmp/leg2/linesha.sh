#!/bin/bash
# usage: linesha.sh <worktree>  -> id, line, sha256 of cited REPORT line for every W3-SCR claims.tsv row
cd "$1"
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) if($i=="status_source") c=i; next} $2=="W3-SCR"{print $1"\t"$c}' Theory_work/INFRA/registry/claims.tsv |
while IFS=$'\t' read id src; do f=${src%%:*}; l=${src##*:}; printf '%s\t%s\t%s\n' "$id" "$src" "$(sed -n "${l}p" "$f" | sha256sum | cut -c1-64)"; done
