PURE check of the 8 NEXT_BATCH patches (fresh Opus seat). Five of the eight are PURE. Three are NOT-PURE, and in all three the inserted text is correct: NB-C3 and NB-C4 misstate their registry effect, and NB-F3 stops applying once the NB-T10 patches are in.

**Snapshot.** HEAD moved three times while I worked: efec7af5 → d432ca4f (T9 card v2, MEAS-D_stage.patch re-staged) → 7ce98792 (NEXT_BATCH landing rules) → 45b89721 (new NB-C1v2, NB-C1r, NB-C4r, NB-C5log, NB-C6err patches). Those five new patches are outside this brief and I did not check them. The 8 patches under test, the brief and all target files are byte-identical between efec7af5 and HEAD. Every check below uses the current files.

**Method.** All work was in `.rc_tmp/nbpure_opus2/` (no tracked change, nothing committed). I used `patch -p1 -F0`, so any fuzz or offset counts as a failure. "Card" means `T9/FABLE_CARD.md` v1 (efec7af5) and v2 (HEAD), and `T10/FABLE_CARD.md` §1. The text match is a script that applies the card's old→new strings to the predecessor state and compares the result with the patched file. Registry effect is `bvsreg.claim_hash` from `Theory_work/INFRA/tools` run on each scratch tree. In BASE it reproduces every `claims.tsv` sha256 involved.

---

**NB-C1: PURE**
1. **Mechanics.** It applies at -F0 on both the current MEAS-D_stage.patch and the efec7af5 one; the two differ only at `W3-SAMP/STATEMENT.md:190`. The only changed line is :36, and the file stays at 192 lines. The patch's `index 17e0ee7e..` line still names the old MEAS-D post-image (the current one is 95351f2b). That is cosmetic for `patch`, but should be refreshed.
2. **Character diff.** A pure insertion at col 232 of :36, right after "…`lemmas/MEAS_D.md`).", of " By erratum E1 (…), … as outer probabilities if the clock is not modelled."
3. **Text match.** Equal to card v1 (c)1 and to v2 §B.1 (script: True for both).
4. **Truth: true.**
   - GW-iii (`W3-AUDIT/track_A/T1_GW/STATEMENT.md:80-83`) gives "on 𝒪 the statistical fields of 𝓒 equal P°'s". CAL-d (`T5_CAL/STATEMENT.md:42`) gives it on 𝒜 as well.
   - GW-iv (:85-91) gives 𝒪 ∩ A ⊆ 𝒪° ∩ A° and 𝒜 = 𝒜° ∩ G ⊆ 𝒜°. The outer-probability caveat is GW "Not claimed" (:99-101).
   - Note for the Fable's addendum (this patch is HELD anyway): for "intersected with the actual 𝒜" the inclusion that does the work is 𝒜 ⊆ 𝒜°, not the displayed 𝒪 ∩ A ⊆ 𝒪° ∩ A°. The cited GW-iv contains it, so the text is not false, but it is imprecise.
   - The transfer rules cited as `:CAL-C` sit in the T5_CAL "flag" paragraph (:45-54), outside CAL-C's registered span 28-43.
   - No new hypothesis.
   - (The brief's path `W3-AUDIT-A/track_A/` does not exist. The files are under `Theory_work/Wave3/W3-AUDIT/track_A/`.)
5. **Registry effect.** It touches the W3-SAMP premises span :20-60. The hash changes for PC, MR, ST, D, LT#, LT#(f), C and TR, which are the same 8 that MEAS-D already changes, so one rehash covers both. CC is not affected (its premises are :38-51). No claim sentence (:88-177) changes.

**NB-C2: PURE**
1. **Mechanics.** It applies at -F0. Only `W3-READER/STATEMENT.md:16` changes, and the file stays at 46 lines.
2. **Character diff.** Insertion at col 33, before ";", of " (the potential pair of the uninterrupted run, `W3-SAMP` erratum E1)".
3. **Text match.** Equal to v1 (c)2 and v2 §B.3. The anchor "success event $\mathcal A\in\sigma(\mathcal C)$" spans lines 15/16.
4. **Truth: true.** 𝒜° ∈ σ(𝓒°) is GW-iv. This is the reading E1 records, and it matches PoolZ Remark (iii).
5. **Registry effect.** It is inside the PoolZ span 12-39, and the PoolZ hash changes, so the recorder rehashes. The claim sentence (:21-23) is unchanged.

**NB-C3: NOT-PURE (registry statement only; the text is PURE)**
1. **Mechanics.** It applies at -F0. Only `lemmas/R4_printed_outputs.md:18` changes, and the file stays at 48 lines.
2. **Character diff.** Insertion at col 52, before the final ".", of "; read as the potential pair by erratum E1 (`W3-AUDIT-A:GW`, `:CAL-C`)".
3. **Text match.** Equal to v1 (c)3 and v2 §B.2.
4. **Truth: true.** Same basis as NB-C1.
5. **Registry effect: misstated.** `claims.tsv` registers `W3-READER:R4` as lines 1-48 of this file, so line 18 is inside its hashed span and the R4 hash changes. The patch header ("Inputs paragraph (not the claim)") and the NEXT_BATCH row ("not the claim") are wrong for the registry. If the recorder skips the rehash, check.py will raise C2-changed. The meaning is EQUAL.
6. **Minimal correction.** In the header, replace "(not the claim)." with "(inside `W3-READER:R4`'s registered span 1-48; premises :25-29 untouched; wording, the recorder rehashes R4)." Make the same change to the NEXT_BATCH.md row. Carry it into the rebuild from the addendum.

**NB-C4: NOT-PURE (registry statement only; the text is PURE)**
1. **Mechanics.** It applies at -F0. Only `READER_VERSIONS.md:1302` changes, and the file stays at 1458 lines.
2. **Character diff.** Insertion at col 35, after "(fallback ladder included)", of ", in the run taken as if uninterrupted".
3. **Text match.** Equal to v1 (c)4 and v2 §B.4.
4. **Truth: true.** completed ⊆ 𝒜 ⊆ 𝒜°. Theorem 10's conclusions are intersections, so they hold for 𝒜° (E1, R4).
5. **Registry effect: misstated.** `W3-READER:R1` has the premise span `READER_VERSIONS.md:1283-1388`, and :1302 is inside it. The R1 hash changes, but the header says "Not a registry span". BATCH_READY_v2 already bumps R1 and cascades it into W3-D2/D3, so if NB-C4 lands separately there will be a second bump.
6. **Minimal correction.** In the header, replace "Not a registry span." with "Inside `W3-READER:R1`'s premise span READER_VERSIONS.md:1283-1388: R1 rehash/bump (join the BATCH_READY_v2 R1 bump if landed together)." Make the same change to the NEXT_BATCH.md row.

**NB-INT: PURE**
1. **Mechanics.** It applies at -F0. Only `W3-READER/STATEMENT.md:32` changes, and the file stays at 46 lines. NEXT_BATCH.md says "this one line 35"; the line is :32.
2. **Character diff.** "; t" at col 20 becomes ". (Both sides are finite. … ≤\kappa_n$.) T". The change from ";" to "." and from "t" to "T" is the punctuation the inserted sentence needs. Nothing else changes.
3. **Text match.** Equal to card v1 (b) once LaTeX is mapped to Unicode ($, \le, \ge, \kappa, b_0, ^{-\nu}, \hat Z, \mathbf 1_{\mathcal A}). Script result: True. Card v2 replaced this text with a MEAS-D citation, but the manager's 7ce98792 landing rule keeps the v1 (b) text, so I matched against v1 (b).
4. **Truth: true.**
   - D_S = Π((n+1)λ_i+1)/(λ_i+1) ≥ 1.
   - Q_S ≥ y'y/(n+1) > 0, because n·z'H⁻¹z ≤ (n/(n+1))·y'P_S·y.
   - So m(S) ≤ (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀))·(2b₀)^{−ν} (`W3-T03ACC/STATEMENT.md:29-30`).
   - ϖ(S) = w(|S|)/W_K sums to 1 (:27), so Z ≤ κ_n.
   - Tower property for Ẑ ≥ 0 in [0,∞] (monotone convergence), then E[1_𝒜Ẑ] = E[1_𝒜Z] ≤ κ_n.
   - No new hypothesis.
   - Readability note: "c_n" is not defined in the span or in T03ACC (which writes the constant out; MEAS-D Step 6 calls it C_n). Line numbers: D_S, Q_S, b₀ and ν are at :29, m(S) at :30, Z at :31.
5. **Registry effect.** It is inside PoolZ 12-39, the hash changes and the recorder rehashes. The claim sentence is unchanged. NEXT_BATCH's note that "NB-C1 and NB-C2 are the only two that change a hashed span" is wrong: NB-INT, NB-C3 and NB-C4 do too.

**NB-T10-1: PURE**
1. **Mechanics.** It applies at -F0. Only `CLAIMS_CARD.md:78` and `READER_VERSIONS.md:956` change, and line counts are unchanged.
2. **Character diff.** At :78 col 118, "$(q_n+s_0)$-sets" becomes "sets of size at most $q_n+s_0$". At :956 col 110, "at most " is inserted.
3. **Text match.** Equal to T10 card row T10-1 (both strings; script True).
4. **Truth: true.** The formal (A1) at `READER_VERSIONS.md:938-939` says |S| ≤ q_n+s_0, and so does `W3-SCR` A1 (:158-159).
5. **Registry effect.** None (no hash changes). :956 lies outside R1's spans (661-811, 1283-1388), and CLAIMS_CARD is in no span.

**NB-T10-2: PURE**
1. **Mechanics.** It applies at -F0 on top of NB-T10-1 and fails without it (checked). Only `CLAIMS_CARD.md:78` and `READER_VERSIONS.md:950` change. :951 ("**not** covered…") is unchanged.
2. **Character diff.**
   - :950 col 69: "Signal sizes or floors that vary with $n$ are" becomes "The bounds $\kappa$, $b_0$, $M$ and $\sigma_*^2$ must not depend on $n$; the coefficients themselves may vary within them. A signal minimum or a floor tending to zero is".
   - :78 col 636: "Signals varying with $n$ are" becomes "The bounds must be fixed in $n$ (the coefficients may vary within them); a signal minimum or floor tending to zero is".
3. **Text match.** Equal to T10 card row T10-2 (script True).
4. **Truth: true.** W3-SCR A1 (:158-163) fixes κ, b, M and σ, not θ*. This matches reader (A2) at :941-942.
5. **Registry effect.** None. The stacking pair NB-T10-1 → NB-T10-2 on :78 works.

**NB-F3: NOT-PURE (mechanics of the stack; the text is PURE)**
1. **Mechanics.**
   - On Sol2-S2-2 it applies at -F0, and only `CLAIMS_CARD.md:76` and :97 change.
   - In the documented full stack (BATCH_READY_v2, then MEAS-D, then NB in order), hunk 1 FAILS at -F0. Its context includes :78, which NB-T10-1 and NB-T10-2 rewrite. It only succeeds "with fuzz 2". The reverse order (F3 first) makes NB-T10-1 and NB-T10-2 fail, because their context includes :76.
   - So NEXT_BATCH's "0 failures" holds only with fuzz, and `git apply` would reject it.
   - The fuzz-2 result is the intended one: :76 and :97 match F3, :78 matches T10-2, and every other line is untouched.
2. **Character diff.**
   - :76 col 249: "the printed evidence" becomes "$\exp$ of the printed field `log_Z` (not `log_Z_list`, row 3.1L)".
   - :97 col 418: "the printed evidence" becomes "$\exp$(`log_Z`), the printed pooled evidence,".
3. **Text match.** Equal to the card's F3 row (v1 and v2; script True).
4. **Truth: true.** `v3_run.R:154` (also at pin 4676af6) sets `out$log_Z <- v3_log_sum_exp(logZr) - log(R)`, so exp(log_Z) = Ẑ. `log_Z_list` is the 3.1L field (:236-266). Registry effect: none.
5. **Minimal correction.** Rebuild the patch on NB-T10-2. The rebuilt patch is at `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9/.rc_tmp/nbpure_opus2/NB-F3_rebuilt.patch`. Its −/+ lines are identical to the staged patch; only the :78 context line and the header ("… and on NB-T10-2 … apply … NB-T10-1 and NB-T10-2 first") differ. With it, the full 37-item stack applies at -F0 with 0 failures.

**Set-level results**
- **Disjointness.** The NB set changes these lines: CLAIMS_CARD 76/78/97, READER_VERSIONS 950/956/1302, READER STATEMENT 16/32, SAMP STATEMENT 36, R4 18. None overlaps a BATCH_READY_v2 changed line except :97, which is stacked on S2-2 as declared. NB-INT (:32) and T9-F1 (:26) are disjoint.
- **Line counts.** Every file keeps its line count except the known ones: W3-DIST 499→500 (BR), and W3-SAMP STATEMENT 186→192, REPORT 194→206 and the new MEAS_D.md (96 lines), all from MEAS-D.

PURE-VERDICT: NOT PURE: NB-C3, NB-C4, NB-F3
