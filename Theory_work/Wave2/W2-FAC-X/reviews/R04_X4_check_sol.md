# R04 — Cross-family key-lemma check of X4

**Verdict: VERIFIED-WITH-AMENDMENTS.**

**FATAL: none. MAJOR: none.** The amendments below are local proof repairs; none requires strengthening locked STATEMENT v3, claim (C2), or changing its perturbation scale. The literal assertion “on 𝔊_n” needs the probability-one restriction in issue 2. I found no positive-probability counterexample to (C2), no escaping band defect under the stated approximate rule and X3 hypotheses, and no circular use of a future path step.

Scope: checked `STATEMENT.md` v3, `X4_path.md` (line numbers below refer to the reviewed 262-line version), all of X1–X3, FAC-B L3/L4 and STATEMENT §1, and N1X/N3X. X1–X3 are inputs **as stated**, not independently certified here. Numerics are evidence only. A short Python calculation checked the false Mills-ratio inequality in issue 1; no simulation was used as a proof. Only this review file was written.

## Numbered issues and required fixes

### 1. MINOR — X4.0, lines 35–41: the stated Mills-ratio inequality is false; count means also need consistent notation

The parenthetical assertion

    Φ̄(t)/Φ̄(t+h) ≤ exp(h(t+h))

is false. For example, t=0 and h=0.001 give a left side approximately 1.0007985216 and a right side approximately 1.0000010000. The hazard rate at zero is √(2/π), not zero. Also the tail count has mean `m_all F`, not `pF`; the window count has mean `m_all q`, although `pq` is a legitimate upper bound.

**Fix.** Use a correct hazard bound, for example

    φ(u)/Φ̄(u) ≤ u+1  (u≥0),
    Φ̄(t)/Φ̄(t+h) ≤ exp(h(t+h+1)).

Consequently, with h=10ϖ,

    q(t) ≤ 20ϖ(1+t) exp(h(t+h+1)) F(t).

The extra factor tends to one uniformly on the grid. Split the proof using `μ=m_all F`: if μ≥log³n, Chernoff gives tail count ≥μ/2, while the window count is at most `e² m_all q + 3 log n + 1 ≤ ε′μ/2` eventually. If μ<log³n, then `m_all q ≤ n^(−c_w)` eventually, and the same T₀ argument works. For m_all=0 the event is automatic. This avoids both the incorrect Mills step and the unstated replacement of a binomial mean. The union bound is valid; include the O(n^−3) failure probability for each window upper bound, as well as the tail lower bound. No exponent or constant in the conclusion needs to change.

### 2. MINOR — X4.0/X4.2/X4.7, especially lines 82, 104–108 and 258–260: the nondegeneracy event must actually be intersected

X3 assumes distinct null coordinates and `ξ_l≠x_i`. X4.7 acknowledges probability-one nondegeneracy but 𝔊_n and Lemma X4 never incorporate it. Thus the literal deterministic assertion on **every** point of 𝔊_n is false.

A configuration on the listed events is p=2, s₀=1, N=∅, η=0, both ξ coordinates zero, a=0, φ²=N=n−3, W=NI, and ‖e‖²=σ²(n−1). Take any nonzero truth coefficient satisfying the locked hypotheses. For large n this satisfies D1–D8 and E′_n, using FAC-B's regime-(S) conventions. Yet x₀=0 equals the kept null coordinate, so a₀=−∞, b₀=+∞, and the kept null lies in (a₀,b₀). The left inclusion of (4.1) fails immediately. This is a measure-zero witness, not a probabilistic counterexample to (C2).

**Fix.** Intersect 𝔊_n with

    ND_n = {distinct null ξ's; ξ_l≠x_T for every null l and every S₀⊆T⊆[p]}.

For fixed n these are finitely many nontrivial linear equalities in ξ,η after conditioning on φ; their union has probability zero. This single event works for every N. At K=∅ use the extended endpoint convention directly; do not invoke X3(i), which assumes a nonempty kept set. No strict uniqueness of deletion gains is required.

### 3. MINOR — Corollary X4.1, lines 68–73: justify the uniform `3H̄` envelope before using it

The quoted X2.1 bound is only `|x_T|≤(1+ℓ)H̄`. It does not by itself imply either `H̄+|x_T|≤3H̄` or `|ξ_j−x_T|≤3H̄−1` for arbitrary fixed ρ. Both are used in the corollary, whose fixed coefficient 6C_X makes this more than a purely cosmetic omission.

**Fix.** Derive the sharper bound from the exact reference centre. Put d=N/φ²∈[1/2,2] on D3 for large n, so κ=d/ℓ² and ϱ=dη/ℓ. For k≥1,

    |x_T|/H̄ ≤ (kℓ²+dℓ)/(kℓ²+d) ≤ 3/2.

Indeed `(kℓ²+d)/2−d(ℓ−1) = kℓ²/2−dℓ+3d/2 > 0` for k≥1 and d≤2 (the quadratic has negative discriminant). Hence `H̄+|x_T|≤2.5H̄` and `|ξ_j−x_T|≤2.5H̄≤3H̄−1` eventually, since H̄→∞ even for bounded p. Proposition X2 then gives `max|δ|≤3ϖ/4` exactly as budgeted. The same envelope covers the null statistics in (g5).

### 4. MINOR — X4.4, lines 186–196: retain the log-log remainder and state the one-move perturbation budget

Multiplying the displayed envelope `H̄²(1+2.2ε_b)` by 1/2 produces `(1+2.2ε_b)L_n`, rather than the `L_n` displayed at line 191. The missing positive `2.2ε_b L_n` cannot be placed in o(1). The final bound with `O(L_n)` is sound.

Also, the swap comparison at T∖j uses an exceptional set of size at most 16, and its addition statistic at T∖j∪l uses at most 17; these are within Proposition X2, but not literally the size-15 hypothesis of Corollary X4.1.

**Fix.** Write `O(L_n)` in the intermediate addition inequality. State that the same absorption calculation, with `#Band+17` unchanged, gives `|δ|≤ϖ` at every required one-move set. At T∖j the centre bound becomes `1.01ε_bH`; its squared envelope can use `1+2.3ε_b` for sufficiently large n. Then `2.3ε_b A₁≤0.23(1/2−A₁)`, leaving ample margin for the stated `−0.6(1/2−A₁)log n` comparison. No claim of no-addition on general structured sets is needed or justified.

### 5. MINOR — X4.5, lines 203–234: make the end-phase induction and imported error budget explicit

The mechanism is valid, but the compressed transfer obscures two details that should be stated in a high-stakes proof.

First, (a)–(c) use the approximate deletion rule at the **current** step. These statements must be applied to the hypothetical deletion of the current best-deletion candidate j°, after deriving its rule from the already established exact structure, and before proving that this candidate is the actual best move. Otherwise the phrase “the deleted null” can be read as assuming the conclusion of B4/end-phase comparison.

Second, the stated input (g5) bounds its last normalization error by `C H̄⁴ max(ω²)`. With `ω²=O(H̄²/n)`, the bound available directly from that input is `O(H̄⁶/n)`, rather than the `O(H̄⁴/n)` in line 223. It is still o(1).

**Fix.** At an established end-phase state, represent its exact hole with width **zero** (so #Band=0 in the sense of X2), apply Proposition X2 and the gain-ordering argument to j°, and then prove (a)–(c) conditionally on deleting j°. Use

    O(ϖH̄ + ϖ² + H̄⁶/n + 1/n) = o(1)

for the perturbation transfer unless the sharper error is separately derived. Copy or restate FAC-B's definitions `I=N₊−N₋`, `h=H̄²`, `s_K=IH̄+E`, and `|E+B|≤e_n=O(L_n)`. In particular,

    H̄/m₁ ≫ δ_e+ϖ,

which justifies the strengthened E-side comparison. Use D3's `κ=κ_∞(1+O(n^(−1/3)))` when transferring c_D; the coarse interval `[κ_∞/2,2κ_∞]` alone would not preserve the displayed c_D. These additions prove the stated margins without changing them.

### 6. MINOR — X4.6, lines 244–249: retain the ρ-dependent projection constant and explain the truth extension of (g2)

The cited X2.1 bound is `q_U≤2p(1+ℓ)²H̄²/N`, not the displayed `4pH̄²/N`. Also X1 explicitly restricts (g2)'s stated null formula and reserves truth moves for X4. The ridge/OLS comparison can indeed be extended, but its ω² identification must not be used for a truth deletion.

**Fix.** Replace 4 by `C_ρ`. For a truth-out swap write the difference through U explicitly:

    Q_T′−Q_T = (Q_T′−Q_U)−(Q_T−Q_U).

For the first difference apply the ridge/OLS partial-regression identity at U to truth j. Its coefficient-norm bound holds because U contains S₀. For the second apply the null identity to l at U (or use zero for a deletion). Both have the same exact multiplier n/(n+1); their OLS values are O(n) since yᵀy=n−1. Thus

    Q_T′−Q_T = [n/(n+1)](RSS_T′−RSS_T)/s² + O(n^(−1/2)) ≥ c′n.

The raw Gram lower bound is uniform by D1, the noise projection bound is uniform by the full-model q bound, and s² is bounded above and below on the design/noise event (derive this for the fixed truth set from X1.1 and D1–D4 if not recording it as a standing consequence). This proves negativity uniformly over every T⊇S₀, without a union bound over T and without (FS).

### 7. MINOR — header and X4.7: use the locked claim label

The header and §X4.7 refer to claim “(X2)”. In locked STATEMENT v3 the path claim is **(C2)**; X2 is the perturbation lemma. Replace the obsolete labels.

## Dependency and mechanism audit

The following checks explain why none of the issues above is FATAL or MAJOR.

### Events, regimes and all-N uniformity

E′_n imports **FAC-B L3's conventions**, including E5–E7 being sure events outside regime (L), and E4 being vacuous for m_all=0. Consequently bounded p is covered: it would be incorrect to require an actual (m₁+16)-th observation in regime (S), but that is not the inherited convention. It is advisable to repeat this convention in X4.0.

In (L), replacing m₁ by m₁+16 in E6 and using the larger δ_e is legitimate. For E7, use cells of length L_n/4 as in L3. Their means are at least L_n(m₁+16)/2. Once these exceed 64, `P(count<16)≤exp(−mean/8)` suffices; union over O(H/L_n+1) cells and both signs tends to zero. Removing any 15 points leaves a point in every relevant interval. The retained extreme order-statistic lower bound also survives every such removal. The harmless enlargement of the gap constant covers the merged gaps and the top tail width.

D8(L) has the correct scale: its close-pair probability is

    O(ϖ(1+H̄)m₁² exp(c₁ϖH̄)) = o(1).

The y_n threshold is positive and well defined eventually in (L). D8(S) costs `O(p²ϖ)=o(1)` uniformly for p≤n^(1/200), including the n^(−1/3) floor. D7 survives the repair in issue 1 because ϖH̄ is polynomially small and T₀ is a fixed constant depending on A₁. Neither D7 nor D8 is conditioned on a selected N.

Every event is defined on the deterministic all-null sample; X2 covers all interval locations and all exceptional sets of size ≤17. Thus there is no omitted union over O(p^15) starts, and no independence assumption concerning random N₀. The proof applies pathwise to every allowed N, then to the X-measurable N₀.

### Established prefixes and the bulk induction

At step i≤i_e, only the established prefix of length I=i is supplied to X3. Its steps have m≥m₁≥3; the final state need not have m≥m₁. The common concentration event gives Q/m₀→0, so the initial-phase hypothesis is uniform in N. Therefore (4.1) at i precedes, rather than depends on, the current rule. The correct order at a bulk state is:

1. Established prefix → (4.1) and its D6 band count.
2. B3(i−1), prefix narrow/wide alternatives and E6 → B1(i).
3. B1(i), B1(i−1), previous rule and prefix structure → B2(i).
4. B2(i), (4.1), D7 and full-sample E5 → B3(i).
5. Structure → approximate rule for best-deletion candidate; B3(i), X2 and X1 gains → B4(i), hence the next actual deletion.

The table in X4.2 is consistent with this order despite B3 being printed before B2 and B1 in the exposition. In B1's narrow branch all previous deletions remain near x₀; in its wide branch only the **previous** rule and B3(i−1) are used to exclude loss of a singleton side. No future rule is assumed.

In Case A of B3, the only negative terms lost from the symmetric top set are deleted negatives in the exterior band. D7 controls them by `ε′(m+15)+T₀`, because points farther than 9ϖ into that tail are kept except for N. E5 on the full top-J″ set then gives J″≤5m and the stated K₁ estimate. The negative-x branch is the simultaneous sign reversal of coordinates and offset.

In Case B, `w·#(−w,0)≤C(pw²+w log n)=o(1)`. Here `pϖ²=O(p²H̄² log n/n+p n^(−2/3))=o(1)` uses A₁<1/2. Thus the displayed lower bound on the deleted sum and m≥m₀/4 are justified, not additional assumptions.

B4's closest-point bound uses descending absolute order statistics, so deleting N can only lower the m-th largest value. The FAC-B deletion computation remains valid with ε_b≤1/50 and p≤n^A₁. Additions at visited T are controlled by the global null envelope and the small centre; the strict A₁<1/2 assumption supplies their log-n margin. For swaps, no-addition is proved separately at T∖j using its explicit centre drift and its size-16/17 exceptional sets. This does not import the false assertion of no-addition on arbitrary interval-hole sets.

### Small regime, end-phase entry, propagation and endpoint

In (S), use X3(ix) on the established prefix to obtain exact structure at T_i; then obtain the current candidate's approximate rule from X2. Spacing excludes crossing and forces the candidate to be an edge point. The crude statistic bound is below 0.1 log n eventually for every fixed ρ; the extra ℓ√(2L_n) term is negligible relative to √log n. The stated deletion/addition/swap separation follows, including endpoint additions. There is no need for sign balance in this regime.

At end-phase entry, (4.1) is supplied by the completed bulk prefix, not by an end-phase move. Case B would force m≥m₀/4 and is impossible there. For finite b>0, D7 bounds the window [b,b+w), while all points beyond b+w are kept except N. Thus at most 2m₁ all-null positive values exceed b. D8 places b in the separated extreme tail and eliminates every possible upper band defect. The lower side is symmetric; an infinite endpoint contributes no band. This proves the exact hole at entry.

For later states, after the current candidate rule has been obtained as in issue 5, (a) excludes crossing, (b) forces edge deletion using extreme-tail spacing, and (c) propagates the exact hole. FAC-B's centre estimate also gives `H̄−|x|≫δ_e`, so sign classes and sides of the centre coincide throughout this phase, including one-sided states. The kept magnitudes therefore remain extreme top sets. E-side lowers |I| whenever it is nonzero and keeps `c_I≤2ε_b+o(1)` when |I|≥2. E-del, E-add and E-swap retain their log-n margins after the stated o(1) perturbation repair. Sample κ need only be replaced by κ_∞ with its D3 o(1) error, not treated as deterministically ≥κ_∞.

The truth-move repair in issue 6 establishes a uniform O(n) loss independently of all path geometry. After exactly m₀ deletions the state is S₀; all additions and truth-removing neighbours are strictly worse. The production tie rule causes no difficulty: all best-move maximizers are null deletions and each satisfies the approximate rule. FAC-B's single-search prefix property then gives certification with a_n≥m₀ and the stated legacy-cap failure.

### Constants and falsification outcome

ε_b is fixed after choosing A₁; K₁=100/ε_b², m₁=⌈K₁L_n⌉ and T₀=O((1/2−A₁)^−1) are compatible. In particular T₀/m₁→0, `10x_(5m)/m≤11/K₁` eventually, and `c_D>0` for s₀≥1, κ_∞>0. The onset may be extraordinarily large; N1X does not test that onset or these constants.

A₁<1/2 is used in X2's stated second-order control, the band absorption `pH̄√(log n/n)→0`, Case B's `pϖ²→0`, and the bulk addition margin. The truth-move argument itself only needs pH̄²=o(n). D7/D8 require a positive polynomial decay exponent and are compatible with the chosen floor. All thresholds and bounds can be chosen uniformly in N.

The attempted on-event falsification found the measure-zero defect in issue 2. With ND_n included, the assumed X3 prefix conclusions prevent an exterior defect from escaping (4.1); D8 removes remaining end-phase defects. I found no configuration satisfying these repaired event conditions that defeats the best-deletion comparison. N1X's 121/121 paths and N3X's zero reported violations support plausibility but are not used to establish any implication above.

**Disposition:** implement issues 1–7 before marking the written proof checked. No FATAL/MAJOR obstruction to locked (C2) was found.
