# Stage B — Opus 5.5 (xhigh) reviewer, round 3 ruling on PROOF_v3 (verbatim)

Same agent as rounds 1–2, continued with SendMessage. Usage reported by the harness: 188,302 tokens, 4 tool uses, 169 s.

---

# Round 3 review: PROOF_v3.tex (T23(ii)) against STATEMENT.md

**Inputs read:** PROOF_v3.tex, PROOF_v3.pdf, B_CHANGES_v2_to_v3.md and the updated CLAIMS_OF_FATAL_FLAWS.md, together with STATEMENT.md and REPORT_FORMAT.md. All are in the packet folder. No commands were run and no files were written.

The PDF matches the TeX, and I see no clipped or overflowing displays in it. Theorem 6(c)–(d) and the constant 𝓑_n are unchanged. Theorem 6(a) now says "Under EX-A", which matches STATEMENT §2 ("uses only the setting and EX-A").

## Part 1: The specific checks requested

### Is the new Section 2 correct?

- **Step kernels and path law (2), l.70–74.** The proof defines a kernel K_e for each labelled step and gives the path law as an average over orders. This is what STATEMENT §1 says a round is: a fixed list of labelled steps, in a uniform order drawn independently of the state, each step acting on the current state.
  - The inference "same K₁, so the K_e are fixed" is carried by "every terminal round uses the same round", not by K₁ alone. STATEMENT §1 supports that wording ("Round at φ = 1… one independence proposal from π₀"; the terminal rounds are "all with the kernel K₁").
- **Per-particle σ-fields, l.82.**
  - 𝓕ⁱ_s ⊆ 𝓕ⁱ_{s+1} holds.
  - X_{i,0},…,X_{i,s} are 𝓕ⁱ_s-measurable. They are computed from the initial draws, the bridge stages and particle i's own rounds 1,…,s, and all of these come before its round s+1 in any processing order.
- **Single-round conditioning, l.93–97.** I checked the backward induction.
  - Write A_t = {Σ=σ, Y₀=x₀, …, Y_t=x_t}. Then P(A_t | 𝒟_t) = 1_{A_{t−1}} · K_{σ(t)}(x_{t−1}, {x_t}), because A_{t−1} ∈ 𝒟_t and, on A_{t−1}, Σ(t) = σ(t) and Y_{t−1} = x_{t−1}.
  - The chain 𝒟₀ ⊆ … ⊆ 𝒟_m is increasing, so the tower property applies. The last step gives E[1_{A₀} | 𝒟₀] = 1{X_{i,s}=x₀}/m!.
  - Summing over σ gives a right-hand side that is 𝓕ⁱ_s-measurable. Since 𝓕ⁱ_s ⊆ 𝒟₀, conditioning on 𝓕ⁱ_s leaves it unchanged, and by (2) it equals the round path law started at X_{i,s}.
- **q-round induction, l.99–101.** This is correct. The step from q to q+1 uses the one-round claim at s+q ≤ L+3 and the induction hypothesis with A = {y}.

### Is (F) a faithful reading of EX-S and CAL, or an added assumption?

It is a faithful reading, not an added assumption.

- **From EX-S.** EX-S idealises the generator as independent i.i.d. uniform streams. When the algorithm takes variates from such streams as it needs them, the variates used by a choice c are the next unused entries. Their positions are decided by earlier draws, so they are stopping times. Fresh entries after a stopping time are i.i.d. uniform and independent of everything drawn before. I checked this for one stream in round 2 (the v2 display), and it extends stream by stream.
- **From CAL.** CAL makes streams 10–13 independent of 𝓒, so conditioning on a fixed successful 𝓒 leaves their law unchanged. The success event lies in σ(data, streams 0–9).
- **From EX-A.** The "Hence" clause of (F), that each choice has the law the method prescribes, also needs EX-A. The proof says so (l.80: "Under EX-A these laws are realised exactly").
- **Two caveats.** v3 states as a primitive what v2 derived. And the wording "drawn before c is made" needs one fix (Finding 1).

### Do Sections 4–5 use Lemma 1 only within its ranges?

Yes. Every use is listed below.

| Where | What is used | Range check |
|---|---|---|
| Lemma 4, bounds on E₂ and E₃ | One-round claim at s = 0,…,H−1 | H ≤ L+4, so s ≤ L+3 |
| Lemma 4, bound on E₄ | q-round claim with s = (l−1)r₀, q = r₀ | l ≤ k gives lr₀ ≤ kr₀ ≤ H ≤ L+4, so s ≤ H−r₀ ≤ L+3 (r₀ ≥ 1) and s+q ≤ L+4. G_{l−1} ∩ {X_{(l−1)r₀} ∈ 𝓡} is 𝓕ⁱ_{(l−1)r₀}-measurable. |
| Lemma 5 | Path claim at s = H = L+h−1 | H runs from L to L+3; {X_{i,H} = S₀} ∈ 𝓕ⁱ_H. Lemma 4 is applied with H ≤ L+3. |
| Theorem (c) | Lemma 5 only | It uses unconditional probabilities, so summing over particles with different per-particle σ-fields is valid. |
| Section 5 | Nothing directly | — |

### Did anything else regress?

Mathematically, no. Lemmas 2–5, Theorem 6, Remarks 7–8, the S₀ ∉ Ω convention and the round counts behind (L+3)η + (L+4)ρ are all intact. One notational regression is reported as Finding 2.

## Findings on PROOF_v3

**Finding 1**
- **Location:** §2, the paragraph defining (F) (l.76–80); the per-particle σ-fields (l.82); the definitions of 𝒟₀,…,𝒟_m in the proof of Lemma 1 (l.93).
- **Severity:** exposition.
- **Claim:** 𝒟_c, 𝓕ⁱ_s and 𝒟_t are all defined by the variates "drawn before" some moment. Read as the time at which variates are generated, this fails for an implementation that draws variates in batches ahead of use.
  - Example: all uniforms for the terminal rounds are generated in one vectorised call at the start of the terminal phase. Then 𝓕ⁱ_s already contains the variates of particle i's round s+1, so X_{i,s+1} is 𝓕ⁱ_s-measurable. Lemma 1 as stated would then be false, and so would (F).
  - A smaller point: for a choice that uses a random number of variates (a rejection-type step), "the variates used by c are i.i.d. uniform" should refer to the fresh sequence that c draws from.
- **Evidence:**
  - *Repair.* Define each σ-field by the variates *used by choices made before* the relevant moment (consumption order), not by when they were generated. With that reading:
    - (F) holds for any batching, processing order or sub-stream layout, as l.80 claims;
    - 𝓕ⁱ_s ⊆ 𝒟₀ ⊆ … ⊆ 𝒟_m still holds;
    - X_{i,0},…,X_{i,s} stay 𝓕ⁱ_s-measurable;
    - the proof of Lemma 1 is unchanged word for word.
  - *Why exposition.* Under the stream model behind EX-S (a variate is taken from the stream when it is needed), the text is correct as written. STATEMENT §1's "drawn … afresh for every particle and every round" points the same way.

**Finding 2**
- **Location:** Lemma 1 statement and proof (l.87–93) compared with §1 (l.46) and Lemma 5 (l.191).
- **Severity:** exposition.
- **Claim:** The symbol X^{(t)}_{i,·} now has two indexings.
  - In §1, Lemma 2 and Lemma 5 it is indexed by the measured round h: X^{(0)}_{i,h} = X_{i,L+h−1}.
  - In Lemma 1 it is indexed by the terminal round s+1: X^{(0)}_{i,s+1} = X_{i,s}.
  - For example, X^{(0)}_{i,1} means X_{i,L} in §1 but X_{i,0} in Lemma 1.
- **Evidence:** Lemma 5 applies Lemma 1 with s = H = L+h−1. The path called X^{(·)}_{i,h} in §1 is called X^{(·)}_{i,H+1} in Lemma 1, and the reader has to translate. v2 avoided this with the subscript "round s+1 of particle i". The context makes the meaning clear, and nothing mathematical is affected.

## Part 2: Rulings on B_CHANGES_v2_to_v3.md and the log

| Entry | Agree with the author? | Does the change fix the finding? |
|---|---|---|
| Opus F1 (ordering and sub-stream assumptions) | Yes | Yes. The per-particle σ-fields 𝓕ⁱ_s, (F) and the step-by-step conditioning remove any dependence on processing order or sub-stream layout. The new proof is correct (Part 1). What remains is the "drawn" vs "used" wording (Finding 1, exposition). |
| Opus F2 / Astra #2 (method details not in STATEMENT.md) | Yes | Yes. §2 now cites only STATEMENT §1 (one round, one kernel K₁, fixed by the data and 𝓒). There is no π₀ construction, block size, neighbour graph or backward sampler, and B appears only as the number of neighbour swaps. I have not seen Astra #2's own wording; the change is checked against the TeX only. |
| Opus F3 ("stream r") | Yes | Yes. l.76 now reads "island r's streams are among 10–13". |
| Opus F4 (P vs P_𝓒; τ < ∞ a.s.) | Yes | Yes. l.68 fixes 𝓒 and works under P_𝓒 throughout, and the stopping time is gone. |
| Opus F5 (clipped display) | Yes | Yes. That display is gone, and the three wide displays are split; I see no clipping anywhere in PROOF_v3.pdf. The claim "pdflatex reports no overfull boxes" is unverified, because there is no build log in my packet and I may not run builds. |
| Opus F6 (stray comma; EX-A wording) | Yes | Yes. Lemma 2's display ends with a period and the blank line is gone (l.111–113). Theorem (a) reads "Under EX-A, on every realisation" (l.202), and the "part of the setting" wording is removed (l.213). |

**CLAIMS_OF_FATAL_FLAWS.md:**
- **Stage A, Stage B round 1, and the Astra #2 round-2 entry.** I cannot verify these: the replies they cite are outside my packet.
- **"Opus reviewer" round-2 entry.** This accurately describes my round-2 report: six findings, all exposition, the quoted sentence "I add no fatal or gap entry for round 2", agreement with the log entry on my round-1 report, and verdict verified. I agree.
- **Round 3.** I add no fatal or gap entry. Both findings above are exposition.

## Summary

PROOF_v3 proves exactly (ii-a)–(ii-d) under exactly the hypotheses of STATEMENT.md, with the same 𝓑_n. The rewritten Section 2 is correct. (F) is a faithful reading of EX-S and CAL, provided "drawn before" is read as "used by earlier choices" (Finding 1). Sections 4–5 use Lemma 1 only within its ranges, and nothing regressed mathematically. The only notational regression is the clash of path indices (Finding 2).

VERDICT: verified
