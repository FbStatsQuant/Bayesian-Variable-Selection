// v4/setup_island.h -- setup.bin -> the island's inputs (WP3 `island::dep::Start`, `island::dep::Neighbours`; WP4's
// calibration uses the same). The tables, start law and neighbour graph are WP2's bits, read back from setup.bin; the
// arrays setup.bin does not store (D-18: codes_by_size, sub_cum) are rebuilt with the same values and bits
// (codes of popcount j in increasing order; cumulative_from_logs of their logr; core/cpp/v3_start.h:101-118).
// Memory note: dep::Start keeps per-block vectors, logr twice (logr and logr_flat) and the D-18 arrays for every block
// (about 28 B per table code instead of 8); at p = 10^6 that is about 25-32 GB (ESTIMATE). The flat v4::setup::Start
// (v4/setup.h; on-demand D-18) is the intended production form.
#pragma once
#include <string>
#include "v4/island/dep.h"
#include "v4/setup.h"

namespace v4::setup {
// Reads setup.bin (verifying every section hash) and fills st (st.D = &D) and nb. Refuses (invalid_input) if the file's
// p, K or n differ from D, or if data_hash is given and differs from the file's meta.inputs["data.bin"].
// Returns setup.bin's content hash.
std::string load_for_island(const std::string& setup_path, const Data& D, island::dep::Start& st, island::dep::Neighbours& nb,
                            const std::string& data_hash = "");
// The same from an in-memory SetupResult (tests; no file).
void to_island(const SetupResult& r, const Data& D, island::dep::Start& st, island::dep::Neighbours& nb);
}  // namespace v4::setup
