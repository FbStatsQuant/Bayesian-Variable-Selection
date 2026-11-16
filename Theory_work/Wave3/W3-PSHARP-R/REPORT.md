# W3-PSHARP-R — REPORT (to the Theory Department / HQ)

Rider T12 (Tier B, NORMAL mode), delta over W3-PSHARP. This report restates nothing (PROTOCOL_v4 §3): it points to
`STATEMENT.md` v1.1 (locked) and to the proof files. Lead: Claude Opus 5.5 (effort high), Claude Third.

## 1. What is claimed
- `W3-PSHARP-R:AE` — Proposition A-E with Corollaries A1-E and A2-E: `STATEMENT.md:61-92`. Notation and changed hypotheses:
  `STATEMENT.md:39-57`. Proof: `lemmas/AE_expectation.md`.
- `W3-PSHARP-R:A2C` — Proposition A2C: `STATEMENT.md:94-100`. Proof: `lemmas/A2C_critical.md`.
- Corrected readings of the parent (not claims): `STATEMENT.md:102-119`. What is not claimed: `STATEMENT.md:121-129`.
- Implications to the parent and supersession: `STATEMENT.md:131-148` (supersession is HQ's decision, PROTOCOL_v4 H5).

## 2. Review trail (verbatim replies in `reviews/`)
| step | reviewer (mode) | brief | reply | disposition |
|---|---|---|---|---|
| statement lock L01 | Sol gpt-6.1-sol, high (NORMAL; fresh, blind) | `reviews/BRIEF_L01_sol.md` | `reviews/L01_statement_lock_sol.md` | `reviews/L01_disposition.md` |
| line check L02 (both lemmas) | Sol gpt-6.1-sol, high (NORMAL; fresh, blind) | `reviews/BRIEF_L02_sol.md` | `reviews/L02_line_check_sol.md` | `reviews/L02_disposition.md` |
| citation check | script | `citecheck.py` | `reviews/CITECHECK.txt` | — |
| council R1 | Sol seat + Opus seat | `reviews/BRIEF_R1_*.md` | `reviews/R1_council_*.md` | `reviews/R1_disposition.md` |
(Rows below L01 are filled as the steps complete; CHECKPOINT_3 carries the final state.)

## 3. Numerics
`numerics/ae_fixed_p.py` → `numerics/ae_fixed_p_out.txt` (N1; run `python3 ae_fixed_p.py 400000`, 18 s): cited in
`STATEMENT.md:122-123` and `TARGET.md` §3 as an observation only. N2 (p = n − 1) and N3 (A2C cap) were optional and were
not run (named, not needed by any claim).

## 4. Open items (named; no work in this ticket)
- O-R1 (HEURISTIC/OPEN): whether the constant of the expectation display is attained (no upper bound for E δ_n claimed;
  N1 suggests it is at fixed p).
- O-R2 (OPEN): A2C on the spherical witness (multi-step fit control).
- O-R3 (OPEN, parked by the BRIEF): dropping (G) under (W-sph); a coherence witness replacing exact orthogonality.
- O-R4 (OPEN, from the parent): the √(log n) factor **in probability** when log p = o(log n) (`STATEMENT.md:113-115`).
- A design-general √(log n) lower bound is not claimed anywhere here: on every design only order n^{−1/2} holds
  (`W3-PSHARP:B`@1.0.0); the √(log n) bounds are on the witness designs only (post-freeze rider POST2-R1).

## 5. Files
`STATEMENT.md`, `TARGET.md`, `PLAN.md`, `READER_DELTA.md`, `DEPS.tsv`, `LOG.md`, `lemmas/AE_expectation.md`,
`lemmas/A2C_critical.md`, `numerics/`, `reviews/`, `citecheck.py`, `CHECKPOINT_1.md`, (CP3) `CHECKPOINT_3.md`.

## 6. Registry blocks

```
REGISTRY
claim: W3-PSHARP-R:AE | kind: proposition | statement: STATEMENT.md:61-92 | premises: STATEMENT.md:39-57
name: Proposition A-E (expectation lower bound on witness designs for every null-block size; Corollaries A1-E, A2-E)
status: PROVED (by this seat, unchecked) | status_source: lemmas/AE_expectation.md:3
assumptions: A:GAUSS-NOISE ; A:ENERGY ; A:PSHARP-COEF ; A:PSHARP-WORTH-E (new | orthogonal null block, expectation form | A:PSHARP-WORTH and (log p)^2 = o(n) | STATEMENT.md:49-50 | shared no) ; A:PSHARP-WSPH-E (new | spherical null block, expectation form | null directions iid uniform on the unit sphere of 1-perp, independent of eps; (log p)^2 = o(n), (rank X_S0 + 1) log(pn) = o(n) | STATEMENT.md:52-57 | shared no)
conclusion: negative: E delta_n >= (1 - eps - L_n) L_n for n >= n0, L_n = (s0+1) [2N/(2p-1-s0)] sqrt(log(p sqrt(n)/(s0+1))/(pi n)), any null-block size N >= 1; all nulls, fixed s0, any p: liminf E delta_n / L_n >= 1; growing s0, all nulls, s0 <= p/2, any p: E delta_n = O(r_n) forces s0 = O(1) | rate: (s0+1) sqrt(log(p sqrt(n)/(s0+1))/(pi n)) (lower bound on E delta_n; constant sqrt((a+1/2)/pi) at p = n^a) | scope: witness designs only (orthogonal null block, or spherical null block with p >> n allowed); bounded p and bounded N included
depends_on: W3-PSHARP:S@proof:Lemma-V,S(4) ; W3-PSHARP:A@proof:A_log_factor.md:26-37,53-63,75-99 ; W3-PSHARP:B@stmt:B1
implies: W3-PSHARP:A (expectation display of Corollary A1 only, STATEMENT.md:142 of this ticket: under A1's hypotheses, 2N/(2p-1-s0) -> 1 and log(p sqrt(n)/(s0+1)) >= log p eventually)
sharpness: A:PSHARP-WORTH-E = ARTEFACT (evidence: TARGET.md:12) ; A:PSHARP-WSPH-E = ARTEFACT (evidence: TARGET.md:13)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better-proposal:f02(Theory_work/Wave3/API_AUDIT/sharp2/results/f02.md) ; better-disposition:adopted(TARGET.md)

REGISTRY
claim: W3-PSHARP-R:A2C | kind: proposition | statement: STATEMENT.md:94-100 | premises: STATEMENT.md:29-37
name: Proposition A2C (critical sparsity scale on the orthogonal witness: limsup pi(S0) <= exp(-lambda))
status: PROVED (by this seat, unchecked) | status_source: lemmas/A2C_critical.md:3
assumptions: A:GAUSS-NOISE ; A:ENERGY ; A:PSHARP-COEF ; A:PSHARP-WORTH
conclusion: negative: all nulls, p -> infinity, s0/p -> 0, Lambda_n -> lambda: P(pi(S0) <= exp(-lambda) + eta) -> 1 for every eta > 0, and limsup E pi(S0) <= exp(-lambda) | scope: orthogonal witness designs only
depends_on: W3-PSHARP:S@proof:S(1),S(2),S(3) ; W3-PSHARP:A@proof:A_log_factor.md:8-24,45-46,53-68,121
implies: W3-PSHARP:A (odds bound of Corollary A2 on the orthogonal witness when Lambda_n -> lambda in (0, infinity))
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better-proposal:f02(Theory_work/Wave3/API_AUDIT/sharp2/results/f02.md) ; better-disposition:adopted(TARGET.md)
```
