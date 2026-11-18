# READER editorial round: hand-off to the recorder (items I did not edit)

Written 2026-11-17 by the READER editor (Sonnet) on `theory/W3-READER-ED`. Registry read at main c9b3b967. Each item is either in a registry file or in a claim's hashed span.

## 1. R4 premise pointer (registry file, `claims.tsv:530`)
- `W3-READER:R4` premises column = `Theory_work/Wave3/W3-READER/lemmas/R4_printed_outputs.md:28-32`. It is stale after the v1.13 re-anchor (d40c9780 left it "for the editorial batch").
- Current text at :25-29 is the Claim paragraph (":25 ## Claim (R4)", ":26-29 Assume Setting R … all conclusions of (C-v) hold with rate ρ_n"). :28-32 now covers the end of the Claim and the start of the proof.
- Proposed pointer: `Theory_work/Wave3/W3-READER/lemmas/R4_printed_outputs.md:25-29`. If R4's lines are edited (items 2 and 3), keep their line count unchanged so this stays correct.

## 2. R5 E-b: R4 header line 5 (R4 hashed span 1-48)
- File: `lemmas/R4_printed_outputs.md:5`.
- Current: `this ticket's bridges R1 (B2.1, B6.1) "PROVED (by this seat, unchecked)".`
- Proposed: `this ticket's bridges R1 (B2.1, B6.1), `W3-READER:R1@1.0.3` "PROVED-CHECKED; council R3, …".` (registry: `W3-READER:R1@1.0.3` "PROVED-CHECKED; council R3, MANIFEST 7aebdf2e…, sol=9.5 PASS, opus=9.4 PASS", main 20d01e52).

## 3. R4 status quotes (R4 hashed span 1-48)
All are in `lemmas/R4_printed_outputs.md`; proposed text follows registry main 20d01e52 (HQ D111).
| line | current | proposed |
|---|---|---|
| 3 | `Status: **PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F** (registry `W3-READER:R4@1.0.1`, council R3)` | `Status: **PROVED-CHECKED** (registry `W3-READER:R4@1.0.2`, council R3; no condition on W1-N1:B, W1-N1:F since main 20d01e52)` |
| 5 | `` `W3-SAMP:C@1.1.5` "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, …" `` | `` `W3-SAMP:C@1.1.6` "PROVED-CHECKED; council R1, …" `` |
| 9 | `` `W3-SAMP:C@1.1.5` … "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS" [REG-2676] `` | `` `W3-SAMP:C@1.1.6` … "PROVED-CHECKED; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS" [REG-20d0] `` |
Keep the line count. The card, READER_VERSIONS.md and REPORT.md (non-registry lines) were requoted on this branch.

## 4. REPORT.md:46, a `depends_on` line inside the R4 REGISTRY block
`depends_on: W3-SAMP:C@1.1.5 ; …` should read `@1.1.6` if the recorder wants the block to match the registry. I left registry blocks untouched.

## 5. W3-RM2-R: the F-UNI cap sentence (R1-F6; not a READER file, not edited)
- Reference: `reviews/R1_council_sol.md:109-116` (W3-READER R1 council, Sol, F6). The frozen `W2-UNI/lemmas/L5_delivery.md:8-12` states the shipped cap ℓ_n+|start mode| and the amended allocation. Only the original `C-DLV` Prop-F used ℓ_n (`C-DLV/STATEMENT.md:32`).
- `Theory_work/Wave3/W3-RM2-R/READER_DELTA.md` has no sentence of that shape (:15 and :44 only mention F-UNI as a bridge target and the move cap).
- Best location guess: `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:219` (implication table, DLV-0 row). It reads "recovers the delivery conclusion of C-DLV:Prop-F@1.0.0 … and of W2-UNI:F-UNI@1.1.0 Step 2 under (D)" and "the method differs from Prop F's (LS0 cap ℓ_n + |S̃₀| instead of ℓ_n …)". It sits next to F-UNI@1.1.0, which may be the version the R1-F6 correction concerns. Also check `STATEMENT.md:23` (T2(a) row, "W2-UNI:F-UNI Step 2, as shipped").
- Proposed correction (Sol's exact wording): "The original C-DLV Prop-F configuration used cap ℓ_n. The frozen F-UNI@2.1.0 states the enlarged cap and amended allocation. The active reader delivery route is RM2-R's DLV-0, whose shipped-code audit and conditions are carried explicitly." If the sentence speaks of a former F-UNI version, give that version and its source.
- The W3-RM2-R lead should confirm the line. `W3-RM2-R/STATEMENT.md` lines are hashed, so a re-anchor is needed.

## 6. Found while running the checks (not caused by this branch)
- `check.py` on this branch and on main c9b3b967: 1 ERROR, `C2-changed W3-READER:R1`: "statement at lemmas/R1_set_sizes.md:1-59 no longer matches its sha256". The R1 lemma is unchanged on this branch (`git diff origin/main` touches only CLAIMS_CARD.md, READER_VERSIONS.md, REPORT.md and this file). It looks like a hash left stale by the 1.0.3 bump (20d01e52). Please check `registry.py rehash W3-READER:R1`.
- `run_ci --steps cite` (Python 3.13 venv): W3-D2, W3-D3 and W3-FAMC citechecks print FAIL (MISS 0 committed → 4, 2 and 3 now). These tickets' files are untouched here. W3-READER has no citecheck of its own.
