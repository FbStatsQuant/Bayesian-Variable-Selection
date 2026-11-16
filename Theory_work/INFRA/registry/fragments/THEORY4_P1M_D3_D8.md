# THEORY-4 carrier: registry wording of Engineering decisions D-3 and D-8 (HQ-confirmed)

Verbatim from Docs/Experiments/P1M/REQUESTS.md section THEORY-4 (root clone, untracked at staging, 2026-11-15).
Frozen here so the registry hashes a stable text. Staged by the SMC-Theory recorder; HQ approves the recording run.

## Entry A (D-3)

**Entry A: D-3, cost column (kind: implementation / reporting rule; no change to any estimate).**

> In runs of the large-p engine (v4, production and compat modes), the published cost measure is `score_counts$logical`:
> the number of logical score events per phase and mechanism, defined exactly as in v3.1 (`cpp/v3_ledger.h:74`; every
> evaluated or held configuration counts once, cache or not). `score_counts$fresh` and cache statistics are
> implementation-dependent. They are reported only with a declared fixed cache capacity, labelled "implementation
> counter", and never enter a published table or theorem check. Published v3.1 tables (EVIDENCE §8, RERUN_SPEC cost
> column, `evidence_h2.py:98-105, 139-141`) keep their values and their definition.
> Scope: W3-SCALE ruling O17, case (a) by redefinition (option B2-3).

Status: HQ-CONFIRMED decision D-3; implementation pending

## Entry B (D-8), outputs (i), (iii), (iv)

**Entry B: D-8, new returned outputs (kind: implementation; additions only; every existing output unchanged).**

Notation: 𝒯 = the merged `top_store`, i.e. the 40p + 1 best-scored distinct models offered to the final ledger(s),
merged over R′ islands as the top-c of the union (O10). F(S) = log ϖ(S) + log m(S), exact scores (CC2).

> (i) `pip_store[j]` = Σ_{S∈𝒯, j∈S} e^{F(S)} / Σ_{S∈𝒯} e^{F(S)}: the store-renormalised PIP. It needs no island weights
>     and is the j-th marginal of Π̂^𝒯 (W3-DIST DIST-C(i)).
> (iii) `law.bin`: the store-BMA law Π̂^𝒯, truncated at relative weight 10⁻¹² (the dropped relative mass is reported).
>     Per model it stores S, F(S) and the conjugate posterior parameters of (θ_S, v) on the standardised scale, plus the
>     column standardisation constants. It is the object of DIST-C(i). Draws from it, if requested, use streams disjoint
>     from the engine's.
> (iv) Terminal particle supports (after the last measured round), archived as a **diagnostic**, explicitly not an
>     estimate. No theorem covers a particle-based law.

Status: HQ-CONFIRMED decision D-8; implementation pending; (i) and (iii) conditional on W3-DIST:DIST-C(i)

## Entry B (D-8), output (ii)

**Entry B: D-8, new returned outputs (kind: implementation; additions only; every existing output unchanged).**

> (ii) `log_Z_store` = log Σ_{S∈𝒯} e^{F(S)}. Under EX-A, log_Z_store ≤ log Z deterministically (F is the log of the
>     unnormalised posterior mass of S, and 𝒯 ⊆ Ω).

Status: CODE-CHECKED (Engineering file:line pins, REQUESTS.md THEORY-5; each pin verified by the HQ recorder): deterministic under EX-A; implementation pending

## Check C (D-7): PLACEHOLDER, not a registry entry

Waits on the PSMC-S0 verdict (due Thu 12:00 CT). Only after it: an output-list change "final islands do not build
leaders_gamma0 / leaders_gamma1 and the fit does not return them" is staged here as an implementation entry.

