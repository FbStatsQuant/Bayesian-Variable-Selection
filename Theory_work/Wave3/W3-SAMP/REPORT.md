# W3-SAMP · REPORT to Theory HQ (PROGRAM item 4: sampler outputs as coded, honestly labelled)

**Flags at the top.**
1. **Pipeline incomplete.** The exhaustive sweep SW1 (Codex Sol, high) ended with status *cancelled*. I did not cancel it,
   and it gave no reason and wrote no file. Because I don't know whether HQ intended the stop, I did not relaunch it. The
   council has **not** run. Everything else is done: statement lock, sharpness gate, two cross-family lemma checks
   (LC1, LC2), the independent mid-point (CONTINUE), and the citation check. The package is ready for SW1 and the
   council; the briefs to reuse are recorded in LOG.md.
2. **Statement strengthened after the lock** through the sharpness gate (STATEMENT v2 → v3). Every change is a
   strengthening and every v2 claim is still implied. The main change: the concentrated-bridge evidence bound no longer
   depends on the number of stages T, and it needs no rate on the start mass. HQ may revert to v2.
3. **Code finding:** main (4676af6) computes **no plain (endpoint) PIP**. The only coded PIP is the Rao–Blackwell PIP,
   recorded before each Gibbs draw. W1-N1's `pip_plain` identification applies only to the frozen v2.2.1 core.
4. **Start-mass rate (P-START, PROGRAM item 2) is an input, not proved here.** Theorem C needs only π₀(S₀) → 1, with no
   rate. Please route this to the item-2 ticket.
5. My LOG first carried estimated clock times that ran ahead of the real clock. I corrected them from file times;
   the order of events is unchanged.

## 1. RESULT

**PARTIAL.** All seven results below are proved. Each was cross-family checked at the lemma level (LC1, LC2, Codex Sol
high), and the independent mid-point review (MP1, gpt-6-astra high) said CONTINUE. All issues from those reviews are
fixed. The results are not yet PROVED-CHECKED: the sweep was cancelled and the council has not run. No counterexample to
any claim was found by any reviewer or by the numerics.

## 2. The statement as proved

File: `STATEMENT.md` (v3). The v2 lock was by SL1 (Codex Sol): LOCK WITH CHANGES, all five changes applied. The v3
amendments come from the sharpness gate (BT1).

All of these are about the method as coded on main and design-agnostic (no design family appears). Finite-sample claims
are given the data and the calibration record 𝓒, on the calibration-success event 𝒜, in W1-N1's localised form.
Asymptotic claims are under the joint law, always intersected with 𝒜 or with {completed}. P(𝒜) → 1 is never assumed.

- **Lemma CC (code facts, CC1–CC7):**
  - every π₀ draw is scored and offered to the HPM ledger *before* its accept decision — the N_e initial draws and the
    one independence proposal per particle per round, accepted or rejected (`cpp/v3_engine.h:182-191, 286-292`);
  - island r makes exactly D_r = N_e(1+T+L+4) draws;
  - on completed runs, the reported HPM is the hpm_better-maximum of all models scored in the run, all of which lie in Ω;
  - pip_primary is the equal-weight mean of the island RB PIPs (`v3_run.R:162`); MPM = {pip_primary > ½};
    log_Z = log of the mean of Ẑ_r;
  - for production calibration, T ≤ 4·max(1000, ⌈log₂(n+p+1)⌉²); B ≤ 16;
  - arbitrary (N_e, L) are reachable only through the engine component. The public wrapper takes them from the budgets.
- **Lemma PC.** A completed run carries the potential (uninterrupted) island records. This is the limited GUARD-W
  comparison needed here.
- **Theorem D (draw discovery, item d).**
  - The draws are iid π₀ given 𝓒, so P(no draw of island r equals S₀ | 𝓒) = (1 − π₀(S₀))^{D_r}, with **equality**.
    Under IND-T the exponent is 4D_r.
  - P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜(1 − π₀(S₀))^{D_r}], where S† is the exact HPM over Ω (MAP premise).
  - Production: D_r ≥ max(2500, n, p)(L+6). So max(n, p)·log₂(n+1)·π₀(S₀) → ∞ suffices, with no condition on mixing, the
    bridge or Ẑ.
- **Lemma MR.** These are T12's frozen-run identities (i.a)–(i.c) and (ii), extended to "given 𝓒" for bridge stages,
  terminal endpoints, and pre-step states. In particular E[W_r p̂_r(j) | 𝓒] = PIP_j for the coded RB recording. This is
  the "mid-round N1 extension" that ADJ_opus called unproved: it was T12 (i.c)/(ii) plus a short freezing extension.
- **Lemma ST (staying at S₀).**
  - Any π-invariant kernel leaves S₀ with probability ≤ o₁ = π(S₀ᶜ)/π(S₀).
  - All p Gibbs coordinates *together* leave with probability ≤ o₁, and K_{G_j}(S₀, S₀ᶜ) = |o_j(S₀) − 1{j∈S₀}|.
  - One round leaves with probability ≤ (B+3)o₁ ≤ 19·o₁.
- **Theorem LT♯ (item b, Lemma LT corrected for the coded outputs).** For each island, all ε, η:
  - P(max_j|p̂_r(j) − 1{j∈S₀}| ≥ κ₀ + 2ε | 𝓒) ≤ δ/(εη) + 19o₁/ε + P(W_r < η | 𝓒), with κ₀ ≤ o₁ exactly attained;
  - the weighted form E[W_r‖p̂_r − 1_{S₀}‖_∞] ≤ g ≤ 21o₁;
  - endpoint, discovery, pooled pip_primary, MPM (strict ½ threshold) and HPM consequences.
  - Asymptotically, P-CONC (δ → 0, no rate) plus non-collapse NC_r gives consistency of pip_primary (sup-norm), MPM
    and HPM, for any N_e and any frozen schedule. The variant LT-e′ allows W_r → 0 slower than the posterior error.
  - **This fixes ADJ_opus Flaw 1.** The RB values are recorded mid-round; the common good/bad particle-round
    classification controls all coordinates at once, with no factor p and no posterior-size control.
  - **Flaw 2 (premise near-circular) is answered by labelling, not by removal.** NC_r is a computational premise:
    - it is discharged by Theorem C;
    - it is replaced by a premise without particle statistics in Theorem TR;
    - it is one-sidedly falsifiable from the ledger: Ẑ_r < η·Σ_top e^F ⇒ W_r < η;
    - no output certifies it;
    - whether it is necessary is **open**: the finite-n probes are illustrations only (LC1).
- **Theorem C (concentrated bridge, item c).** For any grid, any T and any N_e ≥ 1:
  - E|W_r − 1| ≤ β ≤ 2·max{δ, (1−δ)o₀} ≤ 2δ̄, and the same for the pooled Ẑ/Z. The proof telescopes the negative
    potential loss against the bridge identity (BT1 §1, re-derived).
  - Log-evidence tail: P(|log Ẑ − log Z| > u) ≤ β/(1 − e^{−u}).
  - E‖pip_primary − 1_{S₀}‖_∞ ≤ g + β/2 ≤ 22δ̄; P(MPM ≠ S₀) ≤ 44δ̄; bias |E p̂_r(j) − PIP_j| ≤ β/2.
  - Hence if 1_𝒜δ̄ → 0 (P-CONC + π₀(S₀) → 1), then Ẑ/Z → 1, log Ẑ − log Z → 0, and the PIPs, MPM and HPM are
    consistent, with O_P(r_n) rates when δ̄ = O_P(r_n). NC_r holds.
  - This improves the source's T²δ̄ (BLIND_fable Thm 4(b)) and my own locked Tδ̄.
  - The T-dependent bridge-occupation bound C-ii is kept separately.
  - Honest label: this is the regime where the start already concentrates on S₀.
- **Theorem TR (terminal repair; new, from the sharpness gate).**
  - Every φ = 1 round kernel is minorised by π/M, with M = max π/π₀.
  - For any bridge outcome, unweighted: E‖p̂_r − 1_{S₀}‖_∞ ≤ g + (1 − 1/M)^L, and P(MPM ≠ S₀) ≤ 2(g + e_L).
  - So P-CONC plus L/M → ∞ (localised to 𝒜) gives PIP, MPM and HPM consistency with **no condition on Ẑ, the bridge or
    N_e**. In production this reads M = o_P(log n) on 𝒜.
  - Label: a global-overlap condition relative to the executed burn-in, involving no particle statistic.
  - It is not implied by π₀(S₀) → 1 (three-state example), and C and TR are not nested.

## 3. Status per clause

| Clause | Status (verbatim scale) | Evidence |
|---|---|---|
| CC | PROVED (code-checked by lead); LC1 VERIFIED WITH AMENDMENTS, fixed | `lemmas/CC_code_check.md`; `reviews/LC1_*` |
| PC | PROVED; LC1 VERIFIED | `lemmas/PC_completed.md` |
| MR | PROVED; LC1 VERIFIED WITH AMENDMENTS, fixed | `lemmas/MR_identities.md` |
| ST | PROVED; LC1 VERIFIED WITH AMENDMENTS, fixed | `lemmas/ST_stay.md` |
| D (incl. MAP premise) | PROVED; LC1 VERIFIED WITH AMENDMENTS, LC2 VERIFIED, fixed | `lemmas/D_theorem.md` |
| LT♯ a–e, b′, e′ | PROVED; LC1 VERIFIED (a–e), LC2 VERIFIED WITH AMENDMENTS (b′, e′), fixed | `lemmas/LT_theorem.md` |
| LT♯ f (necessity of NC) | **OPEN** (downgraded to illustrations after LC1 issue 3) | same, Step 6 |
| C (T-free) | PROVED; LC1 checked v1 (stopped sum) VERIFIED; LC2 checked v2 Steps 4–6 VERIFIED WITH AMENDMENTS, fixed | `lemmas/C_theorem.md` |
| TR | PROVED; LC2 VERIFIED WITH AMENDMENTS, fixed | `lemmas/TR_theorem.md` |
| Whole package | mid-point **CONTINUE** (MP1); **sweep and council not run** | `reviews/MP1_*` |

Inherited statuses, verbatim:
- W1-N1: "PROVED-CHECKED".
- START/KERNEL: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT".
- T12: "proved (...); not adopted"; the theory card says "PROVED-LOCKED".
- P-CONC: from W3-POST Theorem 1 (Rate), at that ticket's status.

## 4. Review trail

- **Statement lock SL1** (Codex gpt-6.1-sol, high): LOCK WITH CHANGES. Five required changes, all applied
  (`reviews/SL1_*`): localisation; the admissible-h class; Ẑ_r vs `log_Z_r`; component vs production; statuses + Lemma PC.
- **Sharpness gate:**
  - `ASSUMPTION_MAP.md`;
  - boundary numerics (`numerics/RESULTS_v1.txt`, `RESULTS_v1_sec4b.txt`);
  - "better theorem" review BT1 (gpt-6-astra, high): T-free C, terminal repair, MAP premise, uniform RB bound. Adopted
    after re-derivation (`reviews/BT1_*`). Not adopted: the Gibbs-neighbour discovery bound, the secondary estimator,
    and ST constant 18.
- **Lemma checks:**
  - LC1 (Sol high): no CRITICAL; 2 MAJOR (the v3_frozen N/L interface claim; LT-f's asymptotic sharpness) + 5 MINOR,
    all fixed.
  - LC2 (Sol high, the new material): VERIFIED WITH AMENDMENTS; 1 MAJOR (same as MP1 #1) + 4 MINOR, all fixed.
  - The reviewers ran their own exact checks: 12 targets, all orders up to 720, 60,000 islands. Zero violations.
- **Falsification numerics** (`numerics/README.md`): 0 inequality violations across v1–v3; identity max |z| = 2.70.
  Coverage: regression-realisable targets with the block start, pointwise checks of the stopped sum and C-i, the
  telescoping budget (nearly attained), β, TR minorization by exact kernel products, and the D equality (z ≤ 1.07).
- **Mid-point MP1** (gpt-6-astra high, statement + proofs only): **CONTINUE**. 1 MEDIUM (P-OVL∞ forced P(𝒜) → 1) + 2 LOW,
  all fixed.
- **Citation check:** `reviews/CITECHECK.txt`, 82 path:line citations, 0 missing or out of range; the cited lines were
  read against the claims.
- **Sweep SW1:** cancelled externally, no output. **Council:** not run.
- **Models used:** Codex gpt-6.1-sol high ×4 (SL1, LC1, LC2, SW1-cancelled); gpt-6-astra high ×2 (BT1, MP1). No Claude
  subagents. No effort above high.

## 5. Assumptions (ids), implications, sharpness record (for INFRA)

**Inherited premises:** EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT (from W1-N1); IND-T (only D-ii).

**Interfaces consumed:**
- P-CONC: δ → 0.
- P-START: π₀(S₀) → 1, no rate.
- P-MAP: S† = S₀.
- P-OVL: D_rπ₀(S₀) → ∞.
- P-OVL∞: L/M → ∞ (localised).
- NC_r: lower tail of W_r (computational).

**Implications:**
- P-CONC ⇒ P-MAP.
- P-CONC + P-START ⇒ NC_r (Theorem C).
- PROGRAM item 2's rate π₀(S₀) ≥ 1 − n^{−c} ⇒ P-START.
- W3-POST (Rate) ⇒ P-CONC, with an O_P(r_n) rate.
- Production budgets ⇒ D_r ≥ max(n, p)(L+6).
- Theorem C implies the v2 claims; LT♯ + C ⇒ the coded-output consistency.

**Sharpness record:**

| Item | Record |
|---|---|
| D | Equality for the draw mechanism (sharp); only sufficient for the method. |
| κ₀ term | Attained exactly. |
| Linear δ̄ in C | Natural at N_e = 1. |
| T factor in C | Removed. |
| NC_r | Necessity open; TR complements it. |
| P-OVL∞ | Sufficient, not necessary (local moves repair in the "near" probe). |
| B ≤ 16 constant | Loose but harmless. |

## 6. Open items and recommended next steps

1. **Run SW1 and the council.** SW1: the exhaustive sweep, same brief, Codex Sol high. Council: gpt-6-astra high +
   Claude Opus 5.5 high on claudeAgent. Then the dispositions.
2. **Asymptotic witnesses for LT-f.** One triangular array with P-CONC where NC fails and the outputs fail; one where NC
   fails and the outputs succeed. Optional.
3. **Primitive conditions** on (X, θ*) for P-START (item 2), and possibly for P-OVL∞ (M = o(log n)). The full
   GUARD-W audit stays out of scope.
4. **Optional strengthenings recorded in BT1:**
   - a Gibbs/swap-neighbour discovery bound beating draws alone (BT1 §3.2);
   - the evidence-pooled secondary PIP estimator (not a reported field on main);
   - ADJ_opus's "D_n·π₀(S₀) → 0 on NEG" to make the limits section about the full method.

## 7. Files (all under `Theory_work/Wave3/W3-SAMP/`)

- **Top level:** `STATEMENT.md` (v3), `PLAN.md`, `LOG.md`, `CHECKPOINT.md`, `ASSUMPTION_MAP.md`, `REPORT.md`,
  `citecheck.py`.
- **Proofs:** `lemmas/` — `CC_code_check.md`, `PC_completed.md`, `MR_identities.md`, `ST_stay.md`, `D_theorem.md`,
  `LT_theorem.md`, `C_theorem.md`, `TR_theorem.md`.
- **Numerics:** `numerics/` — `README.md`, `samp_sim.py`, `run_checks.py`, `sec4.py`, `run_checks_v2.py`,
  `run_checks_v2b.py`, `run_checks_v3.py`, `RESULTS_v1.txt`, `RESULTS_v1_sec4b.txt`, `RESULTS_v2.txt`, `RESULTS_v3.txt`.
- **Reviews:** `reviews/` — `SL1_statement_lock_sol.md` + disposition, `BT1_better_theorem_astra.md` + disposition,
  `LC1_lemma_check_sol.md` + disposition, `LC2_lemma_check_sol.md` + disposition, `MP1_midpoint_astra.md` + disposition,
  `CITECHECK.txt`.
- Nothing outside the folder was modified, and no git state was changed.
