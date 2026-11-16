# Q6 — Assembly: Theorem RM2-F-plus (C1⁺), Theorem RM2-R-plus (C2⁺), and Cont-plus (C4⁺)

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses — 2026-11-16, lead
Claude Opus 5.5. Ticket W3-RM2-R; statement: `../STATEMENT.md` v1.0 §4 ((C1⁺), (C2⁺)), §6 ((C4⁺)). No new mathematics.
The Form F assembly follows PARENT `Theory_work/Wave3/W3-RM2/lemmas/L3_assemblyF.md:11-34` (W3-RM2:RM2-F@1.0.0) with the
inputs replaced as marked [R-#]; the Form R assembly follows PARENT `lemmas/L5_formR.md:135-147` (W3-RM2:RM2-R@1.0.0) with
the core replaced by RM0-plus [R-5]. (This file replaces the verbatim parent copy that stood here at first: the
assembly text is short, so every sentence is written out and each change from the parent is marked.)
PARENT := `Theory_work/Wave3/W3-RM2/`; RM := `Theory_work/Wave3/W3-RM/`.

Inputs: `Q1_sandF_c.md` (SAND-F-c), `Q2_TL_c.md` (TL-F-c; §6 POST/MODE-F), `Q4_core_plus.md` (RM0-plus), `Q5_dlv0.md`
(DLV-0) of this folder; PARENT `lemmas/L2_width.md` §1 (Lemma NA-W, W3-RM2:NA-W@1.0.0, "PROVED-CHECKED; council R1, …");
PARENT `lemmas/L4_sandR_b.md` (SAND-R-b), `lemmas/L5_formR.md` (P8 = F-to-R, P10 = POST-R) (registry
"PROVED-CHECKED; council R1, …"; POST-R "PROVED-CHECKED, conditional on W2-APP:POST; …"); W3-RM:E4@1.0.0 ("PROVED-CHECKED").

## 1. Theorem RM2-F-plus (claim (C1⁺))

Setting F, the method as coded, premises and configuration of STATEMENT §1. Assume (T1-F♭), (FL) = (FL-16) + (FL-Q),
(V♭), (L^b) = (L-size^b) + (L-feas) + (L-gain) with b < β(η, A), (BM-W⁺) and (W).

*Proof.* (T1-F♭) contains ‖μ‖² ≤ Mn, p ≤ n^A, fixed s₀ ≥ 1 (it is (H0) with only the beta-min clause changed). (L-size^b)
with b < β(η, A) ≤ ½ gives q ≤ n^b, so q log n/n → 0; (L-feas) gives q ≤ K. (As PARENT `L3_assemblyF.md:16-17`.)
* **[SAND(Q)]** [R-1]: `Q1_sandF_c.md`, Lemma B1 ((FL-16) ⇒ (G3a), (V♭) ⇒ (V_b♭), (L-gain) ⇒ (L_b) for the method's partition,
  a deterministic function of the fixed X with blocks ≤ 16) and Lemma SAND-F-c ((S0) from (T1-F♭), (Q) from (L^b), (B)).
* **[NA(Q)]**: PARENT `L2_width.md` §1, Lemma NA-W, from (F0), (FL-Q), (W) (unchanged; it uses no beta-min).
* **[TL(Q)]** [R-2]: `Q2_TL_c.md` §4, Lemma TL-F-c, from (F0), (FL-Q), (BM-W⁺) and P(𝒵_n) → 1 (Lemma NA-W).
* **[POST], [MODE]** [R-3]: `Q2_TL_c.md` §6, Lemma POST/MODE-F, from (T1-F♭) (conditional on SOP:TH09@1.0.0).
* **[E4]**: W3-RM:E4@1.0.0 under its hypotheses (premises of STATEMENT §1).
Then RM0-plus (`Q4_core_plus.md`) with 𝓛′ = 𝓛 gives the conclusions [R-4]: (a) — on Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛) LS0 from
the coded start mode makes exactly |S̃₀ ∖ S₀| moves, each deleting an element of S̃₀ ∖ S₀ ⊆ Q ∖ S₀ (so ≤ |Q ∖ S₀| ≤ n^b
moves), ends at S₀ with a completed scan finding no strict improvement, the cap ℓ_n + |S̃₀| is not binding, and the archive
statement holds; (b⁺) — with 𝒢⁺_n := 𝓜_n ∩ 𝒦_n, every admissible output run reports Ŝ⁺ = S₀ on 𝒢⁺_n and
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) ≤ P(𝓜_nᶜ) + P(St_n(𝓛)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0,
using P(𝓜_nᶜ) → 0 ([MODE]), P(St_n(𝓛)ᶜ) ≤ P(Sand_n(Q)ᶜ) → 0 ([SAND(Q)], Sand_n(Q) ⊆ St_n(𝓛)), [NA(Q)], [TL(Q)]; hence
P(𝒢⁺_n) → 1 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). **Under (D)** (c⁺): in Setting F the input is valid and
non-degenerate a.s. (`Q4_core_plus.md` (c⁺) proof; the declared seed and allocation satisfy (D)), so every admissible
run returns output (DLV-0) and P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0, i.e. P(Ŝ⁺ = S₀) → 1, uniformly over seeds, N_e, R′
and calibration outcomes.
*Block-relative variant.* Lemma SAND-F-c is stated under (G3a), (V_b♭), (L_b) on the method's partition; NA-W, TL-F-c and
POST/MODE-F do not involve the partition. So the conclusions hold with (V♭), (L-gain), (FL-16) replaced by (V_b♭), (L_b),
(G3a) (and (FL-Q) kept). ∎

## 2. Theorem RM2-R-plus (claim (C2⁺))

Setting R, the method as coded, any X-measurable partition with blocks ≤ 16, premises and configuration of STATEMENT §1.
Assume the hypotheses of RM2-R: (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, (W-R).

*Proof.* The interface properties are those of PARENT `L5_formR.md:140-143` (unchanged): [SAND(Q)] by Lemma SAND-R^b
(PARENT `lemmas/L4_sandR_b.md`), [NA(Q)], [TL(Q)] by Lemma P8, [POST] by Lemma P10 (conditional on W2-APP:POST@1.0.1),
[E4] by W3-RM:E4@1.0.0. [MODE] [R-5]: {π(S₀) > ½} ⊆ 𝓜_n (`Q4_core_plus.md` (b⁺) proof), so P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)] → 0
by [POST], under the joint law. Then RM0-plus — a statement for any design (fixed or random) and any deterministic
Q ⊇ S₀ with |Q| ≤ K, applied under the joint law of (X, ε) — gives (a) and (b⁺) exactly as in §1: P(𝒢⁺_n) → 1, every
admissible output run reports Ŝ⁺ = S₀ on 𝒢⁺_n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0. Under (D), (c⁺): in Setting R
the input is valid and non-degenerate a.s. (`Q4_core_plus.md` (c⁺) proof), so P(Ŝ⁺ = S₀) → 1 under the joint law,
uniformly over the run parameters. ∎

## 3. Cont-plus (claim (C4⁺))

**(i) RM2-F-plus ⇒ RM2-F.** RM2-F's hypotheses (PARENT `STATEMENT.md:206-207`): (T1-F), (FL), (V), (L^b) with b < β(η, A),
(BM-W), (W). (T1-F) ⇒ (T1-F♭): BM-∞ is one branch of (T1-F♭)'s beta-min clause, all other clauses identical. (V) ⇒ (V♭):
for any fixed M_V > M_V⁰, M_n ≥ M_V for n ≥ n₀ because M_n → ∞, so δ²_{U,j} ≥ M_n log n ≥ M_V log n. (BM-W) ⇒ (BM-W⁺):
`Q2_TL_c.md` §4 [R-2](a) (for any fixed c_TL > c_TL⁰). (FL), (L^b), (W) are common. So RM2-F's hypotheses imply RM2-F-plus's.
Conclusions: RM2-F concludes [SAND(Q)], [TL(Q)], [NA(Q)], [POST] and the conclusions of RM-0 (PARENT `STATEMENT.md:206-214`);
RM2-F-plus concludes all of these (RM-0's (a) is RM0-plus (a); RM-0's (b) is the special case of (b⁺) through
{π(S₀) > ½} ⊆ 𝓜_n, with [POST] — `Q4_core_plus.md` (b) and (b⁺)), and more. The block-relative variants correspond
likewise ((V_b) ⇒ (V_b♭)).
**(ii) RM2-R-plus ⇒ RM2-R.** Same hypotheses; RM2-R's conclusions ([SAND(Q)], [TL(Q)], [NA(Q)], [POST], RM-0's) are among
RM2-R-plus's, as in (i).
**(iii) RM0-plus ⇒ RM-0.** RM-0(a) is RM0-plus (a) (identical text); RM-0(b) is stated and proved inside `Q4_core_plus.md`
as the special case of (b⁺).
**(iv) Through PARENT (C4).** PARENT (C4) (`STATEMENT.md:236-240`, W3-RM2:Cont-F@1.0.0, Cont-R@1.0.0) shows that RM-F's
hypotheses imply RM2-F's and RM-R's imply RM2-R's, with conclusions ⊇; composing with (i), (ii): RM-F's hypotheses imply
RM2-F-plus's, and RM-R's imply RM2-R-plus's, with conclusions ⊇. So RM2-F-plus ⇒ W3-RM:RM-F and RM2-R-plus ⇒ W3-RM:RM-R.
**(v) Ex-Proxy-d ⇒ Ex-Proxy.** `Q7_proxy_d.md` (b) with θ_n ≡ θ ≠ 0 fixed (then nθ²/log n → ∞) verifies every hypothesis of
RM2-F on PARENT E4's design, which is W3-RM2:Ex-Proxy's content. ∎
**Registry form (HQ ruling at CP1).** Cont-plus records its targets — W3-RM2:RM2-F, W3-RM2:RM2-R, W3-RM:RM-0, W3-RM:RM-F,
W3-RM:RM-R, W3-RM2:Ex-Proxy — under `implies`, not under `depends_on`: they are what it proves to be implied, not inputs.

## 4. Consumed claims in this file (registry id@version; statuses verbatim)

W3-RM:E4@1.0.0 ("PROVED-CHECKED"); W3-RM2:NA-W@1.0.0, SAND-R-b@1.0.0, F-to-R@1.0.0 ("PROVED-CHECKED; council R1, …");
W3-RM2:POST-R@1.0.0 ("PROVED-CHECKED, conditional on W2-APP:POST; …") — so (C2⁺) is conditional on W2-APP:POST@1.0.1;
SOP:TH09@1.0.0 (through `Q2_TL_c.md` §6) — so (C1⁺) is conditional on SOP:TH09@1.0.0; W3-RM2:Cont-F@1.0.0, Cont-R@1.0.0
(only for (iv)). The ticket's own lemmas Q1, Q2, Q4, Q5, Q7 carry their statuses.
