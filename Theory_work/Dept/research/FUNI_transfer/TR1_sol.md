# TR1 — delivery-proof transfer review

## 1. Transfer to the shipped LS0 cap

**TRANSFER: NO** for the stated unrestricted conclusion under IDEAL-W. The resource-counting argument transfers after the changes already incorporated into F-FAC/F-UNI; the claim that all remaining no-output exits are null does not. Two explicit shipped cap validators remain outside that argument.

Paths below are relative to `/home/fb31/BVS-wt/THEORY-DEPT`. Abbreviations: DLV = `Theory_work/Wave1C/C-DLV`; FAC = `Theory_work/Wave2/W2-FAC-A`; UNI = `Theory_work/Wave2/W2-UNI`; CORE = `Scripts/SMC_BVS/core`; FIN = `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex`. These abbreviations in file:line citations expand literally to those paths.

**Methods and premises.** DLV Prop-F concerns the specified v3.1 + deterministic complete-scan LS0 from the exact e4 start maximiser, with LS0 move cap ℓ = ⌈log₂(n+p+1)⌉; its patch freezes a complete tier-1 pilot or successful construction upon grid failure (DLV/STATEMENT.md:10-12,32-42; DLV/lemmas/L4_delivery.md:7-9,53-54,79-91). At that audit, LS0 was a specified component, not yet on the audited shipped call graph (Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md:33). FAC already uses a = ℓ + |S̃₀| ≤ ℓ + K, and UNI explicitly imports that same method and allocation (FAC/lemmas/L7_delivery.md:7-16; UNI/lemmas/L5_delivery.md:8-13). Thus transferring FAC Steps 1–2 requires no further change to its LS0 cap.

In all cases K = min(p,⌊n/2⌋), B ≤ 16, the other local searches retain cap ℓ, each tier has at most ℓ rebuild iterations, and there are at most two tiers. L = max(4,⌈log₂(n+1)⌉), N₀ = max(2500,n,p), H₀ = ⌈512N₀/2500⌉, T₀ = max(1000,ℓ²); tier e has (N_e,H_e,T_e) = 4^e(N₀,H₀,T₀). Pilot/frozen grids have at most T_e intervals, each bisection has 60 halvings, and start-mode enumeration has a 10⁶-maximiser cap followed by the required tie-aware DP, rather than a delivery failure (DLV/lemmas/L1_resources.md:7-29; CORE/cpp/v3_core.cpp:469-472). R′ = 4k and worker count are fixed. EX-A supplies exact unit-cost real arithmetic; MACH supplies the time/space conversion, allocation success and environment assumptions. EX-S, SR, e4, OP-LS0, GUARD-W, CONFIG and TDP-IMPL remain premises; CAL is not assumed.

IDEAL-W is specifically the unbounded-word/address assumption that integer, index, stream-id and allocation arithmetic never overflow, with intentional RNG modular arithmetic retained and `unsupported_size` excluded (DLV/STATEMENT.md:24-25). It does not explicitly remove application-level rejection predicates. The shipped method additionally checks **base cap** `le ≤ 1e6` even at the default `le = ℓ`, and **total cap** `ℓ + |S̃₀| ≤ numeric_limits<int>::max()` (CORE/v3_run.R:95-101; CORE/cpp/v3_core.cpp:473-476). The former is not the start-mode enumeration cap. Under the unchanged code-ceiling reading, write I = 2³¹−1 for the latter ceiling; removing it requires an explicit idealisation beyond bare IDEAL-W.

| Proof step and source (file:line) | Result with LS0 cap a = ℓ + |S̃₀| |
|---|---|
| Prop-F pilot endpoints, strict increase and ≤ T₁ intervals; DLV/lemmas/L4_delivery.md:85-86 | **Holds verbatim.** LS0 does not change calibration. |
| Grid validation, freezing before final randomness; DLV/lemmas/L4_delivery.md:86-87; CORE/v3_calib.R:163-186 | **Holds verbatim**, with complete fallback-grid freezing as already stipulated. |
| Input null sets and scorer positivity; FAC/lemmas/L7_delivery.md:26-34; UNI/lemmas/L5_delivery.md:23-27 | **Holds verbatim** under (V), the Gaussian response law and EX-A; subset rank is irrelevant. |
| LS0 finite scans and scores; DLV/lemmas/L4_delivery.md:37-39; DLV/lemmas/L1_resources.md:25,43 | **Holds with change:** ≤ a+1 ≤ ℓ+K+1 scans and ≤ 1+(ℓ+K+1)q(p) requests, q(p)=p+p²/4. |
| Work, memory and guard allocation; FAC/lemmas/L7_delivery.md:35-36; FIN:33-44 | **Holds with change from DLV:** use W_G,M_G and shipped preflight bounds. FAC/UNI already stipulate these. |
| Ordinary final local search cap; CORE/cpp/v3_core.cpp:456 | **Holds verbatim:** remains ℓ. |
| Total fallback eliminates schedule_limit; DLV/lemmas/L4_delivery.md:87; FAC/lemmas/L7_delivery.md:37 | **Holds verbatim** for this exit, under the total fallback premises. |
| “Rest … applies verbatim” / “exit walk leaves only null exits”; DLV/lemmas/L4_delivery.md:87-88; FAC/lemmas/L7_delivery.md:36-37 | **FAILS for unrestricted shipped inputs:** CORE/v3_run.R:96-97 and CORE/cpp/v3_core.cpp:474 can throw independently of numerical failure, resource guards or schedule_limit. |
| LS0 move-limit termination is not a stop; DLV/lemmas/L4_delivery.md:38-39; CORE/cpp/v3_core.cpp:463-476 | **Holds verbatim once admitted by the validators.** A rejected cap never starts that search. |
| Successful assembly supplies estimates; CORE/v3_run.R:218,223-228 | **Holds verbatim conditionally on reaching it**; a thrown settings/cap error prevents assembly. |
| D′ scored-set argument; DLV/lemmas/L4_delivery.md:65-77 | **Holds with change** to the hypothetical LS0 cap/event; it controls error on output and cannot eliminate these exits. |

**Exact failing inference.** A polynomial operation bound and sufficient allocation do not imply that a fixed cap validator passes. In particular, `v3_final_run` calls `v3_run_settings` before `cpp_final_run` (CORE/v3_run.R:223-228), and the former throws whenever the production base cap exceeds 10⁶. The fit's no-output event includes ending without returning a fit object (DLV/STATEMENT.md:15-16). This is therefore a delivery failure even though it is not returned as `schedule_limit`. The C++ total-cap rejection is likewise an explicit `stop`, not ordinary move-limit termination or a MACH resource guard.

**Concrete counterexample to the unrestricted claim.** In the ideal machine take the finite dimensions n* = 2^(10⁶), p = p_raw = n*/2 and a centred standardized fixed design with orthogonal nonconstant columns. Use the stipulated nondegenerate Gaussian response law, valid seed, production switches and the full enlarged allocation. Then K=p and ℓ=10⁶+1. The exact branch is unavailable: its model count 2^p exceeds (5H₀+4N₀)p ≤ 9n*p (CORE/v3_preprocess.R:18-32). The fallback and other ideal-machine exclusions can supply a grid, but the final settings call deterministically throws at CORE/v3_run.R:96-97. Hence P(no output)=1 at this n*, irrespective of |S̃₀|, seed or final randomness. No overflow is needed.

This configuration can be inserted at one finite index of an otherwise admissible design sequence satisfying UNI's (V),(S),(P), retaining (V) there and leaving the limits (S),(P) unchanged. Also p≤n at the exceptional index. Asymptotic sandwich and posterior conditions therefore cannot rescue the every-n sentence. This base-cap obstruction would also affect a literal shipped implementation of the old ℓ-cap method at sufficiently large dimensions; it is not caused by the additional |S̃₀| term. That term changes the resource count and adds exposure to the total-cap ceiling.

## 2. Every-n delivery: the precise supported claims

**Not on the unrestricted UNI input domain under IDEAL-W alone**, even retaining all its other premises. Here “alone” distinguishes IDEAL-W from IDEAL-W⁺; IDEAL-W by itself would of course not replace EX-A, MACH, input validity or the allocation conditions.

**With the original code ceilings retained.** In addition to all F-UNI method/machine/allocation premises, valid nondegenerate inputs and (V), the branch-aware conditions are:

- The exact-enumeration branch needs neither LS0 ceiling: it returns before the final settings/LS0 call (CORE/v3_fit.R:120-131).
- On the SMC branch require ℓ≤10⁶ and ℓ+|S̃₀|≤I. For a probability-one delivery claim these must hold almost surely under the data law; the start mode is data-dependent. With the remaining stipulated exit exclusions, these are precisely the additional checks at issue. An offending SMC event of positive probability is a non-null no-output event.

A deterministic, data-independent sufficient domain is

    D_K = {(n,p_raw): n≥3, p_raw≥1,
           ℓ_raw=⌈log₂(n+p_raw+1)⌉≤10⁶,
           ℓ_raw+min(p_raw,⌊n/2⌋)≤I}.

This uses p≤p_raw and |S̃₀|≤K. In F-UNI's settings, p=p_raw almost surely. The more conservative domain stated in W3-RM2-R is exactly

    D = {(n,p_raw): ℓ_raw≤10⁶ and ℓ_raw+⌊n/2⌋≤2³¹−1},

with n≥3 and valid nondegenerate inputs understood. D⊆D_K. Both are bounded domains of integer dimension pairs. D is sufficient, not necessary: exact-branch inputs and some inputs with small start modes lie outside it. In particular, it would be inaccurate to say that *every* input outside D fails, or that no unbounded exact-branch family can deliver under IDEAL-W. What fails is the unrestricted every-n assertion for the stated method and classes. Restricting to D or D_K supplies a finite-domain delivery theorem, not the general n→∞ consistency conclusion.

**With IDEAL-W⁺.** Keep all the other validators and method caps. Remove exactly the two upper rejection tests: `le > 1e6` at CORE/v3_run.R:96 and `cap_ll > numeric_limits<int>::max()` at CORE/cpp/v3_core.cpp:474, interpreting integers as unbounded. More precisely these *rejection predicates become false* (equivalently, the corresponding acceptance conditions are always satisfied). Retain numeric/type/length/finiteness/integrality/lower-bound checks and the 10⁶-maximiser enumeration-to-DP fallback. This is an additional idealisation, not a consequence of more resources.

For the shipped cap and preflight the allocation must cover, at raw dimension, q(p)=p+p²/4 and

    Σ_G ≤ Σ̄ + Kq(p),
    W_G = W̄ + C Kq(p)[n³+p(n+2)],
    M_G = M̄ + C K(K+1),
    mem_n  ≥ max{βM_G+β₀, P₀+A, P₁+A},
    time_n ≥ max{2(τW_G+τ₀), P̄_t, P̄_LS0},
    allocation$mem_gb ≥ mem_n/2³⁰, allocation$hours ≥ time_n/3600.

Here C covers the fixed implementation/concurrency, certificate terms remain included in W̄,M̄, s=ℓ+K+1, W=⌈p/64⌉,

    A=(2s+4)(12K+256)+96s+4(8W+4K+96)+4096,
    P̄_LS0=s q(p)(τU_K+τ₀)/100,

where U_K uniformly bounds the entire timed 200-score interval, including model construction and sorting. These are the changes from DLV's original allocation, already required by FAC/UNI (FIN:33-44; Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:7-25). They cover both the actual run and the shipped initial/escalation preflight (CORE/v3_fit.R:43-65,113-117,144-151). Enlarging the allocation without addressing the two ceilings is insufficient.

Under IDEAL-W⁺, this allocation, the stated production configuration (LS0 on, base cap ℓ, plus-mode rule, exact e4/TDP start, complete scans, total tier-1 fallback), valid seed, EX-A/EX-S/SR/GUARD-W/MACH/CONFIG/TDP-IMPL and the inherited P1/S.3 audit qualifications, the delivery argument works for every finite valid nondegenerate input. Under F-UNI's (V) and response law these inputs occur almost surely, yielding its every-admissible-n delivery sentence. Its asymptotic consistency sentence additionally needs (S),(P), feasibility as stated, and this unbounded-domain idealisation; (S),(P) do not enter the deterministic delivery exclusion.

**Comparison with DLV-0.** This agrees with `/home/fb31/BVS-wt/W3-RM2-R/Theory_work/Wave3/W3-RM2-R/STATEMENT.md:71-93,144-161,219`: DLV-0 re-derives the allocation for the shipped cap/preflight and explicitly strengthens IDEAL-W to IDEAL-W⁺; without that lift it states the sufficient bounded domain D. Its definition at :81 says the upper rejection predicates are “treated as true”; read literally that would trigger rejection, so the operative interpretation of “lift” must be that their acceptance conditions are true, as specified above. The dependence table is consistent with the independently identified obstruction; it is not used as proof of it.

Consequently F-UNI's every-n statement is **not established as written on its unrestricted domain under the original IDEAL-W**. Its delivery conclusion is justified with the branch-aware restrictions above (in particular on D), or on the unrestricted finite input domain after explicitly adopting IDEAL-W⁺ and the cap/preflight allocation. No changes to source files, theorem registrations or git state are made by this review; no scratch files were created.

TRANSFER: NO
EVERY-N UNDER IDEAL-W: NO
