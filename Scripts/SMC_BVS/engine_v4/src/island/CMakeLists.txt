# WP3 island kernel. Stand-alone project for now (WP1's engine_v4/CMakeLists.txt adds it with add_subdirectory).
#   cmake -S src/island -B build-island [-DV4_ISLAND_ISA=x86-64-v4]
cmake_minimum_required(VERSION 3.20)
project(v4_island CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
find_package(OpenMP REQUIRED)
# ISA: x86-64-v2 by default (INTERFACES §1). x86-64-v4 (AVX-512, Owls Skylake-SP and NOTS Sapphire Rapids) is the
# measured wide build; the bit-form kernel uses only IEEE + - * / sqrt in vector lanes, so its bits do not depend on the
# ISA (golden-tested in each build); class A uses FMA when the ISA has it.
set(V4_ISLAND_ISA "x86-64-v2" CACHE STRING "-march value for the island kernels")
set(V4_ENGINE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../..)
set(V4_CORE_DIR ${V4_ENGINE_DIR}/../core/cpp)
# v3 flags (core/cpp/Makevars.v3) for everything: FMA only through explicit intrinsics.
set(V4_FLAGS -O2 -fno-math-errno -ffp-contract=off -march=${V4_ISLAND_ISA} -Wall -Wno-psabi)
add_library(v4_island STATIC island_bit.cpp island_a.cpp)
target_include_directories(v4_island PUBLIC ${V4_ENGINE_DIR}/include)
target_compile_options(v4_island PRIVATE ${V4_FLAGS})
target_link_libraries(v4_island PUBLIC OpenMP::OpenMP_CXX)

add_executable(test_island ${V4_ENGINE_DIR}/tests/test_island.cpp)
target_include_directories(test_island PRIVATE ${V4_ENGINE_DIR}/tests)
target_compile_options(test_island PRIVATE ${V4_FLAGS})
target_link_libraries(test_island PRIVATE v4_island)

# golden: core/ headers compiled unchanged with the v3 flags against the island
add_executable(test_island_golden ${V4_ENGINE_DIR}/tests/test_island_golden.cpp)
target_include_directories(test_island_golden PRIVATE ${V4_ENGINE_DIR}/tests ${V4_CORE_DIR})
target_compile_options(test_island_golden PRIVATE ${V4_FLAGS})
target_link_libraries(test_island_golden PRIVATE v4_island)

add_executable(bench_island ${V4_ENGINE_DIR}/tools/bench_island.cpp)
target_compile_options(bench_island PRIVATE ${V4_FLAGS})
target_link_libraries(bench_island PRIVATE v4_island)
