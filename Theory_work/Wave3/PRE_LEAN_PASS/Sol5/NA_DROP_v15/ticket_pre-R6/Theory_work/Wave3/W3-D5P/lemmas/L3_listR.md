# L3 — Corollary LIST-R (assembly) — proof

Claim: STATEMENT.md (C3), §4. Proof by the lead; line-checked by LC1 and LC1R (see REPORT §2); (0.5) added after council R1; Step 0′ and the NA-qualifier removal added in v1.2 [NA-1, NA-2].
Consumed, statuses verbatim (registry, main 029bb748): `W3-RM2-R:RM2-R-plus@1.0.1`, `W3-RM2-R:RM0-plus@1.0.1`,
`W3-RM2-R:DLV-0@1.0.1`: "PROVED-CHECKED; council R3, MANIFEST 5d6d3c90… (= R3 b06a8588 re-frozen as R3r), sol=9.5
PASS, opus=9.4 PASS" (each); `W2-APP:POST@1.0.7`: "PROVED-CHECKED". Internal: LIST-K (L1), LIST-CODE (L2); premise
IMPL-LIST (STATEMENT §1).

## Step 0 — inputs from RM2-R-plus
Under the hypotheses of RM2-R-plus (Setting R, the method as coded, the premises and configuration of RM2R §1, any
X-measurable partition with blocks ≤ 16, and (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, (W-R)), RM2R
`STATEMENT.md:177-182` gives, under the joint law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [MODE], and all
conclusions of RM0-plus (a), (b⁺) with 𝓛′ = 𝓛. We use:
(0.1) for n with s₀ ≤ K: 𝓜_n (S₀ is the unique maximiser of F on Ω) and 𝒦_n are data events, and
P(𝒢⁺_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0, 𝒢⁺_n := 𝓜_n ∩ 𝒦_n: this is RM0-plus (b⁺), a stated conclusion of RM2-R-plus
(RM2R `STATEMENT.md:126-134`, :180) [LC1R-5]: under [MODE], [SAND(Q)], [NA(Q)], [TL(Q)], P(𝒢⁺_n) → 1 (RM2R `STATEMENT.md:131-132`) [LC1-13];
(0.2) [POST]: E ε_n → 0, where ε_n = 1 − π(S₀ | y) (RM `STATEMENT.md` §2 interface table, as imported);
(0.3) s₀ ≤ K for all large n: S₀ ⊆ Q and |Q| ≤ K for n ≥ n₀ ((L-feas), RM `STATEMENT.md:98`, part of (L-R^b)); all
statements below are for such n. For the finitely many n with s₀ > K, STATEMENT §1's convention gives 𝓜_n = 𝒦_n = ∅ and
ε_n = 1, so (i) is vacuous and every probability bound of (ii) has right side ≥ 1 [LC1-2].
(0.3a) p_ret = p almost surely [LC1-5]: under Setting R (rows i.i.d. N(m_n, Σ_n) with unit diagonal, so each column has variance 1 and, with n ≥ 2 independent
rows, is constant with probability 0) [LC1R-2] no column is constant almost surely, and the code drops a column only when all its entries are exactly equal
(`v3_preprocess.R:111-112`). Hence, almost surely, Ω, K, ℓ_n, 𝒦_n and ε_n computed on the retained columns are those of
the design's p, and POST, stated for the design's p, applies to ε_n.
(0.4) (D) ⇒ every admissible run of the pinned core returns output for every valid non-degenerate input (DLV-0, RM2R
`STATEMENT.md:144-147`), and under Setting R the input is valid and non-degenerate with probability one (RM0-plus (c⁺),
RM2R `STATEMENT.md:138-143`, last sentence). DLV-0 is a statement about the pinned core; it is not transferred to the method with the list fields (0.5)–(0.6).
(0.5) *From the pinned core to the method with the list fields* [R1-opus-1]. L2, RM0-plus and DLV-0 are statements
about the core of record (4676af6); LIST-R is about the method with the fields, `method-v3.1.1-listpip` (7100bb3b; IMPL-LIST discharged there, `reviews/IMPL_LIST_codeprint.md` §5). By
IMPL-LIST (the commit computes the fields as SPEC §2 and §4 prescribe, from the returned list and values of the same
run, and changes no other field and no other state; SPEC §7 A.1–A.2) — and the returned list exists only after the
last runtime-guard consultation (`v3_fit.R:121-122` on the exact branch, after `v3_final_run` at `v3_fit.R:162` on the
sampler branch), after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so the new computation, which comes after the last guard consultation, cannot affect any guard decision: for matching guard inputs every guard decision of the tagged fit is that of the pinned fit [R2-E-2] (measured elapsed time and operation durations are not fixed by the input and the uniforms, so no decision-by-decision comparison of separate executions is claimed) — on every input and every
realisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation (not the same measured times) up to the new
fields, and the new computation can end the fit with an error only through the three `stop()` rows of `v3_list_fields`
(`v3_run.R:251, 253, 263`; at `method-v3.1.1-listpip`, 7100bb3b, whose core tree is 61b0a582; `v3_run.R` is unchanged from e9bac478), none of which can fire on an output run [NA-b1]: (i) *count mismatch* (`:251`, "top store has m models and
… scores"): the store is serialised by `store_to_list` (`cpp/v3_core.cpp:358-362`, called at `:366` for the sampler store
and at `:565` for the exact store), which fills the model list and the value vector in one pass over the same set, so
length(F) = m by construction; (ii) *duplicate model* (`:253`): the sampler store `top_store` and the exact store 𝒯^ex
hold distinct models (L2 (iii), (iv)), and `to_orig` is injective (`D.orig` strictly increasing, `v3_setup.R:8`), so their comma-joined keys are distinct; (iii) *column outside the retained set* (`:263`): every stored model is
serialised by `to_orig` (`cpp/v3_core.cpp:38-42`) as the original indices `D.orig[S[i]]` of retained columns, and the
`orig` passed to `v3_list_fields` is that same vector (`ctx$orig`, built from `pre$kept` at `v3_fit.R:118`; passed at `:176` on the sampler branch and, on the exact branch, at `v3_run.R:276` through `v3_exact_list_last` (`v3_fit.R:131`); `v3_run.R:160, 220` is the same vector in a standalone `v3_final_run`, which `v3_fit` calls with `list_fields = FALSE`, `v3_fit.R:162`), so `lut[orig] <- seq_len(p)` assigns a position in 1..p to every stored column. No other line of `v3_list_fields`, `v3_add_list_fields` or `v3_exact_list_last` (`v3_run.R:245-279`) can raise an error on an output run: `integer(max(orig))` needs p ≥ 1, which holds since p = 0 returns `no_predictors` before branching (`v3_preprocess.R:114`, `v3_fit.R:99-102`); `names(pip) <- pip_names` (and `setNames` in `res`) needs length(`pip_names`) = p, which holds since `pip_names` is `names(fit$pip_primary)`, of length p by `v3_run.R:161-162` (sampler), or `names(e$pip)`, of length p by `cpp/v3_core.cpp:558` and `v3_exact.R:9` (exact); the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error other than a failed allocation, which is not excluded here: allocation/delivery of the list fields is not claimed for the tagged method beyond output runs [T6-1, HQ ruling, option (C)], see (0.6). Hence on a post-commit run that returns output, 𝒪, `status`, `hpm`, `top_store`,
`fit$exact` (with its store) and the other existing fields the proof uses are those of core 4676af6 (on the exact branch `finish(fit)` is a lazy argument of `v3_exact_list_last` (`v3_fit.R:131`), forced at `v3_run.R:277` after `v3_list_fields`, so `peak_memory_kb` and `timings$total`, which `finish` samples, are measured after the helper; the proof does not use them, and the conformance citation `reviews/IMPL_LIST_codeprint.md:42` is read for the fields and state the proof uses). So L2 and RM0-plus (b⁺) apply to the method with the list fields on output runs; DLV-0 is not transferred (0.4); and the new fields are SPEC's functions of the pinned outputs.
(0.6) *Allocation and delivery of the list fields: not claimed beyond output runs* [b′-1, T6-1; HQ ruling, option (C), on Sol-6 b″-1]. Allocation/delivery of the list fields is not claimed for the tagged method beyond output runs. A note, **not a claim**: after the last guard the helper (`v3_run.R:245-269`; on the exact branch also `v3_exact_list_last`, `:274-279`) allocates a lookup of length max(orig) ≤ p_raw, m ≤ 40p + 1 duplicate-check key strings (K original indices of at most D ≤ 10 decimal digits each), and numeric vectors of length m and p; `PRE_LEAN_PASS/Sol5/FABLE_ALLOC_CARD.md` counts the live bytes and operations of these objects, but it does not bound the creation and interning of the key strings by `paste`, the live words of R's global string cache, or the operation cost of producing and hashing the decimal strings under IDEAL-W⁺ (Sol-6 b″-1). Therefore no bound against the brackets of C-DLV Lemma R, no constants C_W + 1, C_M + 8, and no extension of Lemma R, Corollary R or (D) to the method with the list fields is asserted; the allocation card's claim is withdrawn.
The reader assumptions (A1)–(A6) of Theorem 6 imply these hypotheses through READER §6 bridges B6.1–B6.4 (this file
does not re-prove them; the corollary is stated with "the hypotheses of RM2-R-plus").

## Step 0′ — (o): the list fields are never NA on an output run [NA-2, NA-C1]
Fix any data set and an admissible run on it that returns output [NA-C2]. By (0.5)
its existing fields are those of the pinned core. SPEC §4, as implemented by `v3_list_fields` and `v3_exact_list_last` (`v3_run.R:245-279`), makes a field NA (or absent) or stops only in these rows: a status other
than `completed` / `exact` (absent; not an output run); an empty list; a duplicate model (SPEC §4) and the implementation's two guards, a count mismatch and a column outside the retained set (the three `stop()` rows, errors; excluded by (0.5) [NA-b1]); a
NaN or +Inf score, or (HQ's confirmed reading) all scores −Inf; and, in the reading of STATEMENT §1 [NA-1], no exact-branch
row any more (`log_Z_list` is computed from `fit$exact$top`). On the sampler branch the list 𝒯 is nonempty — it contains
the hpm_better-maximum of the nonempty offered set 𝓜^run (L2 A4, (iii)) — and consists of distinct models with values
F(S) (L2 (iii)); on the exact branch 𝒯^ex is nonempty — it contains the hpm_better-maximum of Ω (L2 (iv)) — and consists
of distinct models of Ω with values F(S); and on the exact branch `pip_list` = `pip_primary` = PIP and `mpm_list` =
`mpm` = MPM (L2 (iv)), real-valued under EX-A [NA-C5]. Every F(S) is finite: ϖ(k) > 0 (`logprior[k]` finite for 0 ≤ k ≤ K, `cpp/v3_score.h:60-70`) and, under EX-A, log m(S) is finite for every
S ∈ Ω when yᵀy > 0 (Lemma S.2, RM2R `STATEMENT.md:151-152`; yᵀy > 0 on every output run, since a constant response
returns `y_constant` before branching — the test is `v3_preprocess.R:115`, routed at `v3_fit.R:99-102` — and the
scorer's yᵀy is that of the standardised y, `v3_preprocess.R:123`, `cpp/v3_score.h:56`, nonzero when the raw y is not
constant) [NA-C6]. So no NA row fires: `pip_list`, `mpm_list` and
`log_Z_list` = F_max + log Σ e^{F − F_max} (finite: a finite maximum plus the log of a sum in [1, |𝒯|]) are printed.
Nothing here uses the data event or a data law. ∎(o)

## Step 1 — (i): the pathwise statement on 𝒢⁺_n
Fix n with s₀ ≤ K, a data set in 𝒢⁺_n, and an admissible run (any seed, N_e, R′, calibration outcome) that returns
output (event 𝒪); by (0.5) its existing fields are those of the pinned core, so L2 applies. Output occurs only on the two branches [LC1-6]: `estimates_available` becomes TRUE only at
`v3_fit.R:129` (exact branch) or through `v3_fit.R:171` from `v3_run.R:218` (sampler branch), both after `branch_run` is set
(`v3_fit.R:106`); the earlier returns (`v3_fit.R:89`, `:102`) keep the initial FALSE (`v3_fit.R:78`). By L2 (i), on the sampler branch 𝒪 = {status "completed"}; on the exact branch 𝒪 = {status "exact"}
(`v3_fit.R:125-129`: `estimates_available` TRUE iff `e$status == "exact"`; otherwise `:130-131` returns with it FALSE).
*Sampler branch.* By L2 (i) (B4), since the data set is in 𝒦_n, S₀ ∈ 𝓜^run. Since it is in 𝓜_n, F(S₀) > F(S) for
every S ∈ Ω ∖ {S₀}; by L2 (v), S₀ ∈ 𝒯 and `hpm` = S₀. By L2 (iii), 𝒯 ⊆ Ω is a set of distinct models returned with the
values F(S). By IMPL-LIST and the identification of STATEMENT §1 (under EX-A, SPEC §2 applied to models with values
F(S) gives, for every retained column j, `pip_list[j]` = Σ_{S∈𝒯, j∈S} e^{F(S)−F_max} / Σ_{S∈𝒯} e^{F(S)−F_max} = pip_𝒯(j),
`mpm_list` = mpm_𝒯 and `log_Z_list` = F_max + log Σ_{S∈𝒯} e^{F(S)−F_max} = logZ_𝒯). SPEC §4's exceptional rows do not
fire [LC1-7]: the values are F(S), finite under EX-A (the scorer never fails for yᵀy > 0: Lemma S.2, RM2R
`STATEMENT.md:151-152`); 𝒯 ∋ S₀ is not empty; 𝒯 consists of distinct models (L2 (iii)). So the three fields are
present (not NA by Step 0′) [NA-C7]. LIST-K applies with this 𝒯
(S₀ ∈ 𝒯 ⊆ Ω) and gives:
 max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n (LIST-K (a)); max_j |pip_list[j] − PIP_j| ≤ ε_n (LIST-K (b));
 log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z (LIST-K (d)); and if ε_n < ½, `mpm_list` = S₀ = MPM (LIST-K (c)), hence
 `mpm_list` = `hpm` = S₀ = MPM.
*Exact branch.* By L2 (iv), `pip_primary` = PIP and `mpm` = MPM; by IMPL-LIST (SPEC §4), `pip_list` = PIP and
`mpm_list` = MPM, and `log_Z_list` = logZ_{𝒯^ex} computed from `fit$exact$top` [NA-1] (not NA by Step 0′) [NA-C7]. LIST-K (e) (S₀ ∈ Ω, since s₀ ≤ K) gives max_j |PIP_j − 1{j ∈ S₀}| ≤ ε_n, and MPM = S₀ if ε_n < ½;
trivially max_j |pip_list[j] − PIP_j| = 0 ≤ ε_n. On 𝓜_n, L2 (v) gives `hpm` = S₀ and S₀ ∈ 𝒯^ex. With 𝒯^ex ⊆ Ω distinct, values F(S) (L2 (iv)) and S₀ ∈ 𝒯^ex,
LIST-K (d) gives log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z.
No property of the seed, N_e, R′ or calibration outcome was used beyond admissibility, and the data event 𝒢⁺_n does not
depend on them. ∎(i)

## Step 2 — (ii): probability bounds
Fix t ∈ (0, ½) and an admissible run specification (seed, N_e, R′; the calibration outcome is then a function of the
data and the calibration streams). Consider a data set in 𝒢⁺_n ∩ {ε_n ≤ t} and a realisation of the run in 𝒪. By
Step 1, max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n ≤ t and max_j |pip_list[j] − PIP_j| ≤ ε_n ≤ t, so B₁(t), B₂(t) fail; if
|log_Z_list − log Z| ≤ ε_n/(1 − ε_n) ≤ 2ε_n ≤ 2t (LIST-K (d) and its corollary; ε_n ≤ t < ½),
so B₃(t) fails. Hence, as sets of (data, run randomness),
  𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t)) ⊆ (𝒢⁺_nᶜ ∪ {ε_n > t}) × (run randomness),
and likewise, since on 𝒢⁺_n ∩ {ε_n < ½} ∩ 𝒪 Step 1 gives `mpm_list` = `hpm` = S₀,
  𝒪 ∩ B₄ ⊆ (𝒢⁺_nᶜ ∪ {ε_n ≥ ½}) × (run randomness).
Taking probabilities under the joint law (for the left sides: their probability, or outer probability if measurability
is not assumed — the right sides are data events): P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t) and
P(𝒪 ∩ B₄) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n ≥ ½), by (0.1). The right sides tend to 0: (0.1), and Markov's inequality with
(0.2): P(ε_n > t) ≤ E ε_n / t → 0 and P(ε_n ≥ ½) ≤ 2E ε_n → 0.
*Rate.* Let p ≥ 2 for all large n. (T1-R) is hypothesis LSF of POST (RM `STATEMENT.md:128-133` defines (T1-R) as
"the LSF conditions of APP L1_POST(b)"), Setting R is POST's setting with the standardised-signal convention
(`L1_POST.md:8-18`), and POST (b) (`L1_POST.md:31-33`) gives, under the joint law, 1 − π(S₀) = O_P(r_n), r_n = √(log n/n).
Let t_n ∈ (0, ½) be deterministic with t_n/r_n → ∞. Given η > 0, choose M and n₀ with P(ε_n > M r_n) < η for n ≥ n₀;
for n ≥ n₁ ≥ n₀, t_n ≥ M r_n, so P(ε_n > t_n) < η. Hence P(ε_n > t_n) → 0, and with 𝒢♯_n := 𝒢⁺_n ∩ {ε_n ≤ t_n},
P(𝒢♯_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0. On 𝒢♯_n, every admissible output run satisfies, by Step 1 and the
argument above with t = t_n: max_j |pip_list[j] − 1{j ∈ S₀}| ≤ t_n, max_j |pip_list[j] − PIP_j| ≤ t_n, |log_Z_list − log Z|
≤ 2t_n, and (ε_n ≤ t_n < ½) `mpm_list` = `hpm` = S₀. ∎(ii)

## Step 3 — (iii): with delivery
(D) gives P(𝒪ᶜ) = 0 for the pinned core (0.4); for the method with the list fields no such statement is made ((0.5)–(0.6), T6-1), so (iii) is Step 2 on output runs. For every seed, N_e, R′ and calibration outcome, Step 2 gives P(𝒪 ∩ B₄) → 0 and P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) → 0 for every t ∈ (0, ½), and, when p ≥ 2 for all
large n, P(𝒪 ∩ (B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0 for every deterministic t_n ∈ (0, ½) with
t_n/r_n → ∞.
*"i.e. O_P(r_n)".* Let X_n ≥ 0 be any of the three errors (for the evidence, X_n := ½|log_Z_list − log Z|; X_n := 0 on 𝒪ᶜ) [NA-C8], so that {X_n > t} ⊆ 𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t)). Suppose X_n ≠ O_P(r_n). Then there is η > 0 such that for every M and every N some n ≥ N has P(X_n > M r_n) ≥ η. Since r_n → 0, we can choose n₁ < n₂ < … such that, for every k, r_n ≤ min(k⁻², 1/16) for all n ≥ n_k and P(X_{n_k} > k r_{n_k}) ≥ η. Define t_n := k r_n for n_k ≤ n < n_{k+1}, and t_n := ¼ for n < n₁. For n_k ≤ n < n_{k+1}: t_n = k r_n ≤ k·k⁻¹√r_n = √r_n ≤ ¼ (as r_n ≤ k⁻²), so t_n ∈ (0, ½); and t_n/r_n = k → ∞ as n → ∞. But P(X_{n_k} > t_{n_k}) = P(X_{n_k} > k r_{n_k}) ≥ η for every k, contradicting P(𝒪 ∩ (B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n))) → 0. Hence each error is O_P(r_n) on output. ∎(iii)

## Remarks for the checker
- Step 1 is where the two DIST links are used: L2 (i) turns "the run returns output" into "status completed, and LS0
  ran in this run"; L2 (ii)–(iii) turn RM's Ŝ⁺ into the printed `hpm` and put S₀ into `top_store`.
- The only data-level inputs are (0.1)–(0.3) and POST (b); no sampler law (no W1-N1 premise) is used: the claim is
  pathwise in the run.
- IMPL-LIST is used twice [R1-opus-1]: in (0.5), to carry L2 and RM0-plus from the pinned core to the method with
  the list fields on output runs ("changes no other field and no other state"; DLV-0 is not transferred, T6-1); and in Step 1, to identify the printed fields with
  pip_𝒯, mpm_𝒯, logZ_𝒯 (sampler branch) and with PIP, MPM, logZ_{𝒯^ex} (exact branch).
