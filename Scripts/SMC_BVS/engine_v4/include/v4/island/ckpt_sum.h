// ckpt_sum.h -- the checkpoint checksum (WP7 O4; WP3_ARCH_REVIEW R5). A serial FNV-1a byte loop costs ~1 ns per byte:
// 10-13 s per checkpoint (and again on every resume) for a 10 GB store of pi_0-sized models. This checksum is a function of
// the byte stream alone, and is computed in parallel:
//   * the stream is cut into fixed 1 MiB blocks by POSITION (block i = bytes [i * 2^20, (i + 1) * 2^20), the last one short);
//   * every block gets an FNV-1a 64 hash of its bytes (independent: any thread, any order);
//   * the checksum = FNV-1a 64 over (total length, block hash 0, block hash 1, ...) in block order.
// So it does not depend on the number of threads, on how the writer cut the stream into write() calls, or on the reader's
// buffer size: BlockSum::add may be fed any chunking, and the whole-region form of_region (a test and mapped-file helper:
// the engine itself streams) gives the same value (tested).
#pragma once
#include <omp.h>
#include <cstdint>
#include <cstring>
#include <vector>

namespace v4::island {

struct BlockSum {
  static constexpr size_t B = (size_t)1 << 20;
  int threads = 1;
  explicit BlockSum(int t = 1) : threads(t < 1 ? 1 : t) {}

  static uint64_t fnv_block(const unsigned char* c, size_t n) {
    uint64_t h = 0xcbf29ce484222325ULL;
    for (size_t i = 0; i < n; ++i) { h ^= c[i]; h *= 0x100000001b3ULL; }
    return h;
  }
  static uint64_t combine(const std::vector<uint64_t>& bh, uint64_t total) {
    uint64_t h = 0xcbf29ce484222325ULL;
    auto mix = [&](uint64_t x) { const unsigned char* c = (const unsigned char*)&x; for (int i = 0; i < 8; ++i) { h ^= c[i]; h *= 0x100000001b3ULL; } };
    mix(total);
    for (uint64_t x : bh) mix(x);
    return h;
  }

  // streaming: add(...) any number of times, then finish()
  void add(const void* q, size_t n) {
    const unsigned char* c = (const unsigned char*)q;
    total_ += n;
    if (fill_) {   // complete the partial block first
      const size_t take = n < B - fill_ ? n : B - fill_;
      buf_.resize(B); std::memcpy(buf_.data() + fill_, c, take); fill_ += take; c += take; n -= take;
      if (fill_ == B) { bh_.push_back(fnv_block(buf_.data(), B)); fill_ = 0; }
    }
    const size_t nb = n / B;   // whole blocks straight from the caller's memory, in parallel
    if (nb) {
      const size_t base = bh_.size(); bh_.resize(base + nb);
      uint64_t* out = bh_.data() + base;
      if (nb >= 2 && threads > 1) {
        #pragma omp parallel for num_threads(threads) schedule(static)
        for (long long i = 0; i < (long long)nb; ++i) out[i] = fnv_block(c + (size_t)i * B, B);
      } else {
        for (size_t i = 0; i < nb; ++i) out[i] = fnv_block(c + i * B, B);
      }
      c += nb * B; n -= nb * B;
    }
    if (n) { buf_.resize(B); std::memcpy(buf_.data() + fill_, c, n); fill_ += n; }
  }
  uint64_t finish() {
    if (fill_) { bh_.push_back(fnv_block(buf_.data(), fill_)); fill_ = 0; }
    return combine(bh_, total_);
  }
  uint64_t length() const { return total_; }

  // a whole region at once (a mapped file)
  static uint64_t of_region(const unsigned char* p, uint64_t len, int threads) {
    const size_t nb = (size_t)((len + B - 1) / B);
    std::vector<uint64_t> bh(nb);
    #pragma omp parallel for num_threads(threads < 1 ? 1 : threads) schedule(static) if (nb >= 2 && threads > 1)
    for (long long i = 0; i < (long long)nb; ++i) {
      const uint64_t lo = (uint64_t)i * B, hi = lo + B < len ? lo + B : len;
      bh[(size_t)i] = fnv_block(p + lo, (size_t)(hi - lo));
    }
    return combine(bh, len);
  }

 private:
  std::vector<uint64_t> bh_; std::vector<unsigned char> buf_; size_t fill_ = 0; uint64_t total_ = 0;
};

}  // namespace v4::island
