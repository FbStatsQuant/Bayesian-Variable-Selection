# L4 — What the production local search does on the event of L3 (deterministic part of (C2))

Status: **PROVED (by this seat, unchecked)**; lemma check R04 (Codex Sol): VERIFIED-WITH-AMENDMENTS, amendments
applied (v2). Deterministic, from the search semantics M §6.10
(SoP `02_method.tex:463-467`; LS0: SoP `02_method.tex:490-499`).

**Search semantics used (verbatim content of M §6.10, as restated in SoP 02_method.tex:463-467).** From a centre:
scan every feasible flip and swap (additions beyond K excluded), the centre frozen during the scan; every scanned model
is scored; if the best scanned score strictly exceeds the centre's, move there (exact ties among scanned models: the
lexicographically smallest index set) and count one move; at most ℓ moves, then one further scan; stop earlier at the
first scan with no strict improvement (`local_certified`: the returned model is a scanned centre with no improving
neighbour); if the last scan still improves, set `local_limit`. For LS0 the centre is the start mode S̃₀, emitted
(scored) (SoP `02_method.tex:490-494`; premise OP-LS0).

The **uncapped greedy path** from C is the sequence C = S⁰, S¹, … where S^{t+1} is the scan-maximiser at S^t (tie rule
as above) if it strictly improves F(S^t), and the path stops otherwise. τ(C) := min{t : S^t = S₀} (∞ if never).

**Lemma L4.1.** Suppose the conclusion of Corollary L3.4 holds (for the data at hand) and |𝒱| ≤ min(v̄, K) (if S misses
a truth then |S| ≤ |𝒱| − 1, so the designated truth addition is feasible; extra deletions are always feasible; swaps
preserve size).
Then for every centre C ⊆ 𝒱:
(i) every state S^t of the uncapped path lies in 2^𝒱, F(S⁰) < F(S¹) < …, and τ(C) ≤ 2^{v̄} − 1;
(ii) the uncapped path stops at S₀ (no strict improvement there);
(iii) the capped production search from C performs exactly the scans and moves of the uncapped path up to its cap; it
scores S₀ if ℓ ≥ τ(C) − 1 (if τ(C) = 0, S₀ = C is the emitted centre); and if ℓ ≥ τ(C) the **search endpoint** is
S₀, its completed scan finds no strict improvement (the search certifies its endpoint), and the search does not end at
`local_limit`. (The public flag `local_certified` is evaluated on the finally returned HPM, SoP 02_method.tex:505-506;
it refers to S₀ only when the reported Ŝ⁺ equals this endpoint, e.g. on {π(S₀) > ½}. Not needed for D_n.)

*Proof.* (i) Induction: S⁰ = C ⊆ 𝒱. If S^t ⊆ 𝒱 and S^t ≠ S₀, Corollary L3.4 says every maximiser of F over the
feasible neighbours lies in 𝒱 and strictly exceeds F(S^t); the tie rule selects one of these maximisers, so S^{t+1}
exists, S^{t+1} ⊆ 𝒱 and F(S^{t+1}) > F(S^t). Strict monotonicity makes the states pairwise distinct; they lie in
2^𝒱, which has at most 2^{v̄} elements; the path cannot stop at a state ≠ S₀ (each such state has a strict
improvement) and cannot have more than 2^{v̄} distinct states, so it reaches S₀ after τ(C) ≤ 2^{v̄} − 1 moves.
(ii) By Corollary L3.4, S₀ has no feasible neighbour with F ≥ F(S₀), so the path stops there.
(iii) The capped search and the uncapped path make identical decisions while the move count is below ℓ (same
centres, same scans, same tie rule); the cap only truncates. S₀ = S^{τ} is a scanned neighbour of S^{τ−1}, hence scored
in the scan at S^{τ−1}. That scan is performed iff τ − 1 < ℓ (inside the loop) or τ − 1 = ℓ (the one further scan
after ℓ moves). If ℓ ≥ τ, the τ-th move is made, the centre is S₀, and the next scan (inside the loop if τ < ℓ, else
the final scan) finds no strict improvement by (ii): the search stops with S₀ a scanned centre without improving
neighbour (endpoint certified), and `local_limit` is not set. ∎

**Remarks.** (1) Only *centres* stay in 2^𝒱; scanned neighbours outside 𝒱 are scored (and enter the all-scored set),
which is harmless. (2) The bound 2^{v̄} − 1 is crude. A sharper count on LH (Φ(S*) = c moves) needs the separate LH lattice argument
(BS/W4-T38FULL/T38_PROOF.md:217-269, LH-LAT; its own status) and is not claimed here.
(3) Exact ties: the argument holds for any selection among maximisers, because all maximisers lie in 𝒱.
(4) Nothing about the HPM centre of the original final local search is claimed (Lemma 0(b) of W1-T37R: that search
cannot move to S₀ unless F(S₀) exceeds every pre-search score).
