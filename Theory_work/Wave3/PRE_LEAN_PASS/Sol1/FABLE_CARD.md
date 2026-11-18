# Sol-1 Fable card: C1 code audit (`C-DLV:P1-Inventory@1.1.1`, `C-DLV:L2-S3@1.0.1`)

Sol 6.2: ACCEPT ×2, 9.4 PASS, bound to manifest 12802ac7. Snapshot: `origin/theory/PRE-LEAN` 3d94ad40.

## Rulings

1. **S1-1 (status labels at `C1_AUDITS/STATEMENT.md:83-89`): AGREE as an observation; no text change.** I checked the records Sol could not see, and the labels are quoted as recorded:
   - Track A council R2 is sol 9.1 / opus 9.3 (`track_A/reviews/R2_diff_sol.md:79`, `R2_diff_opus.md:175`); T10 is at STATEMENT v2.2 / PROOF v2.1.
   - T14's label is verbatim at `track_A_X/T14_REP/CHECK.md:3`; XR2 is sol 9.4 / opus 9.5 (`XR2_diff_sol.md:45`, `XR2_diff_opus.md:75`).
2. **Core drift: AGREE with Sol's reading.** The three added `stop()` calls check internal invariants (scores and models of equal length, the store is a set, stored columns lie in the retained set), which is the X2 class. The patch adds no return without estimates; the list-PIP flags are fields only.
3. **Two items for the next re-pin, neither touching the claims at pin 4676af6:**
   - L2 S.3's unreachability argument has not been made for these three instances. They run after `finish()`, so one firing would turn a completed fit into an R error. They need an X′-style erratum row when the pin advances.
   - The X5 byte envelope (Corollary R) does not count the new list-field allocations.

## One extra finding (outside the audit's scope; for Engineering)

On main, a final run that ends non-completed after a successful calibration still reaches the last line of `v3_fit` (`v3_fit.R:161-176`). `top_store` is unset on that path (`v3_run.R:143-148` returns before `:210`), so the fit gains NA list fields with `pip_list_flag = "empty_list"`.
- The README says the fields are absent for every non-completed status and that "empty_list" must not occur.
- `tests/list_pip_units.R:152-160` covers preflight and calibration stops only, not this path.
- It is not a new exit: `estimates_available` stays FALSE.
- Verification: I ran `v3_list_fields` on a NULL store and got the flagged NA result. The path through `v3_fit` is from reading the code, not from an end-to-end run.
