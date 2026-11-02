# CLAIMS_OF_FATAL_FLAWS — T11(iii)

Every fatal or gap finding, copied verbatim, with the lead's answer.

## Stage A, round 1 — Astra #1 (session 01a1641a-4997-7370-a99a-43d4f2a4f245), review of PROOF_v1 (verdict: verified)

### A1-F1 (gap)

> **Finding 1**
> 
> 1. **Location:** Section 2, sampler definitions and final equality in Lemma \(\ref{lem:sampler}\).
> 2. **Severity:** **gap** — confined to the supplementary sampler verification.
> 3. **Claim:** The identification of the displayed sampler distribution with \(\pi_0\) is not established from the supplied setting.
> 4. **Evidence:** The setting does not define \(w(k)\), \(W_K\), or the product representation
>    \[
>    \gamma_0(S)=\frac{w(|S|)}{W_K}\prod_b r_b(S\cap C_b).
>    \]
>    Nor does it explicitly supply positivity of every table entry. The algebra is correct given these additional facts, but their applicability is unverified. This does not undermine Claim (iii), because EX-A already supplies sampler exactness.
> 

**Lead's answer: accepted and fixed.** The packet's STATEMENT.md did not carry the definitions of w, W_K, ϖ, γ₀ and the
positivity of the tables, which the sampler verification uses. Change: Setting item 1 of STATEMENT.md now lists these
definitions (taken from 00_COMMON §§1–2 and METHODOLOGY §5, §6.3: w(k) = ½/C(2p−1,k) > 0, W_K = Σ_{k≤K}C(p,k)w(k),
ϖ(S) = w(|S|)/W_K, r_b(U) = m(U)/m(∅) > 0, γ₀(S) = ϖ(S)∏_b r_b(S∩C_b)); these are definitions, not new hypotheses.
PROOF_v2 §2 states that the verification uses exactly these. As the finding notes, the main claim uses only the
exactness in Setting item 3.

### A1-F2 (gap)

> **Finding 2**
> 
> 1. **Location:** Section 3, Remark \(\ref{rem:full}\).
> 2. **Severity:** **gap** — confined to the supplementary implementation justification.
> 3. **Claim:** The assertions about all possible interruption statuses and all matrices factorised cannot be verified from the supplied files.
> 4. **Evidence:** The setting does not specify the cited failure mechanisms or matrix inventory. Positive definiteness follows for the displayed matrices, but their exhaustiveness is unsupported here. Full execution is already stipulated by Setting item 5, so the main proof does not require these assertions.
> 

**Lead's answer: accepted and fixed.** STATEMENT.md now has a section "Method facts quoted verbatim" (statuses of §2,
the §7 pseudocode, §6.13's failure path). Remark 4 of PROOF_v2 ("the final run executes in full") is rewritten: it says the main proof uses Setting item 5
as stated and only explains why item 5 is the method's specification. The argument no longer relies on an inventory of
factorised matrices: `numerical_failure` is "scoring failed after the fallback", and under EX-A scores are computed
exactly, so scoring does not fail; the positive-definiteness of H_S and G_S + I is kept only as an illustration.

### A1-F3 (gap)

> **Finding 3**
> 
> 1. **Location:** Final corollary, “scoring; beyond the stated part.”
> 2. **Severity:** **gap**.
> 3. **Claim:** The scoring conclusion requires implementation facts absent from Setting items 1–6.
> 4. **Evidence:** Those items specify initial draws and independence proposals, but do not require every proposal’s score to be computed or specify the stage-1 weighting calculation. The corollary invokes unavailable methodology sections for those premises. Its set-inclusion argument is valid if the premises hold; the premises remain unverified. This corollary is explicitly outside Claim (iii).
> 

**Lead's answer: accepted and fixed.** The premises are now quoted verbatim in STATEMENT.md (§6.5: "Every proposal is
scored, accepted or not."; §6.12: the evidence product, whose t = 1 factor contains d(S_i^{(0)}), which involves
log m(S_i^{(0)})). The corollary in PROOF_v2 cites these quotes. It remains labelled as beyond the stated part (iii).

## Stage A, round 2 — Astra #1 rulings on round-1 answers and review of PROOF_v2 (verdict: verified)

Rulings (verbatim):

> **Rulings on the three previous findings**
> 
> 1. **A1-F1 — sampler definitions: agree; the fix works.** Updated Setting item 1 supplies positivity of the tables, the size-prior normalisation, and the product formula for \(\gamma_0\). These justify \(M=W_K\bar Z_0\) and the sampler proof’s final identification with \(\pi_0\).
> 
> 2. **A1-F2 — full execution: agree with the substantive answer; the fix works for the main argument.** The proof explicitly takes full execution from Setting item 5. The supplied quotations support the timing of preflight and schedule failures and identify the scoring-failure status. The argument no longer requires an exhaustive matrix inventory. One illustrative implementation assertion remains unsupported; see Finding 1 below.
> 
> 3. **A1-F3 — scoring: partially agree; the fix is incomplete.** The new quotation establishes that every independence proposal is scored. However, the evidence-product formula does not, by itself, establish that each initial draw’s \(\log m(S)\) is computed during the final run. See Finding 2 below.
> 

### A1-R2-F2 (gap; outside Claim (iii))

> **Finding 2**
> 
> 1. **Location:** Final scoring corollary, assertion that each initial draw is scored “by the evidence product.”
> 2. **Severity:** **gap** — outside Claim (iii).
> 3. **Claim:** An expression containing \(d(S)\) does not necessarily require computing \(\log m(S)\) during the final run.
> 4. **Evidence:** Consider the permitted case of one block, \(C_1=[p]\). Then
>    \[
>    r_1(S)=m(S)/m(\emptyset),\qquad
>    d(S)=\log\!\frac{m(S)}{m(\emptyset)}-\log r_1(S)=0.
>    \]
>    Thus every evidence-product factor can be evaluated as \(1\) without computing an initial model’s score during that run. The quoted formula is compatible with this evaluation, while the explicit scoring instruction covers proposals only.
> 
>    Consequently, the quotations do not establish that the event “\(S^*\) is not scored” is contained in the event “\(S^*\) is absent from all initial draws and proposals.” The main absence theorem remains valid.
> 

**Lead's answer: accepted and fixed.** The quoted method text guarantees scoring only for the independence proposals.
PROOF_v3's corollary now uses the proposals alone: each of the Q_p = 4N_e(T+L+4) final proposals is scored (§6.5 quote),
they are iid π₀ given the calibration streams (Proposition 5) and Q_p is 𝓒-measurable, so
P(S* not scored in the final run | 𝓒) ≤ (1 − π₀(S*))^{Q_p} on Λ; the exponent Q_f is stated only conditionally on the
initial draws also being scored. The §6.12 quote was removed from STATEMENT.md (no longer used). Claim (iii) itself is
unaffected (Astra agrees).

Exposition findings of round 2 (not fatal/gap; handled in PROOF_v3): Finding 1 (matrix example in Remark 4 unsupported)
— parenthetical removed. Finding 3 (σ(𝓒) "not independent" of calibration streams too categorical) — reworded to
"in general not ... (𝓒 is computed from them)".

## Stage A, round 3 — Astra #1 rulings and review of PROOF_v3 (verdict: verified; no new findings). Stage A closed: lead and Astra #1 both hold PROOF_v3 correct.

> **Rulings on the author’s responses**
> 
> 1. **Round-2 Finding 2 — scoring gap: agree; the fix works.** The revised corollary uses only the \(Q_p=4N_e(T+L+4)\) independence proposals, which the quoted method text explicitly requires to be scored. Their absence probability gives the stated upper bound on the probability of not being scored. The stronger exponent \(Q_f\) is now explicitly conditional on the initial draws also being scored. Removing the unused §6.12 quotation is consistent with this change.
> 
> 2. **Round-2 Finding 1 — unsupported matrix illustration: agree; the fix works.** The parenthetical implementation assertion has been removed. The main proof continues to use full execution as stipulated by Setting item 5.
> 
> 3. **Round-2 Finding 3 — categorical non-independence: agree; the fix works.** “In general not” correctly allows degenerate cases, including constant calibration output, while explaining why independence from calibration randomness is not guaranteed.
> 

## Stage B, round 1 — Astra #2 (session 01a16421-b0ef-7281-984e-2af293f78cf1): verified, no findings. Opus 5.5 xhigh reviewer: verified, no fatal findings, one gap (F8, outside (iii)) and seven exposition findings. All addressed in PROOF_v4.

### OB-F8 (gap; Corollary 9, outside Claim (iii)) — Opus reviewer

> **F8**
> - **Location:** Corollary 9, lines 211–218. This is outside claim (iii).
> - **Severity:** gap (in the corollary only; it does not affect the verdict on (iii)).
> - **Claim:** The step "by Proposition 5 they [the proposals alone] are iid π₀ given Υ" does not follow from Proposition 5 as stated.
> - **Evidence:**
>   - Proposition 5 proves that the chronologically numbered D_1..D_{Q_f} are iid. The proposals are a sub-family whose positions in that order may depend on Ξ: item 2 lets the order of operations depend on the values read so far, for example through how the islands are interleaved.
>   - A sub-family chosen with data-dependent positions is not iid in general. For example, with D_1, D_2 iid, choosing D_1 if D_1 = s and D_2 otherwise does not give a π₀-distributed result.
>   - The corollary can be repaired by rerunning Proposition 5's stopping-time argument over proposal calls only. Whether a call is a proposal is decided at its start, so that event is 𝓕_{τ_m}-measurable. As written, though, the citation does not supply this.
> 

**Lead's answer: accepted and fixed.** Proposition 5 is restated in PROOF_v4 for any class of *designated* sampler calls
(membership decided by the run's state when the call starts) with a constant number Q of calls; its stopping-time
argument is run over the designated calls only, exactly as the reviewer suggests ({m-th designated call starts after
read t} ∈ 𝓕_t). Parts (a) (all final draws, Q = Q_f) and (b) (independence proposals alone, Q = Q_p) are stated
explicitly; Theorem 6 cites (a) and Corollary 9 cites (b).

Exposition findings (not fatal/gap), handled in PROOF_v4 / STATEMENT.md:
- F1 (constant 0 outside (0,1)): replacement constant is now 1/2.
- F2 (𝓕_τ, τ = ∞): 𝓕_τ now requires A ∈ σ(V); V_{τ+j} := 1/2 on the null set {τ = ∞}.
- F3 (finiteness of τ_m): now justified by item 5 (the m-th designated call occurs) and item 2 (one operation at a time).
- F4 (other sampler calls): covered by the designated-call formulation.
- F5 (single map G): the proof now allows a state-dependent map G_{Z_m} with Z_m 𝓕_{τ_m}-measurable, and Setting item 3
  is worded accordingly (measurable map, possibly state-dependent; exact law π₀ on iid uniform input); the step uses
  Lemma 2 plus Fubini.
- F6: "exactly one path of positive probability".
- F7 (Remark 4): the remark now notes m(S) is finite and positive (item 1) and that environment-imposed aborts are
  outside the idealised model; Setting item 5 now says explicitly that a launched final run executes all its rounds,
  and the "Statement changes" paragraph says item 5 transcribes the method's specification.
- Setting item 6 faithfulness: STATEMENT.md now quotes the theorem file's own definition of S* ("Fix S* ∈ Ω measurable
  w.r.t. data and 𝓒 (before final randomness)").

## Stage B, round 2 — rulings on PROOF_v4

- Astra #2: agrees with every logged answer (A1-F1, A1-F2, A1-F3 as resolved by v4, A1-R2-F2, OB-F8) and with the
  handling of all exposition items; no new findings; **VERDICT: verified** (review/astra2_stageB_round2_review.md).
- Opus reviewer: agrees with every logged answer; OB-F8 closed by Proposition 5(b); F1–F7 and the item-6 concern
  adequately handled; four new exposition findings N1–N4, no fatal or gap; **VERDICT: verified**
  (review/opus_stageB_round2_review.md).
- No open fatal or gap claim. Exposition N1–N4 handled in PROOF_v5 (diff against v4 is exposition only):
  N1 "A = Ω" (clash with the model space) → "A the whole sample space"; N2 Section 2 paraphrase of item 3 updated to the
  reworded item 3; N3 joint measurability of (z, w) ↦ G_z(w) written out (state = history in ⊔_t [0,1]^t; the run is a
  Borel function of the values read, Setting item 2); N4 Remark 4 now states the reading of EX-A it uses ("every score
  computation returns log m(S) exactly").

## Stage B, round 3 — confirmation of PROOF_v5 (final)

- Astra #2: v5 differs from v4 only at N1–N4 (plus title); N3 measurability argument correct; no findings;
  **VERDICT: verified** (review/astra2_stageB_round3_review.md).
- Opus reviewer: same diff check; N3 correct step by step; one exposition note E1 ("for every z" is slightly broader
  than needed: G_z is only defined at histories where a call starts; harmless, "no change is required");
  **VERDICT: verified** (review/opus_stageB_round3_review.md). Lead: E1 noted, no change (the Fubini step evaluates
  G_z only at Z_m, where it is defined).
- Final state: no open fatal or gap claim; all three reviewers (Astra #1, Astra #2, Opus xhigh) hold the proof correct;
  no Astra judge needed.
