# SC1 — statement-change check v0.1 → v0.2, W3-RM2-R (Sol: codex gpt-6.1-sol, reasoningEffort high; new agent; brief BRIEF_SC1_sol.md). Reply verbatim below.

**Verdict: ACCEPT WITH CHANGES.** The coded-start repair and dependency qualification are sound. Before locking, correct the interval identity and make the guard lift and supported domain explicit. Review performed read-only; no files or git state changed.

**1. Resolution of SL1 findings 1–5**

| SL1 finding | Assessment |
|---|---|
| 1 — input definition | **Resolved.** [STATEMENT:88] now requires response length n, no response dimensions, a scalar whole-number seed, and scalar finite positive allocation fields. These cover the cited public validators. |
| 2 — explicit LS0 guards | **Partially resolved.** [STATEMENT:78] correctly acknowledges that the two comparisons need an additional idealisation. However, “fixed machine limit,” “at least,” and “whatever further guards the audit lists” leave its scope insufficiently fixed. The domain needs qualification as a conservative sufficient domain. |
| 3 — coded-start event | **Resolved in (a′)/(b⁺).** They now use `St_n(𝓛′) := {S̃₀ ∈ 𝓛′}`, as requested. The added interval equality at [STATEMENT:66] is nevertheless false without an additional containment condition. |
| 4 — DLV implication edge | **Resolved.** [STATEMENT:217] explicitly removes the registry implication and distinguishes recovery of the delivery conclusion under the new premises. |
| 5 — DLV premise pointers | **Resolved.** The requested ranges are now 21–42 and 43–44. There is a separate new pointer error noted below. |

**2. Dependents, interval events, and guard audit**

The definition St_n(𝓛′)={S̃₀∈𝓛′} is correct. Given E4’s hypotheses, Sand_n(𝓛′)⊆St_n(𝓛′) is also correct: E4 identifies the coded start as one of the maximisers quantified over by `Sand_n`. See [E4:219].

The claimed equality St_n(𝓛′)={[S₀,S̃₀]⊆𝓛′} does **not** follow merely from down-closure. With the usual definition [A,B]={T:A⊆T⊆B}, the interval is empty when A⊄B. For example, take S₀={1}, 𝓛′={{1}}, and S̃₀=∅. Then `St_n` fails, but the empty interval is contained in 𝓛′. E4 does not itself guarantee truth inclusion.

The correct identity is St_n(𝓛′) = {S₀⊆S̃₀} ∩ {[S₀,S̃₀]⊆𝓛′}. Alternatively, retain only the forward implication already justified in the text.

With that correction:

- **(C0⁺)(a′): passes.** Membership of the coded start and down-closure retain the visited sets, including the deletion sets needed by the descent argument. The cap exceeds the number of extra-variable deletions.
- **(C0⁺)(b⁺): passes.** Its pathwise inclusion is unchanged. Replacing `Sand_n` by `St_n` improves the search-failure bound and weakens the sufficient probability hypothesis.
- **(c⁺), (C-D), and the delivery conclusions of (C1⁺)/(C2⁺): remain conditional on the delivery-premise repair below.** Their assembly introduces no additional statistical error.
- **The law-free source clarification passes.** It separates delivery from consistency and respects the distinction in [R-AUD1:32] and [TRIAGE:23].
- **The dependency table passes substantively**, except that the RM0-plus explanation should say that (a′) with 𝓛′=𝓛 *recovers (a) after imposing `Sand_n(Q)`*. With `St_n`, it is stronger than (a), rather than literally identical.

The two named guard sites are correct:

| Site | Actual check | Assessment |
|---|---|---|
| [v3_run.R:95] | Rejects `le > 1e6`, alongside type, length, finiteness, integrality and lower-bound checks | The upper-bound predicate needs the explicit lift. It is an option-validation ceiling, not inherently a machine representability limit. I reproduced rejection at `le = 1000001`. |
| [v3_core.cpp:473] | Rejects negative base cap or total cap greater than `numeric_limits<int>::max()` | The total-cap upper bound needs the stated unbounded-integer interpretation/lift. |

IDEAL-W⁺ should name these **upper-bound predicates exactly**, retain their other validation conditions, and state which other guards, if any, are lifted. A later proof audit should verify this fixed premise rather than determine its contents retrospectively.

For the supported domain, let p be the retained predictor count and ℓ=⌈log₂(n+p+1)⌉, K=min(p,⌊n/2⌋). On an SMC branch, the actual two upper-bound conditions are ℓ≤10⁶, ℓ+|S̃₀|≤2³¹−1. A sufficient condition depending only on dimensions is ℓ≤10⁶, ℓ+K≤2³¹−1.

The displayed raw-dimension domain in [STATEMENT:84] implies these conditions, because p≤p_raw and |S̃₀|≤K≤⌊n/2⌋. Thus its inequalities are **correct as conservative sufficient bounds**, while retaining original IDEAL-W, EX-A, MACH and the allocation premises. They do not describe the exact supported domain:

- They replace retained p with p_raw.
- They replace the actual start size, or even K, with ⌊n/2⌋.
- The exact branch returns before either LS0 guard is consulted.

Remove the unresolved “whatever further guards” qualification, label the domain sufficient, and delete the unsupported claim about *any physical machine*. Its boundedness does correctly explain why this restricted version cannot support unrestricted asymptotics.

I found **no additional reachable size-ceiling rejection requiring a lift** under the stated production configuration. The other relevant fixed-threshold sites are:

| Site | Behaviour and disposition |
|---|---|
| [v3_core.cpp:146], called at [v3_core.cpp:274] | Rejects block width outside 1–16. Production sets B=min(⌊√n⌋,⌊√p⌋,16), so valid non-degenerate inputs pass automatically. Preserve this validator. |
| [v3_start.h:290] | Enumeration count reaching the fixed 10⁶ cap triggers truncation; [v3_start.h:303] invokes the tie-aware DP. This is successful control flow, not a no-output exit; preserve it. |
| [v3_start.h:272] | Rejects a tie-DP enumeration-cap argument below 2. The production call supplies 10⁶, so it cannot fire. |
| [v3_calib.R:19] | The thresholds 25 and 10⁴ control archive snapshots only. The complete candidate set still drives grid construction; preserve them. |

The separate `check_blocks` validator at [v3_core.cpp:148] belongs to supplied-block interfaces, rather than the production setup path. Grid interval and local-search move caps use size-dependent budgets, not fixed machine ceilings.

**3. Classification relative to v0.1**

Classifications distinguish changes to hypotheses from changes to conclusions.

| Clause/change | Tag | Reason |
|---|---|---|
| Version/status text and corrected source ranges | **EQUAL** | Editorial only. |
| Valid non-degenerate input definition | **WEAKER** | Narrows the input domain of the universal delivery assertions. |
| `Sand_n` retained as sufficient; introduction of coded-start notation | **EQUAL** as notation | Does not change the original sandwich event. |
| Claimed interval equality | **NEW-CLAIM** | Additional identity; requires the correction above. |
| (C0⁺)(a′) using `St_n` | **STRONGER** | Same conclusion under a weaker start-event hypothesis. |
| (C0⁺)(b⁺), pathwise mode/search inclusion | **EQUAL** | Unchanged inclusion. |
| (C0⁺)(b⁺), search bound and convergence criterion | **STRONGER** | Smaller start-failure term and weaker sufficient convergence condition. |
| IDEAL-W⁺ and delivery under it: (C-D), (c⁺), delivery parts of (C1⁺)/(C2⁺) | **WEAKER** | Adds an idealisation to the delivery premise; valid-input domain also narrows. |
| Delivery on 𝔇 without the additional lift | **NEW-CLAIM** | Adds an explicit restricted-domain alternative. |
| (C-D) law-free input inventory and exclusion of Prop F’s consistency sentence | **EQUAL** | Clarifies the delivery-only claim already stated in v0.1. |
| DLV-0 dependency row | **WEAKER** | Withdraws the registry implication and retains only qualified recovery of its delivery conclusion. |
| Output-conditional parts of (C1⁺)/(C2⁺), other statistical dependencies | **EQUAL** | Their statements are unchanged by this diff. |

The v0.2 changelog should record these classifications; “pre-lock repair” is not one of the specified tags.

**4. Findings, lines, and fixes**

1. **[S] False unconditional interval identity — [STATEMENT:66].** An interval with incomparable endpoints is empty, making containment vacuous. **Fix:** add S₀⊆S̃₀ to the right-hand event, or state only the forward implication.

2. **[F] Guard lift lacks a closed, precise scope — [STATEMENT:78]; [PLAN:14].** The literal 10⁶ validation ceiling does not fit the stated “machine limit” definition cleanly, and the inventory remains open-ended. **Fix:** specify the exact lifted upper-bound predicates and preserve all other validation, enumeration, fallback and method-cap logic.

3. **[F] Supported-domain statement is provisional and overdescribed — [STATEMENT:84].** Its inequalities are sufficient, not exact; its additional conditions are unspecified. The physical-machine assertion has no supporting premise. **Fix:** define a closed sufficient domain, retain the remaining computational premises explicitly, and remove that assertion.

4. **[E] RM0 dependency explanation overstates identity — [STATEMENT:216].** **Fix:** replace “(a′) with 𝓛′ = 𝓛 is (a)” with “(a′) with 𝓛′ = 𝓛 recovers (a) using Sand_n(Q) ⊆ St_n(𝓛).”

5. **[E] Version, pointer and classification bookkeeping — [STATEMENT:1], [STATEMENT:79], [STATEMENT:254].** **Fix:** update the title to v0.2; cite DLV IDEAL-W at [DLV STATEMENT:24], not 22–23; replace the changelog’s “pre-lock repair” classification with per-clause tags. Extend the allocation-validator pointer through [v3_fit.R:94].
