# R1 council review — seat `opus` (Claude Opus 5.5, high) — W3-AUDIT track A, batch T1–T10 — blind first read

Content reviewed: the frozen round R1, `MANIFEST 01c268b030c3f12619fe885edc02483d0516038ee4e53e66b8840b14b383bc2b`
(`manifest.py verify` → OK, run at the start of this review). The core `Scripts/SMC_BVS/core/` in the worktree is
identical to the method pin 4676af6 (`git diff --quiet 4676af6 -- Scripts/SMC_BVS/core` and `… 4676af6 HEAD …` both
clean). Files read: the twenty `T*/STATEMENT.md`, `T*/PROOF.md`, `T1_GW/CITECHECK.txt`, `citecheck.py`, every file of
the pinned core (all `*.R` and `cpp/*`), and the cited lines of every external input in `reviews/INPUTS_R1.txt`. No
`INDEX.md`, `CHECK.md`, `LOG.md`, `CHECKPOINT*.md`, other `reviews/` file or file outside `track_A/` was opened.

## Verdict summary

I read every claim against the code at the pin myself and tried to break each one. I found no wrong step, no
unstated load-bearing hypothesis and no unfaithful code citation, so I have no C, S or F finding. All ten items can be
accepted as checked. The code readings are accurate line by line. I re-derived the following:
- T1: the complete list of guard sites and clock reads, the stop-only property, the side-by-side induction for P°, and
  𝒜 = 𝒜° ∩ G.
- T2: the cut-and-pack partition invariant and B ≤ K.
- T3: that LS0 executes on every completed run, and the cache-hit/offer argument.
- T4: every N3 (H1) field and the strengthening.
- T5: which streams exist and the bounded-computation measurability argument.
- T6: the telescoping in Claim S.
- T7: detailed balance for the four kernels and the Fisher–Yates bijection.
- T8: the elementary limit.
- T9: E = 𝒜*, the greedy invariant, and the cost and storage bounds.
- T10: the exit map, D2, X9, the X7/X8 bound, and the D1 fallback argument.

A brute-force port of `build_start`/`draw_pi0` and `mode_dp`/`mode_tie_dp` agrees with exact enumeration on 400 random
small instances, 150 of them with ties. My six findings are all editorial (E):
- an arithmetic premise that should be stated in T10's claim header;
- a derivation route in T8's "Consequence" paragraph, which reaches the correct 𝒜° bound through W3-SAMP's
  actual-𝒜 form;
- the ambiguous word "executed" in T8;
- version labels;
- an unlisted non-guard interrupt point in T1;
- statuses quoted in T3/T8 whose recording source is not among the R1 inputs.

## Gate table

| gate | result | justification (what I re-derived or re-read) |
|---|---|---|
| G1 correctness | PASS | Every step was re-derived against the pinned code. T1: all (C1)–(C3) sites by grep of `check(`, `preflight`, `runtime`, `Clock::now`, `secs_since`, `proc.time` (no site missing); `RuntimeGuard` holds no engine, ledger or stream pointer; status assignments only at `cpp/v3_core.cpp:413, 451, 459, 480, 484`; post-fire R paths error-free (`fail`, `vapply(…, 0)` with an integer, NULL island slots, `v3_fit.R:163-173`). T2: tree/cut/pack invariant (incl. `best[i]` always active, `:93, 99-103`). T3: CC2's cache-hit argument, including the `emit = false` centre at `:456`. T6: telescoping ∏ F_b(s_{b−1})/F_{b+1}(s_b) = 1/F_J(k). T7: four detailed-balance identities. T9: d_b-slack telescoping and the greedy invariant. T10: D2, X7 ≤ 32, X8 ≤ 2³⁰+31, pilot-schedule monotonicity. Brute-force check of T6 (S),(Z) and T9 (TDP-b,c,e) under exact rationals: 400 instances, all pass. |
| G2 hypotheses used = stated | PASS | EX-A/H-U appear wherever used (T6 setting, T7 setting, T1–T5 headers). T3's use of T1 (GW-v), T5's use of T1 (GW-i, GW-iv), T8's use of T5 (CAL-b,c,d) and T10's use of T4/T9 are named in the text. |
| G3 no hidden assumptions | PASS | Checked: measurability (T1 "Not claimed" outer-probability clause; T5 Step 3 bounded computation); ranges of n, p (T2 n ≥ 3 from `v3_preprocess.R:106`; T10 R-representability via `cpp/v3_core.cpp:92`); no binary64 fact used under EX-A without saying so (T2 and T10 binary64 remarks are marked as remarks). E1 asks for T10's claim header to state the inventory's arithmetic premise explicitly, but the dependency is already named ("under T4 ENC"), so I record no S finding. |
| G4 imports and statuses | PASS | Quotations re-read at the cited lines: TLF:74, 86; W1-N1:29-31, 70-79, 83-88; W3-SAMP:35, 39-41, 64-67, 76-83, 102-105, 118-124, 182; W3-RM:41-48, 53-63, 168-169, 219-222; W3-RM2:57, 217, 248, 254; C-GROW:57, 65-71; CC_code_check status and CC2/CC7; D_theorem status and :50-54; PC:10-20; L5_assembly:11-16, 44-45; W1-N3:56-57, 78-82, 92-98; TDP_E:1-64; C-DLV STATEMENT:38-42, 52-53, REPORT:70, INVENTORY:15-93, L2:37-72, L4:79-93; W2-UNI L5:12-13; W3-START:185; L10:14-15; START2-R:208-246; START2:181-189; T12:23-31, 48; N9 REPORT:15-26, 64-66. All quoted correctly. Statuses I could not trace within the inputs are listed under E6 and "Not checked". |
| G5 scope and constants | PASS | B ≤ min(16, K); J ≥ ⌈p/B⌉; D_r ≥ N₀(L+6) ≥ 10n; X7 bound ℓ ≤ 32; X8 cap ≤ 32 + 2³⁰ − 1 < INT_MAX; T9 operation bound O(p·(Σ_b(K+1)(t_b+1) + max_b 2^{|C_b|})), storage O(Σ_b 2^{|C_b|} + J(K+1)), fast path O(min(|E|, cap)·(J(B+2) + p log p)) (each internal DFS visit has a leaf below, ≤ J ancestors per leaf); T5 uniform-count bound (≤ 1 + 2J per π₀ draw, m − 1 order uniforms). "For every input" quantifiers match the code paths. |
| G6 fidelity to the code as coded | PASS | Shipped configuration traced from `v3_fit.R:73, 114, 151` and `v3_run.R:88-104` into `cpp_final_run` `:400-404`. Line-identity claims checked with `git diff 39db138 4676af6`: `v3_start.h` first hunk at line 178 (T6), engine only hunk at 374 and none in `v3_blocks.h` (T7). The `Start`, `Data` and neighbour graph are the objects built in `cpp_setup` and are read only through `const` afterwards (T4 ENC-b confirmed for `cpp_cut_group`, `cpp_cal_V`, `cpp_final_run`, `ingest_tables`, `start_summary`). |

## Per-claim table

| id | decision |
|---|---|
| T1 GW (GW-i)–(GW-v) | ACCEPT |
| T2 BLK (BLK-a)–(BLK-c) | ACCEPT |
| T3 OPC (OPC-a)–(OPC-d) | ACCEPT |
| T4 ENC (ENC-a)–(ENC-c) | ACCEPT |
| T5 CAL-C (CAL-a)–(CAL-d) | ACCEPT |
| T6 START-X (Z), (S), (S′) | ACCEPT |
| T7 KER (KER-a)–(KER-d) | ACCEPT |
| T8 OVL (OVL-a)–(OVL-d) | ACCEPT |
| T9 TDP (TDP-a)–(TDP-e), TDP-IMPL discharge | ACCEPT |
| T10 P1′, S.3′, D1 | ACCEPT |

## Findings

**E1 (T10, claim header lacks the arithmetic premise)** — `T10_P1S3/STATEMENT.md:20-33`.
- Problem: the claim says only "On valid declared inputs". Two parts of S.3′ rest on arithmetic premises:
  - X9's root check "passes by T9 TDP-e, under T4 ENC"; T4 is an EX-A statement, and TDP-e alternatively needs
    TDP_E's (H2-FP).
  - C5 is classed "EX-A: never".
- The C-DLV inventory itself is stated under the (d)-premises EX-A, IDEAL-W and MACH. The dependency is named through
  T4, so this is not an unstated hypothesis, but the claim should carry it.
- Further, in binary64 `mb` is never NaN and `M[J][0] = 0`, so X9 is in fact unreachable without (H2-FP) as well. If
  wanted, one sentence can record that.
- Repair: open the Claim with "Under the inventory's (d)-premises EX-A, IDEAL-W, MACH (for X9 alternatively TDP_E's
  (H2-FP)), on valid declared inputs: …".

**E2 (T8, Consequence for (D-iv) reaches the 𝒜° bound through W3-SAMP's actual-𝒜 form)** —
`T8_OVL/STATEMENT.md:49-51`, `T8_OVL/PROOF.md:96-99`.
- Problem: the PROOF writes (D-iii) with the actual 1_𝒜 and then bounds 1_𝒜 ≤ 1_𝒜°. T5's own flag paragraph
  (`T5_CAL/STATEMENT.md:45-54`) says W3-SAMP's conditional arguments are valid for the potential pair (𝒜°, 𝓒°). The
  actual 𝒜 depends on the clock through G, so it is not in σ(𝓒), and (D-iii)'s step E[1_𝒜 P(·|𝓒)] is not directly
  available for it.
- The final inequality, with 1_𝒜°, is correct.
- Repair: write the chain as
  P(completed ∩ {Ŝ ≠ S₀}) ≤ P(𝒪° ∩ {Ŝ° ≠ S₀}) (T1 GW-iv, pathwise)
  ≤ P(S† ≠ S₀) + E[1_𝒜°(1 − π₀(S₀))^{D_r}] ((D-iii) for the potential run, T5 CAL-b),
  and drop "with 𝒜 ⊆ 𝒜°" from the STATEMENT line.

**E3 (T8, "executed N_e, T, L")** — `T8_OVL/STATEMENT.md:28-29` (and the OVL-b last sentence, `PROOF.md:78-79`).
- Problem: on 𝒜° ∖ 𝒪 an actual final-run guard stop can execute fewer than T stages. D_r in P-OVL and in the proof is
  the frozen budget: N_e, T and L of 𝓒°'s frozen object, and the T of the potential, uninterrupted run.
- Repair: replace "executed" by "frozen (those of 𝓒°, i.e. of the uninterrupted run)".

**E4 (version labels)**
- `T1_GW/PROOF.md:1-5`: the header says v5 but lists transitions only up to v3 → v4. Add "v4 → v5: SL1LC2 #1 applied".
- `T2_BLK/STATEMENT.md:71-73`: the v5 changelog row sits above the v4 rows.
- `T3_OPC/STATEMENT.md:1` (v2) vs row v2.1 at `:65`, and `T9_TDP/STATEMENT.md:1` (v2) vs rows v2.1 at `:52`: the
  headers are not bumped.
- `T10_P1S3/PROOF.md:1` says v2.1, but §2's exact X7/X8 bound is STATEMENT v2.2 content (`T10_P1S3/STATEMENT.md:52`).

**E5 (T1, a non-guard interruption point)** — `T1_GW/STATEMENT.md:25-32`.
- Problem: "the complete list" of operational checks omits `Rcpp::checkUserInterrupt()` in exact enumeration
  (`cpp/v3_core.cpp:552`). It is not a guard and has no Boolean, and a user interrupt ends `v3_fit` with an R error, so
  the run has no fit object and is outside 𝒪. It is covered by MACH/INVENTORY X4 and no clause is affected.
- Repair: add one line under "Not claimed" (signals and user interrupts, including `:552`: MACH).

**E6 (statuses not traceable within the R1 inputs)**
- `T3_OPC/STATEMENT.md:53` quotes W3-RM:E4 as "PROVED-CHECKED". The W3-RM STATEMENT records statuses at `:251-259`,
  not E4's.
- `T8_OVL/STATEMENT.md:13, 35` quote IF-START as "PROVED-CHECKED; council R2, …" and W3-START2-R:OVL as
  "PROVED-CHECKED". The cited `W3-START2-R/STATEMENT.md:14` "asserts no proof status".
- The quotes are presumably from the registry, which is not an R1 input.
- Repair: cite the source line of each status (registry row or REPORT line), so that G4 can be checked verbatim.

## Overall score

**9.1 / 10.** No C, S or F finding. The batch is careful, the code citations are exact, and the re-checks of
N9, TDP_E and [OP] add real content. I take nothing off for E findings.

## Checks performed

- Manifest verified; core = pin (two `git diff --quiet` checks). Read every file of `Scripts/SMC_BVS/core/`.
- I computed the R line offsets myself and checked every R and C++ line citation I relied on against those offsets.
- Greps over the core:
  - every `stop`/`stopifnot`/`throw`/`checkUserInterrupt` (completeness of T10's exit map);
  - every clock, guard and option use (completeness of T1's (C1)–(C3) list and of Step 1);
  - every `RngSource`/`seed_stream`/`vs->u` site (T1 Step 1, T5 Step 1).
- Traced all post-fire R paths for an error-free return (`fail`, `v3_calibrate` after a stop, `v3_assemble_final`
  incomplete branch, `v3_fit.R:163-173`, `finish`).
- Re-derived:
  - T2 (BLK-b) for an arbitrary full binary tree;
  - T6 (S) and (Z);
  - T7 detailed balance for each kernel;
  - T9 E = 𝒜*, the greedy invariant (TDP-b) and TDP-e;
  - T9 cost and storage;
  - T10 D2, X7, X8 and D1, including the pilot-schedule monotonicity in binary64.
- `git diff 39db138 4676af6` for the T6/T7 line-identity claims.
- Brute-force script (scratchpad, outside the repo; exact rationals, the multiplicative form of the log-additive code):
  the exact law of `draw_pi0` equals γ₀/Z̄₀, Z̄₀ by convolution equals Σ_Ω γ₀, and `mode_dp`+`mode_tie_dp` return k* and
  S* (smallest size, then lex-min maximiser), on 400 random instances (p ≤ 7, ties in 150).
- Re-read every cited excerpt of the R1 external inputs listed in the G4 row.

## Not checked

- Statuses recorded only in registry tables or REPORT files outside `INPUTS_R1.txt`:
  - W3-RM:E4 "PROVED-CHECKED";
  - W3-START2-R:IF-START "PROVED-CHECKED; council R2, …";
  - W3-START2-R:OVL "PROVED-CHECKED";
  - `A:BLOCK-LE-16` at `assumptions.tsv:15`.
- The internal proofs of imported results:
  - IF-START, OVL⁺, W3-SAMP D and CC, N3, C-DLV L3 Lemma 3.4 are taken as cited;
  - T10's D1 argument for the "last successful construction" branch uses L3 Lemma 3.4, which I checked against
    `build_grid` only in outline.
- `AUDIT.md` §4/§6 (not an input) for the meaning of "(A5)" beyond T8's own definition.
- Binary64 quantitative statements (N9 §5); I did not compile or run the C++.

COUNCIL-VERDICT round=R1 manifest=01c268b030c3f12619fe885edc02483d0516038ee4e53e66b8840b14b383bc2b seat=opus score=9.1 gates=PASS
