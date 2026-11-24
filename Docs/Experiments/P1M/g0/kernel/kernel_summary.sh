#!/usr/bin/env bash
# kernel_summary.sh -- P1M G0 Part K read-back: kernel.log (g0_bench suite output) -> one TSV on stdout.
# Usage: bash kernel_summary.sh kernel.log > g0_kernel.tsv
# Columns: section, T, item, value, unit. Items:
#   batch_<sup>_v<variant>   thread-time ns per (support,label) and wall*T/scores; sup = distinct256 | S0 | S0plus1
#   batch_..._mism           bit/agreement check mismatches "m of n" (T = 1 only)
#   direct                   ns per step per thread (+ mismatches at T = 1)
#   perm                     Fisher-Yates + inverse ns per label per thread
#   bw                       GB/s
#   pass_<sup>_D<Delta>      share of scores with F(S u j) - F(S) >= -Delta
#   offer_<kind>             ns per offer per thread (store of c/T per thread)
set -euo pipefail
awk '
function sup(G, div, k) { return (div == 1) ? "distinct256" : ((k == 6) ? "S0plus1" : "S0") }
/^==== T = / { T = $4; sec = "run" }
/^==== pass fractions/ { sec = "pass" }
/^==== store offers/ { sec = "offer" }
/^batch p=/ { for (i = 1; i <= NF; i++) { split($i, kv, "="); a[kv[1]] = kv[2] }
  bt = a["threads"]; key = "batch_" sup(a["G"], a["div"], a["k"]) "_v" a["variant"] }
/^  total .* per \(support,label\) thread-time/ { if (sec == "run") { print sec "\t" bt "\t" key "\t" $2 "\tns_thread"
  for (i = 1; i <= NF; i++) if ($i == "WALL-BASED") print sec "\t" bt "\t" key "\t" $(i+1) "\tns_wallxT" } }
/^  accepts / { if (sec == "run") { for (i = 1; i <= NF; i++) if ($i == "mismatches") print sec "\t" bt "\t" key "_mism\t" $(i+1) "/" $(i+3) "\tcount"
  print sec "\t" bt "\t" key "_accept_per_score\t" substr($3, 2) "\tratio" } }
/^  PASS fractions/ { for (i = 1; i <= NF; i++) if ($i ~ /^Delta=/) { d = substr($i, 7); sub(":", "", d); print "pass\t" bt "\tpass_" substr(key, 7) "_D" d "\t" $(i+1) "\tshare" } }
/^direct p=/ { for (i = 1; i <= NF; i++) { if ($i ~ /^threads=/) { split($i, kv, "="); dt = kv[2] } if ($i == "ns/step") v = $(i-1); if ($i == "mismatches") m = $(i+4) "/" $(i+6) }
  print "run\t" dt "\tdirect\t" v "\tns_step_thread"; print "run\t" dt "\tdirect_mism\t" m "\tcount" }
/^perm p=/ { for (i = 1; i <= NF; i++) if ($i ~ /^threads=/) { split($i, kv, "="); pt = kv[2] }
  match($0, /fisher_yates [0-9.]+ ms \(([0-9.]+)/, f); match($0, /inverse [0-9.]+ ms \(([0-9.]+)/, g)
  print "run\t" pt "\tperm_fy\t" f[1] "\tns_label_thread"; print "run\t" pt "\tperm_inv\t" g[1] "\tns_label_thread" }
/^bw threads=/ { split($2, kv, "="); for (i = 1; i <= NF; i++) if ($i ~ /^read_GBps=/) { split($i, g, "="); print "run\t" kv[2] "\tbw\t" g[2] "\tGBps" } }
/^offer cap=/ { split($3, kv, "="); ot = kv[2] }
/^  FILL / { sub(/ \[chk.*$/, ""); n = split($0, parts, "|"); for (i = 1; i <= n; i++) { s = parts[i]; gsub(/^ +| +$/, "", s); m = split(s, w, " ");
    nm = w[1]; if (nm ~ /^MIX/) { nm = (i == 6) ? "MIX_pi0.01" : "MIX_pi0.10" } print "offer\t" ot "\toffer_" nm "\t" w[m] "\tns_offer_thread" } }
' "$1"
