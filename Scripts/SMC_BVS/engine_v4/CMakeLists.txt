# engine_v4 -- large-p SMC-BVS engine (P1M). Contract: INTERFACES.md (v0.1). No network at configure/build time.
cmake_minimum_required(VERSION 3.20)
project(smcbvs4 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
include(cmake/flags.cmake)
# git commit recorded in the binary block: HEAD + "-dirty" (tracked changes), refreshed at every build
# (generated header v4_git.h; only rewritten when the value changes)
set(V4_GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)
file(MAKE_DIRECTORY ${V4_GEN_DIR})
add_custom_target(v4_git_version ALL
  COMMAND ${CMAKE_COMMAND} -DSRC=${CMAKE_CURRENT_SOURCE_DIR} -DOUT=${V4_GEN_DIR}/v4_git.h -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/git_version.cmake
  BYPRODUCTS ${V4_GEN_DIR}/v4_git.h COMMENT "git commit (+dirty) -> v4_git.h")
find_package(OpenMP REQUIRED COMPONENTS CXX)

set(V4_COMMON_SRC
  src/common/sha256.cpp src/common/format.cpp src/common/json.cpp src/common/data.cpp src/common/store.cpp
  src/common/ledger.cpp src/common/status.cpp src/common/score.cpp src/common/provenance.cpp src/common/gen.cpp src/common/prep.cpp src/common/pmath_info.cpp)
set(V4_WP4_SRC src/merge/wp4_io.cpp)   # WP4: calib/island/fit files, merge command (calibrate: v4_cmd, island.cmake)
set(V4_STUB_SRC src/stubs/stubs.cpp)
# WP2 setup (bit library: tables and start law must equal the v3 bits)
set(V4_SETUP_SRC src/setup/corr.cpp src/setup/partition.cpp src/setup/tables.cpp src/setup/start.cpp src/setup/setup_run.cpp src/setup/account.cpp src/setup/setup_island.cpp)
# WP5: evaluator and post (bit flags: they call BitScorer and must reproduce the stored F)
set(V4_WP5_SRC src/eval/posterior.cpp src/eval/model.cpp src/eval/dist.cpp src/eval/metrics.cpp src/eval/io.cpp
  src/eval/run.cpp src/post/law.cpp)

# v4_bit: every kernel that must equal the v3 bits (flags of core/cpp/Makevars.v3).
add_library(v4_bit STATIC ${V4_COMMON_SRC} ${V4_WP4_SRC} ${V4_STUB_SRC} ${V4_WP5_SRC} ${V4_SETUP_SRC})
target_include_directories(v4_bit PUBLIC include PRIVATE ${V4_GEN_DIR})
add_dependencies(v4_bit v4_git_version)
target_compile_options(v4_bit PRIVATE ${V4_BIT_FLAGS} ${V4_WARN})
target_link_libraries(v4_bit PUBLIC OpenMP::OpenMP_CXX m)

# v4_a: class-A kernels (WP3 adds sources). Wider ISA only with -DV4_WIDE_ISA=ON.
add_library(v4_a STATIC src/common/class_a_placeholder.cpp)
target_include_directories(v4_a PUBLIC include)
target_compile_options(v4_a PRIVATE ${V4_A_FLAGS} ${V4_WARN})
target_link_libraries(v4_a PUBLIC v4_bit)

add_executable(smcbvs4 src/cli/main.cpp)
target_compile_options(smcbvs4 PRIVATE ${V4_BIT_FLAGS} ${V4_WARN})
target_link_libraries(smcbvs4 PRIVATE v4_cmd v4_a v4_bit)

option(V4_TESTS "build the test executables" ON)
if(V4_TESTS)
  # v3ref: core/ headers compiled unchanged with the v3 flags (golden comparisons). core/ is never edited.
  set(V3_CORE_CPP ${CMAKE_CURRENT_SOURCE_DIR}/../core/cpp)
  add_executable(v4_tests tests/test_main.cpp tests/test_sha256.cpp tests/test_rng.cpp tests/test_format.cpp
    tests/test_store.cpp tests/test_ledger.cpp tests/test_score.cpp tests/test_gen.cpp tests/test_prep.cpp
    tests/test_pmath.cpp tests/test_cli.cpp tests/test_wp4.cpp tests/test_wp4_io.cpp
    tests/wp5/test_eval.cpp tests/wp5/test_golden_v3.cpp tests/wp5/test_post_e2e.cpp tests/wp5/test_t7.cpp tests/wp5/test_scale.cpp
    tests/test_setup.cpp tests/golden/golden_setup.cpp)
  target_include_directories(v4_tests PRIVATE tests tests/wp5 src ${V3_CORE_CPP})
  target_compile_definitions(v4_tests PRIVATE V3_CORE_CPP_DIR="${V3_CORE_CPP}"
    V4_FIXTURE_DIR="${CMAKE_CURRENT_SOURCE_DIR}/tests/fixtures" V4_SMCBVS4="$<TARGET_FILE:smcbvs4>")
  add_dependencies(v4_tests smcbvs4)
  target_compile_options(v4_tests PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_tests PRIVATE v4_cmd v4_a v4_bit quadmath)
  add_executable(v4_pmath_check tools/pmath_check.cpp)
  target_compile_options(v4_pmath_check PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_pmath_check PRIVATE v4_bit quadmath)
  add_executable(v4_bench_store tools/bench_store.cpp)
  target_compile_options(v4_bench_store PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_bench_store PRIVATE v4_bit)
  add_executable(v4_bench_wp4_fv tools/bench_wp4_fv.cpp)
  target_compile_options(v4_bench_wp4_fv PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_bench_wp4_fv PRIVATE v4_bit)
  add_executable(v4_setup_bench tools/bench_setup.cpp)
  target_include_directories(v4_setup_bench PRIVATE tests src/setup)
  target_compile_options(v4_setup_bench PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_setup_bench PRIVATE v4_bit)
  add_executable(v4_bench_score tools/bench_score.cpp)
  target_compile_options(v4_bench_score PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_bench_score PRIVATE v4_bit)
endif()

include(src/island/island.cmake)   # WP3 island kernel (sources, tests, bench)
