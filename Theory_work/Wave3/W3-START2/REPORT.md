# W3-START2 — REPORT (the four BT2 improvements of the start-mass rate; statement v1.4)

Lead: Claude Fable 5.2 (effort high). Statement: `STATEMENT.md` v1.4.1, a delta statement on the base ticket
BASE := `Theory_work/Wave3/W3-START/` (statement v1.3.4). Proofs: `lemmas/P1_LEADING.md`, `lemmas/P2_OVL.md`,
`lemmas/P3_NEC.md`, `lemmas/P4_BR.md`. This file is the technical report and is part of the frozen content that the
council reads. It therefore contains **no review record**: the review trail, the council outcome, the final status of
each claim and the registry blocks are in the ticket's final checkpoint file, which is written after the council and
is not part of the frozen content (the acceptance tool requires the frozen content to be unchanged after the council
round).

## 1. Result (author's statement)

Every claim of `STATEMENT.md` §3 has a proof in `lemmas/`; author status of each: "PROVED (by this seat)". Each proof
re-proves only the steps that change and cites the base proof files by line for the rest. The claims consume the
base ticket's results by statement and by proof step (§4); no other claim is consumed.

In words (all four improvements proposed by the base ticket's better-theorem review are obtained):
* **P1 — a sharper leading term.** With no leakage, the start odds against the true model satisfy
  o₀ = O_P(n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)²) + o_P(n^{−κ}), where for s₀ ≥ 1 the functional 𝔏^♯_n(h) conditions on
  **proper** subsets of the truth only. The term 15√(2/π)z_n/p of version 1.3.4 is gone. Reason: the at most 15 null
  columns that can share a block with every truth have zero mean gain, and for a bounded number of standard normal
  variables a fixed cut-off of the tail replaces the level z_n ≈ √(2 log p) (Lemma LEAK-0). Consequence: the
  strong-signal corollary F2 needs no growth condition on p; for bounded p > s₀ the order n^{−1/2} is exact.
* **P2 — overlap under either visibility condition.** The lower bound π₀(S₀) ≥ n^{−E_n−ε} for a bounded leakage set
  holds under the margin form (V-m) as well as under (V-c), by the exact identity
  1/π₀(S₀) = [Σ_{T∈𝓛(Q)}γ₀(T)/γ₀(S₀)]/π₀(𝓛(Q)) and the lattice clause of Theorem START-F.
* **P3 — a partition-free leaking-null limit that is not vacuous.** For 1 ≤ s₀ ≤ 15: if 17 − s₀ null columns each gain
  more than (1 + 2Ā)·τ²_V·log n on every proper subset V of the truth, then π₀(S₀) → 0 at a polynomial rate, whatever
  the partition. A design satisfying the premise is given for every s₀ ∈ {1, …, 15}.
* **P4 — leakage sets of any size ≤ K under Gaussian rows.** P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)·n^{−1/2}·e^{C_R√log n}) → 1 with no
  restriction on |Q| beyond |Q| ≤ K; the bound is informative up to |Q| = n^{1/2−ε}. Only the reference sets H_l stay
  polylogarithmic.

## 2. The statement as proved, and changes against the ticket brief

| brief (`BRIEF.md`) | delivered | where |
|---|---|---|
| P1: replace 15√(2/π)z_n/p by 1/p in (T1)(b), (T1)(d), (T3)(a), IF-START | the term is **dropped**: since 1/p ≤ 4𝔏^♯_n(h), "𝔏^♯_n(h) + 1/p" and 𝔏^♯_n(h) give the same statements | (D1), LEAK-0, (T1⁺), (T3⁺)(a), IF-START⁺ |
| P1: F2 without p/√log n → ∞ | as asked; bounded p included | F2⁺ |
| P2: OVL under (V-m) as well as (V-c) | as asked; the proof no longer uses the truth-deletion functional e_n | OVL⁺ |
| P3: non-vacuous partition-free limit for 1 ≤ s₀ ≤ 15 with 17 − s₀ designated nulls | as asked; s₀ = 0 excluded; for s₀ ≥ 16 identical to the base (N2) | (N2⁺) |
| P4: (T3)(b) with \|Q\| ≤ n^{1/2−ε_Q} and \|Q\| ≤ K | **no size condition beyond \|Q\| ≤ K**; \|Q\| ≤ n^{1/2−ε_Q} is the stated special case in which the bound gives concentration | (D2), (B-R⁺), (T3⁺)(b) |

Two places are stronger than the brief's wording (P1 and P4, as in the table); each implies the form asked for.
Nothing else of version 1.3.4 changes. The changed hypotheses are listed in `STATEMENT.md:25-28`.

## 3. Claims, proofs and author status

| claim (id W3-START2:…) | statement | proof | what is new in the proof | author status |
|---|---|---|---|---|
| LEAK-0 (lemma, new) | `STATEMENT.md:82-89` | `lemmas/P1_LEADING.md` P1.1–P1.3 | split of the nulls into proper and exceptional columns; union bound at a fixed cut-off H for ≤ 15 exceptional columns; Markov for the rest | "PROVED (by this seat)" |
| START-F (T1⁺) | `STATEMENT.md:93-110` | `lemmas/P1_LEADING.md` P1.4–P1.5 | the event {T₁ ≤ 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)} replaces 𝓜₀ in the base proof of L5.2(ii); same c₀, C, n₀ | "PROVED (by this seat)" |
| F2 (F2⁺) | `STATEMENT.md:112-117` | `lemmas/P1_LEADING.md` P1.6 | 𝔏^♯_n ≤ C_F n^{η′/2} with no remainder | "PROVED (by this seat)" |
| TRANSFER (T3⁺)(a) | `STATEMENT.md:120-133` | `lemmas/P1_LEADING.md` P1.7 | base L8.2–L8.3 with P1.4(ii) | "PROVED (by this seat)" |
| IF-START (IF-START⁺) | `STATEMENT.md:176-180` | `lemmas/P1_LEADING.md` P1.8 | base L10.1 with the new rate | "PROVED (by this seat)" |
| OVL (OVL⁺) | `STATEMENT.md:181-189` | `lemmas/P2_OVL.md` | Lemma P2.1 (identity and product bound); 1/π₀(𝓛(Q)) ≤ 2 from (T1⁺)(a) | "PROVED (by this seat)" |
| NEC (T4⁺) | `STATEMENT.md:154-173` | `lemmas/P3_NEC.md` | counting Lemma P3.1; witness outside the block of S₀; Example P3.3 | "PROVED (by this seat)" |
| BR (B-R⁺) | `STATEMENT.md:147-152` | `lemmas/P4_BR.md` P4.1 | step-by-step record that base L9.1–L9.6 never use \|Q\| | "PROVED (by this seat)" |
| START-R (T3⁺)(b) | `STATEMENT.md:134-145` | `lemmas/P4_BR.md` P4.2–P4.3 | case distinction at each n in place of ϱ̄_n → 0 | "PROVED (by this seat)" |

Unchanged claims of version 1.3.4 (AGG, ASM, NEC-b, FLOOR, the bridges (B1), (B-TK), (B-L), (B-V1), (B-V2), F1, F3, F4,
MIS, the examples table) are not restated and not re-proved (`STATEMENT.md:41-45`).

## 4. Assumptions (ids), dependencies and relations to existing results

| id | name | where stated | shared | bridge |
|---|---|---|---|---|
| A:START2-R-L | (L-R⁺): localised bounded leakage, \|Q\| ≤ K only | `STATEMENT.md:63-73` | new; (L-R) [A:START-R-L] implies it | (B-R⁺) |
| A:START-E, A:START-GF, A:START-V, A:START-AL | energy; unnormalised Gram floor; visibility ((V-c) or (V-m)); averaged leakage | BASE `STATEMENT.md:135-157` | existing ids of the base ticket | base bridges |
| A:START-R-FL, A:START-R-V | population floor; population visibility | BASE `STATEMENT.md:160-162` | existing ids of the base ticket | (B-R⁺) |
| A:BLOCK-LE-16, A:EX-A | partition a function of X with blocks ≤ 16; exact arithmetic | BASE `STATEMENT.md:169-172` | existing ids | — |

**Consumed** (base ticket, by statement or by cited proof step): W3-START:AGG, W3-START:FLOOR, W3-START:TK,
W3-START:LEAK, W3-START:VIS-c, W3-START:VIS-m, W3-START:NEC-b, and the proof files BASE `lemmas/L1`–`L10`. Their status
is recorded by the base ticket and by HQ (`STATEMENT.md:205-210`); the claims of this ticket can be accepted only after
the base ticket is.

**Supersession by implication** (each new claim implies the base claim of the same name; reasons in
`STATEMENT.md:215-224`): START-F, F2, TRANSFER, IF-START, OVL, NEC, BR, START-R. LEAK-0 is new and supersedes nothing;
W3-START:LEAK stays in use for U_Q.

`implies` relations to interface properties (as in the base ticket): START-F and START-R with Q = S₀ ⇒ A:P-START
(IF-START⁺); OVL⁺ ⇒ A:P-OVL in the production form when limsup(E_n − max(1, log p/log n)) < 0.

## 5. Sharpness record

| item | reading | evidence |
|---|---|---|
| leading rate n^{−1/2}·𝔏^♯_n(h) | sharp in order when 𝔏^♯_n(h) = O(1): o₀ ≥ T₁ ≥ ½(n + 1)^{−1/2} on every data set (T0), and 𝔏^♯_n(h) ≥ (p − s₀)/(4p) | `lemmas/P1_LEADING.md` P1.1, P1.6(v) |
| ε-dependent constant in (T1⁺)(d) | NECESSARY-FOR-ROUTE: the cut-off for the exceptional columns grows as the allowed failure probability decreases; exp(Z²/2) has infinite expectation | `lemmas/P1_LEADING.md` P1.3, Remarks |
| s₀ = 0 keeps 𝔏⁰_n(h) | NECESSARY-FOR-ROUTE: every null is exceptional and there are p of them | `lemmas/P1_LEADING.md` P1.3, Remark (4) |
| visibility in OVL⁺ | used only for π₀(𝓛(Q)) → 1 | `lemmas/P2_OVL.md` P2.2, P2.3 |
| 17 − s₀ leaking nulls in (N2⁺) | NECESSARY-FOR-ROUTE: a block can hold S₀ and 16 − s₀ nulls, for which (C2)(i) conditions on S₀ and the gain is 0; whether fewer nulls suffice is open | `lemmas/P3_NEC.md` P3.3, Remark (3) |
| constant c > 1 + 2Ā in (N2⁺) | as in the base (C2)(i) | BASE `lemmas/L7_NEC.md:14-26` |
| size of Q in (T3⁺)(b) | no restriction; the display is trivial when (\|Q\| + 1)n^{−1/2}e^{C_R√log n} ≥ 1; an informative bound beyond that is not claimed | `lemmas/P4_BR.md` P4.2, P4.4 |
| \|H_l\| ≤ (log n)^{κ_Q} | NECESSARY-FOR-ROUTE: the count N_ref of reference pairs | `lemmas/P4_BR.md` P4.1 |

## 6. Numerics (observations, not proofs)

`numerics/falsify_P.R` (output `numerics/out_P.txt`; base R; exact enumeration with the base ticket's helper): Lemma
P2.1(b) on 3000 random positive tables and 300 data sets scored with the transcribed scorer; the facts P1.1 on 60
random designs by numerical integration of J_h; the two counting facts (P1.2(a), Lemma P3.1) on 20000 random and
adversarial partitions; Example P3.3 (eigenvalues, the formula for δ²_{V,l}, the premise) for s₀ ∈ {1, 2, 8, 9, 15}.
No violation. Not tested: the probability bound of Lemma LEAK-0 (its constant e^{2κ_E+1} makes a simulation
uninformative) and P4 (a case distinction on top of base results).

## 7. Open items

* W3-START2-O1: a partition-free leaking-null limit with fewer than 17 − s₀ nulls when s₀ ≤ 15 (or a proof that none
  holds).
* W3-START2-O2: an informative lattice bound under Gaussian rows when (|Q| + 1)·n^{−1/2}·e^{C_R√log n} does not tend to 0;
  reference sets H_l beyond polylogarithmic size; sharpness of e^{C_R√log n}.
* W3-START2-O3: a sharper leading functional for s₀ = 0; a fixed constant in (T1⁺)(d).
* Inherited from the base ticket and unchanged: a Gaussian-row bridge to (V-m); necessity of (GF-16); growing s₀;
  non-Gaussian noise; response-selected targets.

## 8. Files (all under `Theory_work/Wave3/W3-START2/`)

`STATEMENT.md` (v1.4.1), `PLAN.md`, `BRIEF.md`, `REPORT.md`, `citecheck.py`; `lemmas/P1_LEADING.md`, `lemmas/P2_OVL.md`,
`lemmas/P3_NEC.md`, `lemmas/P4_BR.md`; `numerics/falsify_P.R`, `numerics/out_P.txt`. Outside the frozen content: `LOG.md`,
`CHECKPOINT_*.md`, `reviews/`.
