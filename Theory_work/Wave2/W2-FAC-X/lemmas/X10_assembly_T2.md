# X10 — Assembly for Theorem FAC-GL (claims (G3), (G4) of STATEMENT_T2)

Status: **PROVED (by this seat, unchecked)** (lemma check R12: **VERIFIED**, conditional on its path inputs), given the inputs with their recorded statuses (as listed in X6 and FACB L5;
T2/L4r_path.md "PROVED (by this seat, unchecked)"; X8, X9 "PROVED (by this seat, unchecked)").

**𝒦_n.** Let 𝒦_n := {deterministic LS0 from the emitted centre with cap a_n = ℓ_n + |S̃₀| scores S₀}. On the start event
of X8 (S̃₀ = S* = [p] ∖ N₀, unique) intersected with the path event of (G2) — L4r-S's event E_n for (G), X9's event for
(R) — the uncapped search from S* makes exactly |S* ∖ S₀| ≤ |S̃₀| ≤ a_n null deletions and ends at S₀, a strict local
maximum; the prefix property (FINAL s7, Lemma CAP(a)) gives a certified end at S₀. The path statement is uniform over all
starts between S₀ and [p], so no independence between N₀ and the noise is used. Hence P(𝒦_nᶜ) → 0.

**(H0).** (G): λ_min(Σ_n) ≥ ψ_lo := 1 − λ_hi² gives the anchored eigenvalue conditions with φ₀² = ψ_lo and SE_w with
g₀ := ψ_lo (λ_min(X_AᵀX_A) ≥ (n − 1)ψ_lo); energy ‖μ‖² = (n − 1)ϑᵀΣ_{S₀S₀}ϑ ≤ (n − 1)s₀‖ϑ‖² =: Mn-type bound; BM-∞
since ϑ is fixed and nonzero; p ≤ n^{A₁} ≤ n (A = 1); s₀ ≤ K eventually. (R): X6.1 verbatim with c₀ := ψ_lo/5 (raw-design
event 𝒜_n of X8, common constants, every-sequence de-randomisation).

**(G3).** (G): FACB L5.3 verbatim ([OP] gives D_n ≤ P(𝒦_nᶜ); [M5-0] with (H0) and T03♯). (R): X6.3 verbatim (conditioning
on the raw design Z, integration). Hence D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).

**(G4).** (G): FACB L5.4 verbatim (Lemma S inputs for a fixed design with nonconstant columns; P(no output) = 0;
D′'s pathwise inclusion with 𝒦_n). (R): X6.4 verbatim. Hence P(no output) = 0 for every admissible n ≥ 3 and
P(Ŝ⁺ = S₀) → 1, CAL-free, with all of Proposition F's premises, allocation and total tier-1 fallback. ∎
