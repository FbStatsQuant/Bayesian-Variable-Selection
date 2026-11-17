# LC2 reply — blind line check of X1, X3, X5 (Claude Opus 5.5, high; fresh agent)

Scope and method. I read only the files named in `LC2_brief_opus.md` (no LOG, INDEX, CHECKPOINT, CHECK, CITECHECK or
other `reviews/` file). I re-derived every mathematical step and re-read every cited code line at the pin. Mechanical
checks I ran:
- `git diff --stat 4676af6 HEAD -- Scripts/SMC_BVS/core` gives an empty diff, so the pin is HEAD for the core.
- `cmp` shows `Docs/.../PROOF_v3.tex` and `ARC/main@c4ef0dc/Docs/.../PROOF_v3.tex` are identical.
- In the W3-READER worktree (branch `theory/W3-READER`), `Theory_work/Wave3/W3-READER/STATEMENT.md` was last changed at
  68443dcc, and its sha256 prefix is `29696a79d4f0`. Both match X5.
- `W3-READER:PoolZ` has no row in either worktree's `claims.tsv`.

Tags: C = correctness, S = strength (claim vs. proof, hypotheses), F = faithfulness (quotes, statuses, citations),
E = exposition. None of the findings is a C finding.

---

## X1 (Lemma FR: T12 identities at the pin): **VERIFIED WITH AMENDMENTS**

**What I checked and found correct.**
- **Code reading at 4676af6.** Every step of (B-a) and (B-b) holds at the cited lines:
  - `draw_start` = `draw_pi0` (`v3_engine.h:108`). The initial loop is at :286-292, with `init_states = nullptr` at
    `v3_core.cpp:446`.
  - `logZ = D.logm0 + st.logZbar0` (:299). The fixed grid is at :269-273 and :280, and the stage indices at :306-308.
  - `lw = dphi·d` (:317); `inc = LSE − log N` (:318-319), added to `logZ` at :322.
  - Resampling and copy are at :324-327, then one `population_round` at φ_t (:331). There is no round before stage 1.
  - Then come L rounds at φ = 1 (:343-347), the reset `rb_acc.assign(p, 0)` (:350), and Hm measured rounds with
    `rb_on` set only around `population_round` (:351-360). `res.pip[j] = rb_acc[j]/(N·Hm)` (:364).
  - `eval` sets `lg0 = logprior[k] + comp` and `d = (lm − logm0) − comp` (:95-97); `lgphi = lg0 + φd` (:14).
  - `resample` returns the smallest k with W_k ≥ max(u, denorm_min). The guide table never overshoots and the backward
    loop never moves, as W1-N1:B (B-b) argues. W[N−1] = 1 (:240).
  - The Gibbs step records `oj` before its uniform (:128). `oj = 0` exactly when j ∉ S and |S| = K, which matches T12's
    o_j(S, φ) = 0 when |S⁺| > K.
  - `one_round` draws the order first (:203) over m = p + B + 2 labels (:73), and each label appears once per round. So
    `rb_acc[j]` = Σ_u Σ_i o_j(Y^i_{u,j}, 1) exactly.
  - Cache `find` requires an equal hash and an equal set (`v3_score.h:274-282`).
- **T12 lemmas.** I re-derived the bridge identity, reversibility (via T7), prefix invariance with K_{g_j}1_{J_j} = o_j,
  the resampling mean, the round mean, the induction C_t (t = 0 and t−1 → t), the post-terminal induction and (ii).
  All are correct and agree with PROOF_v6. The step from (FR-b)'s prefix clause with κ_j(σ) = σ⁻¹(g_j) − 1 to (FR-c) is
  right: o_j(·, 1) is bounded, π(o_j) = π(J_j), and Ẑ = Ẑ_T is unchanged after stage T.
- **Verdict text.** "No error found in PROOF_v6 §§1–3, 5" is correct.

**Findings.**
1. **F — wrong PROOF_v6 line ranges** (`X1_T12/PROOF.md:47, :50, :71`; also :43).
   - Lemma 1.2 (`lem:rev`) is at `PROOF_v6.tex:54-72`, not 56-77.
   - Lemma 1.3 (`lem:prefix`) is at :74-81, not 79-87. Lines 83-94 are Lemma 1.4 (positivity).
   - The post-terminal paragraph is at :131, not :130.
   - Lemma 1.1 is at :42-52; line 54 already starts Lemma 1.2.

   Fix: cite 42-52, 54-72, 74-81 and 131.
2. **F — T12 STATEMENT range omits (ii)** (`X1_T12/STATEMENT.md:10`). `STATEMENT.md:23-62` stops before (ii), which is at
   `:64`. Fix: cite `:23-64`, or `:23-61, 64`.
3. **F — the code-of-record call is shown with literals, but the code passes variables** (`X1_T12/STATEMENT.md:21`;
   `PROOF.md:21-22`). `v3_core.cpp:446` reads `E.run_island(r, o.N, g, o.L, o.Hm, o.tier, nullptr)`. The literal Hm = 4
   comes through `o.Hm = ro["measured_rounds"]` (`v3_core.cpp:396`) from `measured_rounds = 4L` (`v3_run.R:90`). N_e and
   L are the production budgets `b$tiers$N[tier+1]` and `b$L` (`v3_run.R:90`), not `frozen$N`/`frozen$L`.

   Fix: add `v3_core.cpp:396` to the chain, and adopt W3-SAMP's convention (`W3-SAMP/STATEMENT.md:47-50`): "N_e and L
   denote the values actually executed".
4. **F — "the only change at the pin" overstates CC** (`X1_T12/PROOF.md:83`). `W3-SAMP:CC` (`CC_code_check.md:9-21`) also
   lists other changes outside the island path:
   - the `local_search` phase argument;
   - the ledger's `PH_LS0`;
   - the start-mode DP after `draw_pi0`;
   - 4 lines of `v3_runtime.h`.

   Fix: "the only change on the island's code path is …".
5. **S — the valid-input hypothesis is not stated** (`X1_T12/STATEMENT.md:24`). T12 is stated "for every valid input"
   (T12 §0: n ≥ 3, a retained column, non-constant y; this gives m > 0 and ϖ > 0, which the bridge lemma uses). FR says
   only "Fix the data". Fix: "Fix a valid input (T12 §0) on the SMC branch".
6. **E — "statistical record" is used without a definition** (`X1_T12/STATEMENT.md:27`; `PROOF.md:25`). Fix: point to
   W1-N1:B's record convention (`L1_bridge.md:14-21`).
7. **E — minor citations** (`X1_T12/PROOF.md:9`; `X1_T12/STATEMENT.md:16`).
   - The proof of W1-N1:B spans `L1_bridge.md:45-125`, not 45-110; (B-d) is outside the cited range.
   - The quoted status "PROVED under the named premises … council-passed" is at `L1_bridge.md:3`, not inside `:33-43`.

---

## X3 (re-check of W3-POST:Lemma-1a′): **VERIFIED WITH AMENDMENTS**

**What I checked and found correct.**
- **Step 1.**
  - `lem:slab`'s variational form gives G_T = X_TᵀCX_T = X_TᵀX_T.
  - y_c = Uᵀμ + ε_c by Uᵀ1 = 0 and UᵀC = Uᵀ, and X_{c,T}θ = Uᵀμ.
  - So ϑ = θ gives Q^c_T ≤ σ*²E′ + ρ, with 0 ≤ ρ = (‖μ‖² + ‖θ‖²)/n ≤ M + M′. The case t = 0 also holds.
- **Step 2.**
  - Both exponent inequalities hold for any deterministic ρ ≥ 0: log u ≤ u − 1; 1/u ≥ 2 − u; and u ≥ 1 is used in
    −ρ/(2σ*²u) ≥ −ρ/(2σ*²).
  - On the v-window, f₀(y_c) = (2πσ*²)^{−(n−1)/2}e^{−E′/2}.
  - D_T ≤ (n+1)^t holds with no condition (`lem:spec`(e)).
  - E Λ′ ≤ 1/√2 + (n−1)/(2n) + (M+M′)/(2σ*²) ≤ C′_Λ.
  - None of these steps uses R.
- **Step 3.**
  - `thm:Ta`'s last inequality holds with any T ∈ Ω.
  - v_m = R^T_mϖ(T) (W_K cancels).
  - `lem:num` gives E N_m = v_m.
  - On 𝓑_n, Θ^T ≤ c♯e^{Λ′}Θ^{(1)}. The union bound is valid for L > c♯², and Markov applies to two nonnegative variables.
  - `thm:T01iii` uses only G and ‖μ‖² ≤ nM.
  - The final display: n^{−(t+1)/2}(n+1)^{t/2}√n = (1 + 1/n)^{t/2}.
  - m^T_n(ω) exists because R^T_K = 0 and t ≤ K.
- **Precisions (i) and (ii).** Both are correct.
- **Verdict.** I agree with X3 that the proof of L1a′ is correct as written, given [P1] and [T03R].

**Findings.**
1. **F — "existing, unchecked proof" misdescribes the record** (`X3_L1A/STATEMENT.md:4`). The registry status is
   "PROVED (by this seat, unchecked)", but the lemma file's own header (`L1a_size_tail.md:3-5`) and its registry row
   record a check history:
   - R01 VERIFIED-WITH-AMENDMENTS;
   - R02 VERIFIED;
   - council C1 seats re-derived the proof line by line;
   - council C3 `correct:PASS`.

   X3 is therefore a further line check under PROTOCOL_v4, not the first. Fix: quote the status verbatim and add "prior
   check record: `L1a_size_tail.md:3-5`; the status label has not been updated to it" (for the recorder).
2. **E/S — the v_m = 0 case is not split off** (`X3_L1A/PROOF.md:36-39`). Θ^{(1)} := N_m/v_m and "E Θ^{(1)} = 1" need
   v_m > 0, that is R^T_m > 0. When R^T_m = 0, the set {|S| > m} ∩ Ω is empty, π(E_m) = 0 and Θ^T = 0 by definition, so
   the bound is trivial. [T03R] makes this split at :93 ("Fix … m with R_m > 0 (otherwise nothing to prove)"). L1a′
   inherits it through "As in [T03R] lines 93-97", but X3's re-statement drops it. Fix: add "for m with R^T_m > 0;
   otherwise Θ^T = 0".
3. **F — R^T_m is not defined in [T03R]** (`X3_L1A/PROOF.md:34-35`). The sum Σ_{k=max(m+1,0)}^K with q_k := 0 outside
   [0, K] is W3-POST's corrected form ([C2A-F4], `W3-POST/STATEMENT.md:36`). [T03R]:16 writes Σ_{k=m+1}^K with q_k
   defined only for 0 ≤ k ≤ p. The two agree for m ≥ −1. Fix: "as defined in L1a′ (W3-POST §0, [C2A-F4]); for m ≥ −1
   this is [T03R]'s R_m with S₀ → T".
4. **F — the "in words" summary drops hypotheses** (`X3_L1A/STATEMENT.md:11-14`). It omits:
   - the hypotheses G and n ≥ 3;
   - the second conclusion, π(|S| > m^T_n(ω)) ≤ (1 + 1/n)^{t/2}e^{−ω}Θ^T.

   Since the paragraph says "not restated", either add these or shorten it to a pointer.
5. **E — [P1] citations** (`X3_L1A/STATEMENT.md:18`). Some ranges stop at the statement, not the proof: `lem:spec` runs
   to :111 and `lem:den` to :360. This is harmless but inconsistent with the other citations.

---

## X5 (re-check of W3-READER:PoolZ): **VERIFIED WITH AMENDMENTS**

**What I checked and found correct.**
- **Steps 1–3.**
  - The quotation of Thm-N1 (`W1-N1/STATEMENT.md:98-104`) and of its localised meaning (:94-96) is verbatim and
    correctly applied with h ≡ 1, which is in the class with B_h = 1.
  - R′ = `islands = 4L` (`v3_run.R:91`; `v3_core.cpp:443`).
  - `log_Z = v3_log_sum_exp(logZr) − log(R)` with R = `length(isl)` (`v3_run.R:150-154`).
  - The union of four null sets is null.
  - Linearity holds for nonnegative Ẑ_r, and Z > 0 is constant for fixed data.
- **(X5-b), the substance.** N1's conditioning is valid for the potential pair (𝒜°, 𝓒°), consistent with T1 (GW-iv)
  and T5 (CAL-b, CAL-d). Moving to the actual 𝒜 needs an assumption about the clock that no premise supplies.

**Findings.**
1. **S — step 4 needs joint measurability in the data, which the N1 premises do not supply** (`X5_POOLZ/PROOF.md:15-18`;
   `X5_POOLZ/STATEMENT.md:21-23`).
   - *What step 4 asserts:* that the fixed-data identity is "a version of E[· | data, 𝓒]". The freezing lemma
     (T12 `lem:freeze`) gives this only when (data, 𝓒) is the frozen element and the integrand g(data, c, U) is jointly
     measurable in all three arguments.
   - *Why the cited premise falls short:* W1-N1's MEAS is joint in (c, u) for fixed data only (`W1-N1/STATEMENT.md:83-85`;
     `L1_bridge.md` (B-d) is per fixed data).
   - *What else step 4 uses:* that 𝓒 is a measurable function of (data, streams 0–9) (T5 CAL-b gives Ψ measurable), and
     that the final streams are independent of the data *jointly with* streams 0–9.
   - *Fix:* add a premise MEAS-J ("(data, c, u) ↦ Φ is jointly measurable"), or a one-line extension of (B-d). The record
     is a finite program whose branches compare Borel functions of the data-dependent scores and the uniforms, so the
     extension is routine but must be stated.
   - *Also:* list MEAS-J and "final streams ⫫ (data, streams 0–9)" in the proposed registry premises
     (`X5_POOLZ/STATEMENT.md:33-34`). The equality E[1_𝒜Ẑ] = E[1_𝒜Z] holds in [0, ∞], because both sides are
     nonnegative; no integrability is needed. Say so.
2. **F — wrong line range for the PoolZ proof** (`X5_POOLZ/PROOF.md:3`). The proof in W3-READER `STATEMENT.md` is at
   lines 25–33, not 23–31 (the claim is at :21-23). Fix the range.
3. **E/S — (X5-b) names the wrong failing premise** (`X5_POOLZ/STATEMENT.md:24-26`; `PROOF.md:20-21`). For the actual
   record, 𝒜 *is* in σ(actual 𝓒), because the status is a statistical field (T1's cut rule) and 𝒜 = {status "ok"}. What
   fails is CAL: the actual 𝓒 depends on the clock through the Booleans, so it is not a function of the data and
   streams 0–9.

   So N1's 𝓒 must be read as 𝓒°, and then 𝒜 ∈ σ(𝓒°) forces 𝒜°. The conclusion and the recommended wording ("almost
   surely on 𝒜°") are unchanged. Fix: "N1's conditioning needs 𝓒 to satisfy CAL; only 𝓒° does, and 𝒜 ∈ σ(𝓒°) holds for
   𝒜°, not for 𝒜 = 𝒜° ∩ G".
4. **S — the sufficient condition for the clock is too weak** (`X5_POOLZ/PROOF.md:22-24`). The parenthetical "a function
   of the calibration's own execution and of noise independent of streams 10–13" is not enough. The noise must be
   independent of streams 10–13 *jointly with* (data, streams 0–9). Only then does U_final ⫫ (𝓒°, G) hold, and that is
   what E[Ẑ° | 𝓒°, G] = E[Ẑ° | 𝓒°] uses. Pairwise independence of the noise and U_final does not give it. Fix: state the
   joint independence.

---

LC2-VERDICT: X1=VERIFIED WITH AMENDMENTS; X3=VERIFIED WITH AMENDMENTS; X5=VERIFIED WITH AMENDMENTS
