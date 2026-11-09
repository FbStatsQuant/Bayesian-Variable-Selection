# W3-SAMP · LOG

(Times corrected at 17:20 from file modification times: the first version of this log carried estimated clock times
that ran ahead of the real clock. Order of events unchanged.)

- 2026-11-09 ~16:05 CST — Read Wave3 PROTOCOL/PROGRAM, Wave2/Wave1C/Wave1 protocols, W1-N1 STATEMENT/REPORT/L2, T12
  STATEMENT/STATUS, SR critique §3, ADJ_opus §1(c)-(d), ADJ_astra §1(c)-(d), BLIND_fable Thm 4, BLIND_astra2 Thm 3/5.
- ~16:14 — Code check on main (= 4676af6): `lemmas/CC_code_check.md`. Findings: (i) rejected π₀ proposals are scored and
  offered to the HPM before acceptance (confirms ADJ_opus/ADJ_astra); (ii) **main computes no plain PIP** — only RB PIPs;
  W1-N1's `pip_plain` identification refers to the frozen v2.2.1 core; (iii) T ≤ T_e on every grid path incl. the fallback;
  (iv) B ≤ 16.
- ~16:16 — Key observation: T12 (i.c)/(ii) (proved; card "PROVED-LOCKED") already gives the mid-round RB identity that
  ADJ_opus calls unproved; and a "stay at S₀" kernel bound (any π-invariant kernel leaves S₀ w.p. ≤ o₁; all Gibbs
  coordinates together ≤ o₁; B ≤ 16) gives a sup-norm RB transfer with **no factor p and no posterior size control**,
  which repairs ADJ_opus Flaw 1 and ADJ_astra's "RB values need not be 0/1" (the residual κ₀ ≤ o₁ is exact). For C, a
  stopping-time argument improves T²δ̄ to Tδ̄. Flaw 2 (near-circular premise) is answered by honest labelling + discharge
  by C + one-sided falsifier; no certificate exists from output.
- 16:18 — STATEMENT v1, PLAN v1 written. Next: statement lock (Sol high).
- ~16:22 — Numerics v1 (`numerics/RESULTS_v1.txt`, `RESULTS_v1_sec4b.txt`); ASSUMPTION_MAP.md drafted.
- 16:28 — SL1 (Sol high): LOCK WITH CHANGES, 5 items, all accepted (`reviews/SL1_disposition.md`). STATEMENT v2 LOCKED;
  CC v2. Next: "better theorem" review (Astra high) for the sharpness gate.
- 16:29 — BT1 "better theorem" review launched (gpt-6-astra high). Proofs written (by this seat, unchecked):
  `lemmas/MR_identities.md`, `PC_completed.md`, `ST_stay.md`, `D_theorem.md`, `LT_theorem.md`, `C_theorem.md`.
- ~16:40 — Numerics v2 (`numerics/run_checks_v2.py`, `run_checks_v2b.py` → `RESULTS_v2.txt`): regression-realisable targets
  (T12 §0 score/prior, block start), direct stopped-sum test (pointwise min(U,u) ≤ Y and stagewise bound hold in every
  island), C-i pointwise, heavy-tailed W (max W = 89.5) identities; 0 violations, identity max|z| = 2.70. Concentrated
  regression case n = 400: RB error ≈ κ₀ = 0.041, MPM correct in all islands; T factor again loose.
- 16:41 — LC1 lemma check launched (Sol high), in parallel with BT1. CHECKPOINT.md written.
- 16:34–16:58 — BT1 (Astra high) returned 16:34: T-free C by telescoping; terminal repair; MAP premise; uniform RB error O(δ̄).
  Lead re-derived and adopted (`reviews/BT1_disposition.md`): STATEMENT v3 (strengthenings only), `lemmas/C_theorem.md` v2,
  new `lemmas/TR_theorem.md`, `LT_theorem.md` v2 (Step 2′, LT-e′), `D_theorem.md` v2 (MAP). Numerics v3
  (`numerics/run_checks_v3.py` → `RESULTS_v3.txt`): 0 violations. Flag for HQ: statement strengthened after lock via
  the sharpness gate; HQ may revert to v2 (all v2 claims remain implied by v3).
- 17:06 — LC1 (Sol high): no CRITICAL; LT-a–e, C stopped sum, D iid draws, MR extension, PC verified; 2 MAJOR (v3_frozen
  N/L interface; LT-f asymptotic sharpness claims) + 5 MINOR — all accepted and fixed (`reviews/LC1_disposition.md`).
  Next: independent mid-point (Astra high) on STATEMENT v3 + lemmas only.
- 17:08 — LC2 (Sol high; new BT1-derived pieces) and MP1 (Astra high; statement + proofs only) launched in parallel.
  `citecheck.py` → `reviews/CITECHECK.txt`: 82 citations, 0 missing/out-of-range; first lines eyeballed against claims
  (bare `STATEMENT.md`/`PROOF_v6.tex` resolve to T12). Re-run before the council.
- 17:13 — MP1 (Astra high, statement + proofs only): **CONTINUE**; 1 MEDIUM (P-OVL∞ localisation) + 2 LOW, all fixed
  (`reviews/MP1_disposition.md`). Waiting on LC2.
- 17:15 — LC2 (Sol high): VERIFIED WITH AMENDMENTS (1 MAJOR = MP1 #1, already fixed; 4 MINOR fixed;
  `reviews/LC2_disposition.md`). Next: exhaustive sweep SW1 (Sol high) on the full package.
- 17:15 — SW1 exhaustive sweep (Sol high) launched.
- ~17:19 — SW1 ended with status **cancelled** (not by the lead; no reason attached, no review file written). Per the T3
  rule not to start replacements for externally stopped work, the lead did not relaunch it. Citation check re-run on the
  final text; REPORT.md written (status: proofs cross-family checked at lemma level + mid-point CONTINUE; sweep and
  council NOT run).
