# T8 Fable card (consistency tier for Thm 7): Thm 7 (`W3-RM2-R:RM2-F-plus`, `RM0-plus`, `DLV-0`) and Thm 5 (`W3-START2-R:START-R`, `W3-START:FLOOR`)

Inputs: packet; Astra (FLAWS-FOUND, 3 points, with evidence trail); walk `walks/T8_Thm7.md` on walkB (WALK COMPLETE: 1 MINOR, 1 NOTE). The blind Sol read is on hold. Snapshot: `origin/theory/PRE-LEAN` 86743e30. **For the consultant: answer AGREE or OBJECT per row.**

**Verdict:** no flaw in the mathematics of Theorem 7 or Theorem 5. T8-1 is a wording inversion that was already recorded as an erratum; your reading is confirmed and no text depends on the literal reading. T8-2 restores a qualifier the lemma and the reader already carry. T8-3 is a "=" that should be "≤" on a probability-zero event.

## 1. Rulings on Astra's points

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **T8-1** IDEAL-W⁺ says the two rejection predicates are "treated as true" | **CONFIRM your reading; AGREE with the staged patch** | Wording inversion only, and a known one: `W3-RM2-R/ERRATA.md:6` (E2, from R1 Opus) | **Yes, wording:** DLV-0's premise span, `W3-RM2-R/STATEMENT.md:80-81`. No clause of DLV-0 or of Theorem 7 changes. | As staged in `T8/T8-1_correction.patch`: ", which are treated as true:" → "; the two bounds are treated as satisfied (the rejection predicates `le > 1e6`, `cap_ll > INT_MAX` never fire):". Same sentence in the carrier and in registry row `A:IDEAL-W+`. |
| **T8-2** START-R's optimality remark invokes FLOOR "on every data set" | AGREE with the staged patch | Unstated qualifier in a parenthetical remark; FLOOR needs s₀ < K (`W3-START/STATEMENT.md:241-243`) | **Yes, wording:** `W3-START2-R:START-R` span, `STATEMENT.md:237`. Clauses (i)–(iii) are untouched. | As staged in `T8/T8-2_correction.patch`: "on every data set" → "on every data set with s₀ < K". The lemma (`R3_RATE.md:164`) and the reader (`READER_VERSIONS.md:598-599`) already say this. |
| **T8-3** `R3_RATE.md:87`: on {(I − P_U)x_l = 0} the term "is again √(2/π)z_n" | AGREE | Proof-text slip on a probability-zero event; only the upper bound is used | No (lemma proof file) | Replace "on it δ_{U,l} := 0 and the term is again √(2/π)z_n ≤ F-bound below" by "on it δ_{U,l} := 0 and the term is J_{z_n}(0, τ_U) ≤ √(2/π)z_n (since τ_U ≥ σ), within the bound below". It can ride on the START2-R re-freeze that T8-2 already needs. |

### T8-1: what I checked

- **The two predicates are rejection tests in the code.** `v3_run.R:96` stops when `le > 1e6`; `cpp/v3_core.cpp:474` stops when `cap_ll > INT_MAX`. So "treated as true" read literally would make every run fail, and the delivery proof would be false.
- **Every text that uses IDEAL-W⁺ takes the predicates as not firing.** None depends on the literal reading:
  - the delivery proof `Q5_dlv0.md:93-97, 135` ("lifted by IDEAL-W⁺ (or false on 𝔇)");
  - the same statement's own parentheticals ("it would fire once n + p + 1 > 2^{10⁶}"; "`int` read as unbounded") and its fallback domain 𝔇;
  - registry row `A:IDEAL-W+` ("… are false");
  - C-DLV inventory rows X7, X8 ("this predicate is false");
  - the reader ("lifts two integer limits … neither limit can fire").
- **One leftover, my recommendation is to leave it:** `W2-UNI/lemmas/L5_delivery.md:48` quotes the old words ("its 'treated as true' … is read as 'are false'"). That sentence is pinned to branch commit e78a1055, where the text did say that, and it already gives the correct reading. Editing it would cost a W2-UNI re-freeze for no gain; change it only if W2-UNI is reopened.
- Astra's "blocking for DLV-0 as written" is right about the literal text and wrong about the claim: the intended premise was on record before this pass.

### T8-3: the check

J_h(0, t) = E[exp(aZ²/2)·1{|Z| ≤ h}] with a = σ²/t² ≤ 1, so J_{z_n}(0, τ_U) ≤ √(2/π)z_n, with equality only when τ_U = σ. On the event in question μ̃ may be nonzero, so τ_U can exceed σ.

## 2. Rulings on the walk rows

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Fix |
|---|---|---|---|---|
| **G1 (MINOR):** row 3.2's delivery clause rests on DLV-0 at its core pin; main's core is three commits later and ends `v3_fit` with three `stop()` rows outside DLV-0's exit list | AGREE | Record gap, not a flaw: the walker checked none can fire on an output run, but no recorded result says so for Theorem 7 | No text is wrong (DLV-0 claims nothing off its pin) | No edit now. At the next re-pin, add the three rows to the exit inventory with the reason each cannot fire. This is the same item as my Sol-1 card and walk T6 F2; one re-pin serves rows 3.1 and 3.2. **HQ decision:** which commit the paper's delivery clause is pinned to. |
| **G2 (NOTE, Lean):** c₀(s₀, A) contains C_*, "inside SOP:TH09's proof, not in any statement" | AGREE on the Lean need; **correct the location** | Lean note | No | None. C_* is written explicitly in a recorded statement: `W3-T03ACC/STATEMENT.md:40`, C_* = 2s₀ + 3[A·j_* + s₀ + log(j_* + 1) + 1], j_* = ⌈(2A+1)s₀⌉ + 1. Lean defines it by that formula; the reader's "explicit constant" is accurate. |

**Left uncovered:**
- The walk covers Theorem 7 only. **Theorem 5 (START-R and its inputs) has no walk**, and with the blind Sol read on hold, Astra's trail is the only new evidence on it in this pass.
- For Theorem 7 the walk stops at `SOP:TH09` (covered by T4) and refers the core and delivery to walk T6 §A2 and §A7, which I have not yet been sent.

## 3. Correctness (beyond Astra and the walk)

Nothing further. T8-1, T8-2 and T8-3 are each as described above, and none reaches a conclusion of either theorem.

## 4. Lean readiness (ranked; no item changes a statement)

1. **Theorem 7's core as finite-set mathematics over an explicit interface.** Hypotheses: scored models lie in Ω; on output, the search's scored sets are scored; the reported model maximises F over the scored set. Conclusion on 𝓜_n ∩ 𝒦_n: every output run reports S₀.
   - Gain: Level 1, reusing the order lemma of T2 item 4. The "exactly |S̃₀ ∖ S₀| deletions" count is an induction on a down-closed family.
2. **Probability layer as two bounds.** P(𝓜_nᶜ) ≤ 2·E[1 − π(S₀)] from the T4 headline; P(𝒦_nᶜ) from SAND-F-c, TL-F-c and NA-W.
   - Named axioms: Gaussian tail with union bound; Gaussian concentration for the maximum; plus those of T4.
3. **Delivery as hypotheses, not theorems.** State DLV-0 on the bounded domain 𝔇, or with the two predicates explicitly false (T8-1). The code-reading audits cannot be Lean theorems.
4. **Constants:** define c₀ through C_* at `W3-T03ACC/STATEMENT.md:40` (G2); the BM-∞ branch needs none.
5. **Theorem 5:** FLOOR is a Level-1 target of the same kind as T1 (one-step determinant ratio). In START-R the J-bounds (J0)–(J4) are Level-1 Gaussian integrals; state Step 1's representation with "≤" (T8-3).
   - Named axioms: independence of the Gaussian regression innovation; covariance concentration for Gaussian rows.
