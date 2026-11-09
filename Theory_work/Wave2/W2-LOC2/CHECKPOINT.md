# W2-LOC2 — CHECKPOINT (key lemma proved and checked) — 2026-11-09 ~08:50 CST

**State.** STATEMENT v1.1 LOCKED (R01 LOCK-WITH-CHANGES, 6/6 applied). Key lemma **NA-R** (`lemmas/L2_NAR.md`):
PROVED (by this seat, unchecked); R03 (Codex gpt-6.1-sol xhigh) VERIFIED-WITH-AMENDMENTS, all applied, no counterexample.
Other lemmas: L1_toolkit (L0′ quasi-polynomial toolkit + regularity) and L3_CTd (Combes–Thomas in ℝ^d, CD_d, RB, TAIL):
R02 VERIFIED-WITH-AMENDMENTS (1 MAJOR CD_d indexing fix), applied. L4_LOCd (Theorem LOC-d, Theorem LOC-BF), L5_assembly
(Theorem PLR), L7_delivery (Prop. F-LOC2): R04 V-W-A / V-W-A / VERIFIED, applied.

**Mechanism.** Whole-lattice NA without a 2^{|Q|} union: the population residual e_{T,l} = (reference in a ≤ m₀-dim
frame from ≤ p·n^{o(1)} frames) − (ℓ¹-bounded atom combination). Exact identity (I − P_T)x_l ∝ (I − P_T)Ce_{T,l}; sample
error O((q + log n)/√n); atoms bounded conditionally on ε. Applications: d-dimensional exponential locality (window
residual frames, column atoms, ℓ¹ bound from CT_d) and one-factor groups (frame (F_G, ξ_l), atoms ξ_v, ‖β‖₁ ≤ 1/b_lo).

**What this gives (pending mid-point, sweep, council).** (a) Reported-model consistency + delivery for d-dimensional
exponentially local Gaussian designs on minimum-separated sites (grids, images, spatial), any fixed d. (c) Growing
one-factor / compound-symmetric groups up to (log n)^κ with ≤ one truth per group — the middle regime and beyond, incl.
sequences where the old GROW/LOC route is VN-obstructed. No method change (shipped cap ℓ_n + |S̃₀|).

**Open.** (b) polynomial-decay Toeplitz: parallel Sol prover running (`lemmas/L6_poly.md`, unlocked stretch). Next:
mid-point R05 (fresh Sol xhigh), sweep R06, citation check, council.
