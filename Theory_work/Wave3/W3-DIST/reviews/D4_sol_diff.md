D4 diff check — 05d6a8bc6a6872ca 47ffb2b603de5cc0 e53d74a2551d09f4 f7b05e3fc6872898 b13c4f3de011216e bb7d4a4f5e98205e 43eb0f99c2e3f625 f71ef1c422170bda

Independent diff review of the eight blocks in `reviews/DIFFS_D4.patch` and the new `PINS.md` record. Paths below are relative to `Theory_work/Wave3/W3-DIST/`. All eight launch hashes match, in the order STATEMENT, B3, TARGET, ASSUMPTION_MAP, API_CARDS, REPORT_extra, DEPS, PINS. I also reversed each supplied patch block in memory: its current-side text matches the working file, and the reconstructed old file matches its full SHA-256 in `reviews/MANIFEST_SW1.txt`, including `mkreport.py`. Thus the scope and comparisons below use the supplied freeze, not an inferred baseline.

Summary: 0 CRITICAL / 0 MAJOR / 3 MINOR / 0 NIT. The proof-route description, predictive specialization, positivity repair and historical review-hash repairs check. Three local map/record defects remain.

## Findings

### D4-01 — MINOR — (L₀) does not bound the cost of the reference (S₀, θ*)

**Place:** `TARGET.md:16`, the new sentence saying that (L₀) is enough for the size tail “with reference (S₀, θ*)”.

The distinction between (E)+(C) and (L₀) is now correctly stated for X/X′, but this particular reference claim is false. By `API_CARDS.md:10–11` and the reference definition in `STATEMENT.md:343`,

    L_{S₀} = min_ϑ B_{S₀}(ϑ),
    B_{S₀}(θ*) = (‖μ‖² + ‖θ*‖²)/n = ρ′.

Consequently (L₀; B) supplies a reference on S₀ attaining cost at most B; it does not supply that bound for the true coefficients θ*. For example, take two identical standardized columns, n ≥ 4, and θ* = (R, −R). Then μ = 0, (E; 0) holds, and L_{S₀} = 0, while B_{S₀}(θ*) = 2R²/n can be arbitrarily large. The zero reference coefficients on T = S₀ attain the minimum in this example. This is exactly the coefficient-cost/ridge-loss distinction the repair is intended to preserve.

**Minimal repair:** replace “with reference (S₀, θ*)” by “with reference T = S₀ and ϑ minimizing B_{S₀}(ϑ)”. The minimizer is the design-measurable ridge solution nH_{S₀}^{−1}X_{c,S₀}ᵀμ_c; G+I makes the minimization well defined even for singular designs. The true pair remains an admissible bounded-cost reference under (E)+(C), as the statement and repaired S registry correctly say. The corresponding amended `ASSUMPTION_MAP.md:15` sentence does not make this erroneous identification.

### D4-02 — MINOR — the historical-pin record includes foreign sources, misses local shorthand pins, and misidentifies some destinations

**Place:** `PINS.md:3–9` and the table, especially rows at lines 15–16, 24, 26, 29, 44, 58–59 and 75; missing rows for `COR_C.md:5,89–90` and `ASSEMBLY.md:19`.

Retaining genuine local pins as explicitly historical v1.3.1 references is workable. The present mechanically generated record does not correctly implement that policy:

1. Six table rows are not references to this ticket's STATEMENT at all. `H.md:5` and `H.md:6` cite D0 lines 8–18 and D4.0 lines 84–88 of **W3-POST2/lemmas/D_hellinger.md**. `P6_DISTC.md:64` and `COR_C.md:78` cite **W1-N1/STATEMENT.md:70** (EX-A); `P6_DISTC.md:270` cites **W1-N1/STATEMENT.md:71** (the within-stream law). `B3.md:30` explicitly says **W3-POST (v1.4)** before its bare `STATEMENT.md:38-39` citation, concerning the m♯ bound. The record instead maps these six citations to unrelated W3-DIST objects. In particular the B3 citation is explicitly not a W3-DIST v1.3.1 pin. This also contradicts the record's assurance that foreign sources were excluded.
2. Four local shorthand pins are missing: `COR_C.md:5` (`:171-175`, Theorem A (i), current STATEMENT lines 185–189); `COR_C.md:89` (`:29-39`, response-scale posterior and draw density, current 34–44); `COR_C.md:90` (`:37-39`, draw density/intercept, current 42–44); and `ASSEMBLY.md:19` (`:322-325`, Lemma X's display, current 355–358). These are active citations to this STATEMENT, even though the filename is elided. The first three were among the locations identified by SW1-06.
3. Some changed-text fallbacks identify a containing section instead of the object the citing sentence names. Most directly, `B3.md:26` cites old line 95 for **the four DIST-3 design events**; that line does contain them, and their current location is **103**, not the table's TR₀ definition at 101. `B0.md:115` cites old 139–140 for **the reader's original-units posterior**; the current passage is **148–152**, not Setup's opening at 136. `ASSEMBLY.md:153` cites old 189–192 for **the Example**; its current passage is **204–207**, not Theorem A's opening at 185. Other generic labels should likewise be made specific where the citing sentence is specific: for example `ASSEMBLY.md:15` names the constants convention (current 69–70), not (ND), and `ASSEMBLY.md:197` names Remark (4)'s C₁ formula (current 265–267).

**Minimal repair:** restrict the historical declaration to citations whose resolved source is this ticket's STATEMENT; remove the six foreign rows; add the four local shorthand rows; and correct the object names/current destinations above. Keep the proof files untouched. Use semantic anchors when changed text prevents exact line alignment. This repairs the record without changing any proof. I found no genuine local W3-DIST line citation in these eleven files that requires a post-v1.3.1 baseline; in particular the local citations in ASSEMBLY's later amendment at line 205 still resolve against v1.3.1. Foreign contextual citations, including `[SAMP]`'s bare STATEMENT references, must retain their own sources.

### D4-03 — MINOR — the report still attributes numerical evidence to weakening (A5)

**Place:** `REPORT_extra.md:54–55`, new sharpness prose: “(A3), (A5): candidate weakenings with numerical evidence only (`ASSUMPTION_MAP.md` §3), no proved replacement.”

Removing the WEAKENABLE registry entries correctly withdraws the claim of proved replacements, but the replacement prose still attributes numerical evidence to both assumptions. `ASSUMPTION_MAP.md:59–61` explicitly says that no simulation has tested violation of (A5). Its heavy-tail evidence concerns (A3), and its near-duplicate evidence concerns (A4). The new joint attribution is therefore unsupported for (A5). Calling the evidence numerical rather than a proof does not fix the source mismatch.

**Minimal repair:** split the claims: “(A3): candidate weakening with finite-family numerical evidence only; no proved replacement. (A5): candidate weakening without a proved replacement or a simulation testing its violation.” The removal of the coefficient-cost sharpness edge and the explicit unchecked qualification on the API attempt are otherwise correct.

## Repair checks

### SW1-01: adopted route of Lemma X

The new description agrees with `lemmas/X.md` §§1–7: V(a) is re-proved; the noise event precedes conditional Gaussian/IG control of good models and score suppression of small far models; the intermediate size range uses the untruncated λ = (4A+1)/(4A+2) moment. Non-supersets are compared with their union with S₀. The actual multiplicity factor is

    A_n = 1 + 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}
        ≤ 2·4^{s₀} n^{(A+1)s₀} ≤ 2·4^{s₀} e^t.

The exponent is paid using M₀ ≥ (A+1)s₀^r, with the remaining constants covered by log C₅ in M₀. Sizes above m_n(t) use the file's own numerator-in-expectation/denominator-on-noise-event argument. No stream-C file is an input to this proof. The A0/A1 row now correctly preserves the interface motivation without consuming A1's truncated weights. The actual Lemma X hypothesis/display is byte-for-byte unchanged by this patch. EQUAL is confirmed.

### SW1-03: predictive specialization and TC8

`P6_DISTC.md:151–161,299–317` gives d_H²(f̄_Q,f*) ≤ ε² + Q(B_n). Its Remark 6.6 (`:414–415`) explicitly substitutes ε² = C²tℓ_n/n for DIST-2. The repaired display uses the right ε² for each bad set, with the same completion/store-mass/success event and the same exceptional-probability bound.

EQUAL on TC8 is confirmed. TC8 must be read with the applicable master bad set/rate: the introducing sentence already said “(or (1.2), with its rate)”, and the proof already made that substitution. Read as an isolated formula for DIST-2, the old C²t/n display was an unsupported stronger bound; correcting that isolated formula does not weaken the fixed, contextual TC8 delivery statement. I do not confirm an unqualified C²t/n predictive guarantee for DIST-2.

### SW1-04: B3

The only change in `work/E_bridges/B3.md` is line 11. Positivity now agrees with (A6)(b) at `STATEMENT.md:212`. In Step 5, |β*_j|sd(x_j)/σ* ≥ b_n > 0 and ŝ_j² ≥ Var(x_j)/2 legitimately imply θ*_j² ≥ b_n²/2. Hence the displayed deterministic envelope M_n = b_n²nψ/(8 log n) is valid and diverges. The already appended A-1/A-2 amendments remain part of the current proof. The amended file needs no further repair from this diff check.

### SW1-02 and SW1-05: maps, stretches and protected text

The (E)+(C) bound on ρ′, its use in X/X′ and the 3ρ′ superset comparison, and the failure to establish an (L₀)-only DIST-1 are now correctly distinguished. The remaining reference error is D4-01; SW1-02 is therefore not fully resolved.

All new NEC status statements in TARGET, ASSUMPTION_MAP and Card F agree with `STATEMENT.md:120–124,372–379` and `lemmas/NEC.md` §0. They limit the negative result to the uniform fixed-design in-sample exponential core, leave the in-probability question open, and claim no iid random-design Hellinger counterexample. N4 is now explicitly historical finite-family evidence. SW1-05 is resolved.

An exact comparison with the reverse-patched freeze confirms that TARGET §5 and §6 are untouched. An independent string comparison confirms the complete reader block between the rules, from Setup through the notation table, remains identical to STATEMENT §1R: 9,888 characters in each. In particular Setup through Corollary C is identical.

### SW1-07: all seven registry/report subitems

| Sweep subitem | Result |
|---|---|
| DIST-1 rate at t = M₀ log n | RESOLVED. The explicit √M₀ factor and stated bound on M₀ agree with STATEMENT (c) and X §0; C remains independent of sparsity for the listed fixed constants. |
| DIST-3 scope and design-event premise | RESOLVED. The four events are restored in the in-probability consequence, and the registry retains the stated (RD), polynomial-p scope rather than silently adopting the proof's extra generality. |
| DIST-C alternatives and dependency | RESOLVED. The conclusion distinguishes deterministic domination, DIST-1 with ND, DIST-2 without ND at its rate, and the oracle/selection alternatives under their own premises; DIST-2 is added to depends_on. The combined assumption list is read with these explicit branch qualifications. |
| Theorem A common event | RESOLVED. The common event and single-predictor (A3) qualification of the no-(A4) alternative are recorded, as in the reader statement. |
| S reference hypothesis and cutoff/range | RESOLVED. The design-measurable bounded-cost reference replaces the exact-truth coefficient hypothesis; the pointer covers the actual cutoff and t-range. Under the separately listed energy bound, the true pair is a sufficient special reference when coefficient cost is bounded. |
| P6 predictive-convexity source | RESOLVED. The master-linked registry now lists only (a),(b). The amended mkreport.py P6 row separately points to §3 P6(c) of the proof file, which contains the convexity clause. |
| Point-mass-posterior commentary | RESOLVED. The denial is restricted to store-BMA domination/contraction; selection-based consequences retain their premises. |

The DIST-2 rate notation change p → p_raw agrees with ℓ_n. The revised Inputs and assurance wording accurately limits the absence of an upstream audit to a whole-proof audit and acknowledges the passages read by D1/D3/SW1; it does not discharge SOP:TH09.

### SW1-08: all three implication/sharpness subitems

| Sweep subitem | Result |
|---|---|
| Whole-claim implication edges to POST2:D and POST:Cor-1R | RESOLVED. Both edges are removed. The replacement prose is a comparison under each result's own hypotheses and limits the B2 comparison to the determinant-floor step. |
| A4 necessity from NEC | RESOLVED. The registry sharpness entry is removed, and the prose calls (A4) a sufficient primitive bridge with necessity unestablished. NEC remains fixed-design only. |
| A3/A5 weakening evidence and coefficient-cost sharpness | NOT RESOLVED in full. Proved-WEAKENABLE labels and the unsupported coefficient-cost registry edge are removed, and the API attempt is explicitly unchecked. D4-03 remains for the claimed numerical evidence concerning (A5). |

### SW1-09: historical review versions/hashes

The amended DEPS descriptions correctly bind L6's original verdict to DIST12 v0.1, sha c05fb3f082fcb938, and L7's verdict to NEC v0.2, sha 54340e87b89336a1. These hashes match the reviews' first lines. The current checked hashes and subsequent D1/D3 checks are retained. B3 is transparently marked stale pending this D4 review; the stretch rows merely refresh the STATEMENT hash.

## Historical-pin spot checks (SW1-06)

I read STATEMENT v1.3.1 directly with the permitted read-only `git show f54bd6f:Theory_work/Wave3/W3-DIST/STATEMENT.md`. The following table records 24 checked existing rows, including all required examples. “Correct” means the historical pin identifies the cited object and the supplied current locator is valid; changed-text start locators are accepted where they identify the intended object. Foreign-source and missing-pin defects are detailed in D4-02 rather than counted as successful checks.

| Citing file:line | Historical pin | Object / current locator | Check |
|---|---|---|---|
| H.md:4 | 291–295 | Lemma H / 322–326 | Correct |
| T.md:4 | 297–308 | Lemma T / starts 328 | Correct |
| DIST3.md:4 | 93–104 | DIST-3 / 100–112 | Correct |
| DIST3.md:25 | 390–391 | Inherited-premise paragraph / 438–439 | Correct |
| P6_DISTC.md:46 | 68–71 | DIST-1 (1.1) / 74–77 | Correct |
| P6_DISTC.md:51 | 86–88 | DIST-2 (1.2) / 93–95 | Correct |
| P6_DISTC.md:56 | 390–391 | Inherited-premise paragraph / 438–439 | Correct |
| P6_DISTC.md:96 | 248 | Code-facts heading / 273 | Correct |
| B0.md:14 | 29–32 | Exact posterior / 34–37 | Correct |
| B0.md:16 | 37–39 | Draw density / 42–44 | Correct |
| B0.md:29 | 161–162 | (A1) / 174–175 | Correct |
| B0.md:56 | 29–32 | Exact posterior / 34–37 | Correct |
| B0.md:87 | 45–47 | Distance / 50–52 | Correct |
| B0.md:115 | 139–140 | Reader posterior / should be 148–152 | Wrong destination; D4-02 |
| B1.md:20 | 32–33 | θ*, S₀, μ / 37–38 | Correct |
| B2.md:26 | 54–55 | (ND) display / 60–61 | Correct |
| B2.md:29 | 62 | Cutoff / 68 | Correct |
| B3.md:26 | 95 | Four design events / should be 103 | Wrong object/destination; D4-02 |
| B3.md:46 | 62 | Cutoff / 68 | Correct |
| B3.md:55 | 94 | (TR₀) / 101 | Correct |
| ASSEMBLY.md:11 | 68–71 | (1.1) / 74–77 | Correct |
| ASSEMBLY.md:16 | 86–88 | (1.2) / 93–95 | Correct |
| ASSEMBLY.md:125 | 310–316 | Lemma S / 342–348 | Correct |
| ASSEMBLY.md:153 | 189–192 | Example / should be 204–207 | Wrong object/destination; D4-02 |

I searched all eleven named files for explicit and elided numeric citations and resolved their sources in context. The table is not complete because of the four omitted shorthand pins; nor are all its rows local v1.3.1 pins because of the six foreign-source rows. The three files under `lemmas/` named in the PINS preface do indeed contain no numeric line pin into STATEMENT.

## Item 8: patch scope and mathematical changes

There are ancillary commentary edits beyond the nine numbered repairs: TARGET §4 adds the disposition of SW1's seven unharvested strengthenings, and REPORT_extra's Inputs and assurance section corrects the whole-upstream-audit wording discussed in SW1's unnumbered closing observations. These are accurate commentary changes, not adopted strengthenings. The DIST-2 p_raw notation cleanup also follows SW1's registry-audit note. Thus the literal answer to whether every non-version/non-trail hunk answers a numbered finding is **no**; the additional commentary is disclosed here, not treated as a new theorem or a defect requiring removal.

The literal answer to whether a theorem/lemma formula is touched is **yes**: STATEMENT (C-i)'s predictive formula is corrected for DIST-2, and B3's local copied hypothesis adds positivity. Those are the requested SW1-03/SW1-04 repairs. X's route paragraph is a description, not a proof step. No hunk changes a constant, a proof inference, Lemma X's statement, the master contraction displays (1.1)/(1.2), TARGET §5–§6, or the reader statements. Item 8 is VERIFIED as a completed scope audit with these explicit qualifications; it is not a claim that the patch contains only numbered-finding text or no changed mathematical display.

## Limits

This is a check of the specified repairs and their supporting interfaces, not a new sweep of unchanged mathematics. I did not re-audit external theorem proofs, code behavior, numerical scripts or experiments; the numerical-evidence finding uses the supplied map's explicit statement of what was not simulated. I inspected the supplied proof sections needed for the changed descriptions and formulas, all numeric-citation contexts in the eleven pin files, the historical STATEMENT snapshot, the two historical review headers, and the source-generation pointers. I did not execute mkreport.py or regenerate REPORT.md: writing either file is outside this review's authorization. No agents, cluster jobs, simulations, scratch files or state-changing git commands were used. The sole written file is this review.

## Verdict lines

SW1-01: RESOLVED.
SW1-02: NOT RESOLVED — D4-01.
SW1-03: RESOLVED.
SW1-04: RESOLVED.
SW1-05: RESOLVED.
SW1-06: NOT RESOLVED — D4-02.
SW1-07: RESOLVED — all seven subitems.
SW1-08: NOT RESOLVED — D4-03; subitems 1–2 and the other parts of subitem 3 are repaired.
SW1-09: RESOLVED.
Tag, SW1-01 EQUAL: CONFIRMED.
Tag, SW1-03 EQUAL on TC8: CONFIRMED.
work/E_bridges/B3.md: VERIFIED.
Item 8: VERIFIED — scope audit with the ancillary commentary and requested formula/hypothesis changes explicitly disclosed above.
Overall verdict: VERIFIED-WITH-AMENDMENTS — 0 CRITICAL, 0 MAJOR, 3 MINOR; SW1-02, SW1-06 and SW1-08 need the local repairs specified above.
