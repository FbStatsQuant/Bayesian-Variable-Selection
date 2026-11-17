# C-R1 · council seat `opus` (Claude Opus 5.5, high) · blind first read · W3-AUDIT track A_C item C1

Content reviewed: `C1_AUDITS/STATEMENT.md` (v2), `C1_AUDITS/PROOF.md` (v2.1), `C1_AUDITS/CITECHECK.txt` (not used for
any conclusion), the external inputs of `reviews/INPUTS_CR1.txt`, and DLV-0 at e78a1055 (`W3-RM2-R/STATEMENT.md`
lines 135-170, 220-240; `W3-RM2-R/lemmas/Q5_dlv0.md` in full). Manifest verified:
`verify: OK MANIFEST 221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef`. `git diff 4676af6 -- Scripts/SMC_BVS/core`
is empty in this worktree; the core is also byte-identical at 72785fe, 2aeb860 and e78a1055 (DLV-0's pin), so C1 and
DLV-0 read the same code. Not read (per the brief): `C1_AUDITS/CHECK.md`, any other `CHECK.md`, `INDEX.md`, `LOG.md`,
`P1_CONSUMERS.md`, `H5_T14_CARD.md`, other files in `reviews/`.

## Verdict summary
The substance of C1 holds at pin 4676af6 in the shipped default configuration. I walked every `return` of `v3_fit`
(`v3_fit.R:89, 102, 117, 131, 137, 159, 173`), every status that reaches them, and every explicit `stop` / `stopifnot` /
`throw` / `checkUserInterrupt` in `*.R` and `cpp/` (my own grep, which gives exactly PROOF §1.2's list). I found no reachable
no-estimates exit or error of the shipped `v3_fit` that some row (with the erratum, with A-7) does not cover. I found no
wrong "unreachable" (D2, X2 (i)–(vii), `get_holder`, X9, D1 under EX-A with the fallback) and no wrong re-location
among the roughly 60 pin lines I checked. A-7 is complete: the SMC preflight's two new disjuncts (`ls0_archive`
bytes; LS0 seconds, evaluated only once the bytes fit) and the gate `ls0_wc` are exactly as stated. The escalation
re-preflight's time term cannot newly fire, because ŝ_K is cached and the seconds do not depend on the tier. DLV-0 (E2)
does name and exclude the A-7 exit.

One finding blocks the gates. It is in C1's own description of how DLV-0 excludes the exit, not in DLV-0. (C1-c), and
PROOF §3 with it, says both A-7 terms are excluded by 𝒜_n's FIN A4 term P̄_LS0. P̄_LS0 is a time bound. The
`ls0_archive` byte term is excluded by A4's separate memory addition, mem_n ≥ P_e + A (FIN `s6_delivery.tex:37`;
DLV-0 itself says "memory P_e + A", `Q5_dlv0.md:64`). The fix is one line. Everything else is editorial.

## Gate table
| gate | result | basis |
|---|---|---|
| G1 correctness of every step and code citation | **FAIL** | F1 (the stated exclusion of the byte term is wrong); all code citations I checked are correct |
| G2 hypotheses used = stated | PASS | EX-A, IDEAL-W, MACH, valid declared inputs, A:IDEAL-W⁺ or 𝔇 for X7–X8; T9's (H4) is subsumed (E3) |
| G3 no hidden assumptions | PASS | the default configuration is stated with all five options; the timing path and the extra nodes are named (§1.3) |
| G4 imports and statuses verbatim | **FAIL** | F1 (FIN A4 is quoted as one term for two triggers); missing import statuses are only E4 |
| G5 scope (configuration, options, branches, tiers) | PASS | both branches; tier 0 and the escalation; `ls0`, `v3.ls0`, `v3.grid_fallback`, `v3.ls0_cap`, `v3.ls0_ell`, `v3.ls0_tie_dp` (these are all of the core's `getOption` calls) |
| G6 fidelity to the code as pinned and to the registered texts | PASS | INVENTORY, L2 S.3 and C-DLV STATEMENT spans checked against the files; code lines checked against the pin |

## Claim table
| id | decision |
|---|---|
| C1 | **REJECT as written.** The substance is verified: (C1-a) coverage after A-7, (C1-b) unreachability, and the DLV-0 hand-off all hold. I would ACCEPT after the one-line F1 repair to (C1-c) and PROOF §3. |

## Findings
**F1 (F) — the A-7 byte term is attributed to the wrong allocation term.**
`C1_AUDITS/STATEMENT.md:54-56` ("its (E2) names the SMC LS0 archive and LS0 time preflight terms and excludes them by
the allocation 𝒜_n's term P̄_LS0 (FIN A4)"); `C1_AUDITS/PROOF.md:94-96` ("excluded there by 𝒜_n's FIN A4 term P̄_LS0").
FIN A4 (`Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:37`) adds two separate conditions:
- time_n ≥ P̄_LS0 := (ℓ_n+K+1)q(p)(τU_K+τ₀)/100, which excludes the seconds disjunct (`v3_fit.R:47, 65`);
- mem_n ≥ P_e + A (e = 0, 1), with A the `ls0_archive` bytes, which excludes the byte disjunct (`v3_fit.R:45, 50, 60`)
  at tier 0 (`v3_fit.R:117`) and at escalation (`v3_calib.R:157`).

DLV-0 (E2) states both (`Q5_dlv0.md:63-65`: "the LS0 preflight time 2(ℓ_n + K + 1)q(p)ŝ_K ≤ P̄_LS0 and memory P_e + A"),
so DLV-0 has no gap. C1's restatement of it does.

Failure scenario: an allocation with time_n ≥ max{2[τW_G+τ₀], P̄_t, P̄_LS0} and mem_n ≥ max{βM_G+β₀, P₀, P₁} but
mem_n < P₀ + A. Nothing in FIN makes βM_G+β₀ dominate P_e + A, which is why A4 adds it separately. The preflight then
returns `resource_limit` at `v3_fit.R:117` on the `ls0_archive` bytes, and the mechanism C1 names (P̄_LS0) does not
exclude it.

Repair: in (C1-c) and PROOF §3, write "excludes the LS0 time term by P̄_LS0 and the `ls0_archive` bytes by
mem_n ≥ P_e + A, e = 0, 1 (FIN A4, `s6_delivery.tex:37-44`)". The same wording should replace the brief's shorthand
wherever C1 text is copied into the log or index.

**E1 (E) — the scope of A-7 is worded two ways.**
`STATEMENT.md:60-75` files the escalation re-preflight under "A-7 (B1 …) Row B1′ (or B1 extended)". `PROOF.md:22`
and (C1-c) (`STATEMENT.md:52`) instead read the escalation site as "B3 (with A-7)". Both readings cover the site:
B3's registered trigger, "tier-1 memory estimate > mem" (`INVENTORY.md:31`), names no formula, so it already contains
the archive bytes. Pick one: either "B1′ = the tier-0 site, and B3's estimate includes `ls0_archive`", or "B1′ covers
both sites".

**E2 (E) — the A-7 text says the escalation re-preflight can stop on the LS0 seconds.**
`STATEMENT.md:70-72` says the escalation re-preflight "also returns `resource_limit` when the LS0 worst-case seconds …
exceed `hours`·3600". `PROOF.md:33-34` correctly shows this disjunct cannot newly fire at escalation: tier 0 passed the
same test, and ŝ_K is cached in `time_fun` (`v3_fit.R:107-112`), whose `<<-` writes v3_fit's `tcache`. Only the byte
term can. Align the STATEMENT with PROOF §1.1.

**E3 (E) — T9's (H4) is not named.**
(C1-b) uses T9 (TDP-e) for `cpp/v3_start.h:261`. T9 v3 makes its compiled-code return claims conditional on (H4)
(`track_A/T9_TDP/STATEMENT.md:24-30`): `int` fits, |C_b| ≤ 31, allocations succeed, recursion completes. (H4) is
discharged by IDEAL-W, MACH and T2 (|C_b| ≤ 16), all premises C1 already has. Say so in one clause, so that G2 can be
read off the text.

**E4 (E) — import statuses are not recorded.**
C1 consumes T10 (cited "STATEMENT v2.2 / PROOF v2.1, council-bound R2", `PROOF.md:3-4`; the T10 file header still reads
"STATEMENT v2 (draft, not locked)"), T2 BLK v6, T4 ENC v3, T9 TDP v3, T14 REP v1 ("DRAFT, post-freeze item; not
locked"), `C-DLV:Prop-F` (A-4) and FIN A4 ("OK-WITH-FIXES"). It gives the status of none of them. The P1 and S.3
statuses are quoted verbatim. Add a one-line "Consumed (status verbatim)" list.

**E5 (E) — a note for the L1-R / Cor-R owners; not C1's claim.**
At the pin, the SMC branch now builds a second context in the preflight (`v3_fit.R:12`, through `v3_fit.R:47`), with
m = min(p, max(64, K)) columns, so an m × m Gram and an n × m copy (`cpp/v3_score.h:41-52`). Before ef33f91c the timing
context was built only on the exact branch, with m ≤ max(64, ⌈p/2⌉). On the SMC branch m can be about n/2. This is an
X5 instance and C1's coverage is unaffected. Whether Lemma R's word envelope (or FIN's M_G) counts this object on the
SMC branch is outside C1 ("Not claimed": resource bounds). Recording it here so the owners can check.

**E6 (E) — a cosmetic citation.**
`PROOF.md:18` cites `v3_preprocess.R:98-107` for A3; line 98 is the `bad` helper and the checks are lines 99-107, as
`STATEMENT.md:69` correctly says.

## Overall score
**8.5 / 10** (C, S and F findings only). There are no C or S findings and one F (F1), which is a one-line repair. Its
conclusion is unaffected: DLV-0 (E2) covers both A-7 terms.

## Checks performed
- Ran the manifest verify (OK). Confirmed the core is unchanged between 4676af6 and the working tree, and between
  4676af6 and 72785fe, 2aeb860 and e78a1055.
- Read `v3_fit.R`, `v3_run.R`, `v3_calib.R`, `v3_preprocess.R`, `v3_setup.R`, `v3_exact.R`, `v3.R` and
  `cpp/v3_core.cpp` in full; read `cpp/v3_runtime.h`; read the relevant parts of `cpp/v3_engine.h` (138-155, 296-422),
  `cpp/v3_start.h` (236-305) and `cpp/v3_score.h` (30-70, 220-238).
- Grepped `stop(`, `stopifnot`, `throw`, `checkUserInterrupt`, `Rf_error`, `abort(`, `.at(` across `*.R` and `cpp/`.
  The result equals PROOF §1.2's list exactly. Checked each item's map, and that the off-graph items (core 112, 148,
  209-219, 233-257; `v3_setup.R:18, 49, 81`) are off the graph.
- Every `return` of `v3_fit`, and every status source reaching it: preprocess statuses; preflight (both branches, and the
  `ls0_wc` gate at `v3_fit.R:114`); exact statuses (core 536, 556); setup failure (core 284-297); calibration statuses
  (pilot 637/645, diag 673-680/692, V 717-721, grid guard `v3_calib.R:75-81, 113`, escalation 157, fallback/D1/D2
  163-170); final run (core 451, 459, 480, 483-484; `v3_run.R:143-148, 218`). Also checked that
  `estimates_available` becomes TRUE only at `v3_fit.R:129` and `v3_run.R:218`.
- A-7 in detail: the byte component formula against FIN's A; that the time disjunct is evaluated only when the bytes fit
  (`v3_fit.R:47`); the `isTRUE` on NA (`v3_fit.R:65`); the escalation tier-independence of the seconds; the `tcache`
  closure; and that `cpp_time_scores` clips k to `D.K` (core 126) and catches `NumericalFailure` (core 134), so the
  timing path adds only `get_holder` / implicit / allocation errors, as PROOF §1.3 says.
- D2 unreachable, and the fallback logic for D1 (`v3_calib.R:122-125, 163-170`, with the pilot schedule built at core
  636 and the adaptive stop at `cpp/v3_engine.h:310`).
- X9: core 469 passes cap 10⁶, so `v3_start.h:272` is dead; `:261` is exactly T9's (TDP-e) predicate.
- X7–X8: the R representability bound (core 92, 402, 473-474; `v3_run.R:95-98`).
- C1's citations of INVENTORY (`:6-10, 15-93, 29-31, 71-77, 80-81, 83-93`), L2 (`:37-67, 72`), C-DLV STATEMENT
  (`:52-56`), DLV-0 (`STATEMENT.md:144-162`; `Q5_dlv0.md:59-64`) and FIN (`s6_delivery.tex:33-44`): spans and wording.

## Not checked
- The proofs of T2 BLK, T4 ENC, T9 TDP (TDP-e) and T14 REP. Per the brief they are council-checked siblings; I checked
  only that their statements say what C1 uses.
- T10 §3's monotonicity argument for `pilot_next_phi` (`cpp/v3_calib.h:30-46`); not re-derived.
- Lemma R / Corollary R, FIN A1/A4's derivations (U_K, P_e), and HQ audit A4.
- Engine internals beyond the cited lines (`population_round`, `resample`, ledger/cache code), beyond the X2-imp class
  argument.
- Binary64 behaviour (out of scope under EX-A), non-default options, and inspection helpers off the call graph.
- `CITECHECK.txt` and `citecheck.py` were not re-run.

COUNCIL-VERDICT round=R1 manifest=221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef seat=opus score=8.5 gates=FAIL
