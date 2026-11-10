# W3-SAMP · REPORT to Theory HQ (PROGRAM item 4: sampler outputs as coded, honestly labelled)

**Flags at the top.**
1. **Statement v3** strengthens the locked v2 through the sharpness gate (BT1). HQ accepted it on 2026-11-09.
2. **Code finding:** main (4676af6) computes **no plain (endpoint) PIP**. The only PIP it reports is the Rao–Blackwell
   PIP, recorded before each Gibbs draw. W1-N1's `pip_plain` identification applies only to the frozen v2.2.1 core.
3. **P-START is a named input** (π₀(S₀) → 1 on 𝒜, no rate needed here). The separate item-2 ticket will supply it.
4. **Process incidents**, both disclosed in LOG.md:
   - The first SW1 run was cancelled by a T3 server restart and rerun.
   - My LOG first carried estimated clock times that ran ahead of the real clock; I corrected them from file times.
   - I ran `git rm --cached` once while removing `numerics/sec4.py`, assuming the folder was untracked. It was tracked
     (HQ commit 2ac3896), so a deletion was staged. I undid it at once with `git restore --staged` on that one path. The
     index now holds nothing staged; the working-tree deletion of `sec4.py` is intended (it is superseded).

## 1. RESULT

**PROVED-CHECKED.** All of the following hold for every result in the package:
- a proof file exists;
- the statement was locked (SL1);
- the sharpness gate ran (ASSUMPTION_MAP + boundary numerics + the better-theorem review BT1);
- cross-family lemma checks were done (LC1, LC2, Codex Sol high);
- the independent mid-point said CONTINUE (MP1, gpt-6-astra high);
- every item of the exhaustive sweep (SW1, 28 items) was fixed;
- the citation check passed (85/85 in range; semantics checked by hand);
- the **council passed in round 1**: gpt-6-astra (high) **9.1**, Claude Opus 5.5 (high, claudeAgent) **8.8**, all six
  gates PASS on both seats, nothing blocking.

The checked status attaches to the claims as stated. The claims are **conditional** on the named interfaces. One
labelled sub-question, whether NC_r is necessary, is reported as OPEN; nothing is claimed about it.

## 2. The statement as proved

File: `STATEMENT.md` (v3). It is about the method as coded on main and is design-agnostic.

Two conventions run through every claim:
- Finite-sample claims are given the data and the calibration record 𝓒, on 𝒜, in W1-N1's localised form. In code terms,
  𝒜 = {SMC branch and calibration status "ok", including the tier-1 fallback}.
- Asymptotic claims are under the joint law, always intersected with 𝒜 (potential quantities) or with
  {completed} ⊆ 𝒜 (reported outputs). P(𝒜) → 1 is never assumed.

Results:

- **Lemma CC (code facts).**
  - Every π₀ draw is scored and offered to the HPM ledger before its accept decision. This covers the initial draws and
    the one independence proposal per particle per round, accepted or rejected.
  - Each island makes exactly D_r = N_e(1+T+L+4) draws.
  - The reported HPM is the best model, under the coded strict order, of everything the final run's ledger was offered.
  - pip_primary is the equal-weight mean of the island RB PIPs; MPM = {pip_primary > ½}; log_Z = log of the mean Ẑ_r.
  - In production, T ≤ 4·max(1000, ⌈log₂(n+p+1)⌉²) and B ≤ 16.
  - Every sampler function an island can reach is unchanged from N1's code of record. The differences are the removed
    plain-PIP writes, plus the LS0 start-mode code and event labels outside the island.
- **Lemma PC.** On completed runs, each island's records and its evaluated-model set equal those of the uninterrupted
  run. The reported HPM is the maximum of the whole ledger: islands, tables, inherited models, final search and LS0.
- **Theorem D (draw discovery, item d).**
  - The probability that no draw of an island equals S₀ is exactly (1 − π₀(S₀))^{D_r}. Under IND-T the exponent is 4D_r.
  - P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜(1 − π₀(S₀))^{D_r}], where S† is the exact HPM over Ω.
  - Production: max(n, p)·log₂(n+1)·π₀(S₀) → ∞ suffices, with no condition on mixing, the bridge or Ẑ.
- **Lemma MR.** T12's identities (i.a)–(i.c) and (ii) hold given 𝓒, for bridge stages, terminal endpoints and the
  pre-step states inside measured rounds. In particular E[W_r p̂_r(j) | 𝓒] = PIP_j for the coded RB recording. This is
  the "mid-round extension" that ADJ_opus called unproved.
- **Lemma ST.**
  - Any π-invariant kernel leaves S₀ with probability ≤ o₁.
  - All Gibbs coordinates together leave S₀ with probability ≤ o₁.
  - One round leaves S₀ with probability ≤ (B+3)o₁ ≤ 19o₁.
- **Theorem LT♯ (item b, Lemma LT corrected for the coded outputs).**
  - Finite-sample bound: P(max_j|p̂_r(j) − 1{j∈S₀}| ≥ κ₀ + 2ε) ≤ δ/(εη) + λ₀/ε + P(W_r < η). Here κ₀ ≤ o₁ is attained
    exactly, and λ₀ ≤ 19o₁.
  - Weighted form: E[W_r‖p̂_r − 1_{S₀}‖_∞] ≤ g ≤ 21o₁.
  - Consequences for endpoints, discovery, pooled pip_primary, MPM (strict ½ threshold) and the HPM.
  - Asymptotically: posterior concentration (no rate) plus the non-collapse premise NC_r gives consistency of the coded
    PIPs (sup-norm), MPM and HPM, for any N_e and any schedule. A vanishing-threshold variant is LT-e′.
  - This fixes ADJ_opus Flaw 1 (RB values recorded mid-round, no factor p, no posterior-size control).
  - Flaw 2 (the premise looks circular) is answered by labelling, not by removal. NC_r is computational:
    - Theorem C discharges it;
    - Theorem TR replaces it with a premise that involves no particle statistic;
    - an observable condition certifies the finite-run event {W_r < η};
    - no output certifies W_r ≥ η unless the store holds all of Ω;
    - whether NC_r is necessary is **open**.
- **Theorem C (concentrated bridge, item c).**
  - For any grid, any T and any N_e ≥ 1: E|W_r − 1| ≤ β ≤ 2max{δ, (1−δ)o₀} ≤ 2δ̄, by telescoping (T-free). The same
    bound holds for the pooled Ẑ/Z.
  - Log-evidence tail: P(|log Ẑ − log Z| > u) ≤ β/(1 − e^{−u}).
  - E‖pip_primary − 1_{S₀}‖_∞ ≤ 22δ̄; P(MPM ≠ S₀) ≤ 44δ̄; bias |E p̂_r(j) − PIP_j| ≤ β/2.
  - So 1_𝒜δ̄ → 0, i.e. posterior concentration plus P-START, gives Ẑ/Z → 1 and consistency of the PIPs, MPM and HPM.
    It gives O_P(r_n) rates when δ̄ = O_P(r_n), and NC_r holds.
  - This improves the source's T²δ̄ condition.
  - Label: the regime where the start already concentrates on S₀.
- **Theorem TR (terminal repair, from BT1).**
  - Every φ = 1 round kernel is minorised by π/M, with M = max π/π₀.
  - For any island's bridge outcome: E‖p̂_r − 1_{S₀}‖_∞ ≤ g + (1 − 1/M)^L, and P(MPM ≠ S₀) ≤ 2(g + e_L).
  - Posterior concentration plus P-OVL∞ (L/M → ∞ on 𝒜) gives consistency with no condition on Ẑ, the bridge or N_e.
    In production this reads M = o_P(log n) on 𝒜.
  - Label: a global-overlap condition relative to the executed burn-in, not certified by any output. For abstract
    targets it is not nested with C's condition in either direction; whether coded targets separate the two is open.

## 3. Status per clause

| Clause | Status | Evidence |
|---|---|---|
| CC | CODE-CHECKED (lead; SL1, LC1, SW1, both council seats) | `lemmas/CC_code_check.md` |
| PC, MR, ST, D, LT♯ (a–e, b′, e′), C, TR | PROVED-CHECKED | `lemmas/*.md`; `reviews/LC1_*`, `LC2_*`, `MP1_*`, `SW1_*`, `C1_*` |
| LT♯-f (is NC_r necessary?) | OPEN; nothing claimed (finite-target illustrations only) | `LT_theorem.md` Step 6; `ASSUMPTION_MAP.md` |

Inherited statuses, verbatim:
- W1-N1: "PROVED-CHECKED".
- START/KERNEL: "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT".
- T12: "proved (...); not adopted"; the theory card says "PROVED-LOCKED".
- P-CONC: from W3-POST Theorem 1 (Rate), at that ticket's status.

## 4. Review trail

- **SL1** (statement lock, Sol high): LOCK WITH CHANGES; all 5 required changes applied.
- **Sharpness gate:** ASSUMPTION_MAP, boundary numerics, and **BT1** (Astra high). From BT1 I adopted, after
  re-deriving each: the T-free C, TR, the MAP premise, and the uniform RB bound. HQ accepted v3.
- **LC1** (Sol high): no CRITICAL; 2 MAJOR + 5 MINOR, all fixed.
- **LC2** (Sol high): VERIFIED WITH AMENDMENTS; all fixed.
- **MP1** (Astra high): **CONTINUE**; 1 MEDIUM + 2 LOW, all fixed.
- **SW1** (Sol high; rerun after the restart): 0 CRITICAL / 4 MAJOR / 16 MINOR / 8 EXPOSITION. All 28 fixed: the
  HPM/PC scope; the abstract-example label; numerics provenance with a hash manifest; finite-target labels; non-vacuous
  LT checks (v4); a fixed-N T sweep; the honest citecheck; and others.
- **Council C1:** gpt-6-astra **9.1**, Claude Opus 5.5 **8.8**; all gates PASS; passed in round 1. 11 non-blocking items
  applied (`reviews/C1_disposition.md`).
- **Numerics:** falsification attempts with no violation detected in v1–v4. The largest identity |z| is 2.70.
  - 18 non-vacuous LT cells.
  - The telescoping budget and β, at fixed and varying N.
  - TR minorization: exact over 200 random orders.
  - The D equality: z ≤ 1.07.
  - Independent checks by the reviewers: 60,000 islands (LC1); all orders up to 720 on 12 targets (LC2); 300 targets
    plus 4,800 kernels (Astra seat); 40 cells (Opus seat). Zero violations in all of them.
- **Citations:** 85/85 in range.
- **Models used:** Codex gpt-6.1-sol high ×5 (SL1, LC1, LC2, SW1 cancelled, SW1); gpt-6-astra high ×3 (BT1, MP1, council);
  Claude Opus 5.5 high on claudeAgent ×1 (council). Nothing above high effort.

## 5. Assumptions (ids), implications, sharpness record (for INFRA)

**Inherited premises:** EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT; IND-T (D-ii only).

**Interfaces consumed:**
- P-CONC: δ → 0.
- P-START: 1_𝒜o₀ → 0, no rate; supplied by the item-2 ticket.
- P-MAP: S† = S₀.
- P-OVL: Q_D = D_rπ₀(S₀) on 𝒜, ∞ off 𝒜, and Q_D → ∞.
- P-OVL∞: P(𝒜 ∩ {L/M ≤ c}) → 0.
- NC_r: computational.

**Implications:**
- P-CONC ⇒ P-MAP.
- 1_𝒜o₁ → 0 together with P-START ⇒ NC_r (Theorem C).
- The item-2 rate ⇒ P-START.
- W3-POST (Rate) ⇒ P-CONC with o₁ = O_P(r_n).
- Production budgets ⇒ D_r ≥ max(2500, n, p)(L+6) and T = O(log²(n+p)).
- v3 ⇒ every v2 claim.

**Sharpness record:**

| Item | Record |
|---|---|
| D | Exact for the draw mechanism; only sufficient for the method. |
| κ₀ term | Attained exactly on a path that stays at S₀ throughout. |
| T factor in C | Removed. |
| Linear δ̄ in C | Possible; no lower-bound family claimed. |
| Is NC_r necessary? | Open. |
| TR premise | Sufficient, not necessary (repair outside TR's regime is observed). |
| Constant B + 3 | Loose but harmless. |

## 6. Open items and recommended next steps

1. Item-2 ticket: supply P-START, and the primitive conditions behind it.
2. Optional, not requested: asymptotic witnesses for whether NC_r is necessary; whether coded regression targets
   separate C's and TR's conditions; primitive conditions for M = o(log n).
3. Deferred by HQ: the BT1 strengthenings (neighbour-scoring discovery bound, pooled secondary estimator).
4. For the paper:
   - present LT♯ as the transfer interface;
   - present C and TR as two sufficient, honestly labelled discharges;
   - present D as the discovery mechanism that needs no mixing;
   - say clearly that main reports only RB PIPs.

## 7. Files (all under `Theory_work/Wave3/W3-SAMP/`)

- **Top level:** `STATEMENT.md` (v3), `PLAN.md`, `LOG.md`, `CHECKPOINT.md` (superseded), `ASSUMPTION_MAP.md`,
  `REPORT.md`, `citecheck.py`.
- **Proofs:** `lemmas/` — `CC_code_check.md`, `PC_completed.md`, `MR_identities.md`, `ST_stay.md`, `D_theorem.md`,
  `LT_theorem.md`, `C_theorem.md`, `TR_theorem.md`.
- **Numerics:** `numerics/` — `README.md` (invocations and SHA-256 manifest), `samp_sim.py`, `run_checks.py`,
  `run_checks_v2.py`, `run_checks_v2b.py`, `run_checks_v3.py`, `run_checks_v4.py`, `RESULTS_v1.txt`,
  `RESULTS_v1_sec4b.txt`, `RESULTS_v2.txt`, `RESULTS_v3.txt`, `RESULTS_v4.txt`. `sec4.py` was removed; it is superseded
  by `run_checks.py --sections`.
- **Reviews:** `reviews/` — SL1, BT1, LC1, LC2, MP1, SW1 and C1 (astra, opus), each with its disposition, plus
  `CITECHECK.txt`.
- **Git:** nothing outside the folder was modified. The index has no staged changes (the one accidental staging was
  undone). HQ commits.
