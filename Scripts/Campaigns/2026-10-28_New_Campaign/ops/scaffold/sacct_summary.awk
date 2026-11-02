# sacct_summary.awk : per JobName from a pipe-separated sacct_final.tsv: tasks, AllocCPUS, summed core-hours (AllocCPUS x Elapsed, parent rows),
# max and mean task elapsed (s), max batch-step MaxRSS (MB). Usage: awk -F'|' -f sacct_summary.awk sacct_final.tsv
function secs(t,   d, a, n) { d = 0; if (index(t, "-")) { split(t, a, "-"); d = a[1]; t = a[2] } n = split(t, a, ":"); if (n == 3) return d*86400 + a[1]*3600 + a[2]*60 + a[3]; if (n == 2) return a[1]*60 + a[2]; return t + 0 }
function mb(r,   v, u) { if (r == "") return 0; u = substr(r, length(r)); v = substr(r, 1, length(r) - 1) + 0; if (u == "K") return v/1024; if (u == "M") return v; if (u == "G") return v*1024; return r/1048576 }
NR == 1 { next }
$1 !~ /\./ { name[$1] = $2; s = secs($9); n[$2]++; cpus[$2] = $6; ch[$2] += $6 * s / 3600; tot += $6 * s / 3600; if (s > mx[$2]) mx[$2] = s; sm[$2] += s; next }
$1 ~ /\.batch$/ { split($1, a, "."); j = a[1]; m = mb($12); if (m > rss[name[j]]) rss[name[j]] = m }
END { printf "%-20s %6s %5s %10s %10s %10s %10s\n", "JobName", "tasks", "cpus", "core_h", "max_el_s", "mean_el_s", "maxRSS_MB"
      for (k in n) printf "%-20s %6d %5d %10.3f %10d %10.1f %10.1f\n", k, n[k], cpus[k], ch[k], mx[k], sm[k]/n[k], rss[k]
      printf "TOTAL core-hours (AllocCPUS x Elapsed): %.3f\n", tot }
