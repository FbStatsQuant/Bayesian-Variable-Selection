# W1-PXN — STATEMENT (v2, LOCKED 2026-11-08 after review R00 "LOCK WITH CHANGES", all changes applied)

Ticket: frontier card FR01 (`Theory_work/State_of_Project/sections/06_open_and_plan.tex:73-83`).
Candidate under review: API-PXNGAP = registry TH161, status (verbatim) "PROVED (candidate, API-PXNGAP) given T22(i),(ii),
T03, CONC, W7 Thm B; no SF/XF review in the archive" (`NBH/ID_REGISTRY.md:309`). NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`;
PROOF = `NBH/branch_snapshots/API-PXNGAP/PROOF.md`; W6 = `NBH/branch_snapshots/W6-FIXREV1/T38_STATEMENT.md`.
The theorem is PROOF §10 (PROOF.md:421-446) with §0, except: dependency points D1 (input of (P)) and D2 (constant of (R))
in §4, whose resolution is part of this ticket; any change they force is propagated here and flagged in REPORT.md.
**Precedence (R30 #6):** §5 records the resolutions (D1, D2 resolved) and supersedes every "pending" label below.

## 1. Setting

**Family LH-iid (PROOF.md:36-60).** Fixed integers g ≥ 2, c ≥ 1, v ≥ 0; ρ ∈ (0,1); 0 < |ψ_i| < ρ (i ≤ c), ψ̄ := max|ψ_i|;
nonzero fixed β_1..β_c, β^vis_1..β^vis_v; σ² > 0; **a fixed A ≥ 1 (A > 1, i.e. p ≫ n, allowed; no lower bound p ≥ n^a)**.
p = p_n = G_n g, 18 ≤ p_n ≤ n^A, p_n → ∞. [p] = G_n groups of size g; first member = hub j_h. Groups 1..2c form c linked
pairs (a_i, b_i) = (2i−1, 2i); groups 2c+1..2c+v visible; the rest null. Rows of X^r iid N(0, Σ): within-group
equicorrelation ρ (unit diagonal); groups independent except Σ[C_{a_i}, C_{b_i}] = ψ_i Σ[C_{a_i}, j_{a_i}] Σ[j_{b_i}, C_{b_i}].
Truth θ_{j_{a_i}} = β_i, θ_{j_{b_i}} = −ψ_iβ_i, θ_{j_h} = β^vis_h (visible), else 0; y^r = X^rθ + ε, ε ~ N(0, σ²I_n) ⊥ X^r.
S₀ = supp θ, s₀ = 2c + v; masked set M = {j_{b_i}}; reference S° := S₀ ∖ M, s = c + v; Φ(S) := |S Δ S₀|.
**(SIZE)** g ≤ B_n < 2g for n ≥ n₁, B_n = min(⌊√n⌋, ⌊√p⌋, 16) (the method's block size; so 9 ≤ g ≤ 16 asymptotically).

**Target (posterior) — exactly the v3 score (T03 STATEMENT §1,
`NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md:7-13`).** C = I − 11ᵀ/n;
X = CX^rD_x⁻¹ (column norms² = n−1), y = Cy^r/s_y. K = min(p, ⌊n/2⌋), Ω = {S : |S| ≤ K}. G_S = X_SᵀX_S, z_S = X_Sᵀy,
H_S = (n+1)G_S + I, D_S = det H_S/det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, a₀ = b₀ = 0.01, ν = a₀ + n/2;
m(S) = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) · D_S^{−1/2}(2b₀ + Q_S)^{−ν}; w(k) = ½/C(2p−1, k); W_K = Σ_{k≤K} C(p,k)w(k);
F(S) = log[w(|S|)m(S)/W_K]; π(S) ∝ e^{F(S)} on Ω. (Ridge-type g-prior with g = n, BB(1,p) size prior, IG(a₀, b₀).)

**Method.** SMC-BVS v3 as frozen (partition by complete linkage on 1 − |r̂| + top-down cut + next-fit packing with
capacity B_n; exact block start π₀ from block tables r_b(U) = m(U)/m(∅); tempering; islands; HPM = best scored model),
**plus LS0** (W6:41-44): one production local search (M §6.10: scan all flips and swaps of the centre; move to the best
scanned model if it strictly beats the centre, lexicographic ties; at most ℓ_n = ⌈log₂(n+p+1)⌉ moves, then one final scan),
centred at the exact start mode S̃₀ = argmax π₀ (max-plus convolution of block tables, deterministic tie rule); the
centre is the first evaluation and is offered to the HPM; every scan is completed; LS0 is a deterministic function of
the data. LS0 is a method change relative to the production core (registry DF16: "not merged in production core"). Concretely (C1 Opus #7):
LS0 = `local_search(S̃₀, ell_n, tier, emit_centre = true)` on the start mode returned by `start_mode`, executed after R̄ on every
fit counted in 𝒪; the current core calls only `local_search(led.hpmS, ell, tier, false)` (Scripts/SMC_BVS/core/cpp/v3_core.cpp:447).

**Runs, scored sets, output (W6:30-40).** R̄ = the potential uninterrupted run (EX-A, guards removed), status
st̄ ∈ {exact, completed, schedule_limit}; R̄⁺ = R̄ followed by LS0. The actual run's status st and outputs are functions
of (R̄, Ξ) (Ξ = allocation, clock, load). Strict output event 𝒪 := {st ∈ {exact, completed}}, U := 𝒪ᶜ; 𝒪̄ := {st̄ ∈
{exact, completed}}. 𝒮 = every model scored by the run, 𝒮_LS0 = models scored by LS0, 𝒮⁺ := 𝒮 ∪ 𝒮_LS0, **Ŝ⁺ := the
reported HPM = the best model in 𝒮⁺** under (F, −|S|, lex); barred symbols are the R̄⁺ versions.

**Operational premises (OP) (W6:56-69)** — assumptions, not discharged implementation claims: EX-A, EX-S, CAL
(declared idealisations); SR; GUARD ((G1) the guard reads only the clock, consumes no random number, changes no
setting; (G2) a run no guard check stops performs exactly the R̄ (R̄⁺) computation); OP-LS0 (LS0 executed, centre
emitted, scans completed, on every fit counted in 𝒪; post hoc allowed; a stopped LS0 counts in U). v3 budgets indexed by n.

## 2. Target theorem

Under LH-iid + (SIZE) + (OP), as n → ∞ (conclusions (S), (E), (T), (P) concern the data (X, ε) and the deterministic
LS0 of R̄⁺; only (C) involves the actual run):
- **(R)** P(𝒜_nᶜ) → 0 with Σ_n P(𝒜_nᶜ) < ∞ and P(𝒜_nᶜ) ≤ p^{−C} for n ≥ max{n₁, n₀(A, C, ρ, ψ̄)} (n₁ = the SIZE onset of the sequence), where 𝒜_n := {blocks = groups}.
  Explicit form claimed by the candidate (PROOF.md:79-85; D2 resolved: VERIFIED by R14 with the display split of lemmas/R_branch_repair.md §1): for n ≥ 5 with SIZE at n,
  P(𝒜_nᶜ) ≤ (2/(√π(1−ρ))) p²√n e^{−(n−4)I*}, with I(t; r) := −½ log[(1−r²)(1−t²)/(1−rt)²],
  q := √((1−ψ̄²)/(1−ρ²)), t* := (q−1)/(qρ−ψ̄) ∈ (ψ̄, ρ), I* := I(t*; ψ̄) = I(t*; ρ) > 0.
- **(S)** 1 − π₀(S°) = O_P(√(log n/n)), with the explicit truncated-moment and tail bounds of P3′ (PROOF.md:240-244:
  E[q̃ 1_{𝒢_n}] ≤ C_q√(log n/n), P(q > x) ≤ C_q√(log n/n)/x + P(𝒢_nᶜ)); π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} → 0, more precisely
  log π₀(S₀) + c log p + (c/2) log n →_d Σ_{i≤c} log((s+i)/2) + ½χ²_c (P4, PROOF.md:277): masked regime.
- **(E)** P(S̃₀ = S°) → 1; S° ⊆ S₀ has no extras and Φ(S°) = c (it is a lattice reference in the sense of W6's Lat(S°)).
- **(T)** P(LS0 of R̄⁺ scores S₀) → 1 and P(LS0 of R̄⁺ returns S₀ with local_certified) → 1.
- **(P)** δ₁ := 1 − π(S₀) = O_P(√(log n/n)) under the joint law of (X^r, ε); hence E₀δ₁ → 0 (E₀ = joint expectation).
- **(C)** For every n: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) ≤ P(LS0 of R̄⁺ does not score S₀),
  and D_n → 0. Hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0, liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) =
  1 − limsup_n P(U), and P(𝒪 ∩ {Ŝ⁺ = S₀}) → 1 − u whenever P(U) → u.
- **(K)** LS0 costs ≤ 1 + (ℓ_n+1) max_{k≤K}[p + k(p−k)] = O(p² log(n+p)) scores; on the joint event 𝒯_n of lemmas/LS_P6_repair.md (lattice arrival + (L) + ℓ_n ≥ c), c + 1 scans
  and ≤ 1 + (c+1)(p + s₀p) scores. [v2.1: wording corrected after R15; no change of content beyond the source's error.]

**Headline (what "done" certifies).** On the masked correlated design LH-iid with p ≤ n^A (A > 1 allowed), for v3 + LS0:
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, i.e. P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U_n)) → 0, so liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
**Not claimed:** P(U) → 0 (delivery); the method without LS0; masked PIP/evidence accuracy; the study's own design (groups
of 5 violate SIZE); superpolynomial p; no quantitative finite-n consistency guarantee, in particular none at n = 200 (the
proven margins are vacuous there, PROOF §11 (O5)); (C) itself holds at every n and (K) is deterministic; no uniformity in A.

## 3. Dependence on A (to be confirmed per item)

All rates are √(log n/n) for each fixed A; A enters constants and onsets only:
- Lemma Tr-J families: D = A (P3′, family G_n2^g ≤ 2^{16}n^A) and D = A(s₀+2) (Lemma Λ(a), |𝔉_n| ≤ 2^{s₀+2}n^{A(s₀+2)});
  thresholds t_n = 8(D+1) log n, τ_n = t_n/n; failure ≤ C n^{−1}e^{O(√log n)}.
- Lemma E families: same D's; P(𝒟_nᶜ ∩ ℰ) ≤ 2e^{−n^{1/3}} + Cn^D[n^{−4(D+1)}e^{√(8J(D+1)log n)} + 2n^{−2(D+1)}]; constant C₂(σ², M, D) in (E5).
- Lemma U / (D_S): m_n = (n/2) log(1 + c₂/(4(σ²+M))) − (2A+1) log n − 2κ_E − 2 > 0 needs n ≳ (4A+2)(4(σ²+M)/c₂) log n.
- Lemma Λ(a): needs Mτ_n = 8M(A(s₀+2)+1) log n/n ≤ c₂/8.
- (L): F(S₀+l) − F(S₀) ≤ −½ log n + log log n + O(1), with Z_l² ≤ 2 log p + 2 log log n ≤ 2A log n + 2 log log n and
  RSS_{S₀}/(nσ²) = 1 + O(n^{−1/3}) by (E5); the remainder O(n^{−1/3} log n + (log n)²/n) is o(1) for fixed A.
- Theorem R: onset ((2+C)A + ½) log n + log(2/(√π(1−ρ))) ≤ (n−4)I* (D2 resolved, R14).
- (P) via T03♯: j₀ = ⌈(2A+1)s₀⌉+1; cutoff m♯_n ≤ k_n := max{s₀, ⌈1 + s₀ + (As₀ + (s₀+2)/2) log₂ n⌉} (proved in lemmas/P8_T03sharp.md step 1); SE event over sets of size
  s₀ + max{m_n, m♯_n, j₀, g, s₀+2} = O(log n) needs (log n)·√(A log n/n) → 0 ([CONC], log p = o(n)).

## 4. Dependency points (resolution is part of the ticket)

- **D1 (input of (P)).** PROOF §9 cites "locked T03(i): under G, R, SE, BM-∞" (PROOF.md:24); the locked statement also
  requires H-T02 (= T02(i), "unproved v3 conjecture, used as hypothesis") and is "SAME-FAMILY-ONLY". Repair: route (P)
  through T03♯ (theorem of record TH128, `NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-35,51-60`; final card TH09:
  "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)") — a fixed-design theorem; the random-design extension
  (design event + de-randomisation) is this ticket's own step, file `lemmas/P8_T03sharp.md`.
- **D2 (constant of (R)).** W7-PART "Theorem B XF VERIFIED* (A-REV6 restricted scope; A-REV9 B-exact VERIFIED);
  Corollary B XF GAP (A-REV9, L2 constants)" (`NBH/ID_REGISTRY.md:311`). The explicit form of (R) is Corollary B. If W7
  Lemma 2 does not pass review, (R) is kept only in its first-line form (summable, ≤ p^{−C} eventually) proved by a
  self-contained tail bound; (C) and (P) use only that form.

## 5. Changes after item reviews (v2.2, 2026-11-08; none changes a conclusion of §2)
- **Exact-branch convention (R14 #3; lemmas/R_branch_repair.md §3).** "blocks", π₀, S̃₀ and "LS0 of R̄⁺" denote the
  deterministic make_blocks / block-table / start-mode / local-search functions of the data on every branch (hypothetical
  when the run dispatches to exact enumeration, which can happen for very slowly growing p); on the exact branch the run
  scores all of Ω, so that branch contributes nothing to D_n. No lower growth bound on p is introduced.
- **(R)** is stated as (R-a) S(t) for every t ∈ (ψ̄, ρ), (R-b) S(t*) ≤ K_n (the explicit constant, VERIFIED by R14), (R-c)
  p^{−C} onset and summable form; D2 resolved. Independent cruder route (R′) in lemmas/CR_corr_tails.md.
- **(P)** rests on T03♯ (theorem of record TH128) via lemmas/P8_T03sharp.md, not on locked T03; D1 resolved.
- **(T)/(K)**: arrival after exactly c moves and certification need ℓ_n ≥ c (eventual); c + 1 scans and the O(p) cost hold
  on the joint event 𝒯_n (lemmas/LS_P6_repair.md).
- **(S)**: the "sharp in order" remark of the source is not claimed.
