I hold **WORDING and QUALIFIER findings only. There is no GENUINE GAP.** The inequality chain holds. The memory constant is +8, not +16. Every claimed edit is where the grep table says. The digest verifies.

# R4 council review: Opus seat, NA_DROP v1.4 (manifest 5d06f5c6…)

**What I checked myself:**
- I re-derived the inventory and both inequality chains from `v3_run.R:245-279` at core 61b0a582.
- The copies of the core in `.rc_tmp/bt_nadrop14` are byte-identical to `git show 61b0a582:…`.
- `manifest.py verify` gives **OK 5d06f5c6…**. I ran it on my own copy, `.rc_tmp/r4_opus/bt`, built from `bt_nadrop14` plus the staged ticket.
- A script comparing the staged texts with card §6 is at `.rc_tmp/r4_opus/pure.py`.
- `ingest.py convert` on a scratch copy of REPORT.md: exit 0, 3 records, stderr empty, `conclusion_level` = `reported-model`.
- A small R test confirms the lazy-evaluation order described in C-1.

## Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 | ACCEPT | **The chain holds; nothing is dropped; there is no off-by-one.** The per-model coefficient 236 = 8 (F) + 8 (key vector) + 184 (key-string overhead) + 16 (hash) + 4 (logical) + 16 (F−Fmax, u). The K coefficient is (2D+194)+24 = 2D+218. The p coefficient is 4+8+16 = 28. The constants come to 37,476 + closure ≤ 40,000. T_W sums to 3mK(D+1) + 7mK + m² + 24m + p_raw + 7p + 1873. **Memory, with D ≤ 10:** T_M ≤ 1.375mK + 29.5m + 0.5p_raw + 3.5p + 29.75K + 5000 (2D+218 ≤ 238 → 29.75K). Step 1 holds at the smallest case: K ≥ 1 always (p ≥ 1, n ≥ 3), so K = 0 never occurs, and at K = 1 we need 30.9 ≤ 64. Step 2: 4p_raw + 5000 ≤ 5004p_raw ≤ 2¹⁶p_raw. Step 3: ℓ ≥ 3, so 36K ≤ K(ℓ+3)². The result is T_M ≤ 16A + B + C ≤ 16·𝔅_M. **Work:** with m ≤ 41p and K ≤ p ≤ p_raw, T_W ≤ 3321p_raw² + 2992p_raw. Since 0.051·2¹⁶ = 3342 and 0.003·10⁶ = 3000, this is ≤ 𝔅_W. **Constants, stated exactly:** W̄ = C_W·𝔅_W gives W̄ + T_W ≤ (C_W+1)𝔅_W. M̄ = **2**·C_M·𝔅_M (`L1_resources.md:78`) gives M̄ + 16𝔅_M = 2(C_M+8)𝔅_M. So **+8 is exactly what the inequalities give.** +16 would only follow if M̄ were C_M·𝔅_M, and it is not. The text should show the factor 2 (S-2). The IDEAL-W⁺ variants (9mK operations; 3 words per index, 8(D+1) ≤ 2.67ω) also hold. |
| 2 | ACCEPT (with C-1, C-4) | **Each cited line says what the text says:** `cpp/v3_ledger.h:78` (40p+1) ✓; `cpp/v3_core.cpp:531` ✓; `v3_preprocess.R:103` (`ncol(X)`) ✓; `v3_fit.R:118` (`orig = pre$kept`) ✓, though max(orig) ≤ p_raw also needs `v3_preprocess.R:112` (C-4); `v3_run.R:245-269` ✓; `cpp/v3_core.cpp:459, 480` (the last guard checks, nothing after them in `cpp_final_run`) ✓; `v3_fit.R:115-117` (preflight) ✓; `:121` (enumeration) ✓; `v3_fit.R:79-87` (`finish`: no branch on the clock, frees nothing) ✓; `v3_run.R:274-279` = `v3_exact_list_last` ✓ (the correction is right; :269 is `v3_add_list_fields`). C-DLV `L1_resources.md:73-80` brackets ✓, `:129-143` Corollary R ✓, C-DLV `STATEMENT.md:45-46` ("implementation-dependent constants") ✓, `:28` MACH ✓, RM2-R `STATEMENT.md:76-79` ("re-derived for the shipped code") ✓, `Q5_dlv0.md:113-122` (MACH allocation exits) ✓. **One code-order fact is wrong.** On the exact branch, `finish` runs *after* `v3_list_fields` (C-1). The conclusions do not change. |
| 3 | ACCEPT (with S-3, S-4, C-3) | **"(D) read for the method with the list fields" is not a new kind of premise.** (D) is imported with implementation-relative envelopes (C-DLV `STATEMENT.md:45-46`; RM2-R `:76-79`). The reading does raise the memory constant of that premise from C_M to C_M+8. It is recorded only in the proof; S-4 is for the manager. **No leftover "iff" or "unaffected" depends on return-equivalence:** the remaining "iff" at `STATEMENT.md:84`, `L3:75` and `REPORT:53` concern completed ⇔ estimates_available, which is unrelated; "unaffected" survives only as the historical quote in the ERRATA E1 "text" column. CARD and READER_DELTA have no return-equivalence wording. **One direction is enough.** Step 0′, Step 1 and Step 2 are about runs that return output. Step 3 (`L3:118`, P(𝒪ᶜ) = 0) needs exactly "the post-commit fit returns whenever the pinned fit returns". It also needs (D)-tagged ⇒ (D)-pinned, so that DLV-0 in (0.4) applies; this holds because M̄′ ≥ M̄ and time is unchanged, but it is not written (S-3). The other direction (pinned does not return ⇒ tagged does not return) is used nowhere. It is trivially true under the coupling anyway. |
| 4 | ACCEPT (with F-1) | **The texts are verbatim.** Whitespace-flexible comparison: R-a, R-b, the (0.6) paragraph and the E1 new text are each present once; the old R-a, R-b and E1 phrases are absent. CARD.md and READER_DELTA.md are byte-identical to v1.3. REPORT changes only at :4 and :69; STATEMENT only at :1 and :169. **The E1 cell is not exactly the card's new cell (F-1):** the stale "optionally … `:121-122`" tail was kept. **"[applied]" is meaningful.** It marks that the first clause of the proposed fix is now in L3 (0.5) as R-a. It is not a mis-copy of "[R2-E-2]" (E-1). |
| 5 | ACCEPT | `C-DLV:L1-R` and `C-DLV:Cor-R` exist in `Theory_work/INFRA/registry/claims.tsv` (not `Theory_work/registry/`) at 1.0.0, PROVED-CHECKED, ACTIVE. `@proof:brackets,R.4` parses as two proof uses. The LIST-R spans `STATEMENT.md:100-128` and premises `:29-64` are unchanged, as are the LIST-K (68-76, 39-47) and LIST-CODE (80-96, 29-38, 49-58) spans. The only added line is :169, after every span. No pointer into L3 by line number exists, so the +4-line shift inside L3 moves nothing. One optional note: `brackets` is statement content of L1-R (lines 73-80 lie inside its span 70-81), so `@stmt` would also be correct. `@proof` is the more conservative choice; no change needed. |
| 6 | ACCEPT | No status or claim level is raised: the REPORT status strings are unchanged and the level is `reported-model`. The changelog tag EQUAL is right: only the proof changed, the spans are unchanged, and the withdrawn sentence was a proof sentence. This holds under the manager-accepted reading of (D) (S-4). |

## Findings

- **F-1 (WORDING; faithfulness of application). `ERRATA.md:5`.** The apply script replaced only the quoted part of the old cell. Card §6(ii) gives the old cell as the quoted text *plus* the clause "; optionally: on the exact branch … `:121-122` creates the list". The card's new cell already includes that clause, corrected to `:121`. The staged cell therefore repeats the clause with the outdated range.
  - **Correction:** delete `; optionally: on the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`) and `:121-122` creates the list`. That is the text between the new cell's closing quote and the final ` |`.
  - Apply as written.

- **C-1 (QUALIFIER; code fact). `L3_listR.md:49`, with the card's C2 and §5.**
  - **What happens:** at `v3_fit.R:131`, `return(v3_exact_list_last(finish(fit), e, ctx))` passes `finish(fit)` as a lazy promise. Inside `v3_exact_list_last` it is first forced at `v3_run.R:277`, which is after `v3_list_fields` at `:276`. I confirmed this with Rscript, both interpreted and byte-compiled: the output order was "helper", then "finish".
  - **Effect on the text:** on the exact branch the (0.6) sentence "Up to the call of `v3_list_fields` … runs the pinned code on the same state" is inexact.
  - **Why the conclusions stand:** `finish` consults no guard and allocates O(1) words. At every moment the held words are at most the pinned code's words at the corresponding point plus T_M, so the bound does not depend on the order.
  - **Correction:** replace "runs the pinned code on the same state," with "runs the pinned code on the same state (on the exact branch `finish(fit)` is a lazy argument of `v3_exact_list_last`, forced at `v3_run.R:277`, so `finish` runs after `v3_list_fields`; it consults no guard and allocates O(1) words, and the bounds below do not depend on this order),". Apply as written.
  - **For the manager, an engineering observation, not a LIST-R gap:** on the exact branch, `peak_memory_kb` (VmHWM), `timings$total` and `runtime_guard` are measured after the helper. This defeats the PR68 MAJOR-2 intent ("so the new allocation cannot leak into a legacy field"). SPEC §7 A.1 excludes timings, so IMPL-LIST stands. A fix would be `fit <- finish(fit); return(v3_exact_list_last(fit, e, ctx))`, which is a method change.

- **S-1 (WORDING; the coordinator's own text). `STATEMENT.md:169`.** "they fall under the existing IDEAL-W⁺ premise" names the wrong premise. IDEAL-W⁺ covers overflow and the two lifted predicates. Object sizes are a matter of Lemma R's R-level counting and MACH's β, β₀.
  - **Correction:** replace "they fall under the existing IDEAL-W⁺ premise; no new premise." with "they are counted as R-level objects in the manner of Lemma R (`L1_resources.md:95-96`), and their bytes, like those of R's global string cache that the m keys enter, fall under MACH's peak bytes ≤ β·(words held) + β₀; no new premise."
  - Apply as written.

- **S-2 (WORDING). `L3_listR.md:49`.**
  - **Correction 1:** replace "constants C_W + 1, C_M + 8," with "constants C_W + 1, C_M + 8 (Lemma R's bounds are W̄ = C_W·𝔅_W and M̄ = 2C_M·𝔅_M, `L1_resources.md:73, 78`, so M̄ + 16·𝔅_M = 2(C_M + 8)·𝔅_M),".
  - **Correction 2:** replace "the right sides are terms of the brackets" with "the right sides are sums of terms of the brackets (the first with factor 16)".
  - Apply as written.

- **C-2 (QUALIFIER). `L3_listR.md:49`.** C-DLV's Lemma R covers LS0 with cap ℓ only. (D) for the shipped code is RM2-R's re-derivation, with cap ℓ_n + |S̃₀| and the shipped preflight. Card §3 handles this through M_G; (0.6) does not mention it.
  - **Correction:** after "holds with the same polynomial allocation formulas." add " The same two additive terms carry over to the re-derivation of these envelopes for the shipped code (`W3-RM2-R/STATEMENT.md:76-79`), whose word bound M_G ≥ M̄ is only increased by T_M."
  - Apply as written.

- **C-3 (QUALIFIER, optional). `L3_listR.md:33` (R-a).** "every guard decision of the tagged fit is that of the pinned fit" is a coupling statement. Clock readings are not part of the run's uniforms, and MACH bounds wall time without fixing it. What (iii) actually uses is that each guard consultation is preceded by exactly the pinned operations, so Corollary R's E1–E5 clause applies with the pinned W̄.
  - **Possible replacement:** "so every guard consultation of the tagged fit is preceded by exactly the operations of the pinned fit, and Corollary R's guard clause applies to it with the pinned bound [R2-E-2]".

- **S-3 (WORDING). `L3_listR.md:118`.**
  - **Correction:** replace "Under (D), by (0.4) and (0.5), P(𝒪ᶜ) = 0" with "Under (D), read for the method with the list fields ((0.6); its envelopes dominate the pinned core's, so (0.4) applies), by (0.4), (0.5) and (0.6), P(𝒪ᶜ) = 0".
  - Apply as written.

- **S-4 (QUALIFIER; for the manager). `STATEMENT.md:35`** still imports (D) as RM2R `:71-93`, without the reading. The reading lives only in L3 (0.6). Card §0 itself made application conditional on HQ accepting this reading. If HQ wants a reader of the claim to see it without opening the proof, add a §5 remark after line 146. That is outside every span, and only the changelog line numbers would move.
  - **Possible remark:** "6. *(D) for the method with the list fields.* (D)'s envelopes carry implementation-dependent constants; for `method-v3.1.1-listpip` they are those of C-DLV Lemma R with C_W + 1, C_M + 8 (L3 (0.6))."

- **C-4 (WORDING). `L3_listR.md:45`.**
  - **Correction 1:** replace "and max(orig) ≤ p_raw (`v3_fit.R:118`)" with "and max(orig) ≤ p_raw (`orig` = `pre$kept` = `which(!constant)` over the p_raw columns, `v3_preprocess.R:112`; `v3_fit.R:118`)".
  - **Correction 2:** replace "(`v3_run.R:245-269`)" with "(`v3_run.R:245-269`; on the exact branch also the constant-size wrapper `v3_exact_list_last`, `:274-279`, inside the constant 40000)". The wrapper is about 800 bytes, and the constant has about 2.5 kB of slack.
  - Apply as written.

- **E-1 (WORDING, optional). `ERRATA.md:5`.** "[applied]" is a status marker, not a mis-copy. For clarity, "[applied]" → "[applied in L3 (0.5), v1.4]".

## Gates and score

- **G1 correctness: PASS.** Every step of the chain holds, and C-1 does not affect any bound.
- **G3 faithfulness and scope: PASS.** F-1 is a wording-level application slip, to be applied as written.
- **G4 statuses and pins: PASS.**
- **G5 registration form: PASS.**

**Score: 8.7**

COUNCIL-VERDICT round=R4 manifest=5d06f5c6416c7f075119516605ebcaf63093f3ffaef6f7bb4f5d24f9e62333cb seat=opus score=8.7 gates=PASS
