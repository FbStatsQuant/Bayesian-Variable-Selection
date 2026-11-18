# W3-MEMO-SCR-RM — can certified screening supersede RM's leakage condition?

Lead: Claude Fable 5.2 (claude-personal, high). 2026-11-11. **Version 2 = version 1 revised after review B1**
(gpt-6-astra, high: REJECT as written, recommendation (a) kept; `reviews/B1_review_astra.md`,
`reviews/B1_disposition.md`). The changes are listed in §6 and are **not re-reviewed**. Scoping memo: it states no new
theorem. Tags: **[SRC]** a registered claim, by id@version (`Theory_work/INFRA/registry/claims.tsv`; all W3-SCR:* and
W3-RM:* rows are 1.0.0, ACTIVE); **[DED]** deduced here in a few lines; **[DED✓]** the same, confirmed by B1;
**[SK]** sketch, not proved. Notation: 𝐋_n := 2 log p + log n; ϑ_n := 2 log p/𝐋_n; ℓ_n = ⌈log₂(n+p+1)⌉;
Ŝ = `fit$hpm`; "sparse" = |Ŝ| ≤ q_n; NF(q): φ_n(q) ≥ ϑ_n + ε for a fixed ε > 0 — the floor of SCR-C
(`W3-SCR/STATEMENT.md:171-178`). Since φ_n ≤ 1, NF forces log p/log n ≤ (1 − ε)/(2ε): p is polynomial in n.

## 0. Answer

**Supersession is not established, and nothing in the present results gives it. It is not shown impossible.**

1. SCR-C is a statement about the score landscape: with probability → 1, S₀ is the only locally optimal (LO) model of
   size ≤ q_n [SRC W3-SCR:L5.2, SCR-C]. It says where a search can *stop*. A reported-model theorem also needs a
   *discovery* statement: some coded search scores S₀. SCR-C contains none.
2. The proposed bridge, "P(certified ∧ sparse) → 1", is that discovery statement in other words (I3). SCR-C's
   hypotheses do not give it through LS0: on a proved class satisfying them, LS0 never scores S₀ (I2). Whether the
   full method does there is open.
3. The SCR landscape does suggest a way to do without the lattice condition (N): a potential argument (PL, §2). As
   sketched it works under the shipped cap only when the *realised* start has ≤ (1/(2 log 2) + o(1)) log n extras.
   That case is new only when the start is small inside a large or unknown envelope Q; it is a candidate, not a result.

**HQ's prior: confirmed in substance; three corrections.** (i) "SCR-C needs s₀ = O(1)" does not separate the two
theorems: RM-F and RM-R also fix s₀. (ii) Under SCR-C's hypotheses "P(certified ∧ sparse) → 1" is the discovery
claim; RM's sandwich-plus-descent is one sufficient mechanism for it, not the claim itself, and under RM's hypotheses
it is a corollary (I1). (iii) NF is not only "violated by correlated designs": on the sets it covers it *implies*
every fixed-design floor RM uses (I5). The two hypothesis sets are incomparable, not nested.

**Recommendation: (a)**, with Corollary CERT as a rider, and the two PL sketches handed to the already planned
path-level ticket. Not (b) now. (c) only on a trigger (§4).

## 1. Hypothesis sets side by side, and which implies which

| | SCR-A / A1, SCR-G (screening) | SCR-C (exact) | RM-0 (core) | RM-F / RM-R |
|---|---|---|---|---|
| Setting | fixed standardised design, Gaussian errors; s₀, p free in SCR-A | same; **s₀ = O(1)**, ‖θ*‖₂ = O(σ√n), q_n log p = o(n) | any design, deterministic Q ⊇ S₀ | fixed design / Gaussian rows; s₀ fixed, p ≤ n^A, σ fixed |
| Signal | SV(q): Γ_n(q) above (τ_n√𝐋_n + σ√(2q log p))². A1: θ_min ≥ b, ‖θ*‖₁ ≤ M | as SCR-A | — | BM-∞ (in T1-F); BM-Q beyond (N-χ); fixed [θ_lo, θ_hi] in R |
| Design | DF(q) ⇐ AF(q) ⇐ SF(q+s₀): a floor only where a truth is missing | + **NF(q_n)** on every S ⊇ S₀, \|S\| ≤ q_n (general form: (EC′) violated, L5.2) | — | T1; FL-16, FL-Q (any φ₀ > 0); **(V)**; **(L)**, \|Q\| ≤ (log n)^κ; **(N)** / (D-R); block-relative forms also allowed |
| Start, search, sampler | none | none | events Sand(Q), NA(𝓛), TL(𝓛); [POST]; [E4] | supplied by bridges B1–B9 |
| Premises | EX-A | EX-A | EX-A, EX-S, SR, GUARD-W, OP-LS0 (shipped config), complete scans, E4 hyps | same |
| Conclusion | P(𝒪 ∩ cert ∩ sparse ∩ S₀ ⊄ Ŝ) → 0; G: near-best scanned centres and capped returns ⊇ S₀ | P(𝒪 ∩ cert ∩ sparse ∩ Ŝ ≠ S₀) → 0 | 𝒪 ∩ {Ŝ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ | P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 |
| P(cert ∧ sparse) | **not claimed** (`W3-SCR/STATEMENT.md:217`) | not claimed | — | not needed; follows (I1) |

**I1 — RM's good event implies the certificate [DED✓; code path checked by B1].** There is a data event
𝒢′_n := Sand(Q) ∩ NA(𝓛) ∩ TL(𝓛) ∩ {π(S₀) > ½}, of probability → 1 under RM-F or RM-R, on which every admissible
output run reports Ŝ = S₀ with `local_certified = TRUE`; on completed SMC runs the certification includes LS0
(`local_certified_by ∈ {ls0, both}`); the enumeration branch certifies by status `exact`. Proof: LS0's archive has
`returned` = S₀ and is certified [SRC W3-RM:RM-0, (a) [P7]]; π(S₀) > ½ makes S₀ the unique F-maximiser, so `hpm` = S₀;
then the flag rule (`Scripts/SMC_BVS/core/v3_run.R:179, 193-195`; `v3_exact.R:15`; [SRC W3-SCR:CC, CC2]). Equivalently
P(𝒪 ∩ {uncertified or Ŝ ≠ S₀}) → 0. This is neither P(certified) → 1 nor a limit conditional on 𝒪: delivery is not
controlled.

**I2 — SCR-C's hypotheses do not give discovery through LS0 [DED✓].** Take exact-Gram compound symmetry with
K < p ≤ n − 1 (FAC-PK's class: (CS), (θ), (PK), (PB)) and ρ ≤ 1/3 − ε. Every principal Gram submatrix of size ≥ 2 has
λ_min = (1 − ρ)(n − 1), so A1 holds with κ = 1 − ρ and q_n = o(n/log n), and ϑ_n < 2/3 gives NF(q_n): SCR-C applies.
On the same class, with probability → 1: every start-mode maximiser has size K [SRC W2-FAC-PK:P1@1.0.0]; LS0 under
the shipped cap never scores S₀ [SRC W2-FAC-PK:Thm-NEG@1.0.0]; the uncapped path ends at S₀
[SRC W2-FAC-PK:Thm-PATH@1.0.0], so the capped LS0 is a strict prefix and its archive is uncertified. There
`local_certified` = `cert_final`, and both {Ŝ = S₀} and {certified ∧ sparse} are statements about the SMC and the
final search. **That half is open, not refuted** [SRC W2-FAC-PK:P6@1.0.0, "numerical, pending"]. So: SCR-C alone
supplies no discovery theorem, and the LS0 route to one fails on this class; no more is shown. Mechanism: nulls that
stay visible given ≤ 15 others force a saturated or near-full start [SRC W2-APP:VN@1.0.0, Gaussian rows], and NF
permits such nulls.

**I3 — what the missing event means [DED✓].** Take SCR-C's hypotheses in the A1 form (fixed κ, b, M, σ) and
q_n ≥ s₀ + max(j₀, m♯_n), m♯_n = O(log n). Then NF(q_n) gives every item of T1-F (GROW (H0)), hence [POST]
[SRC SOP:TH09@1.0.0 through W3-RM:RM-F (B6)]. On the resulting good event S₀ is the unique F-maximiser, so on 𝒪
{Ŝ = S₀} = {S₀ was scored}; and {certified ∧ sparse} ⊆ {Ŝ = S₀} by SCR-C. The two differ exactly when S₀ is first
scored as the returned model of a capped search and is not rescanned: then Ŝ = S₀ with the flag FALSE. So in this
regime **the reported-model target needs only "S₀ is scored"**, and "P(certified ∧ sparse) → 1" asks for that plus
"not at a cap". SCR-C adds no reported-model conclusion that [POST] plus discovery does not give. Its content is
different: two *printed* quantities yield the conclusion, with no start, sampler or configuration premise.

**I4 — RM's hypotheses give SV at bounded size and do not imply NF [DED✓].** T1-F's SE_λ(j₀) gives the anchored
floor φ^a_n(q) ≥ φ₀² for q ≤ j₀ = ⌈(2A+1)s₀⌉ + 1; with BM-∞ and ‖μ‖² ≤ Mn, Lemma B2 [SRC W3-SCR:B2] gives
Γ_n(q)/log n → ∞, so (A∞) holds for each fixed q ≤ min(j₀, K − 1). Beyond j₀, RM's floors live on Q ∪ {l} and on
≤ 16-sets. Example of RM-F without NF (B1's): p = ⌊n/2⌋, two truths at correlation 0.9 with θ = (1, 1), all nulls
orthogonal, Q = S₀: T1, FL, (V), (L), (N-χ) hold with floor 0.1, while ϑ_n → 2/3. (Form R: the same on the realised
X [SK].)

**I5 — NF implies RM's fixed-design floors; it implies neither (V) nor (L) [DED✓].** Principal submatrices inherit
λ_min: NF(q) ⇒ FL-16 (q ≥ 16 + s₀), FL-Q (q ≥ |Q| + 1), SE_λ, SE_w, as sample floors (not the population FL-R).
NF ⇏ (L): I2. NF ⇏ (V), even with no leakage (B1's example): two truths at correlation 0.2 with θ = (1, −5),
orthogonal nulls, p = ⌊n/2⌋; NF and A1 hold, x₁ᵀμ = 0, so (V) fails at U = ∅. SV survives because it takes the
*best* missing truth. **NF versus (N):** no derivation of (N)/(D-R) from NF is known here, and no non-implication is
claimed ((N) is a disjunction and depends on Q).

**Summary.** {SV, NF} and {(V), (L), T1, FL, (N)} are incomparable (I4, I5). RM ⇒ the certificate fires (I1).
SCR-C ⇒ no discovery statement; the LS0 route to one fails on a class; the full-method implication is open (I2).

## 2. What is missing for supersession

Target: "SV + NF (or (EC′) violated), without (L) and/or without (N) ⇒ P(𝒪 ∩ {Ŝ ≠ S₀}) → 0." Given [POST] the
target is discovery: P(𝒪 ∩ {S₀ never scored}) → 0 (I3). **One sufficient architecture** for it has three links; it
is not the only conceivable one (other routes below).

**ML1 — sparse entry with reserve.** A coded search has a scanned centre C₀ of size ≤ q_n − r, where r covers every
addition the path may make later (confinement: all later centres must stay of size ≤ q_n − 1).
* LS0: |S̃₀| ≤ q_n − r. False in general under SCR-C's hypotheses (I2). A sandwich gives it, but only its *size*
  consequence is used: not S₀ ⊆ S̃₀, not a small deterministic Q. Weaker sources of a small start exist and are
  unexplored: the block-relative (L_b); a counting form of leakage in which many columns sit above η_A but few
  enter. Difficulty: MEDIUM in fixed design (extension of Lemma B2), HIGH for random designs (the selection problem,
  `W3-RM/SHARPNESS.md` §3.3).
* Final search: the SMC's best model is sparse and near S₀. A sampler claim (W3-SAMP:D plus a start mass). HIGH on
  dense-leak designs; it is Decision D1. FAC-PK does not refute it.

**ML2 — reach S₀ inside the cap.** From C₀, with m₀ := the number of extras at the first centre containing S₀:
* Phase 1 (truths missing) [SK]: every such centre has a truth-addition gaining ≥ c₂n [SRC W3-SCR:SCR-M, M2/M4];
  the F-range over sparse models is O(n) under A1's constants; so phase 1 lasts O(1) moves and adds O(1) to the size.
  (M5 protects containment only once S₀ ⊆ C; it is not used here.) LOW.
* Phase 2 (strict supersets of S₀) — **potential lemma PL [SK; audited as plausible by B1]**. The SCR-C event gives
  *an improving deletion* at each sparse strict superset, not "deletions only". L5.1's Steps 1–3 average over the
  excess set; with Jensen on the log, the best deletion gains ≥ (ε/2φ)𝐋_n(1 − o(1)) (the factor 1 − o(1) needs
  x′ → ∞, x′ = o(𝐋_n), and the probability bookkeeping redone). The total available is ≤ m₀·½𝐋_n(1 + o(1)). So the
  path makes ≤ C·m₀ moves, **C = (φ/ε)(1 + o(1))**, wherever it wanders among sparse supersets. Same device as
  [SRC W2-FAC-PK:L3.4@1.0.0]; it is the "quantitative potential argument" R02 P6(c) asks for
  (`W3-RM/reviews/R02_better_theorem_astra.md:236`). LOW–MEDIUM, 2–3 proof days.
* **What the cap needs, and what PL gives.** The path has m₀ + (non-deletion moves) + O(1) moves; LS0's slack beyond
  m₀ is ℓ_n + s₀. So the requirement is *additive*: non-deletion moves ≤ ℓ_n + s₀ − O(1). It is weaker than NA on the
  visited sets, and weaker than deletion-only descent. PL's multiplicative bound meets it only if (C − 1)m₀ ≲ ℓ_n.
  Since C − 1 ≥ ϑ_n/ε ≥ 2 log p/log n, that is m₀ ≤ (1/(2 log 2) + o(1)) log n ≈ 0.72 log n for p ≥ n (and
  ≈ 0.72 (log n)²/log p for p < n); the final search, with cap ℓ_n, gets less. This is a limit of the estimate, not a
  lower bound on path lengths.
* **Where PL would be new.** m₀ is the *realised* number of extras; (N-χ) bounds the *envelope* |Q ∖ S₀|. If the
  start is small with probability → 1 but may sit anywhere in a large Q — or in no small deterministic Q at all —
  RM needs NA on the whole lattice (the (N-D) branch), while PL under NF needs nothing about Q. This is the
  candidate strengthening: **"small start + SV + NF ⇒ LS0 certifies S₀", without (V), without (N), without a small
  envelope.** It still needs ML1 in size-only form. When the envelope itself has ≤ (1 − δ₀) log n extras, (N-χ)
  already covers it with no floor.
* On RM's own lattice, without NF [SK; "credible" per B1]: restricting L5.1 to E ⊆ Q ∖ S₀ replaces log C(p − s₀, m)
  by log C(|Q|, m). For log|Q| = o(log n) the average deletion gain is then almost the full penalty under FL-Q alone,
  C = 1 + O(log|Q|/(φ₀² log n)), and in-lattice additions and swaps are charged to the budget when
  m₀ log|Q| ≲ φ₀²(log n)². What remains is exit control: no best move imports a column l ∉ Q, which includes
  additions from deletion bases, still a supremum over the lattice; and TL. This would narrow (N), not remove it.
  HIGH (it is R02 P6).

**ML3 — the endpoint is the reported model.** Given [POST], immediate. LOW.

**Other routes (B1), none complete.** (i) Size-only or block-relative entry plus a confined potential argument —
ML1 + PL above. (ii) Lattice PL plus exit control — above. (iii) Exactness from (EC′)/L5.2 with the pair (α, ω)
instead of NF [SRC W3-SCR:L5.2]: widens the designs for the *landscape* step (on exact compound symmetry it holds
for every ρ ∈ (0, 1) [SRC W2-FAC-PK:Thm-PATH]); entry and cap control are still needed. SCR-M on a special family
and SCR-G improve screening and cover capped returns for containment; neither gives discovery or exactness.

## 3. Regimes (defined by which hypothesis sets hold; families only as examples)

Let 𝐇_C := all hypotheses of SCR-C (SV, NF, s₀ = O(1), the growth and coefficient conditions); 𝐇_A := those of SCR-A
only; 𝐇_RM := all hypotheses of RM-F (partition-free or block-relative form) or of RM-R.

| Regime | SCR side gives | RM side gives |
|---|---|---|
| **A: 𝐇_C holds, 𝐇_RM fails in every form** | certified ∧ sparse ⇒ Ŝ = S₀; SCR-G for capped runs. No P(Ŝ = S₀) → 1 | nothing proved |
| **B: 𝐇_RM holds, NF fails for every fixed ε** | under 𝐇_A at q ≤ j₀ (I4): certified ∧ \|Ŝ\| ≤ j₀ ⇒ Ŝ ⊇ S₀; (EC′) constrains any LO strict superset | P(𝒪 ∩ {Ŝ ≠ S₀}) → 0; the certificate fires (I1) |
| **C: both hold** | as A; also both archives, every seed, any cap, `ls0 = FALSE`, EX-A only | as B |
| **D: neither exactness criterion nor 𝐇_RM is verified** | screening under 𝐇_A | nothing proved; Decision D1. Not a negative result |

Sufficient conditions and examples (each needs the listed side conditions checked; none is a theorem here).
* A: 𝐇_C plus nulls visible given ≤ 15 others at order n (then no small Q exists in any form): exact-Gram
  equicorrelation with ρ < 1 − ϑ_n − ε, i.e. ρ < log n/𝐋_n − ε, on FAC-PK's class. Also I5's example: its truth is
  cancelled at U = ∅, and (V), the block-relative (V_b) and (V-R) all quantify over U = ∅ (`W3-RM/STATEMENT.md` §3).
* B: 𝐇_RM with a strongly correlated superset of S₀: I4's example; UNI-0 families and LOC-BF under their own
  conditions, when the local correlation puts λ_min below ϑ_n.
* C: 𝐇_C ∧ (V) ∧ (L) ∧ (N-χ) ∧ T1 — not "NF and no leakage" (I5's example has both and fails (V)). Example:
  exact-Gram orthogonal-type designs with no cancellation.
* D: equicorrelation with ρ ≥ log n/𝐋_n and strong factors at p > K, unless (EC′) is shown violated.

Two cautions. NF couples the exponent to the margin (log p/log n ≤ (1 − ε)/(2ε)), so regimes A and C shrink as p
grows; under the tie-break (design-agnosticism > range of p) this counts against any theorem built on NF. And NF is
sufficient only for the landscape step (route (iii) above).

## 4. Recommendation

**(a) SCR-C as a corollary and examples row — recommended now**, with one rider.
* **Corollary CERT (I1).** "Under RM-F or RM-R there is a data event of probability → 1 on which every admissible
  output run reports S₀ and has `local_certified = TRUE`; on completed SMC runs the certification includes LS0."
  True as stated (B1 checked the code path); half a page from RM-0(a) [P7], CC2 and [POST]. It applies verbatim to
  anything proved through RM-0, RM2 included. It closes SCR's "not claimed" bullet inside RM's regime; it does not
  touch delivery.
* SCR-C is stated as the exact-recovery corollary of Theorem 5, with (EC′)/L5.2 as its general form, and the examples
  table gets a certificate column: *fires provably* (RM's rows), *implies ⊇ S₀* (SV), *implies = S₀* (NF or (EC′)).
* **Headline:** unchanged. Theorem 3 stays "(V) + (L) + lattice condition"; Theorem 5 stays certified screening. One
  sentence joins them: Theorem 3 is the a-priori guarantee, Theorem 5 with SCR-C the a-posteriori certificate, and
  under Theorem 3's conditions the certificate fires. The paper should not say that the two have disjoint uses, that
  a certificate proves recovery without SV, or that (L) and (N) cannot be weakened.

**(b) Merge into W3-RM2 with a named lemma — not now.** The named lemma would be PL (§2). For RM2's target (envelope
|Q| ≤ n^b with a start that may be as large) PL's bound (C − 1)m₀ exceeds the cap's slack, so it does not deliver
RM2's key lemma, and RM2's kill budget (3 attempts) should not be spent on it. Strongest case for (b): if RM2's
sandwich came with a size-only bound m₀ = O(log n), PL under NF would replace whole-lattice NA. **Headline if done:**
RM2's exponent unchanged; one more alternative to (N), under NF.

**(c) A new ticket — only on a trigger; meanwhile hand both PL sketches to the planned path-level ticket** (rule 14:
one Fable attempt, one Astra break review), as its first attempt: lattice PL + exit control, and PL under NF with a
size-only start bound. Trigger for a separate ticket: W3-P6 shows {Ŝ = S₀} at frequency ≈ 1 on regime-A designs
(then: discovery through the final search, with SCR-C as last step) or on regime-D designs (then the last step must
be an (EC′)-based exactness criterion, not NF). **Headline if it succeeded:** a reported-model theorem with no
leakage envelope, under NF or (EC′) — narrower in design and in p than Theorem 3, so a second theorem beside it.

## 5. Open points
1. PL (both forms) is a sketch: constants, the x′ bookkeeping, confinement reserve r, and exit control are unproved.
2. A size-only start bound without a small envelope (counting or block-relative leakage) has no proof route yet.
3. Full-method discovery on FAC-PK's class at ρ < 1/3 is open; it decides whether regime A can ever carry a theorem.
4. NF versus (N): neither an implication nor a counterexample.
5. Version 2's changes are substantive and unreviewed (rule 15); HQ decides whether a Sol or Astra re-check is needed
   before the memo is used for a ticket decision.

## 6. Substantive changes from version 1 (after B1; details in `reviews/B1_disposition.md`)
1. §0: "no supersession, no strengthening" → "not established; not shown impossible"; reason 3 rewritten (F1, F4).
2. I2 and the §1 summary: the arrow "SCR-C ⇏ RM's conclusion" withdrawn; LS0 route fails, full method open (F1).
3. NF forces polynomial p; the non-polynomial-p regime for SCR-C removed (F2).
4. §3 rewritten on full hypothesis sets; row C's sufficient condition corrected with a counterexample (F3).
5. ML2: realised m₀ separated from the envelope |Q|; the requirement restated as an additive budget; "C → 1 is NA"
   withdrawn; the small-start/large-envelope candidate added (F4).
6. §2: ML1–ML3 labelled one sufficient architecture; target restated as discovery; confinement added; M5 no longer
   used in phase 1; "(L) cannot be removed in fixed design" withdrawn; three other routes listed (F5).
7. I5: "NF ⇏ (N)" withdrawn (F6). I1/CERT restated on a common good event with the enumeration branch (F7).
   I4: the 2/3 comparison corrected, example added (F8). I3: cap-return exception stated exactly.
8. Recommendation (a) unchanged; (b) and (c) reworded; PL handed to the path-level ticket.
