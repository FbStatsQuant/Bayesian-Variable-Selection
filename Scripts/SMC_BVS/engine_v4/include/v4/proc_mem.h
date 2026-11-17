// proc_mem.h -- this process's resident memory (Linux only: /proc/self/smaps_rollup when it exists, else /proc/self/status; -1
// elsewhere), for phase records. Review: the first 1M
// merge peaked at 75.1 GiB against a plan of 43.7 GiB; the merge now records its phases (seconds and RSS) in fit.bin's
// meta.timings so the next fit shows where the memory and the time go.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <chrono>
#include <sys/resource.h>
#include <string>
#include <vector>

namespace v4 {
struct ProcMem { int64_t rss_kb = -1, anon_kb = -1, file_kb = -1, hwm_kb = -1; };   // -1 = not available (non-Linux)
// rss / anon / file from /proc/self/smaps_rollup (exact sums over the mappings; file = Rss - Anonymous) when the kernel has it, else
// from /proc/self/status (RssAnon / RssFile / VmRSS: per-thread counters, approximate by the kernel's own documentation, so a
// release can show up one phase late). hwm = VmHWM (status). Linux only; -1 where unavailable.
inline ProcMem proc_mem() {
  ProcMem m;
  bool rolled = false;
  if (FILE* f = std::fopen("/proc/self/smaps_rollup", "r")) {
    char line[256]; int64_t rss = -1, anon = -1;
    while (std::fgets(line, sizeof line, f)) {
      if (std::strncmp(line, "Rss:", 4) == 0) rss = std::strtoll(line + 4, nullptr, 10);
      else if (std::strncmp(line, "Anonymous:", 10) == 0) anon = std::strtoll(line + 10, nullptr, 10);
    }
    std::fclose(f);
    if (rss >= 0 && anon >= 0) { m.rss_kb = rss; m.anon_kb = anon; m.file_kb = rss - anon; rolled = true; }
  }
  if (FILE* f = std::fopen("/proc/self/status", "r")) {
    char line[256];
    while (std::fgets(line, sizeof line, f)) {
      auto kb = [&](const char* key, int64_t& dst) { const size_t n = std::strlen(key); if (std::strncmp(line, key, n) == 0) dst = std::strtoll(line + n, nullptr, 10); };
      if (!rolled) { kb("VmRSS:", m.rss_kb); kb("RssAnon:", m.anon_kb); kb("RssFile:", m.file_kb); }
      kb("VmHWM:", m.hwm_kb);
    }
    std::fclose(f);
  }
  return m;
}
// The process's peak resident set (kB): getrusage(RUSAGE_SELF).ru_maxrss, kB on Linux; -1 if the call fails.
inline int64_t peak_rss_kb_now() {
  struct rusage ru {};
  return getrusage(RUSAGE_SELF, &ru) == 0 ? (int64_t)ru.ru_maxrss : -1;
}
// One sample per phase boundary: wall seconds since the recorder started and the memory at that point.
struct PhaseSample { std::string phase; double t = 0; ProcMem mem; };
struct PhaseLog {
  std::chrono::steady_clock::time_point t0 = std::chrono::steady_clock::now();
  std::vector<PhaseSample> v;
  void mark(const std::string& phase) { v.push_back({phase, std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count(), proc_mem()}); }
  int64_t peak_kb() const { int64_t m = -1; for (const auto& s : v) m = s.mem.hwm_kb > m ? s.mem.hwm_kb : m; return m; }
};
}  // namespace v4
