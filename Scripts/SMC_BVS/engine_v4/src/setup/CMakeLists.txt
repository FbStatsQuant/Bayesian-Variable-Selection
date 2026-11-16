# WP2 setup sources. Integration: WP1's top-level CMakeLists adds V4_SETUP_SOURCES to the v4_bit library (bit flags)
# and tests/test_setup.cpp + tests/golden/golden_setup.cpp to v4_tests. Until then this file also builds standalone:
#   cmake -S src/setup -B build && make -C build -j3   (see tests/run_setup_tests.sh)
cmake_minimum_required(VERSION 3.20)
set(V4_SETUP_SOURCES
  ${CMAKE_CURRENT_LIST_DIR}/corr.cpp
  ${CMAKE_CURRENT_LIST_DIR}/partition.cpp
  ${CMAKE_CURRENT_LIST_DIR}/tables.cpp
  ${CMAKE_CURRENT_LIST_DIR}/start.cpp
  ${CMAKE_CURRENT_LIST_DIR}/setup_run.cpp)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
  project(v4_setup_standalone CXX)
  set(CMAKE_CXX_STANDARD 20)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
  endif()
  # the v3 bit flags (core/cpp/Makevars.v3); wide ISA only on request (lane-wise sums: same bits, no FMA)
  set(V4_BIT_FLAGS -O2 -fno-math-errno -ffp-contract=off)
  option(V4_WIDE_ISA "x86-64-v3 for the bit library (no FMA contraction; same bits)" OFF)
  if(V4_WIDE_ISA)
    list(APPEND V4_BIT_FLAGS -march=x86-64-v3)
  else()
    list(APPEND V4_BIT_FLAGS -march=x86-64-v2)
  endif()
  set(CMAKE_CXX_FLAGS_RELEASE "")
  find_package(OpenMP REQUIRED)
  set(ENGINE ${CMAKE_CURRENT_SOURCE_DIR}/../..)
  set(CORE_CPP ${ENGINE}/../core/cpp)

  add_library(v4_setup STATIC ${V4_SETUP_SOURCES})
  target_include_directories(v4_setup PUBLIC ${ENGINE}/include ${CMAKE_CURRENT_SOURCE_DIR})
  target_compile_options(v4_setup PRIVATE ${V4_BIT_FLAGS} -Wall -Wextra -Wno-unused-parameter)
  target_link_libraries(v4_setup PUBLIC OpenMP::OpenMP_CXX)

  # unit tests + T11 + invariance; golden tests include core/ headers unchanged, compiled with the v3 flags (v3ref)
  add_executable(v4_setup_tests ${ENGINE}/tests/test_setup.cpp ${ENGINE}/tests/golden/golden_setup.cpp ${ENGINE}/tests/setup_main.cpp)
  target_include_directories(v4_setup_tests PRIVATE ${ENGINE}/tests ${CORE_CPP})
  target_compile_options(v4_setup_tests PRIVATE ${V4_BIT_FLAGS} -Wall -Wno-unused-parameter -Wno-unused-variable -Wno-sign-compare)
  target_link_libraries(v4_setup_tests PRIVATE v4_setup)

  add_executable(v4_setup_bench ${ENGINE}/tests/bench_setup.cpp)
  target_include_directories(v4_setup_bench PRIVATE ${ENGINE}/tests)
  target_compile_options(v4_setup_bench PRIVATE ${V4_BIT_FLAGS})
  target_link_libraries(v4_setup_bench PRIVATE v4_setup)
endif()
