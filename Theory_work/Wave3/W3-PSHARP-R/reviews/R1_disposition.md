# R1 disposition — council round R1, MANIFEST fd8b32a5540e5afcfdb73b94048ba7a1324f30a89ade786508ea04e9295bfc30

| seat | file | per-claim | score | gates | C/S/F/E |
|---|---|---|---|---|---|
| sol (gpt-6.1-sol, high) | `reviews/R1_council_sol.md` | AE REJECT (on F1 only), A2C ACCEPT | 7.8 | FAIL (G6) | 0/0/1/3 |
| opus (Claude Opus 5.5, high, Claude Third) | `reviews/R1_council_opus.md` | AE ACCEPT, A2C ACCEPT | 8.6 | FAIL (G6) | 0/0/2/8 |
Both seats: G1–G5 PASS; mathematics of both lemmas re-derived and correct; no C or S finding.

| finding | decision | change (diff `reviews/R2_diff.txt`) |
|---|---|---|
| sol F1 = opus F-1 — two-sided expectation rate in derived copies (`TARGET.md:28`; sol also `READER_DELTA.md:22` §2 item 3) | ACCEPT | TARGET row A1-E(b) now states the lower bound only (sol's exact text, with the constant); READER_DELTA §2 item 3 replaced by sol's exact text. Tag [R1-F1]. |
| opus F-2 — reader growing-s₀ remark covers (N-gauss) with random X^r_{S₀}, beyond Cor A2-E | ACCEPT, option (a) (restrict) | READER_DELTA §3 remark restricted to orthogonal null columns and Gaussian null columns with the S₀ columns fixed; bridge B3.7 says "(N-orth), or (N-gauss) with X^r_{S₀} deterministic". Tag [R1-F2]. Option (b) (a random clause for A2-E) logged as a proposal in ERRATA. |
| E findings (opus E-1…E-8, sol E1…E3) | recorded | `ERRATA.md`; not applied now (v4 §5.3). |

No change to STATEMENT or to either lemma; DEPS rows STMT, AE, A2C unchanged and OK. Diff round R2 (v4 §5.5): new
manifest `reviews/MANIFEST_R2.txt`; each seat, in a fresh thread, gets its own R1 review, the diff, and the DEPS dependents
of the changed objects (TARGET.md and READER_DELTA.md have no dependents under a claim).
