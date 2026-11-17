# D5P1 — blind audit of the list-restricted output claims (LIST-K, LIST-CODE, LIST-R)

Material for a blind referee. Every excerpt is verbatim with its file and original line numbers; status labels and review markers have been removed.

### [ST] `Theory_work/Wave3/W3-D5P/STATEMENT.md` @ a2c465a4 — the statement file (claims (C1) LIST-K, (C2) LIST-CODE, (C3) LIST-R)
lines 1–1:
```
    1| # W3-D5P — STATEMENT v1.1.2 (locked v1.0 + changelog rows v1.1–v1.1.2): the list-restricted outputs on every Theorem 6 design
```
lines 10–154:
```
   10| **Sources (read-only; abbreviations).**
   11| SPEC := `Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md` @ theory/W3-AUDIT 523dda23 (the definition of the new fields).
   12| RM2R := `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (v1.0 LOCKED; claims @1.0.1 on main). RM := `Theory_work/Wave3/W3-RM/STATEMENT.md`.
   13| SAMP := `Theory_work/Wave3/W3-SAMP/STATEMENT.md` and its `lemmas/CC_code_check.md` (CC). DIST := `Theory_work/Wave3/W3-DIST/STATEMENT.md`.
   14| POST := `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`. READER := `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` (Theorem 6 = card row 3.1).
   15| **Code of record:** `Scripts/SMC_BVS/core/` at 4676af6 (= the core on main 029bb748; last changed at 72785fe). The new
   16| fields are added by a later **method commit, pending** (Engineering; recorded as `method_commit` at CP3).
   17| 
   18| ## 0. What this file adds, in one table
   19| 
   20| | claim (new id) | kind | what it says | consumes |
   21| |---|---|---|---|
   22| | **LIST-K** (§2) | deterministic lemma | for any list of distinct models containing S₀, the list-renormalised PIPs, median model and evidence sum are within 1 − π(S₀ \| y) of the truth and of the exact posterior | — |
   23| | **LIST-CODE** (§3) | code-reading lemma at the pin | a completed run is an output run of RM; its printed `hpm` is RM's reported model Ŝ⁺; every model the final run scores is offered to the returned list `top_store`, which keeps the best-scored offered model (and the exact branch's list keeps the best model of Ω) | CC (CC2, CC5) |
   24| | **LIST-R** (§4) | corollary (Gaussian rows; Theorem 6's hypotheses) | on one data event of probability → 1, every admissible run that produces output has S₀ in its list and satisfies the bounds of LIST-K jointly with `hpm` = S₀; errors O_P(√(log n/n)); under the delivery premises, unconditionally | LIST-K, LIST-CODE, RM2-R-plus, RM0-plus, DLV-0, POST |
   25| 
   26| The two links named as unchecked at DIST `STATEMENT.md:297-303` ("whether RM2's output event covers {completed}, and
   27| whether its reported model is `hpm`") are LIST-CODE (i) and (ii).
   28| 
   29| ## 1. Setting, objects and premises
   30| 
   31| **Base, taken unchanged.** Setting R, the method as coded, the shipped configuration, the implementation premises
   32| (EX-A, EX-S, SR, GUARD-W, OP-LS0, complete scans), "admissible run" (every seed, N_e, R′ and calibration outcome), the
   33| events 𝒪 ("the run returns output"), U_n = 𝒪ᶜ, Sand_n(Q), NA(𝓛), TL(𝓛), 𝒦_n and the reported model Ŝ⁺: RM
   34| `STATEMENT.md:32-68` as used by RM2R `STATEMENT.md:33-50`. The mode event 𝓜_n := {S₀ is the unique maximiser of F on Ω}
   35| and 𝒢⁺_n := 𝓜_n ∩ 𝒦_n: RM2R `STATEMENT.md:54-60, 128-137`. The delivery premises (D) with IDEAL-W⁺ and "valid
   36| non-degenerate input": RM2R `STATEMENT.md:71-93`. Notation: Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋), p = p_ret (the
   37| retained columns, indexed by their original indices); S₀ = supp θ*, s₀ = |S₀|.
   38| 
   39| **The exact posterior and its summaries (deterministic definitions).** F(S) := log ϖ(|S|) + log m(S) for S ∈ Ω, with ϖ
   40| the coded size prior normalised on Ω (`cpp/v3_score.h:60-70`) and m the coded marginal likelihood (CC2: e^F ∝ π on Ω).
   41|   Z := Σ_{S∈Ω} e^{F(S)},  π(S) := π(S | y) := e^{F(S)}/Z,  PIP_j := π({S : j ∈ S}),  MPM := {j : PIP_j > ½},
   42|   ε_n := ε_n(y) := 1 − π(S₀ | y).
   43| *Convention*: if S₀ ∉ Ω (i.e. s₀ > K), then π(S₀ | y) := 0, ε_n = 1, and 𝓜_n = 𝒦_n := ∅ (S₀ can then be
   44| neither the maximiser of F on Ω nor scored); every statement below that involves S₀, 𝓜_n or 𝒦_n holds trivially for
   45| such n.
   46| For a nonempty set 𝒯 ⊆ Ω: π(𝒯) := Σ_{S∈𝒯} π(S), Z_𝒯 := Σ_{S∈𝒯} e^{F(S)}, π_𝒯(S) := e^{F(S)}/Z_𝒯 (S ∈ 𝒯), and
   47|   pip_𝒯(j) := π_𝒯({S ∈ 𝒯 : j ∈ S}),  mpm_𝒯 := {j : pip_𝒯(j) > ½},  logZ_𝒯 := log Z_𝒯.
   48| 
   49| **The returned list and the new fields (SPEC §1–§2, §4).**
   50| - *Sampler branch.* 𝒯 := the set of models of `fit$top_store` (`v3_run.R:210`; `cpp/v3_core.cpp:358-362`), each with
   51|   its returned value. On a completed run SPEC defines `pip_list`, `mpm_list`, `log_Z_list` from 𝒯 and the returned
   52|   values by SPEC §2; under EX-A, when every returned value equals F of its model (LIST-CODE (iii)), these are
   53|   `pip_list[j]` = pip_𝒯(j) for every retained column j, `mpm_list` = mpm_𝒯, `log_Z_list` = logZ_𝒯.
   54| - *Exact branch* (status `exact`, `v3_fit.R:120-132`). SPEC §4: `pip_list` := `pip_primary`, `mpm_list` := `mpm`, and
   55|   `log_Z_list` := logZ_{𝒯^ex} for the list 𝒯^ex := the models of the enumeration's store (`fit$exact$top`,
   56|   `cpp/v3_core.cpp:531, 549, 565`) when SPEC's implementation returns it, else NA (no clause about it then).
   57| - Other statuses: the fields are absent (SPEC §4); no claim.
   58| 
   59| **Premise IMPL-LIST (implementation conformance; method commit pending).** The method commit that adds the fields
   60| computes them as SPEC §2 and §4 prescribe, from the returned list and values of the same run, and changes no other field
   61| and no other state (SPEC §7 A.1–A.2). IMPL-LIST is a code fact to be discharged by a code reading of that commit (named
   62| open item until then); it is not a condition on the data, and nothing below depends on SPEC §3's floating-point rules
   63| (EX-A).
   64| 
   65| ## 2. Lemma LIST-K (deterministic list algebra)
   66| 
   67| **(C1) Lemma LIST-K.** *Deterministic.* Fix a data set (F real-valued on Ω, so 0 < Z < ∞) and a set 𝒯 ⊆ Ω
   68| with S₀ ∈ 𝒯. Then:
   69| (a) max_j |pip_𝒯(j) − 1{j ∈ S₀}| ≤ 1 − π_𝒯(S₀) ≤ ε_n, the maximum over all retained columns j;
   70| (b) sup_{𝒜 ⊆ Ω} |π_𝒯(𝒜 ∩ 𝒯) − π(𝒜)| = 1 − π(𝒯) ≤ ε_n; in particular max_j |pip_𝒯(j) − PIP_j| ≤ ε_n;
   71| (c) if ε_n < ½, then mpm_𝒯 = S₀ = MPM;
   72| (d) logZ_𝒯 = log Z + log π(𝒯), hence log Z + log(1 − ε_n) ≤ logZ_𝒯 ≤ log Z and, if ε_n < 1,
   73|     0 ≤ log Z − logZ_𝒯 ≤ −log(1 − ε_n) ≤ ε_n/(1 − ε_n);
   74| (e) for 𝒯 = Ω the quantities are the exact ones: pip_Ω = PIP, mpm_Ω = MPM, logZ_Ω = log Z; and (a), (c) hold for
   75|     PIP and MPM in place of pip_𝒯 and mpm_𝒯 without any list.
   76| 
   77| ## 3. Lemma LIST-CODE (code reading at the pin)
   78| 
   79| **(C2) Lemma LIST-CODE.** Code of record as in the header; shipped configuration (`ls0 = TRUE`, cap
   80| `"ell_n_plus_mode"`, `ls0_ell` = ℓ_n, `ls0_tie_dp = TRUE`); EX-A, EX-S, SR. Let 𝓜^run be the set of models offered to the final-run
   81| ledger (`Ledger::offer_stores`, `cpp/v3_ledger.h:89-94`), as in SAMP `STATEMENT.md:59-60`.
   82| (i) *[Link 1: completed = output on the sampler branch.]* On the sampler branch, `fit$status == "completed"` if and only
   83|     if `fit$estimates_available` is TRUE, i.e. if and only if the run is in 𝒪. On such a run the final run executed LS0
   84|     (`E.local_search(m.S, …, PH_LS0)`, `cpp/v3_core.cpp:465-481`) to its termination, on the final run's own ledger and
   85|     cache, and every model LS0 evaluated is in 𝓜^run. The models LS0 evaluates, and their order, are those of the
   86|     deterministic search in the definition of 𝒦_n (RM `STATEMENT.md:52-53`); in particular on 𝒦_n, S₀ ∈ 𝓜^run.
   87| (ii) *[Link 2: `hpm` = Ŝ⁺.]* On a completed run, `fit$hpm` is the hpm_better-maximum of 𝓜^run (CC2), which is the
   88|     reported model Ŝ⁺ of RM and RM2R; 𝓜^run ⊆ Ω (CC5).
   89| (iii) *[The returned list.]* On a completed run, 𝒯 consists of distinct models of 𝓜^run, written in original indices,
   90|     each returned with value F(S); |𝒯| ≤ 40p + 1; and the hpm_better-maximum of 𝓜^run belongs to 𝒯.
   91| (iv) *[Exact branch.]* On status `exact`, the enumeration scores every S ∈ Ω; `pip_primary` = PIP, `mpm` = MPM and
   92|     `fit$hpm` = the hpm_better-maximum of Ω; 𝒯^ex consists of distinct models of Ω with values F(S) and contains the
   93|     hpm_better-maximum of Ω.
   94| (v) *Consequently,* if F(S₀) > F(S) for every S ∈ Ω ∖ {S₀} (the event 𝓜_n), then: on a completed run with S₀ ∈ 𝓜^run,
   95|     S₀ ∈ 𝒯 and `hpm` = S₀; on an exact-branch run, S₀ ∈ 𝒯^ex and `hpm` = S₀.
   96| 
   97| ## 4. Corollary LIST-R (Gaussian rows; every design inside Theorem 6)
   98| 
   99| **(C3) Corollary LIST-R.** Setting R, the method as coded, the premises and configuration of §1 and IMPL-LIST. Assume
  100| the hypotheses of RM2-R-plus (RM2R `STATEMENT.md:177-182` = those of RM2-R, W3-RM2 `STATEMENT.md:216-218`; reader
  101| form: §5 remark 5). Let 𝒢⁺_n = 𝓜_n ∩ 𝒦_n, so that P(𝒢⁺_n) → 1 (RM2-R-plus, through RM0-plus (b⁺)). Write
  102| r_n := √(log n/n).
  103| (i) *Common data event, pathwise.* On 𝒢⁺_n, every admissible run that returns output — every seed, N_e, R′ and
  104|     calibration outcome, either branch — has S₀ in its list (𝒯, or 𝒯^ex when returned), reports `hpm` = S₀, and its
  105|     fields satisfy, with ε_n = 1 − π(S₀ | y):
  106|       max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n,   max_j |pip_list[j] − PIP_j| ≤ ε_n,
  107|       log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z   (when `log_Z_list` is not NA),
  108|     and, on 𝒢⁺_n ∩ {ε_n < ½}, `mpm_list` = `hpm` = S₀ = MPM.
  109| (ii) *In probability, and rates.* Define, for t > 0, the error events of an output run
  110|       B₁(t) := {max_j |pip_list[j] − 1{j ∈ S₀}| > t},  B₂(t) := {max_j |pip_list[j] − PIP_j| > t},
  111|       B₃(t) := {`log_Z_list` is not NA and |log_Z_list − log Z| > 2t},  B₄ := {`mpm_list` ≠ S₀ or `hpm` ≠ S₀}.
  112|     For every t ∈ (0, ½), for every admissible run (every seed, N_e, R′ and calibration outcome):
  113|       P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t),  P(𝒪 ∩ B₄) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n ≥ ½),
  114|     and every right side tends to 0: P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0 by RM2-R-plus (RM0-plus (b⁺)), and P(ε_n > t),
  115|     P(ε_n ≥ ½) ≤ E ε_n/min(t, ½) → 0 by [POST], a conclusion of RM2-R-plus.
  116|     **Rate (p ≥ 2 for all large n).** If p ≥ 2 for all large n, then ε_n = O_P(r_n) (hypothesis (T1-R) of
  117|     RM2-R-plus is hypothesis LSF of POST, RM `STATEMENT.md:128-133`; POST (b), `L1_POST.md:31-33`), and for every
  118|     deterministic sequence t_n ∈ (0, ½) with t_n/r_n → ∞ the data events 𝒢♯_n := 𝒢⁺_n ∩ {ε_n ≤ t_n} satisfy
  119|     P(𝒢♯_n) → 1; on 𝒢♯_n every admissible run that returns output has
  120|       max_j |pip_list[j] − 1{j ∈ S₀}| ≤ t_n,  max_j |pip_list[j] − PIP_j| ≤ t_n,  `mpm_list` = `hpm` = S₀,
  121|     and, when `log_Z_list` is not NA, |log_Z_list − log Z| ≤ 2t_n.
  122| (iii) *With delivery.* Assume in addition the delivery premises (D). Then every admissible run returns output (DLV-0),
  123|     so for every seed, N_e, R′ and calibration outcome, without "on output": P(B₄) → 0, and P(B₁(t) ∪ B₂(t) ∪ B₃(t)) → 0
  124|     for every t ∈ (0, ½); if moreover p ≥ 2 for all large n, then for every t_n as in (ii), P(B₁(t_n) ∪ B₂(t_n) ∪
  125|     B₃(t_n)) → 0, i.e. the two PIP errors and (where `log_Z_list` is not NA) the evidence error are O_P(r_n).
  126| 
  127| ## 5. Remarks (not part of any claim; not registered)
  128| 
  129| 1. *Scope.* LIST-R adds no hypothesis to Theorem 6: it covers every design inside Theorem 6, AR and block designs
  130|    included when they satisfy (A1)–(A6). It is about fields computed from the returned list. The sampler averages
  131|    (`pip_primary`, `mpm`, `log_Z`) are not covered on such designs; their scope stays that of card row 3.6.
  132| 2. *What the list fields do not say.* They do not certify by themselves how much posterior mass the list holds; that
  133|    comes from Theorem 6's data event. `log_Z_list` ≤ log Z always (LIST-K (d)); log_Z − log_Z_list is an uncertified
  134|    indication (SPEC §6).
  135| 3. *Links in DIST.* LIST-CODE (i)–(ii) are the two links DIST `STATEMENT.md:297-303` names as unchecked; with them,
  136|    RM2-R-plus supplies DIST-C (C-ii)(α)'s premise {S₀ ∈ 𝓜} on Theorem 6 designs. A consequence for Corollary 9C
  137|    (`W3-DIST:Cor-C`) on designs that satisfy both Theorem 9 and Theorem 6 is proposed at CP3, not claimed here.
  138| 4. *Arithmetic.* EX-A throughout, as for Theorem 6. Binary64 agreement (1e−12 between engines; SPEC §3, §7) is an
  139|    engineering acceptance test, not a theorem.
  140| 5. *Reader form of the hypotheses*. In reader form the hypotheses of LIST-R are those of Theorem 6 (READER §6,
  141|    (A1)–(A6)), which reach the hypotheses of RM2-R-plus through Theorem 6's own bridges B6.1–B6.4 (B6.1 and B6.3 marked NEW
  142|    there) and the identities of (A1)–(A3) with Setting R and (V-R) (READER §6 bridge table). LIST-R consumes RM2-R-plus only; the reader corollary inherits exactly Theorem 6's
  143|    bridge record, so any change of Theorem 6's presented hypotheses carries over (D109).
  144| 
  145| ## 6. Dependencies and supersession
  146| 
  147| | new claim | consumes (id@version, status verbatim at CP3) | relation |
  148| |---|---|---|
  149| | LIST-K | — | new; deterministic |
  150| | LIST-CODE | W3-SAMP:CC@1.1.2 (CC2, CC5) | new code fact (top store, LS0 at code level); refines RM-0's text-level step "LS0 … every model it scored joined the all-scored set" (C-DLV `lemmas/L4_delivery.md:66-70`) |
  151| | LIST-R | LIST-K, LIST-CODE, W3-RM2-R:RM2-R-plus@1.0.1, RM0-plus@1.0.1, DLV-0@1.0.1, W2-APP:POST@1.0.7 | adds conclusions to RM2-R-plus on its own data event; implies nothing about the printed sampler averages |
  152| 
  153| No supersession. Card proposal (a new row next to 3.1, or an addition to 3.1/3.6) at CP3; HQ decides.
  154| 
```

### [L1] `Theory_work/Wave3/W3-D5P/lemmas/L1_listK.md` @ a2c465a4 — proof of LIST-K
lines 1–58:
```
    1| # L1 — Lemma LIST-K (deterministic list algebra) — proof
    2| 
    3| [review record omitted]
    4| finite sums over a finite set, real arithmetic, one inequality for log; no measure theory.
    5| 
    6| ## Setting (all deterministic)
    7| Ω is a finite set of models (subsets of [p] := {1, …, p}); F : Ω → ℝ (real-valued: (C1)'s hypothesis; STATEMENT §1 defines
    8| F = log ϖ + log m, finite on Ω); w(S) := e^{F(S)} > 0; Z := Σ_{S∈Ω} w(S) ∈ (0, ∞).
    9| π(S) := w(S)/Z; for 𝒜 ⊆ Ω, π(𝒜) := Σ_{S∈𝒜} π(S); PIP_j := π(𝒜_j) with 𝒜_j := {S ∈ Ω : j ∈ S}; MPM := {j ∈ [p] : PIP_j > ½}.
   10| 𝒯 ⊆ Ω with S₀ ∈ 𝒯 (so S₀ ∈ Ω). Z_𝒯 := Σ_{S∈𝒯} w(S); π_𝒯(S) := w(S)/Z_𝒯 for S ∈ 𝒯; for ℬ ⊆ 𝒯, π_𝒯(ℬ) := Σ_{S∈ℬ} π_𝒯(S);
   11| pip_𝒯(j) := π_𝒯(𝒜_j ∩ 𝒯); mpm_𝒯 := {j ∈ [p] : pip_𝒯(j) > ½}; logZ_𝒯 := log Z_𝒯; ε := 1 − π(S₀). Write m := π(𝒯).
   12| 
   13| ## Step 0 (elementary facts)
   14| (0.1) Z_𝒯 ≥ w(S₀) > 0, so π_𝒯 is well defined, π_𝒯 ≥ 0 and π_𝒯(𝒯) = 1.
   15| (0.2) Z_𝒯 = Σ_{S∈𝒯} Z·π(S) = Z·m, hence m = Z_𝒯/Z ∈ (0, 1] (𝒯 ⊆ Ω, all terms positive) and π_𝒯(S) = π(S)/m for S ∈ 𝒯.
   16| (0.3) π(S₀) ≤ m ≤ 1 (S₀ ∈ 𝒯); hence 1 − m ≤ ε, and ε < 1 because π(S₀) > 0.
   17| (0.4) π_𝒯(S₀) = π(S₀)/m ≥ π(S₀) (by (0.2), (0.3)); hence 1 − π_𝒯(S₀) ≤ ε.
   18| (0.5) If 𝒯 = Ω, then m = 1 and π_Ω = π (by (0.2)); so pip_Ω(j) = π(𝒜_j) = PIP_j, mpm_Ω = MPM and Z_Ω = Z.
   19| 
   20| ## (a)
   21| Fix j ∈ [p]. Always 0 ≤ pip_𝒯(j) ≤ π_𝒯(𝒯) = 1.
   22| - If j ∈ S₀: S₀ ∈ 𝒜_j ∩ 𝒯, so pip_𝒯(j) ≥ π_𝒯(S₀), and |pip_𝒯(j) − 1| = 1 − pip_𝒯(j) ≤ 1 − π_𝒯(S₀).
   23| - If j ∉ S₀: 𝒜_j ∩ 𝒯 ⊆ 𝒯 ∖ {S₀}, so pip_𝒯(j) ≤ π_𝒯(𝒯) − π_𝒯(S₀) = 1 − π_𝒯(S₀), and |pip_𝒯(j) − 0| ≤ 1 − π_𝒯(S₀).
   24| Taking the maximum over j ∈ [p] and using (0.4): max_j |pip_𝒯(j) − 1{j ∈ S₀}| ≤ 1 − π_𝒯(S₀) ≤ ε. ∎(a)
   25| 
   26| ## (b)
   27| Fix 𝒜 ⊆ Ω and put a := π(𝒜 ∩ 𝒯), b := π(𝒜 ∖ 𝒯). Then π(𝒜) = a + b and, by (0.2), π_𝒯(𝒜 ∩ 𝒯) = a/m. So
   28|   D(𝒜) := π_𝒯(𝒜 ∩ 𝒯) − π(𝒜) = a(1 − m)/m − b.
   29| Since 0 ≤ a ≤ m: 0 ≤ a(1 − m)/m ≤ 1 − m. Since 0 ≤ b ≤ π(Ω ∖ 𝒯) = 1 − m: −(1 − m) ≤ −b ≤ 0. Adding,
   30| −(1 − m) ≤ D(𝒜) ≤ 1 − m, i.e. |D(𝒜)| ≤ 1 − m for every 𝒜 ⊆ Ω.
   31| *Attainment.* For 𝒜 = Ω ∖ 𝒯: a = 0, b = 1 − m, so |D(𝒜)| = 1 − m. Hence sup_{𝒜⊆Ω} |D(𝒜)| = 1 − m (a maximum over the
   32| finite power set of Ω), and 1 − m ≤ ε by (0.3).
   33| *PIPs.* For 𝒜 = 𝒜_j: π_𝒯(𝒜_j ∩ 𝒯) = pip_𝒯(j) and π(𝒜_j) = PIP_j; so |pip_𝒯(j) − PIP_j| ≤ 1 − m ≤ ε for every j. ∎(b)
   34| 
   35| ## (c)
   36| Assume ε < ½. By (0.4), π_𝒯(S₀) ≥ π(S₀) = 1 − ε > ½.
   37| - j ∈ S₀: pip_𝒯(j) ≥ π_𝒯(S₀) > ½ (proof of (a)), so j ∈ mpm_𝒯.
   38| - j ∉ S₀: pip_𝒯(j) ≤ 1 − π_𝒯(S₀) < ½ (proof of (a)), so j ∉ mpm_𝒯.
   39| Hence mpm_𝒯 = S₀ (both are subsets of [p]; S₀ ⊆ [p] because S₀ ∈ Ω). The same argument with 𝒯 = Ω (allowed: S₀ ∈ Ω),
   40| where pip_Ω = PIP and mpm_Ω = MPM by (0.5), gives MPM = S₀. ∎(c)
   41| 
   42| ## (d)
   43| By (0.2), logZ_𝒯 = log(Z·m) = log Z + log m. By (0.3), log π(S₀) ≤ log m ≤ 0, i.e.
   44| log Z + log(1 − ε) ≤ logZ_𝒯 ≤ log Z, and 0 ≤ log Z − logZ_𝒯 = −log m ≤ −log(1 − ε). For 0 ≤ ε < 1 (always, by (0.3)),
   45| −log(1 − ε) = log(1 + ε/(1 − ε)) ≤ ε/(1 − ε), by log(1 + x) ≤ x for x ≥ 0. ∎(d)
   46| *Corollary used in L3.* If ε ≤ t < ½ then |logZ_𝒯 − log Z| ≤ ε/(1 − ε) ≤ 2ε ≤ 2t (since 1 − ε > ½).
   47| 
   48| ## (e)
   49| For 𝒯 = Ω the identities are (0.5). Then (a) and (c) at 𝒯 = Ω
   50| read max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π_Ω(S₀) = ε and, if ε < ½, MPM = S₀. ∎(e)
   51| 
   52| ## Remarks for the checker
   53| - Nothing uses the structure of Ω (any finite set of subsets of [p]) or of F (any real function). The lemma is applied in
   54|   L3 with Ω = {S ⊆ [p_ret] : |S| ≤ K} and F the coded score.
   55| - The strict rule "> ½" matters only in (c); (c) needs ε < ½ strictly (with masses (0.3, 0.5, 0.2) on
   56|   {∅, {1}, {2}} and S₀ = {1}, MPM = ∅ ≠ S₀ at ε = ½).
   57| - Falsification: `numerics/listk_check.py` → `numerics/listk_check_out.txt` (20 000 random cases; every inequality,
   58|   and the identity sup|D| = 1 − m by brute force over all 𝒜 when |Ω| ≤ 12).
```

### [L2] `Theory_work/Wave3/W3-D5P/lemmas/L2_listCODE.md` @ a2c465a4 — proof of LIST-CODE (code reading)
lines 1–152:
```
    1| # L2 — Lemma LIST-CODE (code reading at the pin) — proof
    2| 
    3| [review record omitted]
    4| **Code of record:** `Scripts/SMC_BVS/core/` at 4676af6 = the core on main 029bb748 (`git diff 4676af6 029bb748 --
    5| Scripts/SMC_BVS/core` is empty; last change 72785fe). Paths below are relative to `Scripts/SMC_BVS/core/`; line
    6| numbers are those of this worktree (branch theory/W3-D5P). Premises: EX-A (every score is computed exactly), EX-S, SR,
    7| the shipped configuration (`ls0 = TRUE`, `v3.ls0_cap` unset ⇒ `"ell_n_plus_mode"`, `ls0_tie_dp = TRUE`, `ls0_ell` =
    8| `b$ell` = ℓ_n; `v3_run.R:88-103`). Consumed: W3-SAMP:CC@1.1.2 [status omitted]
    9| (`Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md`, CC2 :40-63, CC5).
   10| 
   11| Notation. "The final run" is the call `cpp_final_run` (`cpp/v3_core.cpp:391-518`) made by `v3_final_run`
   12| (`v3_run.R:223-229`) from `v3_fit` (`v3_fit.R:162`). Its ledger `led` and cache `cache` are local objects created at
   13| `cpp/v3_core.cpp:407` and `:409` (empty: `Ledger` constructor `cpp/v3_ledger.h:76-80`; `ScoreCache::init`
   14| `cpp/v3_score.h:264-270`). 𝓜^run := the set of models S for which `led.offer_stores(S, …)` is called during the final
   15| run (`cpp/v3_ledger.h:89-94`). "Sampler branch" := `fit$branch_run == "smc"` (`v3_fit.R:106`).
   16| 
   17| ## Step A — the only writers of the HPM and of the top store, and the offered set
   18| A1. `led.hpmS` is assigned only in `Ledger::offer_hpm` (`cpp/v3_ledger.h:84-88`; no other assignment to `hpmS` in
   19| `cpp/`), and it replaces the current value iff `hpm_better(F, S, hpmF, hpmS)` (`:85`). `offer_hpm` is called at
   20| `cpp/v3_ledger.h:90` (inside `offer_stores`) and at `cpp/v3_core.cpp:502`, which is inside the
   21| `catch (NumericalFailure&)` handler (`:483-508`), entered only after `status = "numerical_failure"` (`:484`).
   22| A2. `led.top.offer` is called only at `cpp/v3_ledger.h:91`, inside `offer_stores`, immediately after `offer_hpm(S, F, …)`
   23| with the same (S, F). (The store at `cpp/v3_core.cpp:549` is the enumeration's own `top`, Step E.)
   24| A3. `offer_stores` is called from `Ledger::event` when `is_fresh` (`cpp/v3_ledger.h:112`) and directly for inherited
   25| models (`cpp/v3_core.cpp:427`). Hence, on every final run whose status stays "completed", the sequence of HPM offers
   26| equals the sequence of top-store offers, and both are the sequence of calls of `offer_stores`; the set of offered
   27| models is 𝓜^run.
   28| A4. 𝓜^run ⊆ Ω (CC5; directly: tables only |U| ≤ K, `cpp/v3_start.h:91-93` and NaN entries skipped
   29| `cpp/v3_core.cpp:379`; inherited models checked `:425`; engine moves keep |S| ≤ K, CC5), and ∅ ∈ 𝓜^run (block-table code
   30| 0, `cpp/v3_core.cpp:376-384`), so 𝓜^run is nonempty.
   31| A5. Every offered value is F(S): tables F = `D.logprior[|U|]` + `logm_tab` (`cpp/v3_core.cpp:382`) with `logm_tab` = the scorer's log m(U)
   32| (`cpp/v3_start.h:93`); inherited F = `D.logprior[|S|]` + `sc.score(S).logm` (`cpp/v3_core.cpp:426-427`); `eval` F = `D.logprior[k]` + lm
   33| with lm the scorer's or the cached scorer's value (`cpp/v3_engine.h:89-101`). `D.logprior[k]` = log ϖ(k), the size prior
   34| normalised on Ω (`cpp/v3_score.h:60-70`). Under EX-A each is exactly F(S) = log ϖ(|S|) + log m(S) (CC2 :46-47). In
   35| particular the value of an offer is a function of the model.
   36| 
   37| ## Step B — (i) Link 1: completed ⇔ output, and LS0 ran on the final run's ledger
   38| B1. *Status and estimates.* On the sampler branch, `v3_fit` returns at `v3_fit.R:117` (status `resource_limit`), `:137`
   39| (`numerical_failure`), `:159` (`cal$status` ≠ "ok") with `estimates_available` FALSE (initial value `:78`; `finish`
   40| `:79-87` sets it only through `v3_unavailable_estimates`, which sets FALSE, `v3_run.R:110-114`), or after the final run
   41| at `v3_fit.R:173`, where every field of `fr` is copied into `fit` (`v3_fit.R:171`), including `status` (`v3_run.R:121`) and
   42| `estimates_available`. In `v3_assemble_final`, if `raw$status != "completed"` the function returns with
   43| `estimates_available` FALSE (`v3_run.R:143-149`); otherwise it reaches `:218` and sets it TRUE. `finish` changes
   44| neither field when `estimates_available` is TRUE (`v3_fit.R:84` concerns `resource_limit` only; `:85` requires FALSE). An
   45| R-level error (`stop`, including C++ `Rcpp::stop`, e.g. `cpp/v3_core.cpp:474`) returns no fit object at all. Hence on
   46| the sampler branch: `fit$status == "completed"` ⇔ `fit$estimates_available` is TRUE. The output event 𝒪 is "the coded
   47| fit returns with `estimates_available = TRUE`" (DLV-0, `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:144-147`).
   48| B2. *LS0 ran.* `status` is initialised to "completed" (`cpp/v3_core.cpp:413`) and changed only to "resource_limit"
   49| (`:451`, `:459`, `:480`) or "numerical_failure" (`:484`); it is never reset to "completed". If it is "completed" at the
   50| end, then: the island loop ran all `o.islands` islands (`:443-452`; `o.islands` is read from `ro` at `:396` and is 4 at `v3_run.R:91`; the argument uses no property of this number); the block `cpp/v3_core.cpp:453-482` ran; in it the guard check after the
   51| final local search did not fire (`:459`), so the condition at `:465` (`o.ls0`, TRUE by `v3_run.R:94` and
   52| `cpp/v3_core.cpp:400`) held and LS0 ran: `start_mode(st, 1000000, o.ls0_tie_dp)` (`:469`) and
   53| `E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0)` (`:476`) returned (no exception: a `NumericalFailure` would
   54| have set `numerical_failure`; any other exception aborts the fit, B1). `E.cache` = `&cache`, `E.led` = `&led` (`:411`).
   55| B3. *Every model LS0 evaluates is in 𝓜^run.* `local_search` (`cpp/v3_engine.h:379-419`) evaluates the centre by
   56| `eval(C, ME_LOCAL, emit_centre)` with `emit_centre = true` for LS0 (`cpp/v3_engine.h:382`, `cpp/v3_core.cpp:476`) and every scanned
   57| neighbour by `eval(q, ME_LOCAL)` (`emit = true`, `cpp/v3_engine.h:391`). In `eval` (`:89-101`): on a cache miss the
   58| scorer runs, `fresh = true`, the result is inserted in the cache (`:91-94`), and `led->event(…, fresh || !cache, …)`
   59| (`:99`) calls `offer_stores` (`cpp/v3_ledger.h:112`), so S ∈ 𝓜^run. On a cache hit, the entry was inserted by an earlier
   60| `eval` of the same model in this final run (the cache is created empty at `cpp/v3_core.cpp:409`, and `insert` is called
   61| only at `cpp/v3_engine.h:93`; `find` matches the model exactly, `cpp/v3_score.h:274-282` with `same` at `:271-273`). That earlier `eval` either had
   62| `emit = true` and was fresh, so it offered S, or had `emit = false`. The only `emit = false` call in the final run is the
   63| centre of the final local search, `E.local_search(led.hpmS, o.ell, o.tier, false)` (`cpp/v3_core.cpp:456`), whose centre
   64| is `led.hpmS`, a model already passed to `offer_hpm`, hence (A1, A3: before any numerical failure) already in 𝓜^run.
   65| (A cache clear, `cpp/v3_score.h:284`, only causes a later miss and a repeated, idempotent offer.) Hence every model LS0
   66| evaluates is in 𝓜^run. (This is CC2 (a), `CC_code_check.md:48-53`, specialised to LS0.)
   67| B4. *LS0 in the run is the search of 𝒦_n.* The control flow of `local_search` reads only the centre, the move cap, p, K
   68| (`cpp/v3_engine.h:384`), and the models and values F produced by `eval` (`:387-418`: scan order flips j = 0..p−1 then
   69| swaps in ascending order; best by larger F then `lex_less`; strict-improvement rule `:408`; cap rule `:409-411`). The
   70| event context `ev` (`:381, :386, :390`) is bookkeeping and is not read by the control flow. `eval` returns
   71| F = `D.logprior[k]` + lm, where lm is either a fresh scorer value or a cached scorer value of the same model; under
   72| EX-A both are log m(S) exactly (A5). The centre is `m.S` = `start_mode(st, 1000000, TRUE).S` (`cpp/v3_core.cpp:469`), a
   73| function of the data through the start tables `st` (setup, no uniforms), and the cap is ℓ_n + |m.S| (`:473`, with
   74| `o.ls0_ell` = ℓ_n). Hence the sequence of models LS0 evaluates, and its termination, are functions of the data alone and
   75| coincide with the deterministic LS0 of the definition of 𝒦_n (RM `STATEMENT.md:52-53`: complete scans, cap ℓ_n + |S̃₀|,
   76| started from the coded start mode; configuration RM `STATEMENT.md:59-67`), whose scan order, tie rule and stop rules are
   77| those fixed by the code pins W3-RM2 `STATEMENT.md:60-67` (imported by RM2R `STATEMENT.md:39-41`): centre and cap
   78| `cpp/v3_core.cpp:465-476`, scan `cpp/v3_engine.h:394-406`, ties `:392`, strict improvement `:408`, stops `:409-414` —
   79| the very lines read above. (W3-RM:E4 is context only: 𝒦_n is defined from the coded start mode itself.) In particular, on 𝒦_n (that search scores S₀), S₀ is evaluated by LS0 in every completed run, so S₀ ∈ 𝓜^run
   80| by B3. ∎(i)
   81| 
   82| ## Step C — (ii) Link 2: `hpm` = Ŝ⁺
   83| On a completed run, `fit$hpm` = `out$hpm` = `led$hpm$model` (`v3_run.R:141-142`, copied at `v3_fit.R:171`) =
   84| `to_orig(D, L.hpmS)` (`cpp/v3_core.cpp:364`, via `ledger_to_list` at `:510`). By A1 and A3, `led.hpmS` is the running
   85| hpm_better-maximum over the sequence of `offer_stores` calls, i.e. the hpm_better-maximum of 𝓜^run (`hpm_better` is a
   86| strict total order on distinct models with values given by A5: larger F, then smaller size, then lexicographic,
   87| `cpp/v3_util.h:121-126`; a running maximum under a strict total order is the maximum of the offered set). This is
   88| CC2's conclusion "Ŝ = the hpm_better-maximum of 𝓜" (`CC_code_check.md:60-63`). RM and RM2R define Ŝ⁺ as the reported
   89| model (RM `STATEMENT.md:54`), and RM-0's pathwise step uses exactly this description: "the reported HPM Ŝ⁺ — the
   90| ≻-maximum of the scored set" (C-DLV `lemmas/L4_delivery.md:66-70`), with ≻ the HPM order and the scored set the set
   91| of models that joined the final run's all-scored set. That set is 𝓜^run: every score event of the final run
   92| that is an `eval` or `held` event is offered or is a re-visit of an offered model (CC2 (a)–(b), `CC_code_check.md:48-54`),
   93| tables and inherited models are offered directly (CC2 "Other offers", `CC_code_check.md:55-57`); conversely every
   94| offered model was scored (tables `cpp/v3_start.h:93`, inherited `cpp/v3_core.cpp:426`, evaluations `cpp/v3_engine.h:92`). So `fit$hpm` = Ŝ⁺, written in original
   95| indices. 𝓜^run ⊆ Ω by A4. ∎(ii)
   96| 
   97| ## Step D — (iii) The returned list
   98| D1. *What is returned.* `fit$top_store` = `out$top_store` = `led$top` (`v3_run.R:210`, `v3_fit.R:171`) =
   99| `store_to_list(L.top, D)` (`cpp/v3_core.cpp:366`): `models[i]` = `to_orig(D, e.S)` and `value[i]` = `e.v` for the entries e
  100| of the set `L.top.s` in its order (`:358-362`), `capacity` = `L.top.cap` = 40p + 1 (`cpp/v3_ledger.h:78`, p = `D.p` =
  101| p_ret, `cpp/v3_score.h:40`). `to_orig` maps internal indices to `D.orig` (`cpp/v3_core.cpp:38-42`), the retained original
  102| indices `pre$kept` (`v3_fit.R:118`), which are also the names of `pip_primary` (`v3_run.R:160-162`, `setup$ctx$orig`).
  103| D2. *TopStore invariant.* `TopStore` (`cpp/v3_ledger.h:43-57`) holds a `std::set` ordered by `TopCmp` with
  104| `hpm_order = true` (`:46-47`, `:78`): e before e′ iff e.v > e′.v, or e.v = e′.v and |e.S| < |e′.S|, or equal values and
  105| sizes and `lex_less(e.S, e′.S)` (`:37-41`). This is a strict total order on pairs (v, S), and it ranks entries exactly as
  106| `hpm_better` ranks (F, S) (`cpp/v3_util.h:121-126`). By A5 the value is a function of the model, and every model vector offered is in sorted (canonical) form:
  107| `to_internal` sorts (`cpp/v3_core.cpp:34`), blocks are sorted (`cpp/v3_blocks.h:141`, so table models are), `start_mode`
  108| sorts (`cpp/v3_start.h:287`), moves use `sorted_insert`/`sorted_erase` (`cpp/v3_util.h:129-130`), π₀ draws sort (`cpp/v3_start.h:174`), the tie-DP
  109| fallback of `start_mode` appends increasing i (`cpp/v3_start.h:263-266`, used at `:303`), and the enumeration
  110| appends increasing j. Hence two entries are equivalent iff they carry the same model: the set holds distinct models. `offer(v, S)` (`:49-57`): (1) returns if cap = 0; (2) rejects e = (v, S) if the set is full and e is not strictly before the last
  111| element; (3) returns if e is already present; (4) otherwise inserts e and, if the size then exceeds cap, erases the last
  112| element. *Invariant:* after every offer, the set contains only offered entries, has size ≤ cap, and contains the
  113| TopCmp-first entry e* among all entries offered so far. Induction on the offers. Initially the set is empty and nothing
  114| has been offered. *First offer*: the set is empty, so (2) and (3) do not apply; e is inserted, no erasure
  115| (1 ≤ cap), and e = e*. *Later offer* e (e* exists). If e is not strictly before the current e*, then e* stays first; in cases (2) and (3) the set
  116| is unchanged; in case (4) the only erased element is the last one of a set of size cap + 1 ≥ 42 ≥ 2, which is not its
  117| first element, and e* is first (it precedes every element of the set, all of which were offered); so e* stays. If e is
  118| strictly before e*, then e is strictly before every element of the set (e* precedes or equals each of them), in
  119| particular before the last, so (2) does not reject; e is not present (it is strictly before every element), so (3) does
  120| not return; e is inserted as the first element and, the set having size ≥ 2 if an erasure happens, it is not the erased
  121| last element. In all cases the set holds the new e* and only offered entries, with size ≤ cap. ∎(invariant)
  122| D3. *Conclusion.* By A2–A3 the offers to `led.top` on a completed run are exactly the pairs (F(S), S), S ∈ 𝓜^run; by
  123| D2, 𝒯 (the models of `top_store`) consists of distinct elements of 𝓜^run, |𝒯| ≤ 40p + 1, each returned with value F(S)
  124| (A5), in original indices (D1), and 𝒯 contains the TopCmp-first offered entry, which is the hpm_better-maximum of
  125| 𝓜^run (same order, D2). ∎(iii)
  126| 
  127| ## Step E — (iv) Exact branch
  128| On the exact branch `v3_fit` calls `v3_enumerate(ctx)` (`v3_fit.R:121`) = `cpp_enumerate` (`v3_exact.R:7`;
  129| `cpp/v3_core.cpp:524-568`). The recursion `rec` (`:537-555`) starts from S = ∅ (`rec(0)`, `:556`) and, from a sorted S
  130| with |S| < K, calls itself on S ∪ {j} for every j greater than the last element of S (`:553-554`); it therefore visits
  131| every subset of [p] of size ≤ K exactly once, i.e. every S ∈ Ω (Ω = {|S| ≤ K}, K = `D.K` = min(p, ⌊n/2⌋),
  132| `cpp/v3_score.h:40`). At each visit it computes F = `D.logprior[|S|]` + logm (`cpp/v3_core.cpp:539`) and offers (F, S) to its own
  133| `TopStore top` with cap 40p + 1 (`:531`, `:549`). If no `NumericalFailure` occurs, status is "exact" (`:536`, `:556`).
  134| Then: `pip[j]` = numer[j]/total (`:559`) where, by the rescaled streaming log-sum-exp (`:542-547`; each rescale
  135| multiplies numer and total by the same factor), numer[j]/total = Σ_{S∋j} e^{F(S)}/Σ_S e^{F(S)} = PIP_j under EX-A;
  136| `log_Z` = mx + log(total) = log Z (`:557`); `v3_enumerate` names `pip` by `ctx$orig` and sets `mpm` = the retained
  137| columns with pip > 0.5 (`v3_exact.R:8-13`), i.e. MPM; `hpm` is the running hpm_better-maximum over all S ∈ Ω (`cpp/v3_core.cpp:548`).
  138| `v3_fit` copies `fit$pip_primary` = `e$pip`, `fit$mpm` = `e$mpm`, `fit$hpm` = `e$hpm`, and `fit$exact` = `e` (which
  139| contains `top` = `store_to_list(top, D)`, `:565`) (`v3_fit.R:122-127`). By the invariant D2 (same `TopStore` code), 𝒯^ex
  140| (the models of `fit$exact$top`) consists of distinct models of Ω with values F(S) (EX-A) and contains the
  141| hpm_better-maximum of Ω. ∎(iv)
  142| 
  143| ## Step F — (v)
  144| Assume F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}. *Sampler branch, completed run with S₀ ∈ 𝓜^run.* Since 𝓜^run ⊆ Ω (A4) and
  145| `hpm_better` ranks by F first, S₀ is the hpm_better-maximum of 𝓜^run; by (ii) `hpm` = S₀ and by (iii) S₀ ∈ 𝒯.
  146| *Exact branch.* S₀ ∈ Ω (the hypothesis presumes it) is the hpm_better-maximum of Ω; by (iv) `hpm` = S₀ and S₀ ∈ 𝒯^ex. ∎(v)
  147| 
  148| ## Remarks for the checker
  149| - The new code facts relative to CC2 are A2 (the top store receives exactly the HPM's offers), D2 (the store never loses
  150|   its first entry) and B4 (LS0 at code level equals 𝒦_n's search). B1–B3 and C restate CC2 with line references.
  151| - The end-to-end run `numerics/e2e_small.R` (27 small cases through this core) is consistent with (i)–(v): S₀ ∈
  152|   `top_store` and `hpm` = S₀ whenever S₀ was the posterior mode (`numerics/e2e_small_out.txt`). It is falsification only.
```

### [L3] `Theory_work/Wave3/W3-D5P/lemmas/L3_listR.md` @ a2c465a4 — proof of LIST-R
lines 1–107:
```
    1| # L3 — Corollary LIST-R (assembly) — proof
    2| 
    3| [review record omitted]
    4| Consumed, statuses verbatim (registry, main 029bb748): `W3-RM2-R:RM2-R-plus@1.0.1`, `W3-RM2-R:RM0-plus@1.0.1`,
    5| `W3-RM2-R:DLV-0@1.0.1`: [status omitted]
    6|  (each); `W2-APP:POST@1.0.7`: [status omitted]. Internal: LIST-K (L1), LIST-CODE (L2); premise
    7| IMPL-LIST (STATEMENT §1).
    8| 
    9| ## Step 0 — inputs from RM2-R-plus
   10| Under the hypotheses of RM2-R-plus (Setting R, the method as coded, the premises and configuration of RM2R §1, any
   11| X-measurable partition with blocks ≤ 16, and (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, (W-R)), RM2R
   12| `STATEMENT.md:177-182` gives, under the joint law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [MODE], and all
   13| conclusions of RM0-plus (a), (b⁺) with 𝓛′ = 𝓛. We use:
   14| (0.1) for n with s₀ ≤ K: 𝓜_n (S₀ is the unique maximiser of F on Ω) and 𝒦_n are data events, and
   15| P(𝒢⁺_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0, 𝒢⁺_n := 𝓜_n ∩ 𝒦_n: this is RM0-plus (b⁺), a stated conclusion of RM2-R-plus
   16| (RM2R `STATEMENT.md:126-134`, :180): under [MODE], [SAND(Q)], [NA(Q)], [TL(Q)], P(𝒢⁺_n) → 1 (RM2R `STATEMENT.md:131-132`);
   17| (0.2) [POST]: E ε_n → 0, where ε_n = 1 − π(S₀ | y) (RM `STATEMENT.md` §2 interface table, as imported);
   18| (0.3) s₀ ≤ K for all large n: S₀ ⊆ Q and |Q| ≤ K for n ≥ n₀ ((L-feas), RM `STATEMENT.md:98`, part of (L-R^b)); all
   19| statements below are for such n. For the finitely many n with s₀ > K, STATEMENT §1's convention gives 𝓜_n = 𝒦_n = ∅ and
   20| ε_n = 1, so (i) is vacuous and every probability bound of (ii) has right side ≥ 1.
   21| (0.3a) p_ret = p almost surely: under Setting R (rows i.i.d. N(m_n, Σ_n) with unit diagonal, so each column has variance 1 and, with n ≥ 2 independent
   22| rows, is constant with probability 0) no column is constant almost surely, and the code drops a column only when all its entries are exactly equal
   23| (`v3_preprocess.R:111-112`). Hence, almost surely, Ω, K, ℓ_n, 𝒦_n and ε_n computed on the retained columns are those of
   24| the design's p, and POST, stated for the design's p, applies to ε_n.
   25| (0.4) (D) ⇒ every admissible run returns output for every valid non-degenerate input (DLV-0, RM2R
   26| `STATEMENT.md:144-147`), and under Setting R the input is valid and non-degenerate with probability one (RM0-plus (c⁺),
   27| RM2R `STATEMENT.md:138-143`, last sentence).
   28| (0.5) *From the pinned core to the method with the list fields*. L2, RM0-plus and DLV-0 are statements
   29| about the core of record (4676af6); LIST-R is about the method after the pending commit that adds the fields. By
   30| IMPL-LIST (the commit computes the fields as SPEC §2 and §4 prescribe, from the returned list and values of the same
   31| run, and changes no other field and no other state; SPEC §7 A.1–A.2) — and the returned list exists only after the
   32| last runtime-guard consultation (`v3_fit.R:121-122` on the exact branch, after `v3_final_run` at `v3_fit.R:162` on the
   33| sampler branch), after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so DLV-0's guard and MACH
   34| accounting are unaffected — on every input and every
   35| realisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation up to the new
   36| fields, and the new computation can end the fit with an error only through SPEC §4's duplicate-model row. That row
   37| cannot fire on an output run: the sampler store `top_store` and the exact store 𝒯^ex hold distinct models (L2 (iii),
   38| (iv)). Hence the post-commit fit returns if and only if the pinned fit returns, and 𝒪, `status`, `hpm`, `top_store`,
   39| `fit$exact` (with its store) and every other existing field are those of core 4676af6. So L2, RM0-plus (b⁺) and DLV-0
   40| apply to the method with the list fields, and the new fields are SPEC's functions of the pinned outputs.
   41| The reader assumptions (A1)–(A6) of Theorem 6 imply these hypotheses through READER §6 bridges B6.1–B6.4 (this file
   42| does not re-prove them; the corollary is stated with "the hypotheses of RM2-R-plus").
   43| 
   44| ## Step 1 — (i): the pathwise statement on 𝒢⁺_n
   45| Fix n with s₀ ≤ K, a data set in 𝒢⁺_n, and an admissible run (any seed, N_e, R′, calibration outcome) that returns
   46| output (event 𝒪); by (0.5) its existing fields are those of the pinned core, so L2 applies. Output occurs only on the two branches: `estimates_available` becomes TRUE only at
   47| `v3_fit.R:129` (exact branch) or through `v3_fit.R:171` from `v3_run.R:218` (sampler branch), both after `branch_run` is set
   48| (`v3_fit.R:106`); the earlier returns (`v3_fit.R:89`, `:102`) keep the initial FALSE (`v3_fit.R:78`). By L2 (i), on the sampler branch 𝒪 = {status "completed"}; on the exact branch 𝒪 = {status "exact"}
   49| (`v3_fit.R:125-129`: `estimates_available` TRUE iff `e$status == "exact"`; otherwise `:130-131` returns with it FALSE).
   50| *Sampler branch.* By L2 (i) (B4), since the data set is in 𝒦_n, S₀ ∈ 𝓜^run. Since it is in 𝓜_n, F(S₀) > F(S) for
   51| every S ∈ Ω ∖ {S₀}; by L2 (v), S₀ ∈ 𝒯 and `hpm` = S₀. By L2 (iii), 𝒯 ⊆ Ω is a set of distinct models returned with the
   52| values F(S). By IMPL-LIST and the identification of STATEMENT §1 (under EX-A, SPEC §2 applied to models with values
   53| F(S) gives, for every retained column j, `pip_list[j]` = Σ_{S∈𝒯, j∈S} e^{F(S)−F_max} / Σ_{S∈𝒯} e^{F(S)−F_max} = pip_𝒯(j),
   54| `mpm_list` = mpm_𝒯 and `log_Z_list` = F_max + log Σ_{S∈𝒯} e^{F(S)−F_max} = logZ_𝒯). SPEC §4's exceptional rows do not
   55| fire: the values are F(S), finite under EX-A (the scorer never fails for yᵀy > 0: Lemma S.2, RM2R
   56| `STATEMENT.md:151-152`); 𝒯 ∋ S₀ is not empty; 𝒯 consists of distinct models (L2 (iii)). So the three fields are
   57| present and not NA on every output run of the sampler branch. LIST-K applies with this 𝒯
   58| (S₀ ∈ 𝒯 ⊆ Ω) and gives:
   59|  max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n (LIST-K (a)); max_j |pip_list[j] − PIP_j| ≤ ε_n (LIST-K (b));
   60|  log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z (LIST-K (d)); and if ε_n < ½, `mpm_list` = S₀ = MPM (LIST-K (c)), hence
   61|  `mpm_list` = `hpm` = S₀ = MPM.
   62| *Exact branch.* By L2 (iv), `pip_primary` = PIP and `mpm` = MPM; by IMPL-LIST (SPEC §4), `pip_list` = PIP and
   63| `mpm_list` = MPM. LIST-K (e) (S₀ ∈ Ω, since s₀ ≤ K) gives max_j |PIP_j − 1{j ∈ S₀}| ≤ ε_n, and MPM = S₀ if ε_n < ½;
   64| trivially max_j |pip_list[j] − PIP_j| = 0 ≤ ε_n. On 𝓜_n, L2 (v) gives `hpm` = S₀ and S₀ ∈ 𝒯^ex. When `log_Z_list` is
   65| not NA it is logZ_{𝒯^ex} (IMPL-LIST, SPEC §4) with 𝒯^ex ⊆ Ω distinct, values F(S) (L2 (iv)), S₀ ∈ 𝒯^ex; LIST-K (d)
   66| gives log Z + log(1 − ε_n) ≤ log_Z_list ≤ log Z.
   67| No property of the seed, N_e, R′ or calibration outcome was used beyond admissibility, and the data event 𝒢⁺_n does not
   68| depend on them. ∎(i)
   69| 
   70| ## Step 2 — (ii): probability bounds
   71| Fix t ∈ (0, ½) and an admissible run specification (seed, N_e, R′; the calibration outcome is then a function of the
   72| data and the calibration streams). Consider a data set in 𝒢⁺_n ∩ {ε_n ≤ t} and a realisation of the run in 𝒪. By
   73| Step 1, max_j |pip_list[j] − 1{j ∈ S₀}| ≤ ε_n ≤ t and max_j |pip_list[j] − PIP_j| ≤ ε_n ≤ t, so B₁(t), B₂(t) fail; if
   74| `log_Z_list` is not NA, |log_Z_list − log Z| ≤ ε_n/(1 − ε_n) ≤ 2ε_n ≤ 2t (LIST-K (d) and its corollary; ε_n ≤ t < ½),
   75| so B₃(t) fails. Hence, as sets of (data, run randomness),
   76|   𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t)) ⊆ (𝒢⁺_nᶜ ∪ {ε_n > t}) × (run randomness),
   77| and likewise, since on 𝒢⁺_n ∩ {ε_n < ½} ∩ 𝒪 Step 1 gives `mpm_list` = `hpm` = S₀,
   78|   𝒪 ∩ B₄ ⊆ (𝒢⁺_nᶜ ∪ {ε_n ≥ ½}) × (run randomness).
   79| Taking probabilities under the joint law (for the left sides: their probability, or outer probability if measurability
   80| is not assumed — the right sides are data events): P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t) and
   81| P(𝒪 ∩ B₄) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n ≥ ½), by (0.1). The right sides tend to 0: (0.1), and Markov's inequality with
   82| (0.2): P(ε_n > t) ≤ E ε_n / t → 0 and P(ε_n ≥ ½) ≤ 2E ε_n → 0.
   83| *Rate.* Let p ≥ 2 for all large n. (T1-R) is hypothesis LSF of POST (RM `STATEMENT.md:128-133` defines (T1-R) as
   84| "the LSF conditions of APP L1_POST(b)"), Setting R is POST's setting with the standardised-signal convention
   85| (`L1_POST.md:8-18`), and POST (b) (`L1_POST.md:31-33`) gives, under the joint law, 1 − π(S₀) = O_P(r_n), r_n = √(log n/n).
   86| Let t_n ∈ (0, ½) be deterministic with t_n/r_n → ∞. Given η > 0, choose M and n₀ with P(ε_n > M r_n) < η for n ≥ n₀;
   87| for n ≥ n₁ ≥ n₀, t_n ≥ M r_n, so P(ε_n > t_n) < η. Hence P(ε_n > t_n) → 0, and with 𝒢♯_n := 𝒢⁺_n ∩ {ε_n ≤ t_n},
   88| P(𝒢♯_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0. On 𝒢♯_n, every admissible output run satisfies, by Step 1 and the
   89| argument above with t = t_n: max_j |pip_list[j] − 1{j ∈ S₀}| ≤ t_n, max_j |pip_list[j] − PIP_j| ≤ t_n, |log_Z_list − log Z|
   90| ≤ 2t_n when `log_Z_list` is not NA, and (ε_n ≤ t_n < ½) `mpm_list` = `hpm` = S₀. ∎(ii)
   91| 
   92| ## Step 3 — (iii): with delivery
   93| Under (D), by (0.4) and (0.5), P(𝒪ᶜ) = 0 for every admissible run of the method with the list fields. Hence for any event B of the run, P(B) ≤ P(𝒪 ∩ B) + P(𝒪ᶜ) =
   94| P(𝒪 ∩ B), and Step 2 gives P(B₄) → 0 and P(B₁(t) ∪ B₂(t) ∪ B₃(t)) → 0 for every t ∈ (0, ½), and, when p ≥ 2 for all
   95| large n, P(B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n)) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0 for every deterministic t_n ∈ (0, ½) with
   96| t_n/r_n → ∞.
   97| *"i.e. O_P(r_n)".* Let X_n ≥ 0 be any of the three errors (for the evidence, X_n := ½|log_Z_list − log Z| on
   98| {`log_Z_list` not NA}, and 0 otherwise), so that {X_n > t} ⊆ B₁(t) ∪ B₂(t) ∪ B₃(t). Suppose X_n ≠ O_P(r_n). Then there is η > 0 such that for every M and every N some n ≥ N has P(X_n > M r_n) ≥ η. Since r_n → 0, we can choose n₁ < n₂ < … such that, for every k, r_n ≤ min(k⁻², 1/16) for all n ≥ n_k and P(X_{n_k} > k r_{n_k}) ≥ η. Define t_n := k r_n for n_k ≤ n < n_{k+1}, and t_n := ¼ for n < n₁. For n_k ≤ n < n_{k+1}: t_n = k r_n ≤ k·k⁻¹√r_n = √r_n ≤ ¼ (as r_n ≤ k⁻²), so t_n ∈ (0, ½); and t_n/r_n = k → ∞ as n → ∞. But P(X_{n_k} > t_{n_k}) = P(X_{n_k} > k r_{n_k}) ≥ η for every k, contradicting P(B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n)) → 0. Hence each error is O_P(r_n). ∎(iii)
   99| 
  100| ## Remarks for the checker
  101| - Step 1 is where the two DIST links are used: L2 (i) turns "the run returns output" into "status completed, and LS0
  102|   ran in this run"; L2 (ii)–(iii) turn RM's Ŝ⁺ into the printed `hpm` and put S₀ into `top_store`.
  103| - The only data-level inputs are (0.1)–(0.3) and POST (b); no sampler law (no W1-N1 premise) is used: the claim is
  104|   pathwise in the run.
  105| - IMPL-LIST is used twice: in (0.5), to carry L2, RM0-plus and DLV-0 from the pinned core to the method with
  106|   the list fields ("changes no other field and no other state"); and in Step 1, to identify the printed fields with
  107|   pip_𝒯, mpm_𝒯, logZ_𝒯 (sampler branch) and with PIP, MPM, logZ_{𝒯^ex} (exact branch).
```

### [SPEC] `Theory_work/Wave3/W3-D5P/sources/SPEC_LIST_PIP_523dda23.md` @ a2c465a4 — definition of the output fields
lines 1–81:
```
    1| <!-- carrier copy of SPEC_LIST_PIP.md at commit 523dda23 -->
    2| # SPEC — list-renormalised PIPs and their median model
    3| 
    4| Owner-approved method companion to #5′. **Nothing existing changes:** `pip_primary` (the equal-weight island mean) and
    5| `mpm` stay the primary outputs; the new fields are additional, are computed after everything else, read no random
    6| numbers and alter no state. Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (core last changed at 72785fe).
    7| 
    8| ## 1. The list
    9| 𝒯 := the returned top store, `fit$top_store` (`v3_run.R:210`, from `led$top`, `:170`), as exported by `store_to_list`
   10| (`cpp/v3_core.cpp:358-362`): `models` (a list of integer vectors of **original** column indices, `to_orig`), `value`
   11| (the scores F(S) = log ϖ(S) + log m(S), one per model), `capacity` = 40p + 1 (`cpp/v3_ledger.h:78`), `full`. The store
   12| holds distinct models, best first under the HPM order (`cpp/v3_ledger.h:32-56`). Let m = length(models), F_i = value[i].
   13| 
   14| ## 2. Definition
   15| For every retained column j (the names of `pip_primary`, `v3_run.R:160-162`), with F_max := max_i F_i and
   16| u_i := exp(F_i − F_max):
   17| 
   18|     pip_list[j] := ( Σ_{i : j ∈ models[i]} u_i ) / ( Σ_{i=1}^{m} u_i ),
   19|     mpm_list    := { j : pip_list[j] > 0.5 }   (strict, the rule of `mpm`, `v3_run.R:163`; increasing original indices),
   20|     log_Z_list  := F_max + log( Σ_{i=1}^{m} u_i ).
   21| 
   22| In words: the posterior over models renormalised to the returned list, its inclusion probabilities, their median
   23| model, and the log of the list's total unnormalised weight (on the scale of the printed `log_Z`).
   24| 
   25| ## 3. Numerical rules
   26| - Log-sum-exp as written: subtract F_max before exponentiating; never exponentiate F_i itself.
   27| - Both sums run over the store **from the last entry to the first** (smallest weights first), in double precision, no
   28|   compensated summation. The result is then deterministic within an implementation.
   29| - Core v3 and engine v4 may differ in the last bits of `exp`; they must agree to 1e−12 in `pip_list` and `log_Z_list`.
   30| - Clamp nothing. By construction 0 ≤ pip_list[j] ≤ 1 up to rounding; a value outside [−1e−12, 1 + 1e−12] is a bug.
   31| 
   32| ## 4. Cases
   33| | Case | Rule |
   34| |---|---|
   35| | Status `completed` (sampler branch) | compute the three fields from `top_store` |
   36| | Status `exact` (enumeration branch, `v3_fit.R:122-127`) | `pip_list := pip_primary`, `mpm_list := mpm` (already exact), `log_Z_list` from the store if it is returned, else NA; `pip_list_source = "exact"` |
   37| | Any other status (`resource_limit`, `invalid_input`, `no_predictors`, `y_constant`, `numerical_failure`, calibration failure; `v3_fit.R:84-158`) | the fields are absent (NULL), also when partial results are returned |
   38| | Single model in the list | `pip_list` is its indicator; `mpm_list` is that model; `log_Z_list` = its score |
   39| | The empty model in the list | it contributes to the denominator only |
   40| | Exact tie, pip_list[j] = 0.5 | j is not in `mpm_list` (strict rule) |
   41| | A column in no listed model / in every listed model | pip_list[j] = 0 / = 1 exactly |
   42| | Empty list (m = 0) on a completed run | must not occur; set the fields to NA, `pip_list_flag = "empty_list"`, and fail the test suite |
   43| | Duplicate models in the list | must not occur (the store is a set); detect and stop with an error, do not merge |
   44| | A non-finite score | −Inf entries get weight 0; NaN or +Inf: fields NA, `pip_list_flag = "nonfinite_score"` |
   45| 
   46| ## 5. Field names
   47| `pip_list` (named numeric vector, same names and order as `pip_primary`), `mpm_list` (integer vector, as `mpm`),
   48| `log_Z_list` (numeric), `list_size` (= m), `list_full` (= `top_store$full`), `pip_list_source` ("store" or "exact"),
   49| `pip_list_flag` (NULL when clean).
   50| 
   51| ## 6. Relation to #5′
   52| These are the quantities #5′ is about. In exact arithmetic `pip_list[j]` = π(j ∈ S | S ∈ 𝒯, y) and
   53| `log_Z_list` = log Z + log π(𝒯 | y). If the list contains S₀, then for every data set
   54| max_j |pip_list[j] − 1{j ∈ S₀}| ≤ 1 − π(S₀ | y), `mpm_list` = S₀ whenever 1 − π(S₀ | y) < ½, and
   55| log Z + log π(S₀ | y) ≤ `log_Z_list` ≤ log Z. #5′ will supply "the list contains S₀" on the designs inside Theorem 6.
   56| The fields say nothing by themselves about how much posterior mass the list holds; `log_Z − log_Z_list` is a rough,
   57| uncertified indication (the printed `log_Z` is an estimate).
   58| 
   59| ## 7. Acceptance tests for Engineering
   60| **A. Nothing existing moves (golden tests).**
   61| 1. On the production-hash set (the 24 + 10 cases already used for the engine comparison) and on one fit per status path
   62|    of §4: every existing field of the fit is `identical()` before and after the change — `hpm`, its score and
   63|    provenance, `pip_r`, `pip_primary`, `mpm`, `log_Z` and per-island values, `top_store` (models, value, capacity,
   64|    full), both leader stores, near ties, flags, local-search and LS0 records, score counts, grid. Timings excluded.
   65| 2. The fit with the new fields removed serialises to the same hash as the old fit.
   66| 3. Same seed, two runs: the new fields are `identical()`.
   67| 
   68| **B. The new fields, by hand.**
   69| 4. Store {1}, {1, 2}, {3} with scores c + log 0.5, c + log 0.3, c + log 0.2: `pip_list` = (0.8, 0.3, 0.2) on columns
   70|    1, 2, 3; `mpm_list` = {1}; `log_Z_list` = c. Run with c = 0, c = 1000 and c = −1000: same `pip_list` to 1e−12.
   71| 5. One model {2, 5}: `pip_list` is 1 on columns 2 and 5 and 0 elsewhere; `mpm_list` = {2, 5}.
   72| 6. Store ∅ and {1} with equal scores: pip_list[1] = 0.5; `mpm_list` is empty.
   73| 7. Two models whose scores differ by 800: no NaN, no Inf; `pip_list` equals the indicator of the better model to 1e−12.
   74| 8. A design with a constant raw column (dropped): names of `pip_list` equal names of `pip_primary`.
   75| 9. A small problem on the enumeration branch whose store holds every model: the formula of §2 applied to the store
   76|    equals the exact PIPs to 1e−10.
   77| 10. Invariants on every golden case: 0 ≤ `pip_list` ≤ 1; with S* the first listed model and w* its renormalised weight,
   78|     max_j |pip_list[j] − 1{j ∈ S*}| ≤ 1 − w* + 1e−12; permuting the store changes `pip_list` by at most 1e−12.
   79| 11. A `resource_limit` fit and a failed calibration: the new fields are absent.
   80| 12. Core v3 against engine v4 on the golden set: `pip_list` and `log_Z_list` within 1e−12; `mpm_list` identical unless
   81|     some pip_list[j] is within 1e−9 of 0.5 (report those cases).
```

### [RM2R] `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` @ a2c465a4 — consumed: RM0-plus, DLV-0, RM2-R-plus (as stated)
lines 33–60:
```
   33| ## 1. Base (taken unchanged)
   34| 
   35| * Settings F and R, method objects, the events Sand_n(Q), NA(𝓛), TL(𝓛), 𝒦_n, 𝒪, U_n, Ŝ⁺, implementation premises
   36|   (EX-A, EX-S, SR, GUARD-W, OP-LS0, complete scans), the configuration (`ls0 = TRUE`, `ls0_ell = ℓ_n`,
   37|   `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp = TRUE`), "admissible run": RM `STATEMENT.md:32-68` as imported by
   38|   PARENT `STATEMENT.md:47-58`.
   39| * Code pins of PARENT `STATEMENT.md:60-68` (LS0 centre, scan, stop rules; Lemma E4 = W3-RM:E4@1.0.0); the pins are
   40|   re-read against the core as on this branch (commit 2aeb860; `Scripts/SMC_BVS/core/` last changed at 72785fe) in the
   41|   lemma files; any difference is reported, not assumed away.
   42| * Notation and functionals: PARENT `STATEMENT.md:70-94` — q, 𝓛, 𝔓, β_{B,l}, β(η, A), a⁰_n, 𝔴⁰_n, 𝔴_n(δ), 𝒟ᵀ_n,
   43|   **d_n := E max_{v∈𝒟ᵀ_n}|vᵀg|**; and **λ_n := (n − 1)φ₀²θ*²_min/σ²** (PARENT `lemmas/L2_width.md:185`).
   44| * Interface properties [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [E4]: PARENT `STATEMENT.md:96-104`.
   45| * Assumptions of PARENT §3 not named in §2 below, unchanged: (FL) = (FL-16) + (FL-Q), (L^b) = (L-size^b) + (L-feas) +
   46|   (L-gain) with b < β(η, A), (W) and its sufficient forms, the block-relative forms (PARENT `STATEMENT.md:128-171`,
   47|   except (V), (T1-F), (BM-W)); all of Form R (PARENT `STATEMENT.md:172-202`); the constants of PARENT
   48|   `STATEMENT.md:112-124`.
   49| * **The toolkit constant.** C_R := 3(M + σ²) (PARENT `lemmas/L0_toolkit_b.md:38`), where M is the energy constant of
   50|   (T1-F) (‖μ‖² ≤ Mn).
   51| 
   52| ## 2. Definitions and hypotheses that change
   53| 
   54| **New event and interface property (T2(b)).** For n with s₀ ≤ K:
   55|   **𝓜_n := {S₀ is the unique maximiser of F on Ω}** (F(S) = log w(|S|) + log m(S), RM `STATEMENT.md:34-37`),
   56| a data event; and
   57| | id | property | consumed by |
   58| |---|---|---|
   59| | [MODE] | P(𝓜_n) → 1 | RM0-plus |
   60| Since π(S) ∝ exp F(S) on Ω, {π(S₀) > ½} ⊆ 𝓜_n; hence P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)] and **[POST] ⇒ [MODE]**.
```
lines 116–163:
```
  116| ## 3. Claims on the core and on delivery (T2)
  117| 
  118| **(C0⁺) Theorem RM0-plus (core; any design; deterministic statement plus one inequality).** Let Q ⊇ S₀ be
  119| deterministic with |Q| ≤ K. Under the implementation premises and configuration of §1 and the hypotheses of Lemma E4:
  120| (a) RM-0(a) as stated at RM `STATEMENT.md:162-167` (unchanged).
  121| (a′) [T2(c)] For every deterministic 𝓛′ ⊆ 𝓛 down-closed in 𝓛: on St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′), LS0 from the coded
  122| start mode S̃₀ performs exactly |S̃₀ ∖ S₀| moves, each deleting one element of S̃₀ ∖ S₀, visits only sets T with
  123| S₀ ⊆ T ⊆ S̃₀ (all in 𝓛′), and ends at S₀ with a completed scan that finds no strict improvement; the cap ℓ_n + |S̃₀| is
  124| not binding; the archive statement of RM-0(a) holds. Hence 𝒦_nᶜ ⊆ St_n(𝓛′)ᶜ ∪ NA(𝓛′)ᶜ ∪ TL(𝓛′)ᶜ, and
  125| St_n(𝓛′) may be replaced by its sufficient form Sand_n(𝓛′).
  126| (b⁺) [T2(b)] For n with s₀ ≤ K, pathwise, for every admissible run (every seed, N_e, R′ and calibration outcome):
  127|   𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ,
  128| a data event. With 𝒢⁺_n := 𝓜_n ∩ 𝒦_n, every admissible output run reports Ŝ⁺ = S₀ on 𝒢⁺_n, and
  129|   P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒢⁺_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ),  P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)],
  130|   P(𝒦_nᶜ) ≤ P(St_n(𝓛′)ᶜ) + P(NA(𝓛′)ᶜ) + P(TL(𝓛′)ᶜ) for every 𝓛′ as in (a′) (in particular 𝓛′ = 𝓛),
  131| uniformly over the run parameters. Under [MODE] and P(St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′)) → 1 for some such 𝓛′ (in
  132| particular under [SAND(Q)], [NA(Q)], [TL(Q)]): P(𝒢⁺_n) → 1 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). On enumeration
  133| branches 𝒦_n refers to the hypothetical search, and there 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ. RM-0(b) is the special case that
  134| uses {π(S₀) > ½} ⊆ 𝓜_n.
  135| (c⁺) [T2(a) + (b)] Assume in addition the delivery premises (D). Then for every valid non-degenerate input every
  136| admissible run returns output (DLV-0), so for every admissible run
  137|   {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ  on the set of valid non-degenerate inputs,
  138| and, for any law of the data under which the input is valid and non-degenerate with probability one,
  139|   P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) [mode failure] + P(𝒦_nᶜ) [search failure],
  140| uniformly over seeds, N_e, R′ and calibration outcomes; under the conditions of (b⁺), P(Ŝ⁺ = S₀) → 1, without
  141| "on output". Under Setting F (fixed standardised X with non-constant columns, model G) and Setting R the input is
  142| valid and non-degenerate with probability one.
  143| 
  144| **(C-D) Lemma DLV-0 (deterministic delivery).** Under the implementation premises and configuration of §1 and the
  145| delivery premises (D): for every valid non-degenerate input, every seed and every realisation of the method's
  146| uniform streams, the coded fit (`v3_fit`, core as pinned in §1) returns with `estimates_available = TRUE`; without
  147| the representability lift of IDEAL-W⁺, the same holds for every such input in the supported domain 𝔇 of §2. No data
  148| law, no model and no design class enters. DLV-0 is a delivery statement only; it asserts nothing about Ŝ⁺.
  149| **Law-free inputs, cited (and only these):** the exit walk of Theorem D (DLV `lemmas/L4_delivery.md:13-42`), in which the
  150| data law enters only through Lemma S.1's null sets for A3–A5 (`lemmas/L2_degenerate.md:5-18`) — replaced here by the
  151| deterministic "valid non-degenerate input[status omitted]
  152| 
  153| for every valid input, every seed and every realisation", `lemmas/L1_resources.md:70-81, 129-143`); grid Lemmas 3.3,
  154| 3.4 (`lemmas/L3_grid.md:30-56`); and the **delivery half only** of Proposition F, in the restated form of
  155| `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md:32-35` ("Under the premises of Theorem D, P(𝒰_n) = 0 for every
  156| n ≥ 3"). The standalone sentence of DLV `lemmas/L4_delivery.md:83-84` ("on the classes above … P(Ŝ⁺ = S₀) → 1
  157| unconditionally") is **not** consumed: it imports Corollary D′'s statistical hypotheses (HQ note,
  158| `API_AUDIT/pass1/TRIAGE.md:23-28`). Consistency in this file comes only from RM0-plus (b⁺)/(c⁺) with [MODE] and the
  159| lattice properties as explicit hypotheses. Templates (no conclusion consumed beyond their delivery step): FACA
  160| `lemmas/L7_delivery.md` Step 2, W2-UNI `lemmas/L5_delivery.md` Step 2. The proof re-audits the exit walk, the
  161| fallback and the resource bounds against the code as pinned. **Scope note:** DLV-0 refers to the core as pinned; Lemma R (DLV `lemmas/L1_resources.md:70-81`) and the
  162| allocation 𝒜_n must be re-audited when v3.2 freezes (the preflight charge changes).
  163| 
```
lines 177–182:
```
  177| **(C2⁺) Theorem RM2-R-plus (Gaussian rows, polynomial leakage).** Setting R, the method as coded, any X-measurable
  178| partition with blocks ≤ 16. Assume the hypotheses of RM2-R (PARENT `STATEMENT.md:216-218`: (T1-R), (FL-R), (V-R),
  179| (L-R^b) with 15ρ + b < ½, (W-R)). Then, under the joint law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [MODE],
  180| hence all conclusions of RM0-plus (a), (b⁺) as in (C1⁺); under in addition (D), every admissible run returns output
  181| and P(Ŝ⁺ = S₀) → 1 with P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ).
  182| 
```

### [RM] `Theory_work/Wave3/W3-RM/STATEMENT.md` @ a2c465a4 — consumed objects, events, configuration, Form R hypotheses
lines 32–68:
```
   32| ## 1. Settings, method objects, events
   33| 
   34| * **Setting F (fixed design)** = GROW `STATEMENT.md` §1 (D0 score, capped BB(1, p) prior w, K = min(p, ⌊n/2⌋),
   35|   Ω = {|S| ≤ K}, F(S) = log w(|S|) + log m(S), block tables r_b, start law γ₀ ∝ w(|S|)∏_b r_b(S ∩ C_b), start mode S̃₀;
   36|   model G: fixed raw design, y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), σ² > 0 fixed; X centred and standardised,
   37|   μ = Xθ*, S₀ = supp θ*, s₀ = |S₀| ≥ 1 fixed, p = p_n ≤ n^A, A ≥ 1 fixed). Notation: P_T projector on span X_T;
   38|   R̂_T := X_TᵀX_T/(n − 1); for l ∉ T with (I − P_T)x_l ≠ 0: u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖,
   39|   **δ_{T,l} := u_{T,l}ᵀμ** (so δ²_{T,l} = ‖(P_{T∪{l}} − P_T)μ‖², the gain in explained mean when l joins T),
   40|   Z_{T,l} := u_{T,l}ᵀε/σ. θ*_min := min_{S₀}|θ*_j|.
   41| * **Setting R (Gaussian rows)** = UNI `STATEMENT.md` §1 design (R) / LOC2 `STATEMENT.md` §1: raw rows iid
   42|   N(m_n, Σ_n), Σ_n unit-diagonal, X centred and sample-standardised, Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the
   43|   raw design, σ² > 0 fixed [C1-B7], s₀ fixed, |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀, p ≤ n^A (p ≫ n allowed). W denotes a
   44|   population row.
   45| * **Move cap.** ℓ_n := ⌈log₂(n + p + 1)⌉ (the method's base cap); LS0's shipped cap is ℓ_n + |S̃₀| [C1-B4].
   46| * **Blocks.** The method's partition C₁, …, C_J (complete linkage on 1 − |r̂|, cut at B = min(⌊√n⌋, ⌊√p⌋, 16), next-fit
   47|   packing; SoP `Theory_work/State_of_Project/sections/02_method.tex:187-211`): an X-measurable partition with
   48|   |C_b| ≤ 16. Nothing else about the partition is used anywhere below.
   49| * **Events** (GROW L1, L3, L4), for a deterministic Q ⊇ S₀ with |Q| ≤ K and 𝓛 := {T : S₀ ⊆ T ⊆ Q}:
   50|   Sand_n(Q) := {S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω};
   51|   NA(𝓛) := {F(T ∪ {l}) < F(T) for all T ∈ 𝓛 with |T| < K, l ∉ T};
   52|   TL(𝓛) := {F(A) < F(T) for every T ∈ 𝓛 and every feasible neighbour A of T with S₀ ⊄ A};
   53|   𝒦_n := {the deterministic LS0 (complete scans, cap ℓ_n + |S̃₀|) started from the coded start mode scores S₀}
   54|   (a data event: LS0 reads no uniforms); 𝒪 = the run returns output; Ŝ⁺ = reported model; U_n = 𝒪ᶜ.
   55| * **Implementation premises** (named, not proved; as UNI `STATEMENT.md` §1 / FIN §1.4): EX-A, EX-S, SR, GUARD-W,
   56|   OP-LS0, complete scans; IND-T and the c₄ search when R′ > 4 (execution conventions of the method: they do not enter
   57|   the start, lattice, posterior or pathwise-reporting arguments of (C0)–(C2) [R08-20]); CAL only where M5(0) is cited in
   58|   its D_n form.
   59|   **[R01-2] Configuration.** Throughout, OP-LS0 includes the shipped options `ls0 = TRUE`, `ls0_ell = ℓ_n`,
   60|   `ls0_cap = "ell_n_plus_mode"` (the public option; it sets the internal field `ls0_cap_plus_mode`, cap ℓ_n + |S̃₀|)
   61|   [R08-19] and `ls0_tie_dp = TRUE`: every successfully completed SMC output run in
   62|   this configuration executes LS0 from `start_mode(...).S`; the exact branch scores every feasible model, and there 𝒦_n
   63|   refers to the hypothetical deterministic search (PACK `lemmas/I1_e4_replacement.md:150-153`). All quantifiers over
   64|   seeds, N_e, R′ and calibration outcomes range over valid inputs satisfying the implementation and execution premises
   65|   (admissible runs). EX-A is an idealisation (exact arithmetic), not a binary64 theorem.
   66|   **e4 is not a premise here**: it is replaced by Lemma E4 (§4 (C3)), whose hypotheses are N3's encoding and execution
   67|   conditions (H1) — strengthened to include the inverse maps, see (C3) — and (H4), and EX-A for the start-mode
   68|   arithmetic (H2).
```
lines 94–136:
```
   94|   (FL-Q) λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p].
   95| * **(V) Visibility.** There is a deterministic M_n → ∞ such that for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with
   96|   |U| ≤ 15: δ²_{U,j} ≥ M_n log n. ("No truth is masked by conditioning on at most 15 variables.")
   97| * **(L) Bounded leakage.** A deterministic Q = Q_n with S₀ ⊆ Q ⊆ [p] such that
   98|   (L-size) |Q| ≤ (log n)^κ; (L-feas) |Q| ≤ K, and Q = [p] or K ≥ 2|Q| + 32s₀ + 1, for n ≥ n₀;
   99|   (L-gain) [P2] for every l ∉ Q and every U ⊆ [p] ∖ {l} with |U| ≤ 15: **δ²_{U,l} ≤ η τ²_U log n**, where
  100|   τ²_U := σ² + ‖(I − P_U)μ‖²/(n − 1) is the residual variance that the set U leaves (noise plus unexplained mean energy).
  101|   ("Outside Q no column gains more than η log n times the residual variance, given any ≤ 15 other columns." Since
  102|   τ²_U ≥ σ², the locked v1.1 form δ²_{U,l} ≤ ησ² log n is a sufficient special case.)
  103| * **(N) Lattice condition.** One of:
  104|   **(N-χ)** |Q ∖ S₀| ≤ (1 − δ₀) log n — nothing else;
  105|   **(N-D)** bounded direction complexity and a signal floor at the lattice scale:
  106|   (i) there are a deterministic finite set 𝒰_n of unit vectors of ℝⁿ and deterministic ρ_n ≥ 0 with
  107|       log|𝒰_n| ≤ log p + h log n for a fixed h < ½ [P1] (v1.1: log p + o(log n)) and ρ_n²(|Q| + log n) = o(log n),
  108|       such that for every T ∈ 𝓛 and l ∉ T some
  109|       v ∈ 𝒰_n ∩ span(X_{Q∪{l}}) has ‖u_{T,l} − v‖ ≤ ρ_n;
  110|   (ii) (BM-Q) θ*²_min nφ₀²/(σ²(|Q| + log n)) → ∞.
  111|   Sufficient for (N-D)(i) — **(N-loc)**: for every l ∈ [p] a set N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
  112|   limsup ν_n/log n < 1/(2 log 2) [P1] (v1.1: ν_n = o(log n)), such
  113|   that ‖(P_T − P_{T∩N_l})x_l‖ ≤ ρ_n‖(I − P_T)x_l‖ for all T ∈ 𝓛 with l ∉ T, with the same deterministic ρ_n and rate
  114|   as in (i) [R01-Q5] (then 𝒰_n := {u_{T∩N_l,l} : T ∈ 𝓛, l ∉ T}, |𝒰_n| ≤ p2^{ν_n}). In particular (N-D)(i) holds with
  115|   ρ_n = 0 whenever limsup |Q|/log n < 1/(2 log 2) (take N_l = Q ∖ {l}), and (N-D)(i) itself (ρ_n = 0, exact directions) contains GROW's
  116|   (G4-dir); (N-loc) is not claimed to contain every low-complexity direction family. Convention [R07-4]: if
  117|   Q = S₀ = [p] there is no pair (T, l); NA(𝓛) is vacuous, 𝒰_n may be any nonempty finite set and, in (D-R), L_n := 0.
  118| * **Block-relative forms (weaker; what the proof consumes).** (V_b) = GROW (G3b): (V) only for U ⊆ C_{b(j)} ∖ {j}.
  119|   (L_b): (L-gain) only for U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l} (with σ² in place of τ²_U this is GROW (G3c)).
  120|   (FL_b) = GROW (G3a) + (FL-Q).
  121|   Claim (B1) below: (V), (L), (FL) imply (V_b), (L_b), (FL_b) for **every** partition into blocks of size ≤ 16, and
  122|   conversely the block-relative forms for every such partition imply the partition-free ones (Lemma B1′). The
  123|   block-relative forms refer to the method's blocks for one reason only: (L_b) conditions on the truths of l's own
  124|   block, so it lets Q omit a column whose only gain is un-conditioned on a truth that the method happens to place in
  125|   the same block; a partition-free condition cannot know this and must put such columns in Q.
  126| 
  127| ### 3.2 Gaussian rows (conditions on (Σ_n, θ*) only)
  128| 
  129| * **(T1-R) Theorem 1's conditions** = (A1-post) of UNI `STATEMENT.md` §2, i.e. the LSF conditions of APP L1_POST(b)
  130|   [R01-opt]: with j₀ = ⌈(2A + 1)s₀⌉ + 1, m̄_n = ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ and
  131|   k̄_n = min{p, s₀ + max(j₀, m̄_n)}: for a fixed φ > 0, λ_min(Σ_{n,S}) ≥ φ² whenever |S| ≤ min(p, s₀ + j₀), and
  132|   λ_min(Σ_{n,S}) ≥ ψ_n whenever |S| ≤ k̄_n, with ψ_n√n/(log n)^{3/2} → ∞. No upper spectral bound.
  133|   Sufficient: λ_min(Σ_n) ≥ c.
  134| * **(FL-R)** λ_min(Σ_{n,S}) ≥ c for every S with |S| ≤ 16 + s₀, and for S = Q ∪ {l}, l ∈ [p].
  135| * **(V-R) Visibility** = PTV(a₀) (APP `lemmas/L3_LOC.md:28`): for every j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15:
  136|   |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀.
```

### [RM2] `Theory_work/Wave3/W3-RM2/STATEMENT.md` @ a2c465a4 — code pins of the local search; interface table; Form R
lines 60–68:
```
   60| **Code pins** (the facts about the method used here; commit `9700e17` of this branch; the three files were last
   61| changed at `0638af9`):
   62| * LS0's centre is the returned start mode, unmodified, and its move cap is ℓ_n + |centre| in the shipped
   63|   configuration: CORE `cpp/v3_core.cpp:465-476` (cap at `:473`, option parsing `:394-404`).
   64| * One LS0 scan scores every single flip (deletion of a member; addition of a non-member when |C| < K) and every swap
   65|   (one member out, one non-member in): CORE `cpp/v3_engine.h:394-406`. It moves to the best neighbour only on a strict
   66|   F improvement, ties broken lexicographically (`:392`, `:408`), and stops with `local_certified = true` when a
   67|   completed scan finds no strict improvement (`:413-414`), or with `local_limit = true` at the cap (`:409-410`).
   68| * Lemma E4 (W3-RM:E4@1.0.0) identifies the centre as a maximiser of γ₀ on Ω.
```
lines 96–104:
```
   96| ## 2. Interface properties (PROTOCOL item 5) — unchanged from RM
   97| 
   98| | id | property | consumed by |
   99| |---|---|---|
  100| | [POST] | E[1 − π(S₀)] → 0 | RM-0 |
  101| | [SAND(Q)] | P(Sand_n(Q)) → 1 | RM-0 |
  102| | [TL(Q)] | P(TL(𝓛)) → 1 | RM-0 |
  103| | [NA(Q)] | P(NA(𝓛)) → 1 | RM-0 |
  104| | [E4] | the emitted LS0 centre is a maximiser of γ₀ on Ω | RM-0 |
```
lines 172–218:
```
  172| ### 3.2 Gaussian rows (conditions on (Σ_n, θ*) and Q only)
  173| 
  174| * **(T1-R)**, **(FL-R)**, **(V-R)**: exactly as in RM `STATEMENT.md:129-136` ((FL-R): λ_min(Σ_{n,S}) ≥ c for
  175|   |S| ≤ 16 + s₀ and for S = Q ∪ {l}, l ∈ [p]; (V-R) = PTV(a₀)).
  176| * **(L-R^b) Polynomial leakage, localised** [CP2-P3, CP2-T6: v1.4]. A deterministic Q ⊇ S₀ with (L-size^b)
  177|   |Q| ≤ n^b and (L-feas), and deterministic sequences ϖ_n, r_n ≥ 0 (ϖ_n is the leak sequence — written ℓ_n in
  178|   v1.4 as first drafted; the symbol ℓ_n is reserved for the LS0 move cap of §1 [SC2-1]) with **ϖ_n√(n/log n) → 0** and **r_n → 0** (no rate),
  179|   such that
  180|   **(L-gain-R)** for every l ∉ Q, every U ⊆ [p] ∖ {l} with |U| ≤ 15 and every j ∈ S₀ ∖ U:
  181|   |Cov(W_l, W_j | W_U)| ≤ ϖ_n;
  182|   **(L-loc-R)** for every l ∉ Q there is a deterministic H_l ⊇ {l} ∪ S₀ with **|H_l| ≤ n^ρ** such that for every
  183|   U ⊆ [p] ∖ {l} with |U| ≤ 15, writing U₀ := U ∩ H_l: |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n
  184|   for every v ∈ U ∖ H_l and j ∈ S₀ ∖ U₀. Budget: 15ρ + b < ½.
  185|   In words: outside Q, the conditional covariance of a column with a truth, given any 15 other columns, is below
  186|   the noise scale √(log n/n) (the Gaussian-row counterpart of (L-gain) with η → 0); and every column outside Q has
  187|   a neighbourhood H_l, with at most n^ρ members, outside which columns are asymptotically conditionally
  188|   uncorrelated with it and with the truths. H_l only has to capture correlations that do not vanish, so ρ may be
  189|   taken as small as the design allows.
  190|   **Sufficient — a generalisation of the v1.3 localised form, (L-R^b-loc)** [SC2-4], which contains RM's (L-R): the leak bound only at the localised sets,
  191|   |Cov(W_l, W_j | W_{U₀})| ≤ ϖ′_n for j ∈ S₀ ∖ U₀ with ϖ′_n√(n/log n) → 0 (RM: ϖ′_n = C_L n^{−1/2}), together with the
  192|   rate r_n(n/log n)^{1/4} → 0 (RM: r_n(n log n)^{1/4} → 0); then (L-gain-R) holds with ϖ_n = ϖ′_n + 15r_n²/c
  193|   (`lemmas/L4_sandR_b.md` §7, item 1 [SC2-3]).
  194| * **(W-R) Lattice width on the realised design** [CP1-P2]. Let 𝒲⁰_n := {λ_min(R̂_{Q∪{l}}) ≥ c/2 for every
  195|   l ∈ [p]} (on it every u_{T,l}, (T, l) ∈ 𝔓, is defined, so 𝔴⁰_n and 𝔴_n(δ) are defined for the realised X)
  196|  . (W-R): there is a deterministic t_n → ∞ with P(𝒲⁰_n ∩ {𝔴⁰_n ≤ −t_n}) → 1.
  197|   Sufficient: P(𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ 0}) → 1 for some fixed δ₀ ∈ (0, 1) (the v1.2 form; then t_n = δ₀√(log n)/(2√(2A + 2))).
  198|   The latter holds **for every fixed δ₀ ∈ (0, 1 − 2b)** under **(D-R^b)**: hypotheses (N1), (R1)–(R3) of LOC2 Lemma NA-R (`Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:23-36`)
  199|   for (Σ_n, Q), with its deterministic latent-extension contract (`L2_NAR.md:15-20`), where (N0)'s size bound is
  200|   replaced by |Q| ≤ n^b, b < ½ (frames: log N_n ≤ log p + o(log n); atoms: L_n² log(|𝒜_n| + 1) = o(log n); variance
  201|   ratio η_n → 0). Sufficient for (D-R^b) — **(D-loc^b)**: RM's (D-loc) (`STATEMENT.md:154-156`) with
  202|   L_n² log(|Q| + 1) = o(log n) (so L_n → 0 at polynomial size).
  203| 
  204| ## 4. Claims
  205| 
  206| **(C1) Theorem RM2-F (fixed design, polynomial leakage).** Setting F, the method as coded, premises and
  207| configuration of §1. Assume (T1-F), (FL), (V), (L^b) with b < β(η, A), (BM-W) and (W). Then [SAND(Q)], [TL(Q)],
  208| [NA(Q)] and [POST] hold, hence all conclusions of RM-0: there is a data event 𝒢_n with P(𝒢_n) → 1 on which every
  209| admissible output run — every seed, N_e, R′ and calibration outcome — reports Ŝ⁺ = S₀; in particular
  210| P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). On Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛) LS0 makes exactly
  211| |S̃₀ ∖ S₀| ≤ |Q ∖ S₀| ≤ n^b moves, all deletions of extras, and its archive has `returned` = S₀, `local_certified` =
  212| true, `local_limit` = false (RM-0(a)); the shipped cap ℓ_n + |S̃₀| is never binding (the old cap `ell_n` is not
  213| covered beyond (W-χ)). The same holds with (V), (L-gain), (FL-16) replaced by the block-relative (V_b), (L_b), (FL_b)
  214| on the method's partition. No delivery claim (P(U_n) → 0 is not asserted).
  215| 
  216| **(C2) Theorem RM2-R (Gaussian rows, polynomial leakage).** Setting R, the method as coded, any X-measurable
  217| partition with blocks ≤ 16. Assume (T1-R), (FL-R), (V-R), (L-R^b) with 15ρ + b < ½, and (W-R). Then, under the joint
  218| law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], hence all conclusions of RM-0 as in (C1).
```

### [DLV4] `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md` @ a2c465a4 — the pathwise reporting step
lines 60–77:
```
   60| lemmas/LS_P6_repair.md:29-35; statuses verbatim in those reports: [status omitted]; for LH with exact Gram the W1-GEN instance row (C5)(a) records its
   61| input "W1-EXP Lemma 4.2 via Thm5-LH, SAME-FAMILY-ONLY", W1-GEN REPORT.md:64, and that instance-level status is
   62| carried here). These are statements about the
   63| data and the deterministic search; they do not involve calibration.
   64| *Claim.* 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ (for n large enough that S₀ is feasible, |S₀| ≤ K).
   65| *Proof.* On a delivered SMC fit, OP-LS0, e4 and the absence of interruption (delivery) imply that LS0 ran to completion
   66| from S̃₀ and every model it scored joined the all-scored set (SoP/02_method.tex:490-501); on the exact branch every
   67| feasible model is scored. So on 𝒪 ∩ 𝒦_n, S₀ is scored; if moreover π(S₀ | y) > ½ then F(S₀) > F(S) for every S ≠ S₀,
   68| and the reported HPM Ŝ⁺ — the ≻-maximum of the scored set — equals S₀. ∎
   69| Hence, under the original (unconditioned) data law and for either calibration law,
   70|   P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀ | y)] + P(𝒦_nᶜ) → 0,  and  P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − o(1) − P(𝒰_n)
   71|                                                                            = 1 − o(1) − P(𝒮ℒ_n)
   72| by Theorem D (P(𝒰_n) = P(𝒮ℒ_n) up to a null set). No bound is conditioned on delivery or on calibration success, and
   73| CAL is not used: both cited theorems list CAL among their premises, but only their data/deterministic-search clauses
   74| are used here — W1-PXN STATEMENT.md:52-53 states that (S), (E), (T), (P) concern the data and the deterministic LS0, and
   75| W1-GEN (C1), (C2) and T03♯ are data-level — while the CAL-bearing assembly step of those tickets is replaced by the
   76| pathwise Claim above. (The proof uses the premises EX-A, EX-S, SR, OP-LS0, e4 as the cited theorems do.)
   77| 
```

### [DLV2] `Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md` @ a2c465a4 — scorer never fails (Lemma S.2)
lines 20–35:
```
   20| ## S.2 Numerical failures (C1–C5) are impossible under EX-A
   21| The only source of `NumericalFailure` is `Scorer::score` (`cpp/v3_score.h:226-238`), thrown only if all three routes
   22| fail. Route 1 (`try_chol`, `cpp/v3_score.h:175-188`) on a model S with 1 ≤ k = |S| ≤ K forms H = (n+1)G_S + I_k and
   23| A = G_S + I_k with G_S = X_SᵀX_S ⪰ 0, so H, A ⪰ I_k are positive definite. In exact arithmetic the Cholesky recursion
   24| `chol_inplace` (`cpp/v3_score.h:76-90`) produces pivots d_j = (L_jj)² > 0 for a positive definite matrix (they are
   25| ratios of leading principal minors), so its failure test `!(d > 0) || !isfinite(d)` (:80) never fires. In
   26| `finish_from_factors` (:204-224) the log-determinants are finite, and
   27|   Q = yᵀy − n zᵀH⁻¹z ≥ yᵀy − (n/(n+1)) yᵀy = yᵀy/(n+1) > 0,
   28| because X_S((n+1)X_SᵀX_S + I)⁻¹X_Sᵀ ⪯ (n+1)⁻¹I (singular values σ²/((n+1)σ² + 1) ≤ 1/(n+1)) and yᵀy = n − 1 > 0 after
   29| standardisation (S.1). If the code recomputes Q by `q_nonneg` (when Q < 10⁻⁸yᵀy, possible only for n + 1 > 10⁸), the
   30| recomputed value equals Q exactly: with β = nH⁻¹z, ‖y − X_Sβ‖² + (‖X_Sβ‖² + ‖β‖²)/n = yᵀy − 2βᵀz + n⁻¹βᵀHβ =
   31| yᵀy − n zᵀH⁻¹z. Hence 2b₀ + Q > 0, log m(S) is finite (:222-223), `try_chol` returns true, and `score` returns at
   32| :233. For k = 0 the score is log m(∅) directly (:232). The k > K throw (:230) is an internal invariant: every caller
   33| passes models of size ≤ K (additions at |S| = K are excluded: Gibbs `o_j = 0`, local search `continue`,
   34| `cpp/v3_engine.h:390`; π₀ draws have size ≤ K; tables have B ≤ K for n ≥ 3, SoP/02_method.tex:193-194). So C1–C5
   35| are empty under EX-A. (No claim is made for floating point; VAL-FP is a separate engineering check.)
```

### [SAMP] `Theory_work/Wave3/W3-SAMP/STATEMENT.md` @ a2c465a4 — objects of the sampler (𝓜, Ŝ)
lines 36–62:
```
   36| final streams 10–13 are idealised as independent of the data as well as of streams 0–9.
   37| 
   38| **The method as coded.** Production core on main = 4676af6, `Scripts/SMC_BVS/core/`; code facts in
   39| `lemmas/CC_code_check.md` (CC1–CC7). Calibration record 𝓒, success event 𝒜 ∈ σ(𝓒) — in code terms 𝒜 = {SMC branch and `v3_calibrate` returns status
   40| "ok"} (`v3_calib.R:144-183`, "ok" includes the tier-1 fallback grid; `v3_fit.R:154` returns before any final run
   41| otherwise), so {completed} ⊆ 𝒜; on 𝒜 a frozen grid
   42| 0 = φ₀ < … < φ_T = 1, N_e ≥ 1, L ≥ 0 (σ(𝓒)-measurable), Hm = 4, R′ = 4 islands, island r on stream 9 + r.
   43| **Component vs production.** §2's Lemma ST and the finite-sample parts of Theorems D, LT♯, C and TR hold for **any**
   44| frozen parameters of the engine component `Engine::run_island(r, N_e, grid, L, 4, tier, nullptr)`
   45| (`cpp/v3_engine.h:269-273`): any valid grid 0 = φ₀ < … < φ_T = 1, integers N_e ≥ 1 and L ≥ 0, Hm = 4, `init_states =
   46| nullptr`, potential run. Through the public wrapper, an arbitrary valid grid reaches the engine unchanged
   47| (`v3_frozen`, `v3_run.R:68-82`; `cpp/v3_core.cpp:446`), but N_e and L are always the production budgets
   48| (`v3_run_settings`, `v3_run.R:88-92`), not `frozen$N`/`frozen$L`. In every claim, N_e and L denote the
   49| values actually executed. The ceiling T ≤ T_e and the deterministic draw-count lower bound hold only for **production
   50| calibration** (budgets `v3_preprocess.R:21-30`); claims that use them are labelled "production corollary".
   51| For island r on 𝒜 (potential, uninterrupted record):
   52| - Ẑ_r := exp(`log_Z_r`[r]) (the code stores log Ẑ_r: `cpp/v3_engine.h:299, 322, 365`); W_r := Ẑ_r/Z; reported evidence
   53|   `log_Z` = log Ẑ, Ẑ := ¼Σ_r Ẑ_r (`v3_run.R:150-154`).
   54| - Bridge fractions A^{br}_{r,t} (fraction of island r's particles at S₀ after the stage-t round, t = 1..T; t = 0: the
   55|   N_e initial draws). Terminal fractions A_{r,q}: after L + q rounds at φ = 1, q = 0..4.
   56| - RB PIP p̂_r(j) := (4N_e)⁻¹ Σ_{q=1}^{4} Σ_i o_j(Y^i_{q,j}), Y^i_{q,j} = particle i's state immediately before its Gibbs-j
   57|   step in measured round q; o_j(S) = γ₁(S∪j)/(γ₁(S∪j) + γ₁(S∖j)), and 0 if j ∉ S, |S| = K (CC3; T12 §2 item 3).
   58| - pip_primary := ¼Σ_r p̂_r; MPM := {j : pip_primary(j) > ½}; on completed runs these are the reported fields
   59|   (`v3_run.R:159-163`) and Ŝ is the reported HPM (CC2). 𝓜_r := models evaluated by island r; 𝓜 := all models offered to
   60|   the final-run ledger.
   61| 
   62| ## 1. Premises (ids for the registry) and dependency statuses
```

### [CC] `Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md` @ a2c465a4 — consumed code facts CC2, CC5
lines 40–63:
```
   40| ## CC2 — the reported HPM is the hpm_better-maximum of every model scored in the final run
   41| 
   42| - `eval` (`cpp/v3_engine.h:89-101`): cache miss ⇒ scorer call, `fresh = true`, cache insert; then, if `emit`,
   43|   `led->event(..., fresh || !cache, ...)` (`:98-100`).
   44| - `Ledger::event` (`cpp/v3_ledger.h:104-113`): if `is_fresh`, `offer_stores` (`:112`) ⇒ `offer_hpm` (`:89-90`), which
   45|   replaces the running best iff `hpm_better(F, S, hpmF, hpmS)` (`:84-88`). `hpm_better` (`cpp/v3_util.h:121-126`) is the
   46|   strict total order: larger F, then smaller size, then lexicographic. F = log ϖ(|S|-model prior) + log m(S)
   47|   (`cpp/v3_engine.h:97`), so e^F ∝ π(S) on Ω and Σ_Ω e^F = Z.
   48| - Non-fresh events are idempotent re-visits: (a) cache hits — the cache is created empty for the final run
   49|   (`cpp/v3_core.cpp:409`) and is owned by it, so a hit means an earlier `eval` of the same model in this run; every
   50|   `eval` with `emit = true` that inserted it also offered it. The only `emit = false` call in the final run is the centre
   51|   of the final local search, `E.local_search(led.hpmS, ...)` with `emit_centre = false` (`cpp/v3_core.cpp:456`;
   52|   `cpp/v3_engine.h:382`), whose centre is the current running best and was therefore already offered. A cache clear
   53|   (`cpp/v3_score.h:284`) only causes a later fresh re-evaluation, hence a repeated (idempotent) offer. (b) `held`
   54|   (`cpp/v3_engine.h:103-105`) re-emits the particle's current state, which entered the particle through an `eval`.
   55| - Other offers: block tables (`cpp/v3_core.cpp:372-386`, `:408`; only |U| ≤ K, `cpp/v3_start.h:92`), inherited
   56|   calibration models (`cpp/v3_core.cpp:418-429`, size checked at `:425`), the final local search and LS0
   57|   (`:456`, `:476`), which use the same `eval`.
   58| - Reporting: on `status == "completed"`, `out$hpm <- led$hpm$model` (`v3_run.R:142`); otherwise the HPM is labelled
   59|   incomplete and no estimates are returned (`v3_run.R:143-149`).
   60| - Hence, on a completed run: **Ŝ = the hpm_better-maximum of 𝓜**, where 𝓜 ⊇ {all models evaluated by the final
   61|   islands} (in particular every π₀ draw of CC1). Since hpm_better ranks by F first, if F(S₀) > F(S) for every S ∈ Ω∖{S₀}
   62|   and S₀ ∈ 𝓜, then Ŝ = S₀ (CC5 gives 𝓜 ⊆ Ω).
   63| 
```
lines 88–100:
```
   88| ## CC5 — every model the ledger sees lies in Ω
   89| 
   90| Particles start in Ω (π₀ on Ω); Gibbs adds only if |S| < K (`cpp/v3_engine.h:116`); swaps preserve size
   91| (`:146-180`); proposals are π₀ draws; local search skips additions at size K (`:397`); tables |U| ≤ K
   92| (`cpp/v3_start.h:92`); inherited models checked (`cpp/v3_core.cpp:425`). So 𝓜 ⊆ Ω.
   93| 
   94| ## CC6 — the frozen grid length is at most T_e (production calibration only)
   95| 
   96| T_e = 4^e·max(1000, ℓ²), ℓ = ⌈log₂(n+p+1)⌉ (`v3_preprocess.R:23, 27, 30`). A constructed grid with more than T_e
   97| intervals is a failure (`cpp/v3_calib.h:94`); in the pilot schedule every non-terminal step advances φ by at least 1/T_e and the
   98| terminal step ends exactly at 1 (`cpp/v3_calib.h:32, 38-44`; the snap is toward 1), so in exact arithmetic it has at most
   99| T_e stages; the tier-1 fallback grid is either a successful construction or the pilot schedule
  100| (`v3_calib.R:122-124`). Hence on 𝒜, **1 ≤ T ≤ 4·max(1000, ⌈log₂(n+p+1)⌉²)**.
```

### [POST] `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` @ a2c465a4 — consumed posterior rate (Lemma POST)
lines 1–33:
```
    1| # L1 — POST: the posterior-level hypotheses for random Gaussian designs
    2| 
    3| [review record omitted]
    4| [review record omitted]
    5| (marked [R02-#]).
    6| Falsification numerics: `numerics/post_check.py` → `numerics/post_check_out.txt`.
    7| 
    8| ## Setting
    9| STATEMENT §1: raw rows iid N(m, Σ_n), Σ_n unit-diagonal WLOG (population correlation matrix), p = p_n ≤ n^A
   10| (A ≥ 1 fixed, p ≫ n allowed, p ≥ max(2, s₀); p = 1 means s₀ = 1, Ω = {∅, {1}}, and only R and BM matter — omitted), X = centred, sample-standardised design, R̂ := XᵀX/(n − 1) (the sample
   11| correlation matrix), Y = Xθ* + Cε with fixed S₀, |S₀| = s₀, θ*_j ∈ [θ_lo, θ_hi] in absolute value on S₀, θ* = 0 off S₀,
   12| ε ~ N(0, σ²I) independent of the raw design. (Raw-scale convention, fixed raw slopes with |β_j| ∈ [b_lo, b_hi] and unit population variances [R02-3]: then
   13| θ* = D_xβ is raw-design-measurable; use the raw-design event 𝒢_n ∩ ℋ_n, ℋ_n := {all sample/population sd ratios in
   14| [½, 2]} (P(ℋ_n) → 1 by χ² tails and p ≤ n^A), take θ_lo = b_lo/2, θ_hi = 2b_hi, and run the diagonal argument over
   15| raw-design sequences; otherwise unchanged.) For the standardised-signal convention: conditionally on X, Y is
   16| Gaussian on the centred contrast space with mean Xθ* and noise variance σ², so the posterior's noise kernel depends
   17| only on X and the supremum over standardised designs below is legitimate [R02-4] (model G with β := D_x⁻¹θ*, which is
   18| raw-design-measurable, not X-measurable).
   19| 
   20| Write j₀ := ⌈(2A + 1)s₀⌉ + 1 and
   21|   m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n] / log(3/2)⌉,  k̄_n := min(p, s₀ + max(j₀, m̄_n)).
   22| 
   23| **Hypothesis LSF (logarithmic sparse floor).** (i) λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ min(p, s₀ + j₀),
   24| for a fixed φ ∈ (0, 1]; and (ii) λ_min(Σ_{n,S}) ≥ ψ_n for every S with |S| ≤ k̄_n, where
   25| ψ_n √n/(log n)^{3/2} → ∞. (If λ_min(Σ_n) ≥ c > 0 for all n, both hold with φ² = ψ_n = c.)
   26| 
   27| ## Lemma POST
   28| **(a)** Under LSF there are X-measurable events 𝒜_n with P(𝒜_n) → 1 on which every design satisfies the T03♯
   29| hypotheses R (with M := s₀²θ_hi² + 1 and φ₀² := φ²/2), SE_λ(j₀) (φ₀²), SE_w(m♯_n; g₀) (g₀ := 1), s₀ ≤ K, and BM-∞ with
   30| the deterministic envelope θ_lo² nφ₀²/(σ² log n) → ∞ — with these common constants and envelope, for n ≥ n₀.
   31| **(b)** Consequently, under the joint law of (raw design, ε): 1 − π(S₀) = O_P(√(log n/n)), and the conclusions of
   32| SL1 (a)–(e) hold with r_n = √(log n/n) (PIP sure screening and specificity uniformly in j, MPM, ξ_q for fixed q ∈ (0, 1) or
   33| deterministic q_n with r_n = o(min(q_n, 1 − q_n)) only, exact HPM, model size); without beta-min (θ*_j allowed to vary, some → 0) the inclusion clause for J_n(c) holds likewise.
```

### [DIST] `Theory_work/Wave3/W3-DIST/STATEMENT.md` @ a2c465a4 — context: the two links
lines 289–318:
```
  289| **Theorem DIST-C (coded output; under P⊗; jointly with output; conditional as labelled).** Let B_n be the bad set of
  290| (1.1) (or (1.2), with its rate) and ϱ_n := e^{−ct} (n₀ enlarged so that ϱ_n ≤ ¼ on the range of t).
  291| - (C-0) **Domination transfer (deterministic) [BT4].** If Q(S) ≤ L_n π(S) for all S ∈ Ω, then QΠ(B) ≤ L_n Π(B | D_n) for
  292|   every measurable B. Store BMA: L_n = 1/π(𝒯). A single model Ŝ: L_n = 1/π(Ŝ).
  293| - (C-i) **Store BMA.** For every λ ∈ [0, c): P⊗( {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) > e^{−(c−λ)t}} ) ≤
  294|   3e^{−ct} + P*(interfaces fail); on {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}} the store-BMA predictive density satisfies
  295|   d_H²(f̄^𝒯, f*) ≤ ε_n² + e^{−(c−λ)t}, where ε_n² = C²t/n for the bad set of (1.1) and ε_n² = C²tℓ_n/n for that of (1.2) [SW1-03]. Threshold form: for every a ∈ (0, 1], on the success event of DIST-1 every completed
  296|   run with π(𝒯) ≥ a has Π̂^𝒯(B_n) ≤ ϱ_n/a (pathwise; proved in `work/D_output/P6_DISTC.md` as (C-i°)) [stream D SCR-2].
  297| - (C-ii) **When does the store hold enough mass?** (α) With selection: on {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½}, S₀ ∈ 𝒯
  298|   and π(𝒯) > ½ (S₀ is then the unique maximiser of F and the top store keeps the best-scored offered model:
  299|   `cpp/v3_ledger.h:49-56`; direct, no further premise). P⊗({completed} ∩ {S₀ ∉ 𝓜}) → 0 is supplied by [SAMP] Theorem D
  300|   (D-i) with P-OVL (discovery by a π₀ draw; P-MAP is needed for identification, not for discovery), or by
  301|   W3-RM2:RM2-F/RM2-R — a **conditional alternative that no proof here uses** (two links unchecked: whether RM2's output
  302|   event covers {completed}, and whether its reported model is `hpm`) [P3 D-01]. (β) Without beta-min:
  303|   π(𝒯) ≥ e^{−λt} is a **premise (P-STORE)** about the run; the output does not certify it in general ([SAMP] LT-f).
  304|   (γ) Description, not a claim: π(𝒯) = Σ_{S∈𝒯}π(S), and (C-0), (C-i) need no model of posterior probability above ½. The store law
  305|   Π̂^𝒯 is in general **a mixture over many models** — typically S₀ and many supersets S₀ ∪ {j} — and (C-i) applies to it as
  306|   it is (measured by the Engineering Department at n = 200, p = 10⁴–10⁵: the one-extra-variable supersets together weigh
  307|   0.5–1.2 times S₀; `Docs/Experiments/P1M/DECISIONS.md` row D-17).
  308| - (C-iii) **HPM plug-in.** 𝔅_n := {S : Π(B_n | S, D_n) > ϱ_n^{1/2}} has π(𝔅_n) ≤ ϱ_n^{1/2} on the success event of DIST-1.
  309|   If the final-run ledger contains a model S′ with π(S′) > ϱ_n^{1/2} (**premise P-HIT**; implied by S₀ ∈ 𝓜 and δ_n < ½),
  310|   then Ŝ ∉ 𝔅_n and Π̂^H(B_n) ≤ ϱ_n^{1/2}. With selection ((α)), Ŝ = S₀ and Π̂^H = Π(· | S₀, D_n); **under the hypotheses of
  311|   DIST-3 ((E), (L₀), (TR₀))** it satisfies DIST-3's second display (exponential oracle bound at √(u/n)).
  312| - (C-iv) **MPM plug-in.** On {MPM = S₀} (P⊗-probability statements: [SAMP] LT-e, C-v, TR-d, under their premises),
  313|   Π̂^M = Π(· | S₀, D_n); **under the hypotheses of DIST-3** the same oracle bound holds.
  314| - **Honest label.** (C-0) and the deterministic parts of (C-i)–(C-iii) need no sampler premise. Everything that says
  315|   the store or the ledger contains enough is conditional on a delivery premise (discovery of S₀, P-STORE, P-HIT) and
  316|   is intersected with {completed}; P⊗(completed) → 1 is neither assumed nor claimed. Bad output events are contained in
  317|   bad data events, so the data-only bounds extend to P⊗ without an independence assumption. EX-A for floating point.
  318|   No statement is made about a particle approximation, because none is returned.
```

### [READER] `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` @ a2c465a4 — reader Theorem 6 and its bridges
lines 660–712:
```
  660| **Card row** 3.1 · **Section version** 0.9 (2026-11-16) · **Pending delta** — (RM2-R rider merged, v0.8)
  661| 
  662| 
  663| ### Reader statement
  664| **Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
  665| correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
  666| $b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
  667| - **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
  668| - **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  669|   $S_0$.
  670| - **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  671|   $U\not\ni j$ with $|U|\le15$.
  672| - **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  673|   $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  674|   (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  675|   $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  676|   (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  677|   $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  678|   and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  679|   $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$.
  680| - **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  681|   $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
  682| - **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  683|   $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$, such that
  684|   $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  685|   where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).
  686| 
  687| Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
  688| which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
  689| internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions
  690| (S4) hold,
  691| $$
  692| P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
  693| $$
  694| The delivery statement lifts two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be reached on any input R can represent ($n, p_{\mathrm{raw}} \le 2^{31}-1$) [T14-REP], so this matters only for the $n\to\infty$ form. The two limits are a base search cap of $10^6$ (`v3_run.R:96`) and a 32-bit integer bound $2^{31}-1$ on the search cap (`cpp/v3_core.cpp:474`). R stores matrix dimensions as 32-bit integers, so in the default configuration the base cap is $\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le32$ and the search cap is at most $32+\lfloor n/2\rfloor\le2^{30}+31$, and neither limit can fire [T14-REP]. Every such input lies in the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, on which delivery holds under the remaining conventions (S4), without IDEAL-W⁺; IDEAL-W⁺ is used only by the asymptotic form. Representable inputs still carry the other obligations of IDEAL-W (for example `2*p-1` in `int` for $p\ge2^{30}$); the statement is for the default configuration (`v3.ls0_ell` unset).
  695| The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]
  696| 
  697| *Remarks.* (o) Under (S4), for every seed and calibration outcome,
  698| $P(\hat S\neq S_0)\le P(S_0\text{ is not the unique maximiser of the score})+P(\text{the local search from the start mode
  699| does not reach }S_0)$. *(Interpretation, not part of the theorem: the two terms are the posterior-mode error and the
  700| search error.)* (i) $\mathcal G_n$ can be chosen ($\mathcal M_n\cap\mathrm{Sand}_n(Q)\cap\mathrm{NA}\cap\mathrm{TL}$) so that on it the local search from the start mode only deletes the spurious members of the start
  701| mode, one per move, at most $n^b$ moves, and certifies $S_0$; its move cap never binds. (ii) The polylogarithmic case
  702| $|Q|\le(\log n)^{\kappa}$ is a special case (the earlier version of the theorem). (iii) Examples (never hypotheses):
  703| metric-local correlation, polynomial correlation decay of exponent $\alpha>2$ (`W3-RM2:Ex-PolyR@1.0.3` [status omitted]
  704| ),
  705| one-factor blocks.
  706| 
  707| ### Why each assumption
  708| - (A2) Fixed signals give the posterior input (Theorem 2) and the truth-removal margin.
  709| - (A3) No truth can be explained away by at most 15 others: every truth enters the start mode. Needed in this form for
  710|   the start; masked designs violate it and are separate examples (the method still works there, by other theorems).
  711| - (A4) Columns outside $Q$ never enter the start mode; columns inside $Q$ may, and the search removes them. $b<\tfrac12$
  712|   is where the prior-plus-Occam penalty of one more variable ($\approx\log p+\tfrac12\log n$) stops dominating the best
```
lines 752–760:
```
  752| 
  753| 
  754| 
  755| 
  756| [review record omitted]
  757| [status omitted], conditional on W2-APP:POST; …[status omitted][status omitted]", main 6cd699dd) [S4-F1, REG-6cd6]. |
  758| | B6.6 | RM2-R conclusions ⇒ F-UNI premises (S), (P), (V); F-UNI's operational premises carried as (S4) | **NEW** (assembly; (V)/(S)/(P) part passed S1) | (S): $P(\mathrm{Sand}\cap\mathrm{NA}\cap\mathrm{TL})\ge1-\sum P(\cdot^c)\to1$ from [SAND(Q)], [NA(Q)], [TL(Q)]; (P) = [POST]; (V) = "(R) with $\lambda_{\min}(\Sigma_n)>0$". LS0 cap and default-on tier-1 fallback match (`v3_calib.R:141-144`). F-UNI's method/premise/allocation paragraph (`L5_delivery.md:7-12`: EX-A as cost model, IDEAL-W, EX-S, SR, e4/TDP-IMPL, GUARD-W, MACH, CONFIG, valid seed, allocation and preflight inequalities at $(n,p_{\mathrm{raw}})$; P1/S.3 [status omitted]) is **not derived**: it is carried as (S4). Premise-by-premise table: proof leg (`lemmas/R3_delivery_assembly.md`). **Historical** (former hypotheses only; superseded by B6.6′). |
  759| | B6.6′ | (S4) ⇔ delivery premises (D) of RM2-R-plus; RM2-R-plus's conclusions are the reader conclusions | identity | (S4)(i)–(iv) state in words `W3-RM2-R/STATEMENT.md:71-93` (IDEAL-W⁺, EX-A, MACH, CONFIG at the shipped configuration, TDP-IMPL, allocation 𝒜_n, valid non-degenerate input). No assembly with F-UNI is needed; B6.6 is kept for the record and superseded by B6.6′ for the shipped method. Needs one line check with the bridges leg. |
  760| | B6.7 | standardised-signal convention | limit | The masters take $\theta^*$ deterministic (Setting R). A raw-scale version (fixed $\beta^*$) would need a **NEW** bridge (medium; the population conditions involve $\theta^*$). Not proposed for CP1. |
```

### [C:run] `Scripts/SMC_BVS/core/v3_run.R` @ a2c465a4 — code
lines 84–163:
```
   84| # Fixed production settings. The frozen tier is selected by calibration, before final randomness.
   85| # ls0 (v3.1 #8, default on): append LS0 after the final local search. ls0 = FALSE reproduces v3 (no LS0 fields in the
   86| # settings, the run or the fit). LS0 uses the production ell and the e4 tie DP of the start mode; the options
   87| # v3.ls0_tie_dp = FALSE (v3 start-mode rule) and v3.ls0_ell (move cap override) exist for testing only.
   88| v3_run_settings <- function(setup, frozen, ls0 = getOption("v3.ls0", TRUE)) {
   89|   b <- setup$budgets; tier <- frozen[["tier"]] %||% 0L
   90|   ro <- list(N = as.integer(b$tiers$N[tier + 1]), L = as.integer(b$L), measured_rounds = 4L,
   91|        islands = 4L, tier = as.integer(tier), ell = as.integer(b$ell),
   92|        cache_capacity = as.numeric(500 * setup$ctx$p))
   93|   if (isTRUE(ls0)) {
   94|     ro$ls0 <- TRUE
   95|     le <- getOption("v3.ls0_ell", b$ell)   # testing override of the LS0 base cap (R05 #2: validated)
   96|     if (!is.numeric(le) || length(le) != 1 || !is.finite(le) || le < 0 || le != round(le) || le > 1e6)
   97|       stop("option v3.ls0_ell must be a whole number in [0, 1e6]")
   98|     ro$ls0_ell <- as.integer(le)
   99|     ro$ls0_tie_dp <- isTRUE(getOption("v3.ls0_tie_dp", TRUE))
  100|     # C-GROW MR1 (adopted by HQ): LS0 move cap ell_n + |S~0| (default "ell_n_plus_mode"); "ell_n" = cap ell_n
  101|     ro$ls0_cap <- if (identical(getOption("v3.ls0_cap", "ell_n_plus_mode"), "ell_n")) "ell_n" else "ell_n_plus_mode"
  102|   }
  103|   ro
  104| }
  105| 
  106| # GUARD-W / v3.1 #15: on every return without complete output, every estimate field is NA by exact name, so no
  107| # consumer can read a partial value (e.g. fit$log_Z partially matching log_Zbar0). Partial island values stay only in
  108| # their labelled archives (partial_final, stage_record, calibration). Used in v3.1 mode (ls0 on) only.
  109| V3_ESTIMATE_FIELDS <- c("log_Z", "log_Z_r", "log_Z_lower95", "log_Z_rel_m0", "log_Z_r_rel_m0", "pip_primary", "pip_r", "mpm")
  110| v3_unavailable_estimates <- function(fit) {
  111|   for (nm in V3_ESTIMATE_FIELDS) fit[nm] <- list(NA)
  112|   fit$estimates_available <- FALSE
  113|   fit
  114| }
  115| 
  116| v3_model_key <- function(S) paste(S, collapse = ",")
  117| 
  118| # Assemble the reported outputs of a final run (CORE_SPEC §6, §7; M §§6.9-6.12).
  119| v3_assemble_final <- function(raw, setup, frozen, ro, seed) {
  120|   isl <- raw$islands
  121|   out <- list(status = raw$status, message = raw$message, seed = seed, settings = ro,
  122|               frozen_sha256 = frozen[["sha256"]], grid = frozen[["grid"]], B = setup$B)
  123|   out <- c(out, v3_randomness(seed))
  124|   out$stream_map$tier[out$stream_map$stream >= 10L] <- ro$tier
  125|   out$stage_record <- isl
  126|   out$streams <- lapply(Filter(Negate(is.null), isl), function(x) x$stream)
  127|   out$stage_table <- v3_stage_table(isl, frozen$rho_V, frozen$grid_label %||% NA_character_)
  128|   if (length(raw$local_search)) {
  129|     out$local_search <- raw$local_search
  130|     out$local_search$phase <- "final"; out$local_search$tier <- ro$tier
  131|     out$local_search$iter <- -1L; out$local_search$island <- "final"
  132|   }
  133|   v31 <- isTRUE(ro$ls0)
  134|   if (v31) {
  135|     out$start_mode <- raw$start_mode; out$hpm_before_ls0 <- raw$hpm_before_ls0
  136|     if (length(raw$ls0)) {
  137|       out$ls0 <- raw$ls0
  138|       out$ls0$phase <- "ls0"; out$ls0$tier <- ro$tier; out$ls0$iter <- -1L; out$ls0$island <- "final"; out$ls0$ell <- ro$ls0_ell
  139|     }
  140|   }
  141|   led <- raw$ledger
  142|   out$hpm <- led$hpm$model; out$hpm_F <- led$hpm$F; out$hpm_provenance <- led$hpm$provenance
  143|   if (raw$status != "completed") {   # numerical_failure: best scored model so far, labelled incomplete (M §2)
  144|     out$ledger <- led; out$hpm_incomplete <- TRUE; out$estimates_available <- FALSE
  145|     out$partial_results <- TRUE; out$partial_final <- raw
  146|     out$local_certified <- FALSE; out$global_certified <- FALSE
  147|     if (v31) out <- v3_unavailable_estimates(out)
  148|     return(out)
  149|   }
  150|   logZr <- vapply(isl, function(r) r$log_Z, 0)
  151|   R <- length(isl)
  152|   out$stage_record <- isl
  153|   out$log_Z_r <- logZr
  154|   out$log_Z <- v3_log_sum_exp(logZr) - log(R)                    # pooled Zhat = (1/R) sum_r Zhat_r (log-sum-exp)
  155|   out$log_Z_lower95 <- log(0.05) + out$log_Z                     # Markov bound 0.05 Zhat (one-sided)
  156|   out$log_Z_rel_m0 <- out$log_Z - raw$log_m0                     # relative to m(empty)
  157|   out$log_Z_r_rel_m0 <- logZr - raw$log_m0
  158|   out$log_increment <- lapply(isl, function(r) r$log_increment)  # per island, per stage (reconstructs W_t, PW2)
  159|   P <- do.call(cbind, lapply(isl, function(r) r$pip))
  160|   orig <- setup$ctx$orig
  161|   out$pip_r <- P; rownames(out$pip_r) <- orig
  162|   out$pip_primary <- setNames(rowMeans(P), orig)                 # equal-weight mean over islands (M §6.11)
  163|   out$mpm <- as.integer(orig[out$pip_primary > 0.5])
```
lines 205–229:
```
  205|                     checks_passed_calibration = NA)
  206|   if (v31) out$flags <- c(out$flags, list(final_local_limit = out$final_local_limit, ls0_local_limit = out$ls0_local_limit,
  207|                                           ls0_improved = out$ls0_improved, ls0_hpm_changed = out$ls0_hpm_changed))
  208|   out$island_best <- led$island_best
  209|   out$hpm_before_local <- hb
  210|   out$leaders_gamma0 <- led$leaders_gamma0; out$leaders_gamma1 <- led$leaders_gamma1; out$top_store <- led$top
  211|   out$score_counts <- list(logical = led$logical, fresh = led$fresh)   # mechanisms incl. gibbs_held / gibbs_flip (R15)
  212|   out$cache <- raw$cache
  213|   out$rb <- lapply(isl, function(r) list(rb_acc = r$rb_acc, rb_round = r$rb_round))
  214|   out$timings <- list(islands = do.call(rbind, lapply(isl, function(r) r$seconds)), local = raw$seconds_local,
  215|                       final_total = raw$seconds_total)
  216|   if (v31) out$timings$ls0 <- raw$seconds_ls0
  217|   out$log_m0 <- raw$log_m0; out$log_Zbar0 <- raw$log_Zbar0
  218|   out$estimates_available <- TRUE
  219|   out
  220| }
  221| 
  222| # Fresh production final run. The runtime pointer shares the complete-fit clock with calibration.
  223| v3_final_run <- function(setup, frozen, seed, runtime = NULL, ls0 = getOption("v3.ls0", TRUE)) {
  224|   stopifnot(inherits(setup, "v3_setup"), inherits(frozen, "v3_frozen"))
  225|   v3_check_grid(frozen[["grid"]]); v3_check_seed(seed)
  226|   ro <- v3_run_settings(setup, frozen, ls0)
  227|   raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime)
  228|   v3_assemble_final(raw, setup, frozen, ro, seed)
  229| }
```

### [C:fit] `Scripts/SMC_BVS/core/v3_fit.R` @ a2c465a4 — code
lines 73–174:
```
   73| v3_fit <- function(X, y, seed, allocation = list(mem_gb = 8, hours = 24), ls0 = getOption("v3.ls0", TRUE)) {
   74|   t_start <- proc.time()[["elapsed"]]
   75|   runtime <- ctx <- NULL
   76|   fit <- list(seed = seed, allocation = allocation, local_certified = FALSE, global_certified = FALSE,
   77|               cut_group = NA, cut_group_count = NA_integer_, cut_group_components = list(),
   78|               partial_results = FALSE, estimates_available = FALSE)
   79|   finish <- function(fit) {
   80|     fit$peak_memory_kb <- v3_peak_memory_kb()
   81|     fit$timings$total <- proc.time()[["elapsed"]] - t_start
   82|     if (!is.null(runtime)) fit$runtime_guard <- .v3cpp$cpp_runtime_report(runtime)
   83|     if (!is.null(ctx)) fit$numerical_routes <- .v3cpp$cpp_numerical_routes(ctx)
   84|     if (identical(fit$status, "resource_limit")) fit$partial_results <- TRUE
   85|     if (isTRUE(ls0) && !isTRUE(fit$estimates_available)) fit <- v3_unavailable_estimates(fit)
   86|     fit
   87|   }
   88|   valid_seed <- tryCatch({ if (length(seed) != 1) stop("seed must be a single integer"); v3_check_seed(seed); TRUE }, error = function(e) conditionMessage(e))
   89|   if (!isTRUE(valid_seed)) { fit$status <- "invalid_input"; fit$message <- valid_seed; return(finish(fit)) }
   90|   fit <- c(fit, v3_randomness(seed))
   91|   if (!is.list(allocation)) stop("allocation must be a list containing mem_gb and hours")
   92|   allocation <- list(mem_gb = allocation[["mem_gb"]] %||% 8, hours = allocation[["hours"]] %||% 24)
   93|   for (nm in names(allocation)) if (!is.numeric(allocation[[nm]]) || length(allocation[[nm]]) != 1 ||
   94|     !is.finite(allocation[[nm]]) || allocation[[nm]] <= 0) stop("allocation$", nm, " must be finite and positive")
   95|   fit$allocation <- allocation
   96|   runtime <- .v3cpp$cpp_runtime_new(allocation$hours, proc.time()[["elapsed"]] - t_start)
   97|   pre <- v3_preprocess(X, y, dup_components = FALSE)
   98|   fit$preprocessing <- pre[setdiff(names(pre), c("X", "y"))]
   99|   if (pre$status != "ok") {
  100|     fit$status <- pre$status
  101|     if (pre$status %in% c("no_predictors", "y_constant")) fit$hpm <- integer(0)
  102|     return(finish(fit))
  103|   }
  104|   n <- pre$n; p <- pre$p; fit$n <- n; fit$p <- p
  105|   b <- v3_budgets(n, p); fit$budgets <- b; fit$B <- b$B
  106|   fit$branch_decision <- fit$branch_run <- if (b$exact_branch) "exact" else "smc"
  107|   tcache <- list()
  108|   time_fun <- function(k) {
  109|     key <- as.character(k)
  110|     if (is.null(tcache[[key]])) tcache[[key]] <<- v3_time_scores(pre$X, pre$y, k)
  111|     tcache[[key]]
  112|   }
  113|   # v3.1: charge LS0's worst case under the C-GROW cap; options(v3.ls0_cap = "ell_n") or ls0 = FALSE: shipped preflight
  114|   ls0_wc <- isTRUE(ls0) && !identical(getOption("v3.ls0_cap", "ell_n_plus_mode"), "ell_n")
  115|   pf <- v3_preflight(n, p, b, fit$branch_run, allocation, time_fun = time_fun, ls0_worst_case = ls0_wc)
  116|   fit$preflight <- pf
  117|   if (pf$exceeds) { fit$status <- "resource_limit"; return(finish(fit)) }
  118|   ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  119|   fit$preprocessing$dup_components <- .v3cpp$cpp_dup_components(ctx)
  120|   if (fit$branch_run == "exact") {
  121|     t0 <- proc.time()[["elapsed"]]; e <- v3_enumerate(ctx)
  122|     fit$timings$exact <- proc.time()[["elapsed"]] - t0; fit$exact <- e; fit$status <- e$status
  123|     fit$hpm <- e$hpm; fit$hpm_F <- e$hpm_F; fit$hpm_provenance <- list(phase = "exact", mechanism = "enumeration")
  124|     fit$near_ties <- e$near_ties; fit$near_tie_F <- e$near_tie_F; fit$near_tie_truncated <- e$near_tie_truncated
  125|     if (e$status == "exact") {
  126|       fit$log_Z <- e$log_Z; fit$log_Z_rel_m0 <- e$log_Z_rel_m0; fit$log_Z_lower95 <- log(0.05) + e$log_Z
  127|       fit$pip_primary <- e$pip; fit$mpm <- e$mpm
  128|       fit$global_certified <- e$global_certified; fit$local_certified <- e$local_certified
  129|       fit$estimates_available <- TRUE
  130|     } else { fit$message <- e$message; fit$hpm_incomplete <- TRUE }
  131|     return(finish(fit))
  132|   }
  133|   t0 <- proc.time()[["elapsed"]]; setup <- v3_setup(ctx)
  134|   if (inherits(setup, "v3_setup_failed")) {
  135|     fit$status <- "numerical_failure"; fit$message <- setup$message
  136|     fit$hpm <- setup$hpm; fit$hpm_F <- setup$hpm_F; fit$hpm_provenance <- setup$hpm_provenance
  137|     fit$hpm_incomplete <- TRUE; return(finish(fit))
  138|   }
  139|   fit$timings$setup <- setup$seconds; fit$timings$setup_total <- proc.time()[["elapsed"]] - t0
  140|   fit$blocks <- setup$blocks; fit$neighbours <- setup$neighbours; fit$log_Zbar0 <- setup$start$log_Zbar0
  141|   cg <- .v3cpp$cpp_cut_group(setup$ptr)
  142|   fit$cut_group <- cg$cut_group; fit$cut_group_count <- cg$count; fit$cut_group_components <- cg$components
  143|   fit$cut_group_graph <- cg[c("threshold", "graph")]
  144|   pf_fun <- function(e) {
  145|     pf <- v3_preflight(n, p, b, "smc", allocation, tier = e, time_fun = time_fun, ls0_worst_case = ls0_wc)
  146|     fit$preflight_escalation <<- pf
  147|     pf$exceeds
  148|   }
  149|   t0 <- proc.time()[["elapsed"]]
  150|   cal <- v3_calibrate(setup, seed, preflight = pf_fun, runtime = runtime,
  151|                       grid_fallback = isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE)))
  152|   fit$timings$calibration <- proc.time()[["elapsed"]] - t0; fit$calibration <- cal
  153|   fit$stage_table <- cal$stage_table
  154|   if (cal$status != "ok") {
  155|     fit$status <- cal$status; fit$flags <- cal$flags
  156|     fit$hpm <- cal$hpm$model; fit$hpm_F <- cal$hpm$F; fit$hpm_provenance <- cal$hpm$provenance
  157|     fit$hpm_incomplete <- TRUE
  158|     if (cal$status == "numerical_failure") fit$message <- cal$tiers[[length(cal$tiers)]]$message
  159|     return(finish(fit))
  160|   }
  161|   frozen <- cal$frozen; fit$frozen <- frozen
  162|   t0 <- proc.time()[["elapsed"]]; fr <- v3_final_run(setup, frozen, seed, runtime, ls0 = ls0)
  163|   fr$stage_table <- v3_bind_records(list(cal$stage_table, fr$stage_table))
  164|   fit$timings$final <- proc.time()[["elapsed"]] - t0; fit$timings$final_detail <- fr$timings; fr$timings <- NULL
  165|   cf <- cal$flags
  166|   fr$flags$escalated <- cf$escalated; fr$flags$checks_passed_calibration <- cf$checks_passed_calibration
  167|   fr$flags$forced_pilot_steps <- cf$forced_pilot_steps; fr$flags$grid_unconverged <- cf$grid_unconverged
  168|   fr$flags$calibration_triggers <- cf$triggers_fired
  169|   # C-DLV B: present only when the fallback fired ("last_successful_construction" or "pilot_schedule"; R05 #1)
  170|   if (!is.null(cf$grid_fallback)) fr$flags$grid_fallback <- cf$grid_fallback
  171|   for (nm in names(fr)) fit[[nm]] <- fr[[nm]]
  172|   fit$flags$cut_group <- fit$cut_group
  173|   finish(fit)
  174| }
```

### [C:exact] `Scripts/SMC_BVS/core/v3_exact.R` @ a2c465a4 — code
lines 1–20:
```
    1| # v3_exact.R -- exact branch and exact references (CORE_SPEC v2 §7 `v3_enumerate`, §8 "Exact references"; M §6.2; R9).
    2| 
    3| # v3_enumerate(ctx): streaming pass over every |S| <= K: log Z (log-sum-exp, long-double accumulators), PIPs, HPM
    4| # (strict order of M §6.10), near ties (top-(40p+1) store), status `exact`. R9: `global_certified` iff
    5| # F(HPM) - eta(HPM) > max_{S != HPM} [F(S) + eta(S)], eta = the scorer's documented error bound (v3_score.h).
    6| v3_enumerate <- function(ctx) {
    7|   r <- .v3cpp$cpp_enumerate(ctx)
    8|   orig <- ctx$orig
    9|   names(r$pip) <- orig
   10|   near <- which(r$top$value >= r$hpm_F - 1e-9)
   11|   r$near_ties <- r$top$models[near]; r$near_tie_F <- r$top$value[near]
   12|   r$near_tie_truncated <- isTRUE(r$top$full) && min(r$top$value) >= r$hpm_F - 1e-9
   13|   r$mpm <- as.integer(orig[r$pip > 0.5])
   14|   r$log_Z_rel_m0 <- r$log_Z - ctx$log_m0
   15|   r$local_certified <- r$status == "exact"   # the HPM is the exact maximiser, so no neighbour improves it
   16|   r$R9 <- list(margin = r$margin, hpm_error_bound = r$hpm_error_bound, hpm_error_bound_kind = r$hpm_error_bound_kind, certificate_bound = r$certificate_bound,
   17|                rule = "certified iff F(HPM) - eta(HPM) > max over other S of F(S) + eta(S)")
   18|   r
   19| }
   20| 
```

### [C:pre] `Scripts/SMC_BVS/core/v3_preprocess.R` @ a2c465a4 — code
lines 97–120:
```
   97| v3_preprocess <- function(X, y, dup_components = TRUE) {
   98|   bad <- function(reason) list(status = "invalid_input", reason = reason)
   99|   if (!is.matrix(X) || !is.numeric(X) || !typeof(X) %in% c("integer", "double"))
  100|     return(bad("X is not a numeric matrix"))
  101|   if (!is.numeric(y) || !is.null(dim(y)) || !typeof(y) %in% c("integer", "double"))
  102|     return(bad("y is not a numeric vector"))
  103|   n <- nrow(X); p_raw <- ncol(X)
  104|   if (length(y) != n) return(bad("length(y) != nrow(X)"))
  105|   if (any(!is.finite(X)) || any(!is.finite(y))) return(bad("non-finite entry in X or y"))
  106|   if (n < 3) return(bad("n < 3"))
  107|   if (p_raw < 1) return(bad("p < 1"))
  108|   # Representation conversion of already validated real numeric inputs only.
  109|   storage.mode(X) <- "double"
  110|   storage.mode(y) <- "double"
  111|   constant <- apply(X, 2, function(x) all(x == x[1]))   # dropped only if all entries are exactly equal
  112|   kept <- which(!constant); dropped <- which(constant)
  113|   base <- list(n = n, p_raw = p_raw, p = length(kept), kept = kept, dropped = dropped)
  114|   if (!length(kept)) return(c(list(status = "no_predictors", hpm = integer(0)), base))
  115|   if (all(y == y[1])) return(c(list(status = "y_constant", hpm = integer(0)), base))
  116|   Xs <- matrix(0, n, length(kept)); cm <- cmu <- csd <- numeric(length(kept))
  117|   centers <- vector("list", length(kept))
  118|   for (a in seq_along(kept)) {
  119|     s <- v3_standardise(X[, kept[a]])
  120|     Xs[, a] <- s$z; cm[a] <- s$max; cmu[a] <- s$mean; csd[a] <- s$sd
```

### [C:ledger] `Scripts/SMC_BVS/core/cpp/v3_ledger.h` @ a2c465a4 — code
lines 1–115:
```
    1| // v3_ledger.h -- operational HPM, stores, aggregate score counts and island maxima.
    2| // Part I ??I.5-I.6. No per-event score archive or profiling observer.
    3| #pragma once
    4| #include "v3_start.h"
    5| 
    6| namespace v3 {
    7| 
    8| // PH_TEST: events of the step/round testing samplers (v3_step_sample, v3_round_sample; code review S-2).
    9| // PH_LS0 (v3.1 #8): the local search from the start mode after the final local search; provenance "ls0". Appended last
   10| // so every other phase keeps its index; ledgers serialise its counter row only when LS0 is enabled (v3_core.cpp).
   11| enum Phase { PH_TABLE = 0, PH_PILOT, PH_DIAG, PH_FINAL_INIT, PH_FINAL_BRIDGE, PH_BURN_IN, PH_MEASURED, PH_LOCAL, PH_INHERITED, PH_TEST, PH_LS0, N_PHASE };
   12| // Gibbs events are split (lead ruling R15): gibbs_held = the current state counted as scored under SR (not
   13| // re-evaluated); gibbs_flip = the other feasible configuration S u j or S \ j (scored).
   14| enum Mech { ME_TABLE = 0, ME_INIT, ME_GIBBS_HELD, ME_GIBBS_FLIP, ME_USWAP, ME_NSWAP, ME_INDEP, ME_LOCAL, ME_INHERITED, N_MECH };
   15| inline const char* phase_name(int ph) {
   16|   static const char* nm[] = {"table", "pilot", "diag", "final_init", "final_bridge", "burn_in", "measured", "local", "inherited", "test", "ls0"};
   17|   return nm[ph];
   18| }
   19| inline const char* mech_name(int me) {
   20|   static const char* nm[] = {"table", "init_draw", "gibbs_held", "gibbs_flip", "uswap", "nswap", "indep", "local_scan", "inherited"};
   21|   return nm[me];
   22| }
   23| 
   24| // Where a score event happened. island: 1..R for final islands, 0 for tables / final local search.
   25| // stage: bridge stage t (0 for initial draws; T for terminal rounds); round: index within the phase
   26| // (bridge: t; burn-in 1..L; measured 1..4; local: move number); particle 1-based; position 1-based in the round order
   27| // (local: index within the scan); phi: temperature of the step.
   28| // iter: calibration rebuild iteration (0 = pilot and its local search; k = diagnostic islands and local search of
   29| // rebuild iteration k); -1 = tables, final run, testing interfaces.
   30| struct EventCtx { int phase = 0, tier = 0, island = 0, stage = 0, round = 0, particle = 0, position = 0, iter = -1; double phi = 0; };
   31| 
   32| // Top-k store of distinct models by a value, with a strict total tie order (so the std::set also finds a model by
   33| // (value, S): a model's value is a deterministic function of the model).
   34| struct TopEntry { double v; std::vector<int> S; };
   35| struct TopCmp {
   36|   bool hpm_order;  // true: exact ties -> smaller size, then lexicographic (HPM rule); false: lexicographic only (R3)
   37|   bool operator()(const TopEntry& a, const TopEntry& b) const {
   38|     if (a.v != b.v) return a.v > b.v;
   39|     if (hpm_order && a.S.size() != b.S.size()) return a.S.size() < b.S.size();
   40|     return lex_less(a.S, b.S);
   41|   }
   42| };
   43| struct TopStore {
   44|   size_t cap = 0;
   45|   TopCmp cmp{true};
   46|   std::set<TopEntry, TopCmp> s{TopCmp{true}};
   47|   void init(size_t c, bool hpm_order) { cap = c; cmp = TopCmp{hpm_order}; s = std::set<TopEntry, TopCmp>(cmp); }
   48|   // returns true if inserted
   49|   bool offer(double v, const std::vector<int>& S) {
   50|     if (cap == 0) return false;
   51|     TopEntry e{v, S};
   52|     if (s.size() >= cap && !cmp(e, *s.rbegin())) return false;  // quick reject: not better than the worst
   53|     if (s.count(e)) return false;
   54|     s.insert(e);
   55|     if (s.size() > cap) s.erase(std::prev(s.end()));
   56|     return true;
   57|   }
   58|   bool would_enter(double v, const std::vector<int>& S) const {
   59|     if (cap == 0) return false;
   60|     if (s.size() < cap) return true;
   61|     TopEntry e{v, S};
   62|     return cmp(e, *s.rbegin());
   63|   }
   64| };
   65| 
   66| class Ledger {
   67|  public:
   68|   const Data* D;
   69|   int islands = 4;
   70|   bool has_hpm = false;
   71|   std::vector<int> hpmS; double hpmF = NEG_INF, hpm_logm = 0; EventCtx hpm_ev; int hpm_mech = 0;
   72|   TopStore top, lead0, lead1;  // top-(40p+1) by F (HPM order); top 20p by log gamma_0; top 20p by log gamma_1 (R3)
   73|   uint64_t logical[N_PHASE][N_MECH] = {}, fresh[N_PHASE][N_MECH] = {};
   74|   std::vector<double> island_best;  // R5: max F over models scored by the island's own particles and proposals
   75| 
   76|   explicit Ledger(const Data* d, int R) : D(d), islands(R) {
   77|     size_t p = d->p;
   78|     top.init(40 * p + 1, true); lead0.init(20 * p, false); lead1.init(20 * p, false);
   79|     island_best.assign(R + 1, NEG_INF);
   80|   }
   81| 
   82|   // HPM running best (M §6.10): strict order hpm_better; provenance = the event at which it became the best
   83|   // (that event is necessarily the model's first score: a model that loses once can never win later).
   84|   void offer_hpm(const std::vector<int>& S, double F, double logm, const EventCtx& ev, int mech) {
   85|     if (!has_hpm || hpm_better(F, S, hpmF, hpmS)) {
   86|       has_hpm = true; hpmS = S; hpmF = F; hpm_logm = logm; hpm_ev = ev; hpm_mech = mech;
   87|     }
   88|   }
   89|   void offer_stores(const std::vector<int>& S, double F, double lg0, double logm, const EventCtx& ev, int mech) {
   90|     offer_hpm(S, F, logm, ev, mech);
   91|     top.offer(F, S);
   92|     lead0.offer(lg0, S);
   93|     lead1.offer(F, S);  // log gamma_1 = log varpi + log m (R3); ordering identical to F
   94|   }
   95| 
   96|   // One logical score event. `fresh` = freshly evaluated (cache miss or uncached source). Stores are idempotent, so
   97|   // they are updated only on fresh evaluations: a cache hit or a held current state was processed when first scored.
   98|   // (The cache is owned by the run, so every cached model was processed by this ledger.)
   99|   inline void event(const std::vector<int>& S, double F, double lg0, double logm, bool is_fresh, bool is_held,
  100|                     const EventCtx& ev, int mech);
  101| };
  102| 
  103| // Aggregate bookkeeping, with no watch sets or per-event archive.
  104| inline void Ledger::event(const std::vector<int>& S, double F, double lg0, double logm, bool is_fresh, bool is_held,
  105|                           const EventCtx& ev, int mech) {
  106|   logical[ev.phase][mech]++;
  107|   if (is_fresh) fresh[ev.phase][mech]++;
  108|   bool own = ev.island >= 1 && ev.island <= islands &&
  109|              (ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED ||
  110|               ev.phase == PH_PILOT || ev.phase == PH_DIAG);
  111|   if (own && F > island_best[ev.island]) island_best[ev.island] = F;
  112|   if (is_fresh) offer_stores(S, F, lg0, logm, ev, mech);
  113| }
  114| 
  115| }  // namespace v3
```

### [C:engine] `Scripts/SMC_BVS/core/cpp/v3_engine.h` @ a2c465a4 — code
lines 86–110:
```
   86| 
   87|   // Score a model (cache, then the scorer) and fill log m, log gamma_0, d, F. Emits one logical score event.
   88|   // d(S) = log BF(S) - sum_b log r_b(S n C_b) (M §6.3); F = log varpi(|S|) + log m(S).
   89|   void eval(Particle& q, int mech, bool emit = true) {
   90|     double lm; bool fresh = false;
   91|     if (!(cache && cache->find(q.S, q.h, lm))) {
   92|       ScoreOut o = sc.score(q.S); lm = o.logm; fresh = true;
   93|       if (cache) cache->insert(q.S, q.h, lm);
   94|     }
   95|     double c = st.comp(q.S, scratch);
   96|     int k = (int)q.S.size();
   97|     q.logm = lm; q.lg0 = D.logprior[k] + c; q.d = (lm - D.logm0) - c; q.F = D.logprior[k] + lm;
   98|     if (emit) {
   99|       if (led) led->event(q.S, q.F, q.lg0, q.logm, fresh || !cache, false, ev, mech);
  100|     }
  101|   }
  102|   // The current state counted as scored without re-evaluation (SR: both Gibbs configurations count as scored).
  103|   void held(const Particle& q, int mech) {
  104|     if (led) led->event(q.S, q.F, q.lg0, q.logm, false, true, ev, mech);
  105|   }
  106| 
  107|   // Exact pi_0 draw
  108|   void draw_start(std::vector<int>& S) { draw_pi0(st, *vs, S); }
  109| 
  110|   // ---- Elementary steps (M §6.5, R1, CORE_SPEC §4.1) ----
```
lines 269–300:
```
  269|   IslandResult run_island(int r, int N, const std::vector<double>& grid, int L, int Hm, int tier,
  270|                           const std::vector<std::vector<int>>* init_states) {
  271|     Schedule sch; sch.grid = &grid;
  272|     return run_island_s(r, N, sch, L, Hm, tier, init_states, -1, -1);
  273|   }
  274|   IslandResult run_island_s(int r, int N, const Schedule& sch, int L, int Hm, int tier,
  275|                             const std::vector<std::vector<int>>* init_states, int phase_override, int iter) {
  276|     IslandResult res;
  277|     res.phase = phase_override >= 0 ? phase_override : PH_FINAL_BRIDGE;
  278|     res.tier = tier; res.iter = iter; res.island = r;
  279|     int p = D.p;
  280|     int T = sch.adaptive ? 0 : (int)sch.grid->size() - 1;
  281|     auto PH = [&](int ph) { return phase_override >= 0 ? phase_override : ph; };
  282|     ev = EventCtx(); ev.island = r; ev.tier = tier; ev.iter = iter;
  283|     std::vector<Particle> P(N);
  284|     auto t0 = Clock::now();
  285|     ev.phase = PH(PH_FINAL_INIT); ev.stage = 0; ev.round = 0; ev.phi = 0;
  286|     for (int i = 0; i < N; ++i) {
  287|       ev.particle = i + 1; ev.position = 0;
  288|       std::vector<int> S;
  289|       if (init_states) S = (*init_states)[i]; else draw_start(S);
  290|       set_model(P[i], S);
  291|       eval(P[i], ME_INIT);
  292|     }
  293|     ev.particle = 0;
  294|     // hash of the initial population: h <- SplitMix64(h xor Zobrist(S_i) xor i), i = 1..N (instrumentation only)
  295|     { uint64_t hh = 0x243F6A8885A308D3ULL;
  296|       for (int i = 0; i < N; ++i) { uint64_t x = hh ^ P[i].h ^ (uint64_t)(i + 1); hh = splitmix64(x); }
  297|       res.init_hash = hh; }
  298|     res.seconds_init = secs_since(t0); t0 = Clock::now();
  299|     double logZ = D.logm0 + st.logZbar0;
  300|     std::vector<double> lw(N), dvec(N);
```
lines 375–422:
```
  375|   // best through the ledger (HPM tie rule), so an exact-tie neighbour can become the HPM without being a move.
  376|   // Scan order: flips j = 1..p, then swaps (j in S ascending) x (l outside S ascending).
  377|   // The search never alters particles. Every evaluated model is a score event (phase local, mechanism local_scan;
  378|   // phase ls0 for LS0, v3.1 #8: the same rules from the start mode, centre emitted).
  379|   LocalArchive local_search(const std::vector<int>& centre, int ell, int tier, bool emit_centre, int iter = -1, int phase = PH_LOCAL) {
  380|     LocalArchive A;
  381|     ev = EventCtx(); ev.phase = phase; ev.tier = tier; ev.island = 0; ev.phi = 1.0; ev.iter = iter;
  382|     Particle C; set_model(C, centre); eval(C, ME_LOCAL, emit_centre);
  383|     A.centre = C.S; A.centre_F = C.F;
  384|     int p = D.p, K = D.K;
  385|     while (true) {
  386|       ev.round = A.moves; ev.stage = (int)A.scanned.size() + 1;
  387|       bool have = false; Particle best, Q;
  388|       int pos = 0;
  389|       auto consider = [&](Particle& q) {
  390|         ev.position = ++pos;
  391|         eval(q, ME_LOCAL); A.n_eval++;
  392|         if (!have || q.F > best.F || (q.F == best.F && lex_less(q.S, best.S))) { best = q; have = true; }
  393|       };
  394|       for (int j = 0; j < p; ++j) {
  395|         Q = C;
  396|         if (bit_get(C.bits, j)) del_var(Q, j);
  397|         else { if ((int)C.S.size() >= K) continue; add_var(Q, j); }
  398|         consider(Q);
  399|       }
  400|       std::vector<int> CS = C.S;
  401|       for (int j : CS)
  402|         for (int l = 0; l < p; ++l) {
  403|           if (bit_get(C.bits, l)) continue;
  404|           Q = C; del_var(Q, j); add_var(Q, l);
  405|           consider(Q);
  406|         }
  407|       A.scanned.push_back(C.S); A.scanned_F.push_back(C.F); A.scan_complete.push_back(1); A.scan_size.push_back(pos);
  408|       if (have && best.F > C.F) {  // strict F improvement only (R14)
  409|         if (A.moves >= ell) {
  410|           A.local_limit = true; A.termination = "move_limit"; A.returned = best.S; A.returned_F = best.F; break;
  411|         }
  412|         C = best; A.moves++; A.path.push_back(C.S); A.path_F.push_back(C.F);
  413|       } else {
  414|         A.termination = "no_improvement"; A.local_certified = true; A.returned = C.S; A.returned_F = C.F; break;
  415|       }
  416|     }
  417|     ev = EventCtx();
  418|     return A;
  419|   }
  420| };
  421| 
  422| }  // namespace v3
```

### [C:core] `Scripts/SMC_BVS/core/cpp/v3_core.cpp` @ a2c465a4 — code
lines 25–46:
```
   25|   std::vector<int> out;
   26|   if (Rf_isNull(Sx)) return out;
   27|   IntegerVector S(Sx);
   28|   for (int v : S) {
   29|     if (v == NA_INTEGER) stop("model contains NA");
   30|     auto it = std::lower_bound(D.orig.begin(), D.orig.end(), v);
   31|     if (it == D.orig.end() || *it != v) stop("index %d is not a retained original column index", v);
   32|     out.push_back((int)(it - D.orig.begin()));
   33|   }
   34|   std::sort(out.begin(), out.end());
   35|   if (std::adjacent_find(out.begin(), out.end()) != out.end()) stop("model has duplicated indices");
   36|   return out;
   37| }
   38| static IntegerVector to_orig(const Data& D, const std::vector<int>& S) {
   39|   IntegerVector o(S.size());
   40|   for (size_t i = 0; i < S.size(); ++i) o[i] = D.orig[S[i]];
   41|   return o;
   42| }
   43| static List models_to_list(const Data& D, const std::vector<std::vector<int>>& Ms) {
   44|   List L(Ms.size());
   45|   for (size_t i = 0; i < Ms.size(); ++i) L[i] = to_orig(D, Ms[i]);
   46|   return L;
```
lines 318–330:
```
  318| }
  319| 
  320| static std::vector<std::vector<int>> models_from_R(const Data& D, SEXP x) {
  321|   std::vector<std::vector<int>> out;
  322|   if (Rf_isNull(x)) return out;
  323|   List l(x);
  324|   for (int i = 0; i < l.size(); ++i) out.push_back(to_internal(D, l[i]));
  325|   return out;
  326| }
  327| static List island_to_list(const IslandResult& r, const Data& D) {
  328|   auto msdf = [](const std::vector<MoveStats>& v) {
  329|     int n = (int)v.size();
  330|     NumericVector g(n), gf(n), ue(n), ua(n), us(n), ne(n), na(n), nn(n), ns(n), ie(n), ia(n);
```
lines 356–389:
```
  356|                       _["n_evaluated"] = (double)A.n_eval);
  357| }
  358| static List store_to_list(const TopStore& s, const Data& D) {
  359|   List M(s.s.size()); NumericVector v(s.s.size()); int i = 0;
  360|   for (auto& e : s.s) { M[i] = to_orig(D, e.S); v[i] = e.v; ++i; }
  361|   return List::create(_["models"] = M, _["value"] = v, _["capacity"] = (double)s.cap, _["full"] = s.s.size() >= s.cap);
  362| }
  363| static List ledger_to_list(const Ledger& L, const Data& D, bool include_ls0 = false) {
  364|   List hpm = L.has_hpm ? List::create(_["model"] = to_orig(D, L.hpmS), _["F"] = L.hpmF, _["log_m"] = L.hpm_logm,
  365|                                       _["provenance"] = event_to_list(L.hpm_ev, L.hpm_mech)) : List();
  366|   List out = List::create(_["hpm"] = hpm, _["top"] = store_to_list(L.top, D), _["leaders_gamma0"] = store_to_list(L.lead0, D),
  367|                           _["leaders_gamma1"] = store_to_list(L.lead1, D),
  368|                           _["island_best"] = NumericVector(L.island_best.begin() + 1, L.island_best.end()),
  369|                           _["logical"] = counter_matrix(L.logical, include_ls0), _["fresh"] = counter_matrix(L.fresh, include_ls0));
  370|   return out;
  371| }
  372| static void ingest_tables(Ledger& led, const Holder& h) {
  373|   const Data& D = *h.D; const Start& st = *h.st;
  374|   EventCtx ev; ev.phase = PH_TABLE; ev.island = 0;
  375|   std::vector<int> U; std::vector<uint64_t> bits(D.W);
  376|   for (int b = 0; b < st.J; ++b) {
  377|     int m = (int)st.blocks[b].size();
  378|     for (uint32_t c = 0; c < (1u << m); ++c) {
  379|       if (std::isnan(st.logm_tab[b][c])) continue;
  380|       U.clear(); std::fill(bits.begin(), bits.end(), 0); uint64_t hh = 0;
  381|       for (int i = 0; i < m; ++i) if (c & (1u << i)) { int j = st.blocks[b][i]; U.push_back(j); bit_set(bits, j); hh ^= D.zob.key[j]; }
  382|       double lm = st.logm_tab[b][c], F = D.logprior[U.size()] + lm, lg0 = D.logprior[U.size()] + st.logr[b][c];
  383|       ev.stage = b + 1; ev.position = (int)c;
  384|       led.event(U, F, lg0, lm, true, false, ev, ME_TABLE);
  385|     }
  386|   }
  387| }
  388| 
  389| // The final run on a frozen grid. Returns raw results; R assembles the reported outputs.
```
lines 391–568:
```
  391| List cpp_final_run(SEXP setup, NumericVector grid, List ro, double seed, SEXP inherited, SEXP runtime) {
  392|   HPtr h = get_holder(setup); const Data& D = *h->D; const Start& st = *h->st;
  393|   if (!h->has_graph) stop("setup required");
  394|   struct RunOpts { int N, L, Hm, islands, tier, ell; double cache_capacity; bool ls0, ls0_tie_dp, ls0_cap_plus_mode; int ls0_ell; };
  395|   RunOpts o;
  396|   o.N = as<int>(ro["N"]); o.L = as<int>(ro["L"]); o.Hm = as<int>(ro["measured_rounds"]); o.islands = as<int>(ro["islands"]);
  397|   o.tier = as<int>(ro["tier"]); o.ell = as<int>(ro["ell"]);
  398|   o.cache_capacity = as<double>(ro["cache_capacity"]);
  399|   // v3.1 LS0 (METHOD_v3.1_FINAL #8). Absent fields = v3 behaviour (no LS0): the switch lives in v3_run_settings.
  400|   o.ls0 = ro.containsElementNamed("ls0") && as<bool>(ro["ls0"]);
  401|   o.ls0_tie_dp = !ro.containsElementNamed("ls0_tie_dp") || as<bool>(ro["ls0_tie_dp"]);
  402|   o.ls0_ell = ro.containsElementNamed("ls0_ell") ? as<int>(ro["ls0_ell"]) : o.ell;
  403|   // C-GROW MR1: LS0 move cap = ell_n + |S~0| (default); ls0_cap = "ell_n" keeps ell_n. The final local search keeps ell_n.
  404|   o.ls0_cap_plus_mode = !ro.containsElementNamed("ls0_cap") || as<std::string>(ro["ls0_cap"]) != "ell_n";
  405|   std::vector<double> g(grid.begin(), grid.end());
  406|   auto t_all = Clock::now();
  407|   Ledger led(&D, o.islands);
  408|   ingest_tables(led, *h);
  409|   ScoreCache cache; cache.init(D.W, (size_t)o.cache_capacity);
  410|   Engine E(D, st, h->Nb, h->B);
  411|   E.cache = &cache; E.led = &led; E.guard = runtime_ptr(runtime);
  412|   List islands(o.islands);
  413|   std::string status = "completed", message;
  414|   List local, hpm_before, ls0, hpm_before_ls0, smode;
  415|   double sec_local = 0, sec_ls0 = 0;
  416|   std::vector<IslandResult> res;
  417|   try {
  418|     // inherited state (frozen calibration): offered to the stores and the HPM with provenance "inherited"
  419|     if (!Rf_isNull(inherited)) {
  420|       List inh(inherited);
  421|       if (inh.containsElementNamed("models")) {
  422|         auto Ms = models_from_R(D, inh["models"]);
  423|         Scorer sc(&D); EventCtx ev; ev.phase = PH_INHERITED;
  424|         for (auto& S : Ms) {
  425|           if ((int)S.size() > D.K) stop("inherited model larger than K");
  426|           double lm = sc.score(S).logm; double c = st.comp(S);
  427|           led.offer_stores(S, D.logprior[S.size()] + lm, D.logprior[S.size()] + c, lm, ev, ME_INHERITED);
  428|         }
  429|       }
  430|       // provenance of the inherited HPM (first score in the calibration) replaces the label "inherited"
  431|       if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
  432|         List hp = inh["hpm"];
  433|         if (led.hpm_ev.phase == PH_INHERITED && hp.containsElementNamed("provenance") &&
  434|             to_internal(D, hp["model"]) == led.hpmS) {
  435|           List pv = hp["provenance"];
  436|           EventCtx e; e.phase = phase_index(as<std::string>(pv["phase"])); e.tier = as<int>(pv["tier"]); e.island = as<int>(pv["island"]);
  437|           e.stage = as<int>(pv["stage"]); e.round = as<int>(pv["round"]); e.particle = as<int>(pv["particle"]);
  438|           e.position = as<int>(pv["position"]); e.phi = as<double>(pv["phi"]); e.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
  439|           led.hpm_ev = e; led.hpm_mech = mech_index(as<std::string>(pv["mechanism"]));
  440|         }
  441|       }
  442|     }
  443|     for (int r = 1; r <= o.islands; ++r) {
  444|       RngSource rng; rng.g.seed_stream((uint64_t)seed, (uint64_t)(9 + r));  // final islands: streams 10..13 (M §6.1)
  445|       E.vs = &rng;
  446|       res.push_back(E.run_island(r, o.N, g, o.L, o.Hm, o.tier, nullptr));
  447|       List island = island_to_list(res.back(), D);
  448|       island["stream"] = List::create(_["stream"] = 9 + r, _["position_start"] = 0.0,
  449|         _["position_end"] = (double)rng.g.count, _["init_draws_hash"] = hex64(res.back().init_hash));
  450|       islands[r - 1] = island;
  451|       if (res.back().partial) { status = "resource_limit"; break; }
  452|     }
  453|     if (status == "completed") {
  454|     hpm_before = List::create(_["model"] = to_orig(D, led.hpmS), _["F"] = led.hpmF);
  455|     auto t0 = Clock::now();
  456|     LocalArchive A = E.local_search(led.hpmS, o.ell, o.tier, false);  // final local search from the global best (R4)
  457|     sec_local = secs_since(t0);
  458|     local = local_to_list(A, D);
  459|     if (E.guard && E.guard->check(sec_local, "local_search", local_event(o.tier, -1))) status = "resource_limit";
  460|     // LS0 (v3.1 #8): after the final local search, one local search with the same rules (ell, tier) from the start
  461|     // mode S~0 = argmax pi_0 (exact block DP; e4 tie DP on truncation), centre emitted, on the same ledger and cache,
  462|     // so every model it scores joins the all-scored set and the stores. Reads no uniforms. Not started on a stopped
  463|     // run. GUARD-W (#6): an LS0 stop (guard below, or a NumericalFailure inside it) leaves status != completed, i.e.
  464|     // no output; a completed LS0 that ends on its move cap is not a stop.
  465|     if (o.ls0 && status == "completed") {
  466|       hpm_before_ls0 = List::create(_["model"] = to_orig(D, led.hpmS), _["F"] = led.hpmF,
  467|                                     _["provenance"] = event_to_list(led.hpm_ev, led.hpm_mech));
  468|       auto t1 = Clock::now();
  469|       ModeResult m = start_mode(st, 1000000, o.ls0_tie_dp);
  470|       smode = List::create(_["model"] = to_orig(D, m.S), _["log_gamma0"] = m.lg0, _["log_pi0"] = m.lg0 - st.logZbar0,
  471|                            _["ties"] = (double)m.ties, _["truncated"] = m.truncated, _["tie_dp_used"] = m.tie_dp_used,
  472|                            _["tie_rule"] = o.ls0_tie_dp ? "enumeration (cap 1e6), e4 tie-aware DP on truncation" : "enumeration (cap 1e6), v3 rule");
  473|       long long cap_ll = (long long)o.ls0_ell + (o.ls0_cap_plus_mode ? (long long)m.S.size() : 0LL);  // checked (R05 #2)
  474|       if (o.ls0_ell < 0 || cap_ll > (long long)std::numeric_limits<int>::max()) stop("LS0 move cap out of range");
  475|       int ls0_cap = (int)cap_ll;
  476|       LocalArchive A0 = E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0);
  477|       sec_ls0 = secs_since(t1);
  478|       ls0 = local_to_list(A0, D);
  479|       ls0["move_cap"] = ls0_cap; ls0["move_cap_rule"] = o.ls0_cap_plus_mode ? "ell_n + |start mode|" : "ell_n";
  480|       if (E.guard && E.guard->check(sec_ls0, "ls0", local_event(o.tier, -1, PH_LS0))) status = "resource_limit";
  481|     }
  482|     }
  483|   } catch (NumericalFailure& e) {
  484|     status = "numerical_failure"; message = e.what();
  485|     // Calibration already scored its saved HPM, even if inheritance stopped before
  486|     // reaching it. Reconcile that known score without another scorer call. This is
  487|     // failure-only so successful rescoring, stores and random draws stay unchanged.
  488|     if (!Rf_isNull(inherited)) {
  489|       List inh(inherited);
  490|       if (inh.containsElementNamed("hpm") && !Rf_isNull(inh["hpm"])) {
  491|         List hp = inh["hpm"];
  492|         if (hp.containsElementNamed("model") && hp.containsElementNamed("F") && hp.containsElementNamed("provenance")) {
  493|           std::vector<int> S = to_internal(D, hp["model"]);
  494|           double F = as<double>(hp["F"]);
  495|           bool better = !led.has_hpm || hpm_better(F, S, led.hpmF, led.hpmS);
  496|           bool restore = led.has_hpm && led.hpm_ev.phase == PH_INHERITED && S == led.hpmS && F == led.hpmF;
  497|           if (better || restore) {
  498|             List pv = hp["provenance"];
  499|             EventCtx ev; ev.phase = phase_index(as<std::string>(pv["phase"])); ev.tier = as<int>(pv["tier"]); ev.island = as<int>(pv["island"]);
  500|             ev.stage = as<int>(pv["stage"]); ev.round = as<int>(pv["round"]); ev.particle = as<int>(pv["particle"]);
  501|             ev.position = as<int>(pv["position"]); ev.phi = as<double>(pv["phi"]); ev.iter = pv.containsElementNamed("iter") ? as<int>(pv["iter"]) : -1;
  502|             if (better) led.offer_hpm(S, F, F - D.logprior[S.size()], ev, mech_index(as<std::string>(pv["mechanism"])));
  503|             else { led.hpm_ev = ev; led.hpm_mech = mech_index(as<std::string>(pv["mechanism"])); }
  504|           }
  505|         }
  506|       }
  507|     }
  508|   }
  509|   List out = List::create(_["status"] = status, _["message"] = message, _["islands"] = islands, _["local_search"] = local,
  510|                           _["hpm_before_local"] = hpm_before, _["ledger"] = ledger_to_list(led, D, o.ls0),
  511|                           _["cache"] = NumericVector::create(_["capacity"] = (double)cache.capacity, _["hits"] = (double)cache.hits,
  512|                                                              _["misses"] = (double)cache.misses, _["inserts"] = (double)cache.inserts,
  513|                                                              _["clears"] = (double)cache.clears, _["entries_at_end"] = (double)cache.count),
  514|                           _["seconds_local"] = sec_local, _["seconds_total"] = secs_since(t_all),
  515|                           _["log_m0"] = D.logm0, _["log_Zbar0"] = st.logZbar0);
  516|   if (o.ls0) { out["ls0"] = ls0; out["hpm_before_ls0"] = hpm_before_ls0; out["start_mode"] = smode; out["seconds_ls0"] = sec_ls0; }
  517|   return out;
  518| }
  519| 
  520| // ---------------------------------------------------------------------------------------------
  521| // Exact branch (CORE_SPEC §7 `v3_enumerate`; M §6.2; R9)
  522| // ---------------------------------------------------------------------------------------------
  523| // [[Rcpp::export]]
  524| List cpp_enumerate(SEXP ctx) {
  525|   HPtr h = get_holder(ctx); const Data& D = *h->D;
  526|   int p = D.p, K = D.K;
  527|   Scorer sc(&D);
  528|   // streaming log-sum-exp with long double accumulators (rescaled when the running maximum increases)
  529|   double mx = NEG_INF; long double total = 0; std::vector<long double> numer(p, 0.0L);
  530|   std::vector<int> hpmS; double hpmF = NEG_INF, hpm_eta = 0; bool has = false;
  531|   TopStore top; top.init(40 * (size_t)p + 1, true);
  532|   // R9: two largest values of F(S) + eta(S) with their models
  533|   double up1 = NEG_INF, up2 = NEG_INF; std::vector<int> upS1, upS2;
  534|   double count = 0;
  535|   std::vector<int> S;
  536|   std::string status = "exact", message;
  537|   std::function<void(int)> rec = [&](int start) {
  538|     ScoreOut o = sc.score(S);
  539|     double F = D.logprior[S.size()] + o.logm;
  540|     double eta = sc.error_bound(o, (int)S.size());
  541|     count += 1;
  542|     if (F > mx) {
  543|       long double scale = (mx == NEG_INF) ? 0.0L : std::exp((long double)(mx - F));
  544|       total *= scale; for (auto& v : numer) v *= scale; mx = F;
  545|     }
  546|     long double w = std::exp((long double)(F - mx));
  547|     total += w; for (int j : S) numer[j] += w;
  548|     if (!has || hpm_better(F, S, hpmF, hpmS)) { has = true; hpmS = S; hpmF = F; hpm_eta = eta; }
  549|     top.offer(F, S);
  550|     double up = F + eta;
  551|     if (up > up1) { up2 = up1; upS2 = upS1; up1 = up; upS1 = S; } else if (up > up2) { up2 = up; upS2 = S; }
  552|     if (((long)count & 65535) == 0) Rcpp::checkUserInterrupt();
  553|     if ((int)S.size() >= K) return;
  554|     for (int j = start; j < p; ++j) { S.push_back(j); rec(j + 1); S.pop_back(); }
  555|   };
  556|   try { rec(0); } catch (NumericalFailure& e) { status = "numerical_failure"; message = e.what(); }
  557|   double logZ = mx + (double)std::log(total);
  558|   NumericVector pip(p);
  559|   for (int j = 0; j < p; ++j) pip[j] = (double)(numer[j] / total);
  560|   double runner_up = (upS1 == hpmS) ? up2 : up1;
  561|   double second_F = NA_REAL;
  562|   if (top.s.size() >= 2) second_F = std::next(top.s.begin())->v;
  563|   bool certified = (status == "exact") && (hpmF - hpm_eta > runner_up);
  564|   return List::create(_["status"] = status, _["message"] = message, _["log_Z"] = logZ, _["pip"] = pip,
  565|                       _["hpm"] = to_orig(D, hpmS), _["hpm_F"] = hpmF, _["models_scored"] = count, _["top"] = store_to_list(top, D),
  566|                       _["second_F"] = second_F, _["margin"] = hpmF - second_F, _["hpm_error_bound"] = hpm_eta, _["hpm_error_bound_kind"] = "heuristic (not a validated interval bound)",
  567|                       _["certificate_bound"] = hpmF - runner_up, _["global_certified"] = certified);
  568| }
```

### [C:score] `Scripts/SMC_BVS/core/cpp/v3_score.h` @ a2c465a4 — code
lines 36–72:
```
   36| };
   37| 
   38| // Build the Data object: G, z, constants. M §5: C_n, w(k), W_K; log w(k) via lgamma; log W_K by log-sum-exp.
   39| inline void data_init(Data& D, const double* X, const double* y, int n, int p, const std::vector<int>& orig) {
   40|   D.n = n; D.p = p; D.K = std::min(p, n / 2); D.W = nwords(p);
   41|   D.X.assign(X, X + (size_t)n * p);
   42|   D.y.assign(y, y + n);
   43|   D.orig = orig;
   44|   D.G.assign((size_t)p * p, 0.0);
   45|   for (int a = 0; a < p; ++a) {
   46|     const double* xa = D.col(a);
   47|     for (int b = a; b < p; ++b) {
   48|       const double* xb = D.col(b);
   49|       double s = 0;
   50|       for (int i = 0; i < n; ++i) s += xa[i] * xb[i];
   51|       D.G[(size_t)b * p + a] = s; D.G[(size_t)a * p + b] = s;
   52|     }
   53|   }
   54|   D.z.assign(p, 0.0);
   55|   for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * D.y[i]; D.z[a] = s; }
   56|   D.yty = 0; for (int i = 0; i < n; ++i) D.yty += D.y[i] * D.y[i];
   57|   D.nu = D.a0 + n / 2.0;
   58|   // log C_n = a0 log(2 b0) + lgamma(a0 + n/2) - (n/2) log(pi) - lgamma(a0)
   59|   D.logCn = D.a0 * std::log(2 * D.b0) + std::lgamma(D.a0 + n / 2.0) - (n / 2.0) * std::log(M_PI) - std::lgamma(D.a0);
   60|   D.logm0 = D.logCn - D.nu * std::log(2 * D.b0 + D.yty);
   61|   D.logw.assign(D.K + 1, 0.0);
   62|   std::vector<double> terms(D.K + 1);
   63|   for (int k = 0; k <= D.K; ++k) {
   64|     // log w(k) = log(1/2) - log C(2p-1, k)   (lgamma form; replaces the beta-function ratio)
   65|     D.logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k);
   66|     terms[k] = lchoose_d((double)p, k) + D.logw[k];
   67|   }
   68|   D.logWK = log_sum_exp(terms);
   69|   D.logprior.assign(D.K + 1, 0.0);
   70|   for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
   71|   D.zob.init(p);
   72| }
```
lines 255–297:
```
  255| class ScoreCache {
  256|  public:
  257|   size_t capacity = 0, nslots = 0, mask = 0, count = 0;
  258|   uint64_t clears = 0, hits = 0, misses = 0, inserts = 0;
  259|   std::vector<uint64_t> hashes, off;
  260|   std::vector<uint32_t> len;
  261|   std::vector<double> logm;
  262|   std::vector<uint8_t> used;
  263|   std::vector<int> pool;
  264|   void init(int /*W (unused)*/, size_t cap) {
  265|     capacity = std::max<size_t>(cap, 1);
  266|     nslots = 16; while (nslots < 2 * capacity) nslots <<= 1;
  267|     mask = nslots - 1;
  268|     hashes.assign(nslots, 0); off.assign(nslots, 0); len.assign(nslots, 0); logm.assign(nslots, 0.0); used.assign(nslots, 0);
  269|     pool.clear(); count = 0;
  270|   }
  271|   inline bool same(size_t s, const std::vector<int>& S) const {
  272|     return len[s] == S.size() && std::equal(S.begin(), S.end(), pool.begin() + off[s]);
  273|   }
  274|   bool find(const std::vector<int>& S, uint64_t h, double& lm) {
  275|     size_t s = h & mask;
  276|     while (used[s]) {
  277|       if (hashes[s] == h && same(s, S)) { lm = logm[s]; ++hits; return true; }
  278|       s = (s + 1) & mask;
  279|     }
  280|     ++misses;
  281|     return false;
  282|   }
  283|   void insert(const std::vector<int>& S, uint64_t h, double lm) {
  284|     if (count >= capacity) { std::fill(used.begin(), used.end(), 0); pool.clear(); count = 0; ++clears; }
  285|     size_t s = h & mask;
  286|     while (used[s]) {
  287|       if (hashes[s] == h && same(s, S)) return;
  288|       s = (s + 1) & mask;
  289|     }
  290|     used[s] = 1; hashes[s] = h; logm[s] = lm; off[s] = pool.size(); len[s] = (uint32_t)S.size();
  291|     pool.insert(pool.end(), S.begin(), S.end());
  292|     ++count; ++inserts;
  293|   }
  294| };
  295| 
  296| }  // namespace v3
  297| 
```

### [C:start] `Scripts/SMC_BVS/core/cpp/v3_start.h` @ a2c465a4 — code
lines 75–97:
```
   75| // capped) and are not scored (entry NaN).
   76| inline void build_tables(Start& st, Scorer& sc) {
   77|   const Data& D = *st.D;
   78|   st.J = (int)st.blocks.size();
   79|   st.blk.assign(D.p, -1); st.pos.assign(D.p, -1);
   80|   for (int b = 0; b < st.J; ++b) for (size_t i = 0; i < st.blocks[b].size(); ++i) { st.blk[st.blocks[b][i]] = b; st.pos[st.blocks[b][i]] = (int)i; }
   81|   st.logr.assign(st.J, {}); st.logm_tab.assign(st.J, {}); st.route_tab.assign(st.J, {});
   82|   std::vector<int> U;
   83|   for (int b = 0; b < st.J; ++b) {
   84|     int m = (int)st.blocks[b].size();
   85|     uint32_t ncode = 1u << m;
   86|     st.logr[b].assign(ncode, std::numeric_limits<double>::quiet_NaN());
   87|     st.logm_tab[b].assign(ncode, std::numeric_limits<double>::quiet_NaN());
   88|     st.route_tab[b].assign(ncode, -1);
   89|     for (uint32_t code = 0; code < ncode; ++code) {
   90|       U.clear();
   91|       for (int i = 0; i < m; ++i) if (code & (1u << i)) U.push_back(st.blocks[b][i]);
   92|       if ((int)U.size() > D.K) continue;
   93|       ScoreOut o = sc.score(U);
   94|       st.logm_tab[b][code] = o.logm; st.route_tab[b][code] = o.route;
   95|       st.logr[b][code] = (code == 0) ? 0.0 : o.logm - D.logm0;
   96|     }
   97|   }
```
lines 165–178:
```
  165|     kb[b] = j; r -= j;
  166|   }
  167|   S.clear();
  168|   for (int b = 0; b < J; ++b) {
  169|     if (kb[b] == 0) continue;
  170|     int i = cat_draw_gt(st.sub_cum[b][kb[b]], vs.u("pi0_submodel"));
  171|     uint32_t code = st.codes_by_size[b][kb[b]][i];
  172|     for (size_t t = 0; t < st.blocks[b].size(); ++t) if (code & (1u << t)) S.push_back(st.blocks[b][t]);
  173|   }
  174|   std::sort(S.begin(), S.end());
  175|   if (sizes_out) *sizes_out = kb;
  176| }
  177| 
  178| // Start mode S~_0 = argmax pi_0 (M §6.3; CORE_SPEC §3): max-plus convolution of per-block per-size maxima, summed
```
lines 255–308:
```
  255|           if (allowed[b - 1][j] && reach[b - 1][r - j] && mode_tight(dp, b, r, j)) ok = 1;
  256|         reach[b][r] = ok;
  257|       }
  258|     return reach[J][dp.kbest] != 0;
  259|   };
  260|   // E is never empty for valid tables (lemma TDP_E (2)); a failed root check is an invariant violation, never an empty model
  261|   if (dp.kbest < 0 || !feasible()) throw std::runtime_error("start_mode tie DP: no tight path from (J, kbest) (invalid tables)");
  262|   std::vector<int> S;
  263|   for (int i = 0; i < p; ++i) {
  264|     int b = st.blk[i]; uint32_t bit = 1u << st.pos[i];
  265|     inm[b] |= bit; refresh(b);
  266|     if (feasible()) { S.push_back(i); continue; }
  267|     inm[b] &= ~bit; outm[b] |= bit; refresh(b);
  268|   }
  269|   return S;
  270| }
  271| inline ModeResult start_mode(const Start& st, long cap = 1000000, bool tie_dp = true) {
  272|   if (tie_dp && cap < 2) throw std::invalid_argument("start_mode: the e4 tie-aware fallback requires cap >= 2 (C-PACK MR2)");
  273|   int J = st.J;
  274|   ModeDP dp = mode_dp(st);
  275|   const auto& mb = dp.mb; const auto& arg = dp.arg; const auto& M = dp.M;
  276|   int kbest = dp.kbest;
  277|   ModeResult res; res.lg0 = dp.vbest;
  278|   // enumerate all optimal choices backward; keep lexicographically smallest set
  279|   std::vector<uint32_t> choice(J, 0);
  280|   bool have = false; std::vector<int> bestS; long count = 0; bool trunc = false;
  281|   std::function<void(int, int)> rec = [&](int b, int r) {
  282|     if (trunc) return;
  283|     if (b == 0) {
  284|       if (r != 0) return;
  285|       std::vector<int> S;
  286|       for (int bb = 0; bb < J; ++bb) for (size_t t = 0; t < st.blocks[bb].size(); ++t) if (choice[bb] & (1u << t)) S.push_back(st.blocks[bb][t]);
  287|       std::sort(S.begin(), S.end());
  288|       ++count;
  289|       if (!have || lex_less(S, bestS)) { bestS = S; have = true; }
  290|       if (count >= cap) trunc = true;
  291|       return;
  292|     }
  293|     for (int j = 0; j < (int)mb[b - 1].size() && j <= r; ++j) {
  294|       if (M[b - 1][r - j] == NEG_INF) continue;
  295|       double v = (j == 0) ? M[b - 1][r - j] : M[b - 1][r - j] + mb[b - 1][j];
  296|       if (v != M[b][r]) continue;
  297|       for (uint32_t c : arg[b - 1][j]) { choice[b - 1] = c; rec(b - 1, r - j); if (trunc) return; }
  298|       choice[b - 1] = 0;
  299|     }
  300|   };
  301|   rec(J, kbest);
  302|   res.S = bestS; res.ties = count; res.truncated = trunc;
  303|   if (trunc && tie_dp) { res.S = mode_tie_dp(st, dp); res.tie_dp_used = true; }
  304|   return res;
  305| }
  306| 
  307| }  // namespace v3
  308| 
```

### [C:util] `Scripts/SMC_BVS/core/cpp/v3_util.h` @ a2c465a4 — code
lines 115–131:
```
  115| 
  116| // Strict lexicographic order on sorted index vectors (a proper prefix precedes the longer vector).
  117| inline bool lex_less(const std::vector<int>& a, const std::vector<int>& b) {
  118|   return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end());
  119| }
  120| // HPM strict order (M §6.10): larger F first; exact ties -> smaller |S|; then lexicographically smaller set.
  121| inline bool hpm_better(double F1, const std::vector<int>& S1, double F2, const std::vector<int>& S2) {
  122|   if (F1 > F2) return true;
  123|   if (F1 < F2) return false;
  124|   if (S1.size() != S2.size()) return S1.size() < S2.size();
  125|   return lex_less(S1, S2);
  126| }
  127| 
  128| // Insert j into / erase j from a sorted vector (models are kept sorted at all times).
  129| inline void sorted_insert(std::vector<int>& v, int j) { v.insert(std::lower_bound(v.begin(), v.end(), j), j); }
  130| inline void sorted_erase(std::vector<int>& v, int j) { v.erase(std::lower_bound(v.begin(), v.end(), j)); }
  131| 
```

### [C:blocks] `Scripts/SMC_BVS/core/cpp/v3_blocks.h` @ a2c465a4 — code
lines 136–144:
```
  136|   for (auto& c : clusters) {
  137|     if (cur.size() + c.size() > (size_t)B) { blocks.push_back(cur); cur.clear(); }
  138|     cur.insert(cur.end(), c.begin(), c.end());
  139|   }
  140|   if (!cur.empty()) blocks.push_back(cur);
  141|   for (auto& b : blocks) std::sort(b.begin(), b.end());
  142|   if (out_tree) *out_tree = T;
  143|   return blocks;
  144| }
```

## Task
Break the proof; findings only. Claims to decide, in this order (clause labels as in the statement file, §2–§4): LIST-K, LIST-CODE.i, LIST-CODE.ii, LIST-CODE.iii, LIST-CODE.iv, LIST-CODE.v, LIST-R.i, LIST-R.ii, LIST-R.iii. For LIST-CODE, open the code excerpts and look for a code path the proof misses. End with exactly one line per claim: `AUDIT D5P1 <claim> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.
