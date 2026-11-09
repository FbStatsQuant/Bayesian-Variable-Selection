# C-GROW — METHOD REQUIREMENTS (for C-ENG, via HQ)

**MR1 — LS0 move cap.** LS0 (local search from the start mode S̃₀; not yet in the production core) runs with move cap

    ℓ^{LS0} := ℓ_n + |S̃₀|,   ℓ_n = ⌈log₂(n + p + 1)⌉ (the production local-search cap),

instead of ℓ_n. Everything else in LS0 is unchanged (M §6.10 moves and scans, lexicographic tie rule, one further
scan after the last move, `local_limit` if that scan still improves, provenance `ls0`, no uniforms, GUARD-W
semantics). The final local search from the global best keeps ℓ_n.

*Why.* Theorem GROW (lemmas/L4_assembly.md) shows that, on the class of designs with a growing relevance set, LS0
reaches S₀ by deleting the extras of the start mode one at a time: exactly |S̃₀ ∖ S₀| moves. That number can exceed
ℓ_n. Numerics (numerics/D2_summary.md, D3_summary.md; S5 covariance, p = 100): |S̃₀ ∖ S₀| has median 16–37 at
n = 3200–12800; with ℓ_n LS0 scores S₀ in 2/40 and 0/40 runs; with ℓ_n + |S̃₀| in 80/80 runs.

*Cost.* At most ℓ_n + |S̃₀| + 1 ≤ ℓ_n + K + 1 scans of ≤ p + k*(p − k*) models each (SoP `02_method.tex:413`);
polynomial. On the theorem's event the actual number of moves is |S̃₀ ∖ S₀| (+1 scan). LS0 is deterministic given the
data, so a data-dependent cap does not affect operational closure [OP] or the stream/uniform accounting.

*Alternative accepted by the proof.* Any cap ≥ |S̃₀ ∖ S₀|, which is unknown, so in practice any cap ≥ |S̃₀| (e.g.
ℓ^{LS0} := max(ℓ_n, |S̃₀|)). *Why a smaller cap cannot carry the guarantee (after R05 item 2):* each local-search
move changes at most two memberships, so from S̃₀ ⊇ S₀ scoring S₀ needs at least ⌈|S̃₀ ∖ S₀|/2⌉ − 1 moves, and on the
theorem's events exactly |S̃₀ ∖ S₀| − 1; a cap o(|S̃₀|) therefore cannot give this LS0 descent guarantee when
|S̃₀ ∖ S₀| → ∞. This concerns the LS0 guarantee only, not discovery by the whole method (SMC and the final local search
may still score S₀); the S5 numerics above are finite-n evidence, not an asymptotic proof.
