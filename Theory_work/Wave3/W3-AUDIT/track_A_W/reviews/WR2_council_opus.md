# WR2 — council diff round, seat `opus` (Claude Opus 5.5, high) — W3-AUDIT track A_W: W1 (ISL), W2 (FRZ)

Manifest: `MANIFEST d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e`; `manifest.py verify` → `verify: OK`
(run 2026-11-17 from `/home/fb31/BVS-wt/W3-AUDIT`). Core: `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` → identical.
Frozen-text hashes in both `CHECK.md` (W1 STATEMENT `2edc44e5d34b`, PROOF `4007223544d9`; W2 STATEMENT `c94e45ae1477`,
PROOF `7d3b84fa8739`) equal the manifest lines.

## Verdict summary
Both W-R1 F findings are resolved. F1: W1 now states and proves normal termination of the island program
(`W1_ISL/STATEMENT.md:46`, `W1_ISL/PROOF.md:43-50`). W2 now has a "No error exit" paragraph
(`W2_FRZ/PROOF.md:40-47`) that covers the `v3_final_run` prelude, the pre-island C++ sites, and islands 1, …, r. I read
each cited site at the pin and each argument is correct. F2: I re-read every corrected locator against the cited file,
and each one now lands on the named step. I also ran the citation check in memory: it reproduces both saved
`CITECHECK.txt` byte-for-byte (79/0 and 43/0). E1–E7 and Sol E1 are resolved. The diff introduces no C, S or F defect. I
found eight new E findings, all non-blocking: the enumeration in W2's new paragraph is incomplete, one locator is
missing, two premises are attributed to the wrong source, one bullet is misplaced, a changelog tag is incomplete, and
two statuses cannot be checked. **gates=PASS.**

## 1. W-R1 findings
| finding | verdict | resolving line(s) |
|---|---|---|
| Opus F1 (exception exits not excluded) | **RESOLVED** | W1: `W1_ISL/STATEMENT.md:46` (ISL-0 "ends normally … for every u ∈ Υ"); `W1_ISL/PROOF.md:43-50` (scorer `NumericalFailure` `v3_score.h:237` excluded by EX-A + valid input; `\|S\| > K` `v3_score.h:230` excluded by Gibbs add only when \|S\| < K `v3_engine.h:115-116`, swaps size-preserving, π₀ ∈ Ω by T6 (S); `nth_nonmember` `v3_engine.h:143` excluded via `:151`; `draw_pi0` categoricals; IDEAL-W/MACH for allocations and int ranges, now a setting premise `W1_ISL/STATEMENT.md:33-34`). W2: `W2_FRZ/PROOF.md:40-47` (prelude `v3_check_seed` `v3_run.R:225`, LS0 validator `v3_run.R:95-97` via T14 (REP-a), pre-island X2 sites incl. `cpp/v3_core.cpp:425` via C1, scorer `:426` under EX-A, islands < r and r via W1 normal termination + T1). Residual completeness points: N1, N2 (E). |
| Opus F2 (locators) | **RESOLVED** | Verified against the files: MR Step 2 `MR_identities.md:51-58` (`W1_ISL/STATEMENT.md:14`, `W2_FRZ/PROOF.md:59`), Step 3 `:60-62` (`W2_FRZ/PROOF.md:79`), Steps 2–4 `:51-67` (`W2_FRZ/STATEMENT.md:12`; Step 4 ends ":67 … localised form. ∎"); L1 (B-0) `:62-75` (`W1_ISL/STATEMENT.md:17`, `W1_ISL/PROOF.md:51`), (B-b) `:77-86` (`W1_ISL/STATEMENT.md:18`, `W1_ISL/PROOF.md` Step 3 end), (B-d) `:119-125` (`W1_ISL/STATEMENT.md:19`, `W1_ISL/PROOF.md` Step 4 end); L3 proof `:25-39` (`W2_FRZ/STATEMENT.md:9`; `:39` is the "∎" line). |
| Opus E1 (ledger citation) | **RESOLVED** | `W1_ISL/PROOF.md:28-29`: `cpp/v3_ledger.h:104-113`. Read at the pin: `Ledger::event` takes `S` and `ev` by const reference and the scalars by value; it writes `logical`, `fresh`, `island_best` and the stores via `offer_stores`. |
| Opus E2 (dangling changelog ref) | **RESOLVED** | `W1_ISL/STATEMENT.md:81`, `W2_FRZ/STATEMENT.md:69` → `reviews/WLC1_disposition.md` (exists). |
| Opus E3 (import statuses) | **RESOLVED** (as text) | `W1_ISL/STATEMENT.md:71-75`, `W2_FRZ/STATEMENT.md:57-62`. Whether they match the registry verbatim is not checkable here: N7. |
| Opus E4 (𝓒° value space; tier) | **RESOLVED** | `W1_ISL/STATEMENT.md:30-33` (E contains ⊥ and non-"ok" records; (T, grid, tier) defined with dummy values and 𝓔-measurable; tier ∈ {0, 1}); `W2_FRZ/STATEMENT.md:22-23`. Residual: N4. |
| Opus E5 (data integration) | **RESOLVED** | `W2_FRZ/STATEMENT.md:52-55`; cited `D_theorem.md:46-51` (integration "over 𝓒 and the data") and `W3-SAMP/STATEMENT.md:35-36` (streams 10–13 independent of the data) are correct. |
| Opus E6 (C1 PROOF reference) | **RESOLVED** | `W2_FRZ/PROOF.md:28-30`. Checked: `v3_frozen` calls `v3_check_grid(grid)` at `v3_run.R:70`; `v3_calibrate` calls `v3_frozen` at `v3_calib.R:186` without `tryCatch`, and `v3_fit.R:150` calls `v3_calibrate` without one, so a grid failure there is an error and the fit is not on 𝒜°. |
| Opus E7 (finiteness of d) | **RESOLVED** | `W2_FRZ/PROOF.md:77-78`: valid input (n ≥ 3, a retained column, non-constant y) gives m > 0, so the `NEG_INF` branch (`cpp/v3_score.h:223`) is not taken. |
| Sol E1 (MR locators) | **RESOLVED** | = F2 rows above. |

## 2. Diff-hunk verdicts (`reviews/DIFF_WR1_to_WR2.patch`)
| file / hunk | verdict | note |
|---|---|---|
| `API_CARD/README.md` (cost line) | OK | Cost estimate only, no claim; outside W1/W2 content. |
| `W1_ISL/CHECK.md` (status, hashes, rows 6–7) | OK | Hashes equal the manifest; citation count 79 matches the in-memory re-run. |
| `W1_ISL/CITECHECK.txt` | OK | In-memory re-run of `citecheck.py` reproduces it byte-for-byte (79 citations, 0 bad). |
| `W1_ISL/PROOF.md` header v1.2 | OK | — |
| `W1_ISL/PROOF.md` ledger sentence (`:28-29`) | OK | Matches `cpp/v3_ledger.h:104-113` (see E1). |
| `W1_ISL/PROOF.md` *Normal termination* (`:43-50`) | OK, E (N3) | Every throw site in the island program at the pin is covered. I grepped `throw`/`stop(` in `cpp/*.h`: the only throws reachable from `run_island` are `v3_score.h:230, 237` and `v3_engine.h:143`. The `start_mode` throws `v3_start.h:261, 272` are LS0-only, after the islands. Each exclusion argument is correct: Gibbs `add_ok = in \|\| \|S\| < K` (`v3_engine.h:116`); `⌊u(p − k)⌋ ≤ p − k − 1` for u < 1 under EX-A and k < p (k = p is the self-loop `:148`); `cumulative_from_logs` sets the tail to exactly 1 from the last positive-mass category (`v3_start.h:23-34`), so `upper_bound` with u < 1 stays in range on rows with positive mass, which T6's exactness supplies on reachable rows; `resample` clamps its index (`v3_engine.h:237-258`). "S.2's EX-A argument" has no locator: N3. |
| `W1_ISL/PROOF.md` (B-0) / (B-b) / (B-d) locators | OK | Verified (F2). |
| `W1_ISL/STATEMENT.md` header | OK | — |
| `W1_ISL/STATEMENT.md` "Steps under check" locators | OK | Verified (F2). |
| `W1_ISL/STATEMENT.md` setting (`:30-34`) | OK | tier ∈ {0, 1} holds on 𝒜° (`v3_calib.R:149, 155, 158`: e starts at `tier = 0` and is set to 1 at most once). The IDEAL-W/MACH wording matches T4 ENC `:24` and T14's quote of IDEAL-W. |
| `W1_ISL/STATEMENT.md` (ISL-0) normal termination (`:46`) | OK | The proof (`PROOF.md:43-50`) covers it under the setting's EX-A, IDEAL-W and MACH. It claims nothing more than is proved. |
| `W1_ISL/STATEMENT.md` "Inputs reused" (`:71-75`) | OK, E (N7) | Registry text not in the inputs. |
| `W1_ISL/STATEMENT.md` changelog v1.2 | OK, E (N6) | Tag omits STRONGER for the new normal-termination conclusion. |
| `W2_FRZ/CHECK.md` | OK | Hashes equal the manifest; citation count 43 matches the re-run. |
| `W2_FRZ/CITECHECK.txt` | OK | In-memory re-run reproduces it byte-for-byte (43 citations, 0 bad). |
| `W2_FRZ/PROOF.md` header v1.2 | OK | — |
| `W2_FRZ/PROOF.md` (FRZ-b)(ii) E6 replacement (`:28-30`) | OK | See E6. |
| `W2_FRZ/PROOF.md` *No error exit* (`:40-47`) | OK, E (N1, N2, N5) | Checked against the code at 4676af6. `v3_run.R:225` = `v3_check_grid(...); v3_check_seed(seed)`. `v3_check_seed` (`v3_preprocess.R:7-11`) passes for an integer in [1, 2³¹ − 1]. The LS0 validator is `v3_run.R:95-97` (`le` ← `getOption("v3.ls0_ell", b$ell)`; it stops unless `le` is numeric, length 1, finite, whole and in [0, 10⁶]). With the option unset, `le` = `b$ell` = ⌈log₂(n + p + 1)⌉ (`v3_preprocess.R:24`), and T14 (REP-a) gives ≤ 32 and "the other conditions of that validator hold". The pre-island sites are `cpp/v3_core.cpp:393` (`setup required`); `models_from_R` → `to_internal` stops (`:29-35`); `phase_index`/`mech_index` stops (`:54-55`) on the provenance path; `:425` (size stop); and `:426` (scorer). All are X2-class (C1 STATEMENT:29-31, 45-48, 54-55) or excluded by EX-A. The `NumericalFailure` catch `:483` is not entered. Islands: W1 normal termination; `partial` is set only by the guard, which is FALSE in P° (T1). The C1 citation supports the conclusion through (C1-c) ("D2 and the X2 class are unreachable") as much as through (C1-b); this is acceptable. |
| `W2_FRZ/PROOF.md` MR Step 2 / Step 3 locators; E7 (`:59, :77-79`) | OK | Verified. |
| `W2_FRZ/STATEMENT.md` header; "Steps under check" locators | OK | Verified (F2). |
| `W2_FRZ/STATEMENT.md` setting (`:22-24`) | OK, E (N2, N5) | The premises are stated, but the "W1's setting, incl. a valid declared seed" attribution is wrong (N5), and the configuration premise is narrower than T14/C1's code of record (N2). |
| `W2_FRZ/STATEMENT.md` "Not claimed": data integration (`:52-55`) | OK | Locators correct; scope matches what D (D-iii) needs. |
| `W2_FRZ/STATEMENT.md` "Inputs reused" (`:57-63`) | OK, E (N4b, N7) | Line 63, "Binary64; interrupted runs (T1 GW)", was a "Not claimed" bullet and now sits under "Inputs reused" (N4b). |
| `W2_FRZ/STATEMENT.md` changelog v1.2 | OK | — |

## 3. New findings (all E; none blocks)
- **N1 (E; W2 `PROOF.md:40-46`) — the error-exit enumeration is incomplete.** These sites are not named:
  - `stopifnot(inherits(setup, "v3_setup"), inherits(frozen, "v3_frozen"))` (`v3_run.R:224`). It is true on 𝒜°: `frozen` comes from `v3_frozen`.
  - `get_holder`'s stop (`cpp/v3_core.cpp:18`), via `get_holder(setup)`, `:392`.
  - The implicit Rcpp conversions of `ro` (`:396-404`).
  - The code *between* islands: `island_to_list`, `hex64` (`:447-450`).

  Each is an X2-class or implicit-error site that C1 (C1-a)/(C1-b) lists as unreachable on valid internal state, or is
  covered by MACH. The conclusion therefore stands. *Repair:* change "Inside `cpp_final_run` before the islands" to
  "before and between the islands", and add "and every other X2-class / implicit-error site (C1)".
- **N2 (E; W2 `STATEMENT.md:23-24`, `PROOF.md:41`) — the configuration premise is narrower than the imports' code of
  record.** "Default configuration (`v3.ls0_ell` unset)" leaves out options that T14 also requires unset (`v3.ls0`,
  `v3.ls0_cap`) and that C1 also requires unset (also `v3.grid_fallback`, `v3.ls0_tie_dp`). Of these, only `v3.ls0_ell`
  affects the validator: `v3.ls0 = FALSE` skips it, and the others do not enter `le`. The pre-island X2 sites do not
  depend on any of them, so the use is sound. *Repair:* write "the shipped default configuration (options as in
  T14/C1)", or add one clause saying why the other options do not matter before island r.
- **N3 (E; W1 `PROOF.md:50`) — "S.2's EX-A argument" has no locator.** It presumably means `C-DLV:L2` step S.2, which is
  not among the inputs. The paragraph gives its own EX-A argument, so the reference is only corroboration. *Repair:*
  give the full ID and path, or delete it.
- **N4 (E; W2 `PROOF.md:31`) — (FRZ-b)(ii) does not check the new condition tier ∈ {0, 1} for "𝓒° ∈ A_s".** v1.2 added
  this condition to A_s. It holds: e ∈ {0, 1} at `v3_calib.R:149, 155, 158`, and `b$tiers$N[tier + 1]` ≥ 2500 is not
  NA. *Repair:* add "tier = e ∈ {0, 1} (`v3_calib.R:149-158, 186`)".
- **N4b (E; W2 `STATEMENT.md:63`) — misplaced bullet.** "Binary64; interrupted runs (T1 GW)" now sits under "Inputs
  reused" instead of "Not claimed". The lemma's scope is unchanged (the setting has EX-A and the potential run). *Repair:*
  move it back above `## Inputs reused`.
- **N5 (E; W2 `STATEMENT.md:23`, `PROOF.md:40-41`) — the seed premise is attributed to W1.** "Valid input (W1's setting,
  incl. a valid declared seed)": W1's setting does not mention the seed. The premise is in fact redundant on 𝒜°:
  `v3_calibrate` already ran `v3_check_seed(seed)` (`v3_calib.R:146`) on the same `seed` that `v3_fit` passes to
  `v3_final_run` (`v3_fit.R:150, 162`). *Repair:* cite that instead, or state the premise as W2's own.
- **N6 (E; W1 `STATEMENT.md:82`) — the changelog tag is incomplete.** v1.2 adds a conclusion to (ISL-0) (normal
  termination), which is STRONGER, besides the WEAKER premise. *Repair:* tag "STRONGER (ISL-0 normal termination) /
  WEAKER (execution premise) / EQUAL (locators)".
- **N7 (E; G4, not checked) — registry statuses.** I could not compare the quoted statuses ("PROVED-CHECKED; council R2",
  main 029bb748) with the registry, which is not in the permitted inputs. Two file headers differ on the surface:
  `track_A_X/T14_REP/STATEMENT.md:1` reads "STATEMENT v1 (DRAFT, …; not locked)" and T6's reads "(draft, not locked)".
  This is presumably registry-after-council versus a stale file header. The recording package should confirm it.

## 4. Gates (applied to the changed content)
| gate | result | basis |
|---|---|---|
| G1 correctness of every step and code citation | PASS | Every new argument was checked at the pin. All corrected locators land on the named text. Citation check re-run in memory: 79/0, 43/0, identical to saved. |
| G2 hypotheses used = stated | PASS | EX-A, IDEAL-W, MACH, valid input/seed, default configuration, T14 (REP-a), C1, T1 and T6 (S) are each stated in the setting or cited (N2, N5 are wording). |
| G3 no hidden assumptions | PASS | The F1 gap is closed. The remaining unnamed sites are covered by the cited C1/MACH (N1). |
| G4 imports and statuses verbatim | PASS | Imports are quoted correctly where I could check them (T14 (REP-a), C1 (C1-b)/(C1-c), T6 (S), D, MR, L1, L3). Registry statuses were not checked (N7). |
| G5 scope | PASS | Potential pair kept. Data integration is now excluded explicitly. The misplaced bullet (N4b) does not widen scope. |
| G6 fidelity to code, older steps, consumers | PASS | Code read at 4676af6. Older-step and consumer locators are corrected and verified. |

## 5. Claims
| id | decision |
|---|---|
| W1 (ISL) v1.2 | ACCEPT |
| W2 (FRZ) v1.2 | ACCEPT |

## Score
**9.3 / 10** (C, S and F only: none held. The deduction reflects that W2's new no-error-exit paragraph closes F1 partly
through an unenumerated class citation, N1.)

## Checks performed
- `manifest.py verify` on MANIFEST_WR2 → OK. Core = 4676af6. `CHECK.md` hashes match the manifest.
- Read `BRIEF_WR1_opus.md`, both W-R1 reviews, `WR1_disposition.md`, the full diff, both `CHECK.md`, T14 STATEMENT,
  C1 STATEMENT, and the current W1/W2 STATEMENT and PROOF around every hunk.
- Code at the pin:
  - `cpp/v3_score.h:215-237`
  - `cpp/v3_engine.h:105-192, 236-258`
  - `cpp/v3_start.h:1-40, 150-175`
  - `cpp/v3_ledger.h:85-113`
  - `cpp/v3_core.cpp:385-500`
  - `v3_run.R:60-110, 210-228`
  - `v3_preprocess.R:7-32`
  - `v3_calib.R:144-189` (grep-located lines)
  - `v3_fit.R:140-174`
  - a grep of every `throw` / `stop(` in `cpp/*.h` and `cpp/v3_core.cpp`
- Locators read in `L1_bridge.md:60-127`, `MR_identities.md:49-70`, `L3_freezing.md:23-42`, `D_theorem.md:44-52`, and
  `W3-SAMP/STATEMENT.md:33-37`.
- `citecheck.py` re-run in memory, with the file write intercepted in a scratch script outside the repository. Its
  output equals both saved `CITECHECK.txt`. No repository file was written except this one.
- Disclosure: a `grep` for `IDEAL-W|MACH` across `track_A/T*/STATEMENT.md` also printed matching lines from T2 BLK, T9
  and T10 STATEMENTs, which are outside the permitted inputs. I did not rely on them: the IDEAL-W/MACH reading rests on
  T4 ENC `:24` and T14's quotation.

## Not checked
- Registry statuses (N7). C1 PROOF / T10 §2 (the per-site invariants behind (C1-b)). `C-DLV:L2` S.2.
- Binary64; Lean targets. Unchanged text that Sol accepted at W-R1, except where a change touches it (N4).

COUNCIL-VERDICT round=R2 manifest=d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e seat=opus score=9.3 gates=PASS
