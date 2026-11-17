// setup_island.cpp -- setup.bin -> island::dep::Start / Neighbours (see v4/setup_island.h).
#include "v4/setup_island.h"
#include "v4/format.h"

namespace v4::setup {

void to_island(const SetupResult& r, const Data& D, island::dep::Start& st, island::dep::Neighbours& nb) {
  const Tables& T = r.tab; const Partition& P = r.part;
  const int J = P.J, K = D.K;
  if (T.K != K || (int)P.blk.size() != D.p) throw Error(Status::invalid_input, "setup: K or p differ from the data");
  st = island::dep::Start();
  st.D = &D; st.J = J;
  st.blocks.assign(J, {});
  for (int b = 0; b < J; ++b) st.blocks[b].assign(P.block(b), P.block(b) + P.size(b));
  st.blk.assign(P.blk.begin(), P.blk.end()); st.pos.assign(P.pos.begin(), P.pos.end());
  st.code_ptr = T.code_ptr; st.logr_flat = T.logr;
  st.logr.assign(J, {}); st.logprof.assign(J, {}); st.codes_by_size.assign(J, {}); st.sub_cum.assign(J, {}); st.cond_cum.assign(J, {});
  std::vector<double> sc;
  for (int b = 0; b < J; ++b) {
    const int m = P.size(b), top = std::min(m, K);
    st.logr[b].assign(T.logr.begin() + T.code_ptr[b], T.logr.begin() + T.code_ptr[b + 1]);
    st.logprof[b].assign(T.logprof.begin() + T.logprof_ptr[b], T.logprof.begin() + T.logprof_ptr[b + 1]);
    st.codes_by_size[b].assign(top + 1, {}); st.sub_cum[b].assign(top + 1, {});
    for (int j = 0; j <= top; ++j) {   // D-18: rebuilt, same values and bits as the sections setup.bin no longer stores
      uint32_t nc; const uint32_t* cs = codes_of_size(m, j, &nc);
      st.codes_by_size[b][j].assign(cs, cs + nc);
      sub_cum_of(T, b, m, j, sc);
      st.sub_cum[b][j] = sc;
    }
    st.cond_cum[b].assign(K + 1, {});   // D-31: dep::Start keeps full rows; rebuilt by cond_row (same bits)
    for (int r0 = 0; r0 <= K; ++r0) cond_row(T, b, r0, st.cond_cum[b][r0]);
  }
  st.logF.assign(J + 1, {});
  for (int b = 0; b <= J; ++b) st.logF[b].assign(T.logF.begin() + (size_t)b * (K + 1), T.logF.begin() + (size_t)(b + 1) * (K + 1));
  st.logZbar0 = T.logZbar0; st.size_logmass = T.size_logmass; st.size_cum = T.size_cum;
  nb.ptr = r.corr.nb.ptr; nb.idx = r.corr.nb.idx;
}

std::string load_for_island(const std::string& setup_path, const Data& D, island::dep::Start& st, island::dep::Neighbours& nb,
                            const std::string& data_hash) {
  std::string h;
  SetupResult r = read_setup_bin(setup_path, &h);
  {
    fmt::Reader rd(setup_path, /*verify=*/false);   // read_setup_bin verified every hash
    Json m = rd.json("meta");
    if (m.at("p").i64() != D.p || m.at("n").i64() != D.n || m.at("K").i64() != D.K)
      throw Error(Status::invalid_input, setup_path + ": n, p or K differ from the data");
    if (!data_hash.empty() && m.at("inputs").at("data.bin").str() != data_hash)
      throw Error(Status::invalid_input, setup_path + ": built from another data.bin (meta.inputs differs)");
  }
  to_island(r, D, st, nb);
  return h;
}

}  // namespace v4::setup
