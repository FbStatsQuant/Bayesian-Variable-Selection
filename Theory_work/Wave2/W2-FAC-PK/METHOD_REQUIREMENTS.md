# W2-FAC-PK — METHOD_REQUIREMENTS (HQ decides on adoption)

Scope of the evidence: exact-Gram compound symmetry, K < p ≤ n − 1 (STATEMENT v3.1 — LOCKED, including the flagged
cap-evaluation restriction for delivery). Statuses: REPORT.md §3.

## The problem with the merged cap (MR1 (C-GROW), ℓ_n + |S̃₀|)
Theorem NEG (L2; hypotheses (CS), (θ) with θ̄ ≠ 0, liminf p/K > 16/15, (PB)): the start mode is size-saturated
(|S̃₀| = K) and the first ⌊n^β⌋ moves of the LS0 path are size-preserving swaps (any fixed β < ½), so LS0 with any
nonnegative integer cap a ≤ |S̃₀| − s₀ − 2 + ⌊n^β⌋ never scores S₀ (w.p. → 1). The LS0 route to reported-model
consistency is therefore unavailable for MR1 on this class, and no O(log n) or polylog allowance can repair it.
This is a statement about the LS0 route, not about the full fit (the full-method question is open; STATEMENT (P6)).

## Proved sufficient change (MR-PK)
Theorem PATH (L3; hypotheses (CS), (θ), K + 16s₀ + 1 ≤ p ≤ n − 1, blocks ≤ 16): for every fixed δ > 0 the uncapped LS0
path ends at S₀ (a strict local maximum) after at most (1 + δ)|S̃₀| moves, w.p. → 1. Hence **any LS0 cap rule
a ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉) for a fixed δ > 0** makes LS0 end certified at S₀ (Theorem FAC-PK, (P4)). Candidate rules:

| rule | δ | proved on this class | worst-case LS0 scans | note |
|---|---|---|---|---|
| ℓ_n + 2|S̃₀| | 1 | yes (any p in range) | ℓ_n + 2K + 1 | largest of the linear-in-mode allowances; dominates the other rows when |S̃₀| = K (observed m*/K ≤ 1.26 in N3) [R07-3] |
| ℓ_n + ⌈(1 + δ)|S̃₀|⌉, e.g. δ = ¼ (0 < δ ≤ 1) | δ | yes (asymptotic) | ℓ_n + ⌈(1 + δ)K⌉ + 1 | cheaper; N3 has finite-n runs with m*/K up to 1.26 (n = 2000, p = n − 1) |
| max(ℓ_n + |S̃₀|, p) | ≥ 1/16 under (PK) | yes when p ≥ (1 + 1/16)K | max(ℓ_n + K, p) + 1 | equals MR1 when p ≤ ℓ_n + |S̃₀|; tied to p, unbounded relative to K for p ≫ n designs |

**"Minimal".** Proved: allowances over |S̃₀| of order ≤ n^β (β < ½) fail; allowances ≥ δ|S̃₀| (any fixed δ > 0) suffice.
No optimality is claimed in between. Heuristically the needed allowance is the swap count W ≈ p·n^{−1/(4M_W)} = o(K)
(N1/N3), but no bound on W is proved. **Recommendation:** ℓ_n + 2|S̃₀| for robustness at moderate n; HQ may prefer a
smaller δ for cost.

**Transfer (R05-4).** Lemma CAP (FINAL s7) is monotone in the cap for caps ≥ ℓ_n. All three rules in the table satisfy
a ≥ ℓ_n + |S̃₀| (= MR1), so LS0's scored set contains MR1's. What transfers under the original hypotheses: positive
discovery statements (LS0 scores S₀), certified-endpoint statements on the events where the smaller-cap search ends
certified, and the joint-with-output HPM statements derived from them (FINAL s7 "What survives"). What does not transfer
verbatim: worst-case resource statements (re-charged below), negative discovery statements (they transfer only
downward), flags/metadata, and cap-dependent no-output events. A rule below MR1 must still satisfy a ≥ ℓ_n (e.g.
max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉)) to inherit even the legacy-cap results.

## Implementation (option plumbing; not done by this ticket) [R07-1]
The cap rule is evaluated after the start mode by O(1) arithmetic (needed for the delivery argument, L4 (β)). Today the
R→C++ interface collapses every non-legacy value to MR1, so a new rule needs plumbing, not a two-line edit:
* `Scripts/SMC_BVS/core/v3_run.R:101` — keep and validate distinct values (e.g. `"ell_n"`, `"ell_n_plus_mode"`,
  `"ell_n_plus_2mode"`, or a δ-parameterised rule with a fixed validated δ and the ceiling ⌈(1 + δ)|S̃₀|⌉) instead of mapping
  everything except `"ell_n"` to `"ell_n_plus_mode"`.
* `Scripts/SMC_BVS/core/cpp/v3_core.cpp:394,404` — carry an enum/string instead of the Boolean `ls0_cap_plus_mode`;
  `v3_core.cpp:473` — compute the selected cap after `start_mode` (range check kept); `v3_core.cpp:479` — matching label.
* `Scripts/SMC_BVS/core/v3_fit.R:44` (and the call sites `v3_fit.R:114–115, 145`) — pass the selected rule's worst-case
  scan count (e.g. `b$ell + 2*K + 1`) into the initial and escalation preflights; keep the existing bounds for the old
  options; archive formula unchanged in form; label at `v3_fit.R:62`.
Keep the range check (`v3_core.cpp:474`) unreachable on admissible inputs: compute the cap in 64-bit; ℓ_n + 2K ≤ INT_MAX
holds under MACH / the allocation premise (R11 optional 2). When plumbing, compute the preflight's worst-case scan count from the same base cap LS0 uses (today the preflight uses
`b$ell`, LS0 uses `ro$ls0_ell`) [R09-opt1]. Alternatively, if HQ adopts MR-PK as a global replacement of MR1, state that explicitly and drop the extra option.

## Cost (upper bounds on LS0's worst-case terms only; not a statement about total fit time)
For a rule with worst case a_max ≤ ℓ_n + 2K: LS0 score requests ≤ 1 + (a_max + 1)q(p), q(p) = p + p²/4; preflight
time charge 2(a_max + 1)q(p)ŝ_K (vs 2(ℓ_n + K + 1)q(p)ŝ_K); archive (2s + 4)(12K + 256) + 96s + 4(8W + 4K + 96) + 4096 bytes
with s = a_max + 1. Delivery envelopes (Proposition F, A1/A2 form): LS0 terms with K replaced by 2K:
W_G′ := W̄ + C·2K·q(p)[n³ + p(n + 2)], M_G′ := M̄ + C·2K(2K + 1), P̄_LS0′ := (ℓ_n + 2K + 1)q(p)(τU_K + τ₀)/100. Each LS0
worst-case charge is at most (a_max + 1)/(ℓ_n + K + 1) ≤ 2 times its MR1 charge (equality only for scan-proportional
terms); conservative envelope increments and total fit time are not claimed to scale by this factor. For rules with a ≥ ℓ_n + |S̃₀| (all three in the table)
realised LS0 work is identical wherever the MR1 search already ends certified (Lemma CAP(a)); not for smaller rules.

**Operational finding (for HQ; numerics/full_method/NF_summary.md).** Already under MR1, the merged preflight's LS0
worst-case time charge is ≈ 5.3·10⁵ s (≈ 146 h) for n = 600, p = 450 (K = 300, 312 scans, 1.59·10⁷ requests,
ŝ_K = 0.0166 s on the local machine). Observed: the 2-hour attempts returned `resource_limit` at preflight; the 1000-hour
attempt timed out after 1200 s of wall clock. Extrapolation (not an observed run): the same recorded charge would also
reject a 24-hour allocation, e.g. the default 8 GB / 24 h [R07-5]. Delivery theorems assume the amended allocation; MR-PK increases this charge by at most a factor two. The
worst-case charge grows like K·p²·ŝ_K, where ŝ_K is measured separately at size K (its dependence on K was not measured
here) [R07-6]. Whether realised LS0 time is close to this charge
was not measured here (no fit completed locally; W2-SIM R2 records timings$ls0). Any tighter valid preflight bound
would be a separate engineering item (finding only).

## Not changed
Prior, SMC kernels, calibration, tables, start-mode rule, final local search (cap ℓ_n).
