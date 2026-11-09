# C-DLV council round 1, Claude Opus 5.5 seat

Reviewed state: the files as they stood at 22:50 (STATEMENT.md and L1 were edited at 22:50:06, after Codex's council
note; I reviewed that version). I did not read C1_council_codex.md. Read-only apart from this file.

What I checked independently:
- **Code:** `v3_fit.R` (all), `v3_calib.R` (all), `cpp/v3_calib.h` (all), `v3_run.R:66-200`, `cpp/v3_runtime.h`,
  `cpp/v3_engine.h:136-160, 295-345, 376-425`, `cpp/v3_score.h:255-300`, `cpp/v3_start.h:1-120 (logr), 150-240`,
  `cpp/v3_ledger.h`, `cpp/v3_core.cpp:665-790`, `v3_preprocess.R:1-40, 90-125`, `v3_setup.R:1-80`, and every
  `stop`/`throw` site in the core.
- **Spec:** `02_method.tex:55-64, 300-352, 400-407, 488-502, 580-592, 650-662`.
- **Cited results:** W1-GEN STATEMENT (C1)-(C3), W1-PXN STATEMENT §2, and W1-N3 L7.
- **Recomputed:** θ, s_θ, λ_θ, the 20.4526 ratio, 2√c₀·2⁶⁰ = 7.4846·10¹⁷, and the n_β root.
- **Algebra re-derived:** Lemmas 3.1, 3.2, 3.2′, 3.3, 3.4, Proposition 3.5, Lemmas 5.0, 5.1, 5.2 and 5.2′
  (including the phase counting), Corollary 5.3, Theorem D (i)-(iv), Corollary D′ and Proposition F.

## Gate verdicts

| gate | verdict | reason |
|---|---|---|
| G1 correctness of proved steps | **PASS** | No step claimed as proved is wrong. Checked: the exact identity (L3 3.1); the Peano-kernel bound and monotonicity of ρ(u,·) (3.2); the pilot cap k ≤ T_e and exact landing at 1 (3.3, against `v3_calib.h:30-46` and `v3_engine.h:303-341`); the bisection semantics, including the smallest-dyadic-mid characterisation of `non_progress` (3.4(c), against `v3_calib.h:68-98`); the closed form and the three bounds (5.1); the perturbation sandwich, the step-length lemma and the phase counting (5.0, 5.2, 5.2′). The constants are correct: θ = 0.918274, s_θ = 0.588144, λ_θ = 2.419119, ratio 20.4526 → 21, giving N̄_b = 22 + …. Theorem D's walk through `v3_fit.R:49-144` and `v3_calib.R:135-175` matches the code: a tier-1 failure, preliminary or rebuild, gives `out$grid` NULL (:120), hence :153 `schedule_limit`; a tier-0 failure forces escalation (:82/:114 → :145-149). Corollary D′ is a correct pathwise argument (Markov on 1 − π, then π(S₀) > ½ ⇒ strict F-maximum ⇒ ≻-max of the scored set equals S₀ once S₀ is scored). The running HPM in `v3_ledger.h` (offer_hpm on every fresh score; a cache hit was processed when first scored) supports "every scored model is a candidate". |
| G2 hypotheses used = stated | **PASS (minor)** | EX-A, IDEAL-W, MACH, CONFIG and TDP-IMPL are used exactly where invoked. EX-S, SR, OP-LS0 and e4 enter only through D′ and the cited results, and L4:68 says so. Two blemishes: L4's Setting omits CONFIG and TDP-IMPL (#4), and IND-T is listed but unused (#4). |
| G3 no hidden assumptions | **PASS (minor)** | The arithmetic, word-size, machine, allocation-success, build and concurrency idealisations are all now explicit premises. No unstated assumption carries weight. The R.1/R.3 work inventory is not exhaustive (#5), but every omitted item is O(p²)-polynomial and already dominated. |
| G4 cited results: status and scope | **PASS (minor)** | W1-N3 L7 (PROVED, XF-checked) is used only for its operation bound; the storage bound is added honestly as a requirement. W1-GEN and W1-PXN are used for the data-level events only. C2/D′ should spell out the class hypotheses and identify 𝒦_n with the exact cited event (#7). |
| G5 constants / rates tracked | **PASS (minor)** | The envelopes are tracked by unit with explicit polynomial shapes. Constants are honestly labelled implementation-dependent. Insertion bounds and thresholds are exact. Two editorial slips remain: the "4000pK" preflight term (#6) and n_β rounded in the wrong direction (#10). |
| G6 fidelity to code and spec | **PASS** | The grid, pilot, rebuild, escalation and freeze logic matches the shipped core line by line. The N3 replay reproduces 51/51 code grids. The spec-only parts (LS0, e4 fallback, workers, certificate) are handled at spec level and labelled. TDP-IMPL is correctly flagged as an added implementation requirement, not a spec fact. |

**Classification honesty:**
- Honest overall. (T) is explicitly not claimed. P1–P5 are genuinely proved, under the stated premises and with the
  code-reading caveat for F2.
- C1 is correctly labelled conditional. Its conditions have no known instance, though, and the STATEMENT does not say
  so (#2).
- F1 is correctly a finding about a shipped component.
- C2 is effectively proved, from the cited results plus Theorem D. The label "conditional/joint" understates it, which
  is the conservative direction and acceptable.

**Is (O) stated exactly?** No. As written it is a sufficient programme, not the exact open event: it omits the
escalation conjunct and the coupling between tier 0 and tier 1 (#1). It is easy to fix.

**Score: 8.6 / 10** (uncapped). No FATAL and no MAJOR findings. Ten MINOR findings, mostly about precision and
surfacing. The mathematics I re-derived is correct throughout.

## Findings

1. **MINOR — (O) is not the exact open event.**
   - Evidence: `STATEMENT.md:72-73`, against `STATEMENT.md:57-59` and `lemmas/L4_delivery.md:12-21`;
     `numerics/N2b_pilot_and_counts.txt:1` (max k/T_e = 1.000); `numerics/SUMMARY_dlv.md` and `N4_SUMMARY.md`
     (0 escalations in 134 fits).
   - By Theorem D the exact remaining question is P(𝒮ℒ_n) → 0, with 𝒮ℒ_n = E_n ∩ ⋃_{c ∈ tier 1}{(α)∨(β)∨(γ)}_c and
     E_n = {some tier-0 trigger fires}.
   - (O) as written asks for "a probability bound on (α)–(γ) for the realised candidate sets and the realised pilot
     stage count". That is one sufficient route. It omits a second one, P(E_n) → 0 (no escalation w.p. → 1). The
     numerics suggest the second route is the operative one: tier 1 was never reached.
   - It also hides the coupling: tier-1 constructions exist only on E_n, and E_n includes `forced_pilot_steps`. Fully
     forced pilots attain k = T_e exactly (N2b), so on that trigger a tier-1 pilot near its own cap is not
     exotic, and any single bisection insertion then gives (α).
   - Required fix: state "(O) ⟺ P(𝒮ℒ_n) → 0 on the classes (equivalently P(E_n ∩ F¹_n) → 0)", then list the two
     sufficient routes, (O-a) P(E_n) → 0 and (O-b) P(F¹_n ∩ E_n) → 0 via (α)–(γ). Say that (O-b) must be proved jointly
     with, or conditionally on, the triggering event, not for an unconditioned tier-1 run.

2. **MINOR — C1 does not say that its sufficient conditions are unrealised at every tested size.**
   - Evidence: `STATEMENT.md:66-68`; `lemmas/L3_grid.md:76-82`; `lemmas/L5_insertions.md:94-104` (Remark 5.4(0));
     `numerics/N3_SUMMARY.md` (r_max ≥ 0.129 in 51/51; 0/51 ≤ 0.02); SUMMARY_dlv and N4 (Λ_V < c₀ in about 12 of
     roughly 410 constructions).
   - C1 is a correct conditional. Its two branches, though, are (a) dominance or small variance and (b) the
     ε-remainder two-model structure, and both are measured to fail on essentially all realised V, while delivery
     still occurred.
   - A reader of the STATEMENT alone cannot see that C1 has no known non-vacuous instance on the classes, so the
     surfacing is incomplete; the classification itself is honest.
   - C1's hypothesis "every calibration candidate set" is also stronger than needed: only tier-1 constructions on E_n
     matter (#1).
   - Required fix: add one sentence to C1 stating the measured status (no design sequence is known to satisfy the
     hypotheses; at the tested sizes they fail with the selected pair; other pairs were not searched). Restrict the
     hypothesis to tier-1 candidate sets.

3. **MINOR — F1's alternative fallback is asserted but not proved.**
   - Evidence: `METHOD_REQUIREMENTS.md:20-21`, against `lemmas/L4_delivery.md:70-82`.
   - METHOD_REQUIREMENTS offers "the tier-1 pilot schedule …, or the last successful construction of that tier
     when one exists". Proposition F proves only the pilot-schedule version.
   - The extension is immediate: a successful construction starts at 0, ends at 1, is strictly increasing, has ≤ T₁
     intervals and passes `v3_check_grid`. It should still be stated, or the alternative dropped.
   - Required fix: add the one-line extension to Proposition F, or remove the alternative from
     METHOD_REQUIREMENTS B.

4. **MINOR — The premise lists are not propagated consistently.**
   - Evidence: `lemmas/L4_delivery.md:6-8` (Setting lists EX-A, EX-S, SR, OP-LS0, e4, GUARD-W, IDEAL-W, MACH), against
     `STATEMENT.md:57` ("P4 … uses P2, hence TDP-IMPL") and `STATEMENT.md:41` ("Used by P2, P4, C2 and F1").
   - Theorem D invokes Corollary R, which holds "within CONFIG" and with TDP-IMPL (L1:69). Proposition F inherits
     "the premises of Theorem D".
   - IND-T (`STATEMENT.md:22`) is listed but used in no delivery proof.
   - Required fix: add CONFIG and TDP-IMPL to L4's Setting. Mark IND-T as "not used by this ticket's proofs (final-run
     validity only)", or drop it.

5. **MINOR — The work inventory claims to be exhaustive but omits on-call-graph items.**
   - Evidence: `lemmas/L1_resources.md:14-28` (R.1 "every loop is capped") and :53-67 (R.3).
   - Omitted items:
     - `cpp_dup_components`, called at `v3_fit.R:92` before the branch split (`cpp/v3_core.cpp:714`: O(p²) pair scan
       plus union-find).
     - `cpp_cut_group` at `v3_fit.R:114` (`cpp/v3_core.cpp:762`: O(p²) scan; Rcpp `List::push_back` up to O(p²)).
     - R-level assembly: `v3_bind_records`/stage tables, the `order()` in `v3_V_snapshot` at O(|V| log|V|),
       `identical(gn$grid, g$grid)`.
     - The R `while` loops in `v3_isqrt`/`v3_ceil_log2` (`v3_preprocess.R:14-15`).
   - All are polynomial and dominated by the np² + p³ + Σ̄ terms, so Lemma R's conclusion stands. The proof's
     "(R.1) every loop is capped" is, however, presented as a complete table.
   - Required fix: add these rows, or one catch-all row with a code-audit note.

6. **MINOR — The "explicit sum" for preflight bytes does not match the code.**
   - Evidence: `lemmas/L1_resources.md:120-122`, "the explicit sums at `v3_fit.R:27-32` … + 4000pK"; the code is
     `cache = 29 * 2^ceiling(log2(2 * C_cache)) + 4 * C_cache * K` with C_cache = 500p (`v3_fit.R:18, :30`), i.e.
     2000pK.
   - The inequality "P_e ≤ …" stays true, as an overestimate, but the text identifies the bound with the code's sum.
   - Required fix: write 2000pK, or say "≤ (overestimate)".

7. **MINOR — C2/D′ cite the consistency results by their headline, not by the exact event and hypotheses used.**
   - Evidence: `STATEMENT.md:69`; `lemmas/L4_delivery.md:50-58`; `Theory_work/Wave1/W1-GEN/STATEMENT.md` (C1)-(C3);
     `Theory_work/Wave1/W1-PXN/STATEMENT.md:51-65`.
   - D′ needs P(𝒦_nᶜ) → 0 with 𝒦_n = {LS0 from S̃₀ scores S₀}. W1-PXN (T) states exactly this. W1-GEN's headline is
     D_n ≤ P(S̃₀ ≠ S*) + P(Ω_nᶜ). The 𝒦_n statement is its (C1)+(C2): on Ω_n ∩ {S̃₀ = S*} the capped search scores S₀
     when ℓ_n ≥ τ(S*) − 1. That requires (H0)–(H2), n ≥ n₀ and ℓ_n ≥ 2^{v̄} − 2.
   - "On the classes" also covers LH (exact Gram) only as a W1-GEN instance.
   - Required fix: in C2/D′, cite W1-GEN (C1)+(C2) and W1-PXN (T) as the source of P(𝒦_nᶜ) → 0. List the class
     hypotheses: (H0)–(H2), n ≥ n₀, ℓ_n = ⌈log₂(n+p+1)⌉ ≥ 2^{v̄} − 2 eventually; (SIZE), (OP) for LH-iid. Say which
     instance covers LH.

8. **MINOR — The numerics never exercise the open event.**
   - Evidence: `numerics/SUMMARY_dlv.md` ("Escalated fits: 0 rows", all trigger strings "t0:" with nothing fired);
     `numerics/N4_SUMMARY.md` (all constructions at tier 0).
   - Across 80 + 54 production fits no tier-1 construction ever ran. The evidence bounds tier-0 construction behaviour
     (max 39 intervals vs T₀ = 1000) and shows triggers rarely fire. It says nothing directly about tier-1
     constructions on E_n.
   - CHECKPOINT/SUMMARY phrasing such as "80/80 completed" is accurate but invites over-reading.
   - Required fix: one line in SUMMARY_dlv and in the REPORT: "no fit escalated; 𝒮ℒ_n was never at risk in these runs;
     the numerics bear on route (O-a), not (O-b)".

9. **MINOR (editorial) — Two stale or colliding labels.**
   - Evidence: `lemmas/L5_insertions.md:49`, "(plus at most one step that crosses from Phase 1)".
     - This conflicts with the final count, which handles the crossing step by starting-coordinate indexing
       (L5:51-57): a crossing trial starts in Phase 1 and is counted there.
     - Delete the parenthetical.
   - `INVENTORY.md:61-69`: rows run F1, F2, F4, F5, F6, F3.
     - "F1" (OOM) collides with finding F1, which is confusing in STATEMENT/L4 cross-references.
     - Rename them, e.g. to P1–P6, and reorder.

10. **MINOR (editorial) — n_β is rounded in the wrong direction.**
    - Evidence: `lemmas/L4_delivery.md:43-48` and `METHOD_REQUIREMENTS.md:30-31`.
    - The stated crude bound equals 2√c₀·2⁶⁰ at n_β = 2.2772·10⁸. At n = 2.28·10⁸ it is 7.503·10¹⁷ > 7.4846·10¹⁷, so
      "(β) impossible for n ≤ 2.28·10⁸" is false at the endpoint.
    - Required fix: write n ≤ 2.277·10⁸ (or "≈ 2.2772·10⁸, rounded down").

## Things I tried to break that held

- **(γ) via a bisection appended at 1.** L5's preamble shows that a bisection-limited trial's snapped point always
  fails validation, because ρ(u,1) ≤ ρ(u,b) < 0.9. So N_p′ ≤ k really counts only pilot targets and snaps.
- **Second `non_progress` site** (`v3_calib.h:90`): it cannot fire once a mid passed (lo > u), nor on a snap, under
  EX-A.
- **`grid_failure_no_escalation`:** unreachable, since a tier-0 failure sets the trigger and then either escalates or
  stops with `resource_limit` (`v3_calib.R:145-149`).
- **Score cache:** linear probing terminates (capacity 500p < nslots ≥ 1000p; full clears at capacity); the ω bound
  is correct.
- **Start-mode fast path:** every visited DFS node lies on an attaining path (M is an exact max), so there are ≤ J·10⁶
  nodes; the 10⁶(J + K log K) term is adequate.
- **Remark D.1's d-range:** `logr` is log m(U) − log m₀ (`v3_start.h:95`), and the size prior cancels in d
  (`v3_core.cpp:683`), so the (K+1)-term bound is valid.
- **`nth_nonmember`:** the floor of u·(p−k) with u ∈ [0,1) stays in range, so S.3 (v) holds.
- **B ≤ K for n ≥ 3:** checked, so the k > K throw is unreachable from the tables.
- **Proposition F:** the pilot schedule passes `v3_check_grid` exactly under EX-A (starts at 0.0, ends at 1.0, strictly
  increasing), has ≤ T₁ intervals and is frozen before the final streams. The patched law differs from the shipped law
  only on 𝒮ℒ_n.
- **Corollary R's guard argument:** both elapsed time (which includes `elapsed_before`) and the just-completed
  operation are ≤ the whole-fit wall time, so time_n ≥ 2(τW̄ + τ₀) suffices.
