// offer_floor.h -- the D-29 offer floor's values and file keys (INTERFACES v0.1.15 §4.1, §5.1, §7; v0.1.17 closes the
// PR45 re-check MINOR-1..4). WP7 O6. Shared by the calib writer (tau_cal), the island (its floor), island_r.bin
// (writer and reader) and the merge check, so all of them read and write the same bits.
//
//   tau_cal  = the c-th best F (c = 40p + 1, the final top-store capacity; HPM order, so the c-th largest F) over the
//              DISTINCT inherited models a completed V-mode calib.bin exports; -inf if there are fewer than c.
//   floor f  = tau_cal for a V-mode final island (offer_floor_from_calib); -inf otherwise and when tau_cal is absent.
//   keys     = calib.bin meta.tau_cal_hex (authoritative bits) + tau_cal (number, "-Inf");
//              island_r.bin meta.offer_floor_hex + offer_floor + offer_floor_calib (null at -inf); absent = -inf.
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include "v4/json.h"
#include "v4/status.h"

namespace v4 {

inline std::string f64_hex(double x) { uint64_t b; std::memcpy(&b, &x, 8); char s[19]; std::snprintf(s, sizeof s, "0x%016llx", (unsigned long long)b); return s; }
inline double f64_of_hex(const std::string& h, const std::string& what) {
  if (h.size() != 18 || h[0] != '0' || h[1] != 'x' || h.find_first_not_of("0123456789abcdefABCDEF", 2) != std::string::npos)
    throw Error(Status::invalid_input, what + ": not a \"0x\" + 16 hex digits f64");
  const uint64_t b = std::strtoull(h.c_str() + 2, nullptr, 16); double x; std::memcpy(&x, &b, 8); return x;
}

// The c-th largest of n finite doubles by a four-pass radix select on the order-preserving 64-bit key (16 bits per pass,
// 65,536 counters): exact, deterministic, O(1) heap (the 512 KiB histogram is thread-local static storage: nothing is
// allocated at call time, so nothing allocates before the island's admission), no copy of the values (review PR54
// re-check: the nth_element copy was ~0.64 GB at 10^6, 8e7 inherited models). -0.0 is folded into +0.0 in the key, so
// +-0 ties are well defined and the result is +0.0 (review PR59 m3). 1 <= c <= n; callers have checked finiteness.
inline double kth_largest_f64(const double* F, size_t n, uint64_t c) {
  auto key = [](double x) { if (x == 0.0) x = 0.0; uint64_t u; std::memcpy(&u, &x, 8); return (u >> 63) ? ~u : (u | 0x8000000000000000ull); };
  static thread_local uint64_t cnt[65536];
  uint64_t prefix = 0, rem = c;   // prefix: the chosen high bits so far; rem: the rank still to find among the keys with that prefix
  for (int shift = 48; shift >= 0; shift -= 16) {
    std::memset(cnt, 0, sizeof cnt);
    const int hi = shift + 16;   // keys whose bits above `shift + 16` equal prefix
    for (size_t i = 0; i < n; ++i) {
      const uint64_t k = key(F[i]);
      if (hi == 64 || (k >> hi) == prefix) ++cnt[(k >> shift) & 0xFFFF];
    }
    int b = 65535; uint64_t acc = 0;
    for (; b > 0; --b) { if (acc + cnt[b] >= rem) break; acc += cnt[b]; }
    rem -= acc; prefix = (prefix << 16) | (uint64_t)b;
  }
  const uint64_t k = prefix; const uint64_t u = (k >> 63) ? (k & 0x7FFFFFFFFFFFFFFFull) : ~k;
  double r; std::memcpy(&r, &u, 8); return r;
}
// tau_cal over the inherited models' F (one value per distinct model): the c-th largest, or -inf if fewer than c
inline double tau_cal_of(const double* F, size_t n, uint64_t c) {
  if (c == 0 || n < c) return -__builtin_huge_val();
  return kth_largest_f64(F, n, c);
}
inline double tau_cal_of(const std::vector<double>& F, uint64_t c) { return tau_cal_of(F.data(), F.size(), c); }
inline void tau_cal_to_meta(Json& meta, double tau) { meta["tau_cal_hex"] = f64_hex(tau); meta["tau_cal"] = tau; }
// calib.bin -> tau_cal (-inf when the key is absent: older files, theory modes, a failed calibration)
inline double tau_cal_of_meta(const Json& meta) {
  if (!meta.contains("tau_cal_hex")) return -__builtin_huge_val();
  const double t = f64_of_hex(meta.at("tau_cal_hex").str(), "calib.bin meta.tau_cal_hex");
  if (std::isnan(t) || t == __builtin_huge_val()) throw Error(Status::invalid_input, "calib.bin meta.tau_cal is NaN or +inf");
  return t;
}

struct OfferFloor { double f = -__builtin_huge_val(); std::string calib; };   // calib: content hash of the calib.bin (empty at -inf)

// MINOR-1: where a final island gets its floor. V-mode final islands read calib.bin meta.tau_cal_hex; every other
// mode, and a calib.bin without tau_cal (fewer than c inherited models, or older), gives -inf.
inline OfferFloor offer_floor_from_calib(const Json& calib_meta, bool v_mode_final, const std::string& calib_content_hash) {
  OfferFloor o;
  if (!v_mode_final) return o;
  o.f = tau_cal_of_meta(calib_meta);
  if (o.f > -__builtin_huge_val()) o.calib = calib_content_hash;
  return o;
}
inline void offer_floor_to_meta(Json& meta, const OfferFloor& o) {
  meta["offer_floor_hex"] = f64_hex(o.f); meta["offer_floor"] = o.f;
  meta["offer_floor_calib"] = o.f > -__builtin_huge_val() ? Json(o.calib) : Json();
}
// island_r.bin meta -> the floor (absent keys = -inf). MINOR-3: NaN and +inf are refused; a floor > -inf names its
// calib.bin. The merge adds the checks that need the calib.bin and the pre-island cut-off (merge.h).
inline OfferFloor offer_floor_of_meta(const Json& meta, const std::string& what) {
  OfferFloor o;
  if (!meta.contains("offer_floor_hex")) return o;
  o.f = f64_of_hex(meta.at("offer_floor_hex").str(), what + ": meta.offer_floor_hex");
  if (std::isnan(o.f) || o.f == __builtin_huge_val()) throw Error(Status::invalid_input, what + ": the offer floor is NaN or +inf");
  if (o.f > -__builtin_huge_val()) {
    if (!meta.contains("offer_floor_calib") || meta.at("offer_floor_calib").type() != Json::STR || meta.at("offer_floor_calib").str().empty())
      throw Error(Status::invalid_input, what + ": an offer floor without offer_floor_calib");
    o.calib = meta.at("offer_floor_calib").str();
  }
  return o;
}

}  // namespace v4
