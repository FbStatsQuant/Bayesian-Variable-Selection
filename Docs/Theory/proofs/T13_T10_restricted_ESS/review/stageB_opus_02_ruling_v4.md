# Stage B — Opus 5.5 (xhigh) reviewer, round 2: rulings on the log and review of PROOF_v4 (reply saved verbatim, 2026-10-22)

**T13 (T10) restricted ESS, Stage B round 2: rulings on the log, and review of PROOF_v4**

PROOF_v4 fixes all nine of my findings and the other reviewer's gap. Every definition the proof needs is now quoted in Appendix B. I checked every step against those quotes, and every step holds. I reran the v4 script and its output matches the printed output exactly. I found no fatal or gap finding in v4. One residual point remains: I cannot confirm from the packet that the Appendix B quotes match the source files (new finding 1). That is a question of where the quotes came from, not a step of the proof, so I do not hold the verdict on it.

**Files read (packet only)**
- <PC_TEMP_PATH>
- <PC_TEMP_PATH>
- <PC_TEMP_PATH> (all 11 pages; matches the .tex, and the Unicode in Appendix B renders correctly)
- From round 1: STATEMENT.md, REPORT_FORMAT.md, PROOF_v3.tex

**Computations this round** (read-only, `python -I -` on stdin, no files written)
- **R2-C1. v3 to v4 diff.** The only changes are the ones the lead describes in CLAIMS_OF_FATAL_FLAWS.md. Parts (i), (ii)(a), (iii) and (iv), Lemmas 2–4, the witness sets and the seven checks are unchanged in substance.
- **R2-C2. v4 Appendix A script rerun.** I piped PROOF_v4.tex lines 191–280 into Python and compared the result with the printed output (lines 284–313). They are identical once line endings are ignored (the .tex uses CRLF). This includes the two new enclosures:
  - r·e^D ∈ [0.0615463325985499584319, 0.0615463325985499584320]
  - r·e^{2D} ∈ [0.7185096848229484693078, 0.7185096848229484693079]

  All seven checks pass.
- **R2-C3. Block rules simulated.** I ran the quoted METHODOLOGY §6.3 rules (complete linkage on 1−|r_jl|, top-down cut at B = 6, next-fit packing) on the explicit round-1 data. The off-diagonal |r_jl| is at most 4e-16, so in exact arithmetic every distance is 1. The tie-break is my reading of "lexicographically on the sorted original-index lists". Result:
  - the blocks partition [40];
  - the largest block has 6 members, and J = 7;
  - the block of j₁ is columns 1–6 (1-based), so any j₂ from 7 to 40 is outside it.
- **R2-C4. Checksums and removed claims.**
  - The METHODOLOGY_v3.md SHA-256 in Appendix B (93043758…b8019c) matches STATEMENT.md.
  - The 00_COMMON.md SHA-256 (a7d05134…819e023d) appears only in the proof.
  - Searching v4 for "Cholesky", "helpers", "reduced enumeration" and "check_sonnet" finds nothing.

---

### (1) Rulings on the logged items

**B-O-1 (m(S) formula unverifiable): I agree with the lead's answer, and the fix works.**
- Lemma 1 now states G_S, z_S, H_S, D_S, Q_S, ν = 0.01 + n/2, a₀ = b₀ = 0.01, m(S), w, W_K and ϖ, citing Appendix B.
- Each matches the quote of 00_COMMON §1 lines 10–11 character for character in content. They also agree with METHODOLOGY §5: C_n = (2b₀)^{a₀} Γ(a₀ + n/2) / (π^{n/2} Γ(a₀)), and the log m(S) formula there.
- The quoted prior (β_S | σ² ~ N_k(0, nσ²(G_S + I_k)⁻¹), σ² ~ IG(a₀, b₀)) is the one whose marginal likelihood I derived in round 1. It gives exactly this m(S).
- My round-1 check (Lemma 4 closed form against this formula, agreeing to 1e-13) therefore now checks against the quoted source.

**B-O-2 (standardisation convention): I agree, and the fix works.**
- Both quotes use the n−1 denominator:
  - 00_COMMON §1 line 9: "s_y² = ‖Cy^r‖²/(n−1); so ‖x_j‖² = ‖y‖² = n − 1".
  - METHODOLOGY §4 item 4: "sample SD (denominator n − 1)".
- I checked the proof's argument for both forms:
  - 00_COMMON form: the raw columns are centred with ‖x_j‖² = 41, so D_x = I, s_y = 1, CX^r = X and Cy^r = y.
  - Method form: x/c stays centred and has sample SD 1/c, so dividing by it gives back x. The same holds for y.
- Lemma 4 is correct as written. Round-1 numerics: every SD computed with the n−1 denominator is 1.0000.

**B-O-3 (block properties): I agree, and the fix works.**
- (a) X only: 00_COMMON §2 line 18 says "deterministic in X", and §6.3 computes the distance "from X". The cut uses node sizes, B and "smallest index first"; the packing uses "dendrogram leaf order". None of these involve y.
- (b) Partition: the root holds all columns. Splitting a node into its two children preserves a partition. Packing takes "whole clusters only (a retained cluster is never split)".
- (c) Size cap: |C_b| ≤ B = min(⌊√n⌋, ⌊√p⌋, 16) = 6, quoted in both files.
- With (a)–(c), choosing j₂ after the blocks are fixed and before y is defined is legitimate. R2-C3 shows the quoted rules produce a partition with blocks of size at most 6 on these data.

**B-O-4 (budget and branch formulas): I agree, and the fix works.**
- Both sources quote H₀ = ⌈512N₀/2500⌉ (00_COMMON §2 line 24; METHODOLOGY §3 table).
- N₀, ℓ, T₀ and T_e = 4^e T₀ match the quotes.
- The exact-branch condition matches 00_COMMON §2 line 25 and METHODOLOGY §6.2.
- The arithmetic is correct (round-1 C5): Σ_{k≤21} C(40, k) = 749961486698 > 502400.

**B-O-5 (no implementation named): I agree, and the fix works.**
- §5.2 now gives one implementation: test b first, then midpoint bisection, then append the largest point that passed.
- It also notes that every pilot temperature passes on its first test, so the output does not depend on the implementation.
- A minor residual is new finding 2.

**B-O-6 (reading of the output grid; frozen-grid parenthetical): I agree, and the fix works.**
- §4(b) now states the reading and why it is the only one consistent with the rules.
- The quoted §6.7 ("start at u = 0 with the pilot temperatures as targets … continue from the appended point") supports it.
- The parenthetical is now explicitly treated as the special case.

**B-O-7 (coverage of the seven checks; uncertified display values): I agree, and the fix works.**
- (a) §5.1 now lists the exact facts separately: t₁ + t₂ < 1, |V_c| = 117, |V_d| = 782 ≤ 800, the interval counts 1 and 2 against T_e, the exact-branch inequality, and P > 0, R > 0.
- (b) The script now prints certified enclosures for r·e^D and r·e^{2D} (R2-C2). They agree with my independent 80-digit values from round 1: 0.06154633259855 and 0.718509684822948.

**B-O-8 (Z_c/P and α displayed identically): I agree, and the fix works.**
- The formula Z_c − A = ϖ(1)n^{−1/2}(38 + g₂) + 38ϖ(2)n^{−1}g₂ is correct. Z_c includes the 38 null singletons, {j₂}, and the 38 pairs {j₂, k}; A does not include them.
- The printed enclosures are disjoint: […023762, …023763] against […023757, …023758].

**B-O-9 (B and C_b used before definition; unneeded step): I agree, and the fix works.**
- Lemma 1 now proves m(U) ∈ (0, ∞) for every U ⊆ [p] without using the size cap.
- The argument is correct. A remark is in new finding 3.

**Other logged items I can judge**

**A1-1 (uncertified numerics): I agree, and the fix works.**
- The certification design is sound: exact rationals, `mpmath.iv` with outward rounding, and decisions made on internal interval endpoints.
- My round-1 spot checks support it. All ϖ(k) numerators and denominators have at most 71 bits, so they convert exactly. Over 900 random tests, iv.log, iv.exp and iv.sqrt always contained the 200-digit reference value.
- The script reproduces in both rounds.

**A1-2 (unaudited independent validation): I agree, and the fix works.** v4 contains no such claim (R2-C4).

**A1-3 (rounded values written as equalities): I agree, and the fix works.**
- "≈" now has a stated meaning.
- 1000/729 is formed exactly as `iv.mpf(1000)/iv.mpf(729)` and compared on its upper endpoint.

**Stage A round 2 exposition item (printed endpoints rounded to nearest): I agree, and the fix works.**
- `show()` converts the binary endpoints exactly to rationals and prints floor(lo·10²²) and ceil(hi·10²²).
- So each printed interval contains the internal interval.

**B-A2-1 (Astra #2: the method definitions cannot be verified from the packet): I agree, and the fix works.**
- The evidence is the same as for B-O-1 to B-O-4.
- The same residual provenance point applies (new finding 1).

---

### (2) Review of PROOF_v4

**Part-by-part coverage**
- **Lemma 1 (positivity):** Verified against the quoted definitions. ϖ > 0, D_S ∈ (0, ∞), Q_S ≥ 0 (algebra rechecked), and m(U) ∈ (0, ∞) for every U ⊆ [p]. It follows that γ₀ > 0 and d is finite.
- **Lemmas 2 and 3:** Verified; unchanged from v3.
- **(i):** Verified for all real u, v.
- **(ii)(a):** Verified.
- **(ii)(b):** Verified. Under the stated reading of the construction, each appended point satisfies ρ_V(φ_{t−1}, φ_t) ≥ 0.90, exactly so under EX-A. Strict progress holds, and φ_{t−1}, φ_t, w_t lie in 𝓔_grid.
- **(ii)(c):** Verified. The witness meets every element of the STATEMENT §0 definition of a method-class witness:
  - input conditions: METHODOLOGY §4 items 1–3, with n = 42 ≥ 3 and p = 40 ≥ 1;
  - standardisation leaves the data unchanged (both forms);
  - the exact-branch condition fails, so the SMC branch runs;
  - blocks, tables, γ₀ and d follow the quotes, with Lemma 4 verified;
  - V_c = V(V_c) has the method's form (117 ≤ 800, ∅ included);
  - tier e = 0 with T_e = 1000;
  - an implementation exists, with pilot list (1) and output grid (0, 1).

  The certified inequalities: a_c(1) ≥ 0.9, a_c(2) < 0.9, and 1 + χ² > 1000/729.
- **(ii)(d):** Verified. V_d = V(V_d), 782 ≤ 800. The pilot list (½, 1) passes both acceptance checks (certified), giving the grid (0, ½, 1). Because β > α (certified), a_d is strictly increasing. So the minimum over 𝓔_grid is attained only at φ₀, and the minimum over {w₁, w₂} is at w₁ = 1, not at w₂ = 3/2.
- **(iii):** Verified: the identity, the W = V case, the bound under coverage at v, and the grid consequence. There is no circularity.
- **(iv)(a):** Verified.
- **(iv)(b):** Verified: F′_V = F_V, ρ′_V = ρ_V, and the transcripts of the implementation coincide by induction.
- **"No assertion derives particle mixing from ESS":** Remark 5; nothing in the proof does so.

**Findings on PROOF_v4**

1. **Location:** Appendix B (preamble and quotations).
   **Severity:** exposition (provenance note; not a step of the proof).
   **Claim:** From the packet I cannot confirm that the quoted passages are faithful copies of 00_COMMON.md and METHODOLOGY_v3.md.
   **Evidence:**
   - The METHODOLOGY SHA-256 matches the one in STATEMENT.md. The 00_COMMON SHA-256 has nothing in the packet to compare against.
   - The "extraction script" that rejoined the wrapped lines is not in the packet.
   - Every quoted passage is consistent with STATEMENT.md §0: Ω and K, ϖ, the tables, γ₀ and d, V(𝒫), ρ_V, the construction, T_e = 4^e T₀, the exact-branch condition and the input conditions all agree. The quotes are also consistent with each other: 00_COMMON §1 against METHODOLOGY §5, and 00_COMMON §2 against METHODOLOGY §3, §6.2 and §6.3.
   - Copying mechanically with checksums is the right remedy. A one-time hash comparison by someone with access to the files would close this point.

2. **Location:** §5.2, "Grid" (the example implementation).
   **Severity:** exposition.
   **Claim:** The named implementation is only a sketch. It does not say:
   - which target comes next after a bisection append (b again, or the next pilot temperature);
   - when the validation and the T_e count are performed.

   **Evidence:** Any deterministic completion of the sketch is an implementation in the STATEMENT §0 sense, so existence is not in doubt. In both witnesses every pilot temperature passes on its first test, so none of the unspecified branches is ever reached. The witnesses' outputs are therefore correct for every completion.

3. **Location:** Lemma 1 proof ("in fact for m(U) with any U ⊆ [p] (the argument does not use |U| ≤ K)").
   **Severity:** exposition.
   **Claim:** METHODOLOGY §5 defines m(S) only for |S| ≤ K, so extending the formula to every U ⊆ [p] goes slightly beyond the source's domain. This is harmless.
   **Evidence:** The source itself guarantees that table sub-models stay within the cap. The quote of METHODOLOGY §6.3 says: "Since B ≤ K for n ≥ 3, no sub-model exceeds the cap." Positivity is therefore needed only where m is defined in the source, and the formula's positivity argument is valid there.

No fatal or gap finding remains.

Verdict: verified
