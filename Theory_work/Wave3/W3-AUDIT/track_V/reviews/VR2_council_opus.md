# VR2 council — seat `opus` (Claude Opus 5.5, high) — diff round — W3-AUDIT track V, V1 (Lemma VIS)

Manifest: `MANIFEST_VR2.txt`, `MANIFEST 0bc1e0b4474f34c422448fdfa25f704b5269ae8ec76fe70cd5f57e685567b946`;
`manifest.py verify` → `verify: OK` (run before reading). Files read (as the brief allows): `BRIEF_VR2_opus.md`,
`BRIEF_VR1_opus.md`, `VR1_council_opus.md`, `VR1_disposition.md`, `DIFF_VR1_to_VR2.patch`, `V1_VIS/STATEMENT.md` v1.3,
`V1_VIS/PROOF.md` v1.3, `V1_VIS/CHECK.md`, `V1_VIS/CITECHECK.txt`, `track_V/citecheck.py`, `TRACK_B.md:209-233`,
`track_C/RESULTS.md` (lines 1-80), `work/C_PLAN.md:8-22` (read in a slightly longer window; nothing beyond the design
table was used), `READER_VERSIONS.md` on origin/main (Thm 5: 565-600; Thm 6: 660-700; Thm 10: 1282-1295). The Sol
review `VR1_council_sol.md` was not needed and not used.

## Verdict summary
All six V-R1 Opus findings are resolved. The rewritten remark on track C (PROOF.md:96-104) is now correct: it
separates the placements, puts the clustered AR, block and one-factor cases in (VIS-a), puts AR-spread and the
three-factor designs outside (VIS-e), and handles blocks with spread truths correctly (which (VIS-a) case applies
depends on whether truths share a block). I checked it against B8 and against track C's design table and results and
found no disagreement. The new (VIS-d)(i) example (growing equicorrelated blocks) and the new (VIS-e) AR-alignment
sentence are correct. I raise no new C, S or F finding. There are four new E findings. One of them, N-1, is a side
effect of the E-2 repair: the per-n bound of (VIS-b) now needs "n ≥ n₀" written into it. It is a two-word fix, and I
recommend making it before the lock.

## 1. V-R1 Opus findings
| # | tag | finding (V-R1) | status | resolving line(s) |
|---|---|---|---|---|
| F-1 | F | track C's spread placements and "aligned factors" were called (VIS-a) instances | **RESOLVED** | PROOF.md:96-104. (a) The placements are now separated (96-97). The clustered AR(ρ > 0), block CS and one-factor D10/D12/D14 cases are (VIS-a) instances (97-99). AR-spread is a (VIS-b) case "(not aligned; there the (VIS-a) inequality itself can fail)" (101). Spread blocks are (VIS-a) instances only when the truths are in different blocks (99-100). The citation is now the full table `RESULTS.md:28-50`, which has both placement columns. (b) The three-factor designs D11, D13, D15 are "not covered by (VIS-e)" (101-102). |
| E-1 | E | "all large n" was not in the theorems' hypotheses | **RESOLVED** | STATEMENT.md:10-11 ("n ≥ n₀ … they are asymptotic, so n ≥ n₀ suffices"). I checked this against the three theorems: the conclusions that use (A4)/(A3) are limits (Thm 5: P(·) → 1, O_P; Thm 6: P(𝒢_n) → 1, P(Ŝ = S₀) → 1; Thm 10 inherits Thm 5's (A4)). Thm 6's "for every admissible n ≥ 3" delivery claim and Thm 5's lower bound "for every valid data set with n ≥ 4" do not use visibility. |
| E-2 | E | domain of n in 𝒩 | **RESOLVED** | STATEMENT.md:27 (𝒩 := closure of ∪_{n≥n₀} 𝒩_n). This has a side effect on unchanged text; see N-1. |
| E-3 | E | AR alignment not written out for ρ < 0 | **RESOLVED** | STATEMENT.md:55-56 ("s^k·sgn(θ*_k) is the same for every k ∈ S₀"); wording nit in N-4. |
| E-4 | E | the B8 sentence did not parse | **RESOLVED** | PROOF.md:102-104. s5 is shown inside by the M-matrix form of Σ⁻¹ (a (VIS-a) instance with D = I); fac2 by explicit conditional covariances. Both match TRACK_B.md:225-228. The non-B8 label "fac-aligned" is gone. |
| E-5 | E | growing equicorrelated blocks were not named in (VIS-d)(i) | **RESOLVED** | STATEMENT.md:48-49; parameter range nit in N-2. |

## 2. Diff-hunk verdicts
| hunk | content | verdict |
|---|---|---|
| CHECK.md @1-8 | status line; frozen hashes v1.3 | OK. `sha256sum` gives STATEMENT `958f7f481d8c` and PROOF `9d1904f8c30d`, which match. |
| CHECK.md @11-16 | V-R1 row; V-R2 pending row | OK. Matches `VR1_disposition.md` (Sol 9.5 PASS, Opus 8.4 FAIL, Opus-only diff round per D91). |
| CITECHECK.txt @1-6 | PROOF citation moved to `RESULTS.md:28-50` | OK. I recomputed all four block hashes read-only with citecheck.py's rule: 70f13b5ab5, 04ce79c82b, **87a4f25c69**, d9e1d973b7. All match. |
| PROOF.md @1 | v1.3 | OK. |
| PROOF.md @92-104 | the remark classifying track C's designs, rewritten | **OK, no new error.** I checked it clause by clause (below). Completeness and conservatism nits are in N-3. |
| STATEMENT.md @1 | v1.3 | OK. |
| STATEMENT.md @8-11 | target: "n ≥ n₀" with the reason | OK (E-1 above). |
| STATEMENT.md @24-27 | 𝒩 over n ≥ n₀; "n₀ as in (VIS-b)" | OK as a definition, but it makes the unchanged per-n bound of (VIS-b) (STATEMENT:36-37, PROOF:44 "Fix n … 𝒩_n ⊆ 𝒩") valid only for n ≥ n₀. See N-1 (E). |
| STATEMENT.md @45-51 | (VIS-d)(i): equicorrelated blocks with a fixed ρ_b, any (also growing) sizes | **Correct.** The labelled Σ_{n,V} (|V| ≤ 15 + s₀) has 1 on the diagonal, ρ_b for a shared block and 0 otherwise. So it is fixed by the block-sharing partition of V plus the labels: finitely many values, whatever the block sizes. c_m ≥ 1 − ρ_b (R: λ_min of a 19-entry equicorrelation(0.5) block = 0.5). The proof's general (i) argument (ℒ finite ⇒ ℒ̄ = ℒ) covers it. Nit: the parameter range (N-2). |
| STATEMENT.md @54-58 | (VIS-e): AR alignment written out | **Correct.** With d_l = s^l, the (VIS-a) alignment d_k sgn θ*_k = σ is s^k sgn θ*_k = σ. For ρ > 0 that means equal signs; for ρ < 0 it means sgn θ*_k = σ(−1)^k. For ρ ≠ 0 the graph of Σ⁻¹ (a path) is connected, so the condition must hold for all of S₀. Wording nit in N-4. |
| STATEMENT.md @83 | changelog v1.3 | OK. "STRONGER ((VIS-d)(i) example)" is honest: the example adds an instance and is justified by its own clause. |

**The rewritten remark, clause by clause** (track C designs from `C_PLAN.md:13-22`; B8 from `TRACK_B.md:221-231`):
- *IND in both placements: (VIS-a), alignment vacuous.* True: Σ⁻¹ = I and its graph has singleton components.
- *Clustered AR(ρ), ρ > 0.* Track C's AR designs are ρ = 0.5, 0.8 and 0.95, all positive. The clustered truths have
  signs (+, +, +, +), D = I, c₁₆ ≥ (1 − ρ)/(1 + ρ) uniformly in n. True.
- *Clustered block CS.* The four truths sit in one block with ρ_b > 0, so D = I and the alignment holds. Growing blocks
  (D07) still give c₁₆ ≥ 1 − ρ_b = 0.5 uniformly. True.
- *One-factor D10, D12, D14.* With one constant loading (D14 = P6's cs(0.5), `C_PLAN.md:20`), Σ_n is equicorrelation
  with ρ_n = h_p ∈ (0, 0.5]. (VIS-e) applies n by n with c₁₆ ≥ 1 − ρ_n ≥ 0.5. True. This is consistent with track C:
  D14 clustered is IN↑ (`RESULTS.md:44, 68`).
- *Spread blocks: (VIS-a) only if the truths are in different blocks, otherwise (VIS-b).* True for contiguous CS blocks
  with ρ_b > 0. Each block is connected in the graph of Σ⁻¹, so D must be constant on a block, and the spread signs
  alternate between consecutive truths. R check (blocks of 5, ρ_b = 0.7, truths at 1, 6, 11, 16 with signs + − + −,
  |U| ≤ 2): min |vis|/(|θ_j| Var(W_j | W_U)) = 1.000, as (VIS-a) predicts.
- *AR spread: not aligned, and the (VIS-a) inequality can fail.* True. The V-R1 example (p = 8) gave ratio 0.504. At
  track C's spacing (gap p/4; R, p = 16, truths 1, 5, 9, 13, ρ = 0.5, |U| ≤ 3) the ratio is 0.800 < 1, while
  min |vis| = 0.60 > 0, so (VIS-b) is the right route.
- *Toeplitz; three-factor D11, D13, D15; S5 spread: (VIS-b).* The three-factor designs are indeed not in (VIS-e). The
  remark claims nothing about their visibility, so this is consistent with track C (D15 spread pop 0, which "Not claimed"
  and the last bullet put on B). For Toeplitz, calling it a (VIS-b) case is conservative: see N-3(c).
- *B8's s5 and fac2.* The s5 sentence ("Σ⁻¹ … has all off-diagonal entries negative (an M-matrix)", TRACK_B:225-226)
  makes s5 with aligned truths a (VIS-a) instance with D = I, as the remark says. fac2 uses conditional covariances
  0.10/det and (0.6 + 0.875·m_opp)/det (TRACK_B:227-228); the remark says it is "an explicit formula for the conditional
  covariances", which is faithful. Citation `TRACK_B.md:222-228` covers both. No disagreement with B8.

## 3. Gates (changed content)
| gate | result | basis |
|---|---|---|
| G1 correctness of every step | PASS | every changed clause re-derived; R checks below; N-1 is a quantifier to add (E), and no consumer uses n < n₀ |
| G2 hypotheses used = stated | PASS | n ≥ n₀ now explicit in the target and in 𝒩; the (VIS-d)(i) example needs only its stated premise (c_m > 0) |
| G3 no hidden assumptions | PASS | the remark's track C attributions rest on C_PLAN's design table and RESULTS' placement definitions (24-25) |
| G4 theorems' hypotheses/notation quoted faithfully | PASS | Thm 5 (A4), Thm 6 (A3), Thm 10 (A4) re-read on origin/main; "asymptotic" holds for every conclusion that uses visibility |
| G5 scope (uniformity in n, n ≥ n₀, PD, which designs) | PASS | uniform constant only for n ≥ n₀, as stated; growing blocks keep c_m ≥ 1 − ρ_b; PD premise of (VIS-a) unchanged |
| G6 fidelity of examples / design statements to B8 and track C | PASS | F-1 repaired; the clause-by-clause check above found no conflict with B8 or track C |

## 4. Claim table
| claim | verdict |
|---|---|
| V1 | ACCEPT (v1.3; recommend the N-1 two-word fix at lock, the others optional) |

## 5. New findings (all E; none blocks)
**N-1 [E] — STATEMENT.md:36-37 and PROOF.md:44 (unchanged text, affected by the E-2 change).** 𝒩 now pools only
n ≥ n₀. The per-n bound "|Cov| ≥ c₁₆·dist(ϑ, B)" and its proof step "ν ∈ 𝒩_n ⊆ 𝒩" therefore hold only for n ≥ n₀;
for n < n₀ that n's hyperplanes need not lie in B. The conclusion actually used ("visibility holds for every n ≥ n₀
with a = c̲·δ") is unaffected. Also, "n₀ as in (VIS-b)" (STATEMENT:27) points to an n₀ that (VIS-b) only introduces
implicitly through c̲.
*Repair:* (VIS-b) "For every n ≥ n₀, j ∈ S₀ and U ∌ j …"; PROOF:44 "Fix n ≥ n₀, j, U"; STATEMENT:27 "(n₀: any index
with c₁₆(Σ_n) > 0 for n ≥ n₀, the same n₀ in (VIS-b) and (VIS-d))".

**N-2 [E] — STATEMENT.md:48-49: range of ρ_b for growing blocks.** An equicorrelated block whose size grows is
positive semidefinite only for ρ_b ≥ 0, which is the same reason the next example restricts to "ρ ∈ [0, 1) when
p → ∞". The premise c_m > 0 excludes bad ρ_b formally, but the example should say it.
*Repair:* "with a fixed ρ_b (ρ_b ∈ [0, 1) when block sizes grow)". Optionally add one clause to PROOF (VIS-d)(i)
(the Lean target): "equicorrelated blocks of a fixed ρ_b: Σ_V is fixed by the block-sharing partition of V and the
labels".

**N-3 [E] — PROOF.md:96-104: completeness and conservatism of the classification.**
(a) Some placements are not classified. One-factor spread D10 and D12 are equicorrelation with mixed signs, so they
are not aligned and fall to (VIS-b); D14 spread is on B. Also missing: S5 clustered (a (VIS-a) instance if D16's Σ is
B8's s5 matrix, as `C_PLAN.md:21` suggests), D17 = S6 (block CS with varying ρ_b, which (VIS-e)'s block combinations
cover), and D18/D19. Saying "the main cases" or adding one line would stop readers taking the list as exhaustive.
(b) In every track C cell the spread spacing ⌊p/4⌋ (p ≥ 200) exceeds the block size (5, or ⌈√p⌉ for D07). So track C's
spread block placements are in fact (VIS-a) instances, and the remark could say so instead of leaving it conditional.
(c) Toeplitz: in R, Σ⁻¹ for Σ_{jk} = (1 + |j − k|)^{−α} has all off-diagonals ≤ 0 for α = 1, 2 at p = 20, 60, 200
(min −0.586 and −0.252). With D = I the clustered positive truths reached the (VIS-a) bound exactly (ratio 1.000,
p = 16, |U| ≤ 3). So clustered Toeplitz looks like a (VIS-a) instance that (VIS-e) does not prove. Listing it as a
(VIS-b) case is conservative, not wrong. One parenthesis would avoid suggesting the sign route fails there: "Toeplitz
(no sign pattern proved here)".

**N-4 [E] — STATEMENT.md:55-56: wording.** "for ρ < 0 signs alternating with the column index" can be misread as
signs that alternate along the ordered truths (+ − + −). The intended condition is sgn θ*_k = σ(−1)^k, fixed by the
parity of k, so two truths at k = 1 and k = 3 must share a sign. Also, at ρ = 0 the stated condition (equal signs) is
sufficient but not needed, because Σ = I has singleton components. Suggest: "for ρ < 0, sgn θ*_k = σ(−1)^k (fixed by
the parity of k); for ρ = 0 no condition (IND)".

## 6. Score
**9.4 / 10** (C, S, F only: none. All V-R1 findings resolved. N-1 to N-4 are E and do not block.)

## 7. Checks performed
1. `manifest.py verify` → `verify: OK MANIFEST 0bc1e0b4…b946`.
2. `sha256sum` of STATEMENT/PROOF v1.3 = `958f7f481d8c` / `9d1904f8c30d` (CHECK.md).
3. CITECHECK block hashes recomputed read-only (4/4 match, incl. the new `RESULTS.md:28-50` = 87a4f25c69). `citecheck.py`
   was not run, because it rewrites CITECHECK.txt.
4. Theorem 5, 6, 10 statements re-read for the "asymptotic, so n ≥ n₀ suffices" sentence.
5. R (Rscript; numpy unavailable). Scripts in the session scratchpad, not in the repo:
   - Toeplitz α = 1, 2 inverse sign pattern at p = 20, 60, 200.
   - (VIS-a) ratio, minimised over j ∈ S₀ and |U| ≤ 3 (or ≤ 2), for Toeplitz clustered, AR(0.5) spread (0.800) and
     spread blocks (1.000).
   - λ_min of a 19-entry equicorrelation(0.5) block (0.5).
6. Remark vs B8 (TRACK_B:221-231) and vs track C (C_PLAN:13-22 designs, RESULTS:24-25 placements, RESULTS:28-50, 63-69
   results), clause by clause (section 2).
7. Confirmed by the D14 hand computation: cs(0.5), ϑ = (1.4, −1, 1.8, −1.2), j = k₂, U = ∅ gives
   vis = −0.5 + 0.5·(1.4 + 1.8 − 1.2) = 0. So D14 spread lies on B, matching "Not claimed" and track C's pop 0.

## 8. Not checked
- Track C's scripts (exact k_f = 1 loadings, the S6 block sizes, the three-factor group sizes); I relied on C_PLAN's table.
- P6 `DESIGN.md` and whether track C's D16 is exactly B8's s5 matrix.
- Unchanged text outside the diff, which the V-R1 Sol seat accepted (re-opened only for N-1).
- Lean formalisation (none in the frozen content).

COUNCIL-VERDICT round=R2 manifest=0bc1e0b4474f34c422448fdfa25f704b5269ae8ec76fe70cd5f57e685567b946 seat=opus score=9.4 gates=PASS
