# Item 4 — Song–Liang (2015) posterior-level corollaries of T03♯ / W1 results (v2)

Author: C-PACK lead (Claude Opus 5.5). **v2** after cross-family check R34 (`reviews/R34_item4_check_sol.md`, verdict ERROR
as written: 0 FATAL / 2 MAJOR / 7 MINOR; SL0(i)–(v), SL1, SL1′, SL2 independently re-derived; the error was SL0(vi)'s
D0-attainment claim). All findings applied (disposition `reviews/R34_disposition.md`). Status of each statement:
PROVED (by this seat, unchecked), R34-checked as listed in the disposition; v2 repairs re-read by R38 (blind mid-point, CONTINUE) and R39 (sweep, fixes applied); council C1 passed (Sol 9.0, Opus 8.7). Input statuses
are quoted in §4; nothing is upgraded. Aliases: `SoP/` = `Theory_work/State_of_Project/sections/`; `W1/` = `Theory_work/Wave1/`;
`NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

## 0. Objects and conventions
π is the exact posterior of the method's target (D0: shipped g = n score, a₀ = b₀ = 0.01, normalised capped BB(1,p)
prior, support Ω = {S : |S| ≤ K}, K = min(p, ⌊n/2⌋); `SoP/04_theory.tex:70-72`; `W1/W1-GEN/STATEMENT.md:26-27`). S₀ = true
support, s₀ = |S₀|. δ := 1 − π(S₀), with π(S₀) := 0 when s₀ > K (zero extension). PIP_j := π({S : j ∈ S});
HPM := argmax_Ω π (the exact-posterior maximiser, any tie rule — distinct from the method's reported best-scored model
Ŝ⁺); MPM := {j : PIP_j > ½}; for q ∈ (0,1), ξ_q := {j : PIP_j > q}.
**Conventions (R34 #3).** Every maximum of the nonnegative errors over an empty coordinate set is defined as zero. For
summary statements involving h(S₀), assume S₀ ∈ Ω eventually, or define h on Ω ∪ {S₀} with the stated range on that union.
Rate sequences and error tolerances are deterministic and positive.

## 1. Lemma SL0 (deterministic; every data set, every n)
(i) For every j: |PIP_j − 1{j ∈ S₀}| ≤ δ. Hence max_{j∈S₀}(1 − PIP_j) + max_{j∉S₀} PIP_j ≤ 2δ.
(ii) For every A ⊆ [p]: |π({S : A ⊆ S}) − 1{A ⊆ S₀}| ≤ δ. If S₀ ∈ Ω, for every h : Ω → ℝ: |π(h) − h(S₀)| ≤ δ·osc(h),
osc(h) := max_Ω h − min_Ω h; in particular sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = TV(π, point mass at S₀) = δ.
(iii) For every q ∈ (0,1): δ < min(q, 1 − q) ⇒ ξ_q = S₀. In particular δ < ½ ⇒ MPM = S₀.
(iv) δ < ½ ⇒ S₀ is the unique maximiser of π (HPM = S₀ for every tie rule).
(v) π({S : |S| = s₀}) ≥ 1 − δ.
(vi) (R34 #1 text) As a bound over arbitrary probability laws on Ω, the constant 2 in (i) is sharp when 1 ≤ s₀ ≤ K and
s₀ < p. Put mass 1−δ on S₀ and δ on a feasible one-for-one swap. This is not an attainment claim for the strictly
positive finite-data D0 posterior. (For a D0 posterior every model, incl. ∅, has positive mass, so for nonempty proper
feasible S₀, PIP_k ≤ δ − π(∅) < δ for k ∉ S₀ and the max-sum is < 2δ; sharpness *within* D0 is not claimed.)

*Proof.* For any event B ⊆ Ω, |π(B) − 1_B(S₀)| ≤ π({S ≠ S₀}) = δ (the indicator differs from its value at S₀ only off
S₀); (i) takes B = {j ∈ S}, (ii) B = {A ⊆ S}. (If s₀ > K then δ = 1 and (i), (ii), (v) are trivial.) For h:
π(h) − h(S₀) = Σ_{S≠S₀} π(S)(h(S) − h(S₀)), |h(S) − h(S₀)| ≤ osc(h); the TV identity is the supremum of this over
[0,1]-valued h (attained by h = 1{S ≠ S₀}). (iii) j ∈ S₀ ⇒ PIP_j ≥ 1 − δ > q; j ∉ S₀ ⇒ PIP_j ≤ δ < q. (iv) For S ≠ S₀:
π(S) ≤ δ < ½ < 1 − δ = π(S₀). (v) {S₀} ⊆ {|S| = s₀}. (vi) With S₁ := (S₀ ∖ {j}) ∪ {k} ∈ Ω (j ∈ S₀, k ∉ S₀; feasible as
|S₁| = s₀ ≤ K) and the two-point law, 1 − PIP_j = δ and PIP_k = δ. ∎

## 2. Corollary SL1 (asymptotic; any law under which δ_n = O_P(r_n))
Let r_n > 0, r_n → 0, and δ_n = O_P(r_n) under some law P (fixed design: the noise law; random design: the joint law of
(X, ε)). Then:
(a) max_j |PIP_j − 1{j ∈ S₀}| = O_P(r_n); in particular max_{j∈S₀}(1 − PIP_j) + max_{j∉S₀} PIP_j = O_P(r_n); and
E[max_j |PIP_j − 1{j ∈ S₀}|] ≤ E δ_n → 0 (no expectation rate is claimed);
(b) for every deterministic q_n ∈ (0,1) with r_n = o(min(q_n, 1 − q_n)) — in particular every fixed q — P(ξ_{q_n} = S₀) → 1;
P(MPM = S₀) → 1;
(c) P(HPM = S₀) ≥ P(δ_n < ½) → 1, and P(HPM ≠ S₀) ≤ 2E δ_n;
(d) sup_{h : Ω → [0,1]} |π(h) − h(S₀)| = O_P(r_n) (convention of §0 on S₀ ∈ Ω);
(e) π(|S| = s₀) = 1 − O_P(r_n).
*Proof.* (a), (d), (e): SL0 (i), (ii), (v). Expectation: δ_n ∈ [0,1], δ_n →_P 0, so E δ_n ≤ ε + P(δ_n > ε) → ε for every
ε > 0. (b): P(ξ_{q_n} ≠ S₀) ≤ P(δ_n ≥ min(q_n, 1 − q_n)) → 0 since δ_n/min(q_n,1−q_n) = O_P(1)·o(1). (c): SL0(iv), and
HPM ≠ S₀ ⇒ δ_n ≥ ½, Markov. ∎

**Instances (statuses in §4).**
- I-a (fixed design): all T03♯ hypotheses R1, G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c > c₀) (TH09,
  `SoP/04_theory.tex:782`), its noise law: r_n = √(log n/n).
- I-b (LH-iid, joint law): all W1-PXN (P) hypotheses: r_n = √(log n/n) (`W1/W1-PXN/lemmas/P8_T03sharp.md:23-24, 36-55`).
- I-c (R34 #4 text) Under GEN (C4), δ_n=O_P(√(log n/n)) under the joint law: apply T03♯ along every deterministic
  sequence in its X-events and use the diagonal tightness transfer of PXN P8♯, step 4. Hence Eδ_n→0. Sources: GEN
  STATEMENT.md:115–120, L5_assembly.md:57–77; PXN lemmas/P8_T03sharp.md:45–55. (The transfer requires GEN's
  every-sequence/common-envelope quantifiers; conditional convergence alone would not suffice.)
- I-d (LH exact Gram): S-T's IC3 row states "LH satisfies fixed sparsity, bounded energy, positive full Gram eigenvalue and
  BM-∞" (`SoP/04_theory.tex:824`), so T03♯ applies and δ_n = O_P(√(log n/n)); M3(f) also records π(S₀) → 1
  (`SoP/04_theory.tex:305`). Thm5-LH retains its SAME-FAMILY-ONLY status.

**Corollary SL1′ (no beta-min; large signals only).** Retaining T03♯'s other hypotheses, its large-signal clause
(`SoP/04_theory.tex:782`) gives π(S ⊉ J_n(c)) = O_P(√(log n/n)) for J_n(c) = {j ∈ S₀ : θ*²_j ≥ cσ² log n/(nφ₀²)}, c > c₀.
Since {j ∉ S} ⊆ {S ⊉ J_n(c)} for j ∈ J_n(c), max_{j∈J_n(c)}(1 − PIP_j) ≤ π(S ⊉ J_n(c)) = O_P(√(log n/n)) (= 0 if J_n(c)
is empty). No specificity or full-support recovery follows from that clause alone.

## 3. What the method's reported quantities satisfy (no upgrade)
(R1) **Reported HPM** Ŝ⁺ (best-scored model over the all-scored set 𝒮⁺): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ + D_n at every n
(M5(0)); → 0 with LS0 on LH-iid (W1-PXN (C)), on GEN's class (W1-GEN (C3)), on LH exact Gram (M5(b1-LH), with item 1's
e4′ in place of e4). Jointly with output; P(𝒪) → 1 is not claimed.
(R2) **Plain measured-endpoint PIP, islandwise** (shipped R′ = 4): W1-N1 Corollary E: for h ∈ [0,1],
E[W_r |H_r(h) − h(S₀)| | 𝓒] ≤ δ₁, a.s. on 𝒜 ∩ {r ≤ R′}, for the potential run, under W1-N1's named premises (EX-A, H-U,
START, KERNEL, CAL, SI, MEAS, worker equivalence); h = 1{j ∈ S} gives the coded `pip_plain[j]` (W1-N1 REPORT §2). This is
not the study's `pip_primary` (equal-weight RB statistic, `SoP/02_method.tex:1021`), and not a statement in probability
about the pooled estimate.
(R3) (R34 #5 text) The cited cards contain no in-probability sure-screening theorem for the pooled shipped-R′=4
estimator. M1(i), status unchanged ("(h), (i): PROVED (by this seat, unchecked)", `SoP/04_theory.tex:130`), supplies
with-output consistency for a fixed finite list at R′_n=4⌈log₂(n+p+1)⌉ under its T03♯, discrepancy (osc d ≤ D* = O_P(1))
and implementation premises (incl. the pending IND-T extension audit). For simultaneous control of a growing declared
list, the card specifies the separate polynomial stacking configuration in its integration note ("R′_n = 4⌈(n + p)⁶/4⌉ for
simultaneous control over ≤ (n + p)² declared summaries", `SoP/04_theory.tex:111`); no uniform-p conclusion is inferred
from the fixed-list statement alone. The finite bound M1(f) is "vacuous at R′ = 4" (`SoP/04_theory.tex:117`). This is a
statement about the cited cards, not an impossibility theorem.
(R4) **Store-restricted PIPs** PIP^𝒯 (π conditioned on the reported deduplicated store 𝒯, `SoP/04_theory.tex:397`):
Corollary SL2. These are distinct from the sampler's reported PIPs.

**Corollary SL2 (store-restricted PIPs, jointly with output).** Assume (α) M4(b): "If S₀ ∈ 𝒯: … |PIP^𝒯_j − PIP_j| ≤ δ₁ for
all j" (`SoP/04_theory.tex:400`); (β) M4(c): "If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 … holds under LS0 with 𝒯_new =
top_c(𝒯_old ∪ 𝒮_added)" (`:401`), with 𝒮 read as the run's all-scored set 𝒮⁺ (justified: M4 defines 𝒮 as "the set of
scored models", `:397`; the method's HPM is over every model ever scored and LS0-scored models join it and the store,
`SoP/02_method.tex:468-478, 494, 503-505`); exact score ordering (EX-A), a positive-capacity store (c = 40p + 1,
`SoP/02_method.tex:486`) updated as top_c; (γ) truth discovery with output, P(𝒪 ∩ {S₀ ∉ 𝒮⁺}) → 0 — W1-PXN:
𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 of R̄⁺ does not score S₀} (`W1/W1-PXN/FINAL_PROOF.md:75-79`), probability ≤ D_n → 0;
W1-GEN: closure `W1/W1-GEN/lemmas/L5_assembly.md:11-16`, D_n → 0 at `:24-38`, random designs `:66-77`; and
δ_n = O_P(r_n) under the chosen law. Then P(𝒪 ∩ {max_j |PIP^𝒯_j − 1{j ∈ S₀}| > 2δ_n}) → 0, and for every deterministic
t_n > 0 with r_n = o(t_n), P(𝒪 ∩ {max_j |PIP^𝒯_j − 1{j ∈ S₀}| > t_n}) → 0.
*Proof (R38 #3 text).* On 𝒪 ∩ {S₀ ∈ 𝒮⁺} ∩ {δ_n < 1/2}, retention gives S₀ ∈ 𝒯, and M4(b) with SL0(i) gives
max_j |PIP^𝒯_j − 1{j ∈ S₀}| ≤ 2δ_n. If δ_n ≥ 1/2, that inequality holds automatically because every coordinate error is at
most one. Consequently P(𝒪 ∩ {max_j |PIP^𝒯_j − 1{j ∈ S₀}| > 2δ_n}) ≤ P(𝒪 ∩ {S₀ ∉ 𝒮⁺}) → 0. For deterministic t_n > 0 with
r_n = o(t_n) (and r_n → 0 as in SL1), add P(2δ_n > t_n) → 0, since δ_n/t_n = O_P(r_n/t_n) = o_P(1). ∎
(R34 remark: once S₀ ∈ 𝒯 the constant 2 can be sharpened to 1 by applying SL0 to π_𝒯, since 1 − π_𝒯(S₀) ≤ δ_n; not needed.)

## 4. Input statuses (verbatim)
- T03♯ / S-T (TH09): "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (`SoP/04_theory.tex:35`); statement `:782`;
  onset "n ≳ 2·10⁶" (`:824`) — a historical disclosure for the exhibited families, not a universal T03♯ onset (`SoP/04_theory.tex:787`: "no universal onset \(n_0\)").
- W1-PXN: REPORT §1 "**PROVED-CHECKED**"; (P) "XF VERIFIED" (R19). W1-GEN: REPORT §1 "**PROVED-CHECKED**". Both Wave-1
  ticket results, not adopted by HQ (frozen-registry statuses are distinct and not updated here).
- W1-N1 Corollary E: "PROVED under the same premises" (W1-N1 REPORT §3; council-passed round 1).
- M1(i): "(h), (i): PROVED (by this seat, unchecked)" (`SoP/04_theory.tex:130`).
- M4(a): "MZ-P3: "PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery"; "candidate: not reviewed, not
  adopted"; AUTHOR-ONLY; W1PC1 §3 TRUE-AS-WRITTEN" (`:410`); M4(b) (raw TeX at `:411`): "same as (a); W1PC1 §3 B.D3(b)
  COUNTEREXAMPLE repaired with ‖h‖$_{∞}$"; M4(c): "N13: PROVED (PC1 claim 5)" (`:412`).
- M5(0): "T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"" (`:489`, `:843`).
- M5(b1-LH): "T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))" (registry ⚑ CONFLICT on the iid
  sub-claim, excluded); … N3 "OPEN"" (`:491`); the conflicted iid sub-claim is not used (LH-iid via W1-PXN). N3 replaced by
  item 1's e4′ (`lemmas/I1_e4_replacement.md` §4), which retains LS0 integration (and FP-TAB for binary64).
- Thm5-LH and M3 assembly (I-d), registry TH03 row (`NBH/ID_REGISTRY.md:25`): "Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP);
  XF: none; SAME-FAMILY-ONLY**"; "Final assembly: **PROOF SKETCH, unchecked**".
- M8 (map row 13), registry TH08 row (`NBH/ID_REGISTRY.md:30`): "MA-PropD "PROVED (counting, given the code's structure)"
  AUTHOR-ONLY"; "assembly PROOF SKETCH (by this seat, unchecked)".

## 5. Numerical falsification (`numerics/R34_falsify.py` → `_out.txt`, reviewer R34)
216 exact D0 posteriors (n ∈ {6,12,24,60}, p ∈ {4,7,10}, six correlation structures incl. masking pair and singular
duplicates; 64,476 model scores), every candidate truth per posterior (84,096 pairs): no violation of SL0(i)–(v) (max excess
1.3·10⁻¹⁵); 80 two-point laws attain 2δ (arbitrary-law sharpness); negative controls at δ = ½ and at q = 1 − δ, q < δ detected.
