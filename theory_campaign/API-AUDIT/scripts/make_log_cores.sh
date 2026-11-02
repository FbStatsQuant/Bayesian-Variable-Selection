#!/usr/bin/env bash
# Instrumented copies core_fp_log / core_ld_log (from core_fp / core_ld built by make_cores.sh). During cpp_final_run
# only (and only if env V3_THR_LOG is set) every threshold that a uniform is compared with is appended to a binary
# file as (int32 tag, long double value):
#   1 Gibbs o_j (include iff u < o_j)       2 uniform-swap alpha     3 neighbour-swap alpha   4 independence alpha
#   8 N (before each resampling)  5 the N normalised cumulative weights W_k (ancestor = smallest k with W_k >= u)
#   6 cum[k], 7 cum[k-1] for every pi_0 categorical draw (k = smallest index with cum[k] > u)
# No arithmetic or draw of the engine is changed; the logging only reads values.
set -euo pipefail
W=${1:-$HOME/api_audit_work}
for v in fp ld; do
  rm -rf "$W/core_${v}_log"; cp -r "$W/core_$v" "$W/core_${v}_log"; rm -rf "$W/core_${v}_log/.cpp_cache"
  cd "$W/core_${v}_log/cpp"
  cat >> v3_util.h <<'CPP'
#include <cstdio>
#include <cstdlib>
namespace v3 {
inline FILE*& thr_file() { static FILE* f = nullptr; return f; }
inline void thr_log(int tag, long double x) {
  FILE* f = thr_file(); if (f) { std::fwrite(&tag, sizeof(int), 1, f); std::fwrite(&x, sizeof(long double), 1, f); }
}
}  // namespace v3
CPP
  perl -pi -e 's/bool include = u < oj;/thr_log(1, oj); bool include = u < oj;/;
               s/(vs->u\("uswap_accept"\);)/$1 thr_log(2, alpha);/;
               s/(vs->u\("nswap_accept"\);)/$1 thr_log(3, alpha);/;
               s/(vs->u\("indep_accept"\);)/$1 thr_log(4, alpha);/;
               s/(W\[N - 1\] = 1\.0;)/$1 thr_log(8, N); for (int i_ = 0; i_ < N; ++i_) thr_log(5, W[i_]);/' v3_engine.h
  perl -pi -e 's/return \(int\)\(std::upper_bound\(cum\.begin\(\), cum\.end\(\), u\) - cum\.begin\(\)\);/int k_ = (int)(std::upper_bound(cum.begin(), cum.end(), u) - cum.begin()); if (k_ < (int)cum.size()) { thr_log(6, cum[k_]); thr_log(7, k_ > 0 ? (long double)cum[k_ - 1] : 0.0L); } return k_;/' v3_start.h
  perl -pi -e 's/(^\s*Ledger led\(&D, o\.islands\);)/$1 { const char* fn_ = std::getenv("V3_THR_LOG"); if (fn_) thr_file() = std::fopen(fn_, "wb"); }/;
               s/(^\s*)(List out = List::create\(_\["status"\] = status, _\["message"\])/$1if (thr_file()) { std::fclose(thr_file()); thr_file() = nullptr; }\n$1$2/' v3_core.cpp
  n=$(grep -c "thr_log(" v3_engine.h v3_start.h | awk -F: '{s+=$2} END {print s}'); m=$(grep -c "thr_file()" v3_core.cpp)
  echo "$v: thr_log lines $n, thr_file lines $m"
done
