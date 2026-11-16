# W3-DIST — disposition of the diff checks D1 and D2 (Sol) and of L7's findings

Written by the lead, 2026-11-16 00:11 CT. Review files: `reviews/D1_sol_diff.md`, `reviews/D2_sol_NEC_diff.md`,
`reviews/L7_sol_NEC.md`. Re-check of everything applied here: D3 (`reviews/BRIEF_D3_sol_diff.md`, `reviews/DIFFS_D3.patch`).

## D1 — what was confirmed
- **The repair of L6-01 is VERIFIED (Part A items 1–7) and the tag "EQUAL on TC3" is CONFIRMED by the reviewer.**
  M₀ ≤ 16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ*²); the radius constant C depends on (A, σ*², M, M′) only. No new condition:
  e^{s₀}q ≤ n^{−1/8} < ½ follows from the existing threshold conditions (a), (d). Reviewer's reading, adopted: the rate is
  read with A fixed (C depends on A) and s₀^r fixed (n₀ depends on it), as (RD) stipulates.
- Lemma X, Lemma X′ (`lemmas/X.md` v0.4), DIST-1, DIST-2 (`lemmas/DIST12.md` v0.2): VERIFIED as they stand.
- Part B: `S.md`, `COR_C.md`, `B3.md`, `ASSEMBLY.md` VERIFIED with their amendments.
- Part C: 15 changelog rows CONFIRMED; `TARGET.md` §6 identical to STATEMENT §1R; TC1–TC9 still implied, no protected
  weakening.

## D1 — findings (4 MINOR, 1 NIT; all ACCEPTED)
| id | finding | action |
|---|---|---|
| D1-01 | `P6_DISTC.md` A-10: the finiteness argument paired the N-dimensional likelihood with the shape 0.01 of the n-dimensional working model | A-10 rewritten with the reviewer's repair: contrast model, shape 0.51, rate 0.01·s_y², factor from T01(i). Positivity and everything downstream unchanged |
| D1-02 | STATEMENT DIST-C (C-i): "on the complementary success event" read literally covers stopped runs and lists of small posterior probability | replaced by the explicit event {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}} (the form proved; SCR-4). Tag: EQUAL on TC8 (TC8 already fixes "jointly with {completed} and under its named premise"); the reviewer of D3 confirms or contests the tag. **If contested as WEAKER on TC8: early checkpoint** |
| D1-03 | the last bridge bullet's range M ≤ √n → M ≤ √n/log n was not in the changelog | recorded in the bridges row as WEAKER, non-target |
| D1-04 | three v1.4 rows had one tag for changes of mixed direction | rows split: Corollary C = EQUAL + **STRONGER** (the true model is the reported most probable model); Remarks = EQUAL + WEAKER (non-target: Remark (1) needs the window at its level); bridges = STRONGER (B2 range) + WEAKER (non-target) |
| D1-05 | the statement patch file was a deletion snapshot | regenerated with `diff -u` (the root clone is on main, where the ticket files are untracked, so `git diff <commit>` showed a deletion) |

**STRONGER beyond CP1 (PROTOCOL_v4 §4.2).** The HPM conclusion of Corollary C (companion result, TC10) was reported to
the manager; **HQ gave its go on 2026-11-16**: it stays in for the sweep and the council, the sweep brief and both
council briefs name it as a point to check (done), and its headline status goes through the H5 card at CP3.

**WEAKER rows, non-target, for CP3:** Remark (1) of §1R (window premise at the level of the radius); bridge remarks
(B0 domain, B3 b_n > 0, withdrawn uncapped window claims, range of the last bridge bullet).

## L7 and D2 — Proposition NEC
- L7: Proposition NEC and Corollary NEC VERIFIED. Three presentation findings on v0.1 (L7-01, L7-03 MINOR; L7-02 NIT),
  applied in v0.2; the same reviewer re-read v0.2: VERIFIED, no outstanding finding. (I amended the file while the
  reviewer was still in its final pass, having taken its written file for a finished review; recorded in LOG.)
- D2 (second reading of v0.2): L7-01, L7-02 RESOLVED; **D2-01 (MINOR)**: the numerical remark §8(d) still asserted
  "slightly smaller" full-posterior masses and the full-posterior event. ACCEPTED: reworded with the reviewer's text
  (v0.3). The remark is evidence, not proof; the Proposition, the Corollary and their constants are unchanged.
- Proposition NEC touches no target clause (the design violates (ND); Lemma X, (1.1) and TC1–TC9 are untouched).
