# R01 — plan review (Codex gpt-6.1-sol, reasoningEffort high), verbatim reply

Reviewer: fresh delegate_task (Codex, gpt-6.1-sol, high), read-only, briefed to break PLAN.md v1.0 against SPEC/SoP/code.
Received 2026-11-08 ~21:34 CST.

---

Paths below use these aliases:

- `PLAN` = `Theory_work/Wave1C/C-ENG/PLAN.md`
- `SPEC` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`
- `CORE` = `Scripts/SMC_BVS/core`
- `N3` = `Theory_work/Wave1/W1-N3`

1. **BLOCKER — The planned LS0-stop return retains the exact API hazard that GUARD-W explicitly requires fixing.**

   **Evidence:** `PLAN:80-84` promises “no log_Z/PIP/MPM fields assigned” and declares explicit NA fields “Not in scope.” But `SPEC:136` requires “all estimate fields NA (#15),” and `SPEC:162` explicitly identifies the partial-match hazard where `fit$log_Z` returns `log_Zbar0`.

   This happens in the current public path: `CORE/v3_fit.R:113` assigns `fit$log_Zbar0`; `CORE/v3_run.R:111-115` returns stopped results without an exact `log_Z` member; `CORE/v3_fit.R:141` copies those results into the existing fit without removing `log_Zbar0`. Consequently, a new LS0 guard stop can still expose a numerical value through `fit$log_Z`.

   **Concrete fix:** Implement exact-name unavailable estimate fields on LS0 failure returns, preferably through a shared unavailable-output helper covering all incomplete returns. Preserve partial island values only in explicitly labelled archives. Test the final public `v3_fit` object using both `fit[["log_Z", exact = TRUE]]` and `fit$log_Z`; absence is not the required result. If the interface repair remains separate, make it a prerequisite and do not claim GUARD-W compliance before it lands.

2. **MAJOR — The planned real-table oracle contradicts TDP-E’s actual contract.**

   **Evidence:** `PLAN:99-114` deliberately computes `lex_min(E)`, acknowledging that E can exclude rounded maximizers. Nevertheless, `PLAN:152-155` proposes comparison against brute-force “lex-min of the smallest-size ĝ-maximisers” on real tables.

   A counterexample, also documented in `N3/lemmas/LFP_floating_point.md`, is:

   | Quantity | Value |
   |---|---:|
   | Block | `{0,1}` |
   | K | 1 |
   | λ(0) | 0 |
   | λ(1) | 2⁵⁴ |
   | ρ(∅) | 0 |
   | ρ({0}) | 1 |
   | ρ({1}) | 2 |

   In round-to-nearest-even binary64, both singleton `log_gamma0` values are 2⁵⁴. Thus the brute-force rounded-objective answer is `{0}`. But `arg[0][1]` contains only `{1}`, so E = `{{1}}`; TDP-E returns `{1}`, including when cap = 1 triggers the fallback.

   This is an abstract-table counterexample within the proposed test domain, not a demonstrated data-generated counterexample.

   **Concrete fix:** Separate the contracts and oracles:

   - For exactly representable integer-table arithmetic, compare against brute-force S* and reference TDP.
   - For general doubles, compare TDP-E against independently enumerated **uncapped E**, and verify objective value and smallest maximizing size separately.
   - Include rounding-created ties at block, prefix and prior additions.

   State explicitly that native-double lexicographic optimality over all ĝ-maximizers is not established. A fallback triggered only on truncation cannot establish it for the unchanged fast path either.

3. **MAJOR — The tests omit the explicitly required merged-core/prototype replay.**

   **Evidence:** `SPEC:399` requires “integrated core versus the O-LS0 export on the 3 designs,” including “a deterministic eviction/tie example.” It gates the claim “LS0 is in the shipped core.” `PLAN:163-169` substitutes small S1–S6 regressions against the old core and optional existing harnesses; it does not commit to comparison against `cpp_final_run_ls0`.

   The prototype provides an independent integration reference: `origin/theory/O-LS0:theory_campaign/O-LS0/scripts/ls0_exports.cpp`, function `cpp_final_run_ls0`, runs emitted-centre LS0 after the final search using the same ledger/cache and production ℓ. Small old-versus-new tests do not replace this comparison.

   **Concrete fix:** Add the three-design integrated-versus-export replay and deterministic eviction/tie fixture. Account explicitly for intended provenance differences: the prototype uses `PH_LOCAL`, iter −2; the plan uses `PH_LS0`, iter −1. Compare computational results after narrowly normalizing those expected metadata differences. If the replay cannot run locally, retain it as an unmet release/claim gate rather than treating local regressions as equivalent evidence.

4. **MAJOR — Keeping public `local_limit` exclusively tied to the final search hides a spec-defined LS0 cap.**

   **Evidence:** `PLAN:67-71` reports LS0’s cap separately while keeping fit-level and flags-level `local_limit` unchanged. `SPEC:136` says a completed capped LS0 “returns output with `local_limit`,” and `SPEC:152,234` says its L1 result is “n/a.”

   A run can therefore have `ls0_local_limit = TRUE` but the established public `local_limit = FALSE`. Consumers looking at the existing flag receive the opposite indication from the spec’s wording.

   **Concrete fix:** Preserve search-specific flags in their archives, add an explicit `final_local_limit` if needed, and make public `local_limit` indicate a cap in either production search. Keep `ls0_local_limit` for attribution. Document the capped-LS0 L1 rule independently of `local_certified`.

   The proposed certificate OR rule is otherwise sound: a fully scanned no-improvement centre that equals the final HPM remains a valid certificate even if the other search capped elsewhere. Do not infer that every LS0 cap invalidates an independently established certificate; do preserve the spec’s separate L1 “n/a” reporting rule.

5. **MAJOR — Several proposed integration assertions can pass without exercising or detecting the intended bug.**

   **Evidence:** `PLAN:156-162` checks centre emission using “logical count of phase ls0 ≥ 1” and centre membership in the scanned list. Those conditions also hold when the centre event is omitted: neighbours generate logical events, and `CORE/cpp/v3_engine.h:406` records the centre independently of emission. Also, `ls0_ell = 0` causes `local_limit` only when a strict improving neighbour exists (`v3_engine.h:407-413`).

   `PLAN:163-166` proposes small-n/p public-fit regressions, but `CORE/v3_fit.R:81,93-104` can route them through exact enumeration, bypassing LS0 entirely.

   **Concrete fix:**

   - Use an uncached, previously unscored centre and check the exact event count: centre plus all scanned neighbours. Arrange for that centre to win the HPM/store comparison so omission is observable.
   - Construct a known strict improving neighbour for the zero-move-cap fixture.
   - Assert `branch_run == "smc"`, completed LS0 archive presence, and LS0 counters in every intended integration fixture.
   - Add deterministic cases for an equal-F HPM tie change, a returned HPM different from both search endpoints, cache eviction, and LS0 numerical failure. Ordinary seeds need not exercise these cases.

6. **MINOR — TDP-E’s proof needs explicit input hypotheses and implementation invariants.**

   **Evidence:** `PLAN:110-114` says the claim “holds in binary64,” without carrying over `N3/STATEMENT.md:92-109`’s encoding, finite-intermediate and successful-execution hypotheses. The cited proof sketch `lemmas/TDP_E.md` is also absent from the reviewed tree.

   **Assessment:** For valid finite inputs, the proposed reachability test is correct and complete **for E**. Each allowed edge supplies a compatible per-block maximizing code; a complete path fixes a size allocation, and independently selected codes combine because the blocks partition the indices. Conversely, every compatible member of E supplies such a path. All members have size `kbest`, so greedy inclusion in global index order returns `lex_min(E)`. Under exact arithmetic, E = 𝒜*, hence the result is S*.

   K binding, interleaved block indices and j = 0 do not invalidate this argument. They require careful bounds and encoding:

   - Restrict j to `0..min(t_b,r)`.
   - Preserve the j = 0 identity operation exactly.
   - Convert global IN/OUT decisions into block-position masks.
   - Treat an empty compatible arg family as `allowed = false`.
   - Initialize only `(0,0)` as reachable.
   - After a failed tentative inclusion, recompute the affected row for the committed OUT decision.
   - Never inspect NaN table entries belonging to sizes greater than K.

   **Concrete fix:** Add the proof and hypotheses, distinguish cap-truncated visits from the **uncapped** family E, and add targeted fixtures for those boundaries. Reject or return a declared failure for invalid feasible entries/no valid root rather than silently returning an empty model. NaNs outside the feasible size range are expected; NaNs inside it are outside N3’s stated contract.

7. **MINOR — The switch-off compatibility claim needs an explicit assembly branch and a narrower equality definition.**

   **Evidence:** `PLAN:134` omits `hpm_before_ls0` when LS0 is off, while `PLAN:142` unconditionally describes “E3 from `hpm_before_ls0`.” Current E3 uses the final HPM (`CORE/v3_run.R:148-151`). The plan must preserve that expression when the new snapshot is absent.

   Moreover, `PLAN:136,146` says switch-off output is “byte-identical,” while `PLAN:164` already qualifies this as “modulo timings.” Runtime guard records contain elapsed and operation times (`CORE/cpp/v3_runtime.h:21-25`), and public fits also contain peak-memory measurements (`CORE/v3_fit.R:55-59`). Near an allocation boundary, timing variation can change delivery status.

   **Concrete fix:** Specify the off branch explicitly: retain old E3, certificate, flags, settings and field layout; emit no LS0 metadata. Pass the counter-row inclusion policy through shared ledger serialization, including calibration (`CORE/cpp/v3_core.cpp:360-366,704`). Define regression equality over deterministic outputs of completed runs with sufficient allocation, excluding named operational measurements. Do not promise literal whole-fit byte identity.

Answers to Q1–Q4:

- **Q1:** Neither proposed choice fully captures the spec. Keep per-search cap flags, but make public `local_limit` reflect either search reaching its cap. Certification must attach to the returned model; cap occurrence is a separate operational fact.
- **Q2:** **Yes.** Recompute E1 against the post-LS0 HPM. `SPEC:151` requires flags to be recomputed for the returned model. Keep island maxima unchanged, and preserve the explicit E3 exception from `SPEC:150`.
- **Q3:** **Yes under EX-A, with a clearly bounded native-double claim.** TDP-E satisfies the exact-arithmetic e4 invariant and correctly returns `lex_min(E)` in binary64 under the stated hypotheses. It does **not** establish the prescribed lexicographic choice over all rounded `log_gamma0` maximizers. The plan must stop conflating these guarantees in testing or reporting.
- **Q4:** **Yes.** `SPEC:150` invokes the existing §6.10 rules; `02_method.tex:463-467` specifies at most ℓ moves followed by one further scan. The prototype also passes production `o.ell`. An independent `ls0_ell` override is suitable for testing, but an alternative production schedule needs separate specification authority.

**Overall verdict: REJECT as written.** The TDP-E algorithm is defensible under its precise contract, but the stopped-output interface, cap reporting and required validation need correction before implementation approval.
