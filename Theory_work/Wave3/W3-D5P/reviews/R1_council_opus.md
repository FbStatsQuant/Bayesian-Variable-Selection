## W3-D5P council review, round R1, seat `opus`

Read-only throughout; nothing written. `manifest.py verify` → `verify: OK MANIFEST 952d9840…`. I read every frozen file of the ticket except LOG, CHECKPOINT and the earlier reviews, plus the external inputs. I opened the cited code lines at the pin (`v3_core.cpp:358-568`, `v3_engine.h:60-130, 265-300, 370-420`, `v3_ledger.h:25-115`, `v3_score.h:30-72, 255-296`, `v3_util.h:115-130`, `v3_fit.R:70-174`, `v3_run.R:80-229`, `v3_exact.R:1-19`, `v3_preprocess.R:105-115`).

### 1. Per-claim table

| id | decision |
|---|---|
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |
| W3-D5P:LIST-R | ACCEPT (conditional on IMPL-LIST), subject to the one-line fix in finding 1 |

### 2. Findings

**1. [C] (minor) `lemmas/L3_listR.md:25-27, 80, 92`, and Step 1 `:37` onward. One step is not written: moving the facts proved for the pinned core over to the method that has the list fields.**
- **What fails.**
  - LIST-CODE (L2) is a code reading of core 4676af6.
  - DLV-0 (RM2R `STATEMENT.md:144-147`) is a statement about `v3_fit` "core as pinned".
  - LIST-R is about the method *after* the pending commit, because the fields do not exist at the pin.
  - Step 1 applies L2 (i)–(v) to the output runs of that later method. Step 3 uses (0.4), that is DLV-0, to get P(𝒪ᶜ) = 0 for it.
  - No step says why 𝒪, `status`, `hpm`, `top_store` and `fit$exact` of the post-commit fit equal those of the pinned fit. No step says the post-commit fit returns whenever the pinned one does.
  - SPEC §4 does let the new code stop with an error on duplicate models.
  - The remark at `:92` says IMPL-LIST "is used only to identify the printed fields". That is inaccurate: IMPL-LIST's "changes no other field and no other state" carries the transfer.
- **Fix.** Add a step (0.5) to L3:
  > By IMPL-LIST (SPEC §7 A.1–A.2), on every input and every run realisation the post-commit fit returns if and only if the pinned fit returns, with every existing field identical. The only SPEC §4 row that stops with an error (duplicates) cannot fire, because by L2 (iii)/(iv) the store and 𝒯^ex hold distinct models. Hence 𝒪, `status`, `hpm`, `top_store` and `fit$exact` are those of core 4676af6, and L2, RM0-plus and DLV-0 apply.

  Then correct the remark at `:92`.

**2. [F] Three derived texts drop STATEMENT's "when `log_Z_list` is not NA" qualifier. The places are `REPORT.md:66` (REGISTRY LIST-R conclusion), `CARD.md:10` (Option A: "the list evidence lies in [π(S₀|y)Z, Z]"), `CARD.md` Option B, and `READER_DELTA.md:23` (display).**
- **What fails.** (C3)(i)–(iii) state the evidence sandwich and rate only "when `log_Z_list` is not NA" (`STATEMENT.md:107, 111, 121, 125`). L3 proves only that form on the exact branch (`L3:51-53`). The derived texts state it on every output run.
- **Fix.** Either add "(where `log_Z_list` is defined)" to the three texts, or, preferably, prove that NA never happens and drop the qualifier everywhere. The argument:
  - At the pin `fit$exact <- e` contains `top` (`v3_fit.R:122`, `cpp/v3_core.cpp:565`).
  - IMPL-LIST changes no other field, so the store is returned.
  - SPEC §4 then computes `log_Z_list` from it: nonempty, distinct, finite under EX-A.
  - So it is never NA on an output run.

**3. [F] `CARD.md:10`, "Why it matters" column: "Consistency of printed estimates … on AR and block designs, which row 3.6 does not reach". Also `READER_DELTA.md:28`: "every design inside Theorem 6 — AR and block designs included —".**
- **What fails.** STATEMENT §5 remark 1 and REGISTRY scope (`REPORT.md:68`) both say "included **when they satisfy (A1)–(A6)**". The card sentence drops that, so it reads as a claim about all AR and block designs. Row 3.6 of the current card was corrected for exactly this reading ([R1-F5]: "for particular AR or block designs that satisfy Theorem 6's … conditions").
- **Fix.** Use "on AR and block designs that satisfy Theorem 6's conditions, which row 3.6 does not reach", and the same in READER_DELTA.

**4. [F] (minor) `REPORT.md:43`, REGISTRY LIST-K "scope: any finite model space and any score".**
- **What fails.** (C1) carries the explicit hypothesis "F real-valued on Ω, so 0 < Z < ∞", added in v1.1 [LC1-12]. "Any score" drops it. With F(S₀) = −∞, Z_𝒯 can be 0 and π_𝒯 is undefined.
- **Fix.** "scope: any finite set of models Ω and any real-valued F on Ω (as (C1)); applied with Ω = {|S| ≤ K} and the coded F."

**5. [E] `STATEMENT.md:79-80`.** The (C2) gloss of "shipped configuration" omits `ls0_ell = ℓ_n`. B4 (`L2:131`, cap ℓ_n + |m.S|) needs it, as does the identification with 𝒦_n's cap. RM §1 includes it. Add it.

**6. [E] Stale headers.**
- `REPORT.md:4` says "STATEMENT.md (v1.0 LOCKED)"; the file is v1.1.1.
- `L1:3`, `L2:3` and `L3:3` say "not yet line-checked", which contradicts the REPORT statuses.
- `TARGET.md:1` says "v0.1 with STATEMENT v0.1".
- The brief calls STATEMENT "v1.1"; the frozen file is v1.1.1.

**7. [E] `REPORT.md:50-52`, REGISTRY LIST-CODE.**
- The premises pointer `STATEMENT.md:29-38` leaves out `:49-57`, where 𝒯 and 𝒯^ex are defined.
- The assumptions list "A:OP ; A:EX-A" while (C2) uses EX-A, EX-S, SR and the shipped configuration. Either confirm that A:OP covers EX-S and SR, or list them.

**8. [E] `READER_DELTA.md:13`.** "A completed run returns … a list" — on the exact branch the status is `exact`. Say "A run that produces output".

**9. [E] `TARGET.md:22`.** The parity verdict "beats 3.6 in scope (AR/BLK)" should say "(AR/BLK designs inside Theorem 6)", as in finding 3.

**10. [E] `DEPS.tsv`.** `checked_sha` records the hash after the fixes, while the checkers (LC1, LC1R) read earlier versions. A note "(post-fix; checker read <sha>)" would make this honest. All four sha256 prefixes match the files (finding-free, see sweep 5).

*Note (not a finding):* in `L2:86-88`, A4's "∅ ∈ 𝓜^run" depends on `logm_tab[b][0]` not being NaN. No claim needs it: nonemptiness also follows from the island and LS0 evaluations.

**Missed-path hunt for LIST-CODE (all clean).**
- **Writers of the HPM.** `hpmS` is assigned only in `offer_hpm` (`v3_ledger.h:86`). Its callers are `offer_stores` (`:90`) and the numerical-failure handler (`v3_core.cpp:502`), which runs only after `status = "numerical_failure"`.
- **Writers of `top`.** `top.offer` is called only at `v3_ledger.h:91`. The enumeration's `top` (`v3_core.cpp:531, 549`) is a separate object.
- **`emit = false`.** The only emit=false evaluation is `eval(C, ME_LOCAL, emit_centre)` with the centre `led.hpmS` (`:456`). That model was already offered, and `set_model` copies the centre, so there is no aliasing.
- **Cache.** Inserts happen only at `v3_engine.h:93`, after a miss in this run's empty cache (`v3_core.cpp:409`). A clear (`v3_score.h:284`) causes only a later re-offer that changes nothing.
- **`held`.** Never used by `local_search`.
- **Top-store eviction.** `TopStore::offer` (`v3_ledger.h:49-57`) erases only `prev(end)` of a set of size cap + 1 ≥ 42, so the best entry is never evicted. The quick-reject rule cannot reject an entry that is strictly before the last.
- **"Completed" without LS0.** `status` starts as "completed" and is only ever demoted (`:451, :459, :480, :484`). `stop()` at `:425` and `:474` throws an R error and no fit is returned.
- **`tier`.** Read in `local_search` only into `ev` (`v3_engine.h:381`), so it is bookkeeping.
- **LS0 cap.** `b$ell` depends on (n, p) only (`v3_run.R:91, 95`).
- **`v3_fit` exits.** On the sampler branch, `estimates_available` is TRUE only via `v3_run.R:218` → `v3_fit.R:171`, and `finish` (`:85`) leaves it alone when TRUE.

### 3. Interpretive sentences inside (C1)–(C3)

| location | sentence | verdict |
|---|---|---|
| (C1)(b) `:70` | "in particular max_j \|pip_𝒯(j) − PIP_j\| ≤ ε_n" | proved (L1 (b), "PIPs") |
| (C1)(d) `:72` | "hence log Z + log(1 − ε_n) ≤ logZ_𝒯 ≤ log Z" | proved (L1 (d), with (0.3)) |
| (C2)(i) `:83` | "i.e. if and only if the run is in 𝒪" | proved (L2 B1, with 𝒪 = `estimates_available` TRUE as in DLV-0, RM2R `:146`) |
| (C2)(i) `:86` | "in particular on 𝒦_n, S₀ ∈ 𝓜^run" | proved (L2 B4 + B3) |
| (C2)(ii) `:87` | "…which is the reported model Ŝ⁺ of RM and RM2R" (relative clause) | proved (L2 Step C; C-DLV L4 `:66-70`) |
| (C2)(v) `:94` | "Consequently, if F(S₀) > F(S) …" | proved (L2 Step F) |
| (C3) preamble `:101` | "so that P(𝒢⁺_n) → 1" | proved by citation (RM2R `:131-132`, RM0-plus (b⁺), a conclusion of RM2-R-plus `:180`) |
| (C3)(iii) `:122-123` | "so for every seed … without 'on output': P(B₄) → 0 …" | proved for the pinned core; for the post-commit method it needs the transfer step of finding 1 |
| (C3)(iii) `:125` | "i.e. the two PIP errors and … the evidence error are O_P(r_n)" | proved (L3 Step 3, contradiction argument; I checked the construction of t_n: t_n ≤ √r_n ≤ ¼, t_n/r_n = k → ∞) |

### 4. Sweep duties

**(1) Statement copies against the lemmas.**
- (C1)(a)–(e) match L1 (a)–(e) clause by clause. The attainment in (b) at 𝒜 = Ω∖𝒯 is correct. The strict-½ example in the L1 remark is right.
- (C2)(i)–(v) match L2 Steps B–F.
- (C3)(i)–(iii) match L3 Steps 1–3. The 2t evidence bound uses ε/(1−ε) ≤ 2ε for ε ≤ t < ½, which is correct.
- Markov: P(ε_n ≥ ½) ≤ 2Eε_n ≤ Eε_n/t, consistent with `min(t, ½)`.

**(2) Quantifiers and uniformity.**
- The inclusions are pathwise in the run, and the right-hand sides are data events independent of seed, N_e, R′ and calibration outcome. That gives uniformity, and either branch is covered (L3 Step 1 handles both).
- There is one data event 𝒢⁺_n, and 𝒢♯_n for the rate.
- t ∈ (0, ½) is used strictly (needed for (c) and for the 2t bound).
- The rate needs p ≥ 2: POST's setting is p ≥ max(2, s₀) (`L1_POST.md:10`). In reader form (S2) gives 2 ≤ p ≤ n^A (`READER_VERSIONS.md:29`), so the card's unqualified rate is fine.
- The NA qualification is consistent in STATEMENT and L3, not in the derived texts (finding 2).
- The convention for s₀ > K is handled at `L3:19-20`.
- p_ret = p almost surely under Setting R (`L3:21-24`; preprocessing drops only columns that are exactly constant).

**(3) Lemma scopes against downstream use.**
- L3 applies LIST-K to 𝒯 ∋ S₀ with 𝒯 ⊆ Ω (from L2 (iii) and (v)), with F real-valued (scores finite under EX-A via Lemma S.2, since yᵀy > 0 almost surely).
- It applies LIST-K (e) on the exact branch.
- It applies L2 (i) and (v) on 𝒦_n ∩ 𝓜_n.
- All of these are within scope, except that the scopes are proved at the pin while the use is post-commit (finding 1).

**(4) REPORT and REGISTRY against STATEMENT.**
- REPORT restates no claim text.
- Line pointers are correct: `:22-24, :59-63, :67-75, :79-95, :82-88, :99-101, :99-125`.
- `status_source` REPORT.md `:17/:18/:19` is correct.
- IDs and statuses are consistent with §6. Depends_on agrees with DEPS.
- Problems: the stale "v1.0 LOCKED" (finding 6), the REGISTRY LIST-K scope (finding 4), the REGISTRY LIST-R NA qualifier (finding 2), and the LIST-CODE premises and assumptions (finding 7, E).

**(5) DEPS.tsv.** I checked every row's sha prefix against the manifest hashes, which `verify` confirms against the files:

| file | prefix |
|---|---|
| STATEMENT.md | `c594e61e72581ad7` |
| L1 | `408e2e4e2c4fedb7` |
| L2 | `1accddb36dd7004c` |
| L3 | `f014059f08d9f2f4` |

All match. Only the convention for `checked_sha` is open (finding 10, E).

**(6) CARD.md and READER_DELTA against STATEMENT.**
- Hypotheses are stated as "those of Theorem 6", with nothing added. IMPL-LIST appears only as a status condition, which is correct.
- 𝒢_n in READER_DELTA: the reader's 𝒢_n (remark (i): 𝓜_n ∩ Sand ∩ NA ∩ TL) is a subset of 𝒢⁺_n, so the pathwise conclusions hold on it.
- No clause goes beyond LIST-R and LIST-CODE.
- Two exceptions: the NA qualifier is dropped (finding 2), and the AR/block qualifier is dropped (finding 3).

### 5. The six gates

| gate | result | reason |
|---|---|---|
| correct | **FAIL** | One minor C (finding 1): the transfer from pin to commit is unwritten. Every other step checks, including the full missed-path hunt above. |
| strength | PASS | No clause is weaker than what the cited inputs give, apart from the vacuous NA case (see note). |
| faithfulness | **FAIL** | Findings 2, 3 and 4 (derived texts against STATEMENT). Code faithfulness of LIST-CODE is clean. |
| lit | PASS | The TARGET parity rows are fair and name the different (list-based) output. Song–Liang is cited as in the card [AUD-S4]. The "beats in scope" wording needs the qualifier in finding 9 (E). |
| necessity | PASS | No necessity claim is made. "Sharp up to √log n" concerns 1 − π(S₀) and cites W3-POST Thm-1 item 7, which exists (`W3-POST/STATEMENT.md:101-104`). |
| better | PASS | No credible, substantively better statement within scope is left undispositioned. |

*Note (stronger statement, not a finding):* under IMPL-LIST, `log_Z_list` is never NA on an output run (argument in finding 2). The NA qualification in (C3) is therefore vacuous and can be dropped; either adopt this or record it in TARGET §4.

### 6. Verdict

Mathematically the ticket is sound. LIST-K is airtight, LIST-CODE survives a full hunt for missed code paths, and the LIST-R assembly is right. The defects are one unwritten one-line transfer step (pinned core to the method with the list fields) and three places where derived texts drop a qualifier STATEMENT carries. The binding rule makes gates FAIL.

```
COUNCIL-VERDICT round=R1 manifest=952d9840170cc7b4f740493c451f91952a1f1077e3ed8574328cf4f1bd21f00a seat=opus score=8.4 gates=FAIL
```
