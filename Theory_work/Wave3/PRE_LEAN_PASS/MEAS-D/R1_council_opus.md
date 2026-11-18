# R1 council review (Opus seat): W3-SAMP:MEAS-D

**Manifest verify:** `python3 Theory_work/Wave3/tools/manifest.py verify …/MEAS-D/ticket …/MANIFEST_MEASD.txt` printed `verify: OK MANIFEST 7fbc2f86e20994967f466b5fb373e1d3427046ad162136615f5a6a4c6a1c09c9`.

**Code pin:** `git diff 4676af6 HEAD -- Scripts/SMC_BVS/core` changes only `README.md`, `v3_fit.R` and `v3_run.R`, which are the list-PIP fields. `cpp/v3_core.cpp` and `cpp/v3_engine.h` are the same as at the pin, so every code line quoted below is pin code.

**Scratch:** the converter ran on a copy in `.rc_tmp/measd_r1_opus/`. No tracked file was modified, nothing was committed, and no subagents were started.

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 | REJECT | **Step 1** is correct. Valid inputs: `W3-RM2-R/STATEMENT.md:90-93`. The branch is a function of (n, p): `v3_budgets(n,p)` → `exact_branch`, `v3_preprocess.R:19-28`, `v3_fit.R:106`. **Step 2** is correct for what it lists. H = (n+1)G_S + I and A = G_S + I are always positive definite (`cpp/v3_score.h:175-183`). The standardisation branch at `v3_preprocess.R:47` gives the same value under EX-A. But Step 2 leaves out one data constant, the neighbour graph (F2). **Step 3** is a faithful citation of CAL-C (CAL-b) and PROOF Step 3, `T5_CAL/PROOF.md:34-48`. **Step 4**: the search bound (at most cap + 1 scans) is correct, and so are the ledger comparisons (`v3_util.h:121-126`, `v3_ledger.h:36-42`). The island input list leaves out the neighbour graph (F2). **Step 5** proves the conditional form only for functions of a single final stream U^{(9+r)}, while the statement claims it for every §2 identity, including clauses that read several streams (F1). |
| 2 | ACCEPT | The four call sites and the routine are re-checked in §2 below. (a) All four call `Engine::local_search`. (b) The loop is bounded. (c) The scan tie rule is F, then `lex_less`. (d) The routine reads no uniform, no clock and no guard. (e) The caps are ℓ_n = ⌈log₂(n+p+1)⌉ (`v3_preprocess.R:23`), and ℓ_n + abs(S̃₀) for LS0. |
| 3 | REJECT | The potential-only scope holds: STATEMENT.md:190-192, the pointer sentence at :36, MEAS_D §0(i) and the REGISTRY conclusion all disclaim the actual 𝒜, 𝒪 and the guard. The one failure: the "Consequently" sentence claims more than Step 5 proves (F1). Two wordings are loose: E3 ("every reported statistical field") and E4 (the §4 "serves" list quotes {completed} clauses without the GW-iv route). |
| 4 | REJECT | The cited statuses match claims.tsv (§4 below). The REGISTRY `depends_on` names `W1-N1:Thm-N1@proof:freezing-lemma-L3`, but the lemma actually used, `L3_freezing.md`, is registered as `W1-N1:F` (F3). Two pins are off by a few lines: `T1_GW/STATEMENT.md:98-101` (E1) and `W3-READER/STATEMENT.md:33-36` (E2). |
| 5 | ACCEPT | `ingest.py convert` on the scratch copy exits 0, with id W3-SAMP:MEAS-D and lines [190, 192]. Before/after: 186 → 192 lines, and the only change to §§0-3 is the end of :36 (`diff` shows `36c36`, then `186a187,192`). STATEMENT.md:188-192 contains no `|`. The only `|` characters in the REGISTRY block are field separators. |
| 6 | ACCEPT | MEAS_D.md:83-85 states EX-A, the dependence on recorded readings at pin 4676af6, and the re-pin remark. One small addition is suggested in E7. |

## 2. Call-site re-check (item 2), quoted

- `v3_core.cpp:456`: `LocalArchive A = E.local_search(led.hpmS, o.ell, o.tier, false);  // final local search from the global best (R4)`
- `v3_core.cpp:476`: `LocalArchive A0 = E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0);`
  - The cap comes from `:472-474`: `cap_ll = o.ls0_ell + (o.ls0_cap_plus_mode ? m.S.size() : 0)`.
  - `o.ls0_ell` defaults to `b$ell` (`v3_run.R:95`), and `b$ell = v3_ceil_log2(n + p + 1)`.
- `v3_core.cpp:642`: `LocalArchive A = E.local_search(c->led->hpmS, ell, tier, false, 0);`
- `v3_core.cpp:689`: `LocalArchive A = E.local_search(c->led->hpmS, ell, tier, false, iter);`
  - Here `ell` is `cs$ell = b$ell` (`v3_calib.R:12, 44, 86`).
- **Routine:** `v3_engine.h:379`, `LocalArchive local_search(const std::vector<int>& centre, int ell, int tier, bool emit_centre, int iter = -1, int phase = PH_LOCAL)`.
- **(b) The loop is bounded.** The loop is `while (true)` at `:385`. It has exactly two exits:
  - `:409-410`: `if (A.moves >= ell) { … "move_limit" … break; }`
  - `:414`: `"no_improvement" … break;`
  - `A.moves++` at `:412` is the only increment. So there are at most ell moves and at most ell + 1 scans.
  - Each scan considers at most p flips plus |S|(p − |S|) swaps (`:394-406`), and additions at size K are skipped (`:397`).
- **(c) The tie rule** is at `:392`: `if (!have || q.F > best.F || (q.F == best.F && lex_less(q.S, best.S)))`.
  - It is F first, then plain lexicographic order (`v3_util.h:117-119`). There is no size step.
  - The brief's "score, then size, then lexicographic" describes `hpm_better` (`v3_util.h:121-126`), which the ledger uses, not the scan. The lemma's wording ("lexicographic tie rule", MEAS_D.md:20, 38) matches the code.
  - A move needs strict improvement: `best.F > C.F` (`:408`).
- **(d) No uniform, clock or guard inside the routine.**
  - The routine's body (`:380-418`) calls only `set_model`, `eval`, `bit_get`, `del_var`/`add_var` and `lex_less`.
  - `eval` (`:89-101`) calls the scorer, the cache, `st.comp` and `led->event`, and `Ledger::event` (`v3_ledger.h:104-113`) contains no RNG, clock or guard.
  - In the engine, `vs`/`u(` appear only in the island steps, `Clock::now` only at `:284-348` and in `run_island`, and `guard` only at `:62` and `:335`.
  - The operational checks all sit after a search returns: `v3_core.cpp:459, 480, 645, 692`. The timers `t0`/`t1` at `:455` and `:470` are also outside the routine. In P° every one of these Booleans is FALSE (GW-v, `T1_GW/STATEMENT.md:93-95`).
  - The only non-operational exit inside the routine is a `NumericalFailure` from `Scorer::score` (`v3_score.h:237`). Under EX-A it cannot be reached, because H and A are positive definite. In any case it is a branch on comparisons (see E5).
  - The range check `stop("LS0 move cap out of range")` at `:475` runs before the call and depends only on (o.ls0_ell, abs(S̃₀)).
- **(e) The caps are functions of (n, p), and of S̃₀ for LS0.** Confirmed above. The `tier` argument sets only `ev.tier`, which is bookkeeping (`:381`).
- **Nothing in the code breaks the lemma's reading.**

## 3. Findings

**F1 (Step 5 is for one stream; the "Consequently" clause covers several). `MEAS_D.md:42-44`; `STATEMENT.md:190`; REGISTRY conclusion.**
- **Problem.** Step 5 conditions only g(data, 𝓒°, U^{(9+r)}), with U "~ the law of one stream". Following L3, independence is used per island (`L3_freezing.md:9-11`; PoolZ Remark (i): "SI is per island").
- The statement nevertheless says "every identity or bound of §2 stated 'given 𝓒 on 𝒜'" holds conditionally on (data, 𝓒°). Some of those clauses read several final streams:
  - D's "exponent 4D_r under IND-T" (`STATEMENT.md:102-103`);
  - anything about the final local search, whose centre is the global best over all four islands (`v3_core.cpp:456`), and about 𝓜, 𝒯 and Ŝ.
- For such a g the one-stream argument does not apply.
- **Exact correction, Step 5.** Replace "U^{(9+r)} is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI …)" by:

  > "U^{(10:13)} := (U^{(10)}, …, U^{(13)}) is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI as idealised, `STATEMENT.md:35-36`, read for the four final streams jointly), hence of (data, 𝓒°)."

  Then use g(data, 𝓒°, U^{(10:13)}) and "U ~ the joint law of the four final streams at fixed data (iid U[0,1) coordinates; IND-T where a §2 clause uses it)".
- **Alternative.** Keep Step 5 as it is and restrict the statement to "…holds, for each island r and for finite sums of single-island quantities, …".
- Either way, the statement should name the reading of H-U/SI it uses.

**F2 (a data constant is missing: the neighbour graph). `MEAS_D.md:32` (Step 2) and `:37` (Step 4, islands).**
- **Problem.** Lemma B (B-d) gives joint measurability in (grid values, *data constants*, u) at fixed data (`L1_bridge.md:119-121`).
- To get measurability in the data as well, every data constant the island reads must be Borel in (X^r, y^r). Step 4 lists only "(grid values, scores, U^{(9+r)})", and Step 2 lists scores, start weights, d, Z, π, π₀, the block partition and S̃₀.
- The neighbour graph `Nb = neighbour_graph(D, B)` (`cpp/v3_blocks.h:149-173`; used by the neighbour-swap step, `v3_engine.h:160-161`, and passed to the final engine at `v3_core.cpp:410`) is a data-dependent input that the proof never covers.
- It is Borel, so the gap is only in the proof, but it is real.
- **Exact correction, Step 2.** Append:

  > "The neighbour graph N(X) (`cpp/v3_blocks.h:149-173`) is determined by finitely many comparisons of the continuous abs(r_jl) among themselves (index tie-break) and with the constant (2 log p / n)^{1/2}, so it is finite-valued with Borel level sets."

- **Exact correction, Step 4.** Replace "(grid values, scores, U^{(9+r)})" by:

  > "(grid values, the data constants of Lemma B: the scores, the start tables and block partition, the neighbour graph, and the cache capacity 500p; and U^{(9+r)})"

  and add "all Borel in the data by Step 2".

**F3 (wrong dependency id for the freezing lemma). `REPORT.md` §8 REGISTRY `depends_on` (staged patch line 18).**
- **Problem.** The block cites `W1-N1:Thm-N1@proof:freezing-lemma-L3`. Step 5 uses `W1-N1/lemmas/L3_freezing.md`, which is its own registered claim, `W1-N1:F` (claims.tsv: `Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md 21-23`, v1.0.0).
- With the current id, a revision of Lemma F would not flag MEAS-D in the DAG.
- **Exact correction.** Replace that entry with `W1-N1:F@stmt`. Keep `Thm-N1` only if some other step uses Theorem N1 itself, and none does.

**E1. `MEAS_D.md:12`.** The pin `T1_GW/STATEMENT.md:98-101` starts at the binary64 bullet (:98). The clock sentence is at :99-102. Change it to `T1_GW/STATEMENT.md:99-102`, or `:97-102` to include the heading.

**E2. `MEAS_D.md:73`.** `W3-READER/STATEMENT.md:22-23, 33-36`: lines 33-36 are "gives the last form. ∎", a blank line and Remarks. The joint-law step of PoolZ's proof is at :28-33. Change it to `:22-23, 28-33`.

**E3. `STATEMENT.md:190` and `MEAS_D.md:24`.** "hence 𝓜, 𝒯, Ŝ and every reported statistical field" can be read as the actual reported output. Change it to "hence 𝓜, 𝒯, Ŝ and every statistical field of P°'s output".

**E4. `MEAS_D.md:65-66, 75-77`.** The "serves" list quotes clauses written with {completed}, for example "P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0", without saying how MEAS-D reaches them. Add after the W3-DIST bullet:

> "MEAS-D makes only the potential events measurable; each {completed} clause is reached through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv), as an outer-probability bound if the clock is not modelled (`T1_GW/STATEMENT.md:99-102`)."

**E5. `MEAS_D.md:38` and `:46`.** Name the two non-operational exits of the final-run searches and state that they are harmless for measurability:
- the `NumericalFailure` throw inside `eval` (`v3_score.h:237`), which cannot be reached under EX-A because H = (n+1)G_S + I and A = G_S + I are positive definite (`v3_score.h:175-183`);
- the LS0 cap-range `stop` (`v3_core.cpp:475`), a function of (n, p, abs(S̃₀)).

Both are branches on Borel predicates, so 𝒪° stays Borel.

**E6. `MEAS_D.md:30, 40`.** On the exact-enumeration cells, 𝒪° = {`v3_enumerate` status "exact"} is a data-only event, and Step 4's argument does not cover it. Add one line: "On the enumeration cells 𝒪° and the reported fields are finite comparisons and sums of the continuous scores of Step 2, hence Borel."

**E7. `MEAS_D.md:85`.** The re-pin remark should add that `v3_list_fields` (`v3_run.R`, re-pin) also has branches on comparisons and a `stop` on a duplicate store entry. These leave 𝒪° Borel, with the `stop` adding only a Borel event (expected empty).

**E8. `STATEMENT.md:190`.** "under the joint law of §0" depends on H-U/SI without naming it. Write "under the joint law of §0 (H-U/SI, :35-36)".

## 4. Statuses checked against claims.tsv

| id | version | status |
|---|---|---|
| W3-AUDIT-A:GW, CAL-C, OPC, TDP, BLK | 1.0.3 | PROVED-CHECKED (council R2, MANIFEST ea8b464a…) |
| W1-N1:B | 1.0.0 | PROVED under the named premises |
| W1-N1:Thm-N1 | 1.0.0 | PROVED-CHECKED |
| W1-N1:F | 1.0.0 | PROVED under the named premises |
| W3-SAMP:CC | 1.1.2 | CODE-CHECKED, method_commit 4676af6 |
| W3-SAMP:PC | 2.1.3 | PROVED-CHECKED |

All quoted ids and versions match.

**Pins spot-checked:**

| pin | result |
|---|---|
| `STATEMENT.md:35-36` (H-U/SI) | correct |
| `W3-RM2-R/STATEMENT.md:90-93` | correct |
| W3-SAMP STATEMENT §4 pins: :102-103, :104-105, :136-138, :139-140, :158, :170 | all correct |
| W3-DIST :293-296, :299-300, :312-313, :316-317 | all correct |
| T1_GW :98-101 | off by one line (E1) |
| W3-READER :33-36 | off (E2) |

**Mathlib names in §3:** all found in `/home/fb31/lean/packages/v4.35.0-rc2/mathlib`: `Measurable.find`, `measurable_from_prod_countable_left`, `condExp_indep_eq`, `Int.measurable_floor`, `Finset.measurable_prod`, `measurableSet_lt`, `Measurable.piecewise`.

## 5. Gates

- **G1 correctness: FAIL.** Steps 1-3 are correct, and so are the call sites. Step 4 has a missing input (F2), and Step 5 covers less than is claimed (F1).
- **G3 faithfulness and scope: FAIL.** The potential-only scope holds, but the "Consequently" sentence goes beyond Step 5 (F1).
- **G4 statuses and pins: FAIL.** One wrong dependency id (F3), plus two pin corrections (E1, E2).
- **G5 registration form: PASS.**

## 6. Score

**8.0.** There are three F findings and no C or S. Each F needs only a few lines to fix, and the measurability conclusion itself is true.

## 7. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R1 manifest=7fbc2f86e20994967f466b5fb373e1d3427046ad162136615f5a6a4c6a1c09c9 seat=opus score=8.0 gates=FAIL
