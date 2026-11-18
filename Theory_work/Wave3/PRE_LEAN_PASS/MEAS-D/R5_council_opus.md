Manifest verify printed `verify: OK MANIFEST 968cd72a718ffe0d68d8e6fd364bcc200c855a7824ffbdfeefd657a6a0dd4f43` (exit 0). I ran the converter on a scratch copy in `.rc_tmp/measd_r5_opus/` and kept all other scratch there too. I edited no tracked file, committed nothing and started no subagents. All 18 claimed edits in the brief's table are at the stated file:line, the three ABSENT checks hold, and the three ticket files match the brief's sha256 prefixes and line counts (194 / 206 / 96).

# R5 council review (Opus seat): W3-SAMP:MEAS-D

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 (F6a) | ACCEPT | **Paragraph versus R4's text.** I compared `MEAS_D.md:50` (from "The same holds…" to just before "∎") character by character with `R4_council_opus.md:58`. There is one difference: an insertion at character 43, ", for every h of §2 whose bound B_h does not depend on the data". Nothing else differs.<br>**|H_r(h)| ≤ B_h.** H_r(h) is an average of values of h (`W1-N1/STATEMENT.md:51`).<br>**H_r(h) Borel in the streams.** The S_{rqi} lie in the island record (`L1_bridge.md:14-17`, which includes the populations and the within-round paths). For data-dependent h see F7.<br>**The two κ_n·B_h bounds.** Both follow from E[1_{𝒜°}Ẑ_r] ≤ κ_n, which the same Step 6 proves earlier.<br>**(N1).** It integrates by the positive/negative split, with each part finite.<br>**MR weights at h ≡ 1** (`STATEMENT.md:107-116`; `MR_identities.md:27-30`). For (MR-b) and (MR-c), E[1_{𝒜°}W_r] = P(𝒜°), using E[W_r | 𝓒] = 1. For (MR-a), the localised weight is 1_{𝒜°∩{T≥t}}Ẑ_{r,t}/Z_t, and (MR-a) at h ≡ 1 gives P(𝒜° ∩ {T ≥ t}) ≤ P(𝒜°). So "expectation P(𝒜°)" is exact only for (MR-b) and (MR-c) (E25). The bound ≤ 1 holds in all three cases.<br>**Premises.** None is added. |
| 2 (F6b) | ACCEPT, with F7 | **Same words in four places.** The identical phrase is at `STATEMENT.md:190`, `MEAS_D.md:24`, `MEAS_D.md:50` and `REPORT.md:203`. The old "bounded h" wording is absent from all three files.<br>**Effect.** The phrase narrows the clause (CORRECTION-ONLY + WEAKER). It matches N1's "deterministic uniform bound" (`W1-N1/STATEMENT.md:62-63`).<br>**But a hypothesis is missing.** The phrase presupposes that h may depend on the data. N1's class lets "the fixed data enter as constants" (`W1-N1/STATEMENT.md:62`), and Theorem C really uses such an h: `C_theorem.md:37-40` has f_t = (1 − e^{Δ_t a})⁺ with a = d − d(S₀). Once h may vary with the data, the clause also needs h to be jointly measurable in the data, and it does not say so (F7).<br>**REGISTRY form.** `REPORT.md:203` uses "§2" next to "section 2" in the same field (E26). |
| 2 (inventory) | ACCEPT (bounds right; list incomplete) | **What I read.** `STATEMENT.md:107-116`; `MR_identities.md:25` (h class) and `:62` (C_d bounds the weight, not h); `LT_theorem.md:26`, `:37` (1{S≠S₀}, 1{S=S₀}); `C_theorem.md:28` (1{S≠s}, with s := S₀ at `C_theorem.md:8-9`) and `:47` (h ≡ 1).<br>**Result.** No h used by a clause that MEAS-D serves has a data-dependent bound.<br>**Omissions.** The inventory misses `C_theorem.md:37-40`, the f_t ∈ [0,1] used by (C-iii) and so by (C-v). That h depends on the data, through d, with B_h = 1. Its sentence "every h … is an indicator or the constant 1" is therefore false as written, though the conclusion holds. It also omits Corollary E's [0,1]-valued h (`W1-N1/STATEMENT.md:108-109`), which also has B_h = 1. |
| 3 E21 | ACCEPT | `MEAS_D.md:38`. The text is R4's E21 wording verbatim. The three exits now read as a list. |
| 3 E22 | ACCEPT | `MEAS_D.md:37` reads "finitely many uniforms u₁, u₂, … of U^{(9+r)}". The file uses κ only as κ_n (8 occurrences) and has no u_κ. |
| 3 E23 | ACCEPT | **Text.** `MEAS_D.md:37` gives the bound N_e[1 + (p + B + 2)(T + L + 4)], which equals R4's derivation with H_m = 4.<br>**Code.** `v3_engine.h:72`: nlabels = p + B + 2. `:113-192`: each step calls `eval` at most once, at `:122`, `:153`, `:174` and `:186`; `held` (`:103-105`) and `set_model` (`:80-83`) do not call it. `:331`: one population round per bridge stage. `:345`: one per burn-in round. `:355`: one per measured round, with Hm = 4. The leading "1 +" counts the N_e initial `eval`s at `:291`, which are cited earlier in the same sentence.<br>**Other `eval` calls.** The only ones are at `:382` and `:391`, both in `local_search`. |
| 3 E24 | ACCEPT | `W1-N1/STATEMENT.md` is at `MEASD5_EXT.txt:30`, at `MANIFEST_MEASD5.txt:22` (#EXTRA) and at `:46` (hash `70712d28…`). Verify is OK. |
| 4 (NB-C1) | ACCEPT, wording E27 | **Claim span.** In `R4_to_R5.diff`, the only change inside :190-192 is the F6(b) phrase. :192 (Conventions) is unchanged.<br>**§§0-3 against main.** I diffed lines 1-186 against `origin/main`: `36c36` is the only change. The main file has 186 lines.<br>**The E1 sentence (:36).** It has no clock clause. It cites GW-iii, which says the actual calibration fields equal 𝓒° on 𝒪 (`T1_GW/STATEMENT.md:80-83`), and GW-iv, which gives 𝒪 ∩ A ⊆ 𝒪° ∩ A° (`:85-88`). It matches `ERRATA_W3-SAMP.md` E1.<br>**The remark (:194).** It says "not part of any claim" and adds no premise. Its last clause is stated too broadly for actual final-run events on 𝒜 ∖ 𝒪 (`T5_CAL/STATEMENT.md:50`; E27). |
| 5 | ACCEPT | **Scope.** Still potential-only (`STATEMENT.md:190`, last sentence).<br>**Converter.** `ingest.py convert` on the scratch copy exits 0. It gives one record: lines [190, 192], status_source `lemmas/MEAS_D.md:3`, `depends_on` with 11 items and no spaces. The "§" survives in `strength.conclusion`.<br>**Absolute-value bars.** There are none in `STATEMENT.md:190-192`. `REPORT.md:199-206` has 5 `|` characters, all field separators.<br>**New items from the R5 edits.** F7 is new in R5. It is a missing hypothesis, so it is more than wording. E25-E29 are wording or registry only. |

## 2. Verdict lines

`(F6a) PROVED, NO NEW PREMISE` (for every h that does not depend on the data, which covers every consumer; for data-dependent h, the step "H_r(h) is Borel" needs F7's hypothesis; the "expectation P(𝒜°)" wording is in E25)

`(F6b) qualifier: CORRECT AND CONSISTENT` (as a narrowing of the bound; F7 adds the companion measurability hypothesis that it presupposes)

`(inventory): RIGHT` (no h with a data-dependent bound exists; the list misses `C_theorem.md:37-40` f_t, which depends on the data with B_h = 1)

`(NB-C1) outside the span, NO NEW PREMISE`

## 3. Findings

**F7 (a measurability hypothesis is missing from the h-clause).** Locations: `STATEMENT.md:190`, `MEAS_D.md:24`, `MEAS_D.md:50`, `REPORT.md:203`.
- **Problem.** "Whose bound B_h does not depend on the data" only has content if h may vary with the data. That is N1's class (`W1-N1/STATEMENT.md:62`, "the fixed data enter as constants"), and `C_theorem.md:37-40` uses such an h.
  - Under the joint law the clause then needs (data, S, c) ↦ h(S; c) to be jointly measurable, and nothing says so.
  - Counterexample: h_x(S; c) := 1{x ∈ N} with N a non-Borel set of data values, so B_h = 1. Then 1_{𝒜°}Ẑ_r·H_r(h) = 1_{𝒜°}Ẑ_r·1{data ∈ N} is not a random variable, so it is not "integrable".
  - In Step 6, "H_r(h) is Borel (the S_{rqi} are coordinates…)" proves Borel measurability only for h with no data argument.
- **Is it more than wording?** Yes: a stated clause lacks a hypothesis, and it would surface at once in Lean. Every consumer is unaffected:
  - 1{S≠S₀}, 1{S=S₀}, 1{j∈S} and 1 do not depend on the data.
  - f_t is continuous in d on each cell (Step 2) and Borel in the grid coordinates of 𝓒°. `C_theorem.md:37` already calls it "data-and-c-measurable".
- **Exact correction.**
  - `STATEMENT.md:190`, `MEAS_D.md:24`, `MEAS_D.md:50` (first sentence of the added text): "for every h of §2 whose bound B_h does not depend on the data" → "for every h of §2 that is a Borel function of (data, S, c) with a bound B_h that does not depend on the data".
  - `REPORT.md:203`: the same words, with "section 2" (see E26).
  - `MEAS_D.md:50`: "H_r(h) is Borel (the S_{rqi} are coordinates of the island record, Step 4)" → "H_r(h) and π(h) are Borel (h is Borel in (data, S, c), 𝓒° is Borel by Step 3, and the S_{rqi} are coordinates of the island record, Step 4)".
- **Related, before R5.** The "Consequently" clause (`STATEMENT.md:190`) applies to (MR) for every h of §2. Step 5's display (`MEAS_D.md:44`) needs a "bounded Borel g", so it presupposes the same joint measurability. The phrase above covers that too if it is also added once to Step 5, after "For every bounded Borel g": "(for (MR) and (N1), g is Borel when h is Borel in (data, S, c))". The fix is one phrase.

**E25 (MR-a weight expectation).** `MEAS_D.md:50`.
- Replace "their weights having expectation P(𝒜°) ≤ 1 by the same identities at h ≡ 1" with "their weights having expectation at most P(𝒜°) ≤ 1 by the same identities at h ≡ 1 (exactly P(𝒜° ∩ {T ≥ t}) for (MR-a), in its localised form, `MR_identities.md:27`; the integrands are Borel because the populations and within-round paths lie in the island record, `W1-N1/lemmas/L1_bridge.md:14-17`)".

**E26 (non-ASCII in the REGISTRY block).** `REPORT.md:203`.
- The field now reads "…for every h of §2 whose bound…", and the same field also says "…statement of section 2…". Of the 106 REGISTRY `conclusion:` lines in `Theory_work/**/REPORT.md`, this is the only one with "§".
- The converter accepts it.
- For uniformity with the block, and with R4's own F6(b) form, write "for every h of section 2 …".
- Optional, if HQ prefers identical words in all four places.

**E27 (the remark's scope).** `STATEMENT.md:194`.
- "A probability of an actual-run event, that is, one intersected with {completed} or with the actual 𝒜, … in either reading it is bounded by the probability of the corresponding potential event."
- This fails for an actual final-run event on 𝒜 ∖ 𝒪. Such events "transfer only on 𝒪" (`T5_CAL/STATEMENT.md:50`).
- §0's usage (`:33-34`) does not reach that case, so no claim is affected.
- Correction: "that is, an event of the statistical state intersected with {completed}, or a potential or calibration-time event intersected with the actual 𝒜 (§0, :33-34),".

**E28 (`depends_on` after the new paragraph).** `REPORT.md:204`.
- Step 6 now uses (MR-a) and (MR-c) at h ≡ 1 and W1-N1's (N1), registered as `W1-N1:Thm-N1`.
- The block records only `W3-SAMP:MR@stmt:MR-b`.
- Correction: `W3-SAMP:MR@stmt:MR-a,MR-b,MR-c ; W1-N1:Thm-N1@stmt`, which makes 12 items.
- Optional: the claimed integrability itself needs only MR-b.

**E29 (stale check-record pointers).** `MEAS_D.md:3`, `REPORT.md:205`.
- The status line still says the Sol 6.2 seat is "bound to the MEASD4 digest", and the gates pointer still names R4.
- MEASD4 lacks the F6 paragraph. At the next freeze, bind the Sol seat to MEASD5 (or its successor) and add R5.

**Outside scope (observation only).** `ERRATA_W3-SAMP.md:3` dates E1 "2026-11-23", which is later than today (11-18). It is not hashed, and it should be checked by HQ.

**Summary.** One F (F7), which is more than wording but leaves every consumer unaffected. No C and no S. E25-E29 are wording or registry only.

## 4. Gates

- **G1 correctness: FAIL.** F7: the h-clause as stated lacks joint measurability in the data. F6(a), E21-E24 and the rest of Steps 1-6 otherwise check out.
- **G3 faithfulness and scope: PASS.** The scope is potential-only and no premise is added. The NB-C1 text is outside :190-192, and §§0-3 differ from main only at :36. E27 is wording in a remark that is part of no claim.
- **G4 statuses and pins: PASS.** I checked these pins:
  - `v3_engine.h:72, 80-83, 103-105, 113-192, 291, 331, 345, 355, 382, 391`
  - `T1_GW/STATEMENT.md:80-88, 97-102`
  - `T5_CAL/STATEMENT.md:47-52`
  - `W1-N1/STATEMENT.md:51, 62-66, 102`
  - `L1_bridge.md:14-17`
  - E24 pinned; verify OK.
  - E29 (stale pointer) is noted.
- **G5 registration form: PASS.** The converter exits 0, the span is 190-192, there are 11 `depends_on` items without spaces, and there are no absolute-value bars. E26 and E28 are optional.

gates=FAIL (one F held).

## 5. Score

**8.8.** One F (F7). It is one missing hypothesis phrase, and no consumer is affected. No C and no S.

## 6. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R5 manifest=968cd72a718ffe0d68d8e6fd364bcc200c855a7824ffbdfeefd657a6a0dd4f43 seat=opus score=8.8 gates=FAIL
