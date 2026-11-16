# LINES_CHECK — W3-MISR STATEMENT.md patch v1.1.0 (Cor-H KL narrow)

Run 2026-11-16 04:24 CST against origin/main c3070591. Method: the origin/main file and a temp copy patched with `patch -p1` (in `.rc_tmp/`, since deleted); hashes use the registry's own rule (`bvsreg.text_hash`: lines rstripped, LF-joined, sha256). The "claim_hash" columns reproduce `bvsreg.claim_hash` (statement span + every premise span with its `--premise path--` marker). That recomputation matches the stored `sha256` of all 7 rows **before** the patch, which validates the method.

**Result: PASS.** Line count is 272 → 272. Changed lines: 1 (header changelog, in place) and 191–195 (inside Cor-H 178–197). Only W3-MISR:Cor-H changes hash. Every other registered span, and every premise span or note cite into this file, is byte-identical.

## A. Rows with file = W3-MISR/STATEMENT.md
| id | lines | span sha256 before | span sha256 after | same? | registry claim_hash before (= stored?) | claim_hash after | same? |
|---|---|---|---|---|---|---|---|
| W3-MISR:R' | 70-106 | 2521c6fa097ce5960af9ba8ece1adcdaa06349d20f05186354256fc0f473d538 | 2521c6fa097ce5960af9ba8ece1adcdaa06349d20f05186354256fc0f473d538 | YES | 0165a8d3705ed8faf738a0646e4f3434c768b67b2c22396faa279fa96f6d3dc8 (= stored) | 0165a8d3705ed8faf738a0646e4f3434c768b67b2c22396faa279fa96f6d3dc8 | YES |
| W3-MISR:MIS(i) | 110-123 | 7e2bdc9912d1e7fba7ee6cc88f98ce1fb14585076aa18edee2ccedb5f2b7b3e8 | 7e2bdc9912d1e7fba7ee6cc88f98ce1fb14585076aa18edee2ccedb5f2b7b3e8 | YES | 3b4a582b2a33a6f154172787eb7208f8873c109504500d7f76e0cded85824f1e (= stored) | 3b4a582b2a33a6f154172787eb7208f8873c109504500d7f76e0cded85824f1e | YES |
| W3-MISR:MIS(i') | 127-140 | e73e121f0ecfa6d58512dc98653079093d437ffc51225f49d1fc0805d8c2da29 | e73e121f0ecfa6d58512dc98653079093d437ffc51225f49d1fc0805d8c2da29 | YES | 91d89f3b42f0f3925fd3288b5fb60c7daf1f78ff6fbdc2116124432f2bf8199c (= stored) | 91d89f3b42f0f3925fd3288b5fb60c7daf1f78ff6fbdc2116124432f2bf8199c | YES |
| W3-MISR:MIS(ii) | 144-160 | 545164059e7926ab69dbd5d0906ebd0221251bbe8a8a9de556eeaeea937d7df2 | 545164059e7926ab69dbd5d0906ebd0221251bbe8a8a9de556eeaeea937d7df2 | YES | 160a6909428dcd71bd2d6f0890f142b0dc30a80e0e6cefca5e7058aca76e46d1 (= stored) | 160a6909428dcd71bd2d6f0890f142b0dc30a80e0e6cefca5e7058aca76e46d1 | YES |
| W3-MISR:Cor-G(a) | 164-170 | 6424b61fd6547963b91a4f3b0dd60fcc45a26795a6739e20f59faca4129e14e8 | 6424b61fd6547963b91a4f3b0dd60fcc45a26795a6739e20f59faca4129e14e8 | YES | 5f4e20dcf45436ac380a2c908f6919c2a0dbed9f9d9509060ac7184abca140b4 (= stored) | 5f4e20dcf45436ac380a2c908f6919c2a0dbed9f9d9509060ac7184abca140b4 | YES |
| W3-MISR:Cor-G(b) | 171-174 | 029cab649df40abc1de859ac494cfe027abc29e04e923345e6b86d241ca6ce4f | 029cab649df40abc1de859ac494cfe027abc29e04e923345e6b86d241ca6ce4f | YES | 82f77ca7b87b5e8d9b90f9604c2e06ac58f05feb28b71871bffc4886b2b3e856 (= stored) | 82f77ca7b87b5e8d9b90f9604c2e06ac58f05feb28b71871bffc4886b2b3e856 | YES |
| W3-MISR:Cor-H | 178-197 | 2f096cac8abd21217fc2d363d66a660c7b9a52be1fb8ad3ccfdc49904bdf294a | 30012859f4a6d021165ff269f3027eacb5b236fbcb4b3020e68d9fc4691cdea9 | NO | 84db3142306e420a4bb16d0e476d9b8ce080e2e6e4a5552acc0a20023d7e46c1 (= stored) | a4f83d8cfcd5cbebc2898cd2114a6ed3dee01c628d8840a023dccac1dfc672c2 | NO |

## B. Every other cite `W3-MISR/STATEMENT.md:a-b` anywhere in claims.tsv (premises, notes, any column)
| cited span | cited by (rows) | sha256 before | sha256 after | same? |
|---|---|---|---|---|
| 17-43 | W3-MISR:Cor-G(a)[premises], W3-MISR:R'[premises] | a7be805fe440cc31fc7fe95e38a62bc4fd822987f567d9df296ad82473ad5623 | a7be805fe440cc31fc7fe95e38a62bc4fd822987f567d9df296ad82473ad5623 | YES |
| 17-66 | W3-MISR:Cor-G(b)[premises], W3-MISR:Cor-H[premises], W3-MISR:MIS(i')[premises], W3-MISR:MIS(i)[premises], W3-MISR:MIS(ii)[premises] | d6af6e35453dff9c695dca56ed5a6226d4111190106ee9af38ceb9bd17a30918 | d6af6e35453dff9c695dca56ed5a6226d4111190106ee9af38ceb9bd17a30918 | YES |
| 164-165 | W3-MISR:Cor-G(b)[premises] | 9062c638891edf890e1fce3281d0b6d0426fdf3d6ea3694c5e2747dbccfd20e1 | 9062c638891edf890e1fce3281d0b6d0426fdf3d6ea3694c5e2747dbccfd20e1 | YES |
| 207 | C-MIS:Thm-MIS(i)[notes], C-MIS:Thm-MIS(ii)[notes] | 747abe9f0e829a88354e4819148047a18438a6794aaf9d9f1a8f2e23d08add36 | 747abe9f0e829a88354e4819148047a18438a6794aaf9d9f1a8f2e23d08add36 | YES |
| 222-245 | W3-MISR:Cor-G(a)[premises], W3-MISR:Cor-G(b)[premises], W3-MISR:Cor-H[premises], W3-MISR:MIS(i')[premises], W3-MISR:MIS(i)[premises], W3-MISR:MIS(ii)[premises] | 9155aaa447fa85afcb781e7ba401b6eaa6c9ca6971d4d390eaeba268fe48be11 | 9155aaa447fa85afcb781e7ba401b6eaa6c9ca6971d4d390eaeba268fe48be11 | YES |
| 249-252 | C-MIS:Thm-MIS(i)[notes], C-MIS:Thm-MIS(ii)[notes] | d9d3fc280701a245c4bf0f9821e19d798f6c05df3ee61e58071a044118a1a034 | d9d3fc280701a245c4bf0f9821e19d798f6c05df3ee61e58071a044118a1a034 | YES |

line count before 272, after 272; changed lines: [1, 191, 192, 193, 194, 195]

Line 1 lies in no registered span or premise span. For the recorder: on apply, Cor-H's registry rehash gives sha256 `a4f83d8cfcd5cbebc2898cd2114a6ed3dee01c628d8840a023dccac1dfc672c2` (span 178-197 unchanged); version 1.0.0 → 1.1.0 per the WEAKER tag. The whole-file sha256 goes 797bca0e…4b87 → 84eb0f27…6ce0 (full: `84eb0f27000da51c748b5f708feafc03572286c44ffe2ea08cf275de202e6ce0`). The patch applies cleanly to origin/main (`git apply --check` OK).
