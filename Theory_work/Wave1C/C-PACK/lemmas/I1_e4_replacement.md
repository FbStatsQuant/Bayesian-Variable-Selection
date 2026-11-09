# Item 1 (N3-USE) — e4 is not needed for consistency: audit, Lemma UM, Lemma UM-FP, premise replacement (v2)

Author: C-PACK lead (Claude Opus 5.5). **v2** (after statement lock R30 and cross-family check R33
`reviews/R33_item1_check_sol.md`, verdict GAP: 0 FATAL / 3 MAJOR / 4 MINOR, no counterexample to UM or UM-FP; all 7
findings applied, disposition `reviews/R33_disposition.md`). Status: PROVED (by this seat); XF-checked R33; v2 repairs re-read by R38 (blind mid-point, CONTINUE) and R39 (sweep, fixes applied); council C1 passed (Sol 9.0, Opus 8.7).
Aliases: `W1/` = `Theory_work/Wave1/`; `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`;
`SoP/` = `Theory_work/State_of_Project/sections/`; `CODE/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.

## 0. Premise e4 as recorded
"emitted LS0 centre = the prescribed smallest-size, lexicographically smallest start-mode maximiser (DP invariant N3
OPEN)" (`SoP/04_theory.tex:84`, quoted at `W1/W1-N3/STATEMENT.md:17-18`). S\* and N (number of smallest-size maximisers)
are defined at `W1/W1-N3/STATEMENT.md:79-83`. e4 has two parts: (e4-a) the centre is the **output of the start-mode
routine** (integration: LS0 is not in production code); (e4-b) that output is the **prescribed** maximiser (DP invariant
N3, the mathematical part).

## 1. Audit (occurrences and substantive uses)
Kinds: **D** = method definition / premise list; **U** = deduction using the centre; **T-move** = LS0 move tie rule;
**T-out** = reported-HPM order; **X** = use outside a uniqueness event (listed and resolved).

| # | location (quoted) | kind | what is used | resolution |
|---|---|---|---|---|
| P1 | `W1/W1-PXN/FINAL_PROOF.md:51-53` "on {π₀(S°) > ½} the start mode is unique, = S°, and exact max-plus DP + backtracking return it (N3 bypassed, not proved)" | U | centre = S° on {π₀(S°) > ½} | Lemma UM |
| P2 | `W1/W1-PXN/lemmas/LS_P6_repair.md:38-42` "On {π₀(S°) > ½}, S° is the unique global maximiser of π₀; exact max-plus maximisation and backtracking (CPP/v3_start.h: 178-239) then return S° … Premise retained: EX-A (exact scores and exact DP arithmetic)" | U | same; EX-A | Lemma UM; EX-A retained |
| P3 | `NBH/branch_snapshots/API-PXNGAP/PROOF.md:286-289` (P5) | U | same | Lemma UM |
| P4 | `W1/W1-PXN/STATEMENT.md:33` "centred at the exact start mode S̃₀ = argmax π₀ (… deterministic tie rule)" | D | definition | e4′ (§4) |
| P5 | `W1/W1-PXN/lemmas/LS_P6_repair.md:24` "the lexicographic rule picks one; Φ drops by 1" | T-move | any choice among best progress moves | not e4 |
| P6 | `NBH/branch_snapshots/API-PXNGAP/PROOF.md:106-108` (Lemma T(i), used via `W1/W1-PXN/FINAL_PROOF.md:14-15`) "On 𝒜_n every block object equals its group version: … S̃₀ = S̃₀^~, … and the LS0 centre is S̃₀^~." | **X** | off-event equality of the coded centre with a group-version centre, from equality of the **unordered** partition | **repaired in §1.1** (R33 #2): not true for a capped ordered routine in general; not needed |
| P7 | `W1/W1-PXN/REPORT.md:47`, `W1/W1-PXN/lemmas/ERRATA.md:17` (council C1-sol note) | D | historical descriptions of the original P5 bypass | preserve; C-PACK addendum points to Lemma UM and §1.1 |
| G1 | `W1/W1-GEN/STATEMENT.md:28`, `:43-44` premise "**e4** (…)" | D | premise list | e4′ (§4) |
| G2 | `W1/W1-GEN/lemmas/L2_centre.md:19-20` "On {π₀(S*) > ½} the maximiser of γ₀ over Ω is unique and equals S*; … whatever the tie rule." | U | uniqueness | Lemma UM |
| G3 | `W1/W1-GEN/lemmas/L2_centre.md:57-59` (step 9) "… any tie rule returns it; under premise e4 the emitted LS0 centre is S*." | U | identification on the event | Lemma UM |
| G4 | `W1/W1-GEN/lemmas/L5_assembly.md:41-45` "Premise e4 is used only on {π₀(S*) > ½} …" | U | same + integration | Lemma UM + e4′ |
| G5 | `W1/W1-GEN/lemmas/L5_assembly.md:11-16` ([OP] closure) "OP-LS0 gives execution of LS0 with the prescribed emitted centre (e4) and completed scans; … LS0 reads no uniforms, so the models it scores are a deterministic function of the data." | D (structural, all data) | the LS0 centre is a deterministic data function emitted and scanned on every potential output run | integration premise, kept in e4′ (§4, clause (iii)); no tie property used |
| G6 | `W1/W1-GEN/lemmas/00_MAIN.md:10`, `W1/W1-GEN/lemmas/L6_instances.md:42` "premises (incl. N3)" | D | premise lists | e4′ |
| G7 | `W1/W1-GEN/lemmas/L4_search.md:10,15,31,37` "the tie rule selects one of these maximisers" | T-move | any choice | not e4 |
| G8 | `W1/W1-GEN/lemmas/L7_counterexample.md:63-75` ((C6)) "Pick a proxy k ∈ C_b and put S′ := S̃₀ ∪ {k} ∈ Ω … contradicting maximality of S̃₀." | **X** | **global maximality** of the (random) centre, off any uniqueness event | **excluded** from the positive replacement: (C6) is a counterexample to the LS0 route, not a consistency conclusion; under EX-A, maximality of `res.S` is N3(a) (`W1/W1-N3/STATEMENT.md:115-116`), unconditionally (also under truncation). In native binary64, rounded maximality (N3(e)) does not imply exact maximality, so (C6) is **not** transferred to binary64 |
| G9 | `W1/W1-GEN/REPORT.md:16,30,97-98` (council C1-sol note) | D | explanatory summaries of the e4/N3 implementation premise; no additional deduction | read the current premise as e4′ of §4; EX-A, the deterministic emitted coded centre, OP-LS0 and completed scans remain; preserve historical quotations and verdicts |
| G10 | `W1/W1-GEN/lemmas/L5_assembly.md:69` "the deterministic tie rules (all chosen as measurable versions …)" (council C1-opus #1) | D (structural) | measurability of the centre as a data function | e4′ (ii): coded centre is a deterministic measurable data function on every branch |
| S1 | `SoP/04_theory.tex:84` (shared definition of e4) (council C1-opus #1) | D | premise definition used by the cards | C-PACK addendum (P-e4 item 18); N3 status unchanged |
| M1 | `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:254` (Theorem b1 step 1, used by Corollary b1-LH) "On {π₀(S°) > ½}, S̃₀ = S°: … no other state can have π₀-mass ≥ ½, so there is no tie." | U | uniqueness | Lemma UM |
| M2 | `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:168-172` Lemma LS-score (centre C₀ arbitrary, "C₀ ≠ S₀, or the centre is emitted") applied with C₀ = S° (`:258`) | U | fixed-data lemma | no tie property |
| M3 | `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:63` "the HPM over 𝒮̄⁺ is S₀, with no tie possible" | T-out | output order | not e4 |
| M4 | `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:263` "*Alternative for (M2), with a data-dependent centre.* … So (M1) can be weakened to P(S̃₀ ∈ R_{a,d}) → 1." | **X** | membership of a data-dependent centre in a repair region (status PROOF SKETCH, `:264`) | **excluded**: not used by Corollary b1-LH; not covered by e4′ |
| M5 | M5 card `SoP/04_theory.tex:505` "LS-score with the e4 centre"; `:521` "the e4 tie-DP invariant N3 is OPEN" | D | card wording | e4′ |

**Audit conclusion (R33 #1 text).** In the positive consistency proofs PXN (E)/(T)/(C), GEN (C1)/(C3)/(C3-fav)/(C4) and
their instances, and the deterministic-reference proof of M5(b1-LH), centre correctness is needed only to identify the
centre with the stated reference on {π₀(R)>½}. No smallest-size or lexicographic start-mode property is needed there.
This statement excludes GEN (C6), which uses global maximality and is instead supported under EX-A by N3(a), and excludes
the optional data-dependent-centre route in T38_PROOF.md:263–266. Structural integration and transfer identities are
accounted for separately (G5 → e4′(iii); P6 → §1.1). In every positive use, R ∈ {S°, S\*} is feasible and deterministic
given X and the fixed model parameters (PXN: `W1/W1-PXN/STATEMENT.md:13-19`; GEN: X-measurable certificate,
`W1/W1-GEN/lemmas/L5_assembly.md:68-82`; T38: deterministic S°, `T38_PROOF.md:249`).

### 1.1 Repair of PXN's centre transfer (R33 #2; C-PACK-local amendment, Wave1 not edited)
Lemma T(i) (P6) asserts equality of the LS0 centre with the group-version centre on all of 𝒜_n, deduced from equality of
the unordered block/group sets. For the prescribed mathematical size/lex maximiser this is order-free; for the capped
coded routine it is not: abstract counterexample (R33, `numerics/R33_falsify_out.txt`): p = 2, K = 1, λ = (−10, 0),
singleton blocks with entries 1, cap = 1: block order [[0],[1]] returns {0}, order [[1],[0]] returns {1} (same unordered
partition, same π₀, exact integer arithmetic, both truncated, neither singleton has mass > ½). The consistency proof does
not need that identity. **Replacement:**
> The unconditional transfer identity on 𝒜_n is used for the mathematical tables, π₀ and aggregation quantities. For a
> centre defined by the capped coded routine, do not assert off-event equality with a group-version centre merely from
> unordered partition equality. Instead, on 𝒜_n∩{π̃₀(S°)>½}, π₀(S°)=π̃₀(S°)>½ and Lemma UM gives the actual centre S°.
> Thus P(C₀≠S°)≤P(𝒜_nᶜ)+P(π̃₀(S°)≤½). In the start-mode-only FP variant, add the probability of the corresponding
> margin/encoding/execution failure. Any stronger equality of coded group and block centres requires identical ordered
> encodings and execution contracts.
This gives exactly PXN's (E) (P(S̃₀ = S°) → 1, `W1/W1-PXN/FINAL_PROOF.md:51-53`), since P(𝒜_nᶜ) → 0 (Theorem R) and
P(π̃₀(S°) ≤ ½) → 0 (P3′); every later step of PXN uses the centre only through C₀ = S° on 𝒯_n ⊆ {S̃₀ = S°}.

## 2. Lemma UM (exact arithmetic)
**Setting.** `W1/W1-N3/STATEMENT.md` §1: instance (p, K, C, λ, ρ), f(S) = λ(|S|) + Σ_b ρ_b(S ∩ C_b) on Ω_K = {S : |S| ≤ K},
γ₀ = e^f, π₀ = γ₀/Σ_{Ω_K}γ₀. In the method K = min(p, ⌊n/2⌋), λ = log ϖ (normalised capped BB(1,p)), ρ_b = log r_b with
r_b(U) = m(U)/m(∅) scored against the full response (`CODE/cpp/v3_score.h:40,63-70`; `CODE/cpp/v3_start.h:92-95`) — the
start π₀ of PXN (`W1/W1-PXN/STATEMENT.md:24-30`), GEN (`W1/W1-GEN/STATEMENT.md:26-28`; GEN's w differs from ϖ by a common
constant) and M5 (D0). R ∈ Ω_K throughout.

**Lemma UM.** Assume (H1)–(H4) of `W1/W1-N3/STATEMENT.md:92-109`. If argmax_{S∈Ω_K} f(S) = {R}, then
`start_mode(st, cap).S` = R. In particular this holds on {π₀(R) > ½}. It requires cap ≥ 1 and not a false truncation flag.

*Proof.* (i) Uniqueness gives 𝒜 = {R}, k\* = |R|, 𝒜\* = {R}, N = 1, S\* = R (`W1/W1-N3/STATEMENT.md:79-83`).
(ii) (H3): cap ≥ 1 = N; N3(c) (`:120-122`, "If N ≤ cap, then `res.S` = S\*") gives `res.S` = R. Alternatively N3(a)
(`:115-116`): `res.S` ∈ 𝒜\* = {R}. (iii) If π₀(R) > ½ then for S ∈ Ω_K ∖ {R}, π₀(S) ≤ 1 − π₀(R) < ½ < π₀(R), so
f(S) < f(R): uniqueness holds. ∎
Remarks. (1) N3(a)/(c) are outputs of W1-N3, status "PROVED-CHECKED" (W1-N3 REPORT §1; Wave-1, not adopted by HQ).
(2) At cap = 10⁶, N = 1 gives `truncated` = [N ≥ cap] = false; at cap = 1, `truncated` = true with the correct set
(`W1/W1-N3/STATEMENT.md:118-119`; observed `numerics/item1_um_checks_out.txt` (A)) — METHOD_REQUIREMENTS MR2.
(3) K = 0: Ω_K = {∅}, R = ∅, trivially returned.

## 3. Lemma UM-FP (binary64; the start-mode identification step only)
**Objects.** f\* = λ\*(|S|) + Σ_b ρ\*_b(S ∩ C_b), the mathematical objective (λ\* = log ϖ); λ̂, ρ̂_b the stored doubles
(`D.logprior`, `st.logr`); f̂(S) the exact real sum of the stored doubles; ĝ(S) = `st.log_gamma0(S)`
(`CODE/cpp/v3_start.h:54-69`): the left-to-right binary64 fold, from 0, of ρ̂_{b₁}(S_{b₁}), …, ρ̂_{b_m}(S_{b_m}) over the
m = m(S) ≤ min(J, |S|) blocks met by S in increasing block order, then fl(λ̂(|S|) + ·). u = 2⁻⁵³, γ_k = ku/(1 − ku),
**assumed ku < 1 for every index used** (incl. k = K in the crude bound). **Domains (R33 #5):** in all table-error and
magnitude maxima, k ranges over 0, …, K and U over subsets of C_b with |U| ≤ min(|C_b|, K); for η_ρ also U ≠ ∅ (η_ρ = 0 if
that set is empty); entries above the cap are excluded and may remain NaN.
- η := max_{S∈Ω_K}|f̂(S) − f\*(S)| ≤ η_λ + Kη_ρ, η_λ := max_k|λ̂(k) − λ\*(k)|, η_ρ := max_{b,U}|ρ̂_b(U) − ρ\*_b(U)|;
- ε := max_{S∈Ω_K} γ_{m(S)}(|λ̂(|S|)| + Σ_{b: S_b≠∅}|ρ̂_b(S_b)|) ≤ γ_K(Λ̂ + K T̂), Λ̂ := max_k|λ̂(k)|, T̂ := max_{b,U}|ρ̂_b(U)|;
- Δ(R) := f\*(R) − max_{S∈Ω_K∖{R}} f\*(S), with max ∅ = −∞ (so Δ(∅) = +∞ when K = 0; then ε = 0 and start_mode returns ∅).

**Fold bound.** |ĝ(S) − f̂(S)| ≤ γ_{m(S)}(|λ̂(|S|)| + Σ_{b:S_b≠∅}|ρ̂_b(S_b)|). *Proof.* ĝ(S) is recursive summation of
the m + 1 doubles (ρ̂_{b₁}, …, ρ̂_{b_m}, λ̂) in this order: 0 + ρ̂_{b₁} is exact; fl(λ̂ + s) = fl(s + λ̂) by commutativity
(not associativity). Under (H2-FP) (round-to-nearest, gradual underflow, no overflow) each addition is (a + b)(1 + δ),
|δ| ≤ u, exact when the result is subnormal (both operands and the sum lie on the 2⁻¹⁰⁷⁴ lattice). Expanding, each term
carries a product of ≤ m factors (1 + δ), so |ŝ − Σx_i| ≤ γ_m Σ|x_i| (Higham, *Accuracy and Stability of Numerical
Algorithms*, 2nd ed., 2002, §4.2); signed terms/cancellation are covered. For m = 0, λ̂ + 0 is exact. ∎

**Lemma UM-FP.** Assume (H1), (H2-FP), (H3), (H4). (a) If argmax_{Ω_K} ĝ = {R}, then `start_mode(st, cap).S` = R.
(b) If Δ(R) > 2(η + ε) (FP-TAB), then argmax_{Ω_K} ĝ = {R}, hence `res.S` = R.
*Proof.* (a) N3(e) (`W1/W1-N3/STATEMENT.md:128-132`): ĝ(`res.S`) = `res.lg0` = max_{Ω_K} ĝ, and `res.S` ∈ Ω_K (one code
per block, total size kbest ≤ K, `CODE/cpp/v3_start.h:198-212,226-228`); so `res.S` = R. (N3(e)'s proof,
`W1/W1-N3/lemmas/LFP_floating_point.md`, uses monotonicity of rounded addition so that a maximal rounded prefix is
retained and a tight path is processed at cap ≥ 1; it does not import lex correctness.)
(b) For S ≠ R: ĝ(R) ≥ f\*(R) − η − ε ≥ f\*(S) + Δ(R) − η − ε > f\*(S) + η + ε ≥ ĝ(S). ∎

**Scope (R33 #3).** All consumer assumptions, including EX-A outside the start-mode subcomputation, are retained. Under
EX-A, UM discharges the needed start-mode identification. Alternatively, for this identification step alone, assume H1,
H2-FP, H3, H4 and FP-TAB. Writing E_n={π₀*(R_n)>½}, an asymptotic centre conclusion follows if P(E_n)→1 and
P(E_n∩{Δ(R_n)≤2(η_n+ε_n)})→0, with encoding/execution failures likewise excluded or of vanishing probability. This does
not give a native-binary64 consistency theorem for the full method; dropping the remaining EX-A assumptions requires
additional scorer, search, ordering and operational contracts. (EX-A: "Exact mathematical scores, arithmetic, sums and
comparisons. This is an idealisation, not a validated floating-point property.", `SoP/04_theory.tex:78`.)

**Margins (R33 #7).** If π₀\*(R) ≥ 1 − t with 0 < t < ½, then Δ(R) ≥ log((1 − t)/t) (for S ≠ R,
f\*(R) − f\*(S) = log(π₀\*(R)/π₀\*(S)) and π₀\*(S) ≤ t). With 1 − π₀\*(R) = O_P(a_n), a_n → 0, log(1/a_n) − Δ(R) is bounded
above in probability; hence for every fixed δ > 0, P(Δ(R) ≥ (c − δ) log n) → 1, with c = ½ for PXN (a_n = √(log n/n),
`W1/W1-PXN/FINAL_PROOF.md:48`) and M5(b1-LH) (a_n = 2^B n^{−1/2}, `NBH/branch_snapshots/W6-FIXREV1/T38_PROOF.md:318`,
B ≤ 16), and c = κ for GEN (a_n = 2^B √(log n) n^{−κ}, `W1/W1-GEN/lemmas/L2_centre.md:18-19`). These are lower bounds,
not Δ ∼ c log n.

**What is needed in binary64 (R33 #7 text).** The cited concentration rates give logarithmic lower bounds on Δ, with the
explicit probability quantifier above. They do not give Δ∼c log n. For Ku bounded away from 1,
ε≤γ_K(Λ̂+KT̂)=O(uKΛ̂+uK²T̂); these crude upper bounds do not by themselves establish the margin condition uniformly at fixed
precision, nor do they prove a lower bound on the actual error. At K=100, conditional on Λ̂,T̂≤10³, the bound is about
1.1×10⁻⁹. The DATA diagnostics report the stored-table margin Δ̂ and law π̂₀, not the mathematical Δ and π₀*. They do not
establish which error term dominates. FP-TAB is the run condition 2(η+ε)<Δ(R). A sufficient, non-equivalent per-entry
condition is 2[η_λ+Kη_ρ+γ_K(Λ̂+KT̂)]<Δ(R). No scorer-error guarantee is asserted.
(The (e)-type lex failure of W1-N3 concerns ĝ-ties; under FP-TAB ĝ has no tie at its maximum.)

## 4. Premise replacement (output of item 1; patches in `patches/P_e4_consumers.md`)
In PXN ((E), (T), (C)), GEN ((C1), (C3), (C3-fav), (C4), premise list) and M5(b1-LH) (Theorem b1 step 1, Corollary b1-LH):
> **replace** "e4 (emitted LS0 centre = the prescribed smallest-size, lexicographically smallest start-mode maximiser;
> DP invariant N3 OPEN)"
> **by** "**e4′**: (i) the LS0 centre is `start_mode(st, cap).S` of the coded routine (`CODE/cpp/v3_start.h:183-240`), or a replacement routine satisfying METHOD_REQUIREMENTS MR1;
> Lemma UM then holds with W1-N3 (c) replaced by MR1's unique-maximiser property, while Lemma UM-FP applies only to the
> current routine (council C1-opus #2); H1
> and H4 of N3 are explicit inherited assumptions. (ii) The routine uses the same retained indices, K=min(p,⌊n/2⌋),
> ordered actual partition, full-response block tables and capped BB(1,p) prior as the mathematical π₀ in the consumer.
> Define the coded centre as a deterministic measurable data function on every branch, using hypothetical block/start
> objects on exact-enumeration branches. (iii) Wherever LS0 is required, its emitted starting centre is this data
> function, with the unchanged OP-LS0/scored-set/guard contracts. Its use is not vetoed merely because `res.truncated` is
> true. The cap is fixed in advance or a specified deterministic measurable data function satisfying H3–H4.
> (iv) Arithmetic: the consumer's EX-A (which includes (H2)); the binary64 alternative (H2-FP)+FP-TAB is available for
> the start-mode identification step only (§3, Scope)."
The step "on {π₀(R) > ½} the start mode is unique and the DP returns it (N3 bypassed)" is now **proved** by Lemma UM from
W1-N3 (c) (or (a)) with N = 1; PXN's off-event centre transfer is replaced by §1.1. What remains of e4 is **integration
only** (e4′ (i)–(iii); LS0 not in the production core; C-ENG; METHOD_REQUIREMENTS.md). The lexicographic rule and the e4
truncation fallback are not needed for any positive consistency statement of PXN, GEN or M5(b1-LH). GEN (C6) and the T38
data-dependent-centre route are outside this replacement (audit rows G8, M4).

## 5. Numerical falsification
- `numerics/item1_um_checks.py` → `_out.txt` (Sonnet helper; frozen start_mode via W1-N3's harness): (A) exact integer tables,
  17,136 runs on 5,712 unique-maximiser instances, `res.S` = R in all; N = 1 in all 4,942 with π₀(R) > ½; `truncated` = 1 at
  cap 1, 0 at cap ≥ 2. (B) binary64 near-ties with η = 0 (so Δ = Δ̂): Δ̂ > 2ε in 1,546 runs, 0 failures; Δ̂ ≤ 2ε in 1,041
  runs, 28 failures (all Δ̂/ε < 1). (C) DATA mode (coded scorer, n ∈ {50, 200, 800}, 20 seeds each): `res.S` = R̂ in 60/60;
  on the 53 runs with π̂₀(R̂) > ½ (stored-table law), Δ̂/(2ε) ≥ 7·10¹²; measured Λ̂ ∈ [6.8, 14.8], T̂ ∈ [4.7, 524]. η not tested.
- `numerics/R33_falsify.py` → `_out.txt` (reviewer R33): 2,407 instances (p ≤ 8; exact rationals for f\*, f̂, η, ε; nonzero η;
  magnitudes 2^−500..2^500, subnormals, K = 0, unread NaNs, shuffled block order, caps 1/2/10⁶): 1,912 satisfy FP-TAB, 0
  violations; negative control (margin 10⁻¹⁴ < 2(η+ε) ≈ 4.4·10⁻¹³) fails as allowed; block-order counterexample of §1.1.
