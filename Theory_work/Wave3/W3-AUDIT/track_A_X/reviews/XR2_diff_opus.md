# XR2 diff round — seat `opus` (Claude Opus 5.5, high) — W3-AUDIT track A_X: X1, X3, X5, T14

Manifest: `MANIFEST 5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6`. I verified it before reading with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_X Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/MANIFEST_XR2.txt`,
which returned `verify: OK`. `git diff --quiet 4676af6 -- Scripts/SMC_BVS/core` confirms the core is the pin.
Inputs read: my brief, my own XR1 review (`XR1_council_opus.md`), `DIFF_XR1_to_XR2.patch`, and the changed T14 text.
For the new Step 3 I read `cpp/v3_start.h:40-120, 185-307` at the pin. I opened `Theory_work/INFRA/DECISIONS.md:95`
again, and only to recheck E8. I did not open the other seat's review or any disposition. I did not re-read the unchanged
X1/X3/X5 text.

## (1) Status of my XR1 findings
| finding | sev | status | note |
|---|---|---|---|
| F1 (T14 brought in EX-A/(H2-FP) through T9) | F | **RESOLVED** | Step 3 now uses a structural bound, \|m.S\| ≤ max(k̂, 0) ≤ K, in place of T9. I checked it below. The Conclusion is reworded to match ("integer structure of `start_mode`; no arithmetic idealisation"). The hypotheses used now match the hypotheses stated. |
| E1 (X1 ledger attribution) | E | NOT RESOLVED | X1 is unchanged. Editorial only, so it does not affect the verdict. |
| E2 (X1 off-path list) | E | NOT RESOLVED | as E1 |
| E3 (X3 summary omits p ≥ 2) | E | NOT RESOLVED | as E1 |
| E4 (X5 source copy truncated) | E | NOT RESOLVED | as E1 |
| E5 (X5 vs T5 CAL-d wording) | E | NOT RESOLVED | as E1 |
| E6 (X5 MEAS-J / "only under" / R = 4) | E | NOT RESOLVED | as E1 |
| E7 (T14 ℓ_n range) | E | **RESOLVED** | STATEMENT (REP-b) now gives ℓ_n ∈ [3, 32], which matches PROOF Step 2. |
| E8 (T14 "19 claims" source; changelog) | E | **PARTLY RESOLVED** | A changelog table now exists. "(19 claims)" at `T14_REP/STATEMENT.md:13` still cites `DECISIONS.md:95`, and that line has no count (I re-read it: "Batch NARROW (A:IDEAL-W⁺ or (D)) as task S4"). Cite the source of the count or drop the number. Editorial only. |

## (2) Does the diff break anything?
I found no new C, S or F finding. I re-derived new Step 3 against the code at the pin:

- **(1)** In `mode_dp` (`v3_start.h:220-224`), the only write to `kbest` is inside `for (int k = 0; k <= K; ++k)`, so
  k̂ ∈ {0..K} ∪ {−1}. Correct.
- **(2)** In `rec(J, k̂)` (`:281-301`), each edge subtracts j from r and a leaf is accepted only when r = 0. Codes come from
  `arg[b-1][j]`. That vector is filled only from `codes_by_size[b][j]` (`:206-209`), and each of those codes has popcount j
  (`:111`) with bits below m_b. `S.size()` therefore equals Σ_b j_b = k̂ exactly. Note that this count does not even need
  the blocks to be disjoint, because S is sorted but never deduplicated. If k̂ = −1 the loop `j <= r` never runs,
  `bestS` stays empty and `count` = 0, so the fallback cannot fire either. Correct.
- **(3)** The step "feasibility is preserved because a witness path for (IN, OUT) cannot contain i" is right. `feasible()`
  is reachability over tight edges whose j has *some* code consistent with IN/OUT, and the constraints are per block.
  So a witness is a tight path together with per-block codes. If adding i to IN fails, every witness for (IN, OUT) avoids
  i, and is therefore a witness for (IN, OUT ∪ {i}). The root check `:261` excludes k̂ = −1 (it throws, so the cap site
  is never reached). At the end, the witness code c_b satisfies inm[b] ⊆ c_b ⊆ ¬outm[b] in each block, so |IN| ≤ Σ_b j_b = k̂.
  Equality also holds once inm ∪ outm covers every position of the block. Correct.
- The remark "integer bookkeeping on whatever doubles" is accurate. `mode_tight` and `rec` compare doubles with `==`, but
  only the graph structure (j decrements, popcounts, reachability) enters the size bound.
- The arithmetic is unchanged and still correct: K = min(p, n/2) ≤ 2³⁰ − 1, so cap_ll ≤ 2³⁰ + 31 < INT_MAX. (REP-b)'s
  "≤ 32 + ⌊n/2⌋" follows from |S̃₀| ≤ K ≤ ⌊n/2⌋.
- CITECHECK lists 36/36 OK, and the 5 new citations are the lines I read. CHECK.md's frozen hashes are updated to v1.
  The changelog tags v1 as EQUAL, which is right because the claim did not change.

**E9 (E, new) — T14 Step 3 (3): the step from block positions to indices is not cited.** In "IN ∪ OUT = {0..p−1} ⇒ IN
equals that path's set", and in the count |IN| ≤ Σ j_b, the proof needs (blk, pos) to be injective from {0..p−1} into the
block positions, and onto them for equality. That map is built at `cpp/v3_start.h:80` from `st.blocks`, which partitions
the internal columns. The bound needs only injectivity, and the partition is the block construction's standing invariant,
so the claim is not at risk. A one-clause citation (`cpp/v3_start.h:80`; blocks partition {0..p−1}) would close this
last implicit step. The claim does not depend on it, because |IN| ≤ k̂ is all (REP-b) needs.

## (3) Per-claim decisions
| id | decision |
|---|---|
| X1 | ACCEPT |
| X3 | ACCEPT |
| X5 | ACCEPT |
| T14 | ACCEPT (F1 resolved; E8 remainder and E9 are editorial) |

## (4) Gates
| gate | result |
|---|---|
| G1 correctness | PASS |
| G2 hypotheses used = stated | PASS (F1 resolved) |
| G3 no hidden assumptions | PASS (F1 resolved; E9 is a citation gap on a structural invariant, not a hidden premise) |
| G4 imports and statuses verbatim | PASS (E8 remainder is description-level) |
| G5 scope and constants | PASS |
| G6 fidelity to pinned code | PASS |

## Score (C, S, F only)
**9.5 / 10.** No C, S or F finding remains. The open items are editorial (E1–E6 untouched, E8 partly fixed, E9 new).

COUNCIL-VERDICT round=R2 manifest=5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6 seat=opus score=9.5 gates=PASS
