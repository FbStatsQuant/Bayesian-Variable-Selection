# T4 Fable card (consistency tier): Thm 1, Thm 1′, presented Thm 2

Inputs: packet; Astra (2 points); blind Sol (3 points); walk `walks/T4.md` on walkA (6 NOTEs, WALK COMPLETE). Snapshot: `origin/theory/PRE-LEAN` 6850c3a5. **For the consultant: answer AGREE or OBJECT per row.**

**Verdict:** no flaw in the mathematics of any of the three theorems. One recorded statement needs a one-clause definedness fix (R1). Two Codex points are already answered by records outside their packets (R2, R5). The walk is complete and leaves nothing uncovered.

## 1. Rulings on the Codex points

| # | Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|---|
| R1 | Astra T4-1: `h(S₀)` undefined when S₀ ∉ Ω (item 4 carried to the joint law by item 6) | AGREE | Definedness gap, not a wrong claim | **Yes:** `W3-POST:Thm-1` item 4, `W3-POST/STATEMENT.md:86`. Inherited by Thm 1′ item 6. Not in the reader theorem or the card; Thm2SG uses items 1–3 only. | Replace `sup_{h:Ω→[0,1]} \|π(h) − h(S₀)\| = O_P(r_n)` by `sup_{h:2^{[p]}→[0,1]} \|Σ_{S∈Ω}π(S)h(S) − h(S₀)\| = δ_n for every data set, hence O_P(r_n)`. |
| R2 | Astra T4-2: reader says coefficient control is "necessary (explicit counterexample)" | **OBJECT** | Neither | No | No change. Optional pointer at `READER_VERSIONS.md:163`: "(explicit counterexample: Proposition C)". |
| R3 | Sol T4-1: weakened-floor proofs reuse locked lemmas whose stated hypotheses include the stronger SE | AGREE, Lean-only | Not a flaw | No | No text change. Lean restates each reused [P3] bound with the hypotheses it actually uses (same as walk N3). |
| R4 | Sol T4-2: B3w introduces m♯_n "computed with p_ret", undefined where s₀ > K_cap | AGREE | Definedness wording | **Yes:** `W3-D3:B3w`, `W3-D3/STATEMENT.md:61-62`, and proof `lemmas/B3w.md:24`. Thm2SG's statement is untouched. | Replace "(computed with p_ret and s₀)" by "(computed with (n, p, s₀), as in (c); on 𝒜_n, p_ret = p)". Apply only if W3-D3 is reopened; Lean uses the deterministic cutoff either way. |
| R5 | Sol T4-3: the T03♯ record admits p = 1, the proof assumes p ≥ 2 | **OBJECT** | Not a flaw | No | No change. Lean states 2 ≤ p, as Theorem 1 (R1) and (S2) already do. |

Reasons, where the ruling is not self-evident:
- **R1.** The new form equals the old wherever the old was defined, and equals 1 = δ_n when S₀ ∉ Ω (take h = 1_{S₀}). It is the convention C-PACK already records (`I4_SL_corollaries.md` §0, R34 #3). I recommend CORRECTION-ONLY, but it edits a registry span, so the route is yours and the consultant's.
- **R2.** `W3-PSHARP:C@1.0.0` (PROVED-CHECKED) is exactly that counterexample. Its text says Remark 2 of Lemma 1a′, "recorded as open, is settled: removal fails" (`W3-PSHARP/STATEMENT.md:141-144`). Astra's packet held only the older Remark 2.
- **R4.** The mathematics is fine: m♯_n is used only on 𝒜_n, where p_ret = p and s₀ ≤ K_cap, and part (c) already uses the cutoff from (n, p, s₀).
- **R5.** Already ruled in the record itself: `W3-T03ACC/STATEMENT.md:99-103` (§4 item 4, SL1 ruling) covers p = 1 by the signal-gain argument on S = ∅. That span was outside Sol's packet (:1-80).

## 2. Rulings on the walk rows

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Fix |
|---|---|---|---|---|
| N1: second form of (A6) is a limit, but the display says "at that n" | AGREE | Wording imprecision in the reader; the master `W3-POST2:C` is right | No (reader prose, `READER_VERSIONS.md:109-110, 121-122`) | In (A6) replace "or θ*_min√(n/log n) → ∞" by "or θ*_min ≥ σ_*√(M_n log n/n)/φ₀ for a fixed sequence M_n → ∞"; in the closing parenthesis replace "the divergence of θ*_min√(n/log n)" by "the sequence (M_n)". Bundle with the Sol-2 reader edit. |
| N2: n₀ is never written out | AGREE | Lean note | No | None. The twelve thresholds of walk §5.4 become explicit Lean hypotheses. |
| N3: T03♯ and Thm 1-OS are proved by diff against [P3] | AGREE | Lean note (same as R3) | No | None. Walk §3–4 give the flattened order. |
| N4: s₀ ≤ K and S₀ ⊆ [p] are not listed in the reader statement | AGREE | Convention | No | None. Lean defines S₀ = supp θ* on retained columns (as `W3-POST` §0) and assumes s₀ ≤ K at that n. |
| N5: reader Thm 2 reads p as retained (random); the master uses the raw count | AGREE | Reading of p | No (the master is correct) | Optional, reader (A1) of Thm 2: append "(p counts the columns of X^r; with probability tending to 1 none is removed)". Lean uses the raw count. |
| N6: item 6's diagonal transfer has a constructive replacement | AGREE, promoted to Lean item 1 | Simplification | No | Lean-only route; paper proof unchanged. |

**Left uncovered by the walk:** nothing. It covers [P1] preliminaries, the size tail, T03♯, the primed steps, Prop ER case (i) and (iii), Thm 1′, B3w, item 6, the assembly and ExSG.

## 3. Correctness (beyond Codex and the walk)

Nothing further. I re-checked the two places a ruling depends on:
- N6's route is valid: on 𝒜′_n the completed pair meets the hypotheses of `W3-POST2:C` case (i) at that n with BM-∞ and the common envelope, so E[δ°·1_{𝒜′_n}] ≤ C·r_n, and Markov plus P(𝒜′_nᶜ) → 0 gives tightness.
- R1's identity holds on every outcome, as stated above.

## 4. Lean readiness (ranked; no item changes a presented statement)

1. **Thm 2 from the presented Thm 1, not from item 6.** Thm2SG ⇐ B3w + `W3-POST2:C` case (i): expectation bound on 𝒜′_n, Markov, add P(𝒜′_nᶜ).
   - Gain: removes the proof by contradiction over sequences of designs and the O_P black box.
   - Cost: Lean-only. Named axioms: B1 (variance concentration for sub-Gaussian coordinates) and B2-core (sparse quadratic-form lower bound), unless proved.
2. **Make the expectation form the Lean headline, at a single n.** Parameters (s₀, A, σ*², M, φ₀, g₀, and c or the envelope M_n); the thresholds of walk §5.4 as hypotheses. The O_P, HPM/MPM and PIP clauses then follow from Markov and SL0 (T2).
   - Gain: no "eventually", no tightness definitions. Cost: none.
3. **Flatten the chain into five lemmas, each with its own hypotheses:** size tail → good event → supersets → underfits → assembly (R3, N3).
   - Gain: no locked-proof diffing inside Lean. Cost: blueprint work only.
4. **Level-2 named axioms for the chain** (one file per source):
   - Laurent–Massart χ² tails;
   - Gaussian tail with a union bound;
   - a Gaussian projected on a rank-d subspace is σ²χ²_d;
   - the truncated χ² moment bound of (C5);
   - the marginal-likelihood identity E₀[m_b(S)/f₀] = 1 (or the closed form, December target 4);
   - Cauchy interlacing, if Mathlib lacks it (I did not check).
5. **Conventions fixed once:** 2 ≤ p (raw count), S₀ on retained columns, m♯ as a function of (n, p, s₀), h on 2^{[p]} (R1, R4, R5, N4, N5).
