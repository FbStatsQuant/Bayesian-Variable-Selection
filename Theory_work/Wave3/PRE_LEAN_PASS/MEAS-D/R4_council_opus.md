Manifest verify printed `verify: OK MANIFEST aa601f82ca78b6f81b6c67e6f1a5ac590004fd9707170a1bd23747da5ea63caa`. I ran the converter on a scratch copy in `.rc_tmp/measd_r4_opus/`. I edited no tracked file, committed nothing and started no subagents.

# R4 council review (Opus seat): W3-SAMP:MEAS-D

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 (F5) | ACCEPT | `MEAS_D.md:37, :40`. Details under §2. The sentence lists the `eval` call sites exactly: `v3_engine.h:122, 153, 174, 186, 291`. A grep of `v3_engine.h` finds only two other calls, at `:382` and `:391`, and both are inside `local_search`, which is not island code. Final islands run with `init_states = nullptr` (`v3_core.cpp:446`), so the `:291` models are π₀ draws (`:289`). `held` (`:118`) re-offers the current state, which is already in 𝓜_r. The bound holds (see below). Notation clash in E22. |
| 2 (S̃₀ / P2) | ACCEPT | `MEAS_D.md:39`. In the code the ledger is offered: tables (`v3_core.cpp:384`), inherited models (`:427`, `offer_stores`), island `eval`s, the final local search's scans (`v3_engine.h:391`; centre not emitted, `v3_core.cpp:456` `false`), the LS0 centre (`:476` `true` → `v3_engine.h:382`) and the LS0 scans. Two other places touch the ledger. `:431-440` rewrites only the HPM provenance label. `:502` runs only under `numerical_failure`, which is unreachable under EX-A and leaves no output. A cache hit gives no offer (`v3_ledger.h:112`), but each model's first evaluation in a run is fresh (`v3_core.cpp:409`), so the offered set equals the evaluated set. |
| 3 (h-paragraph) | REJECT | **The paragraph is not in the frozen file.** `MEAS_D.md:50` (Step 6) ends "…of §2 and of PoolZ are defined. ∎" with no h-sentence. `grep B_h\|H_r\|model summary` on the ticket finds only the statement clause (`:24`) and Step 5's forward reference (`:46`). `R3_to_R4.diff` and `git diff d432ca4f 7c9286dd -- …/ticket` change only citations in Step 6. The commit message ("Step 6 bounded-h paragraph") and the brief describe a paragraph that does not exist. The author's text (`T9_addendum_card.md:21` = `R3_texts_card.md:47`, last three sentences) is mathematically correct (F6). |
| 4 E13 | ACCEPT | `STATEMENT.md:190`, `MEAS_D.md:24`: "integrable under the joint law of §0, for every law of the data". `REPORT.md:203`: "under the joint law (H-U/SI), for every law of the data". |
| 4 E14 | ACCEPT | `MEAS_D.md:42`: the π-λ sentence comes right after the displayed P(·∣data) identity. `:46`: the signed-integrand split is present, but its "each finite by Step 6" depends on F6. |
| 4 E16 | ACCEPT | `v3_score.h:14` gives `a0 = 0.01, b0 = 0.01`. `:61-70` gives w(k) = ½/C(2p−1,k) and logprior = logw − logW_K, so the prior sums to 1 over Ω. T03ACC:27 gives ϖ(S) = w(∣S∣)/W_K. All three are cited at `MEAS_D.md:50`. |
| 4 E17 | ACCEPT | `MEAS_D.md:89` reads "(theory/PRE-LEAN-walkB, dc2e7174)". |
| 4 E18 | ACCEPT, wording E21 | `MEAS_D.md:38`. The content is right: CC5 (`CC_code_check.md:88`) puts every ledger model in Ω, and TDP's S* is a maximiser on Ω (`T9_TDP/STATEMENT.md:14`). But the insertion leaves a run of "…and swaps keep the size, and both centres lie in Ω (…), and the LS0 cap-range `stop`", which hides the three-item list. |
| 4 E19 | ACCEPT | `MEAS_D.md:3` names R1-R4 and MANIFEST_MEASD…MEASD4, with the Sol seat bound to MEASD4. `REPORT.md:205` reads `gates: correct:PENDING(reviews/R4_council_opus.md)`. |
| 4 E20 | ACCEPT | `REPORT.md:204` has `W3-SAMP:PC@stmt:PC-iii`. It is used at `MEAS_D.md:39`, "(`W3-SAMP:PC` (iii))". (iii) is the ledger-offer clause at `STATEMENT.md:92-95`. `W3-SAMP:PC` is in claims.tsv. The locator form matches the block's existing `GW@stmt:GW-iii,…`. |
| 4 REGISTRY h-clause | ACCEPT (matches) | `REPORT.md:203` "1_A0 Zhat_r H_r(h), for every bounded h of section 2" is the ASCII form of `STATEMENT.md:190`. The same qualifier correction applies to both (F6(b)). |
| 5 | ACCEPT | Scope is still potential-only (`STATEMENT.md:190`, last sentence). The converter exits 0 and gives one record: lines [190, 192], status_source `lemmas/MEAS_D.md:3`, 11 `depends_on` items, none with spaces. `STATEMENT.md:188-192` has no `\|` or `‖`, and the block uses `\|` only as a field separator. §§0-3 differ from the repo copy only at `:36`. New items from the R4 edits: F6 (an omission), E21-E24. |

**Item 1 detail.**
- **(a) Call sites.** Covered in the table. The five sites are exact.
- **(b) Borel.** Each proposal is a Borel function of (state, data constants, uniforms), by the same control flow as Lemma B (B-0) and (B-d), just as `D_theorem.md:25-26` argues for the π₀ draws.
  - Gibbs: deterministic flip of coordinate j.
  - Uniform swap: `S[floor(u·k)]`, then `nth_nonmember(floor(u·(p−k)))`.
  - Neighbour swap: candidates from N(X), then `floor(u·|cand|)`.
  - Independence: `draw_pi0`, which is categorical draws on the start tables (`v3_start.h:158-176`).
  - The state comes from Lemma B's record, whose within-round path is the sequence of states.
- **(c) Bound.** Each labelled step calls `eval` at most once (`v3_engine.h:113-192`). A round has m = p + B + 2 labels (`:72`). There is one round per particle per stage (`:331`), per burn-in round (`:345`) and per measured round (`:355`). So on a cell (R, T, N_e, L) the number of evaluations is at most
  - **N_e·[1 + (p + B + 2)(T + L + H_m)]**,
  - with B ∈ {1, …, 16} (`v3_core.cpp:146`) and H_m = `measured_rounds` = 4 (`v3_core.cpp:396`; `W1-N1/STATEMENT.md:31`). Both are fixed options.
  - The number of uniforms read is bounded in the same way.
- **(d) Premise.** None is added.

## 2. Verdict lines

`(F5) 𝓜_r Borel per cell: PROVED, NO NEW PREMISE`

`(S̃₀ / P2): COMPLETE AND CORRECT`

`(h-paragraph) integrability: NOT IN THE FROZEN FILE — MEAS_D.md:50 (Step 6) contains no bounded-h sentence, so the statement clause "1_{𝒜°}Ẑ_r·H_r(h) … integrable" (STATEMENT.md:190, MEAS_D.md:24, REPORT.md:203) has no proof step; the author's text (T9_addendum_card.md:21) is correct; correction in F6. No new premise once the qualifier in F6(b) is written.`

**Checks on the author's text (correct).**
- **|H_r(h)| ≤ B_h.** H_r(h) = (4N_e)⁻¹Σ_qΣ_i h(S_{rqi}; 𝓒) is an average of values of h (`W1-N1/STATEMENT.md:51`), so |H_r(h)| ≤ B_h.
- **Measurability.** H_r(h) is Borel: the S_{rqi} are coordinates of the island record (Step 4), and h is jointly measurable on Ω × E_𝓒 (`STATEMENT.md:107`).
- **The two bounds.** |1_{𝒜°}Ẑ_r H_r(h)| ≤ B_h·1_{𝒜°}Ẑ_r, so its expectation is at most B_h·κ_n by Step 6. |1_{𝒜°}Zπ(h)| ≤ κ_n B_h.
- **The identity.** (N1) (`W1-N1/STATEMENT.md:102`) integrates through Step 5's positive/negative split to E[1_{𝒜°}Ẑ_r H_r(h)] = E[1_{𝒜°}Zπ(h)], with both sides finite.
- **(MR-a)-(MR-c).** These integrate likewise. Their weights Ẑ_{r,t}/Z_t and W_r have expectation P(𝒜°) ≤ 1 by the same identities at h ≡ 1. The card's "likewise" is loose about this.
- **B_h uniform in the data.** It is for every h W3-SAMP uses: 1{j ∈ S}, 1{S = S₀} and [0,1]-valued h (Corollary E), all bounded by 1. The sup-norm errors are statements about H_r and p̂_r, not h's, and are also bounded by 1.

## 3. Findings

**F6 (the h-clause has no proof step). `MEAS_D.md:50`; `STATEMENT.md:190`, `MEAS_D.md:24`, `REPORT.md:203`.**
- **Problem.** R4 adds to the statement the integrability of 1_{𝒜°}Ẑ_r·H_r(h). Step 5 (`:46`) relies on it ("each finite by Step 6"). But Step 6 never proves it: the paragraph the commit message and brief describe is missing from the frozen file.
- **Is it more than wording?** Yes, in that a stated clause has no proof in the file. The fix is a mechanical paste of already-correct text plus one qualifier. The mathematics is not in doubt.
- **Exact correction (a).** In `MEAS_D.md:50`, before the final " ∎", insert:
  > "The same holds with a bounded model summary. For h as in `W1-N1/STATEMENT.md` §1 (`STATEMENT.md:107-108`), with a deterministic bound |h| ≤ B_h that does not depend on the data, H_r(h) is Borel (the S_{rqi} are coordinates of the island record, Step 4) and |H_r(h)| ≤ B_h, so |1_{𝒜°}Ẑ_r·H_r(h)| ≤ B_h·1_{𝒜°}Ẑ_r is integrable with expectation at most κ_n·B_h, and |1_{𝒜°}Z·π(h)| ≤ κ_n·B_h. Hence (N1) integrates, by Step 5's split into positive and negative parts, to E[1_{𝒜°}Ẑ_r·H_r(h)] = E[1_{𝒜°}Z·π(h)], with both sides finite; (MR-a)–(MR-c) likewise, their weights having expectation P(𝒜°) ≤ 1 by the same identities at h ≡ 1."
- **Exact correction (b), the qualifier.** §2's class is "W1-N1's class", where the data enter h as constants, so B_h could be read as depending on the data. Write the qualifier into the statement:
  - `STATEMENT.md:190` and `MEAS_D.md:24`: "for every bounded h of §2" → "for every h of §2 whose bound B_h does not depend on the data".
  - `REPORT.md:203`: "for every bounded h of section 2" → "for every h of section 2 with B_h not depending on the data".
  - Without this, an h whose bound grows with the data gives E[1_{𝒜°}Ẑ_r|H_r(h)|] ≤ κ_n·E[B_h(data)], which need not be finite for every law of the data.

**E21 (E18 sentence). `MEAS_D.md:38`.**
- Rewrite the middle as: "…the scorer's `|S| > K` throw (`cpp/v3_score.h:230`), unreachable because both centres lie in Ω (the running best by CC5, S̃₀ by TDP), the search skips additions at size K (`cpp/v3_engine.h:397`) and swaps keep the size; and the LS0 cap-range `stop` (…)".

**E22 (notation clash). `MEAS_D.md:37`.**
- "u₁, …, u_κ" clashes with κ_n in Step 6 and the statement. Write "finitely many uniforms u₁, u₂, … of U^{(9+r)}", or use another letter.

**E23 (optional, state the bound). `MEAS_D.md:37`.**
- After "bounded by a function of (p, T, N_e, L)" add "(at most N_e[1 + (p + B + 2)(T + L + 4)], B and the 4 measured rounds being options; `cpp/v3_engine.h:72, 113-192, 331, 345, 355`)".

**E24 (external input). `MEASD4_EXT.txt`.**
- F6's text and Step 5 cite `W1-N1/STATEMENT.md` §1 (the h class and H_r) and :102 (N1). That file is not among the 20 frozen inputs. Add it in the next manifest.

No C or S.

## 4. Gates

- **G1 correctness: FAIL.** F6: the statement's h-integrability clause has no proof step in the frozen file. F5, P2 and Steps 5-6 otherwise check out.
- **G3 faithfulness and scope: PASS.** Scope is potential-only and no premise is added. The qualifier in F6(b) only makes explicit what N1's "deterministic bound" already means. One record mismatch should be noted: the commit message and brief describe a Step 6 paragraph that is not in the file.
- **G4 statuses and pins: PASS.** I checked these pins: `v3_engine.h:72, 104, 118, 122, 153, 174, 186, 291, 382, 391, 397`; `v3_core.cpp:384, 409, 427, 446, 456, 474, 476`; `v3_ledger.h:112`; `v3_score.h:14, 59, 61-70`; T03ACC:27. The status line and the gates pointer are updated.
- **G5 registration form: PASS.** The converter exits 0. There are 11 `depends_on` items, none with spaces, and the span is 190-192.

gates=FAIL (one F held).

## 5. Score

**8.7.** One F (F6), fixed by pasting text that is already written and checked, plus one qualifier. No C or S.

## 6. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R4 manifest=aa601f82ca78b6f81b6c67e6f1a5ac590004fd9707170a1bd23747da5ea63caa seat=opus score=8.7 gates=FAIL
