# CHECKPOINT 3 — W3-PSHARP-R (T12; Tier B, NORMAL mode) — 2026-11-16

## Before / after in plain words (for the H5 card; headline row 1.3, PSHARP Cor A1)
**Before** (`W3-PSHARP:A`@1.0.0, Cor A1): on two witness designs (orthogonal null columns, or Gaussian null columns), with
s₀ fixed and p → ∞, the posterior error 1 − π(S₀ | y) is at least (s₀+1)√(log p/(πn)) in probability. In expectation the
same constant was recorded, and only for p → ∞. "No claim when log p = o(log n)" covered both readings.
**After** (`W3-PSHARP-R:AE`, Cor A1-E): on the same witness designs, the posterior mean error satisfies
E[1 − π(S₀ | y)] ≥ (1 − o(1))(s₀+1)·[2(p−s₀)/(2p−1−s₀)]·√(log(p√n/(s₀+1))/(πn)) **for every p**, bounded p included. For
p = n^a the constant is √((a+½)/π) in place of √(a/π). So the √(log n) loss in the posterior mean is present even with a
handful of variables; it is a tail effect of single competitors. The in-probability statement is unchanged.
"No claim when log p = o(log n)" now holds in probability only. On every design only the order n^{−1/2} is proved
(`W3-PSHARP:B`); the √(log n) bounds are on the witness designs only (design-general version: post-freeze POST2-R1).
Bonus (`W3-PSHARP-R:A2C`): at the critical sparsity scale on orthogonal null columns, π(S₀ | y) ≤ e^{−λ} + o_P(1)
(the parent's bound implies only 1/(1+λ)). Nothing in the parent is weakened.
**Buys the paper:** Theorem 3(b) gets an expectation form valid for every p, and the rate-sharpness reading of the
chapter no longer depends on log p ≍ log n for mean-error statements. **Assumptions moved:** N_n → ∞ dropped;
(log p)² = o(n) for a general orthogonal block (automatic when all nulls are used); spherical growth conditions stated in
log(pn). **Evidence:** this checkpoint. **Supersession:** AE implies the parent's Cor A1 expectation display
(`STATEMENT.md:142`); the parent's in-probability clauses stay the record.

## Passing round
Council **R2 (diff round)** on `reviews/MANIFEST_R2.txt`, NORMAL mode: Sol seat gpt-6.1-sol high, `reviews/R2_council_sol.md`,
9.5, gates=PASS; Opus seat Claude Opus 5.5 high (Claude Third), `reviews/R2_council_opus.md`, 9.2, gates=PASS. Per-claim:
both seats ACCEPT `W3-PSHARP-R:AE` and `W3-PSHARP-R:A2C`. R1 (MANIFEST fd8b32a5…): both seats G1–G5 PASS, C 0, S 0; G6 FAIL on
F findings in derived text (TARGET, READER_DELTA), fixed (`reviews/R1_disposition.md`). 11 E items are in `ERRATA.md`.
```
bind: OK, 2 review(s) give a PASS verdict (>= 8.0) on MANIFEST fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e
council cell: R2; MANIFEST fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e; sol=9.5 PASS(reviews/R2_council_sol.md); opus=9.2 PASS(reviews/R2_council_opus.md)
verify: OK MANIFEST fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e
```

## Record
- Chain: lock L01 (Sol) → line check L02 (Sol; A2C CORRECT, AE CORRECT-WITH-FIXES S1) → re-checks L03 (S1 resolved, S2) and
  L04 (S2 resolved; AE CORRECT) → council R1 → R2. All reviews NORMAL mode, Sol or Opus as above; briefs, replies and
  dispositions in `reviews/`.
- DEPS (`DEPS.tsv`, frozen in the manifest): every row under a claim is OK (STMT, AE, A2C, parent rows). Derived rows
  TARGET and READER_DELTA show UNCHECKED in the frozen file; both were checked by the R2 seats (G6 PASS, F findings
  resolved), and that is recorded here rather than in the frozen DEPS. N1 numerics and citecheck are not under a claim.
- citecheck: `reviews/CITECHECK.txt`, 92 token checks + 59 range checks, **0 MISS** (W3-READER text pinned at 88f5dec).
- HOLDS.md (origin/main): no hold.
- Staged ingest `python Theory_work/INFRA/tools/ingest.py claims Theory_work/Wave3/W3-PSHARP-R/REPORT.md --staged`:
  `2 claim(s) to add; 0 problem(s); new tickets ['W3-PSHARP-R']; 2 new assumption(s); 2 sharpness row(s)`;
  `ERROR introduced by this claims fragment: 0`; acceptance REFUSED on **5 × A5-accepted** only: the accept records of the
  consumed parent claims W3-PSHARP:A, :B, :S are stale in the live registry (HQ side; flagged to the manager 11-15; the
  parent files equal their R2 manifest hashes). HQ re-records them (`check.py --acceptance W3-PSHARP:A,B,S --record`), then
  the gates of the two new blocks take the council cell above.

## Per-claim statuses (verbatim from the proof files; HQ records)
- `W3-PSHARP-R:AE` — "PROVED (by this seat, unchecked)" (`lemmas/AE_expectation.md:3`); council R2 PASS as above.
- `W3-PSHARP-R:A2C` — "PROVED (by this seat, unchecked)" (`lemmas/A2C_critical.md:3`); council R2 PASS as above.

## For HQ / W3-READER
- `READER_DELTA.md` v0.3 (checked in R2; supersedes the v0.2 staged at W3-READER `deltas/thm3_W3-PSHARP-R.md`).
- Open items (REPORT §4): constant attainment for E δ_n (numerics suggest yes); A2C on the spherical witness;
  the √(log n) factor in probability when log p = o(log n); design-general √(log n) lower bound (POST2-R1).
- ERRATA (11 E items) for the editorial batch; proposal: a random-(X_{S₀}, θ*) clause for Cor A2-E.
