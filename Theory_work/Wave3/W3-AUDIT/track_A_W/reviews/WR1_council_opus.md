# WR1 — council seat `opus` (Claude Opus 5.5, high) — blind first read — W3-AUDIT track A_W: W1 (ISL), W2 (FRZ)

Manifest: `MANIFEST 0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea`; `manifest.py verify` → `verify: OK`
(run 2026-11-17 from `/home/fb31/BVS-wt/W3-AUDIT`). Core: `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` → identical;
the external inputs I read hash to the manifest's `EXT:` lines (checked `L1_bridge.md` and `MR_identities.md` by `sha256sum`).
Read: W1_ISL/{STATEMENT,PROOF,CITECHECK}, W2_FRZ/{STATEMENT,PROOF,CITECHECK}, `citecheck.py`, and the INPUTS_WR1 list.
Not read: INDEX.md, LOG.md, any CHECK.md, CHECKPOINT_*, API_CARD/, any other `reviews/` file (only the directory listing was seen).

## Verdict summary
The mathematics of both items is sound. W1: the island program at the pin is correctly read (uniform-reading sites,
counts, κ_max, κ(c), D_r(c) = N_e(1 + T + L + 4), stopping-time and fresh-uniform argument, cell-by-cell
measurability, coordinates for MR and D). W2: the freezing lemma proof is a correct monotone-class argument; SI, A₀ and
O_r = Φ(𝓒°, U_r) are established from T5 and the code; the localised conditioning, the three consumer uses and the
evidence bounds are right, and the potential/actual split follows T5. Two blocking but mechanical defects remain:
**F1** the exception exits on the potential path (scorer `NumericalFailure`, `|S| > K`, `nth_nonmember`, the inherited-model
`stop`, `v3_check_seed`) are not addressed, although W2 treats one such exit (`v3_check_grid`) and O_r = Φ(𝓒°, U_r) on E₀
needs all of them excluded; **F2** several citations of the older steps and of MR are shifted onto the wrong text (W2
cites MR "Step 3" at lines that are Step 4's end and the Remark; W1 cites (B-d) at lines that are mostly (B-c)). Both are
one-sentence / line-number repairs. Under the gate rule I must give `gates=FAIL`.

## Gates
| gate | result | basis |
|---|---|---|
| G1 correctness of every step and code citation | FAIL | F2 (wrong-text citations); all steps and all code line citations otherwise verified |
| G2 hypotheses used = stated | PASS | EX-A, H-U/SI, T1 potential run, T5 CAL-a–d, T6 (S)/(S′), T7 KER-d, FR used as stated |
| G3 no hidden assumptions | FAIL | F1 (no reachable exception exit on the island path / final-run prelude) |
| G4 imports and statuses verbatim | PASS | imports quoted correctly where quoted; statuses not recorded in the item files (E3) |
| G5 scope (potential vs actual, executed settings, streams, islands) | PASS | potential pair throughout; executed N_e, L; streams 9 + r; r ≤ 4; actual pair only via T5 |
| G6 fidelity to code, older steps, consumers | FAIL | F2 (older-step/consumer pointers); content agrees with `W1-N1:B`, `:F`, MR, D |

## Claims
| id | decision |
|---|---|
| W1 (ISL) | REJECT (this round; content correct, repair F1 engine-throw sentence and F2 citations) |
| W2 (FRZ) | REJECT (this round; content correct, repair F1 prelude/island exception sentence and F2 citations) |

## Findings

**F1 (F; G3; W2 primary, W1 secondary) — exception exits on the potential path are not excluded.**
`W2_FRZ/PROOF.md:82-88, 89-96` (FRZ-b (ii)/(iii)) argue that on 𝒜° the potential fit reaches `cpp_final_run` and that
island r's potential record is Φ(𝓒°, U_r), and they explicitly exclude one error exit (`v3_check_grid`, `v3_run.R:225`,
"an X2 site, unreachable on 𝒜°"). T1's potential fit replaces only check Booleans by FALSE (T1 Definitions, "Potential
fit"); errors and C++ exceptions still end the run. Unaddressed exits on the same path: `v3_check_seed(seed)`
(`v3_run.R:225`); `stop("inherited model larger than K")` and the scorer call in the inherited-model loop
(`cpp/v3_core.cpp:425-426`); inside every island (r and the islands < r that must complete for island r to run,
`cpp/v3_core.cpp:443-447`): `NumericalFailure` (`cpp/v3_score.h:237`, caught at `cpp/v3_core.cpp:483-484` → status
`numerical_failure`, no further islands), `|S| > K` (`cpp/v3_score.h:230`), `nth_nonmember` out of range
(`cpp/v3_engine.h:143`). If any were reachable on a positive-probability part of E₀, O_r would not exist there and
(FRZ-b)(iii), hence (FRZ-c), would fail as stated. Likewise `W1_ISL/PROOF.md:10-42` ("Hence Φ̃(c, u) is a function of
(c, u)", for every c ∈ A_s and every u ∈ Υ) tacitly assumes the island program terminates without an exception.
None is actually reachable, so the claims are true; the proof omits the reason.
*Repair (one sentence each).* W1 Step 2: under EX-A `sc.score` returns the exact log m, so `cpp/v3_score.h:237` is not
reached; `|S| > K` is unreachable (Gibbs adds only when |S| < K, `cpp/v3_engine.h:116`; swaps preserve |S|; π₀ is supported
on |S| ≤ K, T6 (S)); `nth_nonmember` receives ⌊u(p − k)⌋ ≤ p − k − 1 < #non-members (`cpp/v3_engine.h:151`). W2 (FRZ-b):
add the prelude exits (`v3_check_seed`: valid seed; inherited models are calibration-scored models with |S| ≤ K; scorer
exact under EX-A), or cite C1 (C1-b) ("X2-class sites … unreachable on valid internal state") together with EX-A for
`NumericalFailure`.

**F2 (F; G1, G6) — citations of the older steps and of MR point at the wrong text.** The files match the manifest hashes,
so these are not version drift:
- `W2_FRZ/PROOF.md:126`: "MR's Step 3 (`Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md:67-70`)" — lines 67-70 are the
  end of Step 4 and the Remark; Step 3 (the bound C_d) is `:60-62`.
- `W1_ISL/STATEMENT.md:14` and `W2_FRZ/PROOF.md:107`: MR "Step 2" cited as `MR_identities.md:57-65` — Step 2 is `:51-58`;
  57-65 runs into Step 3 and Step 4. `W2_FRZ/STATEMENT.md:12`: "Steps 2–4" cited as `:57-79` — Steps 2–4 are `:51-67`
  (68-79 are the Remark and the numerics).
- `W1_ISL/STATEMENT.md:19`, `W1_ISL/PROOF.md:78`: (B-d) cited as `L1_bridge.md:115-122` — lines 114-117 are (B-c)
  "Endpoints"; (B-d) is `:119-125`.
- `W1_ISL/STATEMENT.md:17`, `W1_ISL/PROOF.md:42`: (B-0) cited as `L1_bridge.md:65-78` — (B-0) is `:62-75` (78 is in (B-b)).
- Minor, same kind: `W2_FRZ/STATEMENT.md:9` `L3_freezing.md:25-46` for the proof (proof `:25-39`; 41-48 are Remark and
  numerics).
`citecheck.py` is range-only, so it reports all of these OK. *Repair:* replace the ranges as above and re-run citecheck.

**E1 (E) — ledger citation.** `W1_ISL/PROOF.md:27-28` says the ledger reads no uniform and (ISL-0) that it does not
influence Φ̃, citing only `cpp/v3_engine.h:89-105`. True at the pin (`Ledger::event`, `cpp/v3_ledger.h:104-113`: const
inputs, writes counters/stores only; `offer_stores` `:89`); add that citation, as `W1-N1:B` did (`L1_bridge.md:69`).

**E2 (E) — dangling changelog reference.** Both changelogs (`W1_ISL/STATEMENT.md:72`, `W2_FRZ/STATEMENT.md:56`) cite
`reviews/WLC1_reply_opus.md`; no such file is in `reviews/` (listing shows `WLC1_brief_opus.md`, `WLC1_disposition.md`).

**E3 (E; G4) — statuses of imports not recorded.** W1/W2 reuse T1, T5, T6, T7, FR, C1 and the older steps `W1-N1:B`, `:F`,
T12's freezing lemma (PROVED-LOCKED) without quoting their statuses. I could not check whether INDEX.md records them
(blind). Recommend one "Reuse (status verbatim)" line per item.

**E4 (E) — value space of 𝓒°.** T5 sets 𝓒° := ⊥ when P° does not call `v3_calibrate`; `W2_FRZ/STATEMENT.md:21-23` and
`W1_ISL/STATEMENT.md:30-31` need (T, grid, tier) defined (e.g. dummy-valued) and measurable on all of E, ⊥ and non-"ok"
records included, for "A_s is the preimage of a Borel set". Also state tier ∈ {0, 1} in A_s (N_e = `b$tiers$N[tier + 1]`
is NA otherwise); it holds on 𝒜° (`v3_calib.R:185-186`, e ∈ {0, 1}).

**E5 (E; G5) — data integration not in "Not claimed".** FRZ is at fixed data. `W3-SAMP:D` (D-iii) integrates the
conditional bound "over 𝓒 and the data" under the joint law (`D_theorem.md:46-51`), which needs a version jointly
measurable in the data (freezing with (data, 𝓒°) as the conditioning element, streams 10–13 independent of the data,
`W3-SAMP/STATEMENT.md:35-36`). FRZ does not claim it; add it to `W2_FRZ/STATEMENT.md` "Not claimed".

**E6 (E) — C1 PROOF reference.** `W2_FRZ/PROOF.md:85-86` cites "C1 (C1-b) (vii), `track_A_C/C1_AUDITS/PROOF.md`"; that
file is outside the declared inputs and C1's STATEMENT does not give invariant (vii)'s content. The argument does not need
it (if `v3_frozen`'s `v3_check_grid`, `v3_run.R:70`, failed, `v3_calibrate` would error and not return "ok"); say so.

**E7 (E) — finiteness of d.** `W2_FRZ/PROOF.md:124-125` "log m finite" — point to the valid-input hypothesis (FR: n ≥ 3, a
retained column, non-constant y, so m > 0) rather than T4 alone; the scorer has a `NEG_INF` branch
(`cpp/v3_score.h:223`).

## Score
**8.1 / 10** (C, S, F only: no C, no S; F1 a missing exclusion sentence on a path the item itself treats partially; F2
pointer errors to the older steps/consumers).

## Checks performed
- Manifest verify; core pin = HEAD; EXT hashes of `L1_bridge.md`, `MR_identities.md`.
- Every code citation in W1 and W2 read at the pin: `cpp/v3_engine.h` 14-23, 58-368 (eval, held, the four steps,
  draw_order, one_round, population_round, resample incl. u = 0 guard, run_island/run_island_s, clock lines 284/298/304/
  335/336/341/348/361); `cpp/v3_start.h:18-20, 153-176` (cat_draw_gt, draw_pi0 counts ≤ 1 + 2J); `cpp/v3_score.h:226-237,
  262-293` (exact-match find, insert, capacity clear); `cpp/v3_core.cpp:395-447, 483-484, 588-597, 239-249`;
  `cpp/v3_ledger.h:89-113`; `v3_run.R:66-92, 222-228`; `v3_fit.R:140-174`; `v3_calib.R:9-13, 150-193`;
  `v3_preprocess.R:18-32`.
- Stream inventory: grep of `seed_stream`/`RngSource` in the core — only `cpp/v3_core.cpp:241` (inspection helper; its R
  caller `v3_start_draw`, `v3_setup.R:46-52`, is not on the `v3_fit` path), `:444` (final islands), `:596` (calibration
  map). Confirms (FRZ-b)(i).
- Recounted: κ_max = (m − 1) + p + 3 + 3B + (2 + 2J) (equals `W1-N1:B`'s (m − 1) + p + 3(B + 1) + (2 + 2J)); κ(c);
  exactly one `I` label per round ⇒ D_r(c) = N_e(1 + T + L + 4); Y^i_{q,ℓ} at path position σ_i⁻¹(ℓ) − 1 of the
  (T + L + q)-th `population_round`; Ẑ_t formula against `cpp/v3_engine.h:299, 316-322`.
- Strong-Markov step for a bounded stopping time; cell-wise Borel measurability; Polish value space.
- (FRZ-a) proof line by line against T12 `PROOF_v6.tex:157-162` (rectangles, λ/monotone class, ḡ measurable).
- (FRZ-b)(ii): 𝒜° reaches `v3_final_run` (`v3_fit.R:154-162`); frozen grid passed `v3_check_grid` inside `v3_frozen`;
  executed N_e = `b$tiers$N[e + 1]` ≥ 2500 and L = `b$L` ≥ 4 agree with `frozen$N`, `frozen$L`
  (`v3_cal_settings`, `v3_calib.R:9-13`).
- (FRZ-c): localised identity algebra; g for `W1-N1:F` (L3:27-39), MR Step 2 g's, D's indicator; fixed-c values from FR
  (FR-b)/(FR-c) and D:8-20; actual pair per T5 `STATEMENT.md:45-54`.
- (FRZ-d): stage-factor bounds, Z_t = Z₀Σπ₀e^{φ_t d} in the same interval, ratio ≤ C_d, Ẑ ≤ Z₀e^{d_max}, W_r ≤ C_d.
- CITECHECK.txt files read (not re-run: running `citecheck.py` writes CITECHECK.txt, which this seat may not write);
  older-step and MR ranges compared by hand (F2).

## Not checked
- The v2.2.1 → pin differences on the island path (`W1_ISL/PROOF.md:80-83`): the v2.2.1 tree is outside the inputs.
- `W3-SAMP:CC` (CC1, CC4), C1 PROOF.md, T10, T4/T7 proofs: not in the inputs; used only as cited.
- Binary64 / 2⁻⁵³ effects (excluded by EX-A, H-U, as the items state).
- Lean targets.

COUNCIL-VERDICT round=R1 manifest=0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea seat=opus score=8.1 gates=FAIL
