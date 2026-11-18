# D-29 offer floor: WP4's answer (2026-11-16)

Checked against WP4's code on `exp/P1M-wp4-calib2` (PR #46 head 12931094). The original answer never reached the
manager, so this note replaces it.

## (a) Does anything WP4 owns read an island store's tail below τ_cal in V mode? **No.**

- **Merge** (`include/v4/merge.h:278`). `led.merge(I.led)` takes the top-c of the union with the pre-island ledger.
  The pre-island ledger already holds the table events and every inherited calibration model, so its cut-off is
  ≥ τ_cal. Any island entry below the floor is strictly below that cut-off and never survives.
- **Duplicate models** (`store.h:4-6`). The store keeps each model once, with its best value. Dropping a worse
  duplicate offer below the floor changes nothing.
- **Tail** (`tail.h:98`, `merge.h:290`). The local search and LS0 read only the merged store and its cut-off.
- **Assembly** (`merge.h:336-360`). log Z_T, PIP_T and occ_top use only the merged top store. occ_top_r uses the
  islands' terminal supports.
- **Per-island fields** in `island_r.bin`: log Z_r, pip_r, ess, terminal supports, HPM and provenance, logical
  counters and island_best. All come from the Tally or the particles, not from the store. V mode counts every
  consumed score as fresh, so a dropped offer still counts.
- **Calibration** never reads an `island_r.bin`. Its own pilot and diagnostic island ledgers are merged before
  τ_cal exists, so they must run with no floor. `k_store` comes from the calibration ledger.
- **Memory estimate only.** The merge's memory admission takes the mean model size `kbar` from the island store
  section lengths (`wp4_io.cpp:873`). With a floor this is still an upper bound for what is actually loaded. It
  affects no output.
- **Not WP4's code.** WP3/WP7 must confirm that `island_run.h` writes nothing derived from its own store besides the
  store itself, for example a per-island log Z_T or PIP_T.

## (b) What WP1 must add to the contract

1. **τ_cal in calib.bin** (`meta.tau_cal`, f64). It is the c-th best F, with c = 40p+1 in HPM order, over the
   distinct inherited models that calib.bin exports. If there are fewer than c, it is −inf and there is no floor.
   It is written only for a completed V-mode calibration.
2. **The floor in island_r.bin** (`meta.offer_floor`, f64; −inf = none), plus the calib content hash it came from.
   - The island drops an offer only when v < floor; ties are kept.
   - The island store is then "the top c of the offers ≥ floor" and may hold fewer than c entries.
   - I1 is unchanged.
   - HPM, counters and island_best still see every event.
3. **Merge check.** After the tables and inherited models are offered, every island must have
   floor ≤ `pre.top.cutoff()`. Otherwise the merge refuses with `invalid_input` under GUARD-W, with no estimates.
   The comparison is `≤`, not `<`, because offers equal to the floor are kept.
4. **Modes and roles.**
   - The floor applies only to V-mode final-run islands.
   - Compat and law islands, and every calibration role (pilot and diagnostic), must have floor = −inf.
   - The merge refuses any other case.
5. **Wording in §4/§5.** An island store under a floor is not that island's top c. No consumer may use an island
   store on its own; only the merged store has meaning.
