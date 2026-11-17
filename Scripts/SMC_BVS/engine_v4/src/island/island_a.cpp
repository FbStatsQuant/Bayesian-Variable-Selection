// island_a.cpp -- Arith::ClassA instantiation (V-1M: bordered update, FMA when the ISA has it, vector log/exp).
#include "island_impl.h"
namespace v4::island {
template IslandRun run_island<Arith::ClassA>(const Data&, const Start&, const Neighbours&, const IslandConfig&);
}
// D-32 (review PR55 m4): whether class A's fma8 is a true fused multiply-add in THIS build (the class-A flags and the
// island -march decide it, e.g. -DV4_WIDE_ISA=ON gives x86-64-v3 without an island ISA). Read by the binary block
// (provenance.cpp, weak reference: binaries without the class-A library have no "island_fma").
extern "C" int v4_class_a_fma() { return v4::island::kHasFMA() ? 1 : 0; }
