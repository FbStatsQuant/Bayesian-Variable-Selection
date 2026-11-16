// island_bit.cpp -- Arith::Bit instantiation (theory mode T: the v3 scorer's bits). Built with the v3 flags.
#define V4_ISLAND_DEFINE_COMMON
#include "island_impl.h"
namespace v4::island {
template IslandResult run_island<Arith::Bit>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
}
