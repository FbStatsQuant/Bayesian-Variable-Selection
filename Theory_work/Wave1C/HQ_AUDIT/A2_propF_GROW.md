EXTENDS

# A2 — Proposition F on the GROW class

The class restriction is removable under **A1's exact corrected premises**, including its enlarged resource envelopes. No additional statistical or calibration-success assumption is needed. This extends the specified ideal-machine method, relative to the same code-reading audits; it does not audit the fallback implementation. Below, `GROW/`, `DLV/`, and `A1` denote `Theory_work/Wave1C/C-GROW/`, `Theory_work/Wave1C/C-DLV/`, and `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md`; all citations are repository path:line references.

## Exact extended statement

Use the method and premises of `A1:62–75`: v3.1 with deterministic, complete-scan LS0 from the exact e4 start-mode maximiser, emitted centre and all-scored HPM retention; EX-A (unit-cost exact reals), IDEAL-W, EX-S, SR, e4, GUARD-W, TDP-IMPL, MACH, valid declared seed/allocation, fixed declared R′ = 4k and worker count, and CONFIG with OP-LS0 amended to the cap

    ℓ_n = ceil(log₂(n+p+1)),  K = min(p,floor(n/2)),
    a_n = ℓ_n + |S̃₀|.

Other local-search caps remain ℓ_n. At the first failed tier-1 construction, terminate that tier, select its last successful complete grid or, if none exists, its completed pilot grid; preserve tier-1 budgets and inherited scored state, freeze through the normal record/hash construction before final randomness, retain fallback metadata, and make no further calibration attempts. Never use a partial failed grid (`A1:62–64`).

With q(p) = p+p²/4, use

    W_G = W̄ + C K q(p)[n³+p(n+2)],   M_G = M̄ + C K(K+1),
    mem_n  ≥ max{β M_G(n,p_raw)+β₀, P₀, P₁},
    time_n ≥ max{2[τ W_G(n,p_raw)+τ₀], P̄_t},
    allocation$mem_gb ≥ mem_n/2³⁰,  allocation$hours ≥ time_n/3600,

with sufficiently large implementation/concurrency constants, the Lemma R envelopes W̄, M̄, its preflight bounds, and its included polynomial certificate budgets (`A1:9–19,66–75`; `DLV/lemmas/L1_resources.md:70–81,118–137`).

**Add to Proposition F's classes:** (i) fixed designs under GROW's G, (H0), (G1)–(G4), with MR1, including exact-Gram AR(1) under all the hypotheses of (C5)(a); (ii) iid-row AR(1) under all the hypotheses of (C5)(c), including independent Gaussian noise and the separation condition. Precisely these hypotheses are `GROW/STATEMENT.md:51–98,119–126,139–149` (the iid instance uses its joint-law event theorem, not fixed-design NEG or G4-dir).

Then, for every admissible n ≥ 3,

    P(no output) = 0,

and along each such sequence,

    P(Ŝ⁺ = S₀) → 1.

Probabilities use the original unconditioned noise law for fixed designs and the original joint design/noise law for iid rows (and the algorithm's randomness). The first assertion needs only the input/model regularity below; asymptotic statistical hypotheses enter the second. CAL, candidate restricted-ESS success and a bound on fallback probability are unnecessary.

## Proof

**1. Lemma S extends.** For fixed GROW designs, raw columns are finite and nonconstant by G, and standardisation gives centred columns with squared norm n−1 (`GROW/STATEMENT.md:57–59`). This includes the admissible exact-Gram instance (`GROW/STATEMENT.md:119–123`). For iid AR(1), raw entries are finite a.s.; each column has iid N(0,1) entries, so its sample variance is positive a.s. For each finite n,p, the finite union of constant-column events is null. Thus no columns are dropped and p_raw = p a.s. This supplies exactly the inputs needed by S.1, not a bounded relevance set (`DLV/lemmas/L2_degenerate.md:6–14`; iid model: `GROW/lemmas/L6_random_AR1.md:12–16`).

Given a fixed design, a constant raw response requires the Gaussian noise vector to lie on an affine line, hence has probability zero. In the iid instance, conditional on X the centred response is Xθ*+Cε, with ε independent Gaussian; its law on 1-perp has covariance σ²C and hence no atom at zero for n≥3. Integrating gives the same null event, even though the signal coefficients are specified on the standardised scale (`GROW/STATEMENT.md:139–142`). Thus y′y=n−1 a.s. after preprocessing. Valid seed/allocation, n≥3 and IDEAL-W exclude the other input/degenerate paths exactly as in `DLV/lemmas/L2_degenerate.md:8–18`.

For every feasible scored S, G_S=X_S′X_S is positive semidefinite, H=(n+1)G_S+I and A=G_S+I are positive definite, and

    Q_S ≥ y′y/(n+1) = (n−1)/(n+1) > 0.

Consequently route-1 Cholesky and the log score are finite under EX-A, including the exact identity for Q recomputation; the empty-model case and size invariant are unchanged (`DLV/lemmas/L2_degenerate.md:20–35`). This uses neither full-design rank nor a relevance-size bound, so p≫n in the iid instance causes no numerical obstruction.

The remaining S.3 invariants use block size, feasible indices, provenance, setup/context construction and declared seeds, all unchanged here; tier-0 failure still forces escalation (`DLV/lemmas/L2_degenerate.md:38–62,66–67`). In S.3(vii), replace “successful construction” by “successful construction or complete fallback pilot”: both grids pass the same checks (`DLV/lemmas/L2_degenerate.md:63–65`; `A1:39–43`). Thus S.4 holds on both instances, with S.3 retaining its original AUDITED status (`DLV/lemmas/L2_degenerate.md:69–70`).

**2. Delivery extends with the amended allocation.** MR1 permits at most ℓ_n+K+1 scans on every data set (`GROW/METHOD_REQUIREMENTS.md:3–18`), adding at most Kq(p) requests to Lemma R. Their worst-case score/cache/store cost is O(n³+p(n+2)); the additional LS0 archive fits the stated M_G increment (`DLV/lemmas/L1_resources.md:32–43`; `A1:7–19`). Lemma R's counting is uniform in valid inputs, seeds and uniforms, rather than a statistical class property (`DLV/lemmas/L1_resources.md:70–83,110–116`). Corollary R's guard, preflight and allocation proof therefore applies with W_G,M_G (`DLV/lemmas/L1_resources.md:129–137`).

With Step 1, the exit walk of Theorem D excludes every non-grid stop (`DLV/lemmas/L4_delivery.md:24–40`). A completed pilot has strictly increasing endpoints 0 and 1 and at most T₁ intervals; a successful construction has the same properties. The total fallback preserves these bounds and eliminates schedule_limit without retries (`DLV/lemmas/L4_delivery.md:80–91`; `A1:39–43,64`). Hence the same walk returns estimates outside a null set: P(no output)=0. Growing relevance changes none of these exclusions.

**3. Replace D′'s statistical inputs by GROW's data events.** Define 𝒦_n to mean that deterministic LS0 with cap a_n scores S₀, whether or not a run delivers. Put E_n = Sand_n ∩ NA(𝓛) ∩ TL(𝓛). On E_n, the exact start mode lies between S₀ and Q; greedy LS0 deletes one extra per move and scores S₀ within cap a_n≥|S̃₀\S₀|. Therefore

    P(𝒦_nᶜ) ≤ P(Sand_nᶜ)+P(NA(𝓛)ᶜ)+P(TL(𝓛)ᶜ) → 0.

These are precisely the deterministic/data steps of `GROW/STATEMENT.md:102–113` and `GROW/lemmas/L4_assembly.md:25–29`. We do **not** infer this bound merely from D_n→0: operational closure bounds D_n by LS0 failure, in the opposite direction (`GROW/lemmas/L4_assembly.md:11–14,25`). The exact-Gram instance verifies the hypotheses (`GROW/lemmas/L5_instances.md:48–68`). For iid AR(1), the three events are proved directly jointly and the same descent applies; NEG and exact G4-dir are not asserted (`GROW/lemmas/L6_random_AR1.md:35–49,470–476`). None of these data events depends on calibration, so their use requires no CAL premise.

The posterior input is **T03♯ under (H0)**, giving 1−π(S₀)→0 in probability and, by boundedness, E[1−π(S₀)]→0 (`GROW/STATEMENT.md:84–88`; `GROW/lemmas/L4_assembly.md:10,29`). For iid AR(1), L6.2 supplies design events of probability 1−o(1) on which deterministic sequences satisfy (H0) with common constants; L6's diagonal argument then gives the same posterior expectation limit under the joint law (`GROW/lemmas/L6_random_AR1.md:78–83,478–489`). This does not require (H0) on every random realisation or GEN's bounded-relevance hypotheses.

Finally reuse D′'s pointwise scored-set argument: on output and 𝒦_n, S₀ was scored (or exact enumeration scored every feasible model); if π(S₀)>1/2 its score strictly exceeds every competitor. Thus, eventually s₀≤K,

    P(output and Ŝ⁺≠S₀) ≤ 2E[1−π(S₀)] + P(𝒦_nᶜ) → 0

(`DLV/lemmas/L4_delivery.md:65–77`). Together with Step 2 this gives P(Ŝ⁺=S₀)→1. It also extends D′'s delivery-term assembly to GROW (and, for the original calibration with this cap/allocation, Theorem D still identifies the delivery term with schedule_limit). The existing final-chapter exclusion is therefore a scope gap, not an obstruction (`Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:43`). All reused results retain their recorded dependency/audit qualifications.
