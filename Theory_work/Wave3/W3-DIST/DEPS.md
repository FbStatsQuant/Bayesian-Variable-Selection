# W3-DIST — DEPS (dependency trace; HQ steer A2)

Format: `id | version | depends on (ids@version; external claim ids@registry version) | check status`.
Rules: when a lemma is refuted or changed, every dependent is marked SUSPECT in the same edit. No lemma is consumed by
another before its line check. Check-status vocabulary: CANDIDATE (statement only) · SKETCH (route written, unchecked) ·
DRAFT (proof written, unchecked) · PRECHECK (Opus same-family pre-check passed) · LINE-CHECKED (cross-family, file named)
· REFUTED · SUSPECT.

## Lemmas and theorems of this ticket
H     | 1.0 | W3-POST2:D@1.1.0 (Lemma D0 computation only) | SKETCH (5-line proof in STATEMENT §3; unchecked)
T     | 1.0 | external: VC relative deviation inequality (Anthony & Shawe-Taylor 1993; cite to be checked) | SKETCH
S     | 1.0 | locked T01 ([P1] thm:T01i, lem:spec); starting point W3-POST:Lemma-1a'@1.0.0, W3-POST2:B@1.0.0 (not consumed as premises) | CANDIDATE
V     | 0.1 | — (helper H1, `work/prior_probe/REPORT.md` §3 + A2; algebra checked numerically there) | DRAFT (helper-derived, unchecked)
X     | 1.0 | S@1.0; V@0.1; W3-POST2:A0@1.0.0 ((ND) interface, a_J re-derived); templates W3-POST2:D@1.1.0 (D1), W3-POST2:E@1.0.0 (E1(b)) | CANDIDATE
X'    | 1.0 | S@1.0; templates as X (no A0) | CANDIDATE
DIST-1| 1.0 | H@1.0, T@1.0, X@1.0 | CANDIDATE
DIST-2| 1.0 | H@1.0, T@1.0, X'@1.0 | CANDIDATE
DIST-3| 1.0 | H@1.0; W3-POST2:D.D(a)@1.0.0; W3-POST:Thm-1@1.0.0 (item 6) or any source of δ_n → 0 | CANDIDATE (assembly)
P6    | 1.0 | — (deterministic) | SKETCH
DIST-C| 1.0 | P6@1.0; DIST-1@1.0 (or DIST-2@1.0); W3-SAMP:CC@1.1.1; SOP:TH04@1.0.0 (M4(c)); for (C-ii)–(C-iv): W3-SAMP:D@2.1.1, LT#@2.0.1, C@1.1.1, TR@2.1.1; W3-RM2:RM2-F@1.0.0, RM2-R@1.0.0 | CANDIDATE
B1    | 1.0 | — (LLN / sub-Gaussian tails) | CANDIDATE
B2    | 1.0 | external: small-ball lower bound for sample covariance on sparse sets; example W3-POST:Cor-1R@1.0.0 | CANDIDATE
S-APX | 0.1 | X@1.0, S@1.0; W3-POST2:B@1.0.0 | CANDIDATE (stretch)
S-EXP | 0.1 | X@1.0, T@1.0 | CANDIDATE (stretch)
S-FIT | 0.2 | V@0.1 (supersets only) | OPEN (stretch; was S-DIM — its exponential-form size version is REFUTED by duplicates, H1 F4)

## Fallbacks (in-probability, no new lemma)
F-b   | 1.0 | H@1.0, T@1.0; W3-POST2:D.D(b)@1.2.0 | CANDIDATE (assembly; conditional on W3-POST2:D)

## External consumed claims (registry state on main at cef2c32: all ACTIVE)
W3-POST2:D@1.1.0 (D.D(a)@1.0.0, D.D(b)@1.2.0), W3-POST2:A0@1.0.0, A1@1.0.0, B@1.0.0, E@1.0.0 — "PROVED (by this seat, unchecked)".
W3-POST:Thm-1@1.0.0, Lemma-1a'@1.0.0, Prop-LB@1.0.0, Cor-1R@1.0.0. W3-SAMP:CC@1.1.1, D@2.1.1, LT#@2.0.1, C@1.1.1, TR@2.1.1.
W3-RM2:RM2-F@1.0.0, RM2-R@1.0.0. SOP:TH04@1.0.0, SOP:TH09@1.0.0. W2-APP:POST@1.0.1.
Not in the registry (route guide only, not consumed): T04 (`Docs/Theory/proofs/T04_A3_contraction/`).

## Change record
- 2026-11-15 v1.0: file created at scoping. No lemma has a line check; nothing is consumed yet.
- 2026-11-15 v1.1: V added (H1); X now depends on V; S-DIM → S-FIT (size form refuted; no dependents to mark).
