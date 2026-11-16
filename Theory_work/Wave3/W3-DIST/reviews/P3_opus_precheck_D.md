# P3 pre-check, stream D — Lemma P6, Theorem DIST-C, Corollary C

Checker: Claude Opus 5.5 (same family), independent line check, effort high. 2026-11-15.
Files checked: `work/D_output/P6_DISTC.md` (all sections), `work/D_output/COR_C.md` (all sections),
`work/D_output/check_store.py` (re-run: output reproduced exactly, "store invariant and retention: OK, 3000 trials",
"Lemma P6 (a), (b): OK, 2000 trials"). Targets: `STATEMENT.md` v1.3.1 §2, §1R Corollary C, §3 Lemma P6.
Also read: `W3-SAMP/STATEMENT.md` §0–§2, `W3-SAMP/lemmas/CC_code_check.md` (CC2, CC5), `PC_completed.md`,
`D_theorem.md` (cited lines), `W1-N1/STATEMENT.md:69-81`, `W3-RM2/STATEMENT.md:204-210`, and the code
(`Scripts/SMC_BVS/core/`: `v3_run.R`, `v3_fit.R`, `v3_preprocess.R`, `v3_setup.R`, `cpp/v3_ledger.h`, `cpp/v3_core.cpp`,
`cpp/v3_engine.h`, `cpp/v3_util.h`, `cpp/v3_score.h`, `cpp/v3_start.h`, `v3_calib.R`, `v3_exact.R`).
Not read (per the common rules): `reviews/` (other than writing this file), `LOG.md`, `CHECKPOINT_*`, `DEPS.*`.

**Code identity.** I recomputed the SHA-256 of the eleven files listed in `pins_sha256.txt`: all eleven match. So the line
numbers below refer to the same text the author read. The commit identity (4676af6 / fe9a1d7) was not checked (no git).

---

## 1. Code pins re-verified (all 33 pins P1–P33, plus the in-text pins)

Each line was opened and read; "OK" means the cited lines say what the file claims.

| pin | claim | result |
|---|---|---|
| P1 `v3_run.R:142` | `out$hpm <- led$hpm$model` | OK |
| P2 `v3_run.R:159-162` | island PIP matrix; `pip_r`; `pip_primary <- rowMeans(P)` | OK |
| P3 `v3_run.R:163` | `out$mpm <- as.integer(orig[out$pip_primary > 0.5])` | OK |
| P4 `v3_run.R:154` | pooled `log_Z` | OK |
| P5 `v3_run.R:210` | `out$top_store <- led$top` | OK |
| P6 `v3_run.R:143-149` | non-completed: early return with `out$ledger <- led`; `top_store` absent (it is not in `V3_ESTIMATE_FIELDS`, `v3_run.R:109`, so `v3_unavailable_estimates` does not create it) | OK |
| P7 `cpp/v3_core.cpp:358-366` | `store_to_list` iterates the `std::set` (comparator order), `value = e.v` | OK |
| P8, P10 `cpp/v3_ledger.h:43-57` | quick reject `:52`, duplicate reject `:53`, insert + erase last `:54-55` | OK |
| P9 `cpp/v3_ledger.h:78` | `top.init(40 * p + 1, true)`, `p = d->p` | OK |
| P11 `cpp/v3_ledger.h:35-42` | `TopCmp`: v desc, then size asc (hpm_order), then `lex_less` | OK |
| P12 `cpp/v3_ledger.h:84-94` | `offer_stores` calls `offer_hpm` then `top.offer(F, S)` | OK |
| P13 `cpp/v3_ledger.h:104-113` | `if (is_fresh) offer_stores(...)` at `:112` | OK |
| P14 `cpp/v3_util.h:117-126` | `lex_less`, `hpm_better` = same three-level order | OK |
| P15 `cpp/v3_engine.h:89-101` | cache miss → score, insert (`:93`); `F = logprior + lm` (`:97`); event with `fresh ‖ !cache` (`:99`) | OK |
| P16 `cpp/v3_engine.h:103-105` | `held`: `is_fresh = false` | OK |
| P17 `cpp/v3_engine.h:379-382` | centre `eval(C, ME_LOCAL, emit_centre)` | OK |
| P18 `cpp/v3_core.cpp:407-411` | new `Ledger`, `ingest_tables`, new empty `ScoreCache`, `E.cache = &cache` | OK |
| P19 `cpp/v3_core.cpp:372-386` | every non-NaN table code → `led.event(..., true, ...)` | OK |
| P20 `cpp/v3_core.cpp:418-429` | size check `:425`; rescored; `offer_stores` `:427` | OK |
| P21 `cpp/v3_core.cpp:443-452` | stream `9 + r`; partial → `resource_limit` | OK |
| P22 `cpp/v3_core.cpp:456, 459, 476, 480, 483-484` | as claimed | OK |
| P23 `cpp/v3_core.cpp:502` | the only `offer_hpm` call outside `offer_stores` (grep over `cpp/`) is in the `catch` | OK |
| P24 `cpp/v3_score.h:237, 284` | throw after last fallback; clear when full. Also: `find` compares the full model (`same`, `:271-277`), so a hash collision cannot produce a false hit | OK |
| P25 `cpp/v3_score.h:40, 61-70` | `K = min(p, n/2)`; `logprior[k] = logw[k] − logWK` | OK |
| P26 `v3_preprocess.R:111-115`, `v3_fit.R:118` | drop exactly-constant columns; `y_constant` status; context on `kept` | OK |
| P27 `v3_preprocess.R:19-32`, `cpp/v3_core.cpp:72-85` | SMC iff Σ_{k≤K}C(p,k) > (5H₀ + 4N₀)p; N₀ ≥ 2500, H₀ = ⌈512N₀/2500⌉ ≥ 512 ⇒ threshold ≥ 12560p | OK |
| P28 `v3_fit.R:120-132` | exact branch; statuses "exact" / "numerical_failure" only (`cpp/v3_core.cpp:536, 556`) | OK |
| P29 `v3_fit.R:154-160, 162, 171` | return before final run unless calibration "ok"; copy of every field | OK |
| P30 `v3_run.R:121, 218` | status copied; `estimates_available <- TRUE` only on the completed path; `finish` (`v3_fit.R:79-87`) does not alter `status` | OK |
| P31 `cpp/v3_core.cpp:341-348` | no particle states returned | OK |
| P32 `cpp/v3_start.h:92`; P33 `cpp/v3_engine.h:116, 397` | size-K guards | OK |
| in text: `cpp/v3_engine.h:290-291, 131/158/179/191, 122/153/174/186` | init `set_model` + `eval(ME_INIT)`; `P = tmpQ` after `eval(tmpQ)` | OK |
| in text: `cpp/v3_core.cpp:608-613, 728-735` | calibration ledger with own cache and tables; export = union of its three stores | OK |
| in text: `cpp/v3_score.h:253-254` | see D-06 (a comment, not an assertion) | OK as content |

No pin was wrong. Two ranges are loose (P8, P28) and the author already marks them "OK (range)".

## 2. Retention induction (Lemma R, R0, R1) against `cpp/v3_ledger.h`

- **Ordering.** ≺ = (F desc, |S| asc, `std::lexicographical_compare`) is exactly `TopCmp{true}` and `hpm_better`. Strict
  total order on Ω under EX-A (F real by Positivity). Correct.
- **Capacity.** `40 * d->p + 1` with `D.p` = number of kept columns (P25, P26). On the SMC branch p_ret is large, so k ≥ 81
  is safe; the `cap == 0` branch is unreachable.
- **Duplicates.** `std::set` equivalence ⇔ neither compares less ⇔ (same v and same S). Under EX-A every offer of S carries
  F(S) (eval, tables, inherited: all `logprior[|S|] + logm`), so equivalence ⇔ same S. Correct. (Outside EX-A this needs
  the scorer to return the same bits for the same S across the three sources — setup tables, `eval`, the fresh `Scorer` of
  the inherited loop; Remark 6.3 covers this.)
- **Ties.** Fully resolved by size and lexicographic order; the quick reject uses strict `cmp(e, last)`, so an entry tied
  in F with the last one but later in ≺ is rejected, which is what top_k requires.
- **Induction cases.** I re-did all three cases. Case 1 (S already offered): if |s| < k then s = A ∋ S and `count` rejects;
  if |s| = k and S ∈ s, either `cmp(e, last)` fails (S = last) or `count` rejects; if S ∈ A ∖ s then last(s) ≺ S and the
  quick reject fires. Case 2 and Case 3a, 3b are correct; in 3b `std::prev(s.end())` after insertion is last(s) because
  S ≺ last(s). The python mirror in `check_store.py` matches the C++ line by line (tuple key (−v, |S|, S) = `TopCmp`).
- **HPM = first entry (R1).** `offer_hpm` sees exactly the offers of `top` on a completed run (P12, P23), and replaces iff
  strictly better; induction gives the ≺-minimum. Correct.

**Lemma M** (𝓜 = tables ∪ inherited ∪ evaluated). Correct. I checked every `eval`/`held`/`event`/`offer_*` call site in
`cpp/` (grep). The only `emit = false` evaluations in the final run are the centre of the final local search (`:456`),
which is `led.hpmS`, an offered model. Cache hits are exact-model hits. See D-05, D-07 for two small presentational gaps.

## 3. Lemma P6

(a) and (b): recomputed; correct as stated, with a > 0 in (b). (TP) holds because Ω is finite and Π(· | S, D_n) is defined
for every S ∈ Ω (π(S) > 0 by Positivity; Positivity itself is correct: completion ⇒ preprocessing "ok" ⇒ y not constant
⇒ b = 0.01·s_y² > 0 ⇒ proper IG and Gaussian slab, m(S) ∈ (0, ∞)).
(c) (mixture convexity): correct. Joint measurability of (ξ, x, y) ↦ φ(y; â_ξ + xᵀb_ξ, v_ξ) holds piecewise (continuous on
each of finitely many pieces); Jensen with √ concave; Tonelli for nonnegative integrands; d_H² ≤ 1.

**Verdict Lemma P6: VERIFIED.**

## 4. Theorem DIST-C

Checked line by line: §0 hypotheses, Positivity, §1 objects, Lemma W, §5 (P⊗-1/2, Lemma J), Proposition C-i°, (C-0),
(C-i)(a)(b), (C-ii)(α-det), (α-disc), (α′), (β), (C-iii)(a)(b)(c), (C-iv), honest label, Remarks 6.1–6.6, §7.

- (C-0), C-i°, (C-i): correct. The inclusion "bad output event ⊆ {D_n ∉ 𝔊_n(t)}" is pathwise, so Lemma J needs only
  (P⊗-1). The predictive clause follows from P6(c) with A = B_n, ε² = C²t/n. Lemma W: π(𝒯) < 1 needs 𝒯 ⊊ Ω, which holds
  on the SMC branch by P27 (|Ω| > 12560p > 40p + 1).
- (α-det): correct (Lemma U: π(S) ≤ 1 − π(S*) < ½ < π(S*); then R1(ii)).
- (α-disc): correct. The quoted D-i text and premises match `W3-SAMP/STATEMENT.md:97-100` verbatim; Lemma PC (i), (iii)
  match `:90-95`; P-OVL matches `:82-83`. The integration step matches `D_theorem.md:46-52`. S₀ ∉ Ω handled (trivial bound).
- (α′): correct; the case Π(B_n | D_n) = 0 is handled.
- (C-iii)(a), (b): correct. Sufficiency of S₀ ∈ 𝓜, δ_n < ½ for P-HIT needs e^{−ct} ≤ ¼ — SCR-1 is right.
- (C-iii)(c), (C-iv): correct. The conditional use of DIST-3 ("for every design in I³_n, outside a noise event") is legitimate
  because the noise is independent of the design (RD). The reported-vs-potential MPM inclusion is Lemma PC (ii) with
  {completed} ⊆ 𝒜, as quoted.
- **Delivery statements (brief duty).** Every delivery statement quotes its W3-SAMP source and premises (§7 table:
  D-i, PC, P-OVL, D-iv, LT-e, C-v, TR-d, LT-f — each quote checked against `W3-SAMP/STATEMENT.md`; line numbers right),
  and every one is intersected with {completed} (or bounded by an 𝒜-event via {completed} ⊆ 𝒜). The one exception is the
  RM2 alternative, which the file itself marks as not verified (D-01).
- Edge cases: s₀ = 0 (S₀ = ∅ ∈ Ω; see D-04: then S₀ ∈ 𝓜 always), s₀ > K (Remark 6.5), dropped true columns (Remark 6.4),
  p ≤ small (SMC branch not taken: everything vacuous), singular Gram (scores use G_S + I; finite), sets outside Ω
  (𝓜 ⊆ Ω by CC5, re-checked).
- Uniformity: one n₀ (DIST-1's); no new constant is introduced except in SCR-1.

### Assessment of the STATEMENT-CHANGE REQUESTS (P6_DISTC.md)

| SCR | justified? | weakens? | comment |
|---|---|---|---|
| SCR-1 (P-HIT sufficiency needs e^{−ct} ≤ ¼) | **Yes.** π(S₀) > ½ gives π(S₀) > e^{−ct/2} only if e^{−ct/2} ≤ ½ | No (DIST-1 holds for every larger n₀, so one may always take n₀ ≥ 4^{1/(cM₀)}) | Simpler wording: "for n ≥ n₀, with n₀ enlarged so that cM₀ log n₀ ≥ log 4" (D-10) |
| SCR-2 ((C-i) fixed-fraction parenthesis) | **Yes.** At λ = 0 the event needs π(𝒯) ≥ 1, empty on the SMC branch | No: (b) contains (a) (take a = e^{−λt}) and is the intended fixed-fraction statement | Accept (b) as the statement |
| SCR-3 (P⊗ is defined in [SAMP] §0, not §1) | **Yes** (`W3-SAMP/STATEMENT.md:29-36`) | No | editorial |
| SCR-4 ("complementary success event") | **Yes**: the literal complement contains stopped runs and small-π(𝒯) runs | No | Accept the proved form |
| SCR-5 (rename q_n → ϱ_n) | **Yes**: clash with the reader window q_n | No | editorial |
| Optional strengthening (C-i pathwise, C-i°) | Correct | STRONGER | Recommend adopting; Corollary C already uses it |

**Verdict Theorem DIST-C: VERIFIED-WITH-AMENDMENTS** (SCR-1 … SCR-5 to be applied by HQ; D-01 to be resolved or labelled).

## 5. Corollary C (COR_C.md)

- (C1): correct. G_n := {Π(d_H > r_n | D_n) ≤ n^{−cM}} is a data event of P*-probability ≥ 1 − n^{−cM} by Theorem A (i);
  on it, Π̂(B) ≤ n^{−cM}/π(𝒯) ≤ n^{−cM/2} for every completed run with π(𝒯) ≥ n^{−cM/2}. Pathwise, any seed, any
  calibration outcome. The reader-parametrisation transfer (S, θ, v) ↦ (ι(S), β, σ²) is a piecewise bijection with the
  same attached density (ȳ + (x − x̄)ᵀβ = â + xᵀb), so Π̂(d_H > r) is the same number. Correct.
- (C2): correct and deterministic; uses Lemma U, R1(ii), Lemma M, EX-A, (H-ID). It does not use Theorem A.
- RC-1 … RC-5: all five are accurate descriptions of the code (checked against the pins in §1). RC-5's dependency line
  is right: no W3-SAMP premise is used.
- Table §4: I agree with all 13 rows.

### Is the proposed reader wording (COR_C §5) accurate and clear?

Accurate: yes, every sentence is true of the code under EX-A. Clear to a reader without our files: mostly. Three
points (D-02, D-03, D-09) would make it cleaner; D-02 also allows a simpler and stronger sentence than the one proposed.

**Verdict Corollary C: VERIFIED-WITH-AMENDMENTS** (reader wording RC-1 … RC-5 / §5 as amended by D-02, D-03).

---

## 6. Findings

**D-01 — MINOR — P6_DISTC.md §6 (C-ii) "Alternative discovery source"; STATEMENT §2 (C-ii)(α).**
The RM2-F/RM2-R route to {S₀ ∈ 𝓜} is cited, not verified. Two links are open: (i) RM2's output event 𝒪 versus
{completed} (the file says so); (ii) RM2-F's conclusion is about Ŝ⁺ ("reports Ŝ⁺ = S₀"); that Ŝ⁺ is the reported `hpm`
of a completed run (so that Corollary R1(i) gives Ŝ⁺ ∈ 𝓜) is not shown either. STATEMENT §2 lists RM2 as a supplier of
P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0 without these qualifications.
*Repair:* in STATEMENT §2 (C-ii)(α), mark the RM2 route "cited; requires 𝒪 ⊇ {completed} and Ŝ⁺ = reported hpm on
{completed} (unchecked)", or drop it (Theorem D (D-i) + P-OVL already supplies the claim, and D-04 covers s₀ ≤ 1).

**D-02 — MINOR — COR_C.md §5 (reader wording, list sentence) and RC-1.**
The proposed sentence "the best-scoring models among all models scored in the run (including those carried over from the
precomputed block tables and from the calibration)" is true, but "carried over from the calibration" is opaque: the reader
cannot know which calibration models are carried over (the union of the calibration's three stores). A simpler and
stronger statement holds (code reading by this checker; under EX-A):
𝒯 = top_k(𝓜 ∪ 𝓜_cal), where 𝓜_cal is the set offered to the calibration ledger. Reason: the calibration uses one ledger for
all its tiers (`v3_calib.R:148`, one `cpp_cal_new`; "persistent stores", `:139`), built on the same `Data` (same
k = 40p + 1, same F under EX-A), with its own cache and the same `eval`/`offer_stores` code (`cpp/v3_core.cpp:608-613`;
its local-search centres with `emit = false`, `:642, 689`, are its own `hpmS`, hence offered). So Lemma R and Lemma M apply
to it: its top store is top_k(𝓜_cal) and 𝓜_cal contains every model the calibration evaluated. That top store is
inherited, so top_k(𝓜_cal) ⊆ 𝓜. Then for T ∈ 𝓜_cal ∖ top_k(𝓜_cal), the k elements of top_k(𝓜_cal) ⊆ 𝓜 rank before T, so
T ∉ top_k(𝓜 ∪ 𝓜_cal); hence top_k(𝓜 ∪ 𝓜_cal) = top_k(𝓜) = 𝒯. (Remark 6.2 is the special case k = 1.)
*Repair:* reader wording "… the best-scoring models among all models the method examined during the calibration and the
final run (its samplers, its local searches, and a precomputed table of small models) …", with the argument above added to
P6_DISTC.md as a lemma (calibration analogue of Lemma M + the merge identity). If HQ prefers not to add the lemma, keep
COR_C's wording but replace "carried over from … the calibration" by "the best models found by its calibration stage".

**D-03 — MINOR — COR_C.md §5 (reader wording, "completed" and "reported highest-probability model").**
(i) The reader is not told that stopped runs also return a partial list (RC-2's point) — add "(runs stopped by a time or
memory limit or by a numerical failure are not covered)". (ii) The retention sentence says "it is the reported
highest-probability model", but the wording never says the output reports one. *Repair:* "Its output then contains the
model it reports as the highest-probability model and a list 𝒯 …", or drop the HPM clause from the reader text (it is
in DIST-C (C-ii)(α-det)).

**D-04 — NIT (missed strengthening; edge case s₀ ≤ 1) — P6_DISTC.md §6 (C-ii)(α-disc), §7.**
Every subset of a single block with size ≤ K is in 𝓜_tab on every completed run (`cpp/v3_core.cpp:376-385`,
`cpp/v3_start.h:89-95`; blocks cover [p], since π₀ is a product over blocks — code reading). Hence if S₀ is contained in one
block — in particular if s₀ ≤ 1 — then S₀ ∈ 𝓜 deterministically, and (α-det) gives S₀ ∈ 𝒯 on {completed} ∩ {δ_n < ½} with
no discovery premise (no H-U, SI, P-OVL). For s₀ = 0 this is the remark "∅ ∈ 𝓜" already in Lemma M.
*Repair:* add one sentence to (α-disc): "If S₀ lies in one block (e.g. s₀ ≤ 1), P⊗({completed} ∩ {S₀ ∉ 𝓜}) = 0."

**D-05 — NIT — P6_DISTC.md §4 Lemma M proof (a), (b).**
(a) lists two ways a particle state is set (`set_model` + `eval`, and `P = tmpQ`) but omits copies by resampling
(`cpp/v3_engine.h:326`), which copy a state already set in one of these two ways. (b) The recursion "apply the same
reasoning to that earlier call" should say explicitly that the first insertion of S into the cache was by a fresh `eval`
that either had `emit = true` (offered) or was the final-search centre (case (c): `led.hpmS`, offered).
*Repair:* add both sentences. The conclusion is unaffected.

**D-06 — NIT — P6_DISTC.md Remark 6.3.** "`cpp/v3_score.h:253-254` asserts this": those lines are a code comment, not a
runtime assertion. *Repair:* "states (code comment)".

**D-07 — NIT — P6_DISTC.md Lemma M, "∅ ∈ 𝓜".** This uses J ≥ 1 block. It is true (blocks cover [p] ≠ ∅), but 𝓜 ≠ ∅ also
follows from the first initial draw of island 1 (a fresh `eval` with `emit = true` on an empty cache). Either reason may
be cited.

**D-08 — NIT — COR_C.md §3 "Relation to DIST-C".** "t = M log n and λ = c/2" mixes Theorem A's c with DIST-1's c and
ignores the radius constant C (DIST-1: C√(t/n); Theorem A: √(M log n/n)). The proof of (C1) does not use this paragraph.
*Repair:* "(C1) is the analogue of Proposition C-i° with Theorem A (i) in place of DIST-1 (1.1) (threshold n^{−cM},
store condition n^{−cM/2})".

**D-09 — NIT — COR_C.md RC-2 and §1 "Completed".** "the final local search and LS0 finished": LS0 runs only when enabled
(`cpp/v3_core.cpp:465`; default `ls0 = TRUE`, `v3_fit.R:73`). Also, an Rcpp error (e.g. `cpp/v3_core.cpp:425`,
`cpp/v3_score.h:230`) aborts the fit with no returned object; harmless for "nothing sets it back", but worth a clause.

**D-10 — NIT — SCR-1 wording.** Since DIST-1 remains true with any larger n₀, state the sufficiency as "for n ≥ n₀ (n₀
enlarged, if needed, so that cM₀ log n₀ ≥ log 4)" rather than as a conditional on the constants.

## 7. What I could not check

- The commit identity of the code of record (no git); the file text is the one the author read (SHA-256 match).
- DIST-1, DIST-2, DIST-3 and Theorem A are given hypotheses; nothing here checks them.
- The RM2 route (D-01): `W3-RM2` was read only at `STATEMENT.md:204-210`.
- D-02's calibration claim is a code reading (calibration call sites `cpp/v3_core.cpp:603-740`, `v3_calib.R:139-186`); I did
  not line-check every calibration `eval` site with the same care as the final run.
- (H-ID) / locked T01 identification of the coded score with the exact posterior: taken as given, as in the file.

## 8. Verdicts

- **Lemma P6 (a), (b), (c): VERIFIED.**
- **Theorem DIST-C: VERIFIED-WITH-AMENDMENTS** — accept SCR-1 … SCR-5 and the optional strengthening C-i°; resolve or
  label the RM2 route (D-01); NITs D-04 … D-07, D-10.
- **Corollary C: VERIFIED-WITH-AMENDMENTS** — accept RC-1 … RC-5; adopt the §5 reader wording with D-02 and D-03; NITs
  D-08, D-09.

**Overall verdict: VERIFIED-WITH-AMENDMENTS — no CRITICAL or MAJOR finding. All 33 code pins and the store
retention induction check out against the code; 3 MINOR findings and 7 NITs.**
