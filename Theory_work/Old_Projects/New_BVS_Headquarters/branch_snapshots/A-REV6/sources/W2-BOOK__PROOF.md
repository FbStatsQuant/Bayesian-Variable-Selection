# W2-BOOK — PROOF.md: proofs of the restated bookkeeping statements

Run of 2026-11-02, branch `theory/W2-BOOK`. **Nothing here has been reviewed.** Each PROVED below is a candidate:
I checked it line by line, but it is not adopted, and it still needs cross-family review. Notation follows
`Docs/Theory/theorems/00_COMMON.md` and the locked STATEMENT.md files. New symbols are defined where they first appear.

Locked inputs I cite (all PROVED-LOCKED in `Docs/Theory/proofs/LOCKED_PROOFS.md`, not adopted):
- T12 (i)–(iv): `COLLECTED_PROOFS_v2.tex` chapter T12, lines 1119–1503.
- T31(i): the same file, chapter T31, lines 4497 onward.
- T11(iii), T14(i), T15, T23(ii): the same file.
- T21 (C1, routes (a)–(f)): `T21_T14H_HPM_composition/PROOF_v3.tex`.
- T25(iv): `T25iv_T19_crossing_evidence/PROOF_v2.tex`.
- T06/T07: `T06_T07_identifiability_size_prior/PROOF_v2.tex`.

Imported unreviewed input: **Theorem B** and its Corollaries B-unif and B-M, from branch `theory/W1-T24G`
(`theory_campaign/W1-T24G/REPORT.md` §1 and §5, `PROOF.md` §4). They are PROVED (candidate) there and not reviewed.
Anything below that uses them inherits that status.

---

## 0. The run/output split

### 0.1 Objects

The probability space carries three things:
- the data, with law P₀;
- the ideal streams U₀, …, U₁₃ of EX-S, independent of the data;
- an **operational element** Ξ: the allocation, wall-clock readings, hardware and load.

**No independence between Ξ and the streams is assumed.** Wall time depends on which models the particles visit,
because the cost of a score grows with |S|. So Ξ depends on the final-run path.

**Definition (potential uninterrupted run).** R̄ = Ψ(data, U₀, …, U₁₃) is the record that the method's algorithm
produces under EX-A when the preflight and the in-run time guard are removed (infinite allocation). R̄ contains:
- the calibration 𝓒 and its success event 𝒜 ∈ σ(𝓒);
- on 𝒜, the final island records O_r = Φ(𝓒, U_{9+r}), r = 1, …, 4;
- the final local search, the scored set 𝒮̄ ⊇ 𝒮_cal, the HPM Ŝ̄ (total order of 00_COMMON §1 over 𝒮̄), Ẑ̄_r, Ẑ̄,
  PIP̂̄_{rj}, P̄̄_j and MPM̂̄;
- the potential status st̄ ∈ {exact, completed, schedule_limit}.

  Under EX-A, `numerical_failure` does not occur, and a valid input excludes y_constant, no_predictors and
  invalid_input. In what follows a bar marks a potential-run quantity. Where no ambiguity arises, Ẑ_r and PIP̂_{rj}
  with no bar also mean the potential-run quantities. This is the reading of every locked statement (§2).

**Actual execution.** The status st and the reported outputs are functions of (R̄, Ξ).

**Stop event.** 𝒢 := {st = resource_limit}. It includes preflight stops and in-run guard stops at any checkpoint.

**Output-available events.**
- Evidence and PIP outputs: 𝒪_E := {st ∈ {exact, completed}}.
- HPM output: 𝒪_H := U^c, where U is the event that no usable HPM is reported (T21's U).
- Study convention (D61): a stopped fit counts as no output, so 𝒢 ⊆ U. On 𝒜^c, `schedule_limit` returns the best
  scored model, and whether that counts as usable is a convention. Write Ū for the potential-run part, a function of
  R̄ alone, so that U = 𝒢 ∪ (𝒢^c ∩ Ū).

**Hypothesis GUARD (stop-only coupling).** On 𝒢^c, st = st̄, and every reported output equals the corresponding
component of R̄.

*Basis for GUARD.* It is an implementation fact, read from the code on 2026-11-02. It is not a theorem.
- `Scripts/SMC_BVS/core/cpp/v3_runtime.h`: `RuntimeGuard::check` reads `std::chrono::steady_clock` only. It consumes
  no random number and changes no setting.
- `v3_engine.h` (around line 335): the check runs after every bridge stage of an island. On a stop, the island returns
  `partial`.
- `v3_core.cpp` `cpp_final_run`: the islands run sequentially, island r on `seed_stream(seed, 9+r)`. A partial island
  sets `resource_limit`. After the four islands and the final local search there is one more check, and a stop there
  also sets `resource_limit`.
- The preflight reads (n, p, K, N_e, allocation) and, on the exact branch, a timing measurement. It reads no stream.

On 𝒢^c no check fired, so the computation is the uninterrupted one. A same-seed replay at a larger allocation (the
D61 reproduction spot-check) is the empirical test of GUARD: on completed fits it should give bitwise-identical
outputs.

**Finality.** GUARD says nothing about the law of 𝒢 given R̄. That law is unknown and design dependent.

### 0.2 Lemma RO (transfer without conditioning). PROVED.

Assume GUARD. Let 𝒪 ∈ {𝒪_E, 𝒪_H}, and let 𝒪̄ ∈ σ(R̄) be its potential counterpart: {st̄ ∈ {exact, completed}},
or Ū^c. Then 𝒪 = 𝒢^c ∩ 𝒪̄ ⊆ 𝒪̄. Let g be a reported output (or a measurable function of reported outputs) and ḡ
its potential version.
1. 1_𝒪 g = 1_𝒪 ḡ pointwise.
2. For every set A of output values: 𝒪 ∩ {g ∈ A} ⊆ 𝒪̄ ∩ {ḡ ∈ A}. Hence P(𝒪, g ∈ A) ≤ P(𝒪̄, ḡ ∈ A), and
   P(𝒪^c ∪ {g ∉ A}) ≤ P(𝒢) + P(𝒪̄^c) + P(𝒪̄, ḡ ∉ A).
3. If g ≥ 0, then E[1_𝒪 g] ≤ E[1_{𝒪̄} ḡ]. If 0 ≤ g ≤ b, then E[1_{𝒪̄} ḡ] − E[1_𝒪 g] ≤ b·P(𝒢 ∩ 𝒪̄).
4. If P(𝒪̄, ḡ ∈ A) ≤ ε, then P(g ∈ A | 𝒪) ≤ ε / P(𝒪).
5. (Limit, COUNTEREXAMPLE, §0.3.) E[ḡ | 𝒪] = E[ḡ | 𝒪̄] does not follow, even when P(𝒢) is small. Identities of
   expectation are not preserved by conditioning on 𝒪.

*Proof.*
1. 𝒪 ⊆ 𝒢^c, and on 𝒢^c GUARD gives g = ḡ.
2. On 𝒪 we have 𝒢^c, so st = st̄ and 𝒪̄ holds, and g = ḡ by item 1. This gives the inclusion, and the first
   inequality follows by monotonicity. For the second, 𝒪^c = 𝒢 ∪ (𝒢^c ∩ 𝒪̄^c) ⊆ 𝒢 ∪ 𝒪̄^c, and
   𝒪 ∩ {g ∉ A} ⊆ 𝒪̄ ∩ {ḡ ∉ A}. Take a union bound.
3. By item 1, 1_𝒪 g = 1_𝒪 ḡ ≤ 1_{𝒪̄} ḡ when ḡ ≥ 0. The difference is 1_{𝒪̄ ∖ 𝒪} ḡ, where 𝒪̄ ∖ 𝒪 = 𝒪̄ ∩ 𝒢,
   and 0 ≤ ḡ ≤ b.
4. Divide the first inequality of item 2 by P(𝒪).
5. See §0.3. ∎

### 0.3 COUNTEREXAMPLE: conditioning on completion breaks unbiasedness

This is `scripts/frozen_run_exact.py`, log in `results/frozen_run_exact.txt`. It is exact enumeration at 50 digits,
not Monte Carlo.

**Instance.** The T12(iv.b) component instance:
- n = 20, p = 2, with the appendix data of the T12 STATEMENT;
- T = 1, N = 1, L′ = L = 5, M = 4, flag unset.

Its scope is that of T12(iv.b). The full method would take the exact branch at p = 2, and N = 1 is not a production
budget.

**Stylised guard.**
- The cost of scoring a model of size k is 1 + k³ units.
- Under SR, a Gibbs step scores both configurations, a swap scores its proposal, and an independence step scores its
  proposal. The stage-0 start draw is also scored.
- The guard is checked after the stage-1 bridge stage, as in the engine.
- The output is available iff the accumulated cost is at most h.

Then Ẑ/Z₀ = e^{D·B} with B = 1{X₀ = {1,2}} and D = 8.1468, and the run that would take the big model (the large
weight) is also the expensive run.

| h | P(𝒪_h) | E[Ẑ \| 𝒪_h]/Z | E[Ẑ·PIP̂₁ \| 𝒪_h]/(Z·PIP₁) |
|---|---|---|---|
| 8 | 0.5468 | 0.0103 | 0.0079 |
| 30 | 0.9614 | 0.0112 | 0.0091 |
| 32 | 0.9907 | 0.7978 | 0.7975 |
| 33 | 0.99783 | 0.9739 | 0.9739 |
| 40 | 0.9999995 | 0.99998 | 0.99998 |

At h = 33 the guard stops 0.22% of runs, close to the 0.25% observed in PROD-H. Yet the output-conditional evidence
is 2.6% low. At h = 32, 0.9% of stops give 20% bias.

**Mechanism.** The identity E[Ẑ] = Z is carried by rare, high-weight paths, and those are the expensive ones.

Status: **COUNTEREXAMPLE** in a stylised cost model. That the guard depends on the final path is a fact about the
engine (§0.1). The specific cost function is an assumption of the example.

---

## 1. Proposition 2 (restated T12 + T31(i))

**Setting.**
- A valid input on the SMC branch.
- EX-A, START (T09(i)), EX-S, CAL. CAL is read with the frozen object
  𝓒 = (tier e, grid φ₀ < … < φ_T, T, N_e, L, M = 4, island count 4, ℓ, inherited calibration score leaders, and every
  other setting the final run reads).
- 𝓒 is a function of the data and streams 0–9. Escalation is decided before stream 10 is read.
- The allocation, the clock and the guard state are **not** components of 𝓒; they belong to Ξ.
- All hatted quantities are those of R̄.
- Pooled island product: Π̂_j := ¼ Σ_r Ẑ_r PIP̂_{rj}. Primary PIP: P̄_j := ¼ Σ_r PIP̂_{rj}.

**Claims.** Given 𝓒 on 𝒜, for every r and j:
- (a) E[Ẑ_r | 𝓒] = Z and E[Ẑ_r PIP̂_{rj} | 𝓒] = Z·PIP_j.
- (b) E[Ẑ | 𝓒] = Z and E[Π̂_j | 𝓒] = Z·PIP_j.
- (c) E[Ẑ·P̄_j | 𝓒] = Z·PIP_j − ¾·Cov(PIP̂_{1j}, Ẑ₁ | 𝓒) = Z·{PIP_j + ¾(E[P̄_j | 𝓒] − PIP_j)}.
  In the T12(iv.b) component instance, E[Ẑ·P̄₁] − Z·PIP₁ < −0.1275·Z, so pooled × pooled is not an identity.
- (d) For 0 < α < 1: P(Z ≥ αẐ | 𝓒) ≥ 1 − α and P(Z ≥ αẐ_r | 𝓒) ≥ 1 − α; E[log Ẑ | 𝓒] ≤ log Z and
  E[log Ẑ_r | 𝓒] ≤ log Z.
- (e) Under GUARD, for the reported Ẑ^rep:
  - (e1) P(𝒪_E ∩ {αẐ^rep > Z}) ≤ α·P(𝒜) ≤ α;
  - (e2) E[1_{𝒪_E} Ẑ^rep] ≤ Z·P(𝒜);
  - (e3) P(αẐ^rep > Z | 𝒪_E) ≤ α·P(𝒜)/P(𝒪_E).
  E[Ẑ^rep | 𝒪_E] = Z is not claimed, and it is false in general (§0.3).
- (f) Under GUARD and VAL-FP(η, ε): P(𝒪_E ∩ {αẐ^fp > Z}) ≤ α·e^η·P(𝒜) + ε.

**VAL-FP(η, ε)** (new code, a validation contract). There is an event G_fp with P(𝒪_E ∖ G_fp) ≤ ε, on which the
floating-point value Ẑ^fp and the exact-arithmetic value Ẑ̄ on the same streams satisfy |log Ẑ^fp − log Ẑ̄| ≤ η.
A sufficient condition on G_fp is that the floating-point and exact runs make the same discrete decisions (accepts,
Gibbs draws, resampling ancestors, sampler branches) and the evidence recursion is accurate to η.

**Proofs.**
- (a) T12(iii), locked: E[Ẑ_{r,T} q̂_{r,T}(1) | 𝓒] = Z_T = Z and E[Ẑ_r PIP̂_{rj} | 𝓒] = Z·PIP_j. These are stated for
  the islands O_r = Φ(𝓒, U_{9+r}), which are exactly the potential-run islands.
- (b) Linearity applied to (a).
- (c) Write E_𝓒 for E[· | 𝓒] and μ_j := E_𝓒 PIP̂_{1j}. By T12(iv.c), locked, the islands are independent given 𝓒,
  each with the law of I(𝓒), so E_𝓒 PIP̂_{rj} = μ_j and E_𝓒 Ẑ_r = Z for every r. Then
  E_𝓒[Ẑ·P̄_j] = (1/16)Σ_{r,s} E_𝓒[Ẑ_r PIP̂_{sj}].
  - The 4 diagonal terms each equal Z·PIP_j, by (a).
  - The 12 off-diagonal terms factorise by conditional independence, each to Z·μ_j.
  - So E_𝓒[Ẑ·P̄_j] = (Z/16)(4·PIP_j + 12·μ_j) = Z·PIP_j + ¾·Z(μ_j − PIP_j).
  - T12(iv.b), locked, gives μ_j − PIP_j = E_𝓒 P̄_j − PIP_j = −Cov(PIP̂_{1j}, Ẑ₁ | 𝓒)/Z. This proves both forms.
  - For the instance, T12(iv.b) certifies E[P̄₁] − PIP₁ < −0.17, so E[Ẑ·P̄₁] − Z·PIP₁ < −0.1275·Z.
  - The script reproduces the locked value −0.173974177850 independently. It also evaluates the 4-island product by
    direct enumeration, giving a relative bias of −0.13172, which agrees with the closed form to 10⁻⁴⁹.
  - With I islands the factor ¾ becomes (I − 1)/I.
- (d) T12(iii), locked; equivalently T31(i)(a)–(b), with H-T12 discharged by T12(iii).
- (e1) By Lemma RO, 𝒪_E ∩ {αẐ^rep > Z} ⊆ {st̄ ∈ {exact, completed}} ∩ {αẐ̄ > Z}. On the SMC branch
  {st̄ = completed} = 𝒜. By the tower property and (d), P(𝒜 ∩ {αẐ̄ > Z}) = E[1_𝒜 P(αẐ̄ > Z | 𝓒)] ≤ α·P(𝒜).
- (e2) By Lemma RO(3) with g = Ẑ^rep ≥ 0: E[1_{𝒪_E} Ẑ^rep] ≤ E[1_𝒜 Ẑ̄] = E[1_𝒜 E[Ẑ̄ | 𝓒]] = Z·P(𝒜).
- (e3) Divide (e1) by P(𝒪_E).
- (f) On G_fp ∩ 𝒪_E, Ẑ^fp ≤ e^η·Ẑ̄, so {αẐ^fp > Z} ∩ G_fp ∩ 𝒪_E ⊆ 𝒜 ∩ {α·e^η·Ẑ̄ > Z}. Apply (e1) with α·e^η in
  place of α. The bound is trivially true if α·e^η ≥ 1. Add P(𝒪_E ∖ G_fp) ≤ ε. ∎

**Remarks.**
1. The factor e^η cannot be removed. T12(iv.f), locked, gives a NUM-compatible model with the same path and
   Ẑ^impl = e^η·Ẑ.
2. NUM alone does not give G_fp, because it does not give path agreement. So VAL-FP has to be measured, for example
   by an exact or high-precision replay of a sample of fits. Measuring it needs the R/C++ engine, which this run
   does not have.
3. On the exact branch, (a)–(e) hold trivially: Ẑ = Z, and PIPs are exact under EX-A.

### 1.1 Exact proof edits to the locked T12 and T31(i) (against `COLLECTED_PROOFS_v2.tex`)

Line numbers refer to `COLLECTED_PROOFS_v2.tex` at sha256 `acb3e266…eea` (LOCKED_PROOFS.md, wave 1). In the
proof-body lines (1287–1503) the T12 STATEMENT is reproduced verbatim; the source files are
`T12_T8_frozen_run_identities/STATEMENT.md` and `PROOF_v6.tex`.

| # | Where | Edit | Proof changes? |
|---|---|---|---|
| E12-B1 | STATEMENT §2, "Success" item | Append: "All objects of §§2–3 are those of the *potential uninterrupted run* R̄ (no preflight, no in-run time guard). The allocation, the clock and the guard are not components of 𝓒. A statement about reported outputs is obtained only through GUARD and Lemma RO, never by conditioning on completion." | No. The proof (line 1413, eq. T12:eq:freeze) already uses O_r = Φ(𝓒, U_r). That is true for R̄ by definition, but it was false for the deployed method on 𝒢. The edit removes a latent mismatch and adds no new argument. |
| E12-B2 | STATEMENT §2, CAL item | Replace "(grid, T, L, N_e, tier, candidate set and every other setting the final run uses)" with "(tier, grid, T, N_e, L, M = 4, island count, ℓ, the inherited calibration score leaders and every other setting the final run reads; the allocation and clock are not settings)" | No. |
| E12-B3 | STATEMENT §2, "Pooled estimators" | Delete "secondary P̃_j = Σ_rẐ_rPIP̂_{rj}/Σ_rẐ_r". Add "pooled island product Π̂_j = ¼Σ_rẐ_rPIP̂_{rj}". | — |
| E12-B4 | STATEMENT §3 (iii) | After "E[Ẑ_rPIP̂_{rj} \| 𝓒] = Z·PIP_j" insert "; hence E[Π̂_j \| 𝓒] = Z·PIP_j". | Proof of (iii) (line 1421): add the sentence "By linearity, E_c[Π̂_j] = Z·PIP_j." |
| E12-B5 | STATEMENT §3 (iv.b) | Delete "both normalised estimators are biased" and replace by "the primary estimator is biased". Delete "and E[P̃₁] − PIP₁ < −0.15". Add (iv.b′): "Given 𝓒, E[Ẑ·P̄_j \| 𝓒] − Z·PIP_j = −¾·Cov(PIP̂_{1j}, Ẑ₁ \| 𝓒); in the instance this is < −0.1275·Z, so the pooled Ẑ times the primary PIP is not unbiased for Z·PIP_j." | Proof §8.2 (lines 1452–1453): delete the display for E[P̃₁] and its 10⁴-term enumeration sentence. Table (line 1466): delete the E[P̃₁] − PIP₁ row. Line 1469: replace "below −0.17 (primary) and −0.15 (secondary)" by "below −0.17". Add the proof of (iv.b′), which is the four-line computation in §1(c) above; it uses only (ii), (i.a) and (iv.c). The helper `certify_instance.py` should drop the secondary branch; the remaining CHECK lines are unchanged. |
| E12-B6 | STATEMENT §3, new (v) | "(v) Output level. Under GUARD: P(𝒪_E ∩ {αẐ > Z}) ≤ α·P(𝒜); E[1_{𝒪_E}Ẑ] ≤ Z·P(𝒜); no identity is claimed given 𝒪_E." | New short section after §8 (proof of (iv)), citing Lemma RO; it is the proof of (e1)–(e3) above. |
| E12-B7 | STATEMENT §3 (iv.f) | Keep as is (NUM alone). Add the positive companion: "(iv.f′) Under VAL-FP(η, ε), P(𝒪_E ∩ {αẐ^fp > Z}) ≤ α·e^η·P(𝒜) + ε." | New three-line proof, as in (f) above. |
| E12-B8 | STATEMENT §3 (iv.d) | No change. Note: launch events A ∈ σ(𝓒) are covered there. A guard stop **during calibration** is in σ(𝓒, Ξ_cal), not σ(𝓒), so (iv.d) does not directly apply to it. Through R̄ the issue does not arise, because no conditioning is done. | No. |
| E31-B1 | T31 STATEMENT §1, "Final run given c" | Add: "the final run is that of the potential uninterrupted run R̄". | No. |
| E31-B2 | T31 STATEMENT §3, new (a′) | "Under GUARD, for the reported Ẑ: P(𝒪_E ∩ {Z < αẐ}) ≤ α·P(𝒜). The coverage statement for the output is 'a bound is reported and exceeds Z, with probability at most α'. Coverage given completion is ≥ 1 − α·P(𝒜)/P(𝒪_E) only." | One paragraph after Theorem T31:thm:ab: integrate (a) over 𝓒 on 𝒜 and apply Lemma RO. |
| E31-B3 | T31 (c), (d) | No change. (d) is the flag-conditioning failure, and completion-conditioning is the analogous failure for 𝒪_E. | No. |

---

## 2. The run/output split for T11(iii), T14(i), T15, T23(ii), T25(iv), T31, T34

Under GUARD every locked final-run statement below is a statement about R̄. Its proof never read the guard, so no
proof changes. The output-level version follows from Lemma RO in one line. The pattern has two parts:
1. **Statement change:** replace "the (launched/completed) final run" by "the potential uninterrupted final run R̄".
2. **Output corollary:** for a nonnegative error functional e, E[1_𝒪 e^rep] ≤ E[1_{𝒪̄} ē]. For an error event A,
   P(𝒪^c ∪ A^rep) ≤ P(𝒢) + P(𝒪̄^c) + P(𝒪̄ ∩ Ā).

| Result | One-line statement change | Proof changes? |
|---|---|---|
| T11(iii) | Setting item 5: replace "A launched final run executes all these rounds (no early stop; aborts imposed by the computing environment, such as wall time, are outside the idealised model)" by "These are the rounds of the potential uninterrupted run R̄; the reported scored set equals 𝒮̄ on 𝒢^c (GUARD)". Output: P(𝒪_H, S* ∉ 𝒟_f^rep \| 𝓒) ≤ (1 − π₀(S*))^{Q_f}. | No. The proof is a reading scheme on streams 10–13 (T11 Prop. "final run is a reading scheme"); Remark "the final run executes in full on Λ" becomes true by definition. |
| T12 | §1.1 above. | Only E12-B4, B5, B6, B7 add text. |
| T14(i) | "For the potential final run, Ẑ_r/Z = A_T/b_T and E[\|Ẑ_r/Z − 1\| \| 𝓒] ≤ …"; output: E[1_{𝒪_E}\|Ẑ_r^rep/Z − 1\| \| 𝓒] ≤ the same bound. | No. |
| T15 | H-T12 now refers to R̄. Output: E[1_{𝒪_E} f_T^rep(A^c)] ≤ the bound of (i); tail (ii) likewise. | No. |
| T23(ii) | (ii-a)/(ii-b) pathwise on R̄. (ii-c): E_𝓒[1_{𝒪_E} max_j\|P̄_j^rep − 1{j∈S₀}\|] ≤ δ + (1−a)^{⌊L/r₀⌋} + (L+4)(η+ρ) + u_π. (ii-d): P(𝒪_E^c ∪ {MPM̂^rep ≠ S₀}) ≤ P(𝒢) + P(𝒜^c) + 2E[1_𝒜 𝓑_n], with 𝓑_n the (𝓒-measurable) basin bound. | No. (Measured rounds carry no guard check, but the post-local-search check can stop a fit whose PIPs are already computed. Those fits are in 𝒢 and produce no output.) |
| T25(iv) | PW2 and the conclusion Var(W_T) ≤ B_T are for R̄. Output: E[1_{𝒪_E}(W_T^rep − 1)²] ≤ B_T. Var(W_T \| 𝒪_E) is not claimed. Its STATEMENT phrase "Completed final runs means execution of the prescribed finite ideal run" is exactly R̄; rename it to "potential uninterrupted run". | No. |
| T31 | (i): E31-B1–B3. Conjectured parts (ii)–(vii): read on R̄. (v) "discovery after selection" is on 𝒮̄, with the output version via Lemma RO(2). | No (for (i)). |
| T34 (CONJECTURE) | Restate: "st is a function of (R̄, Ξ); st̄ ∈ {exact, completed, schedule_limit} is a potential-run quantity; resource_limit = 𝒢 is operational, its law given R̄ is not modelled, and every guarantee about reported outputs is of the form P(𝒢) + P(potential-run failure) (Lemma RO). P(𝒢) is reported empirically (§4 of REPORT) or controlled by allocation sequences (OP-a/OP-s, V13)." New clause (v) is Lemma RO, PROVED. The rest of T34 is still CONJECTURE. | T34 has no proof; Lemma RO is new. |
| T21 | §4 below. | Yes, small edits (§4.2). |

**Never condition on observed completion.** Every corollary above has 1_𝒪 inside the expectation or 𝒪^c inside the
union. None has 𝒪 behind the conditioning bar. The only conditional form allowed is Lemma RO(4), an inequality that
divides by P(𝒪).

---

## 3. Proposition 1 (restated T07 + one sentence of T06(i))

Setting: m > 0 on Ω, ≺ the method's total tie order (smaller size, then lexicographic), π the target posterior.
For 0 ≤ k ≤ K, S*_k is the ≺-least maximiser of m over {|S| = k}.

**(a), (b), (c)** are T07(ii)(a)–(c), (iii)(c) and (i), locked; they are quoted in REPORT §2. Two short additions
follow.

**(i′) Sharpness of the ceiling. PROVED.** Assume s₀ ≤ K. Then there is a positive size-only prior w̃ with
S†_w̃ = S₀ if and only if S*_{s₀} = S₀.

*Proof.*
- (⇒) This is T07(i), locked.
- (⇐) Let M := max_{S∈Ω} m(S) and m₀ := m(S₀) > 0. Put w̃(s₀) = 1 and w̃(k) = ε for k ≠ s₀, 0 ≤ k ≤ K, where
  0 < ε < m₀/M. The normaliser Σ_k C(p,k)w̃(k) is common to all S, so S†_w̃ is the ≺-least maximiser of
  w̃(|S|)·m(S).
- If |S| ≠ s₀, then w̃·m(S) ≤ ε·M < m₀ = w̃(s₀)·m(S₀).
- If |S| = s₀, then m(S) ≤ m₀, because S₀ = S*_{s₀} maximises m at size s₀. If m(S) = m₀ and S ≠ S₀, then
  S₀ ≺ S, because S₀ is the ≺-least such maximiser.
- So the maximum value m₀ is attained only at models of size s₀ with m = m₀, and S₀ is ≺-least among them. Hence
  S†_w̃ = S₀. ∎

*Reading.* The event "some size prior recovers S₀" is exactly the event "no within-size ranking error". The prior in
the proof is data dependent (ε < m₀/M). So (i′) says nothing about one fixed prior repairing all different-size errors
at once. It is a per-data-set statement.

**(iii′) A certificate from a fitted run. PROVED.** If some scored model S′ ∈ 𝒮 satisfies |S′| = s₀, S′ ≠ S₀ and
F(S′) > F(S₀), then S*_{s₀} ≠ S₀. Hence no positive size-only prior has global HPM S₀ on these data. The same
conclusion holds if F(S′) = F(S₀) and S′ ≺ S₀.

*Proof.* |S′| = |S₀| gives ϖ(S′) = ϖ(S₀), so m(S′) > m(S₀), or m(S′) = m(S₀) with S′ ≺ S₀. In both cases S₀ is not
the ≺-least maximiser of m at size s₀. Then apply T07(i). ∎

*Corollary for the study.* A completed fit is a "posterior miss" (F(S₀) ≤ F(Ŝ), Ŝ ≠ S₀). If such a fit has
|Ŝ| = s₀ and the inequality is strict, then S′ = Ŝ is a certificate. So every strict same-size posterior miss is a
data set on which no size-only prior (BB(1,p) or any retuning, including the dropped BB(1,1) arm) makes the
global HPM equal S₀. Under G and NIS, exact ties have P₀-probability 0 (T06(i)(c), locked), so "strict" holds almost
surely. Subset and superset misses carry no such certificate. Whether S*_{s₀} = S₀ holds on them is not decidable from
the scored set alone.

**T06(i) sentence** (locked T06(i)(a)). F_S = F_{S′} as functions of the response iff X_S X_Sᵀ = X_{S′} X_{S′}ᵀ.
Then |S| = |S′|, and the two supports have equal posterior probability for every response. No data and no size-only
prior can separate them under this target. The added clause "no size-only prior" follows from |S| = |S′|.
**Caution on wording.** THEORY_PRIORITIES writes "projections agree". The locked condition is equality of the outer
products X_S X_Sᵀ, which is not equality of the projection matrices P_S (T06(i)(b): equal spans with different outer
products give different score functions). The paper must use "outer products".

---

## 4. Theorem 4 (restated T21 (C1) with routes (a), (d), (e′))

### 4.1 Statement and proof

Hypotheses: EX-A, EX-S, CAL, SR, GUARD. Use U = 𝒢 ∪ (𝒢^c ∩ Ū) and the potential scored set 𝒮̄.

**(C1′) PROVED** (candidate; it is the locked C1 argument plus Lemma RO):

  P(U or Ŝ ≠ S₀) ≤ P(U) + 2E₀δ₁ + P(Ū^c, S₀ ∉ 𝒮̄),   with P(U) ≤ P(𝒢) + P(Ū).

*Proof.*
- {U or Ŝ ≠ S₀} = U ∪ (U^c ∩ {Ŝ ≠ S₀}), and U^c = 𝒢^c ∩ Ū^c. On this event GUARD gives Ŝ = Ŝ̄ and 𝒮 = 𝒮̄.
- The locked C1 argument (T21 PROOF_v3, lines 63–76) applied to R̄ gives
  {Ū^c, Ŝ̄ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ {Ū^c, S₀ ∉ 𝒮̄}, and P(δ₁ ≥ ½) ≤ 2E₀δ₁. ∎

The last term is a potential-run quantity. So every route below is evaluated on R̄, where "the launched final run
executes all designated draws", "the scan is completed" and "the H rounds execute" hold by definition. The locked
proof's operational-execution premises (T21 STATEMENT §2, "Operational execution is explicit …") are therefore no
longer premises. They are replaced by GUARD, which is a weaker and checkable statement.

**Route (a), iid final draws.** P(Ū^c, S₀ ∉ 𝒮̄) ≤ P(𝒜^c, S₀ ∉ 𝒮_cal) + E[1_𝒜 1{S₀ ∉ 𝒮_cal}(1 − π₀(S₀))^{Q_f}],
with Q_f = 4N_e(T + L + 5). This is the locked proof of (a), lines 92–145, unchanged, read on R̄. It uses T11(iii)
restated in §2.

**Route (d), tables and completed scans.** P(Ū^c, S₀ ∉ 𝒮̄) ≤ P(E_TS^c). Here E_TS is the event that S₀ ⊆ C_b for
some block, or that some local search of R̄ (pilot, diagnostic or final) has a centre in the flip-or-swap
neighbourhood of S₀. This is the locked proof, lines 255–278. On R̄ every scan completes.

**Route (e′), Gibbs-path terminal repair. PROVED as an implication of Theorem B.**

Fix a **selection boundary**: a terminal-round boundary at φ = 1 after which H rounds run with no resampling. In the
final run, the boundary after the stage-T resampling is followed by the stage-T round (at φ_T = 1), the L burn-in
rounds and the 4 measured rounds. So H ≤ L + 5 is available. This is checked in `v3_engine.h`: the burn-in and
measured loops call only `population_round`.

Let A be an availability event measurable at the boundary, for example "some particle is in the eligible set". Let
X_sel be a particle state chosen using only the past. For a state x, Theorem B (W1-T24G) gives the exact data
functions v(x), c_*(x) and η(x), and

  β_H(x) := P(Bin(H, c_*(x)) < v(x)) + H·η(x) ≤ v(x)(1 − c_*(x))^{⌊H/v(x)⌋} + H·η(x).

Feasibility s₀ + a(x) ≤ K is part of eligibility. Then:
- (e′) P(Ū^c, S₀ ∉ 𝒮̄) ≤ P(A^c) + E[1_A min{1, β_H(X_sel)}].
- In final-run form, with A_F = 𝒜 ∩ {an eligible particle at the boundary}:
  P(Ū^c, S₀ ∉ 𝒮̄) ≤ P(𝒜^c, S₀ ∉ 𝒮_cal) + P(𝒜, no eligible particle) + E[1_{A_F} min{1, β_H(X_sel)}].
- (e-M) If I is the past-measurable set of eligible particles at the boundary, the last expectation may be replaced by
  E[1_{A_F} ∏_{i∈I} min{1, β_H(X_i)}].

*Proof.*
1. The locked proof of (e) (lines 280–368) uses H24 only to get the conditional inequality
   P(M_H | selection past) ≤ (1 − a_n)^H + H·η_n on availability, eq. (repair). It then caps the bound at 1,
   integrates, and splits off nonlaunch and no-eligible-particle.
2. Given the selection past, the selected particle's next H rounds form a Markov chain started at X_sel, with fresh
   randomness and the round kernel K₁ (T12 (R3) iterated, no resampling). Theorem B, applied with x = X_sel (a
   past-measurable state; the constants are exact functions of the data and x), gives
   P(M_H | selection past) ≤ β_H(X_sel).
3. Steps 1 and 2 then go through verbatim with (1 − a_n)^H + H·η_n replaced by β_H(X_sel). A pointwise bound is
   enough: no uniformity over 𝓡_d is needed, because the bound is evaluated at the selected state. Cor. B-unif gives
   the uniform version if one is wanted.
4. For (e-M): given the boundary σ-field, the trajectories of distinct particles over the H rounds are conditionally
   independent. This is (R3) applied round by round with no resampling, and it is Cor. B-M of W1-T24G. Also
   M_H ⊆ ⋂_{i∈I} {particle i scores no S₀ in those rounds}. ∎

*Asymptotic form* (PROOF SKETCH; its premises are W1-T24G §4, which are not proved). Suppose H = L + 4 or L + 5,
c_*(X_sel) ≥ c > 0 with probability → 1, v(X_sel) ≤ v̄, and H·η(X_sel) → 0 in probability on A. Then
β_H(X_sel) ≤ v̄(1 − c)^{⌊H/v̄⌋} + o_P(1) → 0, because L → ∞. Together with vanishing availability and nonlaunch
terms, discovery fails with probability → 0. This needs no factorial constant. The rate is slow (W1-T24G Headline 5 estimates about n^{−0.07} for
c_* ≈ 1/(B+3)); I did not re-derive it.

**Routes (b), (c), (f).** These are locked and unchanged, read on R̄ (supplement).

### 4.2 Exact edits to the locked T21 (STATEMENT.md and PROOF_v3.tex)

| # | Where | Edit |
|---|---|---|
| E21-B1 | STATEMENT §2, "Operational execution is explicit …" paragraph | Replace it by: "All scoring and discovery statements concern the potential uninterrupted run R̄. Under GUARD, on U^c the reported Ŝ and 𝒮 equal those of R̄. U contains the stop event 𝒢 (resource_limit). No probability is conditioned on completion." |
| E21-B2 | STATEMENT §2, H24 item | Delete. Add "**H-TB** (imported, W1-T24G Theorem B, PROVED-candidate, unreviewed): for every x and H, P_x(S₀ not scored within H terminal rounds) ≤ β_H(x)." |
| E21-B3 | STATEMENT §3 (C1) | Write the last term as P(Ū^c, S₀ ∉ 𝒮̄) and add "P(U) ≤ P(𝒢) + P(Ū)". |
| E21-B4 | STATEMENT §3 (e) | Replace (1−a_n)^H + Hη_n by β_H(X_sel) throughout. Replace the asymptotic sentence by the (e′) asymptotic form above. Add (e-M). Allow H ≤ L + 5 for the final run. |
| E21-B5 | PROOF_v3 lines 45–50 | Replace by: "Probabilities are never conditioned on future diagnostics or completion. Scoring statements are about R̄, on which the designated draws, scans and rounds execute by definition; GUARD transfers them to the reported output on U^c." |
| E21-B6 | PROOF_v3 lines 68–72 (C1 proof) | Insert before "Hence": "On U^c = 𝒢^c ∩ Ū^c, GUARD gives Ŝ = Ŝ̄ and 𝒮 = 𝒮̄." Replace Sscr by 𝒮̄ in the displayed inclusion. |
| E21-B7 | PROOF_v3 §"Route (e)" (lines 280–368) | Replace eq. (H24) by "Theorem B at x = X_sel". Replace the derivation (exit)–(repair) (lines 296–323) by the one-line citation of Theorem B, keeping the "every terminal endpoint is a scored state" paragraph (lines 312–317), which Theorem B also uses through (R3). Replace (1−a_n)^H + Hη_n in (finalrepair) by β_H(X_sel). Delete lines 358–368 (c_n = 1/(s₀+d+B+2)!) and insert the asymptotic form. |
| E21-B8 | PROOF_v3 "Scope" (lines 398–416) | Add Theorem B (W1-T24G) to the cited inputs, labelled unreviewed. |

### 4.3 How T37 would enter (if a restated T37(i) closes). PROVED as an implication; T37 itself is OPEN.

Suppose a restated T37(i) supplies a data event TD* with the following property. On TD*, every completed local search
of the method whose centre c lies in 𝓡_d, and whose move cap satisfies ℓ ≥ |c Δ S₀| (or the extra-scan rule
applies), scores S₀. Let E_LS be the event that some local search of R̄ has its centre in 𝓡_d. Then

  (d⁺) P(Ū^c, S₀ ∉ 𝒮̄) ≤ P₀(TD*^c) + P(E_LS^c ∩ TD*) + 1{ℓ < s₀ + d}

(drop the last term under the extra-scan rule). On TD* ∩ E_LS the centre is in 𝓡_d, so S₀ is scored. Otherwise one
of the other two events holds. ∎

So T37 enters as a **strengthening of route (d)**, from distance-one centres to 𝓡_d centres, not as route (e). That
is because the local search is a scan route, not a Gibbs path. **Label clash:** FABLE_REVIEW calls this route
"(e′ = T37)", while W1-T24G calls Theorem B "(e′)". I propose (d⁺) = T37 and (e′) = Theorem B. HQ should fix the
labels.

**Eligibility.** E_LS is T38's crux. Its natural sufficient tweak is LS0, local search also from the start mode S̃₀.
With LS0, E_LS ⊇ {S̃₀ ∈ 𝓡_d}, a start-side event of T22(i) type.

**Data remark** (interpretation, needs confirmation by the ANALYSIS-H2 owners). The final local search starts from
the current best scored model. If its centre c ∈ 𝓡₂ is not S₀ and S₀ is not returned, then F(c) ≥ F(S₀) or S₀ is
unscored with F(S₀) > F(c). The second case is a search miss, and the data show 0 search misses. So, for the final
local search, the 541 fits with "centre in 𝓡₂ ∖ {S₀}, never returned S₀" should be posterior-miss fits.
- On posterior-miss data any TD*-type condition fails, because S₀ is not the 𝓡_d maximiser.
- So "local search repaired 0 fits" is not evidence against the T37 mechanism. It shows that (d⁺) is vacuous exactly
  on the error fits, and that Gibbs already scored S₀ whenever it was the posterior winner.
- This deduction holds only if the 541 refer to the final local search. If they include pilot or diagnostic searches,
  it does not follow.
