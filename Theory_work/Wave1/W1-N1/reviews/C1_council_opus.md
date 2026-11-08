# W1-N1 · Council review C1 — Claude Opus 5.5 (effort high), layer 3

Reviewer: Claude Opus 5.5, independent council seat. Date: 2026-11-08.
Read: `Theory_work/Wave1/PROTOCOL.md`; `W1-N1/STATEMENT.md`, `PLAN.md`; `lemmas/` (all six files); `numerics/RESULTS.md`,
`BUILD.md`, `n1_exact.py`, `n1_mc.py`, `cpp/n1_harness.cpp` (MC and export modes), `cpp/instr.diff`,
`cpp/production_headers.sha256`, `json/MANIFEST.sha256`; card TH01 (`State_of_Project/sections/04_theory.tex:99-180`) and FR04
(`06_open_and_plan.tex:109-117`); T12 `STATEMENT.md` and `PROOF_v6.tex:38-180`; N9 `REPORT.md`, `PROOF.md` claim headers;
`METHOD_v3.1_FINAL.md:142,158-159`; TLF `:60-86, 109-119`; `ID_REGISTRY.md:560`; `02_method.tex` divergence boxes; production
core `v3_engine.h`, `v3_start.h:153-176`, `v3_calib.h:60-98`, `v3_score.h:250-295`, `v3_ledger.h:100-115`,
`v3_core.cpp:419-478`, `v3_run.R:70-90`. Not read (per brief): `W1-N1/LOG.md`, `W1-N1/reviews/*`.

Independent checks I ran (read-only):
- `sha256sum` of the 10 production headers = `numerics/cpp/production_headers.sha256` (all 10 match);
  `diff` production `v3_engine.h` vs `numerics/cpp/instr/v3_engine.h` = exactly the 2 read-only lines of `instr.diff`.
- Version transfer v2.1 → v2.2.1 (N9 was code-checked on `Scripts/SMC_BVS/core/cpp/` @ 39db138, N9 `REPORT.md:3`):
  `diff --strip-trailing-cr` shows `v3_start.h`, `v3_score.h`, `v3_blocks.h` identical; `v3_engine.h` differs only by the
  plain-PIP lines (`IslandResult` fields, `:352`, `:359-361`, `:370-371`); `v3_ledger.h` adds only the read-only
  `reg->insert` (`:107`).
- All 70 archived small outputs under `numerics/json/` match `MANIFEST.sha256`; spot check d6 (pilot grid, N = 2):
  max per-q residual 9.33e-15 (= RESULTS headline 9.3e-15); d5 N = 2 MC: max |z| 2.79 (= RESULTS row).
- Re-derived the N = 2 resampling recursion in `n1_exact.py:104-113` by hand (diagonal/off-diagonal terms, including the
  source-pair (y, y) case): correct.

---

## Gate verdicts

### G1 — correctness of every step: **PASS**

- **Lemma P = T12 (i.b).** `L2_post_terminal.md:26-27` is exactly T12 `STATEMENT.md:59-60` ((i.a), (i.b)); the re-derivation
  (`L2:31-45`) matches `PROOF_v6.tex:119-131` step for step (bridge `:42-52`, resampling `:100-106`, round `:108-113`,
  invariance `:54-81`). (i.b) is stated "for every c" and for the population after any post-terminal round, so the four
  measured populations are covered (`PROOF_v6.tex:131`: "covers the L′ rounds and the M measured rounds").
- **Lemma B.** Control flow verified line by line: stage loop `v3_engine.h:304-341` (increment from the *pre-resampling*
  population `:318-323`, then resample `:325-328`, then one round at φ_t `:332`); no stage-0 round; burn-in `:344-346`;
  measured `:353-357`; plain counts read after the round returns `:360`. (R2): the guide-table + forward/backward search
  (`:243-256`) returns min{k : W_k ≥ u} for u > 0 — I re-derived the bracket argument at `L1:75-80`; the `denorm_min`
  substitution (`:252`) only acts on the null event u = 0. (R3): the sequential single-stream execution is handled
  correctly by stopping times + strong Markov property of an iid sequence + chain rule over particles
  (`L1:63-91`); this delivers exactly what T12's Lemma "round" (`PROOF_v6.tex:108-113`) consumes. Uniform-count bound
  κ_max (`L1:67-69`) checked against `v3_start.h:160-170` (≤ 1 + 2J) and the four step functions (`v3_engine.h:114-193`).
  Score cache (`v3_score.h:274-293`): hit requires hash **and** model equality; eviction only causes a miss — the
  "function of S whatever the history" argument (`L1:55-58`) is right.
- **Lemma F.** Correct application of the T12 freezing lemma (`PROOF_v6.tex:157-162`, which is generic in (Υ, 𝓤), so a
  single stream is fine). The localisation via A₀ and the piecewise g that never evaluates o† (`L3:85-97`) is clean;
  joint measurability of g follows from (B-d) plus joint measurability of h.
- **Theorem N1** (`N1_theorem.md:19-25`): F → B → P → linearity over q. Correct. h ≡ 1 gives E[Ẑ_r | 𝓒] = Z.
- **Corollary E** (`E_corollary.md:53-60`): pointwise |h(S;c) − h(S₀;c)| ≤ 1{S ≠ S₀} for h ∈ [0,1]; triangle inequality;
  monotonicity of conditional expectation for the nonnegative weight 1_{E₀}W_r; N1 on the deterministic h₀. The
  S₀ ∉ Ω case (h₀ ≡ 1, δ₁ = 1) is handled. Tightness claim (h = 1{S ≠ S₀}) is correct.

No step is wrong. The proof is short because the real work is in T12 (i.b) and N9; the package correctly identifies
that only the κ ≡ m (full-round) case is needed (`R_remarks.md:1`), so the within-round prefix identity is not used.

### G2 — hypotheses used = hypotheses stated: **PASS**

Used: EX-A (exact LSE, comparisons, scores), H-U within stream 9 + r, START (R1, Z̄₀, independence proposal), KERNEL
(N9 rows 1–5), CAL + SI (independence of U_r from 𝓒), MEAS (discharged by B-d), potential run, σ(𝓒)-measurability of
(grid, N_e, L, R′), bounded jointly measurable h, worker equivalence for v3.1 only. All are in `STATEMENT.md:68-90`.
The post-lock note MP1 (`STATEMENT.md:72-74`) correctly records that only the within-stream part of EX-S and the SI
cross-stream property are used; IND-T and GUARD-W are explicitly *not* used (`N1_theorem.md:31-35`). Nothing stated is
silently dropped in a way that changes the claim.

### G3 — no hidden assumptions: **PASS** (two exposition gaps, NON-BLOCKING items 2–3)

Things I looked for and found handled: data-derived setup objects (blocks, tables, graph, B) are deterministic (no RNG in
`v3_setup.R`/`v3_preprocess.R` except the user utility on stream 200); `tier` only labels events inside `run_island`
(`v3_engine.h:279,283`) and selects N via `v3_run.R:87`; the shared cache/ledger/registry never feed a transition;
`NumericalFailure` (`v3_score.h:237`) is excluded by EX-A; u = 0 is null; the guard is stage-only (`:336-339`) and the
potential-run convention covers it; LS0 / extra c₄ search run after the islands and read no uniforms. Two implicit points
are true but not written (Engine scratch members; success-set convention) — see items 2–3.

### G4 — cited results have adequate status, copied verbatim: **PASS** (one wording item, NON-BLOCKING 5)

- T12: "PROVED-LOCKED" — verbatim from the card row `04_theory.tex` TH01 status "T12, T31(i): PROVED-LOCKED"; used for
  (i.a)/(i.b) and the freezing lemma only. Adequate.
- N9: "PROVED (candidate), code-checked"; CHK_INHERITED "VERIFIED WITH AMENDMENT" — verbatim (card status row). N9 enters
  only as the **named premises** START and KERNEL, never as a proved step; N1's conclusion is therefore "PROVED under
  START/KERNEL", which is the correct, non-upgraded reading (`N1_theorem.md:38-39`).
- TLF `:72` (EX-A) and `:86` (EX-S/IND-T) line pointers verified. TH412 is cited with its own status "PROOF SKETCH
  (NEW-SYNTH)" (`ID_REGISTRY.md:560`) only as the source of the δ₁ form, not as evidence. Seat A's reading
  (`R3_A.md:38`) is cited as a reading. Current card status "N1: PROOF SKETCH" is quoted verbatim (`STATEMENT.md:12`).
- Lemma files carry "PROVED (by this seat, unchecked)", which is conservative (protocol wording), not an upgrade.

### G5 — constants/bounds tracked: **PASS**

- Uniform Ẑ bound Ẑ ∈ [Z₀e^{min_Ω d}, Z₀e^{max_Ω d}] (`L3:92-94`), independent of c; uses Σ_t Δ_t = 1 (grid from 0 to
  exactly 1) and d(∅) = 0 so min d ≤ 0 ≤ max d; |g| ≤ B_h Z₀ e^{max d}. Same bound reused in Corollary E (`E:56-57`).
- δ₁ = 1 − π(S₀) with π(S₀) := 0 for |S₀| > K; the sharper constant δ₁ (attained) implies the card's 2δ₁. Correct.
- Numerical tolerances declared and enforced by assertion (`n1_exact.py:211-220`: residual ≤ 1e-10, |E W − 1| ≤ 1e-10,
  controls > 1e-6, round checks ≤ 1e-12); MC rule |z| ≤ 4, z_E ≤ 4. Observed: residual ≤ 9.3e-15, controls 3.2e-3–7.7e-1,
  max |z| 3.48 over 160 tests, max z_E 2.79. The floating-point vs EX-A gap is stated (`RESULTS.md:7`, `STATEMENT.md:119`).

### G6 — fidelity to the method as coded: **PASS**

Measurement point (after each complete measured `population_round`, `v3_engine.h:357-360`; the hook in the instrumented
copy sits at the same point and reproduces `pip_plain` exactly, hook diff 0 on all 20 MC runs); uniform order
(Fisher–Yates on m − 1 fresh uniforms, `:196-201`; m = p + B + 2, B identical N-labels, `:73, 211`); multinomial
resampling after every reweighting, increment from the pre-resampling population (`:318-328`); grid 0 → exactly 1
(`v3_calib.h:71,73,89-92`, also `v3_run.R:79-80` for a supplied grid); streams 9 + r (`v3_core.cpp:469`); Hm = 4,
islands = 4 (`v3_run.R:87-88`); Ẑ initialisation `:300`. v3.1's R′ = 4k on streams 10..9+R′ is spec-level and is carried
by the named worker-equivalence premise, correctly labelled. The numerical grid is "pilot-derived", not the full
production calibration path — disclosed (`RESULTS.md:9-13`) and irrelevant to an any-frozen-grid statement. The MC runs
the production `run_island` with production headers (hash-verified).

---

## Overall score: **8.9 / 10**

I would sign off on the status **PROVED** for Lemma N1 (M1(b)) and Corollary E (M1(e), with the sharper constant δ₁ ≤ 2δ₁)
**under the named premises** EX-A, H-U (within stream), START and KERNEL (N9: PROVED (candidate), code-checked), CAL, SI,
MEAS (discharged), potential run, and worker equivalence for v3.1's R′ > 4 — cross-family checked conditional on the Sol
seat. The status string should keep the premise qualifier and the inherited N9 status visible; it must not read as an
unconditional PROVED for the shipped floating-point code or for delivered (non-potential) runs.

Why not higher: the code bridge leaves a few true-but-unwritten steps (items 1–3), and the v2.1 → v2.2.1 transfer of the
N9 code-check is asserted rather than recorded. None affects correctness; I verified each myself.

---

## Remaining issues

**BLOCKING:** none.

**NON-BLOCKING**

1. **Record the N9 code-version transfer.** N9 was code-checked on `Scripts/SMC_BVS/core/cpp/` @ 39db138
   (`N9-KERNEL/REPORT.md:3`), but KERNEL/START are applied to the v2.2.1 frozen core. `STATEMENT.md:54-55` asserts only
   that the *engines* differ by the plain-PIP lines; KERNEL/START also rest on `v3_start.h` (Claims S, Z), `v3_blocks.h:170`
   (graph symmetrisation) and `v3_score.h`. *Fix:* add one paragraph to `L1_bridge.md` ("Code version") stating the
   `diff --strip-trailing-cr` result: `v3_start.h`, `v3_score.h`, `v3_blocks.h` identical; `v3_engine.h` differs only at
   `:39-40, 352, 359-361, 370-371` (plain-PIP, write-only); `v3_ledger.h` adds the read-only `reg->insert` (`:107`); note
   that N9's line numbers are v2.1 numbers (engine lines ≥ 40 shift by +1 or more).

2. **(B-0) should cover Engine member state shared across islands.** The single `Engine E` (`v3_core.cpp:435`) is reused
   for all islands; its members `tmpQ`, `scratch`, `rb_acc`, `rb_on`, `ms`, `ev` persist. They are harmless (`tmpQ` is
   read in `step_gibbs` only when `include != in`, which requires `in || add_ok`, the branch that wrote it at `:121-123`;
   the swaps and independence step write `tmpQ` before reading it; `rb_acc` is reset at `:351`; `scratch` is workspace
   for `st.comp`; `ms`/`ev` are bookkeeping). *Fix:* one sentence in `L1:52-61` listing these members and why none
   carries information between steps or islands.

3. **Success-set convention.** Lemma B/F say "c in the success set (so c carries a grid …)" and "A₀ may be taken inside
   the success set's preimage" (`L1:10-11`, `L3:85`). *Fix:* define A_s ⊆ E as the set of c whose grid is
   0 = φ₀ < … < φ_T = 1 with integer T ≥ 1, N_e ≥ 1, L ≥ 0, R′ = 4k; assume (as CAL already implies) that
   𝒜 ⊆ {𝓒 ∈ A_s} and that c ↦ (T, grid, N_e, L, R′) are 𝓔-measurable; then take A₀ := A_s ∩ {R′ ≥ r} ∩ (a preimage set
   of 𝒜). Currently implicit.

4. **σ-field in (R3).** `L1:87-91` uses "H, the σ-field of everything before the round" and F_{τ_i} ⊇ H. *Fix:* set
   H := F_{τ_1} (stream σ-field at the round's first uniform), note σ(record before the round) ⊆ H, and that T12's
   conditional statements for the smaller σ-field follow by the tower property. One line.

5. **Downstream wording.** `R_remarks.md:5` says the PC1c3 premise "is discharged for every bounded declared h". N1 gives
   the *islandwise, conditional-on-𝓒* identity on E₀; pooled uses (clauses (f), (g), (i)) still need IND-T among islands
   for R′ > 4 (the remark lists this, but the first sentence over-reads). *Fix:* "discharged islandwise (given 𝓒, on
   𝒜 ∩ {r ≤ R′}); pooled clauses keep their own premises."

6. **Status headers.** Lemma files still read "PROVED (by this seat, unchecked)" while the package has been through
   lemma checks; after the council, harmonise the headers to the final status string with the premise qualifier, and
   add to `N1_theorem.md` an explicit line: "Status of N1 inherits the premise statuses START/KERNEL (N9: PROVED
   (candidate), code-checked)".

7. **Numerics bookkeeping (cosmetic).** (a) MC uses `seed_stream(70000 + 100·id + N, 10 + r)` with r from 0
   (`n1_harness.cpp:340`), i.e. not the production 9 + r labelling — harmless, but say so in `BUILD.md`. (b) 200 000 /
   50 000 islands per design are many streams under 20 seeds; state that this is the reading of the protocol's "≤ 20
   seeds" rule. (c) `STATEMENT.md:54` cites v2.1 `v3_engine.h:351-362`; the v2.1 measured loop is `:351-360`.

8. **Card-text note for HQ.** When the card is updated, carry Corollary E's constant as "δ₁ (hence the printed 2δ₁)",
   and keep the scope sentence that p ≤ 8 inputs take the exact branch in the full method, so the numerical companion
   tests the SMC component only (`STATEMENT.md:120-121`).
