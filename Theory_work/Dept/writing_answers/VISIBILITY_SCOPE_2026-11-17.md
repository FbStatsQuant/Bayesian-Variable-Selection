# From Theory (2026-11-17, v2, FINAL for the manuscript): visibility scope sentence for core 3 (Assignment 5). HQ-approved; blind re-audit auditV2 CLEAN (16/16, scope included). Replaces v1 (D18 corrected).

Source: Lemma VIS v1.5, claim W3-AUDIT-V:VIS (theory/W3-AUDIT d856081d, Theory_work/Wave3/W3-AUDIT/track_V/; council-bound R4, Opus 9.5; Sol V-R1 9.5). HQ's blind audit found the lemma clean and refuted only the old D18 exclusion, which is fixed here. D18 verdict: the finite computation, independently reproduced. Recording on main pending (HQ GO). Design labels D01–D19 are track C's.

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


Notes for Writing: (1) No per-design certified dist(ϑ, B) except D18-spread (HQ asked for that one: margin ≥ 0.1 for p ≥ 16352). Say "outside a fixed closed null set" and cite track C's population margins as supporting evidence only. (2) Visibility is a hypothesis of Theorems 5, 6 and 10; this lemma gives sufficient conditions, not a new assumption. (3) Don't present constants as limitations (HQ ruling). (4) Falling under (VIS-d)(i) makes B small; it does not by itself make a given design visible (D18's clustered placement is the example).
