// gen.h -- synthetic data generator (ENGINEERING_SPEC §1 row 0; EXPERIMENT_PLAN §2; DECISIONS D-10; OD-14).
// Designs (unit variances; rows iid):
//   IND          x_ij = e_ij
//   AR(rho)      x_i1 = e_i1, x_ij = rho x_i,j-1 + sqrt(1 - rho^2) e_ij   (one sequential recursion over columns)
//   BLK(b, rho)  x_ij = sqrt(rho) f_i,blk(j) + sqrt(1 - rho) e_ij, blocks of b consecutive columns
//   ADJ-OPP      AR(rho) with truths 1 and 2 at adjacent columns (t2 = t1 + 1), beta 1 and -0.8: the marginal effect
//                of truth 2 is -0.8 + rho = -0.2 at rho = 0.6 (manager decision 2026-11-15, recorded here)
// Truth: s0 = 5 truths, k-th at floor((2k - 1) p / 10) (1-based; at least k), later truths shifted to the first column
// of the next block when two share a BLK block; beta = a (1, -0.8, 0.9, -0.7, 0.6); a = 1 strong, 0.6 weak, 0 null
// (S0 empty). y = X beta + sigma eps, sigma = 1.
// Randomness: standard normals by the Marsaglia polar method from Philox addresses (role GEN, key seed = data seed):
// entry (row i, column j) of stream xph uses slots 0, 1, ... (attempts) of address (particle = i, position = j). The
// values depend only on (seed, design, address), never on threads.
// Test rows for any column subset (gen_test): IND and BLK give exactly the values a full test design would have;
// AR / ADJ-OPP use the Markov transition over the sorted subset, x_jk = rho^d x_jk-1 + sqrt(1 - rho^{2d}) e (d = gap),
// equal in law (for the full column set the values equal the full recursion on the test addresses).
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "v4/json.h"

namespace v4::gen {

enum class Design { IND, AR, BLK, ADJOPP };
struct Spec {
  Design design = Design::AR;
  int32_t n = 200, p = 1000, b = 20, s0 = 5;
  double rho = 0.6, a = 1.0, sigma = 1.0;
  uint32_t seed = 1;
};
struct Truth { std::vector<int32_t> S0; std::vector<double> beta; };   // S0 1-based, ascending; beta aligned with S0

Design design_from_name(const std::string& s);
std::string design_name(Design d);
Spec spec_from_json(const Json& j);
Json spec_to_json(const Spec& s);
Truth truth(const Spec& s);
double normal_at(uint32_t seed, uint8_t xph, uint32_t row, uint32_t col);   // polar method on Philox addresses
// Training data: X n x p column-major, y n. Threads over rows (AR) or columns (IND, BLK); bits independent of threads.
void generate(const Spec& s, std::vector<double>& X, std::vector<double>& y);
// ntest test rows on the sorted 1-based column set cols u S0 (returned in out_cols); Xt ntest x |out_cols| col-major.
void generate_test(const Spec& s, int32_t ntest, const std::vector<int32_t>& cols, std::vector<int32_t>& out_cols,
                   std::vector<double>& Xt, std::vector<double>& yt);
// Rows [a, b) of the same test design (global row i uses the address of row i): bit-identical to the corresponding
// rows of generate_test(s, nt >= b, ...); Xt is (b - a) x |out_cols| col-major. For chunked evaluation (WP5).
void generate_test_rows(const Spec& s, int64_t a, int64_t b, const std::vector<int32_t>& cols, std::vector<int32_t>& out_cols,
                        std::vector<double>& Xt, std::vector<double>& yt);
// gen command: writes raw.bin (X_cm, y, meta) and truth.json; returns the record (hashes included).
Json run(const Json& args);
Json run_test(const Json& args);   // writes test.bin (Xt_cm, yt, cols, meta)

}  // namespace v4::gen
