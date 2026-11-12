# sharp1b — triage of the 12 completed sharpness verdicts

Author: HQ consultant (Fable 5.2, high), 2026-11-11. Read-only triage; no agents, no commit (HQ commits).
Inputs: `sharp1b/results/f00,f02,f08,f11,f12,f13,f19.md` (complete), `f20.md` (partial); the cited lemma files;
`Wave3/W3-RM/{STATEMENT,SHARPNESS}.md`; the in-flight `BVS-wt/W3-RM2/.../{STATEMENT,ASSUMPTION_MAP,CHECKPOINT_2}.md`
and `reviews/BT1_disposition.md`; `Wave3/PROGRAM.md` (stop list, tie-break). Classes and ticket numbers continue
`sharp1/TRIAGE.md` (T1–T5; T2 and T4 are queued as riders on W3-RM2).

Classes: **A** real and cheap, worth a ticket · **B** real but already known, superseded or out of scope
(**B\*** = known, undone, cheap) · **C** wrong, or not an improvement that matters.

## 0. Summary

Again 12 of 12 IMPROVABLE-EASY, for the same two reasons as sharp1 (the scale fires on any restatement; each request
sees one ticket). Seven of the 12 claims are family results on the PROGRAM stop list. I found no wrong proposal in the
steps I checked (§4). Two findings are new and worth acting on (T6, T7); one is a free addition to T2.

**Do the RM findings (f19) add anything beyond T2/T4? No new hypothesis-level item.** Every RM proposal is already
written down in `W3-RM/SHARPNESS.md` or is being done in W3-RM2:

| f19 proposal | where it already lives |
|---|---|
| RM-0: unique-mode event instead of {π(S₀) > ½} | SHARPNESS §5; **T2(b)** |
| RM-0: no delivery claim | **T2(a)** |
| RM-F: constant-level (V), no M_n → ∞ | SHARPNESS §2; **T4** |
| RM-F: polynomial Q; counting form of (L); dropping (N) | RM2 itself; RM2 open items O2, O1 |
| RM-F: joint visibility (JV_b) | SHARPNESS §2, recorded and not adopted; gives nothing in the partition-free form |
| RM-R: (N-χ)/sample (N-D) instead of (D-R), by conditioning on X | RM2 bridge (P8) with (W-R) on the realised design |
| RM-R: leak o(√(log n/n)), localisation o((log n/n)^{1/4}) | RM2 P3, one attempt inside L4, else O3 |
| RM-R: vanishing θ_min, PTV(a_n) | declared non-claim (RM §6, RM2 STATEMENT:291); medium |

Two small things f19 adds: **T2(c)** below, and one wording point for T4 — the exponent in η_A may be any constant
≥ limsup log p/log n; "A ≥ 1" is needed only by (T1-F). The second is cosmetic at p ≫ n. f19's remark that a Gram
floor gives an improving deletion at every lattice set (only best-move control is missing) is input for RM2's O1.

## 1. Per-claim triage

| # | claim | class | reason |
|---|---|---|---|
| 1 | W1-GEN:Thm-GEN (f00) | **B** (A residual) | An examples/limits row. Constant-level BM and M̄: T4's theme, on an example. Relative SEP, per-conclusion hypotheses, D_n ≤ P(S̃₀ ⊄ 𝒱) + P(Ω_nᶜ): restatements of an example. O(n^{−1/2}) for P(Ω_nᶜ): note R of sharp1. **Residual A:** the move count. `L4_search.md:30-34` bounds the path by 2^{v̄} − 1 states; `L3_descent.md:57-63` (L3.2(a)) already gives a gain ≥ L_n/(8C_R) − W_n for every move from a state missing a truth, so an energy budget bounds those moves by C‖μ‖²/L_n = O(1). That lemma is what a growing-Q masked-truth theorem needs → **T7**. |
| 2 | W1-PXN:Thm-PXN (f02) | **B** | Examples row; stop list. Mode event instead of Markov: T2(b), applies to every consumer. Dropping 𝒵_n from the D_n bound, rates: restatement / note R. β_min ≍ √(log n/n): moderate, family. SIZE relaxed to g ≤ B (the study's groups of 5): new work on a family → stop list. Would become an example of T7 if T7 gets a Gaussian-row form. |
| 3 | W2-FAC-A:Thm-FAC-L (f08) | **B** (stop list) | One factor, p < n^{1/6}: no exponent work for p ≤ K, no family tickets. Fixed M in (TV): T4's theme. Set-visibility "some V ∋ j": the block-relative (JV_b) again. (AG) slack, γ̄_n, zero loadings, second-order boundary: family polish. Path route: hard, stopped. |
| 4 | W2-FAC-PK:Thm-NEG (f11) | **C** | NEG is a limits remark. Raising the swap exponent from β < ½ to β* ≈ 0.54–0.68 is plausible (uniform residual-fraction bound at size K) but buys nothing: the limit needs only "more swaps than the cap slack ℓ_n + s₀", and any polynomial count gives that. Dropping (PK)/(PB): moderate, family. |
| 5 | W2-FAC-PK:Thm-PATH (f11) | **B** (stop list) | δ fixed → δ_n ≍ log log n/log n is a real sharpening of the sufficient cap on the exact-Gram class. It does not change the recorded cap proposal (ℓ_n + 2\|S̃₀\|) and no method change is on the table before D1. Keep f11 as input if P6 leads to a cap ticket. |
| 6 | W2-FAC-X:Thm-FAC-CS-iid (f12) | **B** (stop list) | n-dependent ϑ_n, (C1) on p ≤ n/2, restricted 𝔫, stating E[1 − π(S₀)] → 0: all easy, all on the compound-symmetry family. Exponent beyond ½: hard. |
| 7 | W2-LOC2:PLR (f13) | **B** | Superseded by W3-RM:RM-R and RM2-R. Polynomial \|Q\| is RM2. Fixed-fraction (R1)–(R3): RM2 states the general width condition (W-R), with (D-R^b) only as a sufficient form; the fixed-fraction analogue is recorded as LOW in W3-RM (SHARPNESS §4 end, REPORT:145-146) — B\*, small. Fixed θ_lo: (BM-W) in Form F, non-claim in Form R. Redundant feasibility dichotomy: C. |
| 8 | W2-LOC2:Thm-Poly (f13) | **A** (new) | The cutoff α > 17/2 comes from the norm-product bound \|z_U − z_0\| ≤ H₃v_n² with v_n = R_n^{−α} + √(log n/n) (`L6_poly.md` (P6)–(P8), checked): it forces a reference radius n^ρ, ρ > 1/(4α), and the count n^{15ρ}. The reviewer's entrywise bound with the triangle inequality d(l,v) + d(v,w) + d(w,k) ≥ d(l,k) gives a cross term O(n^{−1/2}r₀^{−α}) at radius r₀ = log n, hence α > 2. RM2 carries the same budget (15ρ + b < ½) and records it as an artefact with **no known weakening** (`ASSUMPTION_MAP.md:33`, registry line `A:H-size-rho = ARTEFACT`); P3 keeps "the same budget". → **T6**. α > 1 through Jaffard-type inverse decay: hard, B. |
| 9 | W2-LOC2:F-LOC2 (f13) | **B** | "State once under the PLR premises" is RM-0 plus T2(a). Global floor in Step 1 not needed: C. |
| 10 | W3-RM:RM-0 (f19) | **B** (queued) | T2(a), T2(b). New and free: **T2(c)**. |
| 11 | W3-RM:RM-F (f19) | **B** (queued) | T4; the rest is RM2 or its open items (table in §0). |
| 12 | W3-RM:RM-R (f19) | **B** (queued / in RM2) | RM2 (P8), P3/O3 (table in §0). |

Counts: A 1 (Thm-Poly), B with an A residual 1 (GEN), B 9, C 1 (NEG).

## 2. New tickets

**T6 — product-form localisation in Form R (f13). Rider on W3-RM2's Form R lemma (L4), next to P3, one attempt.**
Replace the norm bound on the selection-removal cross term by the entrywise bound: for v, w ∈ U ∖ H_l the term
a_v(R⁻¹)_{vw}b_w is controlled by the *product* of the three covariances, not by each separately. Abstractly,
(L-loc-R) becomes a product condition, weaker than the present two separate bounds by r_n. For the polynomial-decay
class this allows \|H_l\| polylogarithmic: the 15ρ term leaves the budget (Form R then has b < ½ as Form F), and the
example improves from α > 17/2 to α > 2. Cost: about a page plus the (P11)–(P15) arithmetic with λ = 0. Needs the
decay of the 15 × 15 inverse (the cofactor argument of (P1)) and a re-check of the interface with GROW L6.3–L6.4;
the reviewer checked the displayed steps only, and so did I. If the attempt fails, record it under O3.

**T7 — masked truths at growing Q: Theorem 3 without (V) (f00; also sharp1 f09). Moderate, not cheap; kill budget;
after RM2's council (it needs RM2's Toolkit-b).** Idea: an *underfit phase* before the descent. While the centre
misses a truth, every LS0 move gains order nθ²_minφ⁴ (GEN L3.2(a)), so the energy bound ‖μ‖² ≤ Mn allows O(1) such
moves; then the centre is a superset of S₀ in the lattice and RM-0 takes over; the cap is spent on at most
\|S̃₀\| + 2m₁ moves. Hypotheses: (L), floors, the lattice condition, fixed-order signals, and in place of (V) a
separation condition on Q — given any subset of Q, no outside column carries more than a fraction c_S of the best
inside gain (GEN's (H1b) with 𝒱 := Q). GEN and PXN's fixed-design core would become examples. Why now: W3-RM rated
this HIGH risk before a toolkit at growing \|Q\| existed; two blind reviews reach the same lemma independently; and the
numerics agree (W3-RM V1: conclusion held in 296/300 runs without (V); RM2 B3: a weak truth missing from the start
mode in 32/32 runs and LS0 adds it). Tie-break rank: design-agnosticism. First step with a kill budget: the
statement lock, i.e. whether the separation condition is a mild condition on (X, θ*) or a disguised family.

**T2(c) — addition to the RM-0 rider (f19).** State RM-0(a) for any deterministic down-closed family 𝓛′ ⊆ 𝓛 with
P([S₀, S̃₀] ⊆ 𝓛′) → 1 (the descent visits only subsets of S̃₀; checked against GROW L1.2's use in `L0_core`). The
lattice/width condition is then needed on 𝓛′ only, e.g. sets with at most m_n extras. No gain by itself; it is the
form in which RM2's open item O2 (counting leakage) would pay off. One line; add it when T2 is written.

## 3. Truncated requests (f18 W3-POST2, f20 W3-SAMP, f21 W3-SCR)

They carry 6, 4 and 6 claims in one request, which is why they hit max_tokens twice. Re-run with one claim per
request. f18 and f21 returned no text. f20 returned the review of Theorem D and the start of LT♯; two items there
look real and cheap, to be confirmed by the re-run, not ticketed yet:
* D: P-MAP can be localised to the completed-run event 𝒜 (P(𝒜 ∩ {S† ≠ S₀}) → 0 suffices); the C-theorem proof
  already uses that form. P(𝒜) → 1 is never assumed, so this matters.
* LT♯: "NC_r for every r ≤ 4" is more than the HPM clause uses; non-collapse of the pooled evidence appears to
  suffice (the text stops mid-argument). This touches the recorded open item "NC_r necessity".

## 4. What I checked, and what I did not

Checked against the files: every f19 proposal against `W3-RM/SHARPNESS.md` §2–§5 and RM2's STATEMENT, ASSUMPTION_MAP
and BT1 disposition; LOC2 `L6_poly.md` (P5)–(P8) (origin of 17/2); GEN (H1b), L3.2 and the L4 move count; PROGRAM
stop list. Not checked: the T6 cross-term bound beyond the displayed steps; the f11 exponent arithmetic; the f12
conditioning argument for 𝔫; f08's set-visibility step; any citation of the outside literature.
