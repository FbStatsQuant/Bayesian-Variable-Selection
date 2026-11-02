# Stage B Opus 5.5 (xhigh) reviewer, ruling round (r2), on PROOF_v3 + STATEMENT v3 + claims log — saved by the lead (2026-10-22)

Verdict: **verified.** "I agree with every answer in the log, and each change works. PROOF_v3 proves all claims of STATEMENT v3 §§3–4 under the stated hypotheses. The revision introduced no fatal or gap issue; my three new findings (N1–N3) are all minor exposition points."

## Part 1 (rulings on the log), condensed by the lead; every ruling is quoted in substance
- A1-1: agree, fix works (re-checked the counterexample; v3 §5 item 1 correct: under "last centre" the flag is 1 iff NOIMP; under the adopted reading iff NOIMP and R = c_m).
- A1-2: agree, fix works (thin-SVD bound valid since k ≤ K ≤ n).
- Astra #2 remark (inner probability): agree it is harmless.
- F1: agree, fix works. F2: agree, fix works (for any fixed τ, ▷_{F′,τ} and ▷_{F,τ} agree on 𝒮_end ⊇ I_k). F3: agree, fix works. F4: agree, fix works (N ≠ R because R ∉ 𝒩(R)). F5: agree, fix works. F6: agree, fix works (enlarging C only shrinks the bad event). F7: agree, fix works. F8: agree with the handling. F9: agree it is partly addressed; that H03 is the conclusion of T03(i) stays unverified by the reviewer and does not affect the proof. F10: agree, fix works (see N1).
- "No hypothesis or claim content changed": "Accurate in substance." Nuance: the (i-b) change corrects a parenthetical that was false when 𝒮_end = Ω, "in the direction of a weaker, correct claim".

## Part 2 (review of PROOF_v3), verbatim findings

Fidelity check against the newly quoted method text (§0): all checks pass, including: "Another possible reading is that the search re-centres at the running HPM after each scan. That reading is covered too. Reason: by Lemma 2(b), best(𝒮_{<k+1}) has score M > F(c_k) = max_{𝒮_{<k}} F. So it lies in I_k and is the ≻-maximum of I_k. That is exactly the formal procedure with ▷ = ≻."

**N1.** STATEMENT §5 item 5, the new tie-route parenthetical. Severity: **exposition**.
- **Claim:** the wording "an equal-score neighbour of c_m that precedes c_m in the HPM order becomes R" is imprecise in two ways.
- **Evidence:**
  - (a) If several models tie at F(c_m), R is the ≻-maximum of all of them, which need not be the neighbour named.
  - (b) The neighbours of c_m are not the only tie route.
    - Example: c_{m−1} = {1}. Suppose the move tie rule picks c_m = {1,2} over T = {2}, both in I_{m−1} with equal score. A pure-lexicographic τ would do this.
    - Then T ≻ c_m by size, so R = T. T was first scored by scan m−1, not by the final scan.
  - In every case both flags are still 0, and (i-a) still covers the outcome. This text is in the readings section, not a claim of §§3–4.

**N2.** STATEMENT §1, the list of sources feeding the HPM, compared with the §0 quote. Severity: **exposition**.
- **Claim:** the two lists differ slightly. §1 has "accepted and rejected proposals, local scans", and omits "independence proposals". The quote has "rejected proposals, independence proposals, local searches".
- **Evidence:** both lists sit under "every model ever scored", which is what the proof uses. So nothing in the proof is affected.

**N3.** PROOF_v3 (ii-C)3; STATEMENT (ii-C)3. Severity: **exposition** (carried over).
- **Claim:** "E_n is measurable … continuous functions of y" leaves out that y is the standardised response, while P₀ is the law of the raw Gaussian errors.
- **Evidence:** standardisation is continuous wherever the raw response is not constant, which holds P₀-almost surely. So E_n is measurable for the completed P₀. Not stating this is harmless.

Fidelity of STATEMENT v3 §§3–4 to §0: "Faithful and precise." Not checkable from the packet: that H03 is the conclusion of T03(i) (itself a conjecture), and that the quotes match the hashed methodology file. "Both are outside the packet and leave the proof itself unaffected."

## Verdict
**Verified.** "PROOF_v3 correctly proves every claim of STATEMENT v3 §§3–4 under the stated hypotheses (EX-A and EXEC, an arbitrary F for clause (i) and (ii-A), the method's F for (ii-B) and (ii-C), and H03 for (ii-C)). The revision introduced no fatal or gap issue; N1–N3 are exposition only."
