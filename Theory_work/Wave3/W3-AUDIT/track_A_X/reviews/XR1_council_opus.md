# XR1 council — seat `opus` (Claude Opus 5.5, high) — blind first read — W3-AUDIT track A_X: X1, X3, X5, T14

Manifest: `MANIFEST 0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c`. Verified before reading with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_X Theory_work/Wave3/W3-AUDIT/track_A_X/reviews/MANIFEST_XR1.txt`
→ `verify: OK` (including the four EXT core files). `git diff --quiet 4676af6 -- Scripts/SMC_BVS/core` → the core is the pin.
Blind read: I did not open `INDEX.md`, `LOG.md`, any `CHECK.md`, `H5_CARD_DRAFT.md`, or any other file in `reviews/`
except my brief and `INPUTS_XR1.txt` (and `MANIFEST_XR1.txt` for the hash).

## Verdict summary
- **X1 (T12 FR at the pin): ACCEPT.** I re-read every cited engine line at the pin and re-derived T12's bridge identity,
  invariance-by-prefix, resampling mean, round mean, induction C_t, the post-terminal step and (ii). No error found. Two
  editorial points (E1, E2).
- **X3 (L1a′ line check, VERIFIED): ACCEPT.** I re-derived the changed step (variational bound on Q^c_T), the exponent
  chain of [P1] `lem:den` with R_n → ρ, E Λ′_n ≤ C′_Λ, the assembly via `thm:Ta`/`lem:num`/`thm:T01iii`, the Markov
  split and the m = m^T_n(ω) consequence. All correct. One editorial point (E3).
- **X5 (PoolZ, VERIFIED WITH AMENDMENTS): ACCEPT.** The four steps are right, and (X5-b) is a correct, needed precision
  (the conditioning needs CAL, so it works for (𝒜°, 𝓒°)). Three editorial points (E4–E6).
- **T14 (REP): REJECT as written; the claim itself is true.** The arithmetic and the code reading are right. But the
  proof bounds |S̃₀| ≤ K by citing T9 (TDP-a)/(TDP-b), which hold only under EX-A and (H2-FP). T14 states neither, and its
  conclusion says only R's `dim` limit and the option values are used (F1, G2/G3). A short structural argument closes the gap
  without those premises (repair below). Two editorial points (E7, E8).

## Gate table
| gate | result | reason |
|---|---|---|
| G1 correctness of every step and code citation | PASS | every step of X1/X3/X5/T14 re-derived; every load-bearing code citation read at the pin |
| G2 hypotheses used = stated | **FAIL** | F1 (T14 uses T9 (TDP-a,b), proved under EX-A and (H2-FP), without stating them) |
| G3 no hidden assumptions | **FAIL** | F1 (same: T14's "uses only R's `dim` limit and the option values" is not what the written proof uses) |
| G4 imports and statuses verbatim | PASS | quotes checked against W1-N1 STATEMENT, L1_bridge, CC_code_check, T12 STATEMENT/STATUS, L1a′, [P1], [T03R], INVENTORY:93, C-DLV:24-25; E3, E5, E8 are description-level |
| G5 scope and constants | PASS | X3 constants depend on (σ*², M, M′) only (κ = (b₊/b₋)^0.51, c_IG, c♯ checked at [P1]:58, [T03R]:76); T14 bounds ℓ_n ≤ 32, K ≤ 2³⁰ − 1 checked |
| G6 fidelity to pinned code and re-checked sources | PASS | engine/core/run/preprocess/start read at the pin; E4 (truncated source copy) is non-load-bearing |

## Per-claim decisions
| id | decision |
|---|---|
| X1 | ACCEPT |
| X3 | ACCEPT |
| X5 | ACCEPT |
| T14 | REJECT (F1; claim believed true, repair below) |

## Findings

**F1 (F; G2, G3) — T14 imports EX-A and (H2-FP) through T9 without stating them.**
`T14_REP/PROOF.md:24` bounds |m.S| by "every candidate of the enumeration and of the tie-aware fallback has size k̂, and k̂
ranges over 0..K (`cpp/v3_start.h:220-224`; T9 (TDP-a), (TDP-b))". T9 (TDP-b) is stated "under (H2-FP) as in TDP_E, and
under EX-A" (`track_A/T9_TDP/STATEMENT.md`, (TDP-b)). In particular "the fallback returns a set of size k̂" is lex_min E,
i.e. TDP-b. T14's STATEMENT assumes neither premise. Its conclusion says (`T14_REP/PROOF.md:30-31`) "The bounds use only
R's integer `dim` limit and the shipped option values", and the headline is "costs nothing on any input the software can
receive", which is a real-machine statement. As written, the hypotheses used are not the ones stated.
*Failure scenario:* a reader applies REP in binary64 without EX-A (H2-FP). The cited lemma no longer gives |m.S| = k̂.
Without some bound |m.S| ≤ K, the only bound left is |m.S| ≤ p ≤ 2³¹ − 1, and then cap_ll ≤ 2³¹ + 31 does not exclude
INT_MAX.
*Repair (no new premise needed; I checked it at the pin):* replace the T9 citation by the structural bound
|m.S| ≤ max(k̂, 0) ≤ K, valid in any arithmetic:
(1) `mode_dp` selects k̂ only from k ∈ {0..K} (`cpp/v3_start.h:220-224`), or leaves k̂ = −1.
(2) Each leaf of `rec(J, k̂)` (`cpp/v3_start.h:281-301`) has block sizes j_b summing to k̂, with codes c ∈ arg[b][j] ⊆
`codes_by_size[b][j]` (popcount j), so |S| = k̂. If no leaf is reached, `bestS` is empty.
(3) `mode_tie_dp` returns only after the root check `feasible()` passes (`:261`). Each inclusion is kept only if
`feasible()` holds with the enlarged IN. So the final IN masks fit inside a tight path whose block sizes sum to k̂, and
|S| ≤ k̂.
Hence cap_ll ≤ 32 + K ≤ 2³⁰ + 31 < INT_MAX holds with no premise. Alternatively, state EX-A and (H2-FP) as hypotheses and
drop "uses only …" and the real-machine headline. The first repair keeps the claim as the manager worded it.

**E1 (E) — X1: ledger attribution.** `X1_T12/PROOF.md:26-27` cites T1 (GW-i) for "the ledger … feed[s] no transition".
GW-i is about check bodies. For the ledger the right source is W1-N1:B (B-0) (ledger events never feed a proposal or
acceptance). At the pin `grep` shows no `vs->u`/`uniform()` in `v3_ledger.h`, so the fact holds. Cite (B-0) plus the pin
grep.

**E2 (E) — X1: list of off-path changes.** `X1_T12/PROOF.md:83-85` lists the ledger change as "`PH_LS0`". `W3-SAMP:CC`
(`CC_code_check.md:9-21`) records two ledger changes: the added `PH_LS0` and the removed registry hook. Both are off the
island path. Add the second for completeness.

**E3 (E) — X3: "in words" summary omits p ≥ 2.** `X3_L1A/STATEMENT.md:15` paraphrases L1a′ without "(any p ≥ 2)"
(`L1a_size_tail.md:10`; cf. Lemma 1a's [C1B-F3]). The claim is checked by reference, so this does not affect the verdict,
but the summary should carry the hypothesis.

**E4 (E) — X5: the verbatim source copy is cut mid-sentence.** `X5_POOLZ/SOURCE_PoolZ.md:31` ends "(iii) The identity is
about the potential". Source line 37 ends there, and Remark (iii) continues past the copied range. (X5-b)
(`X5_POOLZ/STATEMENT.md:34-35`) leans on "its Remark (iii) already says the identity is about the potential record". The
council cannot see the rest of that remark. The remark is not load-bearing; the verdict stands without it. Extend the
copy to the end of Remark (iii), or drop the attribution.

**E5 (E) — X5 vs T5 (CAL-d): wording.** `X5_POOLZ/STATEMENT.md:33` says "CAL fails … Only 𝓒° satisfies CAL (T5 CAL-b)".
T5 (CAL-d), which X5 lists as an input, ends "Hence CAL holds for 𝓒°, and for the actual record on 𝒜". The substance
agrees: the actual 𝓒 equals 𝓒° on 𝒜, but 𝒜 = 𝒜° ∩ G ∉ σ(𝓒°), so the global conditioning fails. The two sentences read as
contradicting each other. Suggested wording: "CAL fails for the actual record as a random element (its status depends on G);
on 𝒜 it equals 𝓒° (T5 CAL-d), but 𝒜 ∉ σ(𝓒°)".

**E6 (E) — X5: MEAS-J and "only under".** (a) MEAS-J is discharged by analogy ("the same bounded-computation argument as T5
(CAL-b) PROOF Step 3", `X5_POOLZ/PROOF.md:18-21`; `STATEMENT.md:29-30`). That proof is outside this council's inputs. I
find the analogy sound: data enter through Borel score, preprocessing and graph computations; the number of uniforms is
bounded on each (n, p, T, N_e, L) cell; the data space is a countable union of Euclidean spaces. Still, a one-paragraph
argument, or listing MEAS-J as a named premise, would make (X5-a) self-contained. (b) `STATEMENT.md:22-23`, "equality for
the actual 𝒜 holds only under the additional clock-independence premise", asserts more than is shown. Read "is
established only under". (c) `PROOF.md` step 3 equates R with 4. The code has `R <- length(isl)` (`v3_run.R:151`), and
this is 4 because the completed (and the potential) run executes all `islands = 4L` islands (`cpp/v3_core.cpp:443-450`).
Say so.

**E7 (E) — T14: ℓ_n range inconsistent.** `T14_REP/STATEMENT.md:28` gives ℓ_n ∈ [2, 32]. PROOF Step 2 correctly gives
[3, 32] (n ≥ 3, p ≥ 1 ⇒ n + p + 1 ≥ 5). Align the two.

**E8 (E) — T14: source line and changelog.** `T14_REP/STATEMENT.md:13`: "(19 claims)" is not in the cited
`DECISIONS.md:95`, which does mention the batch NARROW (task S4). Cite where the count comes from. T14 also has no
changelog table, unlike X1/X3/X5. Add one before locking.

## Overall score (C, S, F only)
**8.5 / 10.** No C or S. One F (T14, F1), with a short repair that keeps the claim. X1, X3 and X5 are clean at C/S/F level.

## Checks performed
- Manifest verify (OK). Core = pin 4676af6 (`git diff --quiet`).
- **X1:** read `cpp/v3_engine.h` in full at the pin: steps, `draw_order` Fisher–Yates, `one_round`, `population_round`,
  `resample` (guide table: forward/backward loops return min{k : W_k ≥ u}; denorm guard only at u = 0, P = 0 under H-U),
  `run_island(_s)` stage loop, burn-in, measured loop, `rb_acc` reset at :350 and recording at :128, `pip` at :364.
  Also `cpp_final_run` (:390-450: Hm = `measured_rounds`, stream 9 + r, `nullptr`), `v3_run_settings` (`v3_run.R:88-92`),
  `draw_pi0` uniform count (`v3_start.h:157-175`), `uniform()` ∈ [0, 1) on the 2⁻⁵³ grid (`v3_util.h:60`). Grep: no
  uniform read outside `draw_pi0` and engine steps. Re-derived T12 Lemma 1.1, 1.3, 2.1, 2.2, C_t, the post-terminal
  induction and §5 against PROOF_v6:42-153. Checked FR-a against L1_bridge (B-a)/(B-b) and CC_code_check:9-21, and the T6
  and T7 statements (H-U = iid U[0,1); KER-a/b/c). T12 STATUS:19-20 quote matches.
- **X3:** [P1] `lem:slab`, `lem:spec`(e), `lem:prior`(c) proof (:128), `lem:chi`(b), `thm:T01iii`, `thm:Ta`, `lem:num`,
  `lem:den` read in full. Re-derived ρ ≤ M + M′ (centred columns ⇒ G_T = X_TᵀX_T; y_c = Uᵀμ + ε_c). Re-derived the
  exponent chain (log u ≤ u − 1, 1/u ≥ 2 − u, R ≥ 0 so R/(2σ²u) ≤ R/(2σ²)), the bound E Λ′ ≤ C′_Λ, v_m = R^T_m ϖ(T)
  (W_K cancels), Θ^T ≤ c♯e^{Λ′}Θ^{(1)}, and the Markov/union split (needs L > c♯² for log > 0). At
  m = m^T_n(ω): ((n+1)/n)^{t/2}e^{−ω}Θ^T, and existence since R^T_K = 0. [T03R]:16-17, 76, 86-97 compared.
- **X5:** W1-N1 STATEMENT §2-3 (:55-104; CAL, SI, MEAS, localised form) read. Checked `v3_run.R:140-154` (early return
  unless completed; `R <- length(isl)`) and W3-SAMP STATEMENT:30-56. Checked T5 and T1 statements for (CAL-b, CAL-d) and
  (GW-iv). Re-derived linearity on 𝒜° and the freezing-lemma step (needs ḡ(d, c) = Z(d) for every c in the success set,
  which T12/FR gives deterministically) and the localisation via 1_𝒜 ∈ σ(data, 𝓒°).
- **T14:** `v3_preprocess.R:15-30, 97-115` (is.matrix/numeric gate ⇒ R `dim` ≤ 2³¹ − 1; n ≥ 3, p ≥ 1),
  `v3_setup.R:66-70`, `cpp/v3_core.cpp:91-103, 396-404, 462-480`, `v3_run.R:93-103`, `cpp/v3_score.h:40`,
  `cpp/v3_start.h:190-307` (mode_dp, mode_tie_dp, start_mode). Checked arithmetic: n + p + 1 ≤ 2³² − 1 ⇒ ℓ_n ≤ 32;
  K ≤ 2³⁰ − 1; cap_ll in `long long`. Checked INVENTORY:93 and C-DLV STATEMENT:24-25 against the quotes; T9 statement for
  the TDP premises.
- `citecheck.py` read. All four CITECHECK.txt files show every citation OK. I re-opened the load-bearing ones by hand.

## Not checked
- Registry rows (`Theory_work/INFRA/registry/claims.tsv:343`, SOP:TH110 status) and the "council C3 correct:PASS"
  attribution in X3: registry tables are not council inputs (INPUTS_XR1 header), so these status quotes are unverified by
  me.
- T5 PROOF Step 3 (the MEAS-J analogy target), T9/T7/T6/T1 proofs (statements only, as briefed), and T12 Lemma 1.2's four
  detailed-balance computations (taken via T7 KER-b, not re-derived).
- The original W3-READER file (only the frozen verbatim copy). L1a′ Remarks 1-5. Binary64 behaviour (excluded by every
  item).

COUNCIL-VERDICT round=R1 manifest=0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c seat=opus score=8.5 gates=FAIL
