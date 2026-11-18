# W3-MEMO-SCR-RM — can certified screening supersede RM's leakage condition?

Lead: Claude Fable 5.2 (claude-personal, high). 2026-11-11. **Version 1 (before review B1).** Scoping memo: it states
no new theorem. Every sentence carries one of three tags. **[SRC]** = a registered claim, cited by id@version
(`Theory_work/INFRA/registry/claims.tsv`; all W3-SCR:* and W3-RM:* rows are 1.0.0, ACTIVE). **[DED]** = deduced here
from registered claims in a few lines (lead only). **[SK]** = sketch, not proved. Notation: 𝐋_n := 2 log p + log n;
ϑ_n := 2 log p/𝐋_n (= 2A/(2A+1) when p = n^A); ℓ_n = ⌈log₂(n+p+1)⌉; Ŝ = `fit$hpm`; "sparse" = |Ŝ| ≤ q_n;
NF(q): φ_n(q) ≥ ϑ_n + ε, the floor of SCR-C (`W3-SCR/STATEMENT.md:171-178`).

## 0. Answer

**No supersession, and no strengthening of RM's range.** Three reasons.

1. SCR-C is a statement about the score landscape: with probability → 1, S₀ is the only locally optimal (LO) model of
   size ≤ q_n [SRC W3-SCR:L5.2, SCR-C]. It says where a search can *stop*. It does not say that a coded search *enters*
   the sparse region, nor that it stops there before its move cap. Both are needed for P(certified ∧ sparse) → 1.
2. Under SCR-C's own hypotheses that probability claim is the discovery of S₀ (§1, I3). For the LS0 half it is
   **false on a proved class that satisfies SCR-C's hypotheses** (§1, I2). So it cannot be derived from them through
   LS0; what is left is an open full-method (sampler) claim.
3. Where the SCR landscape can replace the lattice condition (N), it does so only for |S̃₀ ∖ S₀| ≤ 0.72 log n under
   the shipped cap [SK, §2 ML2]. (N-χ) already covers |Q ∖ S₀| ≤ (1 − δ₀) log n with no floor.

**HQ's prior is confirmed in substance, with three corrections.** (i) "SCR-C needs s₀ = O(1)" does not separate the
two: RM-F and RM-R also fix s₀ (`W3-RM/STATEMENT.md` §1). (ii) P(certified ∧ sparse) → 1 is not *exactly* RM's claim.
It is the discovery claim; RM's sandwich-plus-descent is one sufficient mechanism for it, and under RM's hypotheses it
is a corollary (I1). (iii) NF is not only "violated by correlated designs": it also *implies* every floor RM uses
(I5), so the two hypothesis sets are incomparable rather than nested.

**Recommendation: (a)**, with one cheap rider (Corollary CERT, §4). Not (b). (c) only on a trigger.

## 1. Hypothesis sets side by side, and which implies which

| | SCR-A / A1, SCR-G (screening) | SCR-C (exact) | RM-0 (core) | RM-F / RM-R |
|---|---|---|---|---|
| Setting | fixed standardised design, Gaussian errors; s₀, p free in SCR-A | same; **s₀ = O(1)**, ‖θ*‖₂ = O(σ√n), q_n log p = o(n) | any design, deterministic Q ⊇ S₀ | fixed design / Gaussian rows; s₀ fixed, p ≤ n^A, σ fixed |
| Signal | SV(q): Γ_n(q) above (τ_n√𝐋_n + σ√(2q log p))². A1: θ_min ≥ b, ‖θ*‖₁ ≤ M | as SCR-A | — | BM-∞ (in T1-F); BM-Q beyond (N-χ); fixed [θ_lo, θ_hi] in R |
| Design | DF(q) ⇐ AF(q) ⇐ SF(q+s₀): a floor only where a truth is missing | + **NF(q_n)**: λ_min ≥ ϑ_n + ε on every S ⊇ S₀, \|S\| ≤ q_n | — | T1; FL-16, FL-Q (any φ₀ > 0); **(V)**; **(L)** \|Q\| ≤ (log n)^κ; **(N)** / (D-R) |
| Start, search, sampler | none | none | events Sand(Q), NA(𝓛), TL(𝓛); [POST]; [E4] | supplied by bridges B1–B9 |
| Premises | EX-A | EX-A | EX-A, EX-S, SR, GUARD-W, OP-LS0 (shipped config), complete scans, E4 hyps | same |
| Conclusion | P(𝒪 ∩ cert ∩ sparse ∩ S₀ ⊄ Ŝ) → 0; G: near-best scanned centres and capped returns ⊇ S₀ | P(𝒪 ∩ cert ∩ sparse ∩ Ŝ ≠ S₀) → 0 | 𝒪 ∩ {Ŝ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ | P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 |
| P(conditioning event) | **not claimed** (`W3-SCR/STATEMENT.md:217`) | not claimed | — | not needed (P(𝒪) → 1 not claimed) |

**I1 — RM's good event implies the certificate [DED].** On 𝒢′_n := Sand(Q) ∩ NA(𝓛) ∩ TL(𝓛) ∩ {π(S₀) > ½}, every
completed admissible run has `local_certified = TRUE`, `local_certified_by ∈ {ls0, both}` and Ŝ = S₀. Proof: LS0's
archive has `returned` = S₀ and is certified [SRC W3-RM:RM-0, clause (a) [P7]]; π(S₀) > ½ makes S₀ the unique
F-maximiser on Ω, and S₀ is in the ledger, so `hpm` = S₀; the flag rule `cert_ls0` (`Scripts/SMC_BVS/core/v3_run.R:193-194`;
[SRC W3-SCR:CC, CC2]) then returns TRUE. On the enumeration branch status `exact` gives the flag directly. Hence under
RM-F or RM-R: P(𝒪 ∩ {not certified, or Ŝ ≠ S₀}) → 0. RM's [P7] stops at the archive; the step to the public flag is
this memo's and needs a code check of the `identical(...)` comparison.

**I2 — the converse fails: SCR-C's hypotheses do not give the event through LS0 [DED].** Take exact-Gram compound
symmetry with K < p ≤ n − 1 (FAC-PK's class: (CS), (θ), (PK), (PB)) and ρ ≤ 1/3 − ε. Every principal Gram submatrix
has λ_min = (1 − ρ)(n − 1), so SF holds on all sets with κ = 1 − ρ and, coefficients being fixed, A1 gives SV(q_n)
for q_n = o(n/log n); ϑ_n < 2/3 gives NF(q_n). So SCR-C applies [SRC W3-SCR:SCR-C, A1]. On the same class, with
probability → 1: every start-mode maximiser has size K [SRC W2-FAC-PK:P1@1.0.0]; LS0 under the shipped cap never
scores S₀ [SRC W2-FAC-PK:Thm-NEG@1.0.0]; and the uncapped path would end at S₀ [SRC W2-FAC-PK:Thm-PATH@1.0.0], so the
capped LS0 is a strict prefix of it and its archive is uncertified. There `local_certified` = `cert_final`: the event
{certified ∧ sparse} is entirely a statement about the SMC and the final search, which is open
[SRC W2-FAC-PK:P6@1.0.0, "numerical, pending"]. General mechanism: nulls that stay visible given ≤ 15 others force a
saturated or near-full start mode [SRC W2-APP:VN@1.0.0, Gaussian rows], and NF permits such nulls (it allows
order-n gains at every column).

**I3 — what the missing event means [DED].** Take SCR-C's hypotheses in the A1 form (fixed κ, b, M, σ), p ≤ n^A and
q_n ≥ s₀ + max(j₀, m♯_n) (m♯_n = O(log n)). Then NF(q_n) gives every item of T1-F (energy from ‖θ*‖₁ ≤ M; SE_λ(j₀)
and SE_w from the floor on supersets of S₀; BM-∞ from θ_min ≥ b), hence [POST] [SRC SOP:TH09@1.0.0 through
W3-RM:RM-F (B6)]. With probability → 1, S₀ is then the unique F-maximiser, so on 𝒪: {Ŝ = S₀} = {S₀ was scored}; and
{certified ∧ sparse} ⊆ {Ŝ = S₀} by SCR-C, the two differing only when S₀ is first scored as the returned model of a
capped search (covered by SCR-G(ii)). So **"P(certified ∧ sparse) → 1" = "S₀ is discovered, and not at a cap"**. In
this regime SCR-C adds no reported-model conclusion that [POST] plus discovery does not already give. Its content is
different: it turns two *printed* quantities into the conclusion, with no start, sampler or configuration premise.

**I4 — RM's hypotheses give SV only at bounded size, and never NF [DED].** T1-F's SE_λ(j₀) bounds the anchored floor
φ^a_n(q) ≥ φ₀² for q ≤ j₀ = ⌈(2A+1)s₀⌉ + 1; with BM-∞ and ‖μ‖² ≤ Mn, Lemma B2 [SRC W3-SCR:B2] gives Γ_n(q)/log n → ∞,
so (A∞) holds for each fixed q ≤ j₀. Beyond j₀, RM's floors live on Q ∪ {l} and on ≤ 16-sets only, and say nothing
about a truth masked by a larger set outside Q. RM's floor constant φ₀² is arbitrary; NF needs ϑ_n + ε ≥ 2/3. So
RM-F ⇒ SCR-A at q = j₀, and RM-F ⇏ SCR-C. (Form R: the same on the realised X with probability → 1 [SK].)

**I5 — NF implies RM's floors, not (V), (L) or (N) [DED].** Principal submatrices inherit λ_min, so NF(q) ⇒ FL-16
(q ≥ 16 + s₀), FL-Q (q ≥ |Q| + 1), SE_λ, SE_w, each with φ₀² = ϑ_n + ε. NF ⇏ (L): I2. NF ⇏ (V): (V) asks every truth
to be visible given any ≤ 15 columns, and one truth can be cancelled marginally by another truth with a larger
opposite coefficient at correlation ≤ 1 − φ; SV survives because it takes the *best* missing truth. NF ⇏ (N): NF is
an ℓ² (eigenvalue) condition; (N-D)/(N-loc)/(D-loc) are direction-count and ℓ¹ conditions.

**Summary.** {SV, NF} and {(V), (L), (N), T1, FL} are incomparable. RM ⇒ certificate fires (I1). SCR-C ⇏ RM's
conclusion (I2). The overlap is the near-orthogonal, no-leak corner (§3).

## 2. The exact missing links for supersession

Target: "SV + NF, no (L), no (N) ⇒ P(𝒪 ∩ {Ŝ ≠ S₀}) → 0." By SCR-C this is equivalent to P(𝒪 ∩ {uncertified or
|Ŝ| > q_n}) → 0, up to cap-edge cases (I3). It splits into three links.

**ML1 — sparse entry.** Some coded search must have a scanned centre of size ≤ q_n − r.
* LS0 side: |S̃₀| ≤ q_n − r. **False in general under SCR-C's hypotheses** (I2). True when a sandwich holds; only its
  *size* consequence is used — neither S₀ ⊆ S̃₀ (phase 1 below re-adds truths) nor, for random designs, a
  deterministic Q. In fixed design "few leaking columns" *is* (L) with Q := S₀ ∪ {leaking columns}, so (L) cannot be
  removed there, only its size enlarged. Best route: RM2's sandwich at |Q| ≤ n^b (junk-exclusion margin loses b log n,
  `W3-RM/reviews/R02_better_theorem_astra.md:196-204`); for random designs the counting form of leakage
  (`W3-RM/ASSUMPTION_MAP.md`, last paragraph of "Why Form R…"). Difficulty: MEDIUM (inside RM2) / HIGH (counting form:
  the selection problem).
* Final-search side: the SMC's best model is sparse and close to S₀. This is a sampler claim (W3-SAMP:D plus a start
  mass), not a screening claim. Difficulty: HIGH on dense-leak designs; it is Decision D1.

**ML2 — reach S₀ inside the cap.** From an entry centre C₀ with m₀ extras, sizes staying ≤ q_n:
* Phase 1 (truths missing) [SK]: SCR-M gives a truth-addition gaining ≥ c₂n at every such centre, and no truth is
  ever dropped [SRC W3-SCR:SCR-M (M2, M5), SCR-G(iii)]. The whole F-range over sparse models is O(n) under A1's
  constants, so phase 1 lasts O(1) moves. Difficulty: LOW.
* Phase 2 (strict supersets of S₀) [SK]: the SCR-C event gives *an improving deletion* at every sparse strict
  superset, not "deletions only". L5.1's Steps 1–3 are an average over the excess set; read quantitatively (Jensen
  on the log), the best deletion gains ≥ (ε/2φ)𝐋_n(1 − o(1)). The total available is F(S₀) − F(C₀) ≤ m₀·½𝐋_n(1 + o(1)).
  So the path makes ≤ C·m₀ moves, **C = (φ/ε)(1 + o(1))**, wherever it wanders among sparse supersets. This is the
  budget device of [SRC W2-FAC-PK:L3.4@1.0.0] and the "quantitative potential argument" that R02 P6(c) says is missing
  for (N) (`R02_better_theorem_astra.md:236`). Difficulty of this lemma ("PL"): LOW–MEDIUM, 2–3 proof days.
* **What PL buys under the shipped caps.** C − 1 ≥ ϑ_n/ε ≥ ϑ_n/(1 − ϑ_n) = 2 log p/log n. LS0's slack beyond m₀ is
  ℓ_n + s₀, so PL certifies only m₀ ≤ ℓ_n/(C − 1) ≤ 0.72 log n (for p ≥ n); the final search (cap ℓ_n) even less.
  (Only in the corner p ≤ n^{0.72} can the bound, 0.72(log n)²/log p, pass (N-χ)'s log n.) Larger m₀ needs C → 1, which *is* deletion-only descent, i.e. NA on the visited sets — the open problem behind (N)
  (W3-RM `SHARPNESS.md` §4). Or a cap c·|S̃₀| with c > φ/ε: a method change, outside PROGRAM's scope.
* On RM's own lattice (no NF) [SK]: restricting L5.1 to E ⊆ Q ∖ S₀ replaces log C(p − s₀, m) by log C(|Q|, m); for
  log|Q| = o(log n) the inequality then fails under FL-Q alone, with C = 1 + O(log|Q|/(φ₀² log n)). In-lattice
  additions and swaps become harmless when m₀ log|Q| ≲ φ₀²(log n)². What remains is NA only for columns l ∉ Q
  ("exit control"), still a supremum over the whole lattice. This narrows (N); it does not remove it. Difficulty: HIGH
  (it is R02 P6); record it as input to the kill-budgeted path-level ticket.

**ML3 — the certified endpoint is the reported model.** Given [POST], immediate (I3). LOW.

**Verdict.** ML1 fails without a leakage-type condition; ML2 is range-limited by the cap to where (N-χ) already
works. Neither (L) nor (N) is superseded.

## 3. Regimes (conditions on (X, θ*); families only as examples)

| Regime | Condition | SCR-C gives | RM gives |
|---|---|---|---|
| **A. SCR only** | NF(q_n) and SV(q_n) hold; and either the set of columns with gain > ητ²_U log n is not polylogarithmic, or some truth fails (V) while SV holds, or p is not polynomial in n | conditional exact recovery: certified ∧ sparse ⇒ Ŝ = S₀; SCR-G for capped runs. **No** P(Ŝ = S₀) → 1 | nothing ((L), (V) or p ≤ n^A fails) |
| **B. RM only** | (V), (L), (N) hold; some superset of S₀ of size ≤ q_n has λ_min < ϑ_n + ε | screening only (certified ∧ size ≤ j₀ ⇒ Ŝ ⊇ S₀), and (EC′) on the excess | P(𝒪 ∩ {Ŝ ≠ S₀}) → 0, and the certificate fires (I1) |
| **C. Both** | NF and no leakage outside a small Q | as A, plus: both archives, every seed, any cap, `ls0 = FALSE`, EX-A only | as B |
| **D. Neither** | dense leakage and λ_min < ϑ_n + ε near S₀ | screening if SV holds | nothing; Decision D1 |

Examples. A: equicorrelation with ρ < 1/(2A+1) (FAC-PK's class at ρ < 1/3); a realised incoherent design with
non-Gaussian rows and a strong signal (Form R does not apply, and the sample (L-gain) with a small Q is not expected
to hold — a heuristic, `W3-RM/STATEMENT.md` §6 last item) [SK].
B: UNI-0 families with strong local correlation, LOC-BF, GEN (C6)'s proxies. C: exact-Gram orthogonal-type designs;
iid Gaussian rows. D: strong factors and equicorrelation ρ ≥ 1/(2A+1) at p > K.
Two cautions. NF's constant rises to 1 as log p/log n grows, so regime A shrinks with p; under the tie-break
(design-agnosticism > range of p) this counts against any theorem built on NF. And NF is sufficient only: on exact
compound symmetry the "no LO strict superset" conclusion holds for every ρ ∈ (0, 1) [SRC W2-FAC-PK:Thm-PATH].

## 4. Recommendation

**(a) SCR-C as a corollary and examples row — recommended**, with one rider:
* **Corollary CERT (new, cheap; I1).** Under RM-F or RM-R, with probability → 1 on 𝒪 the run is certified (by LS0)
  and Ŝ = S₀. Half a page from RM-0(a) [P7], CC2 and [POST]; one Sol check against `v3_run.R:174-200`. It applies
  verbatim to anything proved through RM-0, RM2 included. It closes SCR's "not claimed" bullet inside RM's regime.
* SCR-C is stated as the exact-recovery corollary of Theorem 5, and the examples table gets a certificate column
  with three values: *fires provably* (RM's rows), *implies ⊇ S₀* (SV), *implies = S₀* (NF).
* **Headline:** unchanged. Theorem 3 stays "(V) + (L) + lattice condition"; Theorem 5 stays certified screening. One
  sentence joins them: Theorem 3 is the a-priori guarantee, Theorem 5 with SCR-C the a-posteriori certificate, and
  under Theorem 3's conditions the certificate fires.

**(b) Merge into W3-RM2 with a named lemma — not recommended.** The only candidate is PL (§2). At |Q| = n^b its move
bound is C·m₀ with C > 1 fixed, which exceeds the shipped cap's slack ℓ_n + s₀; SCR-M's TL adds nothing to RM's B3.
So no SCR lemma delivers RM2's key lemma, and RM2's kill budget (3 attempts) should not be spent on it. **Headline
if done anyway:** RM2's exponent b unchanged; one more alternative lattice hypothesis at sub-polynomial size.

**(c) A new ticket — only on a trigger.** If W3-P6 shows {certified ∧ sparse} at frequency ≈ 1 on regime-A or
regime-D designs, open "sparse entry through the final search" (sampler side), with SCR-C as its last step.
**Headline if it succeeded:** a reported-model theorem with no leakage condition under NF — narrower in design and
in p than Theorem 3, so a second theorem beside it, not a replacement. Today ML1 has no route there.

## 5. Open points (what review B1 should attack)
1. I1: the flag step (index order in `identical(...)`; enumeration branch) is unchecked against the code.
2. I2: that FAC-PK's hypotheses are compatible with ρ < 1/3, and that "uncapped path ends at S₀" makes the capped
   archive uncertified.
3. I3: the item-by-item derivation of T1-F from NF (m♯_n = O(log n) is my estimate from GROW (H0)).
4. ML2: PL is a sketch; the constant C = φ/ε and the 0.72 log n comparison rest on leading-order bookkeeping.
5. The recommendation would change if PL could be sharpened to C = 1 + o(1) under NF (then NF would replace (N) up to
   polynomial sizes), or if a size-only sandwich were proved under NF without a leakage condition (I2 says it cannot,
   for LS0).
