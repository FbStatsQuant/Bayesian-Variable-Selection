# Adversarial tests of the LOWP verifiers

Run 2026-10-29 03:03 UTC by `tests/test_adversarial.R`; sealed study `C:/Users/felip/AppData/Local/Temp/lowp_work/gen/study`; R version 4.4.1 (2024-06-14 ucrt). **ALL PASS: 49 of 49 probes behave as required.**

Probes follow Sol's review (findings 1-5, 7, 8) and the NOTS verifier gate semantics (exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE or malformed). A9* run the truth-lock algorithm on a modelled POSIX tree; the real ordinary-user Linux test is `tests/test_truth_lock_linux.sh` (to be run in the NOTS pilot).

| Id | Probe | Required | Observed | Result |
|---|---|---|---|---|
| A0 | control: untouched sealed dev dataset passes every per-dataset gate | 0 problems | 0 problems | ok |
| A1 | input object carries truth fields active/beta | schema problem naming them | unexpected input fields (truth leakage?): active,beta | ok |
| A1b | input object carries truth fields signal/eps | schema problem | unexpected input fields (truth leakage?): signal,eps | ok |
| A1m_n | required I1 field `n` deleted from the input object (all else valid) | schema problem naming it | missing I1 input fields: n | ok |
| A1m_kind | required I1 field `kind` deleted from the input object (all else valid) | schema problem naming it | missing I1 input fields: kind | ok |
| A1m_scales | required I1 field `scales` deleted from the input object (all else valid) | schema problem naming it | missing I1 input fields: scales | ok |
| A1m_all | all three required fields n, kind, scales deleted together | schema problem naming all three | missing I1 input fields: n,kind,scales | ok |
| A2 | input metadata p=999, n=1, kind=prod, scenario=3, replicate=4, scales doubled (id and seeds untouched) | >= 6 metadata problems | 9 metadata problems | ok |
| A3 | signal + 1 with Y rebuilt from it and Y/signal hashes updated (previous gates all pass) | signal gate fails, response gate passes | signal problems 1, response problems 0, hash problems 0 | ok |
| A3b | signal scaled by 1 + 1e-9 (tolerance is explicit, 1e-12 relative) | signal gate fails | signal problems 1 | ok |
| A3c | truth object with an extra field | truth schema problem | truth fields are not exactly {active,beta,signal,eps,scenario,dataset_id} | ok |
| A4c | control: sealed prod and dev manifests validate against the exact grids | no problems | 0 / 0 | ok |
| A4 | dev p20/S2/r5 replaced by r100 (60 unique rows, consistent ids/seeds/paths) | structure problem (grid) | inputs manifest ids differ from the expected grid (missing 1, unexpected 1) | ok |
| A5a | production manifest missing a row | structure problem | inputs manifest has 1199 rows, expected 1200 | ok |
| A5b | duplicate dataset_id (1,200 rows) | structure problem | duplicate dataset_id in inputs manifest: p0020_S1_r001 | ok |
| A5c | out-of-range replicate 101 (consistent id) | structure problem | inputs manifest ids differ from the expected grid (missing 1, unexpected 1) | ok |
| A6 | non-canonical relative path (right basename, wrong per-p directory) | structure problem | non-canonical inputs file path for 1 rows (e.g. p0020_S1_r001: inputs/p0030/p0020_S1_r001.rds) | ok |
| A6b | fold_seed = 999 in one manifest row | seed problem naming fold_seed | fold_seed differs from base + 10000*s + r for 1 rows (e.g. p0020_S1_r005: manifest 999, design 3220005) | ok |
| A6c | inputs manifest with the benchmark column name foldid_sha256 instead of I1 fold_sha256 | structure problem | inputs manifest columns differ from I1 (got: dataset_id,p,scenario,replicate,data_seed,fold_seed,method_seed,file,file_sha256,x_sha256,y_c100_sha256,y_c075_sha2 | ok |
| A7 | S6 p20 with blocks 1 and 4 exchanged: pooled mean unchanged, blocks wrong | block gate FAIL while pooled deviation < 0.02 | pass=FALSE, max block dev 0.300 (block 4), pooled dev 0.0002 | ok |
| A7c | control: correct S6 p20 (100 fresh replicates) | block gate PASS | pass=TRUE, max block dev 0.0021 | ok |
| A8 | p20 data base set to master's p500 base 1,410,000 | collision reported | pass=FALSE, 7 collisions | ok |
| A8b | p20 dev data base 1,220,000 (shifted by one slot: overlaps the p20 production data set) | collision reported | pass=FALSE, 7 collisions | ok |
| A8c | control: actual families (80 sets, 3,160 pairs; includes dev method/repeat and held-out method/repeat families) | PASS, 80 sets, 3160 pairs | pass=TRUE, 80 sets, 3160 pairs | ok |
| A9a | modelled POSIX tree: lock gives mode 000 on every directory (both trees) and file; contents unreachable; one call | all 9 modes 000, root unlistable | modes: 0,0,0,0,0,0,0,0,0; ls(/s/truth) = NULL | ok |
| A9b | modelled POSIX tree: ONE unlock call after a full lock restores dirs 755 and files 444 (root first, each directory before descending) | dirs 755, files 444 | modes: 755,755,755,755,755,444,444,444,444 | ok |
| A9c | a failing chmod on one file during locking is not ignored | error naming the path | chmod 444 failed on /s/truth/p0030/c.rds | ok |
| A9d | idempotence: lock, lock, unlock, unlock | final modes 755/444 | root 755, file 444 | ok |
| A9e | partially locked tree (truth, truth/p0020, one file at 000) repaired by one unlock call | dirs 755, files 444 | root 755, p0020 755, file 444 | ok |
| B1 | control: full manifests (1,200 + 60), dev manifests, all six pilot copies | exit 0 | exit 0 | ok |
| B2 | empty (0-byte) production manifests | exit 3 | exit 3 | ok |
| B3 | header-only production manifests | exit 3 | exit 3 | ok |
| B4 | one correct production row only | exit 3 | exit 3 | ok |
| B5 | --study points to a nonexistent directory | exit 3 | exit 3 | ok |
| B6 | --study omitted | exit 3 | exit 3 | ok |
| B7 | one production row with fold_seed = 999 | exit 1 | exit 1 | ok |
| B8 | one wrong X hash in the production manifest | exit 1 | exit 1 | ok |
| B9 | dev manifests omitted (no dev/manifests next to the production manifests) | exit 3 | exit 3 | ok |
| B10 | only five of the six pilot copies present | exit 3 | exit 3 | ok |
| B11 | a pilot copy whose X differs by 1e-9 in one entry | exit 1 | exit 1 | ok |
| B12 | duplicated dataset_id (still 1,200 rows) | exit 3 | exit 3 | ok |
| B13 | replicate 101 replacing p0030_S6_r100 (consistent id/seeds/paths) | exit 3 | exit 3 | ok |
| B14 | non-canonical relative path in one inputs row | exit 3 | exit 3 | ok |
| B15 | dev manifests with 59 rows | exit 3 | exit 3 | ok |
| B16 | dev row with a wrong fold_seed | exit 1 | exit 1 | ok |
| B17 | wrong inputs-manifest schema (foldid_sha256) | exit 3 | exit 3 | ok |
| B18 | bad command line (no --out) | exit 3 | exit 3 | ok |
| C1 | lowp_verify.R without --bench-gen (no original helper source) | exit 3 (check 7 INCOMPLETE, no FAIL) | exit 3 | ok |
| C2 | --bench-gen pointing to a nonexistent file | exit 3 (INCOMPLETE) | exit 3 | ok |
