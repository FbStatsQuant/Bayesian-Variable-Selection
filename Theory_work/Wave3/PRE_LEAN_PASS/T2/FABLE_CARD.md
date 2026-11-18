# T2 Fable card: posterior summaries SL0 (`C-PACK:SL0@1.0.1`) + pooling bound LT-d (`W3-SAMP:LT#@2.0.6`)

Snapshot: `origin/theory/PRE-LEAN` 3d94ad40. Astra: NO-FLAW, 0 points, no evidence trail.

**Verdict:** no flaw. Both proofs hold as stated, with their constants. No statement change and no proof change proposed.

## 1. Rulings

None to make (Astra returned 0 points).

## 2. Correctness (focused check, done by hand because Astra left no trail)

**SL0** (`I4_SL_corollaries.md:21-37`). All of (i)–(v) follow from one fact: for any event B ⊆ Ω, |π(B) − 1_B(S₀)| ≤ δ.
- (i), (ii) first part, (v): direct instances. With s₀ > K, δ = 1 and each is trivial; in (v) the set is empty and 0 ≥ 1 − 1.
- (ii) h-part: π(h) − h(S₀) = Σ_{S≠S₀} π(S)(h(S) − h(S₀)) uses Σπ = 1 and S₀ ∈ Ω, both stated. The supremum δ is attained at h = 1{S ≠ S₀}.
- (iii): j ∈ S₀ gives PIP_j ≥ 1 − δ > q; j ∉ S₀ gives PIP_j ≤ δ < q. Vacuous when s₀ > K, since min(q, 1 − q) ≤ ½ < 1 = δ.
- (iv): π(S) ≤ δ < ½ < π(S₀) for S ≠ S₀, so the maximiser is unique and the tie rule is irrelevant.
- (vi) is outside the Lean core; its two-point law and the D0 remark are also correct.

**LT-d** (`STATEMENT.md:134-135`, `LT_theorem.md:53-60`).
- Convex combination: |¼Σ_r(p̂_r(j) − 1{j∈S₀})| ≤ ¼Σ_r|…| ≤ max_r ‖p̂_r − 1_{S₀}‖_∞. Correct.
- MPM inclusion: j ∈ S₀ with pip ≤ ½, or j ∉ S₀ with pip > ½, each gives an error ≥ ½. The tie at ½ is covered.
- Constants: o₁ ≤ ¼ and κ₀ ≤ o₁ give κ₀ + 2·(1/8) ≤ ½. LT-b at ε = 1/8 gives 8δ/η + 8λ₀ ≤ 8δ/η + 8·19·o₁ = 8δ/η + 152·o₁. The sum over 4 islands is a union bound.
- HPM clause: δ < ½ gives F(S₀) > F(S) on Ω∖S₀, and S₀ ∈ 𝓜 ⊆ Ω, so the maximum of 𝓜 is S₀.
- Code facts the clause leans on, read at the source:
  - `hpm_better` compares F first and breaks only exact ties (`cpp/v3_util.h:121-126`), so it is a strict total order that refines F.
  - `pip_primary` is `rowMeans` over the islands and `mpm` uses strict `> 0.5` (`v3_run.R:162-163`).

**Two observations, no action on LT-d:**
- The hypothesis "o₁ ≤ ¼" is harmless but never binding: the bound exceeds 1 as soon as o₁ ≥ 1/608.
- `W3-SAMP/STATEMENT.md` says "Production core on main = 4676af6". Main's core has since moved (the list-PIP commits). The lines LT-d cites are untouched: the drift hunks in `v3_run.R` are at :119 and :216 onward. The sentence itself is stale wording for whoever next touches that file.

## 3. Lean readiness (ranked)

**Level-2 named axioms: none for items 1–4** (Level 1). No item changes a paper statement.

1. **One master lemma for SL0.** For a probability π on a finite type and a point a: ∀B, |π(B) − 1_B(a)| ≤ 1 − π(a).
   - Take π on all subsets of [p]; then "π(S₀) := 0 when s₀ > K" is just the value of π, with no case split and no subtype for Ω.
   - Gain: (i), (ii) first part and (v) become one-line instances. Cost: a thin corollary restating them in the paper's Ω form, so the fidelity check reads MATCH.
2. **(ii) h-part without a TV library.** Prove "≤ δ·osc(h)" from the displayed sum, and state the supremum as two facts: ≤ δ for every [0,1]-valued h, and = δ at h = 1{S ≠ S₀}.
   - Gain: no dependency on a total-variation definition. Cost: "TV(π, point mass)" stays a prose label.
3. **LT-d pooling as a pure vector lemma.** For v₁..v₄ and t in ℝ^p: ‖¼Σv_r − t‖_∞ ≤ max_r‖v_r − t‖_∞, and {j : v_j > ½} ≠ S₀ ⇒ some |v_j − 1{j∈S₀}| ≥ ½.
   - `pip_primary := ¼Σ p̂_r` is a Lean definition; CC3 is a code fact and stays outside Lean.
   - Gain: no sampler objects. Cost: none.
4. **HPM clause without formalising the tie rule.** Hypotheses: Ŝ ∈ 𝓜; no S ∈ 𝓜 is better than Ŝ; F(S) > F(T) ⇒ S better than T; S₀ ∈ 𝓜; F(S₀) > F(S) for S ≠ S₀. Conclusion: Ŝ = S₀.
   - Gain: skips the size-then-lex order and its totality proof. Lemma PC and CC2 enter as hypotheses, not axioms. Cost: none.
5. **MPM probability bound: keep out of Lean this round.** If wanted later at Level 2, it is a three-line implication with LT-b, κ₀ ≤ o₁ (ST-b) and λ₀ ≤ 19·o₁ as the named hypotheses.
