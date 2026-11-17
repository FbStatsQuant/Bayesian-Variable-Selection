# CHECKPOINT 2 — Recording package — Lemma VIS (visibility with a margin uniform in n; D112) — for the recorder's dry run → HQ GO

Lead: W3-AUDIT track A lead (Opus 5.5). Branch `theory/W3-AUDIT`; items as bound at 93cc6d0b (v1.5). Pure mathematics (no code).
Owner standards D106/D109: blind Opus line check, one Sol read (lock + line check), council (Sol + Opus), Opus-only diff
rounds, bound; Lean target yes; API blind-audit card ready (`track_V/reviews/API_CARD/`, rebuilt on 93cc6d0b).

## 1. New claim to register (Tier B, key lemma; ticket W3-AUDIT-V)
| id | kind | file | lines | sha256 (file) | status (proposed) | depends_on |
|---|---|---|---|---|---|---|
| `W3-AUDIT-V:VIS` | lemma | `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` | 29-59 | 126a7e483526c37af714310c73baffbdb87519d9d31ee5402bda5ca62a953239 | PROVED-CHECKED; council (below) | — (self-contained linear algebra and topology; cites dossier B8 for s5/fac2 only in a remark) |
Lean target: yes (finite-dimensional; Schur complements, Stieltjes inverses, closed unions of hyperplanes).
**Council record.** V-R1 (MANIFEST c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98): sol=9.5 PASS
(`reviews/VR1_council_sol.md`), opus=8.4 FAIL (F-1, a remark; repaired). Diff rounds, Opus only (D91): V-R2 opus=9.4 PASS
on 0bc1e0b4…; V-R3 opus=9.6 PASS on aee57913…. **HQ API audit V** (main `Theory_work/Wave3/API_AUDIT/auditV_results/`):
clauses VIS-0/a/b/c/d/e and UNIF NO-FINDING (2/2); V:SCOPE REFUTED (2/2) — the D18 exclusion; corrected in v1.5 with the
D18 finite computation (`reviews/D18/D18_VERDICT.md`, independent check D18C CONFIRMED). **Bound (current): `R4; MANIFEST
8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0; opus=9.5 PASS(reviews/VR4_council_opus.md)`** (verify OK). Gate reads: VLC1 (Opus, blind) VERIFIED WITH AMENDMENTS; VSL1 (Sol) LOCK WITH CHANGES + VERIFIED WITH
AMENDMENTS (one C on a proof remark, fixed).

## 2. What it discharges / where it is used
No registry condition is discharged: visibility is a hypothesis of Theorem 6 (A3) and Theorems 5, 10 (A4), not a
recorded condition. VIS gives **sufficient conditions** for it with an explicit uniform constant; it is for the scope
sentence (card rows 3.1, 3.3, 3.6 and the reader versions' "which designs" remarks) and for dossier B8. Recorder actions
(proposed): register the claim; add it as an `@stmt` source to the B8 dossier note and to the reader versions' design
remarks when HQ adopts the scope sentence below; no status change of any existing row.

## 3. Scope sentence (card text; HQ uses it for the scope) — updated after HQ's API audit V (D18)
**Visibility (Theorem 6 (A3); Theorems 5, 10 (A4)) holds with a margin uniform in n in two ways (Lemma VIS, W3-AUDIT track V).**
(i) *Aligned signs (VIS-a), explicit constant a = θ_lo·c₁₆:* when the precision matrix is, after flipping the signs of
some columns, a Stieltjes matrix (nonpositive off-diagonal entries), and within each block the truths' signs agree with
those flips. Our designs inside this way: independent columns (any signs); AR(ρ) with aligned truths (equal signs for
ρ > 0; for ρ < 0 the sign fixed by the parity of the column index) — track C's clustered placement of D02–D04; block
compound-symmetry designs (D05–D07, study S3, S4, S6 = D17) with any signs when the truths lie in different blocks (track
C's spread placement) and with aligned truths within a block (clustered placement); one-factor and compound-symmetry
designs with truths aligned with the loadings (P6 cs, the clustered placement of D10, D12, D14); S5/P6 s5 with aligned
truths (D16 clustered; B8's M-matrix argument). P6 fac2 with aligned truths is inside by B8's explicit computation.
(ii) *Generic position (VIS-b), constant a = c̲·dist(ϑ, B):* for any design with countably many local correlation
patterns (finitely many block, factor or tile types, block sizes fixed or growing; stationary designs with decaying
correlation such as AR(ρ), banded and Toeplitz), every truth vector ϑ off one fixed closed, Lebesgue-null, nowhere-dense
set B ⊆ ℝ^{s₀} of hyperplanes is visible with a margin that does not depend on n. **"Almost every ϑ" here means outside
this one fixed set B — the closure over all n of the local cancellation hyperplanes, limits included — not outside a
null set that changes with n.** Our designs inside this way (when ϑ ∉ B; track C's n-free population margins are
consistent): the spread (mixed-sign) placement of AR (D02–D04), of the one-factor designs D10 and D12, and of S5 (D16);
Toeplitz (D08, D09) in both placements; the three-factor designs D11, D13 and the clustered placement of D15; the
real-data-like designs D18 (riboflavin) and D19 (FRED-QD), both built from one fixed matrix and so with finitely many
local patterns. For D18 the finite computation is explicit: with the spread placement the four truths lie in four
different tiles once p ≥ 16352, so the margin is certified, a ≥ 0.1 (every visibility direction is a coordinate vector,
dist(ϑ, B) = min|θ_k| = 1.0, floor 0.1).
**Outside:** truth vectors on or next to B — the spread mixed-sign truths of the strong factor designs D14, D15
(population margin 0) and D18's clustered placement (four highly correlated truths in one tile: a 15-column conditioning
set gives |Cov| ≤ 6.9 × 10⁻⁹, exact arithmetic, so no usable margin can be certified). No design built from a fixed
matrix is excluded for its pattern structure.

## 4. Residual notes (no effect on the claim)
- Post-bind editorial items for the next manifest (all E): V-R3 R-1–R-3 (define n₀ once in (VIS-b); name D17 (S6) in the
  remark — a sign-route case in both placements; at ρ = 0 the AR alignment is more than needed); V-R4 E-1–E-4 (say in the
  STATEMENT that falling under (VIS-d)(i) makes B small but does not by itself make a design visible — D18's clustered
  placement is numerically on B; closure of patterns vs 𝒩 wording; "like the spread placements of D14, D15" and the range
  p > 4088 for D18 clustered; D18_VERDICT's 5e-14 attribution).
- Track C's population margins are evidence for "ϑ ∉ B" in the (VIS-b) designs, not a proof; for finite-pattern designs
  dist(ϑ, B) is a finite computation (minimum over finitely many normals) if HQ wants a certified number for a design.
