# L5 — Theorem PLR (assembly for polylogarithmic relevance sets)

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses. Model: GROW
`lemmas/L4_assembly.md` (R04 VERIFIED-WITH-AMENDMENTS) and its random-design form APP `lemmas/L3_LOC.md` §L3.8 / GROW L6 §7.
Check record: R04 (Codex gpt-6.1-sol high, `reviews/R04_L4L5L7_check_sol.md`): see `reviews/R04_disposition.md` (L4, L5 VERIFIED-WITH-AMENDMENTS, applied; L7 VERIFIED).

**Inputs (statuses verbatim).** [OP] GEN L5 operational closure "PROVED (by this seat, unchecked)" inside Theorem GEN
"PROVED-CHECKED" (cap-independent, GROW L4); GROW L1 (descent) "PROVED (by this seat, unchecked)", R03 VERIFIED;
GROW L2.1/L2.2 R03 VERIFIED-WITH-AMENDMENTS, here on the L0′ event (L1_toolkit); M5(0)/T38-(0) "PROVED (SF: VERIFIED
(W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; APP L1_POST (Lemma
POST) "PROVED (by this seat, unchecked)", R02 VERIFIED-WITH-AMENDMENTS. This folder: L1 (L0′, regularity), L2 (NA-R).

**Theorem PLR** [R01-1: split]. Setting of STATEMENT §1 (fixed θ_lo > 0). Let Q ⊇ S₀ be deterministic with
|Q| ≤ (log n)^κ and the feasibility dichotomy (Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1), with the floor (N1)
λ_min(Σ_{n,Q∪{l}}) ≥ c for all l, and suppose (i) P(Sand_n) → 1, (ii) for some latent extension as in Lemma NA-R, (R1)–(R3) hold for Q [C1-Opus-6]. Then, under the
joint law of (X, ε) and the implementation premises (incl. "the emitted LS0 centre is some maximiser of γ₀"):
 (C-i)  P(NA(𝓛)) → 1, P(TL(𝓛)) → 1 and D_n ≤ P(Sand_nᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0, with the shipped cap ℓ_n + |S̃₀|;
 (C-ii) if in addition APP L1_POST's LSF holds (sufficient: λ_min(Σ_n) ≥ c), then 1 − π(S₀) = O_P(√(log n/n)),
        P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1).
(C-i) uses only the local floor (N1) and the sandwich hypothesis; LSF enters (C-ii) only through L1_POST.

*Proof.* (a) *Events.* TL(𝓛): L1_toolkit L1.1 (GROW L2.1 on 𝓔_n) conditionally on X ∈ A_X (Gram floor (G2) with φ₀² = c/2
for Q ∪ {l}, from (N1) and L1.2), integrated: P(TL(𝓛)ᶜ) → 0. NA(𝓛): Lemma NA-R (N0) holds by |Q| ≤ (log n)^κ and
|Q| ≤ K_n (q ≤ p and q ≤ (log n)^κ = o(n), so q ≤ ⌊n/2⌋ eventually and q ≤ min(p, ⌊n/2⌋) = K_n [R04-2]), (N1) is assumed; so P(max_𝔓 Z²_{T,l} ≤ c_n) → 1, and GROW L2.2 on 𝓔_n ∩ {that event}
(L1.1) gives P(NA(𝓛)ᶜ) → 0. Sand_n: hypothesis (i).
(b) *Path.* By [OP], D_n ≤ P(LS0 from the emitted centre does not score S₀). On Sand_n the emitted centre S̃₀ (some
maximiser of γ₀) lies in 𝓛 ⊆ Ω (|Q| ≤ K_n). On Sand_n ∩ NA(𝓛) ∩ TL(𝓛), GROW L1.2(ii) with C := S̃₀: LS0 deletes one
element of S̃₀ ∖ S₀ per move and scores S₀ once its cap is ≥ |S̃₀ ∖ S₀| − 1; the shipped cap ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|
(and with cap ≥ |S̃₀ ∖ S₀| the endpoint is S₀, certified). Hence the display for D_n.
(c) *Posterior (C-ii).* By LSF (e.g. from λ_min(Σ_n) ≥ c: λ_min(Σ_{n,S}) ≥ c for all S), L1_POST (b): on X-events
𝒜_n with P(𝒜_n) → 1 every design satisfies (H0) with common constants; the diagonal tightness transfer gives
1 − π(S₀) = O_P(√(log n/n)) under the joint law; in particular E[1 − π(S₀)] → 0 (bounded). M5(0), integrated over the
design: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + D_n → 0; the last identity subtracts this from P(𝒪) = 1 − P(U_n). ∎

**Corollaries.** Theorem LOC-d (L4 Part A: (i) by A.1–A.4, (ii) by A.5, Q of size ≤ (log n)^{d+1} with the dichotomy by
L1.2; the global floor λ_min(Σ_n) ≥ c gives (N1) and LSF) and Theorem LOC-BF (L4 Part B: (i) by B.1, (ii) by B.2,
|Q| ≤ (log n)^{κ+1}; global floor c_B) — PROVED (by this seat,
unchecked).

**Notes.** (1) Cost of the cap: on the three events LS0 makes |S̃₀ ∖ S₀| ≤ |Q| = O((log n)^{κ}) moves; worst case as GROW
L4 Note (4). (2) The exact-enumeration branch only helps (APP L6_ENUM). (3) Nothing is conditioned on 𝒪.
