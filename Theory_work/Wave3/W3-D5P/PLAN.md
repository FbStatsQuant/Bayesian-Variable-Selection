# W3-D5P — PLAN (v0.1, with the statement draft v0.1)

**Route (the consultant's: a short corollary of Result 3 = Theorem 6 + posterior concentration).** No new key lemma.

| step | object | content | inputs | hours |
|---|---|---|---|---|
| 1 | `lemmas/L1_listK.md` — LIST-K | Total-variation identity π_𝒯 vs π (= 1 − π(𝒯)); π_𝒯(S₀) ≥ π(S₀); PIP bounds; strict-½ median rule; Z_𝒯 = π(𝒯)Z. Half a page, elementary; written for Lean (finite sums over a finite set, no measure theory). | — | 1.5 |
| 2 | `lemmas/L2_listCODE.md` — LIST-CODE | Code reading at the pin with `file:line` for every step: (i) status ⇔ estimates_available on the sampler branch (`v3_run.R:141-149, 218`; `v3_fit.R:150-173`, `:79-87`); LS0 executed in the final run (`cpp/v3_core.cpp:413-481`), deterministic given the data (no uniforms; `eval` reads cache or scorer, equal under EX-A/EX-S), same evaluation sequence as 𝒦_n's search; (ii) CC2; (iii) `offer_stores` offers the same (F, S) to `top` (`cpp/v3_ledger.h:89-94`) — the only HPM offer outside `offer_stores` is in the numerical-failure handler (`cpp/v3_core.cpp:483-507`), not on completed runs; TopStore invariant (`cpp/v3_ledger.h:43-57`, cap 40p + 1 ≥ 41): the TopCmp-first offered entry is never rejected or erased; TopCmp ranks value first, as hpm_better; distinctness (std::set keyed by (F, S), F a function of S under EX-A); values = F (`store_to_list`, `cpp/v3_core.cpp:358-362`); original indices (`to_orig`); (iv) `cpp_enumerate` recursion covers Ω (`:533-556`), `v3_enumerate` (`v3_exact.R:6-19`), `v3_fit.R:120-132`. | CC2, CC5 | 3 |
| 3 | `lemmas/L3_listR.md` — LIST-R | Assembly: RM0-plus (b⁺) data event 𝒢⁺_n; on it + completed run: LIST-CODE (i) gives S₀ ∈ 𝓜^run, (v) gives S₀ ∈ 𝒯, `hpm` = S₀; IMPL-LIST identifies the fields with pip_𝒯 etc.; LIST-K gives the bounds. Exact branch via (iv). (ii) [POST] and POST (b) for the rate; the 2t bound from (d); union bound for the P(𝒪 ∩ …) form. (iii) DLV-0. | LIST-K, LIST-CODE, RM2-R-plus, RM0-plus, DLV-0, W2-APP:POST | 2 |
| 4 | numerics | (a) LIST-K by brute force on random small Ω (p ≤ 8, random F, random 𝒯 ∋ S₀): every inequality, and equality in (b) at 𝒜 = Ω ∖ 𝒯; (b) an end-to-end check of the main claim at one small exact case through the real core: a fit on a small Gaussian AR(ρ) design that hits the sampler branch, computing SPEC §2 from `top_store` by hand and comparing with the exact enumeration (v3_enumerate on the same ctx): S₀ ∈ 𝒯, hpm = S₀, the bounds. Post-processing only (the fields are not yet implemented). | — | 2 |
| 5 | READER_DELTA.md | reader form: "Corollary 6L" under Theorem 6 (one display) + card text proposal (new row 3.1L, or an addition to 3.1 / 3.6). | — | 1 |
| 6 | checks | statement lock (one Sol read) → CP1 → blind Opus line check of L1–L3 (one batch, fresh agent) → citecheck → council (Sol + Opus seats) → diff rounds Opus-only (manager's brief) → CP3 → API blind-audit card for HQ (pattern `API_AUDIT/audit1/`, dept/theory). | — | (reviewer time) |

**Total lead time ≈ 10 h + reviews** (estimate 1–2 days; kill at 3 days, HQ).

**Risks.** (R1) the code-level identity of LS0 in the run with 𝒦_n's search needs a careful argument about the cache
(a hit returns the same log m under EX-A); mitigated by CC2(a). (R2) IMPL-LIST stays open until the method commit
exists: the claims are stated against SPEC and carry IMPL-LIST as a named premise; at CP3 either the commit exists and a
short code-reading addendum discharges it, or the status carries "conditional on IMPL-LIST". (R3) the rate clause needs
p ≥ 2 (the range of POST); stated.

**Stop rule.** If the corollary route failed (it has not: no step needs a new estimate), stop at the plan stage and tell
the manager.
