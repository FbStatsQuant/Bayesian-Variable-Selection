// island_a.cpp -- Arith::ClassA instantiation (V-1M: bordered update, FMA when the ISA has it, vector log/exp).
#include "island_impl.h"
namespace v4::island {
template IslandResult run_island<Arith::ClassA>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
}
