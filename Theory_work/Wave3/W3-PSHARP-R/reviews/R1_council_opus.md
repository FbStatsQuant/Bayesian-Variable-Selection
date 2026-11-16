# R1 council review — seat `opus` (Claude Opus 5.5, effort high; blind first read) — W3-PSHARP-R

Content reviewed: MANIFEST `fd8b32a5540e5afcfdb73b94048ba7a1324f30a89ade786508ea04e9295bfc30`
(`reviews/MANIFEST_R1.txt`). I recomputed the sha256 of every ticket file and of the seven external inputs. All 20 rows
match, and the digest of the stored rows reproduces `fd8b32a5…`, so this review covers exactly that content.
Read: every file the manifest covers, the external inputs in `reviews/INPUTS.txt`, and `reviews/CITECHECK.txt`. Nothing
else under `reviews/`, and neither `LOG.md` nor `CHECKPOINT_*.md`. To decode the labels (N-orth), (N-gauss), (S1) and (S2)
in `READER_DELTA.md` I also read the definitions in the on-disk W3-READER `READER_VERSIONS.md` (read-only, §3 and lines 26-27).
Scratch: `reviews/R1_scratch_opus/` (`check_trunc.py`; `ae_rerun_400k.txt`).

## Per-claim decision

| id | decision |
|---|---|
| `W3-PSHARP-R:AE` | ACCEPT |
| `W3-PSHARP-R:A2C` | ACCEPT |

I re-derived both claims, including every consumed parent step, and found them correct. The two blocking findings below
are in derived text (`TARGET.md` and `READER_DELTA.md`), not in the claims or their proofs. Because they are mine,
`gates=FAIL`.

## Gates

**G1 correctness — PASS.** Every step was re-derived.
- **Lemma T (AE §1).**
  - δ ≥ Y − Y², and E Y uses (c).
  - E Y² ≤ cT·L + L², from U² ≤ TU and pairwise independence. Only pairwise independence and a common law are used.
  - The algebra gives E δ ≥ L(e^{−e} min P(G_j) − cT − L). ✓
- **§2 truncated means.**
  - (i) is exact: 2√(2 log T)/√(2π) = 2√(log T/π).
  - (ii): P-A :30-37 use only t² ≤ τ ≤ d/2 and d ≥ 3, so they apply with τ = 2 log T.
  - The conversions τ²/(2d) = 2(log T)²/d and 3τ/(2d) = 3 log T/d are right.
  - Checked numerically for 5 pairs (d, T): the lower bound ≤ E U ≤ the upper bound, and (i) agrees to 1e-15 (`check_trunc.py`).
- **§3.**
  - (2p − 1 − s₀)/p ∈ [1, 2) because s₀ + 1 ≤ K ≤ p. Hence log T ∈ [ℓ_n − log(4/ϵ), ℓ_n], since log(2α) = log(ϵ/2) < 0.
  - T ≥ 1 for n ≥ (4/ϵ)², and a_n is right.
  - 2c_nN√(ℓ_n/π) = Λ^E_n, and c_nT = α. ✓
- **Lemma F.** The identity L(b − α − L) − Λ(1 − ϵ − Λ) = Λ[(θb − 1) + (ϵ − θα) + Λ(1 − θ²)] is correct. With θ ≤ 2, Λ < 1,
  |θ − 1| ≤ ϵ/16 and 1 − b ≤ ϵ/16, the bracket is ≥ ϵ/2 − 4·ϵ/16 − 2·ϵ/16 = ϵ/8 > 0.
  - In §5, θ⁺ ≤ e^{0.5} < 2 once n ≥ 4 and ψ_n ≤ ¼, so the hypothesis θ ≤ 2 holds from n₁ on. ✓
- **§4 (W-orth-E).**
  - P-A :53-63 use (G), (E), (C), (W-orth) and n ≥ 3. They do not use N → ∞. Re-derived: V ≤ σ*²E(1 + 0.04/(n−1)) + 1.06M + M′.
  - Decoupling: C = u_ju_jᵀ + P_j, and P_ju_j = 0 gives R_j ~ χ²_{n−2} independent of g_j. ✓
  - On G_j ∩ {g_j² ≤ 2 log T}: E ≤ (n − 1) + x√(2(n−1)) + 2 log T.
  - (1 + a)(1 + b) − 1 ≤ 1.02a + b for b ≤ 0.02, so e_n is as displayed.
  - Then νγ_j ≥ g_j²/2 − e_n log T. ✓
  - Lemma T(c) holds because U_j depends on g_j and G_j on R_j.
  - Rates: log T ≤ ψ_n√n and x_n = ψ_n^{−1/2} give e_n log T = O(ψ_n^{1/2} + ψ_n² + (1 + (M + M′)/σ*²)ψ_n/√n). n₁ is a function of (ϵ, (ω_n)) only. ✓
- **§5 (W-sph-E).**
  - P-A :79-81 and :86-99 re-derived: s_y² ≤ 3M + 4σ*² on G and E₂ ≥ n/4, which give C₀.
  - P(Gᶜ) ≤ 2/(n−1) + 16/n + 1/x. Neither step uses N → ∞.
  - Independence of (ζ_j) from ε: the conditional law given ε is fixed, so the factorisation argument is valid. The U_j are therefore independent of the ε-event G.
  - θ_n bounds ✓. e′_n log T ≤ C₀ψ_n/√n + 2xω′_n, using log T ≤ log(pn). The choice x_n = (ω′_n)^{−1/2} is fine. n₁ ✓.
- **§6.** Uniformity holds: N_n enters only through Λ^E_n. The random-(X_{S₀}, θ*) integration handles both signs of
  1 − ϵ − Λ^E_n, and the limit form follows. ✓
- **§7 A1-E.**
  - (W-orth) with all nulls gives p ≤ n − 1 + s₀ ≤ 2n. Λ^E_n → 0.
  - p = ⌊n^a⌋ gives ℓ_n = (a + ½) log n + O(1). Fixed p gives ℓ_n = ½ log n + O(1), hence r_n/√(2π). ✓
- **§8 A2-E.**
  - (F1)-(F3) ✓.
  - Step 0: B1 needs s₀ ≤ min(K − 1, p/2), which Setting-E and the hypothesis give. B1 yields δ_n ≥ (s₀+1)/(3√n + s₀ + 1) surely, so the rank condition follows along the sequence.
  - Step 1: sub-blocks inherit the witness hypotheses (growth is stated through p), Λ^E(𝒩^{(k)}) = kΔ_n, and the k* argument is right in both cases.
  - (i) and (ii) ✓.
- **A2C.**
  - §1: Λ_n bounded and log p → ∞ give s₀ = o(√n), K − s₀ → ∞, and c_nN ≤ (s₀ + 1)/√n.
  - §2: S(1) equality and S(2) with g = 0 give the D-ratio n^j and additive Q-decrements. The prior ratio Π(s₀+1+i)/(2p−1−s₀−i) ≥ P_n^j, and (1 − Σγ)^{−ν} ≥ Πe^{νγ_k}. ✓
  - §3: P-A :64-68 (using N ≤ n − 1) and P-A :46 ✓. e_j is monotone and homogeneous ✓.
  - §4: collision bound ✓.
  - §5: Σ_{j≥2} C(j,2)A^{j−2}/j! = e^A/2. B_n ≤ (c_nN)A_n = o_P(1). Lemma W(i) gives A_n ≥ (1 − ϵ′)Λ_n w.p. → 1. The order J₀ → ϵ, ϵ′ → n is legitimate. The equivalence and the expectation step ✓.
- **Refutation attempts.**
  - Bounded N: N = 1 and 3 with c = 10⁻³, and N = 2 with c = 10⁻², by Monte Carlo. E δ = 0.00294, 0.00879 and 0.0463, all above Lemma T's bound (0.00217, 0.00649, 0.0296).
  - Fixed p: N1 reproduces.
  - Huge p: (W-sph-E) needs (log p)² = o(n). On (W-orth-E) a small block with huge p only makes Λ^E_n tiny.
  - Growing s₀: covered by A2-E Step 0 and Step 1.
  - s₀ = 0: ρ̃ = y ≠ 0 and r₀ = 0, and every step goes through.
  - No counterexample found.

**G2 hypotheses used = stated — PASS.**
- AE (W-orth-E) uses (G), (E), (C), (W-orth), (log p)² = o(n) and s₀ + 1 ≤ K.
- AE (W-sph-E) uses the spherical structure and both growth conditions, plus m ≥ n/2 from s₀ + 1 ≤ K ≤ n/2.
- A2-E uses s₀ ≤ p/2 and B1. Without the rank condition, it gets that condition back from E δ_n → 0.
- A2C uses every listed hypothesis. Its explicit N_n → ∞ is implied by the others; that is harmless.
- Quantifiers match: ∀ϵ ∃n₀(ϵ, σ*², M, M′, sequences), uniform over designs, θ*, S₀ and 𝒩_n. The bound is in expectation for A-E, and in probability plus expectation for A2C.
- Every clause of §3.1-§3.4 is proved.

**G3 no hidden assumptions — PASS.**
- Domains: n ≥ 3 in §4 and n ≥ 4 in §5 (d ≥ 3) are both inside n₁. p ≥ 2 is standing. N ≥ 1, and r₀ ≤ s₀.
- What is random: ε, plus the null directions under (W-sph-E). S₀, p and 𝒩_n are deterministic, so Λ^E_n is deterministic.
- AE §4 decoupling: the independence used (g_j vs R_j for each j, and g_j iid across j) is exactly what holds. The dependence of R_j on the other scores is never used.
- AE §5 event: G is ε-measurable and (ζ_j) is independent of ε. Both were checked.

**G4 statuses, citations, records — PASS** (editorial items E-4, E-8 below).
- Both lemma files read "PROVED (by this seat, unchecked)", and REPORT quotes this verbatim with the right `status_source`.
- I spot-checked the cited parent line ranges (P-A :8-10, :12-24, :26-37, :45-46, :53-68, :75-99, :121; P-ST :32-44, :48-60, :63, :99, :101-102). Each says what is claimed. CITECHECK reports 0 MISS.
- The REGISTRY claims, statement and premise lines, conclusions, scope and implies edges match STATEMENT.
- The §6 implies table is right:
  - A1-E ⇒ Cor A1 second display: (W-sph) ⇒ (W-sph-E) for s₀ fixed, 2N/(2p−1−s₀) → 1, and ℓ_n ≥ log p once √n ≥ s₀ + 1.
  - A2C ⇒ Cor A2 for λ ∈ (0, ∞), because e^λ − 1 > λ.

**G5 constants and rates — PASS.**
- Λ^E_n = 2c_nN√(ℓ_n/π) ✓.
- √((a+½)/π) ✓. The fixed-p constant [2(p−s₀)/(2p−1−s₀)]/√(2π) ✓.
- e^λ − 1 and e^{−λ} ✓.
- T = ϵ/(4c_n) with c_nT = α ✓.
- The explicit inequalities (e_n, C₀, P(Gᶜ), the Lemma F slack ϵ/8) ✓.

**G6 faithfulness — FAIL** (F-1, F-2).
- These all hold:
  - The coded target: D, Q, ν, w(k) and π as in W3-POST :16-24.
  - The parent.
  - §4.1/§4.2: these are the right corrections of P-ST :84-88 and :109.
  - The numerics: the script computes the exact π on X'X = (n−1)I with the right importance weight. With `M = 400000` it reproduces `ae_fixed_p_out.txt` byte for byte. It is used as an observation only.
- Two derived texts claim more than the masters plus the listed bridges: TARGET states a two-sided rate at fixed p (F-1), and READER_DELTA states the growing-s₀ remark under (N-gauss) without a covering master or bridge (F-2).

## Sweep duties

1. **Statement copies.**
   - The A2C header (:9-13) matches STATEMENT §3.4. The AE lemma points to STATEMENT and does not restate it.
   - REPORT points by line, and all ranges are right (:39-57, :61-92, :94-100, :102-119, :121-129, :131-148, :142, :113-115).
   - TARGET: one mismatch, F-1.
   - READER_DELTA: one mismatch, F-2.
2. **Quantifiers and uniformity.**
   - n₀ dependence is as stated: (ϵ, (M + M′)/σ*², ω_n) for (W-orth), and (ϵ, C₀(σ*², M, M′), ω_n, ω′_n) for (W-sph).
   - N_n is not restricted.
   - The random clause gives P(𝒜_n)·(…).
3. **Scope against downstream uses.**
   - A1-E uses Prop A-E with the full null block, inside its scope.
   - A2-E uses Prop A-E on sub-blocks chosen per n. This is covered because n₀ does not depend on the block.
   - The consumed parent steps (P-A :26-37, :53-63, :75-99, :64-68, :45-46, :121) never use N → ∞, except :64-68 and :121. Those two are used only in A2C, which keeps N_n → ∞.
4. **REPORT and REGISTRY against STATEMENT.** Consistent. Minor premise-line item E-8.
5. **DEPS spot-check.** I recomputed sha256 for 10 rows (STMT, AE, A2C, PARENT:S, PARENT:A-proof, PARENT:STATEMENT, N1, READER_DELTA, REPORT, CITECHECK). All match `sha` and, where present, `checked_sha`. Every row under a claim is OK.

## Findings

**F-1 (F) — `TARGET.md:28`.**
- The parity row reads "A1-E(b): E δ_n ≍ r_n at fixed p". That is a two-sided rate.
- Cor A1-E(b) (STATEMENT :83-84) is a lower bound only. STATEMENT §4.1 :111-112 says explicitly "for fixed p the upper half is not checked here", and §5 claims no upper bound.
- *Correction:* replace the clause cell with "A1-E(b): E δ_n ≥ (1 − o(1))(s₀+1)[2(p−s₀)/(2p−1−s₀)] r_n/√(2π) at fixed p (a lower bound of order r_n; no upper bound claimed)".

**F-2 (F) — `READER_DELTA.md:47-48`, with bridge B3.7 at `:73`.**
- The remark reads "If s₀ is allowed to grow, then on these designs a posterior mean error of order √(log n/n) forces s₀ to stay bounded, for every p". "These designs" includes (N-gauss), whose S₀-columns X^r_{S₀} may be random.
- The master Cor A2-E (STATEMENT §3.3 :88-92) covers the spherical witness only through (W-sph-E). (W-sph-E) requires X_{S₀} and θ* deterministic (STATEMENT :52), and A2-E has no random-(X_{S₀}, θ*) clause. Prop A-E has one (§3.1 :70-72), and B3.5 uses it for the display.
- B3.7 marks the remark "EXISTS" for "(N-orth)/(N-gauss)", but no master covers the random-X^r_{S₀} case.
- The extension is true. Step 1 of AE §8 holds conditionally with a uniform n₀ and integrates with P(𝒜_n), which is 1 when the energy and coefficient bounds hold surely. Step 0 uses (B1), which holds surely, and r₀ ≤ s₀ is deterministic. Still, it is neither a master claim nor a listed bridge.
- *Correction (either):*
  - (a) restrict the reader sentence to "on orthogonal null columns, and on Gaussian null columns with the S₀-columns fixed", and in B3.7 write "(N-orth), or (N-gauss) with X^r_{S₀} deterministic"; or
  - (b) add a bridge "B3.8 | A2-E with random (X_{S₀}, θ*) | NEW one line | AE §8 Step 1 conditionally on (X_{S₀}, θ*) with uniform n₀ (§3.1 random clause), Step 0 by (B1) (sure), r₀ ≤ s₀ deterministic", and point B3.7 to it.

**E-1 (E) — `STATEMENT.md:122-123`, `lemmas/AE_expectation.md:160`.**
- Both say "E δ_n/Λ^E_n = 0.99–1.03 at n = 10⁶". The output at n = 10⁶ gives 0.990, 1.011, 1.022 and 1.014; the 1.028 is at n = 10⁴.
- *Correction:* "0.99–1.02 at n = 10⁶". For STATEMENT, which is locked, record this in ERRATA.

**E-2 (E) — `TARGET.md:36-38`.**
- "MC s.e. ≤ 5·10⁻⁴ relative" is wrong. 5·10⁻⁴ is the largest *absolute* s.e. (4.5·10⁻⁴); the relative s.e. reaches 2.2·10⁻³ (n = 100, p = 5).
- "1.01 → 1.02 (p = 5)" omits the (p = 5, s₀ = 2) row, which goes 0.967 → 1.014.
- *Correction:* "MC s.e. ≤ 5·10⁻⁴ absolute (≤ 2.2·10⁻³ relative)"; "p = 5: 1.01 → 1.02 (s₀ = 1), 0.97 → 1.01 (s₀ = 2)".

**E-3 (E) — `STATEMENT.md:22` (row C4), `TARGET.md:30`.**
- Both write "limsup π(S₀) ≤ e^{−λ}" with no mode of convergence. The parent's B1 cap at P-ST :101 is "surely", so this can be misread.
- *Correction:* "π(S₀) ≤ e^{−λ} + o_P(1) and limsup E π(S₀) ≤ e^{−λ}".

**E-4 (E) — `STATEMENT.md:133`.**
- The consumed list "Lemma S(1) incl. its equality case, S(2), S(4)" omits S(3). A2C §2 uses S(3) for γ_k ≥ 0, and the A2C header (:5) and the REGISTRY depends_on both list it.
- *Correction:* add S(3) (ERRATA).

**E-5 (E) — `STATEMENT.md:113`.**
- The falsity of an expectation upper bound of order √((1 ∨ log p)/n) when log p = o(log n) is attributed to "(A1-E(b), A2-E)". A2-E is about growing s₀ and is not the relevant result. For slowly growing p the relevant result is the A1-E main display with ℓ_n ≥ ½ log n.
- *Correction:* "(A1-E: main display with ℓ_n ≥ ½ log n, and (b))".

**E-6 (E) — `READER_DELTA.md:6` against `:62`.**
- Line 6 says the proofs are "not yet proved or checked". Line 62 says "the expectation display is proved, not yet independently checked".
- *Correction:* quote the verbatim status "PROVED (by this seat, unchecked)" in both places.

**E-7 (E) — `READER_DELTA.md:40`.**
- "By (b) with p = n^a": under (N-orth), A1-E(a) needs p = min(n − 1, ⌊n^a⌋) with 0 < a ≤ 1. The current reader text has the same shorthand.
- *Correction:* add "(under orthogonal null columns, p = min(n − 1, ⌊n^a⌋), a ≤ 1)".

**E-8 (E) — `REPORT.md:57`.**
- A2C's `premises: STATEMENT.md:29-37` does not include its in-line hypotheses at :96-98.
- *Correction:* `premises: STATEMENT.md:33-37,96-98`.

## Proposals (not findings)
- Add a random-(X_{S₀}, θ*) clause to Cor A2-E in a later version. The proof is the one sketched in F-2(b).
- A2C could also state the in-expectation form of A2-E at the critical scale, liminf E δ_n ≥ 1 − e^{−λ}. It is already
  there; it could be cross-referenced from READER_DELTA's critical-scale remark.

## Score and counts
- Mathematics: correct throughout.
- Blocking findings: two, both low severity and both in derived text, with one-line fixes.
- Counts by tag: C 0, S 0, F 2, E 8.
- Score: 8.6.

`COUNCIL-VERDICT round=R1 manifest=fd8b32a5540e5afcfdb73b94048ba7a1324f30a89ade786508ea04e9295bfc30 seat=opus score=8.6 gates=FAIL`
