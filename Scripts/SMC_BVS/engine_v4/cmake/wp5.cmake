# wp5.cmake -- WP5 targets (eval, post). Included by the engine's top-level CMakeLists.txt (WP1) or by the provisional
# standalone project tests/wp5/CMakeLists.txt until the WP1 skeleton is on exp/P1M-engine.
# Flags: the v3 flags for everything in WP5 (score_bit.cpp must equal the v3 scorer's bits; the rest is cheap).
set(V4_WP5_ROOT ${CMAKE_CURRENT_LIST_DIR}/..)
find_package(OpenMP REQUIRED)
set(V4_WP5_FLAGS -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2)
add_library(v4_wp5 STATIC
  ${V4_WP5_ROOT}/src/eval/prov/prov.cpp
  ${V4_WP5_ROOT}/src/eval/prov/json.cpp
  ${V4_WP5_ROOT}/src/eval/score_bit.cpp
  ${V4_WP5_ROOT}/src/eval/model.cpp
  ${V4_WP5_ROOT}/src/eval/dist.cpp
  ${V4_WP5_ROOT}/src/eval/metrics.cpp
  ${V4_WP5_ROOT}/src/eval/io.cpp
  ${V4_WP5_ROOT}/src/eval/run.cpp
  ${V4_WP5_ROOT}/src/post/law.cpp)
target_include_directories(v4_wp5 PUBLIC ${V4_WP5_ROOT}/include)
target_compile_options(v4_wp5 PRIVATE ${V4_WP5_FLAGS} -Wall -Wextra)
target_compile_features(v4_wp5 PUBLIC cxx_std_20)
target_link_libraries(v4_wp5 PUBLIC OpenMP::OpenMP_CXX)

# provisional CLI (WP1's smcbvs4 main dispatches `eval` / `post` to v4::eval::run / v4::post::run)
add_executable(smcbvs4_wp5 ${V4_WP5_ROOT}/src/cli/wp5_main_prov.cpp)
target_compile_options(smcbvs4_wp5 PRIVATE ${V4_WP5_FLAGS})
target_link_libraries(smcbvs4_wp5 PRIVATE v4_wp5)

# tests: unit + golden (core/ headers compiled unchanged with the v3 flags) + gate T7
set(V4_CORE_CPP ${V4_WP5_ROOT}/../core/cpp)
add_executable(v4_wp5_tests
  ${V4_WP5_ROOT}/tests/wp5/test_main.cpp
  ${V4_WP5_ROOT}/tests/wp5/test_prov.cpp
  ${V4_WP5_ROOT}/tests/wp5/test_eval.cpp
  ${V4_WP5_ROOT}/tests/wp5/test_golden_v3.cpp
  ${V4_WP5_ROOT}/tests/wp5/test_post_e2e.cpp
  ${V4_WP5_ROOT}/tests/wp5/test_t7.cpp)
target_include_directories(v4_wp5_tests PRIVATE ${V4_WP5_ROOT}/src ${V4_WP5_ROOT}/tests/wp5 ${V4_CORE_CPP})
target_compile_options(v4_wp5_tests PRIVATE ${V4_WP5_FLAGS})
target_link_libraries(v4_wp5_tests PRIVATE v4_wp5)
