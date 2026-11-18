# LC1 — reply of the blind line checker (Claude Opus 5.5, effort high, Claude Third), verbatim
<!-- received 2026-11-17 via delegate_task; brief reviews/LC1_brief_opus.md; checked tree a91eb7cb -->

# LC1: blind line check of W3-D5P L1–L3

**Scope.** I checked against the worktree `/home/fb31/BVS-wt/W3-D5P`, branch head `a91eb7cb`. `git diff 4676af6 HEAD -- Scripts/SMC_BVS/core` is empty, so the line numbers here are the line numbers at the pin. I did not open `LOG.md`, `CHECKPOINT_*`, `reviews/` (other than the brief), `TARGET.md` or `READER_DELTA.md`, and I wrote no files.

I opened every `file:line` cited in L2 in `Scripts/SMC_BVS/core/`. I also checked every source citation in L1–L3 and STATEMENT against W3-RM, W3-RM2-R, W3-RM2 (`:60-68`, `:134`, `:176`, `:216-218`), C-DLV L4, CC, SAMP `:59-60`, DIST `:297-303`, L1_POST, READER §6, and SPEC at `523dda23`.

**Code-path search requested by the brief:**
- **Writers of `hpmS`:** only `v3_ledger.h:86`. `offer_hpm` is called only at `v3_ledger.h:90` and at `v3_core.cpp:502`, which is inside the `catch`.
- **Writers of `top`:** in the final run, only `v3_ledger.h:91`. The only other `top.offer` is the enumeration's local store at `v3_core.cpp:549`, and the only other read is the calibration context at `:731`.
- **`emit = false` evaluations:** every `eval` call site uses the default `emit = true` (`v3_engine.h:122, 153, 174, 186, 291, 391`). The one exception is the centre at `:382`, and the only final-run caller with `emit_centre = false` is `v3_core.cpp:456`. The calibration calls at `:642` and `:689` use a different ledger and cache.
- **"completed" without LS0:** not possible in the shipped configuration (`v3_core.cpp:413, 451, 459, 465, 480, 484`; `v3_run.R:94`).
- **Cache insert without an offer:** only at `:456`, whose centre is `led.hpmS`. That model has already been offered: `ingest_tables` runs at `:408` and always offers ∅, because its table code is 0 and |∅| ≤ K, so `has_hpm` is already true.
- **Hash collision:** `find` compares the model exactly (`v3_score.h:271-277`), so a collision cannot return another model's score.
- **Eviction of the first store entry:** cannot happen. `offer` (`v3_ledger.h:49-57`) only ever erases the last element of a set holding at least 2 entries.
- **Unsorted model vectors:** none were found (see LC1-9).

I found no correctness defect. All findings are scope, faithfulness or editorial.

## 1. Per-object verdicts

| object | verdict |
|---|---|
| STATEMENT (C1) LIST-K, as proved | VERIFIED |
| STATEMENT (C2) LIST-CODE, as proved | VERIFIED-WITH-AMENDMENTS (LC1-4, LC1-10) |
| STATEMENT (C3) LIST-R, as proved | VERIFIED-WITH-AMENDMENTS (LC1-1, LC1-2, LC1-3) |
| L1 `lemmas/L1_listK.md` | VERIFIED (editorial LC1-12 only) |
| L2 `lemmas/L2_listCODE.md` | VERIFIED-WITH-AMENDMENTS (LC1-4, LC1-8, LC1-9, LC1-10, LC1-11) |
| L3 `lemmas/L3_listR.md` | VERIFIED-WITH-AMENDMENTS (LC1-1, LC1-2, LC1-5, LC1-6, LC1-7, LC1-13) |

## 2. Findings

**LC1-1: STATEMENT.md:110, and L3:57-59 — tag F.**
The text reads "every right side tends to 0, because E ε_n → 0 ([POST] …)". That reason does not cover all three terms:
- E ε_n → 0 gives P(ε_n > t) → 0 and P(ε_n ≥ ½) → 0.
- It also gives P(𝓜_nᶜ) ≤ 2E ε_n (RM2R `:60`).
- It does not give P(𝒦_nᶜ) → 0. That comes from RM0-plus (b⁺) with [SAND(Q)], [NA(Q)] and [TL(Q)] (RM2R `:130-132`).

L3 proves the conclusion correctly through (0.1) and (0.2); only the reason given in the claim is incomplete. **Fix:** "…every right side tends to 0: P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0 by RM2-R-plus (RM0-plus (b⁺)), and P(ε_n > t), P(ε_n ≥ ½) ≤ E ε_n/min(t, ½) → 0 by [POST]."

**LC1-2: STATEMENT.md:108-109 and :99, and L3:18-19 — tag S.**
(C3)(ii) states the inequalities for every n. L3 (0.3) proves them only for n with s₀ ≤ K ("all statements below are for such n"), and RM2R defines 𝓜_n only "for n with s₀ ≤ K" (RM2R `:54`).

For n with S₀ ∉ Ω, the literal reading makes 𝓜_n = ∅ and ε_n = 1, so the inequalities hold trivially. However, neither STATEMENT nor L3 adopts that convention.

**Fix (either one):**
- add "for n with s₀ ≤ K (all n ≥ n₀, by (L-feas))" to (C3)(i)–(ii); or
- add to §1 the convention "𝓜_n := ∅ when S₀ ∉ Ω (then π(S₀ | y) = 0, ε_n = 1)", plus one sentence in L3 Step 2 saying the bounds are then trivial.

**LC1-3: STATEMENT.md:96-97, the (C3) preamble "[they are] implied by the reader assumptions (A1)–(A6) … through its bridges B6.1–B6.4" — tag F.**
L3 does not establish this, and says so (L3:23-24). Two of the four bridges are not checked inputs: `READER_VERSIONS.md:755` (B6.1) and `:757` (B6.3) are marked **NEW**. B6.2 is an identity and B6.4 is EXISTS-CHECKED.

The sentence is inside the claim span, but it is neither proved here nor listed among the consumed ids in §6. **Fix:** move it to §5 as a remark, or reword it as "(by READER §6, bridges B6.1–B6.4; B6.1 and B6.3 are NEW and pending their check — not consumed by this file)".

**LC1-4: L2:67-77 (B4) — tag F.**
B4 says LS0 in the run "coincide[s] with the deterministic LS0 of the definition of 𝒦_n", and cites RM `STATEMENT.md:52-53` and `:59-67`. Those lines define 𝒦_n only as "complete scans, cap ℓ_n + |S̃₀|, started from the coded start mode". They do not give the scan order, the lexicographic tie-break or the strict-improvement and stop rules, so the citation does not support "the same models in the same order".

The theory's definition of that search is in the code pins at W3-RM2 `STATEMENT.md:60-67`, which RM2R `:39-41` imports: centre and cap at `v3_core.cpp:465-476`, scan at `v3_engine.h:394-406`, ties at `:392`, strict improvement at `:408`, stop at `:409-414`. In addition, "W3-RM:E4 for the centre" is not an input of LIST-CODE and is not needed, because 𝒦_n is defined from the coded start mode itself.

**Fix:** cite W3-RM2 `STATEMENT.md:60-67` (via RM2R `:39-41`) for the identity of the search, and delete the E4 reference or mark it as context only.

**LC1-5: L3 Step 0 — tag E (scope bridge).**
STATEMENT §1 sets p = p_ret, which defines Ω, K, ℓ_n and capacity 40p + 1. RM's Setting R and POST are stated for the design's p.

Under Setting R (Gaussian rows, n ≥ 3), no column is constant with probability 1. The code drops a column only when all its entries are exactly equal (`v3_preprocess.R:111-112`). So p_ret = p almost surely, and Ω, K, ℓ_n and 𝒦_n coincide almost surely. L3 uses this silently, for example when it applies POST (b) to ε_n defined on Ω(p_ret). **Fix:** add this sentence to Step 0.

**LC1-6: L3:27-29 — tag E.**
"Either branch" needs the fact that output occurs only on the two branches, and L3 does not state it. `estimates_available` becomes TRUE only at `v3_fit.R:129` (exact branch) or through `:171` from `v3_run.R:218` (sampler branch). Both come after `branch_run` is set at `v3_fit.R:106`. The earlier returns at `:89` and `:102` keep the initial FALSE (`:78`). **Fix:** add one sentence with these citations.

**LC1-7: L3:32-34 — tag E.**
The identification `pip_list` = pip_𝒯 and the others under IMPL-LIST needs SPEC §4's exceptional rows not to fire:
- non-finite score → fields NA;
- empty list → NA;
- duplicates → error.

L2 (iii) excludes all three, but L3 does not say so. The values are F(S), which is finite under EX-A (Lemma S.2, RM2R `:151-152`). 𝒯 contains S₀, so it is not empty. 𝒯 consists of distinct models. **Fix:** add this sentence. It is also why `pip_list` is never NA on an output run, which (C3)(i) uses without saying so.

**LC1-8: L2 line citations — tag E.**
The code content is correct; only these line ranges are off:

| cited | correct |
|---|---|
| `v3_engine.h:379-424` | `:379-419` (the file has 422 lines) |
| `v3_engine.h:381, :386, :389` (`ev`) | `:381, :386, :390` |
| `v3_score.h:271-281` (`find`) | `:274-282` (`same` is at `:271-273`) |
| `v3_core.cpp:524-570` | `:524-568` |
| `v3_core.cpp:539-555` (`rec`) | `:537-555` |
| `v3_core.cpp:541` (F) | `:539` (`:541` is `count += 1`) |
| `v3_core.cpp:543-547` (rescaled log-sum-exp) | `:542-547` |
| `v3_core.cpp:483-507` (`catch`) | `:483-508` |

**LC1-9: L2:98-113 (D2) — tag E. Unstated premises, all true at the pin.**
- (a) "Two entries are equivalent iff they carry the same model" needs every model vector to be in sorted (canonical) form. Otherwise `lex_less` would separate one set written in two orders. This holds:
  - `to_internal` sorts (`v3_core.cpp:34`);
  - blocks are sorted (`v3_blocks.h:141`), so table models are sorted;
  - `start_mode` sorts (`v3_start.h:287`);
  - `sorted_insert`/`sorted_erase` keep order (`v3_util.h:129-130`);
  - the enumeration pushes increasing j.

  State this, with these citations.
- (b) "cap = 40p + 1 ≥ 41" needs p_ret ≥ 1 on both branches. This holds because a run with no retained column returns `no_predictors` at `v3_fit.R:99-102`, before branching. Cite it.
- (c) The induction should treat the first offer, when no e* exists yet, explicitly. This is trivial.

**LC1-10: L2:50 (B2) "the island loop ran all four islands" — tag S (quantifier over R′).**
The argument does not use the number of islands. `cpp_final_run` reads `o.islands` from `ro` (`v3_core.cpp:396, 443`), and that is `4L` only through `v3_run.R:91`. As written, (C2)(i) and (C3)'s "every … R′" quantifier look tied to R′ = 4. **Fix:** "all `o.islands` islands (4 at `v3_run.R:91`; the argument holds for any value)".

**LC1-11: L2:89 (Step C), "(= 𝓜^run, by A3 and B3)" — tag E.**
B3 covers only the models LS0 evaluates. "The scored set of the final run = 𝓜^run" needs:
- CC2 (a)–(b), for every `eval` and `held` event;
- CC2's "Other offers", for tables and inherited models (`CC_code_check.md:48-57`);
- conversely, every offered model was scored: tables at `v3_start.h:93`, inherited models at `v3_core.cpp:426`, evaluations at `v3_engine.h:92`.

**Fix:** cite these instead of B3.

**LC1-12: L1 — tag E.**
- (i) (c) cites (e) for pip_Ω = PIP, and (e) cites (c) for MPM = S₀. This is not circular, because the identity in (e) uses only (0.2). Still, state the identity (m = 1 ⇒ π_Ω = π) before (c).
- (ii) L1 assumes F : Ω → ℝ (so w > 0, which (0.1) and (0.3) use), while (C1) only says "Z < ∞". They agree because §1 defines F = log ϖ + log m, which is real-valued. Make (C1)'s hypothesis read "F real-valued on Ω (so 0 < Z < ∞)", or note this in L1's Setting.

**LC1-13: L3:15-16 (0.1) — tag E.**
L3 gets P(𝒦_nᶜ) → 0 "by (a′)". RM2-R-plus lists the conclusions of RM0-plus "(a), (b⁺)" (RM2R `:180`), and (b⁺) states P(𝒢⁺_n) → 1 directly under [MODE], [SAND(Q)], [NA(Q)] and [TL(Q)] (RM2R `:131-132`). **Fix:** cite (b⁺), which is a stated conclusion of the consumed theorem, rather than (a′).

**Not a finding (recorded for completeness).** (C3)(iii) "for every … N_e, R′" under (D) depends on RM2R (c⁺) (`:135-140`), which already asserts DLV-0 for every admissible run. DLV-0's own text is about `v3_fit`, where N_e comes from the budgets and R′ = 4k under CONFIG. LIST-R takes over that reading unchanged, which is faithful to the source.

## 3. Interpretive sentences inside the claim spans

| # | location | sentence | established? |
|---|---|---|---|
| 1 | (C1)(b), :66 | "in particular max_j \|pip_𝒯(j) − PIP_j\| ≤ ε_n" | Yes (L1:31, 𝒜 = 𝒜_j) |
| 2 | (C1)(d), :68-69 | "hence log Z + log(1 − ε_n) ≤ logZ_𝒯 ≤ log Z and, if ε_n < 1, … ≤ ε_n/(1 − ε_n)" | Yes (L1:41-43). "If ε_n < 1" always holds (L1 (0.3)). |
| 3 | (C2)(i), :79 | "i.e. if and only if the run is in 𝒪" | Yes on the sampler branch (L2 B1). It identifies 𝒪 with DLV-0's "returns with `estimates_available = TRUE`" (RM2R `:144-147`, as used in (c⁺) `:135-136`). That identification is definitional, and acceptable. |
| 4 | (C2)(i), :82 | "in particular on 𝒦_n, S₀ ∈ 𝓜^run" | Yes (B3 + B4); citation to be fixed (LC1-4) |
| 5 | (C2)(ii), :83-84 | "…, which is the reported model Ŝ⁺ of RM and RM2R" | Yes. It is definitional (RM `:54`: Ŝ⁺ = reported model), and the content (hpm_better-max of 𝓜^run) matches C-DLV L4 `:68-69`; LC1-11 for the scored-set equality. |
| 6 | (C2)(v), :90 | "Consequently, if F(S₀) > F(S) … then …" | Yes (L2 Step F). It presumes S₀ ∈ Ω, which is implicit in 𝓜_n. |
| 7 | (C3) preamble, :96-97 | "[hypotheses] are implied by the reader assumptions (A1)–(A6) … READER §6" | **No.** Not proved in L3, and it rests on NEW bridges B6.1 and B6.3 (LC1-3). |
| 8 | (C3) preamble, :97 | "so that P(𝒢⁺_n) → 1 (RM2-R-plus)" | Yes (L3 (0.1); cite (b⁺), LC1-13) |
| 9 | (C3)(ii), :110 | "and every right side tends to 0, because E ε_n → 0" | The conclusion is established (L3:58-59). The stated reason is incomplete (LC1-1). |
| 10 | (C3)(ii) rate, :111-112 | "ε_n = O_P(r_n) ((T1-R) … is hypothesis LSF of POST …; POST (b))" | Yes (RM `:129-133`; L1_POST `:23-25`, `:31-33`, setting `:8-18`; p ≥ 2 matches POST's p ≥ max(2, s₀)). It needs p_ret = p a.s. (LC1-5). |
| 11 | (C3)(iii), :117-118 | "Then every admissible run returns output (DLV-0), so … P(B₄) → 0 and …" | Yes (L3 Step 3: P(𝒪ᶜ) = 0 by (0.4)). |
| 12 | (C3)(iii), :120 | "i.e. the two PIP errors and … the evidence error are O_P(r_n)" | Yes (L3:74-75). I checked the diagonal construction: t_n = k r_n ≤ √r_n ≤ ¼, t_n/r_n = k → ∞, and P(X_{n_k} > t_{n_k}) ≥ η is a contradiction. |

## 4. Verdict

LC1-VERDICT: VERIFIED-WITH-AMENDMENTS
