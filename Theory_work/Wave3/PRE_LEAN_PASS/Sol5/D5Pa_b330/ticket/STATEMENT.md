# W3-D5P — STATEMENT v1.1.2 (locked v1.0 + changelog rows v1.1–v1.1.2): the list-restricted outputs on every Theorem 6 design

Ticket W3-D5P = track D ticket #5′ (owner GO, `Theory_work/Dept/DECISIONS.md` D105, dept/theory; standard D106), Tier B
corollary ticket, Theory Wave 3. Lead: Claude Opus 5.5 (effort high). Protocol: `Theory_work/Wave3/PROTOCOL_v4.md` with
`Theory_work/Dept/RIDER_RULES.md` (dept/theory). Status of this file: **v1.0 LOCKED** (2026-11-17) = v0.1 with the three findings of the statement-lock review SL1 applied
(`reviews/SL1_statement_lock_sol.md`: LOCK WITH CHANGES; disposition `reviews/SL1_disposition.md`; markers [SL1-#]). It asserts no proof status.
All results are asymptotic (n → ∞) unless marked *deterministic*. **No method change is requested by this file**; it is
about the new output fields defined in SPEC (below), which the method companion of D105 adds.

**Sources (read-only; abbreviations).**
SPEC := `Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md` @ theory/W3-AUDIT 523dda23 (the definition of the new fields).
RM2R := `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (v1.0 LOCKED; claims @1.0.1 on main). RM := `Theory_work/Wave3/W3-RM/STATEMENT.md`.
SAMP := `Theory_work/Wave3/W3-SAMP/STATEMENT.md` and its `lemmas/CC_code_check.md` (CC). DIST := `Theory_work/Wave3/W3-DIST/STATEMENT.md`.
POST := `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`. READER := `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` (Theorem 6 = card row 3.1).
**Code of record:** `Scripts/SMC_BVS/core/` at 4676af6 (= the core on main 029bb748; last changed at 72785fe). The new
fields are added by a later **method commit, pending** (Engineering; recorded as `method_commit` at CP3).

## 0. What this file adds, in one table

| claim (new id) | kind | what it says | consumes |
|---|---|---|---|
| **LIST-K** (§2) | deterministic lemma | for any list of distinct models containing S₀, the list-renormalised PIPs, median model and evidence sum are within 1 − π(S₀ \| y) of the truth and of the exact posterior | — |
| **LIST-CODE** (§3) | code-reading lemma at the pin | a completed run is an output run of RM; its printed `hpm` is RM's reported model Ŝ⁺; every model the final run scores is offered to the returned list `top_store`, which keeps the best-scored offered model (and the exact branch's list keeps the best model of Ω) | CC (CC2, CC5) |
| **LIST-R** (§4) | corollary (Gaussian rows; Theorem 6's hypotheses) | on one data event of probability → 1, every admissible run that produces output has S₀ in its list and satisfies the bounds of LIST-K jointly with `hpm` = S₀; errors O_P(√(log n/n)); under the delivery premises, unconditionally | LIST-K, LIST-CODE, RM2-R-plus, RM0-plus, DLV-0, POST |

The two links named as unchecked at DIST `STATEMENT.md:297-303` ("whether RM2's output event covers {completed}, and
whether its reported model is `hpm`") are LIST-CODE (i) and (ii).

## 1. Setting, objects and premises

**Base, taken unchanged.** Setting R, the method as coded, the shipped configuration, the implementation premises
(EX-A, EX-S, SR, GUARD-W, OP-LS0, complete scans), "admissible run" (every seed, N_e, R′ and calibration outcome), the
events 𝒪 ("the run returns output"), U_n = 𝒪ᶜ, Sand_n(Q), NA(𝓛), TL(𝓛), 𝒦_n and the reported model Ŝ⁺: RM
`STATEMENT.md:32-68` as used by RM2R `STATEMENT.md:33-50`. The mode event 𝓜_n := {S₀ is the unique maximiser of F on Ω}
and 𝒢⁺_n := 𝓜_n ∩ 𝒦_n: RM2R `STATEMENT.md:54-60, 128-137`. The delivery premises (D) with IDEAL-W⁺ and "valid
non-degenerate input": RM2R `STATEMENT.md:71-93`. Notation: Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋), p = p_ret (the
retained columns, indexed by their original indices); S₀ = supp θ*, s₀ = |S₀|.

**The exact posterior and its summaries (deterministic definitions).** F(S) := log ϖ(|S|) + log m(S) for S ∈ Ω, with ϖ
the coded size prior normalised on Ω (`cpp/v3_score.h:60-70`) and m the coded marginal likelihood (CC2: e^F ∝ π on Ω).
  Z := Σ_{S∈Ω} e^{F(S)},  π(S) := π(S | y) := e^{F(S)}/Z,  PIP_j := π({S : j ∈ S}),  MPM := {j : PIP_j > ½},
  ε_n := ε_n(y) := 1 − π(S₀ | y).
*Convention* [LC1-2]: if S₀ ∉ Ω (i.e. s₀ > K), then π(S₀ | y) := 0, ε_n = 1, and 𝓜_n = 𝒦_n := ∅ (S₀ can then be
neither the maximiser of F on Ω nor scored); every statement below that involves S₀, 𝓜_n or 𝒦_n holds trivially for
such n [LC1R-4].
For a nonempty set 𝒯 ⊆ Ω: π(𝒯) := Σ_{S∈𝒯} π(S), Z_𝒯 := Σ_{S∈𝒯} e^{F(S)}, π_𝒯(S) := e^{F(S)}/Z_𝒯 (S ∈ 𝒯), and
  pip_𝒯(j) := π_𝒯({S ∈ 𝒯 : j ∈ S}),  mpm_𝒯 := {j : pip_𝒯(j) > ½},  logZ_𝒯 := log Z_𝒯.

**The returned list and the new fields (SPEC §1–§2, §4).**
- *Sampler branch.* 𝒯 := the set of models of `fit$top_store` (`v3_run.R:210`; `cpp/v3_core.cpp:358-362`), each with
  its returned value. On a completed run SPEC defines `pip_list`, `mpm_list`, `log_Z_list` from 𝒯 and the returned
  values by SPEC §2; under EX-A, when every returned value equals F of its model (LIST-CODE (iii)), these are
  `pip_list[j]` = pip_𝒯(j) for every retained column j, `mpm_list` = mpm_𝒯, `log_Z_list` = logZ_𝒯.
- *Exact branch* (status `exact`, `v3_fit.R:120-132`). SPEC §4: `pip_list` := `pip_primary`, `mpm_list` := `mpm`, and
  `log_Z_list` := logZ_{𝒯^ex} for the list 𝒯^ex := the models of the enumeration's store (`fit$exact$top`,
  `cpp/v3_core.cpp:531, 549, 565`) when SPEC's implementation returns it, else NA (no clause about it then).
- Other statuses: the fields are absent (SPEC §4); no claim.

**Premise IMPL-LIST (implementation conformance; method commit pending).** The method commit that adds the fields
computes them as SPEC §2 and §4 prescribe, from the returned list and values of the same run, and changes no other field
and no other state (SPEC §7 A.1–A.2). IMPL-LIST is a code fact to be discharged by a code reading of that commit (named
open item until then); it is not a condition on the data, and nothing below depends on SPEC §3's floating-point rules
(EX-A).

## 2. Lemma LIST-K (deterministic list algebra)

**(C1) Lemma LIST-K.** *Deterministic.* Fix a data set (F real-valued on Ω, so 0 < Z < ∞) [LC1-12] and a set 𝒯 ⊆ Ω
with S₀ ∈ 𝒯. Then:
(a) max_j |pip_𝒯(j) − 1{j ∈ S₀}| ≤ 1 − π_𝒯(S₀) ≤ ε_n, the maximum over all retained columns j;
(b) sup_{𝒜 ⊆ Ω} |π_𝒯(𝒜 ∩ 𝒯) − π(𝒜)| = 1 − π(𝒯) ≤ ε_n; in particular max_j |pip_𝒯(j) − PIP_j| ≤ ε_n;
(c) if ε_n < ½, then mpm_𝒯 = S₀ = MPM;
(d) logZ_𝒯 = log Z + log π(𝒯), hence log Z + log(1 − ε_n) ≤ logZ_𝒯 ≤ log Z and, if ε_n < 1,
    0 ≤ log Z − logZ_𝒯 ≤ −log(1 − ε_n) ≤ ε_n/(1 − ε_n);
(e) for 𝒯 = Ω the quantities are the exact ones: pip_Ω = PIP, mpm_Ω = MPM, logZ_Ω = log Z; and (a), (c) hold for
    PIP and MPM in place of pip_𝒯 and mpm_𝒯 without any list.

## 3. Lemma LIST-CODE (code reading at the pin)

**(C2) Lemma LIST-CODE.** Code of record as in the header; shipped configuration (`ls0 = TRUE`, cap
`"ell_n_plus_mode"`, `ls0_ell` = ℓ_n, `ls0_tie_dp = TRUE`) [R1-opus-5]; EX-A, EX-S, SR. Let 𝓜^run be the set of models offered to the final-run
ledger (`Ledger::offer_stores`, `cpp/v3_ledger.h:89-94`), as in SAMP `STATEMENT.md:59-60`.
(i) *[Link 1: completed = output on the sampler branch.]* On the sampler branch, `fit$status == "completed"` if and only
    if `fit$estimates_available` is TRUE, i.e. if and only if the run is in 𝒪. On such a run the final run executed LS0
    (`E.local_search(m.S, …, PH_LS0)`, `cpp/v3_core.cpp:465-481`) to its termination, on the final run's own ledger and
    cache, and every model LS0 evaluated is in 𝓜^run. The models LS0 evaluates, and their order, are those of the
    deterministic search in the definition of 𝒦_n (RM `STATEMENT.md:52-53`); in particular on 𝒦_n, S₀ ∈ 𝓜^run.
(ii) *[Link 2: `hpm` = Ŝ⁺.]* On a completed run, `fit$hpm` is the hpm_better-maximum of 𝓜^run (CC2), which is the
    reported model Ŝ⁺ of RM and RM2R; 𝓜^run ⊆ Ω (CC5).
(iii) *[The returned list.]* On a completed run, 𝒯 consists of distinct models of 𝓜^run, written in original indices,
    each returned with value F(S); |𝒯| ≤ 40p + 1; and the hpm_better-maximum of 𝓜^run belongs to 𝒯.
(iv) *[Exact branch.]* On status `exact`, the enumeration scores every S ∈ Ω; `pip_primary` = PIP, `mpm` = MPM and
    `fit$hpm` = the hpm_better-maximum of Ω; 𝒯^ex consists of distinct models of Ω with values F(S) and contains the
    hpm_better-maximum of Ω.
(v) *Consequently,* if F(S₀) > F(S) for every S ∈ Ω ∖ {S₀} (the event 𝓜_n), then: on a completed run with S₀ ∈ 𝓜^run,
    S₀ ∈ 𝒯 and `hpm` = S₀; on a run with status `exact`, S₀ ∈ 𝒯^ex and `hpm` = S₀.

## 4. Corollary LIST-R (Gaussian rows; every design inside Theorem 6)

**(C3) Corollary LIST-R.** Setting R, the method as coded, the premises and configuration of §1 and IMPL-LIST. Assume
the hypotheses of RM2-R-plus (RM2R `STATEMENT.md:177-182` = those of RM2-R, W3-RM2 `STATEMENT.md:216-218`; reader
form: §5 remark 5) [LC1-3]. Let 𝒢⁺_n = 𝓜_n ∩ 𝒦_n, so that P(𝒢⁺_n) → 1 (RM2-R-plus, through RM0-plus (b⁺)) [LC1-13]. Write
r_n := √(log n/n).
(i) *Common data event, pathwise.* On 𝒢⁺_n, every admissible run that returns output — every seed, N_e, R′ and
    calibration outcome, either branch — has S₀ in its list (𝒯, or 𝒯^ex when returned), reports `hpm` = S₀, and its
    fields satisfy, with ε_n = 1 − π(S₀ | y):
      max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n,   max_j |pip_list[j] − PIP_j| ≤ ε_n,
      log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z   (when `log_Z_list` is not NA),
    and, on 𝒢⁺_n ∩ {ε_n < ½}, `mpm_list` = `hpm` = S₀ = MPM.
(ii) *In probability, and rates.* Define, for t > 0, the error events of an output run
      B₁(t) := {max_j |pip_list[j] − 1{j ∈ S₀}| > t},  B₂(t) := {max_j |pip_list[j] − PIP_j| > t},
      B₃(t) := {`log_Z_list` is not NA and |log_Z_list − log Z| > 2t},  B₄ := {`mpm_list` ≠ S₀ or `hpm` ≠ S₀}.
    For every t ∈ (0, ½), for every admissible run (every seed, N_e, R′ and calibration outcome) [SL1-2]:
      P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t),  P(𝒪 ∩ B₄) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n ≥ ½),
    and every right side tends to 0: P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0 by RM2-R-plus (RM0-plus (b⁺)), and P(ε_n > t),
    P(ε_n ≥ ½) ≤ E ε_n/min(t, ½) → 0 by [POST], a conclusion of RM2-R-plus [LC1-1].
    **Rate (p ≥ 2 for all large n) [SL1-3].** If p ≥ 2 for all large n, then ε_n = O_P(r_n) (hypothesis (T1-R) of
    RM2-R-plus is hypothesis LSF of POST, RM `STATEMENT.md:128-133`; POST (b), `L1_POST.md:31-33`), and for every
    deterministic sequence t_n ∈ (0, ½) with t_n/r_n → ∞ the data events 𝒢♯_n := 𝒢⁺_n ∩ {ε_n ≤ t_n} satisfy
    P(𝒢♯_n) → 1; on 𝒢♯_n every admissible run that returns output has
      max_j |pip_list[j] − 1{j ∈ S₀}| ≤ t_n,  max_j |pip_list[j] − PIP_j| ≤ t_n,  `mpm_list` = `hpm` = S₀,
    and, when `log_Z_list` is not NA, |log_Z_list − log Z| ≤ 2t_n [SL1-1].
(iii) *With delivery.* Assume in addition the delivery premises (D). Then every admissible run returns output (DLV-0),
    so for every seed, N_e, R′ and calibration outcome, without "on output": P(B₄) → 0, and P(B₁(t) ∪ B₂(t) ∪ B₃(t)) → 0
    for every t ∈ (0, ½); if moreover p ≥ 2 for all large n, then for every t_n as in (ii), P(B₁(t_n) ∪ B₂(t_n) ∪
    B₃(t_n)) → 0, i.e. the two PIP errors and (where `log_Z_list` is not NA) the evidence error are O_P(r_n).

## 5. Remarks (not part of any claim; not registered)

1. *Scope.* LIST-R adds no hypothesis to Theorem 6: it covers every design inside Theorem 6, AR and block designs
   included when they satisfy (A1)–(A6). It is about fields computed from the returned list. The sampler averages
   (`pip_primary`, `mpm`, `log_Z`) are not covered on such designs; their scope stays that of card row 3.6.
2. *What the list fields do not say.* They do not certify by themselves how much posterior mass the list holds; that
   comes from Theorem 6's data event. `log_Z_list` ≤ log Z always (LIST-K (d)); log_Z − log_Z_list is an uncertified
   indication (SPEC §6).
3. *Links in DIST.* LIST-CODE (i)–(ii) are the two links DIST `STATEMENT.md:297-303` names as unchecked; with them,
   RM2-R-plus supplies DIST-C (C-ii)(α)'s premise {S₀ ∈ 𝓜} on Theorem 6 designs. A consequence for Corollary 9C
   (`W3-DIST:Cor-C`) on designs that satisfy both Theorem 9 and Theorem 6 is proposed at CP3, not claimed here.
4. *Arithmetic.* EX-A throughout, as for Theorem 6. Binary64 agreement (1e−12 between engines; SPEC §3, §7) is an
   engineering acceptance test, not a theorem.
5. *Reader form of the hypotheses* [LC1-3]. In reader form the hypotheses of LIST-R are those of Theorem 6 (READER §6,
   (A1)–(A6)), which reach the hypotheses of RM2-R-plus through Theorem 6's own bridges B6.1–B6.4 (B6.1 and B6.3 marked NEW
   there) and the identities of (A1)–(A3) with Setting R and (V-R) (READER §6 bridge table) [LC1R-3]. LIST-R consumes RM2-R-plus only; the reader corollary inherits exactly Theorem 6's
   bridge record, so any change of Theorem 6's presented hypotheses carries over (D109).

## 6. Dependencies and supersession

| new claim | consumes (id@version, status verbatim at CP3) | relation |
|---|---|---|
| LIST-K | — | new; deterministic |
| LIST-CODE | W3-SAMP:CC@1.1.2 (CC2, CC5) | new code fact (top store, LS0 at code level); refines RM-0's text-level step "LS0 … every model it scored joined the all-scored set" (C-DLV `lemmas/L4_delivery.md:66-70`) |
| LIST-R | LIST-K, LIST-CODE, W3-RM2-R:RM2-R-plus@1.0.1, RM0-plus@1.0.1, DLV-0@1.0.1, W2-APP:POST@1.0.7 | adds conclusions to RM2-R-plus on its own data event; implies nothing about the printed sampler averages |

No supersession. Card proposal (a new row next to 3.1, or an addition to 3.1/3.6) at CP3; HQ decides.

## Changelog (after the lock; PROTOCOL_v4 §4.2)

| version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| v0.1 | all | — | draft for the statement lock | — | — |
| v1.0 | (C3)(ii)–(iii): evidence error events qualified "when `log_Z_list` is not NA"; t, t_n ∈ (0, ½) (was (0, ½]); rate clause under "p ≥ 2 for all large n"; error events named B₁–B₄; (C3) preamble "implied by" the reader assumptions | EQUAL (corrections of the draft before the lock) | SL1-1, SL1-2, SL1-3, SL1 table row "C3 preamble" | `reviews/SL1_statement_lock_sol.md` | applied as the reviewer's fixes; LOCK |
| v1.1 | (C1) hypothesis "F real-valued on Ω (0 < Z < ∞)"; §1 convention for S₀ ∉ Ω; (C3) preamble: the reader-form sentence moved out of the claim span to §5 remark 5; P(𝒢⁺_n) → 1 attributed to RM0-plus (b⁺); (C3)(ii) reason for "every right side tends to 0" completed | EQUAL (hypothesis made explicit as already defined in §1; a convention that makes small-n cases trivially true; an unproved interpretive sentence moved out of the span; citations) | LC1-12, LC1-2, LC1-3, LC1-13, LC1-1 | `reviews/LC1_line_check_opus.md` | council R1 (tags to be confirmed by the seats) |
| v1.1.1 | §1 convention sentence narrowed to statements involving S₀, 𝓜_n or 𝒦_n; §5 remark 5 (outside claims) | EQUAL (wording) | LC1R-4, LC1R-3 | `reviews/LC1R_recheck_opus.md` | fixes applied verbatim from LC1R |
| v1.1.2 | (C2) configuration gloss: `ls0_ell` = ℓ_n added (it is part of the imported shipped configuration, RM `STATEMENT.md:59-67`) | EQUAL (explicit form of an imported premise) | R1-opus-5 | `reviews/R1_council_opus.md` | council diff round R2 |
