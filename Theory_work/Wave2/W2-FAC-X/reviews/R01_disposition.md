# R01 disposition (statement lock, Codex gpt-6.1-sol high — verdict REJECT)

1. **X3 counterexample.** Accepted as a counterexample to PLAN v1's informal X3(c),(d) (no density hypothesis).
   Repair: lemmas/X3_softgap.md (vii) carries an explicit density hypothesis — every interval of length 9ϖ holds ≤ Q
   points and 4Qϖ/(|K_0| − Q − 1 + κ′) ≤ ϖ/10 — under which the narrow-hole (crossing) phase has ≤ Q steps and the centre
   moves by ≤ ϖ/10 during it. R01's configuration has all M + 2 points within 7.5ϖ (Q ≍ |K_0|) and violates it. On the
   Gaussian event D6 (lemmas/X2), Q ≤ 18e²pϖ + 3 log n + 1 = o(m₀) in regime (L), so the hypothesis holds w.h.p.
   Tolerance reconciled: rule (R_ϖ) is |ξ_j − x| ≤ d + 2ϖ throughout (STATEMENT (C2)(i), X3, X4). Band width now 4.3ϖ.
   Falsification: numerics/N3X_out.txt (288 runs with adversarial ϖ-approximate policies; 0 violations of the crossing
   bound and of the containment whenever the (vii) hypothesis holds).
2. **No family-wide no-addition.** Accepted (R01's construction is FACB L4.5(3)'s phenomenon). STATEMENT (C2)(ii) now
   claims additions only at visited T; X4 bounds additions at T and at the swap intermediates T ∖ j using the centre
   bound |x_T| ≤ ε_bH (B3, proved for visited sets) and the drift identity |x_{T∖j} − x_T| ≤ 3H̄/(m₁ − 1); in the end
   phase swaps use FACB's direct swap quantity V through the exact identity X1.4 (g5).
3. **Normalisation / absolute errors.** Fixed: first-order term −(B₀⁻¹Rc)_j with R = W_T/N − I (STATEMENT §0, PLAN X2).
   X1.4 gives absolute bounds: determinant increment e¹ ≤ 3/(c₀n), ridge remainder |r| ≤ Cn^{−3/2}(1 + P⁰), the
   (1 + q) ratio ε^d ∈ [0, 2ω²], M_T ∈ [½(1 − 3q − Cn^{−1/3}), ½(1 + C/n)], and X4.1 converts them into the gain-ordering
   slack C_g n^{−1/2}. STATEMENT §3 says explicitly that the reference is an RSS analogue of FACB's centre, not FACB's
   ridge score reduction.
4. **Random partition / N₀.** STATEMENT §1 and X4 prove the path claim simultaneously for all N with |N| ≤ 15 on events
   over the deterministic null set; E-events are stated for 𝒩_all and transferred to 𝒩* = 𝒩_all ∖ N with explicit
   deterministic errors (≤ 15H̄ in top sums, ≤ 15 in counts); E1 is not imported for N₀; X2 separates the diagonal term
   and the scalar x_T, uses Gaussian conditioning only for ξ-defined sets, crude uniform bounds for band/N₀ sets;
   zero-pair bounds for (C1) conditionally on X (lemmas/X5).
5. **s₀ ≥ 1, (FS′).** s₀ ≥ 1 explicit; (FS) restated as a finite population condition; (FS′) removed from the claims
   (it would be a hypothesis on the random partition), listed in §5.
6. **Frontier algebra.** STATEMENT §5 now states the band term's ratio to the budget, C·p·H̄·√(log n/n), and calls
   leave-one-out a possible approach only. A < ½ is advertised only as this proof's range.
Optional: 1 (keep representation as first lemma) — done; 3 (labels, symbols) — claims renamed (C1)–(C4), perturbation
scale renamed ϖ; 2, 4 — adopted in X4's phase split and in N1X's wording.
