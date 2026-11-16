# SL1 — statement lock, W3-START2-R — reply of Sol (codex gpt-6.1-sol, reasoningEffort high), verbatim
# Brief: reviews/BRIEF_SL1_sol.md. Received 2026-11-15 (see LOG.md).

SL1-VERDICT: LOCK WITH CHANGES

The main mathematical targets appear sound, and the plan is viable. The changes below are needed for faithful supersession and a fully defined statement.

1. **F — Supersession strengthens some parent hypotheses.**  
   STATEMENT lines [98–105](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:98), [139](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:139), and [262–268](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:262).

   The new VIS-c/VIS-m bridges explicitly assume (E), (GF-16), whereas their named BASE counterparts consume [TK], with the additional leakage premises for VIS-c. Likewise, BASE NEC-b is stated under Setting F, (E), [TK], while C2⁺⁺ assumes (GF-16). See [BASE STATEMENT, lines 221–236](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START/STATEMENT.md:221).

   The implication (GF-16), (E) ⇒ [TK] does not justify replacing [TK] by (GF-16) in a claim advertised as implying the parent claim. This is a hypothesis mismatch in the supersession table, even though the intended fixed-design applications already assume (GF-16).

   **Fix:** retain interface-level conclusions under [TK], in the quantitative sense specified by BASE, and present the explicit uniform thresholds/events under (E), (GF-16) as additional refinements. State C2⁺⁺ under (E), [TK], with (GF-16) as a sufficient condition. The planned arguments need only the toolkit at the witness sets, so this repair is inexpensive.

2. **F — The old and new margin forms do not agree when log p/log n → A.**  
   STATEMENT [lines 62–65](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:62).

   The sentence “When log p/log n → A the two forms agree” incorrectly includes (V-m)/(V-mp). For example, with Q = S₀ fixed and a > d,
   \[
   \pi_n(d,a;S_0)
   =-(a-d)(1+2A)\log n+o(\log n),
   \]
   whereas the old price \((1+2A)(d-a)_+\log n\) is zero. The negative-price improvement therefore persists at leading order even when p reaches the envelope.

   **Fix:** say that the constant-level thresholds agree at leading order when log p/log n → A, while the margin form additionally retains the net-addition credit, including in that regime.

3. **E — The random sharp rate needs a definition when Q ≠ S₀.**  
   STATEMENT [lines 160–173](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:160).

   Here h is indexed by l ∉ Q, but line 165 defines \(R^\sharp_n\) using \(\mathfrak L^\sharp_n(h)\) and \(\mathfrak L_n(S_0;h)\). Those functionals require levels for every l ∉ S₀, including l ∈ Q ∖ S₀. They are consequently undefined on admissible designs with Q ⊋ S₀. The existing invalid-input convention does not cover these valid designs.

   This matters in (a2), which assumes only P(Q = S₀) → 1.

   **Fix:** define \(R^\sharp_n\) by the displayed formula on {Q = S₀}, and set it to zero elsewhere. Alternatively, explicitly extend h to Q ∖ S₀. Either choice preserves the claimed result.

4. **E — The “any size” wording exceeds the stated reference-set scope.**  
   STATEMENT [lines 237–239](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:237).

   “Any size in (ii)–(iii)” is not what the claims currently state. BR(ii) inherits BR(i)’s (L-R⁺⁺), and START-R(ii)–(iii) inherit the assumptions in lines 216–217, including the bound log H̄_n ≤ κ_H√log n. Only the standalone BR(iii) expressly dispenses with (L-R⁺⁺).

   **Fix:** describe the scope as “up to exp(κ_H√log n) under (L-R⁺⁺); the standalone leading-functional bridge BR(iii) requires no reference-set hypothesis.” Any further unrestricted-size claim should be stated separately and supported separately.

5. **E — Incorrect plan-section reference.**  
   STATEMENT [lines 13–14](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/STATEMENT.md:13).

   The R1–R5 lemma-file table is in [PLAN §2](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/PLAN.md:23), not §3.

   **Fix:** change the reference to PLAN §2.

The substantive checks supporting this verdict are as follows:

- **D3 and visibility:** the old-to-new implications hold as stated, asymptotically. For s₀ ≥ 1, \(p/c_Q\ge(16s_0)^{-1}\), so n ≥ 256s₀² ensures \(\log n+2\log(p/c_Q)\ge0\). The proposed π_n matches twice BASE L4 Step 5’s price up to a uniformly bounded additive correction. For a > d, the correction from replacing log(n + 1) by log n has the favorable sign. In Step 6, a negative π_n also has the favorable sign because \((1-\varepsilon_1)/(1+\omega_n)\le1\). This remains valid when log(p/c_Q) < 0.

- **D4/D5 and Gaussian rates:** (L-R⁺) implies (L-R⁺⁺), and the C₀ = 0 equivalence in D5 is correct. The proposed N_ref removal is sound: for U ⊊ S₀, conditioning on W_{S₀} preserves the innovation law used in [BASE L9.5](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START/lemmas/L9_BR.md:92). D5 gives \(\|\gamma^2\|=O((n\log n)^{-1/2})\), hence \(\bar d=O((\log n)^{-1/2})\) and \(\Phi_n=O(\sqrt{\log n})\). Summing over at most \(2^{s_0}\) reference sets proves BR(iii) without localization or (V-R). For START-R(iii), the retained (L-R⁺⁺) supplies
  \[
  n^{-1}\mathfrak L_n(S_0)^2
  \le n^{-1}e^{2C_B\sqrt{\log n}}
  =o\!\left(\sqrt{\log n/n}\right).
  \]
  Thus the second display of T1⁺⁺(d) gives the advertised odds rate. The factor N̄_n in (ii), and dependence on κ_H in (i), are appropriate.

- **Necessity and F4:** the pointwise thresholds and both drifting directions are sound. Near the boundary, the witness’s Gaussian cross term is \(O_P(\sqrt{\log n})\), while the stipulated gap dominates that scale. Gains much larger than log n on the leaking-null side can be handled directly with the lower toolkit inequality. F4’s explicit constant \(C_A=2\sqrt{1+2A}+1\) is sufficient: the first term covers the Gaussian cross term, and the additional 1 absorbs the \(\sqrt{\log\log n}\) prefactor uniformly over c_n ≤ 1.

- **Transfer and MIS:** after finding 3’s definition repair, (a1)–(a3) follow from the stated uniform conditional argument; taking maxima over finitely many support sizes handles |S₀| ≤ s̄. The Gaussian MIS instance gives exactly the displayed a, γ and conditional residual variance. Requiring τ² to be independent of n preserves the fixed-noise-variance premise. The warning that γ can be dense correctly preserves the sparsity requirement.

- **Examples:** F-1/F-3 and G-1/G-2 have the stated improved rates under their inherited hypotheses. For F-2, put B = 1 + 2A. The N = ∅ margin limits c_m to B; |N| = 1 permits a larger margin, and |N| ≥ 2 receives the negative-price credit. Thus every \(0<c_m<B\) is valid. The F4 contribution is \(n^{-B/10+o(1)}\), giving the stated \(O_P(n^{-B/10+\eta})\) rate. The sufficient first-order condition has exponent
  \[
  n^{-1/2}\mathfrak L_n(S_0;h)^2
  \le n^{\,3/10-2A/5+o(1)},
  \]
  which tends to zero for A > 3/4, exactly the claimed range.

**OPTIONAL:** Make the requested O_P-envelope consequence explicit after (a2): if \(\varrho_n=O_P(\bar\varrho_n)\) for deterministic \(\bar\varrho_n\to0\), replace the random rate by \(\bar\varrho_n\); similarly replace \(R^\sharp_n\) by any deterministic O_P envelope. This already follows from (a2) and costs no additional estimate.

The draft covers T8, T10, the requested restatements, and the LEAK-0 wording correction. After the repairs above, the remaining supersession rows have the claimed implication routes. The plan is credible within approximately 12 Opus hours and the Wednesday cutoff if T9/T11 remain deferred; the proposed Gaussian leading-term extension does not introduce a new mathematical obstacle requiring a larger proof budget.
