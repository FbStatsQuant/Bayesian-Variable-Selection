# FABLE_ALLOC_CARD — the allocation argument for the list helper's tail (Sol-5b b′-1 = T6-1)

Author: the pre-Lean Fable (Theory, Claude Personal), 2026-11-18, on the brief `PRE_LEAN_PASS/Sol5/FABLE_BRIEF_allocation_b1.md` (17953966). HQ ruling: "proved, not assumed". Status: **DRAFT, unchecked**; the Opus seat and the Sol b″ call are the manager's. I edited no registered or frozen file.

## 0. Verdict

**FITS.** The work and storage of the list helper are bounded by explicit multiples of terms that are already in the brackets of C-DLV Lemma R, evaluated at (n, p_raw). So Lemma R and Corollary R hold for the tagged method with the same polynomials, and the allocation formulas mem_n = C[(n+p)² + Cert_M], time_n = C[…] of Corollary R are unchanged. Explicitly, with 𝔅_W, 𝔅_M the two brackets of Lemma R (`C-DLV/lemmas/L1_resources.md:73-80`):

- operations added: **T_W ≤ 𝔅_W(n, p_raw)**;
- words added at any time: **T_M ≤ 16·𝔅_M(n, p_raw)**;
- every runtime-guard decision is unchanged, and nothing consults the clock after the helper starts, so **no extra declared hours are needed for the run to return**.

**What "fits the envelope" means here, stated plainly.** The envelopes of (D) carry implementation-dependent constants by their own definition: "explicit polynomial shapes; implementation-dependent constants" (`C-DLV/STATEMENT.md:45-46`), "C a large enough constant for the fixed implementation" (FIN Proposition F, Allocation), "re-derived for the shipped code" (`W3-RM2-R/STATEMENT.md:76-79`). For the tagged implementation those constants become C_W + 1 and C_M + 8. So:

- (D), as a statement, is unchanged, and LIST-R (iii) holds under (D) read for the tagged method;
- the sentence "the tagged fit returns whenever the core fit does", for **every** allocation, is **not** proved and must go. A run whose declared memory covers the pinned code's envelope with no margin at all is not covered. The replacement texts in §6 scope the claim to (D).

If HQ reads (D) as a numeric envelope fixed with the pinned code's own constants, then this is a WEAKER (D) by exactly the two additive terms above (memory only matters), and in that case nothing should be applied before HQ rules. I do not think that reading is the documents', for the three quotations just given.

## 1. Code of record, and what I checked

Tag `method-v3.1.1-listpip` = commit 7100bb3b; its core tree `Scripts/SMC_BVS/core` is **61b0a582** (I resolved both). Every line below was read at that tree.

- Against core 4676af6 the tree differs in three files only: `README.md`, `v3_fit.R`, `v3_run.R`. All of `cpp/` is identical (`git diff --quiet`).
- In `v3_fit.R` the diff is three hunks: the exact branch's return (`:131`), the argument `list_fields = FALSE` (`:162`), and the tail (`:173-176`). `finish` (`:79-87`) is unchanged.
- In `v3_run.R` the diff is the `list_fields` argument (`:119`, `:220`, `:225`, `:230`) and the new functions (`:233-279`).
- One line reference in the brief differs at the tag: `v3_exact_list_last` is `v3_run.R:274-279` (line 269 is `v3_add_list_fields`).

Code facts used (file:line at 61b0a582):

| # | Fact | Where |
|---|---|---|
| C1 | Sampler branch: `v3_final_run(…, list_fields = FALSE)`, then `fit <- finish(fit)`, then the helper only if `status == "completed"` | `v3_fit.R:162, 173, 176` |
| C2 | Exact branch: preflight, then enumeration, then `v3_exact_list_last(finish(fit), e, ctx)`, which calls the helper only if `e$status == "exact"` | `v3_fit.R:115-117, 121, 131`; `v3_run.R:274-276` |
| C3 | `finish` reads the peak memory, the clock and the guard's report; it has no branch on the clock and frees nothing | `v3_fit.R:79-87` |
| C4 | Last guard consultations: the LS0 guard on the sampler branch; the preflight on the exact branch (the enumeration has no guard) | `cpp/v3_core.cpp:459, 480`; `v3_fit.R:115-117`; `cpp/v3_core.cpp:552` |
| C5 | The helper | `v3_run.R:245-268` |
| C6 | m := number of stored models ≤ 40p + 1 on both branches | `cpp/v3_ledger.h:78`; `cpp/v3_core.cpp:531` |
| C7 | The store is serialised as a list of integer vectors (original indices) and one double vector | `cpp/v3_core.cpp:358-362`, called for the exact store at `:565` |
| C8 | `orig` = `ctx$orig` = `pre$kept`, strictly increasing original indices; so p = length(orig) and max(orig) ≤ p_raw = `ncol(X)` | `v3_preprocess.R:103, 111-113`; `v3_fit.R:118`; `v3_setup.R:7-8` |
| C9 | The index strings of the retained columns already exist as names of `pip_primary` | `v3_run.R:161-162` |
| C10 | `v3_add_list_fields` assigns at most 7 fields into the fit list | `v3_run.R:269` |

Notation: n; p_raw; p retained columns; K = min(p, ⌊n/2⌋), and every stored model has at most K indices; m ≤ 40p + 1; D := the number of decimal digits of max(orig).

**On D.** `ncol(X)` is an R integer, so on every input the code can receive, p_raw ≤ 2³¹ − 1 and **D ≤ 10**. In the idealisation IDEAL-W⁺ used only for the n → ∞ statements, a machine word holds an index, so it has ω ≥ max(64, ⌈log₂(p_raw + 1)⌉) bits; a decimal index with its comma takes 8(D + 1) ≤ 8(0.302·log₂(p_raw + 1) + 2) ≤ 2.67·ω bits, hence at most 3 such words. Both readings are covered below: "11 bytes per index" on real inputs, "3 words per index" in the idealisation. This is how the logarithmic factor in the key length is handled; it never appears as a factor log p_raw in words.

## 2. Inventory of the tail

Bytes use the R object layout, which I measured on this machine (R 4.6.0): a vector has a 48-byte header and its data rounded up to a size class, so **an object with b data bytes occupies at most b + 184 bytes** (e.g. `integer(0)` 48, `numeric(100)` 848, a string of 100 characters 176). Operations: one elementary operation per element read or written by a vectorised primitive, one per character handled, and a hash insertion charged at its worst case (m probes).

| Line (`v3_run.R`) | Object or work | Live bytes, at most | Operations, at most |
|---|---|---|---|
| 246-249 | lengths, closure `res` | (constant) | 10 |
| 250-251 | `F` (a copy at worst) | 8m + 184 | m + 2 |
| 253 | result of `vapply`: the key vector | 8m + 184 | — |
| 253 | m key strings, each ≤ K(D+1) characters | m·K(D+1) + 184m | 3mK(D+1) + 10m |
| 253 | one `paste` call's temporaries (index strings, their vector, the buffer) | K(2D + 194) + 368 | (counted above) |
| 253 | hash table of `anyDuplicated` | 16m + 184 | m² + m |
| 254-256 | one logical vector of length m at a time; `max` | 4m + 184 | 4m + 1 |
| 257 | `lut`, length max(orig) ≤ p_raw; `seq_len(p)` | 4p_raw + 4p + 368 | p_raw + 3p |
| 258 | `F - Fmax`, `u` | 16m + 368 | 2m |
| 259 | `num` | 8p + 184 | p |
| 260-264 | loop temporaries of one iteration (`j`, two tests, `num[j]`, the sum) | 24K + 920 | 7mK + 6m in total |
| 265-267 | `pip`, the logical `pip > 0.5`, `mpm_list`, scalars, the result list | 16p + 2500 | 3p + 12 |
| 269 | at most 7 assignments into the fit list (91 top-level fields at the tag; I allow 256) | 32032 | 1848 |

Summing everything as if simultaneously live (an over-count):

  **T_B ≤ m·K·(D+1) + 236·m + 4·p_raw + 28·p + (2D + 218)·K + 40000 bytes,**
  **T_W ≤ 3·m·K·(D+1) + 7·m·K + m² + 24·m + p_raw + 7·p + 2000 operations.**

The exact branch runs the same helper on the enumeration's store, with the same bounds (C2, C6).

## 3. Memory: the inequality chain

With D ≤ 10 and 8-byte words, T_M := T_B/8 satisfies

  T_M ≤ 1.375·mK + 29.5·m + 0.5·p_raw + 3.5·p + 29.75·K + 5000 words.

Each group is at most a term of 𝔅_M at (n, p_raw) (Lemma R is evaluated at p_raw, all its terms being monotone in p: `L1_resources.md:110-116`; write K_r, ℓ_r for K and ℓ at p_raw):

1. 1.375·mK + 29.5·m ≤ m·(16K + 48) = 16·m(K + 3) ≤ **16·(40p_raw + 1)(K_r + 3)**, by C6. (The step needs only 1.375K + 29.5 ≤ 16K + 48; it would still hold with 500 bytes of overhead per stored model instead of 236.)
2. 0.5·p_raw + 3.5·p + 5000 ≤ 5004·p_raw ≤ **2¹⁶·p_raw**.
3. 29.75·K ≤ 36·K ≤ **K_r(ℓ_r + 3)²**, since ℓ ≥ ⌈log₂ 5⌉ = 3 for n ≥ 3, p ≥ 1.

The three bold quantities are terms of 𝔅_M (`L1_resources.md:78-79`: "(40p+1)(K + 3)", "2¹⁶p", "K(ℓ + 3)²"), each with coefficient 1. Hence

  **T_M ≤ 16·𝔅_M(n, p_raw).**

In the idealisation the first group reads 3·mK + 29.5·m words, and the same step 1 holds (3K + 29.5 ≤ 16K + 48).

*Conclusion for memory.* Up to the call of the helper the tagged fit runs the pinned code on the same state (C1, C2, §1), so by Lemma R its held words are at most M̄ = 2C_M·𝔅_M. During and after the helper they are at most M̄ + T_M ≤ 2(C_M + 8)·𝔅_M. With the LS0 re-derivation of FIN Proposition F the same holds with M_G = M̄ + C·K(K+1) in place of M̄, since M_G ≥ M̄. Under MACH, peak bytes ≤ β(M_G + T_M) + β₀; so a declared memory at least that, which is (D) for the tagged method, excludes the allocation exits X1 and X5 exactly as in Corollary R.

## 4. Operations and time: the inequality chain

With D ≤ 10, m ≤ 41p and K ≤ p ≤ p_raw:

  T_W ≤ 40·mK + m² + 24·m + p_raw + 7·p + 2000 ≤ (1640 + 1681)·p_raw² + (984 + 1 + 7 + 2000)·p_raw = 3321·p_raw² + 2992·p_raw.

𝔅_W contains "p²(2¹⁶ + n²)" and "10⁶(p + n log n)" (`L1_resources.md:74`), so

  T_W ≤ 0.051·[2¹⁶·p_raw²] + 0.003·[10⁶·p_raw] ≤ **𝔅_W(n, p_raw)**.

(In the idealisation, 3mK(D+1) is replaced by 9mK, three word operations per index, and the same bound holds.)

*Conclusion for time.*
- **Guards.** Every guard consultation precedes the helper (C1–C4). At each of them the tagged run has performed exactly the operations of the pinned run, so each decision is the pinned one, and Corollary R's clause for E1–E5 applies with the pinned W̄ (or W_G).
- **After the last guard** nothing compares elapsed time with the allocation, and MACH has no external interruption. So the helper's time τ·T_W cannot stop the run, whatever the declared hours.
- For the record, total operations are at most W_G + T_W ≤ W_G + 𝔅_W, the same polynomial with C_W + 1.

## 5. Answers to the brief's specific questions

- **"Is the peak at the helper really not above the earlier peak? What does `finish` free?"** `finish` frees nothing (C3). The final run's C++ objects (cache, population, ledger: `cpp/v3_core.cpp:407-410`) are destroyed when `cpp_final_run` returns, which is earlier. But a pathwise claim "the helper's peak is below the run's earlier peak" **cannot be proved**: between that return and the helper, the pinned code itself builds R-level results whose size is not bounded by what was freed. So the phrase "dominated by the store already held" in ERRATA E1 is not a proof, and I do not use it. The proof above is at the level of Lemma R's accounting instead.
- **"Is the log factor handled?"** Yes: see "On D" in §1. E1's count "O(|𝒯| + p) words" was also too small: the keys take O(|𝒯|·K) words and the lookup O(p_raw).
- **"Bound the lookup using max(orig)."** Done: 4·max(orig) + 184 ≤ 4p_raw + 184 bytes. As a cross-check that needs no constants: this is at most one sixth of the bytes of the raw design the caller already holds (8·n·p_raw with n ≥ 3), and equal to the bytes of `pre$kept` and `pre$dropped` together.

## 6. Replacement texts (if the verdict is accepted)

### (i) `W3-D5P/lemmas/L3_listR.md` (0.5), staged NA_DROP v1.3 (lines 33-45 of the staged file)

**R-a.** Old: "after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so DLV-0's guard and MACH accounting are unaffected [R2-E-2] —"
New: "after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so every guard decision of the tagged fit is that of the pinned fit [R2-E-2], while the work and storage of the new computation are bounded in (0.6) —"

**R-b.** Old: "the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error. Hence the post-commit fit returns if and only if the pinned fit returns, and 𝒪, `status`, `hpm`, `top_store`,"
New: "the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error other than a failed allocation, which (0.6) excludes under (D). Hence, under (D) read for the method with the list fields, the post-commit fit returns whenever the pinned fit returns; without (D) the two can differ only through an allocation inside the helper. In both cases 𝒪 on returning runs, `status`, `hpm`, `top_store`,"

**R-c.** New paragraph, inserted after (0.5) (before "The reader assumptions (A1)–(A6)…" or directly after it, at the coordinator's choice):

> (0.6) *Work and storage of the list fields* [b′-1, T6-1]. Let m ≤ 40p + 1 be the number of stored models (`cpp/v3_ledger.h:78`, `cpp/v3_core.cpp:531`), each with at most K original indices of at most D ≤ 10 decimal digits (`ncol(X)` is an R integer, `v3_preprocess.R:103`), and max(orig) ≤ p_raw (`v3_fit.R:118`). Counting every object of `v3_list_fields` and `v3_add_list_fields` (`v3_run.R:245-269`) as live at once, with at most b + 184 bytes for an R object of b data bytes, the new computation holds at most
>   T_B ≤ m·K·(D+1) + 236m + 4p_raw + 28p + (2D + 218)K + 40000 bytes
> and performs at most
>   T_W ≤ 3m·K·(D+1) + 7mK + m² + 24m + p_raw + 7p + 2000 operations
> (the hash insertions of `anyDuplicated` charged at their worst case). In 8-byte words T_M := T_B/8 ≤ 16·(40p_raw + 1)(K + 3) + 2¹⁶p_raw + K(ℓ + 3)², and T_W ≤ 2¹⁶p_raw² + 10⁶p_raw; the right sides are terms of the brackets 𝔅_M, 𝔅_W of C-DLV Lemma R at (n, p_raw) (`Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md:73-80`). So T_M ≤ 16·𝔅_M and T_W ≤ 𝔅_W. Up to the call of `v3_list_fields` the method with the list fields runs the pinned code on the same state, so Lemma R holds for it with the same brackets and constants C_W + 1, C_M + 8, and Corollary R (`L1_resources.md:129-143`) holds with the same polynomial allocation formulas. The envelopes of (D) are, by definition, those of the implementation at hand (`Theory_work/Wave1C/C-DLV/STATEMENT.md:45-46`; `W3-RM2-R/STATEMENT.md:76-79`); (D) is read here for the method with the list fields. Under it, MACH's allocation clause excludes a failed allocation in the new computation, as it does everywhere else (`W3-RM2-R/lemmas/Q5_dlv0.md:113-122`). No declared time is needed for it: every guard consultation precedes it (`cpp/v3_core.cpp:459, 480`; `v3_fit.R:115-117`), and nothing compares elapsed time with the allocation afterwards. Nothing is claimed for a declared memory that covers the pinned code's envelope with no margin. (In the idealisation IDEAL-W⁺ a machine word holds an index, a decimal index with its comma takes at most three words, and the same two bounds hold.)

### (ii) `W3-D5P/ERRATA.md`, row E1, the "proposed fix" cell

Old cell: "so every guard decision is that of the pinned fit, and the added O(\|𝒯\|K) operations and O(\|𝒯\| + p) words, dominated by the store already held, are absorbed by the polynomial envelopes of (D)"; optionally: on the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`) and `:121-122` creates the list

New cell: "so every guard decision is that of the pinned fit [applied]; the added work and storage are bounded in L3 (0.6): at most T_W ≤ 3mK(D+1) + 7mK + m² + 24m + p_raw + 7p + 2000 operations and T_B ≤ mK(D+1) + 236m + 4p_raw + 28p + (2D+218)K + 40000 bytes (m = \|𝒯\| ≤ 40p + 1, D ≤ 10), that is T_W ≤ 𝔅_W and T_B/8 ≤ 16·𝔅_M for the brackets of C-DLV Lemma R at (n, p_raw); Lemma R and Corollary R therefore hold for the method with the list fields with the same polynomials, and (D) is read for that method. The earlier wording ('O(\|𝒯\| + p) words, dominated by the store already held') is withdrawn: the keys take O(\|𝒯\|K) words, the lookup O(p_raw), and no comparison with an earlier peak is claimed. On the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`) and `:121` creates the list. Proof and inventory: `PRE_LEAN_PASS/Sol5/FABLE_ALLOC_CARD.md`."

### (iii) New `depends_on` entries for `W3-D5P:LIST-R`

Add: `C-DLV:L1-R@proof:brackets,R.4 ; C-DLV:Cor-R@stmt` (both at 1.0.0 in the registry). `W3-RM2-R:DLV-0@stmt` (1.0.1) is already listed and stays.

## 7. Limits, stated plainly

- **R internals.** The object sizes are measured on this machine's R 4.6.0. The size of `anyDuplicated`'s hash table (at most 4m four-byte entries) and the temporaries of `paste` are R implementation facts that I did not read in R's source; step 1 of §3 tolerates more than twice my per-model overhead.
- **Garbage.** The byte bound is for live objects. Uncollected garbage is not "words held"; MACH's clause "peak bytes ≤ β·(words held) + β₀" carries that for the helper as it does for the pinned code's own R-level assembly. I tried to measure the live peak with a collection at every allocation and stopped the run: it was too slow to finish, so there is **no empirical confirmation of T_B** in this card.
- **Cost model.** Operations are counted per element and per character, in the manner of `L1_resources.md` R.1's last row. A different unit changes the numbers 3321 and 2992, not the conclusion; the margin in §4 is a factor of about 17.
- **Scope.** Shipped `v3_fit` only. A standalone `v3_final_run` (default `list_fields = TRUE`, `v3_run.R:220`) runs the same helper before returning and is covered by the same counts, but it is not on DLV-0's call graph.
