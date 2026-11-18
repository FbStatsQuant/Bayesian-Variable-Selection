# MEAS-D — joint measurability of the potential records (draft for a new W3-SAMP lemma)

Drafted by the pre-Lean Fable for the Theory manager, 2026-11-18. Sources read at origin/main ad29c22e. Status: **DRAFT, unchecked**; seats (Opus, Sol 6.2) and recording are the manager's. Proposed file: `Theory_work/Wave3/W3-SAMP/lemmas/MEASD.md`; proposed id `W3-SAMP:MEAS-D`.

Purpose: W3-SAMP's joint-law statements, and PoolZ's "Consequently" clause, use that the records are measurable in the data as well as in the streams. N1's premise MEAS covers fixed data only. This lemma proves the missing part, so that **no premise is added anywhere**.

## 0. The two checks, closed

**(i) Potential versus completed records (`W3-AUDIT-A:GW`).** The lemma must be about the potential fit P° only.
- GW defines P° as the same program with every operational check's Boolean replaced by FALSE, and proves that P°'s statistical state is a function of (X, y, seed) and the options (GW-iv).
- The actual 𝒜 and 𝒪 depend on the run-time guard. GW says in terms that it gives no probability model for the clock ("Not claimed", `T1_GW/STATEMENT.md:98-101`): if the clock is jointly measurable, 𝒪 is an event; otherwise the transfer P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°) holds as an outer-probability bound.
- So MEAS-D claims measurability for 𝓒°, 𝒜°, the potential island records, the potential final-run ledger and 𝒪°, and claims **nothing** about the actual 𝒜, 𝒪 or the guard's Booleans. Statements about actual runs are reached only through GW's pathwise inclusions, exactly as `W3-AUDIT-A:CAL-C` already reads W3-SAMP ("Where the T1 flag bites").

**(ii) The final local search and LS0.** The recorded code readings cover them; I do not need to stop.
- LS0: `W3-AUDIT-A:OPC` (OPC-a), (OPC-b) — it is exactly one call of `local_search`, it reads no uniform, and it realises the abstract search LS(S̃₀, ℓ_n + |S̃₀|), "a function of (X, y) given the centre".
- Its centre: `W3-AUDIT-A:TDP` (TDP-b), (TDP-c) — under EX-A the coded start mode is S*, the designated maximiser of the start weights.
- No interruption inside any search: GW (GW-v). Final local-search and LS0 archives and the final ledger are statistical state of P°: GW (GW-iii), (GW-iv).
- Measurability of the routine: `W3-AUDIT-A:CAL-C` PROOF Step 3 covers the calibration's searches by the bounded-computation argument.
- **The one link I supply by reading code:** the final local search and LS0 call the same routine `Engine::local_search` as the calibration searches (`cpp/v3_core.cpp:456` and `:476` against `:642` and `:689`; routine at `cpp/v3_engine.h:379`). The routine's loop is bounded by its move cap, and each scan is a finite set of score comparisons with the fixed lexicographic tie rule. The seats should re-check these four call sites.

## 1. Statement (one sentence for the "Two probability levels" paragraph, `W3-SAMP/STATEMENT.md:28-36`)

> **(MEAS-D) Joint measurability of the potential records.** Fix n, p_raw and the options, and assume EX-A. On the Borel set of valid inputs, the following objects of the potential fit P° (`W3-AUDIT-A:GW`) are Borel functions of (X^r, y^r, U^{(0)}, …, U^{(13)}), the seed entering only as a label: the calibration record 𝓒° and the event 𝒜°; the records of the four final islands; the final local-search and LS0 archives and the final-run ledger, hence 𝓜, 𝒯, Ŝ and every reported statistical field; the output event 𝒪°; and Z, π, π₀. Consequently every identity or bound of §2 stated "given 𝓒 on 𝒜" holds, for the potential pair (𝒜°, 𝓒°), conditionally on (data, 𝓒°) under the joint law of §0; nothing is claimed about the actual 𝒜, 𝒪 or the guard, which enter only through the pathwise inclusions of `W3-AUDIT-A:GW` (GW-iii), (GW-iv). (Proof: `lemmas/MEASD.md`.)

Conventions: off 𝒜° the final-run objects are set to a fixed symbol ⊥ (as 𝓒° := ⊥ when the calibration is not called). "Borel" is with respect to the product σ-field on the streams; each object depends on finitely many of their coordinates.

## 2. Proof

**Step 1 (domain and cells).** Valid inputs (`W3-RM2-R/STATEMENT.md:90-93`) form a Borel set of ℝ^{n×p_raw} × ℝⁿ. Split it by the set R of non-constant columns: finitely many Borel cells, because {Cx_j = 0} is closed. On a cell p = |R| is fixed, and the branch (enumeration or sampler) is a function of (n, p).

**Step 2 (data-only objects are continuous on each cell).** On a cell the sample SDs of the retained columns and s_y are positive and continuous, so the standardised (X, y) is a continuous function of (X^r, y^r). For every S: the entries of G_S and H_S are polynomials in X; det H_S and det(G_S + I) are positive polynomials; Q_S = yᵀy − n·z_SᵀH_S⁻¹z_S is a rational function whose denominator det H_S does not vanish. Hence log m(S), F(S), the start weights γ₀(S) (finite sums over the subsets of a block) and d(S) are continuous, and so are the finite sums Z, Z̄₀ and the ratios π, π₀. The block partition is a function of X determined by finitely many comparisons (`W3-AUDIT-A:BLK`); the start mode is S*, the maximiser of the start weights under a fixed tie rule (`W3-AUDIT-A:TDP` (TDP-b), (TDP-c)), so {S̃₀ = S} is a finite Boolean combination of comparisons of continuous functions. All of these are Borel.

**Step 3 (calibration).** 𝓒° = Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) with Ψ Borel, the seed entering only as a label, and 𝒜° ∈ σ(𝓒°). This is recorded: `W3-AUDIT-A:CAL-C@1.0.3` (CAL-b), PROOF Step 3 — a computation whose length is bounded by a function of (n, p), each step being arithmetic, exp, log or floor, or a branch on a comparison of Borel functions.

**Step 4 (final islands, searches, ledger).**
- *Islands.* For fixed (T, N_e, L), the potential record of island r is computed from (grid values, scores, U^{(9+r)}) by a program of bounded length whose steps are Borel operations or branches on comparisons: `W1-N1` Lemma B (B-0), (B-b), (B-d), valid for the core of record by `W3-SAMP:CC`. The grid and (T, N_e, L) are coordinates of 𝓒° (CAL-c); the scores are Borel in the data by Step 2.
- *Searches.* The final local search is the abstract search from the running best with cap ℓ_n; LS0 is the abstract search from S̃₀ with cap ℓ_n + |S̃₀| (`W3-AUDIT-A:OPC`). Each performs at most cap + 1 scans; a scan compares finitely many scores under the lexicographic tie rule; neither reads a uniform nor is interrupted (GW-v).
- *Ledger.* The running best and the top store are updated by comparisons under strict total orders (`hpm_better`; `W3-SAMP:CC` CC2).
- A finite composition of Borel maps and of branches on Borel predicates is Borel. The cells (R, T, N_e, L) are countably many Borel sets, and on each the composition has bounded length. So the island records, the archives, the ledger and 𝒪° are Borel in (data, calibration value, final streams); composing with Step 3 gives the statement.

**Step 5 (the conditional form).** Under the joint law of §0, U^{(9+r)} is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI as idealised, `STATEMENT.md:35-36`), hence of (data, 𝓒°). For every bounded Borel g:
  E[g(data, 𝓒°, U^{(9+r)}) | data, 𝓒°] = ḡ(data, 𝓒°),  ḡ(x, c) := E g(x, c, U),  U ~ the law of one stream.
This is N1's freezing lemma (`W1-N1/lemmas/L3_freezing.md`) with (data, 𝓒°) in the frozen slot; ḡ is Borel by Fubini, and ḡ(x, ·) is the fixed-data conditional expectation of N1 at data x. So each fixed-data statement "given 𝓒 on 𝒜" is the same statement given (data, 𝓒°) on 𝒜°, and integrating it is legitimate. For nonnegative unbounded g (PoolZ's Ẑ) the same holds in [0, ∞] by monotone convergence. ∎

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
- `W3-READER:PoolZ` — the "Consequently" clause, E[1_𝒜 Ẑ] = E[1_𝒜 Z], read for the potential pair (`W3-READER/STATEMENT.md:22-23, 33-36`). Card rows 3.5 and 4.1 in their joint-law reading.

W3-DIST (`Theory_work/Wave3/W3-DIST/STATEMENT.md`), the P⊗ clauses of `W3-DIST:DIST-C`:
- (C-i) `:293-296`; (C-ii)(α) discovery, "P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0", `:299-300`; (C-iv) `:312-313`; and the honest-label sentence that data-only bounds extend to P⊗, `:316-317`.
- `W3-DIST:Cor-C` in its P⊗ form (`work/D_output/COR_C.md`, "Relation to DIST-C").

Theorem 10 (card row 3.6): through (LT-e), (C-v) and (TR-d). **To be confirmed against `walks/T9_Thm10.md` before the T9 card.**

## 5. Limits, stated plainly

- It is a statement about P° under EX-A (real arithmetic). In binary64 every object is finite-valued and the question does not arise.
- It rests on recorded code readings (GW, CAL-C, OPC, TDP, BLK, Lemma B, CC), which I have not re-read against the code, except for the four call sites named in §0 (ii).
- Those readings are at pin 4676af6. The re-pin to `method-v3.1.1-listpip` adds only the list fields, which are deterministic functions of the top store (finite sums and exponentials), so the same argument covers them; the re-pin should say so in one line.
