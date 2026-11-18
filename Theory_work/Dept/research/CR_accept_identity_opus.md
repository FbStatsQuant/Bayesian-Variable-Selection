# CR: infra/accept-identity-case (INFRA J: case-preserving accept identity)

- Reviewer: Opus (independent review sub-agent; read-only)
- Date: 2026-11-15
- Branch: `origin/infra/accept-identity-case` @ `33a851912a940fc5147dafff50f35592a8d8343b` (1 commit)
- Base: merge-base `5ab981e` (as briefed). `origin/main` has since moved to `c90197c`, but it touches nothing under `Theory_work/INFRA/tools/` since `5ab981e`, so the diff applies unchanged.
- Files: `Theory_work/INFRA/tools/bvsreg.py` (+24/-8), `Theory_work/INFRA/tools/test_lifecycle.py` (+33)

## 1. Correctness

**New records are case-preserving on every OS.**
- `_akey(relpath, fold=False)` returns `_pkey(relpath)` with no case change (bvsreg.py:1896-1901). `_pkey` only normalises the path and turns `\` into `/` (bvsreg.py:98-99).
- `accept_artifacts` now writes both artifact kinds through `_akey(..., fold)`: evidence (bvsreg.py:1926) and MANIFEST (bvsreg.py:1936). Those were the only two `_pcase` calls in the acceptance identity. The `ticket-folder=` line already used `_pkey` via `ticket_dir` (bvsreg.py:1718, 1949).
- The only writer is `check.py --record`. It stores `STAMPS[cid] = R.accept_stamp(cid, by, g, aliases, folder)` (check.py:620), which uses the default `fold=False`, and writes that stamp (check.py:745). No writer passes `fold=True`.
- The path's case comes from strings, not from the file system. `resolve_evidence` builds the candidate from the token and base strings (bvsreg.py:1179) and returns it (bvsreg.py:1189). So Windows and Linux now produce the same identity whenever the token resolves on both.

**Legacy folded stamps are accepted for matching only, and only in A5.**
- `accept_stamp_matches` tries the plain stamp first, then the `fold=True` stamp (bvsreg.py:1966-1971). It has exactly one caller: `unaccepted_inputs`, the A5 check (bvsreg.py:2100). No other code compares accept stamps. I grepped every tool for `accept_stamp`, `accept_records` and `STAMPS`: check.py:620 is the writer, and `records` is passed only to `unaccepted_inputs` (check.py:595, 616).
- `fold=True` reproduces the old Windows identity exactly. The old code computed `_pcase(p) = _pkey(p).lower()` on `nt` (bvsreg.py:102-105); the new code computes `_pkey(p).lower()`. Nothing else in the identity was platform-dependent.
- The "stale" and "predates fp2" messages (bvsreg.py:2106-2113) are unchanged.

**A changed artifact still fails.**
- Folding changes only the `<repo path>` part of each `artifact=` line. The content digest (`_digest(lines)`, bvsreg.py:1927/1936), the token, the pin, the row fields, the inputs and the ticket folder all stay in the hash.
- In-memory probe on the branch head: I added one line to every artifact read, then called `accept_stamp_matches(W3-POST2:A0, {plain, folded})`. It returned **False**. With the reads restored, the folded record alone returned **True**.

**Case-collision analysis (Linux, two files differing only in case).**
- For a folded legacy record to match a different file `X/Foo.md` instead of `X/foo.md`, three things must all hold:
  1. the claim's evidence token must resolve on the current tree;
  2. every other identity line must be identical;
  3. the file content must hash to the same digest.
- So the only extra tolerance is "same bytes, path differs only in case". That cannot let different content through.
- Collision risk on the 24-hex fingerprint grows by a factor of 2 (two stamps tried). That is negligible.
- A token whose case resolved only on Windows's case-insensitive file system resolves to MISSING on Linux, so the record fails there. That is the correct (stricter) result.

Nothing else became looser.

## 2. Scope

- `_pcase` is unchanged (bvsreg.py:102-105). Its other callers are unaffected: POST_REVERT lookups (bvsreg.py:113, 535-536, 1331-1332), `repo_file_exists` (bvsreg.py:690), the checkpoint and own-file checks (bvsreg.py:1240, 1273), the INPUTS coverage check (bvsreg.py:1762, 1770), council seat dedup (bvsreg.py:1822-1824), propagate.py:271, and test_lifecycle.py:715.
- Claim-text hashing (`sha256` and statement hash) is untouched. The `fold` parameter is threaded only through `accept_artifacts`, `accept_identity` and `accept_stamp`, and every new parameter defaults to the old behaviour on Linux.
- Accepted side effect: on **Linux**, plain stamps are byte-identical to before. On **Windows**, freshly computed stamps change (that is the fix). Windows records written before the fix stay valid only through the A5 fallback.

## 3. Tests (test_lifecycle.py:1995-2026)

**(a) Folded record matches on Linux.**
- Directly: `accept_stamp_matches(..., {folded})` is True, `{plain}` is True, and a bogus stamp is False (:2004-2006).
- The candidate is chosen so that `plain != folded` (:1999-2000), so the fold is actually exercised. The probe picked `W3-POST2:A0`; all 67 candidates differ by case.
- Through a consumer's A5: the test replaces the claim's events.log accept rows with the folded stamp only, inside the CI sandbox (`INFRA` = sandbox path, :21-22). It then asserts that `unaccepted_inputs` reports no problem with `cid_j` for its direct consumers (:2010-2016).
- This is not vacuous today: the direct consumers are `W3-POST2:A1` (a `stmt` bridge edge, so A5 applies) and `W3-MISR:Cor-G(b)` (`hyp`).

**(b) A fresh record is case-preserving.** `check.py --acceptance <cid> --record` exits 0, and the last accept row equals `plain`, with `plain != folded` (:2018-2026).

**Negative test.** There is **no** negative test that a folded legacy record with *changed artifact content* fails (directly or in A5). The only negative is a syntactically bogus stamp (:2006), which proves nothing about the fold. My out-of-tree probe confirms that the behaviour is correct, but no regression test protects it. See NB-1.

## 4. Runs (throwaway worktree at 33a8519, `TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261115-CR-accept`, `nice -n 10`)

- `python3 Theory_work/INFRA/tools/test_lifecycle.py`: **175 PASS / 0 FAIL**, rc=0. INFRA J test: PASS.
  - The `ROLLBACK FAILED` / `REGISTRY LOCKED` lines in stderr come from the deliberate Sol-1 fault-injection case inside a sandbox ("Sol-1 failed restore writes .TXN_FAILED": PASS). They are not failures.
- `python3 Theory_work/INFRA/tools/check.py --quiet`: **468 claims; 0 ERROR**, 296 WARN, 159 INFO, rc=0.
- Both match the recorder's numbers.

## Findings

- **NON-BLOCKING NB-1 (tests): no negative test for the legacy path.** Add a case where the folded record exists but one cited artifact's content has changed (e.g. append a line to a sandbox evidence file). Assert that `accept_stamp_matches` is False and that the consumer's A5 reports the claim as stale. This protects the property "fold tolerates case only, never content".
- **NON-BLOCKING NB-2 (tests): the A5 subtest could become vacuous.**
  - `a5_ok = ... if cons else True` (:2012-2014) silently passes if the chosen claim has no direct consumers.
  - It also does not require the consumer edge to be one that A5 actually checks. A `hyp` edge under a matching `conditional on` status is skipped, and that skip would also pass.
  - It holds today (`W3-POST2:A1`, a `stmt` edge). Prefer requiring at least one consumer whose A5 traversal reaches `cid_j`, or choosing `cid_j` among claims with such a consumer.
- **NON-BLOCKING NB-3 (lifecycle of the legacy fallback).** 49 claims currently match **only** through the folded stamp: W3-PSHARP:{A,B,C,S}, W3-MISR:{Cor-G(a),MIS(ii),R'}, most W3-START/START2, and W3-RM2. The fallback has no sunset. Consider a planned re-`--record` of these claims on Linux, after which the fold path could be removed, or at least an INFO count of fold-only matches.
- **NON-BLOCKING NB-4 (cost).** On a miss, `accept_stamp_matches` computes the identity twice, including re-reading and re-hashing every artifact. That is fine at the current scale. Computing the identity once and folding the artifact path segments would halve the cost.
- **NON-BLOCKING NB-5 (pre-existing, out of scope).** `repo_file_exists` uses `os.path.isfile` (bvsreg.py:693), so on Windows a case-mismatched evidence token resolves, while on Linux it is MISSING. INFRA J correctly does not paper over this. A separate check that the token's case matches git's case would close the remaining Windows/Linux gap.

No BLOCKING findings.

CR-VERDICT: APPROVE
