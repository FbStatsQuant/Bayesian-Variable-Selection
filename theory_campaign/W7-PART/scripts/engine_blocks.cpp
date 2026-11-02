// Driver around the UNMODIFIED engine header Scripts/SMC_BVS/core/cpp/v3_blocks.h.
// Reads (p, B, then p*p doubles of the Gram matrix G column-major) from a binary file, runs v3::make_blocks,
// writes one line per block (0-based internal indices), in packing order. Only D.p and D.G are read by
// correlation_matrix/complete_linkage/make_blocks.
#include "../../../Scripts/SMC_BVS/core/cpp/v3_blocks.h"
#include <cstdio>
int main(int argc, char** argv) {
  FILE* f = std::fopen(argv[1], "rb");
  int hdr[2];
  if (std::fread(hdr, sizeof(int), 2, f) != 2) return 2;
  v3::Data D; D.p = hdr[0]; int B = hdr[1];
  D.G.resize((size_t)D.p * D.p);
  if (std::fread(D.G.data(), sizeof(double), D.G.size(), f) != D.G.size()) return 3;
  std::fclose(f);
  auto blocks = v3::make_blocks(D, B);
  for (auto& b : blocks) { for (size_t i = 0; i < b.size(); ++i) std::printf(i ? " %d" : "%d", b[i]); std::printf("\n"); }
  return 0;
}
