# CODE_LEDGER (one tree, ledgered)

## 2026-10-28 — v2.2 core

Author: Terra (CONF). Base: v2.1 production byte-identical reference; SHA256SUMS below (also saved in `conformance/work/impl_smoke/SHA256SUMS_v2_1_baseline`).

Files changed: `core/cpp/v3_registry.h`, `core/cpp/v3_ledger.h`, `core/cpp/v3_engine.h`, `core/cpp/v3_core.cpp`, `core/v3_calib.R`, `core/v3_run.R`, `core/v3_fit.R`, `core/README.md`, `study/adapter.R`, `study/SCHEMA.md`. Purpose: P1 plain PIPs, P2a scored-model registry, P2b instrumentation, and study adapter additions. Invariants claimed: no added random draws or decision changes; pre-existing outputs preserved except timing/memory/provenance; existing list elements retain order; CSV schema unchanged. Diff: `code/core/v2_2.diff`. Status: implemented; regression pending.

```text
61984bf960fd53481d14bb35182910eef72b54ab243759fcc84fe1f075c12894  core/cpp/Makevars.v3
ca8aeb341b6031fe9f3e80f49697efb2d8a1a1ed79fdc6023c0bc5df1ed7abc0  core/cpp/v3_blocks.h
e9ad470bfe82548bdcdef11c57ec4bbff48401ba57d82468ca294c41c4ec2c7e  core/cpp/v3_calib.h
64c0a38c569f0abc673111896ca084bac45b26530f2e50a041e4e986d75324e4  core/cpp/v3_core.cpp
0a0b95ab126bc23b96cb48589fee979e7b03d238c55ee476b1d62785e9bda462  core/cpp/v3_engine.h
1f83b80e2203a102b175713a3d1c4834da298997b3a1e187a4d7376e138d4f27  core/cpp/v3_holder.h
7641811d73e635bf7176ec76be1c6655b60b2b2fb560453c4d7dc328d7b319a7  core/cpp/v3_ledger.h
f28e73c129bab7349b165a6d648cdbadd094bd08bf05416df377cf52f57c4a8c  core/cpp/v3_runtime.h
41173ac1460e180e7a30da98260e1e338efb4a685a5052a6cd815aa7cbe26df7  core/cpp/v3_score.h
19e0a0bd0e47949025ead4c7d7df0a521980454f010ec0b0d7a2176e64b701a7  core/cpp/v3_start.h
1841122ef2ad6d963b1e0f1d622e1bc154f23fd9e5d347e2b7e02890334d2e15  core/cpp/v3_util.h
2d1e768ff2dfabd20cddfdf8ace400cd5adb8fa1214dc67b95ecf1a154cce085  core/README.md
addfae035781bbfbf503d1b2fbd8f4d9fc5d92795276a83f28777fdb51b7de2b  core/source_manifest.json
951ffb3476c38e24de8b532827e83590a40d02fe0d0525beb1d025fb33b4eaed  core/v3.R
268aa414e811af96c470758994773bf598560d14728b5526cd5e2ae5cbf2de06  core/v3_calib.R
18e29edea8d0df176a878d0f28a8662a50c80bfb4e567fb7a4bfde9648ff8ec8  core/v3_exact.R
656f11d704e566c87c4cb3861bffe126a43320e6888809ef91e0ced21cdb5217  core/v3_fit.R
758d97e0f02c01e6b4f6ca824805ee1e9fda55a8214f668d8947b9e1a0e929be  core/v3_preprocess.R
330b9f8347c1e4f373830901b3d402a9147b31775645df6cfa90c665641afbfe  core/v3_run.R
1f8425e77f59c73eca9e67d6294ca3a0d52828d3f079420bf916eab55396215a  core/v3_setup.R
d44ae5a9b74b1809bcfcb6c6937f18838e26e548c619e5c083a788dc5828bfb9  study/adapter.R
6dd5d8ca5a02abaa18bde84dc3bfa031078a9c0f92f184015d12fde0a0dc2886  study/README.md
6907c9321d42c036d207d57642fd4b5a451f7958198a5736fc21d9a67075a92f  study/run_case.R
6150d4dd2e5db5094226e2aa667ec42067a1745432f5ef01580983ef955d4781  study/SCHEMA.md
```

### 2026-10-28 — v2.2 core: regression and manager acceptance (CONF manager)

- Manager diff review: done (no RNG use, no decision change; registry hooked only on fresh ledger events; island list order preserved).
- Diff regenerated CR-insensitively: `code/core/v2_2.diff` (393 lines, `diff -ruN --strip-trailing-cr`; files are CRLF in both trees), sha256 6fa82a8c52735d07eff06c7e852afd8f9ed22eb1d0f7aa2ce55ef0b98a32ca04.
- New-tree manifest: `code/core/v2_2.SHA256SUMS` (25 files). `core/source_manifest.json` is unchanged v2.1 construction provenance and does NOT describe v2.2.
- Compile caches removed from both trees (`.cpp_cache`); `v2_1_baseline/` re-verified equal to production SHA256SUMS.
- Known cosmetic deviation from spec invariant 3: top-level `pip_plain_r`, `pip_plain`, `mpm_plain` precede `peak_memory_kb`, `runtime_guard`, `numerical_routes` (relative order of all pre-existing names unchanged; no positional indexing).
- Regression (independent Sonnet worker): `conformance/REGRESSION.md`. Bit-identity of all pre-existing outputs: PASS. New fields: PASS. Low-p smoke vs exact: PASS.
- Status: **v2.2 accepted by CONF; awaiting Sol review of code + regression** (`conformance/review/`).

### 2026-10-29 — v2.2 core: post-review fixes and regression round 2 (CONF manager)

- Fixes after Sol review (`conformance/review/REGRESSION_REVIEW_sol.md` findings 4, 5): (a) `v3_fit.R` finish() re-appends `pip_plain_r`, `pip_plain`, `mpm_plain` after every v2.1 field (v2.1 name vector is now a prefix of v2.2's); (b) `v3_core.cpp` CalState keeps `registry_keep` (R owner of the registry). Author: CONF manager (Opus); verified by independent regression round 2 (Sonnet) and Sol re-check.
- Supersedes the "known cosmetic deviation" note above.
- Diff: `code/core/v2_2.diff` (404 lines, CR-insensitive), sha256 5d7ce9cd4809a1dcae499637de2c0cba9c241c4b8602ab2bf0d1a82fb517bc04. Manifest: `code/core/v2_2.SHA256SUMS` (25 files).
- Regression round 2 (`conformance/work/regression2/`, hardened comparator cmp2.R): 28 matched comparisons + p=500 adapter record, 0 differences, 0 non-allowlisted additions; 100/100 extra checks. Result in `conformance/REGRESSION.md`.
- Pending gate: NOTS identity job `conformance/jobs/CONF_NOTS_IDENTITY` (production platform + escalation path).
- Status: **v2.2 = candidate for the campaign; release after the NOTS identity gate passes.**

### 2026-10-29 — v2.2 core: review closure (CONF manager)

- No further code change after the round-2 fixes; `code/core/v2_2.SHA256SUMS` (25 files) stands. Sol: code ACCEPT (`conformance/review/FINAL_CHECK_sol.md`).
- Comparator `conformance/work/regression2/cmp2.R` round 3 + F4 (list-hash scalar attributes), self-test 101 assertions; copy in `conformance/jobs/CONF_NOTS_IDENTITY/`.
- Release gate: `conformance/jobs/CONF_NOTS_IDENTITY` (route via HQ → OPS). v2.2 is the campaign code once that gate prints ACCEPT.

## 2026-10-29 — LOWP: low-p study build (lowp/, bench_lowp/, scoring/)

Author: LOWP thread (Opus manager; Sonnet and Terra workers). Areas: `lowp/` (LOWP_SPEC, INTERFACES, RUN_DESIGN, generator/sealing/verification in `R/`, exact enumerator in `enum/`, SMC low-p runner in `smc/`, NOTS pilot bundle in `pilot/`), `bench_lowp/` (8 primary benchmark adapters for p ≤ 30, ADAPTATIONS LA-1–LA-4), `scoring/` (metrics, theory measures, headline tables). Purpose: Regime L (p ∈ {20, 30}) per CHARTER §1 and D1–D3. Depends on `core/v2_2` (scorer headers `v3_score.h`, `v3_util.h` vendored in `lowp/enum/vendor/`, hash-checked against the core; `lowp/smc/` is a copy of the v2.2 study adapter and must be re-synced when v2.2 is frozen). Reviews: `code/review/` (Sol 6.1: REVIEW_a–d, RECHECK_ab/c/d, REVIEW_pilot_bundle, FINAL_CONFIRM–FINAL_CONFIRM4; final: all components ACCEPT, pilot GO for OPS). Status: built and tested locally; no NOTS run yet.

```text
0ab6c4c87e84f58e628564084bc086c8bd09944114dedd29cd5852b26cd65fdc  bench_lowp/ADAPTATIONS.md
69c7a1bcf78106d3bdb2c5c9ffb9c536b93aa01074e7bf92e3558ca5e91e4442  bench_lowp/R/SOURCES_SHA256.txt
aad56bd2d22e346481774221f98b31eac19fed8bebfad3752d14d69c85fc0bca  bench_lowp/R/common.R
c8cebcc7d77caef27af53a59409f4172339887df193acaa15678d88154854502  bench_lowp/R/config_lowp.R
93331f6530c33ee13ce886381c6c04f31661223c463dd1a333434332fd7ad223  bench_lowp/R/methods/fit_A1_susie.R
cc8406d21860c24242153ed1efba0d38300bae512ff3ff1bca73828235a9828f  bench_lowp/R/methods/fit_A2_ssl.R
9bea247710d4b98234f96dc03dd434bcf74cc675394055e156e7714e4ba79048  bench_lowp/R/methods/fit_A3_horseshoe.R
734d6fcc778d7fbadcaa0e3ecdf554dd84f48b00e0569687d14516eb894314bb  bench_lowp/R/methods/fit_F1_lasso.R
f038f80b65451a19d2fe5507b8d5e866867c983cd98c568505aaa79bfc2a93b5  bench_lowp/R/methods/fit_F2_enet.R
eded713d97a406f13f0be29628d7b35c9ff6d57863ca818e134d003f0f98a7f8  bench_lowp/R/methods/fit_F3_alasso.R
8342370a881d7fb8e7a21e264b0c78271456d9e2576a73ef503851f8627d20e9  bench_lowp/R/methods/fit_F4_mcp.R
5edfa0127d0914b6955cfdd7f75535ff441bd855bdeb752309203ffc59bbf7b1  bench_lowp/R/methods/fit_F5_abess.R
cd544cb7c3518eb20b6c28ca903812c26392a45ebd35ae367d200db697bc05da  bench_lowp/R/methods/glmnet_helpers_F1.R
d2ffc988506171c745e0642041102ab4393b267a085d355bad1998d21db0f3a4  bench_lowp/R/methods/glmnet_helpers_F2.R
0d6cd4a894bb1daefeb67b8ad725be24d205ad297b65aef99d285cd3e1e4f4de  bench_lowp/R/methods/glmnet_helpers_F3.R
830edf4aee80cddd9fbf4caa3993277c0b91470f2e1ea90b01bd5b519711d2f0  bench_lowp/R/production_helpers/common_A1.R
fe7d661c6ebcbf076bebd90994d102ae210b7b7d959d7b866b24012eecb5c3d4  bench_lowp/R/production_helpers/common_A2.R
f823725e364b91009dee1e7fc0d945684c9cd5d390f9ea496bd0c291b8b0ac04  bench_lowp/R/production_helpers/common_A3.R
c1c9c46dba0aef3825749237a1b89d827546fd8be821843930826feb5c1d3246  bench_lowp/R/production_helpers/common_F1.R
666bc488c69168f878d811e2061b22d46c5dd8dec86a67b31cc3a3a8b9c7cb26  bench_lowp/R/production_helpers/common_F2.R
fe8e4a372fa7927e5ccd9494fa79c31b251423bf58f6d3df832b332d84042fb1  bench_lowp/R/production_helpers/common_F3.R
2f1471dde45f61c1984c1d2c60ad0094ebbd5ca41c1379c3bffafbd5569b60cd  bench_lowp/R/production_helpers/common_F4.R
f7c9904f93b99354db45fbb9ec6358e7392278cefdb69ad9444f961610da439c  bench_lowp/R/production_helpers/common_F5.R
0b90be4046705d5c46709ab1dcd92fefa2f414dd127a876086048b9ab44425b1  bench_lowp/README.md
237d5f7743b44504702993e915eee677a2182064d2cfade77c4ca2026561c2eb  bench_lowp/run_bench_case.R
c849636dcb277f2fd7af85f1fe7c53c34d439c7184196ecbfa3d1cd00fa481cd  bench_lowp/smoke/SMOKE_REPORT.md
3e244ae19971677b3dffb960830af4f050ad1ebc7cb23c3c0c878b749523bbb6  bench_lowp/smoke/check_determinism.R
d3c329f41206dc0240f763c731763f05ceaf8e27d11a71704233b1a8b47e65a8  bench_lowp/smoke/derived_checks.R
ec7de83d97fe4f279b1f3b17c29f0156be67dee2d869df9dc5bb2434a77a1b87  bench_lowp/smoke/make_smoke_data.R
935aa7c21432e8438f299310c5b0de589d4d36b71fb0bb4443e4a58c6ed4abc7  bench_lowp/smoke/measure_memory.ps1
9a37dc139104dde0dbab1abfc1fbc6317c10cebfe96befe86955f79d85a93425  bench_lowp/smoke/run_smoke.R
9546f7f0c46a7f04fa60dd9ef4c4d28aa540f9190ec49aebb6ae5edafb81df0d  bench_lowp/smoke/smoke3.R
a862531f827081bf190b09c5c110cddddb575f8a6e9db0011bc16b7b5f64efbf  bench_lowp/smoke/test_derived_conditions.R
d4e2b9b02a39d1ddecefb43a7ac747b2b9e45cb157c3914da6d000a059287a05  bench_lowp/smoke/validate_smoke.R
a9b09ed0bb3b5e40c4ac766c6dc6b954c6121837507ca9bbce07de8f4863a796  lowp/INTERFACES.md
4a925a12f9500bd345d669e63c42a70316320a51baa448b1056c98b29db7428e  lowp/LOWP_SPEC.md
15169212117e17f6971be89838f109b7deb4d8daae17abc9c1c23c5a785fb765  lowp/R/lowp_generate.R
db1090a5d249b31b7b59461ebe533a60670bb8ca53254863d97763a40b232efb  lowp/R/lowp_seal.R
0a9c09f3cc670da026cc5d9ee5da8c6cb84b9309873aa120881061a59b10fb64  lowp/R/lowp_verify.R
866ab494e877c09694868fab746d31e9cbda7e804e734dc6df843d6c79d3819a  lowp/R/lowp_verify_nots.R
35defe32b837b4722936da44645af8f997e533a571676c59ec1d74df64406aca  lowp/RUN_DESIGN.md
bb499ef7ea2a8ab1ade275040c4014f813da3b311f16e3f38a1a39e8c734fef6  lowp/enum/Makevars.lowp
d33676556cc5fbd9c33de1b55ee4980150d29a869553a0bd38b929abfff3fda8  lowp/enum/README.md
f52c5050eca15ebb98f67e653322250759ed70541d66874f522abd511eae5ae6  lowp/enum/VALIDATION.md
284db4f180c7b4709bcf635d5a196af3fa5ecaf9963d635e3fa4ec4e273c57bc  lowp/enum/exact_contract.R
ab581c1cb9ef88a950005b2e4656cb7738c9a3196d079e88e4ea0b88d7c9b481  lowp/enum/lowp_enum.R
8b61f0b144ec791caedf024bfb7e997d2cfd64fdcdc09189f9a567c93e3ddf42  lowp/enum/lowp_enum.cpp
1490643ed17d113921a4c95bed883dbf849408df13cc67f54c693d9bc4730cf1  lowp/enum/run_enum_dataset.R
c87e29aa50fbdcae8c775191da0d8dc5e63a4fcaf64f937f9e843e23c7b575c6  lowp/enum/tests/helpers.R
f2bee7a8139d99b909a6dc41ca6d63b0bca72ce7aadf43e5c7b11523378532bb  lowp/enum/tests/logs/t10_cli_completion.log
d399d03871643e36719b03b640611329aa586df69792ae2920afc8561f6bd344  lowp/enum/tests/logs/t11_partial_and_validation.log
467da96aae9d69c5e173b4a7ba2c66aa5a1e72bd6f84a212a1c91f68c17f83a5  lowp/enum/tests/logs/t12_exact_contract.log
233beb4a93dcad64e80b46ced1f7a6a8bb5b93005b05c4d5613b7239f54837b3  lowp/enum/tests/logs/t1_brute.log
4164f6d4503c3b70bc03642cf8a0fcef76dd3aa8f72ffcccf545b1d967917008  lowp/enum/tests/logs/t2_table.log
ae42fb5455db0c735346302fd9c63d02fe2d4070c9a287770282e0721f959ad5  lowp/enum/tests/logs/t2_vs_scorer.log
8f097be39431b4ab78c67fe127b12b3fcca1f1d0c211ac421dd1286174dc9361  lowp/enum/tests/logs/t2b_fallback_ties.log
75719ea6473ff7ee340eb0dbebe3750110ef433e5efb55a40fbd3dad0ec8c07b  lowp/enum/tests/logs/t3_t4_threads_accuracy.log
042faa9a81baf4cdfb35a16e664be4ad55df9835484b06002025ebe7676d087e  lowp/enum/tests/logs/t5_td.log
7bcf22172a1fc277b9e6f3c24e16f2d82ce25a098b2f55c23d5480b01531e3c3  lowp/enum/tests/logs/t6_extrapolate.log
9977688a354d7831cb85c3c4c5f7abc545552344e4a00183f35af0ec5b6fb69a  lowp/enum/tests/logs/t6_full30.log
2d1c156922ddd271062e903de62f45a8901b178bd6af84b80a7ccb3ebe62ea2a  lowp/enum/tests/logs/t6_p20.log
d8de975b41a227cac5a8acacea90928a5a88338d7cc30716eaba50637d882a7f  lowp/enum/tests/logs/t6_p30_subset.log
aff9d2304054c09f6fdcb2e236b7c1eb31e221056305c6847f52b04193d60ecd  lowp/enum/tests/logs/t6_td.log
d54dec5adde7d0665e813bb1a7b8facd6b2762713de61193a209099f7a2df8d6  lowp/enum/tests/logs/t7_cli.log
ff6324826ec2aa72563bd8f32f28c86422014ab9f9fa7f1a4db942f537ef11ad  lowp/enum/tests/logs/t8_vendor_check.log
ca8a38664ec5a20192d31795327d92c5f74be41bf580007b97cc918f7dc6805f  lowp/enum/tests/logs/t9_td_p20_example.log
c3ce3f25dc01c228377ee12578c75555c58f775b913520a9a8d855428a6abd44  lowp/enum/tests/run_with_peak.ps1
f29c6db156e28068eeafb43cc223e2b473d2978325bfc83a82045fa23efacaba  lowp/enum/tests/t10_cli_completion.R
ff1b5588684c641810a80b29dfd26175004796126bcb78ee2e527c9716cae14d  lowp/enum/tests/t11_partial_and_validation.R
07dd618e0c77b4be23f0425c6bc7076f9c0bf1477b1a1365daa77450035df545  lowp/enum/tests/t12_exact_contract.R
0b305c9c29ae5b40a6968d3bd2942fa36ce87bc20ed50d14ce49752a7a12ae05  lowp/enum/tests/t1_brute.R
b1743b500bc76ae1f5e78175010467007e09486a77fc25257e0dbd627169dbce  lowp/enum/tests/t2_vs_scorer.R
0f3298509d19f1b68d65d84c6262a9033619c11f169993012db00c61ff8c0612  lowp/enum/tests/t2b_fallback_ties.R
62818a3c87606861e76c91c7a353fbbb79d6e9a92f2a3f046f32865fffca4510  lowp/enum/tests/t3_t4_threads_accuracy.R
44920456a997ff42a515982c94d9fca9d2b16c414e1c15f9c9e7ceda1c9c12bf  lowp/enum/tests/t5_td.R
e7d4f652be92cf1a8eecba450520148acf46ebe755d4d7bb45cc9c2c46f592f3  lowp/enum/tests/t6_extrapolate.R
09c106866b561e73fa9ccc020fd4e4f8fd4ac24cd31ba13d37f14708fe2576c6  lowp/enum/tests/t6_full30.R
a1994b2fc155b89642c15d04bb04abc03be196f373c38f7bdf9f7aef056915b6  lowp/enum/tests/t6_td_time.R
3a5cbf22c4c0e69c0fdff5a8084fded8bfb940350ec2410a3509f6cef512678d  lowp/enum/tests/t6_time_p20.R
27de1e99fdb8317a4925f90232f95cef746870a581c92bf9e944cc53e04bf85c  lowp/enum/tests/t6_time_p30.R
710b6fba68f7e4e3d35e2ffd69ff48b7066d54d110a6fc571e048a70448aead9  lowp/enum/tests/t7_cli.R
1e5b356e8f96a10cfa0a25e0377f33267d16e7eee4ba78c0bb4be1f6bd0760a9  lowp/enum/tests/t8_vendor_check.R
90ebfe2f48291445bdbebd9aee97c34a54e1d34517f2d96ce9adf199bfdf96d0  lowp/enum/tests/t9_td_p20_example.R
3d8a55fcb0cf4c7d60da1e9af0d413f58658a27e0a21405712301d39b5c673cb  lowp/enum/tests/timing_helpers.R
774fbe67265bc8f8598cbd1f603679248053caf27afc929ff1bfe4907656f7ff  lowp/enum/vendor/VENDOR_SHA256.txt
41173ac1460e180e7a30da98260e1e338efb4a685a5052a6cd815aa7cbe26df7  lowp/enum/vendor/v3_score.h
1841122ef2ad6d963b1e0f1d622e1bc154f23fd9e5d347e2b7e02890334d2e15  lowp/enum/vendor/v3_util.h
78ddaab65d8c29d0608957dace50fb6f28f33e46c7fcb0f9831639c14a996eea  lowp/pilot/JOB.md
618fb0da8c41bbd8ebda6f960a7a053a3cd81192763289e7f574b5351073414b  lowp/pilot/LOCAL_TEST.md
d088d1c51dd217e6c8ef7027ab319a3d183c1ee1f2a14aca539162ca68018f7f  lowp/pilot/R/pilot_bitid.R
a14d79a1605e255d75bd7c21c88b0966cb4265340fba58b425b3114f6c454363  lowp/pilot/R/pilot_build.R
6479a65d901c456694ce6f4f6eb0b88e8d923b972696cdb3ae875485115910ef  lowp/pilot/R/pilot_scaling_subset.R
647da9049c881613a959fdb2c2378a77b12d025a1433ffef1c1b6b4e18db8c3c  lowp/pilot/cleanup_pilot.sh
58ac5727f3e3960e3d980f8cb76fae5dcd70857793950ce746ad31b0b4c7783e  lowp/pilot/final_accounting.sh
3625033365a168dd4e255f4a74453a46378aaf5bfcdcb160ef614923d9232384  lowp/pilot/guard_check.sh
2ec01f9710577a83e6f7445b1fb590c39cc3318adb8cfcb5091238e0934ddedb  lowp/pilot/lists/bench_cases.tsv
15ee4ff5759d589772ae9b4d7aceced62784dd6d5a96397e01d2a1790c3fe322  lowp/pilot/lists/enum20.txt
a739abd33235b4ab1a0cabb909d7976b7527b81a88a8c5f33e93771a1a7a0d0b  lowp/pilot/lists/enum30.txt
c509634aba58b4c08d28b08cf3d35aeae512b72fa8e13d29f85e0f315a4e7172  lowp/pilot/lists/smc_cases.tsv
272aabed3f7da51948486724b2ecbd5a6ab3d3165ea11fbeaed2e7b973c6c70f  lowp/pilot/pilot.env
add6cd10ff0c12611340b4e5e4a90d6545dff2a7d0aa57e474d3f702c280e75e  lowp/pilot/recover_truth.sh
f1dc1907e3165820ae9241dfd39e8ab1664d74bb3a327c1668f6f7bed19245d9  lowp/pilot/slurm/common.sh
77bb1957ae13b9e75593c30debfcbcbf8ec93e111d5c199702ac376069dac2d5  lowp/pilot/slurm/s0_build.sbatch
80d02fcf29553f42e7e2c6f4e70c3d38dbdb8186ba91f2297e155cbadff4aa55  lowp/pilot/slurm/s0_lock.sbatch
7597ff084089ad8bbdaa23ba1c0e66574b97d6868add6cbcb5823caf769d2227  lowp/pilot/slurm/s0_truthlock.sbatch
b767b8eef24e618d9605e8c30f9d8160e545ec46f42b4b7aa6853ae5ae9c4956  lowp/pilot/slurm/s0_verify.sbatch
fca3195706b6b8ab96ad178eb297f2b10fa3fe1e389a54d0622d37d42955153d  lowp/pilot/slurm/s1_bitid.sbatch
eafddcff5d91857b6af5043bd0eb70f55073d0c4cf7c79517bab8a8d962c1d6c  lowp/pilot/slurm/s1_enum20.sbatch
32c421f5238c79c69769dc7237dd586cb3b57004af973186c86c25abb01ad5d1  lowp/pilot/slurm/s1_enum30.sbatch
2643ed8108092def791bcb294d93a9fbc9d29cd648aed2b8d6f7d6c152026a47  lowp/pilot/slurm/s1_scale.sbatch
a7eb45ded0c2295094093a9bf35f40b0c787148e142b24e8d534364c5936c7e8  lowp/pilot/slurm/s2_smc.sbatch
409e276ddb59b1d24cfa7c514197a5ee3a4905db1f5203df8c4c3449b4c75064  lowp/pilot/slurm/s3_bench.sbatch
adb19dd8212fc94e9da1d9705cf54b61c5d6a370a937b71e205b702e0643bf44  lowp/pilot/slurm/s8_unlock.sbatch
a0943672da2b9cc97b6e8281e66027fd45c4b34e2b505b7fe9ed561e77f5e4c5  lowp/pilot/slurm/s9_collect.sbatch
7748fa4b8b91ba4337a988d79fe387014313e6e1d9b3e5353acfc7e99166bb7d  lowp/pilot/stage_local.sh
b2ca81aa0c6b560676fb0e3cb40fd8cf03b9a49dc3dd4d822fbaefa414d4e687  lowp/pilot/submit_pilot.sh
fbe50dbb428b4d5668341b2e2974dc13858b7766e0168eee19d48cc3646decd9  lowp/pilot/summarize_pilot.R
d79940a604849bdf649e16eaa3383e04e8d91eb3228bcedb95443bde7305b1e8  lowp/pilot/tests/make_fabricated_pilot.R
494fcde46e1c2eedcdd9122d24d40be6779d369447d514387369ef5c9687aebf  lowp/pilot/tests/run_negative_tests.R
ad051c9a90d14e1538b3373395e0fcc2ccb214f942a813afb1b26673fb0e2e29  lowp/pilot/tests/test_shell.sh
a4b4ddcd5b8b680cda3c8b30738949cab46a6baaba267e3dccb9acdd6c2436ae  lowp/pilot/truth_lib.sh
7bfd31b8fb95c31dc1a88d9b5c8a976ec188c0fa1425ee134f377ffe45ef5e57  lowp/pilot/truth_wave.sh
6e2f875ff07abacc5d2794c13dbfede125cadd101c0df069de107782d4c7c092  lowp/smc/CHANGES_vs_v2_2_adapter.md
ab16dc75e0e5f6a8e4682604f83eff24615a03447e824992163bada46ed40a5f  lowp/smc/README.md
3d0c836e8c43e2cdad41f95aaa7ee43aa481631c44880d1e4056ed1faf362060  lowp/smc/adapter_lowp.R
017a7fedf70078c99a27dfea26d074e84de602780a9a215dfc464c51174e3c82  lowp/smc/adapter_vs_v2_2.diff
672386325930946596026f41dea162bba99440a00a0a1387c6313f9f69d198f4  lowp/smc/run_smc_case.R
460cdcfee40a4df507040c4ba41f5e052362aacb87491967f28205fb7856bf37  lowp/tests/ADVERSARIAL_TESTS.md
f35e561b2864d5c6fd52d001f8a0b4fdc21cd5236fd8661e028e87c22e985d60  lowp/tests/SMC_SMOKE.md
cae15dc741b1a88945e3dc1afc43a71fe01cebc269e790b8892805791feadf66  lowp/tests/VERIFY_REPORT.md
779cbc396972c7a60f90e440652ef578f3e65aff25caa66baa0ab8f5b602e6e0  lowp/tests/scenario_check_lowp.out
3159d88777f63dcd782ec30a2626a7b88aba0bc1a840c9a45642c63455825741  lowp/tests/seed_collisions.out
b9beb8e6d2e2e77b3ad1bf8c20909b05222005ce05672bebbe99c624d922f7a7  lowp/tests/test_adversarial.R
3d0c2da6ff1d7818b8a3e73d80acef2a81ec3b9e421c499635b7eef18c025416  lowp/tests/test_truth_lock_linux.sh
40a4285105613c51e867de72e2cb63fab7b25b9a6fe504320e90b19a37fd93a7  scoring/FIELD_MAP.md
e05cb46aff686280f09bac2bc9d642e54e47391b7d3a6e3dcdbe385da757a6d7  scoring/METRICS.md
06a6db25d3ef12cc6c5e9ff42bf194504516f0d605adfcb22e96ca83f4aa837f  scoring/R/common.R
b05fceeca8a1b7ecb43a2754967a0bdc5501c69178a5bb2aae6d8c314bf9b4d7  scoring/R/extract_bench.R
2a69175e9869abddb1935657fbebcb208e83ecfbf475a6af9677e6e16969639c  scoring/R/extract_exact.R
80846dace990d360e994a5d787f1c881837cfc827f173748c6fc0aefa16544b3  scoring/R/extract_smc.R
56e11ced4e772075bbd9d4259a10aa3cf3fec7863dcbecf1f38765be408ba86b  scoring/R/load_all.R
4b7e6e00cdd01298842dbd002f821a68e8be661c5557c01c402ccc02c8f60ca3  scoring/R/metrics_selection.R
ac6cfd45a20d0e7d8800be58f619788b653e802011bbf2268334a39efa751444  scoring/R/metrics_smc.R
b30460db998f7d80809c5c43d289db90f372a16c7ce541a5b43cbeaf16b9797f  scoring/R/registry.R
d8a473a330543ae9b30e8e042eb28933cc5ac060bbfb5a1f8de70a4fc19f15a0  scoring/R/tables.R
b5f4b68fa4661ce1553ee643d2b88b686a4f381f15190a0796bfee0631040154  scoring/R/td_slow.R
4c89a665c3eef54c72c830cfc7263693060364b742863dee24d92a776fdf9aec  scoring/R/theory_measures.R
15ff93304edbcead35ea057e9a0913c55cb327a60fefb38d5d67a79a039c2517  scoring/R/truth.R
18f8f739e1130d08a289a7b76e1eb8ef32b105cfc626a8daea3510cab3b543c2  scoring/THEORY_MEASURES.md
d984b0787979e1adbdbe7a57f8100502afd3c1948906726cb541efbd8466a2e6  scoring/make_registry.R
a945bc9bbf9830d3c9241b06908bed9fe90a0ba2e9bd09a7ef0858de0267ccd6  scoring/run_scoring.R
fba31235e351efe17ce1eed3fd10f638e6cd8b911f6392bba1a421385e50bec1  scoring/run_theory_H.R
8f221b4f5a27a57a73bb58237b966a350894a63bfae04b2f294a2d2a2f8847a1  scoring/tests/EXAMPLE_HEADLINE_fixture.md
f925ff52400efd034a41fc72bffdaee7245c29d80873fb5f706b206691d12572  scoring/tests/INTEGRATION_REPORT.md
a0e88ee110339f65d3829a14fa3abde1753a2ee8ff557960dc0c82cca03ee59d  scoring/tests/TEST_REPORT.md
680bada5cdabc06887c3fb9b72dce26751609006412c87bf1bb254bf71f25f28  scoring/tests/integration_real_p20.R
2a95103d3b919b2e924b4dad007b7e1ed2ddd47cd6d2d5aa1afcb0b411131646  scoring/tests/make_fixtures.R
255284ffca7c10fdbbff6f266ad93a8fbb0cecd2553967d87f12b9158feaba21  scoring/tests/regressions_recheck.R
f32f8905da6d6854022eb1a267d7933c7fe8fec3da56745dce498126be5a45cd  scoring/tests/regressions_review.R
28b0c979dd8fa725cf9f5b09ad10a7fe8f9302a5db8742a6b459a3c732e32610  scoring/tests/test_scoring.R
```
Total: 160 files hashed (lowp/ 100, bench_lowp/ 34, scoring/ 26).

## 2026-10-29 — v2.2.1: one code tree for both regimes (CONF-2 / CONF-2b)

Authors: CONF-2 manager (Opus) wrote the merged study layer; CONF-2b (Opus manager, Sonnet workers) did the regression, the pilot rewire and the fork retirement. Basis: D11 (P5), D14, D16, D19, D20, D21.

**Tree.** `code/core/v2_2_1/` = `core/`, byte-identical to v2.2 (all 21 core files equal to `v2_2.SHA256SUMS`), plus:
- `study/adapter.R`: regime table H/L, regime-L repeats, the P5 rerun into `P5_retry/`, adapter 2.2.1-R1;
- `study/run_case.R`: `--repeat`, `--p5-retry`, and a key=value last line with the stop phase;
- `study/SCHEMA.md`, `study/README.md`;
- `tools/p5_scan.R`;
- `CHANGES_v2_2_1.md`.

**Manifest and diff (final, regenerated 2026-10-29 after the regression; identical to the provisional ones).**
- `code/core/v2_2_1.SHA256SUMS`: 27 files, paths relative to `v2_2_1/`; sha256 413c9445722b61af354961fb1c49fba08a946efd8b9cd930271e0c10e5c71bdb.
- `code/core/v2_2_1.diff` against v2.2: 445 lines, `diff -ruN --strip-trailing-cr`; sha256 3e82a68ad455e3237717ba96d23501f330e339996ecedef843eb3e525e3b6996.

**Regression.** PASS (`conformance/REGRESSION.md`, v2.2.1 section; harness `conformance/work/v2_2_1_regression/`; independent verification `verify/VERIFY_REPORT.md`, Terra):
- (a) pre-existing outputs identical to v2.2 under the timing exclusions;
- (b) the LOWP smoke cases identical to the fork and to LOWP's recorded values;
- (c) the P5 cycle and its negatives.

**Retired.** `code/lowp/smc/` (`adapter_lowp.R`, `run_smc_case.R`, `adapter_vs_v2_2.diff`, `CHANGES_vs_v2_2_adapter.md`) was deleted; only a README pointing to v2.2.1 is left. The retired files' hashes are in the LOWP entry above. A copy verified against them (5/5) is kept as regression evidence in `conformance/work/v2_2_1_regression/trees/fork_lowp_smc/`.

**Doc-only changes in LOWP files:**
- `lowp/INTERFACES.md` I3 and `lowp/RUN_DESIGN.md` (runner row) now name `core/v2_2_1/study/run_case.R`;
- `lowp/enum/lowp_enum.R:27` and `enum/README.md` still name `core/v2_2/core` as the enumerator's default core. They were left alone, because editing them would change the enumerator's source fingerprint; the pilot always passes `--core-dir`.

**Pilot bundle.** `code/lowp/pilot/`, revision 7: points at v2.2.1, with a frozen-tree check at staging, submission, build and every SMC task; an informative P5 scan; and a new CSV-v3_status = RDS-native-status gate, which closes a hole found during the rewire. Tests: negative 88/88, shell 46/46, stage test PASS (`LOCAL_TEST.md`, revision 7; `CHANGES_v2_2_1.md`).

**Comparator.** `conformance/jobs/CONF_NOTS_IDENTITY/cmp2.R`, amended per D20 (the length of `record$environment$command` is no longer checked); sha256 f2662113babc300d102957f0d79920a97ba75383fe4ef80b38eeaabaebefa048 (pre-D20 947f6803…fa82).

**Status.** v2.2.1 is the campaign code for PILOT, PROD-L and PROD-H, frozen pending Sol's review of the merge, the regression and both bundles (`conformance/review/`). Any fix means regenerating the manifest and diff and adding a new entry here.

### 2026-10-29 — v2.2.1: Sol review 1 fixes (CONF-2b manager)

Review: `conformance/review/CONF2B_REVIEW1_sol.md`; disposition: `CONF2B_REVIEW1_disposition.md`. Fixes F1, F2 and F4 are in `study/adapter.R`; F3 and F7 in `tools/p5_scan.R`. `CHANGES_v2_2_1.md` gained a "Review fixes" section. The core is unchanged (byte-identical to v2.2); no numerical path changed.

**Supersedes the manifest and diff of the entry above.**
- `code/core/v2_2_1.SHA256SUMS`: 27 files; sha256 fda7c3f3a8e02f28bde82c3aa67aa243ec1eb1fb33a3e9e49e4ee44d1013789c.
- `code/core/v2_2_1.diff`: 518 lines; sha256 807d16509b70fd99e5ad1e370dbdd2992ec9808eed3fa3ba52f8e6e2dea19e06.

**Also changed:**
- F6 in `lowp/pilot/frozen_check.sh` and its PROD-H copy: symlinks and special entries are refused.
- Pilot tests: shell 54/54, negative 88/88 (`lowp/pilot/LOCAL_TEST.md`, revision 7a).

**Regression after the fixes.** All sections are 0 FAIL, plus lane G (F1–F4 and F7 tests) and an F1 mutation check (`conformance/REGRESSION.md`, last section).

Pending: Sol re-check (review 2).

## 2026-10-29 — v2.2.1 FROZEN (CONF-2b manager)

**v2.2.1 is FROZEN**: the single SMC-BVS code tree for PILOT, PROD-L and PROD-H (D19). Authority: Sol review 3, Part A, "YES, ready to FREEZE" (`conformance/review/CONF2B_REVIEW3_sol.md`).

Review history:
- review 1: merge, P5, regression, cmp2 D20, pilot, with fixes F1–F7;
- review 2: R2-2 and R2-3 fixed;
- review 3: freeze.

Dispositions: `conformance/review/CONF2B_REVIEW{1,2}_disposition.md`.

**Since the last entry** (review-2 fixes): `tools/p5_scan.R` uses `record$native_status` only (R2-3), and `CHANGES_v2_2_1.md` gained its R2-3 line and the FROZEN section. The core is byte-identical to v2.2 (21/21 files). No numerical path changed in v2.2.1.

**Final manifest and diff:**
- `code/core/v2_2_1.SHA256SUMS`: 27 files; sha256 **d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1**.
- `code/core/v2_2_1.diff` against v2.2 (`diff -ruN --strip-trailing-cr`): 527 lines; sha256 fabce9fac9d4ac19e7c610a06221e443b44521892de847b6ca49032ab1eab42a.
- The manifest Sol verified was df4e7cf0e20981ef9fe4632fe2280355cbdb9e15d2dd724f1615b2c232054c41. Only `./CHANGES_v2_2_1.md` differs from it (the FROZEN section): 2eb3023c… became ba2ecfb3….

**Regression.** `conformance/REGRESSION.md`, last two sections; harness `conformance/work/v2_2_1_regression/`. Every section has 0 FAIL, including lane G (95 checks + 14 R2-3) and 27 a2 negative controls.

**Bundles reading this manifest at run time** (no hash is hard-coded):
- `code/lowp/pilot/` (revision 7b; shell 54/54, negative 89/89);
- `conformance/jobs/PROD_H/` (Sol review-3 minor fixes pending re-check).

Any later change needs a new version number (v2.2.2), a regression, a review and a new entry here.

## 2026-10-30 — job bundles released for HQ → OPS (CONF-2b manager)

The code tree v2.2.1 is FROZEN and **unchanged**: `code/core/v2_2_1.SHA256SUMS` sha256 d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1, 27/27 verify. Both bundles read this manifest at run time; no hash is hard-coded.

**LOWP pilot**, `code/lowp/pilot/`, revision 7d. Status: READY for OPS (HQ D44).
- Changes since the LOWP entry:
  - revision 7 / 7a / 7b: v2.2.1 rewire, frozen-tree check incl. symlinks, CSV/RDS status gate, `native_status` fixture;
  - revision 7c: GNU time 1.9 resolved by absolute path, verified, fail closed for the sizing arms;
  - revision 7d (HQ D44, after the OPS-4 STOP at P0a):
    - B1: P0a is a cross-platform generator check (exact on fit-consumed bytes; tolerance 1e-12 × max(1, |sealed|) on regenerated floats);
    - B2: unlock when the lock never ran;
    - B3: the clean-up re-executes from memory.
  - Sol PILOT7D minors R7D-1 to R7D-4.
- Reviews: `conformance/review/CONF2B_REVIEW{1,2}_*`, `CONF2B_REVIEW4_sol.md` (pilot READY), `PILOT7D_SOL.md` + `PILOT7D_disposition.md`.
- Tests: P0a 9/9, unlock 10/10, clean-up 5/5, GNU time 37/37, shell 54/54, negative 89/89 (`conformance/work/conf2b_runs/pilot7d_20261030T0710Z/`).
- Changed files (sha256):

```text
9c49594727b9c6cc00d31c4efa283dba9218f5ce81395cae857769a7a494606b  lowp/R/lowp_verify_nots.R
a2c2316a755c4b60409e7f0caef5d9fc0f1250365bc8343141b56c8eb2207a06  lowp/pilot/slurm/common.sh
0c8a384362daa517ff9ad6fc38ace2aafcb599a4fdf4aa3f5f2618dde3d0db00  lowp/pilot/slurm/s0_verify.sbatch
0fd6b1c80dcefca4b6ab37f1a9b4242cb4ebe46d2102ab3945a42a692ea24e5d  lowp/pilot/truth_wave.sh
5871c669e4a1b178d2276544695df8fd606f04afdf2aef7394b9d61e6c69554f  lowp/pilot/cleanup_pilot.sh
ae1aacc23c1ff7c9cea7b9c0016872e805f415c1a839163abe2a9665c9ebbf72  lowp/pilot/frozen_check.sh
7ff0d3885bea3634d2b3fb77ad9c927bae269474113695166658cda3f3b07dd8  lowp/pilot/JOB.md
64ae670ee050e851b5fcb070139caf25da1214af25d88f1a4b6765bb8ea984b5  lowp/pilot/tests/test_gnu_time.sh
43f0122fc7faefe9736288da9a77c8a870cd861967190b960e9f86607a6b9b45  lowp/pilot/tests/test_p0a_tolerance.R
7e1126f7f37fb4167a39fc843a8d25f51293e4d01c82bb0a7c66c6719ebc3f8e  lowp/pilot/tests/test_unlock_never_locked.sh
69e90272a6c0e8ac6dd42af6d5669e0f82e70814462bd62475cd76d9d8bf5311  lowp/pilot/tests/test_cleanup_inplace.sh
```

**PROD-H**, `conformance/jobs/PROD_H/` (renamed from `PROD_H_DRAFT`). Status: REVIEWED (Sol reviews 2 to 7, final READY WITH MINOR FIXES, minors fixed; HQ D48 time-box, D49 throttles 30 + 30). For HQ, then OPS.
- Bundle manifest `conformance/jobs/PROD_H/BUNDLE_SHA256SUMS`: 53 files (runner, staging, tables, test scripts, docs; logs excluded); sha256 2a2a8b1fd3d5ad72ef51e677cd17a097515333ac96eb3d076efeefc8823ba5f3.
- Fix records: `REVIEW2_FIXES.md` … `REVIEW7_FIXES.md`.
- Final suite: Python 51/51, shell 229/229, CLI 6/6, syntax 27/27, tables 1/1 (`conformance/work/conf2b_runs/prodh_20261030T1430Z/`).
- D48 class (ii) items accepted without review: none. The final verdict was READY WITH MINOR FIXES, and both minors are fixed.

## 2026-10-30 — bench_v2 FROZEN + bench_lowp benchmark fix (BENCH-FIX manager, D42)

**What.** One benchmark fix applied to both trees (D36.1):
- **F3 adaptive lasso:** the ridge pilot is replaced by F1's lasso `cv_min` fit (Zhou, van de Geer & Bühlmann 2009), exactly per `bench_audit/AUDIT.md` v2.1 §3: pilot failure fails the fit; w = 1/|b| on the pilot support, stable normalisation r = w/max(w), v = m·r/Σr with fail-on-unrepresentable; m = 0 `pilot_null`, m = 1 closed-form `pilot_single`; full-p EBIC; ridge fields and codes retired. **Chosen after seeing results** (disclosed; the first-deployment ridge rows stay as the labelled sensitivity "F3-ridge").
- **Evidence (D42.5, AUDIT §5):** F1, F2, F3 save a per-rule `coefficients` list (`beta_pen` at the rule's index; `beta_ols` for EBIC rules; failed rules keep an audit vector) and emit `ebic1_K37`, `ebic05_K37` rows (roles S0) in-wrapper; RDS `schema_version` 2. F1/F2 fitting unchanged. At low p, F4 also saves `diagnostics$path_beta` and F4/F5 get per-rule coefficients incl. derived rows.
- **Unchanged:** lasso/EN CV rules, ABESS; no polish companion. Headline-rule promotion of `ebic1_K37` (D42.6) is an analysis label, not a code role.

**code/bench_v2/** (new versioned p ≫ n tree, copied from the deployed `/home/fb31/projects/BVS/Benchmarks/F{1,2,3}_*`, 15/15 deployed hashes verified): `MANIFEST_SHA256.txt` (23 files) sha256 **8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373**. F3 runner `source_sha256` (run_case.R CODE_FILES formula) **3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c** (equals the value the real runner recorded on dev_p0500_S1_r001_c100). Diff vs deployed: `bench_v2/DIFF_vs_deployed.patch`; contract `bench_v2/SPEC.md`; changes `CHANGES_v2.md`; consumers `CONSUMERS.md`.

**code/bench_lowp/** after the port: `bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt` (34 files) sha256 **288e0f8c08e57a48ec487e3cf9107a95ccd6ec2d66933293b22c699f4a415553**; before/after per file `bench_v2/lowp_port/CHANGED_SHA256.txt`; F1–F3 method files byte-identical to bench_v2.

**Evidence (local, R 4.4.1, glmnet 4.1-10 with the audit's test-only override; NOTS 5.1 evidence comes from BENCH_F3_DEV):**
- bench_v2 single runner 71/71 incl. five implementation-mutation negative controls; ridge-weakness test fails on deployed F3, passes on v2; real runner + validator on a dev case, 9 validator corruptions rejected; F2 legacy 24/24; F1 legacy 25/26 with 10b re-run standalone 11/11 PASS (`bench_v2/review/manager/recheck_10b.*`; the suite's 10b failure was the nested process killed at a T3 restart, exit 4); F3 canaries 14/14. Disclosed reclassifications (pre-existing, paired-identical to deployed): CV-min orthogonal exact recovery (F1, F3), F1/F2 no-intercept path tolerance (`tests/TEST_REPORT.md`).
- Reproduction (frozen snapshot `2a8362b2…aa67`, 12 dev datasets × {c100, c050}): F1/F2 original rows, beta, diagnostics identical to deployed 24/24; F3 pilot `identical()` to F1 v2 beta 24/24; coefficient/support and K37-vs-derive_rules 24/24 (`repro/REPRO_REPORT.md`).
- Independent checker (Sonnet, own scripts): hashes PASS; AUDIT §3 clause table 0 deviations; recomputation 168/168; low-p 204/204; diff touches no fitting arithmetic (`review/checker/CHECKER_REPORT.md`).
- bench_lowp: config equality p = 20/30; paired before/after 42/42; smoke 61/61, records 48/48, derived 122/122, repeat 8/8; scoring 195/195 (`lowp_port/LOWP_TEST_REPORT.md`).

**bench_lowp revision r2 (documentation only, HQ D54):** `ADAPTATIONS.md` records the OLS-pilot ruling (out of scope) and the DEFERRED F5 low-p exact best-subset check as a disclosed limitation. New record `bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt` sha256 **85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7**; it differs from the first manifest only in the `ADAPTATIONS.md` line. This r2 record supersedes the first.

**Bundles:** `bench_audit/jobs/BENCH_F3_DEV/`, `bench_audit/jobs/BENCH_F3_PROD/` read these values from `BENCH_F3_PROD/runner/freeze.json` (frozen.py check: FROZEN_OK). **Review (Sol 6.1, `bench_v2/review/`):** R1 (`SOL_REVIEW_1.md`) → R2 final full round (`SOL_REVIEW_2.md`): bench_v2 **ACCEPT**, bench_lowp r2 **ACCEPT**; bundles' validator gaps R2-1/2/3 (class i) fixed in `bench_audit/jobs/BENCH_F3_PROD/runner/validate.R` (`bench_audit/jobs/REVIEW2_FIXES.md`); narrow check (`SOL_NARROW_CHECK_R2.md`): 18/18 targeted checks, **BENCH_F3_DEV READY FOR OPS (first); BENCH_F3_PROD READY FOR OPS after an inspected NOTS DEV pilot fills resources**. Final bundle ledgers: DEV `BUNDLE_SHA256SUMS_FINAL` (28) d5da3b0d57b5d6f3c885c7014e2eafaa7667c8e02999b113186ebb1760a4c4d4; PROD (65) 9129e5df92d5055376f42cdb1ccf1e53f2c8353fdddc4337ad70e7f26cc44827 (now in `archive_ledgers/`).

**2026-11-02, HQ D64 — BENCH_F3_PROD resources set** (dev pilot `20261030T1855Z_bench_f3v2_dev` 26/26, 37–192 s, ≤ 291 MiB): 30 min + 2 GiB per task in every cell, %30 one array at a time. Changed only `runner/resources.json`, both JOB.md, and the expected-time literal in `tests/test_workflow.py`; code freeze unchanged (FROZEN_OK). Historical ledgers archived; authoritative ledgers: PROD `BUNDLE_SHA256SUMS_FINAL` (63) **90579ad6a592916f2a87e5be614a468901884610421ab0c4809ae86666875e07**; DEV (26) **3353b6f667737e225873bc6b97346c80d7c5b321fd6851983f97ec2e94b964ed**. Tests 19/19 + 2/2 + guard 2/2. Any later change needs a new version, a regression, a review and a new entry here.
