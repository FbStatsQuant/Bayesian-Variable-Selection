# MEAS-D: author's fixes after Opus seat R1 (score 8.0, gates FAIL; claim ACCEPT)

Review: `PRE_LEAN_PASS/MEAS-D/R1_council_opus.md` on `origin/theory/PRE-LEAN` ae10ff1c, manifest 7fbc2f86. Line numbers below are those of the staged ticket files under `PRE_LEAN_PASS/MEAS-D/ticket/Theory_work/Wave3/W3-SAMP/`.

## 0. Decisions

| Finding | Decision | One line |
|---|---|---|
| **F1** | ACCEPT the finding; **fix by restricting the "Consequently" sentence, not by the joint reading** | The joint reading genuinely fails the no-added-premise rule (reason below). The restricted sentence still covers every joint-law clause it is meant to serve. |
| **F2** | ACCEPT | The neighbour graph is a data constant the islands read; it is Borel; add it to Steps 2 and 4. |
| **F3** | ACCEPT | Cite `W1-N1:F@stmt`; no step uses Theorem N1 itself. |
| E1 | ACCEPT | Pin: `T1_GW/STATEMENT.md:99-102`. |
| E2 | ACCEPT | Pin: `W3-READER/STATEMENT.md:22-23, 28-33`. |
| E3 | ACCEPT | "every statistical field of P°'s output", so it cannot be read as the actual output. |
| E4 | ACCEPT | Say how the {completed} clauses are reached (GW-iv, outer probability if the clock is not modelled). |
| E5 | ACCEPT | Name the two non-operational exits inside the final-run searches; both are Borel branches. |
| E6 | ACCEPT | One line for 𝒪° on the enumeration cells, which Step 4 did not cover. |
| E7 | ACCEPT | The re-pin remark names the list-field branches and its three `stop` rows (Opus names one; there are three). |
| E8 | ACCEPT | Name H-U/SI in the statement. |

None of E1–E8 is declined: each is either a pin the house rule requires exact, or a real gap in coverage or scope wording.

### Why F1 is fixed by restriction

- SI is per island by definition: "for a fixed index r ≥ 1, U_r … independent of streams 0–9 (premise SI)" (`W1-N1/lemmas/L3_freezing.md:9-11`); PoolZ's Remark (i) says "SI is per island". W3-SAMP lists joint independence of streams 10–13 separately, as IND-T, "only in D-ii" (`STATEMENT.md:64-66`).
- Per-stream independence from (data, streams 0–9) does not imply that the vector of four final streams is independent of it. Reading H-U/SI jointly would therefore give every joint-law clause part of IND-T, a premise those clauses do not state.
- It is also not needed. Every joint-law clause of §2 is obtained from single-island statements by a fixed r, a finite sum, a monotone comparison or a union bound, none of which uses independence across islands. Only (D-ii) and the 4D_r exponent of (D-iii) use the streams jointly, and they already assume IND-T.
- So the statement is narrowed to what Step 5 proves, and Step 5 gains a paragraph showing that this is all the clauses use. **No clause receives an independence premise it does not already state.**

## 1. STATEMENT sentence: it changes (the "Consequently" clause, plus E3 and E8)

`STATEMENT.md:190` (one line; the claim's lines stay 190-192). Replace the whole line by:

> **(MEAS-D) Joint measurability of the potential records.** Fix n, p_raw and the options, and assume EX-A. On the Borel set of valid inputs, the following objects of the potential fit P° (`W3-AUDIT-A:GW`) are Borel functions of (X^r, y^r, U^{(0)}, …, U^{(13)}), the seed entering only as a label: the calibration record 𝓒° and the event 𝒜°; the records of the four final islands; the final local-search and LS0 archives and the final-run ledger, hence 𝓜, 𝒯, Ŝ and every statistical field of P°'s output; the output event 𝒪°; and Z, π, π₀. Consequently, under the joint law of §0 (H-U/SI, :35-36), for each island r every identity or bound of §2 about island r stated "given 𝓒 on 𝒜" holds, for the potential pair (𝒜°, 𝓒°), conditionally on (data, 𝓒°); so do the statements obtained from these by finite sums, monotone comparison and union bounds over r, which is all that the joint-law clauses of §2 use; and where a clause assumes IND-T, the same holds for functions of the four final streams jointly. Nothing is claimed about the actual 𝒜, 𝒪 or the guard, which enter only through the pathwise inclusions of `W3-AUDIT-A:GW` (GW-iii), (GW-iv). (Proof: `lemmas/MEAS_D.md`.)

`STATEMENT.md:36` (pointer sentence) and `:192` (Conventions): unchanged.

## 2. `lemmas/MEAS_D.md`: exact replacements

**(a) Line 12 (E1).** `T1_GW/STATEMENT.md:98-101` → `T1_GW/STATEMENT.md:99-102`.

**(b) Line 24 (§1, the quoted statement).** Replace the quoted sentence by the new sentence of §1 above, verbatim.

**(c) Line 32 (Step 2; F2).** Append at the end of the paragraph, before "All of these are Borel.":

> The neighbour graph N(X) (`cpp/v3_blocks.h:149-173`) is determined by finitely many comparisons of the continuous |r_jl| among themselves (ties by smaller index) and with the constant (2 log p/n)^{1/2}, so it is finite-valued with Borel level sets.

**(d) Line 37 (Step 4, Islands; F2).** Replace "is computed from (grid values, scores, U^{(9+r)}) by a program" by:

> is computed from (grid values; the data constants of Lemma B, namely the scores, the start tables and block partition, the neighbour graph and the cache capacity 500p; and U^{(9+r)}) by a program

and replace the last sentence "the scores are Borel in the data by Step 2." by "the data constants are Borel in the data by Step 2."

**(e) Line 38 (Step 4, Searches; E5).** Append:

> The only non-operational exits inside these searches are the scorer's `NumericalFailure` (`cpp/v3_score.h:237`), unreachable under EX-A because H_S and G_S + I are positive definite (`cpp/v3_score.h:175-183`), and the LS0 cap-range `stop` (`cpp/v3_core.cpp:475`), a function of (n, p, |S̃₀|). Both are branches on Borel predicates, so 𝒪° stays Borel.

**(f) Line 40 (Step 4, last bullet; E6).** Append:

> On the enumeration cells, 𝒪° and the reported fields are finite comparisons and sums of the continuous scores of Step 2, hence Borel.

**(g) Lines 42-44 (Step 5; F1, F3).** Replace the whole step by:

> **Step 5 (the conditional form).** Fix r ≤ 4. Under the joint law of §0, U^{(9+r)} is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI as idealised, `STATEMENT.md:35-36`; SI is per island, `W1-N1/lemmas/L3_freezing.md:9-11`), hence of (data, 𝓒°). For every bounded Borel g:
>   E[g(data, 𝓒°, U^{(9+r)}) | data, 𝓒°] = ḡ(data, 𝓒°),  ḡ(x, c) := E g(x, c, U),  U ~ the law of one stream.
> This is Lemma F (`W1-N1:F`, `W1-N1/lemmas/L3_freezing.md:21-23`) with (data, 𝓒°) in the frozen slot; ḡ is Borel by Fubini, and ḡ(x, ·) is the fixed-data conditional expectation of N1 at data x. So each fixed-data statement about island r "given 𝓒 on 𝒜" is the same statement given (data, 𝓒°) on 𝒜°, and integrating it is legitimate. For nonnegative unbounded g (the Ẑ_r of PoolZ) the same holds in [0, ∞] by monotone convergence.
>
> *Several islands.* A quantity that reads several final streams (pip_primary, MPM, Ẑ, 𝓜, 𝒯, Ŝ, the final local search) is measurable by Steps 1–4, so its conditional expectation given (data, 𝓒°) exists. Bounding it by single-island terms needs no independence across islands: conditional expectation is linear and monotone, and conditional probability is subadditive. Every joint-law clause of §2 is obtained in this way: (D-iii) and (D-iv) from (D-i) for one fixed r; (LT-e) and (LT-e′) from (LT-a)–(LT-d) by a sum over r ≤ 4; (C-v) from (C-iv) and (TR-d) from (TR-c) through ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r‖p̂_r − 1_{S₀}‖_∞; PoolZ by linearity. Only the clauses that assume IND-T, namely (D-ii) and the exponent 4D_r in (D-iii), use the four final streams jointly; for them the display holds with U^{(10:13)} := (U^{(10)}, …, U^{(13)}) in place of U^{(9+r)}, under IND-T read, like SI in `STATEMENT.md:35-36`, with the data adjoined. No clause is given an independence premise it does not already state. ∎

**(h) Line 73 (E2).** `W3-READER/STATEMENT.md:22-23, 33-36` → `W3-READER/STATEMENT.md:22-23, 28-33`.

**(i) After line 77 (end of the W3-DIST bullets; E4).** Insert:

> MEAS-D makes only the potential events measurable. Each {completed} clause above is reached through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv), as an outer-probability bound if the clock is not modelled (`T1_GW/STATEMENT.md:99-102`).

**(j) Line 85 (E7).** Replace the second sentence ("The re-pin to … in one line.") by:

> The re-pin to `method-v3.1.1-listpip` adds only the list fields. They are deterministic functions of the top store (finite sums, exponentials and branches on comparisons), with three `stop` rows (score and model counts differ; duplicate model; a column outside the retained set), each a branch on a Borel predicate. So the same argument covers them and 𝒪° stays Borel; the re-pin should say so in one line.

Lines 1-11, 13-23, 26, 30, 34, 39, 46-72, 74-76, 79 and 83-84: unchanged.

## 3. REGISTRY block (`REPORT.md` §8, lines 200-204 of the staged file)

Lines 200 (`claim: … | statement: STATEMENT.md:190-192 | premises: STATEMENT.md:20-60`) and 202 (`status: …`): unchanged.

**Line 203.** Replace by (no bar characters; plain names as in the staged block):

```
conclusion: identity: under EX-A, for fixed n, p_raw and options, on the Borel set of valid inputs the potential calibration record, the event A0, the four potential island records, the final local-search and LS0 archives, the final-run ledger (hence M, T, S-hat and every statistical field of P0's output), the output event O0, Z, pi and pi0 are Borel functions of (X^r, y^r, U(0), ..., U(13)); so, under the joint law (H-U/SI), for each island r every fixed-data given-C-on-A statement of section 2 about island r holds conditionally on (data, C0), and so do their finite sums, monotone comparisons and union bounds over r; clauses that assume IND-T hold for the four final streams jointly; nothing is claimed about the actual A, O or the guard | scope: the potential fit P0 of W3-AUDIT-A:GW only; EX-A (real arithmetic)
```

**Line 204 (F3).** Replace by:

```
depends_on: W3-AUDIT-A:CAL-C@proof:CAL-b,Step-3 ; W3-AUDIT-A:GW@stmt:GW-iii,GW-iv,GW-v ; W3-AUDIT-A:OPC@stmt:OPC-a,OPC-b ; W3-AUDIT-A:TDP@stmt:TDP-b,TDP-c ; W3-AUDIT-A:BLK@stmt ; W1-N1:B@proof:B-0,B-b,B-d ; W1-N1:F@stmt ; W3-SAMP:CC@proof:CC2
```

## 4. Notes for the R2 diff round

- **What changed in substance:** only the "Consequently" clause, which is now narrower (single-island statements and what follows from them by sums, monotone comparison and unions; IND-T clauses as they state). The measurability half of the statement is unchanged apart from E3's wording.
- **One reading to check:** the IND-T sentence reads IND-T "with the data adjoined", as `STATEMENT.md:35-36` does for SI. This is the reading (D-iii)'s 4D_r variant already needs in order to be unconditional; I state it rather than leave it tacit. If the seat judges it an addition, drop the last clause of the statement ("and where a clause assumes IND-T …") and the matching sentence of Step 5; nothing else depends on it.
- **Clause-by-clause claim in Step 5 ("Every joint-law clause of §2 is obtained in this way"):** I checked (D-iii) against `lemmas/D_theorem.md` §3 and (LT-d), (LT-e) against `lemmas/LT_theorem.md` Steps 3–4. For (C-v) and (TR-d) I rely on the statements of (C-iv) and (TR-c) (`STATEMENT.md:156, 169`), not on their proof files; the seat should confirm those two.
- **F2 checked at the source:** `cpp/v3_blocks.h:149-173` sorts candidates by |r_jl| with index tie-break, keeps those above (2 log p/n)^{1/2}, at least one and at most B, and symmetrises.
