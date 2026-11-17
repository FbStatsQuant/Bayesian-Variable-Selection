# CLC1 reply (Claude Opus 5.5 high, fresh blind agent, delegate 359b20ec; returned 2026-11-16) — verbatim

I found one exit that no row covers, so I'm returning **NOT VERIFIED** on C1 as stated. The fix is an amendment: one inventory row is missing. The rest of the item holds up against the code at the pin.

I confirmed the core at 4676af6 is unchanged at HEAD (`git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`). I re-read `v3_fit` and everything it calls, R and C++, without relying on T10's map. Line numbers are relative to `Scripts/SMC_BVS/core/` unless a path says otherwise.

**What I independently confirm**
- **Status values:** the only ones that can reach `v3_fit` are `invalid_input`, `no_predictors`, `y_constant`, `resource_limit`, `numerical_failure`, `schedule_limit` and `grid_failure_no_escalation`.
- **The §1.1 table (where `estimates_available` becomes TRUE):** this happens only at `v3_fit.R:129`, or by copying the final-run result at `v3_fit.R:171`, which is TRUE only at `v3_run.R:218`. `finish` never sets it.
- **The §1.2 grep list:** it matches the code exactly, and the off-call-graph sites are indeed off the graph.
- **D2:** unreachable. Escalation happens at `v3_calib.R:154-158` and the stop is at `v3_calib.R:170`.
- **Invariants (i)–(vii):** each holds at the re-located lines. For (i), B ≥ 1 follows from `v3_preprocess.R:22` with n ≥ 3, p ≥ 1.
- **`get_holder`:** unreachable.
- **`start_mode` throws:** the `:272` throw needs cap < 2, but the only call passes 10⁶. The `:261` throw sits only on the truncated tie-DP path, which T9 (TDP-e) covers.
- **Provenance lookups:** `hpm_mech` defaults to 0 and every mechanism is ≥ 0, so the "none" string never reaches `mech_index`.
- **D1:** unreachable under EX-A (`v3_calib.h:30-46`: each pilot step either returns 1, moves up by at least 1/T_e, or is snapped to exactly 1).
- **X7/X8 bound:** with the options unset, ℓ ≤ 32 and `cap_ll` ≤ 2³⁰ + 31 < INT_MAX.

**Findings**

1. **C** — `v3_fit.R:43-47, 61-66, 114-117` (and `:145`). Item lines: `C1_AUDITS/PROOF.md:19`, `STATEMENT.md:32-35, 46-49`.
   - **What fails:** with default options, `v3.ls0_cap` is unset, so `ls0_wc = TRUE` (`v3_fit.R:114`). The SMC-branch preflight then also returns `resource_limit` when the estimated worst-case LS0 time, 2·(ℓ+K+1)·(p+p²/4)·ŝ_K, exceeds `hours·3600`, where ŝ_K is a measured time per score of size K (`v3_fit.R:47, 65`). It also adds an `ls0_archive` byte term (`v3_fit.R:45`).
   - **Why no row covers it:** row B1's trigger is memory only, with an explicit byte formula that has no LS0 term. Row B2 is the exact branch only. The item's own reading says a row covers a site only when the site is an instance of the row's trigger, so this exit is uncovered. PROOF §1.1 maps `v3_fit.R:117` to "B1, B2" without comment. T10 §1 notes the option but also files it under B1/B2.
   - **History:** the check came in with commit ef33f91c (2026-11-09), one day after INVENTORY v2.
   - **Reachability:** it fires on valid inputs with the default 8 GiB / 24 h allocation. By the formula, (n, p) = (400, 4000) puts the memory estimate near 2.7 GB, so memory passes. There are about 8.5·10⁸ LS0 score requests, so at ŝ₂₀₀ ≳ 10⁻⁴ s the time estimate exceeds 24 h. That is an order-of-magnitude estimate; I did not run it.
   - **Escalation preflight:** the same check runs in the escalation re-preflight (B3), but it cannot newly fire there. ŝ_K is cached, so the time is the same one that already passed at tier 0.
   - **Consequence for DLV-0:** (C1-c) hands B1–B3 to DLV-0's walk "(Theorem D, Lemma R, Prop F)". But the registered Lemma R (`Theory_work/Wave1C/C-DLV/STATEMENT.md:54-56`) bounds only *exact-branch* preflight seconds. Its CONFIG also counts LS0 at cap ℓ, while the shipped default cap is ℓ+|S̃₀|. So "No correctness break on row 3.1" (`STATEMENT.md:49`) is not supported until someone checks whether DLV-0's own resource re-audit covers this trigger.
   - **Fix:**
     - Add an amendment A-7 and a new row (B1′, or an extended B1) for the SMC LS0 worst-case preflight. Trigger: bytes including `ls0_archive` > mem, **or** the LS0 seconds estimate > hours. Gate: `ls0` on and `v3.ls0_cap ≠ "ell_n"`. Class (b)-like under MACH, as for B2.
     - Map `v3_fit.R:117` and `:154-159` (via `:145`) to it.
     - Tell DLV-0 and Lemma R that the SMC LS0 preflight seconds need a polynomial bound dominated by 𝒜_n.
     - Withdraw the "no correctness break" sentence until that is checked.

2. **S** — `STATEMENT.md:22` (also `:44-45`). "Default options (`ls0 = TRUE`, `grid_fallback = TRUE`)" leaves out the options that the conclusions depend on:
   - `v3.ls0_cap` unset gives the merged LS0 cap used in the X8 bound, and turns on the preflight in finding 1.
   - `v3.ls0_ell` unset is needed for the X7 bound (`le` = ℓ ≤ 32). T14 states this explicitly.
   - `v3.ls0_tie_dp` unset is needed for the `start_mode` reasoning.

   The (C1-b) X7 clause claims more than is proved if those options are free. Fix: state that `v3.ls0`, `v3.grid_fallback`, `v3.ls0_cap`, `v3.ls0_ell` and `v3.ls0_tie_dp` are all unset, as T14 does.

3. **E** — `PROOF.md:25`. It says the pilot and diagnostic guard stops reach `v3_fit` via "`v3_calib.R:57, 67, 100`". Line 67 is the candidate-set (`cpp_cal_V`) `numerical_failure` return (row C3), not a guard route. Fix: `v3_calib.R:57, 100`.

4. **E** — `PROOF.md:43`. "`runtime_ptr` returns NULL-safe, `cpp/v3_core.cpp:780`": the NULL guard is at `cpp/v3_core.cpp:778-779`, with `runtime_ptr` at `cpp/v3_runtime.h:29-31`. Line 780 allocates the records list. Fix the citation.

5. **E** — `PROOF.md:38-46` (§1.3, "nodes not named by T10"). Two nodes are missing; neither adds an error class, so §1.3's conclusion is unchanged:
   - `cpp_exact_count`, reached through `v3_budgets` (`v3_preprocess.R:28`; `cpp/v3_core.cpp:72-85`). It has no stop, uses saturating `__int128` arithmetic, and its only overflow risk falls under IDEAL-W.
   - The SMC-branch timing path `v3_time_scores` → `v3_context` → `cpp_time_scores` (`v3_fit.R:47` via `time_fun`). Item (vi′) cites `v3_fit.R:12` as exact-branch only, but under the default options it is also on the SMC path. It is still safe: k is clipped to K at `cpp/v3_core.cpp:126`, and the `stopifnot` at `v3_setup.R:8` holds for the column submatrix.

   Fix: name both nodes in §1.3 and say in (vi′) that the timing context is reached on both branches.

CLC1-VERDICT: C1=NOT VERIFIED (1 C: uncovered default SMC LS0-worst-case preflight exit, B1 trigger memory-only, Lemma R bounds only exact-branch preflight seconds; 1 S; 3 E — repairable by amendment A-7 + row B1′ and withdrawing "no correctness break" pending DLV-0 resource check)
