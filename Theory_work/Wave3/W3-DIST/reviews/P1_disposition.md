# W3-DIST — disposition of the same-family pre-check P1 (`reviews/P1_opus_precheck.md`; Claude Opus 5.5, Claude Third, high)

P1 is a filter before the cross-family check, not a review layer. Object: STATEMENT v1.2 §1R (reader versions) and §3
bridges. Verdict: **REPAIRABLE** — no reader clause false under its faithful reading. Per clause: Theorem A, Theorem B,
B0, B2-core, B2 REPAIRABLE; Corollary C, B1, B3 SOUND-AS-STATED. 3 MAJOR (all wording), 6 MINOR, 7 NIT. All accepted;
edits in STATEMENT v1.3, TARGET.md §6, ROUTES §2b, API_CARDS card B.

| id | sev. | finding | disposition |
|---|---|---|---|
| P1-01 | MAJOR | Theorem B: "(A4) strengthened to …" reads as replacing (A4); under that reading an exact dependence among (2A+3)s+3 null predictors is a counterexample | **ADOPT**: "(A1)–(A5) … and in addition (A6)", with the fixed floor as (A6)(a) |
| P1-02 | MAJOR | TARGET §6 (A3) row claimed the display "under second moments with probability → 1"; false for the non-degeneracy interface (atom of mass 1 − 1/n: two identical sample columns w.p. ≈ e⁻¹) | **ADOPT**: claim removed; row now says no primitive statement under weaker tails is claimed; parity row P2 (16) annotated |
| P1-03 | MAJOR (wording) | (A3), (A4) depend on M through q_n before M is introduced | **ADOPT**: M (the level) and the window q_n are fixed before the assumptions; the theorem says "with the window q_n of this M" |
| P1-04 | MINOR | B2's one-column determinant formula ((n+1)γ+1)/(γ+1) is false (19 796 of 20 000 random designs); the conclusion holds by interlacing | **ADOPT**: interlacing argument; same conclusion (DG; g₀/(1+g₀)) |
| P1-05 | MINOR | B0: a statement about the law of the posterior is not enough (d_H depends on ȳ, x̄) | **ADOPT**: pathwise form with ỹ = (y − α*)/σ* |
| P1-06 | MINOR | Setup: σ² on two scales; constant columns; intercept wording | **ADOPT** |
| P1-07 | MINOR | B2-core false as literally stated when q ≥ ep | **ADOPT**: q′ = min(q, p); window q_n = min{p, …} |
| P1-08 | MINOR | TARGET §6 (A5) row: coefficient norm alone does not give the energy condition | **ADOPT**: row reworded |
| P1-09 | MINOR | Corollary C's last sentence a tautology; retention content lost | **ADOPT**: "if a completed run evaluated the true model and its posterior probability exceeds ½, the list contains it" |
| P1-10 | NIT | M ≤ √n with κ₀ = 0.4 forces n₀ ≈ e³⁶ | **ADOPT**: range M ≤ √n/log n (κ₀ = ½). Tagged WEAKER (range only) in the changelog; the reader clause was not yet fixed at CP1 |
| P1-11 | NIT | B1 needs n ≥ 3 | **ADOPT** |
| P1-12 | NIT | Corollary C: "completed", exact arithmetic, P* over data and run-uniform, scope | **ADOPT** |
| P1-13 | NIT | triangular arrays covered — say so; "(1+s) log p" hides the dependence of M₀ | **ADOPT**: stated; the "(1+s) log p" phrase removed from the reader text |
| P1-14 | NIT | B1′ is not an alternative to (A5) | **ADOPT**: B1′ dropped |
| P1-15 | NIT | TARGET §6 preface anticipated this pre-check | **ADOPT**: preface rewritten after the fact |
| P1-16 | NIT | Theorem B's conditionality on W3-POST:Thm-1 appears only in the preface | **KEEP as is** in the reader text (it will cite the paper's own selection theorem); the conditionality is in §1R's preface, the consumes table, DEPS and CHECKPOINT_1 |

Checks P1 reports as passed (not a line check): B1's probability and triangle step; B2-core's argument including the
intercept and degenerate directions; λ_min(G_T) ≥ c_ψ/8; q_n ≥ m_n(M log n) + s for all M ≥ 1 with one n₀; the renaming to
n^{−cM}; B3's set sizes and beta-min envelope; Corollary C's bound for every run on the data event.
Still owed: the cross-family check of §1R and the bridges (and of the changelog tags) — for HQ to order.
