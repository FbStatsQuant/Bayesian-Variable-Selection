# Corollary C (§1R) — proof from Theorem A and DIST-C, with exact meanings and scope

**Status: DRAFT (by this seat, unchecked).** Stream D (Claude Opus 5.5), W3-DIST proof leg, 2026-11-15.
Target: `STATEMENT.md` v1.3.1 §1R, "Corollary C (the output of the sampler)" (`STATEMENT.md:202-215`). It is used here
as a consequence of **Theorem A (i)** (`:171-175`, taken as given) and of the deterministic parts of DIST-C proved in
`P6_DISTC.md` (this folder; referred to as [P6]).

---

## STATEMENT-CHANGE REQUEST (reader wording; no mathematical change to the displays)

The two displayed conclusions are proved below as stated. The surrounding reader text says more than the code in
two places (RC-1, RC-2), is imprecise in two others (RC-3, RC-4), and lists dependencies Corollary C does not use
(RC-5). Proposed replacement wording is at the end (§5).

- **RC-1 ("the best-scoring models among all models the run evaluated").** The returned list is the 40p + 1 best
  models of the set 𝓜 offered to the final-run ledger (`P6_DISTC.md` Lemma R, Lemma M). 𝓜 contains every model the
  final run's sampler and local searches evaluated. It also contains **all block-table models** (scored during setup,
  before the run: `cpp/v3_core.cpp:372-386, 408`) and **the models inherited from calibration** (the union of the
  calibration's three stores: `:418-429, 728-735`). So 𝒯 can contain models that "the run" in the sampler sense never
  evaluated. "Best-scoring among all models the run evaluated" is accurate only if "evaluated" is defined to include
  these. The retention sentence remains true under either reading (an evaluated model is in 𝓜).
- **RC-2 ("A run is *completed* when the sampler finishes and returns its output").** Stopped runs also return an
  output object: the HPM labelled incomplete, the partial ledger **including its top store** under `ledger$top`, and
  NA estimates (`v3_run.R:143-149`). The defining property is the reported status. Completion also requires that
  calibration succeeded and that the final local search and LS0 finished (`cpp/v3_core.cpp:451, 459, 480, 483-484`).
- **RC-3 ("each with its unnormalised posterior weight").** The output gives the **log** weight F(S) = log ϖ(S) +
  log m(S) (`top_store$value`). Here ϖ is the size prior normalised over Ω, and m is the marginal likelihood
  computed on the standardised data. The weight is e^{F(S)} = Z·π(S). The common factor Z is not returned
  (`log_Z` is only an estimate of it).
- **RC-4 ("with π(𝒯) ≥ n^{−cM/2}").** This condition cannot be checked from the output, since π(𝒯) = Σ_𝒯 e^F / Z needs Z.
  The last sentence of the corollary covers this in spirit. I suggest adding "and the output does not certify it".
- **RC-5 (dependency line of §1R, `STATEMENT.md:123`: "Corollary C = DIST-C (C-0), (C-i), (C-ii)(α) + Theorem A").** The
  proof uses only Theorem A (i), (C-0) = Lemma P6(a) applied pathwise, and the deterministic retention part of
  (C-ii)(α). It does **not** use the P⊗ form of (C-i), the discovery part of (C-ii)(α), or any premise of W3-SAMP:
  no H-U, SI, START, KERNEL or overlap condition. I suggest "Corollary C = Theorem A (i) + Lemma P6(a) + the store
  retention lemma (DIST-C (C-ii)(α), deterministic part)".

---

## 1. Exact meanings

All references to code are to `Scripts/SMC_BVS/core/`. The pins are re-verified in [P6] §2 (table P1–P33; SHA-256 in
`pins_sha256.txt`).

**Scope.** These are statements about the output of the **final SMC run** returned by the public fit
`v3_fit(X, y, seed, …)`. Excluded: the exact-enumeration branch (taken when Σ_{k≤K} C(p_ret, k) ≤ (5H₀ + 4N₀)p_ret,
`v3_preprocess.R:18-32`; executed at `v3_fit.R:120-132`; its status is "exact" or a failure, never "completed"), and
every fit whose status is not "completed". On the SMC branch |Ω| > 12560·p_ret > 40p_ret + 1, so the list is always a
strict subset of Ω ([P6] pin P27).

**"Completed".** The fit's `status` field equals `"completed"`. The final run's status string starts as "completed"
(`cpp/v3_core.cpp:413`). It is set to "resource_limit" if an island stops early (`:451`) or a guard fires after the
final local search (`:459`) or after LS0 (`:480`), and to "numerical_failure" on any `NumericalFailure` (`:483-484`).
Nothing sets it back. It is copied to the fit (`v3_run.R:121`; `v3_fit.R:171`). A final run happens only if
preprocessing, preflight, setup and calibration succeeded (`v3_fit.R:99-103, 117, 134-138, 154-160`). So completed ⇒ y is
not constant, the SMC branch was taken, and calibration returned "ok".

**"The output contains a list 𝒯".** `fit$top_store` (`v3_run.R:210`), set only on completed runs. It holds
`models` (original column indices, in the store order: decreasing score, ties by smaller size then lexicographic) and
`value` (the score F of each model) (`cpp/v3_core.cpp:358-362`). Its capacity is 40p_ret + 1
(`cpp/v3_ledger.h:78`), where p_ret is the number of non-constant predictors (`v3_preprocess.R:111-113`). So
|𝒯| = min(40p_ret + 1, |𝓜|) ≤ 40p + 1. Models are distinct ([P6] Lemma R0(i)).

**"Evaluated".** A model S is *evaluated by the run* iff S ∈ 𝓜, the set of models offered to the stores of the final-run
ledger ([P6] §4, Definition of 𝓜). By [P6] Lemma M, on a completed run 𝓜 is the union of three sets:
- (a) every model the final run scored or re-visited: the islands' initial π₀ draws, Gibbs flips and held states, swap and
  independence proposals (accepted or rejected), and every centre and scanned neighbour of the final local search and
  of LS0;
- (b) every block-table model;
- (c) every model inherited from calibration.

In original indices, the true model S_true := {j : β*_j ≠ 0} can be evaluated only if all its columns were retained and
|S_true| ≤ K. Otherwise the retention sentence is vacuous. (Remark: by [P6] Remark 6.2, a unique F-maximiser that only
the calibration evaluated also ends up in 𝒯. That is a code reading and is not used.)

**"Computed in exact arithmetic".** Premise EX-A of W1-N1 ("exact scores and arithmetic",
`Theory_work/Wave1/W1-N1/STATEMENT.md:70`), together with the identification (H-ID) of [P6] §0: each returned value is
exactly F(S) = log ϖ(S) + log m(S), and e^{F(S)} = Z·π(S) with Z = Σ_Ω e^F and π(S) = Π(S | D_n). It is used for two
things only:
- (i) the weights of Π̂ are proportional to π, so Π̂ = Π(· | S ∈ 𝒯, D_n) ([P6] Lemma W);
- (ii) the store order is the exact order of π, needed only for the retention sentence.

The first display uses only (i) and 𝒯 ⊆ Ω. It holds for **any** subset of Ω in place of 𝒯, however it was produced.

**Π̂ (a mathematical object, not computed by the method).** Π̂ := Σ_{S∈𝒯} π_𝒯(S)Π(· | S, D_n), with π_𝒯(S) := e^{F(S)}/Σ_{S′∈𝒯}e^{F(S′)}.
In the reader parametrisation (S, β, σ²) this is the same law as [P6]'s Π̂^𝒯 on (S, θ, v), pushed through the map
(S, θ, v) ↦ (S, β, σ²). For each S this map is a bijection: β_j = b_j = θ_j/ŝ_j for j ∈ S and 0 off S, and σ² = v. Both θ and v are on the
response scale (STATEMENT §0, `:29-39`). Under it the density attached to a draw is the same: the reader's mean
ȳ + (x − x̄)ᵀβ equals â + xᵀb, since â = ȳ^r − x̄ᵀb (STATEMENT §0, `:37-39`). Hence Π̂(d_H(f, f*) > r) is the same number in
both notations.

## 2. Statement proved

Let the constants c, M₀, n₀ and the range M₀ ≤ M ≤ √n/log n be those of Theorem A, and assume (A1)–(A5) with the window
q_n of this M. Let r_n := √(M·log n/n). Assume EX-A and (H-ID).

**(C1)** There is a set G_n of data sets, defined from the data alone, with P*(G_n) ≥ 1 − n^{−cM}, such that for every
D_n ∈ G_n and **every** completed run on D_n (any seed, any calibration outcome, any realisation of the final streams)
with π(𝒯) ≥ n^{−cM/2}:  Π̂(d_H(f, f*) > r_n) ≤ n^{−cM/2}.

**(C2)** (Deterministic.) If a completed run evaluated S_true and Π(S = S_true | D_n) > ½, then S_true ∈ 𝒯 and
π(𝒯) > ½. Moreover the reported HPM equals S_true.

## 3. Proofs

**Proof of (C1).** Put G_n := {D_n : Π(d_H(f, f*) > r_n | D_n) ≤ n^{−cM}}. Theorem A (i) says exactly
P*(Π(d_H(f, f*) > r_n | D_n) > n^{−cM}) ≤ n^{−cM}. So P*(G_n) ≥ 1 − n^{−cM}. G_n depends on the data only: Π(· | D_n) is the
exact posterior, which involves no stream.

Fix D_n ∈ G_n and a completed run with π(𝒯) ≥ n^{−cM/2}. Let B := {d_H(f, f*) > r_n} ⊆ 𝚯; it is measurable by the joint
measurability in [P6] Lemma P6(c). By [P6] Lemma W, π_𝒯(S) = π(S)/π(𝒯) on 𝒯 and 0 elsewhere. So Q := π_𝒯 satisfies
Q(S) ≤ L·π(S) for every S ∈ Ω, with L := 1/π(𝒯) ∈ (1, ∞). Note π(𝒯) > 0 by Positivity ([P6] §0) and 𝒯 ≠ ∅ ([P6] Lemma M).
Lemma P6(a) ([P6] §3) gives
  Π̂(B) = QΠ(B) ≤ Π(B | D_n)/π(𝒯) ≤ n^{−cM} / n^{−cM/2} = n^{−cM/2}.
Nothing in this argument depends on the streams beyond the fact that the run returned some 𝒯 ⊆ Ω with exact weights.
So the bound holds for every completed run on D_n. ∎

*Relation to DIST-C.* (C1) is [P6] Proposition C-i° with Theorem A (i) in place of DIST-1 (1.1). In DIST-1's terms,
t = M log n and λ = c/2: the threshold n^{−cM} = e^{−ct} and the store condition n^{−cM/2} = e^{−λt}. The P⊗ version
("P⊗(completed ∩ {π(𝒯) ≥ n^{−cM/2}} ∩ {Π̂(B) > n^{−cM/2}}) ≤ n^{−cM}") follows from (C1) by [P6] Lemma J, under any joint
law whose data marginal is P*.

**Proof of (C2).** Fix the data and a completed run. "Evaluated" means S_true ∈ 𝓜 (in internal indices, through ι⁻¹).
By [P6] Lemma M, 𝓜 ⊆ Ω, so S_true ∈ Ω. Since π(S_true) > ½, [P6] Lemma U shows that S_true is the unique maximiser of F
over Ω. [P6] Corollary R1(ii) — which rests on Lemma R, the invariant of the coded store (`cpp/v3_ledger.h:49-57`),
and on the fact that the store and the running HPM receive the same offers (`:89-94`) — gives S_true ∈ 𝒯, S_true first
in the list, and Ŝ = S_true. Finally π(𝒯) ≥ π(S_true) > ½. ∎

**Last sentence of Corollary C** ("whether the list carries enough posterior probability is a property of the run
that this corollary does not assert"). Consistent with the above. A sufficient condition with a probability bound
needs a delivery premise: discovery of S_true ([P6] (C-ii)(α-disc): W3-SAMP D-i + Lemma PC + P-OVL) together with
δ_n < ½ (selection). Without beta-min, π(𝒯) ≥ n^{−cM/2} is the premise P-STORE, with no proof and no output certificate
([P6] (C-ii)(β)).

## 4. Where the reader text says more than the code or the cited results deliver

| # | reader phrase (`STATEMENT.md:202-215`) | what the code / proof delivers | verdict |
|---|---|---|---|
| 1 | "computes the posterior by a sequential Monte Carlo sampler" | The run returns no particles and no draws (`cpp/v3_core.cpp:341-348`). It returns summaries, model lists, PIPs and evidence estimates. The corollary is about Π̂, which is defined from the returned list, not about an SMC approximation of Π | OK as worded, because the display is about Π̂. Do not call Π̂ "the sampler's posterior" |
| 2 | "A run is completed when the sampler finishes and returns its output" | Defined by status `"completed"`. Stopped runs also return objects (incl. a partial top store under `ledger$top`) | **imprecise** (RC-2) |
| 3 | "a list 𝒯 of at most 40p + 1 distinct models" | capacity 40p_ret + 1 ≤ 40p + 1; distinct | OK |
| 4 | "the best-scoring models among all models the run evaluated" | The best of 𝓜, which also contains the block tables and the inherited calibration models | **says more than the code unless "evaluated" is defined as membership of 𝓜** (RC-1) |
| 5 | "each with its unnormalised posterior weight" | the log weight F(S); e^F = Z·π(S); Z not returned | imprecise (RC-3) |
| 6 | "which we take to be computed in exact arithmetic" | EX-A; also needed for the store order in the retention sentence | OK (assumption stated) |
| 7 | "it contains no draws of (β, σ²)" | true (`cpp/v3_core.cpp:341-348`; no parameter draws anywhere in `v3_assemble_final`) | OK |
| 8 | "Π̂ … each with its exact conditional posterior distribution" | Π̂ is defined, not computed. With exact weights, Π̂ = Π(· \| S ∈ 𝒯, D_n) | OK. Suggest "(Π̂ is not computed by the method)" |
| 9 | "with P*-probability at least 1 − n^{−cM} …, **every** completed run (whatever its random numbers)" | proved pathwise on a data event (C1). No stream idealisation needed | OK (and stronger than DIST-C (C-i) as stated) |
| 10 | "with π(𝒯) ≥ n^{−cM/2}" | a condition on the run that cannot be checked from the output | OK as a hypothesis; add "not certified by the output" (RC-4) |
| 11 | "If a completed run evaluated the true model … and the posterior probability of that model exceeds ½, then the list contains it and π(𝒯) > ½" | proved (C2), deterministic. The HPM then also equals it. Vacuous if a true column was dropped or s > K | OK (with "evaluated" as in RC-1) |
| 12 | "Under the conditions of Theorem A" | Corollary C inherits Theorem A's status (candidate; DIST-1 + bridges B0–B2). It adds no probabilistic step | OK; status must be carried |
| 13 | §1R dependency line "DIST-C (C-0), (C-i), (C-ii)(α) + Theorem A" | Only Theorem A (i), P6(a) and the retention lemma are used. No W3-SAMP premise | over-lists (RC-5) |

## 5. Proposed reader wording (for HQ; same mathematics)

> **Corollary C (the output of the sampler).** The method computes the posterior by a sequential Monte Carlo sampler
> (small problems that it solves by exact enumeration are not covered here). A run is *completed* when the method
> reports the status "completed". Its output then contains a list 𝒯 of at most 40p + 1 distinct models: the
> best-scoring models among all models scored in the run (including those carried over from the precomputed block
> tables and from the calibration). Each model comes with the logarithm of its unnormalised posterior weight, which
> we take to be computed in exact arithmetic. The output contains no draws of (β, σ²). Let π(𝒯) be the posterior
> probability of the list. Let Π̂ — not computed by the method — be the posterior restricted to the list: the models in
> 𝒯, weighted in proportion to their weights, each with its exact conditional posterior distribution of (β, σ²). Under
> the conditions of Theorem A, with P*-probability at least 1 − n^{−cM} over the data, **every** completed run (whatever
> its random numbers) with π(𝒯) ≥ n^{−cM/2} satisfies
>
>     Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}.
>
> If a completed run scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then
> the list contains it, it is the reported highest-probability model, and π(𝒯) > ½. In general, whether the list
> carries enough posterior probability is a property of the run. This corollary does not assert it, and the output
> does not certify it.

## 6. Risks
1. Corollary C is only as good as Theorem A (i), a candidate assembled from DIST-1 and bridges B0–B2. Nothing here
   checks them.
2. (H-ID) and EX-A are hypotheses. In floating point the returned weights are approximations; (C1) would need an
   error term, and (C2) holds for the computed order ([P6] Remark 6.3).
3. The code pins were re-verified on the working tree, but the commit identity was not (no git). The SHA-256 values are
   recorded in `pins_sha256.txt`.

## Amendments (lead, 2026-11-15, after the same-family pre-check; they are part of this file)
A-1 (§3, "Relation to DIST-C"). Read that paragraph with Theorem A's constants throughout: the radius is √(M log n/n) and
the level n^{−cM} with the c of Theorem A (which already absorbs DIST-1's radius constant C); the proof in §2–§4 does not
use the paragraph.
A-2 (§5, reader wording — final form proposed by the lead, replacing the two sentences about the list and the last
paragraph). "A run is *completed* when the method reports the status "completed"; runs that stop early are not
covered. The output of a completed run contains a list 𝒯 of at most 40p + 1 distinct models: the best-scoring models
among those scored in the final run together with those the method scored earlier and carries into it (its
precomputed tables for small groups of predictors, and models kept from its calibration stage). … If a completed run
scored the true model {j : β*_j ≠ 0} and the posterior probability of that model exceeds ½, then the list contains it, it
is the model the method reports as most probable, and π(𝒯) > ½." (The stronger description "the best of everything the
calibration and the final run scored" is not claimed: it was not line-checked.)
A-3 (after the cross-family line check; §1). The first display holds for any **nonempty** subset of Ω (the restricted posterior is
undefined for the empty subset; the returned list is nonempty).
A-4 (§5 opening sentence and §4 row 1). Replace "The method computes the posterior by a sequential Monte Carlo sampler" by
"The method uses a sequential Monte Carlo sampler to explore the models and to compute summaries of the posterior": the
method computes neither the full posterior nor Π̂. (RC-2: completion requires the final local search and, when enabled, LS0.)
