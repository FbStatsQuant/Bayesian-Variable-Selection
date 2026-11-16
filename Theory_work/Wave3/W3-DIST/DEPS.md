# W3-DIST — DEPS notes (dependency trace; HQ steers A2, A4). Table: `DEPS.tsv`

## The table is `DEPS.tsv` (PROTOCOL_v4 §4.1 form, from v1.2 of this file)
`id | file[:lines] | uses | sha | checked_sha | checked_by | state`, state ∈ {OK, UNCHECKED, STALE, REFUTED, DOWNSTREAM},
kept by hand with sha256 until `deps.py` exists. Freeze rule: the sweep and council manifests are frozen only when
every row under a claim is OK; proving and checking may run in parallel (this replaces the ordering rule of HQ steer
A2). At CP1 every row is UNCHECKED: the blind read S1 was a statement review of v1.0.2, not a line check, and the
files have changed since. Rows whose v1.0.2 form S1 refuted (T, B1) are repaired in v1.1 and marked so.

## External consumed claims (registry state on main at fe9a1d7: all ACTIVE; W3-POST2:D per HQ note 2026-11-15: D(b) repaired after council, diff round in progress)
W3-POST2:D@1.1.0 (D.D(a)@1.0.0, D.D(b)@1.2.0), W3-POST2:A0@1.0.0, A1@1.0.0, B@1.0.0, E@1.0.0 — "PROVED (by this seat, unchecked)".
W3-POST:Thm-1@1.0.0, Lemma-1a'@1.0.0, Prop-LB@1.0.0, Cor-1R@1.0.0. W3-SAMP:CC@1.1.1, D@2.1.1, LT#@2.0.1, C@1.1.1, TR@2.1.1.
W3-RM2:RM2-F@1.0.0, RM2-R@1.0.0. SOP:TH04@1.0.0, SOP:TH09@1.0.0. W2-APP:POST@1.0.1.
Not in the registry (route guide only, not consumed): T04 (`Docs/Theory/proofs/T04_A3_contraction/`).

## Change record
- 2026-11-15 v1.0: file created at scoping. No lemma has a line check; nothing is consumed yet.
- 2026-11-15 v1.1: V added (H1); X now depends on V; S-DIM → S-FIT (size form refuted; no dependents to mark).
- 2026-11-15 v1.2: table moved to `DEPS.tsv` in the PROTOCOL_v4 §4.1 form; T and B1 (v1.0.2 forms) refuted by S1 and repaired in STATEMENT v1.1 — dependents of T: DIST-1, DIST-2 (their statements use the repaired range; no other change). DIST-3 no longer uses W3-POST2 D(a).
