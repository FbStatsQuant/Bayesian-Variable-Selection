// test_main.cpp -- runs every registered WP5 test; `--quick` skips the slow ones (gate T7 runs in full mode only).
#include <chrono>
#include <cstring>

#include "wp5_tk.h"

int main(int argc, char** argv) {
  const char* only = nullptr;
  for (int i = 1; i < argc; ++i) {
    if (!std::strcmp(argv[i], "--quick")) tk::quick() = true;
    else if (!std::strcmp(argv[i], "--only") && i + 1 < argc) only = argv[++i];
  }
  int ran = 0, skipped = 0;
  for (auto& c : tk::registry()) {
    if (only && !std::strstr(c.name, only)) continue;
    if (c.slow && tk::quick()) { ++skipped; continue; }
    int f0 = tk::failures();
    auto t0 = std::chrono::steady_clock::now();
    std::printf("[ RUN  ] %s\n", c.name); std::fflush(stdout);
    try { c.fn(); } catch (const std::exception& e) { tk::fail(__FILE__, __LINE__, std::string("exception: ") + e.what()); }
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("[ %s ] %s (%.2f s)\n", tk::failures() == f0 ? " OK " : "FAIL", c.name, s); std::fflush(stdout);
    ++ran;
  }
  std::printf("\n%d tests run, %d skipped, %d check failures\n", ran, skipped, tk::failures());
  return tk::failures() ? 1 : 0;
}
