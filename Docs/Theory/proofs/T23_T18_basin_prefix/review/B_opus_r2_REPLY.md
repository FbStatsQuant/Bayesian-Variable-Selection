# Stage B — Opus 5.5 (xhigh) reviewer, round 2 ruling on PROOF_v2 (verbatim)

Same agent as round 1, continued with SendMessage. Usage reported by the harness: 137,259 tokens, 4 tool uses, 251 s.

---

# Round 2 review: PROOF_v2.tex (T23(ii)) against STATEMENT.md

**Inputs read:** PROOF_v2.tex, PROOF_v2.pdf, CLAIMS_OF_FATAL_FLAWS.md and B_CHANGES_v1_to_v2.md, plus STATEMENT.md and REPORT_FORMAT.md from round 1. All are in the packet folder. No commands were run and no files were written.

The PDF matches the TeX, except that one display is clipped (Finding 5). B_CHANGES says the statement, hypotheses, conclusions and constants are unchanged; I confirmed that. Theorem 6(a)–(d) and 𝓑_n are identical to v1. Lemma 4's hypotheses are weaker (only (B1)), and Lemma 1's range is narrowed.

## Part 1: The revisions

### The new stopping-time argument in Lemma 1 (l.78–92)

- **The kernel is fixed given 𝓒.** The fact the proof actually uses is that every terminal round runs the same kernel K₁, fixed by the data and 𝓒. That fact is in STATEMENT §1 ("all with the kernel K₁"; 𝓒 contains "all settings"). The other details listed there cannot be checked against STATEMENT.md (Finding 2).
- **Stopping time.** τ counts the uniforms consumed before particle i's round s+1 starts. Whether τ = n is decided by (𝓒, U₁,…,U_n), so τ is a stopping time.
- **Fresh tail.** The display P(A ∩ {V ∈ D}) = P(A)·P(V° ∈ D) for A ∈ 𝒢_τ is correct. It uses three facts:
  - A ∩ {τ=n} ∈ 𝒢_n;
  - (U_{n+1},…) is independent of 𝒢_n, which needs (U_n) to be i.i.d. and independent of 𝓒, as EX-S and CAL give;
  - P(τ<∞) = 1.
- **Substitution step.** The sum over x ∈ Ω is correct and gives the conditional law g(X_{i,s}), where g(x) = P(Φ(x,V°) ∈ Γ).
- **Multi-step version.** The tower-property version P(X_{i,s+r} ∈ A | 𝓕_s) = K₁^r(X_{i,s}, A) for s+r ≤ L+4 is correct.
- **Caveat.** The inclusion 𝓕_s ⊆ 𝒢_τ is valid only if all particles finish round s before particle i draws for round s+1, which STATEMENT.md does not say (Finding 1).

### The S₀ ∉ Ω convention (l.38, l.106)

- **Extension of π.** Extending π by 0 outside Ω is consistent. Because γ₁ > 0 on Ω, π(S₀) = 0 exactly when S₀ ∉ Ω. This now covers the (ii-b) parenthetical.
- **Lemma 2 when S₀ ∉ Ω.** Every path state lies in Ω, so B_{i,h} = 1 for all (i,h) and B̄_r = 1. PIP̂_{rj} is an average of values in [0,1], so the left side is at most 1. Both inequalities then hold for any real c_j*.

### The corrected index ranges

- 𝓕_s is defined for 0 ≤ s ≤ L+4, and Lemma 1 holds for 0 ≤ s ≤ L+3.
- Lemma 4 (0 ≤ H ≤ L+4) calls Lemma 1 only for s ≤ H−1 ≤ L+3. Its multi-step step needs lr₀ ≤ kr₀ ≤ H ≤ L+4.
- Lemma 5 uses H = L+h−1 ≤ L+3 in both Lemma 4 and Lemma 1.
- All uses are in range, and the round counts behind (L+3)η + (L+4)ρ are unchanged and correct.

### The other changes

- Lemma 4 now needs only (B1), and its proof uses nothing else.
- Remark 8 is now accurate.
- The note on suppressing the island index (l.52) is correct.
- Lemma 3, Lemma 5 and the proof of Theorem (c)–(d) are unchanged and still correct.

## Findings on PROOF_v2

**Finding 1**
- **Location:** Lemma 1 proof, l.81 ("Also 𝓕_s ⊆ 𝒢_τ, because the randomness used up to the end of round s is among U₁,…,U_τ"), and "possibly split into sub-streams; the argument is the same".
- **Severity:** exposition.
- **Claim:** The inclusion assumes two things STATEMENT.md does not state. First, uniforms are consumed in time order. Second, terminal rounds are processed round by round across the population, so every particle finishes round s before any round-(s+1) draw. Separately, the sub-stream case is asserted to be "the same" without being shown.
- **Evidence:**
  - *Counterexample to the inclusion.* Take a particle-major loop: particle 1 runs all L+4 terminal rounds, then particle 2, and so on. Nothing in STATEMENT §1 rules this out, since terminal rounds have no interaction between particles. Then particle 2's round-1 draws sit in the stream after τ for particle 1's round 2. So 𝓕₁ ⊄ 𝒢_τ, and the full tail V is not independent of 𝓕₁.
  - *The lemma's conclusion still holds.* The blocks used by different particle-rounds are fresh and disjoint.
  - *Local repair.* Use the per-particle filtration 𝓕ⁱ_s := 𝒢_{τ_{i,s}}, where τ_{i,s} is the number of uniforms consumed before particle i's round s+1. It increases in s and X_{i,s} is measurable with respect to it. Lemmas 4–5 only condition on events in σ(X_{i,0},…,X_{i,s}) ⊆ 𝓕ⁱ_s, so their proofs go through verbatim.
  - *Sub-streams.* With per-particle sub-streams, it works to put the other sub-streams entirely into 𝒢_n. With per-purpose sub-streams shared across particles, one needs the sequence of uniforms in consumption order, which is i.i.d. by adaptive selection. Neither case is literally "the same".
  - *Why exposition, not gap.* The proof's definition of 𝓕_s ("up to the end of terminal round s") already presupposes rounds at the population level, and STATEMENT §1's stage structure supports that reading.
  - *My round-1 evidence.* My round-1 evidence for Finding 1 made the same implicit assumption.

**Finding 2**
- **Location:** Lemma 1 proof, l.79 and l.85.
- **Severity:** exposition (unverified citations; not load-bearing).
- **Claim:** The proof credits STATEMENT.md §1 with facts that are not in it:
  - "the start law π₀ (a deterministic function of the data and the blocks)";
  - "the block size B";
  - "the neighbour graph (a deterministic function of X)";
  - "an exact draw from π₀ by the backward sampler".
- **Evidence:** STATEMENT §1 says only "one independence proposal from π₀" and "B neighbour swaps", so there B is a count of swaps, not a block size. It mentions no blocks, neighbour graph or backward sampler. I mark these claims unverified. The only fact the proof needs (one kernel K₁, fixed given 𝓒, for all terminal rounds) is in STATEMENT §1.

**Finding 3**
- **Location:** Lemma 1 proof, l.81 ("stream r").
- **Severity:** exposition.
- **Claim:** "Stream r" is a labelling slip. Island r's final-run stream is one of streams 10–13. Read literally, "stream r" with r ∈ {1,…,4} would be a calibration stream (0–9), which would break the CAL independence used in the next sentence.
- **Evidence:** The next sentence correctly says streams 10–13 are independent of 𝓒, so the intended meaning is clear.

**Finding 4**
- **Location:** Lemma 1 proof, l.81–85.
- **Severity:** exposition.
- **Claim:** There are two small mismatches.
  - The displays are written under P with 𝓒 random inside 𝒢_n, while the lemma is stated under P_𝓒 for a fixed successful 𝓒. As written, the argument gives the result only for P-almost every 𝓒.
  - "τ < ∞, since each round consumes finitely many variates" should read "τ < ∞ almost surely" for rejection-type implementations, where the count is unbounded.
- **Evidence:** (U_n) is independent of 𝓒, so the same argument works verbatim for each fixed c with 𝒢_n = σ(U₁,…,U_n). The display only needs P(τ<∞) = 1. No change to the conclusion.

**Finding 5**
- **Location:** PROOF_v2.pdf, page 3, the stopping-time display (TeX l.82–84).
- **Severity:** exposition.
- **Claim:** The display runs past the right margin, and its ending "∈ D)," is clipped in the PDF.
- **Evidence:** The PDF text ends with "= P(A) P(V° ∈ D", while the TeX has the complete "=P(A)\,P(V^\circ\in D),".

**Finding 6**
- **Location:** Lemma 2 statement (l.97–102); Theorem 6(a) and its proof (l.192, l.203).
- **Severity:** exposition.
- **Claim:** (i) Lemma 2's display still ends with a stray comma followed by a blank line. (ii) Lemma 2 assumes EX-A, but Theorem 6(a) does not list it, and its proof calls EX-A "part of the setting". STATEMENT §2 lists EX-A as a hypothesis, not as part of the setting.
- **Evidence:** Neither point is a mathematical problem. STATEMENT §1 already defines PIP̂ through the exact o_j, so (a) holds as stated.

## Part 2: Rulings on B_CHANGES_v1_to_v2.md and the log

| Entry | Agree with author's answer? | Does the change fix my finding? |
|---|---|---|
| 1. Stopping-time step in Lemma 1 | Yes | Yes. The argument is correct for a single stream consumed in time order with rounds processed across the population. The ordering assumption remains (v2 Finding 1, exposition), with a local repair. |
| 2. Kernel fixed given 𝓒 | Yes | Yes in substance: the citation of "one kernel K₁" to STATEMENT §1 is correct. However, the added ingredient details are not in STATEMENT.md and are unverified (v2 Finding 2). They should be cut back to what the statement says. |
| 3. S₀ ∉ Ω convention, (ii-b) parenthetical | Yes | Yes. π extended by 0 and an arbitrary real c_j* are consistent, and the proof is correct for every choice. A stray comma remains (v2 Finding 6). |
| 4. Index ranges | Yes | Yes. All uses of Lemmas 1 and 4 are within the new ranges (checked above). |
| 5. Lemma 4 hypotheses; Remark 8 | Yes | Yes. Lemma 4 uses only (B1), and Remark 8 is now accurate. |
| 6. EX-A for Lemma 2; island index | Yes | Yes. The EX-A wording is slightly inconsistent between Lemma 2 and Theorem (a) (v2 Finding 6). |

**CLAIMS_OF_FATAL_FLAWS.md:**
- **Stage A (Astra #1) and Stage B round 1 (Astra #2), both "none".** I cannot verify these: the replies they cite are not in my packet, and my contract does not allow reading them.
- **"Opus 5.5 xhigh reviewer: none".** This accurately describes my round-1 report: six findings, all exposition, "no fatal error and no gap", verdict verified. I agree.
- **Round 2.** I add no fatal or gap entry for round 2. All six v2 findings are exposition.

## Summary

PROOF_v2 proves exactly (ii-a)–(ii-d) under exactly the hypotheses of STATEMENT.md, with the same 𝓑_n. The revisions are correct and introduce no mathematical error. What remains is presentation:
- the unstated ordering assumption behind 𝓕_s ⊆ 𝒢_τ, which has a local repair (Finding 1);
- method details credited to STATEMENT.md that I could not verify (Finding 2);
- typographic and notational slips (Findings 3–6).

VERDICT: verified
