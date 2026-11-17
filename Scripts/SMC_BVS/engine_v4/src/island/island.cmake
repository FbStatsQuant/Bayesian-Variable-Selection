# island.cmake -- WP3 sources, tests and tools (included from engine_v4/CMakeLists.txt after the WP1 targets).
# Bit form in v4_bit (v3 flags), class A in v4_a (V4_A_FLAGS: x86-64-v3 + FMA intrinsics with -DV4_WIDE_ISA=ON).
# -DV4_ISLAND_ISA=x86-64-v4 overrides -march for the island sources only (AVX-512 on Owls Skylake-SP and NOTS
# Sapphire Rapids; the bit form uses only IEEE + - * / sqrt in vector lanes, so its bits are ISA-independent: the golden
# tests run in every build).
set(V4_ISLAND_ISA "" CACHE STRING "optional -march override for the island sources (e.g. x86-64-v4)")
set(V4_ISLAND_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src/island)
target_sources(v4_bit PRIVATE ${V4_ISLAND_DIR}/island_bit.cpp ${V4_ISLAND_DIR}/island_file.cpp)
target_sources(v4_a PRIVATE ${V4_ISLAND_DIR}/island_a.cpp)
# calib::run (src/calib/calib_run.cpp, in v4_bit) runs the class-A island (v4_a) in V mode: a cycle between two static
# libraries, which CMake resolves by repeating them on the link line
target_link_libraries(v4_bit PUBLIC v4_a)
# every translation unit that calls run_island shares the island's ISA (the kernels live in an ISA inline namespace):
# calib::run (WP4's calibrate command, which runs the calibration islands) and WP4's island-file test included
set(V4_ISLAND_SOURCES ${V4_ISLAND_DIR}/island_bit.cpp ${V4_ISLAND_DIR}/island_a.cpp ${V4_ISLAND_DIR}/island_file.cpp tests/test_island.cpp tests/test_island_golden.cpp tools/bench_island.cpp tools/pilot_island.cpp
    src/calib/calib_run.cpp tests/test_wp4_io.cpp)   # test_wp4_io writes island files (until m9 moves the API types out of the ISA namespace)
# D-32 (WP7 O5): the binary block records the island ISA (provenance.cpp: "island_isa"; "portable" without the option)
set_property(SOURCE src/common/provenance.cpp APPEND PROPERTY COMPILE_DEFINITIONS V4_ISLAND_ISA_STR="${V4_ISLAND_ISA}")
# -Wno-psabi: the 64-byte vector types are passed between inline functions only (no ABI boundary)
if(V4_ISLAND_ISA)
  set_source_files_properties(${V4_ISLAND_SOURCES} PROPERTIES COMPILE_OPTIONS "-march=${V4_ISLAND_ISA};-Wno-psabi")
else()
  set_source_files_properties(${V4_ISLAND_SOURCES} PROPERTIES COMPILE_OPTIONS "-Wno-psabi")
endif()
if(V4_TESTS)
  target_sources(v4_tests PRIVATE tests/test_island.cpp tests/test_island_golden.cpp)
endif()
# the benchmark needs no test dependency (NOTS: -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids)
add_executable(v4_bench_island tools/bench_island.cpp)
target_compile_options(v4_bench_island PRIVATE ${V4_BIT_FLAGS})
target_link_libraries(v4_bench_island PRIVATE v4_a v4_bit)
target_compile_definitions(v4_bench_island PRIVATE V4_ISLAND_ISA_STR="${V4_ISLAND_ISA}")
# the calibration pilot island alone on production inputs (WP7 O5; the H-11 10^6 pilot measurement)
add_executable(v4_pilot_island tools/pilot_island.cpp)
target_compile_options(v4_pilot_island PRIVATE ${V4_BIT_FLAGS})
target_link_libraries(v4_pilot_island PRIVATE v4_a v4_bit)
