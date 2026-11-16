# T7 · Lemma KER — PROOF v2 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Independent derivation, then a comparison with N9. Write γ := γ_φ, S′ for the proposed set, k := |S|.

## Step 0 — common facts
*The code's γ_φ.* A particle stores `lg0 = log ϖ(|S|) + comp(S)` and `d = (log m(S) − log m(∅)) − comp(S)`
(`cpp/v3_engine.h:95-97`) and `lgphi(φ) = lg0 + φ·d` (`cpp/v3_engine.h:14`) = log γ₀(S) + φd(S) = log γ_φ(S). Under EX-A
the cached and the fresh log m agree: `ScoreCache::find` returns a stored value only for the same model (hash and full
set compared, `cpp/v3_score.h:274-282`), and that value was computed by the same scorer (`cpp/v3_engine.h:91-94`); so
every step reads the exact log γ_φ.
*Fresh uniforms.* Each `vs->u(…)` returns the next value of the island's stream. A step reads a number of uniforms
determined by the state and the uniforms already read in the step; by the strong Markov property of an i.i.d. sequence
(as in `W3-SAMP:CC` CC4), given everything before the step, its uniforms are i.i.d. U[0, 1) and independent of the past.
So the step's transition law given the past is the law computed below from i.i.d. uniforms. Side effects of `eval`,
`held` and `rb_acc` (cache, ledger, recording) do not change the state.
*Index draws.* For u ~ U[0, 1) and an integer c ≥ 1, ⌊u·c⌋ is uniform on {0, …, c − 1}; `P.S` is the sorted list of S,
so `P.S[⌊u k⌋]` is uniform on S (`cpp/v3_engine.h:150, 167`); `nth_nonmember(bits, ⌊u(p − k)⌋)` is uniform on [p] ∖ S
(it returns the m-th non-member in increasing order, `cpp/v3_engine.h:134-144`).

## Step 1 — Gibbs coordinate j (`cpp/v3_engine.h:113-132`)
S⁺ := S ∪ {j}, S⁻ := S ∖ {j}. `add_ok` = (j ∈ S) or |S| < K (`cpp/v3_engine.h:116`), i.e. |S⁺| ≤ K. If so, `tmpQ` is the
other configuration (`cpp/v3_engine.h:120-122`) and `oj = plogis_log(lw − lo)` with lw = log γ(S⁺), lo = log γ(S⁻)
(`cpp/v3_engine.h:124-126`); `plogis_log(x)` = eˣ/(1 + eˣ) (`cpp/v3_util.h:89-93`), so oj = γ(S⁺)/(γ(S⁺) + γ(S⁻)).
Otherwise oj = 0 (`cpp/v3_engine.h:117`). `oj` is added to `rb_acc[j]` before the uniform (`cpp/v3_engine.h:128`). Then
`include = u < oj` and the state becomes S⁺ if include, S⁻ if not (`cpp/v3_engine.h:129-131`: it switches to `tmpQ`
exactly when `include ≠ in`). So the step moves to S⁺ w.p. oj and to S⁻ otherwise, with oj = 0 and S⁻ = S when
|S⁺| > K: T12's Gibbs kernel and its pre-draw recording. It never leaves Ω (S⁺ only if |S⁺| ≤ K).
*Reversibility.* Transitions occur only within pairs {A, A ∪ {j}} ⊆ Ω, j ∉ A; with P(A → A∪j) = γ(A∪j)/Σ and
P(A∪j → A) = γ(A)/Σ, Σ := γ(A) + γ(A∪j): γ(A)P(A → A∪j) = γ(A)γ(A∪j)/Σ = γ(A∪j)P(A∪j → A).

## Step 2 — uniform swap (`cpp/v3_engine.h:146-159`)
If k ∈ {0, p}: stay, no uniform (`cpp/v3_engine.h:148`). Else j uniform on S, l uniform on [p] ∖ S, independent
(Step 0), S′ = S ∖ {j} ∪ {l} (`cpp/v3_engine.h:150-152`), accept iff u < α, α = 1 ∧ γ(S′)/γ(S) (`cpp/v3_engine.h:154-157`;
α = 1 when log ratio ≥ 0, else exp). This is T12's uniform swap. |S′| = k, so S′ ∈ Ω.
*Reversibility.* For S ≠ S′ with |S ∖ S′| = |S′ ∖ S| = 1 (same size k ∉ {0, p}), the pair (j, l) is unique and
q(S → S′) = 1/(k(p − k)) = q(S′ → S). So γ(S)q·(1 ∧ γ(S′)/γ(S)) = q·min(γ(S), γ(S′)) is symmetric.

## Step 3 — neighbour swap (`cpp/v3_engine.h:162-180`)
*The graph.* `neighbour_graph` (`cpp/v3_blocks.h:149-173`) chooses for each j a list of l ≠ j (`cpp/v3_blocks.h:159`) and
sets N(j) := the sorted, deduplicated union of j's choices and of {l : j ∈ chosen(l)} (`cpp/v3_blocks.h:170-171`). So N is
symmetric (l ∈ N(j) ⇔ j ∈ N(l)) and loop-free, and each N(j) is duplicate-free (`std::unique`, `cpp/v3_blocks.h:171`). It is built once from X
(`cpp/v3_core.cpp:302`).
*The step.* If k = 0: stay (`cpp/v3_engine.h:165`). Else j uniform on S (`cpp/v3_engine.h:167`); `cand` = N(j) ∖ S
(`cpp/v3_engine.h:168-169`); if empty, stay (`cpp/v3_engine.h:170`); else l uniform on N(j) ∖ S (`cpp/v3_engine.h:171`),
S′ = S ∖ {j} ∪ {l}, `back` = |N(l) ∖ S′| ≥ 1 (j ∈ N(l) by symmetry and j ∉ S′; `cpp/v3_engine.h:172-173`), and accept iff
u < 1 ∧ [γ(S′)/γ(S)]·|N(j) ∖ S|/|N(l) ∖ S′| (`cpp/v3_engine.h:175-178`). This is T12's neighbour swap; S′ ∈ Ω (same size).
*Reversibility.* For S′ = S ∖ {j} ∪ {l} with l ∈ N(j) ∖ S: q(S → S′) = 1/(k·|N(j) ∖ S|); from S′ the reverse move picks
l ∈ S′ (prob. 1/k) and then j ∈ N(l) ∖ S′ (prob. 1/|N(l) ∖ S′|), so q(S′ → S) = 1/(k·|N(l) ∖ S′|). Then
γ(S)q(S → S′)α(S → S′) = (1/k)·min(γ(S)/|N(j) ∖ S|, γ(S′)/|N(l) ∖ S′|), symmetric in (S, S′). (The pair (j, l) is the
unique one with S′ = S ∖ {j} ∪ {l}.)

## Step 4 — independence proposal (`cpp/v3_engine.h:182-192`)
S′ = `draw_start` (`cpp/v3_engine.h:184`): an exact π₀ draw (T6 START-X (S), (S′)), independent of S given the past
(Step 0); accept iff u < 1 ∧ e^{φ(d(S′) − d(S))} (`cpp/v3_engine.h:187-190`). This is T12's independence proposal.
*Reversibility.* γ(S)π₀(S′)(1 ∧ e^{φ(d(S′)−d(S))}) = Z̄₀⁻¹·min(γ₀(S)e^{φd(S)}γ₀(S′), γ₀(S)γ₀(S′)e^{φd(S′)}), symmetric.

## Step 5 — order and round (`cpp/v3_engine.h:195-214`)
`one_round` calls `draw_order` first (`cpp/v3_engine.h:203`): `ord` = identity on m = `nlabels()` = p + B + 2 labels
(`cpp/v3_engine.h:72, 196-198`), then for i = m − 1 down to 1, jj = ⌊u(i + 1)⌋ (uniform on {0, …, i}) and swap
ord[i], ord[jj] (`cpp/v3_engine.h:199`). The map from (jj_{m−1}, …, jj_1) ∈ ∏_{i=1}^{m−1}{0, …, i} (m! equally likely
tuples) to permutations is a bijection (Fisher–Yates), so the order is uniform; it reads only uniforms, not the state,
and all m − 1 uniforms are read before the first step. The loop then applies label `ord[pos]`, pos = 1..m: labels < p
are Gibbs j, label p the uniform swap, labels p + 1..p + B the neighbour swaps, label p + B + 1 the independence proposal
(`cpp/v3_engine.h:205-211`). m depends only on (p, B), fixed for the run.

## Step 6 — (KER-d)
N (`cpp/v3_core.cpp:302`), B (T2), `st` (T4) and the data are fixed before any island; the engine holds them as
`const` references (`cpp/v3_engine.h:60`). Inside the steps the state enters only through S itself, `add_ok`, the
self-loop tests and |N(j) ∖ S|, |N(l) ∖ S′|, all accounted for above. ∎

## Comparison with N9 (the re-check)
N9 rows 1–5 (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/PROOF.md:59-197`) state the same
kernels and prove reversibility by the same detailed-balance computations; checked line by line against the code at the
pin (lines unchanged since 39db138). N9's answer (a) — "the cap B acts before the symmetric union" — is right
(`cpp/v3_blocks.h:167-170`): degrees may exceed B, and the Hastings factor uses the actual |N(·) ∖ ·|. N9's γ_φ notation
remark (REPORT §2, last bullet) is consistent with Step 0. No error found.
