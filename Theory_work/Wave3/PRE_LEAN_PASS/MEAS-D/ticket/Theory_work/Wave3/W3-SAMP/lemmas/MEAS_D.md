# MEAS-D — joint measurability of the potential records (W3-SAMP, new lemma)

Status: **PROVED (by this seat, unchecked)**. Check record: none yet; council seat R1 (Opus, claudeAgent_personal) on `PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD.txt` (output `PRE_LEAN_PASS/MEAS-D/R1_council_opus.md`); the Sol 6.2 seat follows as a separate section of the Sol-5 call, bound to the same digest.
Notation: `STATEMENT.md` §0 and §4. Claim id `W3-SAMP:MEAS-D`; its statement is `STATEMENT.md` §4 (appended so that the line numbers of §§0-3 stay unchanged). Text drafted by the pre-Lean Fable for the Theory manager (2026-11-18; sources read at origin/main ad29c22e), taken verbatim from `Theory_work/Dept/pre_lean_cards/MEAS-D_draft.md` on dept/theory, with the file name `MEASD.md` written `MEAS_D.md`.

Purpose: W3-SAMP's joint-law statements, and PoolZ's "Consequently" clause, use that the records are measurable in the data as well as in the streams. N1's premise MEAS covers fixed data only. This lemma proves the missing part, so that **no premise is added anywhere**.

## 0. The two checks, closed

**(i) Potential versus completed records (`W3-AUDIT-A:GW`).** The lemma must be about the potential fit P° only.
- GW defines P° as the same program with every operational check's Boolean replaced by FALSE, and proves that P°'s statistical state is a function of (X, y, seed) and the options (GW-iv).
- The actual 𝒜 and 𝒪 depend on the run-time guard. GW says in terms that it gives no probability model for the clock ("Not claimed", `T1_GW/STATEMENT.md:99-102`): if the clock is jointly measurable, 𝒪 is an event; otherwise the transfer P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°) holds as an outer-probability bound.
- So MEAS-D claims measurability for 𝓒°, 𝒜°, the potential island records, the potential final-run ledger and 𝒪°, and claims **nothing** about the actual 𝒜, 𝒪 or the guard's Booleans. Statements about actual runs are reached only through GW's pathwise inclusions, exactly as `W3-AUDIT-A:CAL-C` already reads W3-SAMP ("Where the T1 flag bites").

**(ii) The final local search and LS0.** The recorded code readings cover them; I do not need to stop.
- LS0: `W3-AUDIT-A:OPC` (OPC-a), (OPC-b) — it is exactly one call of `local_search`, it reads no uniform, and it realises the abstract search LS(S̃₀, ℓ_n + |S̃₀|), "a function of (X, y) given the centre".
- Its centre: `W3-AUDIT-A:TDP` (TDP-b), (TDP-c) — under EX-A the coded start mode is S*, the designated maximiser of the start weights.
- No interruption inside any search: GW (GW-v). Final local-search and LS0 archives and the final ledger are statistical state of P°: GW (GW-iii), (GW-iv).
- Measurability of the routine: `W3-AUDIT-A:CAL-C` PROOF Step 3 covers the calibration's searches by the bounded-computation argument.
- **The one link I supply by reading code:** the final local search and LS0 call the same routine `Engine::local_search` as the calibration searches (`cpp/v3_core.cpp:456` and `:476` against `:642` and `:689`; routine at `cpp/v3_engine.h:379`). The routine's loop is bounded by its move cap, and each scan is a finite set of score comparisons with the fixed lexicographic tie rule. The seats should re-check these four call sites.

## 1. Statement (one sentence for the "Two probability levels" paragraph, `W3-SAMP/STATEMENT.md:28-36`)

> **(MEAS-D) Joint measurability of the potential records.** Fix n, p_raw and the options, and assume EX-A. On the Borel set of valid inputs, the following objects of the potential fit P° (`W3-AUDIT-A:GW`) are Borel functions of (X^r, y^r, U^{(0)}, …, U^{(13)}), the seed entering only as a label: the calibration record 𝓒° and the event 𝒜°; the records of the four final islands; the final local-search and LS0 archives and the final-run ledger, hence 𝓜, 𝒯, Ŝ and every statistical field of P°'s output; the output event 𝒪°; and Z, π, π₀. Consequently, under the joint law of §0 (H-U/SI, :35-36), for each island r every identity or bound of §2 about island r stated "given 𝓒 on 𝒜" holds, for the potential pair (𝒜°, 𝓒°), conditionally on (data, 𝓒°); so do the statements obtained from these by finite sums, monotone comparison and union bounds over r, which is all that the joint-law clauses of §2 use; and where a clause assumes IND-T, the same holds for functions of the four final streams jointly. Nothing is claimed about the actual 𝒜, 𝒪 or the guard, which enter only through the pathwise inclusions of `W3-AUDIT-A:GW` (GW-iii), (GW-iv). (Proof: `lemmas/MEAS_D.md`.)

Conventions: off 𝒜° the final-run objects are set to a fixed symbol ⊥ (as 𝓒° := ⊥ when the calibration is not called). "Borel" is with respect to the product σ-field on the streams; each object depends on finitely many of their coordinates.

## 2. Proof

**Step 1 (domain and cells).** Valid inputs (`W3-RM2-R/STATEMENT.md:90-93`) form a Borel set of ℝ^{n×p_raw} × ℝⁿ. Split it by the set R of non-constant columns: finitely many Borel cells, because {Cx_j = 0} is closed. On a cell p = |R| is fixed, and the branch (enumeration or sampler) is a function of (n, p).

**Step 2 (data-only objects are continuous on each cell).** On a cell the sample SDs of the retained columns and s_y are positive and continuous, so the standardised (X, y) is a continuous function of (X^r, y^r). For every S: the entries of G_S and H_S are polynomials in X; det H_S and det(G_S + I) are positive polynomials; Q_S = yᵀy − n·z_SᵀH_S⁻¹z_S is a rational function whose denominator det H_S does not vanish. Hence log m(S), F(S), the start weights γ₀(S) (finite sums over the subsets of a block) and d(S) are continuous, and so are the finite sums Z, Z̄₀ and the ratios π, π₀. The block partition is a function of X determined by finitely many comparisons (`W3-AUDIT-A:BLK`); the start mode is S*, the maximiser of the start weights under a fixed tie rule (`W3-AUDIT-A:TDP` (TDP-b), (TDP-c)), so {S̃₀ = S} is a finite Boolean combination of comparisons of continuous functions. The neighbour graph N(X) (`cpp/v3_blocks.h:149-173`) is determined by finitely many comparisons of the continuous |r_jl| among themselves (ties by smaller index) and with the constant (2 log p/n)^{1/2}, so it is finite-valued with Borel level sets. All of these are Borel.

**Step 3 (calibration).** 𝓒° = Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) with Ψ Borel, the seed entering only as a label, and 𝒜° ∈ σ(𝓒°). This is recorded: `W3-AUDIT-A:CAL-C@1.0.3` (CAL-b), PROOF Step 3 — a computation whose length is bounded by a function of (n, p), each step being arithmetic, exp, log or floor, or a branch on a comparison of Borel functions.

**Step 4 (final islands, searches, ledger).**
- *Islands.* For fixed (T, N_e, L), the potential record of island r is computed from (grid values; the data constants of Lemma B, namely the scores, the start tables and block partition, the neighbour graph and the cache capacity 500p; and U^{(9+r)}) by a program of bounded length whose steps are Borel operations or branches on comparisons: `W1-N1` Lemma B (B-0), (B-b), (B-d), valid for the core of record by `W3-SAMP:CC`. The grid and (T, N_e, L) are coordinates of 𝓒° (CAL-c); the data constants are Borel in the data by Step 2.
- *Searches.* The final local search is the abstract search from the running best with cap ℓ_n; LS0 is the abstract search from S̃₀ with cap ℓ_n + |S̃₀| (`W3-AUDIT-A:OPC`). Each performs at most cap + 1 scans; a scan compares finitely many scores under the lexicographic tie rule; neither reads a uniform nor is interrupted (GW-v). The only non-operational exits of these final-run searches, inside them or at the LS0 call site, are the scorer's `NumericalFailure` (`cpp/v3_score.h:237`), unreachable under EX-A because H_S and G_S + I are positive definite (`cpp/v3_score.h:175-183`), the scorer's `|S| > K` throw (`cpp/v3_score.h:230`), unreachable because the search skips additions at size K (`cpp/v3_engine.h:397`) and swaps keep the size, and the LS0 cap-range `stop` (`cpp/v3_core.cpp:474`), a function of (n, p, |S̃₀|). All three are branches on Borel predicates, so 𝒪° stays Borel.
- *Ledger.* The running best and the top store are updated by comparisons under strict total orders (`hpm_better`; `W3-SAMP:CC` CC2). Its offers are the islands' evaluations, the block-table models (functions of the data, Step 2), the models inherited from calibration (coordinates of 𝓒°) and the two searches' scans (`W3-SAMP:PC` (iii)).
- A finite composition of Borel maps and of branches on Borel predicates is Borel. The cells (R, T, N_e, L) are countably many Borel sets, and on each the composition has bounded length. So the island records, the archives, the ledger and 𝒪° are Borel in (data, calibration value, final streams); composing with Step 3 gives the statement. On the enumeration cells, 𝒪° and the reported fields are finite comparisons and sums of the continuous scores of Step 2, hence Borel.

**Step 5 (the conditional form).** Fix r ≤ 4. Under the joint law of §0, U^{(9+r)} is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI as idealised, `STATEMENT.md:35-36`; SI is per island, `W1-N1/lemmas/L3_freezing.md:9-11`), hence of (data, 𝓒°). Independence from the pair follows from two stated facts: SI holds for each fixed data set, that is, given the data U^{(9+r)} is independent of U^{(0:9)} (`STATEMENT.md:29`); and U^{(9+r)} is independent of the data (`:35-36`). Hence P(U^{(9+r)} ∈ A, U^{(0:9)} ∈ B | data) = P(U^{(9+r)} ∈ A)·P(U^{(0:9)} ∈ B | data). For every bounded Borel g:

  E[g(data, 𝓒°, U^{(9+r)}) | data, 𝓒°] = ḡ(data, 𝓒°),  ḡ(x, c) := E g(x, c, U),  U ~ the law of one stream.

This is Lemma F (`W1-N1:F`, `W1-N1/lemmas/L3_freezing.md:21-23`) with (data, 𝓒°) in the frozen slot; ḡ is Borel by Fubini, and ḡ(x, ·) is the fixed-data conditional expectation of N1 at data x. So each fixed-data statement about island r "given 𝓒 on 𝒜" is the same statement given (data, 𝓒°) on 𝒜°, and integrating it is legitimate. For nonnegative unbounded g (the Ẑ_r of PoolZ) the same holds in [0, ∞] by monotone convergence.

*Several islands.* A quantity that reads several final streams (pip_primary, MPM, Ẑ, 𝓜, 𝒯, Ŝ, the final local search) is measurable by Steps 1–4, so its conditional expectation given (data, 𝓒°) exists. Bounding it by single-island terms needs no independence across islands: conditional expectation is linear and monotone, and conditional probability is subadditive. Every joint-law clause of §2 is obtained in this way: (D-iii) and (D-iv) from (D-i) for one fixed r; (LT-e) and (LT-e′) from (LT-a)–(LT-d) by a sum over r ≤ 4; (C-v) from (C-iii) and (C-iv) for each fixed r: the Ẑ, log Ẑ and NC_r clauses through |Ẑ/Z − 1| ≤ ¼Σ_r|W_r − 1| and (C-iii)'s per-island bound E[|W_r − 1| | 𝓒] ≤ β; the PIP and MPM clauses through ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r‖p̂_r − 1_{S₀}‖_∞, {MPM ≠ S₀} ⊆ {‖pip_primary − 1_{S₀}‖_∞ ≥ ½} and (C-iv)'s per-island bound g + β/2, whose right side depends on the data only. (TR-d) likewise from (TR-b)'s per-island bound g + e_L (σ(data, 𝓒)-measurable, the same for every r). In both, the Ŝ clause comes from the one-island bound on P(S₀ ∉ 𝓜_r | 𝓒) ((C-iv), (TR-c)), the pathwise Ŝ clause of (LT-d) with Lemma PC, and 𝒪 ⊆ 𝒪° (GW-iv); PoolZ by linearity. Only the clauses that assume IND-T, namely (D-ii) and the exponent 4D_r in (D-iii), use the four final streams jointly; for them the display holds with U^{(10:13)} := (U^{(10)}, …, U^{(13)}) in place of U^{(9+r)}, since IND-T, a premise of a fixed-data clause, holds given the data (`STATEMENT.md:29`), and each final stream is independent of the data (SI, `:35-36`), the conditional law of U^{(10:13)} given (data, U^{(0:9)}) is the fixed product law, so U^{(10:13)} is independent of (data, 𝓒°). No clause is given an independence premise it does not already state. ∎

**What the proof does not use.** No supremum or infimum over an uncountable set; no measurable-selection theorem; no tie rule other than fixed finite chains of comparisons; no property of the clock.

## 3. Standard facts used (Mathlib names verified in the pinned checkout)

| Fact | Mathlib |
|---|---|
| Composition of measurable maps | `Measurable.comp` |
| Continuous implies Borel measurable | `Continuous.measurable` |
| Arithmetic, exp, log, floor | `Measurable.mul`, `Measurable.div`, `Real.measurable_exp`, `Real.measurable_log`, `Int.measurable_floor` |
| Finite sums and products | `Finset.measurable_prod` (and its additive version) |
| Comparison sets are measurable | `measurableSet_lt`, `measurableSet_le` |
| Branch on a measurable predicate | `Measurable.ite`, `Measurable.piecewise` |
| Countably many cells | `Measurable.find`, `measurable_from_prod_countable_left` |
| Pairing | `Measurable.prodMk` |
| Independence step | `condExp_indep_eq`, with Fubini for ḡ |

## 4. What MEAS-D serves (exact clauses)

W3-SAMP (`Theory_work/Wave3/W3-SAMP/STATEMENT.md`), every clause stated under the joint law:
- `W3-SAMP:D` — (D-iii) `:102-103`, (D-iv) `:104-105`.
- `W3-SAMP:LT#` — (LT-e) `:136-138`, (LT-e′) `:139-140`.
- `W3-SAMP:C` — (C-v) `:158` onward.
- `W3-SAMP:TR` — (TR-d) `:170` onward.

The fixed-data clauses of the same theorems (D-i, D-ii, LT-a to LT-d, C-i to C-iv, TR-a to TR-c, Lemmas MR, ST, PC) do not need it.

W3-READER:
- `W3-READER:PoolZ` — the "Consequently" clause, E[1_𝒜 Ẑ] = E[1_𝒜 Z], read for the potential pair (`W3-READER/STATEMENT.md:22-23, 28-33`). Card rows 3.5 and 4.1 in their joint-law reading.

W3-DIST (`Theory_work/Wave3/W3-DIST/STATEMENT.md`), the P⊗ clauses of `W3-DIST:DIST-C`:
- (C-i) `:293-296`; (C-ii)(α) discovery, "P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0", `:299-300`; (C-iv) `:312-313`; and the honest-label sentence that data-only bounds extend to P⊗, `:316-317`.
- `W3-DIST:Cor-C` in its P⊗ form (`work/D_output/COR_C.md`, "Relation to DIST-C").

MEAS-D makes only the potential events measurable. Each {completed} clause above is reached through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv), as an outer-probability bound if the clock is not modelled (`T1_GW/STATEMENT.md:99-102`).

Theorem 10 (card row 3.6): through (LT-e), (C-v) and (TR-d). **To be confirmed against `walks/T9_Thm10.md` before the T9 card.**

## 5. Limits, stated plainly

- It is a statement about P° under EX-A (real arithmetic). In binary64 every object is finite-valued and the question does not arise.
- It rests on recorded code readings (GW, CAL-C, OPC, TDP, BLK, Lemma B, CC), which I have not re-read against the code, except for the four call sites named in §0 (ii).
- Those readings are at pin 4676af6. The re-pin to `method-v3.1.1-listpip` adds only the list fields. They are deterministic functions of the top store (finite sums, exponentials and branches on comparisons), with three `stop` rows (score and model counts differ; duplicate model; a column outside the retained set), each a branch on a Borel predicate. So the same argument covers them and 𝒪° stays Borel; the re-pin should say so in one line.
