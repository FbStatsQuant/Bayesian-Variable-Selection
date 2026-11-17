# X1 · Lemma FR — PROOF v1 (re-check of T12 PROOF_v6 §§1–3, 5 and of W1-N1:B at the pin)

T12 = `Docs/Theory/proofs/T12_T8_frozen_run_identities/`; code paths relative to `Scripts/SMC_BVS/core/` (pin 4676af6).
Notation as in T12 STATEMENT §§0–2: γ_φ = γ₀e^{φd}, Z̄_φ = Σ_Ω γ_φ, q_φ = γ_φ/Z̄_φ, Z_t = m(∅)Z̄_{φ_t}, G_t = e^{Δ_t d},
J_j = {S ∈ Ω : j ∈ S}.

## Part 1 — (FR-a): the coded island is I(c) with (R1)–(R3)
`W1-N1:B` proves (B-a) structure and (B-b) randomness for the v2.2.1 core
(`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:33-43`, proof `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:45-110`), status
"PROVED under the named premises … council-passed". `W3-SAMP:CC` ("CODE-CHECKED") records that at the pin
`run_island_s` differs from v2.2.1 only by the removed write-only plain-PIP lines, and that the elementary steps, the
round, resampling and `draw_start` are byte-identical up to line shifts
(`Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md:9-21`). I re-read each step of (B-a)/(B-b) at the pin:
- Initial draws: `init_states = nullptr` (`cpp/v3_core.cpp:446`) ⇒ `draw_start` = `draw_pi0` (`cpp/v3_engine.h:286-292, 108`).
- log Ẑ starts at log m(∅) + log Z̄₀ (`cpp/v3_engine.h:299`; T6 (Z)), i.e. Ẑ₀ = Z₀ = m(∅)Z̄₀.
- Stage loop (`cpp/v3_engine.h:303-339`), fixed grid (`run_island`, `cpp/v3_engine.h:269-273`; T = grid size − 1,
  `cpp/v3_engine.h:280`): φ_{t−1}, φ_t from the grid (`cpp/v3_engine.h:306-308`); lw_i = Δ_t·d(S_i) (`cpp/v3_engine.h:317`);
  inc_t = LSE(lw) − log N = log((1/N)Σ_i G_t(S_i)) under EX-A (`cpp/v3_engine.h:318-319`), added to log Ẑ
  (`cpp/v3_engine.h:322`); ancestors `resample(lw)` and copy (`cpp/v3_engine.h:324-327`); one `population_round` at φ_t
  (`cpp/v3_engine.h:331`). No round before the first reweighting (flag unset).
- After the loop: L rounds at φ = 1 (`cpp/v3_engine.h:343-347`), then Hm = 4 measured rounds at φ = 1
  (`cpp/v3_engine.h:351-360`; `measured_rounds = 4L`, `v3_run.R:90`); no resampling after stage T. So L′ = L, M = 4.
- d and γ_φ are T12's: `eval` sets `lg0` = log ϖ(|S|) + Σ_b log r_b and `d` = (log m − log m(∅)) − Σ_b log r_b
  (`cpp/v3_engine.h:95-97`), `lgphi(φ) = lg0 + φ·d` (`cpp/v3_engine.h:14`).
- (B-0) the statistical record is a function of (c, u): scores through `eval` are exact whatever the cache history (T7
  Step 0: `find` compares the full set, `cpp/v3_score.h:274-282`); the ledger and the clock/guard feed no transition (T1
  GW-i); `rb_acc` is write-only within the island and reset before the measured rounds (`cpp/v3_engine.h:350`).
- (R1): each `draw_pi0` call reads fresh uniforms (stopping-time argument of `W1-N1:B` (B-b), as in `W3-SAMP:CC` CC4) and
  has law π₀ (T6 (S)); so the N_e initial draws are iid π₀.
- (R2): `resample` (`cpp/v3_engine.h:234-259`) reads N fresh uniforms; for u_i > 0 it returns the smallest k with
  W_k ≥ u_i (`cpp/v3_engine.h:243-256`; W_{N−1} := 1 at `cpp/v3_engine.h:240`), so P(a_i = k | past) = w_k/Σ_l w_l, and the
  a_i are conditionally iid (disjoint fresh uniforms); u_i = 0 has probability 0.
- (R3): `population_round` runs `one_round` for i = 1..N in turn (`cpp/v3_engine.h:215-218`); `one_round` draws the order
  first (`cpp/v3_engine.h:203`), uniform and state-independent (T7 KER-c), then applies the steps, each the T12 kernel of its
  label with fresh uniforms (T7 KER-a). The chain-rule argument of `W1-N1:B` (B-b)
  (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:95-107`) gives the product form of the conditional law of the N pairs
  (order, path) given the σ-field before the round. It uses only the facts just listed, all unchanged at the pin.
Hence (FR-a).

## Part 2 — (FR-b), (FR-c): line check of T12 PROOF_v6
Each lemma is re-derived; agreement with PROOF_v6 is noted.

*Bridge identity* (PROOF_v6 Lemma 1.1, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:42-54`). γ_φ > 0 on
the finite Ω, so Z̄_φ ∈ (0, ∞). q_{t−1}(x)G_t(x) = γ₀(x)e^{φ_{t−1}d(x)}e^{Δ_t d(x)}/Z̄_{φ_{t−1}} = γ_{φ_t}(x)/Z̄_{φ_{t−1}}, so
Z_{t−1}q_{t−1}(G_t h) = m(∅)Σ_x γ_{φ_t}(x)h(x) = Z_t q_t(h). γ₀e^{d} = ϖ·m/m(∅), so m(∅)Z̄₁ = Σ_Ω ϖm = Z. Agrees.

*Invariance* (Lemma 1.2, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:56-77`): each elementary kernel is
q_φ-reversible — this is T7 (KER-b), re-derived independently there; PROOF_v6's four computations agree with T7's.

*Prefixes* (Lemma 1.3, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:79-87`): P_κ := (1/m!)Σ_σ
K_{σ(1)}⋯K_{σ(κ(σ))} is an average of products of q_φ-invariant kernels, hence q_φP_κ = q_φ. The Gibbs-j step ends in
J_j exactly when it moves to S⁺, with probability o_j(S, φ) (0 when |S⁺| > K), so K_{g_j}1_{J_j} = o_j(·, φ) and
q_φ(o_j) = (q_φK_{g_j})(1_{J_j}) = q_φ(J_j). Agrees.

*Resampling mean* (Lemma 2.1, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:100-106`): given 𝓕,
E[h(X^{A^i}) | 𝓕] = Σ_k h(X^k)w^k/Σ_l w^l; multiplying by the 𝓕-measurable (1/N)Σ_l w^l and averaging over i gives
(1/N)Σ_k G(X^k)h(X^k). Agrees.

*Round mean* (Lemma 2.2, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:108-113`): by (R3), given 𝓗 and
σ_i = σ the path is Markov from X̃^i with kernels K_{σ(1)}, …, so E[f(X^i_{[κ(σ)]}) | 𝓗, σ_i = σ] =
(K_{σ(1)}⋯K_{σ(κ(σ))}f)(X̃^i); σ_i uniform and independent of 𝓗 gives (P_κ f)(X̃^i). Agrees.

*Claims C_t* (§3, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:115-128`). t = 0: Ẑ₀ = Z₀ deterministic,
X₀^i iid π₀ = q₀ (φ₀ = 0), so E[Ẑ₀(1/N)Σ_i h(X₀^i)] = Z₀q₀(h); flag unset ⇒ X^{(0)} = X₀. t − 1 → t: Ẑ_t = Ẑ_{t−1}(1/N)Σ_l w^l
with w^l = G_t(X^{(t−1),l}) and Ẑ_{t−1} 𝓕-measurable; the resampling mean gives E[Ẑ_t (1/N)Σ_i h(X̃^{(t),i}) | 𝓕] =
Ẑ_{t−1}(1/N)Σ_k (G_t h)(X^{(t−1),k}); C_{t−1}(b) with G_t h and the bridge identity give Z_t q_t(h) (part (a)). For the
stage-t round with prefix κ, Ẑ_t is 𝓗-measurable and the round mean gives E[… | 𝓗] = Ẑ_t(1/N)Σ_i (P_κ f)(X̃^{(t),i});
part (a) with h = P_κ f and prefix invariance give Z_t q_t(P_κ f) = Z_t q_t(f) (part (c)); κ ≡ m gives (b). With t = T,
h ≡ 1: E Ẑ = Z_T = Z. Agrees.

*Post-terminal* (`Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:130`): induction over the L + 4 rounds at
φ = 1, each step the round mean plus prefix invariance at φ = 1 (q₁ = π), starting from C_T(b) with q_T = π. (The code has
no unit-weight resamplings, a case T12 also covers.) Agrees. This is (FR-b).

*(ii)* (§5, `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:145-153`). In measured round u, the code
records o_j at the state immediately before particle i's Gibbs-j step (`cpp/v3_engine.h:128`, `rb_on` only in measured
rounds, `cpp/v3_engine.h:354-356`; T7 KER-a: this value is o_j(S, 1)); that state is X^i_{[κ_j(σ_i)]} with
κ_j(σ) = σ⁻¹(g_j) − 1, a function of the order alone. (FR-b)'s prefix clause with f = o_j(·, 1) and q₁ = π gives
E[Ẑ (1/N)Σ_i o_j(Y^i_{u,j}, 1)] = Z π(o_j(·, 1)) = Z π(J_j) = Z·PIP_j. Averaging over u = 1..4 and dividing as the code does
(`res.pip[j] = rb_acc[j]/(N·Hm)`, `cpp/v3_engine.h:364`) gives (FR-c). Agrees. ∎

## Re-check verdict on T12 (i.a)–(i.c), (ii)
No error found in PROOF_v6 §§1–3, 5. The only change at the pin is the removal of the plain-PIP accumulator, which T12
never used (its (ii) is the Rao–Blackwell record). With this check the T12 inputs of rows 3.5 and 3.6 rest on a
re-check under PROTOCOL_v4 rather than on the PROVED-LOCKED label alone (the label change is the recorder's).
