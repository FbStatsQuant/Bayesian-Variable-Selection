# W3-MISR — PLAN (v1.1, 2026-11-11; v1.1 = claims table updated after the statement lock and the better-theorem review)

Ticket T1 of `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md`: C-MIS v2, the misspecified-subset theorem without fixed
variances. Brief: `BRIEF.md`. Legs CP1 → CP2 pre-approved when reviews are clean (no open FATAL/MAJOR; council ≥ 8.0).

## Target, in one paragraph
The coded posterior depends on the response only through its standardised version, so it is exactly invariant under
y ↦ a1 + c·y. Hence only signal-to-noise ratios matter: "σ², τ² fixed" in C-MIS becomes any σ²_{𝒞,n} > 0, with the
energy bound, the identifiability margin and beta-min stated relative to σ²_{𝒞,n}; and GR is needed only for the
contrast law of the candidate residual. The input theorem changes from T03♯ to W3-POST2 (A1, C, E), so the conclusion
becomes an expectation rate that is uniform over a class of (design, coefficient, variance) configurations; the
random-design clause follows by conditioning.

## Claims (each with its own status)
| id | content | route |
|---|---|---|
| R′ | (a) invariance of π under y ↦ a1 + c·y; equivariance of the parameter posterior; code pin. (b) contrast-law reduction to a unit-noise G-model | direct; code read + compiled-code run (N0) |
| MIS(i) | fixed design: sup over the class 𝒦_n of E[1 − π_𝒞(S₀^𝒞)] ≤ C r_n, constants free of σ²_𝒞; HPM/MPM/PIP rates | R′(b) + W3-POST2:C |
| R′(c) | projective form of the law condition; total-variation stability (v1.2, BT1-A1) | direct |
| MIS(i′) | without the margin: supersets, strong coordinates, localisation — in expectation, per n (v1.2: (d), BT1-A3) | R′(b) + proof steps of W3-POST2:C, A1, E |
| MIS(ii) | conditional form: E[δ_n ∣ 𝓕_n] ≤ C r_n on 𝒜_n; design-measurable σ²_𝒞(x); s-slicing; tight constants | MIS(i) + conditioning + Markov |
| Cor-G | Gaussian rows with n-dependent (Σ, σ², τ²): GR^c holds; growing-p envelope without fixed σ²_𝒞 (example) | C-MIS:Prop-P, C-MIS:GD(b) proof steps |
| Cor-H | density (average Hellinger) contraction around the projected law — Song–Liang Thm 4 analog | R′ + W3-POST2:D |
| Rem-SNR | W3-POST Theorem 1 and W3-POST2 A1, B, C, E hold with σ*²_n in SNR form; C-MIS Theorem F likewise | R′(a) |

## Steps
CP1
1. STATEMENT v1.0 (assumption ids, registry block draft).
2. Sol statement-lock review, blind (codex gpt-6.1-sol, high) → disposition → locked version.
3. ASSUMPTION_MAP.md; numerics (local only, `numerics/`): N0 compiled-code invariance; N1 σ²_{𝒞,n} → 0 / → ∞ with SNR
   held; N2 relative beta-min violated (the R02 "variance n²" example); N3 outside GR^c (non-scalar contrast covariance;
   heavy tails); N4 outside (E^σ).
4. Astra better-theorem review, blind (codex gpt-6-astra, high) → disposition per proposal.
5. CHECKPOINT_1.md; commit.
CP2
6. Proof files `lemmas/` (R′; MIS; Cor-G; Cor-H + remarks). citecheck.
7. Sol lemma checks (blind) → dispositions.
8. Freeze manifest; council (Sol + Opus 5.5 on Claude Work, high; both ≥ 8.0, all gates); reconciliation if a second
   round is needed (one fix round at most, per the run instructions).
9. REPORT.md with the registry block; CHECKPOINT_2.md; commit; end of run.

## Kill budget
Key lemma = R′ + MIS(i). Three failed attempts → STUCK at the checkpoint (PROTOCOL rule 14; BRIEF). A review that is
not clean after one fix round → stop and report.

## Consumed claims (registry id @ version, state on base main 16a7f85)
W3-POST2:C@1.0.0, W3-POST2:E@1.0.0, W3-POST2:A1@1.0.0, W3-POST2:D@1.1.0 (with D.D(a)@1.0.0, D.D(b)@1.2.0),
W3-POST2:A0@1.0.0, W3-POST2:B@1.0.0 and W3-POST:Thm-1@1.0.0 (remark only), C-MIS:Prop-P@1.0.0, C-MIS:GD(b)@1.0.0
(proof steps), C-MIS:Thm-MIS(i)/(ii)@1.0.0, C-MIS:Thm-F@1.0.0, C-MIS:LemZ@1.0.0 (remark only). (C-MIS:LemDR is no longer
consumed: the no-margin clauses are per-n expectation bounds, so no diagonal argument is needed.) All ACTIVE. The W3-POST2 rows carry the verbatim status
"PROVED (by this seat, unchecked)" in the registry ⇒ treated as declared hypotheses (`@hyp`, "conditional on …").
