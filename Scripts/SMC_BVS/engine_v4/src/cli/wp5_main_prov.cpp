// wp5_main_prov.cpp -- PROVISIONAL CLI until WP1's src/cli/main.cpp exists: `smcbvs4_wp5 eval|post [--key value ...]`.
#include <cstdio>
#include <cstring>

#include "v4/eval.h"
#include "v4/post.h"

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: smcbvs4_wp5 eval|post [--key value ...]\n"); return 10 + (int)v4::Status::invalid_input; }
  if (!std::strcmp(argv[1], "eval")) return v4::eval::run(argc - 1, argv + 1);
  if (!std::strcmp(argv[1], "post")) return v4::post::run(argc - 1, argv + 1);
  std::fprintf(stderr, "unknown command %s\n", argv[1]);
  return 10 + (int)v4::Status::invalid_input;
}
