# R2 council review — seat `opus` (Claude Opus 5.5, effort high; diff round) — W3-PSHARP-R

Content reviewed: MANIFEST `fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e`
(`reviews/MANIFEST_R2.txt`).

**Manifest check.**
- I recomputed the sha256 of all 21 rows (14 ticket files and 7 external inputs). Every row matches.
- The digest of the stored rows reproduces `fdfd4562…`, so this review covers exactly that content.
- Compared with `MANIFEST_R1.txt` (`fd8b32a5…`), the only changes are:
  - `TARGET.md`, `READER_DELTA.md` and `DEPS.tsv`, which changed;
  - `ERRATA.md`, which is new.
- Every other row, including `STATEMENT.md`, both lemma files, the numerics and all external inputs, is byte-identical to R1. My R1 re-derivations therefore carry over unchanged.

**What I read.**
- My R1 review and `reviews/R2_diff.txt`.
- `TARGET.md` and `READER_DELTA.md` in full, plus `ERRATA.md` and `DEPS.tsv`.
- `STATEMENT.md` §2–§4 (:40-119), for comparison.
- In the on-disk W3-READER `READER_VERSIONS.md`, the (S1)/(S2) and (N-orth)/(N-gauss) definitions, to decode the labels again.
- I did not read the other seat's review, any disposition, `LOG.md` or the checkpoints.

## 1. Status of my R1 findings (C/S/F)

| finding | status | reason |
|---|---|---|
| F-1 (`TARGET.md:28`, two-sided "E δ_n ≍ r_n at fixed p") | **RESOLVED** | See F-1 below. |
| F-2 (`READER_DELTA.md:47-48` + B3.7, growing-s₀ remark under (N-gauss) with random X^r_{S₀}) | **RESOLVED** | See F-2 below. |

**F-1.**
- The row now reads "E δ_n ≥ (1 − o(1))C_{p,s₀} r_n at fixed p, C_{p,s₀} = (s₀+1)[2(p−s₀)/(2p−1−s₀)]/√(2π) (a lower bound of order r_n; no upper bound claimed)".
- This is exactly Cor A1-E(b), `STATEMENT.md:83-84`.
- C_{p,s₀} > 0 because p ≥ s₀ + 1, so "of order r_n" is correct.
- No other two-sided fixed-p claim remains in TARGET:
  - :18 says "Conclusion level: negative / lower bound";
  - :38 says "attained numerically … (not claimed)".
- READER_DELTA §2 item 3 (:22-23) was also adjusted, and it agrees with `STATEMENT.md` §4.1 :110-114.

**F-2.** I chose correction (a).
- The reader sentence (:48-50) now covers "orthogonal null columns, and Gaussian null columns with the columns in S₀ fixed (nonrandom)".
- B3.7 (:75) now says "(N-orth), or (N-gauss) with X^r_{S₀} deterministic".
- Coverage check against Cor A2-E(ii) (`STATEMENT.md:88-91`):
  - **(N-orth) with 𝒩 = [p]∖S₀** gives (W-orth), and (W-orth) gives p ≤ 2n, hence (W-orth-E).
  - **(N-gauss) with X^r_{S₀} deterministic** satisfies the spherical structure of (W-sph-E) through the (W-sph) example at :55-57:
    - the nulls are independent of X^r_{S₀} and of ε;
    - θ* is a fixed sequence in the reader's model;
    - (S2) p ≤ n^A gives (log p)² = o(n);
    - A2-E drops the rank condition, so growing s₀ needs nothing more.
  - s₀ ≤ p/2 is in the remark's standing proviso (:39) and in B3.7.
- The remark is now fully covered by the master claim plus the listed bridge.

## 2. Does the diff break anything?

No. The diff creates no new C, S or F problem, and no new mismatch with STATEMENT.
- **TARGET :28.** The constant and the fixed-p hypothesis match STATEMENT :83-84 symbol for symbol. The (a)/(c) columns are unchanged and still correct.
- **READER_DELTA :22-23.** "Exactness is asserted only where a matching expectation upper bound is available" agrees with the reader text :45-47 and with STATEMENT §4.1. It no longer restates the parent's "exact whenever log p ≍ log n" for expectation.
- **READER_DELTA :48-50 and :75.** The restriction is consistent between the reader text and the bridge table.
  - It is not stronger than needed: the random-X^r_{S₀} extension remains true, as sketched in R1 F-2(b). The reader now simply does not claim it.
  - The critical-scale sentence and its A2C bridge are unchanged.
- **DEPS.tsv.**
  - The new and changed rows carry the correct sha for TARGET (`168ce342…`) and READER_DELTA (`a7f9d04c…`), both marked UNCHECKED.
  - REPORT is marked OK with checked_sha equal to its unchanged sha. That rests on R1 G4, which is accurate.
  - The claim rows (STMT, AE, A2C) and the PARENT rows are unchanged and still match.
- **ERRATA.md.** Each of my E-1…E-8 is recorded with its place and correction. E-2 now cites a relative s.e. bound of 2.3·10⁻³ instead of my 2.2·10⁻³; that is within rounding and not a finding. The two proposals are carried forward as non-findings.

The E items left in derived text are recorded in ERRATA and are non-blocking under PROTOCOL_v4 §5.3: the READER_DELTA :6 vs :62 status wording, and "p = n^a" at :40. Per the brief, I add no new E findings.

## 3. Per-claim decision

| id | decision |
|---|---|
| `W3-PSHARP-R:AE` | ACCEPT |
| `W3-PSHARP-R:A2C` | ACCEPT |

Both claims, their proofs and STATEMENT are byte-identical to R1, where I re-derived them in full and accepted them.

## 4. Gates on MANIFEST `fdfd4562…`

- **G1 correctness — PASS.** The claims and proofs are unchanged from R1, where every step was re-derived; see R1 G1.
- **G2 hypotheses used = stated — PASS.** Unchanged. The repaired READER_DELTA remark now uses only hypotheses under which A2-E holds.
- **G3 no hidden assumptions — PASS.** Unchanged. The determinism of X^r_{S₀} is now stated where it is used.
- **G4 statuses, citations, records — PASS.** The DEPS rows for the changed files carry correct hashes and honest UNCHECKED states. ERRATA faithfully records the R1 editorial items.
- **G5 constants and rates — PASS.** The C_{p,s₀} in TARGET :28 equals the A1-E(b) constant.
- **G6 faithfulness — PASS.** F-1 and F-2 are resolved. TARGET and READER_DELTA now claim no more than the masters plus the listed bridges.

## Score and counts

- Open findings from this seat: C 0, S 0, F 0.
- E: 8 from R1, all recorded in ERRATA and non-blocking.
- The mathematics is correct throughout, and both blocking derived-text issues are repaired precisely.
- Score: **9.2**.

`COUNCIL-VERDICT round=R2 manifest=fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e seat=opus score=9.2 gates=PASS`
