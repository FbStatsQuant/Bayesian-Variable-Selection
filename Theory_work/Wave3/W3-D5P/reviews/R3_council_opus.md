## W3-D5P targeted re-check, round R3, seat `opus`

I worked read-only and wrote nothing. Checks on what I read:
- `manifest.py verify … MANIFEST_R3.txt` returned `verify: OK MANIFEST 35a027be…`.
- `R3_diff.txt` is byte-identical to `git diff fe76299a a2c465a4` on CARD.md, L3 and DEPS.tsv. The other files in that git range are under `reviews/` or LOG.md, and none of them is in the manifest.
- The sha256 prefixes on disk match DEPS: STATEMENT `5dc11132`, L1 `5c4c081b`, L2 `b023cafb`, L3 `71642c06`.

I read:
- the R2 review, the R3 diff, STATEMENT v1.1.2 in full, L3 `:1-80` and full CARD.md;
- READER_DELTA Corollary 6L and READER Theorem 6 with (S2);
- RM2R (D) `:71-93` and DLV `STATEMENT.md:18-46` (the MACH premise);
- `v3_fit.R:60-174`, `v3_run.R:185-229`, `v3_exact.R` (looking for runtime-guard calls) and `cpp/v3_core.cpp:770-790`.

### 1. R2 findings

| finding | status | one line |
|---|---|---|
| F-1 | RESOLVED | Option A now opens the bound sentence with "On Theorem 6's data event". The PIP, evidence and `mpm_list` clauses are joined by semicolons, so the qualifier covers all three. Option B adds "on Theorem 6's data event (probability → 1)" ahead of all three clauses of its one sentence. |
| E-1 | RESOLVED | The Option A rate sentence now says "the log-evidence error (where printed)". |
| E-2 | RESOLVED | "after everything else" is gone. The guard argument replaces it; see the check in §2 and the wording note E-a. |
| E-3 | RESOLVED | It now reads "`pip_list` (on either branch)". |
| E-4 | RESOLVED | It now reads "the log of the list's total unnormalised weight (the list evidence)". |
| E-5 | RESOLVED | It now reads "`pip_list` (the list-renormalised PIPs; the exact PIPs on exact enumeration)". |

### 2. Does the diff break anything?

**L3 (0.5) is still a correct derivation from IMPL-LIST as STATEMENT §1 (`:59-63`) states it.**
- The IMPL-LIST parenthetical now matches STATEMENT §1 word for word: "as SPEC §2 and §4 prescribe, from the returned list and values of the same run, and changes no other field and no other state; SPEC §7 A.1–A.2". Nothing is added to the premise.
- The guard sentence is true at the pin:
  - **Sampler branch.** The returned list is `out$top_store <- led$top` (`v3_run.R:210`). It is built in `v3_assemble_final` after `cpp_final_run` (`:227`) returns, so after every runtime-guard check inside the engine. After that, `v3_fit.R:163-173` and `finish` (`:79-87`) do not branch on the clock. `finish` reads the clock only to record `timings$total`. `cpp_runtime_report` (`v3_core.cpp:777-790`) only reads `g->records` and `g->elapsed()`. `v3_unavailable_estimates` (`:85`) is not reached on output runs.
  - **Exact branch.** The list is `fit$exact` (`:121-122`). `v3_enumerate(ctx)` takes no runtime pointer, and `v3_exact.R` contains no guard call. So the last guard decision is the preflight at `:115-117`, which comes before the list exists. The sentence holds; see E-a for the wording.
- The rest of (0.5) is unchanged from R2 and still holds:
  - the duplicate-model row of SPEC §4 cannot fire, by L2 (iii) and (iv);
  - therefore the post-commit fit returns if and only if the pinned fit returns;
  - therefore L2, RM0-plus (b⁺) and DLV-0 transfer.
- No new C, S or F.

**CARD Options A and B are now faithful to (C3)** on the four points the brief asks about:

| point | Option A | Option B |
|---|---|---|
| Data event | "on the same data event" for list membership and `hpm`; "On Theorem 6's data event" for the bounds. READER Theorem 6's 𝒢_n is contained in 𝒢⁺_n (R2 check), so this is implied by (C3)(i). | "on Theorem 6's data event (probability → 1)", scoping all three clauses. |
| Branches | Sampler: list-renormalised PIPs and median model, plus the list's log weight. Exact: the exact PIPs and median model. "`pip_list` (on either branch)". These match §1 `:49-57` and Step 1 of L3. | `pip_list` is defined on both branches. `mpm_list` = S₀ when ε_n < ½ is also true on the exact branch (MPM = S₀ by LIST-K (e)). |
| NA qualifier | "where returned" for the list; "(where `log_Z_list` is printed)" for the evidence bound; "(where printed)" in the rate. | "(`log_Z_list`, where printed)". |
| Which evidence error | 1 − ε_n ≤ Z^list/Z ≤ 1, i.e. 0 ≤ log Z − `log_Z_list` ≤ −log(1 − ε_n). This equals (C3)(i), and the rate is stated for the log error. | 0 ≤ log Z − `log_Z_list` ≤ −log(1 − ε_n). |

I also checked the rate clause's hypothesis. (C3)(ii) needs p ≥ 2 for all large n. The CARD and READER texts state the rate under "the hypotheses of Theorem 6" without saying so. Reader (S2) (`READER_VERSIONS.md:29`) requires 2 ≤ p ≤ n^A, and p_ret = p almost surely by L3 (0.3a). So the qualifier is implied by Theorem 6's hypotheses, and there is no finding.

**DEPS.tsv is consistent.**
- The STMT-C1..C3, LIST-K and LIST-CODE rows have `checked_sha` = `sha` = the shas R2 read (as listed in MANIFEST_R2), so `state` OK follows the PROTOCOL_v4 `:148` rule.
- The LIST-R row has `sha` 71642c06 (current) and `checked_sha` b1e91cd8 (what R2 read). It is correctly marked STALE pending this round.

**E notes on changed text only** (none of these affects a gate):
- **E-a.** In (0.5), "so DLV-0's guard and MACH accounting are unaffected" is half right. That wording came from my own R2 E-2 suggestion.
  - Every guard decision is unaffected; that part is correct.
  - The MACH counts are not literally unchanged. The new fields add O(|𝒯|·K) operations and O(|𝒯| + p) words after the last guard.
  - Suggested wording: "so every guard decision is that of the pinned fit, and the added O(|𝒯|K) operations and O(|𝒯| + p) words, dominated by the store already held, are absorbed by the polynomial envelopes of (D)".
  - Optionally, say that on the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`), and that `:121-122` is where the list is created.
- **E-b.** In Option B, "their median model (`mpm_list`)" has lost its plural antecedent now that the subject is `pip_list`. Write "the list's median model (`mpm_list`; the exact MPM on exact enumeration)".

### 3. Per-claim table

| id | decision |
|---|---|
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |
| W3-D5P:LIST-R | ACCEPT (conditional on IMPL-LIST) |

### 4. The six gates

| gate | result | one line |
|---|---|---|
| correct | PASS | The (0.5) guard sentence is true at the pin (`v3_run.R:210, 227`; `v3_fit.R:79-87, 115-122, 162-173`; `cpp_runtime_report` only reads). The transfer to the method with the new fields stands. |
| strength | PASS | STATEMENT is unchanged (v1.1.2, EQUAL). The STRONGER NA-drop is still deferred to HQ in TARGET §4. |
| faithfulness | PASS | F-1 is fixed in both CARD options. Data event, branches, NA qualifiers and the log-evidence error match (C3). The rate's p ≥ 2 is implied by reader (S2). |
| lit | PASS | The diff makes no literature change. |
| necessity | PASS | No necessity claim was added. |
| better | PASS | Nothing is left undispositioned. R2_disposition covers all six R2 findings. |

I hold no C, S or F finding.

`COUNCIL-VERDICT round=R3 manifest=35a027bee24df09f64dc3f3f5b5cb47de7d74b71f77817b87d782f26b5723c8a seat=opus score=9.4 gates=PASS`
