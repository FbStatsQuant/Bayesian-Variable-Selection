# T5 Fable card (consistency tier): Thm 9 (`W3-DIST:Thm-A`), with Thm 9B, Cor 9C and the DIST-1/2/3 chain

Inputs: packet; Astra (4 points); blind Sol (3 points); walk `walks/T5.md` on walkA (4 NOTEs, WALK COMPLETE). Snapshot: `origin/theory/PRE-LEAN` 6850c3a5. **For the consultant: answer AGREE or OBJECT per row.**

**Verdict:** Theorem 9 holds as stated; no display, constant or event in the presented statement changes. Two commentary sentences inside recorded statement spans overclaim (R1, R2), one convention needs to be written down (R4), and one proof-file amendment has a measurability slip that an existing lemma already fixes (R3). All four are one-sentence edits to `W3-DIST`, so one re-freeze covers them.

## 1. Rulings on the Codex points

| # | Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|---|
| R1 | Astra T5-1: DIST-2 says its best squared radius is ≍ (1 + s₀^r)·log n·ℓ_n/n; the proof constants give (1 + s₀^r)³ | AGREE | **Wording overclaim** (sparsity dependence of a constant). For fixed s, which is the theorem's regime, nothing changes. | **Yes:** `W3-DIST:DIST-2`, `STATEMENT.md:96-97` (commentary sentence, not display (1.2)). The reader already says cubic (`READER_VERSIONS.md:1208-1211`). | Replace "Best rate ε_n² ≍ (1 + s₀^r) log n · ℓ_n/n: one logarithm slower than DIST-1 at polynomial p." by "Best rate, for fixed s₀^r: ε_n² ≍ log n · ℓ_n/n, one logarithm slower than DIST-1 at polynomial p. As proved, its constant is at most of order (1 + s₀^r)³ for fixed (A, σ*², M, M′) (an upper bound, not known to be tight; `lemmas/X.md` §9, `lemmas/DIST12.md` D.6)." |
| R2 | Astra T5-2 and Sol T5-1 (found independently): "Equivalently" before the radius-only display of DIST-1 | AGREE | **Wording overclaim** (one connective). The radius-only display follows from (1.1) but does not give back the size clause. | **Yes:** `W3-DIST:DIST-1`, `STATEMENT.md:78`. | Replace "Equivalently, for every sequence ε_n" by "In particular (dropping the size clause), for every sequence ε_n". |
| R3 | Astra T5-3: B3's amendment A-2 intersects the item-6 event with {p_ret = p}, which need not be measurable in the completed pair | AGREE | Genuine but local slip in a proof-file amendment; the conclusion stands | **No** (`work/E_bridges/B3.md:98-103`; the B3 span `STATEMENT.md:409-414` does not mention the completion). Affects Thm 9B only. | In A-2 replace "The event 𝒜′_n is intersected with {p_ret = p} (which holds on the event of B1)." by "𝒜′_n is redefined as the set of outcomes on which the completed pair below satisfies the conditions of Step 6, with m♯_n computed from (n, p, s) and a replacement truth with exactly s nonzero coordinates; it is measurable in the completed pair and contains 𝒜_n (as in `W3-D3/lemmas/B3w.md` (c))." |
| R4 | Astra T5-4, Sol T5-2, walk N1: the displays evaluate the posterior on data where it is not defined; "r = p outside them" is true for the proof's common exceptional set, not for the set in display (i) read literally | AGREE | Convention not written down; **not a flaw** (the proof's exceptional set has probability ≤ n^{−cM} and contains {r < p}) | **Yes, wording only:** `W3-DIST:Thm-A` premises span, `STATEMENT.md:150-152`. Same sentence in the reader, `READER_VERSIONS.md:1065-1067`. | Replace "are counted in them (in particular r = p outside them)" by "are counted in them: there the posterior probabilities in the displays are read as 1. The common exceptional set of the proofs also contains every data set with r < p." Reader: the same sentence with "p < p_raw". |
| R5 | Sol T5-3: Lemma S's cutoff uses log R with R = 0 | AGREE, Lean-only | Not a flaw (log 0 = −∞ is the stated convention) | No | No paper change. Lean states the cutoff in product form, R·√D_T·√n·exp(C[1 + √t + t/√n]) ≤ e^{−2t}, and treats R = 0 first. |

Notes:
- **R1.** I confirmed the count: C_m is linear in s (`X.md:34`), so C_x′, C_P′, Λ′, C_Q′ and C_{X′} are linear; D.6 squares C_{X′}; M₀′ = max{16, (A+1)s} adds one more factor. DIST-1's own linear claim (c) is correct, because C_X does not depend on s. I decline Astra's alternative (re-proving a linear bound): complexity growth.
- **R2.** Nothing downstream uses the reverse direction: the Theorem A assembly consumes (1.1) itself.
- **R3.** `W3-D3:B3w` (c) already contains the correct construction; this aligns the older DIST file with it.

## 2. Rulings on the walk rows

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Fix |
|---|---|---|---|---|
| N1: exceptional set on inadmissible data | AGREE | Convention | Yes, wording (see R4) | R4 |
| N2: n₀ thresholds are written out; n₀ is very large because c₂ = 10⁻⁵ | AGREE | Lean note | No | None |
| N3: Thm 9B takes δ_n → 0 from Thm 1 item 6; a direct route exists through `W3-POST2:C` case (i) | AGREE | Simplification (same as T4 N6) | No | Lean-only route |
| N4: Cor 9C's second sentence is a statement about the code's store | AGREE | Scope note | No | None. In Lean the store invariant is a hypothesis, as in T2 and T3. |

**Left uncovered by the walk** (it is marked complete):
- By its own statement, the code-reading lemmas behind Cor 9C's second sentence (which models are offered to the store: P6_DISTC Lemmas M, R, R0) were read at the cited lines but not re-audited.
- The walk recomputed DIST-2's constants but did not compare them with the sparsity sentence at `STATEMENT.md:96-97`; Astra's R1 fills that.

## 3. Correctness (beyond Codex and the walk)

Nothing further. Presented Theorem 9, the card row and Cor 9C's display are unaffected by R1–R5.

## 4. Lean readiness (ranked; no item changes a presented statement)

1. **State Theorem 9 with an explicit success event.** There is a measurable set G_n of data sets with P*(G_n) ≥ 1 − n^{−cM} such that on G_n the data are admissible, r = p, Π(d_H > √(M log n/n)) ≤ n^{−cM} and Π(|S| > s + C₁M) ≤ n^{−cM}.
   - Gain: no posterior on inadmissible data; displays (i), (ii) and "the same exceptional set" follow at once; it is exactly the G_n that Cor 9C consumes.
   - Cost: the fidelity check must accept this as the paper's "In words" reading.
2. **Three layers for Theorem A.** Deterministic: Lemma H (T3). Fixed-design: Lemma X as "on a noise event, the posterior mass of the bad set is ≤ e^{−t/2}". Design: bridges B1, B2-core, B2.
   - Level-2 named axioms: the Lemma T transfer inequality (growth-function bound, a VC-type fact); Laurent–Massart χ² tails; Gamma tails; sub-Gaussian concentration for B1 and the net bound for B2-core; the marginal-likelihood identity of `lem:num`.
3. **Cor 9C at Level 1** from item 1 and the finite-sum transfer of T3 item 1; exact arithmetic and the store invariant enter as hypotheses.
4. **Thm 9B from the expectation form** (N3), with the completed pair of B3w (c) (R3). Gain: no diagonal argument. Named axioms: as T4 item 1.
5. **Lemma S cutoff in product form** (R5).
