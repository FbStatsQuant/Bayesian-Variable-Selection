## W3-D5P council diff round R2, seat `opus`

I worked read-only and wrote nothing. `manifest.py verify … MANIFEST_R2.txt` returned `verify: OK MANIFEST 7431d66d…`.

I read:
- both R1 reviews and `R2_diff.txt`, which matches `git diff e5cc7d60 a5cd6133` on the ticket folder (9 files);
- STATEMENT v1.1.2 and L3 in full;
- SPEC_LIST_PIP at 523dda23, in full;
- RM2R (D)/DLV-0 (`:71-93, :144-147`) and the RM configuration (`:59-61`);
- `v3_fit.R:70-175`, `v3_run.R:195-229`, `cpp/v3_core.cpp:525-568` and `cpp/v3_ledger.h:74-80`, to judge (0.5).

The DEPS `sha` prefixes match the files: STATEMENT `5dc11132…`, L1 `5c4c081b…`, L2 `b023cafb…`, L3 `b1e91cd8…`.

### 1. Status of each R1 finding

| finding | status | one line |
|---|---|---|
| sol-1 (branch definitions of the fields) | RESOLVED | READER_DELTA, CARD A/B and the REPORT registry block now separate the sampler (list-renormalised) from exact enumeration (`pip_list` = PIP, `mpm_list` = MPM), as STATEMENT §1 does. |
| sol-2 (which evidence error) | RESOLVED | The texts now name the relative deficit 1 − ε_n ≤ Z^list/Z ≤ 1 and the log error 0 ≤ log Z − `log_Z_list` ≤ −log(1 − ε_n). The rate is stated for the log-evidence error. The blanket "within ε_n" is gone. |
| sol-3 (NA / "when returned" qualifiers) | RESOLVED | The qualifiers are restored in REPORT (conclusion and rate), READER_DELTA (display and rate) and CARD A/B (conclusion, and list membership "where returned"). Residual E-1 below: CARD A's rate sentence lacks "(where printed)". |
| opus-1 (pin → post-commit transfer) | RESOLVED | L3 (0.5) is added; Step 1 and Step 3 cite it; the remark at `:102-104` is corrected. Residual E-2 below: one paraphrase in it. |
| opus-2 (NA qualifier in derived texts) | RESOLVED | The qualifier was added. Dropping it is correctly logged in TARGET §4 as STRONGER and deferred to HQ (PROTOCOL_v4 §4.2). |
| opus-3 (AR/BLK qualifier) | RESOLVED | CARD "Why it matters" and the READER remark now say "that satisfy Theorem 6's conditions". |
| opus-4 (REGISTRY LIST-K scope) | RESOLVED | The scope now reads "any real-valued F on Ω (as (C1))". |
| opus-5 (`ls0_ell` = ℓ_n) | RESOLVED | Added to the (C2) gloss and logged in the changelog. |
| opus-6 (stale headers) | RESOLVED | REPORT, L1, L2, L3 and TARGET headers are updated. |
| opus-7 (LIST-CODE premises and assumptions) | RESOLVED | `:49-57` is added. A:OP is glossed as EX-A, EX-S, SR, GUARD-W, OP-LS0 at the shipped configuration. |
| opus-8 (READER "completed run") | RESOLVED | It now reads "A run that produces output". The exact store has the same 40p + 1 capacity (`v3_core.cpp:531`), so the size claim still holds on both branches. |
| opus-9 (TARGET parity wording) | RESOLVED | It now reads "(AR/BLK designs inside Theorem 6)". |
| opus-10 (DEPS `checked_sha` convention) | RESOLVED | The rows give the checker-read SHAs and state STALE until R2. `checked_sha` must be refreshed after this round passes. |

### 2. Does the diff break anything?

**L3 (0.5) is a correct derivation from IMPL-LIST as STATEMENT §1 states it.**
- IMPL-LIST says: computed "as SPEC §2 and §4 prescribe, from the returned list and values of the same run", and "changes no other field and no other state".
- The new computation can stop the fit only through a SPEC §4 row that errors. Only the duplicate row does; the empty-list and non-finite-score rows set NA.
- The duplicate row is reached only on status `completed` or `exact`. The fields are absent, so nothing is computed, on every other status (SPEC §4 row 3).
- On those two statuses, L2 (iii) and (iv) give distinct models. So "returns iff the pinned fit returns" holds, on non-output runs as well.
- RM0-plus (b⁺) concerns data events only. DLV-0 transfers through the "iff".
- One thing (0.5) needs but does not spell out: under (D), DLV-0 also depends on the runtime guard and the MACH accounting.
  - The returned list exists only after the last guard consultation: `v3_fit.R:121-122` on the exact branch, after `v3_final_run` (`:162`) on the sampler branch.
  - After that, `finish()` (`:79-87`) does not branch on the clock.
  - So "from the returned list" already places the new computation after every guard.
- The text's "after everything else" is therefore implied, not an extra premise. See E-2.

**STATEMENT v1.1.2 changelog tag EQUAL: correct.** `ls0_ell = ℓ_n` is part of the imported OP-LS0 configuration (RM `STATEMENT.md:59-61`), which (C2) already assumed through "shipped configuration". No other STATEMENT text changed.

**REPORT registry blocks: faithful** to (C1)–(C3). They state the data event, both branches, "when not NA", "when returned", which evidence error, the rate under p ≥ 2, and "AR and block designs included when they satisfy it".

**READER_DELTA Corollary 6L: faithful.**
- It covers the branches, "where printed" and "where it is returned", and the relative and log evidence bounds.
- The rate is for |log Ẑ^list − log Z| (where printed).
- Every conclusion is scoped by "on the same data events 𝒢_n", which is contained in 𝒢⁺_n.
- Hypotheses are "the assumptions of Theorem 6", with nothing added.

**CARD Option B: not faithful. This is a new F (finding F-1).** Option A is affected at lower severity.

#### F-1 [F] (minor): CARD Option B (`CARD.md` Option B, the rewritten sentence) drops the data-event qualifier

- **What fails.**
  - The sentence reads: "under the hypotheses of Theorem 6, the PIPs computed from the returned list … are within ε_n = … of the truth and of the exact posterior PIPs on output, their median model (`mpm_list`) is S₀ when ε_n < ½, and the list evidence … satisfies 0 ≤ log Z − `log_Z_list` ≤ −log(1 − ε_n)".
  - As written, these are deterministic bounds on **every output run**.
  - (C3)(i) proves them only **on 𝒢⁺_n**, where S₀ is in the list. Off that event they can fail even when ε_n is small:
    - suppose the run misses S₀ (data outside 𝒦_n) while π(S₀ | y) is close to 1;
    - then π(𝒯) ≤ ε_n, so `pip_list` can be wrong by nearly 1;
    - and log Z − `log_Z_list` ≥ −log ε_n, which is larger than −log(1 − ε_n).
  - The R2 rewrite makes this sharper: it replaced the R1 phrasing ("within … = O_P(…)") with explicit pathwise inequalities.
- **Option A.** The sentence was split. "Both PIP fields are within ε_n …; the list evidence satisfies …; `mpm_list` is S₀ when ε_n < ½" now stands alone after the sentence that carries "on the same data event". Only the anaphora "that list" ties it back. In R1 this was a single sentence, so the event qualifier covered it.
- **Fix.**
  - Option B: "…on those designs, under the hypotheses of Theorem 6, on Theorem 6's data event (probability → 1), the PIPs …".
  - Option A: begin the sentence with "On that event, `pip_list` (on either branch) is within ε_n …".

#### E findings, on changed lines only

- **E-1.** In CARD Option A, the rate sentence "The PIP errors and the log-evidence error are O_P(…)" lacks "(where printed)", which READER_DELTA and REPORT carry. Add it for parity.
- **E-2.** In L3 (0.5), the parenthetical attributes "after everything else" to IMPL-LIST, but STATEMENT §1's text of IMPL-LIST does not contain it. It is implied: the computation reads the returned list, which exists only after the last runtime-guard consultation (`v3_fit.R:121-122`, `:162`), and `finish()` does not branch on the clock. Either drop the phrase or replace it with that sentence. This also makes explicit why DLV-0's guard and MACH accounting is unaffected.
- **E-3.** In CARD Option A, "Both PIP fields" can be read as `pip_list` and `pip_primary`. Write "`pip_list` (on either branch)".
- **E-4.** In CARD Option A, "the PIPs, median model and log evidence **of the posterior renormalised to that list**". A normalised posterior has no evidence. Write "and the log of the list's total unnormalised weight (the list evidence)".
- **E-5.** CARD Option B says "the PIPs computed from the returned list (`pip_list`; exact PIPs on exact enumeration)". On the exact branch these are not computed from the list. Write "`pip_list` (the list-renormalised PIPs; the exact PIPs on exact enumeration)".

### 3. Per-claim table

| id | decision |
|---|---|
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |
| W3-D5P:LIST-R | ACCEPT (conditional on IMPL-LIST). The statement, the proof with (0.5), and the registry block are clean. F-1 is in CARD's presentation of LIST-R. |

### 4. The six gates

| gate | result | reason |
|---|---|---|
| correct | PASS | (0.5) closes R1 opus-1 and is derived from the stated IMPL-LIST. No step of L1–L3 is broken by the diff. |
| strength | PASS | The registered statements are unchanged in strength (v1.1.2 is EQUAL). The STRONGER NA-drop is correctly deferred to HQ. |
| faithfulness | **FAIL** | F-1: CARD Option B, and Option A as split, state the pathwise bounds without Theorem 6's data event. |
| lit | PASS | The only literature-relevant change is the TARGET parity row, now qualified "(AR/BLK designs inside Theorem 6)". |
| necessity | PASS | No necessity claim was added. |
| better | PASS | The TARGET §4 row records the NA-drop as a STRONGER option for CP3. Nothing else is left undispositioned. |

By the binding rule, F-1 forces `gates=FAIL`. The fix is a few words in CARD.md, and nothing else needs to change.

`COUNCIL-VERDICT round=R2 manifest=7431d66d533fd256483e44f90c75afc09559dbffaa8b1fffc6e80361d5c8b92d seat=opus score=8.8 gates=FAIL`
