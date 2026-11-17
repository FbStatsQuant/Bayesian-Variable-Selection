# CHECKPOINT 2 — Recording package — Lemma VIS (visibility with a margin uniform in n; D112) — for the recorder's dry run → HQ GO

Lead: W3-AUDIT track A lead (Opus 5.5). Branch `theory/W3-AUDIT`; items as bound at 7df2d81c. Pure mathematics (no code).
Owner standards D106/D109: blind Opus line check, one Sol read (lock + line check), council (Sol + Opus), Opus-only diff
rounds, bound; Lean target yes; API blind-audit card ready (`track_V/reviews/API_CARD/`).

## 1. New claim to register (Tier B, key lemma; ticket W3-AUDIT-V)
| id | kind | file | lines | sha256 (file) | status (proposed) | depends_on |
|---|---|---|---|---|---|---|
| `W3-AUDIT-V:VIS` | lemma | `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/STATEMENT.md` | 29-59 | 267a8d1b0a41e7341657854a7d1a9fb19aa034aeb41f8f98df99e93e8910bd4f | PROVED-CHECKED; council (below) | — (self-contained linear algebra and topology; cites dossier B8 for s5/fac2 only in a remark) |
Lean target: yes (finite-dimensional; Schur complements, Stieltjes inverses, closed unions of hyperplanes).
**Council record.** V-R1 (MANIFEST c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98): sol=9.5 PASS
(`reviews/VR1_council_sol.md`), opus=8.4 FAIL (F-1, a remark; repaired). Diff rounds, Opus only (D91): V-R2 opus=9.4 PASS
on 0bc1e0b4…; **bound: `R3; MANIFEST aee579132aa33715622da7d337d485dd4e7db4303442066a02d3e885eb899f17; opus=9.6 PASS(reviews/VR3_council_opus.md)`**
(verify OK). Gate reads: VLC1 (Opus, blind) VERIFIED WITH AMENDMENTS; VSL1 (Sol) LOCK WITH CHANGES + VERIFIED WITH
AMENDMENTS (one C on a proof remark, fixed).

## 2. What it discharges / where it is used
No registry condition is discharged: visibility is a hypothesis of Theorem 6 (A3) and Theorems 5, 10 (A4), not a
recorded condition. VIS gives **sufficient conditions** for it with an explicit uniform constant; it is for the scope
sentence (card rows 3.1, 3.3, 3.6 and the reader versions' "which designs" remarks) and for dossier B8. Recorder actions
(proposed): register the claim; add it as an `@stmt` source to the B8 dossier note and to the reader versions' design
remarks when HQ adopts the scope sentence below; no status change of any existing row.

## 3. Scope sentence (card text; HQ uses it for the scope)
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
FRED-QD-like tiles (D19).
**Outside:** the spread mixed-sign truths of the strong factor designs D14, D15 lie on B (population margin 0); designs
without a countable pattern structure (riboflavin-like D18) are not covered.

## 4. Residual notes (no effect on the claim)
- Post-bind editorial items (V-R3 Opus R-1–R-3, all optional E): define n₀ once in (VIS-b); name D17 (S6) in the remark
  (it is a sign-route case in both placements); at ρ = 0 the AR alignment is more than needed. For the next manifest.
- Track C's population margins are evidence for "ϑ ∉ B" in the (VIS-b) designs, not a proof; for finite-pattern designs
  dist(ϑ, B) is a finite computation (minimum over finitely many normals) if HQ wants a certified number for a design.
