# sharp2 — triage of the 32 sharpness verdicts (MISR, START, START2, RM2, PSHARP)

Author: triage reviewer (Claude Opus 5.5, high), 2026-11-15. Read-only triage; no agents, no commit (HQ commits).
Inputs: `sharp2/results/f00–f09.md`, `VERDICTS.tsv`, `REQUESTS.tsv`; the five STATEMENT files; the lemma lines each
proposal cites (listed in §5); `PROGRAM.md` (stop list, tie-break); `sharp1/TRIAGE.md`, `sharp1b/TRIAGE.md`,
`HQ_NOW.md`, `HQ_DECISIONS.md` (riders T1–T7); `W3-DIST/STATEMENT.md` v1.0.2 (read only).

Classes: **A** real and cheap, worth doing now (**A1** = this week; **A2** = cheap but low value, do only if the
rider is opened anyway) · **B** real but known, done by a later ticket, superseded or out of scope (**B\*** = known,
undone, cheap) · **C** wrong, not an improvement, or cosmetic · **D** unclear, needs a proof agent.

## 0. Is the referee generous? Partly.

- **27 EASY ≈ 8 real findings plus restatements.** As in sharp1, most "EASY" verdicts rest on a restatement (state
  what the proof already gives, drop an unused premise) or on items a later ticket already did. Where a START
  proposal asks for something START2 already did, I mark it B: NEC (N2) pigeonhole = START2 (N2⁺); OVL under (V-m) =
  OVL⁺; F2's growth condition on p = F2⁺.
- **I found no wrong mathematics in the steps I checked** (§5), and two of the reviewer's "new" claims check out
  exactly against the lemma lines:
  - the discarded Step-5 credit in START's (V-m) proof (`W3-START/lemmas/L4_VIS.md:48-50`);
  - in PSHARP Prop. A, the expectation lower bound can be truncated at T = ε/c_n instead of W ≤ N
    (`W3-PSHARP/lemmas/A_log_factor.md:15-25`, `STATEMENT.md:71-73`).
- **The riders are less open than HQ_NOW says.** T6 (product-form localisation) is already **in** RM2 v1.4:
  `W3-RM2/STATEMENT.md:4-5,176-184` [CP2-T6] and `SHARPNESS.md:40-44` "Proved [T6]". HQ_NOW:18 still lists it for
  Monday's Opus leg; check that it is not redone.
- **One wording erratum.** START2's Lemma LEAK-0 says it "sharpens the T₁ clause of [LEAK(S₀)]"
  (`W3-START2/STATEMENT.md:87-88`). It sharpens only the partition-free 𝔏⁰. 𝔏^♯ (a max over all proper U) and the
  block-relative 𝔏^{b,0} are incomparable (f08 §START-F(b)). Fix the wording in the editorial pass.
- **One honest-reading point.** START2's P1 gain (dropping 15√(2/π)z_n/p) is a rate gain only for p = O(√log n)
  (f08; `W3-START2/STATEMENT.md:65-67`). In the p ≫ n regime START2 v1.4 is rate-equivalent to START v1.3.4. The
  chapter should not sell P1 as a p ≫ n improvement.

## 1. Per-claim triage

| claim | verdict | class | one-line reason | file:line |
|---|---|---|---|---|
| W3-MISR:MIS(i) | HARD | **B** | Hard items (growing s, sharp c₁, (E^σ) relative to v_eff, HPM at (n log n)^{−1/2}) need upstream POST2 work. The "matching lower bound E δ ≥ c r_n" is PSHARP's job and is closed for every p by the T12 fix below; MISR `ASSUMPTION_MAP.md:27` should cross-cite PSHARP. Oracle form: adaptivity only in degenerate cases (C). | `W3-MISR/STATEMENT.md:110-123`; `lemmas/M_misr.md:40-43,61-67` |
| W3-MISR:MIS(i′) | HARD | **B** | Clause (b) at n^{−κ(c)} needs Lemma C2 / (G3′) redone upstream; moderate to hard. The FP/FN asymmetry is worth one sentence in the chapter, not a ticket. | `STATEMENT.md:127-140` |
| W3-MISR:MIS(ii) | EASY | **B** | The "scale-mixture corollary" is already covered: put R in 𝓕_n with κ_n = (X, β, R²v) (`:144-149`), and R′(c)'s example covers a common random scale (`:101-102`). Conditional-(PR) with a TV term is correct (`M_misr.md:143-145` freezes the same way) but adds little. O_P(√((1+log p)/n)) for small p is upstream and off-priority (tie-break: p ≫ n). | `STATEMENT.md:95-117,144-160` |
| W3-MISR:Cor-G(a) | EASY | **A1** | Checked: the proof uses only "ξ := X_𝓜β_𝓜 − a1 − X_𝒞γ ~ N(0, τ²I) independent of X_𝒞" (`G_corollaries.md:26-31`). Restate as: X_𝒞 arbitrary; given X_𝒞, X_𝓜β_𝓜 ~ N(a1 + X_𝒞γ, τ²I). Σ_𝒞𝒞 ≻ 0 is not needed; Cramér gives a partial converse. ~1 h. **Bears on DIST (§3).** | `STATEMENT.md:164-170`; `lemmas/G_corollaries.md:26-34` |
| W3-MISR:Cor-G(b) | EASY | **A2** | All correct and inside G.2: liminf ρ^{BM} > 2c₀/φ₀² in place of → ∞ (step 4, `G_corollaries.md:53-55`); a correlation-matrix floor, since only c_pop/C₀ enters (`:40,47-48`); the explicit bound (`:57-61`). It is an example corollary: low value. Sub-Gaussian candidate rows: B. | `STATEMENT.md:171-174`; `G_corollaries.md:45-61` |
| W3-MISR:Cor-H | EASY | **A1** | Checked: (a) uses the margin only for δ_n →_P 0 and then POST2 D(a), whose own premise is "δ_n → 0" (`W3-POST2/STATEMENT.md:107-111`). Restate (a) under (SZ), (E^σ), (F₀), δ_n →_P 0. Add the uniform-over-class form and the conditional random-design form by the freezing argument of `M_misr.md:143-149`, plus a KL remark. ~2 h. Expectation-rate (b): D. BvM: B. **Bears on DIST (§3).** | `STATEMENT.md:178-197`; `G_corollaries.md:83-87` |
| W3-PSHARP:A | EASY | **A1** | Checked: truncating at T = ε/c_n with Var ≤ c·T·E gives liminf E δ_n / [(s₀+1)√(log(p√n/(s₀+1))/(πn))] ≥ 1 for **every** N ≥ 1, fixed p included (constant √((a+½)/π) vs the stated √(a/π)). So r_n is exact in expectation for every p. This corrects the expectation readings at `:84-88` and `:109`. A2 with e^λ − 1 on (W-orth) (K01-P1 analogue): +1 h. Dropping G under (W-sph) and a coherence witness: B (park). ~3 h total. | `W3-PSHARP/STATEMENT.md:71-77,79-88,109`; `lemmas/A_log_factor.md:15-25,64-68,119` |
| W3-PSHARP:B | SHARP | — | Agreed. The cosmetic readings (supercritical exp(−s₀/(2√n)), the s₀/p → θ cap) are optional editorial items. | `STATEMENT.md:92-111` |
| W3-RM2:RM2-F | EASY | **A1 → T4** | Checked `L2_width.md:205-217`: truth removal needs only √λ_n ≥ 2(d_n + √(2 log n)) and λ_n ≥ C(A, M, σ², C_R) log n, an additive floor at the constant level, not the ratio → ∞ of (BM-W). This is T4's theme (constant-level V and BM): add it to T4. Quantile form of (W) (`:77-86`): correct, gains only under superconcentration (partly O5); A2 in the same leg. Constant (V): already T4 (B). Search-event rate: already recorded (`L3_assemblyF.md:36-38`; note R): B. s²/8 → s²/2, A → log p/log n: C (cosmetic). Leak-profile (L): O2 / T2(c): B. | `W3-RM2/STATEMENT.md:137,140,206-214`; `lemmas/L2_width.md:70-90,205-217` |
| W3-RM2:RM2-R | EASY | **D** (rest B/C) | The aggregated leak \|Cov(W_l, Σθ*_kW_k \| W_U)\| = o(√(log n/n)), with individual covariances o(1), is plausible: s_ly is an aggregate (`L4_sandR_b.md:111-114`), and the Box/standardisation correction is o(h_n). But Lemma 3 bounds ‖m‖ through ‖α‖ (`:150-160`), and moving that bound to mᵀv needs a proof agent. Half a day; design-agnostic but small. κ-frontier = O3′ (B). Decaying a_n, θ_lo: binding input is W2-APP:POST (T5 territory, B). Wishart floors: immaterial while b < ½ (C). | `STATEMENT.md:176-184,216-218`; `lemmas/L4_sandR_b.md:108-176` |
| W3-RM2:Ex-Proxy | EASY | **A1 → T4** | Correct: with r²q → 0 the removal directions give d_n = O(1), so (BM-W) = BM-∞, and E4 holds for nθ_n²/log n → ∞. The present proof goes through BM-Q (`L6_examples.md:372-373`), so the table has **no witness that (BM-W) is strictly weaker than (BM-Q)**. The decaying-θ_n version supplies one. ~1–2 h. Other r_n: A2. p up to n^A: D (Theorem-1 clauses unverified). | `STATEMENT.md:265-267`; `lemmas/L6_examples.md:360-384` |
| W3-RM2:Ex-Equi | EASY | **B\*** | Known: O4′ "open, cheap to settle"; two reviewers already sketched the threshold b = 3/8 (`SHARPNESS.md:65-69,95`). The 3/8 proof plus its converse would give a proved O1 instance (route fails, conclusion plausibly holds). ~3–4 h. Optional in the RM2 leg; not needed for the headline. | `STATEMENT.md:267-270`; `SHARPNESS.md:65-70` |
| W3-START:FLOOR | SHARP | — | Agreed (tight including the constant; exponent ½ belongs to the prior). | `W3-START/STATEMENT.md:241-243` |
| W3-START:START-F | EASY | **A1 → T8** | Checked `L4_VIS.md:48-50` (Step 5): p ≤ n^A enters only as log(2p) ≤ A log n. Stating (V-c)/(V-m) at log n + 2 log p makes sufficiency and necessity (N3) match for every p_n (today A vs A̲). Applies to START2 via the base (V-c)/(V-m). ε₀ removal: correct but cosmetic (C). s₀ ≤ polylog: (e1) is indeed loose (S₀ ⊆ Q), but the claim needs a constant audit and downstream RM/RM2 keep s₀ fixed (D, low leverage). Energy/floor trade: D. (GF-16) on nulls = O2; partition-free (AL) vs block (Lemma ASM is the block form, `:213-219`); p, Gaussian scope: all B. b_n → 0 vs limsup ≤ ε: C. | `STATEMENT.md:135-157,245-264`; `lemmas/L4_VIS.md:40-75`, `L5_ASM_STARTF.md:11,41,64` |
| W3-START:F1 | EASY | **A2 → T9** | Correct: with a = σ²/τ² ≤ ā < 1 on pairs with δ ≠ 0, the exact Laplace exponent η/2 + max_{x≤√(2A)}[√(ηā)x − (1−ā)x²/2] replaces (J2)'s η/2 + √(2Aη) (`L3_LEAK.md:10-19`). Sets U ⊇ S₀ have δ = 0. This unifies F1 with F2 and enlarges η (A = 1, ā = ½: η < ½ vs η_A ≈ 0.10). Value moderate; ~2 h. | `STATEMENT.md:268-271`; `lemmas/L6_COROLLARIES.md:27-40` |
| W3-START:F2 | EASY | **B** | The growth condition p/√log n → ∞ is removed by START2 F2⁺ (`W3-START2/STATEMENT.md:112-117`). 𝔏 = O(n^{(1+η′)/4}) and a direct Δ_lo floor: cosmetic (C). Weak-law constant: moderate (B). | `STATEMENT.md:272-275` |
| W3-START:F3 | EASY | **A2 → T9** | Checked `L6_COROLLARIES.md:62-71`: the growth premise is used once to reach ϱ ≤ c_{0,n}, and L6.0′ is a fixed-n inequality, so it can be dropped. δ² ≤ G_nτ² for any G_n = o(log n) follows from the same (J2) line. The lower-bound example is a remark. ~1 h. | `STATEMENT.md:276-277` |
| W3-START:F4 | EASY | **A2 → T9** | Checked `L3_LEAK.md:95-109`: with \|I_n\| = n^ι and h² = 2 log\|I_n\| + 4 log log n, the budget is 2¹⁶(log n)^{−2}. The charge → 0 iff √c + √(2ι) < √(1+2A), which gives F4 at ι = 0 and F1's η_A at ι = A. One corollary in place of two; ~1–2 h. Pointwise log p: fold into T8. | `STATEMENT.md:278-287` |
| W3-START:NEC | EASY | **B** | The non-vacuous partition-free (N2) is START2 (N2⁺) (`W3-START2/STATEMENT.md:156-166`). Drifting c_n and pointwise log p: fold into T8 (A2). Non-Gaussian negative result: remark (B). | `STATEMENT.md:316-331`; `lemmas/L7_NEC.md:21-43` |
| W3-START:TRANSFER | EASY | **B** | Superseded by START2 (T3⁺)(a). The random-rate/self-normalised restatement belongs there (see START2:TRANSFER). | `STATEMENT.md:290-305` |
| W3-START:START-R | EASY | **A1 → T10** (apply in START2) | Checked `L9_BR.md:94-96`: the reference family is I_l = {U₀ ⊆ H_l, S₀ ⊄ U₀}, and for U ⊊ S₀ ⊆ H_l one has U₀ = U. So the Q = S₀ leading term needs only 2^{s₀} sets, with no N_ref, and C_L = 0 gives o₀ = O_P(√(log n/n)) in place of (log n)^{15κ_Q+1/2}/√n. The second-order term is negligible. Not done in START2 (`:138-139` keeps the polylog). Decaying a_{V,n}: D (θ_lo fixed elsewhere, `L9_BR.md:16-17,61`). Per-column C_{L,l}: A2. Leak scale √(log n/n) = START O1 (B\*). | `STATEMENT.md:306-314`; `lemmas/L9_BR.md:94-175` |
| W3-START:IF-START | EASY | **B** | The block-relative form is Lemma ASM (C1)(b) (`STATEMENT.md:213-219`; (B1) at `:232`), and partition-free is a presentation choice. The C_L = 0 rate plug-in belongs to START2 IF-START⁺ (A, T10). | `STATEMENT.md:334-338` |
| W3-START:OVL | EASY | **B** | (V-m) admitted by START2 OVL⁺ (P2). The slack and q̄ items are better done on OVL⁺ (T11). Joint-gain exponent: B (park). | `STATEMENT.md:339-344` |
| W3-START:MIS | EASY | **D** (A2 part) | Gaussian-row instance (jointly Gaussian candidate and omitted rows → (GR) exact): easy, A2, the start-mass twin of MISR Cor-G. The valuable part is a general deterministic μ ∉ span X_𝒞 with no (GR). μ = Xθ* is used only in (B1)(iii) and F2 (`L3_LEAK.md:36-40`), but the claim needs a careful pass through L2–L5 (D). | `STATEMENT.md:346-357` |
| W3-START:EX | EASY | **A1 → T8 / T10** | (i) Checked `L4_VIS.md:48-50`: for a > d the price Π = (a−d)[log(c_Q/p) − ½ log(n+1)] is strongly negative but is bounded by the constant 15 log(16s₀). Keeping it weakens (V-m) for \|N\| > \|D\| and lifts F-2's κ above ½, so (T1)(c) becomes available. → T8. (ii) G-1/G-2 rate √(log n/n) by the same N_ref observation as START-R → T10. (iii) Low-coherence null frame for F-1/F-3 at p ≫ n: A2 (closes `REPORT.md:44`). F-1 p/√log n: done by START2 (B). | `STATEMENT.md:359-371`; `lemmas/L11_EXAMPLES.md` |
| W3-START2:START-F | EASY | **B** (D part) | The block-relative 𝔏^{b,♯}: a presentation choice. Lemma ASM is already block-relative, and (B1) gives domination. Add one sentence, optional. The LEAK-0 wording erratum (§0) is real. Removing the √log p from clause (a) at Q ⊋ S₀: D (moderate). | `W3-START2/STATEMENT.md:82-110` |
| W3-START2:F2 | EASY | **B** | The averaged gain condition is (T1⁺)(b) with (J1) substituted (`P1_LEADING.md:133-135`); one remark, no ticket. Min with exp((\|δ\|+σh)²/(2τ²)): gains only at p = n^{o(1)} (C, off-priority). | `STATEMENT.md:112-117` |
| W3-START2:TRANSFER | EASY | **A2 → T10** | The self-normalised conditional bound is already proved design by design (`P1_LEADING.md:147-151`). State it, with the O_P-envelope form as a corollary and \|S₀\| ≤ s̄. ~1 h. | `STATEMENT.md:119-133` |
| W3-START2:IF-START | EASY | **A1 → T10** | The C_L = 0 rate of (T3⁺)(b) plugs into IF-START⁺ directly, and the T10 Q = S₀ route brings the Gaussian-row r_n to √(log n/n) (from n^{−1/2}e^{C_R√log n}). This feeds SAMP C(C-v). | `STATEMENT.md:176-180` |
| W3-START2:OVL | EASY | **A2 → T11** | Checked `P2_OVL.md:45-47`: visibility and (AL) are used only for π₀(𝓛(Q)) ≥ ½. State π₀(S₀) ≥ π₀(𝓛(Q))·n^{−E_n−ε} under (E), (GF-16) and the gain bound; slack e^{−M_n√log n} (fixed cut-off, as LEAK-0); q̄ = o(√(log n/log log n)). ~2 h. A Gaussian-row OVL still needs a level bridge (B). | `STATEMENT.md:181-189`; `lemmas/P2_OVL.md:40-58` |
| W3-START2:NEC | EASY | **A2 → T11** | (N2⁺⁺) many leakers: o₀ ≥ T₁ with N_n ≥ n^ν proper leakers gives collapse for c > 1 + 2(Ā − ν). This is the converse of the averaged 𝔏^♯ (Markov on the count, no independence). ~2 h. Single-block counterexample settling the count 17 − s₀ (START2-O1) for abstract partitions: D (cheap). Pointwise log p: T8. | `STATEMENT.md:154-173`; `REPORT.md:107-108` |
| W3-START2:START-R | EASY | **A2 → T10** | Checked `L9_BR.md:136-146` and `P4_BR.md:25-42`: N_ref enters only through E Ψ ≤ N_ref Φ_n and P(Eᶜ) ≤ (4 + 3N_ref)n^{−2}. So \|H_l\| ≤ exp(κ√log n) gives the main display with C_R + 15κ (partly closes START2-O2). Writing the factor in log p: C. The e^{c√log p} lower-bound remark for C_L > 0: D (heuristic; one remark at most). | `STATEMENT.md:134-152`; `lemmas/P4_BR.md:25-45` |

## 2. Rider groupings (Opus hours, lead + self-check; council not included)

| rider | contents | lemmas touched | effort | headline effect |
|---|---|---|---|---|
| **T4 (existing, RM2)** + | add the additive (BM-W) floor (RM2-F), Ex-Proxy with decaying θ_n (first witness BM-W ≠ BM-Q), and optionally the quantile form of (W) | `W3-RM2/lemmas/L2_width.md` §§1,4; `L6_examples.md` E4 | +2–3 h on T4 | weakens two premises of (C1) RM2-F |
| **T2 (existing)** | nothing new (leak profile = O2 = T2(c), already listed) | — | 0 | — |
| **T6 (existing)** | **appears done in RM2 v1.4** (`STATEMENT.md:4-5`, `SHARPNESS.md:40-44`); verify before Monday's leg | — | 0 | — |
| optional in the RM2 leg | Ex-Equi b < 3/8 and its converse (O4′, B\*); aggregated leak in Form R (D) | `L6_examples.md` E5; `L4_sandR_b.md` §§2–3 | 3–4 h; ½ day | examples / premise of (C2) |
| **T8 START-VIS** (new) | visibility at log n + 2 log p, pointwise (START-F); keep the (a−d)₊ Step-5 credit in (V-m) (EX); NEC (N2⁺)/(N3) and F4 with pointwise log p and drifting c_n | `W3-START/lemmas/L4_VIS.md` Steps 4–6, L4.2; `L7_NEC.md`; `L3_LEAK.md` L3.5 | 3–4 h | **weakens the visibility premise of START2 (T1⁺)** and makes sufficiency and necessity match for every p_n |
| **T10 START-RATE** (new) | Q = S₀ leading term without N_ref ⇒ o₀ = O_P(√(log n/n)) under Gaussian rows at C_L = 0; pass it to IF-START⁺; G-1/G-2 rows; \|H_l\| ≤ exp(κ√log n) for the main display; TRANSFER in self-normalised conditional form | `W3-START/lemmas/L9_BR.md` L9.5–L9.7; `W3-START2/lemmas/P4_BR.md`, `P1_LEADING.md` §4 | 4–6 h | **changes the display of START2 (T3⁺)(b) and IF-START⁺'s rate** |
| **T12 PSHARP-E** (new) | expectation lower bound for every p via truncation at ε/c_n (constant √((a+½)/π)); A2 with e^λ − 1 on (W-orth); correct the readings at `STATEMENT.md:84-88,109` | `W3-PSHARP/lemmas/A_log_factor.md` §§1,4,6 | 2–3 h | **changes Corollary A1 and Remark A3/B3 of PSHARP** (expectation rate exact for every p) |
| **T13 MISR-G/H** (new) | Cor-G(a) with the minimal hypothesis; Cor-H(a) under δ_n →_P 0; Cor-H uniform and conditional random-design forms; KL remark; Cor-G(b) cosmetics (A2) | `W3-MISR/lemmas/G_corollaries.md` G.1–G.3; `STATEMENT.md` §§5–6 | 2–3 h | corollary statements only; **input for DIST (§3)** |
| T9 START-LEAK (new, optional) | F1 exact Laplace exponent with ā; F3 with general G_n, no growth premise; F4 at n^ι columns (√c + √(2ι) < √(1+2A)) | `W3-START/lemmas/L3_LEAK.md` L3.1, L3.5; `L6_COROLLARIES.md` L6.1, L6.3 | 4–5 h | corollaries only (larger leakage range) |
| T11 START2-OVL/NEC (new, optional) | factorised OVL⁺ with e^{−M_n√log n} slack and slowly growing q̄; (N2⁺⁺) many leakers | `W3-START2/lemmas/P2_OVL.md`, `P3_NEC.md` | 3–4 h | propositions only |

T8 and T10 touch different START lemma files (L4/L7 vs L9/P4) and can run as one Opus leg on START2 v1.5, with T9
appended if time allows. T12 and T13 are independent half-day legs.

## 3. Distribution consistency (W3-DIST) — what bears on it

1. **Free omitted-variable corollary of DIST-1 (needs T13).** With the minimal Cor-G(a), the candidate problem is
   itself an (RD) instance: rows iid; given x_𝒞, y = α′ + x_𝒞ᵀβ^𝒞 + ε′ with ε′ ~ N(0, σ² + τ²) independent of the
   design (`W3-DIST/STATEMENT.md:24-28` asks exactly this, with ν_x arbitrary). So DIST-1/2/3 apply verbatim to a
   candidate run, with f* the KL projection. This gives Song–Liang Thm 4's out-of-sample statement in the population
   distance. **Caveat:** (RD) needs β^𝒞 = β_𝒞 + γ strictly sparse, and γ is typically dense. Hand to the DIST lead
   as a corollary once DIST-1 is checked; it is not a target change.
2. **σ*² fixed is removable at no cost.** MISR Lemma R′(a′) (`W3-MISR/STATEMENT.md:75-77`) plus the scale invariance
   of the Hellinger distance between normals (`G_corollaries.md`, G.3 Hellinger line) carry DIST-1 to any σ*²_n,
   exactly as Remark SNR (G.4) does for POST/POST2. One remark in DIST, no proof.
3. **The DIST-1 "sharp rate" needs its lower bound written.** f01 (Cor-H(b)) argues that log n/n is the method's rate
   even at fixed p: a coordinate with nθ²/v = small·log n is dropped, so ‖μ̂ − μ‖² ≍ v log n. DIST-3's remark gives
   the one-extra-variable distance √(log n/n) (`W3-DIST/STATEMENT.md:97-98`). For DIST-1(c)'s "sharp" claim, the DIST
   lead should record a lower bound of this kind, or soften the word.
4. **DIST-3 already has the Cor-H(a) form** (premise δ_n →_P 0), consistent with T13; there is nothing to change in DIST.

## 4. Proposals that would change a headline statement

| statement | change | class |
|---|---|---|
| START2 (T1⁺) START-F | visibility premise weaker: log n + 2 log p, plus the (a−d)₊ credit in (V-m) | A1 (T8) |
| START2 (T3⁺)(b) START-R, IF-START⁺ | Gaussian-row rate at C_L = 0, Q = S₀: √(log n/n) in place of (log n)^{15κ_Q+1/2}/√n; \|H_l\| up to exp(κ√log n) | A1 (T10) |
| PSHARP Prop. A / Cor. A1 | expectation lower bound for every p, constant √((a+½)/π); "no claim when log p = o(log n)" becomes in-probability only | A1 (T12) |
| RM2-F (C1) | (BM-W) additive at the constant level; (V) constant (T4) | A1 (T4) |
| MISR Cor-G(a), Cor-H | minimal hypotheses; random-design Cor-H | A1 (T13) |

None of these weakens a conclusion. Each is either a weaker premise or a sharper rate or constant.

## 5. What I checked, and what I did not

Checked against the files:
- MISR: `STATEMENT.md:25-197`; `G_corollaries.md:15-87`; `M_misr.md:135-170`; POST2 Claim D (`:99-118`).
- PSHARP: `STATEMENT.md:40-115`; `A_log_factor.md:15-25,110-125`. I re-derived the truncated second-moment bound.
- RM2:
  - `STATEMENT.md:120-220,255-275`; `SHARPNESS.md` (all);
  - `L2_width.md:70-110,205-220`; `L3_assemblyF.md:30-40`; `L4_sandR_b.md:108-176`; `L6_examples.md:360-384`.
- START:
  - `STATEMENT.md:130-160,197-290`; `L4_VIS.md:5-75`; `L5_ASM_STARTF.md:8-66`;
  - `L3_LEAK.md:1-30,92-110`; `L6_COROLLARIES.md:15-80`; `L9_BR.md:88-175`.
- START2: `STATEMENT.md:1-180`; `P2_OVL.md:40-58`; `P4_BR.md:25-45`; `REPORT.md:105-112`.

Not checked:
- the RM2-R aggregated-leak argument end to end;
- START-F at s₀ ≤ polylog (constant audit);
- START MIS with a general μ;
- the Ex-Equi 3/8 sketch;
- the single-block counterexample for 17 − s₀;
- PSHARP's coherence witness;
- every literature citation in the reports.

## 6. What HQ should do this week

1. Drop T6 from Monday's RM2 leg after a 5-minute check (`W3-RM2/STATEMENT.md:4-5`, `SHARPNESS.md:40-44`); run T2 + T4, with T4 enlarged by additive (BM-W) and Ex-Proxy decaying θ (+2–3 h).
2. Launch one Opus leg on START2 v1.5: T10 (Gaussian-row rate √(log n/n), \|H_l\| ≤ e^{κ√log n}) + T8 (visibility at log n + 2 log p, (V-m) credit); ~8–10 h; T9/T11 only if time remains before the Wed freeze.
3. Run T12 (PSHARP expectation for every p; ~3 h, Opus) before the chapter's sharpness section is assembled.
4. Run T13 (MISR Cor-G(a)/Cor-H restatements; ~2–3 h) and hand §3 items 1–3 to the DIST lead after DIST CP1, not before.
5. Editorial pass: the LEAK-0 "sharpens" wording (`W3-START2/STATEMENT.md:87-88`); MISR `ASSUMPTION_MAP.md:27` cross-cite to PSHARP; do not sell START2-P1 as a p ≫ n gain.
6. Record as named open items (no tickets): RM2-R aggregated leak (D), START MIS with general μ (D), Ex-Equi 3/8 (O4′, B\*), START2-O1 count.

**Counts (30 IMPROVABLE claims): A 17 (A1 9, A2 8) · B 11 (1 B\*) · C 0 as whole claims (cosmetic sub-items only) · D 2.** SHARP: 2, both agreed.
