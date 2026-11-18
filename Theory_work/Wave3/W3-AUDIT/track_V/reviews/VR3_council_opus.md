# VR3 council — seat `opus` (Claude Opus 5.5, high) — second diff round — W3-AUDIT track V, V1 (Lemma VIS)

Manifest: `MANIFEST_VR3.txt`, `MANIFEST aee579132aa33715622da7d337d485dd4e7db4303442066a02d3e885eb899f17`;
`manifest.py verify` → `verify: OK` (run before reading). `sha256sum` of STATEMENT/PROOF v1.4 = `267a8d1b0a41` /
`d40289f08eaf`, matching CHECK.md. Files read: `BRIEF_VR3_opus.md`, `BRIEF_VR2_opus.md`, `VR2_council_opus.md`,
`VR2_disposition.md`, `DIFF_VR2_to_VR3.patch`, `V1_VIS/STATEMENT.md` v1.4, `V1_VIS/PROOF.md` v1.4 (1-12, 40-113),
`V1_VIS/CITECHECK.txt`, `TRACK_B.md:209-233`, `track_C/RESULTS.md:18-70`, `work/C_PLAN.md:8-24`, and the V-R2→V-R3
manifest diff.
*Disclosure:* I listed the manifest diff with `diff`, and it showed that `INDEX.md` also changed. I then looked at its
git diff (read-only). That was outside the reading list: the V-R1 brief excludes INDEX.md. The change is one status
row. I did not use it for anything below. No git state was changed.

## Verdict summary
All four V-R2 E items are resolved in the text. The core repair for N-1 is made. Its optional third part (saying where
n₀ is defined) is not; I carry it forward as R-1 (E). I checked the new track C remark against C_PLAN's design table,
RESULTS' placement definitions and leak sets, and B8. Every new classification is correct: S5 clustered as an M-matrix
(VIS-a) instance, spread block designs as (VIS-a), Toeplitz as a (VIS-b) case with a hedged note, one-factor spread
D10/D12 as (VIS-b), and D19 as (VIS-b). Each claim is either proved by a clause of the lemma or makes no claim. The
v1.4 changelog's "WEAKER" tag for (VIS-b) is honest. I raise no C, S or F finding. There are three minor E items
(R-1 to R-3), and none of them blocks.

## 1. V-R2 E items
| # | finding (V-R2) | status | resolving line(s) |
|---|---|---|---|
| N-1 | (VIS-b) per-n bound valid only for n ≥ n₀ | **RESOLVED** | STATEMENT.md:36 "For every n ≥ n₀, every j ∈ S₀ and U ∌ j"; PROOF.md:44 "Fix n ≥ n₀, j, U". Changelog STATEMENT.md:84 tags it WEAKER "as used", which is correct: the conclusion at STATEMENT.md:40 was already for n ≥ n₀. The optional third part (STATEMENT.md:27 "n₀ as in (VIS-b)" still points to an n₀ that (VIS-b) does not define) was not applied. See R-1. |
| N-2 | ρ_b range for growing equicorrelated blocks | **RESOLVED** | STATEMENT.md:48 "a fixed ρ_b ∈ [0, 1) and any sizes (also growing)". This restricts the example for fixed sizes too, which is harmless: fixed-size negative-ρ_b blocks are still covered by "blocks from a fixed finite list" (47-48). The optional PROOF (i) clause was not added; that is acceptable because the general "ℒ finite" argument (PROOF.md:67) covers it. |
| N-3 | track C classification incomplete or too cautious | **RESOLVED** | PROOF.md:96-105. (a) Added: S5 clustered (99), one-factor spread D10/D12 and D14-on-B (103-104), D19 (105). (b) Spread block placements are now unconditional (VIS-a) instances, with the reason given (99-101). (c) Toeplitz is kept as (VIS-b) with the note that the Stieltjes property "is not proved here" (102-103). That is the conservative option I offered. Remaining completeness nit (D17): R-2. |
| N-4 | AR ρ < 0 wording | **RESOLVED** | STATEMENT.md:56 "for ρ < 0 sgn(θ*_k) = σ·(−1)^k for a common σ, i.e. the sign is fixed by the parity of k". The optional ρ = 0 half ("no condition") was not adopted; see R-3. |

## 2. Diff-hunk verdicts
| hunk | content | verdict |
|---|---|---|
| CHECK.md @1-8 | status; frozen hashes v1.4 | OK. The hashes match `sha256sum`. The V-R2 result is recorded faithfully (9.4 PASS, bound). |
| CHECK.md @12-17 | V-R2 row filled; V-R3 pending row | OK. Matches `VR2_disposition.md` (bound line, 4 E → v1.4). |
| PROOF.md @1 | v1.4 | OK. |
| PROOF.md @44 | "Fix n ≥ n₀, j, U" | **Correct.** For n ≥ n₀, 𝒩_n ⊆ ∪_{n≥n₀}𝒩_n ⊆ 𝒩, so ν^⊥ ⊆ B, and the rest of the step is unchanged. The "Uniform constant" step (48) already ranges over n ≥ n₀. |
| PROOF.md @96-107 | track C remark completed | **OK, no new error.** I checked it clause by clause below. |
| STATEMENT.md @1 | v1.4 | OK. |
| STATEMENT.md @36 | (VIS-b) "For every n ≥ n₀" | **Correct**, and it matches the proof. The statement is weaker, as tagged. No consumer uses n < n₀: the theorems are asymptotic (STATEMENT.md:11, accepted in V-R2). |
| STATEMENT.md @48 | ρ_b ∈ [0, 1) | **Correct.** For ρ_b ∈ [0, 1), a block of any size b has λ_min = 1 − ρ_b > 0. A labelled Σ_V is fixed by block-sharing and labels, so there are finitely many patterns. c_m ≥ 1 − max ρ_b. |
| STATEMENT.md @56 | AR ρ < 0: sgn θ*_k = σ(−1)^k | **Correct.** With d_l = s^l and s = −1, alignment d_k sgn θ*_k = σ gives sgn θ*_k = σ(−1)^k. The graph of the tridiagonal Σ⁻¹ is a path, which is connected for ρ ≠ 0, so the condition applies to all of S₀. |
| STATEMENT.md @84 | changelog v1.4 | OK. "WEAKER ((VIS-b) for n ≥ n₀ only, as used) / EQUAL" is honest. The remark is proof-only, so EQUAL is right for it. |

**The completed remark, clause by clause** (C_PLAN.md:8-22; RESULTS.md:24-25, 28-50; TRACK_B.md:221-231):
- *S5 clustered (D16) is a (VIS-a) instance.* C_PLAN:21 gives Σ = 0.3·11ᵀ + 0.4H + 0.3I, and B8 (TRACK_B:225-226)
  gives Σ⁻¹ = A⁻¹ − κJ with A = 0.3I + 0.4H. These are the same form. More generally, with u := A⁻¹1 > 0 for any block
  sizes, Sherman–Morrison gives off-diagonal entries (A⁻¹)_{ll′} − c·u_lu_{l′} < 0. So D = I, the graph is complete,
  and alignment means equal signs on all of S₀. The clustered β = (1.4, 1.0, 1.8, 1.2) is aligned, with c₁₆ ≥ λ_min(Σ)
  = 0.3. R check (H = block all-ones, block sizes {5×6}, {10×4}, {3,7,5,9}): max off-diagonal of Σ⁻¹ = −0.0115,
  −0.0043, −0.0069 (all < 0); λ_min = 0.300; the (VIS-a) ratio |Cov|/(|θ_j| Var(W_j | W_U)) over j ∈ S₀ and |U| ≤ 2
  from the next 8 columns is 1.80, 1.58, 1.44 (≥ 1, as (VIS-a) predicts). The claim is consistent with track C (D16 cl
  IN↑ 7.8 → 72) and with B8 ("S5 of the study (mixed signs)" unclear; the remark puts S5's spread placement in (VIS-b)).
- *Spread block CS designs are (VIS-a) instances, "since track C's spread truths lie in different blocks".* True.
  The spread step is ⌊p/4⌋ ≥ 50 for p ≥ 200, which is more than the block size 5 (D05/D06) and more than ⌈√p⌉ (D07;
  √p ≤ p/4 ⇔ p ≥ 16). Two indices at distance ≥ b cannot share a contiguous block of size b. Track C's leak sets
  confirm it: D05/D06 spread 20 = 4 blocks × 5; D07 spread 508 ≈ 4⌈√16000⌉ = 508. With one truth per component,
  alignment is vacuous, D = I, and c₁₆ ≥ 1 − ρ_b. This agrees with the V-R2 R check (ratio 1.000).
- *Toeplitz in both placements: (VIS-b), with the Stieltjes note.* No claim beyond "(VIS-b) case". The conditional
  "would put the clustered placement under (VIS-a)" is right (D = I, aligned truths), and "not proved here" is honest.
  The spread placement would stay outside (VIS-a) even if the matrix is Stieltjes, because a connected graph with mixed
  signs is not aligned. That matches "both placements".
- *One-factor spread D10, D12: (VIS-b); D14's spread truths lie on B.* With k_f = 1 and unit loadings, Σ_n is
  equicorrelation h_p > 0, and its complete graph with signs + − + − is not aligned, so (VIS-a) cannot apply. The D14
  parenthetical matches the V-R2 hand computation (vis = 0 at U = ∅) and "Not claimed" (STATEMENT.md:68-69). The
  remark makes no visibility claim for D10/D12, so there is no conflict with track C (both IN↑ there).
- *D19 FRED-QD-like tiles: (VIS-b).* No claim. Consistent with track C (sp UNCL↑, cl IN↑ small) and with B8
  ("typical user ... unclear").
- *Unchanged clauses* (IND; AR clustered/spread; one-factor clustered; three-factor; B8 s5/fac2) are as accepted in
  V-R2. The citation `TRACK_B.md:222-228` is unchanged and CITECHECK still lists it OK. CITECHECK.txt is unchanged
  between the manifests, which is right: no citation was added or moved.

## 3. Findings (all E; none blocks)
**R-1 [E] — STATEMENT.md:27 (N-1 residue).** "(n₀ as in (VIS-b))" still points to an n₀ that (VIS-b) uses but does
not define (36, 39). Mathematically this is harmless. Any n₀ works as long as 𝒩, c̲, δ and c_m are all formed over the
same n ≥ n₀, and the text uses one n₀ throughout. Only the cross-reference is loose. *Optional repair:* "(n₀: a fixed
index of the design sequence, the same in (VIS-b) and (VIS-d))".

**R-2 [E] — PROOF.md:96-105: D17 (S6) not named.** The remark is now presented as a classification of track C. D18 is
handled in "Not claimed" (STATEMENT.md:70-71), but D17 (block CS with ρ_b = 0.4–0.9, C_PLAN:21) is in neither list.
It is in fact a (VIS-a) instance in both placements. It is a block-diagonal combination of equicorrelation blocks
((VIS-e)). Its leak sets 20 / 5 show blocks of 5, so the spread truths fall in different blocks. "The block
compound-symmetry designs" may be meant to include it, but a reader matching IDs will not see D17. *Optional repair:*
"of the block compound-symmetry designs (D05–D07, and S6 = D17)".

**R-3 [E] — STATEMENT.md:55-56: ρ = 0 inside the AR item.** With s := +1 at ρ = 0, the AR alignment asks for equal
signs. At ρ = 0, Σ = I has singleton components, so no condition is needed. The text is sufficient, not wrong, and IND
is listed separately in the same item. Optional.

## 4. Gates (changed content)
| gate | result | basis |
|---|---|---|
| G1 correctness of every step | PASS | PROOF:44 re-derived with n ≥ n₀; ρ_b range, AR parity and every new remark clause checked, with R checks for S5 |
| G2 hypotheses used = stated | PASS | (VIS-b) now states n ≥ n₀, which is the range the proof uses; the S5 and spread-block claims rest only on (VIS-a)/(VIS-e) premises |
| G3 no hidden assumptions | PASS | "different blocks" follows from C_PLAN's step ⌊p/4⌋ and block sizes, and track C's leak sets confirm it; the S5 form comes from C_PLAN:21 = B8 s5 |
| G4 theorems' hypotheses/notation quoted faithfully | PASS | target text unchanged since V-R2 |
| G5 scope (uniformity in n, n ≥ n₀, PD, which designs) | PASS | the narrowing to n ≥ n₀ is tagged WEAKER; the Toeplitz and D19 entries claim nothing; Toeplitz-Stieltjes is explicitly unproved |
| G6 fidelity to B8 and track C | PASS | S5 cl, the spread blocks, D10/D12/D14 sp and D19 all agree with RESULTS:28-50 and TRACK_B:221-231; D17 omission is R-2 (E) |

## 5. Claim table
| claim | verdict |
|---|---|
| V1 | ACCEPT (v1.4 as frozen; R-1 to R-3 optional) |

## 6. Score
**9.6 / 10** (no C, S or F finding; all V-R2 items resolved; three optional E nits).

## 7. Checks performed
1. `manifest.py verify` → `verify: OK MANIFEST aee57913…9f17`. Manifest diff V-R2 → V-R3: INDEX.md, CHECK.md,
   PROOF.md and STATEMENT.md changed; CITECHECK.txt, citecheck.py and the EXT files did not.
2. `sha256sum` STATEMENT/PROOF = `267a8d1b0a41` / `d40289f08eaf` (CHECK.md).
3. R (Rscript; script in the session scratchpad, not the repo): S5 Σ = 0.3·11ᵀ + 0.4H + 0.3I for three block-size
   patterns. Σ⁻¹ off-diagonal entries are all negative; λ_min = 0.3; the (VIS-a) ratio is ≥ 1 for the clustered aligned truths.
4. Spread-block separation, from C_PLAN's step ⌊p/4⌋ and block sizes, cross-checked against RESULTS' leak sets.
5. Each new remark clause compared against C_PLAN:8-22, RESULTS:24-25/28-50/63-69 and TRACK_B:221-231.

## 8. Not checked
- `gen_dev_data.R` (the exact H of S5, the S6 block sizes, contiguity of blocks). I relied on C_PLAN and on the leak-set
  evidence.
- Unchanged text outside the diff (accepted in V-R1/V-R2).
- Lean formalisation (none in the frozen content).

COUNCIL-VERDICT round=R3 manifest=aee579132aa33715622da7d337d485dd4e7db4303442066a02d3e885eb899f17 seat=opus score=9.6 gates=PASS
